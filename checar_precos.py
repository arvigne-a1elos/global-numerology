# -*- coding: utf-8 -*-
"""checar_precos.py — guarda da fonte unica de precos.

FONTE: referencia/precos.py  (unico arquivo que pode declarar preco)
Sai com codigo 1 em qualquer divergencia, para bloquear o deploy.
"""
import os, re, sys, json, urllib.request

RAIZ  = os.path.dirname(os.path.abspath(__file__))
FONTE = "referencia/precos.py"

# Arquivos que NAO podem declarar preco (ordem de varredura).
VIGIADOS = [
    "main.py", "static/produtos.js", "static/translations.js",
    "static/app.js", "scripts/criar_precos_stripe.py",
]
# Padroes de DECLARACAO (nao de leitura).
PADROES = [
    (r"^\s*(?:const|var|let)?\s*PRECO_DISPLAY\s*=",     "declara PRECO_DISPLAY"),
    (r"^\s*(?:const|var|let)?\s*PRECO_BASE\s*=",        "declara PRECO_BASE"),
    (r"^\s*(?:const|var|let)?\s*PRODUTO_FAIXA\s*=",     "declara PRODUTO_FAIXA"),
    (r"^\s*ZERO_DECIMAL\s*=",                           "declara ZERO_DECIMAL (use CASAS)"),
    (r"^\s*VALORES\s*=",                                "declara VALORES"),
    (r"window\.(?:PRECO_DISPLAY|PRECO_BASE|PRODUTO_FAIXA)\s*=", "publica preco no browser"),
]

problemas = []

# ---- 1. Duplicatas de declaracao -------------------------------------------
for rel in VIGIADOS:
    cam = os.path.join(RAIZ, rel)
    if not os.path.exists(cam):
        continue
    for n, linha in enumerate(open(cam, encoding="utf-8"), 1):
        for pat, desc in PADROES:
            if re.search(pat, linha):
                problemas.append(
                    "  %s:%d  %s\n     %s" % (rel, n, desc, linha.strip()[:88]))

# ---- 2. A API publicada concorda com a fonte? ------------------------------
def _api():
    url = "https://global-numerology.onrender.com/api/precos"
    return json.load(urllib.request.urlopen(url, timeout=8))

try:
    sys.path.insert(0, RAIZ)
    from referencia.precos import CASAS, VALORES, PRECO_DISPLAY
    d = _api()
    if sorted(d.keys()) != ["casas", "display", "faixa", "simbolo", "valores"]:
        problemas.append("  /api/precos: chaves inesperadas -> %s" % sorted(d.keys()))
    for lang in ("pt", "ja", "id"):
        if d.get("casas", {}).get(lang) != CASAS.get(lang):
            problemas.append(
                "  /api/precos casas[%s]=%s  x  precos.py=%s"
                % (lang, d.get("casas", {}).get(lang), CASAS.get(lang)))
        if d.get("display", {}).get(lang) != PRECO_DISPLAY.get(lang):
            problemas.append(
                "  /api/precos display[%s] divergente da fonte\n     api:  %s\n     fonte:%s"
                % (lang, d.get("display", {}).get(lang), PRECO_DISPLAY.get(lang)))
except Exception as e:
    problemas.append("  nao foi possivel comparar com a API: %s" % e)

# ---- 3. Relatorio ----------------------------------------------------------
print("FONTE DE PRECOS: %s" % FONTE)
if not problemas:
    print("OK — nenhuma duplicata, API alinhada.")
    sys.exit(0)

print("\nALERTA — %d divergencia(s):\n" % len(problemas))
for p in problemas:
    print(p)
print("\nCORRIJA APENAS EM: referencia/precos.py")
print("Nenhum outro arquivo pode declarar preco. Torne a rodar antes do deploy.")
sys.exit(1)
