# Database of realised signatures with exact certificates.
import json, os
from pool import Pool
DBFILE = "realized.json"
def load():
    if not os.path.exists(DBFILE): return {}
    d = json.load(open(DBFILE))
    return {int(n): {tuple(json.loads(k)): v for k, v in m.items()} for n, m in d.items()}
def save(db):
    tmp = DBFILE + ".tmp%d" % os.getpid()
    json.dump({str(n): {json.dumps(list(k)): v for k, v in m.items()} for n, m in sorted(db.items())}, open(tmp, "w"))
    os.replace(tmp, DBFILE)
def put(db, n, sig, d, pts, src):
    m = db.setdefault(n, {})
    if sig in m: return False
    m[sig] = {"d": d, "points": [[list(c) for c in p] for p in pts], "src": src}
    return True
