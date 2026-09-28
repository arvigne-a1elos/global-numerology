# -*- coding: utf-8 -*-
# produtos/casal.py - Mapa do Casal (compatibilidade de 2 nomes + datas)
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

def analisar_casal(nome1, nasc1, nome2, nasc2):
    e1n, s1n = _energia_nome(nome1)
    e2n, s2n = _energia_nome(nome2)
    e1v, s1v = _caminho_vida(nasc1)
    e2v, s2v = _caminho_vida(nasc2)
    cn = compatibilidade(e1n, e2n)
    cv = compatibilidade(e1v, e2v) if e1v and e2v else None
    if cn["grau"] is None:
        comp_final = cv["grau"] if cv else None
    elif cv is None or cv["grau"] is None:
        comp_final = cn["grau"]
    else:
        comp_final = (cn["grau"] + cv["grau"]) // 2
    return {
        "nome1": nome1, "nasc1": nasc1, "energia_nome1": e1n, "caminho1": e1v,
        "nome2": nome2, "nasc2": nasc2, "energia_nome2": e2n, "caminho2": e2v,
        "soma1": s1n, "soma2": s2n,
        "compatibilidade_nome": cn["grau"], "rotulo_nome": cn["rotulo"],
        "dual_nome": cn["dual"], "alerta_dualidade_nome": cn["alerta_dualidade"],
        "compatibilidade_vida": cv["grau"] if cv else None,
        "rotulo_vida": cv["rotulo"] if cv else None,
        "dual_vida": cv["dual"] if cv else False,
        "alerta_dualidade_vida": cv["alerta_dualidade"] if cv else None,
        "compatibilidade": comp_final,
    }
