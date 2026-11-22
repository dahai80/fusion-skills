# Parallel Topology Search (DP × TP × MTP × mns × capture)

One measured number per cell. Campaign verdicts (27B, 950DT — numbers are
priors, re-measure for your model):

## DP vs TP

- For bandwidth-bound models that fit on one card, DP scales linearly;
  TP2 per-layer allreduce costs more than the halved weight traffic.
  Measured: DP8 = 7429.88, TP2×DP4 = 2442 tok/s.
- 27B weights fit single-card → add cards, not TP.

## MTP draft length k

Sweep k = 0/2/3/4/5. Draft cost grows linearly with k, marginal acceptance
drops; pick the knee. Measured: k=3 won; k=0 5294 / k=2 4644 / k=4 5318 /
k=5 — all worse than k=3's 7429.

## max-num-seqs

Increase until HBM bandwidth saturates; beyond that it only adds TTFT.
Measured: 32 was the cap; 48/64 regressed hard (4402/4225).

## Capture-size coupling (the trap)

concurrency × (1+k) must fit the cudagraph capture size, or graphs fall
back to eager — catastrophic. Enlarging capture can flip prefill share and
net-lose: measured 4979 with capture 256 + mns64 (prefill share doubled).

## Feature flags on an MTP stack

Test each flag A/B — some are structural no-ops: async-scheduling cannot
overlap because draft proposals depend on the current step's output; the
chain is inherently serial (vllm-ascend #21287). batch-memcpy and
balance-scheduling were no-ops when the bottleneck is elsewhere. DyntraLB
hard-requires PD-separated deployment (kv_consumer) — unusable single-node.
