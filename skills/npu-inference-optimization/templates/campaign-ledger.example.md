# Campaign Ledger — Qwen3.8-27B @ Ascend 950DT 2026-11-07 → 11-13 (SMOKE-TEST EXAMPLE)

Baseline: 5390 tok/s | Image: v0.30.0-a5 (PINNED; v0.32.0rc-a5 rejected: acceptance 49→42) | CANN: 9.2.1
Topology: DP8 TP1, mns32, MTP k=3 | Acceptance: ~2.44 (post block_verify)
Target: 10000 tok/s | Floor: ~50 ms/step vs required ≤31 ms → unreachable, ceiling ~7.5k

| # | Hypothesis | Config diff | tok/s | TPOT | TTFT | Accept | Verdict | Root cause / reason |
|---|---|---|---|---|---|---|---|---|
| T1 | TP beats DP for BW-bound 27B | TP2×DP4 | 2442 | | | | ✗ | per-layer allreduce > halved weight traffic |
| T2 | MTP draft length knee | k=0/2/4/5 | 5294/4644/5318 | | | | ✗ | k=3 balances draft cost vs marginal acceptance |
| T3 | more concurrency helps | mns48/64 + capture256 | 4402/4225/4979 | | | | ✗ | capture miss → eager; capture growth flips prefill share |
| S1 | joint cumsum ≡ per-token | block_verify | +2.3% | | | 2.44 | ✓ | mathematically exact, free |
| S2 | batch streaming output | stream-interval 8 | 6485 | | | | ✓ | cuts per-token IPC; 16 no further gain |
| S3 | NUMA locality | cpu_binding on | 5590 (vs 5367) | | | | ✓ | cross-socket access reduced |
| S4 | overlap scheduling | async-scheduling flag | =baseline | | | | ✗ | MTP chain inherently serial (#21287) |
| H1 | skip steady-state sync | E10 conditional sync | 6382.62 | | | | ✓ | sync only on batch change |
| H2 | overlap D2H with prep | E37 deferred sync | 7517 median | 29.93 | −11% | | ✓ | noise-baseline confirmed lossless |
| H3 | p90 dispatch glitches real | E13 investigation | — | | | | ✗ | aarch64 weak-memory stale timestamps, artifact |
| H4 | engine loop fat | E34 decomposition | — | | | | ✗ | 1.7 ms ≈ 3%, no lever |
| H5 | GC tuning helps | GC 50000/100/100 | =baseline | | | | ✗ | no >5 ms GC pauses exist |
| K1 | draft lm_head w8a16 legal | E35 | 7518.06 | | | | ✓ | draft-side only, distribution preserved |
| K2 | matmul has headroom | floor re-measure | — | | | | ✗ | 27 GB @ 2.9 TB/s ≈ 90% HBM peak |
| K3 | static kernels help | E36 static kernel | crash | | | | ✗ | ScatterPaKvCache AI Core 271, mxfp8 PA_NZ (#21412) |
| R1 | loosen acceptance α | entropy_verify 0.4→10 | ≤6940 | | | | ✗ RED LINE | changes output distribution; α=10 = accept-all |
| O1 | custom op beats torch | E44 compact_read | 20.2 vs 1.13 ms | | | | ✗ | 18× slower; gate OFF, archived |
| U1 | upstream backport helps | PR #21388 on DP2 | 1560.5 vs 1611.1 | +1.6% | | = | ✗ | host layer already drained; −2.7%, two rounds |

## Verdict summary

- Adopted: 9 — DP8 TP1 (7429.88), MTP k=3, mns32, block_verify, stream8, cpu_binding, E10, E35, E37 → 7518.06 (+39.5%)
- Rejected: 30+ — grouped: topology dead-ends / no-op flags / instrumentation phantoms / upstream regressions
- Red-line rejections: entropy_verify (all α), target lm_head quantization — zero tolerance

## Losslessness confirmations

| Change | Method | Result |
|---|---|---|
| E37 | double-run noise baseline, diff rate ≤ own noise | lossless |
| E35 | draft-side-only argument (verify decides with target logits) | lossless by construction |

## Ceiling verdict

~50 ms floor > 31 ms required for 10k → unreachable losslessly on this
stack; ceiling ~7.5k achieved (7518.06). Remaining levers are CANN/upstream
(#21285 PA_NZ fix, #21412 op blacklist, GDN chunked parallelism).

## Deliverables checklist

- [x] Adopted-changes summary with numbers
- [x] Ceiling analysis (see ceiling-report.example.md)
- [x] 9 upstream issues filed (see references/upstream.md snapshot)
- [x] Process data cleaned; docs/e44_ascendc_project.md §8 archived
