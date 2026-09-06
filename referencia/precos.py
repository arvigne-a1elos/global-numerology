# -*- coding: utf-8 -*-
# ================================================================
# referencia/precos.py
# TABELA DE REFERÊNCIA DE PREÇOS — A1ELOS
# FONTE ÚNICA DE VERDADE. TODOS os arquivos devem ler daqui:
#   main.py, translations.js (PRECO_DISPLAY), apresentacao_textos.py,
#   cards do site (atualizarPrecos).
#
# Valores fixos e proporcionais por 2 anos (promoção de lançamento),
# calibrados por renda média (PPP), arredondados para cima e sem
# valores quebrados.
#
# Estrutura: 6 faixas por idioma = [Entrada, Intermediário, Avançado, Premium]
#   faixa 0 = Entrada | faixa 1 = Intermediário | faixa 2-3 = Avançado | faixa 4-5 = Premium
# ================================================================

IDIOMAS = ["pt", "en", "es", "it", "fr", "de", "ja", "zh",
           "ru", "he", "ar", "id", "tr", "vi"]

# Símbolo da moeda por idioma (tr padronizado como "TL", não "₺")
SIMBOLO = {
    "pt": "R$", "en": "US$", "es": "€", "it": "€", "fr": "€", "de": "€",
    "ja": "¥", "zh": "¥", "ru": "₽", "id": "Rp", "tr": "TL", "vi": "₫",
    "he": "₪", "ar": "﷼",
}

# Valores em UNIDADES MENORES (centavos) — o que o Stripe cobra.
# Moedas de 2 casas = inteiro × 100. JPY e VND = inteiro (0 casas).
VALORES = {
    "pt": [800, 1700, 2600, 3500, 4400, 9800],
    "en": [2000, 4400, 7100, 8900, 11600, 25100],
    "es": [1100, 2600, 3500, 5300, 6200, 13400],
    "it": [1100, 2600, 3500, 5300, 6200, 13400],
    "fr": [1100, 2600, 3500, 5300, 6200, 13400],
    "de": [1100, 2600, 3500, 5300, 6200, 13400],
    "ja": [1400, 3000, 4600, 6200, 7700, 17000],        # JPY 0 casas
    "zh": [2600, 5300, 7100, 9800, 12500, 26000],
    "ru": [44000, 80000, 125000, 170000, 215000, 440000],
    "id": [1100000, 2300000, 3600000, 4800000, 6000000, 13400000],
    "tr": [5800, 12300, 18800, 25400, 31900, 71000],
    "vi": [25000, 53000, 81000, 109000, 137000, 305000],  # VND 0 casas
    "he": [4400, 9800, 14300, 19700, 24200, 53000],
    "ar": [3500, 7100, 10700, 14300, 17000, 37700],
}

# Valores de EXIBIÇÃO (o que o cliente vê no card) — por idioma.
PRECO_DISPLAY = {
    "pt": ["R$ 8", "R$ 17", "R$ 26–35", "R$ 44–98"],
    "en": ["US$ 20", "US$ 44", "US$ 71–89", "US$ 116–251"],
    "es": ["€ 11", "€ 26", "€ 35–53", "€ 62–134"],
    "it": ["€ 11", "€ 26", "€ 35–53", "€ 62–134"],
    "fr": ["€ 11", "€ 26", "€ 35–53", "€ 62–134"],
    "de": ["€ 11", "€ 26", "€ 35–53", "€ 62–134"],
    "ja": ["¥ 1.400", "¥ 3.000", "¥ 4.600–6.200", "¥ 7.700–17.000"],
    "zh": ["¥ 26", "¥ 53", "¥ 71–98", "¥ 125–260"],
    "ru": ["₽ 440", "₽ 800", "₽ 1.250–1.700", "₽ 2.150–4.400"],
    "id": ["Rp 11.000", "Rp 23.000", "Rp 36.000–48.000", "Rp 60.000–134.000"],
    "tr": ["TL 58", "TL 123", "TL 188–254", "TL 319–710"],
    "vi": ["₫ 25.000", "₫ 53.000", "₫ 81.000–109.000", "₫ 137.000–305.000"],
    "he": ["₪ 44", "₪ 98", "₪ 143–197", "₪ 242–530"],
    "ar": ["﷼ 35", "﷼ 71", "﷼ 107–143", "﷼ 170–377"],
}

# Mapa produto → faixa (0-5). Mantido aqui para centralizar.
PRODUTO_FAIXA = {
    "express": 0, "vida": 0, "completo": 1, "ia": 1,
    "urna": 2, "eleitoral": 2, "imovel": 2, "calendario": 2,
    "artistico": 3, "bebe": 3, "assinatura": 3,
    "negocio": 4, "casal": 4, "familia": 5, "coletivo": 5,
    "nome_pet": 0, "nickname": 0, "nome_dominio": 0, "nome_canal": 0,
    "nome_equipe": 0, "nome_ong": 0, "nome_projeto": 0, "nome_evento": 0,
}

def preco_local(produto, lang):
    """Retorna o valor em unidades menores (o que o Stripe cobra)."""
    lang = lang if lang in VALORES else "en"
    return VALORES[lang][PRODUTO_FAIXA[produto]]

def preco_display(lang, faixa=0):
    """Retorna o preço formatado para exibição no card."""
    lang = lang if lang in PRECO_DISPLAY else "en"
    return PRECO_DISPLAY[lang][faixa]
