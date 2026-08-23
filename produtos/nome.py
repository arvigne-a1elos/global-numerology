# -*- coding: utf-8 -*-
# produtos/nome.py - Análise de energia de nomes (12 produtos)
from .mapa import reduzir, _LETRAS

def analisar_nome(nome, energia=None):
    limpo = nome.upper().replace(" ", "").replace("-", "").replace(".", "").replace(",", "")
    soma = sum(_LETRAS.get(c, 0) for c in limpo)
    en = reduzir(soma)
    res = {"nome": nome.strip().title(), "soma": soma, "energia": en}
    if energia:
        res["energia_desejada"] = int(energia)
        res["match"] = en == int(energia)
    return res
