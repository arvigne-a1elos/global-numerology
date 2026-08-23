# -*- coding: utf-8 -*-
# produtos/calendario.py - Calendário Mensal Energético (vibração do mês)
from .mapa import reduzir

def analisar_calendario(nome, mes):
    try:
        ano, mm = str(mes).split("-")
        num = sum(int(c) for c in ano + mm)
    except Exception:
        num = 1
    return {"nome": nome, "mes": mes, "energia_mes": reduzir(num)}
