# -*- coding: utf-8 -*-
# produtos/imovel.py - Número do Imóvel (análise de vibração do número)
from .mapa import reduzir

def analisar_imovel(numero):
    n = "".join(ch for ch in str(numero) if ch.isdigit())
    if not n:
        return {"numero": str(numero), "energia": None, "ok": False}
    soma = sum(int(d) for d in n)
    return {"numero": n, "soma": soma, "energia": reduzir(soma), "ok": True}
