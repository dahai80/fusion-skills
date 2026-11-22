# Campaign Ledger — <model> @ <hardware> <date-range>

Baseline: <tok/s> | Image: <tag, PINNED> | CANN: <ver> | Driver: <ver>
Topology: <DP/TP, mns, MTP k> | Acceptance: <rate>
Target: <tok/s> | HBM floor analysis: <ms/step floor vs required> → verdict

| # | Hypothesis | Config diff | tok/s | TPOT | TTFT | Accept | Verdict | Root cause / reason |
|---|---|---|---|---|---|---|---|---|
| E1 | <one line> | <diff> | <num> | | | | ✓/✗ | <one line> |

## Verdict summary

- Adopted: <n> — <list with numbers>
- Rejected: <n> — grouped by failure class (no-op / regression / incompatible / red-line)
- Red-line rejections: <list — zero tolerance, with the argument>

## Losslessness confirmations

| Change | Method (double-run noise baseline unless noted) | Result |
|---|---|---|
| <change> | <spread measured, delta vs spread> | lossless / voided |

## Ceiling verdict

<If floor > requirement: state floor ms, required ms, declared ceiling, and
that remaining work moves upstream.>

## Deliverables checklist

- [ ] Adopted-changes summary with numbers
- [ ] Ceiling analysis (templates/ceiling-report.md)
- [ ] Upstream issues filed (English) with status
- [ ] Process data cleaned; final docs archived
