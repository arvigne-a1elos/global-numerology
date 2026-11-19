# -*- coding: utf-8 -*-
"""A1ELOS - energia de nomes e sugestao por energia alvo (v2)."""
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


def _dig(n):
    """Reduz QUALQUER numero a 1-9 (inclui 11 e 22). Use para casar com o seletor."""
    n = abs(int(n))
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n


def reduzir(n):
    """Reduz preservando 11 e 22 (convencao numerologica)."""
    while n > 9 and n not in (11, 22):
        n = sum(int(d) for d in str(n))
    return n


def energia_nome(nome):
    """(energia 1-9, soma bruta). A energia sempre cai em 1-9."""
    limpo = normalizar(nome)
    if not limpo:
        return (0, 0)
    soma = sum(LETRA.get(c, 0) for c in limpo)
    return (_dig(reduzir(soma)), soma)


# Banco curado: 9 energias por tipo, em cada idioma.
# Toda energia 1-9 tem um nome real. Verificado com energia_nome().
CURADO = {
 "pt": {
  "cao":     {1:"Zoe",2:"Rex",3:"Luna",4:"Duna",5:"Apolo",6:"Pipoca",7:"Thor",8:"Simba",9:"Alma"},
  "gato":    {1:"Nala",2:"Loki",3:"Tom",4:"Perola",5:"Sombra",6:"Azul",7:"Nino",8:"Mimi",9:"Bidu"},
  "passaro": {1:"Piu",2:"Cacau",3:"Mel",4:"Blue",5:"Nico",6:"Loro",7:"Kiwi",8:"Zeca",9:"Liro"},
  "reptil":  {1:"Shen",2:"Rex",3:"Cobra",4:"Kaa",5:"Draco",6:"Spike",7:"Viper",8:"Onix",9:"Nagini"},
  "outro":   {1:"Lumi",2:"Aurora",3:"Kira",4:"Duna",5:"Sage",6:"Pipoca",7:"Nova",8:"Atlas",9:"Alma"},
 },
 "en": {
  "cao":     {1:"Zoe",2:"Rex",3:"Luna",4:"Bolt",5:"Duke",6:"Ginger",7:"Thor",8:"Zeus",9:"Coco"},
  "gato":    {1:"Nala",2:"Loki",3:"Tom",4:"Maya",5:"Misty",6:"Ginger",7:"Nino",8:"Mimi",9:"Coco"},
  "passaro": {1:"Sky",2:"Tico",3:"Sunny",4:"Blue",5:"Nico",6:"Loro",7:"Kiwi",8:"Juju",9:"Liro"},
  "reptil":  {1:"Shen",2:"Rex",3:"Cobra",4:"Kaa",5:"Draco",6:"Spike",7:"Viper",8:"Atlas",9:"Nagini"},
  "outro":   {1:"Lumi",2:"Aurora",3:"Kira",4:"Maya",5:"Sage",6:"Ginger",7:"Nova",8:"Atlas",9:"Alma"},
 },
 "es": {
  "cao":     {1:"Zoe",2:"Rex",3:"Luna",4:"Duna",5:"Apolo",6:"Pipoca",7:"Thor",8:"Simba",9:"Alma"},
  "gato":    {1:"Nala",2:"Loki",3:"Tom",4:"Maya",5:"Sombra",6:"Azul",7:"Nino",8:"Mimi",9:"Coco"},
  "passaro": {1:"Sol",2:"Tico",3:"Mel",4:"Blue",5:"Nico",6:"Loro",7:"Kiwi",8:"Juju",9:"Liro"},
  "reptil":  {1:"Shen",2:"Rex",3:"Cobra",4:"Kaa",5:"Draco",6:"Spike",7:"Viper",8:"Atlas",9:"Nagini"},
  "outro":   {1:"Lumi",2:"Aurora",3:"Kira",4:"Maya",5:"Sage",6:"Azul",7:"Nova",8:"Atlas",9:"Alma"},
 },
}

# Ordem de reserva: se o idioma pedido nao tiver o tipo, tenta estes.
# NUNCA troca o tipo (cao continua cao).
RESERVA = ["en", "es", "pt"]


def sugerir_nome(tipo, energia, lang="pt", usados=None):
    """Sugere 1 nome do MESMO tipo, com a energia exata. Nunca inventa."""
    alvo = int(energia) if str(energia).isdigit() else 0
    if alvo < 1 or alvo > 9:
        return None
    alvo = _dig(alvo)
    usados = set(normalizar(u) for u in (usados or []))

    tentativas = [lang] + [l for l in RESERVA if l != lang]
    for l in tentativas:
        grupo = (CURADO.get(l) or {}).get(tipo) or {}
        nome = grupo.get(alvo)
        if nome and normalizar(nome) not in usados:
            return {"nome": nome, "idioma": l}
    # tipo desconhecido: usa 'outro' do proprio idioma
    for l in tentativas:
        grupo = (CURADO.get(l) or {}).get("outro") or {}
        nome = grupo.get(alvo)
        if nome and normalizar(nome) not in usados:
            return {"nome": nome, "idioma": l}
    return None


def avaliar_nomes(nomes, tipo, energia_alvo, lang="pt"):
    """
    3 nomes informados -> 3 avaliacoes.
    Se nenhum atingir a energia, gera 1 sugestao do mesmo tipo = 4a opcao.
    """
    alvo = int(energia_alvo) if str(energia_alvo).isdigit() else 0
    alvo = _dig(alvo) if alvo else 0

    entradas = []
    for n in (nomes or []):
        n = (n or "").strip()
        if not n:
            continue
        e, soma = energia_nome(n)
        entradas.append({"nome": n, "energia": e, "soma": soma, "bate": (alvo > 0 and e == alvo)})

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
        "total_opcoes": len(entradas) + (1 if sug else 0),
    }
