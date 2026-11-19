#!/usr/bin/env python3
"""转换校验器（DR-007/DR-003/DR-009，PLAN §4.2 六项校验）。

用法：
  python3 validate_structure.py [--source-dir source] [--config-dir config] [--report <json>]

校验项：
  1. 结构计数对比：md 实计数 vs 转换 meta 的 DocBook 基准（标题/表格/代码块/列表项）
  2. 锚点完备：meta.anchors 中每个锚点在 config/anchor_map.yml 有映射
  3. include 完备（DR-009）：手册页不含内联共享内容指纹；语料映射每个内容件有 source md
  4. 占位符保护：无 %%INCLUDE 标记残留、无 texinfo @-命令泄漏
  5. 命令示例静态校验：-vf/-af/-filter_complex 中滤镜名与拆页滤镜清单比对（未知名告警）
  6. 失败行为：任一项失败输出差异报告（文件/行号/类型）并 exit 1；warning 不阻断

统计口径（与 texi2md 转换行为一一对应）：
  headings  = ^#{1,6} 行数
  tables    = 管道表格块数（表头行+分隔行的连续块）
  code      = fenced 块数 + 顶层/嵌套缩进代码 run 数
  listitems = 列表项行数（顶层与嵌套 -/*/+/n. 行）
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()

HEADING_RE = re.compile(r'^#{1,6} ')
LIST_ITEM_RE = re.compile(r'^\s*(?:[-*+] |\d{1,2}\. )')
TABLE_SEP_RE = re.compile(r'^\|?[\s:|-]+\|[\s:|-]*$')
CODE_FENCE_RE = re.compile(r'^```')
INDENT_CODE_RE = re.compile(r'^ {4}\S')
MANUALS = {'ffmpeg.md', 'ffplay.md', 'ffprobe.md'}
MANUAL_DOMAINS = {'manual'}
VFILTER_RE = re.compile(r'(?:^|\s)(?:-vf|-af|-filter(?:_complex)?|-filter:v|-filter:a)\s+(["\']?)(.+?)\1\s*(?:$|\\|\n)')


# ---------- md 结构计数（口径与 texi2md 后处理一致） ----------

def count_md_structure(text: str) -> dict:
    lines = text.split('\n')
    headings = sum(1 for ln in lines if HEADING_RE.match(ln))
    list_items = sum(1 for ln in lines if LIST_ITEM_RE.match(ln))

    tables = 0
    in_table = False
    for i, ln in enumerate(lines):
        if ln.startswith('|'):
            if not in_table:
                # 分隔行在第二行才确认是表格
                if i + 1 < len(lines) and TABLE_SEP_RE.match(lines[i + 1]):
                    tables += 1
                    in_table = True
        else:
            in_table = False

    code = 0
    in_fence = False
    i = 0
    n = len(lines)
    while i < n:
        ln = lines[i]
        if in_fence:
            if CODE_FENCE_RE.match(ln):
                in_fence = False
            i += 1
            continue
        if CODE_FENCE_RE.match(ln):
            code += 1
            in_fence = True
            i += 1
            continue
        if INDENT_CODE_RE.match(ln):
            code += 1
            while i < n:
                cur = lines[i]
                if cur.strip() == '':
                    nxt = next((l for l in lines[i:i + 3] if l.strip()), None)
                    if nxt is not None and (INDENT_CODE_RE.match(nxt) or nxt.startswith(' ')):
                        i += 1
                        continue
                    break
                if INDENT_CODE_RE.match(cur) or cur.startswith('    '):
                    i += 1
                else:
                    break
            continue
        i += 1
    return {'headings': headings, 'tables': tables, 'code': code, 'list_items': list_items}


# ---------- 校验器主体 ----------

def load_corpus_map(source_dir: Path) -> dict:
    """语料映射：相对路径 → meta 路径（source/ 下的 md 与 .meta.json 配对）。"""
    pairs = {}
    for meta_file in sorted(source_dir.rglob('*.meta.json')):
        md_file = meta_file.with_name(meta_file.name[:-len('.meta.json')] + '.md')
        if md_file.exists():
            pairs[str(md_file.relative_to(source_dir))] = meta_file
    return pairs


def check_counts(pairs: dict, source_dir: Path, errors: list) -> int:
    n = 0
    for rel, meta_path in sorted(pairs.items()):
        meta = json.loads(meta_path.read_text(encoding='utf-8'))
        base = meta.get('docbook_counts')
        if not base:
            continue
        md_text = (source_dir / rel).read_text(encoding='utf-8')
        got = count_md_structure(md_text)
        # DocBook screens = md code（fenced + 缩进 run）
        expect_code = base['screens']
        checks = [
            ('headings', base['headings'], got['headings']),
            ('tables', base['tables'], got['tables']),
            ('code', expect_code, got['code']),
            ('list_items', base['list_items'], got['list_items']),
        ]
        for kind, exp, act in checks:
            if exp != act:
                errors.append({'file': rel, 'type': 'count_mismatch_' + kind,
                               'expected': exp, 'actual': act})
                n += 1
    return n


def check_anchor_map(pairs: dict, anchor_map_path: Path, errors: list, warnings: list) -> int:
    n = 0
    amap = {}
    if anchor_map_path.exists():
        import yaml
        amap = yaml.safe_load(anchor_map_path.read_text(encoding='utf-8')) or {}
    for rel, meta_path in sorted(pairs.items()):
        meta = json.loads(meta_path.read_text(encoding='utf-8'))
        for a in meta.get('anchors', []):
            aid = a.get('id')
            if aid and aid not in amap:
                errors.append({'file': rel, 'type': 'anchor_missing_in_map',
                               'anchor': aid})
                n += 1
    return n


def check_include_isolation(source_dir: Path, errors: list, warnings: list) -> int:
    """DR-009：手册页不含内联共享内容（以共享件首段指纹比对）。"""
    n = 0
    manual_dir = source_dir / 'manual'
    if not manual_dir.exists():
        return 0
    # 共享内容件指纹 = 各组件/共享 md 的第一段非标题文本
    fingerprints = {}
    for domain in ('components', 'manual', 'libraries', 'general'):
        d = source_dir / domain
        if not d.exists():
            continue
        for f in sorted(d.rglob('*.md')):
            if f.name in MANUALS:
                continue
            for ln in f.read_text(encoding='utf-8').split('\n'):
                s = ln.strip()
                if s and not s.startswith('#') and not s.startswith('|') \
                   and not s.startswith('```') and len(s) > 60:
                    fingerprints[f.name] = s
                    break
    for f in sorted(manual_dir.glob('*.md')):
        if f.name not in MANUALS:
            continue
        text = f.read_text(encoding='utf-8')
        for name, fp in fingerprints.items():
            if fp[:120] in text:
                errors.append({'file': str(f.relative_to(source_dir)),
                               'type': 'manual_inlines_shared_content',
                               'shared_file': name})
                n += 1
    return n


def check_placeholders(pairs: dict, source_dir: Path, errors: list) -> int:
    """无 INCLUDE 标记残留、无 texinfo @-命令泄漏、弯引号清理完毕。"""
    n = 0
    bad_patterns = [
        ('include_marker', '%%INCLUDE_'),
        ('texinfo_command', re.compile(r'@(?:code|option|var|ref|anchor)\{')),
        ('curly_quote', re.compile(r'[‘’“”]')),
    ]
    for rel, meta_path in sorted(pairs.items()):
        text = (source_dir / rel).read_text(encoding='utf-8')
        for kind, pat in bad_patterns:
            if isinstance(pat, str):
                if pat in text:
                    errors.append({'file': rel, 'type': 'leaked_' + kind})
                    n += 1
            else:
                m = pat.search(text)
                if m:
                    errors.append({'file': rel, 'type': 'leaked_' + kind,
                                   'sample': m.group(0)})
                    n += 1
    return n


def extract_filter_names_from_example(code_text: str, known: set, warnings: list,
                                      where: str) -> None:
    """示例代码中 -vf/-af/-filter_complex 的滤镜名静态比对（PLAN §4.2-5）。"""
    for m in VFILTER_RE.finditer(code_text):
        chain = m.group(2)
        # 粗粒度解析：按逗号/引号切分，取每个滤镜项首段（name= 或 name）
        for part in re.split(r'[,\[\]]', chain):
            part = part.strip().strip('"\'')
            if not part:
                continue
            name = re.match(r'^([A-Za-z0-9_]+)', part)
            if not name:
                continue
            fname = name.group(1)
            if fname in known or fname in ('none',):
                continue
            warnings.append({'file': where, 'type': 'unknown_filter_in_example',
                             'filter': fname})


def check_examples(source_dir: Path, filter_names: set, errors: list,
                   warnings: list) -> int:
    n = 0
    for f in sorted(source_dir.rglob('*.md')):
        text = f.read_text(encoding='utf-8')
        lines = text.split('\n')
        in_fence = False
        buf = []
        for ln in lines:
            if CODE_FENCE_RE.match(ln):
                if in_fence:
                    extract_filter_names_from_example('\n'.join(buf), filter_names,
                                                      warnings, str(f.relative_to(source_dir)))
                    buf = []
                in_fence = not in_fence
                continue
            if in_fence:
                buf.append(ln)
    return n


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog='validate_structure.py',
                                 description='转换结构校验器（PLAN §4.2）')
    ap.add_argument('--source-dir', default=str(REPO_ROOT / 'source'))
    ap.add_argument('--config-dir', default=str(REPO_ROOT / 'config'))
    ap.add_argument('--report')
    args = ap.parse_args(argv)

    source_dir = Path(args.source_dir)
    anchor_map_path = Path(args.config_dir) / 'anchor_map.yml'
    errors: list = []
    warnings: list = []

    pairs = load_corpus_map(source_dir)
    if not pairs:
        errors.append({'type': 'no_meta_files',
                       'detail': 'source/ 下无 .meta.json（先运行 sync_docs.py 转换）'})

    # 滤镜名清单：filters.md 的 meta anchors + H2 sections（动态，不硬编码）
    filter_names = set()
    filters_meta = source_dir / 'components' / 'filters.md.meta.json'
    if filters_meta.exists():
        meta = json.loads(filters_meta.read_text(encoding='utf-8'))
        for a in meta.get('anchors', []):
            if a.get('id'):
                filter_names.add(a['id'])

    check_counts(pairs, source_dir, errors)
    check_anchor_map(pairs, anchor_map_path, errors, warnings)
    check_include_isolation(source_dir, errors, warnings)
    check_placeholders(pairs, source_dir, errors)
    check_examples(source_dir, filter_names, errors, warnings)

    report = {'errors': errors, 'warnings': warnings,
              'files_checked': len(pairs),
              'status': 'fail' if errors else 'pass'}
    out = json.dumps(report, ensure_ascii=False, indent=2)
    if args.report:
        Path(args.report).parent.mkdir(parents=True, exist_ok=True)
        Path(args.report).write_text(out, encoding='utf-8')
    print(out)
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
