# Profiling Toolchain — Trio + Failure Modes

Use in preference order; each has a known failure mode.

## 1. py-spy at 200 Hz, from the HOST

- Container ptrace is denied — attach to the same process from the host,
  not inside the container (container run measured `Samples: 1`).
- The sampling window must align with load bursts (e.g. 600p@32 + t+25s),
  or you profile dequeue idle.
- Campaign attribution: launch 25.4% / sync 10.4% / GDN 7%.

## 2. torch_npu profiler

- In-daemon export fails. Use trigger-style collection + offline analysis
  in a NON-daemon process; export kernel_details.csv / chrome trace to
  attribute per-kernel time (located QuantMatmul / GDN in campaign).

## 3. cProfile + source-level engine hooks

Fallback when both profilers fail. Caveat: instrumentation can mask async
overlap — note it in the ledger when it does.

## Dead ends on this image (do not burn time)

- **msprof**: daemon process unreadable; offline PROF-dir analyse yields
  only ACL-layer trace, TASK table missing, runtime-api off. Dead end —
  fall back to #3 (filed Ascend/msprof #1).
- **In-container py-spy**: ptrace denied.

## Rule

A profiler that silently returns nothing is a finding, not a failure of
your method — record it in the ledger, file upstream, move to the next
tool. Do not re-derive a dead end.
