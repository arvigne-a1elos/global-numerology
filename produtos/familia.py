# -*- coding: utf-8 -*-
# produtos/familia.py - Mapa Família Premium (vários membros)
from .mapa import reduzir, _LETRAS

def analisar_familia(texto):
    membros = [m.strip() for m in str(texto).replace(";", "\n").splitlines() if m.strip()]
    resultados = []
    for m in membros:
        s = sum(_LETRAS.get(c, 0) for c in m.upper().replace(" ", ""))
        resultados.append({"membro": m, "soma": s, "energia": reduzir(s)})
    return {"membros": resultados, "total": len(resultados)}
