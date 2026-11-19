#!/usr/bin/env python3
"""texi→md 转换器（DR-007 链：makeinfo→DocBook→pandoc→后处理）。

链路：@include 展开为配对标记 → makeinfo --docbook → DocBook XML（安全解析）
→ variablelist 重组 → pandoc → md 后处理（include 裁剪/弯引号/代码 fenced）。

单文件调试用法（全量调度见 sync_docs.py）：
  python3 texi2md.py <input.texi> --srcdir <ffmpeg/doc 目录> --out <output.md>
      [--strip-all | --strip authors,config] [--meta <meta.json>]
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

MAX_XML_BYTES = 64 * 1024 * 1024
BULLET_TERM_MAXLEN = 80

INCLUDE_RE = re.compile(r'^@include\s+(\S+\.texi)\s*$')
SETTITLE_RE = re.compile(r'^@settitle\s+(.+?)\s*$', re.M)
STRAY_ENTITY_RE = re.compile(r'&([A-Za-z][A-Za-z0-9]*);')
LIST_MARKER_RE = re.compile(r'^(?:[-*+] |\d{1,2}\. )')
START_RE = re.compile(r'^%%INCLUDE_START:(.+?)%%\s*$')
END_RE = re.compile(r'^%%INCLUDE_END:.+?%%\s*$')
CODE_INDENT_RE = re.compile(r'^( {4})+\S')

START_FMT = '%%INCLUDE_START:{}%%'
END_FMT = '%%INCLUDE_END:{}%%'


# ============ ① texi 预处理 ============

def flatten_includes(text: str, srcdir: Path, stack: tuple = (),
                     skip_all: bool = False, skip_names: frozenset = frozenset()) -> str:
    """@include 递归展开：keep 项配对标记包裹；被裁项（DR-009）整体跳过。

    被裁 include 不展开也不插标记——makeinfo 看不到它们，XML 结构计数与
    最终 md 自然一致（标记 para 会被 makeinfo 移入 chapter/sect1 内部，
    XML 层裁剪不可靠，实测教训）。禁止循环 include。"""
    out_lines = []
    for line in text.split('\n'):
        m = INCLUDE_RE.match(line)
        if not m:
            out_lines.append(line)
            continue
        name = m.group(1)
        if skip_all or name in skip_names:
            continue
        if name in stack:
            raise RuntimeError('circular @include: ' + ' -> '.join(stack + (name,)))
        inc_path = srcdir / name
        if not inc_path.is_file():
            raise FileNotFoundError('include not found: ' + name)
        inc_text = inc_path.read_text(encoding='utf-8', errors='replace')
        # 标记前后必须空行：texinfo 以空行分段，否则标记并入 include 首段
        out_lines.append('')
        out_lines.append(START_FMT.format(name))
        out_lines.append('')
        out_lines.append(flatten_includes(inc_text, srcdir, stack + (name,),
                                          skip_all, skip_names))
        out_lines.append('')
        out_lines.append(END_FMT.format(name))
        out_lines.append('')
    return '\n'.join(out_lines)


def strip_texi_boilerplate(text: str) -> str:
    """去除对 md 无意义的 texinfo 外壳指令（titlepage/contents/top）。"""
    text = re.sub(r'@titlepage.*?@end titlepage', '', text, flags=re.S)
    text = re.sub(r'^@contents\s*$', '', text, flags=re.M)
    text = re.sub(r'^@top\s*$', '', text, flags=re.M)
    return text


def extract_settitle(text: str) -> str | None:
    m = SETTITLE_RE.search(text)
    return m.group(1).strip() if m else None


# ============ ② DocBook XML 安全解析与重组 ============

def parse_docbook(xml_text: str) -> ET.Element:
    """安全解析：剥 DOCTYPE 与内建实体（防实体扩展），限长，拒绝残余实体。"""
    if len(xml_text) > MAX_XML_BYTES:
        raise RuntimeError('DocBook XML too large: ' + str(len(xml_text)))
    m = re.search(r'<!DOCTYPE.*?\]>', xml_text, flags=re.S)
    if m:
        block = m.group(0)
        for k, v in re.findall(r'<!ENTITY\s+(\w+)\s+"([^"]*)"', block):
            xml_text = xml_text.replace('&' + k + ';', v)
        xml_text = xml_text.replace(block, '')
    else:
        xml_text = re.sub(r'<!DOCTYPE[^>[]*(\[.*?\])?>', '', xml_text, flags=re.S)
    # 标准 5 实体为 XML 内建、合法；其余命名实体（原 DOCTYPE 定义遗漏）才拒绝
    leftover = [e for e in STRAY_ENTITY_RE.findall(xml_text)
                if e not in ('amp', 'lt', 'gt', 'quot', 'apos')]
    if leftover:
        raise RuntimeError('undefined XML entity: &' + leftover[0] + ';')
    return ET.fromstring(xml_text)


def _text_of(el: ET.Element) -> str:
    return re.sub(r'\s+', ' ', (el.text or '')).strip()


def normalize_ws(el: ET.Element) -> None:
    """递归压缩子树 text/tail 连续空白为单空格（表格单元格需单行）。"""
    if el.text:
        el.text = re.sub(r'\s+', ' ', el.text)
    for child in el.iter():
        if child.tail:
            child.tail = re.sub(r'\s+', ' ', child.tail)


def normalize_anchor_id(text: str) -> str:
    """官方 HTML 锚点命名：空格→'-'，其余非字母数字→_005f 式十六进制。"""
    out = []
    for ch in text:
        if ch.isalnum() or ch == '-':
            out.append(ch)
        elif ch == ' ':
            out.append('-')
        else:
            out.append('_%04x' % ord(ch))
    return ''.join(out)


SECTION_RE = re.compile(r'^(chapter|sect\d)$')


def collect_anchors(root: ET.Element) -> list[dict]:
    """收集 <anchor id> → 所在 section 标题与层级（anchor_map 构建输入）。"""
    anchors = []
    def walk(el, section_stack):
        if el.tag == 'anchor':
            ctx = section_stack[-1] if section_stack else None
            anchors.append({
                'id': el.get('id') or '',
                'raw_title': ctx['title'] if ctx else '',
                'level': ctx['level'] if ctx else 0,
            })
            return
        if SECTION_RE.match(el.tag):
            t = el.find('title')
            if t is not None:
                section_stack.append({'title': _text_of(t),
                                      'level': len(section_stack) + 1})
                for child in el:
                    walk(child, section_stack)
                section_stack.pop()
                return
        for child in el:
            walk(child, section_stack)
    walk(root, [])
    return anchors


def count_structure(root: ET.Element) -> dict:
    """重组后的 DocBook 结构计数（validate_structure 的中间基准）。"""
    def count(tag_re: str) -> int:
        return sum(1 for el in root.iter() if re.match(tag_re, el.tag))
    return {
        'headings': count(r'^(chapter|sect\d)$'),
        'tables': count(r'^(informaltable|table)$'),
        'screens': count(r'^(screen|programlisting)$'),
        'lists': count(r'^(itemizedlist|orderedlist|variablelist)$'),
        'list_items': count(r'^listitem$'),
    }


def restructure_variablelists(root: ET.Element) -> dict:
    """variablelist 重组（DR-007 后处理②：项值对结构化）。

    - 简单值对（单 term + 纯文本短定义，且连续）→ Term/Description 两列表格
    - 其余条目 → 无序列表项：**term** 与首段定义合并，其余子块保持项内顺序
    """
    stats = {'tables': 0, 'bullets': 0}

    def tableify(entries):
        tbl = ET.Element('informaltable')
        tg = ET.SubElement(tbl, 'tgroup', {'cols': '2'})
        thead = ET.SubElement(tg, 'thead')
        hr = ET.SubElement(thead, 'row')
        for h in ('Term', 'Description'):
            e = ET.SubElement(hr, 'entry')
            e.text = h
        tbody = ET.SubElement(tg, 'tbody')
        for term_el, para_el in entries:
            row = ET.SubElement(tbody, 'row')
            for src in (term_el, para_el):
                e = ET.SubElement(row, 'entry')
                e.extend(list(src))
                if src.text and src.text.strip():
                    e.text = src.text
                normalize_ws(e)
        return tbl

    def to_bullet_item(terms, li):
        """varlistentry → listitem：**term** 与首段定义合并，其余子块保持顺序。

        ET 内容模型：first.text 在 em 之前、em.tail 在 em 之后——
        定义文本必须写入 em.tail（否则跑到 term 前面）。
        li 为 None（无定义的裸 term 条目）时仅输出 term，不得丢条目。"""
        item = ET.Element('listitem')
        first = ET.Element('para')
        em = ET.SubElement(first, 'emphasis', {'role': 'bold'})
        if terms:
            t = terms[0]
            em.text = t.text or ''
            for child in list(t):
                em.append(child)
        else:
            em.text = '(item)'
        li_children = list(li) if li is not None else []
        paras = [c for c in li_children if c.tag == 'para']
        if paras:
            pd = paras[0]
            # 不 strip：保留定义文本与首个内联子元素之间的空格
            em.tail = ' ' + re.sub(r'\s+', ' ', pd.text or '')
            for child in list(pd):
                first.append(child)
        else:
            em.tail = ''
        item.append(first)
        for child in li_children:
            if child.tag == 'para':
                if paras and child is paras[0]:
                    continue
                item.append(child)
            else:
                item.append(child)
        return item

    def is_table_candidate(terms, li):
        if li is None:
            return False
        # 条目必须"恰好只有一段纯文本定义"——含嵌套 variablelist/屏幕/第二段的
        # 条目走 bullet 路径（tableify 只搬 term+首段，其余子块会丢失，实测教训）
        children = list(li)
        paras = [c for c in children if c.tag == 'para']
        return (len(terms) == 1 and len(children) == 1 and len(paras) == 1
                and len(paras[0]) == 0
                and bool((paras[0].text or '').strip())
                and len((paras[0].text or '').strip()) <= BULLET_TERM_MAXLEN)

    def build_blocks(vl):
        """单个 variablelist → 替换块序列。

        整表统一判定：全部条目都是简单值对 → 一张表；否则全部转 bullets。
        避免 bullet/表格混排破坏语义列表；无 listitem 的裸 term 条目保留为空定义项。"""
        entries = []
        for ve in vl.findall('varlistentry'):
            terms = ve.findall('term')
            li = ve.find('listitem')
            entries.append((terms, li))
        if entries and all(is_table_candidate(t, li) for t, li in entries):
            stats['tables'] += 1
            return [('table', tableify([
                (t[0], [c for c in li if c.tag == 'para'][0])
                for t, li in entries]))]
        blocks = []
        if entries:
            il = ET.Element('itemizedlist')
            for t, li in entries:
                il.append(to_bullet_item(t, li))
            blocks.append(('bullets', il))
            stats['bullets'] += 1
        return blocks

    def process_children(el):
        """递归下降：替换本层 variablelist，再深入新块处理嵌套 vl。

        不能用预建 parent_map 快照——子树被移动后会失联（filters 实测 317 个
        嵌套 vl 丢失），必须就地递归。"""
        for vl in [c for c in list(el) if c.tag == 'variablelist']:
            blocks = build_blocks(vl)
            idx = list(el).index(vl)
            el.remove(vl)
            for i, (_, blk) in enumerate(blocks):
                el.insert(idx + i, blk)
            for _, blk in blocks:
                process_children(blk)
        for child in list(el):
            process_children(child)

    process_children(root)
    return stats


# ============ ③ 外部工具调用 ============

def run_makeinfo(prepared_texi: Path, srcdir: Path, out_xml: Path) -> None:
    """调用 makeinfo 生成 DocBook XML。"""
    r = subprocess.run(['makeinfo', '--docbook', '-I', srcdir, '--no-split', '--force',
                        '-o', out_xml, prepared_texi],
                       capture_output=True, text=True, timeout=600)
    if not out_xml.exists():
        raise RuntimeError('makeinfo failed (no output)')
    if r.returncode != 0:
        sys.stderr.write('[warn] makeinfo rc=' + str(r.returncode) + '\n')


def run_pandoc(in_xml: Path, out_md: Path) -> None:
    """调用 pandoc 转出 GFM。"""
    r = subprocess.run(['pandoc', '-f', 'docbook', '-t', 'gfm', '--wrap=none',
                        '-o', out_md, in_xml],
                       capture_output=True, text=True, timeout=600)
    if r.returncode != 0 or not out_md.exists():
        raise RuntimeError('pandoc failed')


# ============ ④ md 后处理 ============

def strip_include_regions(lines: list, strip_all: bool, strip_names: set) -> list:
    """裁剪 include 区（DR-009）：标记行一律摘除，被裁区域内容整块移除（嵌套安全）。"""
    out = []
    stripping = 0
    for line in lines:
        m = START_RE.match(line)
        if m:
            if strip_all or stripping > 0 or m.group(1) in strip_names:
                stripping += 1
            continue
        if END_RE.match(line):
            if stripping > 0:
                stripping -= 1
            continue
        if stripping == 0:
            out.append(line)
    return out


def clean_curly_quotes(text: str) -> str:
    """弯引号清理：『‘`code`’』→『`code`』；残余单弯引号→直引号；双弯引号→直双引号。"""
    text = text.replace('‘`', '`').replace('`’', '`')
    text = text.replace('‘', "'").replace('’', "'")
    text = text.replace('“', '"').replace('”', '"')
    return text


def collapse_blank_lines(lines: list) -> list:
    out = []
    for ln in lines:
        if ln.strip() == '':
            if out and out[-1].strip() == '':
                continue
        out.append(ln)
    return out


def postprocess_md(md_text: str, strip_all: bool, strip_names: set) -> str:
    lines = md_text.split('\n')
    lines = strip_include_regions(lines, strip_all, strip_names)
    text = clean_curly_quotes('\n'.join(lines))
    lines = collapse_blank_lines(text.split('\n'))
    # fenced 代码已在 XML 层经 programlisting@language 解决（tag_screen_language），
    # 文本层不再做缩进→fenced 转换（与嵌套列表续行文本不可靠区分）
    lines = collapse_blank_lines(lines)
    return '\n'.join(lines).strip() + '\n'


def tag_screen_language(root) -> dict:
    """<screen> → <programlisting language=...>：让 pandoc 直接输出 fenced 代码。

    语境歧义消除：GFM 缩进代码块与嵌套列表续行文本在文本层不可靠区分
    （实测 codecs/filters 大量 @example 位于列表项内），故在 XML 层解决。
    语言启发式：#!→shell；含 ; 与 ( →c；其余 text（pymdownx 不高亮 unknown）。"""
    stats = {'shell': 0, 'c': 0, 'text': 0}
    parent_map = {c: p for p in root.iter() for c in p}

    def pick_lang(text: str) -> str:
        t = text.strip()
        if t.startswith('#!'):
            return 'shell'
        if ';' in t and '(' in t:
            return 'c'
        return 'text'

    for scr in list(root.iter('screen')):
        lang = pick_lang(''.join(scr.itertext()))
        stats[lang] += 1
        pl = ET.Element('programlisting', {'language': lang})
        pl.text = scr.text
        for child in list(scr):
            pl.append(child)
        parent = parent_map.get(scr)
        if parent is not None:
            idx = list(parent).index(scr)
            parent.remove(scr)
            parent.insert(idx, pl)
    # makeinfo 偶发原生 programlisting（无 language 属性，developer.texi 实测）——
    # 补标注，否则 pandoc 输出缩进代码，计数口径失衡
    for pl in list(root.iter('programlisting')):
        if pl.get('language') is None:
            lang = pick_lang(''.join(pl.itertext()))
            pl.set('language', lang)
            stats[lang] += 1
    return stats




# ============ ⑤ 主流程 ============

def convert(texi_text: str, srcdir: Path, strip_all: bool, strip_names: set,
            workdir: Path) -> dict:
    """单文件全链转换，返回 {"md": ..., "meta": ...}。

    srcdir 下的上游文件属不可信数据：只做文本/XML 解析，不执行其中任何脚本。"""
    workdir.mkdir(parents=True, exist_ok=True)
    flat = flatten_includes(texi_text, srcdir,
                            skip_all=strip_all, skip_names=frozenset(strip_names))
    title = extract_settitle(flat)
    flat = strip_texi_boilerplate(flat)

    prepared = workdir / 'prepared.texi'
    prepared.write_text(flat, encoding='utf-8')
    xml_path = workdir / 'out.dbk'
    md_path = workdir / 'out.md'

    run_makeinfo(prepared, srcdir, xml_path)
    root = parse_docbook(xml_path.read_text(encoding='utf-8', errors='replace'))

    meta = {
        'title': title,
        'anchors': collect_anchors(root),
    }
    meta['restructure'] = restructure_variablelists(root)
    meta['code_languages'] = tag_screen_language(root)
    # 被裁 include 未展开（flatten 层跳过），结构基准与最终 md 口径自然一致
    meta['docbook_counts'] = count_structure(root)

    xml_path.write_text(ET.tostring(root, encoding='unicode'))
    run_pandoc(xml_path, md_path)
    md_text = md_path.read_text(encoding='utf-8')
    md_text = postprocess_md(md_text, strip_all, strip_names)
    return {'md': md_text, 'meta': meta}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog='texi2md.py', description='texi→md 转换器（DR-007）')
    ap.add_argument('input', help='输入 .texi（源码树 doc/ 内文件）')
    ap.add_argument('--srcdir', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--strip-all', action='store_true')
    ap.add_argument('--strip', default='')
    ap.add_argument('--meta')
    args = ap.parse_args(argv)

    texi_text = Path(args.input).read_text(encoding='utf-8', errors='replace')
    srcdir = Path(args.srcdir).resolve()
    strip_names = {s.strip() for s in args.strip.split(',') if s.strip()}
    with tempfile.TemporaryDirectory(prefix='texi2md-') as td:
        result = convert(texi_text, srcdir, args.strip_all, strip_names, Path(td))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(result['md'], encoding='utf-8')
    if args.meta:
        meta_path = Path(args.meta)
        meta_path.parent.mkdir(parents=True, exist_ok=True)
        meta_path.write_text(json.dumps(result['meta'], ensure_ascii=False, indent=2),
                             encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
