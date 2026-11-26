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
from calc_service import reduzir, calc_grid, calc_ciclos, calc_desafios, calc_realizacoes
from dicionarios import SIG, CAM, DES, VIB, t, PRODUTOS, PDF_TEXTS, PDF_SECOES, BOAS_VINDAS, PERIODOS, REALIZ_HEAD
from dicionarios import get_sig, get_cam, get_compat, get_dual
from reportlab.pdfgen import canvas as _rl_canvas
from dicionarios import get_sig, get_cam, get_compat, get_dual
from dicionarios import get_sig_full, get_des, get_vib

# ---- Identidade visual (Padrão Mínimo de Qualidade Total) ----
GOLD = colors.HexColor("#C9A94E")
DARK = colors.HexColor("#1a1a1a")
LGRAY = colors.HexColor("#f5f5f0")
WHITE = colors.white
GRAY = colors.HexColor("#888888")
from fontes import fonte_para, preparar_texto, registrar_tudo
registrar_tudo()
FONTE = "DejaVu"
FN = "DejaVu-Bold"
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

ALERTA_DUALIDADE = (
    "A dualidade da relação permite convergência e divergência e a "
    "instabilidade é uma situação permanente, não havendo uma condição única "
    "e estável nessa relação, mas um cenário de permanente condicionamento "
    "de posturas individuais de ambas as partes."
)

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
    _fr, _fb = fonte_para(lang)
    FONTE, FN = _fr, _fb
    from dicionarios import get_sig, t as _t
    from fontes import preparar_texto as _prep
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
        v = data.get(k, 0)
        sig = get_sig(v, lang)
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
        v = data.get(k, 0)
        sig = get_sig(v, lang)
        e.append(Paragraph(f"<b>{_prep(t(lbl, lang), lang)}:</b> {v} — {_prep(sig[0], lang)}",
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
    _fr, _fb = fonte_para(lang)
    FONTE, FN = _fr, _fb
    from dicionarios import get_sig, get_cam, get_sig_full, get_des, get_vib
    from fontes import preparar_texto as _prep
    S = PDF_SECOES.get(lang, PDF_SECOES["pt"])
    P = PERIODOS.get(lang, PERIODOS["pt"])
    RH = REALIZ_HEAD.get(lang, REALIZ_HEAD["pt"])
    path = os.path.join(TMP, f"p17_{uuid.uuid4().hex[:8]}.pdf")
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=50, rightMargin=50,
                            topMargin=45, bottomMargin=45)
    e = []
    lp = data["life_path"]
    _, desc_cam = get_cam(lp, lang)
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
        v = data.get(k, 0)
        sig = get_sig(v, lang)        
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
        v = data.get(k, 0)
        nm, pos, neg, licao = get_sig_full(v, lang)
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
        desafios_calc = calc_desafios(dt.day, dt.month, dt.year)
        d1, d2, dp_ = desafios_calc["menor1"], desafios_calc["menor2"], desafios_calc["principal"]
        mes_r = reduzir(dt.month)
        dia_r = reduzir(dt.day)
        ano_r = reduzir(dt.year)
    except Exception:
        d1, d2, dp_ = 0, 0, 0
        mes_r, dia_r, ano_r = 0, 0, 0
    desafios = [[t("menor1", lang), t("menor2", lang), t("principal", lang)],
                [str(d1), str(d2), str(dp_)],
                [f"|{mes_r} - {dia_r}|", f"|{dia_r} - {ano_r}|", f"|{d1} - {d2}|"]]
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
    _des_txt = get_des(dp_, lang)
    if _des_txt:
        e.append(Paragraph(f"<b>{t('licao', lang)}:</b> {_des_txt}",
                           _estilo("J", FONTE, 10, DARK, TA_JUSTIFY, sa=LINHA)))
    e.append(Paragraph(f"<b>{t('realizacoes', lang)}</b>",
                       _estilo("BL", FN, 11, GOLD, TA_LEFT, sb=LINHA, sa=LINHA)))
    try:
        dt = dp.parse(bd_str)
        realiz_calc = calc_realizacoes(dt.day, dt.month, dt.year)
        r1, r2, r3, r4 = realiz_calc["r1"], realiz_calc["r2"], realiz_calc["r3"], realiz_calc["r4"]
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
        vib_txt = get_vib(vib_dia, lang)
        if vib_txt:
            e.append(Paragraph(f"<b>{t('vibracao', lang)}: {vib_dia}</b> — {vib_txt}",
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

# ===== PRODUTOS DA IA DE NOMES — 3 NOMES + 4a OPCAO (19/11/2026) =====
IA_TXT = {
 "pt": {"t":"Pesquisa IA de Nomes","ea":"Energia alvo","tp":"Tipo","nm":"Nome","en":"Energia",
        "sx":"Sexo","ok":"Atingiu a energia","no":"Não atingiu","sg":"Sugestão da IA",
        "rm":"Os nomes são analisados em escrita latina porque a numerologia pitagórica atribui valor apenas às 26 letras A–Z. Nomes em outros alfabetos são romanizados antes do cálculo."},
 "en": {"t":"AI Name Search","ea":"Target energy","tp":"Type","nm":"Name","en":"Energy",
        "sx":"Sex","ok":"Reached the energy","no":"Did not reach","sg":"AI suggestion",
        "rm":"Names are analyzed in Latin script because Pythagorean numerology assigns value only to the 26 letters A–Z. Names in other alphabets are romanized before calculation."},
 "es": {"t":"Búsqueda IA de Nombres","ea":"Energía objetivo","tp":"Tipo","nm":"Nombre","en":"Energía",
        "sx":"Sexo","ok":"Alcanzó la energía","no":"No alcanzó","sg":"Sugerencia de la IA",
        "rm":"Los nombres se analizan en escritura latina porque la numerología pitagórica asigna valor solo a las 26 letras A–Z. Los nombres en otros alfabetos se romanizan antes del cálculo."},
 "it": {"t":"Ricerca IA Nomi","ea":"Energia obiettivo","tp":"Tipo","nm":"Nome","en":"Energia",
        "sx":"Sesso","ok":"Ha raggiunto l'energia","no":"Non ha raggiunto","sg":"Suggerimento IA",
        "rm":"I nomi sono analizzati in scrittura latina perché la numerologia pitagorica assegna valore solo alle 26 lettere A–Z. I nomi in altri alfabeti vengono romanizzati prima del calcolo."},
 "fr": {"t":"Recherche IA de Noms","ea":"Énergie cible","tp":"Type","nm":"Nom","en":"Énergie",
        "sx":"Sexe","ok":"A atteint l'énergie","no":"N'a pas atteint","sg":"Suggestion IA",
        "rm":"Les noms sont analysés en écriture latine car la numérologie pythagoricienne n'attribue de valeur qu'aux 26 lettres A–Z. Les noms dans d'autres alphabets sont romanisés avant le calcul."},
 "de": {"t":"KI-Namenssuche","ea":"Zielenergie","tp":"Typ","nm":"Name","en":"Energie",
        "sx":"Geschlecht","ok":"Energie erreicht","no":"Nicht erreicht","sg":"KI-Vorschlag",
        "rm":"Namen werden in lateinischer Schrift analysiert, da die pythagoreische Numerologie nur den 26 Buchstaben A–Z einen Wert zuweist. Namen in anderen Alphabeten werden vor der Berechnung romanisiert."},
 "ja": {"t":"AI名前検索","ea":"目標エネルギー","tp":"タイプ","nm":"名前","en":"エネルギー",
        "sx":"性別","ok":"エネルギーに到達","no":"到達せず","sg":"AIの提案",
        "rm":"名前はラテン文字で分析されます。ピタゴラス数秘術はA–Zの26文字にのみ数値を割り当てるためです。他の文字体系の名前は計算前にローマ字化されます。"},
 "zh": {"t":"AI名字搜索","ea":"目标能量","tp":"类型","nm":"名字","en":"能量",
        "sx":"性别","ok":"达到能量","no":"未达到","sg":"AI建议",
        "rm":"名字以拉丁字母分析，因为毕达哥拉斯数字学只为A–Z这26个字母赋予数值。其他文字系统的名字在计算前会被罗马化。"},
 "ru": {"t":"ИИ-поиск имён","ea":"Целевая энергия","tp":"Тип","nm":"Имя","en":"Энергия",
        "sx":"Пол","ok":"Достигнута энергия","no":"Не достигнута","sg":"Предложение ИИ",
        "rm":"Имена анализируются в латинской записи, так как пифагорейская нумерология придаёт значение только 26 буквам A–Z. Имена в других алфавитах транслитерируются перед расчётом."},
 "id": {"t":"Pencarian Nama AI","ea":"Energi target","tp":"Jenis","nm":"Nama","en":"Energi",
        "sx":"Jenis kelamin","ok":"Mencapai energi","no":"Tidak mencapai","sg":"Saran AI",
        "rm":"Nama dianalisis dalam aksara Latin karena numerologi Pythagoras hanya memberi nilai pada 26 huruf A–Z. Nama dalam aksara lain diromanisasi sebelum perhitungan."},
 "tr": {"t":"AI İsim Arama","ea":"Hedef enerji","tp":"Tür","nm":"İsim","en":"Enerji",
        "sx":"Cinsiyet","ok":"Enerjiye ulaştı","no":"Ulaşmadı","sg":"AI önerisi",
        "rm":"İsimler Latin alfabesinde analiz edilir çünkü Pisagor numerolojisi yalnızca A–Z arasındaki 26 harfe değer verir. Diğer alfabelerdeki isimler hesaplamadan önce romanize edilir."},
 "vi": {"t":"Tìm Kiếm Tên AI","ea":"Năng lượng mục tiêu","tp":"Loại","nm":"Tên","en":"Năng lượng",
        "sx":"Giới tính","ok":"Đạt năng lượng","no":"Không đạt","sg":"Gợi ý AI",
        "rm":"Tên được phân tích bằng chữ Latinh vì thần số học Pythagoras chỉ gán giá trị cho 26 chữ cái A–Z. Tên trong bảng chữ cái khác được La-tinh hóa trước khi tính."},
 "he": {"t":"חיפוש שמות AI","ea":"אנרגיית יעד","tp":"סוג","nm":"שם","en":"אנרגיה",
        "sx":"מין","ok":"הגיע לאנרגיה","no":"לא הגיע","sg":"הצעת AI",
        "rm":"השמות מנותחים בכתב לטיני מכיוון שהנומרולוגיה הפיתגורית מייחסת ערך רק ל-26 האותיות A–Z. שמות באלפבית אחר עוברים תעתיק לפני החישוב."},
 "ar": {"t":"بحث الأسماء بالذكاء الاصطناعي","ea":"الطاقة المستهدفة","tp":"النوع","nm":"الاسم","en":"الطاقة",
        "sx":"الجنس","ok":"وصل إلى الطاقة","no":"لم يصل","sg":"اقتراح الذكاء الاصطناعي",
        "rm":"تُحلَّل الأسماء بالحرف اللاتيني لأن علم الأعداد الفيثاغوري يمنح قيمة للحروف الـ26 من A إلى Z فقط. تُحوَّل الأسماء بالأبجدية الأخرى إلى الحرف اللاتيني قبل الحساب."},
}

# Nome do tipo traduzido (o valor cru e "cao", "gato"...)
TIPO_NOME = {
 "cao":     {"pt":"Cão","en":"Dog","es":"Perro","it":"Cane","fr":"Chien","de":"Hund",
             "ja":"犬","zh":"狗","ru":"Собака","id":"Anjing","tr":"Köpek","vi":"Chó","he":"כלב","ar":"كلب"},
 "gato":    {"pt":"Gato","en":"Cat","es":"Gato","it":"Gatto","fr":"Chat","de":"Katze",
             "ja":"猫","zh":"猫","ru":"Кошка","id":"Kucing","tr":"Kedi","vi":"Mèo","he":"חתול","ar":"قطة"},
 "passaro": {"pt":"Pássaro","en":"Bird","es":"Pájaro","it":"Uccello","fr":"Oiseau","de":"Vogel",
             "ja":"鳥","zh":"鸟","ru":"Птица","id":"Burung","tr":"Kuş","vi":"Chim","he":"ציפור","ar":"طائر"},
 "reptil":  {"pt":"Réptil","en":"Reptile","es":"Reptil","it":"Rettile","fr":"Reptile","de":"Reptil",
             "ja":"爬虫類","zh":"爬行动物","ru":"Рептилия","id":"Reptil","tr":"Sürüngen","vi":"Bò sát","he":"זוחל","ar":"زاحف"},
 "outro":   {"pt":"Outro","en":"Other","es":"Otro","it":"Altro","fr":"Autre","de":"Andere",
             "ja":"その他","zh":"其他","ru":"Другое","id":"Lainnya","tr":"Diğer","vi":"Khác","he":"אחר","ar":"آخر"},
}
SEXO_NOME = {
 "pt":{"f":"Fêmea","m":"Macho","":"Indefinido"},  "en":{"f":"Female","m":"Male","":"Undefined"},
 "es":{"f":"Hembra","m":"Macho","":"Indefinido"}, "it":{"f":"Femmina","m":"Maschio","":"Indefinito"},
 "fr":{"f":"Femelle","m":"Mâle","":"Indéfini"},   "de":{"f":"Weibchen","m":"Männchen","":"Unbestimmt"},
 "ja":{"f":"メス","m":"オス","":"未指定"},          "zh":{"f":"母","m":"公","":"未指定"},
 "ru":{"f":"Самка","m":"Самец","":"Не указан"},   "id":{"f":"Betina","m":"Jantan","":"Tidak tentu"},
 "tr":{"f":"Dişi","m":"Erkek","":"Belirsiz"},     "vi":{"f":"Cái","m":"Đực","":"Không xác định"},
 "he":{"f":"נקבה","m":"זכר","":"לא צוין"},        "ar":{"f":"أنثى","m":"ذكر","":"غير محدد"},
}

def _ia_fonte(lang):
    """Fonte (regular, bold) para o idioma; cai em Helvetica se indisponivel."""
    try:
        mapa = {
            "ja": ("HeiseiKakuGo-W5", "HeiseiKakuGo-W5"),
            "zh": ("STSong-Light", "STSong-Light"),
            "he": ("NotoSansHebrew", "NotoSansHebrew-Bold"),
            "ar": ("NotoNaskhArabic", "NotoNaskhArabic-Bold"),
        }
        if lang in mapa:
            return mapa[lang]
        return ("DejaVu", "DejaVu-Bold")
    except Exception:
        return ("Helvetica", "Helvetica-Bold")


def _pdf_ia_nomes(produto, dados, lang, ia):
    """3 avaliacoes + 4a opcao (sugestao) + sexo + descricao da energia."""
    import tempfile, uuid, os
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from energia_desc import descrever

    T = IA_TXT.get(lang) or IA_TXT["pt"]
    reg, bold = _ia_fonte(lang)
    GOLD = colors.HexColor("#B8860B")
    DARK = colors.HexColor("#222222")
    GRAY = colors.HexColor("#777777")
    LGRAY = colors.HexColor("#f0f0f0")
    CREAM = colors.HexColor("#FDF3D7")

    def est(tam, b=False, cor=DARK, alinh=TA_LEFT, depois=0):
        return ParagraphStyle("e", fontName=(bold if b else reg), fontSize=tam,
                              textColor=cor, alignment=alinh, spaceAfter=depois,
                              leading=tam * 1.45)

    tipo_id = ia.get("tipo") or dados.get("tipo") or ""
    tipo_lbl = (TIPO_NOME.get(tipo_id) or {}).get(lang) or tipo_id
    sexo = ia.get("sexo") or dados.get("sexo") or ""
    sexo_lbl = (SEXO_NOME.get(lang) or SEXO_NOME["pt"]).get(sexo, "")
    alvo = ia.get("energia_alvo", "")

    path = os.path.join(tempfile.gettempdir(), "p_%s_%s.pdf" % (produto, uuid.uuid4().hex[:8]))
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=50, rightMargin=50,
                            topMargin=40, bottomMargin=30)
    e = []
    e.append(Spacer(1, 10))
    e.append(Paragraph(T["t"].upper(), est(17, True, GOLD, TA_CENTER, 4)))
    e.append(Paragraph(str(ia.get("escolhido") or ""), est(14, True, DARK, TA_CENTER, 2)))

    linha = "%s: %s" % (T["ea"], alvo)
    if tipo_lbl:
        linha += "  ·  %s: %s" % (T["tp"], tipo_lbl)
    if sexo_lbl:
        linha += "  ·  %s: %s" % (T["sx"], sexo_lbl)
    e.append(Paragraph(linha, est(9, False, GRAY, TA_CENTER, 8)))

    # --- descricao da energia escolhida ---
    desc = descrever(alvo, lang)
    if desc:
        e.append(Paragraph(
            "<b>%s %s</b> — %s" % (T["en"], alvo, desc),
            est(10, False, GOLD, TA_CENTER, 12)))

    linhas = [["#", T["nm"], T["en"], T["sx"], T["tp"]]]
    for i, x in enumerate(ia.get("entradas") or [], 1):
        sx_e = (SEXO_NOME.get(lang) or SEXO_NOME["pt"]).get(x.get("sexo", ""), "")
        linhas.append([str(i), x.get("nome", ""), str(x.get("energia", "")), sx_e,
                       (T["ok"] if x.get("bate") else T["no"])])
    sug = ia.get("sugestao")
    if sug:
        sx_s = (SEXO_NOME.get(lang) or SEXO_NOME["pt"]).get(ia.get("sugestao_sexo", ""), "")
        linhas.append(["4", sug, str(alvo), sx_s, T["sg"]])

    if len(linhas) > 1:
        tbl = Table(linhas, colWidths=[24, 160, 58, 64, 170])
        estilo = [
            ("BACKGROUND", (0, 0), (-1, 0), GOLD),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), bold),
            ("FONTNAME", (0, 1), (-1, -1), reg),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
            ("BACKGROUND", (0, 1), (-1, -1), LGRAY),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]
        if sug:
            u = len(linhas) - 1
            estilo.append(("BACKGROUND", (0, u), (-1, u), CREAM))
            estilo.append(("TEXTCOLOR", (4, u), (4, u), GOLD))
            estilo.append(("FONTNAME", (4, u), (4, u), bold))
        tbl.setStyle(TableStyle(estilo))
        e.append(tbl)

    e.append(Spacer(1, 14))
    e.append(Paragraph(T["rm"], est(8, False, GRAY)))
    e.append(Spacer(1, 8))
    e.append(Paragraph("(c) A1ELOS", est(7, False, GRAY, TA_CENTER)))
    doc.build(e)
    return path

# ═══════════════════════════════════════════
# PRODUTOS GENÉRICOS (24 produtos, traduzido + conteúdo do livro)
# ═══════════════════════════════════════════
def pdf_produto(produto, dados, nome, bd_str, lang, dado=""):
    _ia = (dados or {}).get("ia_nomes") if isinstance(dados, dict) else None
    if _ia and (produto or "").startswith("nome_"):
        return _pdf_ia_nomes(produto, dados, lang or "pt", _ia)
    T = PDF_TEXTS.get(lang, PDF_TEXTS["pt"])
    from dicionarios import get_sig, get_cam, get_compat, get_sig_full, get_vib
    from fontes import preparar_texto as _prep
    path = os.path.join(TMP, f"p_{uuid.uuid4().hex[:8]}.pdf")
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=50, rightMargin=50,
                            topMargin=45, bottomMargin=45)
    _ctx = {"familia": "familia",
            "compatibilidade_equipes": "equipe"}.get(produto, "casal")
            
    # ===== FONTES POR IDIOMA (CJK para ja/zh, DejaVu para os demais) =====
    global FONTE, FN
    _fontes_antigas = (FONTE, FN)
    FONTE, FN = fonte_para(lang)
    titulo = PRODUTOS.get(lang, PRODUTOS["pt"]).get(produto, produto).upper()
    e = []
    e.append(Spacer(1, 20))
    e.append(Paragraph(titulo, _estilo("T", FN, 24, GOLD, TA_CENTER, sa=ET)))
    e.append(Paragraph(t("seu_perfil", lang), _estilo("S", FONTE, 14, GOLD, TA_CENTER, sa=4)))
    e.append(Paragraph(nome.upper(), _estilo("N", FN, 14, DARK, TA_CENTER, sa=4)))
    e.append(Paragraph(bd_str, _estilo("D", FONTE, 10, GRAY, TA_CENTER, sa=LINHA)))
    if dado:
        e.append(Paragraph(f"<b>{dado}</b>", _estilo("J", FONTE, 11, DARK, TA_CENTER, sa=LINHA)))
    e.append(Paragraph(BOAS_VINDAS.get(lang, BOAS_VINDAS["pt"]),
                       _estilo("BV", FONTE, 10, DARK, TA_JUSTIFY, sa=LINHA)))
    
    # ===== SEÇÃO ESPECÍFICA DO PRODUTO (cálculo próprio) =====
    # Ativada quando o pay_success usou analisar_imovel/calendario/casal/
    # familia/nome. Cada produto renderiza os campos que a função devolveu.
    L_ESP = {
        "pt": {"mes": "Mês", "energia": "Energia", "soma": "Soma",
               "compatibilidade": "Compatibilidade", "energia_desejada": "Energia desejada",
               "numero": "Número", "membros": "Membros",
               "match": "✓ MATCH: bate com a energia desejada",
               "no_match": "✗ não bate com a energia desejada"},
        "en": {"mes": "Month", "energia": "Energy", "soma": "Sum",
               "compatibilidade": "Compatibility", "energia_desejada": "Desired energy",
               "numero": "Number", "membros": "Members",
               "match": "✓ MATCH: meets the desired energy",
               "no_match": "✗ does not meet the desired energy"},
        "es": {"mes": "Mes", "energia": "Energía", "soma": "Suma",
               "compatibilidade": "Compatibilidad", "energia_desejada": "Energía deseada",
               "numero": "Número", "membros": "Miembros",
               "match": "✓ MATCH: coincide con la energía deseada",
               "no_match": "✗ no coincide con la energía deseada"},
        "it": {"mes": "Mese", "energia": "Energia", "soma": "Somma",
               "compatibilidade": "Compatibilità", "energia_desejada": "Energia desiderata",
               "numero": "Numero", "membros": "Membri",
               "match": "✓ MATCH: corrisponde all'energia desiderata",
               "no_match": "✗ non corrisponde all'energia desiderata"},
        "fr": {"mes": "Mois", "energia": "Énergie", "soma": "Somme",
               "compatibilidade": "Compatibilité", "energia_desejada": "Énergie souhaitée",
               "numero": "Numéro", "membros": "Membres",
               "match": "✓ MATCH: correspond à l'énergie souhaitée",
               "no_match": "✗ ne correspond pas à l'énergie souhaitée"},
        "de": {"mes": "Monat", "energia": "Energie", "soma": "Summe",
               "compatibilidade": "Kompatibilität", "energia_desejada": "Gewünschte Energie",
               "numero": "Nummer", "membros": "Mitglieder",
               "match": "✓ MATCH: entspricht der gewünschten Energie",
               "no_match": "✗ entspricht nicht der gewünschten Energie"},
        "ja": {"mes": "月", "energia": "エネルギー", "soma": "合計",
               "compatibilidade": "相性", "energia_desejada": "希望エネルギー",
               "numero": "番号", "membros": "メンバー",
               "match": "✓ MATCH: 希望するエネルギーと一致",
               "no_match": "✗ 希望するエネルギーと一致しません"},
        "zh": {"mes": "月份", "energia": "能量", "soma": "总和",
               "compatibilidade": "兼容性", "energia_desejada": "期望能量",
               "numero": "号码", "membros": "成员",
               "match": "✓ 匹配：符合期望能量",
               "no_match": "✗ 不符合期望能量"},
        "ru": {"mes": "Месяц", "energia": "Энергия", "soma": "Сумма",
               "compatibilidade": "Совместимость", "energia_desejada": "Желаемая энергия",
               "numero": "Номер", "membros": "Члены",
               "match": "✓ СОВПАДЕНИЕ: соответствует желаемой энергии",
               "no_match": "✗ не соответствует желаемой энергии"},
        "id": {"mes": "Bulan", "energia": "Energi", "soma": "Jumlah",
               "compatibilidade": "Kompatibilitas", "energia_desejada": "Energi yang diinginkan",
               "numero": "Nomor", "membros": "Anggota",
               "match": "✓ COCOK: sesuai energi yang diinginkan",
               "no_match": "✗ tidak sesuai energi yang diinginkan"},
        "tr": {"mes": "Ay", "energia": "Enerji", "soma": "Toplam",
               "compatibilidade": "Uyum", "energia_desejada": "İstenen enerji",
               "numero": "Numara", "membros": "Üyeler",
               "match": "✓ EŞLEŞME: istenen enerjiyle uyuşuyor",
               "no_match": "✗ istenen enerjiyle uyuşmuyor"},
        "vi": {"mes": "Tháng", "energia": "Năng lượng", "soma": "Tổng",
               "compatibilidade": "Tương hợp", "energia_desejada": "Năng lượng mong muốn",
               "numero": "Số", "membros": "Thành viên",
               "match": "✓ KHỚP: khớp với năng lượng mong muốn",
               "no_match": "✗ không khớp với năng lượng mong muốn"},
        "he": {"mes": "חודש", "energia": "אנרגיה", "soma": "סכום",
               "compatibilidade": "תאימות", "energia_desejada": "האנרגיה הרצויה",
               "numero": "מספר", "membros": "חברים",
               "match": "✓ תואם: מתאים לאנרגיה הרצויה",
               "no_match": "✗ אינו מתאים לאנרגיה הרצויה"},
        "ar": {"mes": "الشهر", "energia": "الطاقة", "soma": "المجموع",
               "compatibilidade": "التوافق", "energia_desejada": "الطاقة المطلوبة",
               "numero": "الرقم", "membros": "الأعضاء",
               "match": "✓ تطابق: يطابق الطاقة المطلوبة",
               "no_match": "✗ لا يطابق الطاقة المطلوبة"},
    }
    L = L_ESP.get(lang, L_ESP["en"])
        # ===== RÓTULOS DO CALENDÁRIO (v3) — injeta as 4 chaves nos 14 idiomas =====
    ROTULOS_CAL = {
        "pt": {"energia_pessoal_mes": "Energia Pessoal do Mês", "mes_universal": "Mês Universal",
               "caminho_vida": "Caminho de Vida", "ano_pessoal": "Ano Pessoal"},
        "en": {"energia_pessoal_mes": "Personal Month Energy", "mes_universal": "Universal Month",
               "caminho_vida": "Life Path", "ano_pessoal": "Personal Year"},
        "es": {"energia_pessoal_mes": "Energía Personal del Mes", "mes_universal": "Mes Universal",
               "caminho_vida": "Camino de Vida", "ano_pessoal": "Año Personal"},
        "it": {"energia_pessoal_mes": "Energia Personale del Mese", "mes_universal": "Mese Universale",
               "caminho_vida": "Percorso di Vita", "ano_pessoal": "Anno Personale"},
        "fr": {"energia_pessoal_mes": "Énergie Personnelle du Mois", "mes_universal": "Mois Universel",
               "caminho_vida": "Chemin de Vie", "ano_pessoal": "Année Personnelle"},
        "de": {"energia_pessoal_mes": "Persönliche Monatsenergie", "mes_universal": "Universeller Monat",
               "caminho_vida": "Lebensweg", "ano_pessoal": "Persönliches Jahr"},
        "ja": {"energia_pessoal_mes": "月の個人エネルギー", "mes_universal": "ユニバーサル月",
               "caminho_vida": "ライフパス", "ano_pessoal": "パーソナルイヤー"},
        "zh": {"energia_pessoal_mes": "月度个人能量", "mes_universal": "宇宙月",
               "caminho_vida": "生命之路", "ano_pessoal": "个人年"},
        "ru": {"energia_pessoal_mes": "Личная энергия месяца", "mes_universal": "Универсальный месяц",
               "caminho_vida": "Путь жизни", "ano_pessoal": "Личный год"},
        "he": {"energia_pessoal_mes": "אנרגיה אישית של החודש", "mes_universal": "חודש אוניברסלי",
               "caminho_vida": "דרך החיים", "ano_pessoal": "שנה אישית"},
        "ar": {"energia_pessoal_mes": "الطاقة الشخصية للشهر", "mes_universal": "الشهر الكوني",
               "caminho_vida": "طريق الحياة", "ano_pessoal": "السنة الشخصية"},
        "id": {"energia_pessoal_mes": "Energi Pribadi Bulan", "mes_universal": "Bulan Universal",
               "caminho_vida": "Jalur Kehidupan", "ano_pessoal": "Tahun Pribadi"},
        "tr": {"energia_pessoal_mes": "Kişisel Ay Enerjisi", "mes_universal": "Evrensel Ay",
               "caminho_vida": "Yaşam Yolu", "ano_pessoal": "Kişisel Yıl"},
        "vi": {"energia_pessoal_mes": "Năng lượng Cá nhân của Tháng", "mes_universal": "Tháng Phổ quát",
               "caminho_vida": "Đường đời", "ano_pessoal": "Năm Cá nhân"},
    }
    L.update(ROTULOS_CAL.get(lang, ROTULOS_CAL["pt"]))
        # ===== TRADUÇÕES — CARDS DE COMPATIBILIDADE (Família / Equipes) =====
    _TRAD_COMPAT = {
        "por_nome": {
            "pt": "Nome", "en": "Name", "es": "Nombre", "de": "Name",
            "fr": "Nom", "it": "Nome", "nl": "Naam", "pl": "Imię",
            "ru": "Имя", "ja": "名前", "zh": "姓名", "ko": "이름",
            "id": "Nama", "tr": "Ad",
        },
        "por_vida": {
            "pt": "Caminho de Vida", "en": "Life Path", "es": "Camino de Vida",
            "de": "Lebensweg", "fr": "Chemin de Vie", "it": "Percorso di Vita",
            "nl": "Levenspad", "pl": "Ścieżka Życia", "ru": "Путь Жизни",
            "ja": "ライフパス", "zh": "生命历程", "ko": "인생 경로",
            "id": "Jalur Hidup", "tr": "Yaşam Yolu",
        },
        "analise_parcial": {
            "pt": "Análise parcial: o caminho de vida não consta na tabela clássica de referência.",
            "en": "Partial analysis: the life path is not in the classic reference table.",
            "es": "Análisis parcial: el camino de vida no figura en la tabla clásica de referencia.",
            "de": "Teilanalyse: Der Lebensweg ist nicht in der klassischen Referenztabelle enthalten.",
            "fr": "Analyse partielle : le chemin de vie ne figure pas dans la table de référence classique.",
            "it": "Analisi parziale: il percorso di vita non è nella tabella classica di riferimento.",
            "nl": "Gedeeltelijke analyse: het levenspad staat niet in de klassieke referentietabel.",
            "pl": "Analiza częściowa: ścieżka życia nie występuje w klasycznej tabeli referencyjnej.",
            "ru": "Частичный анализ: путь жизни отсутствует в классической таблице.",
            "ja": "部分分析：ライフパスは古典的な参照表に含まれていません。",
            "zh": "部分分析：生命历程不在经典参照表中。",
            "ko": "부분 분석: 인생 경로가 고전 참조표에 없습니다.",
            "id": "Analisis sebagian: jalur hidup tidak terdapat dalam tabel referensi klasik.",
            "tr": "Kısmi analiz: yaşam yolu klasik referans tablosunda yer almıyor.",
        },
        "nota": {
            "pt": "Nota", "en": "Note", "es": "Nota", "de": "Hinweis",
            "fr": "Note", "it": "Nota", "nl": "Opmerking", "pl": "Uwaga",
            "ru": "Примечание", "ja": "注記", "zh": "注", "ko": "참고",
            "id": "Catatan", "tr": "Not",
        },
        "papel_chefe": {
            "pt": "chefe", "en": "leader", "es": "jefe", "de": "Leitung",
            "fr": "responsable", "it": "capo", "nl": "leidinggevende", "pl": "przełożony",
            "ru": "руководитель", "ja": "上司", "zh": "主管", "ko": "책임자",
            "id": "atasan", "tr": "yönetici",
        },
        "papel_colaborador": {
            "pt": "colaborador", "en": "team member", "es": "colaborador",
            "de": "Mitarbeitende", "fr": "collaborateur", "it": "collaboratore",
            "nl": "medewerker", "pl": "pracownik", "ru": "сотрудник",
            "ja": "メンバー", "zh": "成员", "ko": "구성원",
            "id": "anggota tim", "tr": "ekip üyesi",
        },
    }
    for _k, _v in _TRAD_COMPAT.items():
        L.setdefault(_k, _v.get(lang, _v["pt"]))
        
    _espec = None

    if "energia_mes" in dados:
        _espec = [
            f"<b>{L['mes']}:</b> {dados.get('mes', '')}",
            f"<b>{L.get('energia_pessoal_mes', 'Energia Pessoal do Mês')}:</b> "
            f"{dados.get('energia_pessoal_mes', dados.get('energia_mes', ''))}",
            f"<b>{L['energia']}:</b> {dados.get('energia_mes', '')} "
            f"({L.get('mes_universal', 'Mês Universal')})",
        ]
        if dados.get("caminho_vida"):
            _espec.append(
                f"<b>{L.get('caminho_vida', 'Caminho de Vida')}:</b> "
                f"{dados.get('caminho_vida')}")
        if dados.get("ano_pessoal"):
            _espec.append(
                f"<b>{L.get('ano_pessoal', 'Ano Pessoal')}:</b> "
                f"{dados.get('ano_pessoal')}")

    elif "compatibilidade" in dados:
        _espec = [
            f"<b>{dados.get('nome1', '')}</b> → {L['energia']} "
            f"{dados.get('energia_nome1', dados.get('energia1', ''))}",
            f"<b>{dados.get('nome2', '')}</b> → {L['energia']} "
            f"{dados.get('energia_nome2', dados.get('energia2', ''))}",
            f"<b>{L['compatibilidade']}:</b> "
            f"{dados.get('compatibilidade', '')} "
            f"({dados.get('rotulo_nome', '')})",
        ]
        _leitura = get_compat(dados.get("compatibilidade"), _ctx, lang)
        if _leitura:
            _espec.append(f"<font size='9' color='#333333'>{_leitura}</font>")
        _dual = get_dual(dados.get("compatibilidade"), _ctx, lang)
        if _dual:
            _espec.append(f"<font size='9' color='#8a6d1f'>{_dual}</font>")
        if dados.get("compatibilidade_vida") is not None:
            _espec.append(
                f"<b>{L['compatibilidade']} ({L['energia']} de vida):</b> "
                f"{dados.get('compatibilidade_vida')} "
                f"({dados.get('rotulo_vida', '')})")
            _dual_v = get_dual(dados.get("compatibilidade_vida"), _ctx, lang)
            if _dual_v:
                _espec.append(f"<font size='9' color='#8a6d1f'>{_dual_v}</font>")

    elif "membros" in dados:
        _espec = [f"<b>{L['membros']}:</b> {dados.get('total', '')}"]
        for m in dados.get("membros", []):
            papel = m.get("papel", "")
            _papel = f" ({L.get('papel_' + papel, papel)})" if papel else ""
            _espec.append(
                f"{m.get('membro', '')} — {L['energia']} {m.get('energia', '')}"
                f"{_papel}" + (
                    f" — {L.get('caminho_vida', 'Caminho de Vida')} "
                    f"{m.get('caminho_vida')}"
                    if m.get("caminho_vida") else ""))

        for p in dados.get("pares", []):
            _linha = (
                f"<br/><b>{p.get('membro1', '')} × {p.get('membro2', '')}</b><br/>"
                f"{L['compatibilidade']}: <b>{p.get('compatibilidade', '—')}</b>")
            _rot = p.get("rotulo_nome") or p.get("rotulo") or ""
            if _rot:
                _linha += f" — {_rot}"
            _cn = p.get("compatibilidade_nome")
            _cv = p.get("compatibilidade_vida")
            if _cn is not None and _cv is not None:
                _linha += (
                    f"<br/><font size='8' color='#666666'>"
                    f"{L.get('por_nome', 'Nome')}: {_cn} "
                    f"({p.get('rotulo_nome', '')}) · "
                    f"{L.get('por_vida', 'Caminho de Vida')}: {_cv} "
                    f"({p.get('rotulo_vida', '')})</font>")
            elif _cv is None and p.get("rotulo_vida") == "Não catalogado":
                _linha += (
                    f"<br/><font size='8' color='#8a6d1f'>"
                    f"{L.get('analise_parcial', 'Análise parcial: o caminho de vida não consta na tabela clássica de referência.')}"
                    f"</font>")
            _espec.append(_linha)

            _leitura = get_compat(p.get("compatibilidade"), _ctx, lang)
            if _leitura:
                _espec.append(f"<font size='9' color='#333333'>{_leitura}</font>")

            _dual = get_dual(p.get("compatibilidade"), _ctx, lang)
            if _dual:
                _espec.append(f"<font size='9' color='#8a6d1f'>{_dual}</font>")

            _dual_v = get_dual(p.get("compatibilidade_vida"), _ctx, lang)
            if _dual_v:
                _espec.append(f"<font size='9' color='#8a6d1f'>{_dual_v}</font>")
                
        # Número do Imóvel — sugestão única + dica traduzida
        if dados.get("sugestao"):
            _espec.append(
                f"<br/><font color='#8a6d1f'><b>{dados.get('sugestao', '')}</b></font>")
        if dados.get("dica"):
            _espec.append(
                f"<br/>{dados.get('dica', '')}")
    elif "match" in dados or "energia_desejada" in dados:
        _espec = [
            f"<b>{dados.get('nome', nome)}</b> — {L['soma']} {dados.get('soma', '')} — {L['energia']} {dados.get('energia', '')}",
        ]
        if dados.get("energia_desejada"):
            _espec.append(
                f"{L['energia_desejada']}: {dados.get('energia_desejada')} — "
                + (L['match'] if dados.get('match') else L['no_match']))
    if _espec is not None:
        for linha in _espec:
            e.append(Paragraph(linha, _estilo("ESP", FONTE, 11, DARK, TA_LEFT, sa=LINHA * 0.4)))
        e.append(Spacer(1, LINHA))
        e.append(Paragraph(T.get("entrega", ""), _estilo("J", FONTE, 8, GRAY, TA_CENTER, sa=6)))
        e.append(Paragraph("© A1ELOS Assessoria e Consultoria",
                           _estilo("F", FONTE, 8, GRAY, TA_CENTER)))
        doc.build(e, onFirstPage=_cabecalho_pagina, onLaterPages=_cabecalho_pagina)
        FONTE, FN = _fontes_antigas
        return path    
    chaves = [("life_path", "caminho_vida"), ("expression", "expressao"),
              ("soul_urge", "motivacao"), ("personality", "personalidade"),
              ("destiny", "destino")]
    linhas = [[t("numero", lang), t("valor", lang), t("significado", lang)]]
    for k, lbl in chaves:
        v = dados.get(k, 0)
        sig = get_sig(v, lang)
        linhas.append([_prep(t(lbl, lang), lang), str(v), _prep(sig[0], lang)])
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
        v = dados.get(k, 0)
        nm, pos, neg, licao = get_sig_full(v, lang)
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
    _, desc_cam = get_cam(lp, lang)
    if desc_cam:
        e.append(Spacer(1, LINHA))
        e.append(Paragraph(f"<b>{t('caminho_vida', lang)} {lp}:</b> {desc_cam}",
                           _estilo("J", FONTE, 10, DARK, TA_JUSTIFY, sa=LINHA)))
    try:
        dt = dp.parse(bd_str)
        vib_dia = reduzir(dt.day)
        vib_txt = get_vib(vib_dia, lang)
        if vib_txt:
            e.append(Spacer(1, LINHA))
            e.append(Paragraph(f"<b>{t('vibracao', lang)}: {vib_dia}</b> — {vib_txt}",
                               _estilo("J", FONTE, 10, DARK, TA_JUSTIFY, sa=LINHA)))
    except Exception:
        pass
        
    e.append(Spacer(1, LINHA))
    e.append(Paragraph(T.get("entrega", ""), _estilo("J", FONTE, 8, GRAY, TA_CENTER, sa=6)))
    e.append(Paragraph("© A1ELOS Assessoria e Consultoria",
                       _estilo("F", FONTE, 8, GRAY, TA_CENTER)))
    doc.build(e, onFirstPage=_cabecalho_pagina, onLaterPages=_cabecalho_pagina)
    FONTE, FN = _fontes_antigas
    return path

# -*- coding: utf-8 -*-
# pdf_service.py - ADICIONE ESTA FUNCAO AO FINAL DO ARQUIVO
# pdf_urna(nome_completo, cargo_label, resultados, sugestoes, lang="pt")
# resultados vem de validar_nomes_urna (produtos/urna.py):
#   cada item: {nome, forma, soma, energia, eh_ideal, explicacao,
#               letras:[{letra,valor}], nota_traducao, observacao}

import os, uuid
from xml.sax.saxutils import escape
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                Table, TableStyle, KeepTogether)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

# Caminhos de fontes tentados em ordem. Ajuste FONT_CJK_EXTRA para a fonte
# CJK que voce ja usa no servico (o log "Fontes CJK registradas" indica qual).
FONT_DEJAVU = ["static/fonts/DejaVuSans.ttf", "fonts/DejaVuSans.ttf",
               "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
FONT_DEJAVU_BOLD = ["static/fonts/DejaVuSans-Bold.ttf", "fonts/DejaVuSans-Bold.ttf",
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
FONT_CJK_EXTRA = ["static/fonts/NotoSansCJK-Regular.ttc",
                  "static/fonts/NotoSansSC-Regular.otf",
                  "static/fonts/WenQuanYiMicroHei.ttf"]

LABELS_URNA = {
    "pt": {"titulo": "Validação do Nome de Urna", "nome": "Nome completo", "cargo": "Cargo",
           "grafia": "Grafia", "soma": "Soma", "energia": "Energia",
           "ideal": "ENERGIA 8 · IDEAL PARA CANDIDATURA", "letra": "Detalhamento letra a letra",
           "obs": "Observação do autor", "sug": "Sugestões", "nota": "Nota de tradução"},
    "en": {"titulo": "Ballot Name Validation", "nome": "Full name", "cargo": "Position",
           "grafia": "Spelling", "soma": "Total", "energia": "Energy",
           "ideal": "ENERGY 8 · IDEAL FOR CANDIDACY", "letra": "Letter-by-letter breakdown",
           "obs": "Author's note", "sug": "Suggestions", "nota": "Translation note"},
    "es": {"titulo": "Validación del Nombre de Urna", "nome": "Nombre completo", "cargo": "Cargo",
           "grafia": "Grafía", "soma": "Suma", "energia": "Energía",
           "ideal": "ENERGÍA 8 · IDEAL PARA LA CANDIDATURA", "letra": "Desglose letra a letra",
           "obs": "Observación del autor", "sug": "Sugerencias", "nota": "Nota de traducción"},
    "fr": {"titulo": "Validation du Nom d'Urne", "nome": "Nom complet", "cargo": "Poste",
           "grafia": "Graphie", "soma": "Somme", "energia": "Énergie",
           "ideal": "ÉNERGIE 8 · IDÉAL POUR LA CANDIDATURE", "letra": "Détail lettre par lettre",
           "obs": "Observation de l'auteur", "sug": "Suggestions", "nota": "Note de traduction"},
    "de": {"titulo": "Überprüfung des Urnennamens", "nome": "Vollständiger Name", "cargo": "Amt",
           "grafia": "Schreibweise", "soma": "Summe", "energia": "Energie",
           "ideal": "ENERGIE 8 · IDEAL FÜR DIE KANDIDATUR", "letra": "Buchstabenweise Aufschlüsselung",
           "obs": "Anmerkung des Autors", "sug": "Vorschläge", "nota": "Übersetzungshinweis"},
    "it": {"titulo": "Validazione del Nome d'Urna", "nome": "Nome completo", "cargo": "Carica",
           "grafia": "Grafia", "soma": "Somma", "energia": "Energia",
           "ideal": "ENERGIA 8 · IDEALE PER LA CANDIDATURA", "letra": "Dettaglio lettera per lettera",
           "obs": "Osservazione dell'autore", "sug": "Suggerimenti", "nota": "Nota di traduzione"},
    "ja": {"titulo": "ウルナ名の検証", "nome": "フルネーム", "cargo": "役職",
           "grafia": "表記", "soma": "合計", "energia": "エネルギー",
           "ideal": "エネルギー8 · 立候補に最適", "letra": "文字ごとの内訳",
           "obs": "著者の所見", "sug": "提案", "nota": "翻訳に関する注記"},
    "zh": {"titulo": "选票名称验证", "nome": "全名", "cargo": "职位",
           "grafia": "写法", "soma": "总和", "energia": "能量",
           "ideal": "能量8 · 对竞选最理想", "letra": "逐字母分解",
           "obs": "作者说明", "sug": "建议", "nota": "翻译说明"},
    "ru": {"titulo": "Проверка имени в бюллетене", "nome": "Полное имя", "cargo": "Должность",
           "grafia": "Написание", "soma": "Сумма", "energia": "Энергия",
           "ideal": "ЭНЕРГИЯ 8 · ИДЕАЛЬНО ДЛЯ КАНДИДАТУРЫ", "letra": "Разбор по буквам",
           "obs": "Примечание автора", "sug": "Предложения", "nota": "Примечание о переводе"},
    "id": {"titulo": "Validasi Nama di Surat Suara", "nome": "Nama lengkap", "cargo": "Jabatan",
           "grafia": "Ejaan", "soma": "Jumlah", "energia": "Energi",
           "ideal": "ENERGI 8 · IDEAL UNTUK PENCALONAN", "letra": "Rincian per huruf",
           "obs": "Catatan penulis", "sug": "Saran", "nota": "Catatan terjemahan"},
    "tr": {"titulo": "Oy Pusulası Adı Doğrulama", "nome": "Tam ad", "cargo": "Makam",
           "grafia": "Yazım", "soma": "Toplam", "energia": "Enerji",
           "ideal": "ENERJİ 8 · ADAYLIK İÇİN İDEAL", "letra": "Harf harf döküm",
           "obs": "Yazarın notu", "sug": "Öneriler", "nota": "Çeviri notu"},
    "vi": {"titulo": "Xác thực Tên trên Phiếu bầu", "nome": "Họ tên đầy đủ", "cargo": "Chức vụ",
           "grafia": "Cách viết", "soma": "Tổng", "energia": "Năng lượng",
           "ideal": "NĂNG LƯỢNG 8 · LÝ TƯỞNG CHO ỨNG CỬ", "letra": "Chi tiết từng chữ cái",
           "obs": "Nhận xét của tác giả", "sug": "Gợi ý", "nota": "Ghi chú bản dịch"},
    "he": {"titulo": "אימות שם בקלפי", "nome": "שם מלא", "cargo": "תפקיד",
           "grafia": "כתיב", "soma": "סכום", "energia": "אנרגיה",
           "ideal": "אנרגיה 8 · אידיאלי למועמדות", "letra": "פירוט אות אחר אות",
           "obs": "הערת המחבר", "sug": "הצעות", "nota": "הערת תרגום"},
    "ar": {"titulo": "التحقق من اسم بطاقة الاقتراع", "nome": "الاسم الكامل", "cargo": "المنصب",
           "grafia": "الكتابة", "soma": "المجموع", "energia": "الطاقة",
           "ideal": "الطاقة 8 · مثالي للترشح", "letra": "التفصيل حرفًا بحرف",
           "obs": "ملاحظة المؤلف", "sug": "اقتراحات", "nota": "ملاحظة الترجمة"},
}

def _fontes_urna():
    fonts = {}
    for nome, caminhos in (("DejaVu", FONT_DEJAVU), ("DejaVuBold", FONT_DEJAVU_BOLD)):
        for p in caminhos:
            try:
                if os.path.exists(p):
                    pdfmetrics.registerFont(TTFont(nome, p, subfontIndex=0))
                    fonts[nome] = True
                    break
            except Exception:
                continue
    for p in FONT_CJK_EXTRA:
        try:
            if os.path.exists(p):
                pdfmetrics.registerFont(TTFont("CJKUrna", p, subfontIndex=0))
                fonts["CJK"] = True
                break
        except Exception:
            continue
    if "CJK" not in fonts:
        try:
            pdfmetrics.registerFont(UnicodeCIDFont("HeiseiMin-W3"))  # japonês
            fonts["CJK"] = True
        except Exception:
            pass
    return fonts

def pdf_urna(nome_completo, cargo_label, resultados, sugestoes, lang="pt"):
    os.makedirs("static/relatorios", exist_ok=True)
    codigo = uuid.uuid4().hex[:8]
    arquivo = f"static/relatorios/urna_{codigo}.pdf"

    fonts = _fontes_urna()
    fonte_base = "DejaVu" if fonts.get("DejaVu") else "Helvetica"
    fonte_bold = "DejaVuBold" if fonts.get("DejaVuBold") else "Helvetica-Bold"
    fonte_cjk = "CJKUrna" if fonts.get("CJK") else None

    usar_cjk = lang in ("ja", "zh", "ru", "he", "ar")
    f_normal = fonte_cjk if (usar_cjk and fonte_cjk) else fonte_base
    f_bold = fonte_cjk if (usar_cjk and fonte_cjk) else fonte_bold

    L = LABELS_URNA.get(lang, LABELS_URNA["en"])

    st_titulo = ParagraphStyle("t", fontName=f_bold, fontSize=16, leading=20,
                               alignment=1, textColor=colors.HexColor("#1a1a1a"), spaceAfter=4)
    st_sub = ParagraphStyle("s", fontName=f_normal, fontSize=9, leading=12,
                            alignment=1, textColor=colors.HexColor("#888888"), spaceAfter=12)
    st_h = ParagraphStyle("h", fontName=f_bold, fontSize=12, leading=15,
                          textColor=colors.HexColor("#C9A94E"), spaceBefore=10, spaceAfter=4)
    st_txt = ParagraphStyle("t2", fontName=f_normal, fontSize=10, leading=14,
                            textColor=colors.HexColor("#222222"))
    st_graf = ParagraphStyle("g", fontName=f_bold, fontSize=11, leading=14,
                             textColor=colors.HexColor("#1a1a1a"))
    st_obs = ParagraphStyle("o", fontName=f_normal, fontSize=9, leading=12,
                            textColor=colors.HexColor("#555555"))
    st_nota = ParagraphStyle("n", fontName=f_normal, fontSize=8, leading=11,
                             textColor=colors.HexColor("#999999"))
    st_sug = ParagraphStyle("u", fontName=f_normal, fontSize=10, leading=13,
                            textColor=colors.HexColor("#333333"))

    doc = SimpleDocTemplate(arquivo, pagesize=A4,
                            rightMargin=18 * mm, leftMargin=18 * mm,
                            topMargin=16 * mm, bottomMargin=16 * mm,
                            title=f"A1ELOS - {L['titulo']}",
                            author="A1ELOS Global Numerology")
    story = []
    story.append(Paragraph(escape(nome_completo or ""), st_titulo))
    story.append(Paragraph(escape(cargo_label or ""), st_sub))
    story.append(Spacer(1, 6))

    for r in (resultados or []):
        bloco = []
        base_graf = r.get("forma") or r.get("nome") or ""
        energia = r.get("energia", "?")
        soma = r.get("soma", "?")
        eh_ideal = bool(r.get("eh_ideal"))
        bloco.append(Paragraph(f"{L['grafia']}: {escape(str(base_graf))}", st_graf))
        linha = f"{L['soma']}: {soma} &nbsp;·&nbsp; {L['energia']}: {energia}"
        if eh_ideal:
            linha += f"<br/><font color='#0b7a3b'>{escape(L['ideal'])}</font>"
        bloco.append(Paragraph(linha, st_txt))
        letras = r.get("letras") or []
        if letras:
            partes = ", ".join(
                f"{escape(str(l.get('letra', '')))}={l.get('valor', '')}" for l in letras)
            bloco.append(Paragraph(f"{L['letra']}: {partes}", st_obs))
        obs = r.get("observacao")
        if obs:
            bloco.append(Paragraph(f"{L['obs']}: {escape(str(obs))}", st_obs))
        story.append(KeepTogether(bloco))
        story.append(Spacer(1, 8))

    notas = [r.get("nota_traducao") for r in (resultados or []) if r.get("nota_traducao")]
    if notas:
        story.append(Paragraph(f"{L['nota']}: {escape(str(notas[0]))}", st_nota))

    if sugestoes:
        story.append(Paragraph(L["sug"], st_h))
        for s in sugestoes[:3]:
            tag = " · " + L["ideal"] if s.get("eh_ideal") else ""
            story.append(Paragraph(
                f"- {escape(str(s.get('nome', '')))} ({L['energia']}: {s.get('energia', '?')}){tag}",
                st_sug))

    doc.build(story)
    return arquivo

# ===== LEITURAS COMPOSTAS 1-9 + MESTRES (calendário) =====
LEITURAS_ENERGIA = {
    1:  "Liderança e iniciativa — mês de começar. Projetos novos fluem; evite esperar pelos outros.",
    2:  "Cooperação e sensibilidade — parcerias decidem. Ouça antes de agir; paciência traz acordos.",
    3:  "Expressão e criatividade — comunicação favorece. Bom momento para apresentar ideias e publicar.",
    4:  "Estrutura e trabalho — organize bases, contratos e finanças. Os resultados vêm pelo método.",
    5:  "Movimento e mudança — viagens, contatos e novidades. Evite decisões impulsivas em dinheiro.",
    6:  "Família e responsabilidade — harmonize relações e o lar. Bom para conciliar, cuidar e servir.",
    7:  "Estudo e introspecção — pesquisa, análise e espiritualidade. Recolhimento produtivo; evite isolamento.",
    8:  "Poder e materialização — negócios, promoções e dinheiro em foco. Exige ética e firmeza.",
    9:  "Conclusão e generosidade — feche ciclos, perdoe, doe. O novo chega quando o velho termina.",
    11: "Mestre 11 — intuição elevada e inspiração. Grandes percepções pedem equilíbrio emocional.",
    22: "Mestre 22 — o construtor. Idealiza e materializa em grande escala; exige disciplina.",
}

def _leitura_energia(n):
    try:
        return LEITURAS_ENERGIA.get(int(n), "Energia em transição.")
    except (TypeError, ValueError):
        return "Energia em transição."


def gerar_pdf_calendario(dados, lang="pt", nome_exib=""):
    path = os.path.join(TMP, f"p_calendario_{uuid.uuid4().hex[:8]}.pdf")
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=50, rightMargin=50,
                            topMargin=40, bottomMargin=30)
    e = []
    e.append(Spacer(1, 15))
    e.append(Paragraph("CALENDÁRIO MENSAL ENERGÉTICO",
                       _estilo("cal_t", FN, 16, GOLD, TA_CENTER, sa=6)))
    e.append(Paragraph(nome_exib, _estilo("cal_n", FN, 12, DARK, TA_CENTER, sa=2)))
    e.append(Paragraph(f"Nascimento: {dados.get('nascimento', '-')}",
                       _estilo("cal_nb", FONTE, 9, GRAY, TA_CENTER, sa=12)))

    # --- Tabela dos números (rótulos elegantes, campos vazios ocultos) ---
    ROTULOS = {
        "mes": "Mês de referência",
        "caminho_vida": "Caminho de Vida (energia pessoal)",
        "ano_pessoal": "Ano Pessoal",
        "energia_mes": "Energia do Mês (universal)",
        "energia_pessoal_mes": "Energia Pessoal no Mês",
        "mes_pessoal_mestre": "Número-mestre registrado",
    }
    ORDEM = ["mes", "caminho_vida", "ano_pessoal",
             "energia_mes", "energia_pessoal_mes", "mes_pessoal_mestre"]
    linhas = [["Item", "Valor"]]
    for chave in ORDEM:
        valor = dados.get(chave)
        if valor in (None, ""):
            continue
        linhas.append([ROTULOS.get(chave, chave.replace("_", " ").capitalize()), str(valor)])
    tbl = Table(linhas, colWidths=[240, 245])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GOLD),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.4, GRAY),
        ("BACKGROUND", (0, 1), (-1, -1), LGRAY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    e.append(tbl)
    e.append(Spacer(1, 14))

    # --- Rastro do cálculo em caixa dourada (quebra de linha por passo) ---
    rastro = dados.get("rastro", "")
    if rastro:
        st_rastro = _estilo("cal_rastro", FONTE, 9, DARK, TA_LEFT)
        box = Table([[Paragraph("<b>COMO CALCULAMOS</b>", st_rastro)],
                     [Paragraph(rastro.replace(" · ", "<br/>"), st_rastro)]],
                    colWidths=[485])
        box.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FBF5E6")),
            ("BOX", (0, 0), (-1, -1), 1, GOLD),
            ("LINEBELOW", (0, 0), (0, 0), 0.5, GOLD),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        e.append(box)
        e.append(Spacer(1, 14))

    # --- Leituras compostas ---
    e.append(Paragraph("O QUE ESTES NÚMEROS SIGNIFICAM",
                       _estilo("cal_sec", FN, 11, GOLD, TA_LEFT, sa=4)))
    mestre = dados.get("mes_pessoal_mestre")
    for chave, titulo in [
        ("energia_mes", "Energia do Mês"),
        ("energia_pessoal_mes", "Sua Energia neste Mês"),
        ("ano_pessoal", "Seu Ano Pessoal"),
    ]:
        n = dados.get(chave)
        if n in (None, ""):
            continue
        usar = mestre if (chave == "energia_pessoal_mes" and mestre) else n
        e.append(Paragraph(f"<b>{titulo} — {n}</b>",
                           _estilo("cal_l1", FN, 9, DARK, TA_LEFT, sa=2)))
        e.append(Paragraph(_leitura_energia(usar),
                           _estilo("cal_l2", FONTE, 9, DARK, TA_LEFT, sa=6)))

    e.append(Spacer(1, 10))
    e.append(Paragraph("(c) A1ELOS", _estilo("cal_foot", FONTE, 7, GRAY, TA_CENTER)))
    doc.build(e)
    return path

# ═══════════════════════════════════════════
# PRODUTOS DE RELAÇÃO — CASAL, FAMÍLIA, EQUIPES (21/11/2026)
# Templates próprios. Assinatura: fn(dados, lang) -> caminho do PDF.
# NÃO alteram as globais FONTE/FN: usam fonte local por idioma.
# ═══════════════════════════════════════════
try:
    from xml.sax.saxutils import escape as _escape_xml
except Exception:
    _escape_xml = lambda v: str(v)


def _rel_escape(v):
    """Escapa para XML e blinda contra bool, None e números.

    xml.sax.saxutils.escape() chama .replace() no argumento; um booleano
    derruba o PDF inteiro com "'bool' object has no attribute 'replace'".
    """
    return _escape_xml("" if v is None else str(v))
    
REL_TXT = {
    "pt": {"grau1": "Dissonância", "grau2": "Média — Acordo/Desacordo",
           "grau3": "Acordo", "grau4": "Acordo perfeito", "energia": "Energia",
           "compat": "Compatibilidade", "nasc": "Nascimento", "membros": "Membros",
           "papel": "Papel", "chefe": "Chefe", "colaborador": "Colaborador",
           "titular": "Titular", "vida": "Caminho de Vida",
           "pares": "Compatibilidade entre Pares",
           "sem_dados": "Dados insuficientes para gerar este relatório."},
    "en": {"grau1": "Dissonance", "grau2": "Mixed — Agreement/Disagreement",
           "grau3": "Agreement", "grau4": "Perfect agreement", "energia": "Energy",
           "compat": "Compatibility", "nasc": "Birth", "membros": "Members",
           "papel": "Role", "chefe": "Leader", "colaborador": "Team member",
           "titular": "Holder", "vida": "Life Path",
           "pares": "Compatibility between Pairs",
           "sem_dados": "Insufficient data to generate this report."},
    "es": {"grau1": "Disonancia", "grau2": "Media — Acuerdo/Desacuerdo",
           "grau3": "Acuerdo", "grau4": "Acuerdo perfecto", "energia": "Energía",
           "compat": "Compatibilidad", "nasc": "Nacimiento", "membros": "Miembros",
           "papel": "Rol", "chefe": "Jefe", "colaborador": "Colaborador",
           "titular": "Titular", "vida": "Camino de Vida",
           "pares": "Compatibilidad entre Pares",
           "sem_dados": "Datos insuficientes para generar este informe."},
    "it": {"grau1": "Dissonanza", "grau2": "Media — Accordo/Disaccordo",
           "grau3": "Accordo", "grau4": "Accordo perfetto", "energia": "Energia",
           "compat": "Compatibilità", "nasc": "Nascita", "membros": "Membri",
           "papel": "Ruolo", "chefe": "Capo", "colaborador": "Collaboratore",
           "titular": "Titolare", "vida": "Percorso di Vita",
           "pares": "Compatibilità tra Coppie",
           "sem_dados": "Dati insufficienti per generare questo rapporto."},
    "fr": {"grau1": "Dissonance", "grau2": "Moyenne — Accord/Désaccord",
           "grau3": "Accord", "grau4": "Accord parfait", "energia": "Énergie",
           "compat": "Compatibilité", "nasc": "Naissance", "membros": "Membres",
           "papel": "Rôle", "chefe": "Responsable", "colaborador": "Collaborateur",
           "titular": "Titulaire", "vida": "Chemin de Vie",
           "pares": "Compatibilité entre Paires",
           "sem_dados": "Données insuffisantes pour générer ce rapport."},
    "de": {"grau1": "Dissonanz", "grau2": "Mittel — Einigkeit/Uneinigkeit",
           "grau3": "Einigkeit", "grau4": "Perfekte Einigkeit", "energia": "Energie",
           "compat": "Kompatibilität", "nasc": "Geburt", "membros": "Mitglieder",
           "papel": "Rolle", "chefe": "Leitung", "colaborador": "Mitarbeitende",
           "titular": "Inhaber", "vida": "Lebensweg",
           "pares": "Kompatibilität zwischen Paaren",
           "sem_dados": "Unzureichende Daten für diesen Bericht."},
    "ja": {"grau1": "不協和", "grau2": "中間 — 一致/不一致",
           "grau3": "一致", "grau4": "完全な一致", "energia": "エネルギー",
           "compat": "相性", "nasc": "生年月日", "membros": "メンバー",
           "papel": "役割", "chefe": "上司", "colaborador": "メンバー",
           "titular": "対象者", "vida": "ライフパス",
           "pares": "ペア間の相性",
           "sem_dados": "このレポートを生成するにはデータが不足しています。"},
    "zh": {"grau1": "不和谐", "grau2": "中等 — 契合/分歧",
           "grau3": "契合", "grau4": "完美契合", "energia": "能量",
           "compat": "兼容性", "nasc": "出生", "membros": "成员",
           "papel": "角色", "chefe": "主管", "colaborador": "成员",
           "titular": "持有人", "vida": "生命之路",
           "pares": "成员之间的兼容性",
           "sem_dados": "数据不足，无法生成本报告。"},
    "ru": {"grau1": "Диссонанс", "grau2": "Средняя — Согласие/Разногласие",
           "grau3": "Согласие", "grau4": "Идеальное согласие", "energia": "Энергия",
           "compat": "Совместимость", "nasc": "Рождение", "membros": "Члены",
           "papel": "Роль", "chefe": "Руководитель", "colaborador": "Сотрудник",
           "titular": "Владелец", "vida": "Путь Жизни",
           "pares": "Совместимость между парами",
           "sem_dados": "Недостаточно данных для создания отчёта."},
    "he": {"grau1": "אי-התאמה", "grau2": "בינוני — הסכמה/מחלוקת",
           "grau3": "הסכמה", "grau4": "התאמה מושלמת", "energia": "אנרגיה",
           "compat": "תאימות", "nasc": "לידה", "membros": "חברים",
           "papel": "תפקיד", "chefe": "מנהל", "colaborador": "עובד",
           "titular": "בעל המפה", "vida": "דרך החיים",
           "pares": "תאימות בין זוגות",
           "sem_dados": "אין מספיק נתונים להפקת הדוח."},
    "ar": {"grau1": "تنافر", "grau2": "متوسط — اتفاق/اختلاف",
           "grau3": "اتفاق", "grau4": "اتفاق تام", "energia": "الطاقة",
           "compat": "التوافق", "nasc": "الميلاد", "membros": "الأعضاء",
           "papel": "الدور", "chefe": "المدير", "colaborador": "عضو الفريق",
           "titular": "صاحب الخريطة", "vida": "طريق الحياة",
           "pares": "التوافق بين الأزواج",
           "sem_dados": "بيانات غير كافية لإنشاء هذا التقرير."},
    "id": {"grau1": "Disonansi", "grau2": "Sedang — Sepakat/Tidak sepakat",
           "grau3": "Sepakat", "grau4": "Sepakat sempurna", "energia": "Energi",
           "compat": "Kompatibilitas", "nasc": "Kelahiran", "membros": "Anggota",
           "papel": "Peran", "chefe": "Atasan", "colaborador": "Anggota tim",
           "titular": "Pemilik", "vida": "Jalur Hidup",
           "pares": "Kompatibilitas antar Pasangan",
           "sem_dados": "Data tidak cukup untuk membuat laporan ini."},
    "tr": {"grau1": "Uyumsuzluk", "grau2": "Orta — Anlaşma/Anlaşmazlık",
           "grau3": "Anlaşma", "grau4": "Kusursuz anlaşma", "energia": "Enerji",
           "compat": "Uyum", "nasc": "Doğum", "membros": "Üyeler",
           "papel": "Rol", "chefe": "Yönetici", "colaborador": "Ekip üyesi",
           "titular": "Sahip", "vida": "Yaşam Yolu",
           "pares": "Çiftler arası Uyum",
           "sem_dados": "Bu raporu oluşturmak için veri yetersiz."},
    "vi": {"grau1": "Bất hòa", "grau2": "Trung bình — Đồng thuận/Bất đồng",
           "grau3": "Đồng thuận", "grau4": "Đồng thuận hoàn hảo", "energia": "Năng lượng",
           "compat": "Tương hợp", "nasc": "Sinh", "membros": "Thành viên",
           "papel": "Vai trò", "chefe": "Quản lý", "colaborador": "Nhân viên",
           "titular": "Chủ sở hữu", "vida": "Đường đời",
           "pares": "Tương hợp giữa các Cặp",
           "sem_dados": "Không đủ dữ liệu để tạo báo cáo này."},
}

_LBL = {
    "pt": ("Par de apelidos", "Par de nomes"),
    "en": ("Nickname pair", "Full-name pair"),
    "es": ("Par de apodos", "Par de nombres"),
    "it": ("Coppia di soprannomi", "Coppia di nomi"),
    "fr": ("Duo de surnoms", "Duo de noms"),
    "de": ("Rufnamen-Paar", "Namenspaar"),
    "ja": ("呼び名のペア", "本名のペア"),
    "zh": ("称呼名组合", "全名组合"),
    "ru": ("Пара рабочих имён", "Пара полных имён"),
    "id": ("Pasangan nama panggilan", "Pasangan nama lengkap"),
    "tr": ("Takma ad ikilisi", "Tam ad ikilisi"),
    "vi": ("Cặp tên gọi", "Cặp họ tên"),
    "he": ("צמד שמות בשימוש", "צמד שמות מלאים"),
    "ar": ("ثنائي الأسماء المتداولة", "ثنائي الأسماء الكاملة"),
}

def _rel(lang):
    return REL_TXT.get(lang) or REL_TXT["pt"]

def _rel_grau(grau, lang):
    k = {1: "grau1", 2: "grau2", 3: "grau3", 4: "grau4"}.get(grau)
    return _rel(lang).get(k, "") if k else ""

def _rel_path(tag):
    return os.path.join(TMP, f"{tag}_{uuid.uuid4().hex[:8]}.pdf")

# Títulos de produtos que ainda não estão no dicionário PRODUTOS.
TITULOS_EXTRA = {
    "pt": {"compatibilidade_equipes": "Compatibilidade de Equipes"},
    "en": {"compatibilidade_equipes": "Team Compatibility"},
    "es": {"compatibilidade_equipes": "Compatibilidad de Equipos"},
    "it": {"compatibilidade_equipes": "Compatibilità di Squadra"},
    "fr": {"compatibilidade_equipes": "Compatibilité d'Équipe"},
    "de": {"compatibilidade_equipes": "Team-Kompatibilität"},
    "ja": {"compatibilidade_equipes": "チーム相性"},
    "zh": {"compatibilidade_equipes": "团队兼容性"},
    "ru": {"compatibilidade_equipes": "Совместимость команды"},
    "id": {"compatibilidade_equipes": "Kompatibilitas Tim"},
    "tr": {"compatibilidade_equipes": "Ekip Uyumu"},
    "vi": {"compatibilidade_equipes": "Tương Thích Đội Ngũ"},
    "he": {"compatibilidade_equipes": "התאמת צוות"},
    "ar": {"compatibilidade_equipes": "توافق الفريق"},
}

class _NumCanvas(_rl_canvas.Canvas):
    """Numera 'N de TOTAL' no rodapé."""

    def __init__(self, *args, **kwargs):
        _rl_canvas.Canvas.__init__(self, *args, **kwargs)
        self._estados = []

    def showPage(self):
        self._estados.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._estados)
        for st in self._estados:
            self.__dict__.update(st)
            self.setFont(FONTE, 7)
            self.setFillColor(GOLD)
            self.drawRightString(A4[0] - 50, 22, "%d %s %d" % (self._pageNumber, _PAG_DE.get(_LANG_PAG, "de"), total))
            _rl_canvas.Canvas.showPage(self)
        _rl_canvas.Canvas.save(self)

def _cabecalho_rel(canvas, doc, entrega=""):
    """Marca d'água, assinatura, fecho e copyright — fixos no rodapé.

    O fecho NÃO é flowable: assim não gera página órfã quando o conteúdo
    termina no fim da última folha.
    """
    canvas.saveState()
    canvas.setFillColor(GOLD)
    canvas.setFillAlpha(0.15)
    canvas.setFont(FONTE, 58)
    canvas.drawCentredString(A4[0] / 2.0, A4[1] / 2.0, "A1ELOS")
    canvas.setFillAlpha(1.0)
    canvas.setFillColor(GOLD)
    canvas.setFont(FONTE, 7)
    canvas.drawString(50, 22, "A1ELOS Assessoria e Consultoria")
    canvas.setFont(FONTE, 6.5)
    canvas.setFillColor(GRAY)
    if entrega:
        canvas.drawCentredString(A4[0] / 2.0, 38, entrega)
    canvas.drawCentredString(A4[0] / 2.0, 29, "© A1ELOS Assessoria e Consultoria")
    canvas.restoreState()

_L_SINT = {
    "pt": ("Nome completo", "Nome de uso"),
    "en": ("Full name", "Name in use"),
    "es": ("Nombre completo", "Nombre de uso"),
    "it": ("Nome completo", "Nome d'uso"),
    "fr": ("Nom complet", "Nom d'usage"),
    "de": ("Voller Name", "Rufname"),
    "ja": ("本名", "呼び名"),
    "zh": ("全名", "称呼名"),
    "ru": ("Полное имя", "Имя в обиходе"),
    "he": ("שם מלא", "שם בשימוש"),
    "ar": ("الاسم الكامل", "الاسم المتداول"),
    "id": ("Nama lengkap", "Nama panggilan"),
    "tr": ("Tam ad", "Kullanılan ad"),
    "vi": ("Họ tên đầy đủ", "Tên gọi"),
}

def _rel_separador(e, titulo, fb):
    """Traço dourado + título. Substitui a quebra de página entre blocos."""
    e.append(Spacer(1, LINHA * 2))
    tbl = Table([[""]], colWidths=[495], rowHeights=[1])
    tbl.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), GOLD),
                             ("TOPPADDING", (0, 0), (-1, -1), 0),
                             ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    e.append(tbl)
    e.append(Spacer(1, LINHA))
    e.append(Paragraph(_rel_escape(titulo),
                       _estilo("BLK", fb, 13, GOLD, TA_LEFT, sa=LINHA * 0.5)))
    
def _rel_abre(produto, lang):
    _fr, _fb = fonte_para(lang)
    bruto = (PRODUTOS.get(lang, PRODUTOS["pt"]).get(produto)
             or TITULOS_EXTRA.get(lang, {}).get(produto)
             or str(produto).replace("_", " ").title())
    return _fr, _fb, bruto.upper()

def _rel_cabecalho(e, titulo, nome_exib, lang, fr, fb):
    e.append(Spacer(1, 20))
    e.append(Paragraph(_rel_escape(titulo), _estilo("T", fb, 24, GOLD, TA_CENTER, sa=ET)))
    e.append(Paragraph(t("seu_perfil", lang), _estilo("S", fr, 14, GOLD, TA_CENTER, sa=4)))
    if nome_exib:
        e.append(Paragraph(_rel_escape(str(nome_exib).upper()),
                           _estilo("N", fb, 14, DARK, TA_CENTER, sa=4)))
    e.append(Paragraph(BOAS_VINDAS.get(lang, BOAS_VINDAS["pt"]),
                       _estilo("BV", fr, 10, DARK, TA_JUSTIFY, sa=LINHA)))

def _rel_tabela(linhas, larguras, fr):
    tbl = Table(linhas, colWidths=larguras)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GOLD),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("FONTNAME", (0, 0), (-1, -1), fr),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 1), (-1, -1), LGRAY),
        ("TEXTCOLOR", (0, 1), (-1, -1), DARK),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return tbl

# Rótulo de paginação por idioma — 23/11/2026
_LANG_PAG = "pt"
_PAG_DE = {
    "pt": "de", "en": "of", "es": "de", "it": "di", "fr": "sur",
    "de": "von", "ja": "/", "zh": "/", "ru": "из", "id": "dari",
    "tr": "/", "vi": "/", "he": "מתוך", "ar": "من",
}

def _rel_fecha(doc, e, lang, fr):
    T = PDF_TEXTS.get(lang, PDF_TEXTS["pt"])
    entrega = T.get("entrega", "")

    def _pagina(canvas, doc_):
        _cabecalho_rel(canvas, doc_, entrega)

    global _LANG_PAG
    _LANG_PAG = lang

    doc.build(e, onFirstPage=_pagina, onLaterPages=_pagina,
              canvasmaker=_NumCanvas)
    
# ---------- CASAL ----------
def pdf_casal(dados, lang="pt"):
    lang = lang or "pt"
    dados = dict(dados or {})
    L = _rel(lang)
    fr, fb, titulo = _rel_abre("casal", lang)
    path = _rel_path("casal")
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=50, rightMargin=50,
                            topMargin=45, bottomMargin=45)
    e = []
    _rel_cabecalho(e, titulo, "", lang, fr, fb)

    linhas = [[L["titular"], L["energia"], L["nasc"]]]
    energias = []
    for nm, en, ns in (
        (dados.get("nome1"), dados.get("energia_nome1", dados.get("energia1", "")), dados.get("nasc1", "")),
        (dados.get("nome2"), dados.get("energia_nome2", dados.get("energia2", "")), dados.get("nasc2", "")),
    ):
        if not (nm or en or ns):
            continue
        linhas.append([_rel_escape(str(nm or "").upper()), str(en or ""), _rel_escape(ns or "")])
        if en:
            energias.append(str(en).strip())

    if len(linhas) > 1:
        e.append(_rel_tabela(linhas, [235, 80, 180], fr))
        e.append(Spacer(1, LINHA))

    if energias:
        try:
            import energia_desc as _ed
            descs, vistos = [], set()
            for en in energias:
                d = _ed.descrever(en, lang)
                if d and d not in vistos:
                    vistos.add(d)
                    descs.append("<b>%s %s</b> — %s" % (L["energia"], _rel_escape(en), _rel_escape(d)))
            if descs:
                e.append(Paragraph(" · ".join(descs),
                                   _estilo("CASAL_ED", fr, 9, GRAY, TA_LEFT, sa=LINHA * 0.8)))
        except Exception:
            pass

    comp = dados.get("compatibilidade")
    if comp is not None:
        grau_txt = _rel_grau(comp, lang)
        e.append(Paragraph(f"<b>{L['compat']}: {comp}</b> — {_rel_escape(grau_txt)}",
                           _estilo("C", fb, 12, GOLD, TA_LEFT, sa=LINHA * 0.6)))
        leitura = dados.get("leitura") or get_compat(comp, "casal", lang)
        if leitura:
            e.append(Paragraph(_rel_escape(leitura),
                               _estilo("L", fr, 11, DARK, TA_JUSTIFY, sa=LINHA * 0.6)))
        dual = get_dual(comp, "casal", lang)
        if dual:
            e.append(Paragraph(_rel_escape(dual),
                               _estilo("D", fr, 10, colors.HexColor("#8a6d1f"), TA_JUSTIFY, sa=LINHA)))
        try:
            from referencia import relacao_dupla as _rc
            for tit, itens in _rc.bloco(int(comp), lang):
                e.append(Spacer(1, LINHA * 0.8))
                e.append(Paragraph("<b>%s</b>" % _rel_escape(tit),
                                   _estilo("CASAL_FT", fb, 11, GOLD, TA_LEFT, sa=LINHA * 0.5)))
                for it in itens:
                    e.append(Paragraph("• %s" % _rel_escape(it),
                                       _estilo("CASAL_FI", fr, 10, DARK, TA_JUSTIFY, sa=LINHA * 0.35)))
        except Exception:
            pass
    else:
        e.append(Paragraph(L["sem_dados"], _estilo("ND", fr, 10, GRAY, TA_LEFT, sa=LINHA)))
    comp_a = dados.get("compatibilidade_apelido")
    ap1 = (dados.get("apelido1") or "").strip()
    ap2 = (dados.get("apelido2") or "").strip()
    if comp_a is not None and ap1 and ap2:
        _bn, _ba, _bs, _la = _L_BLOCO.get(lang) or _L_BLOCO["pt"]
        _rel_separador(e, _ba, fb)
        if comp_a == 1:
            e.append(Paragraph(_rel_escape(_sugestao_grau1(lang, "casal")),
                               _estilo("SUG2", fr, 9, colors.HexColor("#8a6d1f"),
                                       TA_JUSTIFY, sa=LINHA * 0.4)))
        linhas = [[_la, L["energia"], L["nasc"]]]
        for nm, en, ns in (
            (ap1, dados.get("numero1_apelido"), dados.get("nasc1")),
            (ap2, dados.get("numero2_apelido"), dados.get("nasc2")),
        ):
            linhas.append([_rel_escape(nm), str(en or "—"), _rel_escape(str(ns or ""))])
        e.append(_rel_tabela(linhas, [235, 80, 180], fr))
        e.append(Spacer(1, LINHA))
        e.append(Paragraph("<b>%s: %s</b> — %s" % (
            L["compat"], comp_a, _rel_escape(_rel_grau(comp_a, lang))),
            _estilo("CB3", fb, 12, GOLD, TA_LEFT, sa=LINHA * 0.6)))
        lt = get_compat(comp_a, "casal", lang)
        if lt:
            e.append(Paragraph(_rel_escape(lt),
                               _estilo("CB4", fr, 11, DARK, TA_JUSTIFY, sa=LINHA * 0.6)))
        dl = get_dual(comp_a, "casal", lang)
        if dl:
            e.append(Paragraph(_rel_escape(dl),
                               _estilo("CB5", fr, 10, colors.HexColor("#8a6d1f"),
                                       TA_JUSTIFY, sa=LINHA)))
        try:
            from referencia import relacao_dupla as _rc_c
            for tit, itens in _rc_c.bloco(int(comp_a), lang):
                e.append(Spacer(1, LINHA * 0.8))
                e.append(Paragraph("<b>%s</b>" % _rel_escape(tit),
                                   _estilo("CBF", fb, 11, GOLD, TA_LEFT, sa=LINHA * 0.5)))
                for it in itens:
                    e.append(Paragraph("• %s" % _rel_escape(it),
                                       _estilo("CBI", fr, 10, DARK, TA_JUSTIFY, sa=LINHA * 0.35)))
        except Exception:
            pass
    _rel_fecha(doc, e, lang, fr)
    return path

_L_BLOCO = {
    "pt": ("Compatibilidade pelo NOME COMPLETO", "Compatibilidade pelo NOME DE USO (APELIDO)",
           "Síntese comparativa", "Apelido"),
    "en": ("Compatibility by FULL NAME", "Compatibility by NAME IN USE (NICKNAME)",
           "Comparative summary", "Nickname"),
    "es": ("Compatibilidad por NOMBRE COMPLETO", "Compatibilidad por NOMBRE DE USO (APODO)",
           "Síntesis comparativa", "Apodo"),
    "it": ("Compatibilità per NOME COMPLETO", "Compatibilità per NOME D'USO (SOPRANNOME)",
           "Sintesi comparativa", "Soprannome"),
    "fr": ("Compatibilité par NOM COMPLET", "Compatibilité par NOM D'USAGE (SURNOM)",
           "Synthèse comparative", "Surnom"),
    "de": ("Kompatibilität nach VOLLEM NAMEN", "Kompatibilität nach RUFNAMEN",
           "Vergleichende Übersicht", "Rufname"),
    "ja": ("本名による相性", "呼び名による相性", "比較まとめ", "呼び名"),
    "zh": ("全名兼容性", "称呼名兼容性", "对比总结", "称呼名"),
    "ru": ("Совместимость по ПОЛНОМУ ИМЕНИ", "Совместимость по ИМЕНИ В ОБИХОДЕ",
           "Сравнительная сводка", "Рабочее имя"),
    "he": ("תאימות לפי שם מלא", "תאימות לפי שם בשימוש", "סיכום השוואתי", "שם בשימוש"),
    "ar": ("التوافق بالاسم الكامل", "التوافق بالاسم المتداول", "ملخص مقارن", "الاسم المتداول"),
    "id": ("Kompatibilitas berdasarkan NAMA LENGKAP", "Kompatibilitas berdasarkan NAMA PANGGILAN",
           "Ringkasan perbandingan", "Nama panggilan"),
    "tr": ("TAM AD ile Uyum", "KULLANILAN AD (TAKMA AD) ile Uyum",
           "Karşılaştırmalı özet", "Takma ad"),
    "vi": ("Tương hợp theo HỌ TÊN ĐẦY ĐỦ", "Tương hợp theo TÊN GỌI (BIỆT DANH)",
           "Tóm tắt so sánh", "Tên gọi"),
}

def _rel_separador(e, titulo, fb):
    e.append(Spacer(1, LINHA * 2))
    tbl = Table([[""]], colWidths=[495], rowHeights=[1])
    tbl.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), GOLD),
                             ("TOPPADDING", (0, 0), (-1, -1), 0),
                             ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    e.append(tbl)
    e.append(Spacer(1, LINHA))
    e.append(Paragraph(_rel_escape(titulo),
                       _estilo("BLK", fb, 13, GOLD, TA_LEFT, sa=LINHA * 0.5)))

SUGESTAO_GRAU1 = {
    "pt": "Sugestão: a dissonância no nome de uso pede ajuste. Registrar o apelido com o tratamento (Seu, Dona, Dr.) ou acrescentar uma letra desloca a energia e pode mudar o grau. Teste {ctx} e adote o nome de uso que melhor sustenta a convivência.",
    "en": "Suggestion: dissonance in the name in use calls for adjustment. Adding the form of address (Mr., Mrs., Dr.) or one letter shifts the energy and may change the grade. Test it {ctx} and adopt the name in use that best sustains the relationship.",
    "es": "Sugerencia: la disonancia en el nombre de uso pide ajuste. Añadir el tratamiento (Don, Doña, Dr.) o una letra desplaza la energía y puede cambiar el grado. Pruébalo {ctx} y adopta el nombre de uso que mejor sostiene la convivencia.",
    "it": "Suggerimento: la dissonanza nel nome d'uso richiede un aggiustamento. Aggiungere il trattamento (Signor, Signora, Dott.) o una lettera sposta l'energia e può cambiare il grado. Provalo {ctx} e adotta il nome d'uso che meglio sostiene la convivenza.",
    "fr": "Suggestion : la dissonance du nom d'usage demande un ajustement. Ajouter le traitement (M., Mme, Dr) ou une lettre déplace l'énergie et peut changer le degré. Testez {ctx} et adoptez le nom d'usage qui soutient le mieux la relation.",
    "de": "Hinweis: Die Dissonanz beim Rufnamen verlangt eine Anpassung. Anrede (Herr, Frau, Dr.) oder ein zusätzlicher Buchstabe verschiebt die Energie und kann den Grad ändern. Testen Sie es {ctx}.",
    "ja": "提案：呼び名の不協和は調整が必要です。敬称や文字を一つ加えるとエネルギーが移り、評価が変わる場合があります。{ctx}でお試しください。",
    "zh": "建议：称呼名的失谐需要调整。加上称谓或一个字母就能改变能量，也可能改变评级。请在{ctx}试用。",
    "ru": "Совет: диссонанс рабочего имени требует корректировки. Обращение или одна буква смещают энергию и могут изменить степень. Проверьте {ctx}.",
    "he": "הצעה: אי-ההתאמה בשם בשימוש דורשת התאמה. תואר או אות אחת משנים את האנרגיה ועשויים לשנות את הדרגה. נסו {ctx}.",
    "ar": "اقتراح: التنافر في الاسم المتداول يستدعي تعديلًا. إضافة اللقب أو حرف واحد يغيّر الطاقة وقد يغيّر الدرجة. جرّب {ctx}.",
    "id": "Saran: disonansi pada nama panggilan perlu disesuaikan. Sapaan atau satu huruf menggeser energi dan dapat mengubah tingkat. Ujilah {ctx}.",
    "tr": "Öneri: kullanılan addaki uyumsuzluk düzeltme gerektirir. Hitap veya bir harf eklemek enerjiyi kaydırır. {ctx} deneyin.",
    "vi": "Gợi ý: sự bất hòa ở tên gọi cần điều chỉnh. Thêm cách xưng hô hoặc một chữ cái sẽ dịch chuyển năng lượng. Hãy thử {ctx}.",
}

_CTX1 = {
    "pt": ("em casa", "no trabalho", "em família"),
    "en": ("at home", "at work", "in the family"),
    "es": ("en casa", "en el trabajo", "en familia"),
    "it": ("a casa", "al lavoro", "in famiglia"),
    "fr": ("à la maison", "au travail", "en famille"),
    "de": ("zu Hause", "bei der Arbeit", "in der Familie"),
    "ja": ("家庭で", "職場で", "家族の中で"),
    "zh": ("在家中", "在工作中", "在家庭中"),
    "ru": ("дома", "на работе", "в семье"),
    "he": ("בבית", "בעבודה", "במשפחה"),
    "ar": ("في المنزل", "في العمل", "في العائلة"),
    "id": ("di rumah", "di tempat kerja", "di keluarga"),
    "tr": ("evde", "işte", "ailede"),
    "vi": ("ở nhà", "ở nơi làm việc", "trong gia đình"),
}

_CTX_IDX = {"casal": 0, "compatibilidade_equipes": 1, "familia": 2}


def _sugestao_grau1(lang, produto):
    txt = SUGESTAO_GRAU1.get(lang) or SUGESTAO_GRAU1["pt"]
    ctx = (_CTX1.get(lang) or _CTX1["pt"])[_CTX_IDX.get(produto, 0)]
    return txt.replace("{ctx}", ctx)

ABERTURA_RELACAO = {
    "pt": [
        "Qual conta? O nome mais usado. O princípio da energia é simples: quanto mais um nome é repetido, mais a sua vibração se afirma. No ambiente de trabalho, o nome que circula em corredores, reuniões e chamadas informais é o apelido — e é ele que descreve o comportamento real da pessoa na equipe.",
        "Tudo pode ser medido em energia — inclusive o som que emitimos ao nos comunicar. A palavra tem poder. Palavra escrita e falada: no momento em que damos valor de número às letras, esse poder se torna calculável. Pouco já muda: não é preciso um nome muito diferente para que a energia se desloque.",
        "O nome completo não pode ser alterado: é a identidade de registro. O apelido, sim: pode ser escolhido, testado e ajustado até encontrar a energia que melhor representa a forma como a pessoa é chamada. Por isso fica fácil entender por que a energia muda quando mudamos algum elemento de um processo — essa é a magia da matemática no som: pura energia calculável.",
        "Títulos como Dr., Sr., Sra. ou Seu também somam. Se a pessoa é chamada de \"Seu Antônio\" ou \"Dr. Tonho\", escreva o apelido exatamente assim — o tratamento faz parte do nome de uso e entra no cálculo.",
    ],
    "en": [
        "Which name counts? The most used one. The principle of energy is simple: the more a name is repeated, the more its vibration takes hold. In the workplace, the name that circulates in corridors, meetings and informal calls is the nickname — and it is the one that describes how the person actually behaves in the team.",
        "Everything can be measured in energy — including the sound we emit when we communicate. The word has power. Written and spoken word: the moment we assign a number value to letters, that power becomes calculable. A small change is enough: the name does not need to differ much for the energy to shift.",
        "The full name cannot be altered: it is the identity of record. The nickname can: it may be chosen, tested and adjusted until it finds the energy that best represents the way the person is called. That is why it becomes easy to understand why energy changes when we change any element of a process — this is the magic of mathematics in sound: pure calculable energy.",
        "Titles such as Dr., Mr., Mrs. or Seu also add up. If the person is called \"Seu Antônio\" or \"Dr. Tonho\", write the nickname exactly like that — the form of address is part of the name in use and enters the calculation.",
    ],
    "es": [
        "¿Qué nombre cuenta? El más usado. El principio de la energía es simple: cuanto más se repite un nombre, más se afirma su vibración. En el ambiente de trabajo, el nombre que circula en pasillos, reuniones y llamadas informales es el apodo — y es él el que describe el comportamiento real de la persona en el equipo.",
        "Todo puede medirse en energía — incluso el sonido que emitimos al comunicarnos. La palabra tiene poder. Palabra escrita y hablada: en el momento en que damos valor de número a las letras, ese poder se vuelve calculable. Poco ya cambia: no hace falta un nombre muy diferente para que la energía se desplace.",
        "El nombre completo no puede alterarse: es la identidad de registro. El apodo, sí: puede elegirse, probarse y ajustarse hasta encontrar la energía que mejor representa la forma en que se llama a la persona. Por eso resulta fácil entender por qué la energía cambia cuando cambiamos cualquier elemento de un proceso — esa es la magia de las matemáticas en el sonido: pura energía calculable.",
        "Los tratamientos como Dr., Sr., Sra. o Don también suman. Si a la persona se le llama \"Don Antonio\" o \"Dr. Tonho\", escriba el apodo exactamente así — el tratamiento forma parte del nombre de uso y entra en el cálculo.",
    ],
    "it": [
        "Quale nome conta? Quello più usato. Il principio dell'energia è semplice: più un nome viene ripetuto, più la sua vibrazione si afferma. Nell'ambiente di lavoro, il nome che circola nei corridoi, nelle riunioni e nelle chiamate informali è il soprannome — ed è lui che descrive il comportamento reale della persona nella squadra.",
        "Tutto può essere misurato in energia — incluso il suono che emettiamo comunicando. La parola ha potere. Parola scritta e parlata: nel momento in cui diamo valore numerico alle lettere, quel potere diventa calcolabile. Poco basta: non serve un nome molto diverso perché l'energia si sposti.",
        "Il nome completo non può essere modificato: è l'identità di registro. Il soprannome, sì: può essere scelto, provato e adattato fino a trovare l'energia che meglio rappresenta il modo in cui la persona viene chiamata. Per questo è facile capire perché l'energia cambia quando cambiamo un qualsiasi elemento di un processo — questa è la magia della matematica nel suono: pura energia calcolabile.",
        "Anche i titoli come Dott., Sig., Sig.ra o Seu si sommano. Se la persona viene chiamata \"Seu Antônio\" o \"Dott. Tonho\", scriva il soprannome esattamente così — il trattamento fa parte del nome d'uso ed entra nel calcolo.",
    ],
    "fr": [
        "Quel nom compte ? Le plus utilisé. Le principe de l'énergie est simple : plus un nom est répété, plus sa vibration s'affirme. Dans le milieu professionnel, le nom qui circule dans les couloirs, les réunions et les appels informels est le surnom — et c'est lui qui décrit le comportement réel de la personne dans l'équipe.",
        "Tout peut se mesurer en énergie — y compris le son que nous émettons en communiquant. Le mot a du pouvoir. Mot écrit et parlé : au moment où nous donnons une valeur de nombre aux lettres, ce pouvoir devient calculable. Peu suffit : il n'est pas nécessaire qu'un nom soit très différent pour que l'énergie se déplace.",
        "Le nom complet ne peut pas être modifié : c'est l'identité d'enregistrement. Le surnom, oui : il peut être choisi, testé et ajusté jusqu'à trouver l'énergie qui représente le mieux la façon dont la personne est appelée. C'est pourquoi il devient facile de comprendre pourquoi l'énergie change quand nous changeons un quelconque élément d'un processus — c'est la magie des mathématiques dans le son : pure énergie calculable.",
        "Les titres comme Dr, M., Mme ou Seu s'additionnent aussi. Si la personne est appelée « Seu Antônio » ou « Dr Tonho », écrivez le surnom exactement ainsi — le traitement fait partie du nom d'usage et entre dans le calcul.",
    ],
    "de": [
        "Welcher Name zählt? Der am häufigsten verwendete. Das Prinzip der Energie ist einfach: Je öfter ein Name wiederholt wird, desto mehr setzt sich seine Schwingung durch. Am Arbeitsplatz ist der Name, der in Fluren, Besprechungen und informellen Gesprächen kursiert, der Rufname — und er beschreibt, wie sich die Person im Team tatsächlich verhält.",
        "Alles lässt sich in Energie messen — auch der Schall, den wir beim Kommunizieren aussenden. Das Wort hat Macht. Geschriebenes und gesprochenes Wort: In dem Moment, in dem wir den Buchstaben einen Zahlenwert geben, wird diese Macht berechenbar. Wenig genügt: Der Name muss sich nicht stark unterscheiden, damit sich die Energie verschiebt.",
        "Der vollständige Name lässt sich nicht ändern: Er ist die Identität der Registrierung. Der Rufname schon: Er kann gewählt, getestet und angepasst werden, bis er die Energie findet, die die Art und Weise, wie die Person genannt wird, am besten widerspiegelt. Deshalb ist leicht zu verstehen, warum sich die Energie ändert, wenn wir irgendein Element eines Prozesses ändern — das ist die Magie der Mathematik im Klang: reine berechenbare Energie.",
        "Auch Titel wie Dr., Herr, Frau oder Seu zählen mit. Wenn die Person „Seu Antônio\" oder „Dr. Tonho\" genannt wird, schreiben Sie den Rufnamen genau so — die Anrede gehört zum Gebrauchsnamen und fließt in die Berechnung ein.",
    ],
    "ja": [
        "どの名前が優先されるのか。最も使われている名前です。エネルギーの原理は単純です。名前は繰り返されるほど、その波動が強く定着します。職場では、廊下や会議、日常の呼びかけで交わされる名前が呼び名であり、その呼び名こそがチーム内での実際の振る舞いを表します。",
        "すべてはエネルギーで測ることができます。私たちがコミュニケーションで発する音も含まれます。言葉には力があります。書かれた言葉も話された言葉も、文字に数の値を与えた瞬間、その力は計算可能になります。わずかな違いで十分です。名前が大きく異なる必要はなく、エネルギーは動きます。",
        "本名は変えられません。それは登録上の身元だからです。呼び名は変えられます。どう呼ばれているかを最もよく表すエネルギーが見つかるまで、選び、試し、調整することができます。だからこそ、あるプロセスの要素を一つ変えるだけでエネルギーが変わる理由が容易に理解できます。これが音の中の数学の魔法、計算できる純粋なエネルギーです。",
        "Dr.、Mr.、Sra.、Seu といった敬称も加算されます。「Seu Antônio」や「Dr. Tonho」と呼ばれている場合は、呼び名をそのまま記入してください。敬称は使用名の一部であり、計算に含まれます。",
    ],
    "zh": [
        "哪个名字算数？最常用的那个。能量的原理很简单：一个名字被重复得越多，它的振动就越牢固。在工作环境中，在走廊、会议和日常称呼中流传的名字就是称呼名——正是它描述了此人在团队中的真实表现。",
        "一切都可以用能量来衡量——包括我们交流时发出的声音。词语有力量。无论是书写的还是说出的词语，当我们赋予字母数值的那一刻，这种力量就变得可以计算。一点点差异就足够：名字不必差别很大，能量就会移动。",
        "全名无法更改：它是登记的身份。称呼名可以：可以选择、测试和调整，直到找到最能代表此人被称呼方式的能量。因此很容易理解，为什么改变一个流程中的任何要素，能量就会改变——这就是声音中数学的魔力：纯粹可计算的能量。",
        "Dr.、先生、女士或 Seu 之类的称谓也会累加。如果此人被称为“Seu Antônio”或“Dr. Tonho”，请完全按照这样填写称呼名——称谓是使用名的一部分，会进入计算。",
    ],
    "ru": [
        "Какое имя считается? То, которое используется чаще. Принцип энергии прост: чем чаще повторяется имя, тем сильнее утверждается его вибрация. В рабочей среде имя, которое звучит в коридорах, на совещаниях и в неформальных разговорах, — это имя в обиходе, и именно оно описывает реальное поведение человека в команде.",
        "Всё можно измерить в энергии — включая звук, который мы издаём при общении. Слово обладает силой. Слово написанное и произнесённое: в тот момент, когда мы придаём буквам числовое значение, эта сила становится вычислимой. Достаточно малого: имя не должно сильно отличаться, чтобы энергия сместилась.",
        "Полное имя изменить нельзя: это идентичность записи. Имя в обиходе — можно: его выбирают, проверяют и корректируют, пока не найдётся энергия, которая лучше всего отражает то, как человека называют. Поэтому легко понять, почему энергия меняется, когда мы меняем любой элемент процесса, — это магия математики в звуке: чистая вычислимая энергия.",
        "Титулы вроде Dr., г-н, г-жа или Seu тоже суммируются. Если человека называют «Seu Antônio» или «Dr. Tonho», напишите имя в обиходе именно так — обращение является частью используемого имени и входит в расчёт.",
    ],
    "he": [
        "איזה שם נחשב? זה שבשימוש הרב ביותר. עקרון האנרגיה פשוט: ככל ששם חוזר יותר, כך התנודה שלו מתבססת. בסביבת העבודה, השם שמסתובב במסדרונות, בפגישות ובפניות יומיומיות הוא שם בשימוש — והוא מתאר את ההתנהגות בפועל של האדם בצוות.",
        "הכול ניתן למדוד באנרגיה — כולל הצליל שאנו מפיקים בתקשורת. למילה יש כוח. מילה כתובה ומילה מדוברת: ברגע שאנו נותנים לאותיות ערך מספרי, הכוח הזה הופך לישים לחישוב. מעט כבר משנה: השם לא צריך להיות שונה מאוד כדי שהאנרגיה תזוז.",
        "את השם המלא אי אפשר לשנות: זו הזהות הרשומה. את השם בשימוש כן: אפשר לבחור, לנסות ולכוונן עד שנמצא האנרגיה שמייצגת בצורה הטובה ביותר את האופן שבו האדם נקרא. לכן קל להבין מדוע האנרגיה משתנה כשמשנים מרכיב כלשהו בתהליך — זהו הקסם של המתמטיקה בצליל: אנרגיה טהורה שניתנת לחישוב.",
        "גם תארים כמו Dr., מר, גב' או Seu מצטרפים. אם האדם נקרא \"Seu Antônio\" או \"Dr. Tonho\", כתבו את השם בשימוש בדיוק כך — התואר הוא חלק מהשם בשימוש ונכנס לחישוב.",
    ],
    "ar": [
        "أي اسم يُحتسب؟ الأكثر استخدامًا. مبدأ الطاقة بسيط: كلما تكرر الاسم أكثر، ترسّخ ذبذبه أقوى. في بيئة العمل، الاسم الذي يدور في الممرات والاجتماعات والنداءات اليومية هو الاسم المتداول — وهو الذي يصف السلوك الفعلي للشخص داخل الفريق.",
        "كل شيء يمكن قياسه بالطاقة — بما في ذلك الصوت الذي نصدره عند التواصل. للكلمة سلطة. الكلمة المكتوبة والمنطوقة: في اللحظة التي نمنح فيها الحروف قيمة عددية، تصبح هذه السلطة قابلة للحساب. القليل يكفي: لا يحتاج الاسم إلى اختلاف كبير حتى تتحرك الطاقة.",
        "لا يمكن تغيير الاسم الكامل: فهو هوية التسجيل. أما الاسم المتداول فنعم: يمكن اختياره واختباره وتعديله حتى يُعثر على الطاقة التي تمثّل على أفضل وجه الطريقة التي يُنادى بها الشخص. ولهذا يسهل فهم سبب تغيّر الطاقة عندما نغيّر أي عنصر في أي عملية — هذا هو سحر الرياضيات في الصوت: طاقة خالصة قابلة للحساب.",
        "الألقاب مثل Dr. والسيد والسيدة وSeu تُجمع أيضًا. إذا كان الشخص يُنادى بـ\"Seu Antônio\" أو \"Dr. Tonho\"، فاكتب الاسم المتداول بهذا الشكل تمامًا — فاللقب جزء من الاسم المستخدم ويدخل في الحساب.",
    ],
    "id": [
        "Nama mana yang dihitung? Yang paling sering dipakai. Prinsip energinya sederhana: semakin sering sebuah nama diulang, semakin kuat getarannya mengendap. Di lingkungan kerja, nama yang beredar di lorong, rapat, dan sapaan sehari-hari adalah nama panggilan — dan itulah yang menggambarkan perilaku nyata orang tersebut di tim.",
        "Segala sesuatu dapat diukur dengan energi — termasuk bunyi yang kita keluarkan saat berkomunikasi. Kata memiliki kekuatan. Kata tertulis dan terucap: saat kita memberi nilai angka pada huruf-hurufnya, kekuatan itu menjadi dapat dihitung. Sedikit saja sudah cukup: nama tidak perlu berbeda jauh agar energinya bergeser.",
        "Nama lengkap tidak dapat diubah: itu identitas resmi. Nama panggilan bisa: dapat dipilih, diuji, dan disesuaikan hingga menemukan energi yang paling mewakili cara orang itu dipanggil. Karena itu mudah dipahami mengapa energi berubah ketika kita mengubah salah satu unsur dalam suatu proses — inilah keajaiban matematika dalam bunyi: energi murni yang dapat dihitung.",
        "Sapaan seperti Dr., Bapak, Ibu, atau Seu juga dijumlahkan. Jika orang tersebut dipanggil \"Seu Antônio\" atau \"Dr. Tonho\", tulis nama panggilannya persis seperti itu — sapaan adalah bagian dari nama yang dipakai dan masuk ke dalam perhitungan.",
    ],
    "tr": [
        "Hangi ad sayılır? En çok kullanılan. Enerjinin ilkesi basittir: bir ad ne kadar çok tekrarlanırsa titreşimi o kadar güçlü yerleşir. İş ortamında koridorlarda, toplantılarda ve günlük seslenişlerde dolaşan ad takma addır — ve kişinin ekipte gerçekte nasıl davrandığını da o anlatır.",
        "Her şey enerjiyle ölçülebilir — iletişim kurarken çıkardığımız ses de buna dahil. Sözün gücü vardır. Yazılı ve sözlü söz: harflere sayı değeri verdiğimiz anda bu güç hesaplanabilir hale gelir. Az da yeter: enerjinin kayması için adın çok farklı olması gerekmez.",
        "Tam ad değiştirilemez: kayıt kimliğidir. Takma ad ise değişebilir: kişinin nasıl çağrıldığını en iyi temsil eden enerji bulunana kadar seçilebilir, denenebilir ve ayarlanabilir. Bu yüzden bir süreçteki herhangi bir öğeyi değiştirdiğimizde enerjinin neden değiştiğini anlamak kolaylaşır — sesin içindeki matematiğin büyüsü budur: saf, hesaplanabilir enerji.",
        "Dr., Bay, Bayan veya Seu gibi unvanlar da toplanır. Kişi \"Seu Antônio\" ya da \"Dr. Tonho\" diye çağrılıyorsa, takma adı tam olarak böyle yazın — unvan kullanılan adın parçasıdır ve hesaba girer.",
    ],
    "vi": [
        "Cái tên nào được tính? Tên được dùng nhiều nhất. Nguyên lý của năng lượng rất đơn giản: một cái tên càng được lặp lại nhiều, dao động của nó càng bám rễ vững. Trong môi trường làm việc, cái tên lưu hành ở hành lang, trong các cuộc họp và những lời gọi thường ngày chính là tên gọi — và chính nó mô tả cách hành xử thật sự của người đó trong đội ngũ.",
        "Mọi thứ đều có thể đo bằng năng lượng — kể cả âm thanh chúng ta phát ra khi giao tiếp. Ngôn từ có sức mạnh. Ngôn từ viết và ngôn từ nói: ngay khi ta gán giá trị số cho các chữ cái, sức mạnh đó trở nên có thể tính toán. Chỉ một chút cũng đủ: cái tên không cần khác biệt nhiều để năng lượng dịch chuyển.",
        "Họ tên đầy đủ không thể thay đổi: đó là danh tính đăng ký. Tên gọi thì có thể: có thể chọn, thử và điều chỉnh cho đến khi tìm được năng lượng thể hiện đúng nhất cách người đó được gọi. Vì thế, thật dễ hiểu vì sao năng lượng thay đổi khi ta thay đổi bất kỳ yếu tố nào trong một quá trình — đó là phép màu của toán học trong âm thanh: năng lượng thuần túy có thể tính được.",
        "Các danh xưng như Dr., Ông, Bà hay Seu cũng được cộng vào. Nếu người đó được gọi là \"Seu Antônio\" hoặc \"Dr. Tonho\", hãy viết tên gọi đúng như vậy — danh xưng là một phần của tên đang dùng và đi vào phép tính.",
    ],
}

# ---------- FAMÍLIA / EQUIPES ----------
def _pdf_relacao(produto, dados, lang, contexto, tag):
    lang = lang or "pt"
    dados = dict(dados or {})
    L = _rel(lang)
    _b_nome, _b_apel, _b_sint, _lbl_apel = _L_BLOCO.get(lang) or _L_BLOCO["pt"]
    fr, fb, titulo = _rel_abre(produto, lang)
    path = _rel_path(tag)
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=50, rightMargin=50,
                            topMargin=45, bottomMargin=45)
    e = []
    _rel_cabecalho(e, titulo, dados.get("titular") or dados.get("nome") or "", lang, fr, fb)
    for _ab in ABERTURA_RELACAO.get(lang) or ABERTURA_RELACAO["pt"]:
        e.append(Paragraph(_rel_escape(_ab),
                           _estilo("ABERT", fr, 9, DARK, TA_JUSTIFY, sa=LINHA * 0.6)))
    e.append(Spacer(1, LINHA))  
    if produto == "compatibilidade_equipes":
        try:
            from referencia import relacao_dupla as _rd
            txt = _rd.explicacao(lang)
            if txt:
                e.append(Spacer(1, LINHA * 0.8))
                for _par in txt.split("\n"):
                    if _par.strip():
                        e.append(Paragraph(_rel_escape(_par),
                                           _estilo("EXP", fr, 9, DARK, TA_JUSTIFY, sa=LINHA * 0.4)))
                e.append(Spacer(1, LINHA * 0.8))
        except Exception:
            pass

    membros = dados.get("membros") or []
    pares = dados.get("pares") or []
    total = dados.get("total") or len(membros)
    tem_papel = any(str(m.get("papel") or "").strip() for m in membros)

    def _cn(m):
        return Paragraph(_rel_escape(m.get("membro", "")), _estilo("TC", fr, 9, DARK, TA_LEFT))

    def _ca(m):
        ap = str(m.get("apelido") or "").strip()
        return Paragraph(_rel_escape(ap) if ap else "—", _estilo("TAp", fr, 9, DARK, TA_LEFT))

    # ===== BLOCO 1 — NOME COMPLETO =====
    if membros:
        e.append(Spacer(1, LINHA * 1.5))
        e.append(Paragraph(_rel_escape(_b_nome), _estilo("B1", fb, 14, GOLD, TA_LEFT, sa=LINHA * 0.5)))
        e.append(Paragraph(f"{L['membros']}: {total}", _estilo("MT", fb, 11, DARK, TA_LEFT, sa=LINHA * 0.5)))
        if tem_papel:
            linhas = [[L["membros"], L["papel"], L["energia"], L["vida"]]]
            for m in membros:
                papel = str(m.get("papel") or "").strip()
                linhas.append([_cn(m),
                               _rel_escape(L.get(papel, papel) if papel else ""),
                               str(m.get("energia", "") or ""),
                               str(m.get("caminho_vida") or "—")])
            larguras = [165, 115, 65, 105]
        else:
            linhas = [[L["membros"], L["energia"], L["vida"]]]
            for m in membros:
                linhas.append([_cn(m),
                               str(m.get("energia", "") or ""),
                               str(m.get("caminho_vida") or "—")])
            larguras = [265, 85, 145]
        e.append(_rel_tabela(linhas, larguras, fr))
        e.append(Spacer(1, LINHA))

    # ===== BLOCO 2 — APELIDO =====
    if any(str(m.get("apelido") or "").strip() for m in membros):
        _rel_separador(e, _b_apel, fb)
        e.append(Paragraph(f"{L['membros']}: {total}", _estilo("MT2", fb, 11, DARK, TA_LEFT, sa=LINHA * 0.5)))
        if tem_papel:
            linhas = [[_lbl_apel, L["papel"], L["energia"], L["vida"]]]
            for m in membros:
                papel = str(m.get("papel") or "").strip()
                linhas.append([_ca(m),
                               _rel_escape(L.get(papel, papel) if papel else ""),
                               str(m.get("energia_combinada_apelido") or "—"),
                               str(m.get("caminho_vida") or "—")])
            larguras = [165, 115, 65, 105]
        else:
            linhas = [[_lbl_apel, L["energia"], L["vida"]]]
            for m in membros:
                linhas.append([_ca(m),
                               str(m.get("energia_combinada_apelido") or "—"),
                               str(m.get("caminho_vida") or "—")])
            larguras = [265, 85, 145]
        e.append(_rel_tabela(linhas, larguras, fr))
        e.append(Spacer(1, LINHA))
        for p in pares:
            ap1 = (p.get("apelido1") or "").strip()
            ap2 = (p.get("apelido2") or "").strip()
            if not (ap1 and ap2):
                continue
            comp_a = p.get("compatibilidade_apelido")
            e.append(Paragraph("<b>%s × %s</b>" % (_rel_escape(ap1), _rel_escape(ap2)),
                               _estilo("A1", fb, 11, DARK, TA_LEFT, sa=2)))
            e.append(Paragraph("%s: <b>%s</b> — %s" % (
                L["compat"], comp_a if comp_a is not None else "—",
                _rel_escape(_rel_grau(comp_a, lang) if comp_a is not None else "")),
                _estilo("A2", fr, 10, DARK, TA_LEFT, sa=2)))
            if comp_a == 1:
                e.append(Paragraph(_rel_escape(_sugestao_grau1(lang, produto)),
                                   _estilo("SUG1", fr, 9, colors.HexColor("#8a6d1f"),
                                           TA_JUSTIFY, sa=LINHA * 0.4)))
            if comp_a is not None:
                lt = get_compat(comp_a, contexto, lang)
                if lt:
                    e.append(Paragraph(_rel_escape(lt), _estilo("A3", fr, 9, DARK, TA_JUSTIFY, sa=2)))
                dl = get_dual(comp_a, contexto, lang)
                if dl:
                    e.append(Paragraph(_rel_escape(dl),
                                       _estilo("A4", fr, 9, colors.HexColor("#8a6d1f"), TA_JUSTIFY, sa=LINHA * 0.4)))
                try:
                    from referencia import relacao_dupla as _rc2
                    for tit, itens in _rc2.bloco(int(comp_a), lang):
                        e.append(Spacer(1, LINHA * 0.5))
                        e.append(Paragraph("<b>%s</b>" % _rel_escape(tit),
                                           _estilo("RF2", fb, 10, GOLD, TA_LEFT, sa=LINHA * 0.3)))
                        for it in itens:
                            e.append(Paragraph("• %s" % _rel_escape(it),
                                               _estilo("RI2", fr, 9, DARK, TA_JUSTIFY, sa=LINHA * 0.25)))
                except Exception:
                    pass
            e.append(Spacer(1, LINHA * 0.7))

        # ===== BLOCO 3 — SÍNTESE =====
        _l_nome, _l_uso = _L_SINT.get(lang) or _L_SINT["pt"]
        linhas_s = [[L["pares"], _l_nome, _l_uso]]
        for p in pares:
            ap1 = (p.get("apelido1") or "").strip()
            ap2 = (p.get("apelido2") or "").strip()
            rot = "%s × %s" % (ap1 or p.get("membro1", ""), ap2 or p.get("membro2", ""))
            linhas_s.append([_rel_escape(rot),
                             str(p.get("compatibilidade")) if p.get("compatibilidade") is not None else "—",
                             str(p.get("compatibilidade_apelido")) if p.get("compatibilidade_apelido") is not None else "—"])
        if len(linhas_s) > 1:
            _rel_separador(e, _b_sint, fb)
            e.append(_rel_tabela(linhas_s, [235, 130, 130], fr))

    if not membros and not pares:
        e.append(Paragraph(L["sem_dados"], _estilo("ND", fr, 10, GRAY, TA_LEFT, sa=LINHA)))

    _rel_fecha(doc, e, lang, fr)
    return path

def pdf_familia(dados, lang="pt"):
    return _pdf_relacao("familia", dados, lang, "familia", "familia")


def pdf_equipe(dados, lang="pt"):
    return _pdf_relacao("compatibilidade_equipes", dados, lang, "equipe", "equipe")

AVISO_QR = {
    "pt": "Link do QRCode válido por 1 hora. Salve este PDF agora. Não armazenamos cópias.",
    "en": "QRCode link valid for 1 hour. Save this PDF now. We do not store copies.",
    "es": "Enlace del código QR válido por 1 hora. Guarde este PDF ahora. No almacenamos copias.",
    "it": "Link del QRCode valido per 1 ora. Salva questo PDF ora. Non conserviamo copie.",
    "fr": "Lien du QRCode valable 1 heure. Enregistrez ce PDF maintenant. Nous ne conservons aucune copie.",
    "de": "QRCode-Link 1 Stunde gültig. Speichern Sie dieses PDF jetzt. Wir speichern keine Kopien.",
    "ja": "QRコードのリンクは1時間有効です。今すぐこのPDFを保存してください。当社はコピーを保存しません。",
    "zh": "二维码链接有效期 1 小时。请立即保存此 PDF。我们不保存副本。",
    "ru": "Ссылка в QR-коде действует 1 час. Сохраните этот PDF сейчас. Мы не храним копии.",
    "id": "Tautan QRCode berlaku 1 jam. Simpan PDF ini sekarang. Kami tidak menyimpan salinan.",
    "tr": "QRCode bağlantısı 1 saat geçerlidir. Bu PDF'i şimdi kaydedin. Kopya saklamıyoruz.",
    "vi": "Liên kết QRCode có hiệu lực 1 giờ. Hãy lưu PDF này ngay. Chúng tôi không lưu bản sao.",
    "he": "קישור ה-QRCode תקף לשעה אחת. שמרו את ה-PDF הזה עכשיו. איננו שומרים עותקים.",
    "ar": "رابط رمز QR صالح لمدة ساعة واحدة. احفظ هذا الملف الآن. نحن لا نحتفظ بنسخ.",
}