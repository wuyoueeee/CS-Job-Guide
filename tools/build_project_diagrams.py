"""生成 docs/项目实战 的示意图（架构图 / 流程图 / 时序图）。

用法：
    python tools/build_project_diagrams.py

与 chartkit 系列的图表互补：图表表达数字对比，示意图表达结构与关系。
视觉系统与 chartkit 一致（米白纸感 + 墨蓝 + 陶橙），输出 SVG。

新增示意图：在 spec 里加一条，然后重跑本脚本即可。
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from content_kit import diagramkit  # noqa: E402

OUT = ROOT / "docs" / "项目实战" / "images"
SRC = "来源：本文整理的结构示意，非架构标准答案"


def main() -> None:
    spec = {
        # ---------------- RAG ----------------
        "diagram-rag-arch": {
            "kind": "arch",
            "title": "RAG 系统的四层结构，评测库常常被漏掉",
            "subtitle": "一个能讲清楚架构的 RAG 项目至少长这样",
            "source": SRC,
            "callout": "评测库是分水岭",
            "note": "权限过滤必须在检索前下推，不能等召回后再按权限删",
            "columns": 3,
            "layers": [
                {
                    "name": "接入层",
                    "nodes": [
                        {"label": "问答界面", "sub": "流式输出与引用展示"},
                        {"label": "文档上传", "sub": "触发解析流水线"},
                        {"label": "管理后台", "sub": "测试集与 badcase 维护", "accent": True},
                    ],
                },
                {
                    "name": "服务层",
                    "nodes": [
                        {"label": "查询理解", "sub": "改写、扩写、意图判断"},
                        {"label": "混合检索", "sub": "向量召回加关键词召回", "accent": True},
                        {"label": "重排与生成", "sub": "TopK 重排、带引用生成"},
                    ],
                },
                {
                    "name": "模型层",
                    "nodes": [
                        {"label": "Embedding 模型", "sub": "文档与查询向量化"},
                        {"label": "通用大模型", "sub": "改写与答案生成"},
                        {"label": "重排模型", "sub": "Cross-Encoder 精排"},
                    ],
                },
                {
                    "name": "数据层",
                    "nodes": [
                        {"label": "向量库", "sub": "chunk 向量与元信息"},
                        {"label": "对象存储", "sub": "原始文档"},
                        {"label": "评测集", "sub": "测试问题与标准答案", "accent": True},
                    ],
                },
            ],
        },
        # ---------------- Agent ----------------
        "diagram-agent-seq": {
            "kind": "seq",
            "title": "一次工具调用的完整时序",
            "subtitle": "注意上下文在第三步和第七步各膨胀一次",
            "source": SRC,
            "callout": "两次模型调用是延迟大头",
            "note": "写操作必须在执行前人工确认；校验失败要把具体错误回喂给模型",
            "actors": ["用户", "Agent 服务", "模型", "工具执行器"],
            "messages": [
                {"from": 0, "to": 1, "text": "提交任务：查我上周的订单"},
                {"from": 1, "to": 2, "text": "系统提示 + 工具定义 + 会话历史", "note": "上下文 2100 token"},
                {"from": 2, "to": 1, "text": "返回工具调用 query_order", "kind": "return"},
                {"from": 1, "to": 1, "text": "参数 Schema 校验", "kind": "self"},
                {"from": 1, "to": 3, "text": "执行工具（写操作先人工确认）"},
                {"from": 3, "to": 1, "text": "返回订单 JSON", "kind": "return"},
                {"from": 1, "to": 2, "text": "回喂工具结果，请求总结", "note": "历史再加 800 token"},
                {"from": 2, "to": 1, "text": "生成最终答复", "kind": "return"},
            ],
        },
        # ---------------- 评测平台 ----------------
        "diagram-eval-flow": {
            "kind": "flow",
            "title": "评测平台的运行闭环",
            "subtitle": "没有 badcase 回流，测试集就是一潭死水",
            "source": SRC,
            "callout": "回流比执行更值钱",
            "note": "指标不达标时先归因再改，不要凭感觉调 prompt",
            "col_width": 300,
            "row_height": 96,
            "nodes": [
                {"id": "submit", "label": "提交评测任务", "type": "start", "col": 1, "row": 0},
                {"id": "ready", "label": "测试集就绪？", "type": "decision", "col": 1, "row": 1},
                {"id": "gen", "label": "补充或生成测试集", "col": 0, "row": 2},
                {"id": "run", "label": "并发执行全部用例", "col": 1, "row": 3, "accent": True},
                {"id": "judge", "label": "规则指标 + 裁判模型", "col": 1, "row": 4},
                {"id": "pass", "label": "指标达标？", "type": "decision", "col": 1, "row": 5},
                {"id": "reason", "label": "badcase 归因", "col": 2, "row": 6, "accent": True},
                {"id": "back", "label": "回流进测试集", "col": 2, "row": 7},
                {"id": "report", "label": "生成对比报告", "col": 0, "row": 8},
                {"id": "end", "label": "报告归档", "type": "end", "col": 1, "row": 9},
            ],
            "edges": [
                {"from": "submit", "to": "ready"},
                {"from": "ready", "to": "gen", "label": "否", "kind": "no"},
                {"from": "gen", "to": "run"},
                {"from": "ready", "to": "run", "label": "是", "kind": "yes"},
                {"from": "run", "to": "judge"},
                {"from": "judge", "to": "pass"},
                {"from": "pass", "to": "reason", "label": "否", "kind": "no"},
                {"from": "reason", "to": "back"},
                {"from": "back", "to": "run", "kind": "dash"},
                {"from": "pass", "to": "report", "label": "是", "kind": "yes"},
                {"from": "report", "to": "end"},
            ],
        },
        # ---------------- 文档解析 ----------------
        "diagram-docparse-flow": {
            "kind": "flow",
            "title": "文档解析的分级路由",
            "subtitle": "七成文档走快路，成本立刻降一个量级",
            "source": SRC,
            "callout": "别对所有文档一视同仁",
            "note": "路由判错的代价是质量，不是速度；抽样复核路由准确率要有指标",
            "col_width": 300,
            "row_height": 92,
            "nodes": [
                {"id": "up", "label": "文档入库", "type": "start", "col": 1, "row": 0},
                {"id": "text", "label": "有文本层？", "type": "decision", "col": 1, "row": 1},
                {"id": "fast", "label": "快路：文本提取加版面分析", "col": 0, "row": 2, "accent": True},
                {"id": "ocr", "label": "慢路：OCR 加版面分析", "col": 2, "row": 2},
                {"id": "table", "label": "含表格？", "type": "decision", "col": 1, "row": 3},
                {"id": "tbl", "label": "表格结构识别", "col": 2, "row": 4},
                {"id": "chart", "label": "含图表且需理解？", "type": "decision", "col": 1, "row": 5},
                {"id": "mm", "label": "多模态理解", "col": 2, "row": 6},
                {"id": "chunk", "label": "阅读顺序还原与切分", "col": 1, "row": 7},
                {"id": "ok", "label": "可检索", "type": "end", "col": 1, "row": 8},
            ],
            "edges": [
                {"from": "up", "to": "text"},
                {"from": "text", "to": "fast", "label": "是", "kind": "yes"},
                {"from": "text", "to": "ocr", "label": "否", "kind": "no"},
                {"from": "fast", "to": "table"},
                {"from": "ocr", "to": "table"},
                {"from": "table", "to": "tbl", "label": "是", "kind": "yes"},
                {"from": "tbl", "to": "chart"},
                {"from": "table", "to": "chart", "label": "否"},
                {"from": "chart", "to": "mm", "label": "是", "kind": "yes"},
                {"from": "mm", "to": "chunk"},
                {"from": "chart", "to": "chunk", "label": "否"},
                {"from": "chunk", "to": "ok"},
            ],
        },
        # ---------------- 秒杀 ----------------
        "diagram-seckill-arch": {
            "kind": "arch",
            "title": "秒杀系统的削峰与兜底",
            "subtitle": "每一层都在把不可能变成可能",
            "source": SRC,
            "callout": "兜底比削峰更重要",
            "note": "库存预扣必须原子；订单唯一索引是最后一道防线，超时补偿负责收尾",
            "columns": 3,
            "layers": [
                {
                    "name": "接入层",
                    "nodes": [
                        {"label": "CDN 静态化", "sub": "页面与按钮资源前置"},
                        {"label": "前端拦截", "sub": "置灰、答题、错峰", "accent": True},
                        {"label": "网关限流", "sub": "用户级与接口级"},
                    ],
                },
                {
                    "name": "服务层",
                    "nodes": [
                        {"label": "资格校验", "sub": "预约与令牌发放"},
                        {"label": "库存预扣", "sub": "Redis Lua 原子扣减", "accent": True},
                        {"label": "异步下单", "sub": "写 MQ 后立即返回"},
                    ],
                },
                {
                    "name": "数据层",
                    "nodes": [
                        {"label": "Redis", "sub": "库存与资格位"},
                        {"label": "MySQL", "sub": "订单与流水", "accent": True},
                        {"label": "消息队列", "sub": "削峰填谷"},
                    ],
                },
                {
                    "name": "兜底层",
                    "nodes": [
                        {"label": "唯一索引幂等", "sub": "防重复下单"},
                        {"label": "超时补偿", "sub": "关单并回补库存"},
                        {"label": "对账任务", "sub": "Redis 与 DB 每日核对"},
                    ],
                },
            ],
        },
        # ---------------- 网关 ----------------
        "diagram-gateway-arch": {
            "kind": "arch",
            "title": "API 网关的责任链",
            "subtitle": "每个 filter 只做一件事，顺序就是优先级",
            "source": SRC,
            "callout": "网关自身开销要计量",
            "note": "本地限流挡绝大部分流量，Redis 限流只处理本地放行部分；配置走推送不轮询",
            "columns": 3,
            "layers": [
                {
                    "name": "入口",
                    "nodes": [
                        {"label": "SSL 终止", "sub": "证书与协议升级"},
                        {"label": "连接管理", "sub": "长连接与超时"},
                        {"label": "请求日志", "sub": " traceId 贯穿全链", "accent": True},
                    ],
                },
                {
                    "name": "责任链",
                    "nodes": [
                        {"label": "路由", "sub": "匹配上游服务"},
                        {"label": "鉴权", "sub": "Token 与白名单"},
                        {"label": "限流", "sub": "本地加 Redis 两级", "accent": True},
                        {"label": "熔断", "sub": "异常率加慢调用"},
                        {"label": "灰度", "sub": "按权重分流"},
                        {"label": "协议转换", "sub": "REST 转 gRPC"},
                    ],
                },
                {
                    "name": "上游",
                    "nodes": [
                        {"label": "业务服务 A", "sub": "订单域"},
                        {"label": "业务服务 B", "sub": "用户域"},
                        {"label": "业务服务 C", "sub": "商品域"},
                    ],
                },
                {
                    "name": "支撑",
                    "nodes": [
                        {"label": "配置中心", "sub": "路由与限流规则推送"},
                        {"label": "监控告警", "sub": "QPS、错误率、P99"},
                        {"label": "控制台", "sub": "动态调整阈值"},
                    ],
                },
            ],
        },
        # ---------------- 熔断状态机 ----------------
        "diagram-gateway-breaker": {
            "kind": "flow",
            "title": "熔断器的三个状态",
            "subtitle": "半开探测是恢复的关键，也是最多人做漏的一步",
            "source": SRC,
            "callout": "半开只放少量请求",
            "note": "打开状态有冷却期；半开期放行少量探测请求，成功即关闭，失败即重新打开",
            "col_width": 320,
            "row_height": 88,
            "nodes": [
                {"id": "closed", "label": "关闭：正常放行", "type": "start", "col": 1, "row": 0, "accent": True},
                {"id": "check", "label": "异常率或慢调用超阈值？", "type": "decision", "col": 1, "row": 1},
                {"id": "open", "label": "打开：直接快速失败", "col": 1, "row": 2},
                {"id": "cool", "label": "冷却期结束？", "type": "decision", "col": 1, "row": 3},
                {"id": "half", "label": "半开：放行少量探测请求", "col": 0, "row": 4, "accent": True},
                {"id": "probe", "label": "探测请求成功？", "type": "decision", "col": 1, "row": 5},
                {"id": "reopen", "label": "重新打开", "col": 2, "row": 5},
            ],
            "edges": [
                {"from": "closed", "to": "check"},
                {"from": "check", "to": "open", "label": "是", "kind": "yes"},
                {"from": "check", "to": "closed", "label": "否", "kind": "dash"},
                {"from": "open", "to": "cool"},
                {"from": "cool", "to": "half", "label": "是", "kind": "yes"},
                {"from": "half", "to": "probe"},
                {"from": "probe", "to": "closed", "label": "成功", "kind": "yes"},
                {"from": "probe", "to": "reopen", "label": "失败", "kind": "no"},
                {"from": "reopen", "to": "cool", "kind": "dash"},
            ],
        },
        # ---------------- 秒杀订单状态机 ----------------
        "diagram-seckill-order": {
            "kind": "flow",
            "title": "订单状态机：一开始不定清楚，后面全是坑",
            "subtitle": "每个箭头都要有触发条件和兜底动作",
            "source": SRC,
            "callout": "超时要能自动关单",
            "note": "状态只能单向流转；关单回补库存必须幂等，补偿任务重复执行不能重复加库存",
            "col_width": 300,
            "row_height": 86,
            "nodes": [
                {"id": "init", "label": "INIT 待支付", "type": "start", "col": 1, "row": 0},
                {"id": "pay", "label": "支付结果", "type": "decision", "col": 1, "row": 1},
                {"id": "succ", "label": "SUCCESS 已成交", "type": "end", "col": 0, "row": 2, "accent": True},
                {"id": "fail", "label": "FAILED 已失败", "type": "end", "col": 2, "row": 2},
                {"id": "timeout", "label": "超过 15 分钟未支付？", "type": "decision", "col": 1, "row": 3},
                {"id": "close", "label": "TIMEOUT 关单", "col": 1, "row": 4},
                {"id": "back", "label": "补偿任务回补库存", "col": 1, "row": 5, "accent": True},
            ],
            "edges": [
                {"from": "init", "to": "pay"},
                {"from": "pay", "to": "succ", "label": "成功", "kind": "yes"},
                {"from": "pay", "to": "fail", "label": "失败", "kind": "no"},
                {"from": "init", "to": "timeout"},
                {"from": "timeout", "to": "close", "label": "是", "kind": "yes"},
                {"from": "close", "to": "back"},
                {"from": "back", "to": "fail", "kind": "dash"},
            ],
        },
        # ---------------- IM ----------------
        "diagram-im-seq": {
            "kind": "seq",
            "title": "一条消息从发出到确认",
            "subtitle": "seq 在会话内单调递增，是顺序与去重的共同依据",
            "source": SRC,
            "callout": "ACK 带最大 seq",
            "note": "读扩散写扩散按会话规模选；离线消息进 inbox，上线后按 seq 补拉",
            "actors": ["发送方", "接入网关", "消息服务", "接收方"],
            "messages": [
                {"from": 0, "to": 1, "text": "发送消息（带客户端幂等键）"},
                {"from": 1, "to": 2, "text": "转发到消息服务"},
                {"from": 2, "to": 2, "text": "会话内分配自增 seq", "kind": "self", "note": "单调递增"},
                {"from": 2, "to": 3, "text": "在线直达推送"},
                {"from": 2, "to": 2, "text": "离线写入收件箱", "kind": "self"},
                {"from": 3, "to": 2, "text": "ACK（带已收到的最大 seq）", "kind": "return"},
                {"from": 2, "to": 0, "text": "投递回执", "kind": "return"},
            ],
        },
    }

    produced = diagramkit.build(OUT, spec)
    for p in produced:
        print(f"  {p.relative_to(ROOT)}  {p.stat().st_size / 1024:.1f} KB")
    print(f"\n共生成 {len(produced)} 张示意图")


if __name__ == "__main__":
    main()
