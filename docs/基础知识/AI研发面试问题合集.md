# AI 研发面试问题合集（全网近一年）

这份合集整理自近一年（2025 年秋招季到 2026 年 9 月）各平台公开的 AI 研发方向面经，共 32 个来源：牛客网 16 篇，CSDN 与 GitCode 6 篇，其余 10 个来自个人博客、题库站点和海外面试指南。问题按模块聚合去重，同一道题被多处问到的并列标注来源。

它和[大模型与 AI 面试高频题](./大模型与AI面试高频题.md)分工不同：那篇讲"面试官想考什么、怎么答"，这篇讲"实际考了什么、哪些题反复出现"。准备时先拿这份合集扫盲，再对照高频题补答法。

来源标注用方括号简写，完整链接见文末来源清单。统计口径说明：文中"N 篇提到"只统计本合集收录的来源，不代表全市场频率；个别来源是基于上百条面试记录的统计帖，会单独注明。

## 一、模型结构与基础原理

这一模块是筛掉"背过结构图但没想过为什么"的人的地方，几乎每篇面经都有 2 到 4 题。

### Transformer 与注意力

1. Self-Attention 的计算流程，Q/K/V 分别是什么，Attention Score 为什么除以根号 d_k，不缩放会怎么样【字节多模态、聚合帖-快手2025、百度、基模题库】
2. 多头注意力为什么比单头好，核心优势是什么【字节多模态、快手应用、聚合帖-快手2025、百度、腾讯多模态、大厂真题】
3. Decoder 的因果注意力，QKV 分别来自哪，为什么要用自回归因果掩码【字节多模态、聚合帖-快手2025】
4. MHA、MQA、GQA 三种注意力机制的区别，推理速度、显存占用、KV Cache 占用比例的差异【百度】
5. DeepSeek 的 MLA 讲一下，decode 阶段的计算访存比怎么分析，和 seqlen、batch size 是否相关【聚合帖-快手2025、AI Infra 面经】
6. 为什么现在 Decoder-only 成为主流架构，BERT 和 GPT 的区别，大模型时代小模型还有什么用【字节豆包、聚合帖-快手2025】
7. Transformer 怎么做加速训练，训练和推理有什么区别【字节多模态】
8. Decoder 文本生成有哪几种方法，大模型预测 token 的损失怎么算，常见损失函数有哪些【字节多模态、聚合帖-快手2025】
9. Transformer 的核心优势是什么，为什么适合作为 AI 基础引擎；和 RNN/LSTM 的本质区别【腾讯多模态、基模题库】
10. Transformer 的时间、空间复杂度，降低注意力复杂度的方法【字节推荐、基模题库】
11. Pre-LayerNorm 和 Post-LayerNorm 的区别，为什么现代 LLM 普遍用 Pre-LN；残差连接的作用；Dropout 为什么在 LLaMA 里被去掉【基模题库】
12. FFN 的结构演变，GLU/SwiGLU/GeGLU 是什么；激活函数从 ReLU 到 GELU 到 Swish 的演变【基模题库】
13. Transformer 的参数量和 FLOPs 怎么算；初始化策略，为什么不同层要不同初始化；softmax 的数值稳定性怎么处理【基模题库】
14. 编码器和解码器的注意力有什么区别，Qwen 相比原始 Transformer 有哪些结构改动，Qwen2 又有哪些改进【大厂真题、字节豆包】

### 位置编码与归一化

1. RoPE 的原理和优点，目前常用的位置编码还有哪些，各有什么优缺点【字节豆包、聚合帖-快手2025、百度、基模题库】
2. 为什么用 RMSNorm，和 LayerNorm 有什么差异，什么场景用哪个【快手应用、字节推荐】
3. 长上下文外推技术：YaRN、NTK-Aware、ABF 的原理；怎么扩展模型最大输入长度【基模题库、腾讯多模态】

### 经典模型与 NLP 基础

1. BERT 的结构和训练方式（MLM、NSP），怎么用 BERT 做下游任务【腾讯多模态、基模题库】
2. 隐马尔可夫模型在实体识别里怎么定义观测状态、隐藏状态、前向传播和解码【腾讯多模态】
3. Causal LM 和 Masked LM 的区别，语言模型预训练的目标函数【基模题库】
4. LoRA 微调时，不同秩 r 对最终效果的影响曲线，怎么确定 attention 哪些层需要加 LoRA【CSDN 全攻略】

## 二、预训练与数据工程

这一模块考的是"你真跑过训练还是只跑过开源脚本"。

1. DeepSpeed 和 Megatron 分别介绍一下，分布式训练的常见策略（DDP、Tensor 并行、Pipeline 并行、ZeRO-1/2/3），各自解决什么瓶颈【字节多模态、AI Infra 汇总、基模题库】
2. ZeRO-Offload 加 Sequence Parallel 加 FlashAttention 在万卡训练里怎么组合，3D 并行的通信开销怎么算【AI Infra 面经、美团北斗】
3. 混合精度训练，BF16 和 FP8 的区别，各自有什么数值问题【美团北斗、基模题库】
4. 预训练的数据工程：数据怎么清洗、去重、质量筛选，配比策略怎么定，不同领域和语言怎么分配【百度、基模题库】
5. Tokenizer 详解：BPE、WordPiece、SentencePiece 的特点，文本到 token 的流程【基模题库、聚合帖-快手2025】
6. SFT 数据质量怎么把控：来源筛选、去重去偏、标注规范、交叉校验、评估指标，有没有做长尾任务上采样【MiniMax】
7. 预训练阶段用了多大学习率，warmup 步数怎么设，学习率调度策略有哪些，有没有做上下文扩展、用的什么方案【MiniMax、基模题库】
8. 做 pre-training 时 loss 的权重是怎么设计的【字节面经合集】
9. 合成数据的最终目标是什么，拿到业务需求怎么拆解定义问题，Query 怎么生成与提取，主流合成数据方法（Self-Instruct、Evol-Instruct）的区别【字节面经合集、基模题库】
10. 数据污染怎么检测和处理，测试集泄露怎么发现【基模题库、CSDN 全攻略】
11. 课程学习在大模型训练里怎么应用，MinHash 文档去重怎么实现【基模题库】
12. 大模型的幻觉怎么减轻，复读问题是怎么产生的、业内有什么解决办法【百度】
13. 怎么操作能更容易让模型达到更好性能，之前训练大模型遇到过什么困难、怎么解决的【百度】
14. 课程学习之外，垂类大模型相比通用大模型的核心优势体现在哪【字节面经合集】
15. 训练稳定性：Loss Spike 的常见原因和处理，Checkpoint 策略与故障恢复，怎么判断训练是否健康，集群通信与网络瓶颈（NVLink、InfiniBand、RoCE）【基模题库】

## 三、微调与 PEFT

LoRA 是这一模块的绝对核心，多篇面经问到，且都问到实现细节而不是概念。

1. LoRA 的底层原理，初始化怎么做的，矩阵 A 和 B 分别怎么初始化，B 为什么初始化为 0，A 可以吗，什么是矩阵的秩【字节多模态、聚合帖-快手2025、腾讯多模态】
2. LoRA 用的秩是多少，为什么不选其他数；用 3x3 矩阵时 rank 怎么选【字节多模态、腾讯多模态】
3. LoRA 和 Prompt Tuning 的区别，分别适合什么场景；Adapter 的具体实现方式；PEFT 了解哪些【快手应用、腾讯多模态、字节多模态】
4. LoRA 到底省了多少参数，加在 Transformer 哪些模块，为什么加在这些模块；QLoRA 有什么改进【腾讯多模态、商汤（见[面经库](../面经/商汤大模型算法应用实习面经（已offer）.md)）、基模题库】
5. LoRA 的梯度更新公式，怎么确定哪些层需要加【CSDN 全攻略】
6. LoRA 用于扩散模型微调（DreamBooth 加 LoRA）的流程和注意事项【基模题库】
7. 模型微调时遇到过过拟合吗，怎么处理的【快手应用】
8. 微调的数据集怎么构建，数据怎么处理；中文领域做 Instruction Tuning 要注意哪些数据问题【腾讯多模态、快手应用】
9. 怎么提高大模型的外推性【腾讯多模态】

## 四、后训练与强化学习

2026 年的明显变化：PPO/DPO 已成常规题，GRPO、DAPO 这类新方法和训练细节追问大幅变多。

### SFT 与 RL 的关系

1. SFT 和 RL 在优化目标上的本质区别，能各举一个能力边界的例子【MiniMax、蚂蚁】
2. 为什么有了 SFT 之后还需要 RLHF【字节豆包、字节多模态】
3. SFT 的流程是什么，数据格式有什么要求；CoT 的原理，怎么让模型具备推理能力【基模题库】

### PPO、DPO 与新方法

1. PPO 和 DPO 的主要思想、Loss 形式、核心差异和各自优缺点，什么场景更倾向用 DPO【字节豆包、MiniMax、蚂蚁、大厂真题、基模题库】
2. PPO 训练流程，Actor、Critic、Reward Model、Reference Model 分别做什么，为什么要 KL 约束，KL 散度系数怎么调，clip 函数的作用【字节Seed、蚂蚁、MiniMax、商汤、基模题库】
3. Critic Model 的作用是什么，有了 Reward Model 为什么还需要 Critic【蚂蚁】
4. GRPO 讲一下，GRPO 里 KL 散度和之前的方法有什么区别，DAPO 为什么舍弃 KL 散度，GSPO 的主要改进，DeepSeek-R1 为什么选 GRPO【字节算法、蚂蚁、聚合帖-美图、基模题库】
5. 最近的 RL 方法过一遍：GRPO、DAPO、GSPO 各自解决什么问题【蚂蚁】
6. 过程监督的信号具体怎么设计，PRM 和 ORM 的区别，过程监督还能应用在哪些地方；Reward Model 怎么设计，对比数据怎么构造，有没有考虑排序一致性【聚合帖-美图、MiniMax、字节算法、基模题库】
7. DeepSeek-R1 里面的奖励设计（奖励函数和奖励模型），第一阶段、第二阶段怎么开展【字节算法】
8. On-policy 和 Off-policy 有什么区别；强化学习基础：MDP 五元组、贝尔曼方程、策略梯度定理、REINFORCE、Q-Learning 和 SARSA 的区别、DQN 的经验回放和目标网络、Actor-Critic、A2C 和 A3C、GAE、探索与利用的权衡【聚合帖-快手2025、基模题库】
9. RLHF 里奖励稀疏问题怎么解决，KL 散度惩罚的作用【基模题库】
10. 比较长的对话怎么做 reward，reward 什么时候用模型什么时候用规则；多轮对话怎么微调，如何保持上下文记忆【字节面经合集】
11. 如何避免奖励坍缩和 Reward Hacking，有什么工程方法【字节面经合集、基模题库】
12. RLHF 和 RLAIF 的差异，Constitutional AI 的原理，RLAIF 在企业级场景的可行性，怎么防止反馈循环里的质量劣化【MiniMax、基模题库】
13. o1/R1 类模型怎么训练长思维链推理能力，推理时 Scaling Law 和训练时的区别，Best-of-N、MCTS、Beam Search 在推理中的应用，自我纠正真的有效吗【基模题库】
14. Verl 框架的训练流程，rollout batch size、global batch size、micro batch size per device for update、rollout n 这些参数的关系，怎么影响每张卡上的样本数【蚂蚁】
15. 怎么把强化学习做到你现在的业务上（三面常见问法，考落地不是考概念）【字节算法】

### 训练细节与稳定性

1. 强化学习数据集的构建方法，RL 数据怎么配比【聚合帖-美图、字节算法】
2. 如何保证 RL 的训练效率，平衡效率和稳定；GRPO 训练中出现全 0 或全 1 的奖励怎么解决【聚合帖-美图】
3. 发现策略崩溃（大量重复或无意义输出）怎么处理：检查奖励模型是否被攻击、增大 KL 惩罚、降学习率、回滚检查点【MiniMax】
4. 熵崩溃是什么概念，怎么观察到【字节Seed】
5. 混合推理怎么做（GPT-5 路线），增强推理时怎么保证通用数据不遗忘【聚合帖-美图】
6. 大模型的灾难性遗忘问题怎么解决【字节豆包】

## 五、推理与部署

这是 AI Infra 和部署岗的主战场。一篇基于 355 条面试记录的统计里，「AI 模型部署」出现 8 次居首，「模型量化」6 次，「vLLM」和「模型漂移」各 4 次【MLOps 洞察】。

### KV Cache 与注意力优化

1. KV Cache 怎么起作用，为什么对长上下文推理很关键，占用多少显存，GQA 的思想是什么【快手应用、字节豆包、CSDN 推理15问】
2. PagedAttention 的工作原理，能否降低显存占用、底层原因；vLLM 的整体架构，PagedScheduler 怎么工作，请求在其内部怎么流转【百度、AI Infra 汇总、MLOps 洞察、CSDN 推理15问】
3. Continuous Batching 解决了什么问题，和静态批处理有什么区别，怎么提高 GPU 利用率【AI Infra 汇总、MLOps 洞察、CSDN 推理15问】
4. prefill 和 decode 阶段有什么区别，为什么 decode 是 memory-bound；什么是 Chunked Prefill，解决什么问题【CSDN 推理15问】
5. FSDP 和 DeepSpeed 怎么实现显存优化，GPU 显存怎么优化（量化、KV cache 分页、梯度检查点、混合精度、ZeRO、offload）【MLOps 洞察、AI Infra 汇总】
6. Mooncake 以 KV-Cache 为中心的 PD 分离设计思路，Prefill 与 Decode 分离部署架构为什么这样设计【AI Infra 面经、基模题库】
7. FlashAttention 的思想和做法，为什么能减少 HBM 访问，v2 为什么外层对 Q 循环，Flash Decoding 的 combine kernel 耗时占比大概多少【字节豆包、AI Infra 面经、CSDN 推理15问】
8. Speculative Decoding 和 Medusa 的实现，投机采样和投机解码的区别，能加速多少，什么情况下反而变慢【美团北斗、CSDN 推理15问、阿里系统计】
9. DiT 的推理框架和 LLM 的有什么异同，dLLM 和自回归模型的本质区别【AI Infra 面经】
10. KV Cache 量化有什么风险，KV Cache 压缩技术有哪些，怎么在不损失精度的情况下减少缓存【CSDN 推理15问、基模题库】

### 量化与压缩

1. 量化的基本概念和方法（PTQ、QAT），INT8 和 INT4 的区别和精度损失，INT8/INT4/FP8 的原理，量化后的坑怎么规避（校准集代表性、关键层保精度）【MLOps 洞察、AI Infra 汇总、CSDN 推理15问】
2. 垂直领域部署成本过高，选蒸馏还是量化，说明原因；蒸馏的方法（软标签、蒸馏到小模型）；剪枝的策略（结构化与非结构化）【MLOps 洞察、CSDN 推理15问】
3. GPTQ、AWQ、FP8 的对比，在多模态、推荐模型上的实践；W8A8 在昇腾上为什么要专用量化后端【美团北斗、vLLM-Ascend】
4. 模型压缩会不会把重要信息丢掉，怎么办；量化到 INT8 后精度下降明显怎么排查（先跑 benchmark，再逐层敏感度分析，关键层混合精度）【聚合帖-腾讯后台、FDE 真题】
5. 模型蒸馏的两种方式（硬标签、软标签），知识蒸馏放在预训练阶段是否合适【蚂蚁、AI Infra 汇总、AI Infra 面经】

### 部署工程与服务化

1. 怎么把大参数模型部署在显存有限的环境，本地部署相比调 API 的优缺点；如果只有单卡 24G 怎么跑 13B 模型（量化选型、PagedAttention 加 FlashAttention、8bit KV cache、CPU offload）【MLOps 洞察、CSDN 全攻略】
2. 怎么判断推理时显卡是算力不足还是显存不足；估算部署 235B、稀疏率千分之三的 MoE 需要多少算力【MLOps 洞察】
3. vLLM 关键参数调优：gpu_memory_utilization、max_num_seqs、max_num_batched_tokens、tensor_parallel_size、swap_space 分别起什么作用，OOM 时先调哪个【第四范式】
4. TP、DP、EP 有什么区别，vLLM-Ascend 和原生 vLLM 是什么关系、为什么做成插件【vLLM-Ascend】
5. 端侧部署的挑战，嵌入式场景怎么平衡精度与功耗；硬件选型 GPU/TPU/NPU 的差异；手机跑 LLM 的关键技术【AI Infra 汇总、MLOps 洞察、基模题库】
6. TensorRT 和 TensorRT-LLM 做了哪些优化，为什么算子融合能提升推理速度【MLOps 洞察、CSDN 推理15问】
7. 推理服务的限流和兜底（令牌桶、优先级队列、降级到小模型或规则回复），请求调度和优先级管理【AI Infra 汇总、CSDN 推理15问】
8. 私有化部署的取舍，模型缓存怎么设计（归一化 hash 命中、语义近似、降调用成本）【AI Infra 汇总】
9. 怎么设计高并发 LLM 推理服务系统，考虑哪些维度【基模题库】
10. 设计支持大模型灰度热更新的流量调度平台（新旧模型分流、无损切换、按用户 ID 一致性路由）【MLOps 洞察】
11. 调用 LLM 为什么用多线程并发，流式输出选 SSE 还是 WebSocket【MLOps 洞察】
12. 多模型路由网关怎么设计（一个机房跑多个模型，按 model 字段路由，OpenAI 兼容协议的价值）【vLLM-Ascend】
13. 大模型推理时的加速思路有哪些【快手应用】
14. 国产芯片（昇腾等）上部署的额外考量：量化后端、融合 kernel、吞吐与显存变化【vLLM-Ascend】

### MLOps 与线上问题

1. 模型漂移：离线指标更优的模型上线后效果反而不如旧版，怎么分析；线上 CTR 远低于离线 AUC 从哪排查【MLOps 洞察】
2. CPU 突然打满怎么排查，什么情况出现死锁、怎么解决【蚂蚁】
3. 有很多服务和告警信息不可能全处理，怎么设计处理机制（消息队列解耦、优先级）【聚合帖-腾讯后台】
4. 怎么设计大模型代码能力的评估体系（pass@k、单元测试通过率、人工评分卡、对抗测试）【CSDN 全攻略】
5. 生产环境模型质量下降怎么发现和修复，怎么做 A/B 测试【Bolna】

## 六、多模态

多模态岗的题目分两类：一类考视觉编码器与大模型的连接方式，一类考具体模型的论文细节。

1. 多模态大模型的整体架构与核心组成模块，视觉特征是怎么喂给大模型的【百度、字节多模态、基模题库】
2. 主流视觉语言 Adapter 的种类和功能原理，Q-Former 是什么，Gate 门控机制原理；连接时用 Q-Former 这种复杂 Adaptor 好还是 LLaVA 的简单 MLP 好，各自优缺点【百度、腾讯多模态、大厂真题】
3. ViT 的图像预处理与特征提取机制，ViT 相比 CNN 在视觉任务的核心优势；视觉 Tokenizer 的原理，VQVAE 和 VQGAN 的区别【百度、基模题库】
4. BLIP、BLIP2、ALBEF 的结构，BLIP 的三个损失函数分别是什么，BLIP2 两阶段怎么训练、有哪些损失，BLIP2 相比 BLIP 有哪些改进，BLIP3 又有哪些改进【字节多模态、大厂真题】
5. Video-LLaMA 的结构，论文里的 CoT 是怎么设计的【字节多模态】
6. CLIP 的架构和训练流程，为什么能做零样本分类，image-text matching loss 有什么缺陷；还了解哪些对比学习方法【腾讯多模态、大厂真题、CSDN 全攻略】
7. SAM、SAM2、SAM3 的架构差异，SAM3 整套训练流程和文本数据集构建【腾讯多模态】
8. Qwen2.5-VL 架构拆解，Qwen-VL 的三个训练流程分别是什么、有什么作用，C-Abstractor 怎么压缩视觉 token；看过 Qwen2.5-VL 技术报告吗，项目里为什么没选 SOTA 模型【腾讯多模态、阿里系统计、聚合帖-美图】
9. LLaVA 的架构设计，图像特征怎么对齐到语言空间，LLaVA-1.5 相比 1.0 改了什么；Unified 多模态和拼接式架构的区别（Gemini、GPT-4o 的设计理念）；多模态对齐训练策略，分阶段解冻的原因【基模题库】
10. IP-Adapter 和图片提示技术的实现原理，ControlNet 的架构设计、训练时为什么只训练副本【基模题库】
11. 主流图像生成模型的底层技术路线：Nano、Image2.0、Seedream 等【百度】
12. 视频理解中怎么解决时序建模难题，3D 点云特征怎么融入现有架构，长视频理解的挑战与方案【CSDN 全攻略、基模题库】
13. 开放题：多实例人脸视频追踪怎么处理镜头切换；怎么用 AI 赋能游戏业务；玩家人数、付费价格曲线一般符合什么分布【腾讯多模态】
14. 数字人、AI 短剧、游戏相关 AI 业务了解多少，怎么评估 Token 消耗规模【腾讯多模态】
15. 多模态 Agent 的核心技术难点是什么，怎么推动落地【Agent 岗面经】

## 七、AIGC 视觉与视频生成

这是今年新增明显的方向，视频生成岗的题目已经形成固定套路：架构对比、时序一致性、评估、工程链路。

### 扩散模型基础

1. 扩散模型的前向和反向过程，DDPM 的原理，DDIM 相比 DDPM 改了什么、采样过程是确定性的吗【基模题库】
2. Stable Diffusion 的架构，Latent Diffusion 的核心思想，VAE 的原理、ELBO 损失由哪两部分组成【基模题库】
3. Flow Matching 和扩散模型的关系，有什么优势，rectified flow 是什么，为什么 Flux 用 MMDiT 和 rectified flow 而不是 U-Net 加 DDPM【基模题库、BFL 指南】
4. GAN 的原理，训练不稳定的原因和改进方法【基模题库】
5. CFG（Classifier-Free Guidance）的原理和作用，为什么提高 CFG Scale 会导致过饱和，生产上怎么调【基模题库、视频生成岗指南】
6. 噪声调度策略有哪些，各自对生成质量的影响；图像生成的主流评价指标 FID、IS、CLIP Score 的计算方式和局限性【基模题库】

### DiT 与视频生成

1. DiT 和 U-Net 扩散模型的区别，为什么 DiT 比 U-Net 扩展性更好；时间步和文本条件怎么注入（AdaLN、adaLN-Zero）【基模题库、阿里系统计】
2. Sora 类文生视频模型的技术挑战：时序一致性、物理合理性、长视频计算量、训练数据稀缺；时序一致性怎么保证（3D 时空注意力、视频 VAE 时序压缩、运动先验）【基模题库、阿里系统计】
3. 视频生成的 VAE 设计，为什么时间维度也要压缩，怎么保证隐空间连贯性；多 shot 或故事级生成系统和单片段生成的区别【基模题库、视频生成岗指南】
4. 怎么评估视频输出里的时序幻觉（temporal hallucination），有什么自动化指标；用光流怎么改善拼接片段的一致性【视频生成岗指南】
5. 怎么在小数据集（比如 50 个片段）上微调视频扩散模型不过拟合；怎么保证品牌视觉风格的一致性【视频生成岗指南、BFL 指南】
6. 场景题：设计每天生成 500 个个性化产品演示视频的流水线；设计帧一致的视频生成 pipeline；客户说某段帧人脸变形了，不重新生成整条怎么修【视频生成岗指南、Pika 指南】
7. 怎么强制物理真实感（阴影方向、流体、刚体运动），physics-aware loss 和仿真条件生成【视频生成岗指南】
8. DiT 的分布式训练怎么设计（DP/TP/SP、activation checkpointing、bf16），推理平台怎么在延迟预算内保证质量（少步采样、蒸馏、分级路由）【BFL 指南】
9. 视频编解码基础：HEVC、VP9、AV1 的差异，为什么视频生成岗也要懂 codec【Pika 指南】

## 八、RAG 与 Agent

应用向岗位的核心区，题目从原理很快落到场景设计。Agent 模块在今年被拆得很细：Memory、Tool、规划、多 Agent 各自独立出题。

### RAG

1. RAG 的核心逻辑，GraphRAG 的做法，向量数据库、相似度计算、chunk 切片策略【字节豆包、腾讯多模态、商汤】
2. 设计流程里文本 chunk 怎么做的、为什么这么做，遇到什么困难，怎么提高召回；文本输入大模型后效果不好怎么办【腾讯多模态】
3. 场景题：有医疗或法律等专业领域知识，要搭一个智能助手，RAG 链路怎么设计【字节豆包】
4. RAG 的架构设计，怎么评估和优化检索质量【基模题库】
5. 怎么提升大模型的多轮对话能力，有哪些可改进的点【字节豆包】

### Agent

1. 对 Agent 的理解，大模型智能体是怎么工作的、有哪些组件，Agent 有哪几部分构成、了解哪些具体实现方法【腾讯多模态、百度】
2. Agent 核心技术模块的理解，各模块功能和难点，模块之间的联动逻辑【Agent 岗面经】
3. Memory 模块深挖：短期记忆、长期记忆的存储方式、更新策略、检索机制；怎么优化检索效率和准确性适配长上下文；怎么避免 Memory 冗余提升推理连贯性【Agent 岗面经】
4. 记忆怎么分类：临时上下文、情景记忆、语义记忆、偏好记忆、任务记忆各是什么，每条记忆应包含哪些字段，敏感信息怎么处理【小鹏语音】
5. 跨轮对话的上下文怎么压缩同时不丢关键约束（结构化状态：目标、约束、已确认、待确认、待办）【小鹏语音】
6. "推理断层"和"结果与目标偏离"怎么解决（提示工程、多轮推理、自我纠错、Reflexion）【Agent 岗面经、面试鸭】
7. Tool Usage：怎么设计工具选择策略，怎么解决工具调用的兼容性、准确性问题，多工具协同怎么举例【Agent 岗面经】
8. AutoGen、LangChain、LangGraph 等框架的使用经验，核心优势和局限性，基于框架做过什么二次开发；LangGraph 是什么样的框架【Agent 岗面经、火山引擎（见[面经库](../面经/后端秋招凉经汇总（B站百度字节美团）.md)）】
9. Agentic Search 是什么，和传统搜索、RAG 的核心区别，关键技术点，怎么端到端优化【Agent 岗面经】
10. Agent 工具获取的日志很多、上下文窗口有限怎么办；大模型压缩会不会把重要信息丢掉【聚合帖-腾讯后台】
11. workflow 和 agent 的主要区别；复杂 Agent 流程能否直接封装成 Skill；MCP、A2A 协议了解吗【字节面经合集、火山引擎（见[面经库](../面经/后端秋招凉经汇总（B站百度字节美团）.md)）、面试鸭】
12. 多 Agent 协作：固定的"感知-推理-校验"流程和动态多 Agent 的区别，哪些能并行哪些要顺序，结论冲突怎么处理【商汤（见[面经库](../面经/商汤大模型算法应用实习面经（已offer）.md)）】
13. 长上下文场景怎么优化推理架构（上下文压缩、分层推理）；ReAct 和 Plan-and-Execute 怎么选，怎么定义复杂任务【Agent 岗面经、火山引擎（见[面经库](../面经/后端秋招凉经汇总（B站百度字节美团）.md)）】
14. 有没有参与过 Agent 系统的工业级架构设计；你怎么理解 Agent 的设计【Agent 岗面经、火山引擎（见[面经库](../面经/后端秋招凉经汇总（B站百度字节美团）.md)）】
15. Claude Code 类 Agentic Coding 工具的原理：Agent Loop、规则文件、上下文压缩、权限系统、子代理【面试鸭】
16. 基于 Qwen3 搭建代码补全 Agent，Tokenizer 模块会遇到哪些工程问题，怎么解决【百度】

## 九、语音与实时交互

车载和语音助手方向在今年形成了一套固定问题：流式架构、端点检测、数据集泄漏、指标体系。

1. 详细介绍语音交互平台的流式架构：前端降噪、回声消除、VAD、唤醒，后端流式 ASR、语义解析、对话管理、工具调用、流式 TTS，一次请求的完整链路【小鹏语音】
2. 复合指令（"打开空调并把温度调到 24 度"）怎么处理：任务图识别、动作依赖判断、安全操作二次确认和权限校验【小鹏语音】
3. 系统指标体系：首包响应时间、端到端完成时间、指令执行成功率、错误车控率、打断成功率、弱网重连成功率、长对话状态漂移【小鹏语音】
4. 语音数据集怎么构造，怎么避免训练测试集泄漏（按说话人或场景组切分，检查录音切片、噪声增强版本、伪造数据同源、分布失衡）【小鹏语音】
5. 训练语音大模型时 loss 不下降或突然 NaN 怎么定位（固定种子单卡复现，按特征、标签、mask、logits、loss、梯度逐层检查，FP16 溢出切 BF16）【小鹏语音】
6. CTC、Transducer、Attention Encoder-Decoder 分别解决什么问题，各适合什么场景；流式场景还要比什么（首字延迟、稳态延迟、部分结果回退次数）【小鹏语音】
7. 流式 ASR 为什么会出现 partial result 回退，怎么减少（稳定前缀策略、token 稳定计数、延迟提交、二阶段重打分）【小鹏语音】
8. VAD 和端点检测为什么误切句，怎么设计更稳健的策略（双阈值、状态机、和语义状态联动）【小鹏语音】
9. 怎么设计低延迟的 ASR 到 LLM 到 TTS 实时语音管线；流式 TTS 怎么实现以减少首音频时间；嘈杂音频输入怎么处理不打断下游【Bolna】
10. CTC 的原理，beam search 在 ASR 解码中是什么，语音识别评测指标（WER、CER）【语音题库】
11. TTS 的主要技术流程，Whisper 的架构，音频 Tokenization【语音题库、基模题库】
12. 怎么提升语音识别系统的鲁棒性【语音题库】

## 十、推荐与搜广推（含 LLM4Rec）

推荐岗的题目在 2026 年明显向大模型倾斜，且保留了对特征工程和多目标的传统考察。

1. 为什么在推荐系统里引入 RQVAE，怎么解决坍缩问题【字节推荐】
2. RankMixer 介绍一下，组内做 LLM4Rec 的话业务怎么结合【字节推荐】
3. Transformer 计算的时间和、空间复杂度，如果 QK 变成同一个矩阵会有影响吗，一定要变的话怎么解决【字节推荐】
4. BN 和 LN 的区别，什么场景用哪个【字节推荐、快手应用】
5. BERT 的预训练任务是什么【字节推荐】
6. 精排融合公式有哪些目标，多目标怎么融合，帕累托怎么理解【字节推荐】
7. 怎么挑选特征，对推荐算法特征工程的心得【字节推荐】
8. 最近读的论文，大模型的论文读过吗，讲一个【字节推荐】
9. LHUC 模块单独搭建输入 Embedding 层和直接复用模型主干 Embedding，效果与训练逻辑有什么差异【字节面经合集】
10. 新用户交互行为稀疏、早期 Embedding 训练效果差，有什么落地优化方案；冷启动从基础特征主导切换到用户 Embedding 主导，网络结构层面怎么实现【字节面经合集】
11. 搜广推的经典考察点：协同过滤、矩阵分解等仍会在搜推岗位出现【阿里系统计】

## 十一、手撕代码题库

按本合集出现次数排序列出。字节系对 MHA 和交叉熵有执念，AI Infra 岗大量出 CUDA 和 PyTorch 底层题，AIGC 岗则偏爱带数值味道的 medium 题。

### 出现 2 次以上

1. 手撕 Multi-Head Attention，要求能支持 cross attention，PyTorch 实现【字节算法、字节多模态、字节推荐】
2. 二叉树的右视图，要求实现列表转二叉树【字节推荐、聚合帖-腾讯后台】
3. 实现交叉熵函数【字节推荐】
4. LRU 缓存机制【AI Infra 面经、Agent 岗面经】
5. 合并 K 个升序链表【字节豆包、Agent 岗面经】
6. 二叉树的层序遍历【Agent 岗面经】

### 各出现 1 次

- 合并区间、分割等和子集【字节豆包】
- 编辑距离【字节算法】
- 字符串的全排列、二叉树序列化与反序列化【快手应用】
- 最大正方形【百度】
- 最小生成树【蚂蚁】
- 单调栈类、滑动窗口类【字节Seed】
- 链表相加（双指针）【字节面经合集】
- 买卖股票的最佳时机 I 到 IV 四道连问【百度】
- 最长公共子序列【大厂真题】
- 快排【腾讯多模态】
- 两数之和 II（双指针，O(n) 时间 O(1) 空间）、字符串解码、二叉树的最近公共祖先（BST 和普通二叉树两种场景）【Agent 岗面经】
- 核心代码模式：写大模型预测 token 时 beam 树怎么构建、怎么得到最终结果【蚂蚁】
- 链表倒数第 k 个节点、数组中能组成三角形边的数量【聚合帖-腾讯后台】
- 模拟类非 Hot 100 中等题【聚合帖-美图】
- 实现一个 Tokenizer，只能用 PyTorch 基础语法【百度】

### AI Infra 与模型实现专项

1. C++：实现内存池，支持类似 new Foo[]、delete[] 的功能；比较两个 float 是否相等【AI Infra 面经】
2. CUDA：实现支持 torch broadcast 的 4D tensor elementwise 乘法；计算 (A * B) * C，其中 A(1,256)、B(256,128)、C(128,256)；Embedding Sparse Feature Pooling（100 万个离散 ID 加 100 万个 float，聚合成长度 1000 的数组）【AI Infra 面经】
3. PyTorch：实现 LoRA Adapter【AI Infra 面经】
4. 算法：岛屿个数、Hamming Weight、K-Coverage Intervals【AI Infra 面经】
5. 八股：torch.repeat 和 torch.expand 的区别；torchrun 启动参数有哪些，怎么批量 kill torchrun 进程；Hopper TMA 的优点、调用方式、是否经过 L1【AI Infra 面经】
6. 基模题库的 13 道代码题（可当自测清单）：Scaled Dot-Product Attention（含 causal mask）、MultiHeadAttention 模块、RoPE、BPE Tokenizer、Top-p 采样、LoRA 层、KV Cache 推理循环、DDPM 前向加噪与 loss、DPO 损失、MinHash 去重、Beam Search、FlashAttention 分块伪码、LayerNorm 前向加反向【基模题库】

## 十二、场景与开放题

这类题没有标准答案，考的是链路完整性：能把问题拆成阶段、每个阶段有方案、方案有取舍。

1. 如何搭建训练数据构造 Pipeline（数据来源、清洗、配比、质检、迭代闭环）【字节算法】
2. 电商场景用大模型解决问题，Prompt 怎么设计，怎么处理模型输出，怎么过滤错误格式的输出【字节多模态】
3. 如果为一个通用助手模型做后训练，数据配比和训练阶段怎么设计【MiniMax】
4. 后训练项目里效果提升最大的一个改动是什么，怎么确定是它起的作用（消融实验设计）；画出训练 pipeline 的整体架构，包括数据流、模型更新流程、评测环节的插入位置【MiniMax】
5. 你觉得当前大模型还存在怎样的问题，有什么解决办法；后训练方向最大的技术瓶颈是什么，有足够资源会优先解决哪个【百度、MiniMax】
6. 让你自己设计一个 Agent 会怎么做，为什么这样做；怎么训练一个大模型可以做到精确提取摘要【百度】
7. 拿到业务需求如何拆解、定义问题；项目中有哪些踩坑、效果不佳的经历；怎么评估校验模型中间输出与最终结果的正确性【字节面经合集】
8. 用过豆包吗，觉得目前还存在什么问题；对文心一言这个产品了解吗，有哪些优点和值得改进的点；如果给你 Offer 到这个团队能做出什么贡献【字节豆包、百度】
9. Oncall 场景：很多告警不可能全处理，怎么设计处理机制【聚合帖-腾讯后台】
10. 怎么设计大模型灰度热更新的流量调度平台；AI 生成内容传到前端，流式输出选哪种方式【MLOps 洞察】
11. 2026 年大模型 Agent 落地最容易遇到的技术瓶颈是什么，有什么解决思路；关注哪些前沿趋势（多智能体协作、工具生态融合、低资源优化）【Agent 岗面经】
12. 结合团队业务，你认为可以在哪些方向技术创新和突破【Agent 岗面经】
13. 怎么把 revision 反馈系统化转成 prompt 修改（视频生成场景）【视频生成岗指南】

## 十三、按公司速查

| 公司 | 方向 | 主要来源 | 最鲜明的考察点 |
| --- | --- | --- | --- |
| 字节（算法/豆包/多模态/Seed/推荐） | 大模型算法、多模态、推荐 | 牛客 6 篇 | 手撕 MHA 与交叉熵、RL 落地到业务、多模态论文细节 |
| 阿里（淘天） | 多模态大模型 | 大厂真题、阿里系统计 | BLIP 三代演进、Qwen-VL 训练流程、DiT 与扩散知识点统计 |
| 百度（TPG 文心） | 大模型算法 | 牛客、大厂真题 | 位置编码优缺点、幻觉与复读、股票四连问、Tokenizer 实现 |
| 腾讯（PCG/多模态） | 多模态、NLP | 牛客、大厂真题、聚合帖 | SAM/CLIP 论文级细节、BERT 与 HMM 基础、快排 |
| 蚂蚁 | 大模型算法 | 牛客 | Verl 框架参数细节、GRPO/DAPO 演进、beam 搜索实现 |
| MiniMax | 后训练/SFT/RL | 牛客 | 训练超参细节、策略崩溃处理、归因分析 |
| 快手 | 大模型应用 | 牛客 2 篇 | RMSNorm、Softmax 加速、中文 Instruction Tuning 数据问题 |
| 小鹏汽车 | 语音大模型 | 牛客 | 流式 ASR 架构、端点检测、数据集泄漏、指标体系 |
| 第四范式 | AI Infra | CSDN | vLLM 参数调优、量化与微调落地 |
| 美团（北斗） | AI Infra | 博客园 | 3D 并行通信开销、Speculative Decoding、量化实践 |
| 各家 AI Infra 汇总帖 | 推理/训练框架 | 牛客 2 篇、CSDN 2 篇 | CUDA 算子、vLLM 架构、PD 分离、Chunked Prefill |
| 海外 AIGC 团队（Pika/BFL） | 视频/图像生成 | techinterview、futurevocation | DiT 架构对比、时序一致性、生成管线系统设计 |
| Bolna | 语音 AI | knok.work | 实时 ASR 到 LLM 到 TTS 管线、线上质量监控 |

题库和指南类来源（基模题库、面试鸭、语音题库、视频生成岗指南）不按公司分，适合当自测清单用；其中基模题库有 130 余题的完整目录，面试鸭按知识点分类。

## 十四、用法建议

1. **先扫模块一和模块十一**。基础题和手撕题是入场券，这两块不过，项目讲得再好也走不到后面轮次。
2. **RL 细节是 2026 年最大的增量**。只背 PPO/DPO 概念已经不够，GRPO、DAPO、KL 系数、奖励崩塌处理这些要能讲到数值层面。手里没有真跑过 RL 的，按[大模型与 AI 面试高频题](./大模型与AI面试高频题.md)的 RL 章节搭一个最小训练实验，把超参和日志记下来。
3. **推理优化是 Infra 岗的分水岭**。模块五的题大多围绕"用显存管理换吞吐"这一件事，PagedAttention、Continuous Batching、量化三件套要能脱稿讲 3 分钟并配项目实例。
4. **按目标岗位选模块**。面大模型公司（MiniMax、字节 Seed、蚂蚁）重点模块二到四；面 Infra 岗重点模块五；面多模态岗把模块六当论文复现准备；面 AIGC 岗补模块七；面车载语音补模块九；面搜推岗保留模块十的传统题。
5. **场景题用同一套结构答**：先问清场景和约束，再给分阶段方案，最后讲降级和取舍。模块十二的题都可以这么拆。
6. **每道题标注自己的状态**。建议复制这份合集到自己的笔记里，逐题标"能讲 3 分钟/讲过但接不住追问/没准备过"，优先补第二类。
7. **配合真题源使用**。文末来源里，基模题库有 130 题的完整目录和代码题，面试鸭按知识点分类，适合当自测清单；统计帖（MLOps 洞察、阿里系统计）用来看趋势。

## 来源清单

### 牛客网

| 简写 | 公司与方向 | 链接 |
| --- | --- | --- |
| 字节算法 | 字节大模型算法，26 届秋招 | https://www.nowcoder.com/feed/main/detail/029a292419294b4a8227acde5a00124b |
| 字节豆包 | 字节豆包大模型 | https://k.sina.cn/article_7879848900_1d5acf3c401902w8iw.html |
| 字节多模态 | 字节多模态大模型，26 届校招 | https://www.nowcoder.com/feed/main/detail/ce451a35177e487f916fe34374ad9df8 |
| 字节Seed | 字节 Seed 秋招面试复盘 | https://www.nowcoder.com/feed/main/detail/8bc9b04f56f54d0291515e0306e3b4bd |
| 字节推荐 | 字节推荐算法，26 秋招 | https://www.nowcoder.com/feed/main/detail/4781b16b8dec4313bfca45b9445f5c53 |
| 字节面经合集 | 字节大模型算法岗面经 01 到 05 | https://www.nowcoder.com/discuss/921942397339082752 |
| 腾讯多模态 | 腾讯多模态算法岗一二面 | https://www.nowcoder.com/feed/main/detail/51ecce470a9444d7b5e1cde1f038b72d |
| 百度 | 百度大模型算法岗 | https://m.nowcoder.com/feed/main/detail/8eabfefc27d845f9ab6d6e147849aad3 |
| 快手应用 | 快手大模型应用算法，26 届校招 | https://www.nowcoder.com/feed/main/detail/bc89e6d705794c81838dd48c4a46acd9 |
| 蚂蚁 | 蚂蚁金服大模型算法一面，26 秋招 | https://m.nowcoder.com/feed/main/detail/e2585943c7874b3081b0878b646b6f01 |
| MiniMax | MiniMax 大模型算法，后训练/SFT/RL 方向 | https://ac.nowcoder.com/discuss/1673338 |
| AI Infra 汇总 | AI Infra 面试汇总（含回答思路） | https://www.nowcoder.com/discuss/891334000239734784 |
| AI Infra 面经 | AI Infra 面经（CUDA/PyTorch 手撕向） | https://www.nowcoder.com/feed/main/detail/d695614a06424c148c04586ac3a66e78 |
| 阿里系统计 | 2025-26 算法工程师面试常见问题整理（阿里系，含知识点出现次数统计） | https://www.nowcoder.com/discuss/848942791164981248 |
| 小鹏语音 | 小鹏汽车语音大模型算法一面 | https://www.nowcoder.com/discuss/926067939990568960 |
| MLOps 洞察 | 2025-2026 年 AI 部署与 MLOps 面试高频知识点洞察（约 355 条记录） | https://ac.nowcoder.com/discuss/1673368 |

### CSDN 与 GitCode

| 简写 | 内容 | 链接 |
| --- | --- | --- |
| 第四范式 | 第四范式一面（vLLM 与量化微调） | https://blog.csdn.net/XLYcmy/article/details/163343473 |
| CSDN 推理15问 | 大模型算法工程师面试题精讲：推理优化高频 15 问 | https://blog.csdn.net/lishengzhen123/article/details/162089280 |
| CSDN 全攻略 | AI 大模型面试全攻略（理论与工程实践） | https://devpress.csdn.net/v1/article/detail/164009160 |
| vLLM-Ascend | vLLM-Ascend 企业级实战（含面试题） | https://yushi-javatoai.blog.csdn.net/article/details/166007256 |
| Agent 岗面经 | 大模型 Agent 应用算法岗面试经验（2026 年版） | https://gitcode.csdn.net/69f1b0d154b52172bc70bb2b.html |
| 聚合帖-腾讯后台/美图/快手2025 | 2026 大厂大模型与 Agent 面试题聚合（CSDN 转载牛客帖） | https://gitcode.csdn.net/6a236d7b662f9a54cb7a2bf1.html |

### 其他网站与个人博客

| 简写 | 内容 | 链接 |
| --- | --- | --- |
| 大厂真题 | 百度/腾讯/阿里大模型算法岗面试真题解析（尧图网转载，含百度 TPG 文心三面、腾讯 PCG 实习两面、阿里淘天多模态三面） | https://www.mwwr.cn/news/29748 |
| 基模题库 | 生成基模团队面试题全集（17 模块 130 余题加 13 道代码题） | https://song2yu.github.io/world-model-vla/genai_interview.html |
| 美团北斗 | 美团北斗 AI Infra 面试收录 | https://www.cnblogs.com/xmwblogs/p/19669357 |
| FDE 真题 | FDE 面试真题（vLLM 与量化排查，源自 CSDN，存于 ima 知识库） | https://ima.qq.com/wiki/?shareId=b174c82f988366d735e5d57a34e5e35afe16bf7d271c984f1438c89e0612eb8f |
| 语音题库 | 语音行业面试题（CTC、beam search、WER、TTS） | https://m.shuashuati.com/paper/a0f58b7b34fd4e049d282a32d763f703.html |
| 视频生成岗指南 | AI Video Generation Specialist Interview Questions | https://www.futurevocation.com/interview/ai-video-generation-specialist |
| Pika 指南 | Pika Labs Interview Guide 2026 | https://www.techinterview.org/companies/pika-labs-interview-guide |
| BFL 指南 | Black Forest Labs Interview Guide 2026 | https://www.techinterview.org/companies/black-forest-labs-interview-guide |
| Bolna | Bolna 语音 AI ML 工程师面试 | https://knok.work/blog/bolna-machine-learning-engineer-interview.html |
| 面试鸭 | 人工智能面试题库（AI Agent、大模型、Claude Code 等分类） | https://mianshiya.com/?category=ai |

以上均为公开发布的个人面试分享或题库整理，只保留公司与问题脉络，未收录作者个人信息。题目表述按原意转写，个别口语化问题做了书面化处理；转载帖中的推广内容已剔除；如与原帖有出入，以原帖为准。大厂真题一文覆盖百度、腾讯、阿里三家公司，正文中标了百度、腾讯多模态、大厂真题的题目都可能出自该文。
