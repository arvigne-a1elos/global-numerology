# -*- coding: utf-8 -*-
from nome_energia import CURADO, energia_nome, avaliar_nomes, sugerir_nome, precisa_romanizar

falhas = 0
for lang in sorted(CURADO):
    for tipo in CURADO[lang]:
        g = CURADO[lang][tipo]
        falta = [e for e in range(1, 10) if e not in g]
        errado = [e for e in g if energia_nome(g[e]["nome"])[0] != e]
        reais = sum(1 for e in g if g[e]["real"])
        if falta or errado:
            falhas += 1
            print("FALHA", lang, tipo, "faltam:", falta, "erradas:", errado)
        else:
            print("ok", lang, tipo, "9/9", "| reais:", reais, "| variantes:", 9 - reais)

print("---")
for lang in ("pt", "ja", "ru", "ar"):
    for e in range(1, 10):
        s = sugerir_nome("cao", e, lang)
        print(lang, "cao", e, "->", s["nome"], "| idioma:", s["idioma"], "| real:", s["real"])

print("--- Mel / Thor / Luna, alvo 5, cao/pt ---")
r = avaliar_nomes(["Mel", "Thor", "Luna"], "cao", 5, "pt")
for x in r["entradas"]:
    print(x["nome"], "energia", x["energia"], "bate", x["bate"])
print("sugestao:", r["sugestao"], "de", r["sugestao_idioma"], "real:", r["sugestao_real"], "total:", r["total_opcoes"])

print("--- romanizacao ---")
for t in ("Mel", "\u30e1\u30eb", "\u0418\u0432\u0430\u043d", "\u05e9\u05dc\u05d5\u05dd"):
    print(repr(t), "precisa:", precisa_romanizar(t))

print("TOTAL DE FALHAS:", falhas)

from nome_energia import avaliar_nomes
r = avaliar_nomes(["Mel", "Frida", "Memel"], "cao", 5, "pt")
print("sexo:", r["sexo"], "| sugestao:", r["sugestao"])
r2 = avaliar_nomes(["Thor", "Rex"], "cao", 5, "pt")
print("sexo:", r2["sexo"], "| sugestao:", r2["sugestao"])
