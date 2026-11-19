# -*- coding: utf-8 -*-
from nome_energia import SEME, energia_nome, avaliar_nomes

for tipo in SEME:
    g = {}
    for n in SEME[tipo]:
        g.setdefault(energia_nome(n)[0], []).append(n)
    falta = [e for e in range(1, 10) if e not in g]
    print(tipo, "energias:", sorted(g), "faltam:", falta)

print("---")
r = avaliar_nomes(["Mel", "Thor", "Luna"], "cao", 5)
for x in r["entradas"]:
    print(x["nome"], "energia", x["energia"], "bate", x["bate"])
print("sugestao:", r["sugestao"], "total:", r["total_opcoes"])
