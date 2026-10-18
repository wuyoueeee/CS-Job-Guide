"""生成 README 用的三张总览图。

数据图回答"多少"，示意图回答"怎么连"，这三张回答"从哪开始、仓库里有什么、项目专题长什么样"。
沿用 diagramkit 的米白纸感视觉系统，输出 SVG 后调 sharp 栅格化成 PNG（README 用 PNG 更稳）。

用法：
    python tools/build_readme_visuals.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from content_kit import diagramkit as dk  # noqa: E402

OUT = ROOT / "docs" / "images"
SRC = ROOT / ".workbuddy" / "preview" / "readme"

W = 1400


def _canvas(body: str, width: int, height: int) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}">'
        f'<rect width="{width}" height="{height}" fill="{dk.CREAM}"/>'
        f"{body}</svg>"
    )


def _title(body: list[str], title: str, subtitle: str, callout: str = "") -> None:
    body.append(dk._text(52, 48, title, 27, dk.INK, "start", "bold"))
    if subtitle:
        body.append(dk._text(52, 78, subtitle, 14.5, dk.MUTED, "start"))
    if callout:
        body.append(dk._text(W - 52, 48, callout, 14.5, dk.ORANGE, "end", "bold"))


# ---------------------------------------------------------------- 图一：七环节


STATIONS = [
    ("1", "方向定位", "目标岗位清单和优先级", "盘经历，出匹配度表"),
    ("2", "简历", "3 段可验证经历", "把流水账改成 STAR"),
    ("3", "项目", "1 个主项目加追问准备", "生成追问清单来自测"),
    ("4", "基础复习", "一周计划和错题本", "按薄弱项出题陪练"),
    ("5", "面试", "3 分钟讲解稿和复盘", "模拟面试并结构化复盘"),
    ("6", "投递管理", "第一版投递表", "整理渠道，看漏斗"),
    ("7", "offer 决策", "量化对比和风险清单", "整理决策表，列风险"),
]


def route() -> str:
    height = 436
    margin = 52
    step = (W - margin * 2) / len(STATIONS)
    xs = [margin + step * (i + 0.5) for i in range(len(STATIONS))]
    spine = 212

    body: list[str] = []
    _title(
        body,
        "用 AI 求职的七个环节",
        "每个环节都有一件要交出去的东西，也有一件 AI 能替你做的事",
        "一条主线，七个交付物",
    )

    body.append(dk._line(xs[0], spine, xs[-1], spine, dk.LINE, 2.4))

    for i, (num, name, deliver, ai) in enumerate(STATIONS):
        x = xs[i]
        body.append(dk._rect(x - 19, spine - 19, 38, 38, dk.ORANGE, "none", 19))
        body.append(dk._text(x, spine + 5.5, num, 15, "#FFFFFF", "middle", "bold"))
        body.append(dk._text(x, spine + 52, name, 18.5, dk.INK, "middle", "bold"))

        svg, h = dk._block_text(
            x, spine + 82, deliver, 13, step - 22, dk.MUTED, "middle"
        )
        body.append(svg)
        svg, _ = dk._block_text(
            x, spine + 84 + h + 8, "AI " + ai, 13, step - 22, dk.ORANGE, "middle"
        )
        body.append(svg)

    body.append(
        dk._text(
            W / 2,
            height - 26,
            "灰字是这一步要交出的东西，橙字是 AI 能替你做的那部分；细节和提示词在各节对应文章里",
            11.5,
            dk.MUTED,
        )
    )
    return _canvas("".join(body), W, height)


# ---------------------------------------------------------------- 图二：内容全景


MAP = [
    (
        "路线与规划",
        "15 篇",
        [
            "校招时间线怎么排",
            "岗位路线图五种方向",
            "30 天训练营",
            "按人群使用路线",
            "求职季作战手册",
        ],
    ),
    (
        "简历与项目",
        "24 篇",
        [
            "简历证据库与模板",
            "简历改造案例库",
            "项目实战十篇拆解",
            "作品集模板",
            "STAR 原则与改法",
        ],
    ),
    (
        "面试知识",
        "47 篇",
        [
            "Java 后端与 JVM",
            "MySQL 基础到高级",
            "面试官评分视角",
            "真实面经十八篇",
            "算法与代码面试",
        ],
    ),
    (
        "AI 与大模型",
        "26 篇",
        [
            "用 AI 求职全流程",
            "大模型使用十一篇",
            "AI 应用研发十篇",
            "AI 岗位数据图谱",
            "AI 求职行动手册",
        ],
    ),
    (
        "签约与发展",
        "9 篇",
        [
            "offer 决策表",
            "三方与合同避坑",
            "第一份工作怎么选",
            "校招第一年生存手册",
            "技术人的成长路径",
        ],
    ),
]


def content_map() -> str:
    height = 452
    margin = 52
    gap = 16
    cols = len(MAP)
    cw = (W - margin * 2 - gap * (cols - 1)) / cols
    top = 112
    ch = 274

    body: list[str] = []
    _title(
        body,
        "这个仓库里有什么",
        "五个内容池，按你现在卡在哪一步挑一个进去",
        "121 篇正文",
    )

    for i, (group, count, items) in enumerate(MAP):
        x = margin + i * (cw + gap)
        body.append(dk._rect(x, top, cw, ch, dk.CREAM_2, dk.LINE, 12))
        body.append(dk._text(x + 18, top + 32, group, 17, dk.INK, "start", "bold"))
        body.append(dk._text(x + cw - 18, top + 32, count, 12.5, dk.ORANGE, "end", "bold"))
        body.append(dk._line(x + 18, top + 46, x + cw - 18, top + 46, dk.LINE))

        y = top + 74
        for item in items:
            body.append(
                f'<circle cx="{x + 22:.1f}" cy="{y - 4:.1f}" r="2.6" fill="{dk.ORANGE}"/>'
            )
            svg, h = dk._block_text(
                x + 34, y, item, 13, cw - 50, dk.INK_SOFT, "start"
            )
            body.append(svg)
            y += h + 20

    body.append(
        dk._text(
            W / 2,
            height - 30,
            "另有投稿规范与索引 6 篇、模板 5 个，都在完整目录里",
            10.5,
            dk.MUTED,
        )
    )
    return _canvas("".join(body), W, height)


# ---------------------------------------------------------------- 图三：项目导览


PROJECTS = [
    ("RAG 检索增强", "2.3 秒", "端到端延迟预算，生成占 86%", "切分策略、混合检索、权限下推、评测集"),
    ("Agent 工具调用", "17.3K", "20 轮不压缩的上下文，超 16K 窗口", "工具设计、参数校验、三级权限、循环防护"),
    ("AI 评测平台", "57.5 分钟", "200 条 × 3 版本的一次回归", "测试集资产化、并发执行、回归比对"),
    ("结构化抽取", "0.76", "推荐置信度阈值，上限 0.90", "Schema 约束、校验重试、字段级置信度"),
    ("文档智能解析", "6.6 秒", "一页 PDF 全链路，表格还原 94%", "分级路由、版面分析、表格结构、阅读顺序"),
]

STEPS = ["先算容量与延迟", "再定架构与取舍", "最后给验证方法"]


def projects() -> str:
    height = 470
    margin = 52
    gap = 16
    cols = len(PROJECTS)
    cw = (W - margin * 2 - gap * (cols - 1)) / cols
    top = 186
    ch = 214

    body: list[str] = []
    _title(
        body,
        "项目实战：五个大模型项目，十篇拆解",
        "每个项目都从算账开始，不是先堆技术栈",
        "27 张数据图 + 9 张示意图",
    )

    chip_w, chip_h, arrow_gap = 196, 34, 44
    total = chip_w * len(STEPS) + arrow_gap * (len(STEPS) - 1)
    cx = (W - total) / 2
    cy = 112
    for i, s in enumerate(STEPS):
        x = cx + i * (chip_w + arrow_gap)
        body.append(dk._rect(x, cy, chip_w, chip_h, dk.BLUE_SOFT, "none", 17))
        body.append(dk._text(x + chip_w / 2, cy + 22, s, 13.5, dk.INK, "middle", "bold"))
        if i < len(STEPS) - 1:
            body.append(
                dk._line(
                    x + chip_w + 6,
                    cy + chip_h / 2,
                    x + chip_w + arrow_gap - 8,
                    cy + chip_h / 2,
                    dk.MUTED,
                    1.4,
                    "",
                    "url(#dk-arrow)",
                )
            )

    for i, (name, big, unit, learn) in enumerate(PROJECTS):
        x = margin + i * (cw + gap)
        body.append(dk._rect(x, top, cw, ch, dk.CREAM_2, dk.LINE, 12))
        body.append(dk._text(x + 18, top + 32, name, 16, dk.INK, "start", "bold"))
        body.append(dk._text(x + 18, top + 82, big, 24, dk.ORANGE, "start", "bold"))
        svg, h = dk._block_text(x + 18, top + 106, unit, 12, cw - 36, dk.MUTED, "start")
        body.append(svg)
        body.append(dk._line(x + 18, top + 148, x + cw - 18, top + 148, dk.LINE))
        svg, _ = dk._block_text(
            x + 18, top + 172, learn, 12, cw - 36, dk.INK_SOFT, "start"
        )
        body.append(svg)

    body.append(
        dk._text(
            W / 2,
            height - 30,
            "传统后端五篇作为副线：秒杀、短链、IM、网关、权限，同样按算账、设计、验证来写",
            10.5,
            dk.MUTED,
        )
    )
    return _canvas("".join(body), W, height)


# ---------------------------------------------------------------- 入口


def _rasterize(svg_path: Path, png_path: Path) -> bool:
    node = Path(sys.executable).parent
    for cand in ("node", "node.exe"):
        try:
            subprocess.run(
                [
                    str(cand),
                    str(ROOT / "tools" / "svg2png.js"),
                    str(svg_path),
                    str(png_path),
                    "1400",
                ],
                check=True,
                capture_output=True,
                cwd=str(ROOT),
                env={**_env(), "NODE_PATH": _node_modules()},
            )
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            continue
    return False


def _env() -> dict:
    import os

    return dict(os.environ)


def _node_modules() -> str:
    import os

    return os.environ.get(
        "NODE_PATH", "C:/Users/xw/.workbuddy/binaries/node/workspace/node_modules"
    )


def main() -> None:
    SRC.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    figures = {
        "readme-route": route(),
        "readme-map": content_map(),
        "readme-projects": projects(),
    }
    for name, svg in figures.items():
        svg_path = dk._save(svg, SRC / f"{name}.svg")
        png_path = OUT / f"{name}.png"
        ok = _rasterize(svg_path, png_path)
        size = f"{png_path.stat().st_size / 1024:.0f} KB" if ok else "未生成"
        print(f"  {name}  svg={svg_path.stat().st_size / 1024:.0f}KB  png={size}")
    if not all((OUT / f"{n}.png").exists() for n in figures):
        print("PNG 未全部生成，可用 node tools/svg2png.js 手动转换")
    print(f"\n输出目录：{OUT}")


if __name__ == "__main__":
    main()
