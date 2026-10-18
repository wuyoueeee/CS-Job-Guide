"""CS Job Guide 示意图工具集（架构图 / 流程图 / 时序图）。

与 chartkit 共用一套米白纸感视觉系统，但走手写 SVG 路线：
柱状图表达"数字对比"，架构图表达"结构关系"，两者互补。

排版约定（与 chartkit 一致）：
- 标题左对齐、副标题紧随其下，核心结论右对齐；
- 页脚两行：来源 / 口径说明；
- 箭头一律用 marker 画，不在文本里用箭头字符，避免查看端缺字形；
- 中文字宽按 1 em、ASCII 按 0.56 em 估算，用于自动折行。
"""

from __future__ import annotations

import html
from pathlib import Path
from typing import Sequence

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

FONT = "Microsoft YaHei, PingFang SC, Hiragino Sans GB, sans-serif"
CANVAS_W = 1200

_FOOTER_H = 74
_HEADER_H = 96


# ---------------------------------------------------------------- 基础工具


def _esc(s: str) -> str:
    return html.escape(str(s), quote=True)


def _text_w(s: str, font_size: float) -> float:
    return sum(font_size if ord(c) > 0x2E80 else font_size * 0.56 for c in s)


def _wrap_px(s: str, font_size: float, max_px: float) -> list[str]:
    """按像素宽度折行。"""
    lines, cur, w = [], "", 0.0
    for ch in s:
        cw = _text_w(ch, font_size)
        if w + cw > max_px and cur:
            lines.append(cur)
            cur, w = ch, cw
        else:
            cur += ch
            w += cw
    if cur:
        lines.append(cur)
    return lines or [""]


def _text(x: float, y: float, s: str, size: float, color: str = INK,
          anchor: str = "middle", weight: str = "normal", opacity: float = 1.0) -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" '
        f'fill="{color}" text-anchor="{anchor}" font-weight="{weight}" '
        f'opacity="{opacity}">{_esc(s)}</text>'
    )


def _block_text(x: float, y: float, s: str, size: float, max_px: float,
                color: str = INK, anchor: str = "middle", weight: str = "normal",
                line_height: float | None = None) -> tuple[str, float]:
    """多行文本，返回 (svg, 占用高度)。y 为首行基线。"""
    lh = line_height or size * 1.42
    lines = _wrap_px(s, size, max_px)
    parts = []
    for i, ln in enumerate(lines):
        parts.append(_text(x, y + i * lh, ln, size, color, anchor, weight))
    return "".join(parts), lh * len(lines)


def _rect(x: float, y: float, w: float, h: float, fill: str, stroke: str = "none",
          rx: float = 10, extra: str = "") -> str:
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="1.2" {extra}/>'
    )


def _line(x1: float, y1: float, x2: float, y2: float, color: str = LINE,
          width: float = 1.2, dash: str = "", marker: str = "") -> str:
    d = f' stroke-dasharray="{dash}"' if dash else ""
    m = f' marker-end="{marker}"' if marker else ""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{width}"{d}{m}/>'
    )


def _arrow_defs() -> str:
    return (
        '<defs>'
        f'<marker id="dk-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
        f'markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{MUTED}"/></marker>'
        f'<marker id="dk-arrow-ink" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
        f'markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{INK_SOFT}"/></marker>'
        f'<marker id="dk-arrow-orange" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
        f'markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{ORANGE}"/></marker>'
        '</defs>'
    )


def _wrap_up(svg_body: str, height: float, title: str, subtitle: str,
             source: str, note: str = "", callout: str = "") -> str:
    head = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS_W} {height:.0f}" '
        f'width="{CANVAS_W}" height="{height:.0f}">',
        f'<rect width="{CANVAS_W}" height="{height:.0f}" fill="{CREAM}"/>',
        _arrow_defs(),
        _text(44, 46, title, 25, INK, "start", "bold"),
    ]
    if subtitle:
        head.append(_text(44, 76, subtitle, 13.5, MUTED, "start"))
    if callout:
        head.append(_text(CANVAS_W - 44, 46, callout, 14, ORANGE, "end", "bold"))
    head.append(_line(44, _HEADER_H - 8, CANVAS_W - 44, _HEADER_H - 8))

    foot = [_line(44, height - _FOOTER_H + 14, CANVAS_W - 44, height - _FOOTER_H + 14)]
    y = height - _FOOTER_H + 34
    for ln in _wrap_px(source, 9.5, 1090)[:2]:
        foot.append(_text(44, y, ln, 9.5, MUTED, "start"))
        y += 15
    if note:
        for ln in _wrap_px(f"口径说明：{note}", 9.5, 1090)[:2]:
            foot.append(_text(44, y, ln, 9.5, MUTED, "start"))
            y += 15
    return "\n".join(head + [svg_body] + foot + ["</svg>"])


def _save(svg: str, out: Path) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    text = "\n".join(line.rstrip() for line in svg.split("\n"))
    out.write_text(text, encoding="utf-8")
    return out


# ---------------------------------------------------------------- 架构图


def arch(
    layers: Sequence[dict],
    title: str,
    subtitle: str,
    source: str,
    out: Path,
    note: str = "",
    callout: str = "",
    columns: int = 3,
    gap_label: str = "调用下行 / 响应上行",
    show_flow: bool = True,
) -> Path:
    """分层架构图。

    layers: [{"name": "接入层", "nodes": [{"label", "sub", "tag", "accent"}]}]
    columns: 每层节点按几列排布，超出自动换行。
    """
    pad = 44
    gutter = 116                      # 左侧层名占位
    area_x = pad + gutter
    area_w = CANVAS_W - area_x - pad
    node_gap = 14
    node_w = (area_w - node_gap * (columns - 1)) / columns
    node_h = 62

    body: list[str] = []
    y = _HEADER_H + 18
    layer_boxes: list[tuple[float, float]] = []

    for li, layer in enumerate(layers):
        nodes = layer["nodes"]
        rows = (len(nodes) + columns - 1) // columns
        band_h = rows * (node_h + node_gap) + 22
        body.append(_rect(pad, y, CANVAS_W - 2 * pad, band_h, CREAM_2, LINE, 14))
        # 层名：左侧竖排两字一行更清楚，这里用左对齐多行
        name_lines = _wrap_px(layer["name"], 14.5, gutter - 24)
        ny = y + band_h / 2 - (len(name_lines) - 1) * 10.5
        for ln in name_lines:
            body.append(_text(pad + 16, ny, ln, 14.5, INK, "start", "bold"))
            ny += 21
        if layer.get("desc"):
            body.append(_text(pad + 16, y + band_h - 12, layer["desc"], 11, MUTED, "start"))

        for i, node in enumerate(nodes):
            r, c = divmod(i, columns)
            nx = area_x + c * (node_w + node_gap)
            ny2 = y + 11 + r * (node_h + node_gap)
            accent = bool(node.get("accent"))
            fill = ORANGE_SOFT if accent else "white"
            body.append(_rect(nx, ny2, node_w, node_h, fill, LINE, 10))
            label, _ = _block_text(nx + node_w / 2, ny2 + 25, node["label"], 14.5,
                                   node_w - 18, INK, weight="bold")
            body.append(label)
            if node.get("sub"):
                sub, _ = _block_text(nx + node_w / 2, ny2 + 46, node["sub"], 11.5,
                                     node_w - 18, MUTED)
                body.append(sub)
            if node.get("tag"):
                tag_w = _text_w(node["tag"], 10.5) + 16
                body.append(_rect(nx + node_w - tag_w - 8, ny2 + 6, tag_w, 19,
                                  GREEN_SOFT, "none", 9))
                body.append(_text(nx + node_w - tag_w / 2 - 8, ny2 + 20,
                                  node["tag"], 10.5, GREEN))

        layer_boxes.append((y, y + band_h))
        y += band_h

        if show_flow and li < len(layers) - 1:
            mid_y = y + 13
            cx = area_x + area_w * 0.82
            body.append(_line(cx, y - 2, cx, mid_y - 4, MUTED, 1.4,
                              marker="url(#dk-arrow-ink)"))
            body.append(_text(cx + 10, mid_y + 2, gap_label, 11, MUTED, "start"))
            y += 30

    height = y + _FOOTER_H
    return _save(_wrap_up("".join(body), height, title, subtitle, source, note, callout), out)


# ---------------------------------------------------------------- 流程图


def flow(
    nodes: Sequence[dict],
    edges: Sequence[dict],
    title: str,
    subtitle: str,
    source: str,
    out: Path,
    note: str = "",
    callout: str = "",
    col_width: float = 300,
    row_height: float = 92,
    origin_x: float = 70,
    origin_y: float | None = None,
) -> Path:
    """流程图。节点按 (col, row) 网格摆放，边自动走直线或折线。

    nodes: [{"id", "label", "type": start|process|decision|end, "col", "row",
             "accent", "sub"}]
    edges: [{"from", "to", "label", "kind": normal|yes|no|dash}]
    """
    oy = origin_y if origin_y is not None else _HEADER_H + 34
    pos: dict[str, tuple[float, float]] = {}
    sizes: dict[str, tuple[float, float]] = {}
    body: list[str] = []

    for n in nodes:
        t = n.get("type", "process")
        cx = origin_x + n["col"] * col_width + col_width / 2
        cy = oy + n["row"] * row_height + 46
        pos[n["id"]] = (cx, cy)
        if t == "decision":
            sizes[n["id"]] = (190, 76)
        elif t in ("start", "end"):
            sizes[n["id"]] = (150, 42)
        else:
            sizes[n["id"]] = (col_width - 40, 62)

    # 先画边，再画节点，避免节点盖住线上的文字
    for e in edges:
        a, b = pos[e["from"]], pos[e["to"]]
        aw, ah = sizes[e["from"]]
        bw, bh = sizes[e["to"]]
        dash = e.get("kind") == "dash"
        stroke = ORANGE if e.get("kind") in ("yes", "no") else MUTED
        marker = "url(#dk-arrow-orange)" if e.get("kind") in ("yes", "no") else "url(#dk-arrow)"
        if abs(a[0] - b[0]) < 1:                       # 同列：竖直向下
            x = a[0]
            y1, y2 = a[1] + ah / 2, b[1] - bh / 2
            body.append(_line(x, y1, x, y2 - 1, stroke, 1.5,
                              "5 4" if dash else "", marker))
        else:                                          # 跨列：肘形
            x1, x2 = a[0], b[0]
            y1 = a[1] + ah / 2
            y2 = b[1] - bh / 2
            mid_y = (y1 + y2) / 2
            body.append(
                f'<path d="M {x1:.1f} {y1:.1f} L {x1:.1f} {mid_y:.1f} '
                f'L {x2:.1f} {mid_y:.1f} L {x2:.1f} {y2:.1f}" fill="none" '
                f'stroke="{stroke}" stroke-width="1.5"'
                + (f' stroke-dasharray="5 4"' if dash else "")
                + f' marker-end="{marker}"/>'
            )
        if e.get("label"):
            mx = (a[0] + b[0]) / 2
            my = (a[1] + ah / 2 + b[1] - bh / 2) / 2
            body.append(_text(mx + 8, my - 6, e["label"], 11.5, INK_SOFT, "start", "bold"))

    for n in nodes:
        cx, cy = pos[n["id"]]
        w, h = sizes[n["id"]]
        t = n.get("type", "process")
        accent = bool(n.get("accent"))
        if t == "decision":
            body.append(
                f'<polygon points="{cx:.1f},{cy - h / 2:.1f} {cx + w / 2:.1f},{cy:.1f} '
                f'{cx:.1f},{cy + h / 2:.1f} {cx - w / 2:.1f},{cy:.1f}" '
                f'fill="{ORANGE_SOFT if accent else "white"}" stroke="{LINE}" stroke-width="1.2"/>'
            )
        elif t in ("start", "end"):
            body.append(_rect(cx - w / 2, cy - h / 2, w, h,
                              GREEN_SOFT if t == "start" else ORANGE_SOFT, "none", h / 2))
        else:
            body.append(_rect(cx - w / 2, cy - h / 2, w, h,
                              ORANGE_SOFT if accent else "white", LINE, 10))
        lines = _wrap_px(n["label"], 13.5 if t == "decision" else 14, w - 20)
        ty = cy - (len(lines) - 1) * 10 + (4.5 if t != "decision" else 4.5)
        for ln in lines:
            body.append(_text(cx, ty, ln, 13.5 if t == "decision" else 14, INK, weight="bold"))
            ty += 20
        if n.get("sub"):
            body.append(_text(cx, cy + h / 2 - 10, n["sub"], 11, MUTED))

    max_row = max(n["row"] for n in nodes)
    height = oy + max_row * row_height + 60 + _FOOTER_H
    return _save(_wrap_up("".join(body), height, title, subtitle, source, note, callout), out)


# ---------------------------------------------------------------- 时序图


def seq(
    actors: Sequence[str],
    messages: Sequence[dict],
    title: str,
    subtitle: str,
    source: str,
    out: Path,
    note: str = "",
    callout: str = "",
) -> Path:
    """时序图。

    messages: [{"from": 下标, "to": 下标, "text", "kind": sync|return|async|self,
                "note": 右侧小字注释}]
    """
    n = len(actors)
    left, right = 130, CANVAS_W - 130
    span = (right - left) / max(n - 1, 1)
    xs = [left + i * span for i in range(n)]
    top = _HEADER_H + 46
    msg_h = 46

    body: list[str] = []
    # 参与者头与生命线
    for i, a in enumerate(actors):
        w = max(_text_w(a, 14) + 34, 96)
        body.append(_rect(xs[i] - w / 2, top - 34, w, 36,
                          ORANGE_SOFT if i == 0 else BLUE_SOFT, "none", 18))
        body.append(_text(xs[i], top - 10, a, 14, INK, weight="bold"))

    y = top + 34
    for m in messages:
        fi, ti = m["from"], m["to"]
        kind = m.get("kind", "sync")
        x1, x2 = xs[fi], xs[ti]
        if kind == "self":
            body.append(
                f'<path d="M {x1:.1f} {y - 12:.1f} h 46 v 26 h -46" fill="none" '
                f'stroke="{MUTED}" stroke-width="1.4" marker-end="url(#dk-arrow)"/>'
            )
            body.append(_text(x1 + 58, y + 2, m["text"], 12.5, INK, "start"))
        else:
            dash = kind == "return"
            stroke = BLUE if kind == "async" else MUTED
            body.append(_line(x1, y, x2, y, stroke, 1.5, "5 4" if dash else ""))
            if not dash:
                body.append(_line(x1, y, x2, y - 0.5, stroke, 1.5,
                                  marker="url(#dk-arrow)"))
            lx = min(x1, x2) + 10 if x1 != x2 else x1 + 12
            body.append(_text(lx, y - 9, m["text"], 12.5, INK_SOFT, "start", "bold"))
        if m.get("note"):
            body.append(_text(CANVAS_W - 44, y - 9, m["note"], 11, ORANGE, "end", "bold"))
        y += msg_h

    for i in range(n):
        body.append(_line(xs[i], top + 2, xs[i], y - msg_h + 18, LINE, 1.2, "4 4"))

    height = y + 10 + _FOOTER_H
    return _save(_wrap_up("".join(body), height, title, subtitle, source, note, callout), out)


# ---------------------------------------------------------------- 入口


def build(out_dir: Path, spec: dict) -> list[Path]:
    """规格驱动入口，方便和 chartkit 一样批量生成。

    spec: {文件名: {"kind": "arch"|"flow"|"seq", ...其余参数}}
    """
    produced = []
    for name, cfg in spec.items():
        kind = cfg["kind"]
        common = dict(
            title=cfg["title"],
            subtitle=cfg.get("subtitle", ""),
            source=cfg.get("source", "来源：见正文"),
            out=out_dir / f"{name}.svg",
            note=cfg.get("note", ""),
            callout=cfg.get("callout", ""),
        )
        if kind == "arch":
            produced.append(arch(cfg["layers"], columns=cfg.get("columns", 3),
                                 gap_label=cfg.get("gap_label", "调用下行 / 响应上行"),
                                 show_flow=cfg.get("show_flow", True), **common))
        elif kind == "flow":
            produced.append(flow(cfg["nodes"], cfg["edges"],
                                 col_width=cfg.get("col_width", 300),
                                 row_height=cfg.get("row_height", 92),
                                 origin_x=cfg.get("origin_x", 70), **common))
        elif kind == "seq":
            produced.append(seq(cfg["actors"], cfg["messages"], **common))
        else:
            raise ValueError(f"未知图型 {kind}")
    return produced
