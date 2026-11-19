#!/usr/bin/env python3
"""段级翻译组装器（M2 翻译批次工具，B1 引入）。

用法：
    python3 scripts/assemble_translation.py --source manual/ffmpeg.md \
        --tr-dir /tmp/b1-work/tr [--out zh/manual/ffmpeg.md]

输入：.translation-state.json 中该文件的 segments（texi2md 管线产物，
      每段含 type/content，按序拼接（"\n\n"）可字节级还原源文件）。
译文块格式（一个或多个文件，按文件名排序合并）：

    @@<段索引>
    <译文内容，可多行>
    （空行结束一个块）

规则：
- code_block 段一律从源文件逐字取用（不进译文文件，保证示意图/命令零誊写风险）；
- 其余段（paragraph/heading/table）必须在译文文件中给出对应块，缺失即报错；
- 组装时以 "\n\n" 连接全部段 + 末尾换行，段落结构与源一一对应。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
STATE_FILE = REPO_ROOT / '.translation-state.json'

BLOCK_RE = re.compile(r'^@@(\d+)\s*$')


def load_segments(rel: str) -> list[dict]:
    # 动态取 REPO_ROOT（测试以 monkeypatch 指向临时目录）
    state = json.loads((REPO_ROOT / '.translation-state.json').read_text(encoding='utf-8'))
    files = state.get('files', {})
    if rel not in files:
        raise SystemExit(f'source not in translation state: {rel}')
    return files[rel]['segments']


def parse_translations(paths: list[Path]) -> dict[int, str]:
    trs: dict[int, str] = {}
    for p in paths:
        cur_idx: int | None = None
        cur_lines: list[str] = []
        for raw in p.read_text(encoding='utf-8').split('\n'):
            m = BLOCK_RE.match(raw)
            if m:
                if cur_idx is not None:
                    trs[cur_idx] = '\n'.join(cur_lines).strip('\n')
                cur_idx = int(m.group(1))
                cur_lines = []
            elif cur_idx is not None:
                if raw.strip() == '' and (
                    cur_lines and cur_lines[-1].strip() == ''
                ):
                    continue
                cur_lines.append(raw)
        if cur_idx is not None:
            trs[cur_idx] = '\n'.join(cur_lines).strip('\n')
    return trs


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description='Assemble zh page from segment translations')
    ap.add_argument('--source', required=True, help='源文件相对路径（如 manual/ffmpeg.md）')
    ap.add_argument('--tr-dir', required=True, help='译文块文件目录（@@idx 块格式）')
    ap.add_argument('--out', default=None, help='输出路径（默认 zh/<source>）')
    args = ap.parse_args(argv)

    segs = load_segments(args.source)
    tr_dir = Path(args.tr_dir)
    paths = sorted(p for p in tr_dir.glob('*.txt') if p.is_file())
    if not paths:
        raise SystemExit(f'no translation block files in {tr_dir}')
    trs = parse_translations(paths)

    missing = [
        i for i, s in enumerate(segs)
        if s['type'] != 'code_block' and i not in trs
    ]
    if missing:
        print(f'ERROR: {len(missing)} non-code segments missing translation: {missing[:20]}')
        return 1
    extra = sorted(set(trs) - {i for i, s in enumerate(segs) if s['type'] != 'code_block'})
    if extra:
        print(f'ERROR: translation blocks for unknown/non-code-free indices: {extra[:20]}')
        return 1
    empty = [i for i, t in trs.items() if not t.strip()]
    if empty:
        print(f'ERROR: empty translations at: {empty[:20]}')
        return 1

    parts = []
    for i, s in enumerate(segs):
        if s['type'] == 'code_block':
            parts.append(s['content'])
        else:
            parts.append(trs[i])

    out_path = Path(args.out) if args.out else REPO_ROOT / 'zh' / args.source
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text('\n\n'.join(parts) + '\n', encoding='utf-8')

    n_cb = sum(1 for s in segs if s['type'] == 'code_block')
    print(f'assembled {out_path}: {len(segs)} segments '
          f'({len(trs)} translated, {n_cb} code blocks verbatim)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
