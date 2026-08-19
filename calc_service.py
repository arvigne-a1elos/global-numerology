# -*- coding: utf-8 -*-
# calc_service.py - Cálculos numerológicos puros
import dateutil.parser as dp

def reduzir(n, permitir_mestre=True):
    """Reduz número a um dígito, preservando mestres 11, 22, 33."""
    while n > 9:
        if permitir_mestre and n in (11, 22, 33):
            return n
        n = sum(int(d) for d in str(n))
    return n

def calc_nome(nome):
    """Calcula energia numerológica de um nome. Retorna (numero_reduzido, soma_total)."""
    t = {c: (i % 9 or 9) for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 1)}
    limpo = nome.upper().replace(" ", "").replace(".", "").replace("-", "").replace(",", "")
    total = sum(t.get(c, 0) for c in limpo if c in t)
    return reduzir(total), total

def calc_mapa(nome, data_str):
    """Calcula os 5 números principais do mapa numerológico.
    Retorna dict com life_path, expression, soul_urge, personality, destiny."""
    bd = dp.parse(data_str).date()
    lp = reduzir(bd.day + bd.month + bd.year)
    t = {c: (i % 9 or 9) for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 1)}
    nu = nome.upper().replace(" ", "")
    total_e = total_v = total_p = 0
    for ch in nu:
        val = t.get(ch, 0)
        total_e += val
        if ch in "AEIOU":
            total_v += val
        else:
            total_p += val
    return {
        "life_path": lp,
        "expression": reduzir(total_e),
        "soul_urge": reduzir(total_v),
        "personality": reduzir(total_p),
        "destiny": reduzir(reduzir(total_e) + lp),
    }

def calc_grid(nome):
    """Calcula a grade de inclusão (frequência de cada número 1-9 no nome)."""
    t = {c: (i % 9 or 9) for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 1)}
    g = {i: 0 for i in range(1, 10)}
    for c in nome.upper().replace(" ", ""):
        v = t.get(c, 0)
        if 1 <= v <= 9:
            g[v] += 1
    return g

def calc_ciclos(lp, expr, alma, pers):
    """Calcula os ciclos de vida e seus números regentes."""
    fe = max(36 - min(lp, 36), 25)
    return {
        "fim_formativo": fe,
        "c1": reduzir(lp + expr),
        "c2": reduzir(expr + alma),
        "c3": reduzir(alma + pers),
    }

def calc_desafios(dia, mes, ano):
    """Calcula os 3 desafios a partir da data."""
    d1 = reduzir(abs(dia - mes))
    d2 = reduzir(abs(mes - reduzir(ano)))
    dp_ = reduzir(abs(d1 - d2))
    return {"menor1": d1, "menor2": d2, "principal": dp_}

def calc_realizacoes(dia, mes, ano):
    """Calcula as 4 realizações."""
    return {
        "r1": reduzir(dia + mes),
        "r2": reduzir(dia + ano),
        "r3": reduzir(reduzir(dia + mes) + reduzir(dia + ano)),
        "r4": reduzir(dia + mes + ano),
    }
# ===== FUNÇÕES MOVIDAS DO MAIN.PY (CORRIGIDAS — preservam o comportamento original) =====

CARGO_INFO = {
    "vereador": {"label": "Vereador"},
    "dep_estadual": {"label": "Deputado Estadual"},
    "dep_federal": {"label": "Deputado Federal"},
    "senador": {"label": "Senador"},
}
ENERGIAS = {
    1: "Lideranca", 2: "Cooperacao", 3: "Criatividade",
    4: "Trabalho", 5: "Liberdade", 6: "Familia",
    7: "Sabedoria", 8: "Poder e Prosperidade (IDEAL)", 9: "Humanitarismo",
}

def validar_nomes_urna(nomes, cargo_key):
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
        if en == 8:
            expl = f"Nome {nome.strip().title()} tem ENERGIA 8! Ideal para candidatura."
        else:
            expl = f"Nome {nome.strip().title()} tem energia {en}. {ENERGIAS.get(en, '')}."
        results.append({"nome": nome.strip().title(), "energia": en,
                        "soma": st, "eh_ideal": en == 8,
                        "explicacao": expl, "letras": letras})
    ideal = any(r["eh_ideal"] for r in results)
    sugs = []
    if not ideal:
        for nome in nomes:
            if not nome.strip():
                continue
            lbl = CARGO_INFO.get(cargo_key, {}).get("label", "")
            if not lbl:
                continue
            for nt in [f"{lbl[:3]} {nome.strip()}", f"{nome.strip()} - {lbl.lower()[:3]}"]:
                en, _ = calc_nome(nt)
                sugs.append({"nome": nt.title(), "energia": en, "eh_ideal": en == 8})
                if len(sugs) >= 3:
                    break
            if len(sugs) >= 3:
                break
    return results, ideal, sugs[:3]

def gerar_numeros(sigla, cargo, qtd=5):
    dc = {"vereador": 5, "dep_estadual": 5, "dep_federal": 4, "senador": 3}
    td = dc.get(cargo, 5)
    ss = str(sigla).zfill(2)[:2]
    sm = int(ss[0]) + int(ss[1])
    lv = td - 2
    res = []
    tent = set()
    def busca(alvo):
        enc = []
        for x in range(10 ** lv):
            if len(enc) + len(res) >= qtd:
                break
            dl = str(x).zfill(lv)
            en = reduzir(sm + sum(int(d) for d in dl))
            if en == alvo:
                n = ss + dl
                if n not in tent:
                    if x in range(1, 10) and alvo != reduzir(sm):
                        continue
                    tent.add(n)
                    st = sm + sum(int(d) for d in dl)
                    enc.append({"numero": n, "energia": alvo, "ideal": alvo == 8,
                                "sigla": ss, "digitos_livres": dl,
                                "soma_sigla": sm, "soma_total": st})
        return enc
    res.extend(busca(8))
    if len(res) < qtd:
        res.extend(busca(3))
    if len(res) < qtd:
        for e in [7, 1, 9, 5, 6, 4, 2]:
            if len(res) >= qtd:
                break
            res.extend(busca(e))
    return res[:qtd]
