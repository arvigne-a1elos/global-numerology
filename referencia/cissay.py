# ============================================================
# A1ELOS GLOBAL NUMEROLOGY — FONTE DE VERDADE ABSOLUTA
# referencia/cissay.py
# Quadro das Relações dos Números entre Si
# Fonte canônica: Monique Cissay, "A Numerologia", p. 159
# Legenda: 1=Dissonância | 2=Média (Acordo/Desacordo) | 3=Acordo | 4=Acordo perfeito
# Registro: 28/09/2026 — cruzamento 22x22 é exceção especial (sem grau numérico)
# 28/09/2026 — 7 pares com dualidade convergência/divergência geram alerta no PDF
# ============================================================

GRAUS = {
    1: "Dissonância",
    2: "Média - Acordo/Desacordo",
    3: "Acordo",
    4: "Acordo perfeito",
}

COLUNAS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22]

# Matriz Direcional: MATRIZ[linha_agente][_idx(coluna_receptora)]
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
    22: [4, 2, 3, 4, 2, 3, 1, 3, 3, 3, None],  # (22,22): exceção especial
}

ESPECIAL_22_22 = (
    "Extremo raro — dois 22 (quatro 11): energia imensa e imprevisível. "
    "União ou confronto, sempre a um preço alto demais para ambos. "
    "Depende de fatores complementares; a sorte está lançada."
)

# 7 pares com dualidade: convergência OU divergência — instabilidade permanente.
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

# Pares direcionais para conferência visual na obra
CONFERIR = list(DUAIS)

def _idx(num):
    return COLUNAS.index(num)

def obter_grau(n1, n2):
    """Grau direcional (1-4) de n1 (age) sobre n2 (recebe). None no 22x22."""
    if n1 == 22 and n2 == 22:
        return None
    try:
        return MATRIZ[n1][_idx(n2)]
    except (KeyError, ValueError, IndexError):
        return None

def obter_rotulo(n1, n2):
    """Rótulo textual do grau, ou a nota especial do cruzamento 22x22."""
    if n1 == 22 and n2 == 22:
        return ESPECIAL_22_22
    return GRAUS.get(obter_grau(n1, n2), "Não catalogado")

def eh_dual(n1, n2):
    """True quando o par está na lista de dualidade convergência/divergência."""
    if n1 == 22 and n2 == 22:
        return False
    return frozenset((n1, n2)) in DUAIS

def compatibilidade(n1, n2):
    """Dict pronto para o PDF (casal/família). Inclui alerta de dualidade."""
    if n1 == 22 and n2 == 22:
        return {"n1": n1, "n2": n2, "grau": None,
                "rotulo": ESPECIAL_22_22, "especial": True,
                "dual": False, "alerta_dualidade": None}
    return {"n1": n1, "n2": n2, "grau": obter_grau(n1, n2),
            "rotulo": obter_rotulo(n1, n2), "especial": False,
            "dual": eh_dual(n1, n2),
            "alerta_dualidade": ALERTA_DUALIDADE if eh_dual(n1, n2) else None}
