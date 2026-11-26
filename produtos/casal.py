# -*- coding: utf-8 -*-
# produtos/casal.py - Mapa do Casal
# MOTOR ÚNICO: referencia/cissay.py (mesma fonte de familia.py e equipe.py)
from referencia.cissay import compatibilidade, numero_pessoa
from dicionarios import get_compat


def analisar_casal(nome1, nasc1, nome2, nasc2, apelido1="", apelido2="", lang="pt"):
    n1 = numero_pessoa(nome1, nasc1)
    n2 = numero_pessoa(nome2, nasc2)
    if n1 is None or n2 is None:
        return {"erro": "dados insuficientes", "nome1": nome1, "nome2": nome2}

    comp = compatibilidade(n1, n2)
    g = comp["grau"]

    a1 = numero_pessoa(apelido1, nasc1) if (apelido1 or "").strip() else None
    a2 = numero_pessoa(apelido2, nasc2) if (apelido2 or "").strip() else None
    ca = compatibilidade(a1, a2) if (a1 is not None and a2 is not None) else None
    ga = ca["grau"] if ca else None

    return {
        "nome1": nome1, "nasc1": nasc1, "numero1": n1,
        "energia1": n1, "energia_nome1": n1,
        "nome2": nome2, "nasc2": nasc2, "numero2": n2,
        "energia2": n2, "energia_nome2": n2,
        "compatibilidade": g,
        "rotulo": comp["rotulo"], "rotulo_nome": comp["rotulo"],
        "dual": comp.get("dual", False),
        "alerta_dualidade": comp.get("alerta_dualidade"),
        "leitura": get_compat(g, "casal", lang) if g is not None else comp["rotulo"],
        "apelido1": apelido1, "apelido2": apelido2,
        "numero1_apelido": a1, "numero2_apelido": a2,
        "compatibilidade_apelido": ga,
        "rotulo_apelido": ca["rotulo"] if ca else "",
        "dual_apelido": ca.get("dual", False) if ca else False,
        "alerta_dualidade_apelido": ca.get("alerta_dualidade") if ca else None,
    }
