"""
Script de correção de moedas no index.html
Uso: python corrigir_moedas.py index.html
Substitui apenas os símbolos de moeda nos botões btn_buy e btn_buy17
dentro do objeto DEF, sem alterar a contagem de | (pipes).
"""

SUBSTITUICOES = [
    ("es", "Comprar $8", "Comprar 8€", "Comprar $17", "Comprar 17€"),
    ("ja", "8€で購入", "¥800で購入", "17€で購入", "¥1,700で購入"),
    ("zh", "购买8€", "购买¥8", "购买17€", "购买¥17"),
    ("ru", "Купить 8€", "Купить ₽800", "Купить 17€", "Купить ₽1,700"),
    ("hi", "8€ खरीदें", "₹800 खरीदें", "17€ खरीदें", "₹1,700 खरीदें"),
    ("he", "קנה 8€", "קנה ₪30", "קנה 17€", "קנה ₪65"),
    ("ar", "اشترِ 8€", "اشترِ د.إ30", "اشترِ 17€", "اشترِ د.إ65"),
]

def corrigir(caminho):
    with open(caminho, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    total = 0
    for lang, antes8, depois8, antes17, depois17 in SUBSTITUICOES:
        if antes8 in conteudo and antes17 in conteudo:
            conteudo = conteudo.replace(antes17, depois17)
            conteudo = conteudo.replace(antes8, depois8)
            total += 1
            print(f"  ✅ {lang}: OK")
        else:
            print(f"  ⚠️  {lang}: texto não encontrado!")
    
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    
    print(f"\n📋 {total} de {len(SUBSTITUICOES)} idiomas corrigidos.")

if __name__ == "__main__":
    import sys
    caminho = sys.argv[1] if len(sys.argv) > 1 else "index.html"
    print(f"🔧 Corrigindo: {caminho}\n")
    corrigir(caminho)
    print("\n✅ Pronto! Faça commit e deploy no Render.")
