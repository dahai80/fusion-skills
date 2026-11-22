---
name: npu-inference-optimization
description: Lossless inference throughput optimization for LLM serving on Ascend NPU (vLLM-Ascend, 950DT-class). Use when optimizing serving tok/s, TPOT, TTFT, or speculative decoding (MTP) on NPU hardware — NOT training. Proven playbook Qwen3.8-27B 950DT 5390→7518 tok/s (+39.5%).
---

# NPU Inference Throughput Optimization (Lossless)

Battle-tested playbook: Qwen3.8-27B on Ascend 950DT, 5390 → 7518.06 tok/s
(+39.5%) with zero output-distribution change, via MTP speculative decoding
on vLLM-Ascend. 40+ attempts, 9 adopted, negative results are part of the
deliverable.

## Non-negotiable red lines (read before anything else)

1. **Never touch the target/verify-side distribution.** No target lm_head
   quantization, no entropy/acceptance threshold loosening. Forbidden outright.
2. **Quantization is legal only on the draft side** of speculative decoding
   (draft logits only propose; target-logit verify decides — distribution
   preserving by construction).
3. **Every "lossless" claim passes a double-run noise baseline**: the delta
   must be ≤ the metric's own run-to-run noise. Single-run numbers are never
   accepted.

Details and arguments: read `references/lossless-redline.md` before judging
any change that could alter output distribution.

## Campaign flow

Start a campaign ledger first: copy `templates/campaign-ledger.md` and fill a
row per experiment (hypothesis, config diff, measured numbers, verdict, root
cause). Every experiment gets a verdict — ✓ adopted / ✗ rejected with a
number and one-line reason.

1. **Baseline** — tok/s, TPOT, TTFT, acceptance rate, concurrency, image +
   CANN/driver versions, pinned. Then decompose one decode step and compute
   the theoretical HBM floor. Read `references/baseline.md`.
2. **Parallel topology search** — DP × TP × MTP-k × max-num-seqs × capture
   size, one measured number per cell. Read `references/topology.md`.
3. **Host & scheduler layer** — sync audit, streaming interval, CPU binding,
   instrumentation-artifact identification. Cheapest levers first. Read
   `references/host-scheduler.md`.
4. **Kernel & graph layer** — only after confirming the layer above is
   exhausted. Read `references/kernel-graph.md`.
5. **Custom ops** (only if a real lever survived step 1's floor analysis) —
   read `references/custom-ops.md` AND `references/ops-faults.md` together.
6. **Upstream & closeout** — file issues, A/B backports, write the ceiling
   report from `templates/ceiling-report.md`. Read `references/upstream.md`.

## Profiling

Default trio, in this order: host-side py-spy 200Hz → torch_npu profiler
(trigger-style + offline analysis) → cProfile + source hooks. Known failure
modes and fallbacks: read `references/profiling.md` when instrumenting.

## Honest ceiling — when to stop

If the target tok/s requires a step time below the device HBM floor, declare
the ceiling and reallocate effort upstream. Do not grind a proven-unreachable
number. The campaign that produced this playbook measured ~50 ms/step floor vs
≤31 ms needed for 10k tok/s and stopped at ~7.5k — that was the correct call.

## Final deliverables

Adopted-changes summary with numbers, ceiling analysis, experiment ledger,
upstream issue list with status, archived docs. Process data is cleaned;
only final artifacts and logs persist.

## Known-upstream snapshot

Issue statuses recorded in `references/upstream.md` are a snapshot. Re-check
upstream state at campaign start — a fixed issue can flip a rejected feature
(e.g. static kernel) back to testable.
