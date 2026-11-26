---
name: rl-tuning
description: 为 GRPO/PPO 大模型训练选择、设计和判收端到端吞吐调优实验，适用于 rollout、reward、old/ref log-prob、Actor update 和权重同步，覆盖目标差距、训练语义、数值、显存和收益组合。局部推理或 SFT 用相应专项流程。
---

# RL 训练调优

每轮交付当前可用的父配置、距目标的秒数、首选实验及备选、最小验证、晋级和停线条件。结果回来后用有效对照更新缺口和实验队列。在工作区内按[正式数据标准](references/experiment-data-standard.md)登记实验和运行。以本轮授权决定是否执行。文档任务交付可以交接的实验登记与判据。

项目数据根 $RL_TUNING_ROOT 指向 **10-RL-Tuning 本身**。未设置时向上定位这个目录或包含它的 RL 工作根。入口可独立使用。项目事实和历史阈值从本次任务或数据根读取。

启动新轮次时先写一张能交给执行方的实验卡。把项目目标、可用父运行和同窗吞吐换成秒数预算，让首选候选和至少一个备选按同一工作量比较。若预算只允许做一次观察，说明这项观察的两种结果各会改变什么决定。已有结果回来时直接从 S4 进入，恢复暂停路线时先核实原停线条件的哪一项已经改变。

| 阶段 | 做出的决定与产出 | 按需读 |
|---|---|---|
| S0 立项 | 冻结实际父配置和计分协议，将目标与实际工作量换算为必要秒数，登记质量和资源限制 | [口径](references/01_measurement.md) · [RL 语义](references/07_rl_theory.md) |
| S1 归因 | 核对实际路径。把关键路径的观测、重叠、可消除上界和待查差额入账，列竞争解释 | [实验手册](references/00_playbook.md) · [失败类型](references/06_failure_catalog.md) |
| S2 选实验 | 按缺口、净收益上界、能改变的决策、成本和风险排列候选。登记真实对照、最小完整路径、预期命中回执和结果分支 | [实验手册](references/00_playbook.md) · [实验卡](templates/experiment.md) |
| S3 验证 | 按授权覆盖待测假设的最小路径。核对实际生效配置、首命中、进展、真实退出和产物 | [实验手册](references/00_playbook.md) |
| S4 判收与重排 | 分项判完整性、机制、吞吐、语义、质量、余量与发布。共同父配置复核组合收益。用有效结果刷新缺口和队列 | [口径](references/01_measurement.md) · [质量门](references/05_precision_semantics.md) |
| S5 冻结与 RSI | 按运行和计分身份固化取舍及重开前提。候选规则经反例和回放后试用，再记录真实轮次表现 | [归档与 RSI](references/08_reporting.md) · [轮次模板](templates/campaign.md) |

生成或 Reward 慢时读[生成与奖励](references/02_gen_rollout.md)。Actor、Ref 或 refit 慢时读[训练与同步](references/03_update_train.md)。OOM、并置或回驻问题读[显存](references/04_memory.md)。

项目预登记性能、质量、整卡余量和完整性阈值。调整时记录授权、生效范围、原判与复判。涉及概率来源、采样、奖励、分组、掩码、损失或归一化时，核对实际训练语义和信号量。

需要建立历史文档索引时运行 `python3 scripts/build_index.py --root <资料目录> --out-dir <项目数据根>/data/index`。脚本输出 Markdown 浏览页与 TSV 索引。
