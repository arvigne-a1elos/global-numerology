# -*- coding: utf-8 -*-
import json, os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_IN = os.path.join(RAIZ, "price_ids_teste.json")

SLUG_MAP = {
    "mapa_express": "express", "mapa_completo": "completo",
    "validacao_nome_de_urna": "urna", "numero_eleitoral": "eleitoral",
    "qual_vidaano": "vida", "pesquisa_ia_de_nomes": "ia",
    "nickname_digital": "nickname", "nome_do_pet": "nome_pet",
    "nome_do_dominio": "nome_dominio", "nome_do_canal": "nome_canal",
    "nome_da_equipe": "nome_equipe", "nome_do_projeto": "nome_projeto",
    "nome_do_evento": "nome_evento", "calendario_mensal_energetico": "calendario",
    "numero_do_imovel": "imovel", "nome_de_ong": "nome_ong",
    "validacao_nome_artistico": "artistico", "planejamento_nome_de_bebe": "bebe",
    "validacao_de_assinaturas": "assinatura", "nome_para_negocioproduto": "negocio",
    "mapa_do_casal": "casal", "mapa_familia_premium": "familia",
    "compatibilidade_de_equipes": "compatibilidade_equipes",
    "diagnostico_coletivo": "diagnostico",
}

ORDEM = ["pt", "en", "es", "it", "fr", "de", "ja", "zh", "ru", "id", "tr", "vi", "he", "ar"]

with open(JSON_IN, encoding="utf-8") as f:
    dados = json.load(f)

linhas = ["PRICE_IDS = {"]
for lang in ORDEM:
    itens = []
    for slug, chave in SLUG_MAP.items():
        itens.append(f'"{chave}": "{dados[lang][slug]}"')
    linhas.append(f'    "{lang}": {{' + ", ".join(itens) + "},")
linhas.append("}")

saida = os.path.join(RAIZ, "PRICE_IDS_novo.txt")
with open(saida, "w", encoding="utf-8") as f:
    f.write("\n".join(linhas))

print(f"Gerado: {len(ORDEM)} idiomas x {len(SLUG_MAP)} produtos")
print("Arquivo:", saida)
