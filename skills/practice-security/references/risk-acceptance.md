# Risk acceptance (D3)

When a critical/major security issue is deferred or a control is consciously omitted, write `specs/<f>/gates/risk-<RISK-nn>.md` from the gate template:
- the risk and a concrete exploit scenario;
- likelihood and impact, and who/what is exposed;
- options: fix now / mitigate partially / accept;
- the recommendation (non-binding);
- for acceptance: compensating controls, monitoring, and an **expiry date** after which the risk must be re-decided.
