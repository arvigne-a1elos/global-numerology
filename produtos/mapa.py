# -*- coding: utf-8 -*-
# produtos/mapa.py - Núcleo numerológico compartilhado + express/completo/vida
import dateutil.parser as dp

def reduzir(n):
    while n > 9 and n not in (11, 22, 33):
        n = sum(int(d) for d in str(n))
    return n

_LETRAS = {c: (i % 9 or 9) for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 1)}

def calc_mapa(nome, data_str):
    bd = dp.parse(data_str).date()
    lp = reduzir(bd.day + bd.month + bd.year)
    nu = nome.upper().replace(" ", "").replace("-", "")
    te = tv = tp = 0
    for ch in nu:
        val = _LETRAS.get(ch, 0)
        te += val
        if ch in "AEIOU":
            tv += val
        else:
            tp += val
    return {"life_path": lp, "expression": reduzir(te), "soul_urge": reduzir(tv),
            "personality": reduzir(tp), "destiny": reduzir(reduzir(te) + lp)}

def calc_grid(nome):
    g = {i: 0 for i in range(1, 10)}
    for ch in nome.upper().replace(" ", ""):
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
