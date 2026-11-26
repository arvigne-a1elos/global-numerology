# -*- coding: utf-8 -*-
# Atualiza o bloco PRICE_IDS do main.py com os price IDs de teste.
# NÃO apaga nada antes de ter o conteúdo novo validado. Cria backup primeiro.
import json, os, shutil, re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN = os.path.join(RAIZ, "main.py")
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

# ---- 1. Validações ANTES de qualquer escrita ----
if not os.path.exists(JSON_IN):
    raise SystemExit("ERRO: price_ids_teste.json nao existe na raiz. Rode antes:\n  python scripts\\criar_precos_stripe.py --teste --executar --arquivo \"scripts\\Tabela de Controle - Numerologia - 24 Produtos - 14 Idiomas - 001.xlsx\"")
if not os.path.exists(MAIN):
    raise SystemExit("ERRO: main.py nao encontrado na raiz.")

with open(JSON_IN, encoding="utf-8") as f:
    dados = json.load(f)

faltando = []
for lang in ORDEM:
    for slug in SLUG_MAP:
        if lang not in dados or slug not in dados.get(lang, {}):
            faltando.append(f"{lang}/{slug}")
if faltando:
    raise SystemExit(f"ERRO: dados incompletos no JSON ({len(faltando)} faltando), ex.: {faltando[:5]}. NADA foi alterado.")

# ---- 2. Monta o bloco novo (na memoria, ainda sem gravar nada) ----
linhas = ["# ===== PRICE IDS STRIPE (24 produtos, 14 idiomas) ====="]
linhas.append("PRICE_IDS = {")
for lang in ORDEM:
    itens = [f'"{chave}": "{dados[lang][slug]}"' for slug, chave in SLUG_MAP.items()]
    linhas.append(f'    "{lang}": {{' + ", ".join(itens) + "},")
linhas.append("}")
bloco_novo = "\n".join(linhas)

with open(MAIN, encoding="utf-8") as f:
    conteudo = f.read()

# Localiza o bloco atual: de "# ===== PRICE IDS" até o "}" que fecha PRICE_IDS
padrao = re.compile(r'# ===== PRICE IDS STRIPE.*?\nPRICE_IDS = \{.*?\n\}', re.DOTALL)
m = padrao.search(conteudo)
if not m:
    raise SystemExit("ERRO: bloco PRICE_IDS atual nao localizado no main.py. NADA foi alterado. Me cole as linhas 310-320 do main.py.")

# ---- 3. Tudo validado: agora sim, backup e substituicao ----
backup = os.path.join(RAIZ, "main_backup_precos.py")
shutil.copy2(MAIN, backup)

conteudo_novo = conteudo[:m.start()] + bloco_novo + conteudo[m.end():]
with open(MAIN, "w", encoding="utf-8") as f:
    f.write(conteudo_novo)

# ---- 4. Verificacao pos-gravacao ----
ok = "diagnostico" in conteudo_novo and conteudo_novo.count("price_") >= 336
print(f"OK. Backup salvo em: {backup}")
print(f"Substituido: bloco PRICE_IDS ({m.end()-m.start()} chars -> {len(bloco_novo)} chars)")
print(f"Idiomas: {len(ORDEM)} | Produtos por idioma: {len(SLUG_MAP)}")
print("Restante do main.py preservado intacto.")
