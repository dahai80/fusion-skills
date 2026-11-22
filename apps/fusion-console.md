# fusion-console

**Kind**: app (host/consumer) · **Source repo**: `dahai80/fusion-console`

An advanced LLM (brain) manages base LLMs (work) to automate work tasks, with configurable models and working style.

本地控制台：高级 LLM（brain）一键管理基础 LLM（work）自动化完成工作任务、可以配置模型与工作方式。

## Install

Latest release: **v0.2.23**. `registry.json` carries pinned `artifacts`
(url + sha256 + size per platform, schema v2 reference implementation) — hosts
download, verify the checksum, then unpack/install. Manual path: grab your
platform archive from the
[releases page](https://github.com/dahai80/fusion-console/releases) and check
the sha256 against the registry entry.

Host apps are consumers of the plugin/connector/skill catalog, not entries of
it — they read `registry.json` and install entries on their own.
