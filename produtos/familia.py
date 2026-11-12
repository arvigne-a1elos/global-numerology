# -*- coding: utf-8 -*-
# produtos/familia.py — Mapa Família Premium
# REGRA DE PRODUTO: contratante + 2 membros (3 pessoas).
# Cruzamento: principal x cada membro. NUNCA membro x membro.
# Energia de cada pessoa = reduzir(energia do nome + caminho de vida).
# Cruzamento único sobre essa energia combinada.
from .mapa import reduzir, _LETRAS
from referencia.cissay import compatibilidade

MAX_MEMBROS = 2   # além do principal


def _energia_nome(nome):
    s = sum(_LETRAS.get(c, 0) for c in nome.upper().replace(" ", ""))
    return reduzir(s), s


def _caminho_vida(nasc):
    try:
        d, m, a = nasc.split("-")
        s = sum(int(x) for x in d + m + a)
        return reduzir(s), s
    except Exception:
        return None, 0


def _energia_combinada(energia_nome, caminho_vida):
    """Energia da pessoa = reduzir(energia do nome + caminho de vida)."""
    if energia_nome is None or caminho_vida is None:
        return None
    return reduzir(energia_nome + caminho_vida)


def analisar_familia(texto):
    bruto = str(texto).replace("\\n", "\n")
    linhas = [l.strip() for l in bruto.splitlines() if l.strip()]
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
            "membro": nome,
            "nascimento": nasc,
            "soma": sn,
            "energia": en,
            "caminho_vida": ev,
            "energia_combinada": _energia_combinada(en, ev),
        })

    # Limite de produto: principal + 2
    if len(pessoas) > MAX_MEMBROS + 1:
        pessoas = pessoas[:MAX_MEMBROS + 1]

    principal = pessoas[0] if pessoas else None
    pares = []

    if principal:
        for m in pessoas[1:]:
            c = compatibilidade(principal["energia_combinada"],
                                m["energia_combinada"])
            pares.append({
                "membro1": principal["membro"],
                "membro2": m["membro"],
                "energia1": principal["energia_combinada"],
                "energia2": m["energia_combinada"],
                "compatibilidade": c["grau"],
                "rotulo": c["rotulo"],
                "dual": c["dual"],
                "alerta_dualidade": c["alerta_dualidade"],
                "especial": c["especial"],
            })

    return {
        "principal": principal,
        "membros": pessoas,
        "total": len(pessoas),
        "pares": pares,
    }
