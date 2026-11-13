def calc_mapa(nome, data_str):
    bd = dp.parse(data_str).date()
    nu = normalizar_nome(nome)

    # --- Caminho de Vida ---
    lp_bruto = bd.day + bd.month + bd.year
    lp = reduzir(lp_bruto)
    lp_mestre = lp_bruto if lp_bruto in (11, 22) else None

    # --- Letras ---
    total = vogais = consoantes = 0
    for ch in nu:
        val = _LETRAS.get(ch, 0)
        total += val
        if ch in VOGAIS:
            vogais += val
        else:
            consoantes += val

    assert vogais + consoantes == total, "partição de letras quebrada"

    # --- Energias finais (SEMPRE reduzidas) ---
    personalidade = reduzir(total)
    alma = reduzir(vogais)
    realizacao = reduzir(consoantes)
    numero = reduzir(lp + personalidade)

    return {
        "life_path": lp,
        "life_path_mestre": lp_mestre,

        "expression": personalidade,
        "personality": personalidade,
        "personality_mestre": total if total in (11, 22) else None,

        "soul_urge": alma,
        "soul_urge_mestre": vogais if vogais in (11, 22) else None,

        "realizacao": realizacao,
        "realizacao_mestre": consoantes if consoantes in (11, 22) else None,

        "destiny": numero,
        "destiny_mestre": (lp + personalidade) if (lp + personalidade) in (11, 22) else None,
    }
