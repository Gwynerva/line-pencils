"""Check Kim's published classifications and their geometric consequences."""

import argparse
import json
from pathlib import Path
import sys
from urllib.request import urlopen

from pencils import candidates, f0, melchior_ok, theorem_ok, unkey

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "https://raw.githubusercontent.com/marik-11/linear_space_types/e126faeb3f621ef4c85e3872c320a27a901f229e/"
RESULTS = json.loads((ROOT / "data/kim_results.json").read_text(encoding="utf-8"))


def published_types(n, directory=None):
    name = f"state_{n}.json"
    if directory is None:
        with urlopen(SOURCE + name, timeout=30) as response:
            raw = json.load(response)
    else:
        raw = json.loads((directory / name).read_text(encoding="utf-8"))
    verdicts = {unkey(k): v for k, v in raw.items() if not k.startswith("sub:")}
    expected = {t for t in candidates(n) if len(t) < 2 or t[0] + t[1] <= n + 1}
    assert verdicts.keys() == expected and all(type(v) is bool for v in verdicts.values()), n
    types = {t for t, v in verdicts.items() if v}
    assert len(types) == RESULTS[str(n)]["b"], n
    return types


def extend_sequences(sequences):
    """Record the published terms alongside the local results."""
    for index, result in RESULTS.items():
        n = int(index)
        for letter, value in {"a": len(candidates(n)), **result}.items():
            if letter in sequences:
                entries = sequences[letter]
                entries.extend([None] * max(0, n - len(entries)))
                entries[n - 1] = value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kim-dir", type=Path, help="read the pinned tables from a local directory")
    args = parser.parse_args()
    sys.path.insert(0, str(ROOT / "verifier"))
    from verify import verify

    previous = set()
    for index, result in RESULTS.items():
        n = int(index)
        types = published_types(n, args.kim_dir)
        assert previous <= types, n
        previous = types
        cert_name = "n15_points.json" if n == 15 else f"n{n}.json"
        certs = json.loads((ROOT / "data/certificates" / cert_name).read_text(encoding="utf-8"))
        for cert in certs:
            verify(cert)
            assert tuple(cert["type"]) in types
        if n == 13:
            local = json.loads((ROOT / "data/results/classification_n13.json").read_text(encoding="utf-8"))
            assert all((tuple(r["type"]) in types) == (r["linear_space"] == "YES")
                       for r in local if r["linear_space"] in ("YES", "NO"))
            assert all(tuple(r["type"]) in types for r in local if r["verdict"] == "open")
        if n == 14:
            assert len({tuple(r["type"]) for r in certs}) == result["c"][0]
            assert sum(theorem_ok(n, t) for t in types) == result["c"][1]
            assert len({f0(n, r["type"]) for r in certs}) == result["d"][0]
        if n == 15:
            assert {f0(n, r["type"]) for r in certs} == {31, 33, 37}
        for value in result.get("excluded_f0", []):
            matching = [t for t in types if f0(n, t) == value]
            assert matching and not any(melchior_ok(n, t) for t in matching), (n, value)
            print(f"n={n}: all {len(matching)} types with {value} points fail Melchior")
        print(f"n={n}: checked {len(types)} published possible types")


if __name__ == "__main__":
    main()
