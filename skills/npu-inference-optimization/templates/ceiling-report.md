# Honest Ceiling Report — <model> @ <hardware>

## Question

Is <target tok/s> reachable losslessly on this stack?

## Decode-step decomposition (measured)

| Component | ms | Note |
|---|---|---|
| verify forward | | matmul / attention / quant-copy-lm_head sub-splits |
| draft graph | | |
| worker host | | |
| engine dispatch | | |
| **total** | | |

## Floor calculation

- Measured HBM bandwidth-limited floor: <X> ms/step (method: <how measured>)
- Required step time for target: <Y> ms (topology: <DP/TP>)
- Comparison: <floor vs required>

## Verdict

<Reachable / unreachable. If unreachable: declare ceiling ≈ <Z> tok/s,
state that it was achieved or what remains, and reallocate remaining effort
to upstream work — list the specific issues that would move the ceiling.>

## Downstream consequences

<What was stopped because of this verdict, and where the effort went.>
