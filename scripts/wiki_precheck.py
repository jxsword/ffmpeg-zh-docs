#!/usr/bin/env python3
"""wiki P0 页预处理分级预检（R2：纯文本直译 / 宏密集占位 / 过密降级）。

抓取纪律：每请求间隔 ≥2s（R3 对策）；结果落盘 wiki/meta/p0-precheck.json。
安全边界（Mimosa SSRF 约束）：仅 https、host 白名单（trac.ffmpeg.org）、
解析后 IP 拒绝私网/环回/链路本地地址。
P0 清单（32 页）来自 PLAN §3.2。"""

import json
import re
import socket
import sys
import time
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
META_DIR = REPO_ROOT / 'wiki' / 'meta'
PROXY = 'http://192.168.33.1:10808'
ALLOWED_HOST = 'trac.ffmpeg.org'

P0_PAGES = [
    'EncodingGuide', 'Encode/H.264', 'Encode/H.265', 'Encode/AV1',
    'Encode/VP9', 'Encode/AAC', 'Encode/MP3',
    'CompilationGuide', 'CompilationGuide/Ubuntu', 'CompilationGuide/Generic',
    'CompilationGuide/macOS', 'CompilationGuide/MinGW', 'CompilationGuide/MSVC',
    'CrossCompilingForWindows',
    'FilteringGuide', 'Scaling', 'CroppingVideo', 'Concatenate',
    'AudioVolume', 'FancyFilteringExamples', 'Slideshow', 'AfadeCurves',
    'FFprobeTips', 'How%20to%20use%20-map%20option', 'Seeking',
    'Creating%20multiple%20outputs',
    'HWAccelIntro', 'Hardware/VAAPI', 'Hardware/QuickSync', 'Hardware/AMF',
    'StreamingGuide', 'How%20to%20burn%20subtitles%20into%20the%20video',
]

MACRO_RE = re.compile(r'\[\[([A-Za-z]+)(?:\([^)]*\))?\]\]')


def _check_host(url: str) -> None:
    """SSRF 边界校验：仅 https、host 白名单、解析 IP 拒绝私网/环回。"""
    from urllib.parse import urlparse
    p = urlparse(url)
    if p.scheme != 'https':
        raise ValueError('only https allowed')
    if p.hostname != ALLOWED_HOST:
        raise ValueError('host not in allowlist: ' + str(p.hostname))
    for info in socket.getaddrinfo(p.hostname, 443):
        ip = info[4][0]
        if ip.startswith(('127.', '10.', '192.168.', '169.254.', '0.')) \
                or ip.startswith('172.16.') or ip.startswith('172.17.') \
                or ip.startswith('172.18.') or ip.startswith('172.19.') \
                or ip.startswith('172.2') or ip.startswith('172.30.') \
                or ip.startswith('172.31.') or ip == '::1':
            raise ValueError('resolved private/loopback address: ' + ip)


def fetch(url: str) -> str:
    """白名单校验后抓取；直连失败→代理重试一次（全局网络回退纪律）。"""
    _check_host(url)
    req = urllib.request.Request(url, headers={'User-Agent': 'ffmpeg-zh-docs-sync/0.1'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode('utf-8', errors='replace')
    except Exception:
        proxy = urllib.request.ProxyHandler({'http': PROXY, 'https': PROXY})
        opener = urllib.request.build_opener(proxy)
        _check_host(url)
        req = urllib.request.Request(url, headers={'User-Agent': 'ffmpeg-zh-docs-sync/0.1'})
        with opener.open(req, timeout=30) as r:
            return r.read().decode('utf-8', errors='replace')


def classify(html: str) -> dict:
    """TracWiki 渲染页 → 分级判定（宏/图片/Include 计数）。"""
    macros = len(re.findall(r'class="wiki(?:-macro|\s+image)', html))
    imgs = len(re.findall(r'<img\b', html))
    includes = len(re.findall(r'\[\[Include', html))
    tables = len(re.findall(r'<table\b', html))
    code = len(re.findall(r'<pre\b', html))
    total = macros + imgs + includes
    if total == 0:
        level = 'plain'            # 纯文本/基础标记 → 直译
    elif total <= 8:
        level = 'macro-light'      # 少量宏 → 直译 + 宏占位保护
    elif total <= 25:
        level = 'macro-heavy'      # 宏密集 → 宏输出占位保护、模板段跳过
    else:
        level = 'degrade'          # 过密且常青价值低 → 降级外链不翻译
    return {'macros': macros, 'images': imgs, 'includes': includes,
            'tables': tables, 'code_blocks': code, 'level': level}


def main():
    META_DIR.mkdir(parents=True, exist_ok=True)
    results = {}
    for i, page in enumerate(P0_PAGES):
        url = 'https://' + ALLOWED_HOST + '/wiki/' + page
        try:
            html = fetch(url)
            info = classify(html)
            info['ok'] = True
            info['bytes'] = len(html)
        except Exception as e:
            info = {'ok': False, 'error': type(e).__name__ + ': ' + str(e)[:120]}
        results[page] = info
        print(f"[{i+1}/{len(P0_PAGES)}] {page}: {info.get('level', info.get('error'))}",
              file=sys.stderr)
        time.sleep(2.2)            # 对 trac 限速 ≥2s
    META_DIR.joinpath('p0-precheck.json').write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
    from collections import Counter
    levels = Counter(v.get('level', 'error') for v in results.values())
    print(json.dumps({'pages': len(results), 'levels': dict(levels)},
                     ensure_ascii=False))


if __name__ == '__main__':
    main()
