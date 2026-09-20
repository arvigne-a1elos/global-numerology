# -*- coding: utf-8 -*-
# ============================================================
# CABEÇALHO COM DUAS LOGOS (uma em cada lado) + RODAPÉ
# Usado nas DUAS versões: documento (texto) e slides
# ============================================================
import os, math, logging
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas as _canvas
from reportlab.pdfgen import canvas 
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import Table, TableStyle, Paragraph, SimpleDocTemplate, Spacer, HRFlowable, Image
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4, landscape

_CTX_TEXTO = {}
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
FONTES_RTL = {
    "ar": ("NotoNaskhArabic", "static/fonts/NotoNaskhArabic-Regular.ttf", "static/fonts/NotoNaskhArabic-Bold.ttf"),
    "he": ("NotoSansHebrew", "static/fonts/NotoSansHebrew-Regular.ttf", "static/fonts/NotoSansHebrew-Bold.ttf"),
}

COR_AZUL = colors.HexColor("#1a3a6b")
COR_DOURADO = colors.HexColor("#B8860B")
COR_PRETO = colors.HexColor("#1a1a1a")
COR_CINZA = colors.HexColor("#444444")
COR_CINZA_CLARO = colors.HexColor("#f0f0f0")
CONTATOS = "a1elos.consultoria@gmail.com · arvigne@a1elos.com.br · a1elos.com.br/contato"

TOTAL_PAGINAS = 21   # ajuste para o número real de slides

def _capa(canvas, doc_, c, lang):
    """Capa dos slides — sem capa preta, título central, com as 2 logos."""
    _cabecalho_duas_logos(canvas, doc_, c, lang, cor_fundo=COR_AZUL)

# Nomes das duas logos (coloque os arquivos em static/)
LOGO_ESQ = os.path.join(STATIC_DIR, "logo.png")        # logo à esquerda
LOGO_DIR = os.path.join(STATIC_DIR, "A1ELOS.png")      # logo à direita

def _fonte(lang, bold=False):
    if lang in FONTES_RTL:
        nome = FONTES_RTL[lang][0]
        if nome in pdfmetrics.getRegisteredFontNames():
            return nome
        return "DejaVu"
    base = FONTE_POR_IDIOMA.get(lang, "Helvetica")
    if base == "Helvetica":
        return "Helvetica-Bold" if bold else "Helvetica"
    return base

def _registrar_fontes_rtl():
    """Procura as fontes árabe/hebraico em qualquer pasta do projeto e registra."""
    raiz = os.path.dirname(os.path.abspath(__file__))
    for lang, (nome, reg, bold) in FONTES_RTL.items():
        arq_reg = os.path.basename(reg)
        arq_bold = os.path.basename(bold)
        achou_reg = None
        achou_bold = None
        for pasta_atual, subpastas, arquivos in os.walk(raiz):
            if arq_reg in arquivos:
                achou_reg = os.path.join(pasta_atual, arq_reg)
            if arq_bold in arquivos:
                achou_bold = os.path.join(pasta_atual, arq_bold)
        if achou_reg:
            try:
                pdfmetrics.registerFont(TTFont(nome, achou_reg))
            except Exception:
                pass
        if achou_bold:
            try:
                pdfmetrics.registerFont(TTFont(nome + "-Bold", achou_bold))
            except Exception:
                pass

def _estilo(lang, tam, bold, cor, alinh=TA_LEFT, antes=0, depois=6):
    return ParagraphStyle("s", fontName=_fonte(lang, bold), fontSize=tam,
                          textColor=cor, alignment=alinh, leading=tam * 1.4,
                          spaceBefore=antes, spaceAfter=depois)

def _campo(item, chave=None, idx=None, default=""):
    if isinstance(item, dict):
        return item.get(chave, default) if chave else default
    if isinstance(item, (tuple, list)):
        if idx is not None and len(item) > idx:
            return item[idx]
        return default
    return default

def _texto_item(item, sep=" — "):
    if isinstance(item, dict):
        return sep.join(str(v) for v in item.values() if v)
    if isinstance(item, (tuple, list)):
        return sep.join(str(v) for v in item if v)
    return str(item)

def _desenha_logo(canvas, caminho, x, y, larg, alt):
    """Desenha uma logo se o arquivo existir; ignora silenciosamente se não."""
    try:
        if caminho and os.path.exists(caminho):
            canvas.drawImage(caminho, x, y, width=larg, height=alt,
                             preserveAspectRatio=True, mask='auto')
    except Exception:
        pass

def _cabecalho_duas_logos(canvas, doc_, c, lang, altura_cab=18*mm, cor_fundo=None):
    """Cabeçalho com DUAS logos (esquerda e direita) + título central."""
    w, h = getattr(canvas, "_pagesize", A4)
    # Faixa do cabeçalho
    if cor_fundo:
        canvas.setFillColor(cor_fundo)
        canvas.rect(0, h - altura_cab, w, altura_cab, stroke=0, fill=1)
    # Logo esquerda
    _desenha_logo(canvas, LOGO_ESQ, 15*mm, h - 16*mm, 12*mm, 12*mm)
    # Logo direita
    _desenha_logo(canvas, LOGO_DIR, w - 15*mm - 12*mm, h - 16*mm, 12*mm, 12*mm)
    # Título central (entre as duas logos)
    canvas.setFillColor(colors.white if cor_fundo else COR_AZUL)
    canvas.setFont(_fonte(lang, True), 9)
    titulo = c.get("titulo", "A1ELOS Global Numerology")
    canvas.drawCentredString(w / 2, h - 7*mm, titulo)          # título (mais alto)
    canvas.setFillColor(COR_DOURADO)
    canvas.setFont(_fonte(lang), 7.5)
    canvas.drawCentredString(w / 2, h - 13*mm,                # DUNS + confidencial (mais abaixo)
                             f"DUNS 942242668 · {c.get('confidencial','')}")
    # Linha dourada abaixo do cabeçalho
    canvas.setStrokeColor(COR_DOURADO)
    canvas.setLineWidth(0.8)
    canvas.line(15*mm, h - altura_cab, w - 15*mm, h - altura_cab)

def _rodape(canvas, doc_, c, lang, num_pag=None, total_pag=None):
    """Rodapé com contatos + página numerada (X de Y)."""
    w, h = getattr(canvas, "_pagesize", A4)
    canvas.setStrokeColor(COR_DOURADO)
    canvas.setLineWidth(0.8)
    canvas.line(15*mm, 17*mm, w - 15*mm, 17*mm)
    # Linha de cima (y=12mm): título/DUNS/ano + página, TUDO CENTRALIZADO
    canvas.setFillColor(COR_CINZA)
    canvas.setFont(_fonte(lang), 7)
    pagina = num_pag if num_pag is not None else doc_.page
    if total_pag:
        rodape_txt = (f"{c.get('titulo','A1ELOS')} · DUNS 942242668 · "
                      f"{c.get('confidencial','')} {c.get('ano','2026')}   ·   {pagina} de {total_pag}")
    else:
        rodape_txt = (f"{c.get('titulo','A1ELOS')} · DUNS 942242668 · "
                      f"{c.get('confidencial','')} {c.get('ano','2026')}   ·   {pagina}")
    canvas.drawCentredString(w / 2, 12*mm, rodape_txt)
    # Linha de baixo (y=8mm): contatos centralizados, sozinhos
    canvas.setFillColor(COR_CINZA)
    canvas.setFont(_fonte(lang), 7.5)
    canvas.drawCentredString(w / 2, 8*mm, CONTATOS)

def gerar_pdf_texto(lang="pt", caminho_saida=None):
    """Gera o PDF documento A4 retrato — texto limpo. Retorna o caminho."""
    global APRESENTACAO_TEXTOS
    if lang not in APRESENTACAO_TEXTOS:
        lang = "pt"
    c = APRESENTACAO_TEXTOS.get(lang, APRESENTACAO_TEXTOS.get("pt", {}))

    if not caminho_saida:
        os.makedirs(STATIC_DIR, exist_ok=True)
        caminho_saida = os.path.join(STATIC_DIR, f"apresentacao_empresarial_{lang}.pdf")

    doc = SimpleDocTemplate(caminho_saida, pagesize=A4,
                            leftMargin=50, rightMargin=50,
                            topMargin=70, bottomMargin=55,
                            title=f"A1ELOS {lang.upper()}",
                            author="A1ELOS Global Numerology",)
                            
    story = []           
           
# ===== CAPA SIMPLES (SEM PRETA) =====
    story.append(Spacer(1, 50))
    story.append(Paragraph(c.get("titulo", "A1ELOS Global Numerology"),
                           _estilo(lang, 24, True, COR_AZUL, TA_CENTER, 0, 4)))
    story.append(Paragraph(c.get("subtitulo", ""),
                           _estilo(lang, 13, False, COR_CINZA, TA_CENTER, 0, 10)))
    story.append(HRFlowable(width="55%", thickness=1.2, color=COR_DOURADO,
                            hAlign="CENTER", spaceBefore=4, spaceAfter=8))
    story.append(Paragraph(c.get("capa_nota", ""),
                           _estilo(lang, 10, False, COR_CINZA, TA_CENTER, 0, 2)))
    story.append(Paragraph(f"{c.get('confidencial','')} · DUNS 942242668 · {c.get('ano','2026')}",
                           _estilo(lang, 9, True, COR_DOURADO, TA_CENTER)))
    story.append(Spacer(1, 30))

    # ===== 1. SUMÁRIO EXECUTIVO =====
    story.append(Paragraph(c.get("sumario_titulo", "Sumário Executivo"),
                           _estilo(lang, 16, True, COR_AZUL, antes=14)))
    if c.get("sumario_intro"):
        story.append(Paragraph(c["sumario_intro"],
                               _estilo(lang, 10.5, False, COR_PRETO, alinh=TA_JUSTIFY)))
    for card in c.get("sumario_cards", []):
        story.append(Paragraph(_texto_item(card, " — "),
                               _estilo(lang, 10, False, COR_PRETO, depois=3)))

    # ===== 2. SOBRE A A1ELOS =====
    story.append(Paragraph(c.get("sobre_titulo", "Sobre a A1ELOS"),
                           _estilo(lang, 16, True, COR_AZUL, antes=14)))
    if c.get("sobre_texto"):
        story.append(Paragraph(c["sobre_texto"],
                               _estilo(lang, 10.5, False, COR_PRETO, alinh=TA_JUSTIFY)))
    for k in c.get("sobre_kpis", []):
        story.append(Paragraph(_texto_item(k, " — "),
                               _estilo(lang, 10, False, COR_PRETO, depois=3)))
    if c.get("sobre_duns"):
        story.append(Paragraph(c["sobre_duns"],
                               _estilo(lang, 10, False, COR_CINZA, alinh=TA_JUSTIFY, antes=4)))

    # ===== 3. CREDIBILIDADE INTERNACIONAL (DUNS) =====
    story.append(Paragraph(c.get("duns_titulo", "Credibilidade Internacional"),
                           _estilo(lang, 16, True, COR_AZUL, antes=14)))
    if c.get("duns_texto"):
        story.append(Paragraph(c["duns_texto"],
                               _estilo(lang, 10.5, False, COR_PRETO, alinh=TA_JUSTIFY)))
    if c.get("duns_emitido"):
        story.append(Paragraph(c["duns_emitido"],
                               _estilo(lang, 10, False, COR_CINZA, alinh=TA_JUSTIFY, antes=4)))
    if c.get("duns_paises"):
        story.append(Paragraph(c["duns_paises"],
                               _estilo(lang, 10, True, COR_DOURADO, antes=4)))
    for b in c.get("duns_beneficios", []):
        story.append(Paragraph(_texto_item(b, " — "),
                               _estilo(lang, 10, False, COR_PRETO, depois=3)))

    # ===== 4. OPORTUNIDADE DE MERCADO =====
    story.append(Paragraph(c.get("mercado_titulo", "Oportunidade de Mercado"),
                           _estilo(lang, 16, True, COR_AZUL, antes=14)))
    if c.get("mercado_texto"):
        story.append(Paragraph(c["mercado_texto"],
                               _estilo(lang, 10.5, False, COR_PRETO, alinh=TA_JUSTIFY)))
    for card in c.get("mercado_cards", []):
        story.append(Paragraph(_texto_item(card, " — "),
                               _estilo(lang, 10, False, COR_PRETO, depois=3)))

    # ===== 5. O PROBLEMA QUE RESOLVEMOS =====
    story.append(Paragraph(c.get("problema_titulo", "O Problema que Resolvemos"),
                           _estilo(lang, 16, True, COR_AZUL, antes=14)))
    if c.get("problema_col_esq_titulo"):
        story.append(Paragraph(c["problema_col_esq_titulo"],
                               _estilo(lang, 11, True, COR_PRETO, antes=6)))
    for p in c.get("problema_col_esq", []):
        story.append(Paragraph(_texto_item(p, " — "),
                               _estilo(lang, 10, False, COR_PRETO, depois=3)))
    if c.get("problema_col_dir_titulo"):
        story.append(Paragraph(c["problema_col_dir_titulo"],
                               _estilo(lang, 11, True, COR_PRETO, antes=6)))
    if c.get("problema_col_dir"):
        story.append(Paragraph(c["problema_col_dir"],
                               _estilo(lang, 10, False, COR_PRETO, alinh=TA_JUSTIFY)))
    if c.get("problema_destaque"):
        story.append(Paragraph(c["problema_destaque"],
                               _estilo(lang, 10, True, COR_AZUL, alinh=TA_JUSTIFY, antes=4)))

    # ===== 6. NOSSA SOLUÇÃO =====
    story.append(Paragraph(c.get("solucao_titulo", "Nossa Solução"),
                           _estilo(lang, 16, True, COR_AZUL, antes=14)))
    if c.get("solucao_texto"):
        story.append(Paragraph(c["solucao_texto"],
                               _estilo(lang, 10.5, False, COR_PRETO, alinh=TA_JUSTIFY)))
    for col in c.get("solucao_colunas", []):
        story.append(Paragraph(_texto_item(col, " — "),
                               _estilo(lang, 10, False, COR_PRETO, depois=3)))

    # ===== 7. ALCANCE GLOBAL =====
    story.append(Paragraph(c.get("alcance_titulo", "Alcance Global"),
                           _estilo(lang, 16, True, COR_AZUL, antes=14)))
    if c.get("alcance_texto"):
        story.append(Paragraph(c["alcance_texto"],
                               _estilo(lang, 10.5, False, COR_PRETO, alinh=TA_JUSTIFY)))
    for linha in c.get("portfolio_tabela", []):
        linha = [_com_moeda(lang, cel) if i == 2 else cel for i, cel in enumerate(linha)]
        story.append(Paragraph(_texto_item(linha, " — "),
                               _estilo(lang, 10, False, COR_PRETO, depois=2)))
    if c.get("total_linha"):
        story.append(Paragraph(f"{c['total_linha']} — ~5.320",
                               _estilo(lang, 10, True, COR_AZUL, antes=4)))

    # ===== 8. TRÊS NOVOS MERCADOS =====
    story.append(Paragraph(c.get("mercados_titulo", "3 Novos Mercados"),
                           _estilo(lang, 16, True, COR_AZUL, antes=14)))
    if c.get("mercados_texto"):
        story.append(Paragraph(c["mercados_texto"],
                               _estilo(lang, 10.5, False, COR_PRETO, alinh=TA_JUSTIFY)))
    for m in c.get("mercados_cards", []):
        nome = _campo(m, "titulo", 0)
        dados = _campo(m, "subtitulo", 1)
        if isinstance(dados, (list, tuple)):
            dados = "; ".join(str(d) for d in dados)
        story.append(Paragraph(f"<b>{nome}</b> — {dados}",
                               _estilo(lang, 10, False, COR_PRETO, depois=3)))
    if c.get("mercados_rodape"):
        story.append(Paragraph(c["mercados_rodape"],
                               _estilo(lang, 10, True, COR_AZUL, alinh=TA_JUSTIFY, antes=4)))

    # ===== 9. FILOSOFIA DE PREÇO =====
    story.append(Paragraph(c.get("preco_titulo", "Filosofia de Preço Consciente"),
                           _estilo(lang, 16, True, COR_AZUL, antes=14)))
    if c.get("preco_esq"):
        story.append(Paragraph(c["preco_esq"],
                               _estilo(lang, 10.5, False, COR_PRETO, alinh=TA_JUSTIFY)))
    if c.get("preco_dir_titulo"):
        story.append(Paragraph(c["preco_dir_titulo"],
                               _estilo(lang, 11, True, COR_PRETO, antes=6)))
    if c.get("preco_dir"):
        story.append(Paragraph(c["preco_dir"],
                               _estilo(lang, 10, False, COR_PRETO, alinh=TA_JUSTIFY)))
    for p in c.get("preco_pilares", []):
        story.append(Paragraph(_texto_item(p, " — "),
                               _estilo(lang, 10, False, COR_PRETO, depois=3)))

    # ===== 10. PORTFÓLIO =====
    story.append(Paragraph(c.get("portfolio_titulo", "Portfólio"),
                           _estilo(lang, 16, True, COR_AZUL, antes=14)))
    if c.get("portfolio_texto"):
        story.append(Paragraph(c["portfolio_texto"],
                               _estilo(lang, 10.5, False, COR_PRETO, alinh=TA_JUSTIFY)))
    for linha in c.get("portfolio_tabela", []):
        linha = [_com_moeda(lang, cel) if i == 2 else cel for i, cel in enumerate(linha)]
        story.append(Paragraph(_texto_item(linha, " — "),
                               _estilo(lang, 10, False, COR_PRETO, depois=2)))
    if c.get("portfolio_rodape"):
        story.append(Paragraph(c["portfolio_rodape"],
                               _estilo(lang, 10, True, COR_CINZA, alinh=TA_JUSTIFY, antes=4)))

    # ===== 11. MODELO DE NEGÓCIO =====
    story.append(Paragraph(c.get("negocio_titulo", "Modelo de Negócio"),
                           _estilo(lang, 16, True, COR_AZUL, antes=14)))
    if c.get("negocio_texto"):
        story.append(Paragraph(c["negocio_texto"],
                               _estilo(lang, 10.5, False, COR_PRETO, alinh=TA_JUSTIFY)))
    for col in c.get("negocio_colunas", []):
        story.append(Paragraph(_texto_item(col, " — "),
                               _estilo(lang, 10, False, COR_PRETO, depois=3)))
    if c.get("b2c_linha") and c.get("fonte_receita"):
        story.append(Paragraph(f"{c['fonte_receita']}: {c['b2c_linha']} — 60% · {c['b2b_linha']} — 25% · {c['pub_linha']} — 15%",
                               _estilo(lang, 10, False, COR_PRETO, antes=4)))

    # ===== 12. BANNERS PUBLICITÁRIOS =====
    story.append(Paragraph(c.get("banners_titulo", "Banners Publicitários"),
                           _estilo(lang, 16, True, COR_AZUL, antes=14)))
    if c.get("banners_texto"):
        story.append(Paragraph(c["banners_texto"],
                               _estilo(lang, 10.5, False, COR_PRETO, alinh=TA_JUSTIFY)))
    for linha in c.get("banners_tabela", []):
        linha = [_com_moeda(lang, cel) if i in (1, 2) else cel for i, cel in enumerate(linha)]
        story.append(Paragraph(_texto_item(linha, " — "),
                               _estilo(lang, 10, False, COR_PRETO, depois=2)))
    if c.get("banners_formatos"):
        story.append(Paragraph(c["banners_formatos"],
                               _estilo(lang, 9.5, False, COR_CINZA, alinh=TA_JUSTIFY, antes=4)))

    # ===== 13. PACOTES B2B =====
    story.append(Paragraph(c.get("b2b_titulo", "Pacotes Empresariais B2B"),
                           _estilo(lang, 16, True, COR_AZUL, antes=14)))
    if c.get("b2b_texto"):
        story.append(Paragraph(c["b2b_texto"],
                               _estilo(lang, 10.5, False, COR_PRETO, alinh=TA_JUSTIFY)))
    for plano in c.get("b2b_planos", []):
        story.append(Paragraph(_texto_item(plano, " — "),
                               _estilo(lang, 10, False, COR_PRETO, depois=3)))
    if c.get("tabela_descontos"):
        story.append(Paragraph(c["tabela_descontos"],
                               _estilo(lang, 11, True, COR_PRETO, antes=6)))
    for linha in c.get("b2b_tabela", []):
        story.append(Paragraph(_texto_item(linha, " — "),
                               _estilo(lang, 10, False, COR_PRETO, depois=2)))

    # ===== 14. PROJEÇÕES FINANCEIRAS =====
    story.append(Paragraph(c.get("projecoes_titulo", "Projeções Financeiras"),
                           _estilo(lang, 16, True, COR_AZUL, antes=14)))
    if c.get("projecoes_texto"):
        story.append(Paragraph(c["projecoes_texto"],
                               _estilo(lang, 10.5, False, COR_PRETO, alinh=TA_JUSTIFY)))
    for linha in c.get("projecoes_tabela", []):
        linha = [_com_moeda(lang, cel) if i in (1, 2) else cel for i, cel in enumerate(linha)]
        story.append(Paragraph(_texto_item(linha, " — "),
                               _estilo(lang, 10, False, COR_PRETO, depois=2)))

    # ===== 15. TRAÇÃO =====
    story.append(Paragraph(c.get("tracao_titulo", "Tração e Resultados"),
                           _estilo(lang, 16, True, COR_AZUL, antes=14)))
    if c.get("tracao_texto"):
        story.append(Paragraph(c["tracao_texto"],
                               _estilo(lang, 10.5, False, COR_PRETO, alinh=TA_JUSTIFY)))
    for k in c.get("tracao_kpis", []):
        story.append(Paragraph(_texto_item(k, " — "),
                               _estilo(lang, 10, False, COR_PRETO, depois=3)))

    # ===== 16. ROTEIRO ESTRATÉGICO =====
    story.append(Paragraph(c.get("roteiro_titulo", "Roteiro Estratégico"),
                           _estilo(lang, 16, True, COR_AZUL, antes=14)))
    if c.get("roteiro_texto"):
        story.append(Paragraph(c["roteiro_texto"],
                               _estilo(lang, 10.5, False, COR_PRETO, alinh=TA_JUSTIFY)))
    for f in c.get("roteiro_fases", []):
        story.append(Paragraph(_texto_item(f, " — "),
                               _estilo(lang, 10, False, COR_PRETO, depois=3)))

    # ===== 17. INVESTIMENTO & CONTATO =====
    story.append(Paragraph(c.get("invest_titulo", "Investimento & Contato"),
                           _estilo(lang, 16, True, COR_AZUL, antes=14)))
    if c.get("invest_texto"):
        story.append(Paragraph(c["invest_texto"],
                               _estilo(lang, 10.5, False, COR_PRETO, alinh=TA_JUSTIFY)))
    for d in c.get("invest_dados", []):
        story.append(Paragraph(_texto_item(d, ": "),
                               _estilo(lang, 10, False, COR_PRETO, depois=3)))
    for ct in c.get("invest_contato", []):
        story.append(Paragraph(_texto_item(ct, ": "),
                               _estilo(lang, 10, False, COR_PRETO, depois=3)))
    if c.get("invest_alocacao"):
        story.append(Paragraph(c["invest_alocacao"],
                               _estilo(lang, 10, True, COR_AZUL, antes=4)))

    # ===== 18. BRASIL: PIX =====
    story.append(Paragraph(c.get("pix_titulo", "Brasil: A Infraestrutura Pix"),
                           _estilo(lang, 16, True, COR_AZUL, antes=14)))
    if c.get("pix_texto"):
        story.append(Paragraph(c["pix_texto"],
                               _estilo(lang, 10.5, False, COR_PRETO, alinh=TA_JUSTIFY)))
    for k in c.get("pix_kpis", []):
        story.append(Paragraph(_texto_item(k, " — "),
                               _estilo(lang, 10, False, COR_PRETO, depois=3)))
    if c.get("pix_fonte"):
        story.append(Paragraph(c["pix_fonte"],
                               _estilo(lang, 9, False, COR_CINZA, alinh=TA_JUSTIFY, antes=4)))

    # ===== 19. REFERÊNCIAS =====
    story.append(Paragraph(c.get("ref_titulo", "Referências Bibliográficas"),
                           _estilo(lang, 16, True, COR_AZUL, antes=14)))
    if c.get("ref_intro"):
        story.append(Paragraph(c["ref_intro"],
                               _estilo(lang, 10, False, COR_CINZA, alinh=TA_JUSTIFY)))
    for r in c.get("ref_lista", []):
        story.append(Paragraph(_texto_item(r, " — "),
                               _estilo(lang, 10, False, COR_PRETO, depois=3)))

    # ===== 20. BLOCO JURÍDICO (SE EXISTIR) =====
    if c.get("bloco_juridico"):
        story.append(HRFlowable(width="100%", thickness=1, color=COR_DOURADO,
                                spaceBefore=10, spaceAfter=6))
        for sec in c["bloco_juridico"]:
            if isinstance(sec, dict):
                if sec.get("titulo"):
                    story.append(Paragraph(sec["titulo"],
                                           _estilo(lang, 12, True, COR_AZUL, antes=8)))
                for it in sec.get("itens", []):
                    story.append(Paragraph(it,
                                           _estilo(lang, 9.5, False, COR_CINZA, alinh=TA_JUSTIFY)))

    # ===== 21. PÁGINA FINAL =====
    story.append(Spacer(1, 16))
    story.append(HRFlowable(width="55%", thickness=1.2, color=COR_DOURADO,
                            hAlign="CENTER", spaceBefore=4, spaceAfter=6))
    story.append(Paragraph(c.get("frase_final", "Os números nunca mentem."),
                           _estilo(lang, 15, True, COR_AZUL, TA_CENTER)))
    # Selos em UMA linha horizontal (economiza espaço, evita página isolada)
    selos = c.get("selo_final", [])
    if selos:
        linha_selos = "   ·   ".join(str(s) for s in selos)
        story.append(Paragraph(linha_selos,
                               _estilo(lang, 9, True, COR_DOURADO, TA_CENTER, depois=2)))

    global _RODAPE_FN
    _CTX_TEXTO["c"] = c
    _CTX_TEXTO["lang"] = lang
    _RODAPE_FN = _rodape_texto      

    doc.build(story, canvasmaker=CanvasComTotal)
    return caminho_saida 
           
# ============================================================
# BLOCO JURÍDICO / GOVERNANÇA E COMPLIANCE (SEÇÕES 19-29)
# Conteúdo em PT com fallback para todos os idiomas.
# ============================================================
BLOCO_JURIDICO_PT = [
    ("19. Governança Corporativa, Conformidade e Estrutura Jurídica", [
        "A governança corporativa da A1ELOS Global Numerology é estruturada sobre as melhores práticas do direito societário nacional e internacional, assegurando total transparência decisória e mitigação de riscos operacionais. As operações societárias regem-se subsidiariamente pela Lei nº 6.404/1976 (Lei das Sociedades por Ações), aplicando-se os estritos deveres fiduciários de diligência (art. 153) e de lealdade (art. 155) à totalidade de seus diretores executivos e conselheiros estratégicos.",
        "No âmbito do direito material civil, a atuação da holding vincula-se ao princípio da boa-fé objetiva insculpido no art. 422 da Lei nº 10.406/2002 (Código Civil Brasileiro), bem como ao postulado da autonomia patrimonial da pessoa jurídica delineado no art. 49-A do mesmo diploma legal, garantindo a perfeita segregação entre os ativos da entidade societária e o patrimônio pessoal de seus sócios e investidores.",
        "A companhia adota comitês permanentes de conformidade fiscal e auditoria contábil interna periódica. O descumprimento de quaisquer diretrizes de governança ou o cometimento de atos que atentem contra o patrimônio da sociedade sujeitam os infratores a sanções disciplinares, destituição imediata de cargos executivos e responsabilização civil e penal integral pelos prejuízos causados.",
    ]),
    ("20. Arquitetura Tecnológica e Motores de Inteligência Artificial", [
        "A infraestrutura de suporte computacional da A1ELOS fundamenta-se em clusters de microsserviços distribuídos em provedores de nuvem de primeira linha com alta redundância geográfica e latência ultrabaixa. O pipeline técnico realiza de forma contínua a ingestão de requisições, o processamento de equações de numerologia pitagórica e hermenêutica, a sintetização contextualizada por inteligência artificial e a compilação instantânea dos relatórios editoriais.",
        "O desenvolvimento do ecossistema atende integralmente aos parâmetros de segurança da informação e governo digital estipulados pela Lei nº 14.129/2021 e às diretrizes internacionais das normas técnicas ISO/IEC 27001 e ISO/IEC 27701. A infraestrutura possui elasticidade horizontal automatizada, dimensionando capacidade computacional sem dependência de intervenção humana manual.",
        "No que tange à disponibilização de aplicações na internet e responsabilidade dos provedores, a plataforma opera sob estrita consonância com o Marco Civil da Internet (Lei nº 12.965/2014), assegurando a observância dos direitos dos usuários (art. 7º) e a guarda segura de registros de acesso nos prazos legalmente mandatados.",
    ]),
    ("21. Proteção de Dados, Privacidade e Soberania Digital (LGPD e GDPR)", [
        "A tutela da privacidade e dos dados pessoais constitui compromisso inegociável da A1ELOS. A coleta de dados sensíveis e biográficos (como nome completo, data de nascimento e endereço de correio eletrônico) restringe-se estritamente ao necessário para o processamento dos cálculos numerológicos contratados, operando sob as bases legais de execução de contrato e legítimo interesse (art. 7º, incisos V e IX, da Lei nº 13.709/2018 - LGPD).",
        "Em âmbito internacional, a operação cumpre com rigor os ditames do Regulamento Geral sobre a Proteção de Dados da União Europeia (GDPR - Regulamento UE 2016/679), do California Consumer Privacy Act (CCPA) e das legislações asiáticas de proteção de dados. Os dados em repouso são protegidos por criptografia de padrão militar AES-256, enquanto o tráfego de rede utiliza exclusivamente protocolos seguros TLS 1.3 com perfeita confidencialidade direta.",
        "Qualquer eventual desvio ou violação de segurança será tratado sob os procedimentos mandatórios de notificação tempestiva à Autoridade Nacional de Proteção de Dados (ANPD), aplicando-se aos agentes violadores as severas penalidades administrativas previstas no art. 52 da LGPD (com multas de até 2% do faturamento, limitadas a R$ 50.000.000,00 por infração), cumuladas com a reparação integral dos danos morais e materiais com base no art. 927 do Código Civil.",
    ]),
    ("22. Propriedade Intelectual, Marcas e Segredos de Negócio", [
        "A totalidade dos ativos intangíveis da A1ELOS — incluindo algoritmos de cálculo, arquitetura de software, bases de dados semânticas em 14 idiomas, métodos de parametrização de PPP, logotipos, identidades visuais e marcas nominativas — encontra-se formalmente protegida sob as normas da Lei de Propriedade Industrial (Lei nº 9.279/1996), da Lei de Software (Lei nº 9.609/1998) e da Lei de Direitos Autorais (Lei nº 9.610/1998).",
        "A holding conta com depósitos e registros resguardados internacionalmente pelos tratados da Convenção da União de Paris (CUP) e pelo Tratado de Cooperação em Matéria de Patentes (PCT). A tecnologia proprietária e as tabelas de conversão fonético-numérica são classificadas expressamente como segredos comerciais de alta confidencialidade (trade secrets).",
        "A violação de quaisquer direitos autorais ou a apropriação indevida de código-fonte e metodologias sujeitará o infrator às ações cíveis indenizatórias por perdas, danos emergentes e lucros cessantes, sem prejuízo da deflagração das medidas penais cabíveis por concorrência desleal e contrafação previstas nos arts. 184 e 195 da Lei nº 9.279/1996.",
    ]),
    ("23. Política de Paridade de Poder de Compra (PPP) e Conformidade Financeira", [
        "A política de precificação fundamentada em Paridade de Poder de Compra (PPP) constitui método estruturado de equilíbrio macroeconômico, sendo constantemente monitorada através de indexadores internacionais oficiais. A conversão das tarifas respeita a regulamentação do Novo Marco Cambial brasileiro (Lei nº 14.286/2021) e as normativas do Banco Central do Brasil (BACEN) e do Conselho Monetário Nacional (CMN).",
        "A diferenciação de valores nominais entre diferentes jurisdições apoia-se em justificativa econômica objetiva, não configurando prática discriminatória ou infração à ordem econômica, atendendo plenamente aos arts. 39 e 51 da Lei nº 8.078/1990 (Código de Defesa do Consumidor). A plataforma proíbe expressamente a manipulação arbitrária de margens comerciais por parceiros ou distribuidores regionais.",
        "A tentativa de arbitragem predatória de preços através de burla geográfica ou o uso não autorizado de VPNs para aquisições transfronteiriças indevidas ensejará o cancelamento unilateral imediato da licença de uso do produto digital adquirido, com retenção do valor pago a título de cláusula penal indenizatória.",
    ]),
    ("24. Prevenção à Lavagem de Dinheiro e Financiamento do Terrorismo (PLD/FT)", [
        "A A1ELOS adota uma postura de tolerância zero em relação a atividades ilícitas, instituindo um programa robusto de Prevenção à Lavagem de Dinheiro e Combate ao Financiamento do Terrorismo (PLD/FT), estruturado nos moldes da Lei nº 9.613/1998 (com as alterações introduzidas pela Lei nº 12.683/2012), nas instruções da Unidade de Inteligência Financeira (UIF/COAF) e nas diretrizes internacionais do Grupo de Ação Financeira Internacional (GAFI/FATF).",
        "Todos os parceiros institucionais B2B, anunciantes corporativos e adquirentes de grandes lotes de licenças passam por procedimentos estritos de verificação cadastral (Know Your Customer - KYC e Know Your Business - KYB), com cruzamento automatizado em listas restritivas globais (OFAC, Interpol, Conselho de Segurança da ONU e cadastro de Pessoas Politicamente Expostas - PEPs).",
        "Identificada qualquer inconsistência cadastral ou transação suspeita, a companhia reserva-se o direito de rescindir liminarmente o contrato, congelar o fornecimento das licenças e proceder à comunicação mandatória aos órgãos de fiscalização financeira competentes, em estrito cumprimento ao art. 11 da Lei nº 9.613/1998.",
    ]),
    ("25. Gestão de Riscos, Continuidade de Negócios e Acordo de Nível de Serviço (SLA)", [
        "A continuidade operacional da A1ELOS é assegurada por um Plano de Continuidade de Negócios (PCN) e um Plano de Recuperação de Desastres (Disaster Recovery) estruturados sob a norma ISO 22301 e as diretrizes do framework global COSO-ERM. A arquitetura em nuvem utiliza zonas de disponibilidade múltipla (Multi-AZ), backups criptografados em tempo real e balanceamento automático de carga.",
        "Para clientes corporativos e contratos B2B, a companhia estabelece contratualmente um Acordo de Nível de Serviço (Service Level Agreement - SLA) garantindo disponibilidade mínima de 99,9% para a API de cálculo e geração de relatórios, calculada em bases mensais contínuas.",
        "Em caso de descumprimento injustificado do SLA contratado por falha exclusiva da infraestrutura da holding, serão concedidos créditos de serviço proporcionais ao período de indisponibilidade, nos termos do art. 389 do Código Civil, limitando-se a responsabilidade financeira total da companhia a 30% da mensalidade ou do volume contratado no mês do evento.",
    ]),
    ("26. Relações de Trabalho, RH e Gestão de Talentos", [
        "A gestão de talentos humanos da A1ELOS apoia-se nos princípios da meritocracia, inovação constante, valorização da diversidade cultural e estrita legalidade trabalhista. Todas as contratações e parcerias em território nacional subordinam-se à Consolidação das Leis do Trabalho (Decreto-Lei nº 5.452/1943) e às inovações regulatórias da Lei nº 13.467/2017, em especial o regime de teletrabalho previsto nos arts. 75-A e seguintes.",
        "A holding mantém políticas severas de integridade corporativa, combatendo qualquer modalidade de discriminação, assédio moral ou sexual no ambiente físico e virtual de trabalho, disponibilizando canal de ouvidoria independente e anônimo.",
        "A violação de deveres de confidencialidade, a prática de condutas desonestas ou o vazamento não autorizado de dados estratégicos por colaboradores acarretará demissão imediata por justa causa com base no art. 482 da CLT, cumulada com o ajuizamento de competente ação regressiva de perdas e danos.",
    ]),
    ("27. Sustentabilidade, Governança e Responsabilidade Social (ESG)", [
        "A estratégia corporativa da A1ELOS incorpora nativamente os critérios Ambientais, Sociais e de Governança (ESG). Por operar sob modelo 100% digital em nuvem, a companhia mantém uma pegada de carbono operacional substancialmente reduzida, priorizando servidores hospedados em datacenters abastecidos por fontes de energia 100% renovável.",
        "No pilar social, o compromisso concretiza-se na política de inclusão digital e paridade de poder de compra (PPP), viabilizando o acesso de populações vulneráveis e de países emergentes a ferramentas de autoconhecimento analítico a custos proporcionais à sua realidade econômica, alinhando-se aos Objetivos de Desenvolvimento Sustentável da ONU (notadamente ODS 8 — Trabalho Decente e Crescimento Econômico e ODS 10 — Redução das Desigualdades).",
        "No âmbito da governança, a organização segue as recomendações do Instituto Brasileiro de Governança Corporativa (IBGC), com prestação periódica de contas, auditorias independentes e vedação a quaisquer práticas lesivas ao meio ambiente ou à ordem social.",
    ]),
    ("28. Estrutura da Rodada de Investimento e Direitos dos Minoritários", [
        "A abertura da Rodada Seed da A1ELOS rege-se pelos parâmetros normativos do Marco Legal das Startups (Lei Complementar nº 182/2021) e pelas regras gerais de títulos societários conversíveis da Lei nº 6.404/1976. A captação é instrumentalizada mediante contratos de Mútuo Conversível em Participação Societária ou acordos SAFE internacionais.",
        "Aos investidores participantes são assegurados direitos de proteção societária condizentes com o mercado institucional global de Venture Capital, incluindo: Direito à Informação (acesso a relatórios contábeis, operacionais e financeiros trimestrais, art. 109, III, da Lei das S.A.); Proteção Anti-Diluição (cláusula de ajuste proporcional de participação societária em rodadas futuras de down-round, modelo weighted average); Direito de Venda Conjunta (Tag Along) (garantia de 100% do preço por ação ofertado ao grupo controlador em caso de alienação de controle societário); e Direito de Preferência (prioridade na subscrição de novas emissões de capital da companhia para manutenção do percentual de participação societária detido).",
        "Em caso de inadimplemento voluntário das obrigações contratuais por quaisquer das partes pactuantes, incidirá o vencimento antecipado do montante mútuo aportado, acrescido de correção monetária, juros moratórios de 1% (um por cento) ao mês e cláusula penal compensatória de 20% (vinte por cento) sobre o saldo devedor atualizado, com esteio nos arts. 408 e 412 do Código Civil.",
    ]),
    ("29. Disposições Finais, Foro Competente e Validade Jurídica", [
        "As diretrizes, projeções, políticas e regras estipuladas ao longo desta Apresentação Empresarial consolidam a visão estratégica da diretoria da A1ELOS Global Numerology e refletem fidedignamente o modelo algorítmico, econômico e técnico já implementado no software e em seus microsserviços associados.",
        "O presente instrumento possui plena validade jurídica, sendo reconhecidas como legítimas e vinculantes as assinaturas eletrônicas efetuadas por meio de certificados digitais nos moldes da Medida Provisória nº 2.200-2/2001 e da Lei nº 14.063/2020.",
        "Para dirimir quaisquer controvérsias, dúvidas ou litígios oriundos da interpretação, execução ou validade deste documento e dos contratos a ele conexos, fica expressamente eleito o Foro da Comarca de São Paulo, Estado de São Paulo, com expressa renúncia a qualquer outro, por mais privilegiado que seja, facultando-se a submissão de litígios societários à arbitragem perante a Câmara de Comércio Brasil-Canadá (CCBC) ou Câmara de Arbitragem do Mercado (CAM/B3), nos termos da Lei nº 9.307/1996.",
    ]),
]

def _render_bloco_juridico(doc, largura, altura, lang, c):
    margem = 18 * mm
    largura_texto = largura - 2 * margem
    y = altura - 32 * mm
    doc.setFillColor(COR_AZUL)
    doc.setFont(_fonte(lang, True), 14)
    y = _texto_wrap(doc, "ESTRUTURA JURÍDICA, GOVERNANÇA E COMPLIANCE",
                    _fonte(lang, True), 14, margem, y, largura_texto, COR_AZUL, 7 * mm)
    doc.setStrokeColor(COR_DOURADO)
    doc.setLineWidth(1.2)
    doc.line(margem, y - 2 * mm, largura - margem, y - 2 * mm)
    y -= 8 * mm
    for titulo, paragrafos in BLOCO_JURIDICO_PT:
        if y < 70 * mm:
            doc.showPage()
            y = altura - 30 * mm
        doc.setFillColor(COR_AZUL)
        doc.setFont(_fonte(lang, True), 12)
        y = _texto_wrap(doc, titulo, _fonte(lang, True), 12, margem, y,
                        largura_texto, COR_AZUL, 5.5 * mm)
        y -= 3 * mm
        for p in paragrafos:
            doc.setFillColor(COR_PRETO)
            y = _texto_wrap(doc, p, _fonte(lang), 10, margem, y,
                            largura_texto, COR_PRETO, 4.5 * mm)
            y -= 3 * mm
        y -= 5 * mm
    return y

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self._desenhar_cabecalho()
            self._desenhar_rodape(num_pages)
            super().showPage()
        super().save()

# ------------------------------------------------------------
# CORES DA MARCA
# ------------------------------------------------------------
COR_AZUL = HexColor("#1E3A8A")
COR_DOURADO = HexColor("#C9A94E")
COR_PRETO = HexColor("#1A1A1A")
COR_CINZA = HexColor("#555555")
COR_CINZA_CLARO = HexColor("#9E9E9E")
COR_FUNDO = HexColor("#F7F5EF")   # bege claro editorial
COR_VERDE = HexColor("#2E7D32")
CORES_GRAFICO = [COR_AZUL, COR_DOURADO, HexColor("#3B82F6"), HexColor("#2E7D32"),
                 HexColor("#8E44AD"), HexColor("#E67E22"), HexColor("#C0392B"),
                 HexColor("#16A085"), HexColor("#F39C12"), HexColor("#7F8C8D")]

# ------------------------------------------------------------
# FONTES
# ------------------------------------------------------------
FONTES = {"normal": "Helvetica", "bold": "Helvetica-Bold"}
_FONTES_EXTRA = {}

def _registrar_cid():
    try:
        for nome in ("STSong-Light", "HeiseiMin-W3"):
            try:
                pdfmetrics.registerFont(UnicodeCIDFont(nome))
            except Exception:
                pass
    except Exception:
        pass

def _registrar_fontes_extra():
    global _FONTES_EXTRA
    if _FONTES_EXTRA:
        return
    base = os.path.dirname(os.path.abspath(__file__))
    candidatos = [
        os.path.join(base, "DejaVuSans.ttf"),          # raiz
        os.path.join(base, "fonts", "DejaVuSans.ttf"), # pasta fonts/
        os.path.join(STATIC_DIR, "DejaVuSans.ttf"),    # static/
    ]
    try:
        for nome, arq in [("DejaVu", "DejaVuSans.ttf"),
                          ("DejaVu-Bold", "DejaVuSans-Bold.ttf")]:
            for pasta in (base, os.path.join(base, "fonts"), STATIC_DIR):
                caminho = os.path.join(pasta, arq)
                if os.path.exists(caminho):
                    pdfmetrics.registerFont(TTFont(nome, caminho))
                    _FONTES_EXTRA[nome] = True
                    break
    except Exception as e:
        logger.warning("Fontes extras: %s", e)

def _quebrar_linhas(texto, fonte, tam, largura):
    """Quebra o texto em linhas que cabem na largura dada."""
    from reportlab.pdfbase.pdfmetrics import stringWidth
    def eh_cjk(ch):
        o = ord(ch)
        return (0x4E00 <= o <= 0x9FFF) or (0x3040 <= o <= 0x30FF)  # CJK + japonês
    linhas, atual = [], ""
    for ch in texto:
        teste = atual + ch if (eh_cjk(ch) or atual == "" or eh_cjk(atual[-1])) else atual + " " + ch
        if stringWidth(teste, fonte, tam) <= largura:
            atual = teste
        else:
            linhas.append(atual)
            atual = ch
    if atual:
        linhas.append(atual)
    return linhas

def _encaixar_texto(doc, x, y, largura, altura_max, texto, tam, lang, cor,
                    min_tam=None, altura_linha=None):
    """Quebra e desenha o texto CENTRALIZADO (horizontal e vertical) dentro
    da área (x, y, largura, altura_max). Encolhe a fonte até caber.
    y = TOPO da área reservada. Retorna o y da base do bloco."""
    from reportlab.pdfbase.pdfmetrics import stringWidth

    fator = {"ja": 0.95, "zh": 0.92, "ru": 0.97}.get(lang, 1.0)  # encolhe um pouco (CJK/cirílico)
    fonte = _fonte(lang, False)
    if min_tam is None:
        min_tam = max(6.0, tam * 0.65)          # piso de segurança
    if altura_linha is None:
        altura_linha = lambda t: t * 1.4         # entrelinha proporcional

    t = tam * fator
    linhas = []
    lh = 0
    while t >= min_tam:
        lh = altura_linha(t) if callable(altura_linha) else altura_linha
        linhas = _quebrar_linhas(texto, fonte, t, largura)
        if len(linhas) * lh <= altura_max:
            break
        t -= 0.5

    if not linhas:                                # nunca deve cair aqui; proteção extra
        linhas = _quebrar_linhas(texto, fonte, t, largura)
        lh = altura_linha(t) if callable(altura_linha) else altura_linha

    total = len(linhas) * lh
    # centraliza verticalmente dentro da área reservada
    y_ini = y + (altura_max - total) / 2 + lh
    doc.setFont(fonte, t)
    doc.setFillColor(cor)
    for ln in linhas:
        doc.drawCentredString(x + largura / 2, y_ini, ln)
        y_ini -= lh
    return y_ini + lh                               # base do bloco

# ===== Canvas com total de páginas (X de Y) =====
_RODAPE_FN = None

class CanvasComTotal(canvas.Canvas):
    def _desenhar_cabecalho(self):
        w, h = self._pagesize
        if self._logo_num:
            try:
                self.drawImage(ImageReader(self._logo_num), 28, h - 34,
                               width=24, height=24, preserveAspectRatio=True,
                               mask='auto')
            except Exception:
                pass
        if self._logo_a1elos:
            try:
                self.drawImage(ImageReader(self._logo_a1elos), w - 52, h - 34,
                               width=24, height=24, preserveAspectRatio=True,
                               mask='auto')
            except Exception:
                pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved = []
        self._logo_num = LOGO_ESQ          # ← era LOGO_PATH (logo.png, esquerda)
        self._logo_a1elos = LOGO_DIR       # ← era LOGO_A1ELOS (A1ELOS.png, direita)

    def showPage(self):
        self._desenhar_cabecalho()          # ← desenha os 2 logos em cada página
        self._saved.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._saved)
        for estado in self._saved:
            self.__dict__.update(estado)
            if _RODAPE_FN is not None:
                _RODAPE_FN(self, self._pageNumber, total)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
 
# -*- coding: utf-8 -*-
# apresentacao_textos.py - Textos das apresentações em 14 idiomas (Versão Atualizada 20/09/2026)
# Estrutura preservada. Valores atualizados: tabela de descontos (até 50%) e projeções (1ª década em 1/3/5/7).

APRESENTACAO_TEXTOS = {

"pt": {
        "titulo": "A1ELOS Global Numerology",
        "subtitulo": "A ciência dos números aplicada ao seu sucesso",
        "capa_nota": "Apresentação Estratégica para Investidores e Parceiros",
        "confidencial": "CONFIDENCIAL",
        "ano": "2026",
        "sumario_titulo": "Sumário Executivo",
        "duns_porque": "Por que o DUNS importa?",
        "preco_consciente": "Preço Consciente",
        "idioma_col": "Idioma",
        "falantes_col": "Falantes (mi)",
        "linhas_idiomas": [
           ["Inglês", "1.528"],
           ["Mandarim", "1.184"],
           ["Espanhol", "558"],
           ["Francês", "396"],
           ["Árabe", "335"],
           ["Português", "270"],
           ["Russo", "255"],
           ["Indonésio", "255"],
           ["Alemão", "134"],
           ["Japonês", "123"],
           ["Vietnamita", "97"],
           ["Turco", "90"],
           ["Italiano", "85"],
           ["Hebraico", "9"],
        ],
        "total_linha": "TOTAL",
        "fonte_receita": "Fonte de Receita",
        "participacao": "Participação",
        "b2c_linha": "B2C — 14 Idiomas",
        "b2b_linha": "B2B — Descontos Progressivos",
        "pub_linha": "Publicidade Geolocalizada",
        "tabela_descontos": "Tabela de Descontos Progressivos",
        "grafico_anos": ["1. Ano", "3. Ano", "5. Ano", "7. Ano", "10. Ano"],
        "grafico_titulo": "Projeção Conservadora (R$ mil)",
        "grafico_titulo_linha": "Crescimento Projetado (R$ mil)",
        "fale_conosco": "Fale Conosco",
        "sumario_intro": "Esta apresentação está estruturada para guiar investidores e parceiros por todos os aspectos estratégicos da A1ELOS Global Numerology — da tese de mercado ao modelo de receita recorrente.",
        "sumario_cards": [
            ("01", "Sobre a A1ELOS", "Holding, portfólio e credencial DUNS"),
            ("02", "Oportunidade de Mercado", "Economia global de bem-estar US$ 6,8 tri"),
            ("03", "Solução e Alcance Global", "14 idiomas, ~5,3 bi de falantes"),
            ("04", "3 Novos Mercados", "Indonésia, Turquia e Vietnã"),
            ("05", "Portfólio e Preços", "23 produtos calibrados por poder aquisitivo"),
            ("06", "Receita Recorrente", "Banners publicitários e Pacotes B2B"),
            ("07", "Projeções e Investimento", "Horizonte de 50 anos · Rodada Seed R$ 3,5M"),
        ],
        "sobre_titulo": "Sobre a A1ELOS",
        "sobre_texto": "A A1ELOS é uma holding de tecnologia e conhecimento que une inteligência artificial, numerologia aplicada e estratégia cultural para criar produtos digitais de alto impacto em escala global. Nossa missão: democratizar o autoconhecimento numérico com respeito cultural e respeito ao poder aquisitivo de cada mercado.",
        "sobre_kpis": [
            ("23", "Produtos Ativos", "Em 4 níveis de acesso"),
            ("14", "Idiomas", "~67% da população mundial"),
            ("5,3B", "Falantes", "Mercado endereçável real"),
            ("IA", "Integrada", "Motor de personalização"),
        ],
        "sobre_duns": "DUNS 942242668 — Certificação Dun & Bradstreet válida em 190+ países, habilitando contratos B2B e joint ventures internacionais.",
        "duns_titulo": "Credibilidade Internacional",
        "duns_texto": "O número DUNS é o passaporte corporativo da A1ELOS no cenário internacional. Ele sinaliza a parceiros, clientes corporativos e investidores que a empresa possui identidade verificável, histórico rastreável e capacidade contratual em qualquer jurisdição.",
        "duns_numero": "942242668",
        "duns_emitido": "Emitido pela Dun & Bradstreet — o padrão global de identidade empresarial reconhecido em mais de 190 países.",
        "duns_paises": "190+ PAÍSES",
        "duns_beneficios": [
            ("Contratos B2B", "Habilitação para licitações e fornecedores globais"),
            ("Joint Ventures", "Parcerias internacionais com due diligence facilitada"),
            ("Credibilidade Imediata", "Sinal de seriedade para investidores institucionais"),
        ],
        "mercado_titulo": "Oportunidade de Mercado",
        "mercado_texto": "Vivemos a convergência perfeita: o bem-estar digital explode globalmente enquanto a numerologia e astrologia migram para apps de alto engajamento. A A1ELOS está posicionada exatamente nessa interseção, com 74% da população mundial já online (~6 bilhões de pessoas).",
        "mercado_cards": [
            ("Bem-Estar Global", "US$ 6,8 tri → US$ 9,8 tri até 2029 (+7,6% a.a.)"),
            ("Apps Astrologia/Numerologia", "US$ 3 bi → US$ 9 bi até 2030 · CAGR 20%"),
            ("Apps de Bem-Estar", "CAGR 14,9% → US$ 26,2 bi em 2030"),
            ("Usuários Online", "74% do mundo · ~6 bilhões de pessoas"),
        ],
        "problema_titulo": "O Problema que Resolvemos",
        "problema_col_esq_titulo": "Falhas do Mercado Atual",
        "problema_col_esq": [
            ("Barreira de Idioma", "A esmagadora maioria das ferramentas de numerologia opera apenas em inglês, excluindo bilhões de falantes nativos em outros idiomas."),
            ("Preços Descolados da Realidade", "Produtos cobrados em dólar para mercados emergentes geram exclusão econômica — o usuário não rejeita o produto, rejeita o preço inacessível."),
            ("Ausência de Profundidade", "Ferramentas genéricas entregam respostas superficiais sem personalização, sem contexto cultural e sem aplicação prática ao dia a dia."),
        ],
        "problema_col_dir_titulo": "O Custo da Exclusão",
        "problema_col_dir": "Quando uma plataforma ignora idioma e poder aquisitivo, ela voluntariamente abandona o maior mercado do mundo: os 4+ bilhões de pessoas que vivem em economias emergentes e falam línguas não-anglófonas. Esse é o gap que a A1ELOS ocupa com precisão cirúrgica.",
        "problema_destaque": "Plataformas que ignoram poder aquisitivo local perdem acesso a mais de 60% do mercado endereçável global.",
        "solucao_titulo": "Nossa Solução: 3 Pilares Estratégicos",
        "solucao_texto": "A A1ELOS construiu uma plataforma integrada que combina ciência numérica, inteligência artificial e sensibilidade cultural. A solução opera em três frentes complementares, garantindo receita diversificada e alta retenção.",
        "solucao_colunas": [
            ("Mapas Pessoais", "Análises numéricas profundas e personalizadas para o usuário final — identidade, missão, ciclos de vida e compatibilidade — entregues em 14 idiomas com IA integrada."),
            ("Numerologia Empresarial", "Diagnósticos numerológicos aplicados a marcas, CNPJs, datas de fundação e estratégia corporativa. Produto diferenciado de alto valor percebido pelo mercado B2B."),
            ("White-Label B2B", "Licenciamento da plataforma para empresas parceiras que desejam oferecer numerologia sob sua própria marca — com suporte multilíngue e personalização completa."),
        ],
        "alcance_titulo": "Alcance Global: 14 Idiomas · ~5,3 Bilhões de Falantes",
        "alcance_texto": "A A1ELOS cobre ~67% da população mundial com uma plataforma genuinamente multilíngue. Cada idioma representa um mercado cultural distinto, com precificação calibrada ao poder aquisitivo local.",
        "mercados_titulo": "Os 3 Novos Mercados: +442 Milhões de Falantes",
        "mercados_texto": "A expansão estratégica para Indonésia, Turquia e Vietnã representa um salto qualitativo: mercados com alto crescimento econômico, penetração digital crescente e demanda comprovada por soluções de bem-estar digital acessíveis.",
        "mercados_cards": [
            ("Indonésia", ["285 mi habitantes", "80,5% penetração de internet", "~255 mi falantes de Indonésio", "Bem-estar: US$ 51,2 bi (2025) → US$ 72,8 bi (2034)"]),
            ("Turquia", ["85,9 mi habitantes", "PIB PPP per capita US$ 37.301", "~90 mi falantes de Turco", "Acima da média mundial (US$ 27.211)"]),
            ("Vietnã",  ["~100 mi habitantes", "PIB per capita ~US$ 5.066 (+7,4%/ano)", "~97 mi falantes de Vietnamita", "Bem-estar: US$ 303 mi (2025) → US$ 485 mi (2030)"]),
        ],
        "mercados_rodape": "3 mercados novos = +442 milhões de novos falantes endereçáveis — incorporados à plataforma com precificação culturalmente calibrada.",
        "preco_titulo": "Filosofia de Preço Consciente",
        "preco_esq": "Respeito cultural + respeito ao poder aquisitivo = mercado endereçável real. Mesma proporção de valor. Preços diferentes. Dignidade igual para todos os mercados.",
        "preco_dir_titulo": "Como Funciona na Prática",
        "preco_dir": "A A1ELOS aplica Paridade de Poder de Compra (PPC) como critério central de precificação. O mesmo produto entrega o mesmo valor relativo ao usuário em Lagos, Jacarta, Hanói ou Nova York — o preço é calibrado para que o esforço financeiro seja proporcional à renda local.",
        "preco_pilares": [
            ("Calibração por PPC", "Preços ajustados ao índice de poder aquisitivo de cada país"),
            ("Respeito Cultural", "Idioma, moeda e contexto local integrados ao produto"),
            ("Conversão Superior", "Preço justo gera mais conversão e maior retenção de longo prazo"),
        ],
        "portfolio_titulo": "Portfólio: 23 Produtos em 4 Níveis",
        "portfolio_texto": "A estrutura em camadas garante que cada perfil de usuário — do curioso ao profissional — encontre uma oferta adequada ao seu nível de engajamento e capacidade financeira.",
        "portfolio_tabela": [
            ["Nível", "Produtos", "Faixa de Preço (R$)", "Perfil"],
            ["Básico", "Mapa Express, Mapa Completo", "R$ 8 – 17", "Curioso, primeiro contato"],
            ["Intermediário", "Pesquisa IA, Nome de Urna, Nº Eleitoral", "R$ 26 – 53", "Usuário engajado"],
            ["Avançado", "Numerologia Empresarial, Ciclos, Missão", "R$ 81 – 109", "Profissional, empreendedor"],
            ["Premium", "Diagnósticos Completos, Mapas Pessoais", "R$ 137 – 305", "Alta renda, uso corporativo"],
            ["B2B", "Pacotes empresariais, licenças, brindes", "Sob consulta", "Empresas e equipes"],
        ],
        "portfolio_rodape": "23 produtos cobrem toda a jornada do usuário, do primeiro contato ao cliente recorrente premium — maximizando LTV por idioma e mercado.",
        "negocio_titulo": "Modelo de Negócio: 3 Fontes de Receita",
        "negocio_texto": "A A1ELOS foi desenhada com receita diversificada e escalável: vendas diretas ao consumidor final em escala global, contratos B2B de alto valor e publicidade geolocalizada recorrente — três motores que se alimentam mutuamente.",
        "negocio_colunas": [
            ("B2C — 14 Idiomas", "Venda direta de produtos digitais em todas as moedas, com precificação adaptada por PPC. Escala automática via IA — sem equipe de atendimento proporcional ao crescimento."),
            ("B2B — Descontos Progressivos", "Pacotes corporativos para RH, employer branding e brindes institucionais. Descontos de 10% a 50% conforme volume. Acima de 2.000 códigos, negociação direta (Plano Diamante). Contratos respaldados pelo DUNS 942242668."),
            ("Publicidade Geolocalizada", "Banners segmentados por país, continente ou mundial com rotação automatizada. Receita recorrente mensal de alto valor — sem dependência de volume de vendas de produto."),
        ],
        "banners_titulo": "Banners Publicitários — Receita Recorrente Mensal",
        "banners_texto": "A plataforma A1ELOS oferece espaços publicitários premium com segmentação precisa por geolocalização — país, continente ou mundial. Com rotação automática a cada 8 segundos e formatos otimizados para desktop e mobile, os banners entregam visibilidade mensurável a anunciantes regionais e internacionais.",
        "banners_tabela": [
            ["Segmentação", "Fixo (R$/mês)", "Temporário (R$/mês)", "Perfil de Anunciante"],
            ["País", "R$ 800", "R$ 500", "PMEs locais, comércio regional"],
            ["Continente", "R$ 1.800", "R$ 1.200", "Marcas regionais, expansão continental"],
            ["Mundo", "R$ 3.500", "R$ 2.500", "Empresas globais, apps internacionais"],
            ["Patrocínio Exclusivo", "R$ 6.000", "R$ 4.500/campanha", "Patrocinadores master, lançamentos"],
        ],
        "banners_formatos": "728×90 px — Banner central desktop · 320×100 px — Formato mobile otimizado · 8 segundos — Rotação automática · Geo-alvo — País, continente ou alcance mundial",
        "b2b_titulo": "Pacotes Empresariais B2B — Alto Valor, Alto Volume",
        "b2b_texto": "Os Pacotes B2B transformam a A1ELOS em uma ferramenta de employer branding e bem-estar corporativo. Empresas adquirem códigos de acesso em volume para distribuir como brindes a colaboradores ou clientes — respaldadas pelo DUNS 942242668 para contratos corporativos formais.",
        "b2b_planos": [
            ("Plano Básico · 50 códigos", "50× Mapa Express (R$ 8 cada). Ideal para programas de benefícios a colaboradores e ações de integração."),
            ("Plano Intermediário · 100 códigos", "50× Mapa Express + 50× Pesquisa IA (R$ 17). Perfeito para equipes e estratégia de marca empregadora."),
            ("Plano Premium · 200 códigos", "100× Mapa Express + 100× Mapa Completo (R$ 17). Máxima profundidade analítica para grandes grupos."),
        ],
        "b2b_tabela": [
            ["A partir de", "Desconto", "Perfil", "Uso Recomendado"],
            ["10 códigos", "10%", "Pequenas equipes", "Ação pontual de bem-estar"],
            ["50 códigos", "20%", "Equipes em crescimento", "Programas recorrentes"],
            ["100 códigos", "25%", "PMEs", "Benefício trimestral"],
            ["200 códigos", "30%", "Empresas médias", "Programas completos"],
            ["500 códigos", "40%", "Médias empresas", "Brinde anual a colaboradores"],
            ["1.000 códigos", "45%", "Grandes corporações", "Fidelização de clientes"],
            ["2.000 códigos", "50%", "Grandes grupos", "Larga escala"],
            ["Acima de 2.000", "Negociável", "Plano Diamante sob medida", "Distribuição de bônus em volume"],
        ],
        "projecoes_titulo": "Projeções Financeiras: Horizonte de 50 Anos",
        "projecoes_texto": "As projeções foram construídas com base em estimativas percentuais de penetração sobre o mercado potencial de ~5,32 bilhões de falantes, com conversão conservadora de 3% e resgate de bônus entre 70% e 90%. A primeira década é detalhada nos anos 1, 3, 5 e 7 para evidenciar o momentum.",
        "projecoes_tabela": [
            ["Horizonte", "Conservador (R$)", "Otimista (R$)"],
            ["Ano 1", "R$ 281k", "R$ 702k"],
            ["Ano 3", "R$ 983k", "R$ 2,8M"],
            ["Ano 5", "R$ 2,8M", "R$ 7M"],
            ["Ano 7", "R$ 5,6M", "R$ 14M"],
            ["Ano 10", "R$ 11,2M", "R$ 28,1M"],
            ["Ano 20", "R$ 42,1M", "R$ 112M"],
            ["Ano 30", "R$ 84,3M", "R$ 211M"],
            ["Ano 40", "R$ 126M", "R$ 351M"],
            ["Ano 50", "R$ 169M", "R$ 492M"],
        ],
        "tracao_titulo": "Tração e Resultados Comprovados",
        "tracao_texto": "A A1ELOS já opera com métricas de produto que validam o modelo — alta retenção, avaliação premium e uma base crescente de parceiros B2B demonstram que a plataforma entrega valor real ao usuário final e ao mercado corporativo.",
        "tracao_kpis": [
            ("12K+", "Usuários Ativos", "Base orgânica em crescimento consistente"),
            ("87%", "Retenção", "Muito acima da média da indústria (~30%)"),
            ("4,8★", "Avaliação Média", "Satisfação comprovada do usuário final"),
            ("23", "Parceiros B2B", "Contratos ativos com empresas e RHs"),
        ],
        "roteiro_titulo": "Roteiro Estratégico",
        "roteiro_texto": "A A1ELOS executa um plano em quatro fases progressivas — da consolidação da base atual à liderança global de mercado, com opções claras de saída para investidores.",
        "roteiro_fases": [
            ("Fase 1 · Consolidação", "Fortalecimento da base de usuários nos idiomas já ativos. Otimização de conversão, retenção e LTV. Rodada Seed concluída."),
            ("Fase 2 · Expansão", "Lançamento oficial nos 3 novos mercados: Indonésia, Turquia e Vietnã. Aceleração do canal B2B e publicidade geolocalizada."),
            ("Fase 3 · Entrada Global", "Presença ativa em todos os 14 idiomas com campanhas localizadas. Parcerias white-label em 5+ continentes. Série A."),
            ("Fase 4 · Liderança", "20+ países com operações consolidadas. Plataforma SaaS de referência global em numerologia aplicada. IPO ou exit estratégico."),
        ],
        "invest_titulo": "Investimento & Contato",
        "invest_texto": "Estamos prontos para apresentações privadas, due diligence e negociações. Entre em contato pelo canal de sua preferência.",
        "invest_dados": [
            ("Rodada Seed", "R$ 3,5 milhões"),
            ("Valuation Pré-Money", "R$ 14 milhões"),
            ("Equity Ofertado", "Até 20%"),
        ],
        "invest_contato": [
            ("E-mail Investidores", "a1elos.consultoria@gmail.com"),
            ("E-mail Geral", "contato@a1elos.com"),
            ("Website", "www.a1elos.com"),
            ("DUNS", "942242668 — Dun & Bradstreet"),
        ],
        "invest_alocacao": "Alocação do Capital: 45% Tecnologia · 30% Marketing · 25% Operações",
        "frase_final": "Os números nunca mentem.",
        "selo_final": ["DUNS 942242668", "23 PRODUTOS", "14 IDIOMAS", "~5,3 BI FALANTES"],
        "graf_cons": "Conservador",
        "graf_otim": "Otimista",
        "grafico_titulo_linha": "Crescimento Projetado (R$ mil)",
        "pix_titulo": "Brasil: A Infraestrutura Pix",
        "pix_texto": "O Pix é a infraestrutura pública de pagamentos instantâneos do Brasil. Para a A1ELOS, ele garante cobrança imediata, baixo custo e aceitação universal — o alicerce da operação B2C no mercado brasileiro e a porta de entrada para a expansão internacional.",
        "pix_kpis": [
            ("30,1 bi", "Transações em 2025", "+20% vs 2024 · Febraban"),
            ("76,4%", "da população usa Pix", "211 milhões de brasileiros · Banco Central"),
            ("R$ 68,2 tri", "movimentados no 2º sem. 2025", "78,4 bi de transações · Banco Central"),
            ("~80 bi", "transações em 2025", "+25,7% vs ano anterior · Relatório do Pix"),
        ],
        "pix_fonte": "Fontes: Banco Central do Brasil (Pix em Números) e Febraban (Pesquisa de Tecnologia Bancária).",
        "ref_titulo": "Referências Bibliográficas",
        "ref_intro": "Fontes utilizadas para os dados de mercado, projeções e indicadores desta apresentação.",
        "ref_lista": [
            ("Global Wellness Institute", "Economia global do bem-estar: US$ 6,8 tri (2024) → US$ 9,8 tri (2029)."),
            ("MarkNtel Advisors", "Apps de astrologia e numerologia: US$ 3 bi → US$ 9 bi até 2030 (CAGR ~20%)."),
            ("FMI · Banco Mundial", "PIB e paridade do poder de compra (PPP) por país."),
            ("Banco Central do Brasil", "Estatísticas oficiais do Pix: transações, volume e usuários."),
            ("Febraban", "Pesquisa de Tecnologia Bancária — crescimento do Pix em 2025."),
            ("IBGE", "População e indicadores socioeconômicos do Brasil."),
        ],
        },

"en": {
        "titulo": "A1ELOS Global Numerology",
        "subtitulo": "The science of numbers applied to your success",
        "capa_nota": "Strategic Presentation for Investors and Partners",
        "confidencial": "CONFIDENTIAL",
        "ano": "2026",
        "sumario_titulo": "Executive Summary",
        "duns_porque": "Why does DUNS matter?",
        "preco_consciente": "Conscious Pricing",
        "idioma_col": "Language",
        "falantes_col": "Speakers (M)",
        "linhas_idiomas": [
           ["English", "1,528"],
           ["Mandarin", "1,184"],
           ["Spanish", "558"],
           ["French", "396"],
           ["Arabic", "335"],
           ["Portuguese", "270"],
           ["Russian", "255"],
           ["Indonesian", "255"],
           ["German", "134"],
           ["Japanese", "123"],
           ["Vietnamese", "97"],
           ["Turkish", "90"],
           ["Italian", "85"],
           ["Hebrew", "9"],
        ],
        "total_linha": "TOTAL",
        "fonte_receita": "Revenue Source",
        "participacao": "Share",
        "b2c_linha": "B2C — 14 Languages",
        "b2b_linha": "B2B — Progressive Discounts",
        "pub_linha": "Geolocated Advertising",
        "tabela_descontos": "Progressive Discount Table",
        "grafico_anos": ["Year 1", "Year 3", "Year 5", "Year 7", "Year 10"],
        "grafico_titulo": "Conservative Projection (R$ thousand)",
        "grafico_titulo_linha": "Projected Growth (R$ thousand)",
        "fale_conosco": "Contact Us",
        "sumario_intro": "This presentation is structured to guide investors and partners through all strategic aspects of A1ELOS Global Numerology — from the market thesis to the recurring revenue model.",
        "sumario_cards": [
            ("01", "About A1ELOS", "Holding, portfolio and DUNS credential"),
            ("02", "Market Opportunity", "Global wellness economy US$ 6.8T"),
            ("03", "Solution and Global Reach", "14 languages, ~5.3B speakers"),
            ("04", "3 New Markets", "Indonesia, Turkey and Vietnam"),
            ("05", "Portfolio and Pricing", "23 products calibrated by purchasing power"),
            ("06", "Recurring Revenue", "Advertising banners and B2B Packages"),
            ("07", "Projections and Investment", "50-year horizon · Seed Round R$ 3.5M"),
        ],
        "sobre_titulo": "About A1ELOS",
        "sobre_texto": "A1ELOS is a technology and knowledge holding that combines artificial intelligence, applied numerology and cultural strategy to create high-impact digital products on a global scale. Our mission: to democratize numerical self-knowledge with cultural respect and respect for the purchasing power of each market.",
        "sobre_kpis": [
            ("23", "Active Products", "In 4 access levels"),
            ("14", "Languages", "~67% of the world population"),
            ("5.3B", "Speakers", "Real addressable market"),
            ("AI", "Integrated", "Personalization engine"),
        ],
        "sobre_duns": "DUNS 942242668 — Dun & Bradstreet certification valid in 190+ countries, enabling B2B contracts and international joint ventures.",
        "duns_titulo": "International Credibility",
        "duns_texto": "The DUNS number is A1ELOS's corporate passport on the international stage. It signals to partners, corporate clients and investors that the company has verifiable identity, traceable history and contractual capacity in any jurisdiction.",
        "duns_numero": "942242668",
        "duns_emitido": "Issued by Dun & Bradstreet — the global standard of business identity recognized in more than 190 countries.",
        "duns_paises": "190+ COUNTRIES",
        "duns_beneficios": [
            ("B2B Contracts", "Qualification for tenders and global suppliers"),
            ("Joint Ventures", "International partnerships with facilitated due diligence"),
            ("Immediate Credibility", "A sign of seriousness for institutional investors"),
        ],
        "mercado_titulo": "Market Opportunity",
        "mercado_texto": "We live the perfect convergence: digital wellness explodes globally while numerology and astrology migrate to high-engagement apps. A1ELOS is positioned exactly at this intersection, with 74% of the world population already online (~6 billion people).",
        "mercado_cards": [
            ("Global Wellness", "US$ 6.8T → US$ 9.8T by 2029 (+7.6% p.a.)"),
            ("Astrology/Numerology Apps", "US$ 3B → US$ 9B by 2030 · CAGR 20%"),
            ("Wellness Apps", "CAGR 14.9% → US$ 26.2B in 2030"),
            ("Online Users", "74% of the world · ~6 billion people"),
        ],
        "problema_titulo": "The Problem We Solve",
        "problema_col_esq_titulo": "Current Market Failures",
        "problema_col_esq": [
            ("Language Barrier", "The vast majority of numerology tools operate only in English, excluding billions of native speakers in other languages."),
            ("Prices Out of Touch with Reality", "Products priced in dollars for emerging markets generate economic exclusion — the user does not reject the product, they reject the inaccessible price."),
            ("Lack of Depth", "Generic tools deliver superficial answers without personalization, without cultural context and without practical application to daily life."),
        ],
        "problema_col_dir_titulo": "The Cost of Exclusion",
        "problema_col_dir": "When a platform ignores language and purchasing power, it voluntarily abandons the largest market in the world: the 4+ billion people who live in emerging economies and speak non-Anglophone languages. This is the gap A1ELOS occupies with surgical precision.",
        "problema_destaque": "Platforms that ignore local purchasing power lose access to more than 60% of the global addressable market.",
        "solucao_titulo": "Our Solution: 3 Strategic Pillars",
        "solucao_texto": "A1ELOS built an integrated platform that combines numerical science, artificial intelligence and cultural sensitivity. The solution operates on three complementary fronts, ensuring diversified revenue and high retention.",
        "solucao_colunas": [
            ("Personal Maps", "Deep and personalized numerical analyses for the end user — identity, mission, life cycles and compatibility — delivered in 14 languages with integrated AI."),
            ("Business Numerology", "Numerological diagnostics applied to brands, CNPJs, founding dates and corporate strategy. A differentiated product of high perceived value for the B2B market."),
            ("White-Label B2B", "Platform licensing for partner companies that wish to offer numerology under their own brand — with multilingual support and complete customization."),
        ],
        "alcance_titulo": "Global Reach: 14 Languages · ~5.3 Billion Speakers",
        "alcance_texto": "A1ELOS covers ~67% of the world population with a genuinely multilingual platform. Each language represents a distinct cultural market, with pricing calibrated to local purchasing power.",
        "mercados_titulo": "The 3 New Markets: +442 Million Speakers",
        "mercados_texto": "The strategic expansion into Indonesia, Turkey and Vietnam represents a qualitative leap: markets with high economic growth, growing digital penetration and proven demand for accessible digital wellness solutions.",
        "mercados_cards": [
            ("Indonesia", ["285M inhabitants", "80.5% internet penetration", "~255M Indonesian speakers", "Wellness: US$ 51.2B (2025) → US$ 72.8B (2034)"]),
            ("Turkey", ["85.9M inhabitants", "GDP PPP per capita US$ 37,301", "~90M Turkish speakers", "Above world average (US$ 27,211)"]),
            ("Vietnam",  ["~100M inhabitants", "GDP per capita ~US$ 5,066 (+7.4%/year)", "~97M Vietnamese speakers", "Wellness: US$ 303M (2025) → US$ 485M (2030)"]),
        ],
        "mercados_rodape": "3 new markets = +442 million new addressable speakers — incorporated into the platform with culturally calibrated pricing.",
        "preco_titulo": "Conscious Pricing Philosophy",
        "preco_esq": "Cultural respect + respect for purchasing power = real addressable market. Same proportion of value. Different prices. Equal dignity for all markets.",
        "preco_dir_titulo": "How It Works in Practice",
        "preco_dir": "A1ELOS applies Purchasing Power Parity (PPP) as the central pricing criterion. The same product delivers the same relative value to the user in Lagos, Jakarta, Hanoi or New York — the price is calibrated so that the financial effort is proportional to local income.",
        "preco_pilares": [
            ("PPP Calibration", "Prices adjusted to the purchasing power index of each country"),
            ("Cultural Respect", "Language, currency and local context integrated into the product"),
            ("Superior Conversion", "Fair price generates more conversion and greater long-term retention"),
        ],
        "portfolio_titulo": "Portfolio: 23 Products in 4 Levels",
        "portfolio_texto": "The layered structure ensures that every user profile — from the curious to the professional — finds an offer suited to their level of engagement and financial capacity.",
        "portfolio_tabela": [
            ["Level", "Products", "Price Range (R$)", "Profile"],
            ["Basic", "Express Map, Full Map", "R$ 8 – 17", "Curious, first contact"],
            ["Intermediate", "AI Search, Ballot Name, Electoral No.", "R$ 26 – 53", "Engaged user"],
            ["Advanced", "Business Numerology, Cycles, Mission", "R$ 81 – 109", "Professional, entrepreneur"],
            ["Premium", "Complete Diagnostics, Personal Maps", "R$ 137 – 305", "High income, corporate use"],
            ["B2B", "Business packages, licenses, gifts", "On request", "Companies and teams"],
        ],
        "portfolio_rodape": "23 products cover the entire user journey, from first contact to recurring premium customer — maximizing LTV per language and market.",
        "negocio_titulo": "Business Model: 3 Revenue Streams",
        "negocio_texto": "A1ELOS was designed with diversified and scalable revenue: direct sales to the end consumer on a global scale, high-value B2B contracts and recurring geolocated advertising — three engines that feed each other.",
        "negocio_colunas": [
            ("B2C — 14 Languages", "Direct sale of digital products in all currencies, with pricing adapted by PPP. Automatic scaling via AI — no support team proportional to growth."),
            ("B2B — Progressive Discounts", "Corporate packages for HR, employer branding and institutional gifts. Discounts from 10% to 50% by volume. Above 2,000 codes, direct negotiation (Diamond Plan). Contracts backed by DUNS 942242668."),
            ("Geolocated Advertising", "Banners segmented by country, continent or worldwide with automated rotation. High-value recurring monthly revenue — without dependence on product sales volume."),
        ],
        "banners_titulo": "Advertising Banners — Predictable Monthly Revenue",
        "banners_texto": "The A1ELOS geolocated advertising platform offers advertisers precise segmentation by country, continent or global reach, with formats optimized for desktop and mobile and automated rotation every 8 seconds.",
        "banners_tabela": [
            ["Segmentation", "Fixed (R$/month)", "Temporary (R$/month)", "Advertiser Profile"],
            ["Country", "R$ 800", "R$ 500", "Local SMEs, regional commerce"],
            ["Continent", "R$ 1,800", "R$ 1,200", "Regional brands, continental expansion"],
            ["World", "R$ 3,500", "R$ 2,500", "Global companies, international apps"],
            ["Exclusive Sponsorship", "R$ 6,000", "R$ 4,500/campaign", "Master sponsors, launches"],
        ],
        "banners_formatos": "728×90 px — Central desktop banner · 320×100 px — Optimized mobile format · 8 seconds — Automatic rotation · Geo-target — Country, continent or worldwide reach",
        "b2b_titulo": "B2B Business Packages — High Value, High Volume",
        "b2b_texto": "B2B Packages turn A1ELOS into an employer branding and corporate wellness tool. Companies purchase access codes in volume to distribute as gifts to employees or clients — backed by DUNS 942242668 for formal corporate contracts.",
        "b2b_planos": [
            ("Basic Plan · 50 codes", "50× Express Map (R$ 8 each). Ideal for employee benefit programs and integration actions."),
            ("Intermediate Plan · 100 codes", "50× Express Map + 50× AI Search (R$ 17). Perfect for teams and employer branding strategy."),
            ("Premium Plan · 200 codes", "100× Express Map + 100× Full Map (R$ 17). Maximum analytical depth for large groups."),
        ],
        "b2b_tabela": [
            ["From", "Discount", "Profile", "Recommended Use"],
            ["10 codes", "10%", "Small teams", "One-off wellness action"],
            ["50 codes", "20%", "Growing teams", "Recurring programs"],
            ["100 codes", "25%", "SMEs", "Quarterly benefit"],
            ["200 codes", "30%", "Medium companies", "Complete programs"],
            ["500 codes", "40%", "Medium-sized companies", "Annual gift to employees"],
            ["1,000 codes", "45%", "Large corporations", "Customer loyalty"],
            ["2,000 codes", "50%", "Large groups", "Large scale"],
            ["Above 2,000", "Negotiable", "Custom Diamond Plan", "Volume bonus distribution"],
        ],
        "projecoes_titulo": "Financial Projections: 50-Year Horizon",
        "projecoes_texto": "The projections were built based on percentage penetration estimates over the potential market of ~5.32 billion speakers, with a conservative 3% conversion and bonus redemption between 70% and 90%. The first decade is detailed in years 1, 3, 5 and 7 to highlight momentum.",
        "projecoes_tabela": [
            ["Horizon", "Conservative (R$)", "Optimistic (R$)"],
            ["Year 1", "R$ 281k", "R$ 702k"],
            ["Year 3", "R$ 983k", "R$ 2.8M"],
            ["Year 5", "R$ 2.8M", "R$ 7M"],
            ["Year 7", "R$ 5.6M", "R$ 14M"],
            ["Year 10", "R$ 11.2M", "R$ 28.1M"],
            ["Year 20", "R$ 42.1M", "R$ 112M"],
            ["Year 30", "R$ 84.3M", "R$ 211M"],
            ["Year 40", "R$ 126M", "R$ 351M"],
            ["Year 50", "R$ 169M", "R$ 492M"],
        ],
        "tracao_titulo": "Traction and Proven Results",
        "tracao_texto": "A1ELOS already operates with product metrics that validate the model — high retention, premium rating and a growing base of B2B partners demonstrate that the platform delivers real value to the end user and the corporate market.",
        "tracao_kpis": [
            ("12K+", "Active Users", "Consistently growing organic base"),
            ("87%", "Retention", "Well above industry average (~30%)"),
            ("4.8★", "Average Rating", "Proven end-user satisfaction"),
            ("23", "B2B Partners", "Active contracts with companies and HR"),
        ],
        "roteiro_titulo": "Strategic Roadmap",
        "roteiro_texto": "A1ELOS executes a plan in four progressive phases — from consolidating the current base to global market leadership, with clear exit options for investors.",
        "roteiro_fases": [
            ("Phase 1 · Consolidation", "Strengthening the user base in already active languages. Optimization of conversion, retention and LTV. Seed Round concluded."),
            ("Phase 2 · Expansion", "Official launch in the 3 new markets: Indonesia, Turkey and Vietnam. Acceleration of the B2B channel and geolocated advertising."),
            ("Phase 3 · Global Entry", "Active presence in all 14 languages with localized campaigns. White-label partnerships in 5+ continents. Series A."),
            ("Phase 4 · Leadership", "20+ countries with consolidated operations. Global reference SaaS platform in applied numerology. IPO or strategic exit."),
        ],
        "invest_titulo": "Investment & Contact",
        "invest_texto": "We are ready for private presentations, due diligence and negotiations. Contact us through your preferred channel.",
        "invest_dados": [
            ("Seed Round", "R$ 3.5 million"),
            ("Pre-Money Valuation", "R$ 14 million"),
            ("Equity Offered", "Up to 20%"),
        ],
        "invest_contato": [
            ("Investors Email", "a1elos.consultoria@gmail.com"),
            ("General Email", "contato@a1elos.com"),
            ("Website", "www.a1elos.com"),
            ("DUNS", "942242668 — Dun & Bradstreet"),
        ],
        "invest_alocacao": "Capital Allocation: 45% Technology · 30% Marketing · 25% Operations",
        "frase_final": "Numbers never lie.",
        "selo_final": ["DUNS 942242668", "23 PRODUCTS", "14 LANGUAGES", "~5.3B SPEAKERS"],
        "graf_cons": "Conservative",
        "graf_otim": "Optimistic",
        "grafico_titulo_linha": "Projected Growth (R$ thousand)",
        "pix_titulo": "Brazil: The Pix Infrastructure",
        "pix_texto": "Pix is Brazil's public instant payment infrastructure. For A1ELOS, it guarantees immediate collection, low cost and universal acceptance — the foundation of the B2C operation in the Brazilian market and the gateway to international expansion.",
        "pix_kpis": [
            ("30.1B", "Transactions in 2025", "+20% vs 2024 · Febraban"),
            ("76.4%", "of the population uses Pix", "211 million Brazilians · Central Bank"),
            ("R$ 68.2T", "moved in 2nd half 2025", "78.4B transactions · Central Bank"),
            ("~80B", "transactions in 2025", "+25.7% vs previous year · Pix Report"),
        ],
        "pix_fonte": "Sources: Central Bank of Brazil (Pix in Numbers) and Febraban (Banking Technology Survey).",
        "ref_titulo": "Bibliographic References",
        "ref_intro": "Sources used for the market data, projections and indicators of this presentation.",
        "ref_lista": [
            ("Global Wellness Institute", "Global wellness economy: US$ 6.8T (2024) → US$ 9.8T (2029)."),
            ("MarkNtel Advisors", "Astrology and numerology apps: US$ 3B → US$ 9B by 2030 (CAGR ~20%)."),
            ("IMF · World Bank", "GDP and purchasing power parity (PPP) by country."),
            ("Central Bank of Brazil", "Official Pix statistics: transactions, volume and users."),
            ("Febraban", "Banking Technology Survey — Pix growth in 2025."),
            ("IBGE", "Population and socioeconomic indicators of Brazil."),
        ],
        },
"es": {
        "titulo": "A1ELOS Global Numerology",
        "subtitulo": "La ciencia de los números aplicada a tu éxito",
        "capa_nota": "Presentación Estratégica para Inversores y Socios",
        "confidencial": "CONFIDENCIAL",
        "ano": "2026",
        "sumario_titulo": "Resumen Ejecutivo",
        "duns_porque": "¿Por qué importa el DUNS?",
        "preco_consciente": "Precio Consciente",
        "idioma_col": "Idioma",
        "falantes_col": "Hablantes (M)",
        "linhas_idiomas": [
           ["Inglés", "1.528"],
           ["Mandarín", "1.184"],
           ["Español", "558"],
           ["Francés", "396"],
           ["Árabe", "335"],
           ["Portugués", "270"],
           ["Ruso", "255"],
           ["Indonesio", "255"],
           ["Alemán", "134"],
           ["Japonés", "123"],
           ["Vietnamita", "97"],
           ["Turco", "90"],
           ["Italiano", "85"],
           ["Hebreo", "9"],
        ],
        "total_linha": "TOTAL",
        "fonte_receita": "Fuente de Ingresos",
        "participacao": "Participación",
        "b2c_linha": "B2C — 14 Idiomas",
        "b2b_linha": "B2B — Descuentos Progresivos",
        "pub_linha": "Publicidad Geolocalizada",
        "tabela_descontos": "Tabla de Descuentos Progresivos",
        "grafico_anos": ["Año 1", "Año 3", "Año 5", "Año 7", "Año 10"],
        "grafico_titulo": "Proyección Conservadora (R$ mil)",
        "grafico_titulo_linha": "Crecimiento Proyectado (R$ mil)",
        "fale_conosco": "Contáctenos",
        "sumario_intro": "Esta presentación está estructurada para guiar a inversores y socios por todos los aspectos estratégicos de A1ELOS Global Numerology — desde la tesis de mercado hasta el modelo de ingresos recurrentes.",
        "sumario_cards": [
            ("01", "Sobre A1ELOS", "Holding, portafolio y credencial DUNS"),
            ("02", "Oportunidad de Mercado", "Economía global de bienestar US$ 6,8 billones"),
            ("03", "Solución y Alcance Global", "14 idiomas, ~5,3 mil millones de hablantes"),
            ("04", "3 Nuevos Mercados", "Indonesia, Turquía y Vietnam"),
            ("05", "Portafolio y Precios", "23 productos calibrados por poder adquisitivo"),
            ("06", "Ingresos Recurrentes", "Banners publicitarios y Paquetes B2B"),
            ("07", "Proyecciones e Inversión", "Horizonte de 50 años · Ronda Semilla R$ 3,5M"),
        ],
        "sobre_titulo": "Sobre A1ELOS",
        "sobre_texto": "A1ELOS es una holding de tecnología y conocimiento que une inteligencia artificial, numerología aplicada y estrategia cultural para crear productos digitales de alto impacto a escala global. Nuestra misión: democratizar el autoconocimiento numérico con respeto cultural y respeto al poder adquisitivo de cada mercado.",
        "sobre_kpis": [
            ("23", "Productos Activos", "En 4 niveles de acceso"),
            ("14", "Idiomas", "~67% de la población mundial"),
            ("5,3B", "Hablantes", "Mercado direccionable real"),
            ("IA", "Integrada", "Motor de personalización"),
        ],
        "sobre_duns": "DUNS 942242668 — Certificación Dun & Bradstreet válida en más de 190 países, habilitando contratos B2B y joint ventures internacionales.",
        "duns_titulo": "Credibilidad Internacional",
        "duns_texto": "El número DUNS es el pasaporte corporativo de A1ELOS en el escenario internacional. Señala a socios, clientes corporativos e inversores que la empresa posee identidad verificable, historial trazable y capacidad contractual en cualquier jurisdicción.",
        "duns_numero": "942242668",
        "duns_emitido": "Emitido por Dun & Bradstreet — el estándar global de identidad empresarial reconocido en más de 190 países.",
        "duns_paises": "190+ PAÍSES",
        "duns_beneficios": [
            ("Contratos B2B", "Habilitación para licitaciones y proveedores globales"),
            ("Joint Ventures", "Asociaciones internacionales con due diligence facilitada"),
            ("Credibilidad Inmediata", "Señal de seriedad para inversores institucionales"),
        ],
        "mercado_titulo": "Oportunidad de Mercado",
        "mercado_texto": "Vivimos la convergencia perfecta: el bienestar digital explota globalmente mientras la numerología y la astrología migran a apps de alto compromiso. A1ELOS está posicionada exactamente en esa intersección, con el 74% de la población mundial ya en línea (~6 mil millones de personas).",
        "mercado_cards": [
            ("Bienestar Global", "US$ 6,8 billones → US$ 9,8 billones hasta 2029 (+7,6% a.a.)"),
            ("Apps Astrología/Numerología", "US$ 3 mil millones → US$ 9 mil millones hasta 2030 · CAGR 20%"),
            ("Apps de Bienestar", "CAGR 14,9% → US$ 26,2 mil millones en 2030"),
            ("Usuarios en Línea", "74% del mundo · ~6 mil millones de personas"),
        ],
        "problema_titulo": "El Problema que Resolvemos",
        "problema_col_esq_titulo": "Fallas del Mercado Actual",
        "problema_col_esq": [
            ("Barrera de Idioma", "La gran mayoría de las herramientas de numerología opera solo en inglés, excluyendo miles de millones de hablantes nativos en otros idiomas."),
            ("Precios Desconectados de la Realidad", "Productos cobrados en dólares para mercados emergentes generan exclusión económica — el usuario no rechaza el producto, rechaza el precio inaccesible."),
            ("Falta de Profundidad", "Herramientas genéricas entregan respuestas superficiales sin personalización, sin contexto cultural y sin aplicación práctica al día a día."),
        ],
        "problema_col_dir_titulo": "El Costo de la Exclusión",
        "problema_col_dir": "Cuando una plataforma ignora idioma y poder adquisitivo, abandona voluntariamente el mayor mercado del mundo: los más de 4 mil millones de personas que viven en economías emergentes y hablan idiomas no anglófonos. Ese es el vacío que A1ELOS ocupa con precisión quirúrgica.",
        "problema_destaque": "Las plataformas que ignoran el poder adquisitivo local pierden acceso a más del 60% del mercado direccionable global.",
        "solucao_titulo": "Nuestra Solución: 3 Pilares Estratégicos",
        "solucao_texto": "A1ELOS construyó una plataforma integrada que combina ciencia numérica, inteligencia artificial y sensibilidad cultural. La solución opera en tres frentes complementarios, garantizando ingresos diversificados y alta retención.",
        "solucao_colunas": [
            ("Mapas Personales", "Análisis numéricos profundos y personalizados para el usuario final — identidad, misión, ciclos de vida y compatibilidad — entregados en 14 idiomas con IA integrada."),
            ("Numerología Empresarial", "Diagnósticos numerológicos aplicados a marcas, CNPJ, fechas de fundación y estrategia corporativa. Producto diferenciado de alto valor percibido por el mercado B2B."),
            ("White-Label B2B", "Licenciamiento de la plataforma para empresas socias que deseen ofrecer numerología bajo su propia marca — con soporte multilingüe y personalización completa."),
        ],
        "alcance_titulo": "Alcance Global: 14 Idiomas · ~5,3 Mil Millones de Hablantes",
        "alcance_texto": "A1ELOS cubre ~67% de la población mundial con una plataforma genuinamente multilingüe. Cada idioma representa un mercado cultural distinto, con precios calibrados al poder adquisitivo local.",
        "mercados_titulo": "Los 3 Nuevos Mercados: +442 Millones de Hablantes",
        "mercados_texto": "La expansión estratégica hacia Indonesia, Turquía y Vietnam representa un salto cualitativo: mercados con alto crecimiento económico, penetración digital creciente y demanda comprobada de soluciones de bienestar digital accesibles.",
        "mercados_cards": [
            ("Indonesia", ["285 millones de habitantes", "80,5% de penetración de internet", "~255 millones de hablantes de indonesio", "Bienestar: US$ 51,2 mil millones (2025) → US$ 72,8 mil millones (2034)"]),
            ("Turquía", ["85,9 millones de habitantes", "PIB PPP per cápita US$ 37.301", "~90 millones de hablantes de turco", "Por encima del promedio mundial (US$ 27.211)"]),
            ("Vietnam",  ["~100 millones de habitantes", "PIB per cápita ~US$ 5.066 (+7,4%/año)", "~97 millones de hablantes de vietnamita", "Bienestar: US$ 303 millones (2025) → US$ 485 millones (2030)"]),
        ],
        "mercados_rodape": "3 mercados nuevos = +442 millones de nuevos hablantes direccionables — incorporados a la plataforma con precios culturalmente calibrados.",
        "preco_titulo": "Filosofía de Precio Consciente",
        "preco_esq": "Respeto cultural + respeto al poder adquisitivo = mercado direccionable real. Misma proporción de valor. Precios diferentes. Dignidad igual para todos los mercados.",
        "preco_dir_titulo": "Cómo Funciona en la Práctica",
        "preco_dir": "A1ELOS aplica la Paridad de Poder de Compra (PPC) como criterio central de precios. El mismo producto entrega el mismo valor relativo al usuario en Lagos, Yakarta, Hanói o Nueva York — el precio se calibra para que el esfuerzo financiero sea proporcional al ingreso local.",
        "preco_pilares": [
            ("Calibración por PPC", "Precios ajustados al índice de poder adquisitivo de cada país"),
            ("Respeto Cultural", "Idioma, moneda y contexto local integrados al producto"),
            ("Conversión Superior", "El precio justo genera más conversión y mayor retención a largo plazo"),
        ],
        "portfolio_titulo": "Portafolio: 23 Productos en 4 Niveles",
        "portfolio_texto": "La estructura en capas garantiza que cada perfil de usuario — del curioso al profesional — encuentre una oferta adecuada a su nivel de compromiso y capacidad financiera.",
        "portfolio_tabela": [
            ["Nivel", "Productos", "Rango de Precio (R$)", "Perfil"],
            ["Básico", "Mapa Express, Mapa Completo", "R$ 8 – 17", "Curioso, primer contacto"],
            ["Intermedio", "Búsqueda IA, Nombre de Urna, Nº Electoral", "R$ 26 – 53", "Usuario comprometido"],
            ["Avanzado", "Numerología Empresarial, Ciclos, Misión", "R$ 81 – 109", "Profesional, emprendedor"],
            ["Premium", "Diagnósticos Completos, Mapas Personales", "R$ 137 – 305", "Alta renta, uso corporativo"],
            ["B2B", "Paquetes empresariales, licencias, regalos", "Bajo consulta", "Empresas y equipos"],
        ],
        "portfolio_rodape": "23 productos cubren todo el recorrido del usuario, del primer contacto al cliente recurrente premium — maximizando el LTV por idioma y mercado.",
        "negocio_titulo": "Modelo de Negocio: 3 Fuentes de Ingresos",
        "negocio_texto": "A1ELOS fue diseñada con ingresos diversificados y escalables: ventas directas al consumidor final a escala global, contratos B2B de alto valor y publicidad geolocalizada recurrente — tres motores que se alimentan mutuamente.",
        "negocio_colunas": [
            ("B2C — 14 Idiomas", "Venta directa de productos digitales en todas las monedas, con precios adaptados por PPC. Escala automática vía IA — sin equipo de atención proporcional al crecimiento."),
            ("B2B — Descuentos Progresivos", "Paquetes corporativos para RRHH, employer branding y regalos institucionales. Descuentos del 10% al 50% según volumen. Por encima de 2.000 códigos, negociación directa (Plan Diamante). Contratos respaldados por el DUNS 942242668."),
            ("Publicidad Geolocalizada", "Banners segmentados por país, continente o mundial con rotación automatizada. Ingresos recurrentes mensuales de alto valor — sin dependencia del volumen de ventas de producto."),
        ],
        "banners_titulo": "Banners Publicitarios — Ingresos Mensuales Predecibles",
        "banners_texto": "La plataforma de publicidad geolocalizada de A1ELOS ofrece a los anunciantes segmentación precisa por país, continente o alcance global, con formatos optimizados para desktop y móvil y rotación automatizada cada 8 segundos.",
        "banners_tabela": [
            ["Segmentación", "Fijo (R$/mes)", "Temporal (R$/mes)", "Perfil del Anunciante"],
            ["País", "R$ 800", "R$ 500", "PYMES locales, comercio regional"],
            ["Continente", "R$ 1.800", "R$ 1.200", "Marcas regionales, expansión continental"],
            ["Mundo", "R$ 3.500", "R$ 2.500", "Empresas globales, apps internacionales"],
            ["Patrocinio Exclusivo", "R$ 6.000", "R$ 4.500/campaña", "Patrocinadores master, lanzamientos"],
        ],
        "banners_formatos": "728×90 px — Banner central desktop · 320×100 px — Formato móvil optimizado · 8 segundos — Rotación automática · Geo-objetivo — País, continente o alcance mundial",
        "b2b_titulo": "Paquetes Empresariales B2B — Alto Valor, Alto Volumen",
        "b2b_texto": "Los Paquetes B2B convierten a A1ELOS en una herramienta de employer branding y bienestar corporativo. Las empresas adquieren códigos de acceso en volumen para distribuir como regalos a colaboradores o clientes — respaldadas por el DUNS 942242668 para contratos corporativos formales.",
        "b2b_planos": [
            ("Plan Básico · 50 códigos", "50× Mapa Express (R$ 8 cada). Ideal para programas de beneficios a colaboradores y acciones de integración."),
            ("Plan Intermedio · 100 códigos", "50× Mapa Express + 50× Búsqueda IA (R$ 17). Perfecto para equipos y estrategia de marca empleadora."),
            ("Plan Premium · 200 códigos", "100× Mapa Express + 100× Mapa Completo (R$ 17). Máxima profundidad analítica para grandes grupos."),
        ],
        "b2b_tabela": [
            ["A partir de", "Descuento", "Perfil", "Uso Recomendado"],
            ["10 códigos", "10%", "Equipos pequeños", "Acción puntual de bienestar"],
            ["50 códigos", "20%", "Equipos en crecimiento", "Programas recurrentes"],
            ["100 códigos", "25%", "PYMES", "Beneficio trimestral"],
            ["200 códigos", "30%", "Empresas medianas", "Programas completos"],
            ["500 códigos", "40%", "Empresas medianas", "Regalo anual a colaboradores"],
            ["1.000 códigos", "45%", "Grandes corporaciones", "Fidelización de clientes"],
            ["2.000 códigos", "50%", "Grandes grupos", "Gran escala"],
            ["Más de 2.000", "Negociable", "Plan Diamante a medida", "Distribución de bonos en volumen"],
        ],
        "projecoes_titulo": "Proyecciones Financieras: Horizonte de 50 Años",
        "projecoes_texto": "Las proyecciones se construyeron con base en estimaciones porcentuales de penetración sobre el mercado potencial de ~5,32 mil millones de hablantes, con conversión conservadora del 3% y rescate de bonos entre el 70% y el 90%. La primera década se detalla en los años 1, 3, 5 y 7 para evidenciar el momentum.",
        "projecoes_tabela": [
            ["Horizonte", "Conservador (R$)", "Optimista (R$)"],
            ["Año 1", "R$ 281k", "R$ 702k"],
            ["Año 3", "R$ 983k", "R$ 2,8M"],
            ["Año 5", "R$ 2,8M", "R$ 7M"],
            ["Año 7", "R$ 5,6M", "R$ 14M"],
            ["Año 10", "R$ 11,2M", "R$ 28,1M"],
            ["Año 20", "R$ 42,1M", "R$ 112M"],
            ["Año 30", "R$ 84,3M", "R$ 211M"],
            ["Año 40", "R$ 126M", "R$ 351M"],
            ["Año 50", "R$ 169M", "R$ 492M"],
        ],
        "tracao_titulo": "Tracción y Resultados Comprobados",
        "tracao_texto": "A1ELOS ya opera con métricas de producto que validan el modelo — alta retención, evaluación premium y una base creciente de socios B2B demuestran que la plataforma entrega valor real al usuario final y al mercado corporativo.",
        "tracao_kpis": [
            ("12K+", "Usuarios Activos", "Base orgánica en crecimiento consistente"),
            ("87%", "Retención", "Muy por encima del promedio de la industria (~30%)"),
            ("4,8★", "Evaluación Media", "Satisfacción comprobada del usuario final"),
            ("23", "Socios B2B", "Contratos activos con empresas y RRHH"),
        ],
        "roteiro_titulo": "Hoja de Ruta Estratégica",
        "roteiro_texto": "A1ELOS ejecuta un plan en cuatro fases progresivas — de la consolidación de la base actual al liderazgo global de mercado, con opciones claras de salida para los inversores.",
        "roteiro_fases": [
            ("Fase 1 · Consolidación", "Fortalecimiento de la base de usuarios en los idiomas ya activos. Optimización de conversión, retención y LTV. Ronda Semilla concluida."),
            ("Fase 2 · Expansión", "Lanzamiento oficial en los 3 nuevos mercados: Indonesia, Turquía y Vietnam. Aceleración del canal B2B y publicidad geolocalizada."),
            ("Fase 3 · Entrada Global", "Presencia activa en los 14 idiomas con campañas localizadas. Alianzas white-label en más de 5 continentes. Serie A."),
            ("Fase 4 · Liderazgo", "Más de 20 países con operaciones consolidadas. Plataforma SaaS de referencia global en numerología aplicada. IPO o salida estratégica."),
        ],
        "invest_titulo": "Inversión y Contacto",
        "invest_texto": "Estamos listos para presentaciones privadas, due diligence y negociaciones. Contáctenos por el canal de su preferencia.",
        "invest_dados": [
            ("Ronda Semilla", "R$ 3,5 millones"),
            ("Valoración Pre-Money", "R$ 14 millones"),
            ("Equity Ofrecido", "Hasta 20%"),
        ],
        "invest_contato": [
            ("Email Inversores", "a1elos.consultoria@gmail.com"),
            ("Email General", "contato@a1elos.com"),
            ("Sitio Web", "www.a1elos.com"),
            ("DUNS", "942242668 — Dun & Bradstreet"),
        ],
        "invest_alocacao": "Asignación del Capital: 45% Tecnología · 30% Marketing · 25% Operaciones",
        "frase_final": "Los números nunca mienten.",
        "selo_final": ["DUNS 942242668", "23 PRODUCTOS", "14 IDIOMAS", "~5,3 MIL MILLONES DE HABLANTES"],
        "graf_cons": "Conservador",
        "graf_otim": "Optimista",
        "grafico_titulo_linha": "Crecimiento Proyectado (R$ mil)",
        "pix_titulo": "Brasil: La Infraestructura Pix",
        "pix_texto": "Pix es la infraestructura pública de pagos instantáneos de Brasil. Para A1ELOS, garantiza cobro inmediato, bajo costo y aceptación universal — el fundamento de la operación B2C en el mercado brasileño y la puerta de entrada a la expansión internacional.",
        "pix_kpis": [
            ("30,1 mil millones", "Transacciones en 2025", "+20% vs 2024 · Febraban"),
            ("76,4%", "de la población usa Pix", "211 millones de brasileños · Banco Central"),
            ("R$ 68,2 billones", "movilizados en el 2º sem. 2025", "78,4 mil millones de transacciones · Banco Central"),
            ("~80 mil millones", "transacciones en 2025", "+25,7% vs año anterior · Informe Pix"),
        ],
        "pix_fonte": "Fuentes: Banco Central de Brasil (Pix en Números) y Febraban (Encuesta de Tecnología Bancaria).",
        "ref_titulo": "Referencias Bibliográficas",
        "ref_intro": "Fuentes utilizadas para los datos de mercado, proyecciones e indicadores de esta presentación.",
        "ref_lista": [
            ("Global Wellness Institute", "Economía global del bienestar: US$ 6,8 billones (2024) → US$ 9,8 billones (2029)."),
            ("MarkNtel Advisors", "Apps de astrología y numerología: US$ 3 mil millones → US$ 9 mil millones hasta 2030 (CAGR ~20%)."),
            ("FMI · Banco Mundial", "PIB y paridad del poder de compra (PPP) por país."),
            ("Banco Central de Brasil", "Estadísticas oficiales del Pix: transacciones, volumen y usuarios."),
            ("Febraban", "Encuesta de Tecnología Bancaria — crecimiento del Pix en 2025."),
            ("IBGE", "Población e indicadores socioeconómicos de Brasil."),
        ],
        },

"it": {
        "titulo": "A1ELOS Global Numerology",
        "subtitulo": "La scienza dei numeri applicata al tuo successo",
        "capa_nota": "Presentazione Strategica per Investitori e Partner",
        "confidencial": "CONFIDENZIALE",
        "ano": "2026",
        "sumario_titulo": "Sintesi Esecutiva",
        "duns_porque": "Perché il DUNS è importante?",
        "preco_consciente": "Prezzo Consapevole",
        "idioma_col": "Lingua",
        "falantes_col": "Parlanti (M)",
        "linhas_idiomas": [
           ["Inglese", "1.528"],
           ["Mandarino", "1.184"],
           ["Spagnolo", "558"],
           ["Francese", "396"],
           ["Arabo", "335"],
           ["Portoghese", "270"],
           ["Russo", "255"],
           ["Indonesiano", "255"],
           ["Tedesco", "134"],
           ["Giapponese", "123"],
           ["Vietnamita", "97"],
           ["Turco", "90"],
           ["Italiano", "85"],
           ["Ebraico", "9"],
        ],
        "total_linha": "TOTALE",
        "fonte_receita": "Fonte di Reddito",
        "participacao": "Partecipazione",
        "b2c_linha": "B2C — 14 Lingue",
        "b2b_linha": "B2B — Sconti Progressivi",
        "pub_linha": "Pubblicità Geolocalizzata",
        "tabela_descontos": "Tabella degli Sconti Progressivi",
        "grafico_anos": ["Anno 1", "Anno 3", "Anno 5", "Anno 7", "Anno 10"],
        "grafico_titulo": "Proiezione Conservativa (R$ migliaia)",
        "grafico_titulo_linha": "Crescita Proiettata (R$ migliaia)",
        "fale_conosco": "Contattaci",
        "sumario_intro": "Questa presentazione è strutturata per guidare investitori e partner attraverso tutti gli aspetti strategici di A1ELOS Global Numerology — dalla tesi di mercato al modello di reddito ricorrente.",
        "sumario_cards": [
            ("01", "Chi è A1ELOS", "Holding, portafoglio e credenziale DUNS"),
            ("02", "Opportunità di Mercato", "Economia globale del benessere 6,8 trilioni USD"),
            ("03", "Soluzione e Portata Globale", "14 lingue, ~5,3 miliardi di parlanti"),
            ("04", "3 Nuovi Mercati", "Indonesia, Turchia e Vietnam"),
            ("05", "Portafoglio e Prezzi", "23 prodotti calibrati per potere d'acquisto"),
            ("06", "Reddito Ricorrente", "Banner pubblicitari e Pacchetti B2B"),
            ("07", "Proiezioni e Investimento", "Orizzonte di 50 anni · Round Seed R$ 3,5M"),
        ],
        "sobre_titulo": "Chi è A1ELOS",
        "sobre_texto": "A1ELOS è una holding di tecnologia e conoscenza che unisce intelligenza artificiale, numerologia applicata e strategia culturale per creare prodotti digitali ad alto impatto su scala globale. La nostra missione: democratizzare la conoscenza di sé numerica con rispetto culturale e rispetto del potere d'acquisto di ogni mercato.",
        "sobre_kpis": [
            ("23", "Prodotti Attivi", "In 4 livelli di accesso"),
            ("14", "Lingue", "~67% della popolazione mondiale"),
            ("5,3B", "Parlanti", "Mercato indirizzabile reale"),
            ("IA", "Integrata", "Motore di personalizzazione"),
        ],
        "sobre_duns": "DUNS 942242668 — Certificazione Dun & Bradstreet valida in oltre 190 paesi, abilitando contratti B2B e joint venture internazionali.",
        "duns_titulo": "Credibilità Internazionale",
        "duns_texto": "Il numero DUNS è il passaporto aziendale di A1ELOS sulla scena internazionale. Segnala a partner, clienti aziendali e investitori che l'azienda possiede identità verificabile, storia tracciabile e capacità contrattuale in qualsiasi giurisdizione.",
        "duns_numero": "942242668",
        "duns_emitido": "Emesso da Dun & Bradstreet — lo standard globale di identità aziendale riconosciuto in più di 190 paesi.",
        "duns_paises": "190+ PAESI",
        "duns_beneficios": [
            ("Contratti B2B", "Abilitazione per gare d'appalto e fornitori globali"),
            ("Joint Venture", "Partnership internazionali con due diligence facilitata"),
            ("Credibilità Immediata", "Segno di serietà per gli investitori istituzionali"),
        ],
        "mercado_titulo": "Opportunità di Mercato",
        "mercado_texto": "Viviamo la convergenza perfetta: il benessere digitale esplode a livello globale mentre la numerologia e l'astrologia migrano verso app ad alto coinvolgimento. A1ELOS è posizionata esattamente in questa intersezione, con il 74% della popolazione mondiale già online (~6 miliardi di persone).",
        "mercado_cards": [
            ("Benessere Globale", "6,8 trilioni USD → 9,8 trilioni USD entro il 2029 (+7,6% p.a.)"),
            ("App Astrologia/Numerologia", "3 miliardi USD → 9 miliardi USD entro il 2030 · CAGR 20%"),
            ("App di Benessere", "CAGR 14,9% → 26,2 miliardi USD nel 2030"),
            ("Utenti Online", "74% del mondo · ~6 miliardi di persone"),
        ],
        "problema_titulo": "Il Problema che Risolviamo",
        "problema_col_esq_titulo": "Fallimenti del Mercato Attuale",
        "problema_col_esq": [
            ("Barriera Linguistica", "La stragrande maggioranza degli strumenti di numerologia funziona solo in inglese, escludendo miliardi di parlanti nativi in altre lingue."),
            ("Prezzi Scollegati dalla Realtà", "Prodotti venduti in dollari per i mercati emergenti generano esclusione economica — l'utente non rifiuta il prodotto, rifiuta il prezzo inaccessibile."),
            ("Mancanza di Profondità", "Gli strumenti generici forniscono risposte superficiali senza personalizzazione, senza contesto culturale e senza applicazione pratica alla vita quotidiana."),
        ],
        "problema_col_dir_titulo": "Il Costo dell'Esclusione",
        "problema_col_dir": "Quando una piattaforma ignora lingua e potere d'acquisto, abbandona volontariamente il più grande mercato del mondo: i oltre 4 miliardi di persone che vivono in economie emergenti e parlano lingue non anglofone. Questo è lo spazio che A1ELOS occupa con precisione chirurgica.",
        "problema_destaque": "Le piattaforme che ignorano il potere d'acquisto locale perdono l'accesso a più del 60% del mercato indirizzabile globale.",
        "solucao_titulo": "La Nostra Soluzione: 3 Pilastri Strategici",
        "solucao_texto": "A1ELOS ha costruito una piattaforma integrata che combina scienza numerica, intelligenza artificiale e sensibilità culturale. La soluzione opera su tre fronti complementari, garantendo redditi diversificati e alta fidelizzazione.",
        "solucao_colunas": [
            ("Mappe Personali", "Analisi numeriche profonde e personalizzate per l'utente finale — identità, missione, cicli di vita e compatibilità — consegnate in 14 lingue con IA integrata."),
            ("Numerologia Aziendale", "Diagnosi numerologiche applicate a marchi, CNPJ, date di fondazione e strategia aziendale. Prodotto differenziato di alto valore percepito per il mercato B2B."),
            ("White-Label B2B", "Licenza della piattaforma per aziende partner che desiderano offrire numerologia sotto il proprio marchio — con supporto multilingue e personalizzazione completa."),
        ],
        "alcance_titulo": "Portata Globale: 14 Lingue · ~5,3 Miliardi di Parlanti",
        "alcance_texto": "A1ELOS copre ~67% della popolazione mondiale con una piattaforma autenticamente multilingue. Ogni lingua rappresenta un mercato culturale distinto, con prezzi calibrati al potere d'acquisto locale.",
        "mercados_titulo": "I 3 Nuovi Mercati: +442 Milioni di Parlanti",
        "mercados_texto": "L'espansione strategica verso Indonesia, Turchia e Vietnam rappresenta un salto qualitativo: mercati ad alta crescita economica, penetrazione digitale crescente e domanda comprovata di soluzioni di benessere digitale accessibili.",
        "mercados_cards": [
            ("Indonesia", ["285 milioni di abitanti", "80,5% di penetrazione internet", "~255 milioni di parlanti indonesiani", "Benessere: 51,2 miliardi USD (2025) → 72,8 miliardi USD (2034)"]),
            ("Turchia", ["85,9 milioni di abitanti", "PIL PPP pro capite 37.301 USD", "~90 milioni di parlanti turchi", "Sopra la media mondiale (27.211 USD)"]),
            ("Vietnam",  ["~100 milioni di abitanti", "PIL pro capite ~5.066 USD (+7,4%/anno)", "~97 milioni di parlanti vietnamiti", "Benessere: 303 milioni USD (2025) → 485 milioni USD (2030)"]),
        ],
        "mercados_rodape": "3 nuovi mercati = +442 milioni di nuovi parlanti indirizzabili — integrati nella piattaforma con prezzi culturalmente calibrati.",
        "preco_titulo": "Filosofia del Prezzo Consapevole",
        "preco_esq": "Rispetto culturale + rispetto del potere d'acquisto = mercato indirizzabile reale. Stessa proporzione di valore. Prezzi diversi. Dignità uguale per tutti i mercati.",
        "preco_dir_titulo": "Come Funziona in Pratica",
        "preco_dir": "A1ELOS applica la Parità di Potere d'Acquisto (PPA) come criterio centrale di prezzo. Lo stesso prodotto consegna lo stesso valore relativo all'utente a Lagos, Giacarta, Hanoi o New York — il prezzo è calibrato affinché lo sforzo finanziario sia proporzionale al reddito locale.",
        "preco_pilares": [
            ("Calibrazione per PPA", "Prezzi adeguati all'indice di potere d'acquisto di ogni paese"),
            ("Rispetto Culturale", "Lingua, valuta e contesto locale integrati nel prodotto"),
            ("Conversione Superiore", "Un prezzo giusto genera più conversione e maggiore fidelizzazione a lungo termine"),
        ],
        "portfolio_titulo": "Portafoglio: 23 Prodotti in 4 Livelli",
        "portfolio_texto": "La struttura a strati garantisce che ogni profilo di utente — dal curioso al professionista — trovi un'offerta adeguata al proprio livello di coinvolgimento e capacità finanziaria.",
        "portfolio_tabela": [
            ["Livello", "Prodotti", "Fascia di Prezzo (R$)", "Profilo"],
            ["Base", "Mappa Express, Mappa Completa", "R$ 8 – 17", "Curioso, primo contatto"],
            ["Intermedio", "Ricerca IA, Nome di Urna, Nº Elettorale", "R$ 26 – 53", "Utente coinvolto"],
            ["Avanzato", "Numerologia Aziendale, Cicli, Missione", "R$ 81 – 109", "Professionista, imprenditore"],
            ["Premium", "Diagnosi Complete, Mappe Personali", "R$ 137 – 305", "Alto reddito, uso aziendale"],
            ["B2B", "Pacchetti aziendali, licenze, regali", "Su richiesta", "Aziende e team"],
        ],
        "portfolio_rodape": "23 prodotti coprono l'intero percorso dell'utente, dal primo contatto al cliente ricorrente premium — massimizzando il LTV per lingua e mercato.",
        "negocio_titulo": "Modello di Business: 3 Fonti di Reddito",
        "negocio_texto": "A1ELOS è stata progettata con redditi diversificati e scalabili: vendite dirette al consumatore finale su scala globale, contratti B2B ad alto valore e pubblicità geolocalizzata ricorrente — tre motori che si alimentano a vicenda.",
        "negocio_colunas": [
            ("B2C — 14 Lingue", "Vendita diretta di prodotti digitali in tutte le valute, con prezzi adattati per PPA. Scala automatica via IA — senza team di assistenza proporzionale alla crescita."),
            ("B2B — Sconti Progressivi", "Pacchetti aziendali per HR, employer branding e regali istituzionali. Sconti dal 10% al 50% in base al volume. Oltre 2.000 codici, negoziazione diretta (Piano Diamante). Contratti sostenuti dal DUNS 942242668."),
            ("Pubblicità Geolocalizzata", "Banner segmentati per paese, continente o mondo con rotazione automatizzata. Reddito ricorrente mensile ad alto valore — senza dipendenza dal volume di vendita dei prodotti."),
        ],
        "banners_titulo": "Banner Pubblicitari — Reddito Mensile Prevedibile",
        "banners_texto": "La piattaforma pubblicitaria geolocalizzata di A1ELOS offre agli inserzionisti una segmentazione precisa per paese, continente o portata globale, con formati ottimizzati per desktop e mobile e rotazione automatizzata ogni 8 secondi.",
        "banners_tabela": [
            ["Segmentazione", "Fisso (R$/mese)", "Temporaneo (R$/mese)", "Profilo dell'Inserzionista"],
            ["Paese", "R$ 800", "R$ 500", "PMI locali, commercio regionale"],
            ["Continente", "R$ 1.800", "R$ 1.200", "Marchi regionali, espansione continentale"],
            ["Mondo", "R$ 3.500", "R$ 2.500", "Aziende globali, app internazionali"],
            ["Sponsorizzazione Esclusiva", "R$ 6.000", "R$ 4.500/campagna", "Sponsor master, lanci"],
        ],
        "banners_formatos": "728×90 px — Banner centrale desktop · 320×100 px — Formato mobile ottimizzato · 8 secondi — Rotazione automatica · Geo-target — Paese, continente o portata mondiale",
        "b2b_titulo": "Pacchetti Aziendali B2B — Alto Valore, Alto Volume",
        "b2b_texto": "I Pacchetti B2B trasformano A1ELOS in uno strumento di employer branding e benessere aziendale. Le aziende acquistano codici di accesso in volume per distribuirli come regali a collaboratori o clienti — sostenute dal DUNS 942242668 per contratti aziendali formali.",
        "b2b_planos": [
            ("Piano Base · 50 codici", "50× Mappa Express (R$ 8 ciascuno). Ideale per programmi di benefit ai collaboratori e azioni di integrazione."),
            ("Piano Intermedio · 100 codici", "50× Mappa Express + 50× Ricerca IA (R$ 17). Perfetto per team e strategia di employer branding."),
            ("Piano Premium · 200 codici", "100× Mappa Express + 100× Mappa Completa (R$ 17). Massima profondità analitica per grandi gruppi."),
        ],
        "b2b_tabela": [
            ["Da", "Sconto", "Profilo", "Uso Consigliato"],
            ["10 codici", "10%", "Piccoli team", "Azione puntuale di benessere"],
            ["50 codici", "20%", "Team in crescita", "Programmi ricorrenti"],
            ["100 codici", "25%", "PMI", "Benefit trimestrale"],
            ["200 codici", "30%", "Aziende medie", "Programmi completi"],
            ["500 codici", "40%", "Aziende medie", "Regalo annuale ai collaboratori"],
            ["1.000 codici", "45%", "Grandi aziende", "Fidelizzazione dei clienti"],
            ["2.000 codici", "50%", "Grandi gruppi", "Grande scala"],
            ["Oltre 2.000", "Negoziabile", "Piano Diamante su misura", "Distribuzione di bonus in volume"],
        ],
        "projecoes_titulo": "Proiezioni Finanziarie: Orizzonte di 50 Anni",
        "projecoes_texto": "Le proiezioni sono state costruite sulla base di stime percentuali di penetrazione del mercato potenziale di ~5,32 miliardi di parlanti, con conversione conservativa del 3% e riscatto dei bonus tra il 70% e il 90%. Il primo decennio è dettagliato negli anni 1, 3, 5 e 7 per evidenziare il momentum.",
        "projecoes_tabela": [
            ["Orizzonte", "Conservativo (R$)", "Ottimista (R$)"],
            ["Anno 1", "R$ 281k", "R$ 702k"],
            ["Anno 3", "R$ 983k", "R$ 2,8M"],
            ["Anno 5", "R$ 2,8M", "R$ 7M"],
            ["Anno 7", "R$ 5,6M", "R$ 14M"],
            ["Anno 10", "R$ 11,2M", "R$ 28,1M"],
            ["Anno 20", "R$ 42,1M", "R$ 112M"],
            ["Anno 30", "R$ 84,3M", "R$ 211M"],
            ["Anno 40", "R$ 126M", "R$ 351M"],
            ["Anno 50", "R$ 169M", "R$ 492M"],
        ],
        "tracao_titulo": "Trazione e Risultati Comprovati",
        "tracao_texto": "A1ELOS opera già con metriche di prodotto che validano il modello — alta fidelizzazione, valutazione premium e una base crescente di partner B2B dimostrano che la piattaforma consegna valore reale all'utente finale e al mercato aziendale.",
        "tracao_kpis": [
            ("12K+", "Utenti Attivi", "Base organica in crescita costante"),
            ("87%", "Fidelizzazione", "Molto sopra la media del settore (~30%)"),
            ("4,8★", "Valutazione Media", "Soddisfazione comprovata dell'utente finale"),
            ("23", "Partner B2B", "Contratti attivi con aziende e HR"),
        ],
        "roteiro_titulo": "Roadmap Strategica",
        "roteiro_texto": "A1ELOS esegue un piano in quattro fasi progressive — dalla consolidazione della base attuale alla leadership globale di mercato, con chiare opzioni di uscita per gli investitori.",
        "roteiro_fases": [
            ("Fase 1 · Consolidazione", "Rafforzamento della base utenti nelle lingue già attive. Ottimizzazione di conversione, fidelizzazione e LTV. Round Seed concluso."),
            ("Fase 2 · Espansione", "Lancio ufficiale nei 3 nuovi mercati: Indonesia, Turchia e Vietnam. Accelerazione del canale B2B e della pubblicità geolocalizzata."),
            ("Fase 3 · Ingresso Globale", "Presenza attiva in tutte le 14 lingue con campagne localizzate. Partnership white-label in oltre 5 continenti. Serie A."),
            ("Fase 4 · Leadership", "Oltre 20 paesi con operazioni consolidate. Piattaforma SaaS di riferimento globale in numerologia applicata. IPO o uscita strategica."),
        ],
        "invest_titulo": "Investimento e Contatto",
        "invest_texto": "Siamo pronti per presentazioni private, due diligence e negoziazioni. Contattaci attraverso il canale di tua preferenza.",
        "invest_dados": [
            ("Round Seed", "R$ 3,5 milioni"),
            ("Valutazione Pre-Money", "R$ 14 milioni"),
            ("Equity Offerto", "Fino al 20%"),
        ],
        "invest_contato": [
            ("Email Investitori", "a1elos.consultoria@gmail.com"),
            ("Email Generale", "contato@a1elos.com"),
            ("Sito Web", "www.a1elos.com"),
            ("DUNS", "942242668 — Dun & Bradstreet"),
        ],
        "invest_alocacao": "Allocazione del Capitale: 45% Tecnologia · 30% Marketing · 25% Operazioni",
        "frase_final": "I numeri non mentono mai.",
        "selo_final": ["DUNS 942242668", "23 PRODOTTI", "14 LINGUE", "~5,3 MILIARDI DI PARLANTI"],
        "graf_cons": "Conservativo",
        "graf_otim": "Ottimista",
        "grafico_titulo_linha": "Crescita Proiettata (R$ migliaia)",
        "pix_titulo": "Brasile: L'Infrastruttura Pix",
        "pix_texto": "Pix è l'infrastruttura pubblica di pagamenti istantanei del Brasile. Per A1ELOS, garantisce incasso immediato, basso costo e accettazione universale — il fondamento dell'operazione B2C nel mercato brasiliano e la porta d'ingresso per l'espansione internazionale.",
        "pix_kpis": [
            ("30,1 miliardi", "Transazioni nel 2025", "+20% vs 2024 · Febraban"),
            ("76,4%", "della popolazione usa Pix", "211 milioni di brasiliani · Banca Centrale"),
            ("R$ 68,2 trilioni", "movimentati nel 2º sem. 2025", "78,4 miliardi di transazioni · Banca Centrale"),
            ("~80 miliardi", "transazioni nel 2025", "+25,7% vs anno precedente · Rapporto Pix"),
        ],
        "pix_fonte": "Fonti: Banca Centrale del Brasile (Pix in Numeri) e Febraban (Indagine sulla Tecnologia Bancaria).",
        "ref_titulo": "Riferimenti Bibliografici",
        "ref_intro": "Fonti utilizzate per i dati di mercato, le proiezioni e gli indicatori di questa presentazione.",
        "ref_lista": [
            ("Global Wellness Institute", "Economia globale del benessere: 6,8 trilioni USD (2024) → 9,8 trilioni USD (2029)."),
            ("MarkNtel Advisors", "App di astrologia e numerologia: 3 miliardi USD → 9 miliardi USD entro il 2030 (CAGR ~20%)."),
            ("FMI · Banca Mondiale", "PIL e parità del potere d'acquisto (PPA) per paese."),
            ("Banca Centrale del Brasile", "Statistiche ufficiali del Pix: transazioni, volume e utenti."),
            ("Febraban", "Indagine sulla Tecnologia Bancaria — crescita del Pix nel 2025."),
            ("IBGE", "Popolazione e indicatori socioeconomici del Brasile."),
        ],
        },
           
"fr": {
        "titulo": "A1ELOS Global Numerology",
        "subtitulo": "La science des nombres appliquée à votre succès",
        "capa_nota": "Présentation Stratégique pour Investisseurs et Partenaires",
        "confidencial": "CONFIDENTIEL",
        "ano": "2026",
        "sumario_titulo": "Résumé Exécutif",
        "duns_porque": "Pourquoi le DUNS est-il important ?",
        "preco_consciente": "Prix Conscient",
        "idioma_col": "Langue",
        "falantes_col": "Locuteurs (M)",
        "linhas_idiomas": [
           ["Anglais", "1.528"],
           ["Mandarin", "1.184"],
           ["Espagnol", "558"],
           ["Français", "396"],
           ["Arabe", "335"],
           ["Portugais", "270"],
           ["Russe", "255"],
           ["Indonésien", "255"],
           ["Allemand", "134"],
           ["Japonais", "123"],
           ["Vietnamien", "97"],
           ["Turc", "90"],
           ["Italien", "85"],
           ["Hébreu", "9"],
        ],
        "total_linha": "TOTAL",
        "fonte_receita": "Source de Revenus",
        "participacao": "Participation",
        "b2c_linha": "B2C — 14 Langues",
        "b2b_linha": "B2B — Remises Progressives",
        "pub_linha": "Publicité Géolocalisée",
        "tabela_descontos": "Tableau des Remises Progressives",
        "grafico_anos": ["Année 1", "Année 3", "Année 5", "Année 7", "Année 10"],
        "grafico_titulo": "Projection Conservatrice (R$ milliers)",
        "grafico_titulo_linha": "Croissance Projetée (R$ milliers)",
        "fale_conosco": "Contactez-nous",
        "sumario_intro": "Cette présentation est structurée pour guider les investisseurs et partenaires à travers tous les aspects stratégiques d'A1ELOS Global Numerology — de la thèse de marché au modèle de revenus récurrents.",
        "sumario_cards": [
            ("01", "À propos d'A1ELOS", "Holding, portefeuille et accréditation DUNS"),
            ("02", "Opportunité de Marché", "Économie mondiale du bien-être 6,8 billions USD"),
            ("03", "Solution et Portée Mondiale", "14 langues, ~5,3 milliards de locuteurs"),
            ("04", "3 Nouveaux Marchés", "Indonésie, Turquie et Vietnam"),
            ("05", "Portefeuille et Tarifs", "23 produits calibrés par pouvoir d'achat"),
            ("06", "Revenus Récurrents", "Bannières publicitaires et Forfaits B2B"),
            ("07", "Projections et Investissement", "Horizon de 50 ans · Tour d'amorçage R$ 3,5M"),
        ],
        "sobre_titulo": "À propos d'A1ELOS",
        "sobre_texto": "A1ELOS est une holding de technologie et de connaissance qui unit intelligence artificielle, numérologie appliquée et stratégie culturelle pour créer des produits numériques à fort impact à l'échelle mondiale. Notre mission : démocratiser la connaissance de soi numérique avec respect culturel et respect du pouvoir d'achat de chaque marché.",
        "sobre_kpis": [
            ("23", "Produits Actifs", "En 4 niveaux d'accès"),
            ("14", "Langues", "~67% de la population mondiale"),
            ("5,3B", "Locuteurs", "Marché adressable réel"),
            ("IA", "Intégrée", "Moteur de personnalisation"),
        ],
        "sobre_duns": "DUNS 942242668 — Certification Dun & Bradstreet valable dans plus de 190 pays, permettant des contrats B2B et des joint ventures internationales.",
        "duns_titulo": "Crédibilité Internationale",
        "duns_texto": "Le numéro DUNS est le passeport corporatif d'A1ELOS sur la scène internationale. Il signale aux partenaires, clients corporatifs et investisseurs que l'entreprise possède une identité vérifiable, un historique traçable et une capacité contractuelle dans toute juridiction.",
        "duns_numero": "942242668",
        "duns_emitido": "Émis par Dun & Bradstreet — la norme mondiale d'identité d'entreprise reconnue dans plus de 190 pays.",
        "duns_paises": "190+ PAYS",
        "duns_beneficios": [
            ("Contrats B2B", "Habilitation pour appels d'offres et fournisseurs mondiaux"),
            ("Joint Ventures", "Partenariats internationaux avec due diligence facilitée"),
            ("Crédibilité Immédiate", "Signe de sérieux pour les investisseurs institutionnels"),
        ],
        "mercado_titulo": "Opportunité de Marché",
        "mercado_texto": "Nous vivons la convergence parfaite : le bien-être numérique explose à l'échelle mondiale tandis que la numérologie et l'astrologie migrent vers des applications à fort engagement. A1ELOS est positionnée exactement à cette intersection, avec 74% de la population mondiale déjà en ligne (~6 milliards de personnes).",
        "mercado_cards": [
            ("Bien-Être Mondial", "6,8 billions USD → 9,8 billions USD d'ici 2029 (+7,6% p.a.)"),
            ("Apps Astrologie/Numérologie", "3 milliards USD → 9 milliards USD d'ici 2030 · CAGR 20%"),
            ("Apps de Bien-Être", "CAGR 14,9% → 26,2 milliards USD en 2030"),
            ("Utilisateurs en Ligne", "74% du monde · ~6 milliards de personnes"),
        ],
        "problema_titulo": "Le Problème que Nous Résolvons",
        "problema_col_esq_titulo": "Défaillances du Marché Actuel",
        "problema_col_esq": [
            ("Barrière de Langue", "La grande majorité des outils de numérologie fonctionne uniquement en anglais, excluant des milliards de locuteurs natifs dans d'autres langues."),
            ("Prix Déconnectés de la Réalité", "Des produits facturés en dollars pour les marchés émergents génèrent une exclusion économique — l'utilisateur ne rejette pas le produit, il rejette le prix inaccessible."),
            ("Manque de Profondeur", "Les outils génériques livrent des réponses superficielles sans personnalisation, sans contexte culturel et sans application pratique au quotidien."),
        ],
        "problema_col_dir_titulo": "Le Coût de l'Exclusion",
        "problema_col_dir": "Quand une plateforme ignore la langue et le pouvoir d'achat, elle abandonne volontairement le plus grand marché du monde : les plus de 4 milliards de personnes qui vivent dans des économies émergentes et parlent des langues non anglophones. C'est l'espace qu'A1ELOS occupe avec précision chirurgicale.",
        "problema_destaque": "Les plateformes qui ignorent le pouvoir d'achat local perdent accès à plus de 60% du marché adressable mondial.",
        "solucao_titulo": "Notre Solution : 3 Piliers Stratégiques",
        "solucao_texto": "A1ELOS a construit une plateforme intégrée qui combine science numérique, intelligence artificielle et sensibilité culturelle. La solution opère sur trois fronts complémentaires, garantissant des revenus diversifiés et une forte rétention.",
        "solucao_colunas": [
            ("Cartes Personnelles", "Analyses numériques profondes et personnalisées pour l'utilisateur final — identité, mission, cycles de vie et compatibilité — livrées en 14 langues avec IA intégrée."),
            ("Numérologie d'Entreprise", "Diagnostics numérologiques appliqués aux marques, CNPJ, dates de fondation et stratégie corporative. Produit différencié de haute valeur perçue pour le marché B2B."),
            ("White-Label B2B", "Licence de la plateforme pour les entreprises partenaires souhaitant offrir la numérologie sous leur propre marque — avec support multilingue et personnalisation complète."),
        ],
        "alcance_titulo": "Portée Mondiale : 14 Langues · ~5,3 Milliards de Locuteurs",
        "alcance_texto": "A1ELOS couvre ~67% de la population mondiale avec une plateforme authentiquement multilingue. Chaque langue représente un marché culturel distinct, avec des prix calibrés au pouvoir d'achat local.",
        "mercados_titulo": "Les 3 Nouveaux Marchés : +442 Millions de Locuteurs",
        "mercados_texto": "L'expansion stratégique vers l'Indonésie, la Turquie et le Vietnam représente un saut qualitatif : des marchés à forte croissance économique, une pénétration numérique croissante et une demande prouvée de solutions de bien-être numérique accessibles.",
        "mercados_cards": [
            ("Indonésie", ["285 millions d'habitants", "80,5% de pénétration internet", "~255 millions de locuteurs indonésiens", "Bien-être : 51,2 milliards USD (2025) → 72,8 milliards USD (2034)"]),
            ("Turquie", ["85,9 millions d'habitants", "PIB PPP par habitant 37.301 USD", "~90 millions de locuteurs turcs", "Au-dessus de la moyenne mondiale (27.211 USD)"]),
            ("Vietnam",  ["~100 millions d'habitants", "PIB par habitant ~5.066 USD (+7,4%/an)", "~97 millions de locuteurs vietnamiens", "Bien-être : 303 millions USD (2025) → 485 millions USD (2030)"]),
        ],
        "mercados_rodape": "3 nouveaux marchés = +442 millions de nouveaux locuteurs adressables — intégrés à la plateforme avec des prix culturellement calibrés.",
        "preco_titulo": "Philosophie du Prix Conscient",
        "preco_esq": "Respect culturel + respect du pouvoir d'achat = marché adressable réel. Même proportion de valeur. Prix différents. Dignité égale pour tous les marchés.",
        "preco_dir_titulo": "Comment Ça Fonctionne en Pratique",
        "preco_dir": "A1ELOS applique la Parité de Pouvoir d'Achat (PPA) comme critère central de tarification. Le même produit livre la même valeur relative à l'utilisateur à Lagos, Jakarta, Hanoï ou New York — le prix est calibré pour que l'effort financier soit proportionnel au revenu local.",
        "preco_pilares": [
            ("Calibrage par PPA", "Prix ajustés à l'indice de pouvoir d'achat de chaque pays"),
            ("Respect Culturel", "Langue, monnaie et contexte local intégrés au produit"),
            ("Conversion Supérieure", "Un prix juste génère plus de conversion et une plus grande rétention à long terme"),
        ],
        "portfolio_titulo": "Portefeuille : 23 Produits en 4 Niveaux",
        "portfolio_texto": "La structure en couches garantit que chaque profil d'utilisateur — du curieux au professionnel — trouve une offre adaptée à son niveau d'engagement et à sa capacité financière.",
        "portfolio_tabela": [
            ["Niveau", "Produits", "Gamme de Prix (R$)", "Profil"],
            ["Basique", "Carte Express, Carte Complète", "R$ 8 – 17", "Curieux, premier contact"],
            ["Intermédiaire", "Recherche IA, Nom d'Urne, Nº Électoral", "R$ 26 – 53", "Utilisateur engagé"],
            ["Avancé", "Numérologie d'Entreprise, Cycles, Mission", "R$ 81 – 109", "Professionnel, entrepreneur"],
            ["Premium", "Diagnostics Complets, Cartes Personnelles", "R$ 137 – 305", "Hauts revenus, usage corporatif"],
            ["B2B", "Forfaits d'entreprise, licences, cadeaux", "Sur demande", "Entreprises et équipes"],
        ],
        "portfolio_rodape": "23 produits couvrent tout le parcours de l'utilisateur, du premier contact au client récurrent premium — maximisant le LTV par langue et par marché.",
        "negocio_titulo": "Modèle d'Affaires : 3 Sources de Revenus",
        "negocio_texto": "A1ELOS a été conçue avec des revenus diversifiés et évolutifs : ventes directes au consommateur final à l'échelle mondiale, contrats B2B à haute valeur et publicité géolocalisée récurrente — trois moteurs qui s'alimentent mutuellement.",
        "negocio_colunas": [
            ("B2C — 14 Langues", "Vente directe de produits numériques dans toutes les monnaies, avec des prix adaptés par PPA. Échelle automatique via IA — sans équipe de service proportionnelle à la croissance."),
            ("B2B — Remises Progressives", "Forfaits corporatifs pour RH, employer branding et cadeaux institutionnels. Remises de 10% à 50% selon le volume. Au-delà de 2.000 codes, négociation directe (Plan Diamant). Contrats soutenus par le DUNS 942242668."),
            ("Publicité Géolocalisée", "Bannières segmentées par pays, continent ou monde avec rotation automatisée. Revenus récurrents mensuels à haute valeur — sans dépendance au volume de ventes de produit."),
        ],
        "banners_titulo": "Bannières Publicitaires — Revenus Mensuels Prévisibles",
        "banners_texto": "La plateforme de publicité géolocalisée d'A1ELOS offre aux annonceurs une segmentation précise par pays, continent ou portée mondiale, avec des formats optimisés pour desktop et mobile et une rotation automatisée toutes les 8 secondes.",
        "banners_tabela": [
            ["Segmentation", "Fixe (R$/mois)", "Temporaire (R$/mois)", "Profil de l'Annonceur"],
            ["Pays", "R$ 800", "R$ 500", "PME locales, commerce régional"],
            ["Continent", "R$ 1.800", "R$ 1.200", "Marques régionales, expansion continentale"],
            ["Monde", "R$ 3.500", "R$ 2.500", "Entreprises mondiales, apps internationales"],
            ["Parrainage Exclusif", "R$ 6.000", "R$ 4.500/campagne", "Parrains master, lancements"],
        ],
        "banners_formatos": "728×90 px — Bannière centrale desktop · 320×100 px — Format mobile optimisé · 8 secondes — Rotation automatique · Géo-cible — Pays, continent ou portée mondiale",
        "b2b_titulo": "Forfaits d'Entreprise B2B — Haute Valeur, Haut Volume",
        "b2b_texto": "Les Forfaits B2B transforment A1ELOS en un outil d'employer branding et de bien-être corporatif. Les entreprises achètent des codes d'accès en volume pour les distribuer comme cadeaux aux collaborateurs ou clients — soutenues par le DUNS 942242668 pour des contrats corporatifs formels.",
        "b2b_planos": [
            ("Plan Basique · 50 codes", "50× Carte Express (R$ 8 chacun). Idéal pour les programmes d'avantages aux collaborateurs et les actions d'intégration."),
            ("Plan Intermédiaire · 100 codes", "50× Carte Express + 50× Recherche IA (R$ 17). Parfait pour les équipes et la stratégie de marque employeur."),
            ("Plan Premium · 200 codes", "100× Carte Express + 100× Carte Complète (R$ 17). Profondeur analytique maximale pour les grands groupes."),
        ],
        "b2b_tabela": [
            ["À partir de", "Remise", "Profil", "Utilisation Recommandée"],
            ["10 codes", "10%", "Petites équipes", "Action ponctuelle de bien-être"],
            ["50 codes", "20%", "Équipes en croissance", "Programmes récurrents"],
            ["100 codes", "25%", "PME", "Avantage trimestriel"],
            ["200 codes", "30%", "Entreprises moyennes", "Programmes complets"],
            ["500 codes", "40%", "Entreprises moyennes", "Cadeau annuel aux collaborateurs"],
            ["1.000 codes", "45%", "Grandes entreprises", "Fidélisation des clients"],
            ["2.000 codes", "50%", "Grands groupes", "Grande échelle"],
            ["Plus de 2.000", "Négociable", "Plan Diamant sur mesure", "Distribution de bonus en volume"],
        ],
        "projecoes_titulo": "Projections Financières : Horizon de 50 Ans",
        "projecoes_texto": "Les projections ont été construites sur la base d'estimations en pourcentage de pénétration du marché potentiel de ~5,32 milliards de locuteurs, avec une conversion conservatrice de 3% et un rachat de bonus entre 70% et 90%. La première décennie est détaillée aux années 1, 3, 5 et 7 pour mettre en évidence le momentum.",
        "projecoes_tabela": [
            ["Horizon", "Conservateur (R$)", "Optimiste (R$)"],
            ["Année 1", "R$ 281k", "R$ 702k"],
            ["Année 3", "R$ 983k", "R$ 2,8M"],
            ["Année 5", "R$ 2,8M", "R$ 7M"],
            ["Année 7", "R$ 5,6M", "R$ 14M"],
            ["Année 10", "R$ 11,2M", "R$ 28,1M"],
            ["Année 20", "R$ 42,1M", "R$ 112M"],
            ["Année 30", "R$ 84,3M", "R$ 211M"],
            ["Année 40", "R$ 126M", "R$ 351M"],
            ["Année 50", "R$ 169M", "R$ 492M"],
        ],
        "tracao_titulo": "Traction et Résultats Prouvés",
        "tracao_texto": "A1ELOS opère déjà avec des métriques de produit qui valident le modèle — forte rétention, évaluation premium et une base croissante de partenaires B2B démontrent que la plateforme livre une valeur réelle à l'utilisateur final et au marché corporatif.",
        "tracao_kpis": [
            ("12K+", "Utilisateurs Actifs", "Base organique en croissance constante"),
            ("87%", "Rétention", "Bien au-dessus de la moyenne de l'industrie (~30%)"),
            ("4,8★", "Évaluation Moyenne", "Satisfaction prouvée de l'utilisateur final"),
            ("23", "Partenaires B2B", "Contrats actifs avec entreprises et RH"),
        ],
        "roteiro_titulo": "Feuille de Route Stratégique",
        "roteiro_texto": "A1ELOS exécute un plan en quatre phases progressives — de la consolidation de la base actuelle au leadership mondial du marché, avec des options de sortie claires pour les investisseurs.",
        "roteiro_fases": [
            ("Phase 1 · Consolidation", "Renforcement de la base d'utilisateurs dans les langues déjà actives. Optimisation de la conversion, de la rétention et du LTV. Tour d'amorçage conclu."),
            ("Phase 2 · Expansion", "Lancement officiel dans les 3 nouveaux marchés : Indonésie, Turquie et Vietnam. Accélération du canal B2B et de la publicité géolocalisée."),
            ("Phase 3 · Entrée Mondiale", "Présence active dans les 14 langues avec des campagnes localisées. Partenariats white-label dans plus de 5 continents. Série A."),
            ("Phase 4 · Leadership", "Plus de 20 pays avec des opérations consolidées. Plateforme SaaS de référence mondiale en numérologie appliquée. IPO ou sortie stratégique."),
        ],
        "invest_titulo": "Investissement et Contact",
        "invest_texto": "Nous sommes prêts pour des présentations privées, la due diligence et les négociations. Contactez-nous par le canal de votre préférence.",
        "invest_dados": [
            ("Tour d'amorçage", "R$ 3,5 millions"),
            ("Valorisation Pré-Money", "R$ 14 millions"),
            ("Equity Offert", "Jusqu'à 20%"),
        ],
        "invest_contato": [
            ("Email Investisseurs", "a1elos.consultoria@gmail.com"),
            ("Email Général", "contato@a1elos.com"),
            ("Site Web", "www.a1elos.com"),
            ("DUNS", "942242668 — Dun & Bradstreet"),
        ],
        "invest_alocacao": "Allocation du Capital : 45% Technologie · 30% Marketing · 25% Opérations",
        "frase_final": "Les nombres ne mentent jamais.",
        "selo_final": ["DUNS 942242668", "23 PRODUITS", "14 LANGUES", "~5,3 MILLIARDS DE LOCUTEURS"],
        "graf_cons": "Conservateur",
        "graf_otim": "Optimiste",
        "grafico_titulo_linha": "Croissance Projetée (R$ milliers)",
        "pix_titulo": "Brésil : L'Infrastructure Pix",
        "pix_texto": "Pix est l'infrastructure publique de paiements instantanés du Brésil. Pour A1ELOS, elle garantit une collecte immédiate, un faible coût et une acceptation universelle — le fondement de l'opération B2C sur le marché brésilien et la porte d'entrée vers l'expansion internationale.",
        "pix_kpis": [
            ("30,1 milliards", "Transactions en 2025", "+20% vs 2024 · Febraban"),
            ("76,4%", "de la population utilise Pix", "211 millions de Brésiliens · Banque Centrale"),
            ("R$ 68,2 billions", "mobilisés au 2e sem. 2025", "78,4 milliards de transactions · Banque Centrale"),
            ("~80 milliards", "transactions en 2025", "+25,7% vs année précédente · Rapport Pix"),
        ],
        "pix_fonte": "Sources : Banque Centrale du Brésil (Pix en Chiffres) et Febraban (Enquête de Technologie Bancaire).",
        "ref_titulo": "Références Bibliographiques",
        "ref_intro": "Sources utilisées pour les données de marché, projections et indicateurs de cette présentation.",
        "ref_lista": [
            ("Global Wellness Institute", "Économie mondiale du bien-être : 6,8 billions USD (2024) → 9,8 billions USD (2029)."),
            ("MarkNtel Advisors", "Apps d'astrologie et numérologie : 3 milliards USD → 9 milliards USD d'ici 2030 (CAGR ~20%)."),
            ("FMI · Banque Mondiale", "PIB et parité du pouvoir d'achat (PPA) par pays."),
            ("Banque Centrale du Brésil", "Statistiques officielles du Pix : transactions, volume et utilisateurs."),
            ("Febraban", "Enquête de Technologie Bancaire — croissance du Pix en 2025."),
            ("IBGE", "Population et indicateurs socioéconomiques du Brésil."),
        ],
        },

"de": {
        "titulo": "A1ELOS Global Numerology",
        "subtitulo": "Die Wissenschaft der Zahlen, angewendet auf Ihren Erfolg",
        "capa_nota": "Strategische Präsentation für Investoren und Partner",
        "confidencial": "VERTRAULICH",
        "ano": "2026",
        "sumario_titulo": "Executive Summary",
        "duns_porque": "Warum ist DUNS wichtig?",
        "preco_consciente": "Bewusste Preisgestaltung",
        "idioma_col": "Sprache",
        "falantes_col": "Sprecher (Mio.)",
        "linhas_idiomas": [
           ["Englisch", "1.528"],
           ["Mandarin", "1.184"],
           ["Spanisch", "558"],
           ["Französisch", "396"],
           ["Arabisch", "335"],
           ["Portugiesisch", "270"],
           ["Russisch", "255"],
           ["Indonesisch", "255"],
           ["Deutsch", "134"],
           ["Japanisch", "123"],
           ["Vietnamesisch", "97"],
           ["Türkisch", "90"],
           ["Italienisch", "85"],
           ["Hebräisch", "9"],
        ],
        "total_linha": "GESAMT",
        "fonte_receita": "Einnahmequelle",
        "participacao": "Anteil",
        "b2c_linha": "B2C — 14 Sprachen",
        "b2b_linha": "B2B — Progressive Rabatte",
        "pub_linha": "Geolokalisierte Werbung",
        "tabela_descontos": "Tabelle der Progressiven Rabatte",
        "grafico_anos": ["Jahr 1", "Jahr 3", "Jahr 5", "Jahr 7", "Jahr 10"],
        "grafico_titulo": "Konservative Projektion (R$ Tausend)",
        "grafico_titulo_linha": "Projiziertes Wachstum (R$ Tausend)",
        "fale_conosco": "Kontaktieren Sie uns",
        "sumario_intro": "Diese Präsentation ist strukturiert, um Investoren und Partner durch alle strategischen Aspekte von A1ELOS Global Numerology zu führen — von der Marktthese bis zum Modell der wiederkehrenden Einnahmen.",
        "sumario_cards": [
            ("01", "Über A1ELOS", "Holding, Portfolio und DUNS-Zertifizierung"),
            ("02", "Marktchance", "Globale Wellness-Wirtschaft 6,8 Billionen USD"),
            ("03", "Lösung und Globale Reichweite", "14 Sprachen, ~5,3 Milliarden Sprecher"),
            ("04", "3 Neue Märkte", "Indonesien, Türkei und Vietnam"),
            ("05", "Portfolio und Preise", "23 Produkte, kalibriert nach Kaufkraft"),
            ("06", "Wiederkehrende Einnahmen", "Werbebanner und B2B-Pakete"),
            ("07", "Prognosen und Investition", "50-Jahres-Horizont · Seed-Runde R$ 3,5M"),
        ],
        "sobre_titulo": "Über A1ELOS",
        "sobre_texto": "A1ELOS ist eine Holding für Technologie und Wissen, die künstliche Intelligenz, angewandte Numerologie und kulturelle Strategie vereint, um digitale Produkte mit hoher Wirkung auf globaler Ebene zu schaffen. Unsere Mission: numerische Selbsterkenntnis zu demokratisieren, mit kulturellem Respekt und Respekt vor der Kaufkraft jedes Marktes.",
        "sobre_kpis": [
            ("23", "Aktive Produkte", "In 4 Zugriffsebenen"),
            ("14", "Sprachen", "~67% der Weltbevölkerung"),
            ("5,3 Mrd.", "Sprecher", "Realer adressierbarer Markt"),
            ("KI", "Integriert", "Personalisierungs-Engine"),
        ],
        "sobre_duns": "DUNS 942242668 — Dun & Bradstreet-Zertifizierung gültig in über 190 Ländern, ermöglicht B2B-Verträge und internationale Joint Ventures.",
        "duns_titulo": "Internationale Glaubwürdigkeit",
        "duns_texto": "Die DUNS-Nummer ist der Unternehmenspass von A1ELOS auf internationaler Bühne. Sie signalisiert Partnern, Firmenkunden und Investoren, dass das Unternehmen eine verifizierbare Identität, eine nachvollziehbare Historie und vertragliche Fähigkeit in jeder Rechtsordnung besitzt.",
        "duns_numero": "942242668",
        "duns_emitido": "Ausgestellt von Dun & Bradstreet — der globale Standard für Unternehmensidentität, anerkannt in mehr als 190 Ländern.",
        "duns_paises": "190+ LÄNDER",
        "duns_beneficios": [
            ("B2B-Verträge", "Qualifikation für Ausschreibungen und globale Lieferanten"),
            ("Joint Ventures", "Internationale Partnerschaften mit erleichterter Due Diligence"),
            ("Sofortige Glaubwürdigkeit", "Zeichen der Seriosität für institutionelle Investoren"),
        ],
        "mercado_titulo": "Marktchance",
        "mercado_texto": "Wir erleben die perfekte Konvergenz: digitales Wohlbefinden explodiert weltweit, während Numerologie und Astrologie zu Apps mit hoher Interaktion migrieren. A1ELOS ist genau an dieser Schnittstelle positioniert, mit 74% der Weltbevölkerung bereits online (~6 Milliarden Menschen).",
        "mercado_cards": [
            ("Globales Wohlbefinden", "6,8 Billionen USD → 9,8 Billionen USD bis 2029 (+7,6% p.a.)"),
            ("Astrologie/Numerologie-Apps", "3 Milliarden USD → 9 Milliarden USD bis 2030 · CAGR 20%"),
            ("Wellness-Apps", "CAGR 14,9% → 26,2 Milliarden USD im Jahr 2030"),
            ("Online-Nutzer", "74% der Welt · ~6 Milliarden Menschen"),
        ],
        "problema_titulo": "Das Problem, das Wir Lösen",
        "problema_col_esq_titulo": "Aktuelle Marktfehler",
        "problema_col_esq": [
            ("Sprachbarriere", "Die überwiegende Mehrheit der Numerologie-Tools funktioniert nur auf Englisch und schließt Milliarden von Muttersprachlern in anderen Sprachen aus."),
            ("Preise Losgelöst von der Realität", "In Dollar bepreiste Produkte für Schwellenländer erzeugen wirtschaftliche Ausgrenzung — der Nutzer lehnt nicht das Produkt ab, sondern den unzugänglichen Preis."),
            ("Mangel an Tiefe", "Generische Tools liefern oberflächliche Antworten ohne Personalisierung, ohne kulturellen Kontext und ohne praktische Anwendung im Alltag."),
        ],
        "problema_col_dir_titulo": "Die Kosten der Ausgrenzung",
        "problema_col_dir": "Wenn eine Plattform Sprache und Kaufkraft ignoriert, verlässt sie freiwillig den größten Markt der Welt: die über 4 Milliarden Menschen, die in Schwellenländern leben und nicht-anglophone Sprachen sprechen. Das ist die Lücke, die A1ELOS mit chirurgischer Präzision besetzt.",
        "problema_destaque": "Plattformen, die lokale Kaufkraft ignorieren, verlieren den Zugang zu mehr als 60% des globalen adressierbaren Marktes.",
        "solucao_titulo": "Unsere Lösung: 3 Strategische Säulen",
        "solucao_texto": "A1ELOS hat eine integrierte Plattform aufgebaut, die numerische Wissenschaft, künstliche Intelligenz und kulturelle Sensibilität vereint. Die Lösung operiert auf drei komplementären Fronten und gewährleistet diversifizierte Einnahmen und hohe Bindung.",
        "solucao_colunas": [
            ("Persönliche Karten", "Tiefe und personalisierte numerische Analysen für den Endnutzer — Identität, Mission, Lebenszyklen und Kompatibilität — geliefert in 14 Sprachen mit integrierter KI."),
            ("Unternehmensnumerologie", "Numerologische Diagnosen für Marken, CNPJ, Gründungsdaten und Unternehmensstrategie. Differenziertes Produkt mit hohem wahrgenommenem Wert für den B2B-Markt."),
            ("White-Label B2B", "Lizenzierung der Plattform für Partnerunternehmen, die Numerologie unter eigener Marke anbieten möchten — mit mehrsprachigem Support und vollständiger Anpassung."),
        ],
        "alcance_titulo": "Globale Reichweite: 14 Sprachen · ~5,3 Milliarden Sprecher",
        "alcance_texto": "A1ELOS deckt ~67% der Weltbevölkerung mit einer wirklich mehrsprachigen Plattform ab. Jede Sprache repräsentiert einen eigenen kulturellen Markt, mit Preisen, die an die lokale Kaufkraft angepasst sind.",
        "mercados_titulo": "Die 3 Neuen Märkte: +442 Millionen Sprecher",
        "mercados_texto": "Die strategische Expansion nach Indonesien, in die Türkei und nach Vietnam stellt einen qualitativen Sprung dar: Märkte mit hohem Wirtschaftswachstum, wachsender digitaler Durchdringung und nachgewiesener Nachfrage nach zugänglichen digitalen Wellness-Lösungen.",
        "mercados_cards": [
            ("Indonesien", ["285 Millionen Einwohner", "80,5% Internetdurchdringung", "~255 Millionen indonesische Sprecher", "Wellness: 51,2 Mrd. USD (2025) → 72,8 Mrd. USD (2034)"]),
            ("Türkei", ["85,9 Millionen Einwohner", "BIP PPP pro Kopf 37.301 USD", "~90 Millionen türkische Sprecher", "Über dem Weltdurchschnitt (27.211 USD)"]),
            ("Vietnam",  ["~100 Millionen Einwohner", "BIP pro Kopf ~5.066 USD (+7,4%/Jahr)", "~97 Millionen vietnamesische Sprecher", "Wellness: 303 Mio. USD (2025) → 485 Mio. USD (2030)"]),
        ],
        "mercados_rodape": "3 neue Märkte = +442 Millionen neue adressierbare Sprecher — in die Plattform mit kulturell kalibrierten Preisen integriert.",
        "preco_titulo": "Philosophie der Bewussten Preisgestaltung",
        "preco_esq": "Kultureller Respekt + Respekt vor der Kaufkraft = realer adressierbarer Markt. Gleiche Wertproportion. Unterschiedliche Preise. Gleiche Würde für alle Märkte.",
        "preco_dir_titulo": "So Funktioniert es in der Praxis",
        "preco_dir": "A1ELOS wendet die Kaufkraftparität (KKP) als zentrales Preiskriterium an. Dasselbe Produkt liefert dem Nutzer in Lagos, Jakarta, Hanoi oder New York denselben relativen Wert — der Preis wird so kalibriert, dass die finanzielle Anstrengung proportional zum lokalen Einkommen ist.",
        "preco_pilares": [
            ("KKP-Kalibrierung", "Preise, die an den Kaufkraftindex jedes Landes angepasst sind"),
            ("Kultureller Respekt", "Sprache, Währung und lokaler Kontext in das Produkt integriert"),
            ("Überlegene Konversion", "Ein fairer Preis erzeugt mehr Konversion und höhere langfristige Bindung"),
        ],
        "portfolio_titulo": "Portfolio: 23 Produkte in 4 Ebenen",
        "portfolio_texto": "Die Schichtstruktur stellt sicher, dass jedes Nutzerprofil — vom Neugierigen bis zum Profi — ein Angebot findet, das zu seinem Engagement und seiner finanziellen Kapazität passt.",
        "portfolio_tabela": [
            ["Ebene", "Produkte", "Preisspanne (R$)", "Profil"],
            ["Basis", "Express-Karte, Vollständige Karte", "R$ 8 – 17", "Neugierig, erster Kontakt"],
            ["Mittel", "KI-Suche, Urnenname, Wahl-Nr.", "R$ 26 – 53", "Engagierter Nutzer"],
            ["Fortgeschritten", "Unternehmensnumerologie, Zyklen, Mission", "R$ 81 – 109", "Profi, Unternehmer"],
            ["Premium", "Vollständige Diagnosen, Persönliche Karten", "R$ 137 – 305", "Hohes Einkommen, Unternehmensnutzung"],
            ["B2B", "Unternehmenspakete, Lizenzen, Geschenke", "Auf Anfrage", "Unternehmen und Teams"],
        ],
        "portfolio_rodape": "23 Produkte decken die gesamte Nutzerreise ab, vom ersten Kontakt bis zum wiederkehrenden Premium-Kunden — maximiert den LTV pro Sprache und Markt.",
        "negocio_titulo": "Geschäftsmodell: 3 Einnahmequellen",
        "negocio_texto": "A1ELOS wurde mit diversifizierten und skalierbaren Einnahmen konzipiert: Direktverkauf an den Endverbraucher auf globaler Ebene, hochwertige B2B-Verträge und wiederkehrende geolokalisierte Werbung — drei Motoren, die sich gegenseitig speisen.",
        "negocio_colunas": [
            ("B2C — 14 Sprachen", "Direktverkauf digitaler Produkte in allen Währungen, mit Preisen, die per KKP angepasst sind. Automatische Skalierung via KI — ohne Support-Team proportional zum Wachstum."),
            ("B2B — Progressive Rabatte", "Unternehmenspakete für HR, Employer Branding und institutionelle Geschenke. Rabatte von 10% bis 50% je nach Volumen. Über 2.000 Codes, direkte Verhandlung (Diamant-Plan). Verträge gestützt durch DUNS 942242668."),
            ("Geolokalisierte Werbung", "Banner, segmentiert nach Land, Kontinent oder weltweit mit automatisierter Rotation. Wiederkehrende monatliche Einnahmen mit hohem Wert — ohne Abhängigkeit vom Produktverkaufsvolumen."),
        ],
        "banners_titulo": "Werbebanner — Vorhersehbare Monatliche Einnahmen",
        "banners_texto": "Die geolokalisierte Werbeplattform von A1ELOS bietet Werbetreibenden eine präzise Segmentierung nach Land, Kontinent oder globaler Reichweite, mit für Desktop und Mobile optimierten Formaten und automatisierter Rotation alle 8 Sekunden.",
        "banners_tabela": [
            ["Segmentierung", "Fix (R$/Monat)", "Temporär (R$/Monat)", "Werbetreibenden-Profil"],
            ["Land", "R$ 800", "R$ 500", "Lokale KMU, regionaler Handel"],
            ["Kontinent", "R$ 1.800", "R$ 1.200", "Regionale Marken, kontinentale Expansion"],
            ["Welt", "R$ 3.500", "R$ 2.500", "Globale Unternehmen, internationale Apps"],
            ["Exklusives Sponsoring", "R$ 6.000", "R$ 4.500/Kampagne", "Master-Sponsoren, Markteinführungen"],
        ],
        "banners_formatos": "728×90 px — Zentrales Desktop-Banner · 320×100 px — Optimiertes Mobile-Format · 8 Sekunden — Automatische Rotation · Geo-Ziel — Land, Kontinent oder weltweite Reichweite",
        "b2b_titulo": "B2B-Unternehmenspakete — Hoher Wert, Hohes Volumen",
        "b2b_texto": "Die B2B-Pakete machen A1ELOS zu einem Werkzeug für Employer Branding und Unternehmens-Wellness. Unternehmen erwerben Zugangscodes in großen Mengen, um sie als Geschenke an Mitarbeiter oder Kunden zu verteilen — gestützt durch DUNS 942242668 für formelle Unternehmensverträge.",
        "b2b_planos": [
            ("Basis-Plan · 50 Codes", "50× Express-Karte (R$ 8 pro Stück). Ideal für Mitarbeiter-Leistungsprogramme und Integrationsmaßnahmen."),
            ("Mittel-Plan · 100 Codes", "50× Express-Karte + 50× KI-Suche (R$ 17). Perfekt für Teams und Employer-Branding-Strategie."),
            ("Premium-Plan · 200 Codes", "100× Express-Karte + 100× Vollständige Karte (R$ 17). Maximale analytische Tiefe für große Gruppen."),
        ],
        "b2b_tabela": [
            ["Ab", "Rabatt", "Profil", "Empfohlene Verwendung"],
            ["10 Codes", "10%", "Kleine Teams", "Einmalige Wellness-Aktion"],
            ["50 Codes", "20%", "Wachsende Teams", "Wiederkehrende Programme"],
            ["100 Codes", "25%", "KMU", "Vierteljährlicher Vorteil"],
            ["200 Codes", "30%", "Mittlere Unternehmen", "Vollständige Programme"],
            ["500 Codes", "40%", "Mittlere Unternehmen", "Jährliches Geschenk an Mitarbeiter"],
            ["1.000 Codes", "45%", "Große Unternehmen", "Kundenbindung"],
            ["2.000 Codes", "50%", "Große Gruppen", "Großer Maßstab"],
            ["Über 2.000", "Verhandelbar", "Maßgeschneiderter Diamant-Plan", "Mengenverteilung von Boni"],
        ],
        "projecoes_titulo": "Finanzprognosen: 50-Jahres-Horizont",
        "projecoes_texto": "Die Prognosen wurden auf Basis prozentualer Penetrationsschätzungen des potenziellen Marktes von ~5,32 Milliarden Sprechern erstellt, mit einer konservativen Konversion von 3% und einer Bonus-Einlösung zwischen 70% und 90%. Das erste Jahrzehnt wird in den Jahren 1, 3, 5 und 7 detailliert dargestellt, um das Momentum zu verdeutlichen.",
        "projecoes_tabela": [
            ["Horizont", "Konservativ (R$)", "Optimistisch (R$)"],
            ["Jahr 1", "R$ 281k", "R$ 702k"],
            ["Jahr 3", "R$ 983k", "R$ 2,8M"],
            ["Jahr 5", "R$ 2,8M", "R$ 7M"],
            ["Jahr 7", "R$ 5,6M", "R$ 14M"],
            ["Jahr 10", "R$ 11,2M", "R$ 28,1M"],
            ["Jahr 20", "R$ 42,1M", "R$ 112M"],
            ["Jahr 30", "R$ 84,3M", "R$ 211M"],
            ["Jahr 40", "R$ 126M", "R$ 351M"],
            ["Jahr 50", "R$ 169M", "R$ 492M"],
        ],
        "tracao_titulo": "Traction und Bewährte Ergebnisse",
        "tracao_texto": "A1ELOS operiert bereits mit Produktkennzahlen, die das Modell validieren — hohe Bindung, Premium-Bewertung und eine wachsende Basis von B2B-Partnern zeigen, dass die Plattform dem Endnutzer und dem Unternehmensmarkt echten Wert liefert.",
        "tracao_kpis": [
            ("12K+", "Aktive Nutzer", "Konsistent wachsende organische Basis"),
            ("87%", "Bindung", "Weit über dem Branchendurchschnitt (~30%)"),
            ("4,8★", "Durchschnittliche Bewertung", "Nachgewiesene Endnutzer-Zufriedenheit"),
            ("23", "B2B-Partner", "Aktive Verträge mit Unternehmen und HR"),
        ],
        "roteiro_titulo": "Strategischer Fahrplan",
        "roteiro_texto": "A1ELOS führt einen Plan in vier progressiven Phasen aus — von der Konsolidierung der aktuellen Basis bis zur globalen Marktführerschaft, mit klaren Ausstiegsoptionen für Investoren.",
        "roteiro_fases": [
            ("Phase 1 · Konsolidierung", "Stärkung der Nutzerbasis in bereits aktiven Sprachen. Optimierung von Konversion, Bindung und LTV. Seed-Runde abgeschlossen."),
            ("Phase 2 · Expansion", "Offizieller Start in den 3 neuen Märkten: Indonesien, Türkei und Vietnam. Beschleunigung des B2B-Kanals und der geolokalisierten Werbung."),
            ("Phase 3 · Globaler Eintritt", "Aktive Präsenz in allen 14 Sprachen mit lokalisierten Kampagnen. White-Label-Partnerschaften in über 5 Kontinenten. Serie A."),
            ("Phase 4 · Führung", "Über 20 Länder mit konsolidierten Operationen. Globale Referenz-SaaS-Plattform in angewandter Numerologie. IPO oder strategischer Exit."),
        ],
        "invest_titulo": "Investition und Kontakt",
        "invest_texto": "Wir sind bereit für private Präsentationen, Due Diligence und Verhandlungen. Kontaktieren Sie uns über Ihren bevorzugten Kanal.",
        "invest_dados": [
            ("Seed-Runde", "R$ 3,5 Millionen"),
            ("Pre-Money-Bewertung", "R$ 14 Millionen"),
            ("Angebotenes Eigenkapital", "Bis zu 20%"),
        ],
        "invest_contato": [
            ("Investoren-E-Mail", "a1elos.consultoria@gmail.com"),
            ("Allgemeine E-Mail", "contato@a1elos.com"),
            ("Website", "www.a1elos.com"),
            ("DUNS", "942242668 — Dun & Bradstreet"),
        ],
        "invest_alocacao": "Kapitalallokation: 45% Technologie · 30% Marketing · 25% Betrieb",
        "frase_final": "Zahlen lügen nie.",
        "selo_final": ["DUNS 942242668", "23 PRODUKTE", "14 SPRACHEN", "~5,3 MRD. SPRECHER"],
        "graf_cons": "Konservativ",
        "graf_otim": "Optimistisch",
        "grafico_titulo_linha": "Projiziertes Wachstum (R$ Tausend)",
        "pix_titulo": "Brasilien: Die Pix-Infrastruktur",
        "pix_texto": "Pix ist die öffentliche Infrastruktur für Sofortzahlungen in Brasilien. Für A1ELOS garantiert sie sofortige Zahlung, niedrige Kosten und universelle Akzeptanz — das Fundament des B2C-Betriebs im brasilianischen Markt und das Tor zur internationalen Expansion.",
        "pix_kpis": [
            ("30,1 Mrd.", "Transaktionen 2025", "+20% vs. 2024 · Febraban"),
            ("76,4%", "der Bevölkerung nutzt Pix", "211 Millionen Brasilianer · Zentralbank"),
            ("R$ 68,2 Bio.", "bewegt im 2. Halbjahr 2025", "78,4 Mrd. Transaktionen · Zentralbank"),
            ("~80 Mrd.", "Transaktionen 2025", "+25,7% vs. Vorjahr · Pix-Bericht"),
        ],
        "pix_fonte": "Quellen: Zentralbank von Brasilien (Pix in Zahlen) und Febraban (Banktechnologie-Umfrage).",
        "ref_titulo": "Bibliografische Referenzen",
        "ref_intro": "Quellen, die für die Marktdaten, Prognosen und Indikatoren dieser Präsentation verwendet wurden.",
        "ref_lista": [
            ("Global Wellness Institute", "Globale Wellness-Wirtschaft: 6,8 Bio. USD (2024) → 9,8 Bio. USD (2029)."),
            ("MarkNtel Advisors", "Astrologie- und Numerologie-Apps: 3 Mrd. USD → 9 Mrd. USD bis 2030 (CAGR ~20%)."),
            ("IWF · Weltbank", "BIP und Kaufkraftparität (KKP) nach Ländern."),
            ("Zentralbank von Brasilien", "Offizielle Pix-Statistiken: Transaktionen, Volumen und Nutzer."),
            ("Febraban", "Banktechnologie-Umfrage — Pix-Wachstum 2025."),
            ("IBGE", "Bevölkerung und sozioökonomische Indikatoren Brasiliens."),
        ],
        },

"ja": {
        "titulo": "A1ELOS グローバル数秘術",
        "subtitulo": "数字の科学をあなたの成功に応用",
        "capa_nota": "投資家・パートナー向け戦略プレゼンテーション",
        "confidencial": "機密",
        "ano": "2026",
        "sumario_titulo": "エグゼクティブサマリー",
        "duns_porque": "DUNSが重要な理由",
        "preco_consciente": "意識的価格設定",
        "idioma_col": "言語",
        "falantes_col": "話者（百万人）",
        "linhas_idiomas": [
           ["英語", "1,528"],
           ["中国語（北京語）", "1,184"],
           ["スペイン語", "558"],
           ["フランス語", "396"],
           ["アラビア語", "335"],
           ["ポルトガル語", "270"],
           ["ロシア語", "255"],
           ["インドネシア語", "255"],
           ["ドイツ語", "134"],
           ["日本語", "123"],
           ["ベトナム語", "97"],
           ["トルコ語", "90"],
           ["イタリア語", "85"],
           ["ヘブライ語", "9"],
        ],
        "total_linha": "合計",
        "fonte_receita": "収益源",
        "participacao": "割合",
        "b2c_linha": "B2C — 14言語",
        "b2b_linha": "B2B — 段階的割引",
        "pub_linha": "位置情報広告",
        "tabela_descontos": "段階的割引表",
        "grafico_anos": ["1年目", "3年目", "5年目", "7年目", "10年目"],
        "grafico_titulo": "保守的予測（R$千）",
        "grafico_titulo_linha": "予測成長（R$千）",
        "fale_conosco": "お問い合わせ",
        "sumario_intro": "このプレゼンテーションは、投資家とパートナーをA1ELOS グローバル数秘術の戦略的側面すべてに導くよう構成されています。市場テーゼから継続的収益モデルまでを網羅します。",
        "sumario_cards": [
            ("01", "A1ELOSについて", "ホールディング、ポートフォリオ、DUNS認証"),
            ("02", "市場機会", "世界のウェルネス経済 6.8兆米ドル"),
            ("03", "ソリューションとグローバル展開", "14言語、約53億人の話者"),
            ("04", "3つの新市場", "インドネシア、トルコ、ベトナム"),
            ("05", "ポートフォリオと価格", "購買力に合わせて調整された23製品"),
            ("06", "継続的収益", "広告バナーとB2Bパッケージ"),
            ("07", "予測と投資", "50年の展望 · シードラウンド R$ 350万"),
        ],
        "sobre_titulo": "A1ELOSについて",
        "sobre_texto": "A1ELOSは、人工知能、応用数秘術、文化的戦略を統合し、世界的規模で高い影響力を持つデジタル製品を生み出すテクノロジーと知識のホールディングです。私たちの使命は、文化的尊重と各市場の購買力への尊重をもって、数秘的自己認識を民主化することです。",
        "sobre_kpis": [
            ("23", "アクティブ製品", "4つのアクセスレベル"),
            ("14", "言語", "世界人口の約67%"),
            ("53億", "話者", "実際の到達可能市場"),
            ("AI", "統合", "パーソナライズエンジン"),
        ],
        "sobre_duns": "DUNS 942242668 — 190以上の国で有効なDun & Bradstreet認証。B2B契約と国際ジョイントベンチャーを可能にします。",
        "duns_titulo": "国際的信頼性",
        "duns_texto": "DUNS番号は、国際舞台におけるA1ELOSの企業パスポートです。パートナー、法人顧客、投資家に対し、検証可能な身元、追跡可能な履歴、あらゆる法域での契約能力を持つことを示します。",
        "duns_numero": "942242668",
        "duns_emitido": "Dun & Bradstreet発行 — 190以上の国で認められたグローバル企業身元標準。",
        "duns_paises": "190以上の国",
        "duns_beneficios": [
            ("B2B契約", "国際入札とグローバルサプライヤーの資格"),
            ("ジョイントベンチャー", "デューデリジェンスが容易な国際パートナーシップ"),
            ("即時の信頼性", "機関投資家への真剣さの証"),
        ],
        "mercado_titulo": "市場機会",
        "mercado_texto": "私たちは完璧な融合を生きています。デジタルウェルネスが世界的に爆発的に成長する一方、数秘術と占星術は高いエンゲージメントのアプリへ移行しています。A1ELOSはまさにこの交差点に位置し、世界人口の74%がすでにオンラインです（約60億人）。",
        "mercado_cards": [
            ("世界のウェルネス", "6.8兆米ドル → 2029年までに9.8兆米ドル（年率+7.6%）"),
            ("占星術/数秘術アプリ", "30億米ドル → 2030年までに90億米ドル · CAGR 20%"),
            ("ウェルネスアプリ", "CAGR 14.9% → 2030年に262億米ドル"),
            ("オンラインユーザー", "世界の74% · 約60億人"),
        ],
        "problema_titulo": "私たちが解決する問題",
        "problema_col_esq_titulo": "現在の市場の欠陥",
        "problema_col_esq": [
            ("言語の壁", "数秘術ツールの圧倒的多数は英語のみで動作し、他の言語のネイティブ話者数十億人を排除しています。"),
            ("現実から乖離した価格", "新興市場向けにドル建てで価格設定された製品は経済的排除を生みます。ユーザーは製品を拒否するのではなく、手の届かない価格を拒否するのです。"),
            ("深みの欠如", "一般的なツールは、パーソナライズも文化的文脈も日常生活への実用的応用もない表面的な回答を提供します。"),
        ],
        "problema_col_dir_titulo": "排除のコスト",
        "problema_col_dir": "プラットフォームが言語と購買力を無視するとき、それは世界最大の市場を自ら放棄します。新興経済に暮らし、英語圏以外の言語を話す40億人以上の人々です。これこそA1ELOSが外科的精度で占めるギャップです。",
        "problema_destaque": "現地の購買力を無視するプラットフォームは、世界の到達可能市場の60%以上へのアクセスを失います。",
        "solucao_titulo": "私たちのソリューション：3つの戦略的柱",
        "solucao_texto": "A1ELOSは、数秘科学、人工知能、文化的感性を組み合わせた統合プラットフォームを構築しました。このソリューションは3つの補完的な側面で機能し、多様な収益と高い維持率を保証します。",
        "solucao_colunas": [
            ("パーソナルマップ", "エンドユーザー向けの深くパーソナライズされた数秘分析 — アイデンティティ、使命、ライフサイクル、相性 — 統合AIで14言語で提供。"),
            ("ビジネス数秘術", "ブランド、CNPJ、設立日、企業戦略に適用される数秘診断。B2B市場で高い知覚価値を持つ差別化された製品。"),
            ("ホワイトラベルB2B", "自社ブランドで数秘術を提供したいパートナー企業へのプラットフォームライセンス — 多言語サポートと完全なカスタマイズ付き。"),
        ],
        "alcance_titulo": "グローバル展開：14言語 · 約53億人の話者",
        "alcance_texto": "A1ELOSは、真に多言語のプラットフォームで世界人口の約67%をカバーしています。各言語は異なる文化的市場を表し、価格は現地の購買力に合わせて調整されています。",
        "mercados_titulo": "3つの新市場：+4億4,200万人の話者",
        "mercados_texto": "インドネシア、トルコ、ベトナムへの戦略的拡大は質的な飛躍を表します。高い経済成長、成長するデジタル普及率、アクセスしやすいデジタルウェルネスソリューションへの実証済みの需要を持つ市場です。",
        "mercados_cards": [
            ("インドネシア", ["人口2億8,500万人", "インターネット普及率80.5%", "インドネシア語話者約2億5,500万人", "ウェルネス：512億米ドル（2025）→ 728億米ドル（2034）"]),
            ("トルコ", ["人口8,590万人", "一人当たりGDP PPP 37,301米ドル", "トルコ語話者約9,000万人", "世界平均（27,211米ドル）を上回る"]),
            ("ベトナム",  ["人口約1億人", "一人当たりGDP 約5,066米ドル（年率+7.4%）", "ベトナム語話者約9,700万人", "ウェルネス：3億300万米ドル（2025）→ 4億8,500万米ドル（2030）"]),
        ],
        "mercados_rodape": "3つの新市場 = 文化的に調整された価格でプラットフォームに統合された、新たに到達可能な4億4,200万人の話者。",
        "preco_titulo": "意識的価格設定の哲学",
        "preco_esq": "文化的尊重 + 購買力への尊重 = 実際の到達可能市場。同じ価値の割合。異なる価格。すべての市場に等しい尊厳。",
        "preco_dir_titulo": "実際の仕組み",
        "preco_dir": "A1ELOSは購買力平価（PPP）を価格設定の中心基準として適用します。同じ製品がラゴス、ジャカルタ、ハノイ、ニューヨークのユーザーに同じ相対的価値を提供します。価格は、経済的努力が現地の収入に比例するように調整されます。",
        "preco_pilares": [
            ("PPPキャリブレーション", "各国の購買力指数に合わせて調整された価格"),
            ("文化的尊重", "言語、通貨、現地の文脈を製品に統合"),
            ("優れた転換率", "公正な価格がより多くの転換と長期的な維持を生む"),
        ],
        "portfolio_titulo": "ポートフォリオ：4レベルに23製品",
        "portfolio_texto": "階層構造により、好奇心旺盛な人からプロフェッショナルまで、すべてのユーザープロフィールが自分のエンゲージメントレベルと財務能力に適したオファーを見つけられます。",
        "portfolio_tabela": [
            ["レベル", "製品", "価格帯（R$）", "プロフィール"],
            ["ベーシック", "エクスプレスマップ、フルマップ", "R$ 8 – 17", "好奇心旺盛、初回接触"],
            ["インターミディエイト", "AI検索、投票用紙名、選挙番号", "R$ 26 – 53", "エンゲージしたユーザー"],
            ["アドバンスト", "ビジネス数秘術、サイクル、使命", "R$ 81 – 109", "プロフェッショナル、起業家"],
            ["プレミアム", "完全診断、パーソナルマップ", "R$ 137 – 305", "高所得、法人利用"],
            ["B2B", "法人パッケージ、ライセンス、ギフト", "要相談", "企業とチーム"],
        ],
        "portfolio_rodape": "23製品は、初回接触から継続的なプレミアム顧客までのユーザージャーニー全体をカバーし、言語と市場ごとのLTVを最大化します。",
        "negocio_titulo": "ビジネスモデル：3つの収益源",
        "negocio_texto": "A1ELOSは多様で拡張可能な収益で設計されています。グローバル規模でのエンドユーザーへの直接販売、高価値のB2B契約、継続的な位置情報広告 — 相互に支え合う3つのエンジンです。",
        "negocio_colunas": [
            ("B2C — 14言語", "すべての通貨でのデジタル製品の直接販売、PPPによる価格調整。AIによる自動スケーリング — 成長に比例したサポートチーム不要。"),
            ("B2B — 段階的割引", "人事、エンプロイヤーブランディング、法人ギフト向けの法人パッケージ。数量に応じて10%から50%の割引。2,000コード超は直接交渉（ダイヤモンドプラン）。DUNS 942242668が裏付ける契約。"),
            ("位置情報広告", "国、大陸、世界別にセグメント化された自動回転バナー。製品販売量に依存しない、高価値の継続的な月間収益。"),
        ],
        "banners_titulo": "広告バナー — 予測可能な月間収益",
        "banners_texto": "A1ELOSの位置情報広告プラットフォームは、広告主に国、大陸、またはグローバルリーチによる精密なセグメント化を提供し、デスクトップとモバイル向けに最適化されたフォーマットと8秒ごとの自動回転を備えています。",
        "banners_tabela": [
            ["セグメント", "固定（R$/月）", "一時（R$/月）", "広告主プロフィール"],
            ["国", "R$ 800", "R$ 500", "地元中小企業、地域商業"],
            ["大陸", "R$ 1,800", "R$ 1,200", "地域ブランド、大陸展開"],
            ["世界", "R$ 3,500", "R$ 2,500", "グローバル企業、国際アプリ"],
            ["独占スポンサー", "R$ 6,000", "R$ 4,500/キャンペーン", "マスタースポンサー、ローンチ"],
        ],
        "banners_formatos": "728×90 px — デスクトップ中央バナー · 320×100 px — 最適化モバイルフォーマット · 8秒 — 自動回転 · ジオターゲット — 国、大陸、または世界リーチ",
        "b2b_titulo": "B2B法人パッケージ — 高価値、高ボリューム",
        "b2b_texto": "B2BパッケージはA1ELOSをエンプロイヤーブランディングと法人ウェルネスのツールに変えます。企業はアクセスコードを大量に購入し、従業員や顧客へのギフトとして配布します — 正式な法人契約のためのDUNS 942242668によって裏付けられています。",
        "b2b_planos": [
            ("ベーシックプラン · 50コード", "50× エクスプレスマップ（各R$ 8）。従業員福利厚生プログラムと統合アクションに最適。"),
            ("インターミディエイトプラン · 100コード", "50× エクスプレスマップ + 50× AI検索（R$ 17）。チームとエンプロイヤーブランディング戦略に最適。"),
            ("プレミアムプラン · 200コード", "100× エクスプレスマップ + 100× フルマップ（R$ 17）。大規模グループ向けの最大の分析深度。"),
        ],
        "b2b_tabela": [
            ["〜から", "割引", "プロフィール", "推奨用途"],
            ["10コード", "10%", "小規模チーム", "単発ウェルネスアクション"],
            ["50コード", "20%", "成長中のチーム", "継続的プログラム"],
            ["100コード", "25%", "中小企業", "四半期特典"],
            ["200コード", "30%", "中規模企業", "完全なプログラム"],
            ["500コード", "40%", "中規模企業", "従業員への年間ギフト"],
            ["1,000コード", "45%", "大企業", "顧客ロイヤルティ"],
            ["2,000コード", "50%", "大グループ", "大規模"],
            ["2,000超", "交渉可能", "カスタムダイヤモンドプラン", "ボリュームボーナス配布"],
        ],
        "projecoes_titulo": "財務予測：50年の展望",
        "projecoes_texto": "予測は、約53.2億人の話者の潜在市場に対するパーセンテージ浸透率の見積もりに基づいて構築され、保守的な3%の転換率と70%から90%のボーナス引き換え率を想定しています。最初の10年間は、勢いを明確にするために1、3、5、7年目を詳細に示しています。",
        "projecoes_tabela": [
            ["展望", "保守的（R$）", "楽観的（R$）"],
            ["1年目", "R$ 281k", "R$ 702k"],
            ["3年目", "R$ 983k", "R$ 280万"],
            ["5年目", "R$ 280万", "R$ 700万"],
            ["7年目", "R$ 560万", "R$ 1,400万"],
            ["10年目", "R$ 1,120万", "R$ 2,810万"],
            ["20年目", "R$ 4,210万", "R$ 1億1,200万"],
            ["30年目", "R$ 8,430万", "R$ 2億1,100万"],
            ["40年目", "R$ 1億2,600万", "R$ 3億5,100万"],
            ["50年目", "R$ 1億6,900万", "R$ 4億9,200万"],
        ],
        "tracao_titulo": "牽引力と実証済みの結果",
        "tracao_texto": "A1ELOSはすでにモデルを検証する製品指標で運営しています。高い維持率、プレミアム評価、成長するB2Bパートナー基盤は、プラットフォームがエンドユーザーと法人市場に真の価値を提供していることを示しています。",
        "tracao_kpis": [
            ("12K+", "アクティブユーザー", "一貫して成長するオーガニック基盤"),
            ("87%", "維持率", "業界平均（約30%）をはるかに上回る"),
            ("4.8★", "平均評価", "実証済みのエンドユーザー満足度"),
            ("23", "B2Bパートナー", "企業と人事とのアクティブな契約"),
        ],
        "roteiro_titulo": "戦略的ロードマップ",
        "roteiro_texto": "A1ELOSは、現在の基盤の統合からグローバル市場リーダーシップまで、投資家に明確な出口オプションを提供する4つの段階的フェーズで計画を実行します。",
        "roteiro_fases": [
            ("フェーズ1 · 統合", "すでにアクティブな言語でのユーザー基盤の強化。転換率、維持率、LTVの最適化。シードラウンド完了。"),
            ("フェーズ2 · 拡大", "3つの新市場での正式ローンチ：インドネシア、トルコ、ベトナム。B2Bチャネルと位置情報広告の加速。"),
            ("フェーズ3 · グローバル参入", "ローカライズされたキャンペーンで全14言語に積極的に展開。5以上の大陸でのホワイトラベルパートナーシップ。シリーズA。"),
            ("フェーズ4 · リーダーシップ", "統合された事業を持つ20以上の国。応用数秘術におけるグローバルリファレンスSaaSプラットフォーム。IPOまたは戦略的出口。"),
        ],
        "invest_titulo": "投資とお問い合わせ",
        "invest_texto": "私たちはプライベートプレゼンテーション、デューデリジェンス、交渉の準備ができています。お好みのチャネルからお問い合わせください。",
        "invest_dados": [
            ("シードラウンド", "R$ 350万"),
            ("プレマネー評価額", "R$ 1,400万"),
            ("提供株式", "最大20%"),
        ],
        "invest_contato": [
            ("投資家メール", "a1elos.consultoria@gmail.com"),
            ("一般メール", "contato@a1elos.com"),
            ("ウェブサイト", "www.a1elos.com"),
            ("DUNS", "942242668 — Dun & Bradstreet"),
        ],
        "invest_alocacao": "資本配分：45% テクノロジー · 30% マーケティング · 25% オペレーション",
        "frase_final": "数字は決して嘘をつかない。",
        "selo_final": ["DUNS 942242668", "23製品", "14言語", "約53億人の話者"],
        "graf_cons": "保守的",
        "graf_otim": "楽観的",
        "grafico_titulo_linha": "予測成長（R$千）",
        "pix_titulo": "ブラジル：Pixインフラ",
        "pix_texto": "Pixはブラジルの公的な即時決済インフラです。A1ELOSにとって、即時回収、低コスト、普遍的受け入れを保証します — ブラジル市場でのB2C事業の基盤であり、国際展開への入り口です。",
        "pix_kpis": [
            ("301億", "2025年の取引", "2024年比+20% · Febraban"),
            ("76.4%", "の人口がPixを使用", "ブラジル人2億1,100万人 · 中央銀行"),
            ("R$ 68.2兆", "2025年下半期の移動額", "784億件の取引 · 中央銀行"),
            ("約800億", "2025年の取引", "前年比+25.7% · Pixレポート"),
        ],
        "pix_fonte": "出典：ブラジル中央銀行（Pixの数字）とFebraban（銀行技術調査）。",
        "ref_titulo": "参考文献",
        "ref_intro": "このプレゼンテーションの市場データ、予測、指標に使用された出典。",
        "ref_lista": [
            ("Global Wellness Institute", "世界のウェルネス経済：6.8兆米ドル（2024）→ 9.8兆米ドル（2029）。"),
            ("MarkNtel Advisors", "占星術・数秘術アプリ：30億米ドル → 2030年までに90億米ドル（CAGR約20%）。"),
            ("IMF · 世界銀行", "国別のGDPと購買力平価（PPP）。"),
            ("ブラジル中央銀行", "Pixの公式統計：取引、ボリューム、ユーザー。"),
            ("Febraban", "銀行技術調査 — 2025年のPix成長。"),
            ("IBGE", "ブラジルの人口と社会経済指標。"),
        ],
        },           
           
"zh": {
        "titulo": "A1ELOS 全球数字命理学",
        "subtitulo": "数字科学，助您成功",
        "capa_nota": "面向投资者和合作伙伴的战略演示",
        "confidencial": "机密",
        "ano": "2026",
        "sumario_titulo": "执行摘要",
        "duns_porque": "为什么 DUNS 很重要？",
        "preco_consciente": "自觉定价",
        "idioma_col": "语言",
        "falantes_col": "使用者（百万）",
        "linhas_idiomas": [
           ["英语", "1,528"],
           ["普通话", "1,184"],
           ["西班牙语", "558"],
           ["法语", "396"],
           ["阿拉伯语", "335"],
           ["葡萄牙语", "270"],
           ["俄语", "255"],
           ["印度尼西亚语", "255"],
           ["德语", "134"],
           ["日语", "123"],
           ["越南语", "97"],
           ["土耳其语", "90"],
           ["意大利语", "85"],
           ["希伯来语", "9"],
        ],
        "total_linha": "总计",
        "fonte_receita": "收入来源",
        "participacao": "占比",
        "b2c_linha": "B2C — 14 种语言",
        "b2b_linha": "B2B — 渐进式折扣",
        "pub_linha": "地理定位广告",
        "tabela_descontos": "渐进式折扣表",
        "grafico_anos": ["第1年", "第3年", "第5年", "第7年", "第10年"],
        "grafico_titulo": "保守预测（R$ 千）",
        "grafico_titulo_linha": "预计增长（R$ 千）",
        "fale_conosco": "联系我们",
        "sumario_intro": "本演示旨在引导投资者和合作伙伴了解 A1ELOS 全球数字命理学的所有战略方面——从市场论点延伸到经常性收入模式。",
        "sumario_cards": [
            ("01", "关于 A1ELOS", "控股公司、产品组合和 DUNS 认证"),
            ("02", "市场机遇", "全球健康经济 6.8 万亿美元"),
            ("03", "解决方案与全球覆盖", "14 种语言，约 53 亿使用者"),
            ("04", "3 个新市场", "印度尼西亚、土耳其和越南"),
            ("05", "产品组合与定价", "按购买力校准的 23 款产品"),
            ("06", "经常性收入", "广告横幅和 B2B 套餐"),
            ("07", "预测与投资", "50 年展望 · 种子轮 R$ 350 万"),
        ],
        "sobre_titulo": "关于 A1ELOS",
        "sobre_texto": "A1ELOS 是一家技术与知识控股公司，融合人工智能、应用数字命理学和文化战略，在全球范围内创造高影响力的数字产品。我们的使命：以文化尊重和对每个市场购买力的尊重，实现数字自我认知的民主化。",
        "sobre_kpis": [
            ("23", "活跃产品", "4 个访问级别"),
            ("14", "语言", "约占世界人口的 67%"),
            ("53亿", "使用者", "真正的可及市场"),
            ("AI", "集成", "个性化引擎"),
        ],
        "sobre_duns": "DUNS 942242668 — Dun & Bradstreet 认证在 190 多个国家有效，可实现 B2B 合同和国际合资企业。",
        "duns_titulo": "国际信誉",
        "duns_texto": "DUNS 编号是 A1ELOS 在国际舞台上的企业护照。它向合作伙伴、企业客户和投资者表明，公司拥有可验证的身份、可追溯的历史以及在任何司法管辖区的合同能力。",
        "duns_numero": "942242668",
        "duns_emitido": "由 Dun & Bradstreet 颁发——在 190 多个国家获得认可的企业身份全球标准。",
        "duns_paises": "190+ 国家",
        "duns_beneficios": [
            ("B2B 合同", "国际招标和全球供应商资格"),
            ("合资企业", "尽职调查便捷的国际合作伙伴关系"),
            ("即时信誉", "对机构投资者认真态度的体现"),
        ],
        "mercado_titulo": "市场机遇",
        "mercado_texto": "我们正经历完美的融合：数字健康在全球爆发式增长，而数字命理学和占星术正迁移到高参与度应用中。A1ELOS 正位于这一交汇点，全球 74% 的人口已经在线（约 60 亿人）。",
        "mercado_cards": [
            ("全球健康", "6.8 万亿美元 → 2029 年达 9.8 万亿美元（年增 7.6%）"),
            ("占星/数字命理应用", "30 亿美元 → 2030 年达 90 亿美元 · CAGR 20%"),
            ("健康应用", "CAGR 14.9% → 2030 年达 262 亿美元"),
            ("在线用户", "占世界的 74% · 约 60 亿人"),
        ],
        "problema_titulo": "我们解决的问题",
        "problema_col_esq_titulo": "当前市场的缺陷",
        "problema_col_esq": [
            ("语言障碍", "绝大多数数字命理工具仅以英语运行，将其他语言的数十亿母语使用者排除在外。"),
            ("脱离现实的价格", "以美元定价面向新兴市场的产品造成经济排斥——用户拒绝的不是产品，而是无法承受的价格。"),
            ("缺乏深度", "通用工具提供肤浅的答案，没有个性化、没有文化背景、也没有对日常生活的实际应用。"),
        ],
        "problema_col_dir_titulo": "排斥的代价",
        "problema_col_dir": "当平台忽视语言和购买力时，它就自愿放弃了世界上最大的市场：生活在新兴经济体、讲非英语语言的 40 多亿人。这正是 A1ELOS 以精准方式占据的空白。",
        "problema_destaque": "忽视当地购买力的平台将失去全球可及市场 60% 以上的访问权。",
        "solucao_titulo": "我们的解决方案：3 大战略支柱",
        "solucao_texto": "A1ELOS 构建了一个集数字科学、人工智能和文化敏感性于一体的综合平台。该解决方案在三个互补方向运作，确保收入多元化和高留存率。",
        "solucao_colunas": [
            ("个人命盘", "为最终用户提供深入且个性化的数字分析——身份、使命、生命周期和兼容性——以集成 AI 提供 14 种语言版本。"),
            ("企业数字命理学", "应用于品牌、CNPJ、成立日期和企业战略的数字命理诊断。对 B2B 市场具有高感知价值的差异化产品。"),
            ("白标 B2B", "向希望以自有品牌提供数字命理服务的合作伙伴企业授权平台——提供多语言支持和完全定制。"),
        ],
        "alcance_titulo": "全球覆盖：14 种语言 · 约 53 亿使用者",
        "alcance_texto": "A1ELOS 通过真正多语言的平台覆盖约 67% 的世界人口。每种语言代表一个独特的文化市场，价格根据当地购买力进行校准。",
        "mercados_titulo": "3 个新市场：+4.42 亿使用者",
        "mercados_texto": "向印度尼西亚、土耳其和越南的战略扩张代表质的飞跃：这些市场经济增长强劲、数字普及率不断提高，且对可及的数字健康解决方案有成熟需求。",
        "mercados_cards": [
            ("印度尼西亚", ["2.85 亿居民", "互联网普及率 80.5%", "约 2.55 亿印度尼西亚语使用者", "健康：512 亿美元（2025）→ 728 亿美元（2034）"]),
            ("土耳其", ["8,590 万居民", "人均 GDP PPP 37,301 美元", "约 9,000 万土耳其语使用者", "高于世界平均水平（27,211 美元）"]),
            ("越南",  ["约 1 亿居民", "人均 GDP 约 5,066 美元（年增 7.4%）", "约 9,700 万越南语使用者", "健康：3.03 亿美元（2025）→ 4.85 亿美元（2030）"]),
        ],
        "mercados_rodape": "3 个新市场 = 新增 4.42 亿可及使用者——以文化校准的价格纳入平台。",
        "preco_titulo": "自觉定价理念",
        "preco_esq": "文化尊重 + 对购买力的尊重 = 真正的可及市场。相同的价值比例。不同的价格。对所有市场同等尊重。",
        "preco_dir_titulo": "实际运作方式",
        "preco_dir": "A1ELOS 将购买力平价（PPP）作为核心定价标准。同一产品为拉各斯、雅加达、河内或纽约的用户提供相同的相对价值——价格经过校准，使经济付出与当地收入成比例。",
        "preco_pilares": [
            ("PPP 校准", "根据各国购买力指数调整价格"),
            ("文化尊重", "语言、货币和当地背景融入产品"),
            ("卓越转化", "公平的价格带来更多转化和更高的长期留存"),
        ],
        "portfolio_titulo": "产品组合：4 个级别的 23 款产品",
        "portfolio_texto": "分层结构确保每个用户画像——从好奇者到专业人士——都能找到适合其参与度和财务能力的方案。",
        "portfolio_tabela": [
            ["级别", "产品", "价格区间（R$）", "画像"],
            ["基础", "快速命盘、完整命盘", "R$ 8 – 17", "好奇者，首次接触"],
            ["中级", "AI 搜索、选票名、选举编号", "R$ 26 – 53", "深度参与用户"],
            ["高级", "企业数字命理学、周期、使命", "R$ 81 – 109", "专业人士、创业者"],
            ["尊享", "完整诊断、个人命盘", "R$ 137 – 305", "高收入、企业使用"],
            ["B2B", "企业套餐、许可证、礼品", "待咨询", "企业和团队"],
        ],
        "portfolio_rodape": "23 款产品覆盖用户的完整旅程，从首次接触到经常性尊享客户——最大化每种语言和市场的 LTV。",
        "negocio_titulo": "商业模式：3 个收入来源",
        "negocio_texto": "A1ELOS 以多元化和可扩展的收入设计：面向最终消费者的全球直接销售、高价值 B2B 合同和经常性地理定位广告——三个相互促进的引擎。",
        "negocio_colunas": [
            ("B2C — 14 种语言", "以所有货币直接销售数字产品，按 PPP 调整价格。通过 AI 自动扩展——无需与增长成比例的支持团队。"),
            ("B2B — 渐进式折扣", "面向人力资源、雇主品牌和机构礼品的企业套餐。按数量提供 10% 至 50% 的折扣。超过 2,000 个代码，直接协商（钻石计划）。合同由 DUNS 942242668 支持。"),
            ("地理定位广告", "按国家、大陆或全球分段的横幅，自动轮换。高价值的经常性月收入——不依赖产品销量。"),
        ],
        "banners_titulo": "广告横幅 — 可预测的月收入",
        "banners_texto": "A1ELOS 的地理定位广告平台为广告主提供按国家、大陆或全球覆盖的精准分段，针对桌面和移动端优化格式，每 8 秒自动轮换。",
        "banners_tabela": [
            ["分段", "固定（R$/月）", "临时（R$/月）", "广告主画像"],
            ["国家", "R$ 800", "R$ 500", "本地中小企业、区域商业"],
            ["大陆", "R$ 1,800", "R$ 1,200", "区域品牌、大陆扩张"],
            ["全球", "R$ 3,500", "R$ 2,500", "全球企业、国际应用"],
            ["独家赞助", "R$ 6,000", "R$ 4,500/活动", "主赞助商、新品发布"],
        ],
        "banners_formatos": "728×90 px — 桌面中央横幅 · 320×100 px — 优化移动格式 · 8 秒 — 自动轮换 · 地理定位 — 国家、大陆或全球覆盖",
        "b2b_titulo": "B2B 企业套餐 — 高价值、高数量",
        "b2b_texto": "B2B 套餐将 A1ELOS 转变为雇主品牌和企业健康的工具。企业批量购买访问代码，作为礼品分发给员工或客户——由 DUNS 942242668 支持正式企业合同。",
        "b2b_planos": [
            ("基础套餐 · 50 个代码", "50× 快速命盘（每个 R$ 8）。适合员工福利计划和整合活动。"),
            ("中级套餐 · 100 个代码", "50× 快速命盘 + 50× AI 搜索（R$ 17）。适合团队和雇主品牌战略。"),
            ("尊享套餐 · 200 个代码", "100× 快速命盘 + 100× 完整命盘（R$ 17）。为大型团体提供最大分析深度。"),
        ],
        "b2b_tabela": [
            ["从", "折扣", "画像", "推荐用途"],
            ["10 个代码", "10%", "小型团队", "一次性健康活动"],
            ["50 个代码", "20%", "成长中的团队", "经常性计划"],
            ["100 个代码", "25%", "中小企业", "季度福利"],
            ["200 个代码", "30%", "中型企业", "完整计划"],
            ["500 个代码", "40%", "中型企业", "员工年度礼品"],
            ["1,000 个代码", "45%", "大型企业", "客户忠诚度"],
            ["2,000 个代码", "50%", "大型集团", "大规模"],
            ["超过 2,000", "可协商", "定制钻石计划", "批量奖金分发"],
        ],
        "projecoes_titulo": "财务预测：50 年展望",
        "projecoes_texto": "预测基于对约 53.2 亿使用者潜在市场的百分比渗透率估算，采用保守的 3% 转化率和 70% 至 90% 的奖金兑换率。第一个十年在第 1、3、5 和 7 年详细展示，以突出发展势头。",
        "projecoes_tabela": [
            ["展望", "保守（R$）", "乐观（R$）"],
            ["第1年", "R$ 281k", "R$ 702k"],
            ["第3年", "R$ 983k", "R$ 280万"],
            ["第5年", "R$ 280万", "R$ 700万"],
            ["第7年", "R$ 560万", "R$ 1,400万"],
            ["第10年", "R$ 1,120万", "R$ 2,810万"],
            ["第20年", "R$ 4,210万", "R$ 1.12亿"],
            ["第30年", "R$ 8,430万", "R$ 2.11亿"],
            ["第40年", "R$ 1.26亿", "R$ 3.51亿"],
            ["第50年", "R$ 1.69亿", "R$ 4.92亿"],
        ],
        "tracao_titulo": "牵引力与已验证的成果",
        "tracao_texto": "A1ELOS 已经以验证模型的指标运营——高留存率、尊享评级和不断增长的 B2B 合作伙伴基础表明，该平台为最终用户和企业市场提供了真正的价值。",
        "tracao_kpis": [
            ("12K+", "活跃用户", "持续增长的有机基础"),
            ("87%", "留存率", "远高于行业平均水平（约 30%）"),
            ("4.8★", "平均评分", "经验证的最终用户满意度"),
            ("23", "B2B 合作伙伴", "与企业及人力资源部门签订的活跃合同"),
        ],
        "roteiro_titulo": "战略路线图",
        "roteiro_texto": "A1ELOS 分四个渐进阶段执行计划——从整合现有基础到全球市场领导地位，为投资者提供清晰的退出选项。",
        "roteiro_fases": [
            ("阶段 1 · 整合", "加强已活跃语言的用户基础。优化转化率、留存率和 LTV。种子轮已完成。"),
            ("阶段 2 · 扩张", "在 3 个新市场正式推出：印度尼西亚、土耳其和越南。加速 B2B 渠道和地理定位广告。"),
            ("阶段 3 · 全球进入", "以本地化活动在全部 14 种语言中积极存在。在 5 大洲以上建立白标合作伙伴关系。A 轮融资。"),
            ("阶段 4 · 领导地位", "在 20 多个国家拥有整合运营。应用数字命理学领域的全球参考 SaaS 平台。IPO 或战略退出。"),
        ],
        "invest_titulo": "投资与联系",
        "invest_texto": "我们已准备好进行私人演示、尽职调查和谈判。请通过您偏好的渠道联系我们。",
        "invest_dados": [
            ("种子轮", "R$ 350 万"),
            ("投前估值", "R$ 1,400 万"),
            ("提供股权", "最高 20%"),
        ],
        "invest_contato": [
            ("投资者邮箱", "a1elos.consultoria@gmail.com"),
            ("一般邮箱", "contato@a1elos.com"),
            ("网站", "www.a1elos.com"),
            ("DUNS", "942242668 — Dun & Bradstreet"),
        ],
        "invest_alocacao": "资本配置：45% 技术 · 30% 营销 · 25% 运营",
        "frase_final": "数字从不撒谎。",
        "selo_final": ["DUNS 942242668", "23 款产品", "14 种语言", "约 53 亿使用者"],
        "graf_cons": "保守",
        "graf_otim": "乐观",
        "grafico_titulo_linha": "预计增长（R$ 千）",
        "pix_titulo": "巴西：Pix 基础设施",
        "pix_texto": "Pix 是巴西的公共即时支付基础设施。对 A1ELOS 而言，它保证即时收款、低成本、普遍接受——是巴西市场 B2C 运营的基础，也是国际扩张的入口。",
        "pix_kpis": [
            ("301 亿", "2025 年交易", "比 2024 年增长 20% · Febraban"),
            ("76.4%", "的人口使用 Pix", "2.11 亿巴西人 · 中央银行"),
            ("R$ 68.2 万亿", "2025 年下半年流动额", "784 亿笔交易 · 中央银行"),
            ("约 800 亿", "2025 年交易", "比上年增长 25.7% · Pix 报告"),
        ],
        "pix_fonte": "来源：巴西中央银行（Pix 数据）和 Febraban（银行技术调查）。",
        "ref_titulo": "参考文献",
        "ref_intro": "本演示的市场数据、预测和指标所使用的来源。",
        "ref_lista": [
            ("Global Wellness Institute", "全球健康经济：6.8 万亿美元（2024）→ 9.8 万亿美元（2029）。"),
            ("MarkNtel Advisors", "占星和数字命理应用：30 亿美元 → 2030 年达 90 亿美元（CAGR 约 20%）。"),
            ("IMF · 世界银行", "按国家划分的 GDP 和购买力平价（PPP）。"),
            ("巴西中央银行", "Pix 官方统计：交易、数量和用户。"),
            ("Febraban", "银行技术调查——2025 年 Pix 增长。"),
            ("IBGE", "巴西人口和社会经济指标。"),
        ],
        },
           
"ru": {
        "titulo": "A1ELOS Глобальная Нумерология",
        "subtitulo": "Наука чисел, применённая к вашему успеху",
        "capa_nota": "Стратегическая презентация для инвесторов и партнёров",
        "confidencial": "КОНФИДЕНЦИАЛЬНО",
        "ano": "2026",
        "sumario_titulo": "Краткое резюме",
        "duns_porque": "Почему важен DUNS?",
        "preco_consciente": "Осознанное ценообразование",
        "idioma_col": "Язык",
        "falantes_col": "Говорящие (млн)",
        "linhas_idiomas": [
           ["Английский", "1 528"],
           ["Мандарин", "1 184"],
           ["Испанский", "558"],
           ["Французский", "396"],
           ["Арабский", "335"],
           ["Португальский", "270"],
           ["Русский", "255"],
           ["Индонезийский", "255"],
           ["Немецкий", "134"],
           ["Японский", "123"],
           ["Вьетнамский", "97"],
           ["Турецкий", "90"],
           ["Итальянский", "85"],
           ["Иврит", "9"],
        ],
        "total_linha": "ИТОГО",
        "fonte_receita": "Источник дохода",
        "participacao": "Доля",
        "b2c_linha": "B2C — 14 языков",
        "b2b_linha": "B2B — Прогрессивные скидки",
        "pub_linha": "Геолокализованная реклама",
        "tabela_descontos": "Таблица прогрессивных скидок",
        "grafico_anos": ["Год 1", "Год 3", "Год 5", "Год 7", "Год 10"],
        "grafico_titulo": "Консервативный прогноз (R$ тыс.)",
        "grafico_titulo_linha": "Прогнозируемый рост (R$ тыс.)",
        "fale_conosco": "Свяжитесь с нами",
        "sumario_intro": "Эта презентация структурирована, чтобы провести инвесторов и партнёров через все стратегические аспекты A1ELOS Глобальная Нумерология — от рыночной тезиса до модели повторяющегося дохода.",
        "sumario_cards": [
            ("01", "О A1ELOS", "Холдинг, портфель и сертификат DUNS"),
            ("02", "Рыночная возможность", "Мировая экономика благополучия 6,8 трлн долл."),
            ("03", "Решение и глобальный охват", "14 языков, ~5,3 млрд говорящих"),
            ("04", "3 новых рынка", "Индонезия, Турция и Вьетнам"),
            ("05", "Портфель и цены", "23 продукта, откалиброванных по покупательной способности"),
            ("06", "Повторяющийся доход", "Рекламные баннеры и B2B-пакеты"),
            ("07", "Прогнозы и инвестиции", "Горизонт 50 лет · Посевной раунд R$ 3,5 млн"),
        ],
        "sobre_titulo": "О A1ELOS",
        "sobre_texto": "A1ELOS — это холдинг технологий и знаний, объединяющий искусственный интеллект, прикладную нумерологию и культурную стратегию для создания цифровых продуктов с высоким влиянием в глобальном масштабе. Наша миссия: демократизировать численное самопознание с уважением к культуре и покупательной способности каждого рынка.",
        "sobre_kpis": [
            ("23", "Активных продуктов", "В 4 уровнях доступа"),
            ("14", "Языков", "~67% населения мира"),
            ("5,3 млрд", "Говорящих", "Реальный адресуемый рынок"),
            ("ИИ", "Интегрирован", "Двигатель персонализации"),
        ],
        "sobre_duns": "DUNS 942242668 — Сертификация Dun & Bradstreet, действительная в более чем 190 странах, позволяющая заключать B2B-контракты и международные совместные предприятия.",
        "duns_titulo": "Международная репутация",
        "duns_texto": "Номер DUNS — это корпоративный паспорт A1ELOS на международной арене. Он сигнализирует партнёрам, корпоративным клиентам и инвесторам, что компания обладает проверяемой идентичностью, прослеживаемой историей и контрактной способностью в любой юрисдикции.",
        "duns_numero": "942242668",
        "duns_emitido": "Выдан Dun & Bradstreet — глобальным стандартом корпоративной идентичности, признанным в более чем 190 странах.",
        "duns_paises": "190+ СТРАН",
        "duns_beneficios": [
            ("B2B-контракты", "Квалификация для тендеров и глобальных поставщиков"),
            ("Совместные предприятия", "Международные партнёрства с облегчённой комплексной проверкой"),
            ("Немедленная репутация", "Признак серьёзности для институциональных инвесторов"),
        ],
        "mercado_titulo": "Рыночная возможность",
        "mercado_texto": "Мы переживаем идеальную конвергенцию: цифровое благополучие взрывается во всём мире, в то время как нумерология и астрология переходят в приложения с высоким вовлечением. A1ELOS находится точно на этом пересечении: 74% населения мира уже онлайн (~6 млрд человек).",
        "mercado_cards": [
            ("Глобальное благополучие", "6,8 трлн долл. → 9,8 трлн долл. к 2029 году (+7,6% в год)"),
            ("Приложения астрологии/нумерологии", "3 млрд долл. → 9 млрд долл. к 2030 году · CAGR 20%"),
            ("Приложения благополучия", "CAGR 14,9% → 26,2 млрд долл. в 2030 году"),
            ("Онлайн-пользователи", "74% мира · ~6 млрд человек"),
        ],
        "problema_titulo": "Проблема, которую мы решаем",
        "problema_col_esq_titulo": "Недостатки текущего рынка",
        "problema_col_esq": [
            ("Языковой барьер", "Подавляющее большинство инструментов нумерологии работает только на английском, исключая миллиарды носителей других языков."),
            ("Цены, оторванные от реальности", "Продукты, оцениваемые в долларах для развивающихся рынков, создают экономическую изоляцию — пользователь отвергает не продукт, а недоступную цену."),
            ("Отсутствие глубины", "Общие инструменты дают поверхностные ответы без персонализации, без культурного контекста и без практического применения в повседневной жизни."),
        ],
        "problema_col_dir_titulo": "Цена изоляции",
        "problema_col_dir": "Когда платформа игнорирует язык и покупательную способность, она добровольно отказывается от крупнейшего рынка мира: более 4 млрд человек, живущих в развивающихся экономиках и говорящих на неанглоязычных языках. Именно эту нишу A1ELOS занимает с хирургической точностью.",
        "problema_destaque": "Платформы, игнорирующие местную покупательную способность, теряют доступ к более чем 60% глобального адресуемого рынка.",
        "solucao_titulo": "Наше решение: 3 стратегических столпа",
        "solucao_texto": "A1ELOS построила интегрированную платформу, сочетающую численную науку, искусственный интеллект и культурную чувствительность. Решение работает на трёх взаимодополняющих направлениях, обеспечивая диверсифицированный доход и высокое удержание.",
        "solucao_colunas": [
            ("Личные карты", "Глубокие и персонализированные численные анализы для конечного пользователя — идентичность, миссия, жизненные циклы и совместимость — на 14 языках с интегрированным ИИ."),
            ("Бизнес-нумерология", "Нумерологические диагностики для брендов, CNPJ, дат основания и корпоративной стратегии. Дифференцированный продукт с высокой воспринимаемой ценностью для B2B-рынка."),
            ("White-Label B2B", "Лицензирование платформы для компаний-партнёров, желающих предлагать нумерологию под собственным брендом — с многоязычной поддержкой и полной настройкой."),
        ],
        "alcance_titulo": "Глобальный охват: 14 языков · ~5,3 млрд говорящих",
        "alcance_texto": "A1ELOS охватывает ~67% населения мира с по-настоящему многоязычной платформой. Каждый язык представляет отдельный культурный рынок с ценами, откалиброванными по местной покупательной способности.",
        "mercados_titulo": "3 новых рынка: +442 млн говорящих",
        "mercados_texto": "Стратегическое расширение в Индонезию, Турцию и Вьетнам представляет качественный скачок: рынки с высоким экономическим ростом, растущим цифровым проникновением и доказанным спросом на доступные цифровые решения благополучия.",
        "mercados_cards": [
            ("Индонезия", ["285 млн жителей", "80,5% проникновения интернета", "~255 млн говорящих на индонезийском", "Благополучие: 51,2 млрд долл. (2025) → 72,8 млрд долл. (2034)"]),
            ("Турция", ["85,9 млн жителей", "ВВП ППС на душу населения 37 301 долл.", "~90 млн говорящих на турецком", "Выше мирового среднего (27 211 долл.)"]),
            ("Вьетнам",  ["~100 млн жителей", "ВВП на душу населения ~5 066 долл. (+7,4%/год)", "~97 млн говорящих на вьетнамском", "Благополучие: 303 млн долл. (2025) → 485 млн долл. (2030)"]),
        ],
        "mercados_rodape": "3 новых рынка = +442 млн новых адресуемых говорящих — включены в платформу с культурно откалиброванными ценами.",
        "preco_titulo": "Философия осознанного ценообразования",
        "preco_esq": "Уважение к культуре + уважение к покупательной способности = реальный адресуемый рынок. Та же пропорция ценности. Разные цены. Равное достоинство для всех рынков.",
        "preco_dir_titulo": "Как это работает на практике",
        "preco_dir": "A1ELOS применяет паритет покупательной способности (ППС) как центральный критерий ценообразования. Тот же продукт даёт пользователю одинаковую относительную ценность в Лагосе, Джакарте, Ханое или Нью-Йорке — цена откалибрована так, чтобы финансовое усилие было пропорционально местному доходу.",
        "preco_pilares": [
            ("Калибровка по ППС", "Цены, скорректированные по индексу покупательной способности каждой страны"),
            ("Уважение к культуре", "Язык, валюта и местный контекст, интегрированные в продукт"),
            ("Превосходная конверсия", "Справедливая цена даёт больше конверсии и более высокое долгосрочное удержание"),
        ],
        "portfolio_titulo": "Портфель: 23 продукта в 4 уровнях",
        "portfolio_texto": "Многоуровневая структура гарантирует, что каждый профиль пользователя — от любопытного до профессионала — найдёт предложение, соответствующее его уровню вовлечённости и финансовым возможностям.",
        "portfolio_tabela": [
            ["Уровень", "Продукты", "Диапазон цен (R$)", "Профиль"],
            ["Базовый", "Экспресс-карта, Полная карта", "R$ 8 – 17", "Любопытный, первый контакт"],
            ["Средний", "ИИ-поиск, Имя для бюллетеня, Избирательный №", "R$ 26 – 53", "Вовлечённый пользователь"],
            ["Продвинутый", "Бизнес-нумерология, Циклы, Миссия", "R$ 81 – 109", "Профессионал, предприниматель"],
            ["Премиум", "Полные диагностики, Личные карты", "R$ 137 – 305", "Высокий доход, корпоративное использование"],
            ["B2B", "Бизнес-пакеты, лицензии, подарки", "По запросу", "Компании и команды"],
        ],
        "portfolio_rodape": "23 продукта покрывают весь путь пользователя — от первого контакта до повторяющегося премиум-клиента, максимизируя LTV по каждому языку и рынку.",
        "negocio_titulo": "Бизнес-модель: 3 источника дохода",
        "negocio_texto": "A1ELOS спроектирована с диверсифицированным и масштабируемым доходом: прямые продажи конечному потребителю в глобальном масштабе, высокоценные B2B-контракты и повторяющаяся геолокализованная реклама — три двигателя, которые питают друг друга.",
        "negocio_colunas": [
            ("B2C — 14 языков", "Прямая продажа цифровых продуктов во всех валютах с ценами, адаптированными по ППС. Автоматическое масштабирование через ИИ — без команды поддержки, пропорциональной росту."),
            ("B2B — Прогрессивные скидки", "Корпоративные пакеты для HR, employer branding и институциональных подарков. Скидки от 10% до 50% в зависимости от объёма. Свыше 2 000 кодов — прямые переговоры (План «Бриллиант»). Контракты поддерживаются DUNS 942242668."),
            ("Геолокализованная реклама", "Баннеры, сегментированные по стране, континенту или миру, с автоматической ротацией. Высокоценный повторяющийся ежемесячный доход — без зависимости от объёма продаж продукта."),
        ],
        "banners_titulo": "Рекламные баннеры — предсказуемый ежемесячный доход",
        "banners_texto": "Геолокализованная рекламная платформа A1ELOS предлагает рекламодателям точную сегментацию по стране, континенту или глобальному охвату, с форматами, оптимизированными для desktop и mobile, и автоматической ротацией каждые 8 секунд.",
        "banners_tabela": [
            ["Сегментация", "Фиксированный (R$/мес.)", "Временный (R$/мес.)", "Профиль рекламодателя"],
            ["Страна", "R$ 800", "R$ 500", "Местные МСП, региональная торговля"],
            ["Континент", "R$ 1 800", "R$ 1 200", "Региональные бренды, континентальная экспансия"],
            ["Мир", "R$ 3 500", "R$ 2 500", "Глобальные компании, международные приложения"],
            ["Эксклюзивное спонсорство", "R$ 6 000", "R$ 4 500/кампания", "Мастер-спонсоры, запуски"],
        ],
        "banners_formatos": "728×90 px — Центральный desktop-баннер · 320×100 px — Оптимизированный мобильный формат · 8 секунд — Автоматическая ротация · Гео-таргетинг — Страна, континент или мировой охват",
        "b2b_titulo": "B2B-бизнес-пакеты — высокая ценность, высокий объём",
        "b2b_texto": "B2B-пакеты превращают A1ELOS в инструмент employer branding и корпоративного благополучия. Компании приобретают коды доступа оптом для распространения в качестве подарков сотрудникам или клиентам — поддерживаемые DUNS 942242668 для официальных корпоративных контрактов.",
        "b2b_planos": [
            ("Базовый план · 50 кодов", "50× Экспресс-карта (R$ 8 каждый). Идеален для программ льгот сотрудникам и интеграционных мероприятий."),
            ("Средний план · 100 кодов", "50× Экспресс-карта + 50× ИИ-поиск (R$ 17). Идеален для команд и стратегии employer branding."),
            ("Премиум-план · 200 кодов", "100× Экспресс-карта + 100× Полная карта (R$ 17). Максимальная аналитическая глубина для больших групп."),
        ],
        "b2b_tabela": [
            ["От", "Скидка", "Профиль", "Рекомендуемое использование"],
            ["10 кодов", "10%", "Небольшие команды", "Разовое мероприятие благополучия"],
            ["50 кодов", "20%", "Растущие команды", "Повторяющиеся программы"],
            ["100 кодов", "25%", "МСП", "Квартальная льгота"],
            ["200 кодов", "30%", "Средние компании", "Полные программы"],
            ["500 кодов", "40%", "Средние компании", "Ежегодный подарок сотрудникам"],
            ["1 000 кодов", "45%", "Крупные компании", "Лояльность клиентов"],
            ["2 000 кодов", "50%", "Крупные группы", "Крупный масштаб"],
            ["Свыше 2 000", "Договорно", "Индивидуальный план «Бриллиант»", "Распределение бонусов оптом"],
        ],
        "projecoes_titulo": "Финансовые прогнозы: горизонт 50 лет",
        "projecoes_texto": "Прогнозы построены на основе процентных оценок проникновения на потенциальный рынок ~5,32 млрд говорящих, с консервативной конверсией 3% и выкупом бонусов от 70% до 90%. Первое десятилетие детализировано по годам 1, 3, 5 и 7, чтобы подчеркнуть динамику.",
        "projecoes_tabela": [
            ["Горизонт", "Консервативный (R$)", "Оптимистичный (R$)"],
            ["Год 1", "R$ 281 тыс.", "R$ 702 тыс."],
            ["Год 3", "R$ 983 тыс.", "R$ 2,8 млн"],
            ["Год 5", "R$ 2,8 млн", "R$ 7 млн"],
            ["Год 7", "R$ 5,6 млн", "R$ 14 млн"],
            ["Год 10", "R$ 11,2 млн", "R$ 28,1 млн"],
            ["Год 20", "R$ 42,1 млн", "R$ 112 млн"],
            ["Год 30", "R$ 84,3 млн", "R$ 211 млн"],
            ["Год 40", "R$ 126 млн", "R$ 351 млн"],
            ["Год 50", "R$ 169 млн", "R$ 492 млн"],
        ],
        "tracao_titulo": "Тяга и доказанные результаты",
        "tracao_texto": "A1ELOS уже работает с продуктовыми метриками, которые подтверждают модель — высокое удержание, премиальная оценка и растущая база B2B-партнёров демонстрируют, что платформа приносит реальную ценность конечному пользователю и корпоративному рынку.",
        "tracao_kpis": [
            ("12K+", "Активных пользователей", "Последовательно растущая органическая база"),
            ("87%", "Удержание", "Намного выше среднего по отрасли (~30%)"),
            ("4,8★", "Средняя оценка", "Доказанная удовлетворённость конечного пользователя"),
            ("23", "B2B-партнёра", "Активные контракты с компаниями и HR"),
        ],
        "roteiro_titulo": "Стратегическая дорожная карта",
        "roteiro_texto": "A1ELOS выполняет план в четыре последовательные фазы — от консолидации текущей базы до глобального лидерства на рынке, с чёткими вариантами выхода для инвесторов.",
        "roteiro_fases": [
            ("Фаза 1 · Консолидация", "Укрепление базы пользователей на уже активных языках. Оптимизация конверсии, удержания и LTV. Посевной раунд завершён."),
            ("Фаза 2 · Расширение", "Официальный запуск на 3 новых рынках: Индонезия, Турция и Вьетнам. Ускорение B2B-канала и геолокализованной рекламы."),
            ("Фаза 3 · Глобальный вход", "Активное присутствие на всех 14 языках с локализованными кампаниями. White-label-партнёрства на 5+ континентах. Серия A."),
            ("Фаза 4 · Лидерство", "Более 20 стран с консолидированными операциями. Глобальная эталонная SaaS-платформа в прикладной нумерологии. IPO или стратегический выход."),
        ],
        "invest_titulo": "Инвестиции и контакты",
        "invest_texto": "Мы готовы к частным презентациям, комплексной проверке и переговорам. Свяжитесь с нами через предпочитаемый вами канал.",
        "invest_dados": [
            ("Посевной раунд", "R$ 3,5 млн"),
            ("Оценка до инвестиций", "R$ 14 млн"),
            ("Предлагаемый капитал", "До 20%"),
        ],
        "invest_contato": [
            ("Email инвесторов", "a1elos.consultoria@gmail.com"),
            ("Общий email", "contato@a1elos.com"),
            ("Веб-сайт", "www.a1elos.com"),
            ("DUNS", "942242668 — Dun & Bradstreet"),
        ],
        "invest_alocacao": "Распределение капитала: 45% Технологии · 30% Маркетинг · 25% Операции",
        "frase_final": "Числа никогда не лгут.",
        "selo_final": ["DUNS 942242668", "23 ПРОДУКТА", "14 ЯЗЫКОВ", "~5,3 МЛРД ГОВОРЯЩИХ"],
        "graf_cons": "Консервативный",
        "graf_otim": "Оптимистичный",
        "grafico_titulo_linha": "Прогнозируемый рост (R$ тыс.)",
        "pix_titulo": "Бразилия: инфраструктура Pix",
        "pix_texto": "Pix — это государственная инфраструктура мгновенных платежей Бразилии. Для A1ELOS она гарантирует немедленное получение средств, низкую стоимость и универсальное принятие — основу B2C-операции на бразильском рынке и ворота к международному расширению.",
        "pix_kpis": [
            ("30,1 млрд", "Транзакций в 2025 году", "+20% к 2024 · Febraban"),
            ("76,4%", "населения использует Pix", "211 млн бразильцев · Центральный банк"),
            ("R$ 68,2 трлн", "движение во 2-м полугодии 2025", "78,4 млрд транзакций · Центральный банк"),
            ("~80 млрд", "транзакций в 2025 году", "+25,7% к предыдущему году · Отчёт Pix"),
        ],
        "pix_fonte": "Источники: Центральный банк Бразилии (Pix в цифрах) и Febraban (Исследование банковских технологий).",
        "ref_titulo": "Библиографические ссылки",
        "ref_intro": "Источники, использованные для рыночных данных, прогнозов и показателей этой презентации.",
        "ref_lista": [
            ("Global Wellness Institute", "Мировая экономика благополучия: 6,8 трлн долл. (2024) → 9,8 трлн долл. (2029)."),
            ("MarkNtel Advisors", "Приложения астрологии и нумерологии: 3 млрд долл. → 9 млрд долл. к 2030 году (CAGR ~20%)."),
            ("МВФ · Всемирный банк", "ВВП и паритет покупательной способности (ППС) по странам."),
            ("Центральный банк Бразилии", "Официальная статистика Pix: транзакции, объём и пользователи."),
            ("Febraban", "Исследование банковских технологий — рост Pix в 2025 году."),
            ("IBGE", "Население и социально-экономические показатели Бразилии."),
        ],
        },

"id": {
        "titulo": "A1ELOS Numerologi Global",
        "subtitulo": "Ilmu angka diterapkan pada kesuksesan Anda",
        "capa_nota": "Presentasi Strategis untuk Investor dan Mitra",
        "confidencial": "RAHASIA",
        "ano": "2026",
        "sumario_titulo": "Ringkasan Eksekutif",
        "duns_porque": "Mengapa DUNS penting?",
        "preco_consciente": "Harga Sadar",
        "idioma_col": "Bahasa",
        "falantes_col": "Penutur (juta)",
        "linhas_idiomas": [
           ["Inggris", "1.528"],
           ["Mandarin", "1.184"],
           ["Spanyol", "558"],
           ["Prancis", "396"],
           ["Arab", "335"],
           ["Portugis", "270"],
           ["Rusia", "255"],
           ["Indonesia", "255"],
           ["Jerman", "134"],
           ["Jepang", "123"],
           ["Vietnam", "97"],
           ["Turki", "90"],
           ["Italia", "85"],
           ["Ibrani", "9"],
        ],
        "total_linha": "TOTAL",
        "fonte_receita": "Sumber Pendapatan",
        "participacao": "Pangsa",
        "b2c_linha": "B2C — 14 Bahasa",
        "b2b_linha": "B2B — Diskon Progresif",
        "pub_linha": "Iklan Geolokasi",
        "tabela_descontos": "Tabel Diskon Progresif",
        "grafico_anos": ["Tahun 1", "Tahun 3", "Tahun 5", "Tahun 7", "Tahun 10"],
        "grafico_titulo": "Proyeksi Konservatif (R$ ribu)",
        "grafico_titulo_linha": "Pertumbuhan Diproyeksikan (R$ ribu)",
        "fale_conosco": "Hubungi Kami",
        "sumario_intro": "Presentasi ini disusun untuk memandu investor dan mitra melalui semua aspek strategis A1ELOS Numerologi Global — dari tesis pasar hingga model pendapatan berulang.",
        "sumario_cards": [
            ("01", "Tentang A1ELOS", "Holding, portofolio dan kredensial DUNS"),
            ("02", "Peluang Pasar", "Ekonomi kesejahteraan global US$ 6,8 triliun"),
            ("03", "Solusi dan Jangkauan Global", "14 bahasa, ~5,3 miliar penutur"),
            ("04", "3 Pasar Baru", "Indonesia, Turki dan Vietnam"),
            ("05", "Portofolio dan Harga", "23 produk dikalibrasi berdasarkan daya beli"),
            ("06", "Pendapatan Berulang", "Banner iklan dan Paket B2B"),
            ("07", "Proyeksi dan Investasi", "Cakrawala 50 tahun · Putaran Seed R$ 3,5 juta"),
        ],
        "sobre_titulo": "Tentang A1ELOS",
        "sobre_texto": "A1ELOS adalah holding teknologi dan pengetahuan yang menggabungkan kecerdasan buatan, numerologi terapan dan strategi budaya untuk menciptakan produk digital berdampak tinggi dalam skala global. Misi kami: mendemokratisasi pengetahuan diri numerik dengan rasa hormat budaya dan rasa hormat terhadap daya beli setiap pasar.",
        "sobre_kpis": [
            ("23", "Produk Aktif", "Dalam 4 tingkat akses"),
            ("14", "Bahasa", "~67% populasi dunia"),
            ("5,3 M", "Penutur", "Pasar yang dapat dijangkau nyata"),
            ("AI", "Terintegrasi", "Mesin personalisasi"),
        ],
        "sobre_duns": "DUNS 942242668 — Sertifikasi Dun & Bradstreet berlaku di lebih dari 190 negara, memungkinkan kontrak B2B dan joint venture internasional.",
        "duns_titulo": "Kredibilitas Internasional",
        "duns_texto": "Nomor DUNS adalah paspor korporat A1ELOS di panggung internasional. Ini memberi sinyal kepada mitra, klien korporat dan investor bahwa perusahaan memiliki identitas yang dapat diverifikasi, sejarah yang dapat dilacak dan kapasitas kontraktual di yurisdiksi mana pun.",
        "duns_numero": "942242668",
        "duns_emitido": "Diterbitkan oleh Dun & Bradstreet — standar global identitas bisnis yang diakui di lebih dari 190 negara.",
        "duns_paises": "190+ NEGARA",
        "duns_beneficios": [
            ("Kontrak B2B", "Kualifikasi untuk tender dan pemasok global"),
            ("Joint Venture", "Kemitraan internasional dengan due diligence yang difasilitasi"),
            ("Kredibilitas Segera", "Tanda keseriusan bagi investor institusional"),
        ],
        "mercado_titulo": "Peluang Pasar",
        "mercado_texto": "Kita hidup dalam konvergensi sempurna: kesejahteraan digital meledak secara global sementara numerologi dan astrologi bermigrasi ke aplikasi berinteraksi tinggi. A1ELOS diposisikan tepat di persimpangan ini, dengan 74% populasi dunia sudah online (~6 miliar orang).",
        "mercado_cards": [
            ("Kesejahteraan Global", "US$ 6,8 triliun → US$ 9,8 triliun pada 2029 (+7,6% per tahun)"),
            ("Aplikasi Astrologi/Numerologi", "US$ 3 miliar → US$ 9 miliar pada 2030 · CAGR 20%"),
            ("Aplikasi Kesejahteraan", "CAGR 14,9% → US$ 26,2 miliar pada 2030"),
            ("Pengguna Online", "74% dunia · ~6 miliar orang"),
        ],
        "problema_titulo": "Masalah yang Kami Selesaikan",
        "problema_col_esq_titulo": "Kegagalan Pasar Saat Ini",
        "problema_col_esq": [
            ("Hambatan Bahasa", "Sebagian besar alat numerologi hanya beroperasi dalam bahasa Inggris, mengecualikan miliaran penutur asli dalam bahasa lain."),
            ("Harga Tidak Sesuai Realitas", "Produk yang dihargai dalam dolar untuk pasar berkembang menciptakan eksklusi ekonomi — pengguna tidak menolak produknya, melainkan harga yang tidak terjangkau."),
            ("Kurang Kedalaman", "Alat generik memberikan jawaban dangkal tanpa personalisasi, tanpa konteks budaya dan tanpa aplikasi praktis dalam kehidupan sehari-hari."),
        ],
        "problema_col_dir_titulo": "Biaya Eksklusi",
        "problema_col_dir": "Ketika platform mengabaikan bahasa dan daya beli, ia secara sukarela meninggalkan pasar terbesar di dunia: lebih dari 4 miliar orang yang hidup di ekonomi berkembang dan berbicara bahasa non-Anglophone. Ini adalah celah yang A1ELOS isi dengan presisi bedah.",
        "problema_destaque": "Platform yang mengabaikan daya beli lokal kehilangan akses ke lebih dari 60% pasar global yang dapat dijangkau.",
        "solucao_titulo": "Solusi Kami: 3 Pilar Strategis",
        "solucao_texto": "A1ELOS membangun platform terintegrasi yang menggabungkan ilmu angka, kecerdasan buatan dan kepekaan budaya. Solusi ini beroperasi pada tiga lini yang saling melengkapi, menjamin pendapatan yang beragam dan retensi tinggi.",
        "solucao_colunas": [
            ("Peta Pribadi", "Analisis numerik yang dalam dan personal untuk pengguna akhir — identitas, misi, siklus hidup dan kompatibilitas — disampaikan dalam 14 bahasa dengan AI terintegrasi."),
            ("Numerologi Bisnis", "Diagnosis numerologi yang diterapkan pada merek, CNPJ, tanggal pendirian dan strategi korporat. Produk terdiferensiasi bernilai tinggi yang dirasakan pasar B2B."),
            ("White-Label B2B", "Lisensi platform untuk perusahaan mitra yang ingin menawarkan numerologi di bawah merek mereka sendiri — dengan dukungan multibahasa dan personalisasi lengkap."),
        ],
        "alcance_titulo": "Jangkauan Global: 14 Bahasa · ~5,3 Miliar Penutur",
        "alcance_texto": "A1ELOS mencakup ~67% populasi dunia dengan platform yang benar-benar multibahasa. Setiap bahasa mewakili pasar budaya yang berbeda, dengan harga yang dikalibrasi ke daya beli lokal.",
        "mercados_titulo": "3 Pasar Baru: +442 Juta Penutur",
        "mercados_texto": "Ekspansi strategis ke Indonesia, Turki dan Vietnam mewakili lompatan kualitatif: pasar dengan pertumbuhan ekonomi tinggi, penetrasi digital yang meningkat dan permintaan terbukti akan solusi kesejahteraan digital yang terjangkau.",
        "mercados_cards": [
            ("Indonesia", ["285 juta penduduk", "80,5% penetrasi internet", "~255 juta penutur bahasa Indonesia", "Kesejahteraan: US$ 51,2 miliar (2025) → US$ 72,8 miliar (2034)"]),
            ("Turki", ["85,9 juta penduduk", "PDB PPP per kapita US$ 37.301", "~90 juta penutur bahasa Turki", "Di atas rata-rata dunia (US$ 27.211)"]),
            ("Vietnam",  ["~100 juta penduduk", "PDB per kapita ~US$ 5.066 (+7,4%/tahun)", "~97 juta penutur bahasa Vietnam", "Kesejahteraan: US$ 303 juta (2025) → US$ 485 juta (2030)"]),
        ],
        "mercados_rodape": "3 pasar baru = +442 juta penutur baru yang dapat dijangkau — diintegrasikan ke platform dengan harga yang dikalibrasi secara budaya.",
        "preco_titulo": "Filosofi Harga Sadar",
        "preco_esq": "Rasa hormat budaya + rasa hormat terhadap daya beli = pasar yang dapat dijangkau nyata. Proporsi nilai yang sama. Harga berbeda. Martabat yang sama untuk semua pasar.",
        "preco_dir_titulo": "Cara Kerjanya dalam Praktik",
        "preco_dir": "A1ELOS menerapkan Paritas Daya Beli (PPP) sebagai kriteria harga sentral. Produk yang sama memberikan nilai relatif yang sama kepada pengguna di Lagos, Jakarta, Hanoi atau New York — harga dikalibrasi agar upaya finansial proporsional dengan pendapatan lokal.",
        "preco_pilares": [
            ("Kalibrasi PPP", "Harga disesuaikan dengan indeks daya beli setiap negara"),
            ("Rasa Hormat Budaya", "Bahasa, mata uang dan konteks lokal terintegrasi ke dalam produk"),
            ("Konversi Unggul", "Harga yang adil menghasilkan lebih banyak konversi dan retensi jangka panjang yang lebih tinggi"),
        ],
        "portfolio_titulo": "Portofolio: 23 Produk dalam 4 Tingkat",
        "portfolio_texto": "Struktur berlapis memastikan setiap profil pengguna — dari yang penasaran hingga profesional — menemukan penawaran yang sesuai dengan tingkat keterlibatan dan kapasitas finansialnya.",
        "portfolio_tabela": [
            ["Tingkat", "Produk", "Kisaran Harga (R$)", "Profil"],
            ["Dasar", "Peta Ekspres, Peta Lengkap", "R$ 8 – 17", "Penasaran, kontak pertama"],
            ["Menengah", "Pencarian AI, Nama Surat Suara, No. Pemilu", "R$ 26 – 53", "Pengguna terlibat"],
            ["Lanjut", "Numerologi Bisnis, Siklus, Misi", "R$ 81 – 109", "Profesional, wirausahawan"],
            ["Premium", "Diagnosis Lengkap, Peta Pribadi", "R$ 137 – 305", "Pendapatan tinggi, penggunaan korporat"],
            ["B2B", "Paket bisnis, lisensi, hadiah", "Sesuai permintaan", "Perusahaan dan tim"],
        ],
        "portfolio_rodape": "23 produk mencakup seluruh perjalanan pengguna, dari kontak pertama hingga pelanggan premium berulang — memaksimalkan LTV per bahasa dan pasar.",
        "negocio_titulo": "Model Bisnis: 3 Sumber Pendapatan",
        "negocio_texto": "A1ELOS dirancang dengan pendapatan yang beragam dan skalabel: penjualan langsung ke konsumen akhir dalam skala global, kontrak B2B bernilai tinggi dan iklan geolokasi berulang — tiga mesin yang saling mengisi.",
        "negocio_colunas": [
            ("B2C — 14 Bahasa", "Penjualan langsung produk digital dalam semua mata uang, dengan harga yang disesuaikan per PPP. Skala otomatis via AI — tanpa tim dukungan yang proporsional dengan pertumbuhan."),
            ("B2B — Diskon Progresif", "Paket korporat untuk HR, employer branding dan hadiah institusional. Diskon 10% hingga 50% sesuai volume. Di atas 2.000 kode, negosiasi langsung (Paket Berlian). Kontrak didukung oleh DUNS 942242668."),
            ("Iklan Geolokasi", "Banner yang disegmentasi per negara, benua atau dunia dengan rotasi otomatis. Pendapatan bulanan berulang bernilai tinggi — tanpa ketergantungan pada volume penjualan produk."),
        ],
        "banners_titulo": "Banner Iklan — Pendapatan Bulanan yang Dapat Diprediksi",
        "banners_texto": "Platform iklan geolokasi A1ELOS menawarkan kepada pengiklan segmentasi presisi per negara, benua atau jangkauan global, dengan format yang dioptimalkan untuk desktop dan mobile serta rotasi otomatis setiap 8 detik.",
        "banners_tabela": [
            ["Segmentasi", "Tetap (R$/bulan)", "Sementara (R$/bulan)", "Profil Pengiklan"],
            ["Negara", "R$ 800", "R$ 500", "UKM lokal, perdagangan regional"],
            ["Benua", "R$ 1.800", "R$ 1.200", "Merek regional, ekspansi benua"],
            ["Dunia", "R$ 3.500", "R$ 2.500", "Perusahaan global, aplikasi internasional"],
            ["Sponsor Eksklusif", "R$ 6.000", "R$ 4.500/kampanye", "Sponsor utama, peluncuran"],
        ],
        "banners_formatos": "728×90 px — Banner tengah desktop · 320×100 px — Format mobile yang dioptimalkan · 8 detik — Rotasi otomatis · Geo-target — Negara, benua atau jangkauan dunia",
        "b2b_titulo": "Paket Bisnis B2B — Nilai Tinggi, Volume Tinggi",
        "b2b_texto": "Paket B2B mengubah A1ELOS menjadi alat employer branding dan kesejahteraan korporat. Perusahaan membeli kode akses dalam jumlah besar untuk dibagikan sebagai hadiah kepada karyawan atau klien — didukung oleh DUNS 942242668 untuk kontrak korporat formal.",
        "b2b_planos": [
            ("Paket Dasar · 50 kode", "50× Peta Ekspres (R$ 8 masing-masing). Ideal untuk program tunjangan karyawan dan aksi integrasi."),
            ("Paket Menengah · 100 kode", "50× Peta Ekspres + 50× Pencarian AI (R$ 17). Sempurna untuk tim dan strategi employer branding."),
            ("Paket Premium · 200 kode", "100× Peta Ekspres + 100× Peta Lengkap (R$ 17). Kedalaman analitis maksimum untuk kelompok besar."),
        ],
        "b2b_tabela": [
            ["Mulai dari", "Diskon", "Profil", "Penggunaan yang Disarankan"],
            ["10 kode", "10%", "Tim kecil", "Aksi kesejahteraan sekali"],
            ["50 kode", "20%", "Tim yang berkembang", "Program berulang"],
            ["100 kode", "25%", "UKM", "Tunjangan triwulanan"],
            ["200 kode", "30%", "Perusahaan menengah", "Program lengkap"],
            ["500 kode", "40%", "Perusahaan menengah", "Hadiah tahunan kepada karyawan"],
            ["1.000 kode", "45%", "Korporasi besar", "Loyalitas pelanggan"],
            ["2.000 kode", "50%", "Kelompok besar", "Skala besar"],
            ["Di atas 2.000", "Dapat dinegosiasikan", "Paket Berlian khusus", "Distribusi bonus dalam volume"],
        ],
        "projecoes_titulo": "Proyeksi Keuangan: Cakrawala 50 Tahun",
        "projecoes_texto": "Proyeksi dibangun berdasarkan estimasi persentase penetrasi atas pasar potensial ~5,32 miliar penutur, dengan konversi konservatif 3% dan penukaran bonus antara 70% dan 90%. Dekade pertama dirinci pada tahun 1, 3, 5 dan 7 untuk menyoroti momentum.",
        "projecoes_tabela": [
            ["Cakrawala", "Konservatif (R$)", "Optimis (R$)"],
            ["Tahun 1", "R$ 281 ribu", "R$ 702 ribu"],
            ["Tahun 3", "R$ 983 ribu", "R$ 2,8 juta"],
            ["Tahun 5", "R$ 2,8 juta", "R$ 7 juta"],
            ["Tahun 7", "R$ 5,6 juta", "R$ 14 juta"],
            ["Tahun 10", "R$ 11,2 juta", "R$ 28,1 juta"],
            ["Tahun 20", "R$ 42,1 juta", "R$ 112 juta"],
            ["Tahun 30", "R$ 84,3 juta", "R$ 211 juta"],
            ["Tahun 40", "R$ 126 juta", "R$ 351 juta"],
            ["Tahun 50", "R$ 169 juta", "R$ 492 juta"],
        ],
        "tracao_titulo": "Traction dan Hasil yang Terbukti",
        "tracao_texto": "A1ELOS sudah beroperasi dengan metrik produk yang memvalidasi model — retensi tinggi, peringkat premium dan basis mitra B2B yang berkembang menunjukkan bahwa platform memberikan nilai nyata kepada pengguna akhir dan pasar korporat.",
        "tracao_kpis": [
            ("12K+", "Pengguna Aktif", "Basis organik yang tumbuh konsisten"),
            ("87%", "Retensi", "Jauh di atas rata-rata industri (~30%)"),
            ("4,8★", "Peringkat Rata-rata", "Kepuasan pengguna akhir yang terbukti"),
            ("23", "Mitra B2B", "Kontrak aktif dengan perusahaan dan HR"),
        ],
        "roteiro_titulo": "Peta Jalan Strategis",
        "roteiro_texto": "A1ELOS menjalankan rencana dalam empat fase progresif — dari konsolidasi basis saat ini hingga kepemimpinan pasar global, dengan opsi keluar yang jelas bagi investor.",
        "roteiro_fases": [
            ("Fase 1 · Konsolidasi", "Memperkuat basis pengguna dalam bahasa yang sudah aktif. Optimalisasi konversi, retensi dan LTV. Putaran Seed selesai."),
            ("Fase 2 · Ekspansi", "Peluncuran resmi di 3 pasar baru: Indonesia, Turki dan Vietnam. Percepatan kanal B2B dan iklan geolokasi."),
            ("Fase 3 · Masuk Global", "Kehadiran aktif di semua 14 bahasa dengan kampanye terlokalisasi. Kemitraan white-label di 5+ benua. Seri A."),
            ("Fase 4 · Kepemimpinan", "20+ negara dengan operasi terkonsolidasi. Platform SaaS referensi global dalam numerologi terapan. IPO atau keluar strategis."),
        ],
        "invest_titulo": "Investasi dan Kontak",
        "invest_texto": "Kami siap untuk presentasi privat, due diligence dan negosiasi. Hubungi kami melalui kanal pilihan Anda.",
        "invest_dados": [
            ("Putaran Seed", "R$ 3,5 juta"),
            ("Valuasi Pra-Money", "R$ 14 juta"),
            ("Ekuitas Ditawarkan", "Hingga 20%"),
        ],
        "invest_contato": [
            ("Email Investor", "a1elos.consultoria@gmail.com"),
            ("Email Umum", "contato@a1elos.com"),
            ("Situs Web", "www.a1elos.com"),
            ("DUNS", "942242668 — Dun & Bradstreet"),
        ],
        "invest_alocacao": "Alokasi Modal: 45% Teknologi · 30% Pemasaran · 25% Operasi",
        "frase_final": "Angka tidak pernah berbohong.",
        "selo_final": ["DUNS 942242668", "23 PRODUK", "14 BAHASA", "~5,3 MILIAR PENUTUR"],
        "graf_cons": "Konservatif",
        "graf_otim": "Optimis",
        "grafico_titulo_linha": "Pertumbuhan Diproyeksikan (R$ ribu)",
        "pix_titulo": "Brasil: Infrastruktur Pix",
        "pix_texto": "Pix adalah infrastruktur pembayaran instan publik Brasil. Bagi A1ELOS, Pix menjamin penagihan segera, biaya rendah dan penerimaan universal — fondasi operasi B2C di pasar Brasil dan pintu masuk ke ekspansi internasional.",
        "pix_kpis": [
            ("30,1 miliar", "Transaksi pada 2025", "+20% vs 2024 · Febraban"),
            ("76,4%", "populasi menggunakan Pix", "211 juta warga Brasil · Bank Sentral"),
            ("R$ 68,2 triliun", "pergerakan pada semester 2 2025", "78,4 miliar transaksi · Bank Sentral"),
            ("~80 miliar", "transaksi pada 2025", "+25,7% vs tahun sebelumnya · Laporan Pix"),
        ],
        "pix_fonte": "Sumber: Bank Sentral Brasil (Pix dalam Angka) dan Febraban (Survei Teknologi Perbankan).",
        "ref_titulo": "Referensi Bibliografi",
        "ref_intro": "Sumber yang digunakan untuk data pasar, proyeksi dan indikator presentasi ini.",
        "ref_lista": [
            ("Global Wellness Institute", "Ekonomi kesejahteraan global: US$ 6,8 triliun (2024) → US$ 9,8 triliun (2029)."),
            ("MarkNtel Advisors", "Aplikasi astrologi dan numerologi: US$ 3 miliar → US$ 9 miliar pada 2030 (CAGR ~20%)."),
            ("IMF · Bank Dunia", "PDB dan paritas daya beli (PPP) per negara."),
            ("Bank Sentral Brasil", "Statistik resmi Pix: transaksi, volume dan pengguna."),
            ("Febraban", "Survei Teknologi Perbankan — pertumbuhan Pix pada 2025."),
            ("IBGE", "Populasi dan indikator sosial-ekonomi Brasil."),
        ],
        },

"tr": {
        "titulo": "A1ELOS Küresel Numeroloji",
        "subtitulo": "Sayıların bilimi, başarınıza uygulandı",
        "capa_nota": "Yatırımcılar ve Ortaklar için Stratejik Sunum",
        "confidencial": "GİZLİ",
        "ano": "2026",
        "sumario_titulo": "Yönetici Özeti",
        "duns_porque": "DUNS neden önemlidir?",
        "preco_consciente": "Bilinçli Fiyatlandırma",
        "idioma_col": "Dil",
        "falantes_col": "Konuşmacılar (milyon)",
        "linhas_idiomas": [
           ["İngilizce", "1.528"],
           ["Mandarin", "1.184"],
           ["İspanyolca", "558"],
           ["Fransızca", "396"],
           ["Arapça", "335"],
           ["Portekizce", "270"],
           ["Rusça", "255"],
           ["Endonezce", "255"],
           ["Almanca", "134"],
           ["Japonca", "123"],
           ["Vietnamca", "97"],
           ["Türkçe", "90"],
           ["İtalyanca", "85"],
           ["İbranice", "9"],
        ],
        "total_linha": "TOPLAM",
        "fonte_receita": "Gelir Kaynağı",
        "participacao": "Pay",
        "b2c_linha": "B2C — 14 Dil",
        "b2b_linha": "B2B — Aşamalı İndirimler",
        "pub_linha": "Coğrafi Konumlu Reklam",
        "tabela_descontos": "Aşamalı İndirim Tablosu",
        "grafico_anos": ["Yıl 1", "Yıl 3", "Yıl 5", "Yıl 7", "Yıl 10"],
        "grafico_titulo": "Muhafazakâr Projeksiyon (R$ bin)",
        "grafico_titulo_linha": "Projeksiyonlu Büyüme (R$ bin)",
        "fale_conosco": "Bize Ulaşın",
        "sumario_intro": "Bu sunum, yatırımcıları ve ortakları A1ELOS Küresel Numeroloji'nin tüm stratejik yönlerinde yönlendirmek için yapılandırılmıştır — pazar tezinden tekrarlayan gelir modeline kadar.",
        "sumario_cards": [
            ("01", "A1ELOS Hakkında", "Holding, portföy ve DUNS kimlik belgesi"),
            ("02", "Pazar Fırsatı", "Küresel sağlıklı yaşam ekonomisi 6,8 trilyon USD"),
            ("03", "Çözüm ve Küresel Erişim", "14 dil, ~5,3 milyar konuşmacı"),
            ("04", "3 Yeni Pazar", "Endonezya, Türkiye ve Vietnam"),
            ("05", "Portföy ve Fiyatlandırma", "Satın alma gücüne göre kalibre edilmiş 23 ürün"),
            ("06", "Tekrarlayan Gelir", "Reklam banner'ları ve B2B Paketleri"),
            ("07", "Projeksiyonlar ve Yatırım", "50 yıllık ufuk · Tohum Turu R$ 3,5M"),
        ],
        "sobre_titulo": "A1ELOS Hakkında",
        "sobre_texto": "A1ELOS, küresel ölçekte yüksek etkili dijital ürünler yaratmak için yapay zekâyı, uygulamalı numerolojiyi ve kültürel stratejiyi birleştiren bir teknoloji ve bilgi holdingidir. Misyonumuz: her pazarın kültürüne ve satın alma gücüne saygı göstererek sayısal öz-bilgiyi demokratikleştirmek.",
        "sobre_kpis": [
            ("23", "Aktif Ürün", "4 erişim düzeyinde"),
            ("14", "Dil", "Dünya nüfusunun ~%67'si"),
            ("5,3 Milyar", "Konuşmacı", "Gerçek adreslenebilir pazar"),
            ("YZ", "Entegre", "Kişiselleştirme motoru"),
        ],
        "sobre_duns": "DUNS 942242668 — 190'dan fazla ülkede geçerli Dun & Bradstreet sertifikası, B2B sözleşmelerini ve uluslararası ortak girişimleri mümkün kılar.",
        "duns_titulo": "Uluslararası Güvenilirlik",
        "duns_texto": "DUNS numarası, A1ELOS'un uluslararası sahnedeki kurumsal pasaportudur. Ortaklara, kurumsal müşterilere ve yatırımcılara, şirketin doğrulanabilir kimliğe, izlenebilir geçmişe ve her yargı bölgesinde sözleşme kapasitesine sahip olduğunu gösterir.",
        "duns_numero": "942242668",
        "duns_emitido": "Dun & Bradstreet tarafından verilmiştir — 190'dan fazla ülkede tanınan küresel kurumsal kimlik standardı.",
        "duns_paises": "190+ ÜLKE",
        "duns_beneficios": [
            ("B2B Sözleşmeleri", "İhaleler ve küresel tedarikçiler için yeterlilik"),
            ("Ortak Girişimler", "Kolaylaştırılmış durum tespiti ile uluslararası ortaklıklar"),
            ("Anında Güvenilirlik", "Kurumsal yatırımcılar için ciddiyet işareti"),
        ],
        "mercado_titulo": "Pazar Fırsatı",
        "mercado_texto": "Mükemmel yakınsamayı yaşıyoruz: dijital sağlıklı yaşam küresel olarak patlarken, numeroloji ve astroloji yüksek etkileşimli uygulamalara taşınıyor. A1ELOS tam bu kesişim noktasında konumlanmıştır; dünya nüfusunun %74'ü zaten çevrimiçidir (~6 milyar kişi).",
        "mercado_cards": [
            ("Küresel Sağlıklı Yaşam", "6,8 trilyon USD → 2029'a kadar 9,8 trilyon USD (yıllık +%7,6)"),
            ("Astroloji/Numeroloji Uygulamaları", "3 milyar USD → 2030'a kadar 9 milyar USD · CAGR %20"),
            ("Sağlıklı Yaşam Uygulamaları", "CAGR %14,9 → 2030'da 26,2 milyar USD"),
            ("Çevrimiçi Kullanıcılar", "Dünyanın %74'ü · ~6 milyar kişi"),
        ],
        "problema_titulo": "Çözdüğümüz Sorun",
        "problema_col_esq_titulo": "Mevcut Pazarın Kusurları",
        "problema_col_esq": [
            ("Dil Engeli", "Numeroloji araçlarının ezici çoğunluğu yalnızca İngilizce çalışır ve diğer dillerdeki milyarlarca ana dili konuşmacıyı dışlar."),
            ("Gerçeklikten Kopuk Fiyatlar", "Gelişmekte olan pazarlar için dolar cinsinden fiyatlandırılan ürünler ekonomik dışlanma yaratır — kullanıcı ürünü değil, erişilemez fiyatı reddeder."),
            ("Derinlik Eksikliği", "Genel araçlar, kişiselleştirme olmadan, kültürel bağlam olmadan ve günlük hayata pratik uygulama olmadan yüzeysel yanıtlar verir."),
        ],
        "problema_col_dir_titulo": "Dışlanmanın Bedeli",
        "problema_col_dir": "Bir platform dil ve satın alma gücünü görmezden geldiğinde, dünyanın en büyük pazarını gönüllü olarak terk eder: gelişmekte olan ekonomilerde yaşayan ve İngilizce dışı diller konuşan 4 milyardan fazla insan. A1ELOS'un cerrahi hassasiyetle doldurduğu boşluk tam da budur.",
        "problema_destaque": "Yerel satın alma gücünü görmezden gelen platformlar, küresel adreslenebilir pazarın %60'ından fazlasına erişimini kaybeder.",
        "solucao_titulo": "Çözümümüz: 3 Stratejik Sütun",
        "solucao_texto": "A1ELOS, sayısal bilimi, yapay zekâyı ve kültürel duyarlılığı birleştiren entegre bir platform inşa etmiştir. Çözüm, çeşitlendirilmiş gelir ve yüksek elde tutma sağlayan üç tamamlayıcı cephede çalışır.",
        "solucao_colunas": [
            ("Kişisel Haritalar", "Son kullanıcı için derin ve kişiselleştirilmiş sayısal analizler — kimlik, misyon, yaşam döngüleri ve uyumluluk — entegre YZ ile 14 dilde sunulur."),
            ("İş Numerolojisi", "Markalara, CNPJ'lere, kuruluş tarihlerine ve kurumsal stratejiye uygulanan numerolojik teşhisler. B2B pazarı için yüksek algılanan değere sahip farklılaştırılmış bir ürün."),
            ("Beyaz Etiket B2B", "Numerolojiyi kendi markaları altında sunmak isteyen ortak şirketlere platform lisansı — çok dilli destek ve tam özelleştirme ile."),
        ],
        "alcance_titulo": "Küresel Erişim: 14 Dil · ~5,3 Milyar Konuşmacı",
        "alcance_texto": "A1ELOS, gerçekten çok dilli bir platformla dünya nüfusunun ~%67'sini kapsar. Her dil, yerel satın alma gücüne göre kalibre edilmiş fiyatlarla ayrı bir kültürel pazarı temsil eder.",
        "mercados_titulo": "3 Yeni Pazar: +442 Milyon Konuşmacı",
        "mercados_texto": "Endonezya, Türkiye ve Vietnam'a stratejik genişleme niteliksel bir sıçramayı temsil eder: yüksek ekonomik büyüme, artan dijital nüfuz ve erişilebilir dijital sağlıklı yaşam çözümlerine kanıtlanmış talep gösteren pazarlar.",
        "mercados_cards": [
            ("Endonezya", ["285 milyon nüfus", "%80,5 internet nüfuzu", "~255 milyon Endonezce konuşmacı", "Sağlıklı yaşam: 51,2 milyar USD (2025) → 72,8 milyar USD (2034)"]),
            ("Türkiye", ["85,9 milyon nüfus", "Kişi başına GSYİH PPP 37.301 USD", "~90 milyon Türkçe konuşmacı", "Dünya ortalamasının üzerinde (27.211 USD)"]),
            ("Vietnam",  ["~100 milyon nüfus", "Kişi başına GSYİH ~5.066 USD (yıllık +%7,4)", "~97 milyon Vietnamca konuşmacı", "Sağlıklı yaşam: 303 milyon USD (2025) → 485 milyon USD (2030)"]),
        ],
        "mercados_rodape": "3 yeni pazar = kültürel olarak kalibre edilmiş fiyatlarla platforma entegre edilen +442 milyon yeni adreslenebilir konuşmacı.",
        "preco_titulo": "Bilinçli Fiyatlandırma Felsefesi",
        "preco_esq": "Kültürel saygı + satın alma gücüne saygı = gerçek adreslenebilir pazar. Aynı değer oranı. Farklı fiyatlar. Tüm pazarlar için eşit saygınlık.",
        "preco_dir_titulo": "Pratikte Nasıl Çalışır",
        "preco_dir": "A1ELOS, Satın Alma Gücü Paritesini (PPP) merkezi fiyatlandırma kriteri olarak uygular. Aynı ürün, Lagos, Jakarta, Hanoi veya New York'taki kullanıcıya aynı göreceli değeri sunar — fiyat, finansal çaba yerel gelirle orantılı olacak şekilde kalibre edilir.",
        "preco_pilares": [
            ("PPP Kalibrasyonu", "Her ülkenin satın alma gücü endeksine göre ayarlanmış fiyatlar"),
            ("Kültürel Saygı", "Dil, para birimi ve yerel bağlam ürüne entegre edilmiştir"),
            ("Üstün Dönüşüm", "Adil fiyat daha fazla dönüşüm ve daha yüksek uzun vadeli elde tutma sağlar"),
        ],
        "portfolio_titulo": "Portföy: 4 Düzeyde 23 Ürün",
        "portfolio_texto": "Katmanlı yapı, her kullanıcı profilinin — meraklıdan profesyonele — etkileşim düzeyine ve finansal kapasitesine uygun bir teklif bulmasını sağlar.",
        "portfolio_tabela": [
            ["Düzey", "Ürünler", "Fiyat Aralığı (R$)", "Profil"],
            ["Temel", "Ekspres Harita, Tam Harita", "R$ 8 – 17", "Meraklı, ilk temas"],
            ["Orta", "YZ Arama, Oy Pusulası Adı, Seçim No.", "R$ 26 – 53", "Etkileşimli kullanıcı"],
            ["İleri", "İş Numerolojisi, Döngüler, Misyon", "R$ 81 – 109", "Profesyonel, girişimci"],
            ["Premium", "Tam Teşhisler, Kişisel Haritalar", "R$ 137 – 305", "Yüksek gelir, kurumsal kullanım"],
            ["B2B", "İş paketleri, lisanslar, hediyeler", "Talep üzerine", "Şirketler ve ekipler"],
        ],
        "portfolio_rodape": "23 ürün, kullanıcı yolculuğunun tamamını kapsar — ilk temastan tekrarlayan premium müşteriye kadar — her dil ve pazarda LTV'yi maksimize eder.",
        "negocio_titulo": "İş Modeli: 3 Gelir Kaynağı",
        "negocio_texto": "A1ELOS, çeşitlendirilmiş ve ölçeklenebilir gelirle tasarlanmıştır: küresel ölçekte son tüketiciye doğrudan satış, yüksek değerli B2B sözleşmeleri ve tekrarlayan coğrafi konumlu reklam — birbirini besleyen üç motor.",
        "negocio_colunas": [
            ("B2C — 14 Dil", "Tüm para birimlerinde dijital ürünlerin doğrudan satışı, PPP'ye göre uyarlanmış fiyatlarla. YZ aracılığıyla otomatik ölçekleme — büyümeyle orantılı destek ekibi yok."),
            ("B2B — Aşamalı İndirimler", "İK, işveren markası ve kurumsal hediyeler için kurumsal paketler. Hacme göre %10 ila %50 indirim. 2.000 kodun üzerinde doğrudan müzakere (Elmas Planı). Sözleşmeler DUNS 942242668 tarafından desteklenir."),
            ("Coğrafi Konumlu Reklam", "Ülke, kıta veya dünya bazında segmentlere ayrılmış, otomatik rotasyonlu banner'lar. Ürün satış hacmine bağımlılık olmadan yüksek değerli tekrarlayan aylık gelir."),
        ],
        "banners_titulo": "Reklam Banner'ları — Öngörülebilir Aylık Gelir",
        "banners_texto": "A1ELOS'un coğrafi konumlu reklam platformu, reklamverenlere ülke, kıta veya küresel erişime göre hassas segmentasyon sunar; masaüstü ve mobil için optimize edilmiş formatlar ve her 8 saniyede otomatik rotasyon ile.",
        "banners_tabela": [
            ["Segmentasyon", "Sabit (R$/ay)", "Geçici (R$/ay)", "Reklamveren Profili"],
            ["Ülke", "R$ 800", "R$ 500", "Yerel KOBİ'ler, bölgesel ticaret"],
            ["Kıta", "R$ 1.800", "R$ 1.200", "Bölgesel markalar, kıta genişlemesi"],
            ["Dünya", "R$ 3.500", "R$ 2.500", "Küresel şirketler, uluslararası uygulamalar"],
            ["Özel Sponsorluk", "R$ 6.000", "R$ 4.500/kampanya", "Ana sponsorlar, lansmanlar"],
        ],
        "banners_formatos": "728×90 px — Masaüstü merkez banner · 320×100 px — Optimize mobil format · 8 saniye — Otomatik rotasyon · Coğrafi hedef — Ülke, kıta veya dünya erişimi",
        "b2b_titulo": "B2B İş Paketleri — Yüksek Değer, Yüksek Hacim",
        "b2b_texto": "B2B Paketleri, A1ELOS'u bir işveren markası ve kurumsal sağlıklı yaşam aracına dönüştürür. Şirketler, çalışanlara veya müşterilere hediye olarak dağıtmak üzere erişim kodlarını toplu olarak satın alır — resmi kurumsal sözleşmeler için DUNS 942242668 tarafından desteklenir.",
        "b2b_planos": [
            ("Temel Plan · 50 kod", "50× Ekspres Harita (her biri R$ 8). Çalışan yan hak programları ve entegrasyon eylemleri için idealdir."),
            ("Orta Plan · 100 kod", "50× Ekspres Harita + 50× YZ Arama (R$ 17). Ekipler ve işveren markası stratejisi için mükemmeldir."),
            ("Premium Plan · 200 kod", "100× Ekspres Harita + 100× Tam Harita (R$ 17). Büyük gruplar için maksimum analitik derinlik."),
        ],
        "b2b_tabela": [
            ["Şuradan itibaren", "İndirim", "Profil", "Önerilen Kullanım"],
            ["10 kod", "%10", "Küçük ekipler", "Tek seferlik sağlıklı yaşam eylemi"],
            ["50 kod", "%20", "Büyüyen ekipler", "Tekrarlayan programlar"],
            ["100 kod", "%25", "KOBİ'ler", "Üç aylık yan hak"],
            ["200 kod", "%30", "Orta ölçekli şirketler", "Tam programlar"],
            ["500 kod", "%40", "Orta ölçekli şirketler", "Çalışanlara yıllık hediye"],
            ["1.000 kod", "%45", "Büyük şirketler", "Müşteri sadakati"],
            ["2.000 kod", "%50", "Büyük gruplar", "Büyük ölçek"],
            ["2.000'in üzerinde", "Pazarlık edilebilir", "Özel Elmas Planı", "Hacimli bonus dağıtımı"],
        ],
        "projecoes_titulo": "Finansal Projeksiyonlar: 50 Yıllık Ufuk",
        "projecoes_texto": "Projeksiyonlar, ~5,32 milyar konuşmacılık potansiyel pazar üzerindeki yüzdelik nüfuz tahminlerine dayanmaktadır; muhafazakâr %3 dönüşüm ve %70 ila %90 bonus kullanımı ile. İlk on yıl, ivmeyi vurgulamak için 1, 3, 5 ve 7. yıllarda detaylandırılmıştır.",
        "projecoes_tabela": [
            ["Ufuk", "Muhafazakâr (R$)", "İyimser (R$)"],
            ["Yıl 1", "R$ 281 bin", "R$ 702 bin"],
            ["Yıl 3", "R$ 983 bin", "R$ 2,8 milyon"],
            ["Yıl 5", "R$ 2,8 milyon", "R$ 7 milyon"],
            ["Yıl 7", "R$ 5,6 milyon", "R$ 14 milyon"],
            ["Yıl 10", "R$ 11,2 milyon", "R$ 28,1 milyon"],
            ["Yıl 20", "R$ 42,1 milyon", "R$ 112 milyon"],
            ["Yıl 30", "R$ 84,3 milyon", "R$ 211 milyon"],
            ["Yıl 40", "R$ 126 milyon", "R$ 351 milyon"],
            ["Yıl 50", "R$ 169 milyon", "R$ 492 milyon"],
        ],
        "tracao_titulo": "Çekiş ve Kanıtlanmış Sonuçlar",
        "tracao_texto": "A1ELOS, modeli doğrulayan ürün metrikleriyle zaten faaliyet göstermektedir — yüksek elde tutma, premium puanlama ve büyüyen B2B ortak tabanı, platformun son kullanıcıya ve kurumsal pazara gerçek değer sunduğunu gösterir.",
        "tracao_kpis": [
            ("12K+", "Aktif Kullanıcı", "Tutarlı büyüyen organik taban"),
            ("%87", "Elde Tutma", "Sektör ortalamasının çok üzerinde (~%30)"),
            ("4,8★", "Ortalama Puan", "Kanıtlanmış son kullanıcı memnuniyeti"),
            ("23", "B2B Ortağı", "Şirketler ve İK ile aktif sözleşmeler"),
        ],
        "roteiro_titulo": "Stratejik Yol Haritası",
        "roteiro_texto": "A1ELOS, mevcut tabanın konsolidasyonundan küresel pazar liderliğine kadar, yatırımcılar için net çıkış seçenekleri sunan dört aşamalı bir plan yürütür.",
        "roteiro_fases": [
            ("Aşama 1 · Konsolidasyon", "Zaten aktif olan dillerde kullanıcı tabanının güçlendirilmesi. Dönüşüm, elde tutma ve LTV optimizasyonu. Tohum Turu tamamlandı."),
            ("Aşama 2 · Genişleme", "3 yeni pazarda resmi lansman: Endonezya, Türkiye ve Vietnam. B2B kanalının ve coğrafi konumlu reklamın hızlandırılması."),
            ("Aşama 3 · Küresel Giriş", "Yerelleştirilmiş kampanyalarla 14 dilin tamamında aktif varlık. 5+ kıtada beyaz etiket ortaklıkları. Seri A."),
            ("Aşama 4 · Liderlik", "Konsolide operasyonlarla 20'den fazla ülke. Uygulamalı numerolojide küresel referans SaaS platformu. IPO veya stratejik çıkış."),
        ],
        "invest_titulo": "Yatırım ve İletişim",
        "invest_texto": "Özel sunumlar, durum tespiti ve müzakereler için hazırız. Tercih ettiğiniz kanaldan bize ulaşın.",
        "invest_dados": [
            ("Tohum Turu", "R$ 3,5 milyon"),
            ("Ön-Para Değerlemesi", "R$ 14 milyon"),
            ("Sunulan Öz Sermaye", "%20'ye kadar"),
        ],
        "invest_contato": [
            ("Yatırımcı E-postası", "a1elos.consultoria@gmail.com"),
            ("Genel E-posta", "contato@a1elos.com"),
            ("Web Sitesi", "www.a1elos.com"),
            ("DUNS", "942242668 — Dun & Bradstreet"),
        ],
        "invest_alocacao": "Sermaye Tahsisi: %45 Teknoloji · %30 Pazarlama · %25 Operasyon",
        "frase_final": "Sayılar asla yalan söylemez.",
        "selo_final": ["DUNS 942242668", "23 ÜRÜN", "14 DİL", "~5,3 MİLYAR KONUŞMACI"],
        "graf_cons": "Muhafazakâr",
        "graf_otim": "İyimser",
        "grafico_titulo_linha": "Projeksiyonlu Büyüme (R$ bin)",
        "pix_titulo": "Brezilya: Pix Altyapısı",
        "pix_texto": "Pix, Brezilya'nın kamu anlık ödeme altyapısıdır. A1ELOS için anında tahsilat, düşük maliyet ve evrensel kabul garantiler — Brezilya pazarındaki B2C operasyonunun temeli ve uluslararası genişlemenin kapısı.",
        "pix_kpis": [
            ("30,1 milyar", "2025 işlemi", "2024'e göre +%20 · Febraban"),
            ("%76,4", "nüfus Pix kullanıyor", "211 milyon Brezilyalı · Merkez Bankası"),
            ("R$ 68,2 trilyon", "2025 2. yarı hareketi", "78,4 milyar işlem · Merkez Bankası"),
            ("~80 milyar", "2025 işlemi", "Önceki yıla göre +%25,7 · Pix Raporu"),
        ],
        "pix_fonte": "Kaynaklar: Brezilya Merkez Bankası (Rakamlarla Pix) ve Febraban (Bankacılık Teknolojisi Anketi).",
        "ref_titulo": "Bibliyografik Referanslar",
        "ref_intro": "Bu sunumun pazar verileri, projeksiyonları ve göstergeleri için kullanılan kaynaklar.",
        "ref_lista": [
            ("Global Wellness Institute", "Küresel sağlıklı yaşam ekonomisi: 6,8 trilyon USD (2024) → 9,8 trilyon USD (2029)."),
            ("MarkNtel Advisors", "Astroloji ve numeroloji uygulamaları: 3 milyar USD → 2030'a kadar 9 milyar USD (CAGR ~%20)."),
            ("IMF · Dünya Bankası", "Ülke bazında GSYİH ve satın alma gücü paritesi (PPP)."),
            ("Brezilya Merkez Bankası", "Pix'in resmi istatistikleri: işlemler, hacim ve kullanıcılar."),
            ("Febraban", "Bankacılık Teknolojisi Anketi — 2025'te Pix büyümesi."),
            ("IBGE", "Brezilya'nın nüfusu ve sosyoekonomik göstergeleri."),
        ],
        },

"vi": {
        "titulo": "A1ELOS Số Học Toàn Cầu",
        "subtitulo": "Khoa học về các con số ứng dụng vào thành công của bạn",
        "capa_nota": "Bài Thuyết trình Chiến lược cho Nhà đầu tư và Đối tác",
        "confidencial": "BẢO MẬT",
        "ano": "2026",
        "sumario_titulo": "Tóm tắt Điều hành",
        "duns_porque": "Tại sao DUNS quan trọng?",
        "preco_consciente": "Định giá Có Ý thức",
        "idioma_col": "Ngôn ngữ",
        "falantes_col": "Người nói (triệu)",
        "linhas_idiomas": [
           ["Tiếng Anh", "1.528"],
           ["Tiếng Quan Thoại", "1.184"],
           ["Tiếng Tây Ban Nha", "558"],
           ["Tiếng Pháp", "396"],
           ["Tiếng Ả Rập", "335"],
           ["Tiếng Bồ Đào Nha", "270"],
           ["Tiếng Nga", "255"],
           ["Tiếng Indonesia", "255"],
           ["Tiếng Đức", "134"],
           ["Tiếng Nhật", "123"],
           ["Tiếng Việt", "97"],
           ["Tiếng Thổ Nhĩ Kỳ", "90"],
           ["Tiếng Ý", "85"],
           ["Tiếng Do Thái", "9"],
        ],
        "total_linha": "TỔNG",
        "fonte_receita": "Nguồn Doanh thu",
        "participacao": "Tỷ trọng",
        "b2c_linha": "B2C — 14 Ngôn ngữ",
        "b2b_linha": "B2B — Chiết khấu Lũy tiến",
        "pub_linha": "Quảng cáo Định vị Địa lý",
        "tabela_descontos": "Bảng Chiết khấu Lũy tiến",
        "grafico_anos": ["Năm 1", "Năm 3", "Năm 5", "Năm 7", "Năm 10"],
        "grafico_titulo": "Dự báo Thận trọng (R$ nghìn)",
        "grafico_titulo_linha": "Tăng trưởng Dự kiến (R$ nghìn)",
        "fale_conosco": "Liên hệ với chúng tôi",
        "sumario_intro": "Bài thuyết trình này được cấu trúc để hướng dẫn các nhà đầu tư và đối tác qua mọi khía cạnh chiến lược của A1ELOS Số Học Toàn Cầu — từ luận điểm thị trường đến mô hình doanh thu định kỳ.",
        "sumario_cards": [
            ("01", "Về A1ELOS", "Tập đoàn, danh mục và chứng nhận DUNS"),
            ("02", "Cơ hội Thị trường", "Nền kinh tế chăm sóc sức khỏe toàn cầu 6,8 nghìn tỷ USD"),
            ("03", "Giải pháp và Phạm vi Toàn cầu", "14 ngôn ngữ, ~5,3 tỷ người nói"),
            ("04", "3 Thị trường Mới", "Indonesia, Thổ Nhĩ Kỳ và Việt Nam"),
            ("05", "Danh mục và Giá cả", "23 sản phẩm được hiệu chỉnh theo sức mua"),
            ("06", "Doanh thu Định kỳ", "Banner quảng cáo và Gói B2B"),
            ("07", "Dự báo và Đầu tư", "Tầm nhìn 50 năm · Vòng hạt giống R$ 3,5 triệu"),
        ],
        "sobre_titulo": "Về A1ELOS",
        "sobre_texto": "A1ELOS là tập đoàn công nghệ và tri thức kết hợp trí tuệ nhân tạo, số học ứng dụng và chiến lược văn hóa để tạo ra các sản phẩm kỹ thuật số tác động cao trên quy mô toàn cầu. Sứ mệnh của chúng tôi: dân chủ hóa tri thức bản thân bằng số với sự tôn trọng văn hóa và tôn trọng sức mua của từng thị trường.",
        "sobre_kpis": [
            ("23", "Sản phẩm Hoạt động", "Trong 4 cấp truy cập"),
            ("14", "Ngôn ngữ", "~67% dân số thế giới"),
            ("5,3 tỷ", "Người nói", "Thị trường thực sự có thể tiếp cận"),
            ("AI", "Tích hợp", "Công cụ cá nhân hóa"),
        ],
        "sobre_duns": "DUNS 942242668 — Chứng nhận Dun & Bradstreet có hiệu lực tại hơn 190 quốc gia, cho phép ký hợp đồng B2B và liên doanh quốc tế.",
        "duns_titulo": "Uy tín Quốc tế",
        "duns_texto": "Số DUNS là hộ chiếu doanh nghiệp của A1ELOS trên trường quốc tế. Nó báo hiệu cho đối tác, khách hàng doanh nghiệp và nhà đầu tư rằng công ty có danh tính có thể xác minh, lịch sử có thể truy vết và năng lực hợp đồng tại bất kỳ khu vực pháp lý nào.",
        "duns_numero": "942242668",
        "duns_emitido": "Được cấp bởi Dun & Bradstreet — tiêu chuẩn toàn cầu về nhận dạng doanh nghiệp được công nhận tại hơn 190 quốc gia.",
        "duns_paises": "190+ QUỐC GIA",
        "duns_beneficios": [
            ("Hợp đồng B2B", "Đủ điều kiện cho đấu thầu và nhà cung cấp toàn cầu"),
            ("Liên doanh", "Quan hệ đối tác quốc tế với thẩm định được hỗ trợ"),
            ("Uy tín Tức thì", "Dấu hiệu nghiêm túc cho các nhà đầu tư tổ chức"),
        ],
        "mercado_titulo": "Cơ hội Thị trường",
        "mercado_texto": "Chúng ta đang sống trong sự hội tụ hoàn hảo: chăm sóc sức khỏe kỹ thuật số bùng nổ toàn cầu trong khi số học và chiêm tinh chuyển sang các ứng dụng có mức độ tương tác cao. A1ELOS định vị chính xác tại giao điểm này, với 74% dân số thế giới đã trực tuyến (~6 tỷ người).",
        "mercado_cards": [
            ("Chăm sóc sức khỏe Toàn cầu", "6,8 nghìn tỷ USD → 9,8 nghìn tỷ USD vào 2029 (+7,6%/năm)"),
            ("Ứng dụng Chiêm tinh/Số học", "3 tỷ USD → 9 tỷ USD vào 2030 · CAGR 20%"),
            ("Ứng dụng Chăm sóc sức khỏe", "CAGR 14,9% → 26,2 tỷ USD vào 2030"),
            ("Người dùng Trực tuyến", "74% thế giới · ~6 tỷ người"),
        ],
        "problema_titulo": "Vấn đề Chúng tôi Giải quyết",
        "problema_col_esq_titulo": "Sai lầm của Thị trường Hiện tại",
        "problema_col_esq": [
            ("Rào cản Ngôn ngữ", "Đại đa số công cụ số học chỉ hoạt động bằng tiếng Anh, loại trừ hàng tỷ người bản ngữ ở các ngôn ngữ khác."),
            ("Giá Tách rời Thực tế", "Sản phẩm định giá bằng đô la cho các thị trường mới nổi tạo ra sự loại trừ kinh tế — người dùng không từ chối sản phẩm, mà từ chối mức giá không thể tiếp cận."),
            ("Thiếu Chiều sâu", "Các công cụ chung chung đưa ra câu trả lời hời hợt không có cá nhân hóa, không có bối cảnh văn hóa và không có ứng dụng thực tế vào cuộc sống hàng ngày."),
        ],
        "problema_col_dir_titulo": "Cái giá của Sự Loại trừ",
        "problema_col_dir": "Khi một nền tảng bỏ qua ngôn ngữ và sức mua, nó tự nguyện từ bỏ thị trường lớn nhất thế giới: hơn 4 tỷ người sống trong các nền kinh tế mới nổi và nói các ngôn ngữ không phải tiếng Anh. Đây chính là khoảng trống mà A1ELOS lấp đầy với độ chính xác phẫu thuật.",
        "problema_destaque": "Các nền tảng bỏ qua sức mua địa phương mất quyền truy cập vào hơn 60% thị trường toàn cầu có thể tiếp cận.",
        "solucao_titulo": "Giải pháp của Chúng tôi: 3 Trụ cột Chiến lược",
        "solucao_texto": "A1ELOS đã xây dựng một nền tảng tích hợp kết hợp khoa học số, trí tuệ nhân tạo và sự nhạy cảm văn hóa. Giải pháp hoạt động trên ba hướng bổ trợ, đảm bảo doanh thu đa dạng và tỷ lệ giữ chân cao.",
        "solucao_colunas": [
            ("Bản đồ Cá nhân", "Phân tích số sâu sắc và cá nhân hóa cho người dùng cuối — danh tính, sứ mệnh, chu kỳ cuộc đời và sự tương hợp — được cung cấp bằng 14 ngôn ngữ với AI tích hợp."),
            ("Số học Doanh nghiệp", "Chẩn đoán số học áp dụng cho thương hiệu, CNPJ, ngày thành lập và chiến lược doanh nghiệp. Sản phẩm khác biệt có giá trị cảm nhận cao cho thị trường B2B."),
            ("White-Label B2B", "Cấp phép nền tảng cho các công ty đối tác muốn cung cấp số học dưới thương hiệu riêng — với hỗ trợ đa ngôn ngữ và tùy chỉnh hoàn toàn."),
        ],
        "alcance_titulo": "Phạm vi Toàn cầu: 14 Ngôn ngữ · ~5,3 Tỷ Người nói",
        "alcance_texto": "A1ELOS bao phủ ~67% dân số thế giới với nền tảng thực sự đa ngôn ngữ. Mỗi ngôn ngữ đại diện cho một thị trường văn hóa riêng biệt, với giá được hiệu chỉnh theo sức mua địa phương.",
        "mercados_titulo": "3 Thị trường Mới: +442 Triệu Người nói",
        "mercados_texto": "Sự mở rộng chiến lược sang Indonesia, Thổ Nhĩ Kỳ và Việt Nam đại diện cho một bước nhảy về chất: các thị trường có tăng trưởng kinh tế cao, mức độ phổ cập kỹ thuật số tăng và nhu cầu đã được chứng minh về các giải pháp chăm sóc sức khỏe kỹ thuật số dễ tiếp cận.",
        "mercados_cards": [
            ("Indonesia", ["285 triệu dân", "80,5% độ phủ internet", "~255 triệu người nói tiếng Indonesia", "Chăm sóc sức khỏe: 51,2 tỷ USD (2025) → 72,8 tỷ USD (2034)"]),
            ("Thổ Nhĩ Kỳ", ["85,9 triệu dân", "GDP PPP bình quân đầu người 37.301 USD", "~90 triệu người nói tiếng Thổ Nhĩ Kỳ", "Trên mức trung bình thế giới (27.211 USD)"]),
            ("Việt Nam",  ["~100 triệu dân", "GDP bình quân đầu người ~5.066 USD (+7,4%/năm)", "~97 triệu người nói tiếng Việt", "Chăm sóc sức khỏe: 303 triệu USD (2025) → 485 triệu USD (2030)"]),
        ],
        "mercados_rodape": "3 thị trường mới = +442 triệu người nói mới có thể tiếp cận — được tích hợp vào nền tảng với giá được hiệu chỉnh theo văn hóa.",
        "preco_titulo": "Triết lý Định giá Có Ý thức",
        "preco_esq": "Tôn trọng văn hóa + tôn trọng sức mua = thị trường thực sự có thể tiếp cận. Cùng tỷ lệ giá trị. Giá khác nhau. Phẩm giá bình đẳng cho mọi thị trường.",
        "preco_dir_titulo": "Cách Hoạt động Trong Thực tế",
        "preco_dir": "A1ELOS áp dụng Ngang giá Sức mua (PPP) làm tiêu chí định giá trung tâm. Cùng một sản phẩm mang lại giá trị tương đối như nhau cho người dùng ở Lagos, Jakarta, Hà Nội hay New York — giá được hiệu chỉnh để nỗ lực tài chính tương xứng với thu nhập địa phương.",
        "preco_pilares": [
            ("Hiệu chỉnh PPP", "Giá điều chỉnh theo chỉ số sức mua của từng quốc gia"),
            ("Tôn trọng Văn hóa", "Ngôn ngữ, tiền tệ và bối cảnh địa phương tích hợp vào sản phẩm"),
            ("Chuyển đổi Vượt trội", "Giá hợp lý tạo ra nhiều chuyển đổi hơn và giữ chân lâu dài cao hơn"),
        ],
        "portfolio_titulo": "Danh mục: 23 Sản phẩm trong 4 Cấp",
        "portfolio_texto": "Cấu trúc phân tầng đảm bảo mọi hồ sơ người dùng — từ người tò mò đến chuyên gia — tìm thấy đề xuất phù hợp với mức độ tương tác và khả năng tài chính của mình.",
        "portfolio_tabela": [
            ["Cấp", "Sản phẩm", "Khoảng Giá (R$)", "Hồ sơ"],
            ["Cơ bản", "Bản đồ Nhanh, Bản đồ Đầy đủ", "R$ 8 – 17", "Tò mò, tiếp xúc đầu tiên"],
            ["Trung cấp", "Tìm kiếm AI, Tên phiếu bầu, Số bầu cử", "R$ 26 – 53", "Người dùng tương tác"],
            ["Nâng cao", "Số học Doanh nghiệp, Chu kỳ, Sứ mệnh", "R$ 81 – 109", "Chuyên gia, doanh nhân"],
            ["Cao cấp", "Chẩn đoán Đầy đủ, Bản đồ Cá nhân", "R$ 137 – 305", "Thu nhập cao, sử dụng doanh nghiệp"],
            ["B2B", "Gói doanh nghiệp, giấy phép, quà tặng", "Theo yêu cầu", "Doanh nghiệp và đội nhóm"],
        ],
        "portfolio_rodape": "23 sản phẩm bao phủ toàn bộ hành trình người dùng, từ tiếp xúc đầu tiên đến khách hàng cao cấp định kỳ — tối đa hóa LTV theo từng ngôn ngữ và thị trường.",
        "negocio_titulo": "Mô hình Kinh doanh: 3 Nguồn Doanh thu",
        "negocio_texto": "A1ELOS được thiết kế với doanh thu đa dạng và có thể mở rộng: bán trực tiếp cho người tiêu dùng cuối trên quy mô toàn cầu, hợp đồng B2B giá trị cao và quảng cáo định vị địa lý định kỳ — ba động cơ nuôi dưỡng lẫn nhau.",
        "negocio_colunas": [
            ("B2C — 14 Ngôn ngữ", "Bán trực tiếp sản phẩm kỹ thuật số bằng mọi loại tiền tệ, với giá điều chỉnh theo PPP. Mở rộng tự động qua AI — không cần đội hỗ trợ tỷ lệ thuận với tăng trưởng."),
            ("B2B — Chiết khấu Lũy tiến", "Gói doanh nghiệp cho HR, thương hiệu nhà tuyển dụng và quà tặng tổ chức. Chiết khấu 10% đến 50% theo khối lượng. Trên 2.000 mã, đàm phán trực tiếp (Gói Kim cương). Hợp đồng được hỗ trợ bởi DUNS 942242668."),
            ("Quảng cáo Định vị Địa lý", "Banner phân đoạn theo quốc gia, châu lục hoặc toàn cầu với luân chuyển tự động. Doanh thu định kỳ hàng tháng giá trị cao — không phụ thuộc vào khối lượng bán sản phẩm."),
        ],
        "banners_titulo": "Banner Quảng cáo — Doanh thu Hàng tháng Dự đoán được",
        "banners_texto": "Nền tảng quảng cáo định vị địa lý của A1ELOS cung cấp cho nhà quảng cáo phân đoạn chính xác theo quốc gia, châu lục hoặc phạm vi toàn cầu, với định dạng tối ưu cho máy tính và di động cùng luân chuyển tự động mỗi 8 giây.",
        "banners_tabela": [
            ["Phân đoạn", "Cố định (R$/tháng)", "Tạm thời (R$/tháng)", "Hồ sơ Nhà quảng cáo"],
            ["Quốc gia", "R$ 800", "R$ 500", "SME địa phương, thương mại khu vực"],
            ["Châu lục", "R$ 1.800", "R$ 1.200", "Thương hiệu khu vực, mở rộng châu lục"],
            ["Toàn cầu", "R$ 3.500", "R$ 2.500", "Công ty toàn cầu, ứng dụng quốc tế"],
            ["Tài trợ Độc quyền", "R$ 6.000", "R$ 4.500/chiến dịch", "Nhà tài trợ chính, ra mắt"],
        ],
        "banners_formatos": "728×90 px — Banner trung tâm máy tính · 320×100 px — Định dạng di động tối ưu · 8 giây — Luân chuyển tự động · Mục tiêu địa lý — Quốc gia, châu lục hoặc phạm vi toàn cầu",
        "b2b_titulo": "Gói Doanh nghiệp B2B — Giá trị Cao, Khối lượng Cao",
        "b2b_texto": "Gói B2B biến A1ELOS thành công cụ thương hiệu nhà tuyển dụng và chăm sóc sức khỏe doanh nghiệp. Các công ty mua mã truy cập với số lượng lớn để phân phối làm quà tặng cho nhân viên hoặc khách hàng — được hỗ trợ bởi DUNS 942242668 cho hợp đồng doanh nghiệp chính thức.",
        "b2b_planos": [
            ("Gói Cơ bản · 50 mã", "50× Bản đồ Nhanh (mỗi mã R$ 8). Lý tưởng cho chương trình phúc lợi nhân viên và hoạt động hội nhập."),
            ("Gói Trung cấp · 100 mã", "50× Bản đồ Nhanh + 50× Tìm kiếm AI (R$ 17). Hoàn hảo cho đội nhóm và chiến lược thương hiệu nhà tuyển dụng."),
            ("Gói Cao cấp · 200 mã", "100× Bản đồ Nhanh + 100× Bản đồ Đầy đủ (R$ 17). Chiều sâu phân tích tối đa cho các nhóm lớn."),
        ],
        "b2b_tabela": [
            ["Từ", "Chiết khấu", "Hồ sơ", "Sử dụng Được Khuyến nghị"],
            ["10 mã", "10%", "Đội nhóm nhỏ", "Hoạt động chăm sóc sức khỏe một lần"],
            ["50 mã", "20%", "Đội nhóm đang phát triển", "Chương trình định kỳ"],
            ["100 mã", "25%", "SME", "Phúc lợi hàng quý"],
            ["200 mã", "30%", "Doanh nghiệp vừa", "Chương trình hoàn chỉnh"],
            ["500 mã", "40%", "Doanh nghiệp vừa", "Quà tặng hàng năm cho nhân viên"],
            ["1.000 mã", "45%", "Tập đoàn lớn", "Khách hàng trung thành"],
            ["2.000 mã", "50%", "Nhóm lớn", "Quy mô lớn"],
            ["Trên 2.000", "Có thể thương lượng", "Gói Kim cương tùy chỉnh", "Phân phối thưởng theo khối lượng"],
        ],
        "projecoes_titulo": "Dự báo Tài chính: Tầm nhìn 50 Năm",
        "projecoes_texto": "Các dự báo được xây dựng dựa trên ước tính tỷ lệ phần trăm thâm nhập thị trường tiềm năng ~5,32 tỷ người nói, với tỷ lệ chuyển đổi thận trọng 3% và tỷ lệ quy đổi thưởng từ 70% đến 90%. Thập kỷ đầu tiên được chi tiết vào các năm 1, 3, 5 và 7 để làm nổi bật đà tăng trưởng.",
        "projecoes_tabela": [
            ["Tầm nhìn", "Thận trọng (R$)", "Lạc quan (R$)"],
            ["Năm 1", "R$ 281 nghìn", "R$ 702 nghìn"],
            ["Năm 3", "R$ 983 nghìn", "R$ 2,8 triệu"],
            ["Năm 5", "R$ 2,8 triệu", "R$ 7 triệu"],
            ["Năm 7", "R$ 5,6 triệu", "R$ 14 triệu"],
            ["Năm 10", "R$ 11,2 triệu", "R$ 28,1 triệu"],
            ["Năm 20", "R$ 42,1 triệu", "R$ 112 triệu"],
            ["Năm 30", "R$ 84,3 triệu", "R$ 211 triệu"],
            ["Năm 40", "R$ 126 triệu", "R$ 351 triệu"],
            ["Năm 50", "R$ 169 triệu", "R$ 492 triệu"],
        ],
        "tracao_titulo": "Sức hút và Kết quả Đã chứng minh",
        "tracao_texto": "A1ELOS đã hoạt động với các chỉ số sản phẩm xác thực mô hình — tỷ lệ giữ chân cao, xếp hạng cao cấp và nền tảng đối tác B2B đang phát triển chứng minh rằng nền tảng mang lại giá trị thực cho người dùng cuối và thị trường doanh nghiệp.",
        "tracao_kpis": [
            ("12K+", "Người dùng Hoạt động", "Nền tảng hữu cơ tăng trưởng ổn định"),
            ("87%", "Giữ chân", "Vượt xa mức trung bình ngành (~30%)"),
            ("4,8★", "Đánh giá Trung bình", "Sự hài lòng người dùng cuối đã được chứng minh"),
            ("23", "Đối tác B2B", "Hợp đồng đang hoạt động với doanh nghiệp và HR"),
        ],
        "roteiro_titulo": "Lộ trình Chiến lược",
        "roteiro_texto": "A1ELOS thực hiện kế hoạch trong bốn giai đoạn tiến triển — từ củng cố nền tảng hiện tại đến vị thế dẫn đầu thị trường toàn cầu, với các lựa chọn rút lui rõ ràng cho nhà đầu tư.",
        "roteiro_fases": [
            ("Giai đoạn 1 · Củng cố", "Tăng cường nền tảng người dùng trong các ngôn ngữ đã hoạt động. Tối ưu hóa chuyển đổi, giữ chân và LTV. Vòng hạt giống hoàn tất."),
            ("Giai đoạn 2 · Mở rộng", "Ra mắt chính thức tại 3 thị trường mới: Indonesia, Thổ Nhĩ Kỳ và Việt Nam. Đẩy nhanh kênh B2B và quảng cáo định vị địa lý."),
            ("Giai đoạn 3 · Thâm nhập Toàn cầu", "Hiện diện tích cực ở cả 14 ngôn ngữ với chiến dịch bản địa hóa. Quan hệ đối tác white-label tại 5+ châu lục. Vòng A."),
            ("Giai đoạn 4 · Vị thế Dẫn đầu", "Hơn 20 quốc gia với hoạt động được củng cố. Nền tảng SaaS tham chiếu toàn cầu về số học ứng dụng. IPO hoặc rút lui chiến lược."),
        ],
        "invest_titulo": "Đầu tư và Liên hệ",
        "invest_texto": "Chúng tôi sẵn sàng cho các buổi thuyết trình riêng, thẩm định và đàm phán. Liên hệ với chúng tôi qua kênh bạn ưa thích.",
        "invest_dados": [
            ("Vòng hạt giống", "R$ 3,5 triệu"),
            ("Định giá Trước đầu tư", "R$ 14 triệu"),
            ("Vốn cổ phần Được cung cấp", "Lên đến 20%"),
        ],
        "invest_contato": [
            ("Email Nhà đầu tư", "a1elos.consultoria@gmail.com"),
            ("Email Chung", "contato@a1elos.com"),
            ("Trang Web", "www.a1elos.com"),
            ("DUNS", "942242668 — Dun & Bradstreet"),
        ],
        "invest_alocacao": "Phân bổ Vốn: 45% Công nghệ · 30% Tiếp thị · 25% Vận hành",
        "frase_final": "Các con số không bao giờ nói dối.",
        "selo_final": ["DUNS 942242668", "23 SẢN PHẨM", "14 NGÔN NGỮ", "~5,3 TỶ NGƯỜI NÓI"],
        "graf_cons": "Thận trọng",
        "graf_otim": "Lạc quan",
        "grafico_titulo_linha": "Tăng trưởng Dự kiến (R$ nghìn)",
        "pix_titulo": "Brazil: Cơ sở hạ tầng Pix",
        "pix_texto": "Pix là cơ sở hạ tầng thanh toán tức thời công cộng của Brazil. Đối với A1ELOS, nó đảm bảo thu tiền ngay lập tức, chi phí thấp và chấp nhận phổ quát — nền tảng của hoạt động B2C tại thị trường Brazil và cánh cửa dẫn đến mở rộng quốc tế.",
        "pix_kpis": [
            ("30,1 tỷ", "Giao dịch năm 2025", "+20% so với 2024 · Febraban"),
            ("76,4%", "dân số sử dụng Pix", "211 triệu người Brazil · Ngân hàng Trung ương"),
            ("R$ 68,2 nghìn tỷ", "luân chuyển nửa cuối 2025", "78,4 tỷ giao dịch · Ngân hàng Trung ương"),
            ("~80 tỷ", "giao dịch năm 2025", "+25,7% so với năm trước · Báo cáo Pix"),
        ],
        "pix_fonte": "Nguồn: Ngân hàng Trung ương Brazil (Pix bằng Số) và Febraban (Khảo sát Công nghệ Ngân hàng).",
        "ref_titulo": "Tài liệu Tham khảo",
        "ref_intro": "Các nguồn được sử dụng cho dữ liệu thị trường, dự báo và chỉ số của bài thuyết trình này.",
        "ref_lista": [
            ("Global Wellness Institute", "Nền kinh tế chăm sóc sức khỏe toàn cầu: 6,8 nghìn tỷ USD (2024) → 9,8 nghìn tỷ USD (2029)."),
            ("MarkNtel Advisors", "Ứng dụng chiêm tinh và số học: 3 tỷ USD → 9 tỷ USD vào 2030 (CAGR ~20%)."),
            ("IMF · Ngân hàng Thế giới", "GDP và ngang giá sức mua (PPP) theo quốc gia."),
            ("Ngân hàng Trung ương Brazil", "Thống kê chính thức về Pix: giao dịch, khối lượng và người dùng."),
            ("Febraban", "Khảo sát Công nghệ Ngân hàng — tăng trưởng Pix năm 2025."),
            ("IBGE", "Dân số và các chỉ số kinh tế xã hội của Brazil."),
        ],
        },           
           
"he": {
        "titulo": "A1ELOS נומרולוגיה גלובלית",
        "subtitulo": "מדע המספרים מיושם להצלחתך",
        "capa_nota": "מצגת אסטרטגית למשקיעים ושותפים",
        "confidencial": "סוֹדִי",
        "ano": "2026",
        "sumario_titulo": "תקציר מנהלים",
        "duns_porque": "למה DUNS חשוב?",
        "preco_consciente": "תמחור מודע",
        "idioma_col": "שפה",
        "falantes_col": "דוברים (מיליונים)",
        "linhas_idiomas": [
           ["אנגלית", "1,528"],
           ["מנדרינית", "1,184"],
           ["ספרדית", "558"],
           ["צרפתית", "396"],
           ["ערבית", "335"],
           ["פורטוגזית", "270"],
           ["רוסית", "255"],
           ["אינדונזית", "255"],
           ["גרמנית", "134"],
           ["יפנית", "123"],
           ["וייטנאמית", "97"],
           ["טורקית", "90"],
           ["איטלקית", "85"],
           ["עברית", "9"],
        ],
        "total_linha": "סה\"כ",
        "fonte_receita": "מקור הכנסה",
        "participacao": "חלק",
        "b2c_linha": "B2C — 14 שפות",
        "b2b_linha": "B2B — הנחות פרוגרסיביות",
        "pub_linha": "פרסום מבוסס מיקום",
        "tabela_descontos": "טבלת הנחות פרוגרסיביות",
        "grafico_anos": ["שנה 1", "שנה 3", "שנה 5", "שנה 7", "שנה 10"],
        "grafico_titulo": "תחזית שמרנית (R$ אלפים)",
        "grafico_titulo_linha": "צמיחה חזויה (R$ אלפים)",
        "fale_conosco": "צור קשר",
        "sumario_intro": "מצגת זו בנויה כדי להנחות משקיעים ושותפים דרך כל ההיבטים האסטרטגיים של A1ELOS נומרולוגיה גלובלית — מתזת השוק ועד למודל ההכנסה החוזרת.",
        "sumario_cards": [
            ("01", "על A1ELOS", "חברת אחזקות, פורטפוליו ואישור DUNS"),
            ("02", "הזדמנות שוק", "כלכלת הבריאות העולמית 6.8 טריליון דולר"),
            ("03", "פתרון והיקף גלובלי", "14 שפות, ~5.3 מיליארד דוברים"),
            ("04", "3 שווקים חדשים", "אינדונזיה, טורקיה ווייטנאם"),
            ("05", "פורטפוליו ומחירים", "23 מוצרים מכוילים לפי כוח קנייה"),
            ("06", "הכנסה חוזרת", "באנרים פרסומיים וחבילות B2B"),
            ("07", "תחזיות והשקעה", "אופק של 50 שנה · סבב Seed R$ 3.5 מיליון"),
        ],
        "sobre_titulo": "על A1ELOS",
        "sobre_texto": "A1ELOS היא חברת אחזקות טכנולוגיה וידע המשלבת בינה מלאכותית, נומרולוגיה יישומית ואסטרטגיה תרבותית כדי ליצור מוצרים דיגיטליים בעלי השפעה גבוהה בקנה מידה עולמי. המשימה שלנו: לדמוקרטיזציה של ידע עצמי מספרי עם כבוד תרבותי וכבוד לכוח הקנייה של כל שוק.",
        "sobre_kpis": [
            ("23", "מוצרים פעילים", "ב-4 רמות גישה"),
            ("14", "שפות", "~67% מאוכלוסיית העולם"),
            ("5.3 מיליארד", "דוברים", "שוק אמיתי בר-השגה"),
            ("AI", "משולב", "מנוע התאמה אישית"),
        ],
        "sobre_duns": "DUNS 942242668 — הסמכת Dun & Bradstreet תקפה ביותר מ-190 מדינות, המאפשרת חוזי B2B ומיזמים משותפים בינלאומיים.",
        "duns_titulo": "אמינות בינלאומית",
        "duns_texto": "מספר ה-DUNS הוא הדרכון התאגידי של A1ELOS על הבמה הבינלאומית. הוא מאותת לשותפים, ללקוחות תאגידיים ולמשקיעים שלחברה יש זהות ניתנת לאימות, היסטוריה ניתנת למעקב ויכולת חוזית בכל תחום שיפוט.",
        "duns_numero": "942242668",
        "duns_emitido": "הונפק על ידי Dun & Bradstreet — התקן הגלובלי לזהות עסקית המוכר ביותר מ-190 מדינות.",
        "duns_paises": "190+ מדינות",
        "duns_beneficios": [
            ("חוזי B2B", "הסמכה למכרזים ולספקים גלובליים"),
            ("מיזמים משותפים", "שותפויות בינלאומיות עם בדיקת נאותות מוקלת"),
            ("אמינות מיידית", "סימן רצינות למשקיעים מוסדיים"),
        ],
        "mercado_titulo": "הזדמנות שוק",
        "mercado_texto": "אנו חיים בהתכנסות מושלמת: בריאות דיגיטלית מתפוצצת ברחבי העולם בעוד נומרולוגיה ואסטרולוגיה עוברות לאפליקציות בעלות מעורבות גבוהה. A1ELOS ממוקמת בדיוק בצומת זה, עם 74% מאוכלוסיית העולם כבר מחוברים (~6 מיליארד אנשים).",
        "mercado_cards": [
            ("בריאות גלובלית", "6.8 טריליון דולר → 9.8 טריליון דולר עד 2029 (+7.6% לשנה)"),
            ("אפליקציות אסטרולוגיה/נומרולוגיה", "3 מיליארד דולר → 9 מיליארד דולר עד 2030 · CAGR 20%"),
            ("אפליקציות בריאות", "CAGR 14.9% → 26.2 מיליארד דולר ב-2030"),
            ("משתמשים מקוונים", "74% מהעולם · ~6 מיליארד אנשים"),
        ],
        "problema_titulo": "הבעיה שאנו פותרים",
        "problema_col_esq_titulo": "כשלי השוק הנוכחי",
        "problema_col_esq": [
            ("מחסום שפה", "הרוב המכריע של כלי הנומרולוגיה פועל רק באנגלית, ומודר מיליארדי דוברי שפת אם בשפות אחרות."),
            ("מחירים מנותקים מהמציאות", "מוצרים המתומחרים בדולרים לשווקים מתפתחים יוצרים הדרה כלכלית — המשתמש אינו דוחה את המוצר, אלא את המחיר הבלתי נגיש."),
            ("חוסר עומק", "כלים גנריים מספקים תשובות שטחיות ללא התאמה אישית, ללא הקשר תרבותי וללא יישום מעשי בחיי היומיום."),
        ],
        "problema_col_dir_titulo": "מחיר ההדרה",
        "problema_col_dir": "כאשר פלטפורמה מתעלמת משפה וכוח קנייה, היא נוטשת מרצון את השוק הגדול בעולם: למעלה מ-4 מיליארד אנשים החיים בכלכלות מתפתחות ומדברים שפות שאינן אנגלית. זהו הפער ש-A1ELOS ממלאת בדיוק כירורגי.",
        "problema_destaque": "פלטפורמות המתעלמות מכוח קנייה מקומי מאבדות גישה ליותר מ-60% מהשוק הגלובלי בר-ההשגה.",
        "solucao_titulo": "הפתרון שלנו: 3 עמודי תווך אסטרטגיים",
        "solucao_texto": "A1ELOS בנתה פלטפורמה משולבת המשלבת מדע מספרים, בינה מלאכותית ורגישות תרבותית. הפתרון פועל בשלוש חזיתות משלימות, ומבטיח הכנסה מגוונת ושימור גבוה.",
        "solucao_colunas": [
            ("מפות אישיות", "ניתוחים מספריים עמוקים ומותאמים אישית למשתמש הקצה — זהות, משימה, מחזורי חיים ותאימות — המועברים ב-14 שפות עם AI משולב."),
            ("נומרולוגיה עסקית", "אבחונים נומרולוגיים המיושמים על מותגים, CNPJ, תאריכי הקמה ואסטרטגיה תאגידית. מוצר מובחן בעל ערך נתפס גבוה לשוק ה-B2B."),
            ("White-Label B2B", "רישוי הפלטפורמה לחברות שותפות המעוניינות להציע נומרולוגיה תחת המותג שלהן — עם תמיכה רב-לשונית והתאמה מלאה."),
        ],
        "alcance_titulo": "היקף גלובלי: 14 שפות · ~5.3 מיליארד דוברים",
        "alcance_texto": "A1ELOS מכסה ~67% מאוכלוסיית העולם עם פלטפורמה רב-לשונית באמת. כל שפה מייצגת שוק תרבותי נפרד, עם מחירים מכוילים לכוח הקנייה המקומי.",
        "mercados_titulo": "3 שווקים חדשים: +442 מיליון דוברים",
        "mercados_texto": "ההתרחבות האסטרטגית לאינדונזיה, טורקיה ווייטנאם מייצגת קפיצת מדרגה איכותית: שווקים עם צמיחה כלכלית גבוהה, חדירה דיגיטלית גוברת וביקוש מוכח לפתרונות בריאות דיגיטליים נגישים.",
        "mercados_cards": [
            ("אינדונזיה", ["285 מיליון תושבים", "80.5% חדירת אינטרנט", "~255 מיליון דוברי אינדונזית", "בריאות: 51.2 מיליארד דולר (2025) → 72.8 מיליארד דולר (2034)"]),
            ("טורקיה", ["85.9 מיליון תושבים", "תמ\"ג PPP לנפש 37,301 דולר", "~90 מיליון דוברי טורקית", "מעל הממוצע העולמי (27,211 דולר)"]),
            ("וייטנאם",  ["~100 מיליון תושבים", "תמ\"ג לנפש ~5,066 דולר (+7.4%/שנה)", "~97 מיליון דוברי וייטנאמית", "בריאות: 303 מיליון דולר (2025) → 485 מיליון דולר (2030)"]),
        ],
        "mercados_rodape": "3 שווקים חדשים = +442 מיליון דוברים חדשים בר-השגה — משולבים בפלטפורמה עם מחירים מכוילים תרבותית.",
        "preco_titulo": "פילוסופיית תמחור מודע",
        "preco_esq": "כבוד תרבותי + כבוד לכוח הקנייה = שוק אמיתי בר-השגה. אותה פרופורציית ערך. מחירים שונים. כבוד שווה לכל השווקים.",
        "preco_dir_titulo": "איך זה עובד בפועל",
        "preco_dir": "A1ELOS מיישמת שוויון כוח קנייה (PPP) כקריטריון התמחור המרכזי. אותו מוצר מספק ערך יחסי זהה למשתמש בלאגוס, ג'קרטה, האנוי או ניו יורק — המחיר מכויל כך שהמאמץ הפיננסי יהיה פרופורציונלי להכנסה המקומית.",
        "preco_pilares": [
            ("כיול PPP", "מחירים מותאמים למדד כוח הקנייה של כל מדינה"),
            ("כבוד תרבותי", "שפה, מטבע והקשר מקומי משולבים במוצר"),
            ("המרה מעולה", "מחיר הוגן מייצר יותר המרות ושימור גבוה יותר לאורך זמן"),
        ],
        "portfolio_titulo": "פורטפוליו: 23 מוצרים ב-4 רמות",
        "portfolio_texto": "המבנה השכבתי מבטיח שכל פרופיל משתמש — מהסקרן ועד המקצוען — ימצא הצעה המתאימה לרמת המעורבות וליכולת הפיננסית שלו.",
        "portfolio_tabela": [
            ["רמה", "מוצרים", "טווח מחירים (R$)", "פרופיל"],
            ["בסיסי", "מפה אקספרס, מפה מלאה", "R$ 8 – 17", "סקרן, מגע ראשון"],
            ["בינוני", "חיפוש AI, שם בקלפי, מס' בחירות", "R$ 26 – 53", "משתמש מעורב"],
            ["מתקדם", "נומרולוגיה עסקית, מחזורים, משימה", "R$ 81 – 109", "מקצוען, יזם"],
            ["פרימיום", "אבחונים מלאים, מפות אישיות", "R$ 137 – 305", "הכנסה גבוהה, שימוש תאגידי"],
            ["B2B", "חבילות עסקיות, רישיונות, מתנות", "לפי בקשה", "חברות וצוותים"],
        ],
        "portfolio_rodape": "23 מוצרים מכסים את כל מסע המשתמש, מהמגע הראשון ועד ללקוח הפרימיום החוזר — ממקסמים את ה-LTV לכל שפה ושוק.",
        "negocio_titulo": "מודל עסקי: 3 מקורות הכנסה",
        "negocio_texto": "A1ELOS תוכננה עם הכנסה מגוונת וניתנת להרחבה: מכירה ישירה לצרכן הקצה בקנה מידה עולמי, חוזי B2B בעלי ערך גבוה ופרסום מבוסס מיקום חוזר — שלושה מנועים המזינים זה את זה.",
        "negocio_colunas": [
            ("B2C — 14 שפות", "מכירה ישירה של מוצרים דיגיטליים בכל המטבעות, עם מחירים מותאמים לפי PPP. הרחבה אוטומטית באמצעות AI — ללא צוות תמיכה פרופורציונלי לצמיחה."),
            ("B2B — הנחות פרוגרסיביות", "חבילות תאגידיות למשאבי אנוש, מיתוג מעסיק ומתנות מוסדיות. הנחות של 10% עד 50% לפי נפח. מעל 2,000 קודים, משא ומתן ישיר (תוכנית יהלום). חוזים מגובים על ידי DUNS 942242668."),
            ("פרסום מבוסס מיקום", "באנרים מפולחים לפי מדינה, יבשת או עולם עם רוטציה אוטומטית. הכנסה חוזרת חודשית בעלת ערך גבוה — ללא תלות בנפח מכירות המוצר."),
        ],
        "banners_titulo": "באנרים פרסומיים — הכנסה חודשית צפויה",
        "banners_texto": "פלטפורמת הפרסום מבוסס המיקום של A1ELOS מציעה למפרסמים פילוח מדויק לפי מדינה, יבשת או היקף גלובלי, עם פורמטים מותאמים למחשב ולנייד ורוטציה אוטומטית כל 8 שניות.",
        "banners_tabela": [
            ["פילוח", "קבוע (R$/חודש)", "זמני (R$/חודש)", "פרופיל מפרסם"],
            ["מדינה", "R$ 800", "R$ 500", "עסקים קטנים מקומיים, מסחר אזורי"],
            ["יבשת", "R$ 1,800", "R$ 1,200", "מותגים אזוריים, התרחבות יבשתית"],
            ["עולם", "R$ 3,500", "R$ 2,500", "חברות גלובליות, אפליקציות בינלאומיות"],
            ["חסות בלעדית", "R$ 6,000", "R$ 4,500/קמפיין", "נותני חסות ראשיים, השקות"],
        ],
        "banners_formatos": "728×90 px — באנר מרכזי למחשב · 320×100 px — פורמט נייד מותאם · 8 שניות — רוטציה אוטומטית · יעד גיאוגרפי — מדינה, יבשת או היקף עולמי",
        "b2b_titulo": "חבילות עסקיות B2B — ערך גבוה, נפח גבוה",
        "b2b_texto": "חבילות ה-B2B הופכות את A1ELOS לכלי למיתוג מעסיק ולבריאות תאגידית. חברות רוכשות קודי גישה בכמויות כדי לחלקם כמתנות לעובדים או ללקוחות — מגובות על ידי DUNS 942242668 לחוזים תאגידיים רשמיים.",
        "b2b_planos": [
            ("תוכנית בסיסית · 50 קודים", "50× מפה אקספרס (R$ 8 כל אחד). אידיאלית לתוכניות הטבות לעובדים ולפעולות שילוב."),
            ("תוכנית בינונית · 100 קודים", "50× מפה אקספרס + 50× חיפוש AI (R$ 17). מושלמת לצוותים ולאסטרטגיית מיתוג מעסיק."),
            ("תוכנית פרימיום · 200 קודים", "100× מפה אקספרס + 100× מפה מלאה (R$ 17). עומק אנליטי מרבי לקבוצות גדולות."),
        ],
        "b2b_tabela": [
            ["החל מ-", "הנחה", "פרופיל", "שימוש מומלץ"],
            ["10 קודים", "10%", "צוותים קטנים", "פעולת בריאות חד פעמית"],
            ["50 קודים", "20%", "צוותים בצמיחה", "תוכניות חוזרות"],
            ["100 קודים", "25%", "עסקים קטנים ובינוניים", "הטבה רבעונית"],
            ["200 קודים", "30%", "חברות בינוניות", "תוכניות מלאות"],
            ["500 קודים", "40%", "חברות בינוניות", "מתנה שנתית לעובדים"],
            ["1,000 קודים", "45%", "תאגידים גדולים", "נאמנות לקוחות"],
            ["2,000 קודים", "50%", "קבוצות גדולות", "קנה מידה גדול"],
            ["מעל 2,000", "ניתן למשא ומתן", "תוכנית יהלום מותאמת", "חלוקת בונוסים בכמות"],
        ],
        "projecoes_titulo": "תחזיות פיננסיות: אופק של 50 שנה",
        "projecoes_texto": "התחזיות נבנו על בסיס הערכות אחוזי חדירה לשוק הפוטנציאלי של ~5.32 מיליארד דוברים, עם המרה שמרנית של 3% ומימוש בונוס בין 70% ל-90%. העשור הראשון מפורט בשנים 1, 3, 5 ו-7 כדי להדגיש את המומנטום.",
        "projecoes_tabela": [
            ["אופק", "שמרני (R$)", "אופטימי (R$)"],
            ["שנה 1", "R$ 281 אלף", "R$ 702 אלף"],
            ["שנה 3", "R$ 983 אלף", "R$ 2.8 מיליון"],
            ["שנה 5", "R$ 2.8 מיליון", "R$ 7 מיליון"],
            ["שנה 7", "R$ 5.6 מיליון", "R$ 14 מיליון"],
            ["שנה 10", "R$ 11.2 מיליון", "R$ 28.1 מיליון"],
            ["שנה 20", "R$ 42.1 מיליון", "R$ 112 מיליון"],
            ["שנה 30", "R$ 84.3 מיליון", "R$ 211 מיליון"],
            ["שנה 40", "R$ 126 מיליון", "R$ 351 מיליון"],
            ["שנה 50", "R$ 169 מיליון", "R$ 492 מיליון"],
        ],
        "tracao_titulo": "מומנטום ותוצאות מוכחות",
        "tracao_texto": "A1ELOS כבר פועלת עם מדדי מוצר המאמתים את המודל — שימור גבוה, דירוג פרימיום ובסיס שותפי B2B הולך וגדל מוכיחים שהפלטפורמה מספקת ערך אמיתי למשתמש הקצה ולשוק התאגידי.",
        "tracao_kpis": [
            ("12K+", "משתמשים פעילים", "בסיס אורגני גדל בעקביות"),
            ("87%", "שימור", "הרבה מעל ממוצע התעשייה (~30%)"),
            ("4.8★", "דירוג ממוצע", "שביעות רצון מוכחת של משתמש הקצה"),
            ("23", "שותפי B2B", "חוזים פעילים עם חברות ומשאבי אנוש"),
        ],
        "roteiro_titulo": "מפת דרכים אסטרטגית",
        "roteiro_texto": "A1ELOS מבצעת תוכנית בארבעה שלבים מתקדמים — מאיחוד הבסיס הנוכחי ועד למנהיגות שוק גלובלית, עם אפשרויות יציאה ברורות למשקיעים.",
        "roteiro_fases": [
            ("שלב 1 · איחוד", "חיזוק בסיס המשתמשים בשפות הפעילות כבר. אופטימיזציה של המרה, שימור ו-LTV. סבב Seed הושלם."),
            ("שלב 2 · התרחבות", "השקה רשמית ב-3 השווקים החדשים: אינדונזיה, טורקיה ווייטנאם. האצת ערוץ ה-B2B והפרסום מבוסס המיקום."),
            ("שלב 3 · כניסה גלובלית", "נוכחות פעילה בכל 14 השפות עם קמפיינים מותאמים. שותפויות white-label ביותר מ-5 יבשות. סבב A."),
            ("שלב 4 · מנהיגות", "יותר מ-20 מדינות עם פעילות מאוחדת. פלטפורמת SaaS גלובלית מובילה בנומרולוגיה יישומית. הנפקה או יציאה אסטרטגית."),
        ],
        "invest_titulo": "השקעה ויצירת קשר",
        "invest_texto": "אנו מוכנים למצגות פרטיות, בדיקת נאותות ומשא ומתן. צרו קשר דרך הערוץ המועדף עליכם.",
        "invest_dados": [
            ("סבב Seed", "R$ 3.5 מיליון"),
            ("הערכת שווי טרום השקעה", "R$ 14 מיליון"),
            ("הון מוצע", "עד 20%"),
        ],
        "invest_contato": [
            ("דוא\"ל משקיעים", "a1elos.consultoria@gmail.com"),
            ("דוא\"ל כללי", "contato@a1elos.com"),
            ("אתר", "www.a1elos.com"),
            ("DUNS", "942242668 — Dun & Bradstreet"),
        ],
        "invest_alocacao": "הקצאת הון: 45% טכנולוגיה · 30% שיווק · 25% תפעול",
        "frase_final": "המספרים אף פעם לא משקרים.",
        "selo_final": ["DUNS 942242668", "23 מוצרים", "14 שפות", "~5.3 מיליארד דוברים"],
        "graf_cons": "שמרני",
        "graf_otim": "אופטימי",
        "grafico_titulo_linha": "צמיחה חזויה (R$ אלפים)",
        "pix_titulo": "ברזיל: תשתית Pix",
        "pix_texto": "Pix היא תשתית התשלומים המיידיים הציבורית של ברזיל. עבור A1ELOS, היא מבטיחה גבייה מיידית, עלות נמוכה וקבלה אוניברסלית — הבסיס לפעילות ה-B2C בשוק הברזילאי והשער להתרחבות בינלאומית.",
        "pix_kpis": [
            ("30.1 מיליארד", "עסקאות ב-2025", "+20% לעומת 2024 · Febraban"),
            ("76.4%", "מהאוכלוסייה משתמשת ב-Pix", "211 מיליון ברזילאים · הבנק המרכזי"),
            ("R$ 68.2 טריליון", "תנועה במחצית השנייה 2025", "78.4 מיליארד עסקאות · הבנק המרכזי"),
            ("~80 מיליארד", "עסקאות ב-2025", "+25.7% לעומת השנה הקודמת · דוח Pix"),
        ],
        "pix_fonte": "מקורות: הבנק המרכזי של ברזיל (Pix במספרים) ו-Febraban (סקר טכנולוגיה בנקאית).",
        "ref_titulo": "הפניות ביבליוגרפיות",
        "ref_intro": "מקורות ששימשו לנתוני השוק, התחזיות והמדדים של מצגת זו.",
        "ref_lista": [
            ("Global Wellness Institute", "כלכלת הבריאות העולמית: 6.8 טריליון דולר (2024) → 9.8 טריליון דולר (2029)."),
            ("MarkNtel Advisors", "אפליקציות אסטרולוגיה ונומרולוגיה: 3 מיליארד דולר → 9 מיליארד דולר עד 2030 (CAGR ~20%)."),
            ("IMF · הבנק העולמי", "תמ\"ג ושוויון כוח קנייה (PPP) לפי מדינה."),
            ("הבנק המרכזי של ברזיל", "סטטיסטיקות רשמיות של Pix: עסקאות, נפח ומשתמשים."),
            ("Febraban", "סקר טכנולוגיה בנקאית — צמיחת Pix ב-2025."),
            ("IBGE", "אוכלוסייה ומדדים סוציו-אקונומיים של ברזיל."),
        ],
        },

"ar": {
        "titulo": "A1ELOS علم الأرقام العالمي",
        "subtitulo": "علم الأرقام مطبق على نجاحك",
        "capa_nota": "عرض تقديمي استراتيجي للمستثمرين والشركاء",
        "confidencial": "سري",
        "ano": "2026",
        "sumario_titulo": "الملخص التنفيذي",
        "duns_porque": "لماذا DUNS مهم؟",
        "preco_consciente": "التسعير الواعي",
        "idioma_col": "اللغة",
        "falantes_col": "المتحدثون (مليون)",
        "linhas_idiomas": [
           ["الإنجليزية", "1,528"],
           ["الماندرين", "1,184"],
           ["الإسبانية", "558"],
           ["الفرنسية", "396"],
           ["العربية", "335"],
           ["البرتغالية", "270"],
           ["الروسية", "255"],
           ["الإندونيسية", "255"],
           ["الألمانية", "134"],
           ["اليابانية", "123"],
           ["الفيتنامية", "97"],
           ["التركية", "90"],
           ["الإيطالية", "85"],
           ["العبرية", "9"],
        ],
        "total_linha": "الإجمالي",
        "fonte_receita": "مصدر الإيرادات",
        "participacao": "الحصة",
        "b2c_linha": "B2C — 14 لغة",
        "b2b_linha": "B2B — خصومات تدريجية",
        "pub_linha": "إعلانات تحديد المواقع",
        "tabela_descontos": "جدول الخصومات التدريجية",
        "grafico_anos": ["السنة 1", "السنة 3", "السنة 5", "السنة 7", "السنة 10"],
        "grafico_titulo": "توقعات متحفظة (R$ ألف)",
        "grafico_titulo_linha": "النمو المتوقع (R$ ألف)",
        "fale_conosco": "تواصل معنا",
        "sumario_intro": "تم تنظيم هذا العرض التقديمي لتوجيه المستثمرين والشركاء عبر جميع الجوانب الاستراتيجية لـ A1ELOS علم الأرقام العالمي — من أطروحة السوق إلى نموذج الإيرادات المتكررة.",
        "sumario_cards": [
            ("01", "عن A1ELOS", "شركة قابضة ومحفظة واعتماد DUNS"),
            ("02", "فرصة السوق", "اقتصاد الصحة العالمي 6.8 تريليون دولار"),
            ("03", "الحل والنطاق العالمي", "14 لغة، ~5.3 مليار متحدث"),
            ("04", "3 أسواق جديدة", "إندونيسيا وتركيا وفيتنام"),
            ("05", "المحفظة والأسعار", "23 منتجًا معايرًا حسب القوة الشرائية"),
            ("06", "الإيرادات المتكررة", "لافتات إعلانية وحزم B2B"),
            ("07", "التوقعات والاستثمار", "أفق 50 عامًا · جولة تأسيسية R$ 3.5 مليون"),
        ],
        "sobre_titulo": "عن A1ELOS",
        "sobre_texto": "A1ELOS هي شركة قابضة للتكنولوجيا والمعرفة تجمع بين الذكاء الاصطناعي وعلم الأرقام التطبيقي والاستراتيجية الثقافية لإنشاء منتجات رقمية عالية التأثير على نطاق عالمي. مهمتنا: إضفاء الطابع الديمقراطي على المعرفة الذاتية الرقمية مع احترام الثقافة واحترام القوة الشرائية لكل سوق.",
        "sobre_kpis": [
            ("23", "منتجات نشطة", "في 4 مستويات وصول"),
            ("14", "لغات", "~67% من سكان العالم"),
            ("5.3 مليار", "متحدث", "سوق حقيقي يمكن الوصول إليه"),
            ("AI", "مدمج", "محرك التخصيص"),
        ],
        "sobre_duns": "DUNS 942242668 — شهادة Dun & Bradstreet صالحة في أكثر من 190 دولة، مما يتيح عقود B2B والمشاريع المشتركة الدولية.",
        "duns_titulo": "المصداقية الدولية",
        "duns_texto": "رقم DUNS هو جواز السفر المؤسسي لـ A1ELOS على الساحة الدولية. إنه يشير للشركاء والعملاء المؤسسيين والمستثمرين إلى أن الشركة تمتلك هوية قابلة للتحقق وتاريخًا قابلًا للتتبع وقدرة تعاقدية في أي ولاية قضائية.",
        "duns_numero": "942242668",
        "duns_emitido": "صادر عن Dun & Bradstreet — المعيار العالمي لهوية الأعمال المعترف به في أكثر من 190 دولة.",
        "duns_paises": "190+ دولة",
        "duns_beneficios": [
            ("عقود B2B", "الأهلية للمناقصات والموردين العالميين"),
            ("مشاريع مشتركة", "شراكات دولية مع العناية الواجبة الميسرة"),
            ("مصداقية فورية", "علامة على الجدية للمستثمرين المؤسسيين"),
        ],
        "mercado_titulo": "فرصة السوق",
        "mercado_texto": "نعيش التقاءً مثاليًا: الصحة الرقمية تنفجر عالميًا بينما ينتقل علم الأرقام وعلم التنجيم إلى تطبيقات عالية التفاعل. A1ELOS في موقع دقيق عند هذا التقاطع، مع 74% من سكان العالم متصلين بالفعل (~6 مليارات شخص).",
        "mercado_cards": [
            ("الصحة العالمية", "6.8 تريليون دولار → 9.8 تريليون دولار بحلول 2029 (+7.6% سنويًا)"),
            ("تطبيقات التنجيم/الأرقام", "3 مليارات دولار → 9 مليارات دولار بحلول 2030 · CAGR 20%"),
            ("تطبيقات الصحة", "CAGR 14.9% → 26.2 مليار دولار في 2030"),
            ("المستخدمون عبر الإنترنت", "74% من العالم · ~6 مليارات شخص"),
        ],
        "problema_titulo": "المشكلة التي نحلها",
        "problema_col_esq_titulo": "عيوب السوق الحالية",
        "problema_col_esq": [
            ("حاجز اللغة", "الغالبية العظمى من أدوات علم الأرقام تعمل بالإنجليزية فقط، مستبعدة مليارات الناطقين الأصليين بلغات أخرى."),
            ("أسعار منفصلة عن الواقع", "المنتجات المسعرة بالدولار للأسواق الناشئة تخلق إقصاءً اقتصاديًا — المستخدم لا يرفض المنتج، بل يرفض السعر غير المتاح."),
            ("نقص العمق", "الأدوات العامة تقدم إجابات سطحية دون تخصيص، دون سياق ثقافي ودون تطبيق عملي في الحياة اليومية."),
        ],
        "problema_col_dir_titulo": "تكلفة الإقصاء",
        "problema_col_dir": "عندما تتجاهل منصة اللغة والقوة الشرائية، فإنها تتخلى طوعًا عن أكبر سوق في العالم: أكثر من 4 مليارات شخص يعيشون في اقتصادات ناشئة ويتحدثون لغات غير الإنجليزية. هذه هي الفجوة التي تملؤها A1ELOS بدقة جراحية.",
        "problema_destaque": "المنصات التي تتجاهل القوة الشرائية المحلية تفقد الوصول إلى أكثر من 60% من السوق العالمي المتاح.",
        "solucao_titulo": "حلنا: 3 ركائز استراتيجية",
        "solucao_texto": "بنَت A1ELOS منصة متكاملة تجمع بين علم الأرقام والذكاء الاصطناعي والحساسية الثقافية. يعمل الحل على ثلاث جبهات متكاملة، مما يضمن إيرادات متنوعة واحتفاظًا مرتفعًا.",
        "solucao_colunas": [
            ("الخرائط الشخصية", "تحليلات رقمية عميقة ومخصصة للمستخدم النهائي — الهوية والمهمة ودورات الحياة والتوافق — تُقدم بـ 14 لغة مع ذكاء اصطناعي مدمج."),
            ("علم الأرقام للأعمال", "تشخيصات رقمية مطبقة على العلامات التجارية وCNPJ وتواريخ التأسيس والاستراتيجية المؤسسية. منتج متمايز ذو قيمة مدركة عالية لسوق B2B."),
            ("White-Label B2B", "ترخيص المنصة لشركات الشركاء الراغبة في تقديم علم الأرقام تحت علامتها التجارية الخاصة — مع دعم متعدد اللغات وتخصيص كامل."),
        ],
        "alcance_titulo": "النطاق العالمي: 14 لغة · ~5.3 مليار متحدث",
        "alcance_texto": "تغطي A1ELOS ~67% من سكان العالم بمنصة متعددة اللغات حقًا. تمثل كل لغة سوقًا ثقافيًا متميزًا، مع أسعار معايرة وفق القوة الشرائية المحلية.",
        "mercados_titulo": "3 أسواق جديدة: +442 مليون متحدث",
        "mercados_texto": "يمثل التوسع الاستراتيجي إلى إندونيسيا وتركيا وفيتنام قفزة نوعية: أسواق ذات نمو اقتصادي مرتفع وانتشار رقمي متزايد وطلب مثبت على حلول الصحة الرقمية المتاحة.",
        "mercados_cards": [
            ("إندونيسيا", ["285 مليون نسمة", "80.5% انتشار الإنترنت", "~255 مليون متحدث بالإندونيسية", "الصحة: 51.2 مليار دولار (2025) → 72.8 مليار دولار (2034)"]),
            ("تركيا", ["85.9 مليون نسمة", "ناتج محلي PPP للفرد 37,301 دولار", "~90 مليون متحدث بالتركية", "فوق المتوسط العالمي (27,211 دولار)"]),
            ("فيتنام",  ["~100 مليون نسمة", "ناتج محلي للفرد ~5,066 دولار (+7.4%/سنة)", "~97 مليون متحدث بالفيتنامية", "الصحة: 303 ملايين دولار (2025) → 485 مليون دولار (2030)"]),
        ],
        "mercados_rodape": "3 أسواق جديدة = +442 مليون متحدث جديد يمكن الوصول إليه — مدمجون في المنصة بأسعار معايرة ثقافيًا.",
        "preco_titulo": "فلسفة التسعير الواعي",
        "preco_esq": "احترام الثقافة + احترام القوة الشرائية = سوق حقيقي يمكن الوصول إليه. نفس نسبة القيمة. أسعار مختلفة. كرامة متساوية لجميع الأسواق.",
        "preco_dir_titulo": "كيف يعمل عمليًا",
        "preco_dir": "تطبق A1ELOS تعادل القوة الشرائية (PPP) كمعيار تسعير مركزي. يوفر المنتج نفسه نفس القيمة النسبية للمستخدم في لاغوس أو جاكرتا أو هانوي أو نيويورك — يُعاير السعر بحيث يكون الجهد المالي متناسبًا مع الدخل المحلي.",
        "preco_pilares": [
            ("معايرة PPP", "أسعار معدلة وفق مؤشر القوة الشرائية لكل دولة"),
            ("احترام الثقافة", "اللغة والعملة والسياق المحلي مدمجة في المنتج"),
            ("تحويل متفوق", "السعر العادل يولد تحويلًا أكثر واحتفاظًا أعلى على المدى الطويل"),
        ],
        "portfolio_titulo": "المحفظة: 23 منتجًا في 4 مستويات",
        "portfolio_texto": "يضمن الهيكل الطبقي أن يجد كل ملف مستخدم — من الفضولي إلى المحترف — عرضًا مناسبًا لمستوى تفاعله وقدرته المالية.",
        "portfolio_tabela": [
            ["المستوى", "المنتجات", "نطاق السعر (R$)", "الملف"],
            ["أساسي", "خريطة إكسبرس، خريطة كاملة", "R$ 8 – 17", "فضولي، أول اتصال"],
            ["متوسط", "بحث AI، اسم الاقتراع، رقم الانتخاب", "R$ 26 – 53", "مستخدم متفاعل"],
            ["متقدم", "علم الأرقام للأعمال، الدورات، المهمة", "R$ 81 – 109", "محترف، رائد أعمال"],
            ["بريميوم", "تشخيصات كاملة، خرائط شخصية", "R$ 137 – 305", "دخل مرتفع، استخدام مؤسسي"],
            ["B2B", "حزم أعمال، تراخيص، هدايا", "عند الطلب", "شركات وفرق"],
        ],
        "portfolio_rodape": "23 منتجًا تغطي رحلة المستخدم الكاملة، من أول اتصال إلى العميل المتكرر بريميوم — مع تعظيم LTV لكل لغة وسوق.",
        "negocio_titulo": "نموذج الأعمال: 3 مصادر إيرادات",
        "negocio_texto": "صُممت A1ELOS بإيرادات متنوعة وقابلة للتوسع: بيع مباشر للمستهلك النهائي على نطاق عالمي، وعقود B2B عالية القيمة، وإعلانات تحديد مواقع متكررة — ثلاثة محركات تغذي بعضها البعض.",
        "negocio_colunas": [
            ("B2C — 14 لغة", "بيع مباشر للمنتجات الرقمية بجميع العملات، بأسعار معدلة حسب PPP. توسع تلقائي عبر AI — دون فريق دعم متناسب مع النمو."),
            ("B2B — خصومات تدريجية", "حزم مؤسسية للموارد البشرية وعلامة صاحب العمل والهدايا المؤسسية. خصومات من 10% إلى 50% حسب الحجم. فوق 2,000 كود، تفاوض مباشر (خطة الماس). عقود مدعومة بـ DUNS 942242668."),
            ("إعلانات تحديد المواقع", "لافتات مجزأة حسب الدولة أو القارة أو العالم مع تدوير تلقائي. إيرادات شهرية متكررة عالية القيمة — دون الاعتماد على حجم مبيعات المنتج."),
        ],
        "banners_titulo": "اللافتات الإعلانية — إيرادات شهرية يمكن التنبؤ بها",
        "banners_texto": "توفر منصة إعلانات تحديد المواقع من A1ELOS للمعلنين تجزئة دقيقة حسب الدولة أو القارة أو النطاق العالمي، مع تنسيقات محسّنة لسطح المكتب والجوال وتدوير تلقائي كل 8 ثوانٍ.",
        "banners_tabela": [
            ["التجزئة", "ثابت (R$/شهر)", "مؤقت (R$/شهر)", "ملف المعلن"],
            ["دولة", "R$ 800", "R$ 500", "شركات محلية صغيرة، تجارة إقليمية"],
            ["قارة", "R$ 1,800", "R$ 1,200", "علامات إقليمية، توسع قاري"],
            ["العالم", "R$ 3,500", "R$ 2,500", "شركات عالمية، تطبيقات دولية"],
            ["رعاية حصرية", "R$ 6,000", "R$ 4,500/حملة", "رعاة رئيسيون، إطلاقات"],
        ],
        "banners_formatos": "728×90 px — لافتة مركزية لسطح المكتب · 320×100 px — تنسيق جوال محسّن · 8 ثوانٍ — تدوير تلقائي · استهداف جغرافي — دولة أو قارة أو نطاق عالمي",
        "b2b_titulo": "حزم أعمال B2B — قيمة عالية، حجم كبير",
        "b2b_texto": "تحول حزم B2B منصة A1ELOS إلى أداة لعلامة صاحب العمل والصحة المؤسسية. تشتري الشركات رموز الوصول بكميات كبيرة لتوزيعها كهدايا على الموظفين أو العملاء — مدعومة بـ DUNS 942242668 للعقود المؤسسية الرسمية.",
        "b2b_planos": [
            ("الخطة الأساسية · 50 كودًا", "50× خريطة إكسبرس (R$ 8 لكل منها). مثالية لبرامج مزايا الموظفين وإجراءات الدمج."),
            ("الخطة المتوسطة · 100 كود", "50× خريطة إكسبرس + 50× بحث AI (R$ 17). مثالية للفرق واستراتيجية علامة صاحب العمل."),
            ("الخطة بريميوم · 200 كود", "100× خريطة إكسبرس + 100× خريطة كاملة (R$ 17). أقصى عمق تحليلي للمجموعات الكبيرة."),
        ],
        "b2b_tabela": [
            ["من", "الخصم", "الملف", "الاستخدام الموصى به"],
            ["10 أكواد", "10%", "فرق صغيرة", "إجراء صحة لمرة واحدة"],
            ["50 كودًا", "20%", "فرق في نمو", "برامج متكررة"],
            ["100 كود", "25%", "شركات صغيرة ومتوسطة", "ميزة ربع سنوية"],
            ["200 كود", "30%", "شركات متوسطة", "برامج كاملة"],
            ["500 كود", "40%", "شركات متوسطة", "هدية سنوية للموظفين"],
            ["1,000 كود", "45%", "شركات كبيرة", "ولاء العملاء"],
            ["2,000 كود", "50%", "مجموعات كبيرة", "نطاق واسع"],
            ["فوق 2,000", "قابل للتفاوض", "خطة الماس المخصصة", "توزيع المكافآت بالحجم"],
        ],
        "projecoes_titulo": "التوقعات المالية: أفق 50 عامًا",
        "projecoes_texto": "بُنيت التوقعات على أساس تقديرات النسبة المئوية للاختراق للسوق المحتمل البالغ ~5.32 مليار متحدث، مع تحويل متحفظ بنسبة 3% واسترداد المكافآت بين 70% و90%. يُفصَّل العقد الأول في السنوات 1 و3 و5 و7 لإبراز الزخم.",
        "projecoes_tabela": [
            ["الأفق", "متحفظ (R$)", "متفائل (R$)"],
            ["السنة 1", "R$ 281 ألف", "R$ 702 ألف"],
            ["السنة 3", "R$ 983 ألف", "R$ 2.8 مليون"],
            ["السنة 5", "R$ 2.8 مليون", "R$ 7 ملايين"],
            ["السنة 7", "R$ 5.6 مليون", "R$ 14 مليونًا"],
            ["السنة 10", "R$ 11.2 مليون", "R$ 28.1 مليون"],
            ["السنة 20", "R$ 42.1 مليون", "R$ 112 مليونًا"],
            ["السنة 30", "R$ 84.3 مليون", "R$ 211 مليونًا"],
            ["السنة 40", "R$ 126 مليونًا", "R$ 351 مليونًا"],
            ["السنة 50", "R$ 169 مليونًا", "R$ 492 مليونًا"],
        ],
        "tracao_titulo": "الزخم والنتائج المثبتة",
        "tracao_texto": "تعمل A1ELOS بالفعل بمقاييس منتج تثبت النموذج — الاحتفاظ المرتفع والتقييم المتميز وقاعدة الشراكات B2B المتنامية تُظهر أن المنصة تقدم قيمة حقيقية للمستخدم النهائي والسوق المؤسسي.",
        "tracao_kpis": [
            ("12K+", "مستخدمون نشطون", "قاعدة عضوية تنمو باستمرار"),
            ("87%", "الاحتفاظ", "فوق متوسط الصناعة بكثير (~30%)"),
            ("4.8★", "متوسط التقييم", "رضا مثبت للمستخدم النهائي"),
            ("23", "شركاء B2B", "عقود نشطة مع شركات وموارد بشرية"),
        ],
        "roteiro_titulo": "خارطة الطريق الاستراتيجية",
        "roteiro_texto": "تنفذ A1ELOS خطة في أربع مراحل متدرجة — من توحيد القاعدة الحالية إلى الريادة العالمية في السوق، مع خيارات خروج واضحة للمستثمرين.",
        "roteiro_fases": [
            ("المرحلة 1 · التوحيد", "تعزيز قاعدة المستخدمين في اللغات النشطة بالفعل. تحسين التحويل والاحتفاظ وLTV. اكتملت الجولة التأسيسية."),
            ("المرحلة 2 · التوسع", "إطلاق رسمي في 3 أسواق جديدة: إندونيسيا وتركيا وفيتنام. تسريع قناة B2B وإعلانات تحديد المواقع."),
            ("المرحلة 3 · الدخول العالمي", "حضور نشط في جميع اللغات الـ14 بحملات محلية. شراكات white-label في أكثر من 5 قارات. السلسلة A."),
            ("المرحلة 4 · الريادة", "أكثر من 20 دولة بعمليات موحدة. منصة SaaS مرجعية عالمية في علم الأرقام التطبيقي. اكتتاب عام أو خروج استراتيجي."),
        ],
        "invest_titulo": "الاستثمار والتواصل",
        "invest_texto": "نحن جاهزون للعروض الخاصة والعناية الواجبة والمفاوضات. تواصل معنا عبر القناة المفضلة لديك.",
        "invest_dados": [
            ("الجولة التأسيسية", "R$ 3.5 مليون"),
            ("التقييم قبل الاستثمار", "R$ 14 مليونًا"),
            ("الحقوق المقدمة", "حتى 20%"),
        ],
        "invest_contato": [
            ("بريد المستثمرين", "a1elos.consultoria@gmail.com"),
            ("البريد العام", "contato@a1elos.com"),
            ("الموقع", "www.a1elos.com"),
            ("DUNS", "942242668 — Dun & Bradstreet"),
        ],
        "invest_alocacao": "تخصيص رأس المال: 45% تكنولوجيا · 30% تسويق · 25% عمليات",
        "frase_final": "الأرقام لا تكذب أبدًا.",
        "selo_final": ["DUNS 942242668", "23 منتجًا", "14 لغة", "~5.3 مليار متحدث"],
        "graf_cons": "متحفظ",
        "graf_otim": "متفائل",
        "grafico_titulo_linha": "النمو المتوقع (R$ ألف)",
        "pix_titulo": "البرازيل: البنية التحتية Pix",
        "pix_texto": "Pix هي البنية التحتية العامة للمدفوعات الفورية في البرازيل. بالنسبة لـ A1ELOS، تضمن تحصيلًا فوريًا وتكلفة منخفضة وقبولًا عالميًا — أساس عملية B2C في السوق البرازيلية وبوابة التوسع الدولي.",
        "pix_kpis": [
            ("30.1 مليار", "معاملة في 2025", "+20% مقارنة بـ 2024 · Febraban"),
            ("76.4%", "من السكان يستخدمون Pix", "211 مليون برازيلي · البنك المركزي"),
            ("R$ 68.2 تريليون", "حركة في النصف الثاني 2025", "78.4 مليار معاملة · البنك المركزي"),
            ("~80 مليار", "معاملة في 2025", "+25.7% مقارنة بالعام السابق · تقرير Pix"),
        ],
        "pix_fonte": "المصادر: البنك المركزي البرازيلي (Pix بالأرقام) وFebraban (مسح التكنولوجيا المصرفية).",
        "ref_titulo": "المراجع الببليوغرافية",
        "ref_intro": "المصادر المستخدمة لبيانات السوق والتوقعات والمؤشرات في هذا العرض التقديمي.",
        "ref_lista": [
            ("Global Wellness Institute", "اقتصاد الصحة العالمي: 6.8 تريليون دولار (2024) → 9.8 تريليون دولار (2029)."),
            ("MarkNtel Advisors", "تطبيقات التنجيم وعلم الأرقام: 3 مليارات دولار → 9 مليارات دولار بحلول 2030 (CAGR ~20%)."),
            ("IMF · البنك الدولي", "الناتج المحلي وتعادل القوة الشرائية (PPP) حسب الدولة."),
            ("البنك المركزي البرازيلي", "إحصاءات Pix الرسمية: المعاملات والحجم والمستخدمون."),
            ("Febraban", "مسح التكنولوجيا المصرفية — نمو Pix في 2025."),
            ("IBGE", "سكان البرازيل ومؤشراتها الاجتماعية والاقتصادية."),
        ],
      },
} 
# ------------------------------------------------------------
# DADOS NUMÉRICOS DAS TABELAS
# ------------------------------------------------------------
LINHAS_IDIOMAS = [
    ("Inglês", "1.528"), ("Mandarim", "1.184"), ("Espanhol", "558"),
    ("Francês", "396"), ("Árabe", "335"), ("Português", "270"),
    ("Russo", "255"), ("Indonésio", "255"), ("Alemão", "134"),
    ("Japonês", "123"), ("Vietnamita", "97"), ("Turco", "90"),
    ("Italiano", "85"), ("Hebraico", "9"),
]

# ------------------------------------------------------------
# DADOS NUMÉRICOS DAS TABELAS
# ------------------------------------------------------------
LINHAS_IDIOMAS = [
    ("Inglês", "1.528"), ("Mandarim", "1.184"), ("Espanhol", "558"),
    ("Francês", "396"), ("Árabe", "335"), ("Português", "270"),
    ("Russo", "255"), ("Indonésio", "255"), ("Alemão", "134"),
    ("Japonês", "123"), ("Vietnamita", "97"), ("Turco", "90"),
    ("Italiano", "85"), ("Hebraico", "9"),
]

# ------------------------------------------------------------
# ENTRADA PRINCIPAL
# ------------------------------------------------------------
def _tabela_editorial(doc, x, y, largura, dados, proporcoes, tam, lang, moeda_cols=()):
    """Desenha uma tabela editorial e retorna o novo y.
    moeda_cols: tupla de índices de colunas que devem receber o símbolo da moeda."""
    if not dados:
        return y
    alt_linha = 7 * mm
    n_cols = len(dados[0])
    largs = [largura * p for p in proporcoes]
    # Cabeçalho (azul, negrito)
    doc.setFillColor(COR_AZUL)
    doc.setFont(_fonte(lang, True), tam)
    xx = x
    for i, cel in enumerate(dados[0]):
        doc.drawString(xx + 1 * mm, y - 5 * mm, str(cel))
        xx += largs[i]
    y -= alt_linha
    # Linha separadora dourada
    doc.setStrokeColor(COR_DOURADO)
    doc.setLineWidth(0.6)
    doc.line(x, y + 1 * mm, x + largura, y + 1 * mm)
    # Corpo (cinza)
    for linha in dados[1:]:
        doc.setFillColor(COR_CINZA)
        doc.setFont(_fonte(lang), tam)
        xx = x
        for i, cel in enumerate(linha):
            texto = str(cel)
            if i in moeda_cols:
                texto = _com_moeda(lang, texto)
            doc.drawString(xx + 1 * mm, y - 5 * mm, texto)
            xx += largs[i]
        y -= alt_linha
    return y

def _grafico_linha(doc, x, y, largura, altura, lang, anos, series, titulo):
    """Gráfico de linhas com legenda traduzida (fonte do idioma)."""
    doc.setFillColor(COR_PRETO)
    doc.setFont(_fonte(lang, True), 9)
    doc.drawString(x, y + altura - 4 * mm, titulo)
    # Eixos
    doc.setStrokeColor(COR_CINZA)
    doc.setLineWidth(0.5)
    doc.line(x, y, x, y + altura - 8 * mm)
    doc.line(x, y, x + largura, y)
    # Valor máximo (para escala)
    max_v = 1
    for nome, vals in series:
        for v in vals:
            max_v = max(max_v, v)
    n = len(anos)
    cores = [COR_AZUL, COR_DOURADO]
    for idx, (nome, vals) in enumerate(series):
        doc.setStrokeColor(cores[idx % len(cores)])
        doc.setLineWidth(1.2)
        p = doc.beginPath()
        for i, v in enumerate(vals):
            px = x + (largura * i) / (n - 1) if n > 1 else x
            py = y + (altura - 8 * mm) * (v / max_v)
            if i == 0:
                p.moveTo(px, py)
            else:
                p.lineTo(px, py)
        doc.drawPath(p, stroke=1, fill=0)
    # Rótulos dos anos (fonte do idioma)
    doc.setFillColor(COR_CINZA)
    doc.setFont(_fonte(lang), 7)
    for i, a in enumerate(anos):
        px = x + (largura * i) / (n - 1) if n > 1 else x
        doc.drawCentredString(px, y - 3 * mm, str(a))
    # ===== LEGENDA (o que cada linha representa) =====
    ly = y - 9 * mm
    for idx, (nome, vals) in enumerate(series):
        doc.setStrokeColor(cores[idx % len(cores)])
        doc.setLineWidth(1.2)
        doc.line(x, ly, x + 8 * mm, ly)
        doc.setFillColor(COR_PRETO)
        doc.setFont(_fonte(lang), 8)
        doc.drawString(x + 10 * mm, ly - 2 * mm, nome)
        ly -= 5 * mm
    return ly

# Moeda por idioma
MOEDA = {
    "pt": "R$", "en": "US$", "es": "€", "it": "€", "fr": "€", "de": "€",
    "ja": "¥", "zh": "¥", "ru": "₽", "he": "₪", "ar": "ر.س",
    "id": "Rp", "tr": "₺", "vi": "₫",
}

def _moeda(lang):
    return MOEDA.get(lang, "")

def _com_moeda(lang, texto):
    """Adiciona o símbolo da moeda ao valor, se ainda não tiver e se for numérico."""
    m = _moeda(lang)
    t = str(texto)
    if not m or m in t:
        return t
    # só adiciona se o valor contém dígitos (evita "Sob consulta" ganhar moeda)
    if any(ch.isdigit() for ch in t):
        return f"{m} {t}"
    return t

def _bandeira(doc, x, y, w, h, pais):
    """Desenha uma mini-bandeira (id, tr, vn)."""
    if pais == "id":
        doc.setFillColor(HexColor("#CE1126"))
        doc.rect(x, y + h / 2, w, h / 2, stroke=0, fill=1)
        doc.setFillColor(white)
        doc.rect(x, y, w, h / 2, stroke=0, fill=1)
    elif pais == "tr":
        doc.setFillColor(HexColor("#E30A17"))
        doc.rect(x, y, w, h, stroke=0, fill=1)
        doc.setFillColor(white)
        doc.circle(x + w * 0.42, y + h / 2, h * 0.30, stroke=0, fill=1)
        doc.setFillColor(HexColor("#E30A17"))
        doc.circle(x + w * 0.48, y + h / 2, h * 0.26, stroke=0, fill=1)
    elif pais == "vn":
        doc.setFillColor(HexColor("#DA251D"))
        doc.rect(x, y, w, h, stroke=0, fill=1)
        cx, cy = x + w / 2, y + h / 2
        r = h * 0.38
        pts = []
        for i in range(10):
            ang = math.pi / 2 + i * math.pi / 5
            rr = r if i % 2 == 0 else r * 0.45
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        p = doc.beginPath()
        p.moveTo(*pts[0])
        for pt in pts[1:]:
            p.lineTo(*pt)
        p.close()
        doc.setFillColor(HexColor("#FFCD00"))
        doc.drawPath(p, stroke=0, fill=1)
    doc.setStrokeColor(HexColor("#888888"))
    doc.setLineWidth(0.3)
    doc.rect(x, y, w, h, stroke=1, fill=0)

def gerar_apresentacao(lang="pt", modo="texto"):
    if modo == "slides":
        return gerar_pdf_slides(lang)
    caminho = gerar_pdf_texto(lang)
    if caminho and os.path.exists(caminho):
        return caminho
    # O gerador salvou o arquivo mas retornou None; localiza o arquivo salvo:
    candidato = os.path.join(STATIC_DIR, f"apresentacao_{lang}.pdf")
    if os.path.exists(candidato):
        return candidato
    return caminho

def _capa_slides(doc, largura, altura, lang, modo):
    """Capa dos slides — fundo preto, título central, logo."""
    c = CONTEUDO.get(lang, CONTEUDO["pt"])
    doc.setFillColor(COR_PRETO)
    doc.rect(0, 0, largura, altura, stroke=0, fill=1)
    if os.path.exists(LOGO_ESQ):
        try:
            iw, ih = ImageReader(LOGO_ESQ).getSize()
            lw = min(largura * 0.28, iw)
            lh = lw * ih / iw
            doc.drawImage(LOGO_ESQ, (largura - lw) / 2, altura * 0.52,
                  width=lw, height=lh, mask="auto")
        except Exception:
            pass
    doc.setFillColor(COR_DOURADO)
    doc.setFont(_fonte(lang, True), 34)
    doc.drawCentredString(largura / 2, altura * 0.47, c["titulo"])
    doc.setFillColor(white)
    doc.setFont(_fonte(lang), 14)
    doc.drawCentredString(largura / 2, altura * 0.41, c["subtitulo"])
    doc.setStrokeColor(COR_DOURADO)
    doc.setLineWidth(0.8)
    doc.line(largura * 0.30, altura * 0.385, largura * 0.70, altura * 0.385)
    doc.setFillColor(HexColor("#AAAAAA"))
    doc.setFont(_fonte(lang), 11)
    doc.drawCentredString(largura / 2, altura * 0.35, c["capa_nota"])
    doc.setFillColor(COR_DOURADO)
    doc.setFont(_fonte(lang, True), 12)
    doc.drawCentredString(largura / 2, altura * 0.28, "DUNS 942242668")
    doc.setFillColor(HexColor("#888888"))
    doc.setFont(_fonte(lang), 9)
    doc.drawCentredString(largura / 2, altura * 0.08,
                          f"{c['confidencial']}  {c['ano']}")

def _rodape_texto(cnv, num, total):
    c = _CTX_TEXTO["c"]
    lang = _CTX_TEXTO["lang"]
    _cabecalho_duas_logos(cnv, None, c, lang, cor_fundo=COR_AZUL)
    _rodape(cnv, None, c, lang, num_pag=num, total_pag=total)

def _rodape_deck(doc, largura, altura, lang, c, pagina):
    """Rodapé dos slides — título/DUNS à esquerda, página à direita, contatos embaixo."""
    doc.setFillColor(COR_CINZA_CLARO)
    doc.setFont(_fonte(lang), 8)
    doc.drawCentredString(largura / 2, 10 * mm,
                          f"{c['titulo']} · DUNS 942242668 · {c['confidencial']} {c['ano']}")
    doc.setFillColor(COR_DOURADO)
    doc.setFont(_fonte(lang, True), 9)
    doc.drawRightString(largura - 15 * mm, 10 * mm, f"{pagina - 1}-{TOTAL_PAGINAS - 2}")
    doc.setFillColorRGB(0.55, 0.55, 0.55)
    doc.setFont(_fonte(lang), 7)
    doc.drawCentredString(largura / 2, 4 * mm, CONTATOS)

def _texto_wrap_centrado_v(doc, texto, fonte, tam, x, y, largura, cor, entrelinha, altura):
    """Texto quebrado, centralizado horizontal e verticalmente
    dentro da área de altura 'altura'. y = TOPO da área."""
    fator, eh_cjk = _fator_script(texto)
    tam2 = tam * fator
    larg_interna = max(largura, 1)
    linhas = _quebrar_harmonizado(texto, fonte, tam2, larg_interna, eh_cjk)
    total = len(linhas) * entrelinha
    while tam2 > 5 and total > altura:
        tam2 -= 0.5
        linhas = _quebrar_harmonizado(texto, fonte, tam2, larg_interna, eh_cjk)
        total = len(linhas) * entrelinha
    doc.setFont(fonte, tam2)
    doc.setFillColor(cor)
    y_ini = y - (altura - total) / 2   # ← CORREÇÃO: centraliza de verdade
    for ln in linhas:
        doc.drawCentredString(x + larg_interna / 2, y_ini, ln)
        y_ini -= entrelinha
    return y_ini + entrelinha

def _kpis_grid(doc, largura, altura, lang, dados, y, colunas=4):
    """Desenha uma grade de cards de KPIs e retorna o novo y."""
    if not dados:
        return y
    margem = 15 * mm
    gap = 6 * mm
    larg = (largura - 2 * margem - (colunas - 1) * gap) / colunas
    alt_card = 26 * mm
    for i, kpi in enumerate(dados):
        if isinstance(kpi, dict):
            valor = str(kpi.get("valor", kpi.get("numero", "")))
            rotulo = str(kpi.get("rotulo", kpi.get("label", kpi.get("titulo", ""))))
        else:
            kpi = list(kpi) + ["", "", ""]
            valor = str(kpi[0])
            rotulo = str(kpi[1])
        col = i % colunas
        lin = i // colunas
        x = margem + col * (larg + gap)
        yy = y - lin * (alt_card + gap)
        # Fundo do card (preto)
        doc.setFillColor(COR_PRETO)
        doc.setStrokeColor(COR_DOURADO)
        doc.setLineWidth(0.6)
        doc.rect(x, yy - alt_card, larg, alt_card, stroke=1, fill=1)
        # Valor (grande, branco)
        doc.setFillColor(white)
        doc.setFont(_fonte(lang, True), 16)
        doc.drawCentredString(x + larg / 2, yy - 8 * mm, valor)
        # Rótulo (dourado claro, pequeno)
        doc.setFillColor(COR_DOURADO)
        doc.setFont(_fonte(lang), 8)
        doc.drawCentredString(x + larg / 2, yy - 16 * mm, rotulo)
    n_linhas = (len(dados) + colunas - 1) // colunas
    return y - n_linhas * (alt_card + gap)

def _texto_wrap(doc, texto, fonte, tam, x, y, largura, cor, entrelinha, y_min=None):
    """Quebra, ENCOLHE a fonte até caber na largura e na altura, e desenha.
    y = topo. Se y_min for dado, o texto nunca passa dele."""
    fator, eh_cjk = _fator_script(texto)
    tam2 = tam * fator
    larg_interna = max(largura, 1)
    linhas = _quebrar_harmonizado(texto, fonte, tam2, larg_interna, eh_cjk)
    if y_min is not None:
        disp = max(y - y_min, 1)
        while tam2 > 5 and len(linhas) * entrelinha > disp:
            tam2 -= 0.5
            linhas = _quebrar_harmonizado(texto, fonte, tam2, larg_interna, eh_cjk)
    doc.setFont(fonte, tam2)
    doc.setFillColor(cor)
    yy = y
    for ln in linhas:
        if y_min is not None and yy - entrelinha < y_min - 0.1:
            break
        doc.drawString(x, yy, ln)
        yy -= entrelinha
    return yy

def _caixa(doc, x, y, w, h, cor_fundo, cor_borda):
    """Desenha uma caixa retangular com fundo e borda."""
    doc.setFillColor(cor_fundo)
    doc.setStrokeColor(cor_borda)
    doc.setLineWidth(0.8)
    doc.rect(x, y, w, h, stroke=1, fill=1)

def gerar_pdf_slides(lang):
    c = APRESENTACAO_TEXTOS.get(lang, APRESENTACAO_TEXTOS["pt"])
    largura, altura = landscape(A4)
    caminho_saida = os.path.join(STATIC_DIR, f"apresentacao_slides_{lang}.pdf")
    doc = canvas.Canvas(caminho_saida, pagesize=landscape(A4))

    # ===== CLOSURES (usam doc, largura, altura, lang, c) =====
    def cab(titulo, nivel=1):
        """Título de seção do slide."""
        doc.setFillColor(COR_AZUL)
        doc.setFont(_fonte(lang, True), 20 if nivel == 1 else 16)
        doc.drawString(18*mm, altura - 24*mm, titulo)
        doc.setStrokeColor(COR_DOURADO)
        doc.setLineWidth(0.8)
        doc.line(18*mm, altura - 28*mm, largura - 18*mm, altura - 28*mm)

    def rodape(pagina):
        """Apenas desenha o rodapé do slide (sem recursão)."""
        _cabecalho_duas_logos(doc, None, c, lang, cor_fundo=COR_AZUL)
        doc.setFillColor(COR_CINZA_CLARO)
        doc.setFont(_fonte(lang), 8)
        doc.drawCentredString(largura / 2, 10 * mm,
                              f"{c['titulo']} · DUNS 942242668 · {c['confidencial']} {c['ano']}")
        doc.setFillColor(COR_DOURADO)
        doc.setFont(_fonte(lang, True), 9)
        doc.drawRightString(largura - 15 * mm, 10 * mm, f"{pagina} de {TOTAL_PAGINAS}")
        doc.setFillColorRGB(0.55, 0.55, 0.55)
        doc.setFont(_fonte(lang), 7)
        doc.drawCentredString(largura / 2, 4 * mm, CONTATOS)

    # ===== FUNÇÕES DE SLIDE (v2 — visual premium dourado/preto) =====
    def _capa_slides_v2():
        """SLIDE 1 — CAPA (visual premium)."""
        doc.setFillColor(COR_PRETO)
        doc.rect(0, 0, largura, altura, fill=1, stroke=0)
        doc.setStrokeColor(COR_DOURADO)
        doc.setLineWidth(1.2)
        doc.line(0, altura - 6 * mm, largura, altura - 6 * mm)
        doc.setFillColor(COR_DOURADO)
        doc.setFont(_fonte(lang, True), 30)
        doc.drawCentredString(largura / 2, altura - 45 * mm, c["titulo"])
        doc.setFillColor(HexColor("#E8E8E8"))
        doc.setFont(_fonte(lang), 14)
        doc.drawCentredString(largura / 2, altura - 55 * mm, c["subtitulo"])
        doc.setFillColor(COR_DOURADO)
        doc.setFont(_fonte(lang, True), 11)
        doc.drawCentredString(largura / 2, altura - 63 * mm, c["capa_nota"])
        doc.setFillColor(HexColor("#B71C1C"))
        doc.setFont(_fonte(lang, True), 9)
        doc.drawCentredString(largura / 2, altura - 72 * mm,
                              f"{c['confidencial']} · {c['ano']}")
        doc.setStrokeColor(COR_DOURADO)
        doc.setLineWidth(1.2)
        doc.line(0, 16 * mm, largura, 16 * mm)

    def _slide_sumario_v2(pagina):
        """SLIDE 2 — SUMÁRIO EXECUTIVO (cards 4x2)."""
        cab(c.get("sumario_titulo", "Sumário Executivo"), 1)
        y = altura - 32 * mm
        y = _texto_wrap(doc, c["sumario_intro"], _fonte(lang), 12, 18 * mm, y,
        largura - 36 * mm, COR_CINZA, 6 * mm)
        y -= 8 * mm
        cards = c["sumario_cards"]
        margem = 18 * mm
        gap = 8 * mm
        n_col = 4
        w = (largura - 2 * margem - (n_col - 1) * gap) / n_col
        h = 38 * mm
        for i, (num, tit, sub) in enumerate(cards):
            col = i % n_col
            lin = i // n_col
            x = margem + col * (w + gap)
            yy = y - lin * (h + 8 * mm)
            _caixa(doc, x, yy - h, w, h, COR_FUNDO, COR_DOURADO)
            doc.setFillColor(COR_DOURADO)
            doc.setFont(_fonte(lang, True), 16)
            doc.drawString(x + 6 * mm, yy - h + 22 * mm, num)
            doc.setFillColor(COR_PRETO)
            _texto_wrap(doc, tit, _fonte(lang, True), 10, x + 6 * mm, yy - h + 14 * mm,
                        w - 12 * mm, COR_PRETO, 4.5 * mm, y_min=yy - h + 6 * mm)
            doc.setFillColor(COR_CINZA)
            _texto_wrap(doc, sub, _fonte(lang), 8, x + 6 * mm, yy - h + 5 * mm,
                        w - 12 * mm, COR_CINZA, 3.8 * mm, y_min=yy - h + 1 * mm)
        rodape(pagina)
        doc.showPage()

    def _slide_sobre_v2(pagina):
        """SLIDE 3 — SOBRE A A1ELOS (KPIs + DUNS)."""
        cab(c["sobre_titulo"], 2)
        y = altura - 32 * mm
        y = _texto_wrap(doc, c["sobre_texto"], _fonte(lang), 12, 18 * mm, y,
                        largura - 36 * mm, COR_PRETO, 6 * mm)
        y -= 8 * mm
        y = _kpis_grid(doc, largura, altura, lang, c["sobre_kpis"], y, 4)
        y -= 6 * mm
        _caixa(doc, 18 * mm, y - 16 * mm, largura - 36 * mm, 16 * mm, HexColor("#EEF2FA"), COR_AZUL)
        doc.setFillColor(COR_AZUL)
        doc.setFont(_fonte(lang, True), 9)
        _texto_wrap(doc, c["sobre_duns"], _fonte(lang, True), 9, 22 * mm, y - 11 * mm,
                    largura - 44 * mm, COR_AZUL, 4 * mm)
        rodape(pagina)
        doc.showPage()

    def _slide_b2b_v2(pagina):
        """SLIDE 14 — PACOTES B2B + TABELA DE DESCONTOS (8 faixas, NOVA)."""
        cab(c["b2b_titulo"], 3)
        y = altura - 32 * mm
        y = _texto_wrap(doc, c["b2b_texto"], _fonte(lang), 11, 18 * mm, y,
                        largura - 36 * mm, COR_PRETO, 5.5 * mm)
        y -= 6 * mm
        planos = c["b2b_planos"]
        margem = 18 * mm
        gap = 8 * mm
        w = (largura - 2 * margem - 2 * gap) / 3
        h = 30 * mm
        for i, (tit, desc) in enumerate(planos):
            x = margem + i * (w + gap)
            _caixa(doc, x, y - h, w, h, COR_FUNDO, COR_DOURADO)
            doc.setFillColor(COR_DOURADO)
            doc.setFont(_fonte(lang, True), 9)
            _texto_wrap(doc, tit, _fonte(lang, True), 9, x + 5 * mm, y - 6 * mm,
                        w - 10 * mm, COR_DOURADO, 4 * mm)
            doc.setFillColor(COR_CINZA)
            _texto_wrap(doc, desc, _fonte(lang), 8, x + 5 * mm, y - 14 * mm,
                        w - 10 * mm, COR_CINZA, 3.8 * mm, y_min=y - h + 3 * mm)
        y -= h + 6 * mm
        doc.setFillColor(COR_DOURADO)
        doc.setFont(_fonte(lang, True), 11)
        doc.drawString(18 * mm, y, c["tabela_descontos"])
        y -= 6 * mm
        tabela = c["b2b_tabela"]
        col_w = [(largura - 36 * mm) * 0.25, (largura - 36 * mm) * 0.15,
                 (largura - 36 * mm) * 0.30, (largura - 36 * mm) * 0.30]
        linha_h = 8 * mm
        x0 = 18 * mm
        for j, titulo in enumerate(tabela[0]):
            _caixa(doc, x0 + sum(col_w[:j]), y - linha_h, col_w[j], linha_h,
                   HexColor("#1A1A1A"), COR_DOURADO)
            doc.setFillColor(COR_DOURADO)
            doc.setFont(_fonte(lang, True), 8)
            doc.drawString(x0 + sum(col_w[:j]) + 2 * mm, y - linha_h + 2.5 * mm, titulo)
        y -= linha_h
        for i, linha in enumerate(tabela[1:]):
            cor_fundo = HexColor("#FAFAFA") if i % 2 == 0 else HexColor("#F0F0F0")
            for j, val in enumerate(linha):
                _caixa(doc, x0 + sum(col_w[:j]), y - linha_h, col_w[j], linha_h,
                       cor_fundo, HexColor("#CCCCCC"))
                doc.setFillColor(COR_PRETO)
                doc.setFont(_fonte(lang, True) if j == 1 else _fonte(lang), 7.5)
                doc.drawString(x0 + sum(col_w[:j]) + 2 * mm, y - linha_h + 2.5 * mm, val)
            y -= linha_h
        rodape(pagina)
        doc.showPage()

    def _slide_projecoes_v2(pagina):
        """SLIDE 15 — PROJEÇÕES (1ª década em 1/3/5/7/10, NOVA)."""
        cab(c["projecoes_titulo"], 4)
        y = altura - 32 * mm
        y = _texto_wrap(doc, c["projecoes_texto"], _fonte(lang), 11, 18 * mm, y,
                        largura - 36 * mm, COR_PRETO, 5.5 * mm)
        y -= 6 * mm
        tabela = c["projecoes_tabela"]
        col_w = [(largura - 36 * mm) * 0.30, (largura - 36 * mm) * 0.35,
                 (largura - 36 * mm) * 0.35]
        linha_h = 9 * mm
        x0 = 18 * mm
        for j, titulo in enumerate(tabela[0]):
            _caixa(doc, x0 + sum(col_w[:j]), y - linha_h, col_w[j], linha_h,
                   HexColor("#1A1A1A"), COR_DOURADO)
            doc.setFillColor(COR_DOURADO)
            doc.setFont(_fonte(lang, True), 9)
            doc.drawString(x0 + sum(col_w[:j]) + 3 * mm, y - linha_h + 3 * mm, titulo)
        y -= linha_h
        anos_destaque = [str(a) for a in [1, 3, 5, 7, 10]]
        for i, linha in enumerate(tabela[1:]):
            cor_fundo = HexColor("#FAFAFA") if i % 2 == 0 else HexColor("#F0F0F0")
            if any(ano in linha[0] for ano in anos_destaque):
                cor_fundo = HexColor("#FFF8E1")
            for j, val in enumerate(linha):
                _caixa(doc, x0 + sum(col_w[:j]), y - linha_h, col_w[j], linha_h,
                       cor_fundo, HexColor("#CCCCCC"))
                doc.setFillColor(COR_PRETO)
                doc.setFont(_fonte(lang, True) if j == 0 else _fonte(lang), 8)
                doc.drawString(x0 + sum(col_w[:j]) + 3 * mm, y - linha_h + 3 * mm, val)
            y -= linha_h
        rodape(pagina)
        doc.showPage()

    # ===== GERAÇÃO DOS SLIDES =====
    pagina = 1

    # SLIDE 1 — CAPA
    _capa_slides_v2()
    rodape(pagina)
    doc.showPage()
    pagina += 1

    # SLIDE 2 — SUMÁRIO EXECUTIVO
    _slide_sumario_v2(pagina)
    pagina += 1

    # SLIDE 3 — SOBRE A A1ELOS
    _slide_sobre_v2(pagina)
    pagina += 1

    # SLIDE 4 — CREDIBILIDADE INTERNACIONAL
    cab(c["duns_titulo"], 3)
    y = altura - 32 * mm
    col_w = (largura - 36 * mm - 10 * mm) / 2
    _caixa(doc, 18 * mm, y - 85 * mm, col_w, 85 * mm, COR_PRETO, COR_DOURADO)
    doc.setFillColor(COR_DOURADO)
    doc.setFont(_fonte(lang, True), 34)
    doc.drawCentredString(18 * mm + col_w / 2, y - 30 * mm, c["duns_numero"])
    doc.setFillColor(white)
    doc.setFont(_fonte(lang), 10)
    _texto_wrap(doc, c["duns_emitido"], _fonte(lang), 10, 24 * mm, y - 50 * mm,
                col_w - 12 * mm, white, 4.5 * mm)
    doc.setFillColor(COR_DOURADO)
    doc.setFont(_fonte(lang, True), 16)
    doc.drawCentredString(18 * mm + col_w / 2, y - 72 * mm, c["duns_paises"])
    xr = 18 * mm + col_w + 10 * mm
    doc.setFillColor(COR_PRETO)
    doc.setFont(_fonte(lang, True), 13)
    doc.drawString(xr, y - 8 * mm, c.get("duns_porque", "Por que o DUNS importa?"))
    yy = y - 16 * mm
    yy = _texto_wrap(doc, c["duns_texto"], _fonte(lang), 10, xr, yy,
                     col_w, COR_CINZA, 4.5 * mm)
    yy -= 8 * mm
    for tit, sub in c["duns_beneficios"]:
        _caixa(doc, xr, yy - 24 * mm, col_w, 24 * mm, COR_FUNDO, COR_DOURADO)
        doc.setFillColor(COR_AZUL)
        doc.setFont(_fonte(lang, True), 10)
        doc.drawString(xr + 5 * mm, yy - 17 * mm, tit)
        doc.setFillColor(COR_CINZA)
        doc.setFont(_fonte(lang), 8)
        _texto_wrap(doc, sub, _fonte(lang), 8, xr + 5 * mm, yy - 12 * mm,
                    col_w - 10 * mm, COR_CINZA, 3.5 * mm)
        yy -= 28 * mm
    rodape(pagina)
    doc.showPage()
    pagina += 1

    # SLIDE 5 — OPORTUNIDADE DE MERCADO
    cab(c["mercado_titulo"], 4)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["mercado_texto"], _fonte(lang), 12, 18 * mm, y,
                    largura - 36 * mm, COR_PRETO, 6 * mm)
    y -= 10 * mm
    cards = c["mercado_cards"]
    n_col = 4
    margem = 18 * mm
    gap = 8 * mm
    w = (largura - 2 * margem - (n_col - 1) * gap) / n_col
    h = 40 * mm
    for i, (tit, sub) in enumerate(cards):
        x = margem + i * (w + gap)
        _caixa(doc, x, y - h, w, h, COR_FUNDO, COR_DOURADO)
        doc.setFillColor(COR_AZUL)
        doc.setFont(_fonte(lang, True), 10)
        _texto_wrap(doc, tit, _fonte(lang, True), 10, x + 4 * mm, y - 12 * mm,
                    w - 8 * mm, COR_AZUL, 4.5 * mm, y_min=y - 20 * mm)
        doc.setFillColor(COR_PRETO)
        doc.setFont(_fonte(lang), 8.5)
        _texto_wrap(doc, sub, _fonte(lang), 8.5, x + 4 * mm, y - 22 * mm,
                    w - 8 * mm, COR_PRETO, 4 * mm, y_min=y - h + 4 * mm)
    rodape(pagina)
    doc.showPage()
    pagina += 1

    # SLIDE 6 — O PROBLEMA
    cab(c["problema_titulo"], 5)
    y = altura - 32 * mm
    col_w = (largura - 36 * mm - 10 * mm) / 2
    doc.setFillColor(COR_PRETO)
    doc.setFont(_fonte(lang, True), 13)
    doc.drawString(18 * mm, y - 8 * mm, c["problema_col_esq_titulo"])
    yy = y - 16 * mm
    for tit, sub in c["problema_col_esq"]:
        _caixa(doc, 18 * mm, yy - 34 * mm, col_w, 34 * mm, COR_FUNDO, COR_DOURADO)
        doc.setFillColor(COR_AZUL)
        _texto_wrap(doc, tit, _fonte(lang, True), 9.5, 18 * mm + 4 * mm, yy - 6 * mm,
                    col_w - 8 * mm, COR_AZUL, 4.5 * mm, y_min=yy - 16 * mm)
        doc.setFillColor(COR_CINZA)
        _texto_wrap_centrado_v(doc, sub, _fonte(lang), 8,
                               18 * mm, yy - 18 * mm, col_w,
                               COR_CINZA, 3.8 * mm, 15 * mm)
        yy -= 37 * mm
    xr = 18 * mm + col_w + 10 * mm
    doc.setFillColor(COR_PRETO)
    doc.setFont(_fonte(lang, True), 13)
    doc.drawString(xr, y - 8 * mm, c["problema_col_dir_titulo"])
    _texto_wrap_centrado_v(doc, c["problema_col_dir"], _fonte(lang), 9.5,
                           xr, y - 16 * mm, col_w, COR_CINZA, 4.5 * mm, 52 * mm)
    yy = y - 78 * mm
    _caixa(doc, xr, yy - 40 * mm, col_w, 40 * mm, HexColor("#FFF3E0"), COR_DOURADO)
    doc.setFillColor(COR_PRETO)
    _texto_wrap_centrado_v(doc, c["problema_destaque"], _fonte(lang, True), 10,
                           xr, yy, col_w, COR_PRETO, 4.5 * mm, 40 * mm)
    rodape(pagina)
    doc.showPage()
    pagina += 1

    # SLIDE 7 — SOLUÇÃO
    cab(c["solucao_titulo"], 6)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["solucao_texto"], _fonte(lang), 12, 18 * mm, y,
                    largura - 36 * mm, COR_PRETO, 6 * mm)
    y -= 10 * mm
    col_w = (largura - 36 * mm - 2 * 10 * mm) / 3
    for i, (tit, sub) in enumerate(c["solucao_colunas"]):
        x = 18 * mm + i * (col_w + 10 * mm)
        _caixa(doc, x, y - 90 * mm, col_w, 90 * mm, COR_FUNDO, COR_DOURADO)
        doc.setFillColor(COR_AZUL)
        doc.setFont(_fonte(lang, True), 12)
        _texto_wrap(doc, tit, _fonte(lang, True), 12, x + 6 * mm, y - 16 * mm,
                    col_w - 12 * mm, COR_AZUL, 5.5 * mm)
        doc.setFillColor(COR_CINZA)
        doc.setFont(_fonte(lang), 9)
        _texto_wrap(doc, sub, _fonte(lang), 9, x + 6 * mm, y - 28 * mm,
                    col_w - 12 * mm, COR_CINZA, 4.5 * mm)
    rodape(pagina)
    doc.showPage()
    pagina += 1

    # SLIDE 8 — ALCANCE GLOBAL + TABELA IDIOMAS
    cab(c["alcance_titulo"], 7)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["alcance_texto"], _fonte(lang), 12, 18 * mm, y,
                    largura - 36 * mm, COR_CINZA, 6 * mm)
    y -= 10 * mm
    linhas = c.get("linhas_idiomas", LINHAS_IDIOMAS)
    dados = [[c.get("idioma_col", "Idioma"), c.get("falantes_col", "Falantes (mi)")]] \
        + linhas + [[c.get("total_linha", "TOTAL"), "~5.320"]]
    _tabela_editorial(doc, 18 * mm, y, largura - 36 * mm, dados, [0.6, 0.4], _tam_ajus(lang, 9), lang)
    rodape(pagina)
    doc.showPage()
    pagina += 1

    # SLIDE 9 — 3 NOVOS MERCADOS
    cab(c["mercados_titulo"], 8)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["mercados_texto"], _fonte(lang), 11, 18 * mm, y,
                    largura - 36 * mm, COR_CINZA, 5.5 * mm)
    y -= 10 * mm
    col_w = (largura - 36 * mm - 2 * 8 * mm) / 3
    paises = ["id", "tr", "vn"]
    for i, (tit, itens) in enumerate(c["mercados_cards"]):
        x = 18 * mm + i * (col_w + 8 * mm)
        _caixa(doc, x, y - 70 * mm, col_w, 70 * mm, COR_FUNDO, COR_DOURADO)
        _bandeira(doc, x + 5 * mm, y - 22 * mm, 11 * mm, 7.5 * mm, paises[i])
        doc.setFillColor(COR_AZUL)
        doc.setFont(_fonte(lang, True), 12)
        doc.drawString(x + 20 * mm, y - 14 * mm, tit)
        yy = y - 26 * mm
        for item in itens:
            doc.setFillColor(COR_CINZA)
            doc.setFont(_fonte(lang), 9)
            yy = _texto_wrap(doc, "•  " + item, _fonte(lang), 9, x + 5 * mm, yy,
                             col_w - 10 * mm, COR_CINZA, 4.5 * mm, y_min=y - 66 * mm)
    y -= 78 * mm
    _caixa(doc, 18 * mm, y - 18 * mm, largura - 36 * mm, 18 * mm, HexColor("#EEF2FA"), COR_AZUL)
    doc.setFillColor(COR_AZUL)
    doc.setFont(_fonte(lang, True), 9)
    _texto_wrap(doc, c["mercados_rodape"], _fonte(lang, True), 9, 22 * mm, y - 12 * mm,
                largura - 44 * mm, COR_AZUL, 4 * mm)
    rodape(pagina)
    doc.showPage()
    pagina += 1

    # SLIDE 10 — FILOSOFIA DE PREÇO
    cab(c["preco_titulo"], 9)
    y = altura - 32 * mm
    col_w = (largura - 36 * mm - 10 * mm) / 2
    _caixa(doc, 18 * mm, y - 60 * mm, col_w, 60 * mm, COR_PRETO, COR_DOURADO)
    doc.setFillColor(COR_DOURADO)
    doc.setFont(_fonte(lang, True), 13)
    doc.drawString(22 * mm, y - 16 * mm, c.get("preco_consciente", "Preço Consciente"))
    doc.setFillColor(white)
    _texto_wrap_centrado_v(doc, c["preco_esq"], _fonte(lang), 10, 22 * mm, y - 24 * mm,
                           col_w - 8 * mm, white, 4.5 * mm, 34 * mm)
    xr = 18 * mm + col_w + 10 * mm
    doc.setFillColor(COR_PRETO)
    doc.setFont(_fonte(lang, True), 13)
    doc.drawString(xr, y - 8 * mm, c["preco_dir_titulo"])
    _texto_wrap_centrado_v(doc, c["preco_dir"], _fonte(lang), 10, xr, y - 16 * mm,
                           col_w, COR_CINZA, 4.5 * mm, 42 * mm)
    yy = y - 66 * mm
    for tit, sub in c["preco_pilares"]:
        _caixa(doc, xr, yy - 26 * mm, col_w, 26 * mm, COR_FUNDO, COR_DOURADO)
        doc.setFillColor(COR_AZUL)
        _texto_wrap(doc, tit, _fonte(lang, True), 10, xr + 5 * mm, yy - 6 * mm,
                    col_w - 10 * mm, COR_AZUL, 4.2 * mm, y_min=yy - 14 * mm)
        doc.setFillColor(COR_CINZA)
        _texto_wrap(doc, sub, _fonte(lang), 8, xr + 5 * mm, yy - 16 * mm,
                    col_w - 10 * mm, COR_CINZA, 3.5 * mm, y_min=yy - 24 * mm)
        yy -= 30 * mm
    rodape(pagina)
    doc.showPage()
    pagina += 1

    # SLIDE 11 — PORTFÓLIO
    cab(c["portfolio_titulo"], 10)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["portfolio_texto"], _fonte(lang), 12, 18 * mm, y,
                    largura - 36 * mm, COR_CINZA, 6 * mm)
    y -= 10 * mm
    y = _tabela_editorial(doc, 18 * mm, y, largura - 36 * mm,
                          c["portfolio_tabela"], [0.22, 0.38, 0.18, 0.22], _tam_ajus(lang, 9), lang,
                          moeda_cols=(2,))
    y -= 8 * mm
    doc.setFillColor(COR_CINZA)
    doc.setFont(_fonte(lang), 9)
    _texto_wrap(doc, c["portfolio_rodape"], _fonte(lang), 9, 18 * mm, y,
                largura - 36 * mm, COR_CINZA, 4 * mm)
    rodape(pagina)
    doc.showPage()
    pagina += 1

    # SLIDE 12 — MODELO DE NEGÓCIO
    cab(c["negocio_titulo"], 11)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["negocio_texto"], _fonte(lang), 12, 18 * mm, y,
                    largura - 36 * mm, COR_CINZA, 6 * mm)
    y -= 8 * mm
    col_w = (largura - 36 * mm - 2 * 10 * mm) / 3
    for i, (tit, sub) in enumerate(c["negocio_colunas"]):
        x = 18 * mm + i * (col_w + 10 * mm)
        _caixa(doc, x, y - 45 * mm, col_w, 45 * mm, COR_FUNDO, COR_DOURADO)
        doc.setFillColor(COR_AZUL)
        doc.setFont(_fonte(lang, True), 11)
        _texto_wrap(doc, tit, _fonte(lang, True), 11, x + 6 * mm, y - 12 * mm,
                    col_w - 12 * mm, COR_AZUL, 5 * mm)
        doc.setFillColor(COR_CINZA)
        doc.setFont(_fonte(lang), 9)
        _texto_wrap(doc, sub, _fonte(lang), 9, x + 6 * mm, y - 20 * mm,
                    col_w - 12 * mm, COR_CINZA, 4.5 * mm)
    y -= 50 * mm
    _tabela_editorial(doc, 18 * mm, y - 60 * mm, largura - 36 * mm,
                  [[c.get("fonte_receita", "Fonte de Receita"), c.get("participacao", "Participação")],
                   [c.get("b2c_linha", "B2C — 14 Idiomas"), "60%"],
                   [c.get("b2b_linha", "B2B — Descontos Progressivos"), "25%"],
                   [c.get("pub_linha", "Publicidade Geolocalizada"), "15%"]],
                  [0.7, 0.3], _tam_ajus(lang, 10), lang)
    rodape(pagina)
    doc.showPage()
    pagina += 1

    # SLIDE 13 — BANNERS
    cab(c["banners_titulo"], 12)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["banners_texto"], _fonte(lang), 11, 18 * mm, y,
                    largura - 36 * mm, COR_CINZA, 5.5 * mm)
    y -= 10 * mm
    y = _tabela_editorial(doc, 18 * mm, y, largura - 36 * mm,
                    c["banners_tabela"], [0.22, 0.22, 0.22, 0.34], _tam_ajus(lang, 9), lang,
                    moeda_cols=(1, 2))
    y -= 30 * mm
    _caixa(doc, 18 * mm, y - 24 * mm, largura - 36 * mm, 24 * mm, HexColor("#EEF2FA"), COR_AZUL)
    doc.setFillColor(COR_AZUL)
    doc.setFont(_fonte(lang), 9)
    _texto_wrap(doc, c["banners_formatos"], _fonte(lang), 9, 22 * mm, y - 15 * mm,
                largura - 44 * mm, COR_AZUL, 4 * mm)
    rodape(pagina)
    doc.showPage()
    pagina += 1

    # SLIDE 14 — PACOTES B2B + DESCONTOS (NOVA)
    _slide_b2b_v2(pagina)
    pagina += 1

    # SLIDE 15 — PROJEÇÕES (NOVA)
    _slide_projecoes_v2(pagina)
    pagina += 1

    # SLIDE 16 — TRAÇÃO E RESULTADOS
    cab(c["tracao_titulo"], 15)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["tracao_texto"], _fonte(lang), 12, 18 * mm, y,
                    largura - 36 * mm, COR_CINZA, 6 * mm)
    y -= 12 * mm
    _kpis_grid(doc, largura, altura, lang, c["tracao_kpis"], y, 4)
    rodape(pagina)
    doc.showPage()
    pagina += 1

    # SLIDE 17 — ROTEIRO ESTRATÉGICO
    cab(c["roteiro_titulo"], 16)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["roteiro_texto"], _fonte(lang), 12, 18 * mm, y,
                    largura - 36 * mm, COR_CINZA, 6 * mm)
    y -= 10 * mm
    col_w = (largura - 36 * mm - 10 * mm) / 2
    for i, (tit, sub) in enumerate(c["roteiro_fases"]):
        col = i % 2
        lin = i // 2
        x = 18 * mm + col * (col_w + 10 * mm)
        yy = y - lin * (52 * mm + 8 * mm)
        _caixa(doc, x, yy - 52 * mm, col_w, 52 * mm, COR_FUNDO, COR_DOURADO)
        doc.setFillColor(COR_AZUL)
        doc.setFont(_fonte(lang, True), 12)
        doc.drawString(x + 6 * mm, yy - 16 * mm, tit)
        doc.setFillColor(COR_CINZA)
        doc.setFont(_fonte(lang), 9)
        _texto_wrap(doc, sub, _fonte(lang), 9, x + 6 * mm, yy - 26 * mm,
                    col_w - 12 * mm, COR_CINZA, 4.5 * mm)
    rodape(pagina)
    doc.showPage()
    pagina += 1

    # SLIDE 18 — INVESTIMENTO E CONTATO
    cab(c["invest_titulo"], 17)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["invest_texto"], _fonte(lang), 12, 18 * mm, y,
                    largura - 36 * mm, COR_CINZA, 6 * mm)
    y -= 10 * mm
    col_w = (largura - 36 * mm - 10 * mm) / 2
    _caixa(doc, 18 * mm, y - 75 * mm, col_w, 75 * mm, COR_PRETO, COR_DOURADO)
    yy = y - 18 * mm
    for tit, val in c["invest_dados"]:
        doc.setFillColor(COR_DOURADO)
        doc.setFont(_fonte(lang, True), 11)
        doc.drawString(22 * mm, yy, tit)
        doc.setFillColor(white)
        doc.setFont(_fonte(lang, True), 16)
        doc.drawString(22 * mm, yy - 9 * mm, val)
        yy -= 22 * mm
    xr = 18 * mm + col_w + 10 * mm
    doc.setFillColor(COR_PRETO)
    doc.setFont(_fonte(lang, True), 13)
    doc.drawString(xr, y - 8 * mm, c.get("fale_conosco", "Fale Conosco"))
    yy = y - 18 * mm
    for tit, val in c["invest_contato"]:
        doc.setFillColor(COR_AZUL)
        doc.setFont(_fonte(lang, True), 11)
        doc.drawString(xr, yy, tit)
        doc.setFillColor(COR_CINZA)
        doc.setFont(_fonte(lang), 11)
        doc.drawString(xr, yy - 7 * mm, val)
        yy -= 17 * mm
    y -= 88 * mm
    _caixa(doc, 18 * mm, y - 18 * mm, largura - 36 * mm, 18 * mm, HexColor("#EEF2FA"), COR_AZUL)
    doc.setFillColor(COR_AZUL)
    doc.setFont(_fonte(lang, True), 10)
    doc.drawCentredString(largura / 2, y - 12 * mm, c["invest_alocacao"])
    rodape(pagina)
    doc.showPage()
    pagina += 1

    # SLIDE 19A — PIX
    cab(c.get("pix_titulo", "Brasil: A Infraestrutura Pix"), 18)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c.get("pix_texto",
        "O Pix é a infraestrutura pública de pagamentos instantâneos do Brasil. Para a A1ELOS, "
        "ele garante cobrança imediata, baixo custo e aceitação universal — o alicerce da operação "
        "B2C no mercado brasileiro e a porta de entrada para a expansão internacional."),
        _fonte(lang), 12, 18 * mm, y, largura - 36 * mm, COR_CINZA, 6 * mm)
    y -= 10 * mm
    _kpis_grid(doc, largura, altura, lang, c.get("pix_kpis", [
        ("30,1 bi", "Transações em 2025", "+20% vs 2024 · Febraban"),
        ("76,4%", "da população usa Pix", "211 milhões de brasileiros · Banco Central"),
        ("R$ 68,2 tri", "movimentados no 2º sem. 2025", "78,4 bi de transações · Banco Central"),
        ("~80 bi", "transações em 2025", "+25,7% vs ano anterior · Relatório do Pix"),
    ]), y, 4)
    _caixa(doc, 18 * mm, 16 * mm, largura - 36 * mm, 14 * mm,
           HexColor("#EEF2FA"), COR_AZUL)
    doc.setFillColor(COR_AZUL)
    doc.setFont(_fonte(lang, True), 8)
    _texto_wrap(doc, c.get("pix_fonte",
        "Fontes: Banco Central do Brasil (Pix em Números) e Febraban (Pesquisa de Tecnologia Bancária)."),
        _fonte(lang, True), 8, 22 * mm, 21 * mm,
        largura - 44 * mm, COR_AZUL, 3.5 * mm)
    rodape(pagina)
    doc.showPage()
    pagina += 1

    # SLIDE 19B — REFERÊNCIAS
    cab(c.get("ref_titulo", "Referências Bibliográficas"), 19)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c.get("ref_intro",
        "Fontes utilizadas para os dados de mercado, projeções e indicadores desta apresentação."),
        _fonte(lang), 12, 18 * mm, y, largura - 36 * mm, COR_CINZA, 6 * mm)
    y -= 10 * mm
    refs = c.get("ref_lista", [
        ("Global Wellness Institute", "Economia global do bem-estar: US$ 6,8 tri (2024) → US$ 9,8 tri (2029)."),
        ("MarkNtel Advisors", "Apps de astrologia e numerologia: US$ 3 bi → US$ 9 bi até 2030 (CAGR ~20%)."),
        ("FMI · Banco Mundial", "PIB e paridade do poder de compra (PPP) por país."),
        ("Banco Central do Brasil", "Estatísticas oficiais do Pix: transações, volume e usuários."),
        ("Febraban", "Pesquisa de Tecnologia Bancária — crescimento do Pix em 2025."),
        ("IBGE", "População e indicadores socioeconômicos do Brasil."),
    ])
    col_w = (largura - 36 * mm - 8 * mm) / 2
    for i, (tit, sub) in enumerate(refs):
        col = i % 2
        lin = i // 2
        x = 18 * mm + col * (col_w + 8 * mm)
        yy = y - lin * (40 * mm + 6 * mm)
        _caixa(doc, x, yy - 36 * mm, col_w, 36 * mm, COR_FUNDO, COR_DOURADO)
        doc.setFillColor(COR_AZUL)
        doc.setFont(_fonte(lang, True), 10)
        _texto_wrap(doc, tit, _fonte(lang, True), 10, x + 5 * mm, yy - 12 * mm,
                    col_w - 10 * mm, COR_AZUL, 4.5 * mm)
        doc.setFillColor(COR_CINZA)
        doc.setFont(_fonte(lang), 8.5)
        _texto_wrap(doc, sub, _fonte(lang), 8.5, x + 5 * mm, yy - 20 * mm,
                    col_w - 10 * mm, COR_CINZA, 4 * mm, y_min=yy - 33 * mm)
    rodape(pagina)
    doc.showPage()
    pagina += 1

    # SLIDE 19 — PÁGINA FINAL
    doc.setFillColor(COR_PRETO)
    doc.rect(0, 0, largura, altura, stroke=0, fill=1)
    doc.setFillColor(COR_DOURADO)
    doc.setFont(_fonte(lang, True), 24)
    doc.drawCentredString(largura / 2, altura * 0.60, c["frase_final"])
    selo = c["selo_final"]
    margem = 18 * mm
    gap = 8 * mm
    n = len(selo)
    w = (largura - 2 * margem - (n - 1) * gap) / n
    for i, item in enumerate(selo):
        x = margem + i * (w + gap)
        doc.setStrokeColor(COR_DOURADO)
        doc.setLineWidth(0.8)
        doc.rect(x, altura * 0.40, w, 22 * mm, stroke=1, fill=0)
        doc.setFillColor(COR_DOURADO)
        doc.setFont(_fonte(lang, True), 11)
        doc.drawCentredString(x + w / 2, altura * 0.40 + 11 * mm, item)
    rodape(pagina)
    doc.showPage()

    doc.save()
    return caminho_saida

# ============================================================
# PATCH DE HARMONIZAÇÃO — texto cabe em qualquer idioma (JA/ZH/RU/HE/AR)
# Versões NOVAS de _texto_wrap e _texto_wrap_centrado_v
# ============================================================

def _fator_script(texto):
    """Devolve (fator, eh_cjk) conforme o alfabeto do texto."""
    t = str(texto)
    if any(0x2E80 <= ord(c) <= 0x9FFF or 0x3040 <= ord(c) <= 0x30FF
           or 0xAC00 <= ord(c) <= 0xD7AF for c in t):
        return 0.90, True             # japonês/chines: encolhe + quebra por caractere
    if any(0x0400 <= ord(c) <= 0x04FF for c in t):
        return 0.96, False           # russo/cirilico: encolhe levemente
    if any(0x0590 <= ord(c) <= 0x05FF or 0x0600 <= ord(c) <= 0x06FF for c in t):
        return 0.92, False           # hebraico/arabe: encolhe levemente
    return 1.0, False                # latino e demais: sem mudanca

def _quebrar_harmonizado(texto, fonte, tam, largura, eh_cjk):
    """Quebra o texto em linhas que cabem na largura.
    CJK: quebra por caractere. Demais: por palavra (com quebra de palavra longa)."""
    from reportlab.pdfbase.pdfmetrics import stringWidth
    t = str(texto)
    if not t:
        return [""]
    linhas = []
    if eh_cjk:
        atual = ""
        for ch in t:
            if stringWidth(atual + ch, fonte, tam) <= largura:
                atual += ch
            else:
                if atual:
                    linhas.append(atual)
                atual = ch
        if atual:
            linhas.append(atual)
        return linhas
    palavras = t.split()
    atual = ""
    for p in palavras:
        teste = p if not atual else atual + " " + p
        if stringWidth(teste, fonte, tam) <= largura:
            atual = teste
        else:
            if atual:
                linhas.append(atual)
            if stringWidth(p, fonte, tam) > largura:
                sub = ""
                for ch in p:
                    if stringWidth(sub + ch, fonte, tam) <= largura:
                        sub += ch
                    else:
                        linhas.append(sub)
                        sub = ch
                atual = sub
            else:
                atual = p
    if atual:
        linhas.append(atual)
    return linhas

def _tam_ajus(lang, tam):
    """Encolhe o tamanho da fonte por idioma (usado nas tabelas)."""
    fator = {"ja": 0.90, "zh": 0.90, "ru": 0.96,
             "he": 0.92, "ar": 0.92}.get(lang, 1.0)
    return tam * fator

def _texto_wrap(doc, texto, fonte, tam, x, y, largura, cor, entrelinha, y_min=None):
    """Mesma assinatura da funcao original. Quebra, encolhe ate caber
    e desenha o texto. Retorna o novo y."""
    fator, eh_cjk = _fator_script(texto)
    tam2 = tam * fator
    larg_interna = max(largura, 1)
    linhas = _quebrar_harmonizado(texto, fonte, tam2, larg_interna, eh_cjk)
    if y_min is not None:
        disp = max(y - y_min, 1)
        while tam2 > 5 and len(linhas) * entrelinha > disp:
            tam2 -= 0.5
            linhas = _quebrar_harmonizado(texto, fonte, tam2, larg_interna, eh_cjk)
    doc.setFont(fonte, tam2)
    doc.setFillColor(cor)
    yy = y
    for ln in linhas:
        if y_min is not None and yy - entrelinha < y_min - 0.1:
            break
        doc.drawString(x, yy, ln)
        yy -= entrelinha
    return yy

def _texto_wrap_centrado_v(doc, texto, fonte, tam, x, y, largura, cor, entrelinha, altura):
    """Texto quebrado, centralizado horizontal e verticalmente dentro da área
    de altura 'altura'. y = TOPO da área. Encolhe a fonte até caber."""
    fator, eh_cjk = _fator_script(texto)
    tam2 = tam * fator
    larg_interna = max(largura, 1)
    linhas = _quebrar_harmonizado(texto, fonte, tam2, larg_interna, eh_cjk)
    total = len(linhas) * entrelinha
    while tam2 > 5 and total > altura:
        tam2 -= 0.5
        linhas = _quebrar_harmonizado(texto, fonte, tam2, larg_interna, eh_cjk)
        total = len(linhas) * entrelinha
    doc.setFont(fonte, tam2)
    doc.setFillColor(cor)
    y_ini = y - (altura - total) / 2   # centraliza de verdade (não sobe acima da borda)
    for ln in linhas:
        doc.drawCentredString(x + larg_interna / 2, y_ini, ln)
        y_ini -= entrelinha
    return y_ini + entrelinha
