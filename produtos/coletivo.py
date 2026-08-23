# -*- coding: utf-8 -*-
# produtos/coletivo.py - Bônus Coletivo/Empresarial (desconto progressivo)
def desconto_bc(qtd_total, empresarial=False):
    if empresarial:
        if qtd_total >= 3000: return 0.70
        if qtd_total >= 2000: return 0.60
    if qtd_total >= 2000: return 0.50
    if qtd_total >= 1000: return 0.45
    if qtd_total >= 500: return 0.40
    if qtd_total >= 200: return 0.30
    if qtd_total >= 100: return 0.25
    if qtd_total >= 50: return 0.20
    if qtd_total >= 10: return 0.10
    return 0.0
