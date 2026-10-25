import csv, sys
from math import comb
from final_tables import classify
nmax = int(sys.argv[1])
T = classify(nmax)
REASON = {"real": "", "comb": "комбинаторно невозможно (перебор)", "melchior": "неравенство Мельхиора",
          "cs": "теорема Чимы–Сойера", "orient": "ни одно разложение не ориентируемо (перебор)", "open": "не решено"}
FIELD = {0: "рациональные", 2: "с √2", 3: "с √3", 5: "с √5"}
with open("таблица_наборов.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["n", "набор (с двойками)", "пучки из 3+ прямых", "двоек", "можно нарисовать", "почему нельзя", "координаты примера"])
    for n in range(2, nmax + 1):
        for s, r, d in T[n]:
            t2 = comb(n, 2) - sum(comb(k, 2) for k in s)
            full = "{" + ", ".join(map(str, list(s) + [2] * t2)) + "}"
            rich = "{" + ", ".join(map(str, s)) + "}" if s else "—"
            w.writerow([n, full, rich, t2, "да" if r == "real" else ("?" if r == "open" else "нет"), REASON[r], FIELD.get(d, "") if r == "real" else ""])
print("ok")
