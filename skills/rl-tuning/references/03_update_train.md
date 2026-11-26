# Actor、Ref 与 refit

按前向、log-prob/head、重算、反向、梯度同步、优化器和上下卡拆 Actor。记录有效 token、微批数、打包长度和最慢 rank。通信累计量用来识别热点，确认落到关键路径的暴露时间后再按可能节省定价。移除同步之后复核下游阻塞与 wall，设备实际工作会向下一个同步点转移。

- **改变分片或微批**。先确认 DP/SP/TP 与梯度缩放和归一化，动态预算和实测微批最大 shape 分开记录。检查分片换拓扑后的通信与驻留峰。
- **优化 head 或减少无效行**。从实际 loss、entropy、KL 和辅助输出核对掩码，确认 token shift、label、序列边界和 reduction。用真实固定批对拍有效 log-prob、loss 分项、dHidden/dWeight 等。分布式下含极端长度、不均衡和空 response rank 的处理。
- **Ref 前向**。复用代码需重新核对角色、温度、forward-only、输入和目标输出。在 Actor 通过的梯度对拍不能直接充当 Ref 的 log-prob 验收。维持 Ref 身份与更新规则。
- **权重桥**。核对参数名、dtype、shard、元数据和 consumer 接口。记录 Actor 上下卡和 rollout refit 的窗口、屏障、KV ready、步间版本对应关系。用小接口探针再进完整训练。估收益时区分遍历、搬运、屏障和回驻，避免对父子计时重复结算。
