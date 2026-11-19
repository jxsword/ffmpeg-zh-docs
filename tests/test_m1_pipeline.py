"""texi2md/sync_docs 管线单测（固样测试，无外部工具依赖）。"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

import texi2md  # noqa: E402
import sync_docs  # noqa: E402


# ---------- flatten_includes ----------

def test_flatten_includes_markers(tmp_path):
    src = tmp_path / 'doc'
    src.mkdir()
    (src / 'a.texi').write_text('@chapter A\n@include b.texi\n', encoding='utf-8')
    (src / 'b.texi').write_text('@chapter B\n', encoding='utf-8')
    flat = texi2md.flatten_includes((src / 'a.texi').read_text(encoding='utf-8'), src)
    assert '%%INCLUDE_START:b.texi%%' in flat
    assert '%%INCLUDE_END:b.texi%%' in flat
    assert '@chapter B' in flat
    # 标记独立成行且前后有空行（texinfo 分段语义）
    lines = flat.split('\n')
    i = lines.index('%%INCLUDE_START:b.texi%%')
    assert lines[i - 1] == '' and lines[i + 1] == ''


def test_flatten_includes_circular(tmp_path):
    src = tmp_path / 'doc'
    src.mkdir()
    (src / 'a.texi').write_text('@include b.texi\n', encoding='utf-8')
    (src / 'b.texi').write_text('@include a.texi\n', encoding='utf-8')
    with pytest.raises(RuntimeError):
        texi2md.flatten_includes((src / 'a.texi').read_text(encoding='utf-8'), src)


# ---------- parse_docbook（安全解析） ----------

def test_parse_docbook_strips_doctype_entities():
    xml = ('<?xml version="1.0"?>\n<!DOCTYPE book PUBLIC "x" "y" [\n'
           '  <!ENTITY tex "TeX">\n]>\n<book><para>&tex; &amp; ok</para></book>')
    root = texi2md.parse_docbook(xml)
    assert root.tag == 'book'
    assert root[0].text == 'TeX & ok'


def test_parse_docbook_rejects_unknown_entity():
    xml = '<book><para>&bogus;</para></book>'
    with pytest.raises(RuntimeError):
        texi2md.parse_docbook(xml)


def test_parse_docbook_size_limit():
    with pytest.raises(RuntimeError):
        texi2md.parse_docbook('x' * (texi2md.MAX_XML_BYTES + 1))


# ---------- restructure_variablelists ----------

def _book_with_vl(entries_xml):
    return texi2md.parse_docbook('<book><chapter><title>T</title>' + entries_xml +
                                 '</chapter></book>')


def test_restructure_table_uniform_short_defs():
    root = _book_with_vl(
        '<variablelist>'
        '<varlistentry><term><literal>ntsc</literal></term>'
        '<listitem><para>720x480</para></listitem></varlistentry>'
        '<varlistentry><term><literal>pal</literal></term>'
        '<listitem><para>720x576</para></listitem></varlistentry>'
        '</variablelist>')
    stats = texi2md.restructure_variablelists(root)
    assert stats['tables'] == 1 and stats['bullets'] == 0
    tbl = root.find('.//informaltable')
    assert tbl is not None
    rows = tbl.findall('.//tbody/row')
    assert len(rows) == 2
    assert rows[0][0].find('literal').text == 'ntsc'


def test_restructure_bullet_preserves_entries_without_listitem():
    """无 listitem 的裸 term 条目不得丢失（in_w/iw 类常量表实测）。"""
    root = _book_with_vl(
        '<variablelist>'
        '<varlistentry><term><option>in_w</option></term></varlistentry>'
        '<varlistentry><term><option>in_h</option></term>'
        '<listitem><para>The input video width.</para></listitem></varlistentry>'
        '</variablelist>')
    stats = texi2md.restructure_variablelists(root)
    assert stats['bullets'] == 1
    items = root.findall('.//listitem')
    assert len(items) == 2            # 裸 term 也成项
    texts = [''.join(x.itertext()) for x in items]
    assert 'in_w' in texts[0] and 'in_h' in texts[1]


def test_restructure_bullet_def_after_term():
    """定义文本在 term 之后（ET 内容模型：em.tail），不跑到前面。"""
    root = _book_with_vl(
        '<variablelist>'
        '<varlistentry><term><literal>ld(idx)</literal></term>'
        '<listitem><para>Load the value of index '
        '<replaceable>idx</replaceable>, stored before.</para>'
        '<para>Second paragraph.</para></listitem></varlistentry>'
        '</variablelist>')
    texi2md.restructure_variablelists(root)
    item_para = root.find('.//listitem/para')
    em = item_para.find('emphasis')
    # term 的 literal 子元素整体迁入 em（pandoc → **`ld(idx)`**）
    assert em.find('literal').text == 'ld(idx)'
    assert em.tail.startswith(' Load the value of index ')
    assert item_para.find('replaceable') is not None
    paras = root.findall('.//listitem/para')
    assert len(paras) == 2            # 第二段保留在项内


def test_restructure_nested_variablelist():
    """列表项内嵌套 variablelist 不得丢失（含嵌套内容的条目禁走表格路径），
    嵌套 vl 同样被重组。"""
    root = _book_with_vl(
        '<variablelist>'
        '<varlistentry><term><option>eval</option></term>'
        '<listitem><para>Values:</para>'
        '<variablelist>'
        '<varlistentry><term><literal>init</literal></term>'
        '<listitem><para>Once at init.</para></listitem></varlistentry>'
        '</variablelist>'
        '</listitem></varlistentry>'
        '</variablelist>')
    texi2md.restructure_variablelists(root)
    assert len(list(root.iter('variablelist'))) == 0
    text = ''.join(root.itertext())
    assert 'Values:' in text
    assert 'Once at init.' in text
    # 嵌套表格在项内（listitem 后代）
    tbl = root.find('.//listitem/informaltable')
    assert tbl is not None


# ---------- strip_include_regions ----------

def test_strip_include_regions_md_manual():
    lines = ['A', '%%INCLUDE_START:x.texi%%', 'X1', '%%INCLUDE_END:x.texi%%', 'B']
    out = texi2md.strip_include_regions(lines, strip_all=True, strip_names=set())
    assert out == ['A', 'B']


def test_strip_include_regions_md_keep():
    lines = ['A', '%%INCLUDE_START:x.texi%%', 'X1', '%%INCLUDE_END:x.texi%%', 'B']
    out = texi2md.strip_include_regions(lines, strip_all=False, strip_names=set())
    assert out == ['A', 'X1', 'B']


def test_strip_include_regions_nested_strip():
    lines = ['A', '%%INCLUDE_START:out.texi%%', 'OUT',
             '%%INCLUDE_START:in.texi%%', 'IN', '%%INCLUDE_END:in.texi%%',
             '%%INCLUDE_END:out.texi%%', 'B']
    out = texi2md.strip_include_regions(lines, strip_all=False,
                                        strip_names={'out.texi'})
    assert out == ['A', 'B']


def test_flatten_skip_names(tmp_path):
    """被裁 include 在 flatten 层跳过（makeinfo 不可见，DR-009）。"""
    src = tmp_path / 'doc'
    src.mkdir()
    (src / 'shell.texi').write_text('@chapter C\n@include content.texi\n'
                                    '@include authors.texi\n', encoding='utf-8')
    (src / 'content.texi').write_text('@chapter Content\n', encoding='utf-8')
    (src / 'authors.texi').write_text('@chapter Authors\n', encoding='utf-8')
    flat = texi2md.flatten_includes((src / 'shell.texi').read_text(encoding='utf-8'),
                                    src, skip_names=frozenset({'authors.texi'}))
    assert 'Authors' not in flat
    assert '%%INCLUDE_START:content.texi%%' in flat
    assert '%%INCLUDE_START:authors.texi%%' not in flat


def test_flatten_skip_all(tmp_path):
    src = tmp_path / 'doc'
    src.mkdir()
    (src / 'man.texi').write_text('@chapter M\n@include utils.texi\n', encoding='utf-8')
    (src / 'utils.texi').write_text('@chapter U\n', encoding='utf-8')
    flat = texi2md.flatten_includes((src / 'man.texi').read_text(encoding='utf-8'),
                                    src, skip_all=True)
    assert 'utils' not in flat and '@chapter U' not in flat


# ---------- tag_screen_language ----------

def test_tag_screen_language():
    root = texi2md.parse_docbook(
        '<book><screen>ffmpeg -i a b</screen>'
        '<screen>#!/bin/sh\necho hi</screen>'
        '<screen>st(0,42); print(f(x));</screen></book>')
    stats = texi2md.tag_screen_language(root)
    assert stats == {'shell': 1, 'c': 1, 'text': 1}
    langs = [pl.get('language') for pl in root.iter('programlisting')]
    assert langs == ['text', 'shell', 'c']
    assert len(list(root.iter('screen'))) == 0


# ---------- normalize_anchor_id / slug ----------

def test_normalize_anchor_id():
    assert texi2md.normalize_anchor_id('Video size') == 'Video-size'
    assert texi2md.normalize_anchor_id('quoting_and_escaping') == \
        'quoting_005fand_005fescaping'
    assert texi2md.normalize_anchor_id('date syntax') == 'date-syntax'


# ---------- clean_curly_quotes ----------

def test_clean_curly_quotes():
    assert texi2md.clean_curly_quotes('‘`x`’ and “q”') == '`x` and "q"'
    assert texi2md.clean_curly_quotes('plain ‘q’') == "plain 'q'"


# ---------- segment_md（sync_docs） ----------

def test_segment_md_basic():
    md = ('# Title\n\n\nPara one.\n\n'
          '- item 1\n- item 2\n\n```\ncode\n```\n\n'
          '| Term | Description |\n|------|-------------|\n| a | b |\n')
    segs = sync_docs.segment_md(md, 'x.md')
    types = [s['type'] for s in segs]
    assert types[0] == 'heading'
    assert 'paragraph' in types and 'code_block' in types and 'table' in types
    for s in segs:
        assert s['hash'] and s['line_start'] >= 1


def test_segment_md_no_infinite_loop():
    """跨行 '<' 开头内容不触发死循环（fmt DR-011 教训回归）。"""
    md = '<!-- broken\ncomment -->\ntext after\n'
    segs = sync_docs.segment_md(md, 'x.md')
    assert len(segs) >= 1


# ---------- detect_latest_tag ----------

def test_detect_latest_tag_parsing(monkeypatch):
    class FakeProc:
        def __init__(self, out):
            self.stdout = out
            self.stderr = ''
            self.returncode = 0
    raw = ('abc\trefs/tags/n8.0\n'
           'def\trefs/tags/n9.0.1\n'
           'ghi\trefs/tags/n9.0.2\n'
           'jkl\trefs/tags/n9.0.2^{}\n'
           'mno\trefs/tags/n9.1-dev\n')
    monkeypatch.setattr(sync_docs.proc, 'git_output',
                        lambda args, timeout=0, cwd=None: raw)
    assert sync_docs.detect_latest_tag('https://example/ffmpeg.git') == 'n9.0.2'


# ---------- build_anchor_map ----------

def test_build_anchor_map(tmp_path):
    import json as _json
    meta_path = tmp_path / 'a.md.meta.json'
    meta_path.write_text(_json.dumps({
        'title': 'T', 'anchors': [{'id': 'Date', 'raw_title': 'Date', 'level': 2}],
    }, ensure_ascii=False), encoding='utf-8')
    out = tmp_path / 'anchor_map.yml'
    n = sync_docs.build_anchor_map({'a.md': meta_path}, out)
    assert n == 1
    import yaml
    data = yaml.safe_load(out.read_text(encoding='utf-8'))
    entry = data['pages']['a.md']['Date']
    assert entry['slug'] == 'date'   # mkdocs 小写口径


# ---------- slugify_title ----------

def test_slugify_title():
    assert sync_docs.mkdocs_slug('Video size') == 'video-size'
    assert sync_docs.mkdocs_slug('ffmpeg-devel?') == 'ffmpeg-devel'
    assert sync_docs.mkdocs_slug('top-posting') == 'top-posting'
