#!/usr/bin/env python3
"""链接/锚点修复器（fmt fix_links.py 移植改造 + anchor_map 双向映射）。

职责：站内 `](#anchor)` 裸锚点链接在拆页/独有内容重组后指向可能跨页，
构建期按以下优先级重写：
  1. 本页内 slug 命中 → 保持
  2. 全站标题 slug 索引命中 → 重写为相对页路径 + #slug
  3. anchor_map.yml（官方 @anchor id → 页面 + 目标标题 slug）命中 → 重写
  4. filters 别名清单命中 → 重写为滤镜页路径
  5. 未命中 → 保留并记 warning（报告 JSON）

用法：python3 fix_links.py --site-dir zh [--report docs/link-report.json]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
ZH_DIR = REPO_ROOT / 'zh'
CONFIG_DIR = REPO_ROOT / 'config'
MANIFEST = REPO_ROOT / 'docs' / 'filters-manifest.json'

LINK_RE = re.compile(r'\]\(#([^)\s]+)\)')
HTML_LINK_RE = re.compile(r'\]\(([A-Za-z0-9_./-]+\.html)(#[^)\s]*)?\)')
WWW_RE = re.compile(r'\]\((www\.[^)\s]+)\)')
HEADING_RE = re.compile(r'^(#{1,6}) (.*)$')
FENCE_RE = re.compile(r'^\s*```')


def aggressive_form(text: str) -> str:
    """激进归一化：剥全部非字母数字（大小写/连字符/_00XX 编码差异全部抹平）。"""
    return re.sub(r'[^a-z0-9]', '', text.lower())


def page_slug(text: str) -> str:
    """对齐 mkdocs toc.slugify（python-markdown）：小写、空格→'-'、保留 '-'/'_'。"""
    out = []
    for ch in text:
        if ch.isalnum():
            out.append(ch.lower())
        elif ch in (' ', '-', '_'):
            out.append(ch if ch != ' ' else '-')
    return re.sub(r'-+', '-', ''.join(out)).strip('-')


def collect_headings(pages: dict) -> dict:
    """全站标题 slug 索引：slug → [(page, heading_text)...]。"""
    index: dict = {}
    for page, text in pages.items():
        in_fence = False
        for ln in text.split('\n'):
            if FENCE_RE.match(ln):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            m = HEADING_RE.match(ln)
            if m:
                slug = page_slug(m.group(2).strip())
                index.setdefault(slug, []).append((page, m.group(2).strip()))
    return index


def build_fixer():
    """返回 (headings_index, anchor_index, alias_map, page_index)。"""
    import yaml
    pages = {}
    for md in sorted(ZH_DIR.rglob('*.md')):
        rel = str(md.relative_to(ZH_DIR))
        pages[rel] = md.read_text(encoding='utf-8')
    headings = collect_headings(pages)
    # 页名索引（.html 链接重写用）：'platform' → 'general/platform.md'
    page_index: dict = {}
    for rel in pages:
        stem = Path(rel).stem
        page_index.setdefault(stem, rel)
    # 官方页面文件名 → 我方页面（pandoc 保留的 ffmpeg-protocols.html 式链接）
    OFFICIAL_STEMS = {
        'ffmpeg': 'manual/ffmpeg.md', 'ffplay': 'manual/ffplay.md',
        'ffprobe': 'manual/ffprobe.md',
        'ffmpeg-utils': 'components/utils.md',
        'ffmpeg-scaler': 'components/scaler.md',
        'ffmpeg-resampler': 'components/resampler.md',
        'ffmpeg-codecs': 'components/codecs.md',
        'ffmpeg-bitstream-filters': 'components/bitstream-filters.md',
        'ffmpeg-formats': 'components/formats.md',
        'ffmpeg-protocols': 'components/protocols.md',
        'ffmpeg-devices': 'components/devices.md',
        'ffmpeg-filters': 'filters/overview.md',
        'git-howto': 'general/git-howto.md', 'fate': 'general/fate.md',
    }
    for stem, rel in OFFICIAL_STEMS.items():
        if stem not in page_index:
            page_index[stem] = rel

    # 滤镜路由：slug 名 → (group, page)（卷内锚点路由到拆页/overview）
    filter_route: dict = {}
    if MANIFEST.exists():
        manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
        for group, names in manifest.get('groups', {}).items():
            for name in names:
                filter_route.setdefault(page_slug(name), (group, name))
        for a in manifest.get('aliases', []):
            filter_route.setdefault(page_slug(a['alias']),
                                    (a['group'], a['page']))

    amap = {}
    amap_path = CONFIG_DIR / 'anchor_map.yml'
    if amap_path.exists():
        amap = yaml.safe_load(amap_path.read_text(encoding='utf-8')) or {}
    anchor_index: dict = {}
    for page, entries in (amap.get('pages') or {}).items():
        for aid, info in entries.items():
            entry = (page, info)
            # 锚点 id 形态谱系：官方（大小写+_00XX 编码）→ pandoc 链接（小写、
            # 再 slug 化、编码有时保留有时丢弃）。解码+激进归一全变体登记。
            def decode(s):
                # makeinfo 编码：'_' + 4 位十六进制（_002d→'-'、_005f→'_'、_003f→'?'）
                return re.sub(r'_([0-9a-f]{4})',
                              lambda m: chr(int(m.group(1), 16)), s)
            stripped = re.sub(r'(?:_00[0-9a-f]{3})+$', '', aid)
            decoded = decode(aid)
            variants = {aid, stripped, decoded, decode(stripped),
                        aggressive_form(aid), aggressive_form(stripped),
                        aggressive_form(decoded), aggressive_form(decode(stripped))}
            for v in variants:
                if v:
                    anchor_index.setdefault(v, []).append(entry)

    # 标题桥接（DR-011）：目标页翻译后标题 slug 中文化，站内入链仍书写
    # 英文锚点时的显式映射（键经 aggressive_form 归一化）
    bridge: dict = {}
    bridge_path = CONFIG_DIR / 'heading-bridge.yml'
    if bridge_path.exists():
        bdata = yaml.safe_load(bridge_path.read_text(encoding='utf-8')) or {}
        for written, info in (bdata.get('entries') or {}).items():
            bridge[aggressive_form(written)] = (info['page'], info['slug'])

    alias_map = {}
    if MANIFEST.exists():
        manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
        for a in manifest.get('aliases', []):
            alias_map[a['alias']] = (a['group'], a['page'])
    return headings, anchor_index, alias_map, page_index, filter_route, bridge


def fix_page(text: str, page_rel: str, headings: dict, anchor_index: dict,
             alias_map: dict, page_index: dict, filter_route: dict,
             warnings: list, bridge: dict | None = None) -> str:
    bridge = bridge or {}
    """单页链接重写。page_rel 形如 manual/ffmpeg.md。"""
    def rel_target(src: str, dst: str) -> str:
        """mkdocs 相对链接基于源 md 所在目录解析。"""
        import posixpath
        return posixpath.relpath(dst, posixpath.dirname(src) or '.')

    def resolve(anchor: str):
        # 站内 slug 一律小写（mkdocs toc.slugify 口径）；官方大小写/编码锚点
        # 由 anchor_map/别名映射兜底
        key = anchor.lower()
        # 1) 本页内命中 → 保持（重写为小写以对齐站点 slug）
        if any(p == page_rel for p, _ in headings.get(key, [])):
            return None
        # 2) 全站标题 slug
        hits = headings.get(key)
        if hits:
            target = hits[0][0]
            return rel_target(page_rel, target), key
        # 2.5) 标题桥接（DR-011）：目标页已翻译（标题 slug 中文化）的跨页英文锚点
        bhit = bridge.get(aggressive_form(anchor))
        if bhit:
            page, slug = bhit
            return rel_target(page_rel, page), slug
        # 3) 官方 @anchor id（anchor_map；激进归一化抹平编码/大小写/连字符差异）
        hit = (anchor_index.get(anchor)
               or anchor_index.get(aggressive_form(anchor)))
        if hit:
            page, info = hit[0]
            slug = (info.get('slug') or anchor).lower()
            return rel_target(page_rel, page), slug
        # 4) 滤镜别名
        if anchor in alias_map:
            group, name = alias_map[anchor]
            return rel_target(page_rel, 'filters/' + group + '/' + name + '.md'), key
        return 'KEEP', anchor

    def resolve_html(name: str):
        """pandoc 残留的 .html 链接 → 站内页面（同名优先）；
        未命中且非外链者按官方文档页外链兜底。"""
        stem = name.rsplit('/', 1)[-1][:-len('.html')]
        target = page_index.get(stem)
        if target is not None:
            return rel_target(page_rel, target)
        return 'https://ffmpeg.org/' + name.rsplit('/', 1)[-1]

    warnings_local = []

    out_lines = []
    in_fence = False
    for ln in text.split('\n'):
        if FENCE_RE.match(ln):
            in_fence = not in_fence
            out_lines.append(ln)
            continue
        if not in_fence and '](#' in ln:
            def repl(m):
                anchor = m.group(1)
                res = resolve(anchor)
                if res is None:
                    # 本页内命中：仅统一为小写（对齐 mkdocs slug）
                    return '](#' + anchor.lower() + ')'
                if res[0] == 'KEEP':
                    warnings_local.append({'file': page_rel, 'anchor': anchor})
                    return m.group(0)
                target, slug = res
                if target.endswith('components/filters.md'):
                    # 卷文件不上站（DR-008 拆页）：滤镜名 → 拆页；其余 → overview
                    route = filter_route.get(slug)
                    if route:
                        target = rel_target(page_rel,
                                            'filters/' + route[0] + '/' + route[1] + '.md')
                    else:
                        target = rel_target(page_rel, 'filters/overview.md')
                return '](' + target + '#' + slug + ')'
            ln = LINK_RE.sub(repl, ln)
        if not in_fence and '.html' in ln:
            def repl_html(m):
                target = resolve_html(m.group(1))
                if target is None:
                    warnings_local.append({'file': page_rel, 'html': m.group(1)})
                    return m.group(0)
                return '](' + target + (m.group(2) or '') + ')'
            ln = HTML_LINK_RE.sub(repl_html, ln)
        if not in_fence and '](www.' in ln:
            ln = WWW_RE.sub(lambda m: '](https://' + m.group(1) + ')', ln)
        out_lines.append(ln)
    warnings.extend(warnings_local)
    return '\n'.join(out_lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog='fix_links.py')
    ap.add_argument('--site-dir', default=str(ZH_DIR))
    ap.add_argument('--report', default=str(REPO_ROOT / 'docs' / 'link-report.json'))
    args = ap.parse_args(argv)

    site = Path(args.site_dir)
    headings, anchor_index, alias_map, page_index, filter_route, bridge = build_fixer()
    warnings: list = []
    for md in sorted(site.rglob('*.md')):
        text = md.read_text(encoding='utf-8')
        fixed = fix_page(text, str(md.relative_to(site)), headings,
                         anchor_index, alias_map, page_index, filter_route,
                         warnings, bridge)
        if fixed != text:
            md.write_text(fixed, encoding='utf-8')
    Path(args.report).parent.mkdir(parents=True, exist_ok=True)
    Path(args.report).write_text(json.dumps(
        {'unresolved': warnings, 'total': len(warnings)},
        ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'unresolved': len(warnings)}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
