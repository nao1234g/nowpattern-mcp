# nowpattern-calibration-routing (MCP)

Query a counterparty's MEASURED judgment quality before delegating.

Third-party-resolved, OTS-sealed calibration records. Read-only. Money OFF.
Default-deny on unverified candidates. The operator's own losses are
published (notary honesty doctrine).

## Endpoints

- Descriptor: https://nowpattern.com/.well-known/calibration-routing.json
- Route (POST JSON): https://nowpattern.com/calibration-routing/route
- Discovery index: https://nowpattern.com/.well-known/mcp.json

## Zero-trust verification (3 lines, no account, offline)

    curl -O https://nowpattern.com/.well-known/rjp/genuine_only_v1.json
    curl -O https://nowpattern.com/.well-known/rjp/rjp_verify.py
    python rjp_verify.py genuine_only_v1.json

Recomputes the published Brier aggregate from the sealed records inside the
bundle. Honesty context included: genuine-only segment n=173, mean Brier
0.3096 vs 0.2117 base rate, 74.93% provenance contamination quarantined and
disclosed, Hosmer-Lemeshow / Murphy-decomposition audit attached.

## License

Data: CC BY 4.0 with attribution to nowpattern.com. Verifier: MIT.
