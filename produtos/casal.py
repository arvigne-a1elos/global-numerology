# -*- coding: utf-8 -*-
# produtos/casal.py - Mapa do Casal (usa o MESMO motor do mapa.py)
import unicodedata
from .mapa import reduzir, _LETRAS, calc_mapa
from referencia.cissay import compatibilidade


def _limpar(nome):
    """Normaliza igual ao mapa.py: remove acentos e mantém só A-Z."""
    n = unicodedata.normalize("NFD", (nome or "").upper())
    n = "".join(c for c in n if unicodedata.category(c) != "Mn")
    return "".join(c for c in n if "A" <= c <= "Z")


def _energia_nome(nome):
    limpo = _limpar(nome)
    s = sum(_LETRAS.get(c, 0) for c in limpo)
    return reduzir(s), s


def _caminho_vida(nasc, nome=""):
    """Usa calc_mapa para garantir o MESMO caminho de vida do mapa principal."""
    if not nasc:
        return None, 0
    try:
        r = calc_mapa(nome or "Teste", nasc)
        cv = r.get("life_path")
        if cv is None:
            return None, 0
        if r.get("life_path_mestre") and int(cv) in (11, 22):
            return int(cv), int(cv)
        return reduzir(int(cv)), int(cv)
    except Exception:
        try:
            d, m, a = nasc.split("-")
            s = sum(int(x) for x in d + m + a)
            return reduzir(s), s
        except Exception:
            return None, 0


def analisar_casal(nome1, nasc1, nome2, nasc2):
    e1n, s1n = _energia_nome(nome1)
    e2n, s2n = _energia_nome(nome2)
    e1v, s1v = _caminho_vida(nasc1, nome1)
    e2v, s2v = _caminho_vida(nasc2, nome2)

    cn = compatibilidade(e1n, e2n)
    cv = compatibilidade(e1v, e2v) if e1v and e2v else None

    # MESMO critério da família: caminho de vida manda
    if cv and cv.get("grau") is not None:
        comp_final = cv["grau"]
    elif cn.get("grau") is not None:
        comp_final = cn["grau"]
    else:
        comp_final = None

    return {
        "nome1": nome1, "nasc1": nasc1, "energia_nome1": e1n, "caminho1": e1v,
        "nome2": nome2, "nasc2": nasc2, "energia_nome2": e2n, "caminho2": e2v,
        "soma1": s1n, "soma2": s2n,
        "compatibilidade_nome": cn.get("grau"),
        "rotulo_nome": cn.get("rotulo"),
        "dual_nome": cn.get("dual"),
        "alerta_dualidade_nome": cn.get("alerta_dualidade"),
        "compatibilidade_vida": cv["grau"] if cv else None,
        "rotulo_vida": cv["rotulo"] if cv else None,
        "dual_vida": cv["dual"] if cv else False,
        "alerta_dualidade_vida": cv["alerta_dualidade"] if cv else None,
        "compatibilidade": comp_final,
        "rotulo": cv["rotulo"] if cv else (cn.get("rotulo") if cn else None),
    }
        "dual_vida": cv["dual"] if cv else False,
        "alerta_dualidade_vida": cv["alerta_dualidade"] if cv else None,
        "compatibilidade": comp_final,
    }
