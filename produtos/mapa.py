# -*- coding: utf-8 -*-
# produtos/mapa.py - Núcleo numerológico compartilhado
# FONTE ÚNICA: referencia/cissay.py
import dateutil.parser as dp
from referencia.cissay import (
    LETRAS_BASE, reduzir, energia_nome,
    energia_data, numero_pessoa, normalizar_nome,
)

# Alias de compatibilidade com o resto do projeto
_LETRAS = LETRAS_BASE


def calc_mapa(nome, data_str):
    bd = dp.parse(data_str).date()

    # Caminho de vida: soma dia + mês + ano (sem reduzir cada parte antes)
    lp = reduzir(bd.day + bd.month + bd.year)

    # Acento NÃO zera: normaliza antes de somar
    nu = normalizar_nome(nome)

    te = tv = tp = 0
    for ch in nu:
        val = _LETRAS.get(ch, 0)
        te += val
        if ch in "AEIOU":
            tv += val
        else:
            tp += val

    exp = reduzir(te)

    return {
        "life_path": lp,
        "expression": exp,
        "soul_urge": reduzir(tv),
        "personality": reduzir(tp),
        "destiny": reduzir(exp + lp),
    }


def calc_grid(nome):
    g = {i: 0 for i in range(1, 10)}
    for ch in normalizar_nome(nome):
        v = _LETRAS.get(ch, 0)
        if 1 <= v <= 9:
            g[v] += 1
    return g


def analisar_express(nome, data_str):
    return {"mapa": calc_mapa(nome, data_str), "tipo": "express"}


def analisar_completo(nome, data_str):
    return {"mapa": calc_mapa(nome, data_str), "grid": calc_grid(nome), "tipo": "completo"}


def analisar_vida(nome, data_str):
    return {"mapa": calc_mapa(nome, data_str), "tipo": "vida"}
