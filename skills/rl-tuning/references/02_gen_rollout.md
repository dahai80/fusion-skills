# Rollout 与 Reward

先用同上下文及响应长度分布拆解 prefill、decode、调度、服务等待、RM 和权重同步。记录实际运行的引擎、TP/DP、graph 模式、KV 容量/占用、preemption 和 prefix 命中。聚合计数必须能绑定角色、进程和窗口。用一致输入观察并发曲线，容量足够时批更宽仍可能抬高 decode step 时延。

扩容预算先用当前点和一组有判别力的并发对照，观察生成吞吐、decode 步时、抢占与整卡余量。把容量与吞吐的比例关系登记为待验假设。方向分清后，再在拐点附近加测。

| 证据 | 候选 | 复核 |
|---|---|---|
| 服务存在可归因的排队且设备吃不满 | 请求并发、调度和批上限 | 客户端排队与服务批次一起看 |
| 引擎有 KV preemption 或 OOM | KV 预算、并发、缓存释放策略 | 全步及跨步回驻，保留 Reward 和 Actor 余量 |
| decode 核耗时高 | 兼容的图形态、dtype 或实现 | 按长度/批宽对比，验证日志命中和真实生成 |
| RM 服务候选 | prefix cache、客户端并发、分片 | 检查 reward 数值、顺序和按样本关联 |

区分 rollout 权重量化、KV cache dtype 与 Actor update 混精。需要权重重载的量化方案同时验证首轮、更新后重载、后续步生成和 Ref/Actor 显存门。同步成本在主指标里计全。确保采样参数、模型版本、tokenizer 和 truncation 与设计一致。异步流水线增加 policy lag 时记录样本策略版本和重要性权重契约。
