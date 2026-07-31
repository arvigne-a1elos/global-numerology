"""
Script de correção de moedas nos CARDS DE PRODUTO (.price)
Uso: python corrigir_moedas.py index.html

O QUE ELE FAZ (e SOMENTE isso):
1. Injeta uma função JS 'updatePrices()' no index.html
2. Faz a função applyLang() chamar updatePrices() a cada troca de idioma
3. updatePrices() troca o texto dos 4 divs .price pela moeda do idioma ativo

NAO mexe em: botões, KEYS, DEF, traduções, data-i18n dos preços.
Os <div class="price"> continuam SEM data-i18n (por isso não somem).
Se precisar ajustar algum valor, edite o dicionario PRECOS abaixo e rode de novo.
"""

PRECOS = {
    "pt": ["R$ 8",   "R$ 17",   "R$ 26",    "R$ 26"],
    "en": ["$8",     "$17",     "$26",      "$26"],
    "es": ["8€",     "17€",     "26€",      "26€"],
    "fr": ["8€",     "17€",     "26€",      "26€"],
    "de": ["8€",     "17€",     "26€",      "26€"],
    "it": ["8€",     "17€",     "26€",      "26€"],
    "ja": ["¥800",   "¥1,700",  "¥2,600",   "¥2,600"],
    "zh": ["¥8",     "¥17",     "¥26",      "¥26"],
    "ru": ["₽800",   "₽1,700",  "₽2,600",   "₽2,600"],
    "hi": ["₹800",   "₹1,700",  "₹2,600",   "₹2,600"],
    "he": ["₪30",    "₪65",     "₪100",     "₪100"],
    "ar": ["د.إ30",  "د.إ65",   "د.إ100",   "د.إ100"],
}

def gerar_js_update():
    linhas = ["function updatePrices(){",
              "var l=localStorage.getItem('a1elos-lang')||'pt';",
              "var m={"]
    for lang, vals in PRECOS.items():
        arr = ",".join("'" + v.replace("'", "\'") + "'" for v in vals)
        linhas.append(f"{lang}:[{arr}],")
    linhas += ["};",
               "var ps=document.querySelectorAll('.price');",
               "(m[l]||m.pt).forEach(function(v,i){if(ps[i])ps[i].textContent=v;});",
               "}"]
    return "\n".join(linhas)

def corrigir(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        html = f.read()

    if "function updatePrices" in html:
        print("updatePrices() ja existe — nada foi alterado (rodar de novo e seguro).")
        return

    # 1) Injeta a funcao updatePrices antes de applyLang()
    marcador = "function applyLang(){"
    if marcador not in html:
        print("ERRO: nao encontrei 'function applyLang()' no arquivo.")
        return
    html = html.replace(marcador, gerar_js_update() + "\n" + marcador, 1)

    # 2) Faz applyLang() chamar updatePrices()
    alvo = "el.textContent=t(el.dataset.i18n)});"
    if alvo not in html:
        print("ERRO: nao encontrei o loop de data-i18n dentro de applyLang().")
        return
    html = html.replace(alvo, alvo + "\n  updatePrices();", 1)

    with open(caminho, "w", encoding="utf-8") as f:
        f.write(html)

    print("OK! updatePrices() injetado e chamado em applyLang().")
    print("Faça commit e deploy no Render.")

if __name__ == "__main__":
    import sys
    caminho = sys.argv[1] if len(sys.argv) > 1 else "index.html"
    corrigir(caminho)
