#!/usr/bin/env python3
"""构建历史语料索引。只读扫描，不改动任何原文。"""

import argparse
import csv
import hashlib
import re
from datetime import datetime
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", ".pytest_cache", "__pycache__", "10-RL-Tuning"}

TAG_RULES = [
    ("gen", [r"\bgen\b", r"\brollout\b", "生成段", "推理段", "decode", "prefill"]),
    ("ref", [r"\bref\b", "ref 段", "参考策略", "reference"]),
    ("update", [r"\bupdate\b", "训练段", "update_actor", "反向"]),
    ("reward", [r"\bRM\b", r"\breward\b", "奖励模型", "打分"]),
    ("memory", ["显存", r"\bHBM\b", "OOM", "reserved", "allocated", "KV cache"]),
    ("precision", ["精度", r"\bMXFP8\b", r"\bFP8\b", "收敛", "loss", "grad_norm"]),
    ("comm", [r"\bHCCL\b", "通信", "RoCE", "all-gather", "reduce-scatter", "fsdp_size"]),
    ("profile", [r"\bprofile\b", r"\bprofiling\b", "py-spy", "上板", "采集"]),
    ("failure", ["判死", "失败", "踩坑", "误判", "不可行", "出局"]),
    ("sweep", ["扫参", "单变量", "A/B", "实验矩阵", "敏感性"]),
    ("stack", ["版本", "容器", r"\bverl\b", "vllm-ascend", "CANN", "镜像"]),
    ("sema", ["语义", "bypass", "降频", "折 ref", "关 KL", "off-policy"]),
]

TYPE_RULES = [
    ("交付件", ["交付_", "交付"]),
    ("复盘", ["复盘", "六问", "六题", "盘点"]),
    ("实验清单", ["实验清单", "实验列表", "实验矩阵"]),
    ("任务书", ["任务书", "托管"]),
    ("收口简报", ["收口"]),
    ("证据与分析", ["报告", "分析", "判读", "拆解", "机理", "审计", "证据", "对照"]),
    ("参考资料", ["handbook", "guide", "best-practice", "最佳实践", "索引", "README"]),
    ("规划", ["计划", "规划", "蓝图", "草案", "路线"]),
]


DIR_RULES = [
    ("归档", ["/归档/"]),
    ("客户材料", ["客户技术交流"]),
    ("参考资料", ["/community/", "/docs/"]),
]


def classify(name, rel):
    for label, keys in DIR_RULES:
        if any(k in rel for k in keys):
            return label
    for label, keys in TYPE_RULES:
        if any(k in name for k in keys):
            return label
    return "其他"


def tags_of(text, name):
    blob = name + "\n" + text
    hits = []
    for tag, pats in TAG_RULES:
        count = 0
        for pat in pats:
            if pat.startswith(r"\b"):
                count += len(re.findall(pat, blob, flags=re.I))
            else:
                count += blob.count(pat)
        if count >= 3:
            hits.append((tag, count))
    hits.sort(key=lambda x: -x[1])
    return ",".join(t for t, _ in hits[:6])


def title_of(text, fallback):
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()[:120]
    return fallback


def date_of(name, mtime):
    m = re.search(r"20(\d{2})(\d{2})(\d{2})", name)
    if m:
        return f"20{m.group(1)}-{m.group(2)}-{m.group(3)}"
    return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="待索引的项目资料根目录")
    ap.add_argument("--out-dir", default=None)
    args = ap.parse_args()
    root = Path(args.root).resolve()
    out_dir = Path(args.out_dir).resolve() if args.out_dir else root / "10-RL-Tuning" / "data" / "index"
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    for path in root.rglob("*.md"):
        if out_dir in path.parents or any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        stat = path.stat()
        rel = str(path.relative_to(root))
        digest = hashlib.sha1(text.encode("utf-8", errors="ignore")).hexdigest()[:10]
        rows.append({
            "type": classify(path.name, rel),
            "date": date_of(path.name, stat.st_mtime),
            "title": title_of(text, path.stem),
            "path": rel,
            "size_kb": round(stat.st_size / 1024, 1),
            "h2": sum(1 for line in text.splitlines() if line.startswith("## ")),
            "tags": tags_of(text, path.name),
            "hash": digest,
        })

    best = {}
    for row in rows:
        current = best.get(row["hash"])
        key = (len(row["path"]), row["path"])
        if current is None or key < current[0]:
            best[row["hash"]] = (key, row["path"])
    for row in rows:
        canonical = best[row["hash"]][1]
        row["dup_of"] = "" if canonical == row["path"] else canonical

    rows.sort(key=lambda r: (r["type"], r["date"], r["path"]), reverse=False)
    tsv = out_dir / "corpus_index.tsv"
    fields = ["type", "date", "title", "path", "size_kb", "h2", "tags", "hash", "dup_of"]
    with tsv.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)

    lines = ["# 历史语料索引", "", f"扫描根目录：{root}", f"文件数：{len(rows)}（仅 .md）", ""]
    current = None
    for row in rows:
        if row["type"] != current:
            current = row["type"]
            lines.append("")
            lines.append(f"## {current}")
            lines.append("")
        dup = "" if not row["dup_of"] else " | 同文副本"
        lines.append(f"- {row['date']} | {row['title']} | {row['path']} | {row['size_kb']}KB | {row['tags']}{dup}")
    (out_dir / "corpus_index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    counts = {}
    for row in rows:
        counts[row["type"]] = counts.get(row["type"], 0) + 1
    print(f"indexed={len(rows)} -> {tsv}")
    for k, v in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
