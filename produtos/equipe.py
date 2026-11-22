# -*- coding: utf-8 -*-
# produtos/equipe.py — Compatibilidade de Equipes (RH)
# REGRA: chefe + 2 colaboradores. Cruzamento: chefe x cada colaborador.
import unicodedata
from .mapa import reduzir, _LETRAS, calc_mapa
from referencia.cissay import compatibilidade
from itertools import combinations
import re

_DATA = re.compile(r"^\d{1,4}[/-]\d{1,2}[/-]\d{1,4}$")


def _quebra(linha):
    """Aceita 'Nome', 'Nome;data', 'Nome;data;Apelido' e 'Nome;Apelido;data'."""
    sep = ";" if ";" in linha else ("," if "," in linha else None)
    partes = [p.strip() for p in linha.split(sep)] if sep else [linha.strip()]
    nome = partes[0] if partes else ""
    nasc, apelido = "", ""
    for p in partes[1:]:
        if p and not nasc and _DATA.match(p):
            nasc = p
        elif p and not apelido:
            apelido = p
    return nome, apelido, nasc

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
        nome, apelido, nasc = _quebra(linha)
        if nasc and "/" in nasc:
            dd, mm, aa = nasc.split("/")
            nasc = f"{aa}-{mm}-{dd}"
        en, sn = _energia_nome(nome)
        ea, sa = (_energia_nome(apelido) if apelido else (None, 0))
        ev, sv = _caminho_vida(nasc)
        pessoas.append({
            "membro": nome, "apelido": apelido, "nascimento": nasc, "soma": sn,
            "energia": en, "energia_apelido": ea, "soma_apelido": sa,
            "caminho_vida": ev,
            "energia_combinada": _energia_combinada(en, ev),
            "energia_combinada_apelido": (_energia_combinada(ea, ev) if apelido else None),
        })

    if len(pessoas) > MAX_MEMBROS + 1:
        pessoas = pessoas[:MAX_MEMBROS + 1]

    chefe = pessoas[0] if pessoas else None
    if chefe:
        chefe["papel"] = "chefe"

    def _par(x, y, papel_x, papel_y):
        c = compatibilidade(x["energia_combinada"], y["energia_combinada"])
        ca = None
        if x.get("energia_combinada_apelido") and y.get("energia_combinada_apelido"):
            ca = compatibilidade(x["energia_combinada_apelido"],
                                 y["energia_combinada_apelido"])
        return {
            "membro1": x["membro"], "papel1": papel_x,
            "membro2": y["membro"], "papel2": papel_y,
            "apelido1": x.get("apelido") or "",
            "apelido2": y.get("apelido") or "",
            "energia1": x["energia_combinada"],
            "energia2": y["energia_combinada"],
            "compatibilidade": c["grau"], "rotulo": c["rotulo"],
            "dual": c["dual"], "alerta_dualidade": c["alerta_dualidade"],
            "energia1_apelido": x.get("energia_combinada_apelido"),
            "energia2_apelido": y.get("energia_combinada_apelido"),
            "compatibilidade_apelido": ca["grau"] if ca else None,
            "rotulo_apelido": ca["rotulo"] if ca else "",
            "dual_apelido": ca["dual"] if ca else "",
            "alerta_dualidade_apelido": ca["alerta_dualidade"] if ca else "",
        }

    pares = []
    for m in pessoas[1:]:
        m["papel"] = "colaborador"
        if chefe:
            pares.append(_par(chefe, m, "chefe", "colaborador"))

    colaboradores = pessoas[1:] if len(pessoas) > 1 else []
    for a, b in combinations(colaboradores, 2):
        pares.append(_par(a, b, "colaborador", "colaborador"))

    return {"chefe": chefe, "membros": pessoas,
            "total": len(pessoas), "pares": pares}
