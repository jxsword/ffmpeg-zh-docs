#!/usr/bin/env python3
r"""翻译层校验器（fmt-zh-docs validate_translation.py 移植适配，B1 落地）。

校验项（CI 强制，见 config/style-guide.md §四）：
  1. 代码块完整性    —— 数量一致 + 逐字节一致（error）
  2. 内联代码完整性  —— 多重集计数一致（error；语序调整导致的句内互换属正常现象）
  3. HTML 标签完整性 —— 两级：类型 multiset 计数 + 栈配对（error；
     检查前剥离代码与转义尖括号占位符，两侧一致故 multiset 天然对齐）
  4. URL 完整性      —— 数量与取值（warning）
  5. 术语一致性      —— glossary 英文术语出现在源正文 ⇒ 中文译名须出现在译文（warning）
  6. 占位符还原      —— PROTECTED_* 不得残留（error）
  7. 结构完整性      —— 标题数 / 空行分隔段块数 / 表格行数（error）
  8. 中文标点        —— CJK 相邻 ASCII 逗号/句号（warning）

用法：python3 scripts/validate_translation.py [--file manual/ffmpeg.md]
退出码：有 error → 1；仅 warning → 0。
"""

import json
import logging
import re
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).parent.parent.resolve()
SOURCE_DIR = REPO_ROOT / "source"
ZH_DIR = REPO_ROOT / "zh"
STATE_FILE = REPO_ROOT / ".translation-state.json"
GLOSSARY_FILE = REPO_ROOT / "config" / "glossary.yml"


def load_glossary() -> dict[str, str]:
    terms = {}
    if not GLOSSARY_FILE.exists():
        return terms
    try:
        import yaml
        with open(GLOSSARY_FILE, encoding='utf-8') as f:
            data = yaml.safe_load(f)
        for term in data.get('terms', []):
            en, zh = term.get('en', ''), term.get('zh', '')
            if en and zh:
                terms[en] = zh
    except Exception as e:
        logger.warning("Failed to load glossary: %s", e)
    return terms


def load_state() -> dict:
    if not STATE_FILE.exists():
        return {}
    return json.loads(STATE_FILE.read_text(encoding='utf-8'))


def extract_code_blocks(content: str) -> list[str]:
    """按 fence 提取代码块（含缩进围栏的原始行序列）。"""
    lines = content.split('\n')
    out, i = [], 0
    while i < len(lines):
        if re.match(r'^\s*```', lines[i]):
            blk = [lines[i]]
            i += 1
            while i < len(lines) and not re.match(r'^\s*```', lines[i]):
                blk.append(lines[i])
                i += 1
            if i < len(lines):
                blk.append(lines[i])
                i += 1
                out.append('\n'.join(blk))
        else:
            i += 1
    return out


def extract_inline_code(content: str) -> list[str]:
    return re.findall(r'`[^`\n]+`', content)


def extract_html_tags(content: str) -> list[str]:
    return re.findall(r'<[^>]+>', content)


def extract_urls(content: str) -> list[str]:
    return re.findall(r'\[[^\]]+\]\((https?://[^)]+)\)', content)


def strip_code(content: str) -> str:
    r"""剥离代码使结构检查只作用于散文：fenced 块、行内码、缩进代码块
    （corpus 惯例=4 空格起；列表续行散文为 2 空格）。
    同时中和转义尖括号占位符（\<codec\> 是渲染文本而非标签，
    ffmpeg 手册散文中大量出现，不剥离会让配对检查误报未闭合标签）。
    防止占位符 / `src/format.cc` 触发 HTML 标签 / 术语误报。"""
    content = re.sub(r'```[\s\S]*?```', ' ', content)
    content = re.sub(r'`[^`\n]+`', ' ', content)
    content = content.replace('\\<', ' ').replace('\\>', ' ')
    return '\n'.join(
        ' ' if re.match(r'^ {4,}\S', ln) else ln
        for ln in content.split('\n')
    )


def multiset(items) -> dict:
    d = {}
    for x in items:
        d[x] = d.get(x, 0) + 1
    return d


def multiset_diff(src: dict, tgt: dict) -> list[str]:
    parts = []
    for key in sorted(set(src) | set(tgt)):
        s, t = src.get(key, 0), tgt.get(key, 0)
        if s != t:
            parts.append(f"{key}:{s}->{t}")
    return parts


CJK_RE = re.compile(r'[\u4e00-\u9fff]')
BAD_PUNCT_RE = re.compile(r'[\u4e00-\u9fff][,;]|[,;][\u4e00-\u9fff]')


def validate_file(source_path: Path, target_path: Path, glossary: dict) -> dict:
    errors, warnings = [], []

    if not source_path.exists():
        errors.append(f"Source file not found: {source_path}")
        return {"errors": errors, "warnings": warnings}
    if not target_path.exists():
        errors.append(f"Target file not found: {target_path}")
        return {"errors": errors, "warnings": warnings}

    source_content = source_path.read_text(encoding='utf-8')
    target_content = target_path.read_text(encoding='utf-8')

    # 1. 代码块完整性（数量 + 逐字节）
    src_blocks = extract_code_blocks(source_content)
    tgt_blocks = extract_code_blocks(target_content)
    if len(src_blocks) != len(tgt_blocks):
        errors.append(f"Code block count mismatch: source={len(src_blocks)}, target={len(tgt_blocks)}")
    else:
        for i, (s, t) in enumerate(zip(src_blocks, tgt_blocks)):
            if s != t:
                errors.append(f"Code block {i} modified in translation")

    # 2. 内联代码完整性（多重集）
    diff = multiset_diff(
        multiset(extract_inline_code(source_content)),
        multiset(extract_inline_code(target_content)),
    )
    if diff:
        errors.append("Inline code multiset mismatch (missing/extra/modified spans): "
                      + ", ".join(diff))

    # 3. HTML 标签完整性（两级；检查前剥离代码）
    src_tags = extract_html_tags(strip_code(source_content))
    tgt_tags = extract_html_tags(strip_code(target_content))
    diff = multiset_diff(multiset(src_tags), multiset(tgt_tags))
    if diff:
        errors.append("HTML tag type counts mismatch: " + ", ".join(diff))
    if tgt_tags:
        stack = []
        balanced = True
        for tag in tgt_tags:
            if re.match(r'^<https?://', tag):
                continue  # markdown 自动链接 <URL>（如 <http://www.json.org/>），非 HTML 标签
            m = re.match(r'^</?\s*([a-zA-Z][a-zA-Z0-9-]*)', tag)
            if not m:
                continue  # \<...\> 转义占位符等非标签 token
            name, closing = m.group(1).lower(), tag.startswith('</')
            if name in ('img', 'br', 'hr', 'input', 'meta', 'link'):
                continue
            if closing:
                if not stack or stack[-1] != name:
                    balanced = False
                    break
                stack.pop()
            else:
                stack.append(name)
        if not balanced or stack:
            errors.append("Translated HTML tags are unbalanced or improperly nested")

    # 4. URL 完整性
    src_urls = extract_urls(source_content)
    tgt_urls = extract_urls(target_content)
    if len(src_urls) != len(tgt_urls):
        warnings.append(f"URL count mismatch: source={len(src_urls)}, target={len(tgt_urls)}")
    else:
        for i, (s, t) in enumerate(zip(src_urls, tgt_urls)):
            if s != t:
                warnings.append(f"URL {i} modified: {s} -> {t}")

    # 5. 术语一致性（剥离代码与 URL 后的源正文上匹配英文术语）
    source_prose = re.sub(r'https?://\S+', ' ', strip_code(source_content))
    for en_term, zh_term in glossary.items():
        if en_term in source_prose and zh_term not in target_content:
            warnings.append(f"Glossary term '{en_term}' not translated as '{zh_term}'")

    # 6. 占位符还原
    if 'PROTECTED_' in target_content:
        errors.append("Unrestored PROTECTED_* placeholders found in translation")

    # 7. 结构完整性（标题数 / 段块数 / 表格行数）
    def nblocks(t: str) -> int:
        return len([b for b in re.split(r'\n\s*\n', t) if b.strip()])

    src_head = re.findall(r'^#{1,6} .+', source_content, re.M)
    tgt_head = re.findall(r'^#{1,6} .+', target_content, re.M)
    if len(src_head) != len(tgt_head):
        errors.append(f"Heading count mismatch: source={len(src_head)}, target={len(tgt_head)}")
    if nblocks(source_content) != nblocks(target_content):
        errors.append(f"Block count mismatch: source={nblocks(source_content)}, "
                      f"target={nblocks(target_content)}")
    src_rows = len(re.findall(r'^\s*\|', source_content, re.M))
    tgt_rows = len(re.findall(r'^\s*\|', target_content, re.M))
    if src_rows != tgt_rows:
        errors.append(f"Table row count mismatch: source={src_rows}, target={tgt_rows}")

    # 8. 中文标点（warning：CJK 相邻 ASCII 逗号/分号）
    prose = strip_code(target_content)
    for ln in prose.split('\n'):
        if BAD_PUNCT_RE.search(ln):
            warnings.append(f"ASCII punctuation adjacent to CJK: {ln.strip()[:60]}")
            break  # 每文件报一条即可，避免刷屏

    return {"errors": errors, "warnings": warnings}


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Validate translation quality")
    parser.add_argument("--file", default=None,
                        help="只校验指定文件（如 manual/ffmpeg.md）；缺省校验全部")
    args = parser.parse_args()

    state = load_state()
    glossary = load_glossary()
    logger.info("Loaded %d glossary terms", len(glossary))

    all_errors, all_warnings = [], []
    targets = list(state.get('files', {}).keys())
    if args.file:
        if args.file not in state.get('files', {}):
            logger.error("File not in translation state: %s", args.file)
            return 2
        targets = [args.file]

    for fname in targets:
        finfo = state.get('files', {}).get(fname, {})
        if finfo.get('excluded'):
            logger.info("Skipping %s (excluded from translation, DR-014)", fname)
            continue
        # 只校验已开工的文件：无任何 done 段（未翻译/整卷待译）不与 source
        # 全量对比，否则占位页/缺失目标必然报错
        segs = finfo.get('segments', [])
        if not any(s.get('status') == 'done' for s in segs):
            logger.info("Skipping %s (no translated segments yet)", fname)
            continue
        target_path = ZH_DIR / fname
        # 占位页兜底：仍是占位横幅的文件跳过（内容与 source 相同，
        # 会因含英文正文触发大量术语 warning）
        zh_text = target_path.read_text(encoding='utf-8') if target_path.exists() else ''
        if '翻译占位页' in zh_text[:200]:
            logger.info("Skipping %s (placeholder page, not translated yet)", fname)
            continue
        logger.info("Validating %s", fname)
        result = validate_file(SOURCE_DIR / fname, target_path, glossary)
        all_errors.extend(f"{fname}: {e}" for e in result['errors'])
        all_warnings.extend(f"{fname}: {w}" for w in result['warnings'])

    if all_warnings:
        logger.warning("Warnings (%d):", len(all_warnings))
        for w in all_warnings:
            logger.warning("  %s", w)
    if all_errors:
        logger.error("Errors (%d):", len(all_errors))
        for e in all_errors:
            logger.error("  %s", e)
        return 1
    logger.info("All validations passed!")
    return 0


if __name__ == '__main__':
    sys.exit(main())
