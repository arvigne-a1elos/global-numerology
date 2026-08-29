"""
corrigir_precos_v2.py — Corrige o alinhamento dos precos nos cards.

DIAGNOSTICO
Os precos estao trocados porque a ordem dos valores adicionados no DEF
nao corresponde a ordem das chaves no KEYS. Cada chave puxa a posicao
errada.

SOLUCAO
Remove as 4 chaves antigas do KEYS e os 4 valores antigos do DEF,
depois reinsere tudo na ordem correta.

Uso: python corrigir_precos_v2.py index.html
"""

import re
import sys

PRECOS = {
    "pt": ["R$ 8,00", "R$ 17,00", "R$ 26,00", "R$ 26,00"],
    "en": ["US$ 1,50", "US$ 3,50", "US$ 5,00", "US$ 5,00"],
    "es": ["€ 1,50", "€ 3,50", "€ 5,00", "€ 5,00"],
    "fr": ["€ 1,50", "€ 3,50", "€ 5,00", "€ 5,00"],
    "de": ["€ 1,50", "€ 3,50", "€ 5,00", "€ 5,00"],
    "it": ["€ 1,50", "€ 3,50", "€ 5,00", "€ 5,00"],
    "ja": ["¥ 250", "¥ 550", "¥ 800", "¥ 800"],
    "zh": ["¥ 12", "¥ 25", "¥ 40", "¥ 40"],
    "ru": ["₽ 130", "₽ 280", "₽ 430", "₽ 430"],
    "id": ["Rp 24.000", "Rp 56.000", "Rp 80.000", "Rp 80.000"],
    "tr": ["₺ 51", "₺ 119", "₺ 170", "₺ 170"],
    "vi": ["₫ 38.000", "₫ 88.000", "₫ 125.000", "₫ 125.000"],
    "he": ["₪ 5,00", "₪ 13,00", "₪ 19,00", "₪ 19,00"],
    "ar": ["﷼ 6,00", "﷼ 13,00", "﷼ 19,00", "﷼ 19,00"],
}

NOVAS_CHAVES = "'price_express','price_completo','price_urna','price_eleitoral'"

def corrigir(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        html = f.read()

    # PASSO 1: Verificar se as chaves ja existem no KEYS
    if "price_express" in html:
        print("Chaves price_* ja existem. Removendo e reinserindo na ordem correta...")
        
        # Remove as 4 chaves do KEYS (podem estar em qualquer ordem)
        html = re.sub(r",'price_express'", "", html)
        html = re.sub(r",'price_completo'", "", html)
        html = re.sub(r",'price_urna'", "", html)
        html = re.sub(r",'price_eleitoral'", "", html)
        
        # Remove os 4 valores do final de cada idioma no DEF
        # Cada idioma termina com |VALOR1|VALOR2|VALOR3|VALOR4'
        for lang in PRECOS.keys():
            # Remove os ultimos 4 pipes + valores antes da aspa final
            padrao = re.escape(f"|{PRECOS[lang][0]}|{PRECOS[lang][1]}|{PRECOS[lang][2]}|{PRECOS[lang][3]}'")
            html = re.sub(padrao, "'", html)
        
        print("  Valores antigos removidos.")
    
    # PASSO 2: Adicionar as chaves no KEYS (antes de footer_text)
    if "'price_express'" not in html:
        html = html.replace("'footer_text'", f"{NOVAS_CHAVES},'footer_text'", 1)
        print("  Chaves adicionadas ao KEYS.")
    
    # PASSO 3: Adicionar os 4 valores no final de cada idioma no DEF
    for lang, valores in PRECOS.items():
        # Encontra o final da string do idioma (antes da aspa simples de fechamento)
        # O padrao e: lang:'...ULTIMO_VALOR'
        sufixo = "|" + "|".join(valores)
        
        # Procura por lang:'...' e substitui o ' final por sufixo + '
        # Usa lookbehind para encontrar a aspa que fecha a string
        padrao = re.compile(r"(" + re.escape(lang) + r":'(?:[^'\]|\.)*?)'")
        
        def substituir(m):
            return m.group(1) + sufixo + "'"
        
        html = padrao.sub(substituir, html, count=1)
        print(f"  {lang}: valores adicionados.")
    
    # PASSO 4: Verificar os 4 divs de preco
    # Eles ja devem ter data-i18n, mas vamos garantir
    divs = [
        ('<div class="price" data-i18n="price_express">R$ 8</div>', 'price_express'),
        ('<div class="price" data-i18n="price_completo">R$ 17</div>', 'price_completo'),
        ('<div class="price" data-i18n="price_urna">R$ 26</div>', 'price_urna'),
        ('<div class="price" data-i18n="price_eleitoral">R$ 26</div>', 'price_eleitoral'),
    ]
    
    for div_esperado, chave in divs:
        if div_esperado not in html:
            # Tenta encontrar o div sem data-i18n e adicionar
            div_sem = div_esperado.replace(f' data-i18n="{chave}"', "")
            if div_sem in html:
                html = html.replace(div_sem, div_esperado, 1)
                print(f"  Div .price com {chave} corrigido.")
    
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(html)
    
    print("\nPRONTO! Alinhamento corrigido. Faca commit e deploy no Render.")

</body>
</html>

if __name__ == "__main__":
    caminho = sys.argv[1] if len(sys.argv) > 1 else "index.html"
    print(f"Corrigindo alinhamento em: {caminho}\n")
    corrigir(caminho)
