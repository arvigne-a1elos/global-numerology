# -*- coding: utf-8 -*-
import os, traceback
import gerador_pdf as G
from nome_energia import sugerir_nome, avaliar_nomes

# --- espia qual template cada produto realmente chama ---
chamadas = []
for _n in ("pdf_casal", "pdf_familia", "pdf_equipe", "pdf_produto", "pdf8", "pdf17"):
    _orig = getattr(G, _n, None)
    if _orig:
        def _wrap(*a, _nome=_n, _o=_orig, **k):
            chamadas.append(_nome)
            return _o(*a, **k)
        setattr(G, _n, _wrap)

print("=== 1. MATRIZ DE SUGESTAO (cao / pt) ===")
for e in range(1, 10):
    s = sugerir_nome("cao", e, "pt")
    print(e, "->", s["nome"] if s else None, "| idioma:", (s or {}).get("idioma", "-"))

print("\n=== 2. Mel / Thor / Luna, alvo 5 ===")
r = avaliar_nomes(["Mel", "Thor", "Luna"], "cao", 5, "pt")
for x in r["entradas"]:
    print(" ", x["nome"], "energia", x["energia"], "bate", x["bate"])
print("  escolhido:", r["escolhido"], "| sugestao:", r["sugestao"],
      "| total:", r["total_opcoes"])

print("\n=== 3. ORQUESTRADOR nome_pet ===")
try:
    p = gerar_pdf("nome_pet", {}, "pt", "", "",
                  dado="Mel", dado2="Thor", dado3="Luna", energia=5, tipo="cao")
    ok = bool(p) and os.path.exists(p)
    print("  PDF:", p, "| existe:", ok,
          "| bytes:", os.path.getsize(p) if ok else 0)
except Exception:
    traceback.print_exc()

print("\n=== 4. REGRESSAO dos produtos de relacao ===")
chamadas.clear()
for prod in ("casal", "familia", "compatibilidade_equipes"):
    antes = len(chamadas)
    try:
        gerar_pdf(prod, {}, "pt", "Teste", "01/01/1990")
    except Exception as e:
        pass
    usou = chamadas[antes:] or ["(nenhuma funcao registrada)"]
    print(" ", prod, "->", usou)
