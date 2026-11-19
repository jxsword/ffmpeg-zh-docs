#!/usr/bin/env python3
"""filters 整卷拆页器（DR-008）：构建期按 @section <滤镜名> 拆分为每滤镜一页。

用法：
  python3 split_filters.py <volume.md> --out-dir zh/filters --manifest <manifest.json>

规则：
  - H1 章节（@chapter）：Audio/Video/Multimedia Filters → 对应分组目录
  - 章内每个 H2（@section）= 一个滤镜 → <group>/<滤镜名>.md（标题降一级）
  - 其余章节（Filtering Introduction / graph2dot / Timeline 等）→ overview.md
  - 内建校验（PLAN 质量层"拆分层"）：拆分页集合 == 整卷滤镜小节集合，无丢失/重复

翻译单元=滤镜小节：source 整卷存储、段落 hash 到滤镜级；本脚本对 source 与
zh 译文卷使用同一逻辑（构建 zh/filters 页面与校验拆分完备性）。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()

HEADING_RE = re.compile(r'^(#{1,6}) (.*)$')
CHAPTER_GROUP = [
    (re.compile(r'video', re.I), 'video'),
    (re.compile(r'audio', re.I), 'audio'),
    (re.compile(r'multimedia', re.I), 'multimedia'),
]
FILTER_HEADING_RE = re.compile(r'^## ([A-Za-z0-9_, ]+?)\s*$')
FILTER_NAME_RE = re.compile(r'^[A-Za-z0-9_]+$')


def parse_filter_names(heading: str) -> list:
    """H2 → 滤镜名列表（官方存在一节多滤镜，如 "## aderivative, aintegral"）。

    首名为主页文件名，其余为别名（官方锚点 #aintegral → aderivative 页）。"""
    m = FILTER_HEADING_RE.match(heading)
    if not m:
        return []
    names = [n.strip() for n in m.group(1).split(',')]
    return [n for n in names if n and FILTER_NAME_RE.match(n)]


def demote_headings(lines: list) -> list:
    """块内标题整体升一级（滤镜页独立成篇：## → #，### → ## …）。

    fenced 代码块内以 `# ` 开头的注释行不改写（保护代码内容）。"""
    out = []
    in_fence = False
    for ln in lines:
        if ln.startswith('```'):
            in_fence = not in_fence
            out.append(ln)
            continue
        if in_fence:
            out.append(ln)
            continue
        m = HEADING_RE.match(ln)
        if m:
            level = max(len(m.group(1)) - 1, 1)
            out.append('#' * level + ' ' + m.group(2))
        else:
            out.append(ln)
    return out


def split_volume(text: str) -> dict:
    """整卷 → {"overview": lines, "filters": [{"name","aliases","group","chapter","lines"}...]}。

    H1 章节按 CHAPTER_GROUP 映射分组；组内 H2 段落逐一成页（一节多滤镜时
    首名为主页、其余为别名）；无组章节内容并入 overview（保留原标题层级）。"""
    lines = text.split('\n')
    overview: list = []
    filters: list = []

    cur_group = None        # 当前章节的分组 slug（None = overview 区）
    cur_chapter = ''
    buf: list = []          # 当前 H2 段落缓冲
    cur_name = None         # 当前 H2 主名（None = 章节前言/overview 内容）
    cur_aliases: list = []
    in_fence = False

    def flush():
        nonlocal buf, cur_name, cur_aliases
        if cur_name is None:
            overview.extend(buf)
        else:
            filters.append({'name': cur_name, 'aliases': cur_aliases,
                            'group': cur_group, 'chapter': cur_chapter,
                            'lines': buf})
        buf = []
        cur_name = None
        cur_aliases = []

    for ln in lines:
        # fenced 代码块内以 # 开头的注释不是标题（实测 filters 卷 19 处）
        if ln.startswith('```'):
            in_fence = not in_fence
        if in_fence:
            if cur_group is None:
                overview.append(ln)
            else:
                buf.append(ln)
            continue
        m = HEADING_RE.match(ln)
        if m and len(m.group(1)) == 1:          # H1 章节
            flush()
            cur_chapter = m.group(2).strip()
            cur_group = None
            for pat, slug in CHAPTER_GROUP:
                if pat.search(cur_chapter):
                    cur_group = slug
                    break
            if cur_group is None:
                overview.append(ln)
            # 分组章标题不进任何页面（每滤镜页自带标题；分组导航由 build_site 生成）
            continue
        if m and len(m.group(1)) == 2 and cur_group is not None:
            names = parse_filter_names(ln)
            if not names:
                # 组内非滤镜 H2——并入 overview 并终止本组（防内容误归属）
                flush()
                cur_group = None
                overview.append(ln)
                continue
            flush()
            cur_name = names[0]
            cur_aliases = names[1:]
            buf = [ln]
            continue
        if cur_group is None:
            overview.append(ln)
        else:
            buf.append(ln)
    flush()

    return {'overview': overview, 'filters': filters}


def validate_split(volume_text: str, result: dict) -> dict:
    """拆分完备性校验（无丢失/重复）：组内 H2 滤镜名全集（含一节多滤镜展开）
    == 主页名 + 别名集合。"""
    volume_filters = []
    cur_group = None
    in_fence = False
    for ln in volume_text.split('\n'):
        if ln.startswith('```'):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEADING_RE.match(ln)
        if not m:
            continue
        if len(m.group(1)) == 1:
            cur_group = None
            for pat, slug in CHAPTER_GROUP:
                if pat.search(m.group(2)):
                    cur_group = slug
                    break
        elif len(m.group(1)) == 2 and cur_group is not None:
            volume_filters.extend(parse_filter_names(ln))
    volume_set = set(volume_filters)
    split_names = []
    for f in result['filters']:
        split_names.append(f['name'])
        split_names.extend(f.get('aliases', []))
    split_set = set(split_names)
    dupes = sorted({n for n in split_names if split_names.count(n) > 1})
    missing = sorted(volume_set - split_set)
    extra = sorted(split_set - volume_set)
    return {
        'volume_filter_count': len(volume_set),
        'split_filter_count': len(split_set),
        'missing': missing,
        'extra': extra,
        'duplicates': dupes,
        'ok': not (missing or extra or dupes),
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog='split_filters.py',
                                 description='filters 整卷拆页（DR-008）')
    ap.add_argument('volume', help='filters 整卷 md（source 或 zh 译文）')
    ap.add_argument('--out-dir', required=True, help='拆页输出目录（<out>/<group>/<name>.md）')
    ap.add_argument('--manifest', help='输出 manifest JSON 路径（分组/清单/校验结果）')
    ap.add_argument('--overview-name', default='overview.md')
    args = ap.parse_args(argv)

    volume_path = Path(args.volume)
    text = volume_path.read_text(encoding='utf-8')
    result = split_volume(text)
    report = validate_split(text, result)

    out_dir = Path(args.out_dir)
    for group in ('video', 'audio', 'multimedia'):
        (out_dir / group).mkdir(parents=True, exist_ok=True)
    for f in result['filters']:
        page = '\n'.join(demote_headings(f['lines'])).strip() + '\n'
        (out_dir / f['group'] / (f['name'] + '.md')).write_text(page, encoding='utf-8')
    overview = '\n'.join(result['overview']).strip() + '\n'
    if overview.strip():
        (out_dir / args.overview_name).write_text(overview, encoding='utf-8')

    report['filters'] = [{'name': f['name'], 'group': f['group'],
                          'chapter': f['chapter']} for f in result['filters']]
    if args.manifest:
        Path(args.manifest).parent.mkdir(parents=True, exist_ok=True)
        Path(args.manifest).write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k != 'filters'},
                     ensure_ascii=False, indent=2))
    if not report['ok']:
        print('split validation FAILED', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
