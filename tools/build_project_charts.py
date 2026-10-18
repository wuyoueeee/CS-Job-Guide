"""生成 docs/项目实战 专题配图。

用法：
    python tools/build_project_charts.py

数据统一来自 docs/_data/project-metrics.json，规格集中在本文件。
注意：本专题数字全部是「按正文假设推导的工程量级」，不是实测数据，
因此每张图的 source 都指向 M1/M2，并在 note 里重复口径。

新增图表：在 spec 里加一条，然后重跑本脚本即可。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from content_kit import chartkit  # noqa: E402

DATA = ROOT / "docs" / "_data" / "project-metrics.json"
OUT = ROOT / "docs" / "项目实战" / "images"


def load() -> dict:
    return json.loads(DATA.read_text(encoding="utf-8"))


def items(data: dict, key: str) -> list[dict]:
    return data["metrics"][key]["items"]


def main() -> None:
    data = load()

    spec = {
        # ---------------- 秒杀 ----------------
        "chart-seckill-funnel": {
            "kind": "hbar",
            "title": "100 万人抢 1 万件，流量要一层层削下来",
            "subtitle": "各环节每秒需要处理的请求量（按正文假设推导）",
            "source": "M1",
            "items": items(data, "seckill_funnel"),
            "suffix": " 次/秒",
            "decimals": 0,
            "highlight": ["理论点击峰值"],
            "callout": "每层约削减 70% 到 90%",
            "note": "假设 100 万人参与、第一秒 30% 点击、人均 3 次请求；为教学用量级估算，非实测",
        },
        "chart-seckill-latency": {
            "kind": "hbar",
            "title": "36 毫秒怎么花的：一次秒杀请求的延迟预算",
            "subtitle": "从点击到返回「排队中」的各环节耗时（P95 目标 100 毫秒）",
            "source": "M1",
            "items": items(data, "seckill_latency_budget"),
            "suffix": " 毫秒",
            "decimals": 1,
            "highlight": ["MQ 发送后即返回", "客户端到网关网络"],
            "callout": "合计 36 毫秒",
            "note": "预算拆分而非实测值；网络往返占比最大，说明优化重点不在 Redis",
        },
        # ---------------- 短链 ----------------
        "chart-shortlink-hit": {
            "kind": "hbar",
            "title": "缓存命中率每跌 1 个百分点，数据库多扛 100 次",
            "subtitle": "跳转读 10,000 次/秒时，不同命中率对应的数据库 QPS",
            "source": "M1",
            "items": items(data, "shortlink_cache_hit"),
            "suffix": " 次/秒",
            "decimals": 0,
            "highlight": ["命中率 90%", "完全不走缓存"],
            "callout": "99% 到 90% 差 10 倍",
            "note": "按 10,000 次/秒读推导；命中率看似只差几个点，落到数据库是 10 倍差距",
        },
        "chart-shortlink-stats": {
            "kind": "hbar",
            "title": "统计千万不能同步写：聚合粒度决定写入量",
            "subtitle": "10,000 次跳转/秒下，三种统计写法的数据库写入量",
            "source": "M1",
            "items": items(data, "shortlink_stats_write"),
            "suffix": " 行/秒",
            "decimals": 0,
            "highlight": ["逐条同步写"],
            "callout": "小时聚合降到 3 行/秒",
            "note": "假设跳转分散在 1 万个短码上；短码越集中，聚合收益越大",
        },
        # ---------------- IM ----------------
        "chart-im-storage": {
            "kind": "hbar",
            "title": "离线消息存一年，是 TB 级的事",
            "subtitle": "100 万日活、人均 50 条/天，不同消息长度的年增量",
            "source": "M1",
            "items": items(data, "im_storage_growth"),
            "suffix": " TB",
            "decimals": 2,
            "highlight": ["平均 500 字节/条"],
            "callout": "只算正文，不含索引",
            "note": "索引与副本通常再放大 1.5 到 3 倍，是冷热分离的直接理由",
        },
        "chart-im-memory": {
            "kind": "hbar",
            "title": "连接数不是随便涨的：10 万连接吃掉 5 GB",
            "subtitle": "单机 WebSocket 连接数与常驻内存估算（Java NIO）",
            "source": "M2",
            "items": items(data, "im_connection_memory"),
            "suffix": " GB",
            "decimals": 1,
            "highlight": ["10 万连接", "20 万连接"],
            "callout": "按 50 KB/连接估算",
            "note": "工程常见量级，非实测；实际取决于缓冲区大小与 GC 策略",
        },
        # ---------------- API 网关 ----------------
        "chart-gateway-ratelimit": {
            "kind": "hbar",
            "title": "同样限 100 次/秒，固定窗口能放进 200 次",
            "subtitle": "四种限流算法在同一秒内的最大放行数",
            "source": "M1",
            "items": items(data, "gateway_ratelimit_algo"),
            "suffix": " 次",
            "decimals": 0,
            "highlight": ["固定窗口计数"],
            "refline": 100,
            "refline_label": "",
            "callout": "突刺发生在窗口边界",
            "note": "令牌桶允许突发是特性不是缺陷；要严格平滑才选漏桶",
        },
        "chart-gateway-overhead": {
            "kind": "hbar",
            "title": "网关自身开销 2 毫秒，下游占 20 毫秒",
            "subtitle": "一次经过网关的请求耗时拆分",
            "source": "M1",
            "items": items(data, "gateway_overhead"),
            "suffix": " 毫秒",
            "decimals": 1,
            "highlight": ["下游服务调用"],
            "callout": "网关占比不到 10%",
            "note": "网关自身合计 2.1 毫秒；优化网关前先确认慢在下游还是入口",
        },
        # ---------------- RAG ----------------
        "chart-rag-latency": {
            "kind": "hbar",
            "title": "一次问答 2.3 秒，其中 2 秒在等模型生成",
            "subtitle": "RAG 全链路非流式耗时拆分",
            "source": "M1",
            "items": items(data, "rag_latency"),
            "suffix": " 毫秒",
            "decimals": 0,
            "highlight": ["LLM 生成"],
            "callout": "生成占 86%",
            "note": "按输出约 800 token、400 token/秒估算；上流式可把首字延迟压到 0.5 秒级",
        },
        "chart-rag-context": {
            "kind": "stacked",
            "title": "上下文窗口里，检索片段占了六成",
            "subtitle": "一次问答的 token 预算分配",
            "source": "M1",
            "items": items(data, "rag_context_budget"),
            "callout": "片段决定上限",
            "note": "按中文 1 字约 1 token 估算；片段越多越全，但挤压对话与指令空间",
        },
        # ---------------- 权限 ----------------
        "chart-authz-cost": {
            "kind": "hbar",
            "title": "每次请求都查库做鉴权，接口直接慢 15 毫秒",
            "subtitle": "三种权限缓存策略下单次请求的额外耗时",
            "source": "M1",
            "items": items(data, "authz_check_cost"),
            "suffix": " 毫秒",
            "decimals": 1,
            "highlight": ["每次请求查数据库"],
            "callout": "本地缓存快 30 倍",
            "note": "本地缓存需处理权限变更后的失效，不能只图快",
        },
        # ---------------- 新增图型：折线 / 矩阵 ----------------
        "chart-seckill-stock": {
            "kind": "line",
            "title": "超卖不是玄学，是扣减逻辑少了原子性",
            "subtitle": "库存 500 件时两种扣减方式的剩余库存曲线",
            "source": "M1",
            "x_labels": data["metrics"]["seckill_stock_curve"]["x_labels"],
            "items": items(data, "seckill_stock_curve"),
            "suffix": " 件",
            "decimals": 0,
            "y_title": "剩余库存",
            "markers": [{"x": 5, "label": "库存耗尽"}],
            "callout": "扣成负数就是超卖",
            "note": "无锁曲线在第 600 次请求前后跌破 0；原子预扣用 Redis Lua 或数据库唯一索引兜底",
        },
        "chart-gateway-algo-curve": {
            "kind": "line",
            "title": "同样限 200 次每秒，四种算法的放行形状完全不同",
            "subtitle": "流量突刺下每秒放行量随时间的变化",
            "source": "M1",
            "x_labels": data["metrics"]["gateway_ratelimit_curve"]["x_labels"],
            "items": items(data, "gateway_ratelimit_curve"),
            "suffix": " 次/秒",
            "decimals": 0,
            "y_title": "每秒放行量",
            "callout": "固定窗口有边界突刺",
            "note": "阈值统一 200 次/秒、令牌桶容量 500；漏桶恒定速率，令牌桶允许有界突发",
        },
        "chart-shortlink-dbqps": {
            "kind": "line",
            "title": "命中率从 90% 掉到 80%，数据库流量翻一倍",
            "subtitle": "读 1 万 QPS 时缓存命中率与数据库 QPS 的关系",
            "source": "M1",
            "x_labels": data["metrics"]["shortlink_db_qps"]["x_labels"],
            "items": items(data, "shortlink_db_qps"),
            "suffix": " 次/秒",
            "decimals": 0,
            "y_title": "数据库 QPS",
            "callout": "命中率是命门",
            "note": "按 10,000 x (1 - 命中率) 推导；命中率跌 10 个百分点，DB 流量涨 5 倍",
        },
        "chart-authz-matrix": {
            "kind": "matrix",
            "title": "越权测试要按角色和资源组合逐个跑",
            "subtitle": "三类角色对三类数据资源的访问控制期望",
            "source": "M1",
            "rows": data["metrics"]["authz_matrix"]["rows"],
            "cols": data["metrics"]["authz_matrix"]["cols"],
            "cells": data["metrics"]["authz_matrix"]["cells"],
            "row_label": "角色",
            "callout": "每个红格都是一条测试用例",
            "note": "绿为允许、橙为需二次授权、红为必须拒绝；矩阵里每一格都要有用例覆盖，漏一格就是漏洞",
        },
    }

    produced = chartkit.build(DATA, OUT, spec)
    for p in produced:
        print(f"  {p.relative_to(ROOT)}  {p.stat().st_size / 1024:.1f} KB")
    print(f"\n共生成 {len(produced)} 张图表")


if __name__ == "__main__":
    main()
