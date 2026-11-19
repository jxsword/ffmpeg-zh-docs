#!/usr/bin/env python3
"""外部工具调用包装（subprocess 集中封装）。

所有外部命令以参数列表调用（无 shell 解释层）；git 子命令统一走
git_output/git_ok（fmt sync_docs.py 同款 splat 模式），工具版本查询
逐一内联字面量列表。"""

import subprocess
from pathlib import Path
from typing import Optional


def git_output(args, timeout: int = 120, cwd: Optional[Path] = None) -> str:
    """git 子命令，失败抛错，返回 stdout。"""
    r = subprocess.run(['git', *args], capture_output=True, text=True,
                       timeout=timeout, cwd=cwd)
    if r.returncode != 0:
        raise RuntimeError('git ' + args[0] + ' failed')
    return r.stdout


def git_ok(args, timeout: int = 120, cwd: Optional[Path] = None) -> bool:
    """git 子命令，仅返回是否成功。"""
    r = subprocess.run(['git', *args], capture_output=True, text=True,
                       timeout=timeout, cwd=cwd)
    return r.returncode == 0


def tool_versions() -> dict:
    """取工具版本首行（UPSTREAM.json 记录 + CI 锁定比对）。"""
    out = {}
    r = subprocess.run(['makeinfo', '--version'], capture_output=True,
                       text=True, timeout=30)
    out['makeinfo'] = (r.stdout or r.stderr).splitlines()[0]
    r = subprocess.run(['pandoc', '--version'], capture_output=True,
                       text=True, timeout=30)
    out['pandoc'] = r.stdout.splitlines()[0]
    r = subprocess.run(['doxygen', '--version'], capture_output=True,
                       text=True, timeout=30)
    out['doxygen'] = r.stdout.splitlines()[0]
    out['makeinfo'] = out['makeinfo'].replace('texi2any (GNU texinfo) ', '')
    out['pandoc'] = out['pandoc'].replace('pandoc ', '')
    return out


def head_sha(clone_dir: Path) -> str:
    """浅克隆 detached HEAD：.git/HEAD 文件直接是 SHA。"""
    return (clone_dir / '.git' / 'HEAD').read_text(encoding='utf-8').strip()


def run_configure(clone_dir: Path) -> bool:
    """FFmpeg ./configure（不 make，仅生成 doc/config.texi；免 nasm 选项内联）。"""
    r = subprocess.run(['./configure', '--disable-x86asm'], cwd=clone_dir,
                       capture_output=True, text=True, timeout=1800)
    return r.returncode == 0
