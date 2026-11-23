# -*- coding: utf-8 -*-
"""checar_precos.py — guarda da fonte unica de precos.

FONTE: referencia/precos.py  (unico arquivo que pode declarar preco)
Sai com codigo 1 em qualquer divergencia, para bloquear o deploy.
Rodar antes de cada commit:  python checar_precos.py
"""
import os, re, sys, json, urllib.request

RAIZ = os.path.dirname(os.path.abspath(__file__))
API  = "https://global-numerology.onrender.com/api/precos"

# Arquivos que NAO podem declarar preco.
VIGIADOS = [
    "main.py",
    "static/app.js",
    "static/produtos.js",
    "static/translations.js",
    "static/index.html",
    "scripts/criar_precos_stripe.py",
]

# Padroes de DECLARACAO (nao de leitura).
PADROES = [
    (r"^\s*(?:const\s+|let\s+|var\s+)?(?:window\.)?PRECO_DISPLAY\s*=", "declara PRECO_DISPLAY"),
    (r"^\s*(?:const\s+|let\s+|var\s+)?(?:window\.)?PRECO_BASE\s*=",    "declara PRECO_BASE"),
    (r"^\s*(?:const\s+|let\s+|var\s+)?(?:window\.)?PRODUTO_FAIXA\s*=", "declara PRODUTO_FAIXA"),
    (r"^\s*ZERO_DECIMAL\s*=",                                          "declara ZERO_DECIMAL (use CASAS)"),
    (r"^\s*VALORES\s*=",                                               "declara VALORES"),
    (r"^\s*PRICE_IDS\s*=",                                             "declara PRICE_IDS", "main.py"),
]

# Linhas que apenas RECEBEM o dado da API sao legitimas.
RECEBE_API = re.compile(r"(d\.(?:valores|display|faixa|casas|simbolo)|window\.PRECO_VALORES)")

# Arquivos mortos que nao podem existir na raiz.
PROIBIDOS = [
    "main_backup_precos.py",
    "main_backup_precos_LOCAL.py",
    "price_ids_teste.py",
    "apresentacao_textos.py",
    "scripts/atualizar_main_prices_LOCAL.py",
    "scripts/gerar_prices_LOCAL.py",
]

problemas = []

# ---- 1. Declaracoes de preco fora da fonte --------------------------------
for rel in VIGIADOS:
    cam = os.path.join(RAIZ, rel)
    if not os.path.exists(cam):
        continue
    for n, linha in enumerate(open(cam, encoding="utf-8", errors="replace"), 1):
        for pat, desc in PADROES:
            if re.search(pat, linha):
                if RECEBE_API.search(linha):
                    continue  # recebe da API: legitimo
                problemas.append(
                    "  %s:%d  %s\n     %s" % (rel, n, desc, linha.strip()[:88]))
                break

# ---- 2. Arquivos mortos na raiz -------------------------------------------
for rel in PROIBIDOS:
    if os.path.exists(os.path.join(RAIZ, rel)):
        problemas.append("  %s  existe (mover para _historico/ ou apagar)" % rel)

# ---- 3. A API publicada concorda com a fonte local? -----------------------
try:
    sys.path.insert(0, RAIZ)
    from referencia.precos import CASAS, VALORES, PRECO_DISPLAY
    d = json.load(urllib.request.urlopen(API, timeout=8))

    chaves = sorted(d.keys())
    if chaves != ["casas", "display", "faixa", "simbolo", "valores"]:
        problemas.append("  /api/precos: chaves inesperadas -> %s" % chaves)

    for lang in ("pt", "en", "ja", "vi", "id"):
        if d.get("casas", {}).get(lang) != CASAS.get(lang):
            problemas.append(
                "  casas[%s]: api=%s  fonte=%s"
                % (lang, d.get("casas", {}).get(lang), CASAS.get(lang)))
        if d.get("display", {}).get(lang) != PRECO_DISPLAY.get(lang):
            problemas.append(
                "  display[%s] divergente\n     api:   %s\n     fonte: %s"
                % (lang, d.get("display", {}).get(lang), PRECO_DISPLAY.get(lang)))
except Exception as e:
    problemas.append("  nao foi possivel comparar com a API: %s" % e)

# ---- 4. Relatorio ---------------------------------------------------------
print("FONTE DE PRECOS: referencia/precos.py")
print("API CONSULTADA : %s\n" % API)

if not problemas:
    print("OK - nenhuma duplicata, API alinhada com a fonte.")
    sys.exit(0)

print("ALERTA - %d divergencia(s):\n" % len(problemas))
for p in problemas:
    print(p)
print("\n" + "-" * 60)
print("CORRIJA APENAS EM: referencia/precos.py")
print("Nenhum outro arquivo pode declarar preco.")
print("Depois torne a rodar. Nao commite com pendencia.")
sys.exit(1)
