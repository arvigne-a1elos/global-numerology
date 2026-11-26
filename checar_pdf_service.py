import re

src = open("pdf_service.py", encoding="utf-8").read()
linhas = src.splitlines()
alvos = list(re.finditer(r"\b(SIG|CAM|DES|VIB)\.get\(", src))

print(f"{len(alvos)} ocorrência(s)\n")
for m in alvos:
    n = src[:m.start()].count("\n")
    print(f"{n + 1:>5}  {linhas[n].strip()[:74]}")
