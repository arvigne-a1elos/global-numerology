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
    "en": [1700, 4400, 7100, 9800, 12500, 15200],
    "es": [1700, 4400, 7100, 9800, 12500, 15200],
    "it": [1700, 4400, 7100, 9800, 12500, 15200],
    "fr": [1700, 4400, 7100, 9800, 12500, 15200],
    "de": [1700, 4400, 7100, 9800, 12500, 15200],
    "ja": [1376, 2924, 4472, 6020, 7568, 16856],        # JPY 0 casas
    "zh": [5300, 11600, 17000, 23300, 29600, 64700],
    "ru": [44000, 93500, 143000, 192500, 242000, 539000],
    "id": [1095200, 2327300, 3559400, 4791500, 6023600, 13416200],
    "tr": [6200, 13400, 20600, 26900, 34100, 76400],
    "vi": [24992, 53108, 81224, 109340, 137456, 306152],  # VND 0 casas
    "he": [5300, 11600, 17000, 23300, 29600, 64700],
    "ar": [5300, 11600, 17000, 23300, 29600, 64700],
}

# Valores de EXIBIÇÃO (o que o cliente vê no card) — por idioma.
PRECO_DISPLAY = {
    "pt": ["R$ 8", "R$ 17", "R$ 26", "R$ 35", "R$ 44", "R$ 98"],
    "en": ["US$ 17", "US$ 44", "US$ 71", "US$ 98", "US$ 125", "US$ 152"],
    "es": ["€ 17", "€ 44", "€ 71", "€ 98", "€ 125", "€ 152"],
    "it": ["€ 17", "€ 44", "€ 71", "€ 98", "€ 125", "€ 152"],
    "fr": ["€ 17", "€ 44", "€ 71", "€ 98", "€ 125", "€ 152"],
    "de": ["€ 17", "€ 44", "€ 71", "€ 98", "€ 125", "€ 152"],
    "ja": ["¥ 1.376", "¥ 2.924", "¥ 4.472", "¥ 6.020", "¥ 7.568", "¥ 16.856"],
    "zh": ["¥ 53", "¥ 116", "¥ 170", "¥ 233", "¥ 296", "¥ 647"],
    "ru": ["₽ 440", "₽ 935", "₽ 1.430", "₽ 1.925", "₽ 2.420", "₽ 5.390"],
    "id": ["Rp 10.952", "Rp 23.273", "Rp 35.594", "Rp 47.915", "Rp 60.236", "Rp 134.162"],
    "tr": ["TL 62", "TL 134", "TL 206", "TL 269", "TL 341", "TL 764"],
    "vi": ["₫ 24.992", "₫ 53.108", "₫ 81.224", "₫ 109.340", "₫ 137.456", "₫ 306.152"],
    "he": ["₪ 53", "₪ 116", "₪ 170", "₪ 233", "₪ 296", "₪ 647"],
    "ar": ["﷼ 53", "﷼ 116", "﷼ 170", "﷼ 233", "﷼ 296", "﷼ 647"],
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
