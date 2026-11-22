# Honest Ceiling Report — Qwen3.8-27B @ Ascend 950DT (SMOKE-TEST EXAMPLE)

## Question

Is 10000 tok/s reachable losslessly on this stack (DP8, MTP k=3, mns32)?

## Decode-step decomposition (measured)

| Component | ms | Note |
|---|---|---|
| verify forward | 25.2 | matmul 9.5 (at floor) + GDN ~6 (structural) + quant/copy/lm_head ~9 |
| draft graph | 7.5 | single ACLGraph capture |
| worker host | 10 | E10/E37 already applied |
| engine dispatch | 5 | schedule 1.1 + update 0.38 confirmed drained |
| **total** | **~50** | |

## Floor calculation

- Measured HBM floor: ~50 ms/step (QuantMatmul 27 GB @ 2.9 TB/s ≈ 90% peak;
  early 54 GB estimate was wrong by 2× — corrected by measurement)
- Required for 10k tok/s at DP8: ≤31 ms/step
- 31 ms < 50 ms floor → unreachable losslessly

## Verdict

Unreachable. Ceiling ≈ 7500 tok/s; achieved 7518.06. Effort reallocated
upstream: #21285 (mxfp8 PA_NZ layout fix), #21412 (op blacklist /
validator exclusion), GDN chunked-parallel redesign — each worth a few
percentage points when landed.

## Downstream consequences

10k target closed; E44 (AscendC custom ops) closed as the last technical
lever; torch compact_read kept as production path; lossless stack frozen
at DP8 k3 mns32 + block_verify + stream8 + cpu_binding + E10/E35/E37.
