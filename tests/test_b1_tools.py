"""B1 工具链单测：cjk_slugify / assemble_translation / validate_translation。

固样测试，无外部工具依赖；惯例沿用 test_m1_pipeline.py（sys.path 注入 + noqa）。
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT))

import assemble_translation  # noqa: E402
import cjk_slugify  # noqa: E402
import validate_translation  # noqa: E402


# ---------- cjk_slugify ----------

def test_slugify_keeps_chinese():
    assert cjk_slugify.slugify('流选择') == '流选择'
    assert cjk_slugify.slugify('回环解码器') == '回环解码器'


def test_slugify_mixed_ascii_chinese():
    # 空格→'-'、ASCII 小写、中文保留（对齐 fix_links.page_slug）
    assert cjk_slugify.slugify('vstats 文件格式') == 'vstats-文件格式'
    assert cjk_slugify.slugify('X11 抓取') == 'x11-抓取'


def test_slugify_ascii_matches_legacy():
    # 英文标题行为与旧 markdown.extensions.toc.slugify 一致
    assert cjk_slugify.slugify('Stream selection') == 'stream-selection'
    assert cjk_slugify.slugify('Advanced Video options') == 'advanced-video-options'


def test_slugify_drops_punctuation_and_collapses():
    assert cjk_slugify.slugify('Options (framesync)') == 'options-framesync'
    assert cjk_slugify.slugify('a  --  b') == 'a-b'
    assert cjk_slugify.slugify('  leading') == 'leading'


def test_slugify_custom_separator():
    assert cjk_slugify.slugify('a b c', separator='_') == 'a_b_c'


# ---------- assemble_translation ----------

def _write_state(tmp_path: Path, segments: list[dict]) -> Path:
    state = {'files': {'demo/page.md': {'segments': segments}}}
    (tmp_path / '.translation-state.json').write_text(
        json.dumps(state, ensure_ascii=False), encoding='utf-8')
    return tmp_path


def _seed(tmp_path: Path) -> None:
    segs = [
        {'type': 'heading', 'content': '# Title'},
        {'type': 'paragraph', 'content': 'Hello world.'},
        {'type': 'code_block', 'content': '``` text\nffmpeg -i in\n```'},
        {'type': 'paragraph', 'content': 'Bye.'},
    ]
    _write_state(tmp_path, segs)
    tr = tmp_path / 'tr'
    tr.mkdir()
    (tr / '01.txt').write_text(
        '@@0\n# 标题\n\n@@1\n你好世界。\n', encoding='utf-8')
    (tr / '02.txt').write_text('@@3\n再见。\n', encoding='utf-8')


def _run_assemble(tmp_path: Path):
    argv = ['--source', 'demo/page.md', '--tr-dir', str(tmp_path / 'tr')]
    old_root = assemble_translation.REPO_ROOT
    assemble_translation.REPO_ROOT = tmp_path
    try:
        return assemble_translation.main(argv)
    finally:
        assemble_translation.REPO_ROOT = old_root


def test_assemble_happy_path(tmp_path):
    _seed(tmp_path)
    assert _run_assemble(tmp_path) == 0
    out = tmp_path / 'zh' / 'demo' / 'page.md'
    text = out.read_text(encoding='utf-8')
    # 段落 1:1 + "\n\n" 连接 + 代码块逐字取用
    assert text == '# 标题\n\n你好世界。\n\n``` text\nffmpeg -i in\n```\n\n再见。\n'


def test_assemble_missing_translation_fails(tmp_path, capsys):
    _seed(tmp_path)
    (tmp_path / 'tr' / '02.txt').unlink()
    assert _run_assemble(tmp_path) == 1
    assert 'missing translation' in capsys.readouterr().out


def test_assemble_extra_index_fails(tmp_path, capsys):
    _seed(tmp_path)
    # @@3 合法保留，另加未知索引块 → 触发 unknown 检查（missing 先行）
    (tmp_path / 'tr' / '03.txt').write_text('@@99\n多余\n', encoding='utf-8')
    assert _run_assemble(tmp_path) == 1
    assert 'unknown' in capsys.readouterr().out


def test_assemble_empty_translation_fails(tmp_path, capsys):
    _seed(tmp_path)
    (tmp_path / 'tr' / '02.txt').write_text('@@3\n   \n', encoding='utf-8')
    assert _run_assemble(tmp_path) == 1
    assert 'empty' in capsys.readouterr().out


def test_load_segments_from_real_state():
    segs = assemble_translation.load_segments('manual/ffmpeg.md')
    assert len(segs) == 805
    assert sum(1 for s in segs if s['type'] == 'code_block') == 95


# ---------- validate_translation ----------

def test_extract_code_blocks_indented():
    text = 'para\n\n  ``` text\n  ffmpeg -i in\n  ```\n\nafter\n``` c\nx\n```\n'
    blocks = validate_translation.extract_code_blocks(text)
    assert len(blocks) == 2
    assert blocks[0].startswith('  ``` text')


def test_strip_code_neutralizes_escaped_brackets():
    prose = 'use \\<codec\\> and <b>bold</b>\n\n    indented_code()\n'
    stripped = validate_translation.strip_code(prose)
    assert '<codec' not in stripped.replace(' ', '') or '\\<' not in stripped
    assert '<b>' in stripped          # 真实标签保留
    assert 'indented_code' not in stripped  # 缩进代码块剥离


def test_multiset_diff_reports_changes():
    assert validate_translation.multiset_diff({'a': 1, 'b': 2}, {'a': 2}) == ['a:1->2', 'b:2->0']


def _pair(tmp_path: Path, src: str, tgt: str) -> dict:
    s = tmp_path / 's.md'
    t = tmp_path / 't.md'
    s.write_text(src, encoding='utf-8')
    t.write_text(tgt, encoding='utf-8')
    return validate_translation.validate_file(s, t, {'filter': '滤镜'})


def test_validate_happy_path(tmp_path):
    src = '# 滤镜\n\n一个 `scale` 滤镜。\n\n``` text\nffmpeg -i in\n```\n\n| `a` | 描述 |\n'
    r = _pair(tmp_path, src, src)
    assert r['errors'] == []
    assert r['warnings'] == []


def test_validate_code_block_modified(tmp_path):
    src = '``` text\nffmpeg -i in\n```\n'
    r = _pair(tmp_path, src, '``` text\nffmpeg -i OUT\n```\n')
    assert any('Code block 0 modified' in e for e in r['errors'])


def test_validate_inline_code_mismatch(tmp_path):
    r = _pair(tmp_path, '使用 `-ss` 定位。\n', '使用 -ss 定位。\n')
    assert any('Inline code multiset mismatch' in e for e in r['errors'])


def test_validate_structure_counts(tmp_path):
    src = '# A\n\n段落一。\n\n# B\n\n段落二。\n'
    tgt = '# A\n\n段落一。\n'
    r = _pair(tmp_path, src, tgt)
    assert any('Heading count mismatch' in e for e in r['errors'])
    assert any('Block count mismatch' in e for e in r['errors'])


def test_validate_glossary_and_punctuation_warnings(tmp_path):
    # 术语出现于源正文但译文缺失译名 → warning；CJK 相邻 ASCII 逗号 → warning
    r = _pair(tmp_path, 'the filter works\n', '器件, 正常工作\n')
    assert any("Glossary term 'filter'" in w for w in r['warnings'])
    assert any('ASCII punctuation' in w for w in r['warnings'])


def test_validate_protected_placeholder(tmp_path):
    r = _pair(tmp_path, 'text\n', 'has PROTECTED_CODE_abc123 here\n')
    assert any('PROTECTED_' in e for e in r['errors'])


def test_validate_missing_target(tmp_path):
    s = tmp_path / 's.md'
    s.write_text('x\n', encoding='utf-8')
    r = validate_translation.validate_file(s, tmp_path / 'nope.md', {})
    assert any('Target file not found' in e for e in r['errors'])


def test_fix_links_heading_bridge():
    # DR-011：目标页翻译后标题 slug 中文化，跨页英文锚点经 heading-bridge 重写
    import fix_links  # noqa: E402
    headings = {'流说明符': [('manual/common-options.md', 'Stream specifiers')]}
    bridge = {fix_links.aggressive_form('Stream-specifiers'):
              ('manual/common-options.md', '流说明符')}
    warnings = []
    out = fix_links.fix_page(
        '另请参见[流说明符](#Stream-specifiers)章节。\n',
        'manual/headings-bridge-test-src.md', headings, {}, {}, {}, {},
        warnings, bridge)
    assert '](common-options.md#流说明符)' in out
    assert warnings == []
