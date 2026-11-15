# -*- coding: utf-8 -*-
# produtos/casal.py - Mapa do Casal (motor único, valores validados)
import unicodedata
from .mapa import reduzir, calc_mapa
from referencia.cissay import MATRIZ
from dicionarios import get_compat


def _limpar(nome):
    n = unicodedata.normalize("NFD", (nome or "").upper())
    n = "".join(c for c in n if unicodedata.category(c) != "Mn")
    return "".join(c for c in n if "A" <= c <= "Z")


def numero_pessoa(nome, nasc):
    """Um número por pessoa: reduzir(energia_nome + energia_data)."""
    m = calc_mapa(nome, nasc)
    nome_n = m.get("expression") or m.get("personality")
    data_n = m.get("life_path")
    if nome_n is None or data_n is None:
        return None
    total = int(nome_n) + int(data_n)
    while total > 9 and total not in (11, 22):
        total = sum(int(d) for d in str(total))
    return total


_ROTULO = {
    1: "Dissonância",
    2: "Média - Acordo/Desacordo",
    3: "Acordo",
    4: "Acordo perfeito",
}


def analisar_casal(nome1, nasc1, nome2, nasc2):
    n1 = numero_pessoa(nome1, nasc1)
    n2 = numero_pessoa(nome2, nasc2)
    if n1 is None or n2 is None:
        return {
            "erro": "dados insuficientes",
            "nome1": nome1,
            "nome2": nome2,
        }

    # ordem fixada no método: primeiro nome ocupa a LINHA
    comp = MATRIZ[n1][n2]
    rotulo = _ROTULO.get(comp, "")

    rotulo = _ROTULO.get(comp, "")

    
    return {
        "nome1": nome1, "nasc1": nasc1, "numero1": n1,
        "energia1": n1, "energia_nome1": n1,
        "nome2": nome2, "nasc2": nasc2, "numero2": n2,
        "energia2": n2, "energia_nome2": n2,
        "compatibilidade": comp,
        "rotulo": rotulo,
        "rotulo_nome": rotulo,
        "leitura": get_compat(comp, "casal"),
    }
