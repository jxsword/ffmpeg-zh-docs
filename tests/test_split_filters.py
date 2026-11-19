"""split_filters / validate_structure 单测（DR-008 拆页与结构计数口径）。"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

import split_filters  # noqa: E402
import validate_structure as vs  # noqa: E402


# ---------- split_volume ----------

VOLUME = '''# Filtering Introduction

Intro text here.

# Audio Filters

## aap

Audio auto-pass filter.

### Options

- option one

## aecho, aecho2

Apply echoing.

```shell
# shell comment, NOT a heading
ffmpeg -af aecho=0.8
```

# Video Filters

## scale

Scale (resize) the input video.

### Examples

```shell
## not a heading either
ffmpeg -vf scale=640:480
```

## scale_cuda

CUDA scale variant.
'''


def test_split_volume_groups():
    r = split_filters.split_volume(VOLUME)
    names = [(f['name'], f['group']) for f in r['filters']]
    assert ('aap', 'audio') in names
    assert ('scale', 'video') in names
    assert ('scale_cuda', 'video') in names


def test_split_volume_aliases():
    r = split_filters.split_volume(VOLUME)
    aecho = [f for f in r['filters'] if f['name'] == 'aecho'][0]
    assert aecho['aliases'] == ['aecho2']
    assert 'Apply echoing.' in '\n'.join(aecho['lines'])


def test_split_volume_fence_protection():
    """fenced 内 # 行不得当章节（会把后续滤镜踢出分组）。"""
    r = split_filters.split_volume(VOLUME)
    # scale 不因 shell 注释掉入 overview
    assert any(f['name'] == 'scale' for f in r['filters'])
    # 注释行保留在滤镜页内容里
    scale = [f for f in r['filters'] if f['name'] == 'scale'][0]
    assert '## not a heading either' in '\n'.join(scale['lines'])


def test_split_volume_overview():
    r = split_filters.split_volume(VOLUME)
    ov = '\n'.join(r['overview'])
    assert 'Intro text here.' in ov
    assert 'Filtering Introduction' in ov
    # 组章标题不进 overview
    assert ov.count('Audio Filters') == 0


def test_split_volume_demote():
    r = split_filters.split_volume(VOLUME)
    scale = [f for f in r['filters'] if f['name'] == 'scale'][0]
    page = '\n'.join(split_filters.demote_headings(scale['lines']))
    assert page.startswith('# scale')
    assert '### Examples' not in page
    assert '## Examples' in page


def test_validate_split_ok():
    r = split_filters.split_volume(VOLUME)
    report = split_filters.validate_split(VOLUME, r)
    assert report['ok'], report
    assert report['volume_filter_count'] == report['split_filter_count']


def test_validate_split_detects_loss():
    r = split_filters.split_volume(VOLUME)
    r['filters'] = [f for f in r['filters'] if f['name'] != 'aap']
    report = split_filters.validate_split(VOLUME, r)
    assert not report['ok']
    assert 'aap' in report['missing']


def test_validate_split_counts_aliases():
    r = split_filters.split_volume(VOLUME)
    report = split_filters.validate_split(VOLUME, r)
    assert 'aecho2' not in report['missing']


# ---------- validate_structure.count_md_structure ----------

def test_count_md_structure_basic():
    md = ('# H1\n\n## H2\n\nText para.\n\n'
          '- item\n- item2\n\n``` c\nint x;\n```\n\n'
          '| Term | Description |\n|------|-------------|\n| a | b |\n')
    r = vs.count_md_structure(md)
    assert r['headings'] == 2
    assert r['tables'] == 1
    assert r['code'] == 1
    assert r['list_items'] == 2


def test_count_md_structure_fenced_content_not_structural():
    """fenced 内 #/|/- 行不算结构（filters 卷 shell 注释实测）。"""
    md = ('# H1\n\n```shell\n# comment\n| not a table |\n- not a list\n```\n\nText.\n')
    r = vs.count_md_structure(md)
    assert r['headings'] == 1
    assert r['tables'] == 0
    assert r['list_items'] == 0


def test_count_md_structure_indented_table_in_list():
    """列表项内缩进表格（codecs 选项值表实测形态）。"""
    md = ('- **`eval`** values:\n\n'
          '  | Term | Description |\n'
          '  |------|-------------|\n'
          '  | `init` | once |\n')
    r = vs.count_md_structure(md)
    assert r['tables'] == 1
    assert r['list_items'] == 1


def test_count_md_structure_indented_fence_in_list():
    """列表项内缩进 fenced 代码（XML 层 programlisting 产物）计入 code；
    无 fence 的裸缩进文本不再视为代码（全部代码已 fenced）。"""
    md = '- item:\n\n  ``` text\n  code line\n  ```\n\n- bare indented text\n\n      not code\n'
    r = vs.count_md_structure(md)
    assert r['code'] == 1
    assert r['list_items'] == 2
