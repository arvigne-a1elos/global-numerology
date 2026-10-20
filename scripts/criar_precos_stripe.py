# -*- coding: utf-8 -*-
"""
criar_precos_stripe.py — A1ELOS Global Numerology
Cria os 336 preços (24 produtos × 14 idiomas) da planilha de controle no Stripe.

MODOS DE USO
  python criar_precos_stripe.py                       -> SIMULAÇÃO (nada é criado), ambiente ao vivo
  python criar_precos_stripe.py --executar            -> CRIA no modo AO VIVO (pede confirmação digitada)
  python criar_precos_stripe.py --teste               -> SIMULAÇÃO no ambiente DE TESTE
  python criar_precos_stripe.py --teste --executar    -> CRIA no modo DE TESTE (sem gastar nada)

EXTRAS
  --arquivo "caminho.xlsx"   usa outra planilha
  --apenas pt,en             simula/cria só os idiomas listados

CHAVES (nunca cole chave no chat nem dentro do código)
  AO VIVO -> variável de ambiente STRIPE_SECRET_KEY
  TESTE   -> variável de ambiente STRIPE_SECRET_KEY_TEST
             (se não existir, o script pede que você digite, sem eco na tela)

SAÍDA (somente com --executar)
  price_ids_live.py  / price_ids_teste.py    -> constantes PRONTAS para colar no main.py
  price_ids_live.json / price_ids_teste.json -> backup completo dos IDs
"""
import argparse
import getpass
import json
import os
import re
import sys
import time
import unicodedata
from datetime import datetime

try:
    import pandas as pd
except ImportError:
    sys.exit("Falta a biblioteca pandas. Rode: pip install pandas openpyxl")

try:
    import stripe
except ImportError:
    sys.exit("Falta a biblioteca stripe. Rode: pip install stripe")

PLANILHA_PADRAO = "Tabela de Controle - Numerologia - 24 Produtos - 14 Idiomas - 001.xlsx"

IDIOMAS = ["pt", "en", "es", "it", "fr", "de", "ja", "zh", "ru", "he", "ar", "id", "tr", "vi"]

NOMES_IDIOMA = {
    "pt": "pt", "portugues": "pt",
    "en": "en", "ingles": "en", "english": "en",
    "es": "es", "espanhol": "es", "spanish": "es",
    "it": "it", "italiano": "it",
    "fr": "fr", "frances": "fr",
    "de": "de", "alemao": "de",
    "ja": "ja", "japones": "ja",
    "zh": "zh", "chines": "zh",
    "ru": "ru", "russo": "ru",
    "he": "he", "hebraico": "he",
    "ar": "ar", "arabe": "ar",
    "id": "id", "indonesio": "id",
    "tr": "tr", "turco": "tr",
    "vi": "vi", "vietnamita": "vi",
}

PRODUTOS_CONHECIDOS = {
    "express", "vida", "completo", "ia", "urna", "eleitoral", "imovel", "calendario",
    "artistico", "bebe", "assinatura", "negocio", "casal", "familia", "coletivo",
    "compatibilidade_equipes", "nome_pet", "nickname", "nome_dominio", "nome_canal",
    "nome_equipe", "nome_ong", "nome_projeto", "nome_evento",
}

# Moedas sem casas decimais no Stripe (unit_amount recebe o valor inteiro)
ZERO_DECIMAL = {"jpy", "vnd", "idr", "krw", "clp", "isk", "ugx", "bif", "djf",
                "gnf", "kmf", "mga", "pyg", "rwf", "vuv", "xaf", "xof", "xpf"}

# Correções de código de moeda da planilha -> código Stripe
FIX_MOEDA = {"NIS": "ils", "RMB": "cny"}

FAIXA_PRECO_BRL = {0: 8, 1: 17, 2: 26, 3: 35, 4: 44, 5: 98}


# ===== UTILITÁRIOS =====

def _sem_acento(txt):
    return "".join(c for c in unicodedata.normalize("NFD", txt)
                   if unicodedata.category(c) != "Mn")


def norm_idioma(v):
    s = _sem_acento(str(v or "").strip().lower())
    return NOMES_IDIOMA.get(s)


def norm_produto(v):
    s = _sem_acento(str(v or "").strip().lower())
    s = re.sub(r"[\s\-]+", "_", s)
    s = re.sub(r"[^a-z0-9_]", "", s)
    return s


def norm_moeda(v):
    s = str(v or "").strip().upper()
    s = FIX_MOEDA.get(s, s)
    return s.lower()


def parse_preco(v):
    if v is None:
        return None
    s = str(v).strip()
    if not s:
        return None
    try:
        return float(s.replace(",", "."))
    except ValueError:
        return None


def slug(txt):
    s = _sem_acento(txt).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:80]


# ===== PLANILHA =====

def carregar_linhas(caminho):
    df = pd.read_excel(caminho, header=None)

    # Localiza a linha de cabeçalho (procura a célula "produto")
    idx_hdr = -1
    for i in range(min(6, len(df))):
        cels = [str(x).strip().lower() for x in df.iloc[i].tolist()]
        if "produto" in cels:
            idx_hdr = i
            break

    col = {"lang": 0, "produto": 1, "faixa": 2, "preco": 5, "iso": 6, "capa": 8}
    if idx_hdr >= 0:
        cels = [str(x).strip().lower() for x in df.iloc[idx_hdr].tolist()]
        mapa = {"lang": ["pt", "idioma", "lang"],
                "produto": ["produto"],
                "faixa": ["faixa"],
                "preco": ["preço", "preco"],
                "iso": ["iso 4217", "iso4217", "iso"],
                "capa": ["nome da capa", "capa"]}
        for chave, candidatos in mapa.items():
            for j, c in enumerate(cels):
                if c in candidatos:
                    col[chave] = j
                    break

    linhas = []
    for i in range(idx_hdr + 1, len(df)):
        r = [("" if pd.isna(x) else str(x).strip()) for x in df.iloc[i].tolist()]
        if not any(r):
            continue
        lang = norm_idioma(r[col["lang"]]) if col["lang"] < len(r) else None
        if not lang:
            continue  # linha de separação ou rodapé
        prod = norm_produto(r[col["produto"]]) if col["produto"] < len(r) else ""
        if not prod:
            continue
        preco = parse_preco(r[col["preco"]]) if col["preco"] < len(r) else None
        iso = norm_moeda(r[col["iso"]]) if col["iso"] < len(r) else ""
        capa = r[col["capa"]] if col["capa"] < len(r) else ""
        if not capa and len(r) > 3:
            capa = r[3]
        try:
            faixa = int(float(str(r[col["faixa"]]).replace(",", "."))) if col["faixa"] < len(r) else None
        except ValueError:
            faixa = None
        if prod not in PRODUTOS_CONHECIDOS:
            print(f"Aviso: linha {i+1}, produto '{prod}' fora da lista dos 24 (seguirá mesmo assim).")
        linhas.append({"lang": lang, "produto": prod, "faixa": faixa, "preco": preco,
                       "iso": iso, "capa": capa, "linha": i + 1})
    return linhas


def validar_faixas(linhas):
    for l in linhas:
        if (l["lang"] == "pt" and l["iso"] == "brl"
                and l["faixa"] is not None and l["preco"] is not None):
            esperado = FAIXA_PRECO_BRL.get(l["faixa"])
            if esperado and abs(l["preco"] - esperado) > 0.01:
                print(f"Aviso: linha {l['linha']}, faixa {l['faixa']} deveria ser R$ {esperado}, "
                      f"planilha diz R$ {l['preco']}.")


# ===== CHAVES E AMBIENTE =====

def resolver_chave(modo):
    if modo == "teste":
        chave = os.environ.get("STRIPE_SECRET_KEY_TEST", "").strip()
        if not chave:
            chave = getpass.getpass("Cole a chave SECRETA de TESTE (sk_test_...): ").strip()
        if not chave.startswith(("sk_test_", "rk_test_")):
            sys.exit("Chave de TESTE inválida: deve começar com sk_test_ (ou rk_test_). Nada foi criado.")
    else:
        chave = os.environ.get("STRIPE_SECRET_KEY", "").strip()
        if not chave:
            chave = getpass.getpass("Cole a chave SECRETA AO VIVO (sk_live_...): ").strip()
        if not chave.startswith(("sk_live_", "rk_live_")):
            sys.exit("Chave AO VIVO inválida. Nada foi criado.")
    return chave


def conferir_ambiente(modo):
    try:
        acct = stripe.Account.retrieve()
    except Exception as e:
        print(f"Aviso: não consegui confirmar o ambiente da chave ({e}). Seguindo mesmo assim.")
        return
    if acct.livemode and modo == "teste":
        sys.exit("ERRO: você passou --teste mas a chave é AO VIVO. Nada foi criado.")
    if (not acct.livemode) and modo == "live":
        sys.exit("ERRO: execução AO VIVO pedida, mas a chave é de TESTE. Nada foi criado.")


# ===== SIMULAÇÃO =====

def simular(linhas):
    print("=" * 70)
    print("SIMULAÇÃO — nenhuma alteração será feita no Stripe")
    print("=" * 70)
    com_preco, sem_preco = 0, 0
    for l in linhas:
        if l["preco"] is None or l["preco"] <= 0:
            sem_preco += 1
            print(f"L{l['linha']:>3} {l['lang']} {l['produto']:<24} (sob consulta, sem preço no Stripe)")
            continue
        com_preco += 1
        moeda = l["iso"] or "???"
        print(f"L{l['linha']:>3} {l['lang']} {l['produto']:<24} {moeda:>4} {l['preco']:>10.2f}  {l['capa']}")
    print("-" * 70)
    print(f"Linhas com preço: {com_preco} | Sob consulta (puladas): {sem_preco}")


# ===== EXECUÇÃO =====

def carregar_existentes():
    prods = {}
    for p in stripe.Product.list(active=True, limit=100).auto_paging_iter():
        prods[p.name] = p.id
    precos = {}
    for pr in stripe.Price.list(active=True, limit=100).auto_paging_iter():
        if pr.unit_amount is not None:
            precos[(pr.product, pr.currency, pr.unit_amount)] = pr.id
    return prods, precos


def executar(linhas, modo):
    exist_prod, exist_price = carregar_existentes()
    resultado, erros = {}, []
    criados_p = reap_p = criados_v = reap_v = puladas = 0

    for l in linhas:
        if l["preco"] is None or l["preco"] <= 0:
            puladas += 1
            continue
        if not l["iso"]:
            erros.append((l, "sem código de moeda ISO na planilha"))
            continue
        nome_capa = l["capa"] or f"{l['produto']} ({l['lang']})"
        valor = int(l["preco"]) if l["iso"] in ZERO_DECIMAL else int(round(l["preco"] * 100))
        try:
            pid = exist_prod.get(nome_capa)
            if not pid:
                pid = stripe.Product.create(
                    name=nome_capa,
                    idempotency_key=f"prod-{modo}-{slug(nome_capa)}",
                ).id
                exist_prod[nome_capa] = pid
                criados_p += 1
            else:
                reap_p += 1
            vid = exist_price.get((pid, l["iso"], valor))
            if not vid:
                vid = stripe.Price.create(
                    product=pid, currency=l["iso"], unit_amount=valor,
                    idempotency_key=f"price-{modo}-{slug(nome_capa)}-{l['iso']}-{valor}",
                ).id
                exist_price[(pid, l["iso"], valor)] = vid
                criados_v += 1
            else:
                reap_v += 1
            resultado[f"{l['lang']}|{l['produto']}"] = vid
        except Exception as e:
            erros.append((l, str(e)))
        time.sleep(0.05)

    return resultado, (criados_p, reap_p, criados_v, reap_v, puladas, erros)


def escrever_saidas(resultado, modo):
    sufixo = "teste" if modo == "teste" else "live"
    py_path, json_path = f"price_ids_{sufixo}.py", f"price_ids_{sufixo}.json"
    agrupado = {}
    for chave, vid in sorted(resultado.items()):
        lang, prod = chave.split("|")
        agrupado.setdefault(lang, {})[prod] = vid

    ambiente = "DE TESTE" if modo == "teste" else "AO VIVO"
    with open(py_path, "w", encoding="utf-8") as f:
        f.write(f"# Gerado automaticamente em {datetime.now():%d/%m/%Y %H:%M} | MODO {ambiente}\n")
        f.write("# Cole as constantes abaixo no main.py do ambiente correspondente.\n\n")
        for lang, prods in agrupado.items():
            for prod, vid in prods.items():
                f.write(f'PRICE_ID_{lang.upper()}_{prod.upper()} = "{vid}"\n')
            f.write("\n")
        f.write("PRICES = {\n")
        for lang, prods in agrupado.items():
            f.write(f'    "{lang}": {{\n')
            for prod, vid in prods.items():
                f.write(f'        "{prod}": "{vid}",\n')
            f.write("    },\n")
        f.write("}\n")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(agrupado, f, ensure_ascii=False, indent=2)
    return py_path, json_path


# ===== MAIN =====

def main():
    ap = argparse.ArgumentParser(description="Cria os preços A1ELOS no Stripe (ao vivo ou teste)")
    ap.add_argument("--executar", action="store_true", help="cria de verdade (sem isso, só simula)")
    ap.add_argument("--teste", action="store_true", help="usa a chave de TESTE (sk_test_...)")
    ap.add_argument("--arquivo", default=PLANILHA_PADRAO, help="caminho da planilha")
    ap.add_argument("--apenas", default="", help="idiomas separados por vírgula, ex.: pt,en")
    args = ap.parse_args()

    modo = "teste" if args.teste else "live"
    print("=" * 70)
    print("SIMULAÇÃO — nada será criado." if not args.executar else "MODO EXECUÇÃO — recursos serão criados!")
    print("AMBIENTE: DE TESTE (sk_test_)" if modo == "teste" else "AMBIENTE: AO VIVO (sk_live_)")
    print("=" * 70)

    if args.executar and modo == "live":
        confirma = input('Digite "CRIAR LIVE" para confirmar a criação ao vivo: ').strip()
        if confirma != "CRIAR LIVE":
            sys.exit("Confirmação não recebida, nada foi criado.")

    stripe.api_key = resolver_chave(modo)
    if args.executar:
        conferir_ambiente(modo)

    linhas = carregar_linhas(args.arquivo)
    if args.apenas:
        filtro = {x.strip() for x in args.apenas.split(",") if x.strip()}
        linhas = [l for l in linhas if l["lang"] in filtro]
    if not linhas:
        sys.exit("Nenhuma linha válida encontrada na planilha.")

    validar_faixas(linhas)

    if not args.executar:
        simular(linhas)
        return

    resultado, (cp, rp, cv, rv, pul, erros) = executar(linhas, modo)
    py_path, json_path = escrever_saidas(resultado, modo)

    print("=" * 70)
    print(f"CONCLUÍDO — MODO {'DE TESTE' if modo == 'teste' else 'AO VIVO'}")
    print(f"  Produtos: criados {cp} | reaproveitados {rp}")
    print(f"  Preços:   criados {cv} | reaproveitados {rv}")
    print(f"  Puladas (sob consulta): {pul} | Erros: {len(erros)}")
    for l, e in erros:
        print(f"    ERRO linha {l['linha']} ({l['lang']} {l['produto']}): {e}")
    print(f"Arquivos gerados: {py_path} | {json_path}")
    if modo == "teste":
        print("Lembrete: esses IDs só existem no modo TESTE. Não cole no main.py de produção.")
    print("=" * 70)


if __name__ == "__main__":
    main()
