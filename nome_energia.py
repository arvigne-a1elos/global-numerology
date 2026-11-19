# -*- coding: utf-8 -*-
"""A1ELOS - energia de nomes e sugestao por energia alvo."""
import unicodedata

LETRA = {c: (i % 9) + 1 for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ")}
ESP = {"\u00c6": "AE", "\u0152": "OE", "\u00d8": "O", "\u0110": "D",
       "\u0141": "L", "\u00de": "TH", "\u00d0": "D", "\u0126": "H",
       "\u0166": "T", "\u014a": "N"}


def normalizar(t):
    s = str(t or "").upper()
    for k, v in ESP.items():
        s = s.replace(k, v)
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return "".join(c for c in s if "A" <= c <= "Z")


def reduzir(n):
    while n > 9 and n not in (11, 22):
        n = sum(int(d) for d in str(n))
    return n


def energia_nome(nome):
    limpo = normalizar(nome)
    if not limpo:
        return (0, 0)
    soma = sum(LETRA.get(c, 0) for c in limpo)
    return (reduzir(soma), soma)


SEME = {
    "cao": ["Thor", "Luna", "Bela", "Rex", "Kira", "Nina", "Max", "Zoe", "Alma", "Duna"],
    "gato": ["Mimi", "Loki", "Nala", "Simba", "Frida", "Tom", "Sombra", "Jade", "Nino"],
    "passaro": ["Kiwi", "Piu", "Azul", "Nino", "Pingo", "Zeca", "Juju", "Liro"],
    "reptil": ["Draco", "Naga", "Kaa", "Shen", "Rex", "Zara", "Viper", "Tuga"],
    "outro": ["Aurora", "Nova", "Atlas", "Lumi", "Sage", "Onix", "Vega", "Aria"],
}


def sugerir_nome(tipo, energia, usados=None):
    alvo = int(energia) if str(energia).isdigit() else 0
    if not alvo:
        return None
    usados = set(normalizar(u) for u in (usados or []))
    grupos = [SEME.get(tipo) or [], SEME["outro"]]
    for grupo in grupos:
        for n in grupo:
            if normalizar(n) in usados:
                continue
            if energia_nome(n)[0] == alvo:
                return n
    base = normalizar((SEME.get(tipo) or SEME["outro"])[0]) or "A1ELOS"
    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for a in letras:
        for cand in (base + a, a + base):
            if normalizar(cand) in usados:
                continue
            if energia_nome(cand)[0] == alvo:
                return cand.capitalize()
    for a in letras:
        for b in letras:
            cand = base + a + b
            if normalizar(cand) in usados:
                continue
            if energia_nome(cand)[0] == alvo:
                return cand.capitalize()
    return None


def avaliar_nomes(nomes, tipo, energia_alvo):
    alvo = int(energia_alvo) if str(energia_alvo).isdigit() else 0
    entradas = []
    for n in (nomes or []):
        n = (n or "").strip()
        if not n:
            continue
        e, soma = energia_nome(n)
        entradas.append({"nome": n, "energia": e, "soma": soma, "bate": e == alvo})
    escolhido = None
    for x in entradas:
        if x["bate"]:
            escolhido = x["nome"]
            break
    sugestao = None
    if not escolhido and alvo:
        sugestao = sugerir_nome(tipo, alvo, [x["nome"] for x in entradas])
    return {
        "energia_alvo": alvo,
        "tipo": tipo,
        "entradas": entradas,
        "escolhido": escolhido or sugestao or (entradas[0]["nome"] if entradas else None),
        "sugestao": sugestao,
        "total_opcoes": len(entradas) + (1 if sugestao else 0),
    }
