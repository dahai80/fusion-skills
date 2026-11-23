# fusion-skills

fusion 生态公共内容仓库：收录精选 **插件（plugins）**、**连接器（connectors）**、
**技能（skills）**。fusion 站点插件市场（fusion-site）以本仓库为内容源——
每张市场卡片链接到这里的对应文档；`registry.json` 是机器可读的映射表
（id、类别、来源模块）。

## 目录结构

- `apps/` — 宿主应用（console、cowork、agent-studio）：市场的消费端，不是市场的商品
- `plugins/` — 宿主模块插件（文件访问、文档处理、行情面板等）
- `connectors/` — 本地服务连接器（推理、图像/视频生成、语音）
- `skills/` — 智能体技能（联网检索、长文写作、代码评审、昇腾推理优化、UI/UX 设计、单页报告）
- `registry.json` — 供各 fusion 界面消费的目录映射

## 安装

安装与更新在 [fusion Shell](https://github.com/dahai80/fusion-web-shell) 内完成
（需 fusion 账号）；本仓库是可浏览的内容来源。

## 与其他仓库的关系

- `fusion-plugins-ecosystem` — 插件运行时框架（PluginManifest 注册表）
- `fusion-site` — 公开市场界面；只保存映射，不保存内容
- `fusion-web-shell` — 安装/更新交互入口
