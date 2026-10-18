"""CS Job Guide 图表工具集。

设计目标：
1. 与仓库既有插图视觉一致（米白纸感底 + 墨蓝正文 + 陶橙强调）；
2. 规格驱动，新增图表只需在 data JSON 里加一条 spec，不写绘图代码；
3. 统一来源标注，逼迫每张图都写清出处与口径；
4. 输出 SVG（矢量、体积小、GitHub 原生渲染、可 diff）。

排版约定：
- 标题左对齐、副标题紧随其下，核心结论（callout）右对齐，不抢副标题位置；
- 页脚固定两行：来源 / 口径，超宽自动按中日韩字符宽度折行；
- 数值统一千分位，单位直接写进数值标签，不单独画 x 轴标题。
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path
from typing import Iterable, Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# ---------------------------------------------------------------- 视觉系统

INK = "#17233D"
INK_SOFT = "#3A4A66"
MUTED = "#65728A"
CREAM = "#FFFDF8"
CREAM_2 = "#F7F4EE"
LINE = "#E6DED1"
ORANGE = "#F27649"
ORANGE_SOFT = "#F9D3BF"
BLUE = "#5D78B7"
BLUE_SOFT = "#DDE5F7"
GREEN = "#4E8F7C"
GREEN_SOFT = "#DCEDE6"
RED = "#B5433C"

FONT = "Microsoft YaHei"
W, H = 12.0, 7.2  # dpi=100 时为 1200x720

plt.rcParams.update(
    {
        "font.family": FONT,
        "font.size": 13,
        "svg.fonttype": "path",
        "axes.unicode_minus": False,
        "figure.facecolor": CREAM,
        "axes.facecolor": CREAM,
        "savefig.facecolor": CREAM,
    }
)


def _disp_width(s: str) -> int:
    """估算显示宽度：中日韩字符按 2 计，其余按 1 计。"""
    return sum(2 if ord(c) > 0x2E80 else 1 for c in s)


def _wrap(s: str, limit: int) -> list[str]:
    """按显示宽度折行，避免长来源标注被画布裁切。"""
    lines, cur, w = [], "", 0
    for ch in s:
        cw = 2 if ord(ch) > 0x2E80 else 1
        if w + cw > limit and cur:
            lines.append(cur)
            cur, w = ch, cw
        else:
            cur += ch
            w += cw
    if cur:
        lines.append(cur)
    return lines


def _frame(fig, title: str, subtitle: str, source: str,
           note: str = "", callout: str = "") -> None:
    fig.text(0.045, 0.955, title, fontsize=25, color=INK, weight="bold", va="top")
    if subtitle:
        fig.text(0.045, 0.898, subtitle, fontsize=13, color=MUTED, va="top")
    if callout:
        fig.text(0.955, 0.898, callout, fontsize=13, color=ORANGE,
                 weight="bold", va="top", ha="right")

    # 页脚：分隔线 + 来源（可折行）+ 口径
    fig.add_artist(
        plt.Line2D([0.045, 0.955], [0.135, 0.135], transform=fig.transFigure,
                   color=LINE, linewidth=1)
    )
    y = 0.098
    for ln in _wrap(source, 104)[:2]:
        fig.text(0.045, y, ln, fontsize=9.5, color=MUTED, va="top")
        y -= 0.032
    if note:
        for ln in _wrap(f"口径说明：{note}", 104)[:2]:
            fig.text(0.045, y - 0.006, ln, fontsize=9.5, color=MUTED, va="top")
            y -= 0.032


def _clean_axes(ax, hide_left=False) -> None:
    for side in ("top", "right", "bottom", "left"):
        ax.spines[side].set_visible(False)
    ax.tick_params(length=0)
    if hide_left:
        ax.set_yticks([])


def _save(fig, out: Path) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, format="svg")
    plt.close(fig)
    return out


def _num(v: float, decimals: int, suffix: str) -> str:
    if decimals == 0:
        return f"{v:,.0f}{suffix}"
    return f"{v:,.{decimals}f}{suffix}"


# ---------------------------------------------------------------- 图型


def hbar(
    items: Sequence[dict],
    title: str,
    subtitle: str,
    source: str,
    out: Path,
    suffix: str = "",
    decimals: int = 0,
    highlight: Iterable[str] = (),
    refline: float | None = None,
    refline_label: str = "",
    note: str = "",
    callout: str = "",
) -> Path:
    """横向条形图。highlight 中的标签用陶橙加粗，其余浅蓝。"""
    fig = plt.figure(figsize=(W, H))
    _frame(fig, title, subtitle, source, note, callout)
    ax = fig.add_axes([0.31, 0.20, 0.63, 0.61])

    labels = [i["label"] for i in items]
    values = [float(i["value"]) for i in items]
    hi = set(highlight)
    colors = [ORANGE if lb in hi else BLUE_SOFT for lb in labels]

    y = list(range(len(labels)))
    ax.barh(y, values, color=colors, height=0.58, zorder=3)
    ax.invert_yaxis()

    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=12.5, color=INK)
    top = max(values + [refline or 0])
    ax.set_xlim(0, top * 1.22)
    _clean_axes(ax)
    ax.grid(axis="x", color=LINE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", labelsize=10.5, colors=MUTED)

    for i, v in enumerate(values):
        # 长条把数值放到条内右端，避免压住参考线或画布边缘
        if v > top * 0.72:
            ax.text(v - top * 0.015, i, _num(v, decimals, suffix), va="center",
                    ha="right", fontsize=12.5,
                    color=ORANGE if labels[i] in hi else INK,
                    weight="bold" if labels[i] in hi else "normal", zorder=4)
        else:
            ax.text(v + top * 0.015, i, _num(v, decimals, suffix), va="center",
                    fontsize=12.5, color=ORANGE if labels[i] in hi else INK_SOFT,
                    weight="bold" if labels[i] in hi else "normal", zorder=4)

    if refline is not None:
        ax.axvline(refline, color=RED, linewidth=1.2, linestyle=(0, (4, 3)), zorder=2)
        if refline_label:
            ax.text(refline, len(labels) - 0.45, refline_label,
                    color=RED, fontsize=10.5, ha="center", va="top")

    return _save(fig, out)


def vbar(
    items: Sequence[dict],
    title: str,
    subtitle: str,
    source: str,
    out: Path,
    suffix: str = "",
    decimals: int = 1,
    colors: Sequence[str] | None = None,
    note: str = "",
    callout: str = "",
    label_width: int = 18,
) -> Path:
    """纵向柱状图，适合两期对比。长标签按显示宽度折行。"""
    fig = plt.figure(figsize=(W, H))
    _frame(fig, title, subtitle, source, note, callout)
    ax = fig.add_axes([0.09, 0.22, 0.82, 0.58])

    labels = [i["label"] for i in items]
    values = [float(i["value"]) for i in items]
    cols = list(colors) if colors else [BLUE] * len(values)

    x = list(range(len(labels)))
    ax.bar(x, values, color=cols, width=0.42, zorder=3)
    ax.set_xticks(x)
    ax.set_xticklabels(["\n".join(_wrap(lb, label_width)) for lb in labels],
                       fontsize=12, color=INK)
    ax.set_ylim(0, max(values) * 1.26)
    _clean_axes(ax)
    ax.grid(axis="y", color=LINE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}{suffix}"))
    ax.tick_params(axis="y", labelsize=10.5, colors=MUTED)

    for i, v in enumerate(values):
        ax.text(i, v + max(values) * 0.03, _num(v, decimals, suffix), ha="center",
                fontsize=16, color=INK, weight="bold")

    return _save(fig, out)


def stacked(
    segments: Sequence[dict],
    title: str,
    subtitle: str,
    source: str,
    out: Path,
    note: str = "",
    callout: str = "",
) -> Path:
    """单条 100% 堆叠条，适合占比拆分。小占比段标签外置避免压字。"""
    fig = plt.figure(figsize=(W, H))
    _frame(fig, title, subtitle, source, note, callout)
    ax = fig.add_axes([0.06, 0.34, 0.88, 0.26])

    palette = [ORANGE, BLUE, GREEN, MUTED]
    total = sum(float(s["value"]) for s in segments)
    left = 0.0
    for idx, seg in enumerate(segments):
        v = float(seg["value"])
        w = v / total * 100
        ax.barh([0], [w], left=left, color=palette[idx % len(palette)],
                height=0.66, zorder=3, edgecolor=CREAM, linewidth=2)
        ax.text(left + w / 2, -0.56, seg["label"], ha="center", va="top",
                fontsize=12.5, color=INK)
        if w >= 10:
            ax.text(left + w / 2, 0, f"{v:.1f}%", ha="center", va="center",
                    fontsize=17, color=CREAM, weight="bold", zorder=4)
        else:
            ax.text(left + w - 0.4, 0.44, f"{v:.1f}%", ha="right", va="bottom",
                    fontsize=12, color=INK, weight="bold", zorder=4)
        left += w

    ax.set_xlim(0, 100)
    ax.set_ylim(-1.15, 0.75)
    _clean_axes(ax, hide_left=True)
    ax.set_xticks([])

    return _save(fig, out)


# ---------------------------------------------------------------- 入口


def build(data_path: Path, out_dir: Path, spec: dict) -> list[Path]:
    data = json.loads(data_path.read_text(encoding="utf-8"))
    produced: list[Path] = []

    for name, cfg in spec.items():
        src_ids = cfg.get("source", [])
        if isinstance(src_ids, str):
            src_ids = [src_ids]
        pubs = []
        for sid in src_ids:
            for s in data["sources"]:
                if s["id"] == sid:
                    pubs.append(f"{s['publisher']}《{s['title']}》{s['period']}")
        source_line = "数据来源：" + " ；".join(pubs)

        items = [
            {**it, "value": it.get("value", it.get("count", it.get("growth", 0)))}
            for it in cfg["items"]
        ]
        out = out_dir / f"{name}.svg"
        kind = cfg["kind"]
        common = dict(
            title=cfg["title"],
            subtitle=cfg.get("subtitle", ""),
            source=source_line,
            out=out,
            note=cfg.get("note", ""),
            callout=cfg.get("callout", ""),
        )

        if kind == "hbar":
            produced.append(
                hbar(items, suffix=cfg.get("suffix", ""),
                     decimals=cfg.get("decimals", 0),
                     highlight=cfg.get("highlight", ()),
                     refline=cfg.get("refline"),
                     refline_label=cfg.get("refline_label", ""), **common)
            )
        elif kind == "vbar":
            produced.append(
                vbar(items, suffix=cfg.get("suffix", ""),
                     decimals=cfg.get("decimals", 1),
                     colors=cfg.get("colors"),
                     label_width=cfg.get("label_width", 18), **common)
            )
        elif kind == "stacked":
            produced.append(stacked(items, **common))
        else:
            raise ValueError(f"未知图型 {kind}")

    return produced
