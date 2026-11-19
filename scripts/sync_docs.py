#!/usr/bin/env python3
"""上游同步调度器（fmt sync_docs.py 改造，PLAN §4.4）。

全量流程（--tag / --latest）：
  检测/校验最新稳定 tag → 浅克隆 → ./configure（不 make，仅取 config.texi）
  → 48 texi → 30 页语料全量转换 → source/ + .meta.json 侧车
  → 段落切分 + hash → .translation-state.json → 聚合锚点 → anchor_map.yml
  → 输出变更摘要 JSON。

增量（--since，M3）：diff since..tag → 仅转换变更页 + hash 迁移段落状态（骨架）。

语料映射（PLAN §3.1；48 texi → 30 页）：手册页 strip-all（DR-009）；外壳页
strip authors,config；内容页 keep；APIchanges 纯文本 → fenced 英文占位页
（fmt DR-014 口径，翻译豁免）。
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import re
import shutil
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import proc  # noqa: E402
import texi2md  # noqa: E402

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
log = logging.getLogger('sync_docs')

REPO_ROOT = Path(__file__).parent.parent.resolve()
SOURCE_DIR = REPO_ROOT / 'source'
CONFIG_DIR = REPO_ROOT / 'config'
STATE_FILE = REPO_ROOT / '.translation-state.json'
UPSTREAM_JSON = SOURCE_DIR / 'UPSTREAM.json'
ANCHOR_MAP = CONFIG_DIR / 'anchor_map.yml'
PROXY = 'http://192.168.33.1:10808'

UPSTREAM_REPO = 'https://github.com/FFmpeg/FFmpeg.git'
DOC_DIR = 'doc'
TAG_RE = re.compile(r'^n(\d+)\.(\d+)(?:\.(\d+))?$', re.ASCII)

# 语料映射（texi → source 相对路径）
# mode: manual=--strip-all（DR-009 独有内容）；shell=--strip authors.texi,config.texi；
# keep=保留 include 内容
CORPUS = [
    # 手册页（独有内容）
    ('ffmpeg.texi', 'manual/ffmpeg.md', 'manual'),
    ('ffplay.texi', 'manual/ffplay.md', 'manual'),
    ('ffprobe.texi', 'manual/ffprobe.md', 'manual'),
    # 组件外壳页
    ('ffmpeg-utils.texi', 'components/utils.md', 'shell'),
    ('ffmpeg-scaler.texi', 'components/scaler.md', 'shell'),
    ('ffmpeg-resampler.texi', 'components/resampler.md', 'shell'),
    ('ffmpeg-codecs.texi', 'components/codecs.md', 'shell'),
    ('ffmpeg-bitstream-filters.texi', 'components/bitstream-filters.md', 'shell'),
    ('ffmpeg-formats.texi', 'components/formats.md', 'shell'),
    ('ffmpeg-protocols.texi', 'components/protocols.md', 'shell'),
    ('ffmpeg-devices.texi', 'components/devices.md', 'shell'),
    # 滤镜整卷（DR-008 翻译单元=滤镜小节）
    ('filters.texi', 'components/filters.md', 'keep'),
    # 手册共享件独立页
    ('fftools-common-opts.texi', 'manual/common-options.md', 'keep'),
    # 库页
    ('libavutil.texi', 'libraries/libavutil.md', 'keep'),
    ('libavcodec.texi', 'libraries/libavcodec.md', 'keep'),
    ('libavformat.texi', 'libraries/libavformat.md', 'keep'),
    ('libavdevice.texi', 'libraries/libavdevice.md', 'keep'),
    ('libavfilter.texi', 'libraries/libavfilter.md', 'keep'),
    ('libswscale.texi', 'libraries/libswscale.md', 'keep'),
    ('libswresample.texi', 'libraries/libswresample.md', 'keep'),
    # General
    ('faq.texi', 'general/faq.md', 'keep'),
    ('general.texi', 'general/general.md', 'shell'),
    ('platform.texi', 'general/platform.md', 'keep'),
    ('developer.texi', 'general/developer.md', 'keep'),
    ('git-howto.texi', 'general/git-howto.md', 'keep'),
    ('fate.texi', 'general/fate.md', 'keep'),
    ('authors.texi', 'general/authors.md', 'keep'),
    # P2（官网未列但可构建）
    ('mailing-list-faq.texi', 'general/mailing-list-faq.md', 'keep'),
    ('nut.texi', 'general/nut.md', 'keep'),
    ('community.texi', 'general/community.md', 'keep'),
    ('drawvg-reference.texi', 'general/drawvg-reference.md', 'keep'),
]

# general.texi 外壳仅含 general_contents.texi，strip 名单与组件外壳相同
SHELL_STRIP = ('authors.texi', 'config.texi')

# 翻译豁免文件（fmt DR-014 口径）
EXCLUDED = {'general/APIchanges.md'}

APICHANGES_TEXI = 'APIchanges'
APICHANGES_OUT = 'general/APIchanges.md'


def compute_hash(content: str) -> str:
    return hashlib.sha256(content.encode('utf-8')).hexdigest()[:16]


# ============ tag 检测与上游获取（subprocess 一律经 proc.py） ============

def detect_latest_tag(repo_url: str) -> str:
    """ls-remote 枚举 tag → 正则过滤稳定版（nX.Y[.Z]，剔除 peeled ^{}）→ 版本序取最大。"""
    raw = proc.git_output(['ls-remote', '--tags', repo_url], timeout=180)
    tags = []
    for line in raw.splitlines():
        ref = line.split('\t')[-1]
        if ref.endswith('^{}'):
            continue
        name = ref.removeprefix('refs/tags/')
        if TAG_RE.match(name):
            tags.append(name)
    if not tags:
        raise RuntimeError('no stable tags found')
    tags.sort(key=lambda t: tuple(int(x or '0') for x in TAG_RE.match(t).groups()))
    return tags[-1]


def clone_tag(tag: str, dest: Path, repo_url: str) -> tuple:
    """浅克隆指定 tag（直连失败→代理重试一次，纪律要求），返回 (SHA, channel)。"""
    ok = proc.git_ok(['clone', '--depth', '1', '--branch', tag,
                      '--single-branch', repo_url, str(dest)], timeout=900)
    channel = 'direct'
    if not ok:
        log.info('direct clone failed, retry via proxy once')
        channel = 'proxy'
        ok = proc.git_ok(['-c', 'http.proxy=http://192.168.33.1:10808',
                          '-c', 'https.proxy=http://192.168.33.1:10808',
                          'clone', '--depth', '1', '--branch', tag,
                          '--single-branch', repo_url, str(dest)], timeout=900)
    if not ok:
        raise RuntimeError('clone+configure+convert failed on both channels')
    return proc.head_sha(dest), channel


def run_configure(clone_dir: Path) -> None:
    """./configure（不 make）：仅生成 doc/config.texi；--disable-x86asm 免 nasm。"""
    ok = proc.run_configure(clone_dir)
    if not (clone_dir / DOC_DIR / 'config.texi').exists():
        raise RuntimeError('configure did not produce doc/config.texi')
    if not ok:
        log.warning('configure nonzero rc but config.texi present')


def verify_tag_date(clone_dir: Path, tag: str) -> str:
    """annotated tag 日期实测：cat-file tag 原始输出的 tagger 时间戳。"""
    raw = proc.git_output(['cat-file', 'tag', tag], cwd=clone_dir, timeout=60)
    for line in raw.splitlines():
        if line.startswith('tagger '):
            m = re.search(r'(\d{9,11}) ', line)
            if m:
                ts = int(m.group(1))
                return time.strftime('%Y-%m-%d %H:%M:%S %z', time.gmtime(ts))
    return ''


# ============ 段落切分与翻译状态（fmt segment_md 改造：--wrap=none 单行段） ============

HEADING_LINE = re.compile(r'^#{1,6} ')
LIST_ITEM = re.compile(r'^\s*(?:[-*+] |\d{1,2}\. )')
TABLE_LINE = re.compile(r'^\|')
FENCE = re.compile(r'^```')


def segment_md(content: str, fname: str) -> list:
    """md → 段落列表（fmt 同款结构；护栏防死循环，fmt DR-011 教训）。

    单行段（--wrap=none）：paragraph/code_block/table/heading；段落 hash 为
    增量迁移的键。filters 卷按滤镜小节二次归属（metadata.section=滤镜名）。"""
    segs = []
    lines = content.split('\n')
    i = 0
    para_idx = 0
    cur_sec = ''
    cur_filter = ''
    n = len(lines)
    while i < n:
        line = lines[i]
        st = line.strip()
        if FENCE.match(st):
            start = i
            i += 1
            while i < n and not FENCE.match(lines[i].strip()):
                i += 1
            if i < n:
                i += 1
            code = '\n'.join(lines[start:i])
            segs.append(seg_dict(fname, 'code_block', code, start + 1, i,
                                 cur_sec, cur_filter, para_idx))
            para_idx += 1
            continue
        if st.startswith('|') and '|' in st[1:]:
            start = i
            while i < n and lines[i].strip().startswith('|'):
                i += 1
            tbl = '\n'.join(lines[start:i])
            segs.append(seg_dict(fname, 'table', tbl, start + 1, i,
                                 cur_sec, cur_filter, para_idx))
            para_idx += 1
            continue
        if HEADING_LINE.match(st):
            level = len(st) - len(st.lstrip('#'))
            title = st.lstrip('#').strip()
            segs.append(seg_dict(fname, 'heading', line, i + 1, i + 1,
                                 cur_sec, cur_filter, para_idx, level, title))
            cur_sec = title
            if level == 1 and st.count('#') == 1:
                pass
            para_idx = 0
            i += 1
            continue
        if st:
            start = i
            paras = []
            while i < n and lines[i].strip() != '':
                ls = lines[i].strip()
                if i > start and (HEADING_LINE.match(ls) or FENCE.match(ls)
                                  or (ls.startswith('|') and '|' in ls[1:])):
                    break
                paras.append(lines[i])
                i += 1
            p = '\n'.join(paras)
            segs.append(seg_dict(fname, 'paragraph', p, start + 1, i,
                                 cur_sec, cur_filter, para_idx))
            para_idx += 1
            if i == start:
                # 防死循环护栏（fmt DR-011：内层未推进时强制前进）
                i += 1
        else:
            i += 1
    return segs


def seg_dict(fname, stype, content, l0, l1, section, filter_name, idx,
            level=None, title=None) -> dict:
    d = {
        'id': fname + '-p' + str(idx),
        'type': stype,
        'content': content,
        'hash': compute_hash(content),
        'line_start': l0,
        'line_end': l1,
        'metadata': {'section': section},
    }
    if filter_name:
        d['metadata']['filter'] = filter_name
    if level is not None:
        d['metadata']['level'] = level
        d['metadata']['title'] = title
    return d


class FileState:
    def __init__(self, file_path, upstream_hash, upstream_commit, segments,
                 excluded=False):
        self.file_path = file_path
        self.upstream_hash = upstream_hash
        self.upstream_commit = upstream_commit
        self.segments = segments
        self.excluded = excluded

    def to_dict(self):
        return {'file_path': self.file_path, 'upstream_hash': self.upstream_hash,
                'upstream_commit': self.upstream_commit,
                'segments': self.segments, 'excluded': self.excluded}


# ============ 语料转换调度 ============

def convert_corpus(srcdir: Path, workdir: Path, out_root: Path) -> dict:
    """48 texi → 30 页全量转换。返回 {"pages": [...], "anchors_total": n}。

    产物写 out_root（成功后由调用方整体落位 source/）；meta 侧车与 md 同目录。"""
    pages = []
    anchors_total = 0
    for texi_name, out_rel, mode in CORPUS:
        texi_path = srcdir / texi_name
        if not texi_path.exists():
            raise FileNotFoundError('corpus texi missing: ' + texi_name)
        texi_text = texi_path.read_text(encoding='utf-8', errors='replace')
        strip_all = mode == 'manual'
        strip_names = set(SHELL_STRIP) if mode == 'shell' else set()
        result = texi2md.convert(texi_text, srcdir, strip_all, strip_names,
                                 workdir / 'conv')
        out_path = out_root / out_rel
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(result['md'], encoding='utf-8')
        meta_path = out_path.with_name(out_path.name + '.meta.json')
        meta_path.write_text(json.dumps(result['meta'], ensure_ascii=False, indent=2),
                             encoding='utf-8')
        pages.append({'texi': texi_name, 'out': out_rel, 'mode': mode,
                      'bytes': len(result['md'].encode('utf-8'))})
        anchors_total += len(result['meta'].get('anchors', []))
        log.info('converted %s -> %s', texi_name, out_rel)
    return {'pages': pages, 'anchors_total': anchors_total}


def convert_apichanges(srcdir: Path, out_root: Path) -> dict:
    """doc/APIchanges（纯文本 changelog）→ fenced 英文占位页（fmt DR-014 口径）。"""
    txt_path = srcdir / APICHANGES_TEXI
    body = ''
    if txt_path.exists():
        body = txt_path.read_text(encoding='utf-8', errors='replace')
    header = ('<!-- 英文原文占位页（不翻译）：源 doc/APIchanges，'
              '见 LICENSE_TRANSLATION.md 与 fmt DR-014 口径 -->\n\n'
              '# FFmpeg APIchanges\n\n'
              '> 此页为官方 API 变更日志英文原文（不翻译）。基线：n' + '9.0.2。\n\n')
    md = header + '```text\n' + body + '\n```\n'
    out_path = out_root / APICHANGES_OUT
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding='utf-8')
    meta = {'title': 'FFmpeg APIchanges (English)', 'anchors': [],
            'docbook_counts': None, 'excluded': True}
    out_path.with_name(out_path.name + '.meta.json').write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')
    return {'out': APICHANGES_OUT, 'bytes': len(md.encode('utf-8'))}


def mkdocs_slug(title: str) -> str:
    """对齐 mkdocs toc.slugify（python-markdown）：小写、空格→'-'、
    剔除其余标点但保留 '-' 与 '_'（\\w 与 '-' 均在 mkdocs 保留字符集内）。

    与 normalize_anchor_id（官方 HTML 命名，_005f 编码）分工：
    本函数产出"我方站点锚点"，官方锚点兼容经 anchor_map id → mkdocs_slug 映射。"""
    out = []
    for ch in title:
        if ch.isalnum():
            out.append(ch.lower())
        elif ch in (' ', '-', '_'):
            out.append(ch if ch != ' ' else '-')
    return re.sub(r'-+', '-', ''.join(out)).strip('-') or 'section'


def build_anchor_map(pairs: dict, out_path: Path) -> int:
    """聚合各页 meta.anchors → anchor_map.yml（官方锚点 → 页面/标题 slug）。

    pairs: {页面相对路径: meta.json 路径}（与 validate_structure.load_corpus_map
    同源，测试可注入临时路径）。结构：pages → page → anchor_id → {title,
    level, slug}。"""
    import yaml
    amap: dict = {'pages': {}}
    pages_map = amap['pages']
    for page, meta_path in sorted(pairs.items()):
        meta = json.loads(Path(meta_path).read_text(encoding='utf-8'))
        entries: dict = {}
        for a in meta.get('anchors', []):
            aid = a.get('id')
            if not aid:
                continue
            entries[aid] = {'title': a.get('raw_title') or '',
                            'level': a.get('level', 0),
                            # slug=我方站点锚点（mkdocs 小写口径）；官方大小写/
                            # _005f 编码锚点作为 map 键由 fix_links 兜底映射
                            'slug': mkdocs_slug(a.get('raw_title') or '')}
        pages_map.setdefault(page, {}).update(entries)
    # anchor_map 为纯派生产物（构建期生成，PLAN §7.1），整体重写不做旧文件合并——
    # 合并会让过时 slug 回写覆盖（实测踩坑）
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(yaml.safe_dump(amap, allow_unicode=True,
                                       sort_keys=True), encoding='utf-8')
    return sum(len(v) for v in amap['pages'].values())


def full_sync(tag: str, repo_url: str, dry_run: bool) -> dict:
    """全量同步主流程（PLAN §4.4）。"""
    started = time.strftime('%Y-%m-%d %H:%M:%S')
    with tempfile.TemporaryDirectory(prefix='ffmpeg-sync-') as td:
        tmp = Path(td)
        clone_dir = tmp / 'src'
        log.info('cloning %s at %s', repo_url, tag)
        sha, channel = clone_tag(tag, clone_dir, repo_url)
        tag_date = verify_tag_date(clone_dir, tag)
        log.info('clone ok (%s), sha=%s, tag date=%s', channel, sha[:12], tag_date)
        run_configure(clone_dir)
        srcdir = clone_dir / DOC_DIR
        staging = tmp / 'source'
        if dry_run:
            staging = tmp / 'source-dryrun'
        conv = convert_corpus(srcdir, tmp, staging)
        apich = convert_apichanges(srcdir, staging)
        log.info('converted %d corpus pages + APIchanges', len(conv['pages']))

        if dry_run:
            return {'mode': 'full', 'tag': tag, 'commit': sha, 'channel': channel,
                    'tag_date': tag_date, 'dry_run': True,
                    'pages': len(conv['pages']),
                    'apichanges': apich['out']}

        # 落位 source/
        if SOURCE_DIR.exists():
            for p in sorted(SOURCE_DIR.rglob('*')):
                if p.is_file():
                    p.unlink()
        staging_root = tmp / 'source'
        for p in staging_root.rglob('*'):
            if p.is_file():
                rel = p.relative_to(staging_root)
                dest = SOURCE_DIR / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(p, dest)

        # UPSTREAM.json（工具版本锁定输入）
        tools = proc.tool_versions()
        upstream = {
            'tag': tag,
            'tag_date': tag_date,
            'commit': sha,
            'repo': repo_url,
            'channel': channel,
            'converted_at': started,
            'tools': tools,
            'pages': conv['pages'],
        }
        UPSTREAM_JSON.parent.mkdir(parents=True, exist_ok=True)
        UPSTREAM_JSON.write_text(json.dumps(upstream, ensure_ascii=False, indent=2),
                                 encoding='utf-8')

        # 段落切分与状态
        state = {'upstream_repo': repo_url, 'upstream_commit': sha,
                 'upstream_tag': tag, 'tag_date': tag_date,
                 'converted_at': started, 'files': {}}
        for page in conv['pages'] + [apich]:
            rel = page['out']
            md_path = SOURCE_DIR / rel
            content = md_path.read_text(encoding='utf-8')
            fname = Path(rel).name
            segs = segment_md(content, fname)
            excluded = rel in EXCLUDED
            for d in segs:
                d['status'] = 'skipped' if excluded else 'pending'
            state['files'][rel] = {
                'upstream_hash': compute_hash(content),
                'upstream_commit': sha,
                'excluded': excluded,
                'segments': segs,
            }
        STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2),
                              encoding='utf-8')

        # 锚点聚合
        meta_pairs = {}
        for meta_file in sorted(SOURCE_DIR.rglob('*.meta.json')):
            page = str(meta_file.relative_to(SOURCE_DIR))[:-len('.meta.json')]
            meta_pairs[page] = meta_file
        anchor_count = build_anchor_map(meta_pairs, ANCHOR_MAP)
        log.info('anchor_map entries: %d', anchor_count)

        total_segments = sum(len(f['segments']) for f in state['files'].values())
        return {'mode': 'full', 'tag': tag, 'commit': sha, 'channel': channel,
                'tag_date': tag_date, 'pages': len(conv['pages']) + 1,
                'anchors': anchor_count, 'segments': total_segments,
                'converted_at': started}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog='sync_docs.py', description='上游文档同步调度器')
    ap.add_argument('--tag', help='全量同步到指定 tag（如 n9.0.2）')
    ap.add_argument('--latest', action='store_true', help='检测最新稳定 tag 并全量同步')
    ap.add_argument('--detect-only', action='store_true', help='仅检测最新稳定 tag')
    ap.add_argument('--repo', default=UPSTREAM_REPO)
    ap.add_argument('--dry-run', action='store_true', help='只转换到临时目录不落盘')
    args = ap.parse_args(argv)

    if args.detect_only:
        print(json.dumps({'latest_stable_tag': detect_latest_tag(args.repo)},
                         ensure_ascii=False))
        return 0
    if not (args.tag or args.latest):
        ap.error('需指定 --tag / --latest / --detect-only 之一')

    tag = detect_latest_tag(args.repo) if args.latest else args.tag
    if args.tag and not TAG_RE.match(args.tag):
        ap.error('--tag 需为 nX.Y[.Z] 格式（如 n9.0.2）')
    res = full_sync(tag, args.repo, args.dry_run)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
