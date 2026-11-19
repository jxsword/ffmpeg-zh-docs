#!/usr/bin/env python3
"""CJK 兼容的 mkdocs toc slug（B1 引入，DR-010）。

背景：mkdocs 默认的 markdown.extensions.toc.slugify 是 ASCII-only
（NFKD + ascii ignore），中文标题的 slug 会变为空串或残缺：
  - 译文页内中文锚点链接（#流选择 等）全部失效；
  - 纯中文标题永远无法被锚定（跨页锚点无从指向）。
本函数与 scripts/fix_links.py 的 page_slug 保持同一口径
（小写、空格→'-'、保留 '-'/'_'、CJK 等 Unicode 字母保留、连续 '-' 折叠），
修复两套实现的分裂（M1 坑位 #5 的"对齐"结论只对英文成立）。

引用方式：mkdocs.yml 经 !!python/name:cjk_slugify.slugify 挂载；
模块位于仓库根且无第三方依赖，mkdocs 必须经 `python3 -m mkdocs` 运行
（-m 模式 sys.path[0]=cwd，模块才可导入；CI deploy workflow 已同步改写）。
"""

import re


def slugify(value: str, separator: str = '-') -> str:
    """对齐 fix_links.page_slug：小写、空格→'-'、保留 '-'/'_'、字母数字保留。"""
    out = []
    for ch in value:
        if ch.isalnum():
            out.append(ch.lower())
        else:
            out.append(separator if ch == ' ' else ch if ch in ('-', '_') else '')
    return re.sub(r'-{2,}', '-', ''.join(out)).strip('-')
