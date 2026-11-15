# -*- coding: utf-8 -*-
# produtos/equipe.py — Compatibilidade de Equipes (RH)
# REGRA: chefe + 2 colaboradores. Cruzamento: chefe x cada colaborador.
import unicodedata
from .mapa import reduzir, _LETRAS, calc_mapa
from referencia.cissay import compatibilidade
from itertools import combinations

MAX_MEMBROS = 2


def _limpar(nome):
    n = unicodedata.normalize("NFD", (nome or "").upper())
    n = "".join(c for c in n if unicodedata.category(c) != "Mn")
    return "".join(c for c in n if "A" <= c <= "Z")


def _energia_nome(nome):
    limpo = _limpar(nome)
    s = sum(_LETRAS.get(c, 0) for c in limpo)
    return reduzir(s), s


def _caminho_vida(nasc):
    if not nasc:
        return None, 0
    try:
        d, m, a = nasc.split("-")
        s = sum(int(x) for x in d + m + a)
        return reduzir(s), s
    except Exception:
        return None, 0


def _energia_combinada(energia_nome, caminho_vida):
    if energia_nome is None or caminho_vida is None:
        return None
    return reduzir(energia_nome + caminho_vida)


def analisar_equipe(texto, separador="|"):
    bruto = str(texto or "")
    if "\n" in bruto:
        linhas = [l.strip() for l in bruto.splitlines() if l.strip()]
    elif separador in bruto:
        linhas = [l.strip() for l in bruto.split(separador) if l.strip()]
    else:
        linhas = [bruto.strip()] if bruto.strip() else []

    pessoas = []
    for linha in linhas:
        partes = [p.strip() for p in linha.split(";", 1)] if ";" in linha else [linha]
        nome = partes[0]
        nasc = partes[1] if len(partes) > 1 else ""
        if nasc and "/" in nasc:
            dd, mm, aa = nasc.split("/")
            nasc = f"{aa}-{mm}-{dd}"
        en, sn = _energia_nome(nome)
        ev, sv = _caminho_vida(nasc)
        pessoas.append({
            "membro": nome, "nascimento": nasc, "soma": sn,
            "energia": en, "caminho_vida": ev,
            "energia_combinada": _energia_combinada(en, ev),
        })

    if len(pessoas) > MAX_MEMBROS + 1:
        pessoas = pessoas[:MAX_MEMBROS + 1]

    chefe = pessoas[0] if pessoas else None
    if chefe:
        chefe["papel"] = "chefe"

    pares = []
    if chefe:
        for m in pessoas[1:]:
            m["papel"] = "colaborador"
            c = compatibilidade(chefe["energia_combinada"],
                                m["energia_combinada"])
            pares.append({
                "membro1": chefe["membro"], "papel1": "chefe",
                "membro2": m["membro"], "papel2": "colaborador",
                "energia1": chefe["energia_combinada"],
                "energia2": m["energia_combinada"],
                "compatibilidade": c["grau"], "rotulo": c["rotulo"],
                "dual": c["dual"], "alerta_dualidade": c["alerta_dualidade"],
            })

    # Pares entre colaboradores (o card promete "membros × membros")
    colaboradores = pessoas[1:] if len(pessoas) > 1 else []
    for a, b in combinations(colaboradores, 2):
        c = compatibilidade(a["energia_combinada"], b["energia_combinada"])
        pares.append({
            "membro1": a["membro"], "papel1": "colaborador",
            "membro2": b["membro"], "papel2": "colaborador",
            "energia1": a["energia_combinada"],
            "energia2": b["energia_combinada"],
            "compatibilidade": c["grau"], "rotulo": c["rotulo"],
            "dual": c["dual"], "alerta_dualidade": c["alerta_dualidade"],
        })
    
    return {"chefe": chefe, "membros": pessoas,
            "total": len(pessoas), "pares": pares}
