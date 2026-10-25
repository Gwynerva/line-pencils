# For a candidate multiset: enumerate all linear spaces with these pencils and test orientability.
import sys, json, time
from comb import enumerate_all
from orient import orientable
def classify(n, sizes, max_orientable=5):
    cnt = [0]; ori = []
    def cb(blocks):
        cnt[0] += 1
        ok,_ = orientable(n, blocks)
        if ok:
            ori.append(blocks)
            return len(ori) >= max_orientable
        return False
    enumerate_all(n, sizes, cb)
    return cnt[0], ori
if __name__ == "__main__":
    n = int(sys.argv[1]); sizes = json.loads(sys.argv[2])
    t0=time.time()
    c, o = classify(n, sizes)
    print(n, sizes, "packings:", c, "orientable found:", len(o), f"{time.time()-t0:.1f}s")
    for b in o[:2]: print("  ", b)
