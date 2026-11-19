# -*- coding: utf-8 -*-
"""A1ELOS — Energia de nomes e sugestão por energia alvo."""
import unicodedata

LETRA_VALOR = {'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'H':8,'I':9,
               'J':1,'K':2,'L':3,'M':4,'N':5,'O':6,'P':7,'Q':8,'R':9,
               'S':1,'T':2,'U':3,'V':4,'W':5,'X':6,'Y':7,'Z':8}
ESPECIAIS = {'Æ':'AE','Œ':'OE','Ø':'O','Đ':'D','Ł':'L','Þ':'TH','Ð':'D','Ħ':'H','Ŧ':'T','Ŋ':'N'}

def normalizar(txt):
    s = str(txt or '').upper()
    for k, v in ESPECIAIS.items():
        s = s.replace(k, v)
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return ''.join(c for c in s if 'A' <= c <= 'Z')

def reduzir(n):
    while n > 9 and n not in (11, 22):
        n = sum(int(d) for d in str(n))
    return n

def energia_nome(nome):
    """Retorna (energia 1-9, soma bruta)."""
    limpo = normalizar(nome)
    soma = sum(LETRA_VALOR.get(c, 0) for c in limpo)
    return (reduzir(soma), soma) if limpo else (0, 0)

# Banco de nomes por tipo e idioma. NÃO pré-classificado: a energia é
# calculada em tempo de execução, então nunca fica inconsistente.
BANCO = {
    'pt': {
        'cao':     ['Thor','Luna','Bela','Rex','Pipoca','Amora','Titan','Kira','Zen','Íris','Nina','Bolt','Zoe','Apolo','Alma','Max','Estrela','Fumaça','Duna','Pandora'],
        'gato':    ['Mimi','Loki','Nala','Simba','Frida','Tom','Mel','Sombra','Perola','Atena','Jade','Brisa','Cacau','Nino','Tigre'],
        'passaro': ['Kiwi','Piu','Azul','Cacau','Liro','Nino','Pingo','Zeca','Alfa','Juju'],
        'reptil':  ['Draco','Naga','Kaa','Shen','Rex','Zara','Viper','Tuga'],
        'outro':   ['Aurora','Nova','Atlas','Lumi','Sage','Onix','Vega','Aria']
    },
    'en': {
        'cao':     ['Thor','Luna','Bella','Rex','Poppy','Amber','Titan','Kira','Zen','Iris','Nina','Bolt','Zoe','Apollo','Alma','Max','Star','Smoky','Dune','Pandora'],
        'gato':    ['Mimi','Loki','Nala','Simba','Frida','Tom','Honey','Shadow','Pearl','Athena','Jade','Breeze','Cocoa','Nino','Tiger'],
        'passaro': ['Kiwi','Peep','Blue','Cocoa','Lyro','Nino','Pingo','Zack','Alpha','Juju'],
        'reptil':  ['Draco','Naga','Kaa','Shen','Rex','Zara','Viper','Tuga'],
        'outro':   ['Aurora','Nova','Atlas','Lumi','Sage','Onyx','Vega','Aria']
    },
    # es, it, fr, de, ja, zh, ru, id, tr, vi, he, ar: use o mesmo padrão.
    # Se o idioma não estiver aqui, cai em 'pt' automaticamente.
}

def sugerir_nome(tipo, energia, lang='pt', usados=None):
    alvo = int(energia) if str(energia).isdigit() else 0
    if not alvo:
        return None
    usados_up = {normalizar(u) for u in (usados or [])}
    b_lang = BANCO.get(lang) or BANCO.get('pt') or {}
    b_tipo = b_lang.get(tipo) or b_lang.get('outro') or []
    # 1) banco do idioma
    for nome in b_tipo:
        if normalizar(nome) in usados_up:
            continue
        if energia_nome(nome)[0] == alvo:
            return nome
    # 2) banco pt como reserva
    for nome in (BANCO.get('pt', {}).get(tipo) or BANCO['pt']['outro']):
        if normalizar(nome) in usados_up:
            continue
        if energia_nome(nome)[0] == alvo:
            return nome
    # 3) fallback determinístico: ajusta a base até bater a energia
    base = normalizar(b_tipo[0] if b_tipo else 'A1ELOS')
    for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        for cand in (base + c, c + base):
            if energia_nome(cand)[0] == alvo:
                return cand.capitalize()
    return None

def avaliar_nomes(nomes, tipo, energia_alvo, lang='pt'):
    """
    3 nomes informados → 3 avaliações.
    Se nenhum atingir a energia, gera 1 sugestão = 4ª opção.
    """
    alvo = int(energia_alvo) if str(energia_alvo).isdigit() else 0
    entradas = []
    for n in nomes:
        n = (n or '').strip()
        if not n:
            continue
        e, soma = energia_nome(n)
        entradas.append({'nome': n, 'energia': e, 'soma': soma, 'bate': (e == alvo)})

    escolhido = next((x['nome'] for x in entradas if x['bate']), None)
    sugestao = None
    if not escolhido and alvo:
        sugestao = sugerir_nome(tipo, alvo, lang, [x['nome'] for x in entradas])

    return {
        'energia_alvo': alvo,
        'tipo': tipo,
        'entradas': entradas,

      if __name__ == "__main__":
    for lang in BANCO:
        for tipo in BANCO[lang]:
            grupos = {}
            for n in BANCO[lang][tipo]:
                grupos.setdefault(energia_nome(n)[0], []).append(n)
            faltam = [e for e in range(1, 10) if e not in grupos]
            print(lang, tipo, '-> energias:', sorted(grupos), '| faltam:', faltam)
        'escolhido': escolhido or sugestao or (entradas[0]['nome'] if entradas else None),
        'sugestao': sugestao,
        'total_opcoes': len(entradas) + (1 if sugestao else 0)
    }
