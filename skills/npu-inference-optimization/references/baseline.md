# Baseline & Floor Analysis

## Record before changing anything

At fixed load (e.g. 2400–6000 prompt tokens @ target concurrency, timed
window offset to skip warmup/dequeue):

- tok/s, TPOT, TTFT, MTP acceptance rate, max-num-seqs, DP/TP topology
- image tag, CANN version, driver version — **pin the known-good image**
- A new image can silently regress acceptance (measured 49→42 on
  v0.32.0rc-a5 vs v0.30.0-a5 for Qwen3.8 MTP). Version-pin and re-baseline
  on any image/driver change. Never compare numbers across images.

## Decompose one decode step

Before optimizing anything, split one ~step into layers. Campaign reference
point (~50 ms/step at 27B/950DT):

- verify forward ≈ 25.2 ms (QuantMatmul 9.5 — already at floor + GDN ~6
  structural + quant/copy/lm_head ~9)
- draft graph ≈ 7.5 ms
- worker host ≈ 10 ms
- engine dispatch ≈ 5 ms

This decomposition decides where headroom exists. If a layer is a few
percent of step time, declare it exhausted and move on (engine loop measured
1.7 ms ≈ 3% — no lever there).

## Compute the theoretical floor

Device HBM bandwidth vs required step time for target tok/s. Example:
10k tok/s at DP8 needs ≤31 ms/step, but the measured floor is ~50 ms —
the target is unreachable on this stack, losslessly.

Floor estimates themselves can be wrong: an early 54 GB matmul-floor
estimate was corrected to 27 GB (2.9 TB/s ≈ 90% HBM peak) by measurement.
Confirm the floor with a real bandwidth measurement before declaring it.

## Structural floors are not bugs

Some traffic is required by construction and cannot be optimized away
without a redesign: MTP draft reads the ssm cache slots written per-token
by verify (~6 ms/step GDN state traffic). Verify a "waste" is not a
structural dependency before proposing to skip it.
