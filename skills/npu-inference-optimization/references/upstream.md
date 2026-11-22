# Upstream & Community Discipline

## Filing issues

File GitHub issues (English only) for every upstream bug found: crash
signatures, no-op flags, layout-corruption root causes, feature requests
(op blacklists, validator exclusions). Follow up with A/B data and
mechanism analysis — it accelerates fixes.

Campaign snapshot (2026-11-13 — RE-CHECK STATUS at campaign start; a fixed
issue can flip a rejected feature back to testable):

| Issue | Topic | Snapshot status |
|---|---|---|
| vllm-ascend #21285 | mxfp8 index-read corruption (PA_NZ layout) | root cause confirmed, awaiting fix |
| vllm-ascend #21286 | super kernel AI Core 271, CANN 9.2.1 + mxfp8 | filed |
| vllm-ascend #21287 | async-scheduling no-op on MTP stack | filed + conclusion updated |
| vllm-ascend #21366 | GDN RecurrentGatedDeltaRule kernel analysis | filed |
| vllm-ascend #21412 | static kernel 271 + op blacklist request | filed |
| vllm-ascend #21528 | top-k layout read feature request | filed |
| vllm-ascend #21529 | v0.32 MTP acceptance 49→41.6 regression | filed |
| Ascend/pytorch #182 | state registration during graph capture ERR00007 | filed |
| Ascend/pytorch #183 | view(uint8) value-conversion semantics | filed |
| Ascend/msprof #1 | container --pid attach broken | filed |

## Backport A/B discipline

Before backporting an upstream PR, A/B it on YOUR topology. A fix that
helps elsewhere can regress a host-exhausted stack: campaign PR #21388
(GDN host cumsum staging) measured −2.7% on DP2 (1560.5 vs 1611.1, noise
0.5%, two rounds) — the host layer was already drained (E13–E34). Publish
data and mechanism either way.

## Etiquette

- All GitHub artifacts English-only.
- Observe the PR timeline, not just comments (conflicts may be resolved by
  force-push).
- Data promises must be kept — refill the bench numbers as soon as a
  window opens; credibility is leverage.
- Related community tracks (e.g. LSA qsa-weights) get the same
  flat-repro-then-integrate treatment.
