# -*- coding: utf-8 -*-
# produtos/urna.py - Validação de Nomes de Urna (5 tentativas + cálculo letra a letra)
from .mapa import reduzir, _LETRAS

CARGO_LABEL = {"vereador": "Vereador", "dep_estadual": "Dep. Estadual",
               "dep_federal": "Dep. Federal", "senador": "Senador"}

def validar_nomes_urna(nomes, cargo_key):
    results = []
    for nome in nomes:
        if not nome.strip():
            continue
        limpo = nome.upper().replace(" ", "").replace(".", "").replace("-", "").replace(",", "")
        letras = []
        st = 0
        for c in limpo:
            v = _LETRAS.get(c, 0)
            letras.append({"letra": c, "valor": v})
            st += v
        en = reduzir(st)
        expl = (f"Nome {nome.strip().title()} tem ENERGIA 8! Ideal para candidatura."
                if en == 8 else f"Nome {nome.strip().title()} tem energia {en}.")
        results.append({"nome": nome.strip().title(), "energia": en, "soma": st,
                        "eh_ideal": en == 8, "explicacao": expl, "letras": letras})
    ideal = any(r["eh_ideal"] for r in results)
    sugs = []
    if not ideal:
        lbl = CARGO_LABEL.get(cargo_key, "")
        for nome in nomes:
            if not nome.strip():
                continue
            for nt in [f"{lbl[:3]} {nome.strip()}", f"{nome.strip()} - {lbl.lower()[:3]}"]:
                total = sum(_LETRAS.get(c, 0) for c in nt.upper().replace(" ", ""))
                en = reduzir(total)
                sugs.append({"nome": nt.title(), "energia": en, "eh_ideal": en == 8})
                if len(sugs) >= 3:
                    break
            if len(sugs) >= 3:
                break
    return results, ideal, sugs[:3]
