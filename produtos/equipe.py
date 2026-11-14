def analisar_equipe(texto, separador="|"):
    bruto = str(texto or "")
    if "\n" in bruto:
        linhas = [l.strip() for l in bruto.splitlines() if l.strip()]
    elif separador in bruto:
        linhas = [l.strip() for l in bruto.split(separador) if l.strip()]
    else:
        linhas = [bruto.strip()] if bruto.strip() else []

    pessoas = []
    for linha in linhas:
        partes = [p.strip() for p in linha.split(";", 1)] if ";" in linha else [linha]
        nome = partes[0]
        nasc = partes[1] if len(partes) > 1 else ""
        if nasc and "/" in nasc:
            dd, mm, aa = nasc.split("/")
            nasc = f"{aa}-{mm}-{dd}"
        en, sn = _energia_nome(nome)
        ev, sv = _caminho_vida(nasc)
        pessoas.append({
            "membro": nome, "nascimento": nasc, "soma": sn,
            "energia": en, "caminho_vida": ev,
            "energia_combinada": _energia_combinada(en, ev),
        })

    if len(pessoas) > MAX_MEMBROS + 1:
        pessoas = pessoas[:MAX_MEMBROS + 1]

    chefe = pessoas[0] if pessoas else None
    if chefe:
        chefe["papel"] = "chefe"

    pares = []
    if chefe:
        for m in pessoas[1:]:
            m["papel"] = "colaborador"
            # MESMA regra da família: cruza a ENERGIA COMBINADA
            c = compatibilidade(chefe["energia_combinada"],
                                m["energia_combinada"])
            pares.append({
                "membro1": chefe["membro"], "papel1": "chefe",
                "membro2": m["membro"], "papel2": "colaborador",
                "energia1": chefe["energia_combinada"],
                "energia2": m["energia_combinada"],
                "compatibilidade": c["grau"], "rotulo": c["rotulo"],
                "dual": c["dual"], "alerta_dualidade": c["alerta_dualidade"],
            })

    return {"chefe": chefe, "membros": pessoas,
            "total": len(pessoas), "pares": pares}
