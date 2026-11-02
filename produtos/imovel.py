# -*- coding: utf-8 -*-
# produtos/imovel.py - Número do Imóvel (3 campos: imóvel + apto/escritório + sala)
from .mapa import reduzir

LETRAS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def _valor_alfanumerico(texto):
    """Dígitos somam direto; letras viram número pitagórico (A=1...I=9, J=1...Z=8).
    Ex.: 'B' -> 2 · '7' -> 7 · 'C2' -> 3+2=5"""
    if not texto:
        return None
    t = str(texto).upper()
    soma = 0
    tem_algo = False
    for ch in t:
        if ch.isdigit():
            soma += int(ch)
            tem_algo = True
        else:
            idx = LETRAS.find(ch)
            if idx >= 0:
                soma += (idx % 9) + 1
                tem_algo = True
    if not tem_algo:
        return None
    while soma > 9 and soma not in (11, 22, 33):
        soma = sum(int(d) for d in str(soma))
    return soma

def analisar_imovel(dado, dado2="", dado3=""):
    """Recebe os 3 campos do modal. Qualquer combinação >= 1 campo gera o PDF.
    Ex.: imóvel 81, escritório 7, sala B -> 9 + 7 + 2 = 18 -> (9)"""
    partes = [_valor_alfanumerico(dado),
              _valor_alfanumerico(dado2),
              _valor_alfanumerico(dado3)]
    partes = [p for p in partes if p is not None]
    if not partes:
        return {"numero": str(dado), "energia": None, "ok": False}
    total = sum(partes)
    while total > 9 and total not in (11, 22, 33):
        total = sum(int(d) for d in str(total))
    return {
        "numero": " + ".join(str(x) for x in [dado, dado2, dado3] if str(x).strip()),
        "partes": partes,
        "soma": sum(partes),
        "energia": total,
        "ok": True,
    }
