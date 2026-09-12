# -*- coding: utf-8 -*-
# gerar_apresentacao_texto.py
# Gera o PDF EDITORIAL (texto) A4 retrato, sem capa preta, dados empresariais.
# Salva em: static/apresentacao_empresarial_{lang}.pdf
# Retorna o caminho do arquivo gerado (é isso que faz a rota servir o PDF novo).
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable)
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
IDIOMAS = ["pt", "en", "es", "it", "fr", "de", "ja", "zh",
           "ru", "he", "ar", "id", "tr", "vi"]

# Fontes para idiomas especiais (CJK + cirílico + vietnamita/turco)
try:
    pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))  # zh
    pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))  # ja
    pdfmetrics.registerFont(TTFont('DejaVu', 'fonts/DejaVuSans.ttf'))  # ru/tr/vi
except Exception:
    pass

FONTE_POR_IDIOMA = {'ja': 'HeiseiMin-W3', 'zh': 'STSong-Light',
                    'ru': 'DejaVu', 'tr': 'DejaVu', 'vi': 'DejaVu'}

COR_AZUL = colors.HexColor("#1a3a6b")
COR_DOURADO = colors.HexColor("#B8860B")
COR_PRETO = colors.HexColor("#1a1a1a")
COR_CINZA = colors.HexColor("#555555")
COR_CINZA_CLARO = colors.HexColor("#f0f0f0")
CONTATOS = "a1elos.consultoria@gmail.com · arvigne@a1elos.com.br · a1elos.com.br/contato"

def _fonte(lang, bold=False):
    base = FONTE_POR_IDIOMA.get(lang, "Helvetica")
    if base in ("Helvetica",):
        return "Helvetica-Bold" if bold else "Helvetica"
    return base

def _estilo(lang, tam, bold, cor, alinh=TA_LEFT, antes=0, depois=6):
    return ParagraphStyle("s", fontName=_fonte(lang, bold), fontSize=tam,
                          textColor=cor, alignment=alinh, leading=tam * 1.35,
                          spaceBefore=antes, spaceAfter=depois)

def _render_bloco_juridico(story, c, lang):
    """Bloco jurídico final (sem inventar conteúdo; usa o que existir no CONTEUDO)."""
    if "bloco_juridico" not in c:
        return
    story.append(HRFlowable(width="100%", thickness=1, color=COR_DOURADO,
                            spaceBefore=6, spaceAfter=6))
    for sec in c["bloco_juridico"]:
        if isinstance(sec, dict):
            titulo = sec.get("titulo", "")
            itens = sec.get("itens", [])
            if titulo:
                story.append(Paragraph(titulo, _estilo(lang, 11, True, COR_AZUL, antes=8)))
            for it in itens:
                story.append(Paragraph("•  " + it, _estilo(lang, 9, False, COR_CINZA, alinh=TA_JUSTIFY)))

def gerar_pdf_texto(lang="pt", caminho_saida=None):
    """Gera o PDF editorial A4 retrato. Retorna o caminho do arquivo."""
    try:
        from apresentacao_textos import CONTEUDO
    except Exception:
        CONTEUDO = {}
    if lang not in CONTEUDO:
        lang = "pt"
    c = CONTEUDO.get(lang, CONTEUDO.get("pt", {}))
    if not caminho_saida:
        os.makedirs(STATIC_DIR, exist_ok=True)
        caminho_saida = os.path.join(STATIC_DIR, f"apresentacao_empresarial_{lang}.pdf")

    doc = SimpleDocTemplate(caminho_saida, pagesize=A4,
                            leftMargin=45, rightMargin=45,
                            topMargin=55, bottomMargin=45,
                            title=f"A1ELOS {lang.upper()}",
                            author="A1ELOS Global Numerology")
    story = []

    # ---- CAPA SIMPLES (SEM PRETA) ----
    story.append(Spacer(1, 40))
    story.append(Paragraph(c.get("titulo", "A1ELOS Global Numerology"),
                           _estilo(lang, 24, True, COR_AZUL, TA_CENTER, 0, 4)))
    story.append(Paragraph(c.get("subtitulo", ""),
                           _estilo(lang, 13, False, COR_CINZA, TA_CENTER, 0, 10)))
    story.append(HRFlowable(width="60%", thickness=1.2, color=COR_DOURADO,
                            hAlign="CENTER", spaceBefore=6, spaceAfter=6))
    story.append(Paragraph(c.get("capa_nota", ""),
                           _estilo(lang, 10, False, COR_CINZA, TA_CENTER, 0, 2)))
    story.append(Paragraph(f"{c.get('confidencial','')} · DUNS 942242668 · {c.get('ano','2026')}",
                           _estilo(lang, 9, True, COR_DOURADO, TA_CENTER)))
    story.append(Spacer(1, 30))

    # ---- SUMÁRIO EXECUTIVO ----
    if c.get("sumario_intro"):
        story.append(Paragraph(c.get("sumario_titulo", "Sumário Executivo"),
                               _estilo(lang, 16, True, COR_AZUL, antes=10)))
        story.append(Paragraph(c["sumario_intro"], _estilo(lang, 10, False, COR_CINZA, alinh=TA_JUSTIFY)))
    if c.get("sumario_cards"):
        for card in c["sumario_cards"]:
            txt = f"<b>{card.get('numero','')} — {card.get('titulo','')}</b><br/>{card.get('subtitulo','')}"
            story.append(Paragraph(txt, _estilo(lang, 9.5, False, COR_PRETO, depois=4)))

    # ---- SOBRE ----
    if c.get("sobre_texto"):
        story.append(Paragraph(c.get("sobre_titulo", "Sobre a A1ELOS"),
                               _estilo(lang, 16, True, COR_AZUL, antes=12)))
        story.append(Paragraph(c["sobre_texto"], _estilo(lang, 10, False, COR_CINZA, alinh=TA_JUSTIFY)))
    if c.get("sobre_kpis"):
        kpis = [[k.get("valor", ""), k.get("rotulo", "")] for k in c["sobre_kpis"]]
        if kpis:
            t = Table(kpis, colWidths=[90, 130])
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), COR_CINZA_CLARO),
                ("GRID", (0, 0), (-1, -1), 0.4, COR_DOURADO),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("TEXTCOLOR", (0, 0), (-1, -1), COR_PRETO),
            ]))
            story.append(t)

    # ---- MERCADO ----
    if c.get("mercado_texto"):
        story.append(Paragraph(c.get("mercado_titulo", "Oportunidade de Mercado"),
                               _estilo(lang, 16, True, COR_AZUL, antes=12)))
        story.append(Paragraph(c["mercado_texto"], _estilo(lang, 10, False, COR_CINZA, alinh=TA_JUSTIFY)))
    if c.get("mercado_cards"):
        for card in c["mercado_cards"]:
            story.append(Paragraph(f"<b>{card.get('titulo','')}</b> — {card.get('valor','')}",
                                   _estilo(lang, 9.5, False, COR_PRETO, depois=3)))

    # ---- PORTFÓLIO (tabela) ----
    if c.get("portfolio_tabela"):
        story.append(Paragraph(c.get("portfolio_titulo", "Portfólio"),
                               _estilo(lang, 16, True, COR_AZUL, antes=12)))
        linhas = [list(r) for r in c["portfolio_tabela"]]
        t = Table(linhas, colWidths=[60, 120, 80, 80])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), COR_AZUL),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
            ("FONTSIZE", (0, 0), (-1, -1), 8.5),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, COR_CINZA_CLARO]),
        ]))
        story.append(t)

    # ---- PROJEÇÕES (tabela) ----
    if c.get("projecoes_tabela"):
        story.append(Paragraph(c.get("projecoes_titulo", "Projeções Financeiras"),
                               _estilo(lang, 16, True, COR_AZUL, antes=12)))
        linhas = [list(r) for r in c["projecoes_tabela"]]
        t = Table(linhas, colWidths=[90, 110, 110])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), COR_AZUL),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
            ("FONTSIZE", (0, 0), (-1, -1), 8.5),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, COR_CINZA_CLARO]),
        ]))
        story.append(t)

    # ---- INVESTIMENTO & CONTATO ----
    if c.get("invest_dados"):
        story.append(Paragraph(c.get("invest_titulo", "Investimento & Contato"),
                               _estilo(lang, 16, True, COR_AZUL, antes=12)))
        for d in c["invest_dados"]:
            story.append(Paragraph(f"<b>{d.get('rotulo','')}:</b> {d.get('valor','')}",
                                   _estilo(lang, 10, False, COR_PRETO, depois=3)))
        if c.get("invest_alocacao"):
            story.append(Paragraph(c["invest_alocacao"],
                                   _estilo(lang, 9.5, True, COR_DOURADO, antes=6)))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1, color=COR_DOURADO))
    story.append(Paragraph(CONTATOS, _estilo(lang, 8, False, COR_CINZA, TA_CENTER, 4, 0)))

    # ---- BLOCO JURÍDICO ----
    _render_bloco_juridico(story, c, lang)

    # ---- CABEÇALHO E RODAPÉ (todas as páginas) ----
    def on_page(canvas, doc_):
        w, h = A4
        # Cabeçalho
        canvas.setFillColor(COR_AZUL)
        canvas.rect(0, h - 18 * mm, w, 18 * mm, stroke=0, fill=1)
        canvas.setFillColor(colors.white)
        canvas.setFont(_fonte(lang, True), 9)
        canvas.drawString(20 * mm, h - 11 * mm, c.get("titulo", "A1ELOS Global Numerology"))
        canvas.setFillColor(COR_DOURADO)
        canvas.setFont(_fonte(lang), 8)
        canvas.drawRightString(w - 20 * mm, h - 11 * mm, f"DUNS 942242668 · {c.get('confidencial','')}")
        # Rodapé
        canvas.setFillColor(COR_CINZA_CLARO)
        canvas.setFont(_fonte(lang), 7.5)
        canvas.drawCentredString(w / 2, 12 * mm, CONTATOS)
        canvas.setFillColor(COR_DOURADO)
        canvas.setFont(_fonte(lang, True), 8)
        canvas.drawRightString(w - 20 * mm, 12 * mm, str(doc_.page))
        canvas.setFillColor(COR_CINZA)
        canvas.setFont(_fonte(lang), 7)
        canvas.drawCentredString(w / 2, 6 * mm,
                                 f"{c.get('titulo','A1ELOS')} · DUNS 942242668 · {c.get('confidencial','')} {c.get('ano','2026')}")

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    return caminho_saida  # ← retorna o caminho (é isso que faz a rota servir o PDF novo)

if __name__ == "__main__":
    for lang in IDIOMAS:
        p = gerar_pdf_texto(lang)
        print(f"[{lang}] {p}")

  
