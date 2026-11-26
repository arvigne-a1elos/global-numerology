import re

src = open("static/translations.js", encoding="utf-8").read()
bloco = src[src.index("const translations = {"):]
bloco = bloco[:bloco.index("\n};")]
partes = re.split(r"\n    ([a-z]{2}):\s*\{", bloco)

for i in range(1, len(partes), 2):
    lang, corpo = partes[i], partes[i + 1]
    chaves = re.findall(r"^\s{8}([A-Za-z_][\w]*)\s*:", corpo, re.M)
    dup = {c: chaves.count(c) for c in set(chaves) if chaves.count(c) > 1}
    if dup:
        print(lang, dup)
