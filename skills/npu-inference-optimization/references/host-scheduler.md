# Host & Scheduler Layer

Biggest cheap wins on NPU stacks. Work this layer before kernels.

## Sync audit

- Audit every `event.synchronize` / D2H sync. Make syncs conditional (only
  on batch change) or deferred (overlap D2H copy with prep).
  Campaign wins: E10 conditional accepted-counts sync (6382.62);
  E37 deferred async-branch sync + device-side reorder (TPOT 30.24→29.93,
  TTFT −11%, losslessness confirmed via double-run noise baseline).
- Verify losslessness via the noise baseline, not by argument.

## Scheduler / config

- block_verify: joint cumsum validation is exactly equivalent to per-token
  checks — a free win, +2.3%, acceptance 2.08→2.44. Not a relaxation.
- stream-interval: batch streaming output; 8 measured sufficient, 16 gave
  no further gain.
- enable_cpu_binding: NUMA-local pinning, measured 5367 off vs 5590 on.

## Identify instrumentation artifacts before fixing

Not every anomaly is real:

- **Weak-memory stale timestamps** (aarch64): p90 ~100 ms dispatch glitches
  were an instrumentation artifact — fix the instrumentation and the
  account balances. Do not chase phantom scheduling bugs.
- **GC pauses**: measure before tuning. Campaign found no >5 ms GC pause;
  GC parameter tuning was a no-op.
- **Engine overhead**: decompose the loop; if host engine share is a few
  percent of step time, that lever does not exist. Measured: schedule
  1.1 ms + update 0.38 ms, rest is device wait.
