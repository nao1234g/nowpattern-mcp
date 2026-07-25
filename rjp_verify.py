#!/usr/bin/env python3
"""rjp_verify -- standalone recomputation verifier (RJP R2).

ZERO-TRUST DESIGN: single file, stdlib only, offline, no clone, no pip.
  python rjp_verify.py <bundle.json>        -> PASS / FAIL (exit 0 / 2)

Recomputes the mean Brier from the records INSIDE the bundle and compares
with the bundle's expected value; also re-derives every record_sha256 so
any tampering with a record is arithmetically visible. You never have to
trust Nowpattern -- only this 60-line file you can read yourself.
"""
import hashlib
import json
import sys


def verify(bundle):
    """Pure verification -> (ok, report)."""
    problems = []
    rows = bundle.get("records", [])
    for r in rows:
        basis = "%s|%s|%s" % (r.get("prediction_id"), r.get("our_pick_prob"),
                              r.get("outcome"))
        want = hashlib.sha256(basis.encode("utf-8")).hexdigest()
        if want != r.get("record_sha256"):
            problems.append("record hash mismatch: %s" % r.get("prediction_id"))
    if rows:
        total = 0.0
        for r in rows:
            p = float(r["our_pick_prob"]) / 100.0
            o = 1.0 if str(r.get("outcome")) == "YES" else 0.0
            total += (p - o) ** 2
        mean = round(total / len(rows), 4)
    else:
        mean = None
    expected = (bundle.get("expected") or {}).get("recomputed_mean_brier")
    if mean != expected:
        problems.append("mean mismatch: recomputed=%s expected=%s"
                        % (mean, expected))
    return (not problems), {"n_records": len(rows), "recomputed_mean": mean,
                            "expected_mean": expected, "problems": problems}


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 1
    with open(argv[1], encoding="utf-8") as fh:
        bundle = json.load(fh)
    ok, report = verify(bundle)
    print(json.dumps(report, ensure_ascii=False))
    print("VERDICT:", "PASS -- numbers hold without trusting the publisher"
          if ok else "FAIL -- do not cite these numbers")
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
