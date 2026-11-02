# -*- coding: utf-8 -*-
# produtos/imovel.py - Número do Imóvel (3 campos + sugestão única + dica traduzida)
from .mapa import reduzir

LETRAS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def _valor_alfanumerico(texto):
    """Dígitos somam direto; letras viram número pitagórico (A=1...I=9, J=1...Z=8).
    Ex.: 'B' -> 2 · '7' -> 7 · 'C2' -> 3+2=5"""
    if not texto:
        return None
    t = str(texto).upper()
    soma = 0
    tem_algo = False
    for ch in t:
        if ch.isdigit():
            soma += int(ch)
            tem_algo = True
        else:
            idx = LETRAS.find(ch)
            if idx >= 0:
                soma += (idx % 9) + 1
                tem_algo = True
    if not tem_algo:
        return None
    while soma > 9 and soma not in (11, 22, 33):
        soma = sum(int(d) for d in str(soma))
    return soma

# Sugestão única por energia do imóvel
SUGESTAO_UNICA = {
    1: "Lugar ideal para: empreendimentos e escritórios de negócios — energia de iniciativa e novos começos.",
    2: "Lugar ideal para: famílias, casais e ambientes de cuidado — energia de cooperação e paz.",
    3: "Lugar ideal para: agências, estúdios e espaços sociais — energia de criatividade e comunicação.",
    4: "Lugar ideal para: clínicas, escritórios e projetos de longo prazo — energia de estabilidade e trabalho.",
    5: "Lugar ideal para: comércio, viagens e transformações — energia de movimento e liberdade.",
    6: "Lugar ideal para: lares, escolas e serviços de saúde — energia de família e responsabilidade.",
    7: "Lugar ideal para: consultórios, bibliotecas e retiros — energia de estudo e espiritualidade.",
    8: "Lugar ideal para: empresas, bancos e finanças — energia de poder material e realização.",
    9: "Lugar ideal para: causas sociais, ONGs e acolhimento — energia de compaixão e conclusões.",
}

# Dica traduzida por idioma
DICAS_HARMONIZACAO = {
    "pt": "💡 Dica: a energia do imóvel é fixa, mas cada ambiente pode ter a sua. Numere ou dê nome às salas e portas — cada palavra ou número vibra em uma energia que se soma à do local. Nossas ferramentas de nomenclatura (Nome para Negócio/Produto) indicam a melhor designação para cada cômodo.",
    "en": "💡 Tip: the energy of the property is fixed, but each room can have its own. Number or name the rooms and doors — every word or number carries an energy that adds to the place. Our naming tools (Business/Product Name) indicate the best designation for each room.",
    # ... es, it, fr, de, ja, zh, ru, he, ar, id, tr, vi
}

def analisar_imovel(dado, dado2="", dado3="", lang="pt"):
    """Recebe os 3 campos do modal. Qualquer combinação >= 1 campo gera o PDF.
    Ex.: imóvel 81, escritório 7, sala B -> 9 + 7 + 2 = 18 -> (9)"""
    partes = [_valor_alfanumerico(dado),
              _valor_alfanumerico(dado2),
              _valor_alfanumerico(dado3)]
    partes = [p for p in partes if p is not None]
    if not partes:
        return {"numero": str(dado), "energia": None, "ok": False}
    total = sum(partes)
    while total > 9 and total not in (11, 22, 33):
        total = sum(int(d) for d in str(total))
    return {
        "numero": " + ".join(str(x) for x in [dado, dado2, dado3] if str(x).strip()),
        "partes": partes,
        "soma": sum(partes),
        "energia": total,
        "sugestao": SUGESTAO_UNICA.get(total, ""),
        "dica": DICAS_HARMONIZACAO.get(lang, DICAS_HARMONIZACAO["pt"]),
        "ok": True,
    }
