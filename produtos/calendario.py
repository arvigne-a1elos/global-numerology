# -*- coding: utf-8 -*-
# produtos/calendario.py - Calendário Mensal Energético (v3, com Caminho de Vida)
# Regra de cálculo definida por Antonio (18/10/2026):
#   1) Caminho de Vida (energia pessoal) = redução da data completa de nascimento.
#   2) Mês Universal = reduzir(mês da pesquisa) + reduzir(ano da pesquisa).
#   3) Mês Pessoal = reduzir(Mês Universal + Caminho de Vida).
#   4) Ano Pessoal (serviço embutido) = reduzir(dia) + reduzir(mês nasc.) + reduzir(ano pesquisa).
from .mapa import reduzir


def _reduz9(n):
    """Reduz a um único dígito 1-9, sem preservar números-mestre.
    Regra do produto: cada etapa termina em um dígito."""
    n = int(n)
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n


def _digitos_data(nascimento):
    """Aceita AAAA-MM-DD (input de data do HTML) ou DD/MM/AAAA.
    Retorna o texto de todos os dígitos, ou '' se inválido."""
    partes = str(nascimento).replace("/", "-").split("-")
    if len(partes) == 3 and all(p.strip().isdigit() for p in partes):
        return "".join(p.strip() for p in partes)
    return ""


def caminho_vida(nascimento):
    """Energia pessoal: redução de todos os dígitos da data de nascimento."""
    digitos = _digitos_data(nascimento)
    if not digitos:
        return None
    return _reduz9(sum(int(c) for c in digitos))


def _dia_mes_nascimento(nascimento):
    """Retorna (dia, mês) de nascimento, detectando a ordem da data."""
    partes = str(nascimento).replace("/", "-").split("-")
    if len(partes) != 3:
        return None, None
    try:
        p0, p1, p2 = (p.strip() for p in partes)
        if len(p0) == 4:          # AAAA-MM-DD
            return int(p2), int(p1)
        return int(p0), int(p1)   # DD-MM-AAAA
    except (ValueError, TypeError):
        return None, None


def analisar_calendario(nome, mes, nascimento=""):
    """Analisa um mês no formato 'AAAA-MM'."""
    # 1) Mês Universal (energia própria do mês, sem indivíduo)
    try:
        ano, mm = str(mes).split("-")
        e_mes = _reduz9(sum(int(c) for c in mm))
        e_ano = _reduz9(sum(int(c) for c in ano))
        universal = _reduz9(e_mes + e_ano)
    except (ValueError, TypeError):
        import logging; logging.getLogger(__name__).warning("Calendario: dado invalido: %s", str(mes)[:20])
        universal = 1

    # 2) Caminho de Vida (energia pessoal da pessoa)
    cv = caminho_vida(nascimento) if nascimento else None

    # 3) Mês Pessoal (a energia DA PESSOA naquele mês)
    pessoal_mes = _reduz9(universal + cv) if cv else universal

    # 4) Ano Pessoal (serviço embutido no produto)
    ano_pessoal = None
    d_n, m_n = _dia_mes_nascimento(nascimento) if nascimento else (None, None)
    if d_n:
        try:
            ano_pesq = str(mes).split("-")[0]
            e_d = _reduz9(sum(int(c) for c in str(d_n)))
            e_m = _reduz9(sum(int(c) for c in str(m_n)))
            e_a = _reduz9(sum(int(c) for c in ano_pesq))
            ano_pessoal = _reduz9(e_d + e_m + e_a)
        except (ValueError, TypeError):
            ano_pessoal = None

    return {
        "nome": nome,
        "mes": mes,
        "nascimento": nascimento or "",
        "caminho_vida": cv,                  # energia pessoal (sua: 8)
        "ano_pessoal": ano_pessoal,          # serviço embutido
        "energia_mes": universal,            # energia geral do mês (PDF atual lê esta chave)
        "energia_pessoal_mes": pessoal_mes,  # energia da pessoa naquele mês
    }


def analisar_periodo(nome, meses, nascimento=""):
    """Analisa um mês (string 'AAAA-MM') ou vários (lista). Um mês ou mais."""
    if isinstance(meses, str):
        return analisar_calendario(nome, meses, nascimento)
    return [analisar_calendario(nome, m, nascimento) for m in meses]
