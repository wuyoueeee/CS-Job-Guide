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
    # matplotlib 导出的 SVG 每行末尾带空格，清掉后再落盘，
    # 否则 git diff --check 会报 trailing whitespace
    text = out.read_text(encoding="utf-8")
    cleaned = "\n".join(line.rstrip() for line in text.split("\n"))
    if cleaned != text:
        out.write_text(cleaned, encoding="utf-8")
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
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))
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
    """单条 100% 堆叠条，适合占比拆分。

    注意：segments 的 value 是原始值，占比由 value / total 计算，
    图上一律显示计算出的百分比，不显示原始值。
    窄段（占比小于 15%）的标签下沉到单独一行，相邻窄段交错排列避免重叠。
    """
    fig = plt.figure(figsize=(W, H))
    _frame(fig, title, subtitle, source, note, callout)
    ax = fig.add_axes([0.06, 0.34, 0.88, 0.26])

    palette = [ORANGE, BLUE, GREEN, MUTED]
    total = sum(float(s["value"]) for s in segments)

    segs = []
    left = 0.0
    for idx, seg in enumerate(segments):
        v = float(seg["value"])
        w = v / total * 100
        segs.append({"idx": idx, "label": seg["label"], "v": v, "w": w, "start": left})
        left += w

    for s in segs:
        w, start, idx = s["w"], s["start"], s["idx"]
        ax.barh([0], [w], left=start, color=palette[idx % len(palette)],
                height=0.66, zorder=3, edgecolor=CREAM, linewidth=2)
        if w >= 10:
            ax.text(start + w / 2, 0, f"{w:.1f}%", ha="center", va="center",
                    fontsize=17, color=CREAM, weight="bold", zorder=4)
        else:
            # 窄段放不下文字，百分比挂到段上方
            ax.text(start + w / 2, 0.44, f"{w:.1f}%", ha="center", va="bottom",
                    fontsize=12, color=INK, weight="bold", zorder=4)

    # 标签行：宽段一行；窄段下沉，相邻窄段交替到两个更低的层级
    narrow_rows = [-0.60, -1.02, -1.44]
    last_narrow_row = -1
    for s in segs:
        w, start = s["w"], s["start"]
        if w < 15:
            row = (last_narrow_row + 1) % len(narrow_rows)
            last_narrow_row = row
            y = narrow_rows[row]
        else:
            y = -0.60
            last_narrow_row = -1
        ax.text(start + w / 2, y, s["label"], ha="center", va="top",
                fontsize=12.5, color=INK)

    ax.set_xlim(0, 100)
    ax.set_ylim(-1.62, 0.75)
    _clean_axes(ax, hide_left=True)
    ax.set_xticks([])

    return _save(fig, out)


# ---------------------------------------------------------------- 新图型


def _push_apart(ys: list[float], min_gap: float, lo: float, hi: float) -> list[float]:
    """把一叠纵向标签按最小间隔错开（简易贪心，先按原序推）。"""
    ys = sorted(ys)
    for i in range(1, len(ys)):
        if ys[i] - ys[i - 1] < min_gap:
            ys[i] = ys[i - 1] + min_gap
    overflow = ys[-1] - hi if ys else 0
    if overflow > 0:
        ys = [y - overflow for y in ys]
    return ys


def line(
    series: Sequence[dict],
    x_labels: Sequence[str],
    title: str,
    subtitle: str,
    source: str,
    out: Path,
    y_suffix: str = "",
    decimals: int = 0,
    y_decimals: int | None = None,
    y_min: float | None = None,
    note: str = "",
    callout: str = "",
    y_title: str = "",
    markers: Sequence[dict] = (),
    legend_rows: int = 1,
) -> Path:
    """多序列折线图，适合看趋势和拐点。

    series: [{"label", "values", "color", "dash"(可选)}]
    markers: 竖参考线 [{"x": 下标, "label": "16K 窗口"}]
    """
    fig = plt.figure(figsize=(W, H))
    _frame(fig, title, subtitle, source, note, callout)
    ax = fig.add_axes([0.10, 0.22, 0.86, 0.58])

    x = list(range(len(x_labels)))
    ends = []
    for s in series:
        vals = [float(v) for v in s["values"]]
        color = s.get("color") or BLUE
        ax.plot(x, vals, color=color, linewidth=2.6, zorder=3,
                linestyle=s.get("dash", "-"), marker="o", markersize=6,
                markerfacecolor=color, markeredgecolor=CREAM, markeredgewidth=1.2,
                label=s["label"])
        ends.append({"label": s["label"], "y": vals[-1], "color": color})

    # 末端数值标签：相邻太近的按最小间隔错开；末值相同的序列只标一次
    ydec = decimals if y_decimals is None else y_decimals
    top = max(float(v) for s in series for v in s["values"])
    bottom = min(float(v) for s in series for v in s["values"]) if y_min is None else y_min
    gap = (top - bottom) * 0.07
    uniq: list[dict] = []
    for e in sorted(ends, key=lambda d: d["y"]):
        if uniq and abs(uniq[-1]["y"] - e["y"]) < gap * 0.5:
            continue
        uniq.append(e)
    ys = _push_apart([e["y"] for e in uniq], gap, bottom, top)
    for e, yy in zip(uniq, ys):
        ax.text(len(x_labels) - 1 + 0.15, yy, f"{e['y']:,.{ydec}f}{y_suffix}",
                fontsize=12.5, color=e["color"], va="center", weight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(x_labels, fontsize=12, color=INK)
    ax.set_xlim(-0.3, len(x_labels) - 1 + 0.9)
    ax.set_ylim(bottom, top * 1.22 if y_min is None else top + (top - bottom) * 0.30)
    _clean_axes(ax)
    ax.grid(axis="y", color=LINE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda v, _: f"{v:,.{ydec}f}{y_suffix}"))
    ax.tick_params(axis="y", labelsize=10.5, colors=MUTED)
    if y_title:
        ax.text(-0.085, 0.5, y_title, transform=ax.transAxes, rotation=90,
                va="center", ha="center", fontsize=11, color=MUTED)

    for m in markers:
        mx = m["x"]
        ax.axvline(mx, color=RED, linewidth=1.2, linestyle=(0, (4, 3)), zorder=2)
        ax.text(mx, top + (top - bottom) * 0.12, m.get("label", ""), color=RED,
                fontsize=11, ha="center", va="top")

    ax.legend(loc="upper left", frameon=False, fontsize=12, ncol=legend_rows,
              labelcolor=INK, handlelength=1.6)
    return _save(fig, out)


def grouped(
    groups: Sequence[str],
    series: Sequence[dict],
    title: str,
    subtitle: str,
    source: str,
    out: Path,
    y_suffix: str = "",
    decimals: int = 1,
    note: str = "",
    callout: str = "",
    label_width: int = 10,
) -> Path:
    """分组柱状图，适合同一维度下多方案横向对比。

    groups: x 轴分组名；series: [{"label", "values", "color"}]
    """
    fig = plt.figure(figsize=(W, H))
    _frame(fig, title, subtitle, source, note, callout)
    ax = fig.add_axes([0.09, 0.22, 0.88, 0.56])

    n = len(series)
    x = list(range(len(groups)))
    width = 0.74 / n
    top = max(float(v) for s in series for v in s["values"])
    for i, s in enumerate(series):
        vals = [float(v) for v in s["values"]]
        color = s.get("color") or [ORANGE, BLUE, GREEN, MUTED][i % 4]
        off = (i - (n - 1) / 2) * width
        ax.bar([xx + off for xx in x], vals, width=width * 0.9, color=color,
               zorder=3, label=s["label"])
        for xx, v in zip(x, vals):
            ax.text(xx + off, v + top * 0.025, f"{v:,.{decimals}f}{y_suffix}",
                    ha="center", va="bottom", fontsize=11, color=INK_SOFT)

    ax.set_xticks(x)
    ax.set_xticklabels(["\n".join(_wrap(g, label_width)) for g in groups],
                       fontsize=12.5, color=INK)
    ax.set_ylim(0, top * 1.30)
    _clean_axes(ax)
    ax.grid(axis="y", color=LINE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda v, _: f"{v:,.{decimals}f}{y_suffix}"))
    ax.tick_params(axis="y", labelsize=10.5, colors=MUTED)
    ax.legend(loc="upper right", frameon=False, fontsize=12, ncol=n,
              labelcolor=INK, handlelength=1.2, columnspacing=1.2)
    return _save(fig, out)


def scatter(
    points: Sequence[dict],
    title: str,
    subtitle: str,
    source: str,
    out: Path,
    x_title: str = "",
    y_title: str = "",
    x_suffix: str = "",
    y_suffix: str = "",
    note: str = "",
    callout: str = "",
    x_decimals: int = 0,
    y_decimals: int = 0,
    label_points: bool = True,
    zones: Sequence[dict] = (),
) -> Path:
    """散点图，可带分组折线，适合看权衡关系和分布。

    points: [{"x", "y", "label", "color", "group", "size"}]
    zones: 背景分区 [{"x0","x1","label","color"}]，用于标注可接受区间
    """
    fig = plt.figure(figsize=(W, H))
    _frame(fig, title, subtitle, source, note, callout)
    ax = fig.add_axes([0.11, 0.22, 0.85, 0.58])

    for z in zones:
        ax.axvspan(z["x0"], z["x1"], color=z.get("color", GREEN_SOFT), alpha=0.55, zorder=0)
        ax.text((z["x0"] + z["x1"]) / 2, 0.965, z.get("label", ""),
                transform=ax.get_xaxis_transform(), ha="center", va="top",
                fontsize=11.5, color=INK_SOFT)

    groups: dict[str, list[dict]] = {}
    for p in points:
        groups.setdefault(p.get("group", ""), []).append(p)

    for gname, pts in groups.items():
        pts = sorted(pts, key=lambda d: d["x"])
        if gname:
            ax.plot([p["x"] for p in pts], [p["y"] for p in pts],
                    color=pts[0].get("color") or BLUE, linewidth=1.8,
                    linestyle=(0, (3, 2)), zorder=2, alpha=0.85)
        for p in pts:
            ax.scatter([p["x"]], [p["y"]], s=p.get("size", 90),
                       color=p.get("color") or BLUE, zorder=4,
                       edgecolor=CREAM, linewidth=1.2)

    # 标签统一后画，避免被分区背景盖住
    ymax = max(p["y"] for p in points)
    for p in points:
        if label_points and p.get("label"):
            ax.annotate(p["label"], (p["x"], p["y"]),
                        textcoords="offset points", xytext=(0, 11),
                        ha="center", fontsize=11.5, color=INK, weight="bold")

    xs = [p["x"] for p in points]
    ax.set_xlim(min(xs) - (max(xs) - min(xs)) * 0.08, max(xs) + (max(xs) - min(xs)) * 0.10)
    ax.set_ylim(0, ymax * 1.22)
    _clean_axes(ax)
    ax.grid(axis="y", color=LINE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.{x_decimals}f}{x_suffix}"))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.{y_decimals}f}{y_suffix}"))
    ax.tick_params(labelsize=10.5, colors=MUTED)
    if x_title:
        ax.set_xlabel(x_title, fontsize=11.5, color=MUTED, labelpad=8)
    if y_title:
        ax.set_ylabel(y_title, fontsize=11.5, color=MUTED, labelpad=8)
    return _save(fig, out)


def matrix(
    rows: Sequence[str],
    cols: Sequence[str],
    cells: Sequence[Sequence[dict]],
    title: str,
    subtitle: str,
    source: str,
    out: Path,
    note: str = "",
    callout: str = "",
    row_label: str = "",
    col_label: str = "",
) -> Path:
    """矩阵热力图，适合测试矩阵与指标对照。

    cells[r][c] = {"level": 0/1/2, "text": "通过"}，level 决定底色。
    """
    fig = plt.figure(figsize=(W, H))
    _frame(fig, title, subtitle, source, note, callout)
    ax = fig.add_axes([0.20, 0.16, 0.72, 0.68])

    palette = {0: GREEN_SOFT, 1: ORANGE_SOFT, 2: "#F2C9C4"}
    fg = {0: GREEN, 1: "#B4552F", 2: RED}
    nr, nc = len(rows), len(cols)
    for r in range(nr):
        for c in range(nc):
            cell = cells[r][c]
            lv = int(cell.get("level", 0))
            ax.add_patch(
                plt.Rectangle((c, nr - 1 - r), 0.94, 0.94,
                              facecolor=palette.get(lv, CREAM_2),
                              edgecolor=CREAM, linewidth=2.4, zorder=2)
            )
            ax.text(c + 0.47, nr - 1 - r + 0.47, cell.get("text", ""),
                    ha="center", va="center", fontsize=12.5,
                    color=fg.get(lv, INK), weight="bold", zorder=3)

    ax.set_xlim(0, nc)
    ax.set_ylim(0, nr)
    ax.set_xticks([c + 0.47 for c in range(nc)])
    ax.set_xticklabels(["\n".join(_wrap(cl, 12)) for cl in cols],
                       fontsize=12, color=INK)
    ax.set_yticks([nr - 1 - r + 0.47 for r in range(nr)])
    ax.set_yticklabels(rows, fontsize=12, color=INK)
    ax.tick_params(length=0)
    for side in ("top", "right", "bottom", "left"):
        ax.spines[side].set_visible(False)
    if row_label:
        ax.text(-0.02, 1.02, row_label, transform=ax.transAxes, ha="right",
                fontsize=11.5, color=MUTED)
    if col_label:
        ax.text(1.0, 1.02, col_label, transform=ax.transAxes, ha="right",
                fontsize=11.5, color=MUTED)
    return _save(fig, out)


def radar(
    axes: Sequence[str],
    series: Sequence[dict],
    title: str,
    subtitle: str,
    source: str,
    out: Path,
    note: str = "",
    callout: str = "",
    max_value: float = 100,
) -> Path:
    """雷达图，适合两个方案的多维对比。

    axes: 维度名；series: [{"label", "values", "color"}]
    """
    import numpy as np

    fig = plt.figure(figsize=(W, H))
    _frame(fig, title, subtitle, source, note, callout)
    ax = fig.add_axes([0.16, 0.10, 0.68, 0.62], projection="polar")

    n = len(axes)
    angles = [i / n * 2 * np.pi for i in range(n)]
    closed = angles + angles[:1]

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles)
    ax.set_xticklabels(axes, fontsize=12.5, color=INK)
    ax.set_ylim(0, max_value)
    ax.set_yticks([max_value * f for f in (0.25, 0.5, 0.75, 1.0)])
    ax.set_yticklabels([f"{max_value * f:,.0f}" for f in (0.25, 0.5, 0.75, 1.0)],
                       fontsize=9.5, color=MUTED)
    ax.grid(color=LINE, linewidth=0.9)
    ax.spines["polar"].set_color(LINE)
    ax.tick_params(pad=8)

    for s in series:
        vals = [float(v) for v in s["values"]]
        color = s.get("color") or BLUE
        ax.plot(closed, vals + vals[:1], color=color, linewidth=2.4, zorder=3,
                label=s["label"])
        ax.fill(closed, vals + vals[:1], color=color, alpha=0.14, zorder=2)

    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.20), frameon=False,
              fontsize=12.5, ncol=len(series), labelcolor=INK)
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
        raw = cfg.get("items", [])

        if kind == "hbar":
            items = [
                {**it, "value": it.get("value", it.get("count", it.get("growth", 0)))}
                for it in raw
            ]
            produced.append(
                hbar(items, suffix=cfg.get("suffix", ""),
                     decimals=cfg.get("decimals", 0),
                     highlight=cfg.get("highlight", ()),
                     refline=cfg.get("refline"),
                     refline_label=cfg.get("refline_label", ""), **common)
            )
        elif kind == "vbar":
            items = [
                {**it, "value": it.get("value", it.get("count", it.get("growth", 0)))}
                for it in raw
            ]
            produced.append(
                vbar(items, suffix=cfg.get("suffix", ""),
                     decimals=cfg.get("decimals", 1),
                     colors=cfg.get("colors"),
                     label_width=cfg.get("label_width", 18), **common)
            )
        elif kind == "stacked":
            items = [
                {**it, "value": it.get("value", it.get("count", it.get("growth", 0)))}
                for it in raw
            ]
            produced.append(stacked(items, **common))
        elif kind == "line":
            produced.append(
                line(raw, cfg["x_labels"], y_suffix=cfg.get("suffix", ""),
                     decimals=cfg.get("decimals", 0),
                     y_decimals=cfg.get("y_decimals"),
                     y_min=cfg.get("y_min"),
                     y_title=cfg.get("y_title", ""),
                     markers=cfg.get("markers", ()),
                     legend_rows=cfg.get("legend_rows", 1), **common)
            )
        elif kind == "grouped":
            produced.append(
                grouped(cfg["groups"], raw, y_suffix=cfg.get("suffix", ""),
                        decimals=cfg.get("decimals", 1),
                        label_width=cfg.get("label_width", 10), **common)
            )
        elif kind == "scatter":
            produced.append(
                scatter(raw, x_title=cfg.get("x_title", ""),
                        y_title=cfg.get("y_title", ""),
                        x_suffix=cfg.get("x_suffix", ""),
                        y_suffix=cfg.get("y_suffix", ""),
                        x_decimals=cfg.get("x_decimals", 0),
                        y_decimals=cfg.get("y_decimals", 0),
                        label_points=cfg.get("label_points", True),
                        zones=cfg.get("zones", ()), **common)
            )
        elif kind == "matrix":
            produced.append(
                matrix(cfg["rows"], cfg["cols"], cfg["cells"],
                       row_label=cfg.get("row_label", ""),
                       col_label=cfg.get("col_label", ""), **common)
            )
        elif kind == "radar":
            produced.append(
                radar(cfg["axes"], raw, max_value=cfg.get("max_value", 100), **common)
            )
        else:
            raise ValueError(f"未知图型 {kind}")

    return produced
