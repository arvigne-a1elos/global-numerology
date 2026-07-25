# -*- coding: utf-8 -*-
# urna.py - Validação de Nomes de Urna Eleitoral
from calc_service import calc_nome, reduzir

ENERGIAS = {
    1: "Liderança", 2: "Cooperação", 3: "Criatividade", 4: "Trabalho",
    5: "Liberdade", 6: "Família", 7: "Sabedoria",
    8: "Poder e Prosperidade (IDEAL)", 9: "Humanitarismo",
}

CARGO_LABELS = {
    "vereador": "Vereador", "dep_estadual": "Deputado Estadual",
    "dep_federal": "Deputado Federal", "senador": "Senador",
}

def validar_nomes(nomes, cargo_key):
    """Valida até 5 nomes de urna. Retorna (resultados, tem_ideal, sugestoes)."""
    results = []
    lv = {c: (i % 9 or 9) for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 1)}
    for nome in nomes:
        if not nome.strip():
            continue
        limpo = nome.upper().replace(" ", "").replace(".", "").replace("-", "").replace(",", "")
        letras = []
        st = 0
        for c in limpo:
            v = lv.get(c, 0)
            letras.append({"letra": c, "valor": v})
            st += v
        en = reduzir(st)
        eh_ideal = en == 8
        expl = (
            f"Nome {nome.strip().title()} tem ENERGIA 8! Ideal para candidatura."
            if eh_ideal else
            f"Nome {nome.strip().title()} tem energia {en}. {ENERGIAS.get(en, '')}. O 8 (Poder) é o ideal."
        )
        results.append({
            "nome": nome.strip().title(),
            "energia": en, "soma": st, "eh_ideal": eh_ideal,
            "explicacao": expl, "letras": letras,
        })
    ideal = any(r["eh_ideal"] for r in results)
    sugs = _gerar_sugestoes(nomes, cargo_key) if not ideal else []
    return results, ideal, sugs[:3]

def _gerar_sugestoes(nomes, cargo_key):
    """Gera sugestões de variações de nome com energia 8."""
    sugs = []
    label = CARGO_LABELS.get(cargo_key, "")
    prefixo = label[:3] if label else ""
    for nome in nomes:
        if not nome.strip():
            continue
        for tentativa in [
            f"{prefixo} {nome.strip()}",
            f"{nome.strip()} - {prefixo.lower()[:3]}",
        ]:
            en, _ = calc_nome(tentativa)
            sugs.append({"nome": tentativa.title(), "energia": en, "eh_ideal": en == 8})
            if len(sugs) >= 3:
                return sugs
    return sugs
