"""生成 docs/项目实战 的大模型项目配图。

用法：
    python tools/build_llm_project_charts.py

数据统一来自 docs/_data/llm-project-metrics.json，规格集中在本文件。
注意：本专题数字全部是「按正文假设推导的工程量级」，不是实测数据，
因此每张图的 source 都指向 L1/L2，并在 note 里重复口径。

新增图表：在 spec 里加一条，然后重跑本脚本即可。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from content_kit import chartkit  # noqa: E402

DATA = ROOT / "docs" / "_data" / "llm-project-metrics.json"
OUT = ROOT / "docs" / "项目实战" / "images"


def load() -> dict:
    return json.loads(DATA.read_text(encoding="utf-8"))


def items(data: dict, key: str) -> list[dict]:
    return data["metrics"][key]["items"]


def main() -> None:
    data = load()

    spec = {
        # ---------------- Agent 工具调用平台 ----------------
        "chart-agent-token-growth": {
            "kind": "hbar",
            "title": "Agent 真正的成本：上下文随轮数线性膨胀",
            "subtitle": "5 个工具、每轮重发工具定义与会话历史的 token 占用",
            "source": "L1",
            "items": items(data, "agent_token_growth"),
            "suffix": " token",
            "decimals": 0,
            "highlight": ["20 轮工具调用"],
            "callout": "20 轮就超 16K 窗口",
            "note": "每轮约增 800 token；不压缩历史，长任务必然撞窗口",
        },
        "chart-agent-latency": {
            "kind": "hbar",
            "title": "一轮工具调用 3.6 秒，模型生成占大头",
            "subtitle": "单轮工具调用的耗时拆分",
            "source": "L2",
            "items": items(data, "agent_latency_budget"),
            "suffix": " 毫秒",
            "decimals": 0,
            "highlight": ["结果注入与总结生成", "工具执行"],
            "callout": "合计 3.6 秒",
            "note": "规划与总结两次模型调用合计 1.8 秒；外部工具只占 1 秒",
        },
        # ---------------- 评测平台 ----------------
        "chart-eval-cost": {
            "kind": "hbar",
            "title": "一次回归评测，串行要跑一个半小时",
            "subtitle": "不同测试集规模与版本数的串行总耗时",
            "source": "L1",
            "items": items(data, "eval_run_cost"),
            "suffix": " 分钟",
            "decimals": 1,
            "highlight": ["200 条 x 5 版本"],
            "callout": "必须并发执行",
            "note": "按单次 5.75 秒推导；并发 10 路可压到十分之一，是评测平台的必备能力",
        },
        # ---------------- 结构化抽取 ----------------
        "chart-extract-threshold": {
            "kind": "hbar",
            "title": "阈值每降一档，自动化上去、漏错也跟着上去",
            "subtitle": "不同置信度阈值下需人工复核的文档量（每 1000 份）",
            "source": "L1",
            "items": items(data, "extract_threshold_review"),
            "suffix": " 份",
            "decimals": 0,
            "highlight": ["阈值 0.9", "不设阈值全自动"],
            "refline": 150,
            "refline_label": "",
            "callout": "阈值是业务决策不是技术参数",
            "note": "假设置信度分布为 0.9 以上 60%、0.7 到 0.9 占 25%、0.7 以下 15%",
        },
        "chart-extract-latency": {
            "kind": "hbar",
            "title": "单份抽取 2.2 秒，模型生成占九成",
            "subtitle": "结构化信息抽取的耗时拆分",
            "source": "L2",
            "items": items(data, "extract_latency_budget"),
            "suffix": " 毫秒",
            "decimals": 0,
            "highlight": ["模型生成结构化结果"],
            "callout": "合计 2.2 秒",
            "note": "Schema 校验只占 10 毫秒，但它是拦住错误结果的唯一关卡",
        },
        # ---------------- 文档智能解析 ----------------
        "chart-docparse-cost": {
            "kind": "hbar",
            "title": "一页 PDF 要 6.6 秒，100 页就是 11 分钟",
            "subtitle": "单页文档解析的全链路耗时",
            "source": "L2",
            "items": items(data, "docparse_page_cost"),
            "suffix": " 毫秒",
            "decimals": 0,
            "highlight": ["图表多模态理解", "扫描件 OCR"],
            "callout": "必须异步流水线",
            "note": "多模态与 OCR 两项占七成；批量入库只能走队列，不能同步等",
        },
        # ---------------- 新增图型：分组 / 折线 / 矩阵 / 散点 ----------------
        "chart-rag-chunking": {
            "kind": "grouped",
            "title": "切分策略比换模型更影响召回",
            "subtitle": "三种切分策略在 200 条测试集上的表现",
            "source": "L1",
            "groups": data["metrics"]["rag_chunking_compare"]["groups"],
            "items": items(data, "rag_chunking_compare"),
            "decimals": 2,
            "label_width": 8,
            "callout": "语义切分召回最高",
            "note": "Recall@5 指答案出现在前 5 个 chunk 的比例；引用准确率指引用段落确实含答案",
        },
        "chart-agent-context": {
            "kind": "line",
            "title": "压不压缩历史，决定 Agent 能跑多少轮",
            "subtitle": "两种上下文管理策略随轮数的增长曲线",
            "source": "L1",
            "x_labels": data["metrics"]["agent_context_curve"]["x_labels"],
            "items": items(data, "agent_context_curve"),
            "suffix": " token",
            "decimals": 0,
            "y_title": "上下文占用",
            "markers": [{"x": 6, "label": "超出 16K 窗口"}],
            "callout": "20 轮差出一倍",
            "note": "每轮新增约 800 token；压缩策略为保留最近 4 轮原文，更早历史摘要成 300 token",
        },
        "chart-eval-agreement": {
            "kind": "line",
            "title": "裁判模型要先和人工对齐，再谈自动评测",
            "subtitle": "裁判与人工标注的一致率随校准样本量变化",
            "source": "L1",
            "x_labels": data["metrics"]["eval_judge_agreement"]["x_labels"],
            "items": items(data, "eval_judge_agreement"),
            "suffix": "",
            "decimals": 2,
            "y_decimals": 2,
            "y_min": 0.70,
            "y_title": "一致率",
            "callout": "85% 是可用门槛",
            "note": "低于 85% 时裁判的判定不能直接采信，仍需人工复核；超过 200 条后收益衰减",
        },
        "chart-eval-matrix": {
            "kind": "matrix",
            "title": "版本回归要看全部指标，不能只看一个数",
            "subtitle": "四个版本在五类指标上的回归结果",
            "source": "L1",
            "rows": data["metrics"]["eval_metric_matrix"]["rows"],
            "cols": data["metrics"]["eval_metric_matrix"]["cols"],
            "cells": data["metrics"]["eval_metric_matrix"]["cells"],
            "row_label": "指标",
            "callout": "v1.2 质量最好但延迟回退",
            "note": "绿为通过、橙为持平、红为回退；延迟以 P95 2.5 秒为门槛",
        },
        "chart-extract-tradeoff": {
            "kind": "scatter",
            "title": "自动化率与漏错率是一对权衡，没有免费午餐",
            "subtitle": "不同置信度阈值下的自动化率与漏错率",
            "source": "L1",
            "items": items(data, "extract_tradeoff"),
            "x_title": "自动化率",
            "y_title": "漏错率",
            "x_decimals": 2,
            "y_decimals": 3,
            "zones": data["metrics"]["extract_tradeoff"]["zones"],
            "callout": "阈值是业务决策",
            "note": "自动化率与漏错率此消彼长；推荐区间需结合人工成本与错误成本定，不是技术最优解",
        },
        "chart-docparse-quality": {
            "kind": "grouped",
            "title": "解析深度决定下游能不能用",
            "subtitle": "三种解析深度在 100 份含表格文档上的还原质量",
            "source": "L1",
            "groups": data["metrics"]["docparse_quality"]["groups"],
            "items": items(data, "docparse_quality"),
            "decimals": 2,
            "label_width": 9,
            "callout": "表格必须结构识别",
            "note": "纯文本提取下表格还原率为 0；加表格结构模型后顺序与还原同时到位",
        },
    }

    produced = chartkit.build(DATA, OUT, spec)
    for p in produced:
        print(f"  {p.relative_to(ROOT)}  {p.stat().st_size / 1024:.1f} KB")
    print(f"\n共生成 {len(produced)} 张图表")


if __name__ == "__main__":
    main()
