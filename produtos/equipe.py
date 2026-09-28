# -*- coding: utf-8 -*-
# produtos/equipe.py - Compatibilidade de Equipes Empresariais (RH)
# Cruza chefes x membros e membros x membros pela fonte de verdade Cissay.
from .mapa import reduzir, _LETRAS
from referencia.cissay import compatibilidade

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

def analisar_equipe(texto):
    # Formato por linha: "Nome; DD/MM/AAAA; CHEFE"  ou "Nome; DD/MM/AAAA" (membro)
    linhas = [m.strip() for m in str(texto).replace(";", "\n").splitlines() if m.strip()]
    membros = []
    for m in linhas:
        partes = [p.strip() for p in m.split(",")] if "," in m else [m]
        nome = partes[0]
        nasc = partes[1] if len(partes) > 1 else ""
        papel = partes[2] if len(partes) > 2 else "membro"
        if nasc and "/" in nasc:
            dd, mm, aa = nasc.split("/")
            nasc = f"{aa}-{mm}-{dd}"
        en, sn = _energia_nome(nome)
        ev, sv = _caminho_vida(nasc)
        membros.append({"membro": nome, "nascimento": nasc, "papel": papel,
                        "soma": sn, "energia": en, "caminho_vida": ev})
    # Cruzamento entre todos os pares (fonte de verdade Cissay)
    pares = []
    n = len(membros)
    for i in range(n):
        for j in range(i + 1, n):
            comp = compatibilidade(membros[i]["energia"], membros[j]["energia"])
            pares.append({
                "membro1": membros[i]["membro"], "papel1": membros[i]["papel"],
                "membro2": membros[j]["membro"], "papel2": membros[j]["papel"],
                "compatibilidade": comp["grau"], "rotulo": comp["rotulo"],
                "dual": comp["dual"], "alerta_dualidade": comp["alerta_dualidade"],
                "especial": comp["especial"],
            })
    return {"membros": membros, "total": n, "pares": pares}
