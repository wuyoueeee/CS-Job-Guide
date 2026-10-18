from __future__ import annotations

import html
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import markdown
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "docs" / "AI应用研发"
OUTPUT_DIR = ROOT / "wechat-ai-rd"
ASSET_DIR = OUTPUT_DIR / "assets"
ARTICLE_DIR = OUTPUT_DIR / "articles"

WIDTH = 1200
HEIGHT = 675
COLORS = {
    "ink": "#17233D",
    "muted": "#65728A",
    "navy": "#17233D",
    "navy_2": "#24375D",
    "cream": "#F7F4EE",
    "cream_2": "#FFFDF8",
    "orange": "#F27649",
    "orange_light": "#F9D3BF",
    "blue": "#5D78B7",
    "blue_light": "#DDE5F7",
    "green": "#4E8F7C",
    "green_light": "#DCEDE6",
    "line": "#E6DED1",
    "white": "#FFFFFF",
}


@dataclass(frozen=True)
class Article:
    number: str
    filename: str
    short_title: str
    subtitle: str
    digest: str
    keywords: tuple[str, ...]
    flow: tuple[str, ...]
    checklist: tuple[str, ...]

    @property
    def slug(self) -> str:
        return Path(self.filename).stem


ARTICLES: tuple[Article, ...] = (
    Article(
        "01",
        "01-岗位能力地图与十二周路线.md",
        "岗位能力地图",
        "用十二周建立可交付的 AI 应用研发能力",
        "从岗位问题出发，拆出后端基础、模型应用、系统设计与业务表达四层能力。",
        ("上下文", "任务拆解", "评测", "性能", "安全"),
        ("后端基础", "模型调用", "RAG", "Agent", "评测观测"),
        ("完成一条可运行链路", "每周留下可验证产物", "用业务指标描述项目", "准备一个失败案例"),
    ),
    Article(
        "02",
        "02-Agent系统设计与工程化.md",
        "Agent 系统设计",
        "先做可控工作流，再谈自主规划",
        "Agent 的价值不是循环调用模型，而是在可验证边界中管理状态、工具和失败恢复。",
        ("状态", "编排", "工具", "重试", "边界"),
        ("用户目标", "任务拆解", "工具调用", "结果校验", "失败恢复"),
        ("先判断是否真的需要 Agent", "显式保存关键状态", "限制反思和重试次数", "为工具失败设计退路"),
    ),
    Article(
        "03",
        "03-RAG从检索到评测.md",
        "RAG 检索链路",
        "从接入向量库走向可评测系统",
        "一个可靠的 RAG 系统要把分块、召回、排序、上下文拼装和生成评测拆开验证。",
        ("分块", "召回", "排序", "上下文", "评测"),
        ("原始文档", "结构化分块", "混合检索", "上下文拼装", "答案评测"),
        ("准备代表性问题集", "区分检索错和生成错", "记录召回证据", "持续回归失败样本"),
    ),
    Article(
        "04",
        "04-ToolCalling与MCP.md",
        "Tool Calling 与 MCP",
        "让模型调用真实系统，也守住边界",
        "工具调用首先是 API 设计问题：参数要清晰、权限要分级、副作用要可控。",
        ("Schema", "权限", "副作用", "MCP", "审计"),
        ("识别意图", "选择工具", "参数校验", "执行确认", "结果审计"),
        ("只读和写操作分级", "写操作增加确认步骤", "外部内容视为不可信输入", "记录参数与执行结果"),
    ),
    Article(
        "05",
        "05-评测可观测与安全.md",
        "评测、观测与安全",
        "把失败变成可以定位、回归和优化的数据",
        "上线前先建立失败分类、评测集、Trace 和降级策略，再谈规模化增长。",
        ("评测集", "Trace", "指标", "降级", "安全"),
        ("收集样本", "离线评测", "线上观测", "失败归因", "回归优化"),
        ("建立失败分类表", "跟踪端到端 Trace", "拆分延迟和成本", "把 Prompt 与权限隔离"),
    ),
    Article(
        "06",
        "06-作品集与面试准备.md",
        "作品集与面试准备",
        "别只做一个聊天框",
        "作品集要证明你能完成工程闭环：场景约束、架构设计、评测报告和失败复盘。",
        ("场景", "架构", "评测", "复盘", "表达"),
        ("真实问题", "最小链路", "评测报告", "失败案例", "面试表达"),
        ("选择有约束的场景", "准备一张架构图", "展示一组评测数据", "讲清一个真实难点"),
    ),
    Article(
        "07",
        "07-推理性能基础.md",
        "推理性能基础",
        "理解延迟、Streaming 与 KV Cache",
        "性能优化不是换一个模型，而是拆解请求链路，找到首字延迟、生成速度和并发瓶颈。",
        ("TTFT", "Streaming", "KV Cache", "并发", "成本"),
        ("请求进入", "Prompt 处理", "首字输出", "持续生成", "性能验证"),
        ("分别测量 TTFT 与总耗时", "用 Streaming 改善体验", "控制上下文长度", "优化后重新跑基准"),
    ),
    Article(
        "08",
        "08-AICoding工程实践.md",
        "AI Coding 工程实践",
        "让模型提高效率，不替你承担责任",
        "把 AI 放进开发闭环：明确目标、审查 diff、运行测试、保护仓库和数据边界。",
        ("目标", "上下文", "Diff", "测试", "边界"),
        ("明确任务", "提供上下文", "生成修改", "审查 Diff", "运行验证"),
        ("把目标写成验收条件", "每次都检查 diff", "边改边跑测试", "敏感数据不进入模型"),
    ),
    Article(
        "09",
        "09-向量数据库选型与实战.md",
        "向量数据库选型",
        "从六款数据库对比到 Chroma 实战",
        "向量数据库选型要结合数据规模、过滤需求、运维成本和团队能力，而不是只看流行度。",
        ("Embedding", "索引", "过滤", "召回率", "运维"),
        ("业务需求", "规模与过滤", "索引选择", "写入检索", "监控验证"),
        ("先确认是否需要专用向量库", "用数据规模驱动选型", "验证过滤后的召回率", "监控增量更新一致性"),
    ),
    Article(
        "10",
        "10-LangChain与LlamaIndex框架对比.md",
        "LangChain 与 LlamaIndex",
        "框架选型要服务于问题，不是替代思考",
        "LangChain 偏流程编排，LlamaIndex 偏数据与检索；复杂度不高时，也可以先不用框架。",
        ("编排", "数据", "RAG", "Agent", "抽象"),
        ("明确问题", "判断核心复杂度", "选择框架", "隔离接口", "验证收益"),
        ("先写清核心链路", "避免过早绑定框架", "用接口隔离版本变化", "能解释为何选择或不用"),
    ),
)


def find_font(bold: bool = False) -> str:
    candidates = (
        (Path("C:/Windows/Fonts/msyhbd.ttc"), Path("C:/Windows/Fonts/msyh.ttc")),
        (Path("C:/Windows/Fonts/simhei.ttf"), Path("C:/Windows/Fonts/simsun.ttc")),
    )
    for bold_path, regular_path in candidates:
        path = bold_path if bold else regular_path
        if path.exists():
            return str(path)
    raise FileNotFoundError("No Chinese font was found under C:/Windows/Fonts.")


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(find_font(bold), size=size)


def color(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def rounded(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], radius: int, fill: str, outline: str | None = None, width: int = 1) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=color(fill), outline=color(outline) if outline else None, width=width)


def draw_text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, size: int, fill: str, bold: bool = False, spacing: int = 8) -> None:
    draw.multiline_text(xy, text, font=font(size, bold), fill=color(fill), spacing=spacing)


def wrap_text(draw: ImageDraw.ImageDraw, text: str, max_width: int, size: int, bold: bool = False) -> str:
    output: list[str] = []
    current = ""
    current_font = font(size, bold)
    for char in text:
        candidate = current + char
        if draw.textlength(candidate, font=current_font) <= max_width:
            current = candidate
        else:
            output.append(current)
            current = char
    if current:
        output.append(current)
    return "\n".join(output)


def make_canvas() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (WIDTH, HEIGHT), color(COLORS["cream"]))
    draw = ImageDraw.Draw(image)
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        start = color(COLORS["cream_2"])
        end = color(COLORS["cream"])
        line_color = tuple(round(start[i] * (1 - ratio) + end[i] * ratio) for i in range(3))
        draw.line((0, y, WIDTH, y), fill=line_color)
    draw.ellipse((980, -120, 1320, 220), fill=color(COLORS["orange_light"]))
    draw.ellipse((-130, 520, 140, 790), fill=color(COLORS["blue_light"]))
    return image, draw


def draw_brand(draw: ImageDraw.ImageDraw, article: Article, label: str) -> None:
    rounded(draw, (54, 38, 414, 82), 22, COLORS["navy"])
    draw_text(draw, (74, 50), "AI APPLICATION ENGINEERING", 20, COLORS["white"], True)
    draw_text(draw, (1032, 46), article.number, 40, COLORS["orange"], True)
    draw_text(draw, (55, 618), f"AI 应用研发工程师求职专题  /  {label}", 20, COLORS["muted"])


def draw_cover(article: Article, output: Path) -> None:
    image, draw = make_canvas()
    draw_brand(draw, article, "SERIES COVER")
    draw_text(draw, (56, 148), article.short_title, 62, COLORS["ink"], True)
    subtitle = wrap_text(draw, article.subtitle, 700, 33, True)
    draw_text(draw, (58, 238), subtitle, 33, COLORS["blue"], True, spacing=12)
    digest = wrap_text(draw, article.digest, 760, 25)
    draw_text(draw, (60, 352), digest, 25, COLORS["muted"], spacing=10)
    x = 60
    for keyword in article.keywords:
        pill_width = int(draw.textlength(keyword, font=font(22, True))) + 42
        rounded(draw, (x, 500, x + pill_width, 548), 24, COLORS["white"], COLORS["line"])
        draw_text(draw, (x + 21, 512), keyword, 22, COLORS["navy"], True)
        x += pill_width + 14
    rounded(draw, (910, 160, 1148, 456), 24, COLORS["navy"])
    for index, keyword in enumerate(article.keywords[:5]):
        y = 194 + index * 50
        rounded(draw, (942, y, 1114, y + 34), 17, COLORS["navy_2"])
        draw_text(draw, (960, y + 6), f"{index + 1:02d}  {keyword}", 19, COLORS["white"], True)
    image.save(output, quality=94)


def draw_flow(article: Article, output: Path) -> None:
    image, draw = make_canvas()
    draw_brand(draw, article, "CORE FLOW")
    draw_text(draw, (58, 130), "核心链路", 52, COLORS["ink"], True)
    draw_text(draw, (60, 202), "把复杂问题拆成可以验证的步骤", 26, COLORS["muted"])
    card_width = 196
    gap = 23
    for index, step in enumerate(article.flow):
        x = 58 + index * (card_width + gap)
        rounded(draw, (x, 308, x + card_width, 470), 20, COLORS["white"], COLORS["line"], 2)
        rounded(draw, (x + 18, 328, x + 64, 374), 23, COLORS["orange"] if index == 0 else COLORS["navy"])
        draw_text(draw, (x + 30, 338), str(index + 1), 24, COLORS["white"], True)
        label = wrap_text(draw, step, card_width - 34, 25, True)
        draw_text(draw, (x + 18, 398), label, 25, COLORS["navy"], True, spacing=8)
        if index < len(article.flow) - 1:
            arrow_x = x + card_width + 5
            draw.line((arrow_x, 389, arrow_x + 14, 389), fill=color(COLORS["orange"]), width=4)
            draw.polygon(((arrow_x + 14, 381), (arrow_x + 26, 389), (arrow_x + 14, 397)), fill=color(COLORS["orange"]))
    image.save(output, quality=94)


def draw_checklist(article: Article, output: Path) -> None:
    image, draw = make_canvas()
    draw_brand(draw, article, "ACTION CHECKLIST")
    draw_text(draw, (58, 130), "实战检查清单", 52, COLORS["ink"], True)
    draw_text(draw, (60, 202), "读完文章后，用四个动作留下项目证据", 26, COLORS["muted"])
    positions = ((60, 292), (602, 292), (60, 424), (602, 424))
    for index, (item, (x, y)) in enumerate(zip(article.checklist, positions), start=1):
        rounded(draw, (x, y, x + 500, y + 100), 18, COLORS["white"], COLORS["line"], 2)
        rounded(draw, (x + 20, y + 26, x + 68, y + 74), 24, COLORS["green"])
        draw_text(draw, (x + 33, y + 36), str(index), 24, COLORS["white"], True)
        label = wrap_text(draw, item, 390, 25, True)
        draw_text(draw, (x + 88, y + 32), label, 25, COLORS["navy"], True, spacing=6)
    image.save(output, quality=94)


def remove_first_heading(source: str) -> tuple[str, str]:
    match = re.search(r"^#\s+(.+?)\s*$", source, flags=re.MULTILINE)
    if not match:
        raise ValueError("Article does not contain an H1 heading.")
    title = match.group(1)
    return title, source[: match.start()] + source[match.end() :]


def local_asset_path(filename: str) -> str:
    return f"../assets/{filename}"


def image_block(filename: str, caption: str) -> str:
    return (
        f'\n<p class="wx-image" data-wx-asset="{html.escape(filename)}">'
        f'<img src="{html.escape(local_asset_path(filename))}" alt="{html.escape(caption)}" />'
        f'<span>{html.escape(caption)}</span></p>\n'
    )


def insert_image_blocks(source: str, article: Article) -> str:
    sections = list(re.finditer(r"^##\s+.+$", source, flags=re.MULTILINE))
    if len(sections) < 3:
        raise ValueError(f"{article.filename} does not contain enough sections.")
    names = (
        f"{article.slug}-01-cover.png",
        f"{article.slug}-02-flow.png",
        f"{article.slug}-03-checklist.png",
    )
    cover = image_block(names[0], f"{article.short_title}：{article.subtitle}")
    flow = image_block(names[1], f"{article.short_title}核心链路")
    checklist = image_block(names[2], f"{article.short_title}实战检查清单")
    insertions = (
        (0, cover),
        (sections[len(sections) // 2].start(), flow),
        (sections[-1].start(), checklist),
    )
    for index, block in sorted(insertions, reverse=True):
        source = source[:index] + block + source[index:]
    return source


def apply_styles(fragment: str, article: Article, title: str) -> str:
    soup = BeautifulSoup(fragment, "html.parser")
    styles = {
        "p": "margin:16px 0;color:#2F3A50;font-size:16px;line-height:1.9;letter-spacing:0.3px;",
        "h2": "margin:38px 0 16px;padding-left:12px;border-left:4px solid #F27649;color:#17233D;font-size:22px;line-height:1.45;font-weight:700;",
        "h3": "margin:26px 0 12px;color:#24375D;font-size:18px;line-height:1.55;font-weight:700;",
        "ul": "margin:12px 0 20px;padding-left:22px;color:#2F3A50;font-size:16px;line-height:1.85;",
        "ol": "margin:12px 0 20px;padding-left:22px;color:#2F3A50;font-size:16px;line-height:1.85;",
        "li": "margin:7px 0;color:#2F3A50;font-size:16px;line-height:1.85;",
        "blockquote": "margin:20px 0;padding:14px 18px;border-left:4px solid #5D78B7;background:#F4F7FC;color:#526078;font-size:15px;line-height:1.8;",
        "pre": "margin:18px 0;padding:16px;overflow-x:auto;border-radius:10px;background:#17233D;color:#F6F2EA;font-size:13px;line-height:1.65;white-space:pre-wrap;word-break:break-word;",
        "code": "font-family:Consolas,Menlo,monospace;",
        "table": "width:100%;margin:18px 0;border-collapse:collapse;border-spacing:0;font-size:14px;line-height:1.7;",
        "th": "padding:10px 8px;border:1px solid #E1D9CE;background:#F7F4EE;color:#17233D;text-align:left;font-weight:700;",
        "td": "padding:10px 8px;border:1px solid #E1D9CE;color:#39465D;vertical-align:top;",
        "a": "color:#4767A8;text-decoration:none;",
        "strong": "color:#17233D;font-weight:700;",
    }
    for tag_name, style in styles.items():
        for node in soup.find_all(tag_name):
            if not node.get("style"):
                node["style"] = style
    for node in soup.select("p.wx-image"):
        node["style"] = "margin:28px 0;text-align:center;"
        image = node.find("img")
        caption = node.find("span")
        if image:
            image["style"] = "display:block;width:100%;max-width:100%;height:auto;border-radius:12px;"
        if caption:
            caption["style"] = "display:block;margin-top:8px;color:#8A94A6;font-size:12px;line-height:1.6;text-align:center;"
    intro = BeautifulSoup(
        f"""
<section style="margin:0 0 22px;padding:18px 18px 16px;border-radius:12px;background:#17233D;color:#FFFFFF;">
  <div style="margin-bottom:8px;color:#F9D3BF;font-size:13px;letter-spacing:1px;">AI 应用研发工程师求职专题 · 第 {article.number} 篇</div>
  <div style="font-size:26px;line-height:1.35;font-weight:700;">{html.escape(title)}</div>
  <div style="margin-top:10px;color:#DDE5F7;font-size:15px;line-height:1.75;">{html.escape(article.digest)}</div>
</section>
""",
        "html.parser",
    )
    outro = BeautifulSoup(
        """
<section style="margin:34px 0 8px;padding:16px 18px;border-radius:10px;background:#F7F4EE;color:#65728A;font-size:14px;line-height:1.8;">
  <strong style="color:#17233D;">阅读建议</strong><br />
  不要急着收集更多名词。挑一个真实场景，把链路跑通、评测补齐、失败记录下来，项目才会变成面试里站得住的证据。
</section>
""",
        "html.parser",
    )
    soup.insert(0, intro)
    soup.append(outro)
    return str(soup)


def article_html(article: Article) -> tuple[str, str]:
    source = (SOURCE_DIR / article.filename).read_text(encoding="utf-8")
    title, source = remove_first_heading(source)
    source = insert_image_blocks(source, article)
    body = markdown.markdown(
        source,
        extensions=("fenced_code", "tables", "sane_lists"),
        output_format="html5",
    )
    body = apply_styles(body, article, title)
    document = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(title)}</title>
  <style>
    body {{ margin:0; background:#EEEAE2; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Microsoft YaHei",sans-serif; }}
    .article {{ box-sizing:border-box; width:min(100%,760px); margin:0 auto; padding:28px 24px 42px; background:#FFFDF8; }}
  </style>
</head>
<body>
  <article class="article">{body}</article>
</body>
</html>
"""
    return title, document


def write_index(manifest: Iterable[dict[str, object]]) -> None:
    cards = []
    for item in manifest:
        cards.append(
            f"""
      <a class="card" href="articles/{html.escape(str(item['html']))}">
        <img src="assets/{html.escape(str(item['assets'][0]))}" alt="" />
        <div class="meta">第 {html.escape(str(item['number']))} 篇</div>
        <h2>{html.escape(str(item['title']))}</h2>
        <p>{html.escape(str(item['digest']))}</p>
      </a>"""
        )
    index = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>AI 应用研发工程师求职专题</title>
  <style>
    * {{ box-sizing:border-box; }}
    body {{ margin:0; padding:36px 18px 64px; background:#EEEAE2; color:#17233D; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Microsoft YaHei",sans-serif; }}
    main {{ max-width:1060px; margin:0 auto; }}
    header {{ margin-bottom:26px; padding:26px 28px; border-radius:18px; background:#17233D; color:#fff; }}
    header p {{ margin:10px 0 0; color:#DDE5F7; line-height:1.8; }}
    .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(290px,1fr)); gap:18px; }}
    .card {{ overflow:hidden; border:1px solid #E1D9CE; border-radius:14px; background:#FFFDF8; color:inherit; text-decoration:none; transition:transform .2s ease,box-shadow .2s ease; }}
    .card:hover {{ transform:translateY(-3px); box-shadow:0 12px 28px rgba(23,35,61,.12); }}
    .card img {{ display:block; width:100%; height:auto; }}
    .card .meta {{ margin:16px 18px 0; color:#F27649; font-size:13px; font-weight:700; }}
    .card h2 {{ margin:7px 18px; font-size:19px; line-height:1.45; }}
    .card p {{ margin:0 18px 20px; color:#65728A; font-size:14px; line-height:1.75; }}
  </style>
</head>
<body>
  <main>
    <header>
      <h1>AI 应用研发工程师求职专题</h1>
      <p>从会调用模型，走向能交付一个可靠的 AI 系统。共 10 篇文章，每篇包含 3 张公众号信息卡。</p>
    </header>
    <section class="grid">{''.join(cards)}
    </section>
  </main>
</body>
</html>
"""
    (OUTPUT_DIR / "index.html").write_text(index, encoding="utf-8")


def main() -> None:
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    ASSET_DIR.mkdir(parents=True)
    ARTICLE_DIR.mkdir(parents=True)
    manifest: list[dict[str, object]] = []
    for article in ARTICLES:
        assets = (
            f"{article.slug}-01-cover.png",
            f"{article.slug}-02-flow.png",
            f"{article.slug}-03-checklist.png",
        )
        draw_cover(article, ASSET_DIR / assets[0])
        draw_flow(article, ASSET_DIR / assets[1])
        draw_checklist(article, ASSET_DIR / assets[2])
        title, document = article_html(article)
        html_name = f"{article.slug}.html"
        (ARTICLE_DIR / html_name).write_text(document, encoding="utf-8")
        manifest.append(
            {
                "number": article.number,
                "source": article.filename,
                "title": title,
                "shortTitle": article.short_title,
                "digest": article.digest,
                "html": html_name,
                "assets": list(assets),
            }
        )
    write_index(manifest)
    (OUTPUT_DIR / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Built {len(manifest)} articles and {len(manifest) * 3} PNG assets under {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
