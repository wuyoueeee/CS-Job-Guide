"""生成 docs/AI求职 专题配图。

用法：
    python tools/build_charts.py

数据统一来自 docs/_data/ai-job-market.json，规格集中在本文件。
新增图表：在 spec 里加一条，然后重跑本脚本即可。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from content_kit import chartkit  # noqa: E402

DATA = ROOT / "docs" / "_data" / "ai-job-market.json"
OUT = ROOT / "docs" / "AI求职" / "images"


def load() -> dict:
    return json.loads(DATA.read_text(encoding="utf-8"))


def items(data: dict, key: str) -> list[dict]:
    return data["metrics"][key]["items"]


def main() -> None:
    data = load()

    spec = {
        "chart-campus-ai-growth": {
            "kind": "vbar",
            "title": "同一个校招市场，两条完全不同的曲线",
            "subtitle": "2026 年 1-5 月新发校招岗位量同比",
            "source": "S1",
            "items": items(data, "campus_ai_growth"),
            "suffix": "%",
            "decimals": 2,
            "colors": [chartkit.BLUE_SOFT, chartkit.ORANGE],
            "callout": "增速差 43.7 个百分点",
        },
        "chart-ai-penetration": {
            "kind": "vbar",
            "title": "每 10 个校招岗位，已有近 4 个与 AI 相关",
            "subtitle": "新发校招岗位中的 AI 渗透率",
            "source": "S1",
            "items": items(data, "ai_penetration"),
            "suffix": "%",
            "decimals": 2,
            "colors": [chartkit.BLUE_SOFT, chartkit.ORANGE],
            "callout": "一年提升 11.15 个百分点",
        },
        "chart-city-penetration": {
            "kind": "hbar",
            "title": "同样是校招，北京近一半岗位与 AI 相关",
            "subtitle": "各城市新发校招岗位的 AI 渗透率",
            "source": "S1",
            "items": items(data, "city_penetration"),
            "suffix": "%",
            "decimals": 2,
            "highlight": ["北京"],
            "note": "渗透率反映结构，不等于岗位总量；北京同时是岗位量第一的城市",
        },
        "chart-salary-median": {
            "kind": "hbar",
            "title": "AI 岗位内部，薪酬断成两级台阶",
            "subtitle": "2026 届校招 AI 相关岗位月薪中位数",
            "source": "S2",
            "items": items(data, "salary_median"),
            "suffix": " 元",
            "decimals": 0,
            "highlight": ["大模型算法工程师", "AI 测试工程师", "AI 数据训练师"],
            "callout": "最高与最低相差 2.9 倍",
            "note": "多模态、自动驾驶、机器学习、推荐四类报告仅给出「均超过 23000」，此处按 23000 绘制",
        },
        "chart-supply-demand": {
            "kind": "hbar",
            "title": "越难的岗位，越缺人",
            "subtitle": "供需比 = 人才供给 / 岗位需求，低于 1 即供不应求",
            "source": "S1",
            "items": items(data, "supply_demand"),
            "decimals": 2,
            "highlight": ["高性能计算工程师"],
            "refline": 1.0,
            "refline_label": "",
            "callout": "约 7 个岗位抢 1 人",
            "note": "本图口径为供需比，与智联招聘「需供比」互为倒数，不可直接比较数值大小",
        },
        "chart-role-growth": {
            "kind": "hbar",
            "title": "增长最猛的不是算法，是智能体开发",
            "subtitle": "2026 年上半年 AI 相关岗位职位数同比",
            "source": "S3",
            "items": items(data, "role_growth"),
            "suffix": "%",
            "decimals": 1,
            "highlight": ["AI 智能体开发"],
            "callout": "同比增长 244%",
            "note": "全行业口径（含社招），非纯校招",
        },
        "chart-screening": {
            "kind": "hbar",
            "title": "名校学历只排第五",
            "subtitle": "企业招聘 AI 应届生时最看重的因素",
            "source": "S2",
            "items": items(data, "screening_criteria"),
            "suffix": "%",
            "decimals": 1,
            "highlight": ["名校学历"],
            "note": "多选题，各项合计大于 100%",
        },
        "chart-jd-keywords": {
            "kind": "hbar",
            "title": "6 份真实校招 JD 里，反复出现的就是这几项",
            "subtitle": "AI 应用开发岗公开 JD 中技能关键词出现份数",
            "source": "S7",
            "items": items(data, "jd_keywords"),
            "suffix": " 份",
            "decimals": 0,
            "highlight": ["RAG / 检索增强", "Agent / 智能体"],
            "callout": "Python 六份全中",
            "note": "样本仅 6 份公开 JD，用于关键词归纳，不代表全市场分布",
        },
        "chart-jd-threshold": {
            "kind": "hbar",
            "title": "先补门槛项，再谈加分项",
            "subtitle": "同一批 6 份 JD，按出现频次分成两组",
            "source": "S7",
            "items": items(data, "jd_keywords"),
            "suffix": " 份",
            "decimals": 0,
            "highlight": [
                "Python",
                "RAG / 检索增强",
                "Agent / 智能体",
                "Docker / K8s",
                "FastAPI / Flask",
                "SQL / 向量库",
            ],
            "callout": "6 项门槛，3 项加分",
            "note": "分组标准为本文设定：出现 4 份及以上记为门槛项（陶橙），2 份记为加分项（浅蓝）",
        },
        "chart-firm-size": {
            "kind": "stacked",
            "title": "六成半企业，一年只招 5 个以内的 AI 应届生",
            "subtitle": "企业招聘 AI 相关应届生的规模分布",
            "source": "S2",
            "items": items(data, "firm_hiring_size"),
            "callout": "65.8%",
            "note": "AI 岗位增长更多来自「更多企业开始招」，而不是「每家企业招很多」",
        },
        "chart-expand-intent": {
            "kind": "stacked",
            "title": "近六成企业打算扩招，但没人敢大扩",
            "subtitle": "企业 2026 年 AI 相关应届生招聘计划",
            "source": "S2",
            "items": items(data, "firm_expand_intent"),
            "callout": "58.2% 计划扩招",
            "note": "显著增加 21.9% 与小幅增加 36.3% 合计 58.2%；持平 38.8%",
        },
        "chart-industry-ai": {
            "kind": "hbar",
            "title": "AI 工程师的岗位，正在长到实体行业里",
            "subtitle": "两个增速最快的跨界方向的 AI 工程师平均招聘月薪",
            "source": "S3",
            "items": items(data, "industry_ai_salary"),
            "suffix": " 元",
            "decimals": 0,
            "highlight": ["新能源"],
            "note": "全行业社招口径（非校招），可与互联网 AI 岗对照，但不可与校招中位数直接比较",
        },
        "chart-embodied": {
            "kind": "vbar",
            "title": "具身智能：一年 15 倍的招聘热度",
            "subtitle": "平台招聘指数对比，2026 年 1-4 月 vs 2025 年同期",
            "source": "S5",
            "items": [
                {"label": "2025 年同期", "value": 36},
                {"label": "2026 年 1-4 月", "value": 579},
            ],
            "decimals": 0,
            "colors": [chartkit.BLUE_SOFT, chartkit.ORANGE],
            "callout": "约 16 倍",
            "note": "招聘指数为平台自建相对指标，非职位绝对数",
        },
    }

    produced = chartkit.build(DATA, OUT, spec)
    for p in produced:
        print(f"  {p.relative_to(ROOT)}  {p.stat().st_size / 1024:.1f} KB")
    print(f"\n共生成 {len(produced)} 张图表")


if __name__ == "__main__":
    main()
