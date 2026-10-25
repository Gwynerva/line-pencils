"""One-off: convert the legacy certificate database (realized_legacy.json) to the documented
certificate format used by verifier/verify.py, one file per n: data/certificates/n{n}.json.

Legacy format: {"n": {"[k1, k2, ...]": {"d": d, "points": [[[a0,a1],[b0,b1],[c0,c1]], ...], "src": s}}}
where a "point" (a:b:c) in the dual plane is the line a x + b y + c z = 0.  So the numbers
carry over unchanged; only the names change ("points" -> "lines", "src" -> "source").
"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "verifier"))
from verify import verify, Reject

legacy = json.load(open(os.path.join(ROOT, "data", "certificates", "realized_legacy.json")))
out_dir = os.path.join(ROOT, "data", "certificates")
total = 0
for n_str, m in sorted(legacy.items(), key=lambda kv: int(kv[0])):
    n = int(n_str)
    certs = []
    for key, c in m.items():
        t = sorted(json.loads(key), reverse=True)
        cert = {"n": n, "type": t, "d": c["d"], "lines": c["points"], "source": "legacy search: " + c["src"]}
        verify(cert)                       # raises if the legacy certificate is bad
        certs.append(cert)
    certs.sort(key=lambda c: (len(c["type"]), c["type"]), reverse=True)
    fn = os.path.join(out_dir, "n%d.json" % n)
    # merge with an existing file (keep existing entries, add new types)
    existing = json.load(open(fn)) if os.path.exists(fn) else []
    have = {tuple(c["type"]) for c in existing}
    added = [c for c in certs if tuple(c["type"]) not in have]
    allc = existing + added
    allc.sort(key=lambda c: (-sum(c["type"]), c["type"]))
    with open(fn, "w") as f:
        json.dump(allc, f, separators=(",", ":"))
        f.write("\n")
    total += len(allc)
    print("n=%d: %d certificates (%d new)" % (n, len(allc), len(added)))
print("total", total)
