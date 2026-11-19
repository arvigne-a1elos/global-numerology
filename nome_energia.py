# -*- coding: utf-8 -*-
"""A1ELOS - energia de nomes, romanizacao e sugestao por energia alvo (v3).
Regra: nomes em escrita latina em TODOS os idiomas (numerologia pitagorica
so atribui valor a A-Z). O banco e construido e verificado no import.
"""
import unicodedata

LETRA = {c: (i % 9) + 1 for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ")}
ESP = {"\u00c6": "AE", "\u0152": "OE", "\u00d8": "O", "\u0110": "D",
       "\u0141": "L", "\u00de": "TH", "\u00d0": "D", "\u0126": "H",
       "\u0166": "T", "\u014a": "N"}


def normalizar(t):
    s = str(t or "").upper()
    for k, v in ESP.items():
        s = s.replace(k, v)
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return "".join(c for c in s if "A" <= c <= "Z")


def precisa_romanizar(t):
    """True quando o texto tem letras nao-latinas (energia seria 0)."""
    s = str(t or "")
    tem_letra = any(c.isalpha() for c in s)
    if not tem_letra:
        return False
    return len(normalizar(s)) == 0


def _dig(n):
    n = abs(int(n))
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n


def reduzir(n):
    while n > 9 and n not in (11, 22):
        n = sum(int(d) for d in str(n))
    return n


def energia_nome(nome):
    """(energia 1-9, soma bruta). Sempre 1-9; 0 se nao houver letras."""
    limpo = normalizar(nome)
    if not limpo:
        return (0, 0)
    soma = sum(LETRA.get(c, 0) for c in limpo)
    return (_dig(reduzir(soma)), soma)


# Sementes reais, em escrita latina, por idioma e tipo.
SEEDS = {
 "pt": {"cao":["Thor","Luna","Bela","Rex","Kira","Nina","Max","Zoe","Alma","Duna"],
        "gato":["Mimi","Loki","Nala","Simba","Frida","Tom","Sombra","Jade","Nino"],
        "passaro":["Kiwi","Piu","Azul","Loro","Pingo","Zeca","Juju","Nico"],
        "reptil":["Draco","Naga","Kaa","Shen","Viper","Zara","Tuga","Onix"],
        "outro":["Aurora","Nova","Atlas","Lumi","Sage","Vega","Aria","Iris"]},
 "en": {"cao":["Thor","Luna","Bella","Rex","Kira","Nina","Max","Zoe","Amber","Dune"],
        "gato":["Mimi","Loki","Nala","Simba","Frida","Tom","Shadow","Jade","Nino"],
        "passaro":["Kiwi","Peep","Blue","Loro","Pingo","Zack","Juju","Nico"],
        "reptil":["Draco","Naga","Kaa","Shen","Viper","Zara","Tuga","Onyx"],
        "outro":["Aurora","Nova","Atlas","Lumi","Sage","Vega","Aria","Iris"]},
 "es": {"cao":["Thor","Luna","Bela","Rex","Kira","Nina","Max","Zoe","Alma","Duna"],
        "gato":["Mimi","Loki","Nala","Simba","Frida","Tom","Sombra","Jade","Nino"],
        "passaro":["Kiwi","Pio","Azul","Loro","Pingo","Zeca","Juju","Nico"],
        "reptil":["Draco","Naga","Kaa","Shen","Viper","Zara","Tuga","Onix"],
        "outro":["Aurora","Nova","Atlas","Lumi","Sage","Vega","Aria","Iris"]},
 "it": {"cao":["Thor","Luna","Bella","Rex","Kira","Nina","Max","Zoe","Alma","Duna"],
        "gato":["Mimi","Loki","Nala","Simba","Frida","Tom","Ombra","Jade","Nino"],
        "passaro":["Kiwi","Pio","Azzurro","Loro","Pingo","Zeca","Juju","Nico"],
        "reptil":["Draco","Naga","Kaa","Shen","Viper","Zara","Tuga","Onice"],
        "outro":["Aurora","Nova","Atlas","Lumi","Sage","Vega","Aria","Iris"]},
 "fr": {"cao":["Thor","Luna","Belle","Rex","Kira","Nina","Max","Zoe","Alma","Dune"],
        "gato":["Mimi","Loki","Nala","Simba","Frida","Tom","Ombre","Jade","Nino"],
        "passaro":["Kiwi","Piou","Bleu","Loro","Pingo","Zack","Juju","Nico"],
        "reptil":["Draco","Naga","Kaa","Shen","Vipre","Zara","Tuga","Onyx"],
        "outro":["Aurore","Nova","Atlas","Lumi","Sage","Vega","Aria","Iris"]},
 "de": {"cao":["Thor","Luna","Bella","Rex","Kira","Nina","Max","Zoe","Alma","Dune"],
        "gato":["Mimi","Loki","Nala","Simba","Frida","Tom","Schatten","Jade","Nino"],
        "passaro":["Kiwi","Piep","Blau","Loro","Pingo","Zack","Juju","Nico"],
        "reptil":["Draco","Naga","Kaa","Shen","Viper","Zara","Tuga","Onyx"],
        "outro":["Aurora","Nova","Atlas","Lumi","Sage","Vega","Aria","Iris"]},
 "ja": {"cao":["Hana","Yuki","Sora","Haru","Riku","Mei","Aoi","Kaito","Momo","Taro"],
        "gato":["Mio","Kuro","Shiro","Neko","Yuki","Haru","Rin","Sora","Tama"],
        "passaro":["Piyo","Sora","Tori","Hana","Kii","Rin","Momo","Kaze"],
        "reptil":["Ryu","Kage","Hebi","Tatsu","Zara","Kira","Oni","Sora"],
        "outro":["Hikari","Nozomi","Kaede","Rin","Akira","Yui","Sakura","Kaze"]},
 "zh": {"cao":["Mei","Lan","Xin","Yu","Hao","Lin","Wen","Jun","Bao","Dou"],
        "gato":["Mi","Mao","Hei","Bai","Xiao","Lin","Yu","Xin","Hua"],
        "passaro":["Niao","Fei","Yu","Lan","Xin","Mei","Yun","He"],
        "reptil":["Long","She","Hu","Bao","Lin","Xin","Yu","Shan"],
        "outro":["Ming","Hua","Yun","Lan","Xin","Tao","Mei","Jun"]},
 "ru": {"cao":["Ivan","Anna","Misha","Natasha","Sasha","Boris","Lena","Yuri","Dasha"],
        "gato":["Murka","Vasya","Barsik","Masha","Pushok","Timka","Sonya","Ryzhik"],
        "passaro":["Ptichka","Kesha","Gavryusha","Chizhik","Sinichka","Ptakha","Klyuv"],
        "reptil":["Zmey","Gorynych","Drako","Kaa","Vip","Zara","Tuga","Oniks"],
        "outro":["Sveta","Vera","Nadezhda","Lada","Mir","Zarya","Iskra","Volya"]},
 "id": {"cao":["Thor","Luna","Bela","Rex","Kira","Nina","Max","Zoe","Bulan","Bintang"],
        "gato":["Mimi","Loki","Nala","Simba","Frida","Tom","Bayang","Jade","Nino"],
        "passaro":["Kiwi","Cicit","Biru","Loro","Pingo","Zeca","Juju","Nico"],
        "reptil":["Draco","Naga","Kaa","Shen","Viper","Zara","Tuga","Oniks"],
        "outro":["Aurora","Nova","Atlas","Lumi","Sage","Vega","Aria","Iris"]},
 "tr": {"cao":["Thor","Luna","Bela","Rex","Kira","Nina","Max","Zoe","Can","Duman"],
        "gato":["Mimi","Loki","Nala","Simba","Frida","Tom","Golge","Jade","Nino"],
        "passaro":["Kiwi","Cik","Mavi","Loro","Pingo","Zeca","Juju","Nico"],
        "reptil":["Draco","Naga","Kaa","Shen","Viper","Zara","Tuga","Oniks"],
        "outro":["Aurora","Nova","Atlas","Lumi","Sage","Vega","Aria","Iris"]},
 "vi": {"cao":["Thor","Luna","Bela","Rex","Kira","Nina","Max","Zoe","Mai","Sao"],
        "gato":["Mimi","Loki","Nala","Simba","Frida","Tom","Bong","Jade","Nino"],
        "passaro":["Kiwi","Chim","Xanh","Loro","Pingo","Zeca","Juju","Nico"],
        "reptil":["Draco","Naga","Kaa","Shen","Viper","Zara","Tuga","Oniks"],
        "outro":["Aurora","Nova","Atlas","Lumi","Sage","Vega","Aria","Iris"]},
 "he": {"cao":["Noa","Ariel","Tamar","Yosef","David","Maya","Eitan","Shira","Lavi","Dov"],
        "gato":["Mika","Lulu","Nuni","Simba","Keti","Bougi","Zohar","Riki"],
        "passaro":["Tzipor","Ofi","Nuri","Tzippi","Peri","Kanarit","Dror"],
        "reptil":["Tanin","Nahash","Draco","Kaa","Viper","Zara","Tuga","Oniks"],
        "outro":["Or","Shai","Roni","Gal","Tal","Noam","Aviv","Maayan"]},
 "ar": {"cao":["Layla","Omar","Amir","Nour","Yasmin","Karim","Salma","Zayn","Fares"],
        "gato":["Mimi","Loki","Nala","Simba","Frida","Tom","Qamar","Jade","Nino"],
        "passaro":["Asfur","Nour","Sama","Loro","Pingo","Zeca","Juju","Nico"],
        "reptil":["Tinnin","Afaa","Draco","Kaa","Viper","Zara","Tuga","Oniks"],
        "outro":["Nur","Sama","Amal","Huda","Rami","Lina","Dina","Farah"]},
}

# Sufixos naturais usados SO para preencher energia faltante.
SUFIXOS = ["", "a", "o", "i", "e", "ia", "io", "el", "ar", "in", "on", "is", "us"]


def _construir():
    tab = {}
    for lang, tipos in SEEDS.items():
        tab[lang] = {}
        for tipo, nomes in tipos.items():
            mapa = {}
            for n in nomes:                              # 1) nomes reais
                e = energia_nome(n)[0]
                if e and e not in mapa:
                    mapa[e] = {"nome": n, "real": True}
            for n in nomes:                              # 2) variantes
                for s in SUFIXOS[1:]:
                    c = n + s
                    e = energia_nome(c)[0]
                    if e and e not in mapa:
                        mapa[e] = {"nome": c, "real": False}
            tab[lang][tipo] = mapa
    return tab


CURADO = _construir()
RESERVA = ["en", "es", "pt"]


def sugerir_nome(tipo, energia, lang="pt", usados=None):
    alvo = int(energia) if str(energia).isdigit() else 0
    if not alvo:
        return None
    alvo = _dig(alvo)
    usados = set(normalizar(u) for u in (usados or []))

    for l in [lang] + [x for x in RESERVA if x != lang]:
        grupo = (CURADO.get(l) or {}).get(tipo) or {}
        item = grupo.get(alvo)
        if item and normalizar(item["nome"]) not in usados:
            return {"nome": item["nome"], "idioma": l, "real": item["real"]}
    for l in [lang] + [x for x in RESERVA if x != lang]:
        grupo = (CURADO.get(l) or {}).get("outro") or {}
        item = grupo.get(alvo)
        if item and normalizar(item["nome"]) not in usados:
            return {"nome": item["nome"], "idioma": l, "real": item["real"]}
    return None


def avaliar_nomes(nomes, tipo, energia_alvo, lang="pt"):
    alvo = int(energia_alvo) if str(energia_alvo).isdigit() else 0
    alvo = _dig(alvo) if alvo else 0

    entradas = []
    for n in (nomes or []):
        n = (n or "").strip()
        if not n:
            continue
        e, soma = energia_nome(n)
        entradas.append({"nome": n, "energia": e, "soma": soma,
                         "bate": (alvo > 0 and e == alvo),
                         "romanizar": precisa_romanizar(n)})

    escolhido = None
    for x in entradas:
        if x["bate"]:
            escolhido = x["nome"]
            break

    sug = None
    if not escolhido and alvo:
        sug = sugerir_nome(tipo, alvo, lang, [x["nome"] for x in entradas])

    return {
        "energia_alvo": alvo,
        "tipo": tipo,
        "idioma": lang,
        "entradas": entradas,
        "escolhido": escolhido or (sug["nome"] if sug else None) or (entradas[0]["nome"] if entradas else None),
        "sugestao": sug["nome"] if sug else None,
        "sugestao_idioma": sug["idioma"] if sug else None,
        "sugestao_real": sug["real"] if sug else None,
        "total_opcoes": len(entradas) + (1 if sug else 0),
    }
