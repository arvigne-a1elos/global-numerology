# -*- coding: utf-8 -*-
from nome_energia import CURADO, _dig, energia_nome, avaliar_nomes, sugerir_nome

for lang in CURADO:
    for tipo in CURADO[lang]:
        g = CURADO[lang][tipo]
        falta = [e for e in range(1, 10) if e not in g]
        erro = [(e, g[e]) for e in g if energia_nome(g[e])[0] != e]
        print(lang, tipo, "faltam:", falta, "| energia errada:", erro)

print("--- sugestao para cada energia (cao/pt) ---")
for e in range(1, 10):
    s = sugerir_nome("cao", e, "pt")
    print(e, "->", s)

print("--- caso Mel / Thor / Luna, alvo 5 ---")
r = avaliar_nomes(["Mel", "Thor", "Luna"], "cao", 5, "pt")
for x in r["entradas"]:
    print(x["nome"], "energia", x["energia"], "bate", x["bate"])
print("sugestao:", r["sugestao"], "de", r["sugestao_idioma"], "| total:", r["total_opcoes"])
