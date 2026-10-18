"""检查仓库内 Markdown 的相对链接是否有效。

用法：
    python tools/check_links.py            # 扫描全库
    python tools/check_links.py --quiet    # 只输出汇总

规则：
- 扫描所有 .md，跳过 .git / node_modules / _chart_preview 等目录
- 提取 Markdown 行内链接与引用式链接
- 跳过 http(s)://、mailto:、纯锚点 #
- 目标是目录时视为有效（部分仓库习惯链接目录）
- 有失效链接时退出码为 1，便于接入 CI
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "node_modules", "_chart_preview", ".idea", ".vscode", "venv", "__pycache__"}

# [文本](目标) 与 ![alt](目标)
INLINE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
# 引用式链接定义： [id]: 目标
REFDEF = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*(\S+)", re.MULTILINE)


def iter_markdown(root: Path):
    for p in root.rglob("*.md"):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        yield p


def extract_targets(text: str):
    """产出 (行号, 原始目标)。"""
    for m in INLINE.finditer(text):
        line_no = text.count("\n", 0, m.start()) + 1
        yield line_no, m.group(1)
    for m in REFDEF.finditer(text):
        line_no = text.count("\n", 0, m.start()) + 1
        yield line_no, m.group(1)


def is_external(target: str) -> bool:
    low = target.lower()
    return (
        low.startswith(("http://", "https://", "mailto:", "tel:", "data:"))
        or target.startswith("#")
    )


def check(root: Path = ROOT):
    broken = []
    total = 0
    for md in iter_markdown(root):
        text = md.read_text(encoding="utf-8", errors="ignore")
        for line_no, raw in extract_targets(text):
            if is_external(raw):
                continue
            target = unquote(raw.split("#", 1)[0].strip())
            if not target:
                continue
            total += 1
            resolved = (md.parent / target).resolve()
            if not resolved.exists():
                broken.append((md, line_no, raw, resolved))
    return total, broken


def main() -> int:
    global ROOT

    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true", help="只输出汇总")
    ap.add_argument("--root", default=str(ROOT), help="扫描根目录，默认仓库根")
    args = ap.parse_args()

    ROOT = Path(args.root).resolve()
    total, broken = check(ROOT)

    if broken and not args.quiet:
        print("失效链接：\n")
        for md, line_no, raw, expected in broken:
            try:
                rel = md.relative_to(ROOT)
            except ValueError:
                rel = md
            try:
                exp = expected.relative_to(ROOT)
            except ValueError:
                exp = expected
            print(f"{rel}:{line_no}  {raw}  ->  期望路径 {exp}")

    if broken:
        print(f"\n共检查 {total} 条内部链接，失效 {len(broken)} 条")
        return 1

    print(f"共检查 {total} 条内部链接，失效 0 条")
    return 0


if __name__ == "__main__":
    sys.exit(main())
