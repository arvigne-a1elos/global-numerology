# -*- coding: utf-8 -*-
# pdf_service.py - Geração de todos os PDFs (ReportLab)
import os, uuid
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
import dateutil.parser as dp
from calc_service import reduzir, calc_grid
from dicionarios import SIG, CAM, DES, VIB, t

# Constantes visuais
GOLD = colors.HexColor("#B8860B")
LGRAY = colors.HexColor("#f0f0f0")
DARK = colors.HexColor("#222")
GRAY = colors.HexColor("#888")
FONTE = "Helvetica"
FN = "Helvetica-Bold"
TAM_T = 20
TAM_C = 14
EL = TAM_C * 1.5
ET = TAM_T * 2.0

def _estilo(nome, fonte, size, cor, alinhamento, sb=0, sa=0):
    return ParagraphStyle(nome, fontName=fonte, fontSize=size,
                          textColor=cor, alignment=alinhamento,
                          spaceBefore=sb, spaceAfter=sa, leading=size * 1.5)

# ----- PDF8 - Mapa Express -----
def pdf8(data, nome, bd):
    path = f"/tmp/p8_{uuid.uuid4().hex[:8]}.pdf"
    doc = SimpleDocTemplate(path, pagesize=A4,
                            leftMargin=50, rightMargin=50,
                            topMargin=45, bottomMargin=45)
    e = []
    TX = {1: "Líder nato, pioneiro.", 2: "Diplomata, sensível.",
          3: "Criativo, comunicador.", 4: "Prático, disciplinado.",
          5: "Livre, aventureiro.", 6: "Amoroso, responsável.",
          7: "Sábio, espiritual.", 8: "Poderoso, próspero.",
          9: "Humanitário, generoso.", 11: "Mestre intuitivo.",
          22: "Mestre construtor."}
    e.append(Spacer(1, 30))
    e.append(Paragraph("MAPA NUMEROLÓGICO",
                       _estilo("T", FN, TAM_T, GOLD, TA_CENTER, sa=ET)))
    e.append(Paragraph("EXPRESS",
                       _estilo("S", FONTE, 18, GOLD, TA_CENTER, sa=ET)))
    e.append(Paragraph(nome.upper(),
                       _estilo("N", FN, TAM_C + 2, DARK, TA_CENTER, sa=4)))
    e.append(Paragraph(bd,
                       _estilo("D", FONTE, TAM_C - 2, GRAY, TA_CENTER, sa=EL)))
    td = [["Número", "Valor"],
          ["Caminho de Vida", str(data["life_path"])],
          ["Expressão", str(data["expression"])],
          ["Motivação da Alma", str(data["soul_urge"])],
          ["Personalidade", str(data["personality"])],
          ["Destino", str(data["destiny"])]]
    tbl = Table(td, colWidths=[200, 150])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GOLD),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), TAM_C - 2),
        ("FONTNAME", (0, 0), (-1, -1), FONTE),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (1, 0), (1, -1), "CENTER"),
        ("BACKGROUND", (0, 1), (-1, -1), LGRAY),
        ("TEXTCOLOR", (0, 1), (-1, -1), DARK),
    ]))
    e.append(tbl)
    e.append(Spacer(1, EL))
    for k, l in [("life_path", "Caminho de Vida"), ("expression", "Expressão"),
                  ("soul_urge", "Motivação"), ("personality", "Personalidade"),
                  ("destiny", "Destino")]:
        v = data[k]
        e.append(Paragraph(f"<b>{l} {v}:</b> {TX.get(v, 'Único.')}",
                           _estilo("X", FONTE, TAM_C, DARK, TA_LEFT, sa=EL * 0.5)))
    e.append(Paragraph("© A1ELOS Assessoria e Consultoria",
                       _estilo("F", FONTE, 10, GRAY, TA_CENTER, sb=EL * 2)))
    doc.build(e)
    return path

# ----- PDF17 - Mapa Completo -----
def pdf17(data, nome, bd_str, lang="pt"):
    path = f"/tmp/p17_{uuid.uuid4().hex[:8]}.pdf"
    doc = SimpleDocTemplate(path, pagesize=A4,
                            leftMargin=50, rightMargin=50,
                            topMargin=45, bottomMargin=45)
    e = []
    lp = data["life_path"]
    _, desc_cam = CAM.get(lp, ("", ""))
    nome_p = nome.split()[0] if " " in nome else nome

    e.append(Spacer(1, 30))
    e.append(Paragraph("M A P A   N U M E R O L Ó G I C O",
                       _estilo("T", FN, TAM_T, GOLD, TA_CENTER, sa=4)))
    e.append(Paragraph("C O M P L E T O",
                       _estilo("U", FONTE, 18, GOLD, TA_CENTER, sa=ET)))
    e.append(Paragraph(nome.upper(),
                       _estilo("N", FN, TAM_C + 2, DARK, TA_CENTER, sa=4)))
    e.append(Paragraph(bd_str,
                       _estilo("D", FONTE, TAM_C - 2, GRAY, TA_CENTER, sa=EL)))

    # Tabela resumo
    td = [["Número", "Valor", "Significado"],
          ["Caminho de Vida", str(lp), SIG.get(lp, ("", "", "", ""))[0]],
          ["Expressão", str(data["expression"]), SIG.get(data["expression"], ("", "", "", ""))[0]],
          ["Motivação", str(data["soul_urge"]), SIG.get(data["soul_urge"], ("", "", "", ""))[0]],
          ["Personalidade", str(data["personality"]), SIG.get(data["personality"], ("", "", "", ""))[0]],
          ["Destino", str(data["destiny"]), SIG.get(data["destiny"], ("", "", "", ""))[0]]]
    tbl = Table(td, colWidths=[125, 45, 280])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GOLD),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), TAM_C - 2),
        ("FONTNAME", (0, 0), (-1, -1), FONTE),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (1, 0), (1, -1), "CENTER"),
        ("BACKGROUND", (0, 1), (-1, -1), LGRAY),
        ("TEXTCOLOR", (0, 1), (-1, -1), DARK),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    e.append(tbl)
    e.append(PageBreak())

    # Análise detalhada
    e.append(Paragraph("<b>Análise Detalhada dos Números</b>",
                       _estilo("SE", FN, 18, GOLD, TA_LEFT, sb=EL, sa=ET)))
    e.append(Paragraph(
        "Cada número possui um sentido positivo e um negativo. Conhecer ambos é "
        "o primeiro passo para o autoconhecimento e a evolução pessoal.",
        _estilo("J", FONTE, TAM_C - 1, DARK, TA_JUSTIFY, sa=EL * 0.4)))

    for k, l in [("life_path", "Caminho de Vida"), ("expression", "Expressão"),
                  ("soul_urge", "Motivação"), ("personality", "Personalidade"),
                  ("destiny", "Destino")]:
        v = data[k]
        nm, pos, neg, licao = SIG.get(v, ("", "", "", ""))
        e.append(Paragraph(f"<b>{l} {v} — {nm}</b>",
                           _estilo("BL", FN, TAM_C - 1, DARK, TA_LEFT, sa=EL * 0.3)))
        e.append(Paragraph(pos,
                           _estilo("JP", FONTE, TAM_C - 1, DARK, TA_JUSTIFY, sa=EL * 0.4)))
        e.append(Paragraph(f"<b>Desafio:</b> {neg}",
                           _estilo("JP", FONTE, TAM_C - 1, DARK, TA_JUSTIFY, sa=EL * 0.4)))
        e.append(Paragraph(f"<b>Lição:</b> {licao}",
                           _estilo("JP", FONTE, TAM_C - 1, DARK, TA_JUSTIFY, sa=EL * 0.4)))

    bd = dp.parse(bd_str.split(" ")[0] if " " in bd_str else bd_str).date()
    d, m, a = bd.day, bd.month, bd.year

    # Ciclos
    fe = max(36 - min(lp, 36), 25)
    c1 = reduzir(lp + data["expression"])
    c2 = reduzir(data["expression"] + data["soul_urge"])
    c3 = reduzir(data["soul_urge"] + data["personality"])
    e.append(Paragraph("<b>Ciclos da Vida</b>",
                       _estilo("SE", FN, 18, GOLD, TA_LEFT, sb=EL, sa=ET)))
    e.append(Paragraph(f"<b>1º Formativo (0-{fe}a) Regente {c1}:</b> Fase de aprendizado.",
                       _estilo("JP", FONTE, TAM_C - 1, DARK, TA_LEFT, sa=EL * 0.4)))
    e.append(Paragraph(f"<b>2º Produtivo ({fe+1}-{fe+27}a) Regente {c2}:</b> Fase de trabalho.",
                       _estilo("JP", FONTE, TAM_C - 1, DARK, TA_LEFT, sa=EL * 0.4)))
    e.append(Paragraph(f"<b>3º Colheita ({fe+28}+a) Regente {c3}:</b> Fase de sabedoria.",
                       _estilo("JP", FONTE, TAM_C - 1, DARK, TA_LEFT, sa=EL * 0.4)))

    # Desafios
    d1 = reduzir(abs(d - m))
    d2 = reduzir(abs(m - reduzir(a)))
    dp_ = reduzir(abs(d1 - d2))
    e.append(Paragraph("<b>Desafios</b>",
                       _estilo("SE", FN, 18, GOLD, TA_LEFT, sb=EL, sa=ET)))
    e.append(Paragraph(f"<b>Menor 1 (Dia×Mês) {d1}:</b> {DES.get(d1, '')}",
                       _estilo("JP", FONTE, TAM_C - 1, DARK, TA_JUSTIFY, sa=EL * 0.4)))
    e.append(Paragraph(f"<b>Menor 2 (Mês×Ano) {d2}:</b> {DES.get(d2, '')}",
                       _estilo("JP", FONTE, TAM_C - 1, DARK, TA_JUSTIFY, sa=EL * 0.4)))
    e.append(Paragraph(f"<b>Principal {dp_}:</b> {DES.get(dp_, '')}",
                       _estilo("JP", FONTE, TAM_C - 1, DARK, TA_JUSTIFY, sa=EL * 0.4)))

    # Realizações
    r1v = reduzir(d + m)
    r2v = reduzir(d + a)
    r3v = reduzir(r1v + r2v)
    r4v = reduzir(d + m + a)
    e.append(Paragraph("<b>Realizações</b>",
                       _estilo("SE", FN, 18, GOLD, TA_LEFT, sb=EL, sa=ET)))
    e.append(Paragraph(f"<b>1ª ({r1v}) Juventude</b>",
                       _estilo("JP", FONTE, TAM_C - 1, DARK, TA_LEFT, sa=EL * 0.4)))
    e.append(Paragraph(f"<b>2ª ({r2v}) Vida Adulta</b>",
                       _estilo("JP", FONTE, TAM_C - 1, DARK, TA_LEFT, sa=EL * 0.4)))
    e.append(Paragraph(f"<b>3ª ({r3v}) Maturidade</b>",
                       _estilo("JP", FONTE, TAM_C - 1, DARK, TA_LEFT, sa=EL * 0.4)))
    e.append(Paragraph(f"<b>4ª ({r4v}) Legado</b>",
                       _estilo("JP", FONTE, TAM_C - 1, DARK, TA_LEFT, sa=EL * 0.4)))

    # Vibração
    vib = reduzir(d)
    e.append(Paragraph("<b>Vibração do Dia</b>",
                       _estilo("SE", FN, 18, GOLD, TA_LEFT, sb=EL, sa=ET)))
    e.append(Paragraph(f"{VIB.get(vib, '')}",
                       _estilo("J", FONTE, TAM_C - 1, DARK, TA_JUSTIFY, sa=EL * 0.4)))

    # Grade
    grid = calc_grid(nome)
    pres = [str(n) for n in range(1, 10) if grid.get(n, 0) > 0]
    aus = [str(n) for n in range(1, 10) if grid.get(n, 0) == 0]
    e.append(Paragraph("<b>Grade de Inclusão</b>",
                       _estilo("SE", FN, 18, GOLD, TA_LEFT, sb=EL, sa=ET)))
    e.append(Paragraph(
        f"<b>Presentes:</b> {', '.join(pres) if pres else 'nenhum'}. "
        f"<b>Carências:</b> {', '.join(aus) if aus else 'nenhum'}.",
        _estilo("J", FONTE, TAM_C - 1, DARK, TA_JUSTIFY, sa=EL * 0.4)))
    if aus:
        nomes_aus = [f"{n}({SIG.get(int(n), ('', '', '', ''))[0]})" for n in aus]
        e.append(Paragraph(
            f"As carências ({', '.join(nomes_aus)}) indicam qualidades a desenvolver.",
            _estilo("J", FONTE, TAM_C - 1, DARK, TA_JUSTIFY, sa=EL * 0.4)))

    # Nota final
    e.append(Paragraph("<b>Nota Final</b>",
                       _estilo("SE", FN, 18, GOLD, TA_LEFT, sb=EL, sa=ET)))
    e.append(Paragraph(
        "A numerologia é uma ferramenta de autoconhecimento baseada no estudo da "
        "vibração dos números e das letras. Ela não determina seu destino, mas ilumina "
        "os caminhos possíveis e revela potencialidades. Os números mostram tendências, "
        "mas o livre arbítrio é sempre seu maior poder.",
        _estilo("J", FONTE, TAM_C - 1, DARK, TA_JUSTIFY, sa=EL * 0.4)))

    e.append(Paragraph("© A1ELOS Assessoria e Consultoria",
                       _estilo("F", FONTE, 10, GRAY, TA_CENTER, sb=EL * 2)))
    doc.build(e)
    return path

# ----- PDF URNA -----
def pdf_urna(nc, cl, resultados, sugestoes):
    path = f"/tmp/u_{uuid.uuid4().hex[:8]}.pdf"
    doc = SimpleDocTemplate(path, pagesize=A4,
                            leftMargin=50, rightMargin=50,
                            topMargin=45, bottomMargin=45)
    e = []
    e.append(Spacer(1, 25))
    e.append(Paragraph("VALIDAÇÃO DE NOME DE URNA",
                       _estilo("T", FN, TAM_T, GOLD, TA_CENTER, sa=ET * 0.5)))
    e.append(Paragraph(nc.title(),
                       _estilo("N", FN, TAM_C + 2, DARK, TA_CENTER, sa=4)))
    e.append(Paragraph(f"Cargo: {cl}",
                       _estilo("D", FONTE, TAM_C - 2, GRAY, TA_CENTER, sa=EL)))
    for r in resultados:
        ic = "✅" if r["eh_ideal"] else "❌"
        co = "#4CAF50" if r["eh_ideal"] else "#e74c3c"
        e.append(Paragraph(
            f"{ic} <b>{r['nome']}</b> — Energia <b><font color='{co}'>{r['energia']}</font></b>",
            _estilo("B", FN, TAM_C - 1, DARK, TA_LEFT, sa=EL * 0.3)))
        if r["letras"]:
            ls = ", ".join(f'{l["letra"]}={l["valor"]}' for l in r["letras"])
            e.append(Paragraph(f"<i>{ls} → {r['soma']} → {r['energia']}</i>",
                               _estilo("C", FONTE, TAM_C - 2, GRAY, TA_LEFT, sa=EL * 0.2)))
        e.append(Paragraph(r["explicacao"],
                           _estilo("J", FONTE, TAM_C - 1, DARK, TA_JUSTIFY, sa=EL * 0.4)))
    if sugestoes:
        e.append(Paragraph("Sugestões:",
                           _estilo("SU", FN, 18, GOLD, TA_LEFT, sb=EL, sa=ET)))
        for s in sugestoes[:3]:
            e.append(Paragraph(
                f'<b>{s["nome"]}</b> — Energia {s["energia"]}',
                _estilo("X", FONTE, TAM_C, DARK, TA_LEFT, sa=EL * 0.3)))
    e.append(Paragraph("© A1ELOS",
                       _estilo("F", FONTE, 8, GRAY, TA_CENTER)))
    doc.build(e)
    return path

# ----- PDF ELEITORAL -----
def pdf_eleitoral(ss, cl, sugestoes, ne=None):
    path = f"/tmp/e_{uuid.uuid4().hex[:8]}.pdf"
    doc = SimpleDocTemplate(path, pagesize=A4,
                            leftMargin=50, rightMargin=50,
                            topMargin=45, bottomMargin=45)
    e = []
    e.append(Spacer(1, 25))
    e.append(Paragraph("NÚMERO ELEITORAL — ANÁLISE COMPLETA",
                       _estilo("T", FN, TAM_T, GOLD, TA_CENTER, sa=ET * 0.5)))
    e.append(Paragraph(f"Cargo: {cl} | Sigla: {ss}",
                       _estilo("D", FONTE, TAM_C - 2, GRAY, TA_CENTER, sa=EL)))

    # Como calculamos
    e.append(Paragraph("<b>Como calculamos?</b>",
                       _estilo("SE", FN, 18, GOLD, TA_LEFT, sb=EL, sa=ET)))
    e.append(Paragraph(
        "Na numerologia eleitoral, cada número possui uma vibração que influencia "
        "a campanha. O cálculo soma todos os dígitos e reduz a um dígito (exceto 11, 22).",
        _estilo("J", FONTE, TAM_C - 1, DARK, TA_JUSTIFY, sa=EL * 0.4)))
    e.append(Paragraph(
        f"Para {cl}, os 2 primeiros dígitos são fixos (sigla {ss}, soma "
        f"{int(ss[0]) + int(ss[1])}). Os demais são escolhidos para energia 8.",
        _estilo("J", FONTE, TAM_C - 1, DARK, TA_JUSTIFY, sa=EL * 0.4)))

    e.append(Paragraph("<b>Por que a energia 8?</b>",
                       _estilo("SE", FN, 18, GOLD, TA_LEFT, sb=EL, sa=ET)))
    e.append(Paragraph(
        "O número 8 representa Poder, Prosperidade e Realização material. "
        "Para candidatos, atrai autoridade, sucesso nas urnas e capacidade de realizar obras.",
        _estilo("J", FONTE, TAM_C - 1, DARK, TA_JUSTIFY, sa=EL * 0.4)))

    # Sugestões
    e.append(Paragraph("Sugestões de Números",
                       _estilo("SE", FN, 18, GOLD, TA_LEFT, sb=EL, sa=ET)))
    ideais = [s for s in sugestoes if s.get("ideal")]
    fallbacks = [s for s in sugestoes if not s.get("ideal")]
    if ideais:
        e.append(Paragraph("<b>Energia 8 — IDEAL:</b>",
                           _estilo("B", FN, TAM_C - 1, DARK, TA_LEFT, sa=EL * 0.3)))
        for s in ideais:
            e.append(Paragraph(f"✅ <b>{s['numero']}</b> — Energia 8 — Poder e Prosperidade!",
                               _estilo("X", FONTE, TAM_C, colors.HexColor("#4CAF50"), TA_LEFT, sa=EL * 0.2)))
            if "explicacao_calculo" in s:
                e.append(Paragraph(f"<i>Cálculo: {s['explicacao_calculo']}</i>",
                                   _estilo("C", FONTE, TAM_C - 2, GRAY, TA_LEFT, sa=EL * 0.2)))
    if fallbacks:
        e.append(Paragraph("<b>Alternativas:</b>",
                           _estilo("B", FN, TAM_C - 1, DARK, TA_LEFT, sb=EL * 0.5, sa=EL * 0.3)))
        for s in fallbacks:
            e.append(Paragraph(f"{s['numero']} — Energia {s['energia']} — {s.get('nome_energia', '')}",
                               _estilo("X", FONTE, TAM_C - 1, DARK, TA_LEFT, sa=EL * 0.2)))
    if ne:
        e.append(Paragraph("<b>Número Existente Analisado:</b>",
                           _estilo("SE", FN, 18, GOLD, TA_LEFT, sb=EL, sa=ET)))
        e.append(Paragraph(f"<b>{ne['numero']}</b> — Energia {ne['energia']}",
                           _estilo("X", FONTE, TAM_C, DARK, TA_LEFT, sa=EL * 0.3)))
        if ne["energia"] == 8:
            e.append(Paragraph("Este número já possui energia 8! Excelente.",
                               _estilo("J", FONTE, TAM_C - 1, DARK, TA_JUSTIFY, sa=EL * 0.4)))
        else:
            e.append(Paragraph(f"Tem energia {ne['energia']}, diferente do ideal 8.",
                               _estilo("J", FONTE, TAM_C - 1, DARK, TA_JUSTIFY, sa=EL * 0.4)))
    e.append(Paragraph("© A1ELOS — Numerologia aplicada ao sucesso eleitoral",
                       _estilo("F", FONTE, 8, GRAY, TA_CENTER, sb=EL * 2)))
    doc.build(e)
    return path
