# -*- coding: utf-8 -*-
# produtos/equipe.py — Compatibilidade de Equipes (RH)
# REGRA DE PRODUTO: chefe/gestor + 2 colaboradores (3 pessoas).
# Cruzamento: chefe x cada colaborador. NUNCA colaborador x colaborador.
# Profundidade: energia do nome + caminho de vida (padrão casal.py).
from .mapa import reduzir, _LETRAS
from referencia.cissay import compatibilidade

MAX_MEMBROS = 2   # além do chefe

def _energia_nome(nome):
    s = sum(_LETRAS.get(c, 0) for c in nome.upper().replace(" ", ""))
    return reduzir(s), s

def _caminho_vida(nasc):
    try:
        d, m, a = nasc.split("-")
        s = sum(int(x) for x in d + m + a)
        return reduzir(s), s
    except Exception:
        return None, 0

def analisar_equipe(texto):
    bruto = str(texto).replace("\\n", "\n")
    linhas = [l.strip() for l in bruto.splitlines() if l.strip()]
    pessoas = []
    for linha in linhas:
        if ";" in linha:
            partes = [p.strip() for p in linha.split(";", 1)]
        elif "," in linha:
            partes = [p.strip() for p in linha.split(",", 1)]
        else:
            partes = [linha]
        nome = partes[0]
        nasc = partes[1] if len(partes) > 1 else ""
        if nasc and "/" in nasc:
            dd, mm, aa = nasc.split("/")
            nasc = f"{aa}-{mm}-{dd}"
        en, sn = _energia_nome(nome)
        ev, sv = _caminho_vida(nasc)
        pessoas.append({"membro": nome, "nascimento": nasc, "soma": sn,
                        "energia": en, "caminho_vida": ev})

    if len(pessoas) > MAX_MEMBROS + 1:
        pessoas = pessoas[:MAX_MEMBROS + 1]

    chefe = pessoas[0] if pessoas else None
    if chefe:
        chefe["papel"] = "chefe"

    pares = []
    if chefe:
        for m in pessoas[1:]:
            m["papel"] = "colaborador"
            cn = compatibilidade(chefe["energia"], m["energia"])
            cv = None
            if chefe["caminho_vida"] and m["caminho_vida"]:
                cv = compatibilidade(chefe["caminho_vida"], m["caminho_vida"])

            if cn["grau"] is None:
                grau_final = cv["grau"] if cv else None
            elif cv is None or cv["grau"] is None:
                grau_final = cn["grau"]
            else:
                grau_final = (cn["grau"] + cv["grau"]) // 2

            pares.append({
                "membro1": chefe["membro"], "papel1": "chefe",
                "membro2": m["membro"], "papel2": "colaborador",
                "energia1": chefe["energia"], "energia2": m["energia"],
                "caminho1": chefe["caminho_vida"], "caminho2": m["caminho_vida"],
                "compatibilidade_nome": cn["grau"], "rotulo_nome": cn["rotulo"],
                "compatibilidade_vida": cv["grau"] if cv else None,
                "rotulo_vida": cv["rotulo"] if cv else None,
                "compatibilidade": grau_final,
                "dual": cn["dual"] or (cv["dual"] if cv else False),
                "alerta_dualidade": cn["alerta_dualidade"],
            })

    return {"chefe": chefe, "membros": pessoas,
            "total": len(pessoas), "pares": pares}
