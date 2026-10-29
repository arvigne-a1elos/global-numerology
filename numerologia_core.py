# -*- coding: utf-8 -*-
"""
numerologia_core.py — A1ELOS Global Numerology
================================================
Módulo de cálculo e leitura. NÃO renderiza PDF, NÃO escolhe template.
Responsabilidade única: transformar (data_nascimento, ano_ref, mes_ref)
em um dicionário de leitura pronto para o gerador de PDF consumir.

Corrige os bugs:
  #1 — recebe data de nascimento COMPLETA (não o mês escolhido)
  #2 — ano_pessoal = reduzir(ano_geral + caminho_vida)  [sem mês]
  #3 — entrega núcleos editoriais + leitura cruzada (não tabela crua)
"""

from datetime import date

# ============================================================================
# 1. REDUÇÃO
# ============================================================================

def reduzir(n: int) -> int:
    """Reduz a um dígito, preservando os mestres 11 e 22."""
    n = abs(int(n))
    while n > 9 and n not in (11, 22):
        n = sum(int(d) for d in str(n))
    return n


def caminho_vida(dia: int, mes: int, ano: int) -> int:
    """CV = reduzir(dia + mês + ano)."""
    return reduzir(dia + mes + ano)


# ============================================================================
# 2. CÁLCULOS DO PERÍODO
# ============================================================================

def ano_geral(ano: int) -> int:
    return reduzir(ano)


def mes_geral(ano: int, mes: int) -> int:
    return reduzir(ano_geral(ano) + reduzir(mes))


def ano_pessoal(ano: int, cv: int) -> int:
    """ATENÇÃO: NÃO soma o mês. Esta era a origem do bug #2."""
    return reduzir(ano_geral(ano) + cv)


def mes_pessoal(ano: int, mes: int, cv: int) -> int:
    return reduzir(mes_geral(ano, mes) + cv)


def leitura_cruzada(n_geral: int, n_pessoal: int) -> int:
    return reduzir(n_geral + n_pessoal)


# ============================================================================
# 3. MATRIZ DE TOM
# ============================================================================

RACIONAIS  = {1, 4, 7, 8, 11}
EMOCIONAIS = {2, 3, 5, 6, 22}
REFORCADOR = 9


def _tom_individual(n: int) -> str:
    if n in RACIONAIS:
        return "racional"
    if n in EMOCIONAIS:
        return "emocional"
    return "neutro"  # 9


def tom_da_soma(a: int, b: int) -> dict:
    """
    Regras (fixadas pelo A1ELOS):
      - 9 na soma  -> reforça o tom do parceiro
      - 9 + 9      -> integração plena
      - resultado com tom definido prevalece
      - resíduo é sinalizado quando a parcela diverge do resultado
    """
    resultado = reduzir(a + b)
    ta, tb = _tom_individual(a), _tom_individual(b)

    # 9 + 9
    if a == REFORCADOR and b == REFORCADOR:
        return {
            "resultado": 9,
            "tom": "integracao",
            "label": "integração plena — emoção e razão juntas",
            "residuo": None,
        }

    # um dos dois é 9 -> reforça o parceiro
    if a == REFORCADOR or b == REFORCADOR:
        parceiro = b if a == REFORCADOR else a
        tom = _tom_individual(parceiro)
        if tom == "neutro":
            tom = "integracao"
        return {
            "resultado": resultado,
            "tom": f"{tom}_reforcado",
            "label": f"{tom} reforçado pelo nove",
            "residuo": None,
        }

    # tom do resultado prevalece
    tom_res = _tom_individual(resultado)
    if tom_res == "neutro":
        tom_res = "integracao"
        residuo = None
    elif ta == tb:
        residuo = None
    else:
        # parcelas divergentes -> sinaliza o resíduo que iniciou
        residuo = ta if ta != tom_res else tb

    return {
        "resultado": resultado,
        "tom": tom_res,
        "label": f"{tom_res}" + (f" (com resíduo {residuo})" if residuo else ""),
        "residuo": residuo,
    }


# ============================================================================
# 4. NÚCLEOS EDITORIAIS (fonte única — reutilizada nas duas camadas)
# ============================================================================

NUCLEOS = {
    1: {
        "titulo": "A Iniciativa sem Peso",
        "natureza": (
            "O primeiro é o início de tudo — aquele que começa, que inova, que cria. "
            "Mas não carrega o peso de acertar de primeira em tudo o que fizer."
        ),
        "sombra": (
            "O estigma de precisar estar sempre certo, por ter liderado ou iniciado algo "
            "que pode vir a te superar como indivíduo. Esperar a versão perfeita que nunca "
            "chega é confundir excelência com imobilidade."
        ),
        "falta": "A passividade de quem espera que outro inicie por ele.",
        "fecho": (
            "Inicie, comece, dê o primeiro passo — e faça a sua parte. Até o mais belo "
            "trabalho artístico começa com um pequeno ponto, e esse ponto pode virar as "
            "linhas de toda uma vida. Não tema criar nem ser superado pelo que criar."
        ),
    },
    2: {
        "titulo": "A Sensibilidade em Par",
        "natureza": (
            "O dois é o par, o espelho, a cooperação. É a energia que só se realiza na "
            "presença do outro."
        ),
        "sombra": (
            "A dependência do olhar alheio — existir apenas quando refletido."
        ),
        "falta": "A recusa da própria sensibilidade, por medo de parecer frágil.",
        "fecho": (
            "Trabalhe a dois, não sozinho. A sua força neste período está na parceria."
        ),
    },
    3: {
        "titulo": "A Luz Regulável",
        "natureza": (
            "O três é expressão, comunicação, criatividade. A luz que se mostra."
        ),
        "sombra": "Ofuscar em vez de iluminar — a expressão que busca aplauso, não sentido.",
        "falta": "O silêncio de quem tem algo a dizer e não diz.",
        "fecho": (
            "Escolha a intensidade: vela ou sol. Ambos iluminam — mas um aquece sem cegar."
        ),
    },
    4: {
        "titulo": "O Trabalho Digno",
        "natureza": (
            "O quatro é estrutura, base, método. A energia que constrói o que sustenta."
        ),
        "sombra": "A rigidez de quem confunde disciplina com imobilidade.",
        "falta": "A desistência de construir, por achar que já é tarde para começar a base.",
        "fecho": (
            "Mude a variável, não o objetivo: a decisão de recomeçar a estrutura é sua."
        ),
    },
    5: {
        "titulo": "O Amor e o Desejo",
        "natureza": (
            "O cinco é emoção em movimento. As chances de algo que interfira no seu "
            "emocional de modo forte e marcante são consideráveis neste período."
        ),
        "sombra": (
            "A confusão entre os dois motores: buscar desejo e chamar de amor, ou buscar "
            "amor e não sustentar o desejo."
        ),
        "falta": "A recusa da emoção — a armadura de quem já não reconhece quando algo o toca.",
        "fecho": (
            "Valorize o amor e o desejo por quem você ama. Amor e desejo nem sempre andam "
            "juntos — se andarem, pessoas felizes vivem melhor juntas."
        ),
    },
    6: {
        "titulo": "A Missão Humana",
        "natureza": (
            "O seis pede espiritualidade — que pode ser feita com sensibilidade e trabalho, "
            "com luz, com iniciativa ou com emoção afetiva. Mas há um amor que se distingue: "
            "o amor altruísta, pela humanidade."
        ),
        "sombra": "O cuidado que cobra retorno — dar para receber, ajudar para ser visto.",
        "falta": (
            "O recolhimento de quem acha que não tem nada a oferecer, quando o que se "
            "oferece aqui não é material."
        ),
        "fecho": (
            "Cumpra sua missão humana neste período. Às vezes é um gesto, uma palavra. "
            "O que nos torna humanos não é sermos humanos — é nos tornarmos humanos. "
            "Seja grato pelo que a lei do retorno lhe assegura."
        ),
    },
    7: {
        "titulo": "A Sabedoria e o Conhecimento",
        "natureza": (
            "Um ser pode ser sábio e não ter conhecimento, ou ter conhecimento e não ter "
            "sabedoria. A energia do conhecimento não te torna mais sábio — ela abre portas."
        ),
        "sombra": (
            "Acumular sem aplicar: colecionar informação como troféu. E a recusa de aprender "
            "o que ameaça o que já se acredita."
        ),
        "falta": (
            "A recusa da profundidade — chamar de praticidade o que é medo de questionar."
        ),
        "fecho": (
            "Abra mão de algo que julgava por certo. O compromisso não é com o que você vai "
            "aprender, é com você. Conhecimento é poder — poder de escolha."
        ),
    },
    8: {
        "titulo": "A Sorte Planejada",
        "natureza": (
            "Dinheiro e poder vêm com trabalho dobrado: 99% de transpiração e 1% de "
            "inspiração. A maioria erra mais do que acerta — até que, por insistência, "
            "conquista seu espaço."
        ),
        "sombra": (
            "O atalho: querer o resultado sem a transpiração, buscar o poder sem o "
            "conhecimento que o sustenta, confundir sorte com permissão para não fazer nada."
        ),
        "falta": (
            "A recusa do próprio tamanho: competência que não se apresenta, talento que "
            "não se posiciona, gente que trabalha dobrado e nunca cobra."
        ),
        "fecho": (
            "Sem conhecimento não há poder — estudos, informação e pesquisa contínuos, "
            "multidisciplinaridade com foco inabalável, resiliência muito mais que resistência. "
            "E planeje a sorte: 'Eu faço a minha sorte.' Faz? Você a planejou em algum momento?"
        ),
    },
    9: {
        "titulo": "A Fênix e a Águia",
        "natureza": (
            "O nove é finalização — mas não confunda com morte. É a última vida neste plano, "
            "resgate, transmutação. Quem viveu oito vidas antes carrega as dores de todas elas."
        ),
        "sombra": (
            "A amargura que se fecha: usar a experiência como muro em vez de ponte."
        ),
        "falta": "A negação da própria bagagem — fingir que não viu o que viu.",
        "fecho": (
            "A fênix renasce por ritual; a águia renasce por escolha. Ela quebra o bico na "
            "pedra, arranca as garras, arranca as penas — e volta mais forte. A morte é uma "
            "certeza; o seu renascimento é escolha sua."
        ),
    },
    11: {
        "titulo": "A Força Dobrada",
        "natureza": (
            "O onze não é um dois: é o um duplicado — Deus em espelho. Age como amplificador. "
            "O que já estava em curso não muda de direção, muda de intensidade."
        ),
        "sombra": (
            "Ambição sem preparo: desejar com força dobrada o que não se tem estrutura para "
            "sustentar, apontar o dedo e receber o retorno triplicado."
        ),
        "falta": "O medo de exercer o próprio poder — a recusa de assumir que também se recebe em dobro.",
        "fecho": (
            "Saiba pedir e saiba agir. O onze não atende pedido confuso. Quem aponta um dedo "
            "recebe três de volta e um para cima. Ele não cria caráter — expõe em tamanho maior."
        ),
    },
    22: {
        "titulo": "A Obra Sagrada",
        "natureza": (
            "O vinte e dois é a reafirmação da sensibilidade, da arte, da força feminina — "
            "em escala mestre. É a força criativa dobrada, voltada para a obra."
        ),
        "sombra": (
            "A grandiosidade sem entrega: querer a obra sem o ofício, falar do projeto "
            "sem construir."
        ),
        "falta": "A recusa do próprio tamanho: talento que se diminui para caber no que os outros esperam.",
        "fecho": (
            "Faça o trabalho diferenciado — acima da média, com especial tendência artística. "
            "Não é para você se exibir: é para transformar algo ao redor."
        ),
    },
}


# ============================================================================
# 5. LEITURA COMPLETA
# ============================================================================

def gerar_leitura(data_nasc: str, ano_ref: int, mes_ref: int, nome: str = "") -> dict:
    """
    data_nasc: 'DD-MM-AAAA' ou 'DD/MM/AAAA' (data COMPLETA — bug #1)
    ano_ref / mes_ref: período consultado (inputs separados)
    """
    sep = "/" if "/" in data_nasc else "-"
    dia, mes_n, ano_n = (int(p) for p in data_nasc.split(sep))

    cv = caminho_vida(dia, mes_n, ano_n)
    ag = ano_geral(ano_ref)
    mg = mes_geral(ano_ref, mes_ref)
    ap = ano_pessoal(ano_ref, cv)          # sem mês (bug #2)
    mp = mes_pessoal(ano_ref, mes_ref, cv)
    cruz = leitura_cruzada(mg, mp)
    tom = tom_da_soma(mg, mp)

    return {
        "identificacao": {
            "nome": nome,
            "nascimento": data_nasc,
            "caminho_vida": cv,
            "periodo": {"ano": ano_ref, "mes": mes_ref},
        },
        "energia_geral": {
            "numero": mg,
            "exibir_como": "2 e 11" if mg == 11 else str(mg),
            "nucleos": [NUCLEOS[2], NUCLEOS[11]] if mg == 11 else [NUCLEOS[mg]],
        },
        "ano_pessoal": {"numero": ap, "nucleo": NUCLEOS.get(ap)},
        "energia_pessoal": {"numero": mp, "nucleo": NUCLEOS[mp]},
        "leitura_cruzada": {
            "numero": cruz,
            "nucleo": NUCLEOS.get(cruz),
            "tom": tom,
        },
        "energia_dobrada": mg == mp,
        "alerta_dois_onze": (mg == 11 and mp == 11),
    }


# ============================================================================
# 6. TESTES — validação com o caso do autor
# ============================================================================

if __name__ == "__main__":
    # Caso A1ELOS: CV 8, referência outubro/2026
    r = gerar_leitura("11-03-1980", 2026, 10, "Antonio")

    assert r["identificacao"]["caminho_vida"] == 8, "CV deveria ser 8"
    assert r["energia_geral"]["numero"] == 2, "Mês geral out/2026 = 2"
    assert r["ano_pessoal"]["numero"] == 9, "Ano pessoal 2026 com CV 8 = 9"
    assert r["energia_pessoal"]["numero"] == 1, "Mês pessoal = 1"

    # Tom: 2 (emocional) + 1 (racional) -> resultado 3 (emocional)
    assert r["leitura_cruzada"]["numero"] == 3
    assert r["leitura_cruzada"]["tom"]["tom"] == "emocional"

    print("✓ Todos os testes passaram")
    print(f"CV....: {r['identificacao']['caminho_vida']}")
    print(f"Ano P.: {r['ano_pessoal']['numero']}")
    print(f"Mês G.: {r['energia_geral']['exibir_como']}")
    print(f"Mês P.: {r['energia_pessoal']['numero']}")
    print(f"Cruzado: {r['leitura_cruzada']['numero']} ({r['leitura_cruzada']['tom']['label']})")
