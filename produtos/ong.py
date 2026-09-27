# -*- coding: utf-8 -*-
"""Análise de nome e sigla para entidades (ONG, OSCIP, Associação, Fundação,
Instituto, Confraria, Clube). Gera 3 análises do cliente + 2 sugestões da IA."""

import random

LETRAS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def _valor_letra(ch):
    idx = LETRAS.find(ch.upper())
    if idx < 0:
        return 0
    return (idx % 9) + 1

def _reduzir(n):
    while n > 9 and n not in (11, 22, 33):
        n = sum(int(d) for d in str(n))
    return n

def energia_texto(texto):
    if not texto:
        return None
    soma = sum(_valor_letra(ch) for ch in texto if ch.isalpha())
    return _reduzir(soma) if soma else None

def _melhor(nome, sigla, alvo):
    en = energia_texto(nome)
    es = energia_texto(sigla)
    if en is None and es is None:
        return "sem dados"
    if en is None:
        return "sigla"
    if es is None:
        return "nome"
    if abs(en - alvo) < abs(es - alvo):
        return "nome"
    if abs(es - alvo) < abs(en - alvo):
        return "sigla"
    return "empate"

def _grau(item, alvo):
    diffs = [abs(x - alvo) for x in (item.get("energia_nome"), item.get("energia_sigla"))
             if x is not None]
    return min(diffs) if diffs else 99

PALAVRAS = {
    "associacao": ["Associação", "Confraria", "Círculo", "Comunidade"],
    "fundacao": ["Fundação", "Instituto", "Casa"],
    "instituto": ["Instituto", "Centro", "Núcleo"],
    "confraria": ["Confraria", "Irmandade", "Sociedade"],
    "clube": ["Clube", "Círculo", "Liga"],
    "": ["Associação", "Instituto", "Fundação"],
}

def _sugerir_2(natureza, tipo, alvo):
    rng = random.Random(20260926)
    usadas = set()
    base = PALAVRAS.get((tipo or "").strip().lower(), PALAVRAS[""])
    sugestoes = []
    for i in range(2):
        sigla = None
        for _ in range(600):
            s = "".join(rng.choice(LETRAS) for _ in range(3))
            if s in usadas:
                continue
            if energia_texto(s) == alvo:
                sigla = s
                usadas.add(s)
                break
        if sigla is None:
            s = "".join(rng.choice(LETRAS) for _ in range(3))
            sigla = s
            usadas.add(s)
        palavra = base[i % len(base)]
        nome = f"{palavra} {sigla[0]}{sigla[1]} {sigla[2]}"
        sugestoes.append({
            "nome": nome,
            "sigla": sigla,
            "energia_nome": energia_texto(nome),
            "energia_sigla": energia_texto(sigla),
        })
    return sugestoes

def analisar_ong(dados):
    alvo = int(str(dados.get("energia") or "6"))
    natureza = dados.get("natureza", "ong")
    tipo = dados.get("tipo_entidade", "")
    escopo = dados.get("escopo", "nacional")

    nomes = []
    for k in ("1", "2", "3"):
        nome = (dados.get("nome" + k) or "").strip()
        sigla = (dados.get("sigla" + k) or "").strip()
        if not nome and not sigla:
            continue
        nomes.append({
            "nome": nome,
            "sigla": sigla,
            "energia_nome": energia_texto(nome),
            "energia_sigla": energia_texto(sigla),
            "melhor": _melhor(nome, sigla, alvo),
        })

    sugestoes = _sugerir_2(natureza, tipo, alvo)

    recomendacao = ""
    if nomes:
        melhor = min(nomes, key=lambda it: _grau(it, alvo))
        en = melhor.get("energia_nome")
        es = melhor.get("energia_sigla")
        if en is not None and es is not None:
            if abs(en - alvo) <= abs(es - alvo):
                recomendacao = (f"Melhor combinação: nome '{melhor['nome']}' "
                                f"com energia {en}, mais próxima da pesquisada {alvo}.")
            else:
                recomendacao = (f"Melhor combinação: sigla '{melhor['sigla']}' "
                                f"com energia {es}, mais próxima da pesquisada {alvo}.")
        elif en is not None:
            recomendacao = f"Nome '{melhor['nome']}' com energia {en}."
        else:
            recomendacao = f"Sigla '{melhor['sigla']}' com energia {es}."

    return {
        "natureza": natureza,
        "tipo": tipo,
        "escopo": escopo,
        "energia_alvo": alvo,
        "energia_ideal": 6,
        "nomes": nomes,
        "sugestoes": sugestoes,
        "recomendacao": recomendacao,
    }
