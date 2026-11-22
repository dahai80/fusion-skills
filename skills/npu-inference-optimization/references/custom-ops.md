# Custom Ops (AscendC) — E44 Playbook

Only after the floor analysis says a real lever exists. Read
`references/ops-faults.md` together with this file.

## The binary integrity rule (iron law)

Op binary hashes are unrelated to source names — same-name binaries exist
across versions. **Before interpreting ANY device output**: build-output
md5 == pushed-source md5 AND zero build errors. Stale binaries produce
convincing fake PASS results — the campaign's early conclusions were all
voided by this.

## Parity sweep before any serving decision

Full sweep across D/W/U dims and chip variants (campaign: D=64/128/256,
W≤2052, U≤8192, davinci1/3; tail block W=2052 solved by 32B rounding +
full-buffer zeroing). End-to-end container A/B with real serving shapes for
the final verdict — unit parity is not serving parity (aclnn arm measured
55 s vs 10.7 s per layer on real 4309-prompt shapes despite unit PASS).

## Real kernel bugs cost a probe/bisect round each

Campaign examples — expect this class:
- loop guard `SKIP && w0 < W` constant-false → all-zero output (root cause)
- ReduceSum f32 len≥128 fault → bypass via seg-64 segmentation
- GM scalar write racing MTE3 output on the same 64B row → clobbered row0

## Benchmark before committing; keep it behind a gate

Functionally correct can still lose: scalar vector gather measured 18×
worse than uniq+index_select+grouped bmm (20.2 ms vs 1.13 ms @sb=32).
A kernel that fails the performance gate does not ship — feature gate OFF,
results archived (campaign gate: `VLLM_QSA_ACLNN=OFF`, verdict final).

## Binding notes

`aclCreateTensor` lives in libopapi.so, not libascendcl.so. bf16→f32:
use `.float()` — bit-exact and ~5000× faster than manual view<<16 bit
expansion (97 ms → 0.02 ms per 16 MB).
