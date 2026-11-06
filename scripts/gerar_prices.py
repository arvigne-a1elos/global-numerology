# -*- coding: utf-8 -*-
# scripts/gerar_prices.py - traduz price_ids_teste.json para o PRICES do main.py
import json, os

SLUG_MAP = {
    "mapa_express": "express", "mapa_completo": "completo",
    "validacao_nome_de_urna": "urna", "numero_eleitoral": "eleitoral",
    "qual_vidaano": "vida_ano", "pesquisa_ia_de_nomes": "pesquisa_nomes",
    "nickname_digital": "nickname", "nome_do_pet": "pet",
    "nome_do_dominio": "dominio", "nome_do_canal": "canal",
    "nome_da_equipe": "equipe", "nome_do_projeto": "projeto",
    "nome_do_evento": "evento", "calendario_mensal_energetico": "calendario",
    "numero_do_imovel": "imovel", "nome_de_ong": "ong",
    "validacao_nome_artistico": "artistico", "planejamento_nome_de_bebe": "bebe",
    "validacao_de_assinaturas": "assinaturas", "nome_para_negocioproduto": "negocio",
    "mapa_do_casal": "casal", "mapa_familia_premium": "familia",
    "compatibilidade_de_equipes": "compatibilidade", "diagnostico_coletivo": "diagnostico",
}

ORDEM_IDIOMAS = ["pt", "en", "es", "it", "fr", "de", "ja", "zh", "ru", "id", "tr", "vi", "he", "ar"]

with open("price_ids_teste.json", encoding="utf-8") as f:
    dados = json.load(f)

linhas = ["PRICES = {"]
total = 0
for lang in ORDEM_IDIOMAS:
    bloco = dados[lang]
    itens = []
    for slug, chave in SLUG_MAP.items():
        pid = bloco[slug]
        itens.append(f'"{chave}": "{pid}"')
        total += 1
    linjas_lang = ", ".join(itens)
    linhas.append(f'    "{lang}": {{{linjas_lang}}},')
linhas.append("}")

with open("PRICES_novo.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(linhas))

print(f"PRICES gerado: {len(ORDEM_IDIOMAS)} idiomas, {total} price IDs")
print("Arquivo: PRICES_novo.txt (cole o conteúdo no lugar do PRICES do main.py)")
