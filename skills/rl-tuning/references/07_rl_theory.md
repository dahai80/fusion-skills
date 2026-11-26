# RL 训练的变更契约

在真实 trainer 和 loss 中追踪四路概率及策略版本。相同字段名在不同栈可能指不同数据流。

| 概率 | 含义 | 调优时查什么 |
|---|---|---|
| rollout log-prob | 生成引擎给出采到动作时的概率记录 | checkpoint、温度、top-k/p 与采样后是否重归一化，真实行为分布与日志值是否相符 |
| old log-prob | PPO/GRPO 更新使用的冻结分母，可能由训练栈重算或来自 rollout | 计算引擎、快照、mask、更新过程中是否保持冻结 |
| current log-prob | 当前 Actor 对同一批动作的概率，参与梯度 | 对齐 token shift、输出范围及有效位置，保留前向和反向路径 |
| ref log-prob | 相对参考策略的 KL 或奖励项输入 | Ref checkpoint、是否计算与更新、KL 在 reward 或 loss 哪一侧 |

以常见 PPO surrogate 为例，r = exp(logp_current − logp_old)，将 r 与 clipped r 乘 advantage 形成裁剪目标。真实实现可能在 token 或 sequence 层聚合，也可能另用 rollout 概率计算重要性采样校正。有偏行为策略、训推差异及 rollout 版本落后会影响权重尾部和有效样本。查实际 ratio、校正、裁剪、过滤和 KL 估计器，不能只比较平均 LP。训练栈重算 old 和直接复用 rollout 的 bypass，视两侧输出和算法契约可能改变分母及裁剪。按语义变更评估，保留该项目已经批准的用法与边界。

GRPO 常按同一 prompt 的多条响应估计组内相对 advantage。核对组大小、组完整性、全同奖励、归一化 epsilon、是否除组内标准差、剪裁和长度偏置。PPO 使用 critic/GAE 时还须查 value、done/截断和 bootstrap。改变采样参数、取消长响应、超时补样、RM 跳算、mask 或每 token/每序列 reduction，会影响目标或训练分布，应比较有效样本与 advantage 分布。仅紧缩投影到有效响应行时，需证实目标涉及的所有行都保留且分母和梯度聚合不变。
