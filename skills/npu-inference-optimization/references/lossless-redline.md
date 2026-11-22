# Lossless Red Line — Distribution Arguments

The red line: zero output-distribution change. Every optimization is judged
against this before performance is even discussed.

## What is legal

**Draft-side quantization** (speculative decoding only). The verify stage
decides every token with target logits; the draft distribution only affects
proposal quality. Quantizing draft lm_head to w8a16 changes which tokens get
proposed, never which tokens get accepted — mathematically distribution
preserving. Campaign E35 adopted on this argument, +1.2%.

**Mathematically-equivalent reformulations**. block_verify (joint cumsum
validation) replaces per-token independent checks with a computation that
accepts exactly the same token sets — equivalence, not relaxation.

## What is forbidden outright

- **Target/verify-side lm_head quantization** — rewrites the final logits
  distribution directly. Output fidelity gone. Never.
- **entropy_verify / acceptance-threshold loosening** (α tuning) — changes
  what gets accepted, i.e. the output distribution. Campaign measured α=0.4→10
  variants up to 6940 tok/s and rejected every one; α=10 degenerates to
  accept-all. No accuracy sacrifice, not one.

## How to prove a claim lossless

Double-run noise baseline: run baseline twice, measure the metric's own
run-to-run spread; the optimized arm must sit within that spread on
distribution-sensitive metrics (output diff rate / acceptance rate). A
single A/B pair proves nothing. Campaign E37 was confirmed this way.

## Lossless is necessary, not sufficient

A custom kernel can be mathematically lossless and still be rejected for
being 18× slower (E44 compact_read: 20.2 ms vs 1.13 ms). Performance gate
applies on top of the red line.
