#!/usr/bin/env python3
"""生成翻译看板 docs/translation-board.md（M1 收尾，PLAN §10 批次计划落盘）。

批次粒度 = 单会话可完成（约 400-600 段）；批次划分依据 .translation-state.json
的段落分布 + filters 卷按章节分组（DR-008 翻译单元=滤镜小节）。"""

import json
import re
import sys
from collections import OrderedDict
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
STATE = REPO_ROOT / '.translation-state.json'
BOARD = REPO_ROOT / 'docs' / 'translation-board.md'
UPSTREAM = REPO_ROOT / 'source' / 'UPSTREAM.json'

# 批次顺序（P0 → P2，PLAN §3.1 优先级）
ORDER = [
    'manual/ffmpeg.md', 'manual/ffplay.md', 'manual/ffprobe.md',
    'manual/common-options.md',
    'components/utils.md', 'components/scaler.md', 'components/resampler.md',
    'components/codecs.md', 'components/bitstream-filters.md',
    'components/formats.md', 'components/protocols.md', 'components/devices.md',
    'libraries/libavutil.md', 'libraries/libavcodec.md',
    'libraries/libavformat.md', 'libraries/libavdevice.md',
    'libraries/libavfilter.md', 'libraries/libswscale.md',
    'libraries/libswresample.md',
    'general/faq.md', 'general/general.md', 'general/platform.md',
    'general/developer.md', 'general/git-howto.md', 'general/fate.md',
    'general/authors.md',
    'general/mailing-list-faq.md', 'general/nut.md',
    'general/community.md', 'general/drawvg-reference.md',
]

BATCH_SEGMENTS = 500   # 单批次目标段数


def main():
    state = json.loads(STATE.read_text(encoding='utf-8'))
    upstream = json.loads(UPSTREAM.read_text(encoding='utf-8'))
    files = state['files']

    lines = []
    lines.append('# 翻译任务看板（translation-board）')
    lines.append('')
    lines.append('> 基线：' + upstream['tag'] + '（' + upstream['tag_date'][:10]
                 + '）· 段落总数：' + str(sum(len(f["segments"]) for f in files.values()))
                 + ' · 状态口径：pending=待翻译 / skipped=不译豁免（fmt DR-014）')
    lines.append('> 生成：scripts/gen_board.py（M1 收尾）· 批次粒度 ≈ '
                 + str(BATCH_SEGMENTS) + ' 段/会话')
    lines.append('')

    # 总览表
    lines.append('## 总览')
    lines.append('')
    lines.append('| 文件 | 段落 | 待译 | 豁免 | 优先级 |')
    lines.append('|---|---|---|---|---|')
    for rel in ORDER:
        f = files.get(rel)
        if not f:
            continue
        segs = f['segments']
        pend = sum(1 for s in segs if s['status'] == 'pending')
        skip = sum(1 for s in segs if s['status'] == 'skipped')
        prio = 'P2' if rel.split('/')[-1].split('.')[0] in (
            'mailing-list-faq', 'nut', 'community', 'drawvg-reference') else 'P0'
        lines.append('| ' + rel + ' | ' + str(len(segs)) + ' | ' + str(pend)
                     + ' | ' + str(skip) + ' | ' + prio + ' |')
    api = files.get('general/APIchanges.md')
    if api:
        lines.append('| general/APIchanges.md | ' + str(len(api['segments']))
                     + ' | 0 | ' + str(len(api['segments']))
                     + ' | 豁免（英文占位页，fmt DR-014） |')
    lines.append('')

    # 非滤镜批次（B 系列）
    lines.append('## 批次（正文 B 系列，按优先级排序）')
    lines.append('')
    lines.append('| 批次 | 范围 | 段数 | 状态 |')
    lines.append('|---|---|---|---|')
    b_idx = 1
    cur = []
    cur_count = 0
    for rel in ORDER:
        f = files.get(rel)
        if not f:
            continue
        n = sum(1 for s in f['segments'] if s['status'] == 'pending')
        cur.append(rel)
        cur_count += n
        if cur_count >= BATCH_SEGMENTS:
            lines.append('| B' + str(b_idx) + ' | ' + ' + '.join(cur) + ' | '
                         + str(cur_count) + ' | 未开始 |')
            b_idx += 1
            cur, cur_count = [], 0
    if cur:
        lines.append('| B' + str(b_idx) + ' | ' + ' + '.join(cur) + ' | '
                     + str(cur_count) + ' | 未开始 |')
        b_idx += 1
    lines.append('')

    # filters 批次（F 系列，按章节）
    lines.append('## 批次（filters 卷 F 系列，按章节分组，DR-008）')
    lines.append('')
    lines.append('| 批次 | 章节 | 滤镜数 | 段数 | 状态 |')
    lines.append('|---|---|---|---|---|')
    fsegs = files.get('components/filters.md')
    if fsegs:
        # 走段落序列，按 H1 章节聚合（metadata.section + heading 段）
        chapters = OrderedDict()
        cur_ch = '(前言)'
        for s in fsegs['segments']:
            if s['type'] == 'heading' and s['metadata'].get('level') == 1:
                cur_ch = s['metadata'].get('title') or cur_ch
                chapters.setdefault(cur_ch, {'segs': 0, 'filters': 0})
                continue
            chapters.setdefault(cur_ch, {'segs': 0, 'filters': 0})
            chapters[cur_ch]['segs'] += 1
        f_idx = 1
        pend_total = 0
        for ch, info in chapters.items():
            lines.append('| F' + str(f_idx) + ' | ' + ch + ' | - | '
                         + str(info['segs']) + ' | 未开始 |')
            pend_total += info['segs']
            f_idx += 1
    lines.append('')
    lines.append('## 纪律（M2 跨会话，R2 补充）')
    lines.append('')
    lines.append('- 每批完成即 git 提交 + 本看板勾销 + 交接文档随更新')
    lines.append('- 上下文过半或批次完成即收尾交接，不以"快完了"硬撑新批')
    lines.append('- 术语冻结点：B1 批完成后 glossary v1 冻结（PLAN §9）')

    BOARD.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('board written:', BOARD)


if __name__ == '__main__':
    main()
