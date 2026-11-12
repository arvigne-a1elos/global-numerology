# -*- coding: utf-8 -*-
# produtos/equipe.py - Compatibilidade de Equipes Empresariais (RH)
# Cruza chefes x membros e membros x membros pela fonte de verdade Cissay.
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

def analisar_equipe(texto):
    linhas = [m.strip() for m in str(texto).replace(";", "\n").splitlines() if m.strip()]
    pessoas = []
    for m in linhas:
        partes = [p.strip() for p in m.split(",")] if "," in m else [m]
        nome = partes[0]
        nasc = partes[1] if len(partes) > 1 else ""
        if nasc and "/" in nasc:
            dd, mm, aa = nasc.split("/")
            nasc = f"{aa}-{mm}-{dd}"
        en, sn = _energia_nome(nome)
        ev, sv = _caminho_vida(nasc)
        pessoas.append({"membro": nome, "nascimento": nasc, "soma": sn,
                        "energia": en, "caminho_vida": ev})

    # Limite de produto: principal + 2
    if len(pessoas) > MAX_MEMBROS + 1:
        pessoas = pessoas[:MAX_MEMBROS + 1]

    principal = pessoas[0] if pessoas else None
    pares = []

    if principal:
        for m in pessoas[1:]:
            cn = compatibilidade(principal["energia"], m["energia"])
            cv = None
            if principal["caminho_vida"] and m["caminho_vida"]:
                cv = compatibilidade(principal["caminho_vida"], m["caminho_vida"])

            if cn["grau"] is None:
                grau_final = cv["grau"] if cv else None
            elif cv is None or cv["grau"] is None:
                grau_final = cn["grau"]
            else:
                grau_final = (cn["grau"] + cv["grau"]) // 2

            pares.append({
                "membro1": principal["membro"], "membro2": m["membro"],
                "energia1": principal["energia"], "energia2": m["energia"],
                "caminho1": principal["caminho_vida"], "caminho2": m["caminho_vida"],
                "compatibilidade_nome": cn["grau"], "rotulo_nome": cn["rotulo"],
                "compatibilidade_vida": cv["grau"] if cv else None,
                "rotulo_vida": cv["rotulo"] if cv else None,
                "compatibilidade": grau_final,
                "dual": cn["dual"] or (cv["dual"] if cv else False),
                "alerta_dualidade": cn["alerta_dualidade"],
            })

    return {"principal": principal, "membros": pessoas,
            "total": len(pessoas), "pares": pares}
