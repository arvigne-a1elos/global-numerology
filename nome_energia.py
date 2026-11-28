# -*- coding: utf-8 -*-
"""A1ELOS - energia de nomes, romanizacao e sugestao por energia alvo (v3).
Regra: nomes em escrita latina em TODOS os idiomas (numerologia pitagorica
so atribui valor a A-Z). O banco e construido e verificado no import.
"""
import unicodedata

CURADO = _construir()
_faltando = [(l, t, e) for l in SEEDS for t in SEEDS[l]
             for e in range(1, 10)
             if e not in ((CURADO.get(l) or {}).get(t) or {})]
if _faltando:
    import logging
    logging.getLogger(__name__).warning(
        "nome_energia: %d combinacoes idioma/tipo/energia sem nome curado", len(_faltando))

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

# Nomes reais que completam as energias ausentes nas sementes.
# Aplicados sobre os SEEDS antes de gerar variantes.
EXTRA = {
 "pt": {
   "cao":     {5:"Duque", 6:"Pandora", 8:"Estrela"},
   "gato":    {4:"Amora", 6:"Pipoca", 9:"Zara"},
   "passaro": {2:"Tico", 3:"Mel", 4:"Lira", 5:"Kiara"},
   "reptil":  {3:"Naga", 6:"Tanin", 8:"Zeca", 9:"Draco"},
   "outro":   {3:"Amora", 4:"Lira", 6:"Pandora", 9:"Zara"},
 },
 "en": {
   "cao":     {5:"Duke", 6:"Pandora", 8:"Toby"},
   "gato":    {4:"Amber", 6:"Pippa", 9:"Zara"},
   "passaro": {2:"Tico", 3:"Sunny", 4:"Lira", 5:"Kiara"},
   "reptil":  {3:"Naga", 6:"Tanin", 8:"Zack", 9:"Draco"},
   "outro":   {3:"Amber", 4:"Lira", 6:"Pippa", 9:"Zara"},
 },
 "es": {
   "cao":     {5:"Duque", 6:"Pandora", 8:"Estrella"},
   "gato":    {4:"Amora", 6:"Pipoca", 9:"Zara"},
   "passaro": {2:"Tico", 3:"Mel", 4:"Lira", 5:"Kiara"},
   "reptil":  {3:"Naga", 6:"Tanin", 8:"Zeca", 9:"Draco"},
   "outro":   {3:"Amora", 4:"Lira", 6:"Pandora", 9:"Zara"},
 },
}

# Sufixos naturais usados SO para preencher energia faltante.
SUFIXOS = ["", "a", "o", "i", "e", "ia", "io", "el", "ar", "in", "on", "is", "us"]


# ===== v4: SEXO DO ANIMAL / DO NOME =====
# Banco curado com os 9 numeros para cada sexo. Nomes reais, verificados.
BANCO_SEXO = {
 "pt": {
  "cao": {
   "f": {1:"Zoe",2:"Bela",3:"Luna",4:"Duna",5:"Sombra",6:"Pandora",7:"Meg",8:"Estrela",9:"Alma"},
   "m": {1:"Kiko",2:"Rex",3:"Tom",4:"Bolt",5:"Duque",6:"Kid",7:"Thor",8:"Simba",9:"Ciro"}},
  "gato": {
   "f": {1:"Nala",2:"Frida",3:"Luna",4:"Lia",5:"Sombra",6:"Pandora",7:"Meg",8:"Mimi",9:"Alma"},
   "m": {1:"Kiko",2:"Loki",3:"Tom",4:"Xerife",5:"Tigre",6:"Kid",7:"Nino",8:"Simba",9:"Guto"}},
  "passaro": {
   "f": {1:"Piu",2:"Nina",3:"Mel",4:"Lira",5:"Kika",6:"Pipoca",7:"Kiwi",8:"Estrela",9:"Alma"},
   "m": {1:"Kiko",2:"Tico",3:"Kai",4:"Robin",5:"Nico",6:"Loro",7:"Pingo",8:"Zeca",9:"Liro"}},
  "reptil": {
   "f": {1:"Shen",2:"Bela",3:"Cobra",4:"Kaa",5:"Naga",6:"Pandora",7:"Viper",8:"Onix",9:"Nagini"},
   "m": {1:"Kiko",2:"Rex",3:"Kai",4:"Tuga",5:"Draco",6:"Kid",7:"Pingo",8:"Zeca",9:"Liro"}},
  "outro": {
   "f": {1:"Lumi",2:"Aurora",3:"Kira",4:"Duna",5:"Sombra",6:"Pandora",7:"Meg",8:"Estrela",9:"Alma"},
   "m": {1:"Kiko",2:"Rex",3:"Tom",4:"Bolt",5:"Duque",6:"Kid",7:"Thor",8:"Simba",9:"Ciro"}},
 },
 "en": {
  "cao": {
   "f": {1:"Zoe",2:"Nina",3:"Luna",4:"Daisy",5:"Bella",6:"Pandora",7:"Meg",8:"Mimi",9:"Alma"},
   "m": {1:"Arlo",2:"Rex",3:"Tom",4:"Bolt",5:"Duke",6:"Kid",7:"Thor",8:"Simba",9:"Ciro"}},
  "gato": {
   "f": {1:"Nala",2:"Nina",3:"Luna",4:"Daisy",5:"Bella",6:"Pandora",7:"Meg",8:"Mimi",9:"Alma"},
   "m": {1:"Arlo",2:"Loki",3:"Tom",4:"Bolt",5:"Tiger",6:"Kid",7:"Nino",8:"Simba",9:"Guto"}},
  "passaro": {
   "f": {1:"Piu",2:"Nina",3:"Mel",4:"Lira",5:"Kika",6:"Pipoca",7:"Kiwi",8:"Stella",9:"Alma"},
   "m": {1:"Kiko",2:"Tico",3:"Kai",4:"Robin",5:"Nico",6:"Loro",7:"Pingo",8:"Zack",9:"Liro"}},
  "reptil": {
   "f": {1:"Shen",2:"Bella",3:"Cobra",4:"Kaa",5:"Naga",6:"Pandora",7:"Viper",8:"Onyx",9:"Nagini"},
   "m": {1:"Kiko",2:"Rex",3:"Kai",4:"Tuga",5:"Draco",6:"Kid",7:"Pingo",8:"Zack",9:"Liro"}},
  "outro": {
   "f": {1:"Lumi",2:"Aurora",3:"Kira",4:"Daisy",5:"Bella",6:"Pandora",7:"Meg",8:"Stella",9:"Alma"},
   "m": {1:"Kiko",2:"Rex",3:"Tom",4:"Bolt",5:"Duke",6:"Kid",7:"Thor",8:"Simba",9:"Ciro"}},
 },
}

FEMININOS = set("""ZOE LUNA BELA BELLA KIRA NINA ALMA DUNA PANDORA ESTRELA STELLA AMORA IRIS MIMI NALA
FRIDA SOMBRA JADE ZARA MEL HANA YUKI MIO KURO SHIRO NEKO RIN TAMA MEI LAN XIN YU LIN WEN HUA MI
MAO HEI BAI XIAO ANNA NATASHA LENA DASHA MURKA MASHA SONYA BOUGI RIKI NOA TAMAR MAYA SHIRA LAYLA
YASMIN SALMA BELLE OMRA BAYANG BULAN BINTANG SAKURA MOMO PIPOCA GINGER MISTY POPPY AMBER DAISY
LIA MEG KIKA LIRA PIU COCO NECA TITA BINA DORA PEROLA CACAU LILI TZIPOR OFI NURI TZIPPI PERI
KANARIT DROR HIKARI NOZOMI KAEDE AKIRA YUI SVETA VERA NADEZHDA LADA ZARYA ISKRA VOLYA AMAL HUDA
LINA DINA FARAH NUR SAMA AVIV MAYAAN SHIRA""".split())

MASCULINOS = set("""THOR REX MAX DUQUE DUKE ARLO BOLT SIMBA ZEUS TITA PINGO LOKI TOM NINO KIKO DRACO NAGA
KAA SHEN VIPER TUGA ONIX ONYX IVAN MISHA SASHA BORIS YURI VASYA BARSIK PUSHOK TIMKA RYZHIK KESHA
ZACK ZECA LIRO TICO KAITO HARU RIKU SORA AOI TARO AKIRA HAO JUN BAO TORI TATSU ONI LONG SHE
ARIEL YOSEF DAVID EITAN LAVI DOV OMAR AMIR NOUR KARIM ZAYN FARES RAMI ASLAN TIGRE TIGER KID
XERIFE GUTO ROBIN KAI NICO LORO CIRO CAIRO JACK FINN CODY TOBY BUSTER""".split())


def sexo_de(nome):
    """'f', 'm' ou '' (indefinido). Heuristica final: -a feminino, -o masculino."""
    n = normalizar(nome)
    if not n:
        return ""
    if n in FEMININOS:
        return "f"
    if n in MASCULINOS:
        return "m"
    if n.endswith("A"):
        return "f"
    if n.endswith("O"):
        return "m"
    return ""


def _inferir_sexo(nomes):
    """Deduz o sexo a partir dos nomes digitados (maioria)."""
    f = m = 0
    for n in (nomes or []):
        s = sexo_de(n)
        if s == "f":
            f += 1
        elif s == "m":
            m += 1
    if f > m:
        return "f"
    if m > f:
        return "m"
    return ""


def sugerir_nome(tipo, energia, lang="pt", usados=None, sexo=""):
    """Sugere 1 nome do MESMO tipo, com a energia exata e o MESMO sexo."""
    alvo = int(energia) if str(energia).isdigit() else 0
    if not alvo:
        return None
    alvo = _dig(alvo)
    usados = set(normalizar(u) for u in (usados or []))

    ordens_lang = [lang] + [x for x in ("en", "pt") if x != lang]
    ordens_sexo = [sexo] if sexo in ("f", "m") else ["f", "m", ""]

    # 1) banco curado por sexo
    for sx in ordens_sexo:
        for l in ordens_lang:
            g = ((BANCO_SEXO.get(l) or {}).get(tipo) or {}).get(sx or "")
            nome = (g or {}).get(alvo)
            if nome and normalizar(nome) not in usados:
                return {"nome": nome, "idioma": l, "sexo": sx, "real": True}

    # 2) banco antigo (CURADO), filtrado por sexo
    for l in ordens_lang:
        item = ((CURADO.get(l) or {}).get(tipo) or {}).get(alvo)
        if not item:
            continue
        sx_item = sexo_de(item["nome"])
        if sexo in ("f", "m") and sx_item and sx_item != sexo:
            continue
        if normalizar(item["nome"]) not in usados:
            return {"nome": item["nome"], "idioma": l, "sexo": sx_item, "real": item["real"]}

    # 3) variantes com sufixo coerente com o sexo
    SUF_F = ["a", "ia", "ina", "ela", "ana", "ora", "ita"]
    SUF_M = ["o", "el", "on", "us", "io", "ino", "aro"]
    SUF_U = ["a", "o", "el", "in", "is"]
    base_item = ((CURADO.get(lang) or {}).get(tipo) or {}).get(alvo)
    fonte = base_item["nome"] if base_item else ((BANCO_SEXO.get("pt") or {}).get(tipo) or {}).get("f", {}).get(alvo, "A1ELOS")
    suf = SUF_F if sexo == "f" else (SUF_M if sexo == "m" else SUF_U)
    for s in suf:
        cand = fonte + s
        if normalizar(cand) in usados:
            continue
        if energia_nome(cand)[0] == alvo:
            return {"nome": cand, "idioma": lang, "sexo": sexo, "real": False}
    return None


def avaliar_nomes(nomes, tipo, energia_alvo, lang="pt", sexo=""):
    """3 nomes -> 3 avaliacoes; se nenhum bater, 1 sugestao = 4a opcao.
    O sexo e respeitado; se nao vier, e deduzido dos nomes digitados."""
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
                         "sexo": sexo_de(n),
                         "romanizar": precisa_romanizar(n)})

    sx = sexo if sexo in ("f", "m") else _inferir_sexo([x["nome"] for x in entradas])

    escolhido = None
    for x in entradas:
        if x["bate"]:
            escolhido = x["nome"]
            break

    sug = None
    if not escolhido and alvo:
        sug = sugerir_nome(tipo, alvo, lang, [x["nome"] for x in entradas], sx)

    return {
        "energia_alvo": alvo,
        "tipo": tipo,
        "idioma": lang,
        "sexo": sx,
        "sexo_inferido": (sexo not in ("f", "m")),
        "entradas": entradas,
        "escolhido": escolhido or (sug["nome"] if sug else None) or (entradas[0]["nome"] if entradas else None),
        "sugestao": sug["nome"] if sug else None,
        "sugestao_idioma": sug["idioma"] if sug else None,
        "sugestao_real": sug["real"] if sug else None,
        "sugestao_sexo": sug["sexo"] if sug else None,
        "total_opcoes": len(entradas) + (1 if sug else 0),
    }

def _construir():
    tab = {}
    for lang, tipos in SEEDS.items():
        tab[lang] = {}
        ex_lang = EXTRA.get(lang, {})
        for tipo, nomes in tipos.items():
            mapa = {}
            for n in nomes:                              # 1) nomes reais
                e = energia_nome(n)[0]
                if e and e not in mapa:
                    mapa[e] = {"nome": n, "real": True}
            for e, n in (ex_lang.get(tipo) or {}).items():   # 2) EXTRA reais
                if e not in mapa and energia_nome(n)[0] == e:
                    mapa[e] = {"nome": n, "real": True}
            for n in nomes:                              # 3) variantes
                for s in SUFIXOS[1:]:
                    c = n + s
                    e = energia_nome(c)[0]
                    if e and e not in mapa:
                        mapa[e] = {"nome": c, "real": False}
            tab[lang][tipo] = mapa
    return tab

RESERVA = ["en", "es", "pt"]


def _sugerir_nome_antigo(tipo, energia, lang="pt", usados=None):
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


def _avaliar_nomes_antigo(nomes, tipo, energia_alvo, lang="pt"):
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
