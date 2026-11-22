# Kernel & Graph Layer

Enter only after the host layer is exhausted and the matmul is confirmed at
its bandwidth floor.

## Confirm the floor first

Measure GB/s vs HBM peak before optimizing a matmul. Campaign: QuantMatmul
27 GB / 2.9 TB/s ≈ 90% of HBM peak — already at the floor, no headroom.
Early floor estimates can be wrong by 2×; measure.

## The one legal kernel-level win: draft-side quantization

Draft only proposes; target-logit verify decides. Quantizing the draft
lm_head (w8a16) does not change the output distribution. Campaign E35:
4 full-vocab logits per step, 3 downgraded to w8a16 → 7518.06 tok/s (+1.2%),
the only kernel-level win.

## Static kernels / graph features are fragile on quantized layouts

- `enable_static_kernel`: ScatterPaKvCache AI Core error 271 on mxfp8 QFA
  PA_NZ scatter layout (vllm-ascend #21412). No per-op blacklist exists —
  the whole feature must stay OFF until upstream adds validator exclusion.
- super+static kernel: same fragile area, AI Core 271 (#21286), CANN 9.2.1.
- `VLLM_USE_BREAKABLE_CUDAGRAPH`: crash registering state during capture
  (Ascend/pytorch #182). torch_npu forbids state registration in capture.

Expect AI Core errors on these paths, file upstream issues, keep features
gated OFF until fixed. Re-test only after the upstream snapshot check in
SKILL.md says the blocker is fixed.

## Fusion/overlap proposals must respect data dependencies

- GDN builder CPU partition: measured 6309 vs 6383 — the builder already
  runs on a stream overlapping verify forward; not a bound path.
- Draft triple-replay fusion: v0.30 already captures the entire draft
  propose as a single ACLGraph — no replay to merge.
- Skipping GDN intermediate-state writes: structurally required (draft
  reads the ssm slots verify writes per-token) — a floor, not a bug.
