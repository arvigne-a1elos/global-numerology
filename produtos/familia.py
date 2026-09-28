# -*- coding: utf-8 -*-
# produtos/familia.py - Mapa Família Premium (membros com nome + data)
# Compatibilidade: fonte de verdade absoluta referencia/cissay.py (Monique Cissay, p. 159)
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

def analisar_familia(texto):
    # Formato por linha: "Nome; DD/MM/AAAA" ou "Nome; AAAA-MM-DD" (aceita "Nome, AAAA-MM-DD")
    membros = [m.strip() for m in str(texto).replace(";", "\n").splitlines() if m.strip()]
    resultados = []
    for m in membros:
        partes = [p.strip() for p in m.split(",")] if "," in m else [m]
        nome = partes[0]
        nasc = partes[1] if len(partes) > 1 else ""
        # converte DD/MM/AAAA -> AAAA-MM-DD se for o caso
        if nasc and "/" in nasc:
            dd, mm, aa = nasc.split("/")
            nasc = f"{aa}-{mm}-{dd}"
        en, sn = _energia_nome(nome)
        ev, sv = _caminho_vida(nasc)
        resultados.append({"membro": nome, "nascimento": nasc,
                           "soma": sn, "energia": en,
                           "caminho_vida": ev})

    # Cruzamento entre todos os pares (fonte de verdade Cissay)
    pares = []
    n = len(resultados)
    for i in range(n):
        for j in range(i + 1, n):
            a = resultados[i]["energia"]
            b = resultados[j]["energia"]
            comp = compatibilidade(a, b)
            pares.append({
                "membro1": resultados[i]["membro"],
                "membro2": resultados[j]["membro"],
                "energia1": a,
                "energia2": b,
                "compatibilidade": comp["grau"],
                "rotulo": comp["rotulo"],
                "especial": comp["especial"],
                "dual": comp["dual"],
                "alerta_dualidade": comp["alerta_dualidade"],
            })

    return {"membros": resultados, "total": n, "pares": pares}
