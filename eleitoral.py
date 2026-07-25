# -*- coding: utf-8 -*-
# eleitoral.py - Geração de Números Eleitorais
from calc_service import reduzir

ENERGIAS = {
    8: "Poder e Prosperidade (IDEAL)", 7: "Sabedoria", 3: "Criação",
    1: "Liderança", 9: "Humanitarismo", 5: "Liberdade",
    6: "Família", 4: "Trabalho", 2: "Associação",
}

DIGITOS_CARGO = {
    "vereador": 5, "dep_estadual": 5,
    "dep_federal": 4, "senador": 3,
}

def gerar_numeros(sigla, cargo, qtd=5):
    """Gera números eleitorais com energia 8 prioritariamente.
    Retorna lista de dicts com numero, energia, ideal, explicacao_calculo."""
    td = DIGITOS_CARGO.get(cargo, 5)
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
                    tent.add(n)
                    st = sm + sum(int(d) for d in dl)
                    dl_sum = "+".join(dl)
                    enc.append({
                        "numero": n, "energia": alvo, "ideal": alvo == 8,
                        "sigla": ss, "digitos_livres": dl,
                        "soma_sigla": sm, "soma_total": st,
                        "nome_energia": ENERGIAS.get(alvo, ""),
                        "explicacao_calculo": (
                            f"Sigla {ss} ({ss[0]}+{ss[1]}={sm}) + "
                            f"dígitos {dl} ({dl_sum}={sum(int(d) for d in dl)}) = "
                            f"{st} -> {alvo}"
                        ),
                    })
        return enc

    res.extend(busca(8))  # IDEAL primeiro
    if len(res) < qtd:
        res.extend(busca(3))
    for e in [7, 1, 9, 5, 6, 4, 2]:
        if len(res) >= qtd:
            break
        res.extend(busca(e))
    return res[:qtd]
