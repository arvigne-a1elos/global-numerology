# -*- coding: utf-8 -*-
# produtos/calendario.py - Calendário Mensal Energético (v4 — REGRA A1ELOS)
# Regra de cálculo definida por Antonio (01/11/2026):
#   1) Caminho de Vida (energia pessoal) = redução da data completa de nascimento.
#   2) Energia do Mês Universal = mês da pesquisa (11 e 22 permanecem mestres).
#   3) Ano Universal = redução do ano da pesquisa.
#   4) Ano Pessoal = reduzir(Caminho de Vida + Ano Universal).
#   5) Mês Pessoal = reduzir(Ano Pessoal + mês da pesquisa), com o mestre
#      registrado quando o resultado bruto for 11 ou 22.
# Exemplo de verificação (Antonio, 05/08/1966, mês 2026-11):
#   CV: 5+8+22 = 8 · Ano Universal: 2+0+2+6 = 1 · Ano Pessoal: 8+1 = 9
#   Mês Pessoal: 9+11 = 20 → 2 (mestre 11 registrado)
from .mapa import reduzir


def _reduz_mestre(n):
    """Reduz preservando números-mestre 11 e 22 (regra A1ELOS)."""
    n = int(n)
    while n > 9 and n not in (11, 22):
        n = sum(int(d) for d in str(n))
    return n


def _digitos_data(nascimento):
    """Aceita AAAA-MM-DD ou DD/MM/AAAA. Retorna os dígitos, ou '' se inválido."""
    partes = str(nascimento).replace("/", "-").split("-")
    if len(partes) == 3 and all(p.strip().isdigit() for p in partes):
        return "".join(p.strip() for p in partes)
    return ""


def caminho_vida(nascimento):
    """Energia pessoal: redução de todos os dígitos da data de nascimento."""
    digitos = _digitos_data(nascimento)
    if not digitos:
        return None
    return _reduz_mestre(sum(int(c) for c in digitos))


def analisar_calendario(nome, mes, nascimento=""):
    """Analisa um mês no formato 'AAAA-MM' — REGRA A1ELOS."""
    # 1) Energia do Mês Universal = o próprio mês (mestres preservados)
    try:
        ano, mm = str(mes).split("-")
        e_mes = _reduz_mestre(int(mm))
        e_ano = _reduz_mestre(sum(int(c) for c in ano))   # Ano Universal
    except (ValueError, TypeError):
        import logging; logging.getLogger(__name__).warning("Calendario: dado invalido: %s", str(mes)[:20])
        e_mes, e_ano = 1, 1

    # 2) Caminho de Vida (energia pessoal da pessoa)
    cv = caminho_vida(nascimento) if nascimento else None

    # 3) Ano Pessoal (regra A1ELOS): Caminho de Vida + Ano Universal
    ano_pessoal = _reduz_mestre(cv + e_ano) if cv else None

    # 4) Mês Pessoal: Ano Pessoal + mês da pesquisa (mestre registrado)
    bruto = (ano_pessoal + int(mm)) if (ano_pessoal is not None) else e_mes
    pessoal_mes = _reduz_mestre(bruto)
    mestre_mes = bruto if bruto in (11, 22) else ""

    # 5) Rastro do cálculo — caixa dourada do PDF
    rastro = (
        f"Vida: {nascimento} = {cv} · "
        f"Ano Universal: {ano} = {e_ano} · "
        f"Ano Pessoal: {cv}+{e_ano} = {ano_pessoal} · "
        f"Mês Pessoal: {ano_pessoal}+{int(mm)} = {bruto}"
        + (f" → {pessoal_mes} (mestre {mestre_mes})" if mestre_mes else f" → {pessoal_mes}")
    )

    return {
        "nome": nome,
        "mes": mes,
        "nascimento": nascimento or "",
        "caminho_vida": cv,                  # energia pessoal (sua: 8)
        "ano_pessoal": ano_pessoal,          # sua regra: 9
        "energia_mes": e_mes,                # mês universal (11 fica 11)
        "energia_pessoal_mes": pessoal_mes,  # energia da pessoa naquele mês (2)
        "mes_pessoal_mestre": mestre_mes,    # "11" quando houver mestre
        "rastro": rastro,                    # caixa dourada do PDF
    }


def analisar_periodo(nome, meses, nascimento=""):
    """Analisa um mês (string 'AAAA-MM') ou vários (lista). Um mês ou mais."""
    if isinstance(meses, str):
        return analisar_calendario(nome, meses, nascimento)
    return [analisar_calendario(nome, m, nascimento) for m in meses]
