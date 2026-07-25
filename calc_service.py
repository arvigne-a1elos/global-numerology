# -*- coding: utf-8 -*-
# calc_service.py - Cálculos numerológicos puros
import dateutil.parser as dp

def reduzir(n, permitir_mestre=True):
    """Reduz número a um dígito, preservando mestres 11, 22, 33."""
    while n > 9:
        if permitir_mestre and n in (11, 22, 33):
            return n
        n = sum(int(d) for d in str(n))
    return n

def calc_nome(nome):
    """Calcula energia numerológica de um nome. Retorna (numero_reduzido, soma_total)."""
    t = {c: (i % 9 or 9) for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 1)}
    limpo = nome.upper().replace(" ", "").replace(".", "").replace("-", "").replace(",", "")
    total = sum(t.get(c, 0) for c in limpo if c in t)
    return reduzir(total), total

def calc_mapa(nome, data_str):
    """Calcula os 5 números principais do mapa numerológico.
    Retorna dict com life_path, expression, soul_urge, personality, destiny."""
    bd = dp.parse(data_str).date()
    lp = reduzir(bd.day + bd.month + bd.year)
    t = {c: (i % 9 or 9) for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 1)}
    nu = nome.upper().replace(" ", "")
    total_e = total_v = total_p = 0
    for ch in nu:
        val = t.get(ch, 0)
        total_e += val
        if ch in "AEIOU":
            total_v += val
        else:
            total_p += val
    return {
        "life_path": lp,
        "expression": reduzir(total_e),
        "soul_urge": reduzir(total_v),
        "personality": reduzir(total_p),
        "destiny": reduzir(reduzir(total_e) + lp),
    }

def calc_grid(nome):
    """Calcula a grade de inclusão (frequência de cada número 1-9 no nome)."""
    t = {c: (i % 9 or 9) for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 1)}
    g = {i: 0 for i in range(1, 10)}
    for c in nome.upper().replace(" ", ""):
        v = t.get(c, 0)
        if 1 <= v <= 9:
            g[v] += 1
    return g

def calc_ciclos(lp, expr, alma, pers):
    """Calcula os ciclos de vida e seus números regentes."""
    fe = max(36 - min(lp, 36), 25)
    return {
        "fim_formativo": fe,
        "c1": reduzir(lp + expr),
        "c2": reduzir(expr + alma),
        "c3": reduzir(alma + pers),
    }

def calc_desafios(dia, mes, ano):
    """Calcula os 3 desafios a partir da data."""
    d1 = reduzir(abs(dia - mes))
    d2 = reduzir(abs(mes - reduzir(ano)))
    dp_ = reduzir(abs(d1 - d2))
    return {"menor1": d1, "menor2": d2, "principal": dp_}

def calc_realizacoes(dia, mes, ano):
    """Calcula as 4 realizações."""
    return {
        "r1": reduzir(dia + mes),
        "r2": reduzir(dia + ano),
        "r3": reduzir(reduzir(dia + mes) + reduzir(dia + ano)),
        "r4": reduzir(dia + mes + ano),
    }
