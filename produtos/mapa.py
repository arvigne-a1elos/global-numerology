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

VOGAIS = "AEIOU"

def calc_mapa(nome, data_str):
    bd = dp.parse(data_str).date()
    nu = normalizar_nome(nome)

    # --- Caminho de Vida ---
    lp_bruto = bd.day + bd.month + bd.year
    lp = reduzir(lp_bruto)
    lp_mestre = lp_bruto if lp_bruto in (11, 22) else None

    # --- Letras ---
    total = vogais = consoantes = 0
    for ch in nu:
        val = _LETRAS.get(ch, 0)
        total += val
        if ch in VOGAIS:
            vogais += val
        else:
            consoantes += val

    assert vogais + consoantes == total, "partição de letras quebrada"

    # --- Energias finais (SEMPRE reduzidas) + mestre como observação ---
    personalidade = reduzir(total)
    alma = reduzir(vogais)
    realizacao = reduzir(consoantes)
    numero = reduzir(lp + personalidade)

    return {
        "life_path": lp,
        "life_path_mestre": lp_mestre,
        "expression": personalidade,
        "personality": personalidade,
        "personality_mestre": total if total in (11, 22) else None,
        "soul_urge": alma,
        "soul_urge_mestre": vogais if vogais in (11, 22) else None,
        "realizacao": realizacao,
        "realizacao_mestre": consoantes if consoantes in (11, 22) else None,
        "destiny": numero,
        "destiny_mestre": (lp + personalidade) if (lp + personalidade) in (11, 22) else None,
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
