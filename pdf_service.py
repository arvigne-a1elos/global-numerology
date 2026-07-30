# pdf_service.py - Geração de PDFs com template premium (ReportLab)
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

# Cores do template premium
GOLD = colors.HexColor("#C9A94E")
DARK = colors.HexColor("#1a1a1a")
LGRAY = colors.HexColor("#f5f5f0")
WHITE = colors.white
GRAY = colors.HexColor("#888888")

FN = "Helvetica"
FONTE = "Helvetica"
TAM_T = 28
TAM_C = 12
EL = 12
ET = 6

def _estilo(nome, fonte, tam, cor, alinhamento, sa=0, sb=0):
    return ParagraphStyle(nome, fontName=fonte, fontSize=tam, textColor=cor,
                          alignment=alinhamento, spaceAfter=sa, spaceBefore=sb,
                          leading=tam * 1.4)

def _cabecalho_pagina(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(colors.HexColor("#C9A94E"))
    canvas.setFont("Helvetica", 7)
    canvas.setFillAlpha(0.15)
    canvas.drawString(30, 15, "A1ELOS Assessoria e Consultoria")
    canvas.restoreState()

# ═══════════════════════════════════════════
# PDF8 - MAPA EXPRESS (1 página premium)
# ═══════════════════════════════════════════
def pdf8(data, nome, bd):
    path = f"/tmp/p8_{uuid.uuid4().hex[:8]}.pdf"
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=50, rightMargin=50, topMargin=45, bottomMargin=45)
    e = []
    e.append(Spacer(1, 20))
    e.append(Paragraph("MAPA NUMEROLÓGICO", _estilo("T", FN, TAM_T, GOLD, TA_CENTER, sa=ET)))
    e.append(Paragraph("EXPRESS", _estilo("S", FONTE, 16, GOLD, TA_CENTER, sa=4)))
    e.append(Paragraph(nome.upper(), _estilo("N", FN, 14, DARK, TA_CENTER, sa=4)))
    e.append(Paragraph(bd, _estilo("D", FONTE, 10, GRAY, TA_CENTER, sa=EL)))
    td = [["Número", "Valor", "Significado"],
          ["Caminho de Vida", str(data["life_path"]), "Propósito central da sua existência"],
          ["Expressão", str(data["expression"]), "Seus talentos e habilidades naturais"],
          ["Motivação da Alma", str(data["soul_urge"]), "O desejo mais profundo do seu ser"],
          ["Personalidade", str(data["personality"]), "Como o mundo te percebe"],
          ["Destino", str(data["destiny"]), "A missão que você veio realizar"]]
    tbl = Table(td, colWidths=[180, 60, 220])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GOLD), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTSIZE", (0, 0), (-1, -1), 9), ("FONTNAME", (0, 0), (-1, -1), FONTE),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (1, 0), (1, -1), "CENTER"), ("ALIGN", (2, 0), (2, -1), "LEFT"),
        ("BACKGROUND", (0, 1), (-1, -1), LGRAY), ("TEXTCOLOR", (0, 1), (-1, -1), DARK),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    e.append(tbl)
    e.append(Spacer(1, EL))
    TX = {1: "Líder nato, pioneiro, independente.", 2: "Diplomata, sensível, cooperativo.",
          3: "Criativo, comunicador, otimista.", 4: "Prático, disciplinado, estável.",
          5: "Livre, aventureiro, versátil.", 6: "Amoroso, responsável, familiar.",
          7: "Sábio, espiritual, analítico.", 8: "Poderoso, próspero, realizado.",
          9: "Humanitário, generoso, compassivo.", 11: "Mestre intuitivo, iluminado.",
          22: "Mestre construtor, visionário."}
    for k, l in [("life_path", "Caminho de Vida"), ("expression", "Expressão"),
                 ("soul_urge", "Motivação"), ("personality", "Personalidade"),
                 ("destiny", "Destino")]:
        v = data[k]
        desc = TX.get(v, f"Número {v}")
        e.append(Paragraph(f"<b>{l}:</b> {v} — {desc}", _estilo("TX", FONTE, 10, DARK, TA_LEFT, sa=3)))
    e.append(Spacer(1, EL))
    e.append(Paragraph("© A1ELOS Assessoria e Consultoria", _estilo("F", FONTE, 8, GRAY, TA_CENTER)))
    doc.build(e, onFirstPage=_cabecalho_pagina, onLaterPages=_cabecalho_pagina)
    return path

# ═══════════════════════════════════════════
# PDF17 - MAPA COMPLETO (template premium)
# ═══════════════════════════════════════════
def pdf17(data, nome, bd_str, lang="pt"):
    path = f"/tmp/p17_{uuid.uuid4().hex[:8]}.pdf"
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=50, rightMargin=50, topMargin=45, bottomMargin=45)
    e = []
    lp = data["life_path"]
    _, desc_cam = CAM.get(lp, ("", ""))
    # CAPA
    e.append(Spacer(1, 120))
    e.append(Paragraph("MAPA NUMEROLÓGICO", _estilo("T", FN, 32, GOLD, TA_CENTER, sa=ET)))
    e.append(Paragraph("COMPLETO", _estilo("S", FONTE, 18, GOLD, TA_CENTER, sa=10)))
    e.append(Spacer(1, 20))
    e.append(Paragraph("Uma jornada profunda pelos números que regem sua essência,", _estilo("SUB", FONTE, 11, GRAY, TA_CENTER, sa=2)))
    e.append(Paragraph("seu propósito e seu destino.", _estilo("SUB", FONTE, 11, GRAY, TA_CENTER, sa=EL)))
    e.append(Spacer(1, 40))
    e.append(Paragraph(nome.upper(), _estilo("NOME", FN, 16, DARK, TA_CENTER, sa=4)))
    e.append(Paragraph(bd_str, _estilo("DATA", FONTE, 11, GRAY, TA_CENTER, sa=EL)))
    e.append(Spacer(1, 30))
    e.append(Paragraph(f"Caminho da Vida: <b>{lp}</b> — {desc_cam}", _estilo("CV", FN, 12, GOLD, TA_CENTER, sa=EL)))
    e.append(PageBreak())
    # TABELA DOS 5 NÚMEROS
    e.append(Paragraph("Seus Números Principais", _estilo("SEC", FN, 18, GOLD, TA_LEFT, sb=EL, sa=EL)))
    td = [["Número", "Categoria", "Valor"],
          ["Caminho de Vida", "Propósito", str(data["life_path"])],
          ["Expressão", "Talentos", str(data["expression"])],
          ["Motivação da Alma", "Desejo Interno", str(data["soul_urge"])],
          ["Personalidade", "Imagem Externa", str(data["personality"])],
          ["Destino", "Missão", str(data["destiny"])]]
    tbl = Table(td, colWidths=[180, 150, 80])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GOLD), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTSIZE", (0, 0), (-1, -1), 10), ("FONTNAME", (0, 0), (-1, -1), FONTE),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey), ("ALIGN", (2, 0), (2, -1), "CENTER"),
        ("BACKGROUND", (0, 1), (-1, -1), LGRAY), ("TEXTCOLOR", (0, 1), (-1, -1), DARK),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    e.append(tbl)
    e.append(Spacer(1, EL))
    # ANÁLISE DETALHADA
    e.append(Paragraph("Análise Detalhada dos Números", _estilo("SEC", FN, 18, GOLD, TA_LEFT, sb=EL, sa=EL)))
    e.append(Paragraph("Cada número carrega uma vibração única que molda aspectos específicos da sua vida. Cada número de 1 a 9 — além dos mestres 11 e 22 — possui significados positivos, sombras e uma lição essencial de vida.", _estilo("J", FONTE, 10, DARK, TA_JUSTIFY, sa=EL)))
    for k, l in [("life_path", "Caminho de Vida"), ("expression", "Expressão"),
                 ("soul_urge", "Motivação"), ("personality", "Personalidade"),
                 ("destiny", "Destino")]:
        v = data[k]
        nm, pos, neg, licao = SIG.get(v, ("", "", "", ""))
        e.append(Paragraph(f"<b>{l} {v} — {nm}</b>", _estilo("BL", FN, 10, DARK, TA_LEFT, sa=3)))
        e.append(Paragraph(f"<b>Positivo:</b> {pos}", _estilo("JP", FONTE, 9, DARK, TA_LEFT, sa=2)))
        e.append(Paragraph(f"<b>Negativo:</b> {neg}", _estilo("JP", FONTE, 9, DARK, TA_LEFT, sa=2)))
        e.append(Paragraph(f"<b>Lição:</b> {licao}", _estilo("JP", FONTE, 9, DARK, TA_LEFT, sa=6)))
    e.append(Paragraph("<i>Os números mestres 11 e 22 carregam uma responsabilidade espiritual mais elevada e não são reduzidos, pois representam potencial de transformação coletiva.</i>", _estilo("J", FONTE, 9, GRAY, TA_JUSTIFY, sa=EL)))
    e.append(PageBreak())
    # CAMINHO DA VIDA E CICLOS
    e.append(Paragraph("Caminho da Vida e Ciclos", _estilo("SEC", FN, 18, GOLD, TA_LEFT, sb=EL, sa=EL)))
    e.append(Paragraph(f"<b>Caminho da Vida {lp}:</b> {desc_cam}", _estilo("J", FONTE, 11, DARK, TA_JUSTIFY, sa=EL)))
    e.append(Spacer(1, 6))
    try:
        dt = dp.parse(bd_str)
        mes, dia, ano = reduzir(dt.month), reduzir(dt.day), reduzir(dt.year)
    except:
        mes, dia, ano = 0, 0, 0
    ciclos = [["Ciclo", "Período", "Número", "Significado"],
              ["1º — Formativo", "0 a 28/36 anos", str(mes), "Aprendizado, formação de identidade"],
              ["2º — Produtivo", "28/36 a 54/63 anos", str(dia), "Realização, carreira, construção"],
              ["3º — Colheita", "54/63 anos em diante", str(ano), "Integração, sabedoria, colheita"]]
    tbl3 = Table(ciclos, colWidths=[120, 120, 60, 160])
    tbl3.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GOLD), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTSIZE", (0, 0), (-1, -1), 9), ("FONTNAME", (0, 0), (-1, -1), FONTE),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey), ("ALIGN", (2, 0), (2, -1), "CENTER"),
        ("BACKGROUND", (0, 1), (-1, -1), LGRAY), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    e.append(tbl3)
    e.append(Spacer(1, EL))
    # DESAFIOS
    e.append(Paragraph("Desafios e Realizações", _estilo("SEC", FN, 18, GOLD, TA_LEFT, sb=EL, sa=EL)))
    e.append(Paragraph("Os desafios e realizações são períodos de aprendizado e oportunidade calculados diretamente a partir da data de nascimento. Eles revelam os temas centrais que surgirão ao longo da vida para impulsionar o crescimento pessoal e espiritual.", _estilo("J", FONTE, 10, DARK, TA_JUSTIFY, sa=EL)))
    e.append(Spacer(1, 6))
    try:
        dt = dp.parse(bd_str)
        m, d, a = dt.month, dt.day, dt.year
        m_r, d_r, a_r = reduzir(m), reduzir(d), reduzir(a)
        d1, d2 = abs(m_r - d_r), abs(d_r - a_r)
        dp_ = abs(d1 - d2)
    except:
        d1, d2, dp_ = 0, 0, 0
    desafios = [["Desafio", "Cálculo", "Valor"],
                ["1º Desafio Menor", f"|{m_r} - {d_r}|", str(d1)],
                ["2º Desafio Menor", f"|{d_r} - {a_r}|", str(d2)],
                ["Desafio Principal", f"|{d1} - {d2}|", str(dp_)]]
    tbl4 = Table(desafios, colWidths=[150, 150, 80])
    tbl4.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GOLD), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTSIZE", (0, 0), (-1, -1), 9), ("FONTNAME", (0, 0), (-1, -1), FONTE),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey), ("ALIGN", (2, 0), (2, -1), "CENTER"),
        ("BACKGROUND", (0, 1), (-1, -1), LGRAY), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    e.append(tbl4)
    e.append(Spacer(1, EL))
    e.append(PageBreak())
    # GRADE DE INCLUSÃO
    e.append(Paragraph("Grade de Inclusão", _estilo("SEC", FN, 18, GOLD, TA_LEFT, sb=EL, sa=EL)))
    e.append(Paragraph("A Grade de Inclusão mapeia a frequência com que cada número de 1 a 9 aparece nas letras do seu nome completo de nascimento. Números ausentes indicam áreas de aprendizado; números frequentes revelam tendências dominantes.", _estilo("J", FONTE, 10, DARK, TA_JUSTIFY, sa=EL)))
    e.append(Spacer(1, 6))
    grid = calc_grid(nome)
    grid_data = [["Nº", "Frequência", "Nº", "Frequência", "Nº", "Frequência"]]
    for i in range(3):
        n1, n2, n3 = i * 3 + 1, i * 3 + 2, i * 3 + 3
        grid_data.append([str(n1), str(grid.get(n1, 0)), str(n2), str(grid.get(n2, 0)), str(n3), str(grid.get(n3, 0))])
    tbl5 = Table(grid_data, colWidths=[40, 80, 40, 80, 40, 80])
    tbl5.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GOLD), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTSIZE", (0, 0), (-1, -1), 10), ("FONTNAME", (0, 0), (-1, -1), FONTE),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey), ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BACKGROUND", (0, 1), (-1, -1), LGRAY), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    e.append(tbl5)
    e.append(Spacer(1, EL))
    # VIBRAÇÃO DO DIA
    e.append(Paragraph("Vibração do Dia do Nascimento", _estilo("SEC", FN, 18, GOLD, TA_LEFT, sb=EL, sa=EL)))
    try:
        dt = dp.parse(bd_str)
        vib_dia = reduzir(dt.day)
        e.append(Paragraph(f"<b>Dia {dt.day} → {vib_dia}</b> — O número do dia em que você nasceu carrega uma vibração específica que influencia diretamente suas atitudes, habilidades instintivas e a forma como você reage ao mundo. Representa seus dons mais espontâneos e naturais.", _estilo("J", FONTE, 10, DARK, TA_JUSTIFY, sa=EL)))
    except:
        pass
    e.append(Spacer(1, EL))
    # ENCERRAMENTO
    e.append(Spacer(1, 30))
    e.append(Paragraph("Este mapa numerológico foi gerado com base nos ensinamentos da numerologia pitagórica. Os números revelam tendências e potenciais, mas o livre arbítrio é sempre seu maior poder.", _estilo("J", FONTE, 10, GRAY, TA_CENTER, sa=EL)))
    e.append(Paragraph("© A1ELOS Assessoria e Consultoria", _estilo("F", FONTE, 8, GRAY, TA_CENTER)))
    doc.build(e, onFirstPage=_cabecalho_pagina, onLaterPages=_cabecalho_pagina)
    return path

# ═══════════════════════════════════════════
# PDF URNA (100% preservado do original)
# ═══════════════════════════════════════════
def pdf_urna(nc, cl, resultados, sugestoes):
    path = f"/tmp/u_{uuid.uuid4().hex[:8]}.pdf"
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=50, rightMargin=50, topMargin=45, bottomMargin=45)
    e = []
    e.append(Spacer(1, 25))
    e.append(Paragraph("VALIDAÇÃO DE NOME DE URNA", _estilo("T", FN, TAM_T, GOLD, TA_CENTER, sa=ET * 0.5)))
    e.append(Paragraph(nc.title(), _estilo("N", FN, TAM_C + 2, DARK, TA_CENTER, sa=4)))
    e.append(Paragraph(f"Cargo: {cl}", _estilo("D", FONTE, TAM_C - 2, GRAY, TA_CENTER, sa=EL)))
    for r in resultados:
        ic = "✅" if r["eh_ideal"] else "❌"
        co = "#4CAF50" if r["eh_ideal"] else "#e74c3c"
        e.append(Paragraph(f"{ic} {r['nome']} — Energia {r['energia']}", _estilo("B", FN, TAM_C - 1, DARK, TA_LEFT, sa=EL * 0.3)))
        if r["letras"]:
            ls = ", ".join(f'{l["letra"]}={l["valor"]}' for l in r["letras"])
            e.append(Paragraph(f"{ls} → {r['soma']} → {r['energia']}", _estilo("C", FONTE, TAM_C - 2, GRAY, TA_LEFT, sa=EL * 0.2)))
        e.append(Paragraph(r["explicacao"], _estilo("J", FONTE, TAM_C - 1, DARK, TA_JUSTIFY, sa=EL * 0.4)))
    if sugestoes:
        e.append(Paragraph("Sugestões:", _estilo("SU", FN, 18, GOLD, TA_LEFT, sb=EL, sa=ET)))
        for s in sugestoes[:3]:
            e.append(Paragraph(f'{s["nome"]} — Energia {s["energia"]}', _estilo("X", FONTE, TAM_C, DARK, TA_LEFT, sa=EL * 0.3)))
    e.append(Paragraph("© A1ELOS", _estilo("F", FONTE, 8, GRAY, TA_CENTER)))
    doc.build(e)
    return path

# ═══════════════════════════════════════════
# PDF ELEITORAL (100% preservado do original)
# ═══════════════════════════════════════════
def pdf_eleitoral(ss, cl, sugestoes, ne=None):
    path = f"/tmp/e_{uuid.uuid4().hex[:8]}.pdf"
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=50, rightMargin=50, topMargin=45, bottomMargin=45)
    e = []
    e.append(Spacer(1, 25))
    e.append(Paragraph("NÚMERO ELEITORAL — ANÁLISE COMPLETA", _estilo("T", FN, TAM_T, GOLD, TA_CENTER, sa=ET * 0.5)))
    e.append(Paragraph(f"Cargo: {cl} | Sigla: {ss}", _estilo("D", FONTE, TAM_C - 2, GRAY, TA_CENTER, sa=EL)))
    e.append(Paragraph("Como calculamos?", _estilo("SE", FN, 18, GOLD, TA_LEFT, sb=EL, sa=ET)))
    e.append(Paragraph("Na numerologia eleitoral, cada número possui uma vibração que influencia a campanha. O cálculo soma todos os dígitos e reduz a um dígito (exceto 11, 22).", _estilo("J", FONTE, TAM_C - 1, DARK, TA_JUSTIFY, sa=EL * 0.4)))
    e.append(Paragraph(f"Para {cl}, os 2 primeiros dígitos são fixos (sigla {ss}, soma {int(ss[0]) + int(ss[1])}). Os demais são escolhidos para energia 8.", _estilo("J", FONTE, TAM_C - 1, DARK, TA_JUSTIFY, sa=EL * 0.4)))
    e.append(Paragraph("Por que a energia 8?", _estilo("SE", FN, 18, GOLD, TA_LEFT, sb=EL, sa=ET)))
    e.append(Paragraph("O número 8 representa Poder, Prosperidade e Realização material. Para candidatos, atrai autoridade, sucesso nas urnas e capacidade de realizar obras.", _estilo("J", FONTE, TAM_C - 1, DARK, TA_JUSTIFY, sa=EL * 0.4)))
    e.append(Paragraph("Sugestões de Números", _estilo("SE", FN, 18, GOLD, TA_LEFT, sb=EL, sa=ET)))
    ideais = [s for s in sugestoes if s.get("ideal")]
    fallbacks = [s for s in sugestoes if not s.get("ideal")]
    if ideais:
        e.append(Paragraph("Energia 8 — IDEAL:", _estilo("B", FN, TAM_C - 1, DARK, TA_LEFT, sa=EL * 0.3)))
        for s in ideais:
            e.append(Paragraph(f"✅ {s['numero']} — Energia 8 — Poder e Prosperidade!", _estilo("X", FONTE, TAM_C, colors.HexColor("#4CAF50"), TA_LEFT, sa=EL * 0.2)))
            if "explicacao_calculo" in s:
                e.append(Paragraph(f"Cálculo: {s['explicacao_calculo']}", _estilo("C", FONTE, TAM_C - 2, GRAY, TA_LEFT, sa=EL * 0.2)))
    if fallbacks:
        e.append(Paragraph("Alternativas:", _estilo("B", FN, TAM_C - 1, DARK, TA_LEFT, sb=EL * 0.5, sa=EL * 0.3)))
        for s in fallbacks:
            e.append(Paragraph(f"{s['numero']} — Energia {s['energia']} — {s.get('nome_energia', '')}", _estilo("X", FONTE, TAM_C - 1, DARK, TA_LEFT, sa=EL * 0.2)))
    if ne:
        e.append(Paragraph("Número Existente Analisado:", _estilo("SE", FN, 18, GOLD, TA_LEFT, sb=EL, sa=ET)))
        e.append(Paragraph(f"{ne['numero']} — Energia {ne['energia']}", _estilo("X", FONTE, TAM_C, DARK, TA_LEFT, sa=EL * 0.3)))
        if ne["energia"] == 8:
            e.append(Paragraph("Este número já possui energia 8! Excelente.", _estilo("J", FONTE, TAM_C - 1, DARK, TA_JUSTIFY, sa=EL * 0.4)))
        else:
            e.append(Paragraph(f"Tem energia {ne['energia']}, diferente do ideal 8.", _estilo("J", FONTE, TAM_C - 1, DARK, TA_JUSTIFY, sa=EL * 0.4)))
    e.append(Paragraph("© A1ELOS — Numerologia aplicada ao sucesso eleitoral", _estilo("F", FONTE, 8, GRAY, TA_CENTER, sb=EL * 2)))
    doc.build(e)
    return path
