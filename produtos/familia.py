# -*- coding: utf-8 -*-
# produtos/familia.py — Mapa Família Premium
import unicodedata
from .mapa import reduzir, _LETRAS, calc_mapa
from referencia.cissay import compatibilidade

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


def analisar_familia(texto, separador="|"):
    """Aceita nomes separados por | e datas separadas por |."""
    bruto = str(texto or "")
    # primeiro tenta quebra de linha, depois o separador recebido
    if "\n" in bruto:
        linhas = [l.strip() for l in bruto.splitlines() if l.strip()]
    elif separador in bruto:
        linhas = [l.strip() for l in bruto.split(separador) if l.strip()]
    else:
        linhas = [bruto.strip()] if bruto.strip() else []

    pessoas = []
    for linha in linhas:
        if ";" in linha:
            partes = [p.strip() for p in linha.split(";", 1)]
        elif "," in linha:
            partes = [p.strip() for p in linha.split(",", 1)]
        else:
            partes = [linha]
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

    principal = pessoas[0] if pessoas else None
    pares = []
    if principal:
        for m in pessoas[1:]:
            c = compatibilidade(principal["energia_combinada"],
                                m["energia_combinada"])
            pares.append({
                "membro1": principal["membro"], "membro2": m["membro"],
                "energia1": principal["energia_combinada"],
                "energia2": m["energia_combinada"],
                "compatibilidade": c["grau"], "rotulo": c["rotulo"],
                "dual": c["dual"], "alerta_dualidade": c["alerta_dualidade"],
            })

    return {"principal": principal, "membros": pessoas,
            "total": len(pessoas), "pares": pares}
