# pdf_service.py - A1ELOS Global Numerology
# RENDERIZADOR: funções puras de montagem de PDF (ReportLab).
# Papel único: recebe dados + idioma e devolve o caminho do PDF gerado.
# Sem regra de negócio, sem cálculo, sem entrega (isso é do gerador_pdf.py).
# Textos: dicionarios.py (TRAD, PDF_TEXTS, PDF_SECOES, BOAS_VINDAS, PERIODOS, REALIZ_HEAD, SIG, CAM, DES, VIB, PRODUTOS).

import os, uuid, tempfile
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
import dateutil.parser as dp
from calc_service import reduzir, calc_grid
from dicionarios import SIG, CAM, DES, VIB, t, PRODUTOS, PDF_TEXTS, PDF_SECOES, BOAS_VINDAS, PERIODOS, REALIZ_HEAD

# ---- Identidade visual (Padrão Mínimo de Qualidade Total) ----
GOLD = colors.HexColor("#C9A94E")
DARK = colors.HexColor("#1a1a1a")
LGRAY = colors.HexColor("#f5f5f0")
WHITE = colors.white
GRAY = colors.HexColor("#888888")
FONTE = "Helvetica"
FN = "Helvetica"
TAM_T = 28
TAM_C = 12
EL = 12
ET = 6
LINHA = 8  # espaçamento de uma linha entre seções (Q5)
TMP = tempfile.gettempdir()
ENERGIA_LBL = {
    "pt": "Energia", "en": "Energy", "es": "Energía", "it": "Energia",
    "fr": "Énergie", "de": "Energie", "ja": "エネルギー", "zh": "能量",
    "ru": "Энергия", "hi": "ऊर्जा", "he": "אנרגיה", "ar": "الطاقة",
}

def _estilo(nome, fonte, tam, cor, alinhamento, sa=0, sb=0):
    return ParagraphStyle(nome, fontName=fonte, fontSize=tam, textColor=cor,
                          alignment=alinhamento, spaceAfter=sa, spaceBefore=sb,
                          leading=tam * 1.4)

def _cabecalho_pagina(canvas, doc):
    """Marca d'água A1ELOS (15%) + rodapé institucional em todas as páginas."""
    canvas.saveState()
    canvas.setFillColor(GOLD)
    canvas.setFillAlpha(0.15)
    canvas.setFont(FONTE, 58)
    canvas.drawCentredString(A4[0] / 2.0, A4[1] / 2.0, "A1ELOS")
    canvas.setFillAlpha(1.0)
    canvas.setFont(FONTE, 7)
    canvas.setFillColor(GOLD)
    canvas.drawString(50, 22, "A1ELOS Assessoria e Consultoria")
    canvas.drawRightString(A4[0] - 50, 22, str(doc.page))
    canvas.restoreState()

# ═══════════════════════════════════════════
# MAPA EXPRESS (1 página, traduzido)
# ═══════════════════════════════════════════
def pdf8(data, nome, bd, lang="pt"):
    T = PDF_TEXTS.get(lang, PDF_TEXTS["pt"])
    path = os.path.join(TMP, f"p8_{uuid.uuid4().hex[:8]}.pdf")
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=50, rightMargin=50,
                            topMargin=45, bottomMargin=45)
    e = []
    e.append(Spacer(1, 20))
    e.append(Paragraph(T.get("t_express", "MAPA EXPRESS"),
                       _estilo("T", FN, TAM_T, GOLD, TA_CENTER, sa=ET)))
    e.append(Paragraph(t("seu_perfil", lang),
                       _estilo("S", FONTE, 16, GOLD, TA_CENTER, sa=4)))
    e.append(Paragraph(nome.upper(), _estilo("N", FN, 14, DARK, TA_CENTER, sa=4)))
    e.append(Paragraph(bd, _estilo("D", FONTE, 10, GRAY, TA_CENTER, sa=EL)))
    e.append(Paragraph(BOAS_VINDAS.get(lang, BOAS_VINDAS["pt"]),
                       _estilo("BV", FONTE, 10, DARK, TA_JUSTIFY, sa=EL)))
    chaves = [("life_path", "caminho_vida"), ("expression", "expressao"),
              ("soul_urge", "motivacao"), ("personality", "personalidade"),
              ("destiny", "destino")]
    linhas = [[t("numero", lang), t("valor", lang), t("significado", lang)]]
    for k, lbl in chaves:
        v = data[k]
        sig = SIG.get(v, (t("nenhum", lang), "", "", ""))
        linhas.append([t(lbl, lang), str(v), sig[0]])
    tbl = Table(linhas, colWidths=[180, 60, 220])  # 460pt <= 495pt
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GOLD), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTSIZE", (0, 0), (-1, -1), 9), ("FONTNAME", (0, 0), (-1, -1), FONTE),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (1, 0), (1, -1), "CENTER"), ("ALIGN", (2, 0), (2, -1), "LEFT"),
        ("BACKGROUND", (0, 1), (-1, -1), LGRAY), ("TEXTCOLOR", (0, 1), (-1, -1), DARK),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    e.append(tbl)
    e.append(Spacer(1, LINHA))
    for k, lbl in chaves:
        v = data[k]
        sig = SIG.get(v, (t("nenhum", lang), "", "", ""))
        e.append(Paragraph(f"<b>{t(lbl, lang)}:</b> {v} — {sig[0]}",
                           _estilo("TX", FONTE, 10, DARK, TA_LEFT, sa=3)))
    e.append(Spacer(1, LINHA))
    e.append(Paragraph(T.get("entrega", ""), _estilo("J", FONTE, 8, GRAY, TA_CENTER, sa=6)))
    e.append(Paragraph("© A1ELOS Assessoria e Consultoria",
                       _estilo("F", FONTE, 8, GRAY, TA_CENTER)))
    doc.build(e, onFirstPage=_cabecalho_pagina, onLaterPages=_cabecalho_pagina)
    return path

# ═══════════════════════════════════════════
# MAPA COMPLETO (template premium, traduzido)
# ═══════════════════════════════════════════
def pdf17(data, nome, bd_str, lang="pt"):
    T = PDF_TEXTS.get(lang, PDF_TEXTS["pt"])
    S = PDF_SECOES.get(lang, PDF_SECOES["pt"])
    P = PERIODOS.get(lang, PERIODOS["pt"])
    RH = REALIZ_HEAD.get(lang, REALIZ_HEAD["pt"])
    path = os.path.join(TMP, f"p17_{uuid.uuid4().hex[:8]}.pdf")
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=50, rightMargin=50,
                            topMargin=45, bottomMargin=45)
    e = []
    lp = data["life_path"]
    _, desc_cam = CAM.get(lp, ("", ""))
    # CAPA
    e.append(Spacer(1, 120))
    e.append(Paragraph(T.get("t_completo", "MAPA COMPLETO"),
                       _estilo("T", FN, 32, GOLD, TA_CENTER, sa=ET)))
    e.append(Paragraph(t("seu_perfil", lang), _estilo("S", FONTE, 18, GOLD, TA_CENTER, sa=10)))
    e.append(Spacer(1, 20))
    e.append(Paragraph(nome.upper(), _estilo("NOME", FN, 16, DARK, TA_CENTER, sa=4)))
    e.append(Paragraph(bd_str, _estilo("DATA", FONTE, 11, GRAY, TA_CENTER, sa=EL)))
    e.append(Paragraph(BOAS_VINDAS.get(lang, BOAS_VINDAS["pt"]),
                       _estilo("BV", FONTE, 10, GRAY, TA_CENTER, sa=EL)))
    e.append(Spacer(1, 30))
    e.append(Paragraph(f"{t('caminho_vida', lang)}: <b>{lp}</b> — {desc_cam}",
                       _estilo("CV", FN, 12, GOLD, TA_CENTER, sa=EL)))
    e.append(PageBreak())
    # NÚMEROS PRINCIPAIS
    e.append(Paragraph(S.get("numeros_principais", "Seus Números Principais"),
                       _estilo("SEC", FN, 18, GOLD, TA_LEFT, sb=EL, sa=LINHA)))
    chaves = [("life_path", "caminho_vida"), ("expression", "expressao"),
              ("soul_urge", "motivacao"), ("personality", "personalidade"),
              ("destiny", "destino")]
    linhas = [[t("numero", lang), t("significado", lang), t("valor", lang)]]
    for k, lbl in chaves:
        v = data[k]
        sig = SIG.get(v, (t("nenhum", lang), "", "", ""))
        linhas.append([t(lbl, lang), sig[0], str(v)])
    tbl = Table(linhas, colWidths=[180, 220, 80])  # 480pt <= 495pt
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GOLD), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTSIZE", (0, 0), (-1, -1), 9), ("FONTNAME", (0, 0), (-1, -1), FONTE),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (2, 0), (2, -1), "CENTER"),
        ("BACKGROUND", (0, 1), (-1, -1), LGRAY), ("TEXTCOLOR", (0, 1), (-1, -1), DARK),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    e.append(tbl)
    e.append(Spacer(1, LINHA))
    # ANÁLISE DETALHADA
    e.append(Paragraph(t("analise", lang), _estilo("SEC", FN, 18, GOLD, TA_LEFT, sb=LINHA, sa=LINHA)))
    for k, lbl in chaves:
        v = data[k]
        nm, pos, neg, licao = SIG.get(v, (t("nenhum", lang), "", "", ""))
        e.append(Paragraph(f"<b>{t(lbl, lang)} {v} — {nm}</b>",
                           _estilo("BL", FN, 10, DARK, TA_LEFT, sa=3)))
        if pos:
            e.append(Paragraph(f"<b>{t('positivo', lang)}:</b> {pos}",
                               _estilo("JP", FONTE, 9, DARK, TA_LEFT, sa=2)))
        if neg:
            e.append(Paragraph(f"<b>{t('negativo', lang)}:</b> {neg}",
                               _estilo("JP", FONTE, 9, DARK, TA_LEFT, sa=2)))
        if licao:
            e.append(Paragraph(f"<b>{t('licao', lang)}:</b> {licao}",
                               _estilo("JP", FONTE, 9, DARK, TA_LEFT, sa=6)))
    e.append(PageBreak())
    # CAMINHO DA VIDA E CICLOS
    e.append(Paragraph(S.get("caminho_ciclos", "Caminho da Vida e Ciclos"),
                       _estilo("SEC", FN, 18, GOLD, TA_LEFT, sb=LINHA, sa=LINHA)))
    e.append(Paragraph(f"<b>{t('caminho_vida', lang)} {lp}:</b> {desc_cam}",
                       _estilo("J", FONTE, 11, DARK, TA_JUSTIFY, sa=LINHA)))
    try:
        dt = dp.parse(bd_str)
        mes, dia, ano = reduzir(dt.month), reduzir(dt.day), reduzir(dt.year)
    except Exception:
        mes, dia, ano = 0, 0, 0
    ciclos = [[t("formativo", lang), t("produtivo", lang), t("colheita", lang)],
              [P[0], P[1], P[2]],
              [str(mes), str(dia), str(ano)]]
    tbl3 = Table(ciclos, colWidths=[165, 165, 165])  # 495pt
    tbl3.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GOLD), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTSIZE", (0, 0), (-1, -1), 9), ("FONTNAME", (0, 0), (-1, -1), FONTE),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BACKGROUND", (0, 1), (-1, -1), LGRAY), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    e.append(tbl3)
    e.append(Spacer(1, LINHA))
    # DESAFIOS E REALIZAÇÕES
    e.append(Paragraph(S.get("desafios_realizacoes", "Desafios e Realizações"),
                       _estilo("SEC", FN, 18, GOLD, TA_LEFT, sb=LINHA, sa=LINHA)))
    try:
        dt = dp.parse(bd_str)
        m_r, d_r, a_r = reduzir(dt.month), reduzir(dt.day), reduzir(dt.year)
        d1, d2 = abs(m_r - d_r), abs(d_r - a_r)
        dp_ = abs(d1 - d2)
    except Exception:
        d1, d2, dp_ = 0, 0, 0
    desafios = [[t("menor1", lang), t("menor2", lang), t("principal", lang)],
                [str(d1), str(d2), str(dp_)],
                [f"|{m_r} - {d_r}|", f"|{d_r} - {a_r}|", f"|{d1} - {d2}|"]]
    tbl4 = Table(desafios, colWidths=[165, 165, 165])  # 495pt
    tbl4.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GOLD), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTSIZE", (0, 0), (-1, -1), 9), ("FONTNAME", (0, 0), (-1, -1), FONTE),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BACKGROUND", (0, 1), (-1, -1), LGRAY), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    e.append(tbl4)
    e.append(Spacer(1, LINHA))
    if DES.get(dp_):
        e.append(Paragraph(f"<b>{t('licao', lang)}:</b> {DES.get(dp_)}",
                           _estilo("J", FONTE, 10, DARK, TA_JUSTIFY, sa=LINHA)))
    e.append(Paragraph(f"<b>{t('realizacoes', lang)}</b>",
                       _estilo("BL", FN, 11, GOLD, TA_LEFT, sb=LINHA, sa=LINHA)))
    try:
        dt = dp.parse(bd_str)
        m2, d2r, a2 = reduzir(dt.month), reduzir(dt.day), reduzir(dt.year)
        r1 = reduzir(m2 + d2r)
        r2 = reduzir(d2r + a2)
        r3 = reduzir(r1 + r2)
        r4 = reduzir(m2 + a2)
    except Exception:
        r1, r2, r3, r4 = 0, 0, 0, 0
    realiz = [[t("realizacoes", lang), RH[0], RH[1], t("numero", lang)],
              [t("juventude", lang), P[0], "0 a 28/36", str(r1)],
              [t("vida_adulta", lang), P[1], "28/36 a 54/63", str(r2)],
              [t("maturidade", lang), P[2], "54/63 +", str(r3)],
              [t("legado", lang), "—", "—", str(r4)]]
    tblR = Table(realiz, colWidths=[120, 130, 90, 80])  # 420pt <= 495pt
    tblR.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GOLD), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTSIZE", (0, 0), (-1, -1), 8), ("FONTNAME", (0, 0), (-1, -1), FONTE),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (3, 0), (3, -1), "CENTER"),
        ("BACKGROUND", (0, 1), (-1, -1), LGRAY), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    e.append(tblR)
    e.append(Spacer(1, LINHA))
    e.append(PageBreak())
    # GRADE DE INCLUSÃO
    e.append(Paragraph(t("grade", lang), _estilo("SEC", FN, 18, GOLD, TA_LEFT, sb=LINHA, sa=LINHA)))
    grid = calc_grid(nome)
    grid_data = [["1", t("vibracao", lang), "2", t("vibracao", lang), "3", t("vibracao", lang)]]
    for i in range(3):
        n1, n2, n3 = i * 3 + 1, i * 3 + 2, i * 3 + 3
        grid_data.append([str(n1), str(grid.get(n1, 0)),
                          str(n2), str(grid.get(n2, 0)),
                          str(n3), str(grid.get(n3, 0))])
    tbl5 = Table(grid_data, colWidths=[40, 80, 40, 80, 40, 80])  # 360pt
    tbl5.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GOLD), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTSIZE", (0, 0), (-1, -1), 9), ("FONTNAME", (0, 0), (-1, -1), FONTE),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BACKGROUND", (0, 1), (-1, -1), LGRAY), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    e.append(tbl5)
    e.append(Spacer(1, LINHA))
    # VIBRAÇÃO DO DIA
    e.append(Paragraph(t("vibracao", lang), _estilo("SEC", FN, 18, GOLD, TA_LEFT, sb=LINHA, sa=LINHA)))
    try:
        dt = dp.parse(bd_str)
        vib_dia = reduzir(dt.day)
        if VIB.get(vib_dia):
            e.append(Paragraph(f"<b>{t('vibracao', lang)}: {vib_dia}</b> — {VIB.get(vib_dia)}",
                               _estilo("J", FONTE, 10, DARK, TA_JUSTIFY, sa=LINHA)))
    except Exception:
        pass
    e.append(Spacer(1, LINHA))
    # ENCERRAMENTO
    e.append(Paragraph(T.get("entrega", ""), _estilo("J", FONTE, 10, GRAY, TA_CENTER, sa=LINHA)))
    e.append(Paragraph("© A1ELOS Assessoria e Consultoria",
                       _estilo("F", FONTE, 8, GRAY, TA_CENTER)))
    doc.build(e, onFirstPage=_cabecalho_pagina, onLaterPages=_cabecalho_pagina)
    return path

# ═══════════════════════════════════════════
# NOME DE URNA (traduzido)
# ═══════════════════════════════════════════
def pdf_urna(nc, cl, resultados, sugestoes, lang="pt"):
    T = PDF_TEXTS.get(lang, PDF_TEXTS["pt"])
    E = ENERGIA_LBL.get(lang, "Energia")
    path = os.path.join(TMP, f"u_{uuid.uuid4().hex[:8]}.pdf")
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=50, rightMargin=50,
                            topMargin=45, bottomMargin=45)
    e = []
    e.append(Spacer(1, 25))
    e.append(Paragraph(T.get("t_urna", "VALIDACAO DE NOME DE URNA"),
                       _estilo("T", FN, TAM_T, GOLD, TA_CENTER, sa=ET * 0.5)))
    e.append(Paragraph(nc.title(), _estilo("N", FN, TAM_C + 2, DARK, TA_CENTER, sa=4)))
    e.append(Paragraph(f"{T.get('cargo', 'Cargo')}: {cl}",
                       _estilo("D", FONTE, TAM_C - 2, GRAY, TA_CENTER, sa=LINHA)))
    e.append(Paragraph(BOAS_VINDAS.get(lang, BOAS_VINDAS["pt"]),
                       _estilo("BV", FONTE, 10, DARK, TA_JUSTIFY, sa=LINHA)))
    for r in resultados:
        ic = "✅" if r["eh_ideal"] else "❌"
        e.append(Paragraph(f"{ic} {r['nome']} — {E} {r['energia']}",
                           _estilo("B", FN, TAM_C - 1, DARK, TA_LEFT, sa=LINHA * 0.3)))
        if r["letras"]:
            ls = ", ".join(f'{l["letra"]}={l["valor"]}' for l in r["letras"])
            e.append(Paragraph(f"{ls} → {r['soma']} → {r['energia']}",
                               _estilo("C", FONTE, TAM_C - 2, GRAY, TA_LEFT, sa=LINHA * 0.2)))
        e.append(Paragraph(r["explicacao"], _estilo("J", FONTE, TAM_C - 1, DARK,
                                                    TA_JUSTIFY, sa=LINHA * 0.4)))
    if sugestoes:
        e.append(Paragraph(T.get("sugestoes", "Sugestões:"),
                           _estilo("SU", FN, 18, GOLD, TA_LEFT, sb=LINHA, sa=LINHA)))
        for s in sugestoes[:3]:
            e.append(Paragraph(f'{s["nome"]} — {E} {s["energia"]}',
                               _estilo("X", FONTE, TAM_C, DARK, TA_LEFT, sa=LINHA * 0.3)))
    e.append(Paragraph("© A1ELOS", _estilo("F", FONTE, 8, GRAY, TA_CENTER)))
    doc.build(e, onFirstPage=_cabecalho_pagina, onLaterPages=_cabecalho_pagina)
    return path

# ═══════════════════════════════════════════
# NÚMERO ELEITORAL (traduzido)
# ═══════════════════════════════════════════
def pdf_eleitoral(ss, cl, sugestoes, ne=None, lang="pt"):
    T = PDF_TEXTS.get(lang, PDF_TEXTS["pt"])
    S = PDF_SECOES.get(lang, PDF_SECOES["pt"])
    E = ENERGIA_LBL.get(lang, "Energia")
    path = os.path.join(TMP, f"e_{uuid.uuid4().hex[:8]}.pdf")
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=50, rightMargin=50,
                            topMargin=45, bottomMargin=45)
    e = []
    e.append(Spacer(1, 25))
    e.append(Paragraph(T.get("t_eleitoral", "NUMERO ELETTORALE"),
                       _estilo("T", FN, TAM_T, GOLD, TA_CENTER, sa=ET * 0.5)))
    e.append(Paragraph(f"{T.get('cargo', 'Cargo')}: {cl} | {T.get('numero', 'Numero')}: {ss}",
                       _estilo("D", FONTE, TAM_C - 2, GRAY, TA_CENTER, sa=LINHA)))
    e.append(Paragraph(BOAS_VINDAS.get(lang, BOAS_VINDAS["pt"]),
                       _estilo("BV", FONTE, 10, DARK, TA_JUSTIFY, sa=LINHA)))
    e.append(Paragraph(S.get("como_calculamos", "Como calculamos?"),
                       _estilo("SE", FN, 18, GOLD, TA_LEFT, sb=LINHA, sa=LINHA)))
    e.append(Paragraph(T.get("entrega", ""), _estilo("J", FONTE, TAM_C - 1, DARK,
                                                     TA_JUSTIFY, sa=LINHA * 0.4)))
    e.append(Paragraph(S.get("por_que_energia_8", "Por que a energia 8?"),
                       _estilo("SE", FN, 18, GOLD, TA_LEFT, sb=LINHA, sa=LINHA)))
    e.append(Paragraph(f"{E} 8: {T.get('op8', 'Energia 8 - IDEAL')}",
                       _estilo("J", FONTE, TAM_C - 1, DARK, TA_JUSTIFY, sa=LINHA * 0.4)))
    ideais = [s for s in sugestoes if s.get("ideal")]
    fallbacks = [s for s in sugestoes if not s.get("ideal")]
    if ideais:
        e.append(Paragraph(S.get("energia_8_ideal", "Energia 8 - IDEAL:"),
                           _estilo("B", FN, TAM_C - 1, DARK, TA_LEFT, sa=LINHA * 0.3)))
        for s in ideais:
            e.append(Paragraph(f"✅ {s['numero']} — {E} 8",
                               _estilo("X", FONTE, TAM_C, colors.HexColor("#4CAF50"),
                                       TA_LEFT, sa=LINHA * 0.2)))
            if "explicacao_calculo" in s:
                e.append(Paragraph(f"{T.get('calculo', 'Calculo')}: {s['explicacao_calculo']}",
                                   _estilo("C", FONTE, TAM_C - 2, GRAY, TA_LEFT, sa=LINHA * 0.2)))
    if fallbacks:
        e.append(Paragraph(S.get("alternativas", "Alternativas:"),
                           _estilo("B", FN, TAM_C - 1, DARK, TA_LEFT, sb=LINHA * 0.5, sa=LINHA * 0.3)))
        for s in fallbacks:
            e.append(Paragraph(f"{s['numero']} — {E} {s['energia']} — {s.get('nome_energia', '')}",
                               _estilo("X", FONTE, TAM_C - 1, DARK, TA_LEFT, sa=LINHA * 0.2)))
    if ne:
        e.append(Paragraph(f"{T.get('num_existente', 'Numero existente')}:",
                           _estilo("SE", FN, 18, GOLD, TA_LEFT, sb=LINHA, sa=LINHA)))
        e.append(Paragraph(f"{ne['numero']} — {E} {ne['energia']}",
                           _estilo("X", FONTE, TAM_C, DARK, TA_LEFT, sa=LINHA * 0.3)))
        if ne["energia"] == 8:
            e.append(Paragraph(f"{E} 8! ✓", _estilo("J", FONTE, TAM_C - 1, DARK,
                                                    TA_JUSTIFY, sa=LINHA * 0.4)))
        else:
            e.append(Paragraph(f"{E} {ne['energia']} — 8.", _estilo("J", FONTE, TAM_C - 1,
                                                                    DARK, TA_JUSTIFY, sa=LINHA * 0.4)))
    e.append(Paragraph("© A1ELOS — Numerologia aplicada ao sucesso eleitoral",
                       _estilo("F", FONTE, 8, GRAY, TA_CENTER, sb=EL * 2)))
    doc.build(e, onFirstPage=_cabecalho_pagina, onLaterPages=_cabecalho_pagina)
    return path

# ═══════════════════════════════════════════
# PRODUTOS GENÉRICOS (19 produtos, traduzido + conteúdo do livro)
# ═══════════════════════════════════════════
def pdf_produto(produto, dados, nome, bd_str, lang="pt"):
    T = PDF_TEXTS.get(lang, PDF_TEXTS["pt"])
    path = os.path.join(TMP, f"p_{uuid.uuid4().hex[:8]}.pdf")
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=50, rightMargin=50,
                            topMargin=45, bottomMargin=45)
    titulo = PRODUTOS.get(lang, PRODUTOS["pt"]).get(produto, produto).upper()
    e = []
    e.append(Spacer(1, 20))
    e.append(Paragraph(titulo, _estilo("T", FN, 24, GOLD, TA_CENTER, sa=ET)))
    e.append(Paragraph(t("seu_perfil", lang), _estilo("S", FONTE, 14, GOLD, TA_CENTER, sa=4)))
    e.append(Paragraph(nome.upper(), _estilo("N", FN, 14, DARK, TA_CENTER, sa=4)))
    e.append(Paragraph(bd_str, _estilo("D", FONTE, 10, GRAY, TA_CENTER, sa=LINHA)))
    e.append(Paragraph(BOAS_VINDAS.get(lang, BOAS_VINDAS["pt"]),
                       _estilo("BV", FONTE, 10, DARK, TA_JUSTIFY, sa=LINHA)))
    chaves = [("life_path", "caminho_vida"), ("expression", "expressao"),
              ("soul_urge", "motivacao"), ("personality", "personalidade"),
              ("destiny", "destino")]
    linhas = [[t("numero", lang), t("valor", lang), t("significado", lang)]]
    for k, lbl in chaves:
        v = dados[k]
        sig = SIG.get(v, (t("nenhum", lang), "", "", ""))
        linhas.append([t(lbl, lang), str(v), sig[0]])
    tbl = Table(linhas, colWidths=[180, 60, 220])  # 460pt <= 495pt
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GOLD), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTSIZE", (0, 0), (-1, -1), 9), ("FONTNAME", (0, 0), (-1, -1), FONTE),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (1, 0), (1, -1), "CENTER"), ("ALIGN", (2, 0), (2, -1), "LEFT"),
        ("BACKGROUND", (0, 1), (-1, -1), LGRAY), ("TEXTCOLOR", (0, 1), (-1, -1), DARK),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    e.append(tbl)
    e.append(Spacer(1, LINHA))
    # ANÁLISE DETALHADA — conteúdo do livro (SIG/CAM/DES/VIB)
    e.append(Paragraph(t("analise", lang), _estilo("SEC", FN, 18, GOLD, TA_LEFT, sb=LINHA, sa=LINHA)))
    for k, lbl in chaves:
        v = dados[k]
        nm, pos, neg, licao = SIG.get(v, (t("nenhum", lang), "", "", ""))
        e.append(Paragraph(f"<b>{t(lbl, lang)} {v} — {nm}</b>",
                           _estilo("BL", FN, 10, DARK, TA_LEFT, sa=3)))
        if pos:
            e.append(Paragraph(f"<b>{t('positivo', lang)}:</b> {pos}",
                               _estilo("JP", FONTE, 9, DARK, TA_LEFT, sa=2)))
        if neg:
            e.append(Paragraph(f"<b>{t('negativo', lang)}:</b> {neg}",
                               _estilo("JP", FONTE, 9, DARK, TA_LEFT, sa=2)))
        if licao:
            e.append(Paragraph(f"<b>{t('licao', lang)}:</b> {licao}",
                               _estilo("JP", FONTE, 9, DARK, TA_LEFT, sa=6)))
    lp = dados.get("life_path", 0)
    _, desc_cam = CAM.get(lp, ("", ""))
    if desc_cam:
        e.append(Spacer(1, LINHA))
        e.append(Paragraph(f"<b>{t('caminho_vida', lang)} {lp}:</b> {desc_cam}",
                           _estilo("J", FONTE, 10, DARK, TA_JUSTIFY, sa=LINHA)))
    try:
        dt = dp.parse(bd_str)
        vib_dia = reduzir(dt.day)
        if VIB.get(vib_dia):
            e.append(Spacer(1, LINHA))
            e.append(Paragraph(f"<b>{t('vibracao', lang)}: {vib_dia}</b> — {VIB.get(vib_dia)}",
                               _estilo("J", FONTE, 10, DARK, TA_JUSTIFY, sa=LINHA)))
    except Exception:
        pass
    e.append(Spacer(1, LINHA))
    e.append(Paragraph(T.get("entrega", ""), _estilo("J", FONTE, 8, GRAY, TA_CENTER, sa=6)))
    e.append(Paragraph("© A1ELOS Assessoria e Consultoria",
                       _estilo("F", FONTE, 8, GRAY, TA_CENTER)))
    doc.build(e, onFirstPage=_cabecalho_pagina, onLaterPages=_cabecalho_pagina)
    return path
