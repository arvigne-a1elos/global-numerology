# -*- coding: utf-8 -*-
# produtos/casal.py - Mapa do Casal (compatibilidade de 2 nomes + datas)
from .mapa import reduzir, _LETRAS
from referencia.cissay import obter_grau

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

def analisar_casal(nome1, nasc1, nome2, nasc2):
    e1n, s1n = _energia_nome(nome1)
    e2n, s2n = _energia_nome(nome2)
    e1v, s1v = _caminho_vida(nasc1)
    e2v, s2v = _caminho_vida(nasc2)
    # Cruzamento principal: energia do nome (fonte de verdade Cissay)
    comp_nome = obter_grau(e1n, e2n)
    # Cruzamento secundário: caminho de vida (se datas presentes)
    comp_vida = obter_grau(e1v, e2v) if e1v and e2v else None
    if comp_nome is None:
        comp_final = comp_vida
    elif comp_vida is None:
        comp_final = comp_nome
    else:
        comp_final = (comp_nome + comp_vida) // 2
    return {
        "nome1": nome1, "nasc1": nasc1, "energia_nome1": e1n, "caminho1": e1v,
        "nome2": nome2, "nasc2": nasc2, "energia_nome2": e2n, "caminho2": e2v,
        "soma1": s1n, "soma2": s2n,
        "compatibilidade_nome": comp_nome,
        "compatibilidade_vida": comp_vida,
        "compatibilidade": comp_final,
    }
