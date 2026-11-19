#!/usr/bin/env python3
"""站点构建调度（filters 拆页 + mkdocs nav 生成 + zh/ 占位页落位）。

M1 阶段 zh/ 尚无译文：为每个 source 页生成"英文原文占位页"（fmt DR-014
同款口径），M2 译文落位后本脚本自动改用译文内容——生成规则：
  zh/<rel>.md 存在（人工翻译/翻译产物）→ 用译文；
  否则 → 源 md 内容 + 占位提示横幅。

filters 卷（DR-008）拆为 zh/filters/{video,audio,multimedia}/<滤镜>.md
+ overview 页 + 各分组索引页；nav 中只挂分组索引（每滤镜一页经索引页与
站内搜索到达，避免 576 项 nav）。

用法：python3 build_site.py [--nav-only]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
SOURCE_DIR = REPO_ROOT / 'source'
ZH_DIR = REPO_ROOT / 'zh'
MKDOCS_YML = REPO_ROOT / 'mkdocs.yml'
MANIFEST = REPO_ROOT / 'docs' / 'filters-manifest.json'

BANNER = ('!!! warning "翻译占位页"\n'
          '    本页为英文原文占位（翻译进行中，进度见[翻译看板]'
          '(https://github.com/jxsword/ffmpeg-zh-docs/blob/main/docs/translation-board.md)）。\n'
          '    术语与示例以英文原文为准。\n')

# 页面标题表（nav 用；M2 翻译后标题替换为中文，来源=meta.title 或本表）
PAGE_TITLES = {
    'manual/ffmpeg.md': 'ffmpeg 手册',
    'manual/ffplay.md': 'ffplay 手册',
    'manual/ffprobe.md': 'ffprobe 手册',
    'manual/common-options.md': '公共选项（ffmpeg/ffplay/ffprobe）',
    'components/utils.md': '工具（Utils）',
    'components/scaler.md': '缩放器（Scaler）',
    'components/resampler.md': '重采样器（Resampler）',
    'components/codecs.md': '编解码器（Codecs）',
    'components/bitstream-filters.md': '比特流滤镜（Bitstream Filters）',
    'components/formats.md': '格式（Formats）',
    'components/protocols.md': '协议（Protocols）',
    'components/devices.md': '设备（Devices）',
    'libraries/libavutil.md': 'libavutil',
    'libraries/libavcodec.md': 'libavcodec',
    'libraries/libavformat.md': 'libavformat',
    'libraries/libavdevice.md': 'libavdevice',
    'libraries/libavfilter.md': 'libavfilter',
    'libraries/libswscale.md': 'libswscale',
    'libraries/libswresample.md': 'libswresample',
    'general/faq.md': 'FAQ',
    'general/general.md': '通用目录（General）',
    'general/platform.md': '平台（Platform）',
    'general/developer.md': '开发者（Developer）',
    'general/git-howto.md': 'Git 使用（Git Howto）',
    'general/fate.md': 'FATE 测试',
    'general/authors.md': '作者（Authors）',
    'general/mailing-list-faq.md': '邮件列表 FAQ',
    'general/nut.md': 'NUT 格式',
    'general/community.md': '社区（Community）',
    'general/drawvg-reference.md': 'drawvg 参考',
    'general/APIchanges.md': 'API 变更日志（英文原文）',
}

GROUP_TITLES = {'video': '视频滤镜', 'audio': '音频滤镜', 'multimedia': '多媒体滤镜'}

NAV_MARK_BEGIN = '# === NAV-BEGIN（build_site.py 生成，勿手改） ==='
NAV_MARK_END = '# === NAV-END ==='


def write_zh_page(rel: str) -> bool:
    """单页落位：译文优先，否则占位。返回是否占位。"""
    src = SOURCE_DIR / rel
    dest = ZH_DIR / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    zh_native = ZH_DIR / rel
    if zh_native.exists():
        return False  # 译文已在（M2 产物或人工页），不覆盖
    body = src.read_text(encoding='utf-8')
    dest.write_text(BANNER + '\n' + body, encoding='utf-8')
    return True


def write_filter_pages() -> dict:
    """filters 卷拆页落位 zh/filters/，生成分组索引页。返回 manifest。"""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import split_filters
    volume = ZH_DIR / 'components' / 'filters.md'
    if not volume.exists():
        volume = SOURCE_DIR / 'components' / 'filters.md'
    text = volume.read_text(encoding='utf-8')
    result = split_filters.split_volume(text)
    report = split_filters.validate_split(text, result)
    if not report['ok']:
        raise RuntimeError('filters split validation failed: '
                           + json.dumps(report, ensure_ascii=False))

    out_root = ZH_DIR / 'filters'
    groups = {'video': [], 'audio': [], 'multimedia': []}
    for f in result['filters']:
        page = '\n'.join(split_filters.demote_headings(f['lines'])).strip() + '\n'
        dest = out_root / f['group'] / (f['name'] + '.md')
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(page, encoding='utf-8')
        groups[f['group']].append(f['name'])

    # overview 页
    overview = '\n'.join(result['overview']).strip()
    if overview:
        (out_root / 'overview.md').write_text(overview + '\n', encoding='utf-8')

    # 分组索引页（列表 + 别名重定向说明）
    manifest = {'groups': {}, 'aliases': []}
    for group, names in groups.items():
        names = sorted(set(names))
        lines = ['# ' + GROUP_TITLES[group] + '（' + str(len(names)) + ' 个滤镜）', '']
        for name in names:
            lines.append('- [' + name + '](' + name + '/)')
        (out_root / group / 'index.md').write_text('\n'.join(lines) + '\n',
                                                   encoding='utf-8')
        manifest['groups'][group] = names
    for f in result['filters']:
        for alias in f.get('aliases', []):
            manifest['aliases'].append({'alias': alias, 'page': f['name'],
                                        'group': f['group']})
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2),
                        encoding='utf-8')
    return manifest


def build_nav(manifest: dict) -> list:
    """DR-009 nav 结构 + filters 分组动态 nav。"""
    def page(rel):
        return {PAGE_TITLES.get(rel, rel): rel}

    nav = [{'首页': 'index.md'},
           {'手册': [page('manual/ffmpeg.md'), page('manual/ffplay.md'),
                     page('manual/ffprobe.md'), page('manual/common-options.md')]},
           {'组件': [page('components/utils.md'), page('components/scaler.md'),
                     page('components/resampler.md'), page('components/codecs.md'),
                     page('components/bitstream-filters.md'),
                     page('components/formats.md'), page('components/protocols.md'),
                     page('components/devices.md')]},
           {'滤镜': [{'滤镜总览': 'filters/overview.md'}] +
                    [{'视频滤镜（' + str(len(manifest['groups']['video'])) + '）':
                      'filters/video/index.md'},
                     {'音频滤镜（' + str(len(manifest['groups']['audio'])) + '）':
                      'filters/audio/index.md'},
                     {'多媒体滤镜（' + str(len(manifest['groups']['multimedia'])) + '）':
                      'filters/multimedia/index.md'}]},
           {'库': [page('libraries/libavutil.md'), page('libraries/libavcodec.md'),
                   page('libraries/libavformat.md'), page('libraries/libavdevice.md'),
                   page('libraries/libavfilter.md'), page('libraries/libswscale.md'),
                   page('libraries/libswresample.md')]},
           {'General': [page('general/faq.md'), page('general/general.md'),
                        page('general/platform.md'), page('general/developer.md'),
                        page('general/git-howto.md'), page('general/fate.md'),
                        page('general/authors.md'),
                        page('general/mailing-list-faq.md'), page('general/nut.md'),
                        page('general/community.md'),
                        page('general/drawvg-reference.md'),
                        page('general/APIchanges.md')]},
           ]
    return nav


def patch_mkdocs_nav(nav: list) -> None:
    """重写 mkdocs.yml 的 NAV 标记块（块内为完整 nav: 映射，整体替换）。

    首次运行：文件尾追加标记块；此后仅替换标记行之间的内容。"""
    import yaml
    text = MKDOCS_YML.read_text(encoding='utf-8')
    nav_yaml = yaml.safe_dump({'nav': nav}, allow_unicode=True, sort_keys=False,
                              default_flow_style=False)
    lines = text.rstrip('\n').split('\n')
    begin = end = None
    for i, ln in enumerate(lines):
        s = ln.strip()
        if s.startswith(NAV_MARK_BEGIN):
            begin = i
        elif s.startswith(NAV_MARK_END):
            end = i
            break
    if begin is None or end is None:
        block = [NAV_MARK_BEGIN] + nav_yaml.rstrip('\n').split('\n') + [NAV_MARK_END]
        text = text.rstrip('\n') + '\n\n' + '\n'.join(block) + '\n'
    else:
        block = [NAV_MARK_BEGIN] + nav_yaml.rstrip('\n').split('\n') + [NAV_MARK_END]
        lines = lines[:begin] + block + lines[end + 1:]
        text = '\n'.join(lines)
    MKDOCS_YML.write_text(text, encoding='utf-8')


def write_index() -> None:
    upstream = {}
    up_json = SOURCE_DIR / 'UPSTREAM.json'
    if up_json.exists():
        upstream = json.loads(up_json.read_text(encoding='utf-8'))
    tag = upstream.get('tag', 'n9.0.2')
    total = sum(len(v) for v in read_manifest_groups().values())
    md = ('# FFmpeg 中文文档\n\n'
          '> 译自 [FFmpeg 官方文档](https://ffmpeg.org/documentation.html)，'
          '基线 **' + tag + '**。跟随上游 release 节奏增量翻译：'
          '上游出新版本只译变更内容。\n\n'
          '## 内容导航\n\n'
          '- **手册**：ffmpeg / ffplay / ffprobe 命令行工具与公共选项\n'
          '- **组件**：编解码器、格式、协议、设备等官方组件文档\n'
          '- **滤镜**：' + str(total) + ' 个滤镜每滤镜一页（视频/音频/多媒体分组）\n'
          '- **库**：libav* 等 7 个库页\n'
          '- **General**：FAQ、平台、开发者文档等\n\n'
          '## 许可\n\n'
          '除 wiki 精选页（CC BY-SA 3.0）外，译文基于 FFmpeg 官方文档'
          '（LGPL 2.1+）以 LGPL-2.1-or-later 提供；详见 '
          '[LICENSE_TRANSLATION.md](https://github.com/jxsword/ffmpeg-zh-docs/blob/main/LICENSE_TRANSLATION.md)。\n')
    (ZH_DIR / 'index.md').parent.mkdir(parents=True, exist_ok=True)
    (ZH_DIR / 'index.md').write_text(md, encoding='utf-8')


def read_manifest_groups() -> dict:
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text(encoding='utf-8')).get('groups', {})
    return {'video': [], 'audio': [], 'multimedia': []}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog='build_site.py')
    ap.add_argument('--nav-only', action='store_true',
                    help='仅重生成 nav（不重建占位页）')
    args = ap.parse_args(argv)

    manifest = write_filter_pages()
    if not args.nav_only:
        placeholders = 0
        for md in sorted(SOURCE_DIR.rglob('*.md')):
            rel = str(md.relative_to(SOURCE_DIR))
            if rel == 'components/filters.md':
                continue          # 卷文件不直接上站（拆页后上站）
            if rel == 'index.md':
                continue
            if write_zh_page(rel):
                placeholders += 1
        write_index()
    # 跨页锚点链接修复（PLAN §4.1 fix_links 兜底）
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import fix_links
    fix_links.main(['--report', str(REPO_ROOT / 'docs' / 'link-report.json')])
    patch_mkdocs_nav(build_nav(manifest))
    print(json.dumps({'status': 'ok',
                      'filters': {k: len(v) for k, v in manifest['groups'].items()},
                      'aliases': len(manifest['aliases'])},
                     ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
