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
    lp = reduzir(bd.day + bd.month + bd.year)
    nu = normalizar_nome(nome)

    total = vogais = consoantes = 0
    for ch in nu:
        val = _LETRAS.get(ch, 0)
        total += val
        if ch in "AEIOU":
            vogais += val
        else:
            consoantes += val

    personalidade = reduzir(total)      # TODAS as letras
    alma = reduzir(vogais)              # vogais
    realizacao = reduzir(consoantes)    # consoantes

    return {
        "life_path": lp,
        "expression": personalidade,     # compatibilidade
        "personality": personalidade,    # todas as letras
        "soul_urge": alma,               # vogais
        "realizacao": realizacao,        # consoantes (NOVO)
        "destiny": reduzir(lp + personalidade),  # número da pessoa
    }

def analisar_express(nome, data_str):
    return {"mapa": calc_mapa(nome, data_str), "tipo": "express"}


def analisar_completo(nome, data_str):
    return {"mapa": calc_mapa(nome, data_str), "grid": calc_grid(nome), "tipo": "completo"}


def analisar_vida(nome, data_str):
    return {"mapa": calc_mapa(nome, data_str), "tipo": "vida"}
