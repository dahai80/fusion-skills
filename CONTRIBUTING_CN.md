# fusion-skills 入库指南

本仓库是 fusion 生态的公共目录：plugins / connectors / skills / 宿主应用。
`registry.json` 是宿主应用（console、shell、cowork）与 fusion-site 市场共同
消费的机器可读映射。

**安装自动化与上传方式无关** — 取决于 registry 条目是否带"机器可解析指针 +
完整性锚"：

- 二进制资产 → Release 资产直链 + sha256
- 仓库内 skill → 消费端按 commit SHA 锚定拉取

## 什么放哪

| 类型 | 载荷位置 | registry 字段 |
|------|----------|----------------|
| skill（纯文本） | 本仓 `skills/<id>/`（`SKILL.md` + 文件） | `source_path`（仓内路径），可选打包 `artifacts` |
| plugin | 源仓库 GitHub Releases | `artifacts: [{os, arch, url, sha256, size}]` |
| connector | 源仓库 GitHub Releases | `artifacts`（同上） |
| app（宿主） | 各自仓库 GitHub Releases | `releases` 页链接，可选 pin 的 `artifacts` |

二进制一律不放本仓 — git 放文本，Releases 放包。

## 入库路径

1. **直接 PR（随时可用）** — clone → 放文件 → 更新 `registry.json` → PR。
   CI 自动校验 schema。merge 即发布，宿主下次刷新即生效。
2. **自动管线（fusion-plugins-ecosystem#76，规划中）** — 模块发 Release 后
   由管线算 sha256 并自动开 registry PR。
3. **社区提交** — 当前同为 PR 路径；后续可能切换为 marketplace API 提交流。

## Skill 自动打包

每次 push 到 `main` 触碰 `skills/` 后，CI 会把变更的 skill 打成
`skill-<id>-<短sha>.tar.gz` 附到本仓 `skills-auto` Release，并发布 SHA256SUMS。
仓内 `source_path` 仍是主安装锚（消费端 pin commit SHA）；打包资产是便利镜像，
sha256 随包发布 — 偏好压缩包的宿主可直接从 Release 解析，无需任何人工步骤。

## 训练器挖掘的技能库

由训练 rollout 挖掘的技能（fusion-trainer#123：`ft skills mine`）与人工编写的
skill 走同一套 `kind=skill` 入库流程。用可选的 `provenance` 字段标注来源，
消费者可在注入前执行防投毒策略：

```json
{
  "id": "my_mined_skill",
  "kind": "skill",
  "source_path": "skills/my_mined_skill/",
  "doc": "skills/my_mined_skill/SKILL.md",
  "provenance": {
    "origin": "trainer-mined",
    "run": "fusion-trainer#123",
    "evidence_count": 42,
    "verifier": "grpo-verifier-v1"
  }
}
```

- `origin`（有 `provenance` 时必填）：`human-authored` 或 `trainer-mined`
- `run`：训练器 run / 追踪引用，用于溯源回链
- `evidence_count`：准入时支持的 rollout 引用数量
- `verifier`：准入该技能的校验器摘要

机器载荷（版本化技能库 JSONL）以 release 资产形式挂入 `artifacts[]`，完整性
规则与 plugin 相同；文本载荷也可留在仓内 `source_path` 下。运行时注入见
fusion-harness#174。

## registry PR 自查清单

- [ ] `id` 唯一，`kind` ∈ plugin | connector | skill | app
- [ ] description 中英双语齐全
- [ ] `doc` 指向的文档真实存在
- [ ] 仓内 skill：`source_path` 指向技能目录（如 `skills/<id>/`），且目录内有 `SKILL.md`
- [ ] `provenance`（可选，仅 `kind=skill`）：`origin` ∈ human-authored | trainer-mined；`evidence_count` 为非负整数
- [ ] 每个 `artifacts[]` 含 `os`、`arch`、`url`、`sha256`（64 位十六进制）、`size`
- [ ] 二进制 sha256 按上传的原始文件计算
- [ ] 安装文档描述基于资产的流程，而不只是 shell
