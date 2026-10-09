# -*- coding: utf-8 -*-
"""
criar_precos_stripe.py — MODO SIMULAÇÃO (padrão)
Lê a planilha (24 produtos x 14 idiomas), reconstrói o nome real da capa
e monta a URL de cada um dos 336 produtos. Por padrão NÃO cria nada no Stripe.

USO:
  python criar_precos_stripe.py            -> simulação (padrão, seguro)
  python criar_precos_stripe.py --executar -> cria de verdade no Stripe
"""

import os, re, sys, unicodedata
import pandas as pd
import stripe

# ---------------------------------------------------------------
# 1. CONFIG
# ---------------------------------------------------------------
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
URL_CAPAS = "https://arvigne-a1elos.github.io/capas-a1elos/"
PLANILHA = "Tabela de Controle - Numerologia - 24 Produtos - 14 Idiomas - 001.xlsx"

# Sigla do idioma (coluna A do cabeçalho de cada bloco) -> prefixo do arquivo
SIGLAS_IDIOMA = {
    "alemao": "alemao", "de": "alemao",
    "arabe": "arabe", "ar": "arabe",
    "chines": "chines", "zh": "chines",
    "espanhol": "espanhol", "es": "espanhol",
    "frances": "frances", "fr": "frances",
    "hebraico": "hebraico", "he": "hebraico",
    "indonesio": "indonesio", "id": "indonesio",
    "ingles": "ingles", "en": "ingles",
    "italiano": "italiano", "it": "italiano",
    "japones": "japones", "ja": "japones",
    "portugues": "portugues", "pt": "portugues",
    "russo": "russo", "ru": "russo",
    "turco": "turco", "tr": "turco",
    "vietnamita": "vietnamita", "vi": "vietnamita",
}

# Moeda ISO por idioma (fallback; o script prefere a coluna G da planilha)
MOEDA_PADRAO = {
    "alemao": "eur", "arabe": "aed", "chines": "cny", "espanhol": "eur",
    "frances": "eur", "hebraico": "ils", "indonesio": "idr", "ingles": "usd",
    "italiano": "eur", "japones": "jpy", "portugues": "brl", "russo": "rub",
    "turco": "try", "vietnamita": "vnd",
}

ZERO_DECIMAL = {"jpy", "vnd", "idr", "krw", "clp", "pyg",
                "ugx", "isk", "xof", "xaf", "xpf", "bif",
                "djf", "gnf", "kmf", "rwf", "vuv"}

unit = int(round(float(preco))) if moeda in ZERO_DECIMAL else int(round(float(preco) * 100))

# ---------------------------------------------------------------
# 2. NORMALIZAÇÃO (bate 1:1 com os arquivos do GitHub)
# ---------------------------------------------------------------
def normalizar(texto):
    t = unicodedata.normalize("NFD", str(texto))
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    t = t.lower()
    t = re.sub(r"\s+", "_", t)          # espaços -> _
    t = re.sub(r"[^a-z0-9_]", "", t)    # remove símbolos
    return t

def montar_nome(prefixo, faixa, moeda, produto):
    return f"{prefixo}_-_{faixa}-{moeda}_-_{normalizar(produto)}.png"

# ---------------------------------------------------------------
# 3. LEITURA DA PLANILHA (detecta os blocos por idioma)
# ---------------------------------------------------------------
# Colunas (0-indexadas):
#   0=PT  1=Produto  2=Faixa  3=tradução  4=Cifra  5=Preço  6=ISO4217  7=Moeda  8=Nome da Capa
COL_PT, COL_PROD, COL_FAIXA, COL_PRECO, COL_ISO = 0, 1, 2, 5, 6

def carregar_blocos():
    df = pd.read_excel(PLANILHA, header=None)
    blocos = []          # (idioma, [linhas])
    idioma_atual = None
    linhas_atual = []

    for _, row in df.iterrows():
        a = row[COL_PT]
        # Cabeçalho de bloco: coluna A é texto (sigla do idioma), não número
        if isinstance(a, str) and not str(a).strip().isdigit():
            if idioma_atual and linhas_atual:
                blocos.append((idioma_atual, linhas_atual))
            idioma_atual = str(a).strip().lower()
            linhas_atual = []
        else:
            linhas_atual.append(row)

    if idioma_atual and linhas_atual:
        blocos.append((idioma_atual, linhas_atual))
    return blocos

# ---------------------------------------------------------------
# 4. LÓGICA PRINCIPAL
# ---------------------------------------------------------------
def main():
    executar = "--executar" in sys.argv
    if not executar:
        print("=" * 72)
        print("MODO SIMULAÇÃO — nada será criado no Stripe.")
        print("Para criar de verdade: python criar_precos_stripe.py --executar")
        print("=" * 72)

    if STRIPE_SECRET_KEY:
        stripe.api_key = STRIPE_SECRET_KEY

    blocos = carregar_blocos()
    total = 0
    erros = []

    for idioma, linhas in blocos:
        prefixo = SIGLAS_IDIOMA.get(idioma)
        if not prefixo:
            erros.append(f"[BLOCO] Idioma não reconhecido: {idioma!r}")
            continue

        for row in linhas:
            produto = str(row[COL_PROD]).strip()
            faixa   = str(row[COL_FAIXA]).strip().zfill(2)
            preco   = row[COL_PRECO]
            iso     = str(row[COL_ISO]).strip().lower() if pd.notna(row[COL_ISO]) else ""

            # Moeda: prefere a coluna G, corrige NIS -> ils, senão usa o padrão
            moeda = iso if iso else MOEDA_PADRAO.get(prefixo, "")
            moeda = moeda.replace("\u00a5", "y").replace("\uffe5", "y")  # JP\u00a5 -> jpy
            if moeda == "nis":
               moeda = "ils"

            nome = montar_nome(prefixo, faixa, moeda, produto)
            url  = URL_CAPAS + nome
            total += 1

            if executar:
                try:
                    prod = stripe.Product.create(
                        name=f"{produto} ({prefixo})",
                        images=[url],
                        metadata={"idioma": prefixo, "produto": produto, "faixa": faixa},
                    )
                    stripe.Price.create(
                        product=prod["id"],
                        unit_amount=int(round(float(preco) * 100)),
                        currency=moeda,
                    )
                    print(f"  OK  {produto:28s} | {moeda.upper()} {preco:>8} | {url}")
                except Exception as e:
                    erros.append(f"[{produto}/{prefixo}] Stripe: {e}")
            else:
                print(f"  [sim] {produto:28s} | {moeda.upper()} {preco:>8} | {url}")

    print("\n" + "=" * 72)
    print(f"Total de produtos processados: {total} (esperado: 336)")
    if erros:
        print(f"ERROS ({len(erros)}):")
        for e in erros:
            print("  -", e)
    else:
        print("Nenhum erro. Tudo consistente.")
    print("=" * 72)

if __name__ == "__main__":
    main()
