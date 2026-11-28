# -*- coding: utf-8 -*-
# produtos/nome.py - Análise de energia de nomes
import unicodedata
from .mapa import reduzir, _LETRAS

# Letras que o NFD do Unicode não decompõe em letra + acento.
_LETRAS_ESPECIAIS = {
    "Æ": "AE", "Œ": "OE", "Ø": "O", "Đ": "D", "Ł": "L",
    "Þ": "TH", "Ð": "D", "Ħ": "H", "Ŧ": "T", "Ŋ": "N",
}

def normalizar(texto):
    """Mesma regra do produtos.js: maiúsculas, sem acento, apenas A-Z."""
    s = str(texto or "").upper()
    for k, v in _LETRAS_ESPECIAIS.items():
        s = s.replace(k, v)
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return "".join(c for c in s if "A" <= c <= "Z")

def analisar_nome(nome, energia=None):
    limpo = normalizar(nome)

    # Alfabeto não suportado: recusar explicitamente em vez de entregar zero.
    if not limpo:
        return {
            "nome": nome.strip(),
            "soma": 0,
            "energia": None,
            "erro": "alfabeto_nao_suportado",
        }

    soma = sum(_LETRAS.get(c, 0) for c in limpo)
    en = reduzir(soma)
    res = {"nome": nome.strip(), "soma": soma, "energia": en}

    if energia:
        res["energia_desejada"] = int(energia)
        res["match"] = en == int(energia)
    return res
