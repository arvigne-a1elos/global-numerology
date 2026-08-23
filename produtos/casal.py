# -*- coding: utf-8 -*-
# produtos/casal.py - Mapa do Casal (compatibilidade de 2 nomes)
from .mapa import reduzir, _LETRAS

def analisar_casal(nome1, nome2):
    def energia(nome):
        s = sum(_LETRAS.get(c, 0) for c in nome.upper().replace(" ", ""))
        return reduzir(s), s
    e1, s1 = energia(nome1)
    e2, s2 = energia(nome2)
    return {"nome1": nome1, "nome2": nome2, "energia1": e1, "energia2": e2,
            "soma1": s1, "soma2": s2, "compatibilidade": reduzir(e1 + e2)}
