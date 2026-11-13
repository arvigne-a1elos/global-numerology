# ============================================================
# A1ELOS GLOBAL NUMEROLOGY — FONTE DE VERDADE ABSOLUTA
# referencia/cissay.py
# Quadro das Relações dos Números entre Si
# Fonte canônica: Monique Cissay, "A Numerologia", p. 159
# Legenda: 1=Dissonância | 2=Média (Acordo/Desacordo) | 3=Acordo | 4=Acordo perfeito
# ------------------------------------------------------------
# REGRAS CONSOLIDADAS (12/11/2026)
# 1. Acento NÃO zera letra: É=E=5, Á=A=1, Ã=A=1, Ç=C=3
# 2. Tabela pythagórica padrão A1..I9, J1..R9, S1..Z8
# 3. Número da pessoa = reduzir(energia_nome + energia_data)
# 4. reduzir() preserva 11 e 22 (números mestres)
# 5. O PRIMEIRO nome da lista ocupa a LINHA (margem esquerda)
# 6. Grau = MATRIZ[linha][coluna] — um único cruzamento
# 7. 22 x 22 = exceção especial, sem grau numérico
# 8. 7 pares de dualidade geram alerta no PDF
# ============================================================

import unicodedata

GRAUS = {
    1: "Dissonância",
    2: "Média - Acordo/Desacordo",
    3: "Acordo",
    4: "Acordo perfeito",
}

COLUNAS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22]

MATRIZ = {
    1:  [1, 2, 4, 3, 4, 1, 3, 4, 4, 4, 4],
    2:  [2, 2, 2, 3, 2, 4, 2, 4, 1, 3, 2],
    3:  [4, 2, 4, 1, 4, 3, 3, 3, 3, 3, 3],
    4:  [3, 3, 1, 2, 1, 3, 3, 2, 1, 1, 4],
    5:  [4, 2, 4, 1, 4, 1, 2, 3, 3, 2, 2],
    6:  [4, 4, 3, 3, 1, 2, 2, 3, 2, 3, 3],
    7:  [3, 2, 2, 4, 2, 2, 4, 1, 2, 2, 1],
    8:  [1, 4, 3, 2, 1, 3, 1, 1, 1, 4, 3],
    9:  [4, 1, 3, 4, 3, 2, 4, 2, 1, 4, 3],
    11: [4, 3, 3, 1, 2, 3, 2, 4, 4, 2, 3],
    22: [4, 2, 3, 4, 2, 3, 1, 3, 3, 3, None],
}

ESPECIAL_22_22 = (
    "Extremo raro — dois 22 (quatro 11): energia imensa e imprevisível. "
    "União ou confronto, sempre a um preço alto demais para ambos. "
    "Depende de fatores complementares; a sorte está lançada."
)

DUAIS = {
    frozenset((1, 6)),
    frozenset((1, 8)),
    frozenset((3, 7)),
    frozenset((4, 7)),
    frozenset((4, 9)),
    frozenset((5, 8)),
    frozenset((7, 9)),
}

ALERTA_DUALIDADE = (
    "A dualidade da relação permite convergência e divergência e a "
    "instabilidade é uma situação permanente, não havendo uma condição única "
    "e estável nessa relação, mas um cenário de permanente condicionamento "
    "de posturas individuais de ambas as partes."
)

CONFERIR = list(DUAIS)


# ------------------------------------------------------------
# TABELA DE LETRAS — REGRA 1 e 2
# ------------------------------------------------------------
LETRAS_BASE = {
    "A": 1, "B": 2, "C": 3, "D": 4, "E": 5,
    "F": 6, "G": 7, "H": 8, "I": 9,
    "J": 1, "K": 2, "L": 3, "M": 4, "N": 5,
    "O": 6, "P": 7, "Q": 8, "R": 9,
    "S": 1, "T": 2, "U": 3, "V": 4, "W": 5,
    "X": 6, "Y": 7, "Z": 8,
}

LETRAS_ESPECIAIS = {
    "Đ": "D",   # vietnamita — D implosivo, valor 4
    "Æ": "AE",  # dinamarquês/norueguês
    "Ø": "O",   # dinamarquês/norueguês
    "Ł": "L",   # polonês
    "Þ": "TH",  # islandês
    "ß": "SS",  # alemão
    "Ơ": "O",   # vietnamita
    "Ư": "U",   # vietnamita
    "Ğ": "G",   # turco
    "İ": "I",   # turco
    "Œ": "OE",  # francês
    "Ħ": "H",   # maltês
}

def normalizar_nome(nome):
    """Remove acentos preservando a letra-base. É=E, Á=A, Ç=C.
    Aplica as substituições de LETRAS_ESPECIAIS antes de remover acentos."""
    n = str(nome).upper()
    for orig, sub in LETRAS_ESPECIAIS.items():
        n = n.replace(orig, sub)
    n = unicodedata.normalize("NFD", n)
    n = "".join(c for c in n if unicodedata.category(c) != "Mn")
    return "".join(c for c in n if c.isalpha())


def normalizar_nome(nome):
    """Remove acentos preservando a letra-base. É=E, Á=A, Ç=C."""
    n = unicodedata.normalize("NFD", str(nome).upper())
    n = "".join(c for c in n if unicodedata.category(c) != "Mn")
    return "".join(c for c in n if c.isalpha())


def energia_nome(nome):
    """Soma as letras do nome. Acento não zera; a letra-base vale."""
    n = normalizar_nome(nome)
    return sum(LETRAS_BASE.get(c, 0) for c in n)


def reduzir(n):
    """Reduz a 1-9 preservando 11 e 22 (regra 4)."""
    while n > 9 and n not in (11, 22):
        n = sum(int(d) for d in str(n))
    return n


def energia_data(nasc):
    """Soma os dígitos da data AAAA-MM-DD e reduz."""
    try:
        s = sum(int(c) for c in str(nasc) if c.isdigit())
        return reduzir(s)
    except Exception:
        return None


def numero_pessoa(nome, nasc_iso):
    """Regra 3: N = reduzir(energia do nome + energia da data)."""
    en = energia_nome(nome)
    ed = energia_data(nasc_iso)
    if ed is None:
        return None
    return reduzir(en + ed)


# ------------------------------------------------------------
# CRUZAMENTO
# ------------------------------------------------------------
def _idx(num):
    return COLUNAS.index(num)


def obter_grau(n_linha, n_coluna):
    """Grau direcional. n_linha = primeiro nome da lista (topo).
    Retorna None no 22x22."""
    if n_linha == 22 and n_coluna == 22:
        return None
    try:
        return MATRIZ[n_linha][_idx(n_coluna)]
    except (KeyError, ValueError, IndexError):
        return None


def obter_rotulo(n_linha, n_coluna):
    if n_linha == 22 and n_coluna == 22:
        return ESPECIAL_22_22
    return GRAUS.get(obter_grau(n_linha, n_coluna), "Não catalogado")


def eh_dual(n1, n2):
    if n1 == 22 and n2 == 22:
        return False
    return frozenset((n1, n2)) in DUAIS


def compatibilidade(n_linha, n_coluna):
    """Dict pronto para o PDF. n_linha = primeiro nome da lista.
    Regra 5 e 6: primeiro nome na linha, um único cruzamento."""
    if n_linha == 22 and n_coluna == 22:
        return {"linha": n_linha, "coluna": n_coluna, "grau": None,
                "rotulo": ESPECIAL_22_22, "especial": True,
                "dual": False, "alerta_dualidade": None}
    g = obter_grau(n_linha, n_coluna)
    d = eh_dual(n_linha, n_coluna)
    return {"linha": n_linha, "coluna": n_coluna, "grau": g,
            "rotulo": obter_rotulo(n_linha, n_coluna), "especial": False,
            "dual": d,
            "alerta_dualidade": ALERTA_DUALIDADE if d else None}
