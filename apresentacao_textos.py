# -*- coding: utf-8 -*-
# ============================================================
# CABEÇALHO COM DUAS LOGOS (uma em cada lado) + RODAPÉ
# ============================================================
import os, math, logging
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas as _canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import Table, TableStyle, Paragraph, SimpleDocTemplate, Spacer, HRFlowable, Image
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4, landscape
from fontes import registrar_tudo, fonte_para          ← LINHA OBRIGATÓRIA, ANTES DA LINHA 45

_CTX_TEXTO = {}
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
IDIOMAS = ["pt", "en", "es", "it", "fr", "de", "ja", "zh",
           "ru", "he", "ar", "id", "tr", "vi"]

try:
    registrar_tudo()
except Exception as e:
    print(f"[fontes] aviso: {e}")

FONTE_POR_IDIOMA = {l: fonte_para(l)[0] for l in IDIOMAS}

# Fontes RTL (árabe e hebraico) — registro robusto, procura em qualquer pasta
FONTES_RTL = {
    "ar": ("NotoNaskhArabic", "static/fonts/NotoNaskhArabic-Regular.ttf", "static/fonts/NotoNaskhArabic-Bold.ttf"),
    "he": ("NotoSansHebrew", "static/fonts/NotoSansHebrew-Regular.ttf", "static/fonts/NotoSansHebrew-Bold.ttf"),
}

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
            except Exception as e:
                print(f"[RTL {lang}] erro regular: {e}")
        if achou_bold:
            try:
                pdfmetrics.registerFont(TTFont(nome + "-Bold", achou_bold))
            except Exception as e:
                print(f"[RTL {lang}] erro bold: {e}")

_registrar_fontes_rtl()   # ← chamada DEPOIS da definição (essencial!)

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
    """Resolve a fonte do idioma delegando ao fontes.py (fonte única)."""
    try:
        reg, bold_nome = fonte_para(lang)
    except Exception:
        return "Helvetica-Bold" if bold else "Helvetica"
    if bold:
        return bold_nome or reg or "Helvetica-Bold"
    return reg or "Helvetica"

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
           ["Inglês", "1.528"], ["Mandarim", "1.184"], ["Espanhol", "558"],
           ["Francês", "396"], ["Árabe", "335"], ["Português", "270"],
           ["Russo", "255"], ["Indonésio", "255"], ["Alemão", "134"],
           ["Japonês", "123"], ["Vietnamita", "97"], ["Turco", "90"],
           ["Italiano", "85"], ["Hebraico", "9"],
        ],
        "total_linha": "TOTAL",
        "fonte_receita": "Fonte de Receita",
        "participacao": "Participação",
        "b2c_linha": "B2C — 14 Idiomas",
        "b2b_linha": "B2B — Três Portas de Contratação (10% a 70%)",
        "pub_linha": "Publicidade Geolocalizada",
        "tabela_descontos": "Descontos Progressivos — Porta 1 e Porta 2",
        "grafico_anos": ["1. Ano", "3. Ano", "5. Ano"],
        "grafico_titulo": "Projeção Conservadora (R$ mil)",
        "grafico_titulo_linha": "Crescimento Projetado (R$ mil)",
        "fale_conosco": "Fale Conosco",

        "sumario_intro": "Esta apresentação está estruturada para guiar investidores e parceiros por todos os aspectos estratégicos da A1ELOS Global Numerology — da tese de mercado ao modelo de receita recorrente.",
        "sumario_cards": [
            ("01", "Sobre a A1ELOS", "Holding, portfólio e credencial DUNS"),
            ("02", "Oportunidade de Mercado", "Economia global de bem-estar US$ 6,8 tri"),
            ("03", "Solução e Alcance Global", "14 idiomas, ~5,3 bi de falantes"),
            ("04", "Novos Mercados", "Indonésia, Turquia, Vietnã e RH Corporativo"),
            ("05", "Portfólio e Preços", "24 produtos calibrados por poder aquisitivo"),
            ("06", "Receita Recorrente", "Banners publicitários e Pacotes B2B"),
            ("07", "Projeções e Investimento", "Horizonte de 50 anos · Rodada Seed R$ 3,5M"),
        ],

        "sobre_titulo": "Sobre a A1ELOS",
        "sobre_texto": "A A1ELOS é uma holding de tecnologia e conhecimento que une inteligência artificial, numerologia aplicada e estratégia cultural para criar produtos digitais de alto impacto em escala global. Nossa missão: democratizar o autoconhecimento numérico com respeito cultural e respeito ao poder aquisitivo de cada mercado.",
        "sobre_kpis": [
            ("24", "Produtos Ativos", "Em 4 níveis de acesso"),
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
        "mercado_rh_titulo": "Novo Mercado: RH Corporativo — o 24º Produto",
        "mercado_rh_texto": (
            "O 24º produto — Compatibilidade de Equipes RH (R$ 98) — abre o principal mercado B2B "
            "da A1ELOS: o RH corporativo. A análise de compatibilidade energética entre gestores e "
            "colaboradores (energia ideal: número 8) posiciona a plataforma como ferramenta pioneira "
            "de employer branding e bem-estar corporativo, contratada por três portas distintas: "
            "Planos Prontos com desconto progressivo de 10% a 50% conforme o volume, Montar Sob Medida "
            "com desconto automático até 50%, e Negociação Direta acima de 2.000 códigos com desconto "
            "de até 70% (Plano Diamante)."
        ),
        "mercado_rh_vantagens": [
            "Harmonia energética do setor → redução de atritos interpessoais e maior coesão da equipe",
            "Alinhamento de posturas e pensamentos entre gestores e colaboradores → comunicação mais fluida",
            "Menor rotatividade (turnover) e maior retenção de talentos",
            "Clima organizacional positivo → ganho de produtividade e bem-estar",
            "Employer branding fortalecido → atração de talentos alinhados à cultura",
        ],
        "mercado_rh_cards": [
            ["HR Tech", "US$ 42,34 bi (2025) → US$ 77,74 bi (2031)", "CAGR 10,35% · Mordor Intelligence"],
            ["Employer Branding", "US$ 1,89 bi (2025) → US$ 3,62 bi (2031)", "CAGR 11,19% · Mordor Intelligence"],
            ["Corporate Wellness", "US$ 66,31 bi (2025) → US$ 94,5 bi (2031)", "CAGR 6,12% · Mordor Intelligence"],
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

        "portfolio_titulo": "Portfólio: 24 Produtos em 7 Níveis",
        "portfolio_texto": "A estrutura em camadas garante que cada perfil de usuário — do curioso ao profissional — encontre uma oferta adequada ao seu nível de engajamento e capacidade financeira.",
        "portfolio_cabecalho": ["Nível", "Produtos", "Faixa (R$)", "Perfil"],
        "portfolio_linhas": [
             ["Entrada", "Mapa Express, Qual Vida/Ano, Pesquisa IA de Nomes, Nome do Pet, Nickname, Domínio, Canal, Equipe, Projeto, Evento", "8", "Curioso, primeiro contato"],
             ["Intermediário", "Mapa Completo", "17", "Usuário engajado"],
             ["Avançado", "Nome de Urna, Nº Eleitoral, Nº do Imóvel, Calendário Mensal", "26", "Usuário recorrente"],
             ["Profissional", "Nome Artístico, Nome de Bebê, Assinatura, Nome de ONG", "35", "Profissional, empreendedor"],
             ["Premium", "Nome de Negócio, Mapa do Casal", "44", "Empreendedor consolidado"],
             ["Corporativo", "Mapa Família, Compatibilidade de Equipes RH ★", "98", "Alta renda / RH"],
             ["B2B", "Bônus Coletivo/Empresarial (3 portas)", "Sob consulta", "Empresas e equipes"],
        ],
        "portfolio_rodape": "24 produtos cobrem toda a jornada do usuário, do primeiro contato ao cliente recorrente premium — maximizando LTV por idioma e mercado. Destaque: Compatibilidade de Equipes RH (R$ 98) — produto pioneiro no mercado de RH corporativo, energia ideal 8.",

        "negocio_titulo": "Modelo de Negócio: 3 Fontes de Receita",
        "negocio_texto": "A A1ELOS foi desenhada com receita diversificada e escalável: vendas diretas ao consumidor final em escala global, contratos B2B de alto valor e publicidade geolocalizada recorrente — três motores que se alimentam mutuamente.",
        "negocio_colunas": [
            ("B2C — 14 Idiomas", "Venda direta de produtos digitais em todas as moedas, com precificação adaptada por PPC. Escala automática via IA — sem equipe de atendimento proporcional ao crescimento."),
            ("B2B — Três Portas de Contratação", "Porta 1: Planos Prontos (10% a 50%). Porta 2: Montar Sob Medida com desconto automático até 50%. Porta 3: Negociação Direta acima de 2.000 códigos, com desconto de até 70% (Plano Diamante). Contratos respaldados pelo DUNS 942242668."),
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

        "pacotes_b2b_titulo": "Pacotes Empresariais B2B — Alto Valor, Alto Volume",
        "pacotes_b2b_sub": (
            "Uma linha de negócio com três formas de contratar. A empresa escolhe o nível "
            "de controle que precisa — do pacote pronto à negociação sob medida."
        ),
        "pacotes_b2b_texto": (
            "Os Pacotes B2B transformam a A1ELOS em uma ferramenta de employer branding e "
            "bem-estar corporativo. No centro dessa estratégia está o produto exclusivo e "
            "contínuo: a Compatibilidade de Equipes RH. Diferente de brindes pontuais, a análise "
            "de compatibilidade é uma ferramenta de gestão de pessoas que a empresa incorpora ao "
            "seu dia a dia — calculando setores e equipes com a energia desejada e sincronizando "
            "todos os membros na mesma sintonia. Ideal para pequenas e grandes empresas, é o "
            "serviço que o Departamento de Recursos Humanos usa de forma constante, apoiado em "
            "mercados em forte crescimento: HR Tech (CAGR 10,35%), Employer Branding (CAGR 11,19%) "
            "e Corporate Wellness (CAGR 6,12%)."
        ),
        "portas_titulo": "As Três Portas de Contratação",
        "porta_1_nome": "Porta 1 — Planos Prontos (praticidade imediata)",
        "porta_1_texto": (
             "Pacotes pré-definidos com produtos e quantidades fixas. A empresa escolhe, paga e "
             "recebe a lista de códigos em minutos. Sem negociação, sem reunião, sem espera. Feito "
             "para quem precisa agir agora: uma promoção, uma data comemorativa, um lançamento."
        ),
        "porta_2_nome": "Porta 2 — Montar Sob Medida (controle total do pedido)",
        "porta_2_texto": (
             "A empresa define exatamente o que quer: cada produto, cada quantidade. O desconto é "
             "aplicado automaticamente conforme o volume. Sem limite de compra. Ideal para "
             "diferenciação de clientes por categoria, premiação de funcionários por desempenho e "
             "gincanas internas."
        ),
        "porta_3_nome": "Porta 3 — Negociação Direta (grandes volumes)",
        "porta_3_texto": (
             "A partir de 2.000 unidades, ou quando o desconto necessário ultrapassa 50%, a empresa "
             "preenche um formulário de proposta e recebe uma condição personalizada — com "
             "possibilidade de chegar a 70% de desconto. Reservado a operações de larga escala."
        ),
        "b2b_nota_fechamento": (
             "Um único pedido de 2.000 códigos na faixa premium representa R$ 98.000 de receita em "
             "uma transação. O B2B não é acessório do modelo: é o motor de ticket alto que sustenta "
             "o crescimento de curto prazo."
        ),

        "descontos_titulo": "Descontos Progressivos",
        "descontos_linhas": [
             ["A partir de", "Desconto", "Perfil", "Uso Recomendado"],
             ["10 códigos", "10%", "Pequenas equipes", "Ação pontual de bem-estar"],
             ["50 códigos", "15%", "Equipes em crescimento", "Programas recorrentes"],
             ["100 códigos", "20%", "PMEs", "Benefício trimestral"],
             ["200 códigos", "30%", "Empresas médias", "Programas completos"],
             ["500 códigos", "40%", "Médias empresas", "Brinde anual a colaboradores"],
             ["1.000 códigos", "45%", "Grandes corporações", "Fidelização de clientes"],
             ["2.000 códigos", "50%", "Grandes grupos", "Larga escala"],
             ["Acima de 2.000", "Até 70% (Porta 3)", "Plano Diamante sob medida", "Distribuição de bônus em volume"],
        ],

        "rh_titulo": "Compatibilidade de Equipes RH — O 24º Produto",
        "rh_sub": "O mesmo motor do Mapa Família. Uma nova capa. Um mercado inteiramente novo.",
        "rh_texto_1": (
             "O 24º produto da A1ELOS é a demonstração prática da eficiência do nosso modelo: "
             "reaproveitamos o motor de cruzamento energético que já sustenta o Mapa Família "
             "Premium — nosso produto de afinidade emocional — e o reposicionamos para o ambiente "
             "corporativo. Nenhuma linha de código nova. Uma nova capa, um novo texto, um novo "
             "comprador: o Departamento de Recursos Humanos."
        ),
        "rh_texto_2": (
             "A análise de compatibilidade energética entre gestores e colaboradores, e entre os "
             "membros de uma mesma equipe, posiciona a A1ELOS como pioneira no mercado de RH "
             "corporativo. A harmonia energética do setor reduz atritos interpessoais, alinha "
             "posturas e pensamentos, diminui a rotatividade, fortalece o clima organizacional e "
             "eleva a produtividade."
        ),
        "rh_texto_3": (
             "Diferença de propósito: no Mapa Família, a energia é fixa em 5 e 6 — território do "
             "afeto e da harmonia doméstica. Na Compatibilidade de Equipes, a energia fica aberta "
             "para o pesquisador, com sugestão de 8 (poder e liderança), 4 (estrutura) e 7 "
             "(análise) — território do trabalho e da execução. O sistema é o mesmo; o propósito "
             "é outro."
        ),
        "rh_ancoras": [
             "Zero custo de desenvolvimento — reaproveitamento integral do motor existente",
             "Ticket por unidade 12 vezes maior — R$ 98 contra a média de R$ 8 da cauda longa",
             "Volume escalável — o RH compra para toda a empresa, não para uma pessoa",
             "Mercado em crescimento de dois dígitos — HR Tech (10,35%), Employer Branding (11,19%), Corporate Wellness (6,12%)",
             "Contrato respaldado por DUNS — habilita venda corporativa formal",
        ],

        "projecoes_titulo": "Projeções Financeiras: Horizonte de 50 Anos",
        "projecoes_texto": "As projeções foram construídas com base em estimativas percentuais de penetração sobre o mercado potencial de ~5,32 bilhões de falantes, com conversão conservadora de 3% e resgate de bônus entre 70% e 90%. Com o 24º produto — Compatibilidade de Equipes RH (R$ 98) e o canal Bônus Coletivo/Empresarial —, a receita B2B de RH passa a compor a projeção, ancorada em mercados verificados: HR Tech (CAGR 10,35%), Employer Branding (CAGR 11,19%) e Corporate Wellness (CAGR 6,12%). O curto prazo (anos 1–5) evidencia o crescimento acelerado da nova frente B2B; o longo prazo reflete a estabilidade contínua do modelo até a assimilação plena do mercado endereçável.",
        "projecoes_tabela": [
            ["Horizonte", "Conservador (R$)", "Otimista (R$)"],
            ["Ano 1", "R$ 318k", "R$ 810k"],
            ["Ano 2", "R$ 630k", "R$ 1,8M"],
            ["Ano 3", "R$ 1,20M", "R$ 3,50M"],
            ["Ano 4", "R$ 2,2M", "R$ 6,2M"],
            ["Ano 5", "R$ 3,70M", "R$ 9,6M"],
        ],
        "projecoes_tabela_50": [
            ["Horizonte", "Conservador (R$)", "Otimista (R$)"],
            ["Ano 1", "R$ 318k", "R$ 810k"],
            ["Ano 3", "R$ 1,20M", "R$ 3,50M"],
            ["Ano 5", "R$ 3,70M", "R$ 9,6M"],
            ["Ano 7", "R$ 7,8M", "R$ 20,5M"],
            ["Ano 10", "R$ 16,3M", "R$ 44,0M"],
            ["Ano 20", "R$ 64M", "R$ 184M"],
            ["Ano 30", "R$ 133M", "R$ 359M"],
            ["Ano 40", "R$ 202M", "R$ 606M"],
            ["Ano 50", "R$ 276M", "R$ 869M"],
        ],
        "projecoes_curto_titulo": "Projeções Financeiras: Curto Prazo (Anos 1–5)",
        "projecoes_curto_texto": "O curto prazo evidencia o crescimento acelerado da nova frente B2B de RH (Compatibilidade de Equipes + Bônus Coletivo), quase 12x em 5 anos no cenário conservador — antes da estabilização de longo prazo.",
        "projecoes_curto_tabela": [
            ["Horizonte", "Conservador (R$)", "Otimista (R$)"],
            ["Ano 1", "R$ 318k", "R$ 810k"],
            ["Ano 2", "R$ 630k", "R$ 1,8M"],
            ["Ano 3", "R$ 1,20M", "R$ 3,50M"],
            ["Ano 4", "R$ 2,2M", "R$ 6,2M"],
            ["Ano 5", "R$ 3,70M", "R$ 9,6M"],
        ],

        "tracao_titulo": "Tração e Resultados Comprovados",
        "tracao_texto": "A A1ELOS já opera com métricas de produto que validam o modelo — alta retenção, avaliação premium e uma base crescente de parceiros B2B demonstram que a plataforma entrega valor real ao usuário final e ao mercado corporativo.",
        "tracao_kpis": [
            ("12K+", "Usuários Ativos", "Pessoas físicas que já usaram a plataforma"),
            ("87%", "Retenção de Usuários", "Muito acima da média da indústria (~30%)"),
            ("4,8★", "Avaliação Média", "Satisfação comprovada do usuário final"),
            ("23", "Empresas Parceiras B2B", "Contratos corporativos ativos (≠ 24 produtos do catálogo)"),
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
        "selo_final": ["DUNS 942242668", "24 PRODUTOS", "14 IDIOMAS", "~5,3 BI FALANTES"],
        "graf_cons": "Conservador",
        "graf_otim": "Otimista",

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
        "falantes_col": "Speakers (mi)",
        "linhas_idiomas": [
           ["English", "1.528"],
           ["Mandarin", "1.184"],
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
        "tabela_descontos": "Progressive Discounts Table",
        "grafico_anos": ["Year 1", "Year 3", "Year 5"],
        "grafico_titulo": "Conservative Projection (R$ thousand)",
        "grafico_titulo_linha": "Projected Growth (R$ thousand)",
        "fale_conosco": "Contact Us",
        "sumario_intro": "This presentation is structured to guide investors and partners through every strategic aspect of A1ELOS Global Numerology — from the market thesis to the recurring revenue model.",
        "sumario_cards": [
            ("01", "About A1ELOS", "Holding, portfolio and DUNS credential"),
            ("02", "Market Opportunity", "Global wellness economy US$ 6,8 tri"),
            ("03", "Solution and Global Reach", "14 languages, ~5,3 bi speakers"),
            ("04", "New Markets", "Indonesia, Turkey, Vietnam and Corporate HR"),
            ("05", "Portfolio and Pricing", "24 products calibrated by purchasing power"),
            ("06", "Recurring Revenue", "Advertising banners and B2B Packages"),
            ("07", "Projections and Investment", "50-year horizon · Seed Round R$ 3,5M"),
        ],
        "sobre_titulo": "About A1ELOS",
        "sobre_texto": "A1ELOS is a technology and knowledge holding company that combines artificial intelligence, applied numerology and cultural strategy to create high-impact digital products on a global scale. Our mission: to democratize numerical self-knowledge with cultural respect and respect for the purchasing power of each market.",
        "sobre_kpis": [
            ("23", "Active Products", "Across 4 access levels"),
            ("14", "Languages", "~67% of the world population"),
            ("5,3B", "Speakers", "Real addressable market"),
            ("AI", "Integrated", "Personalization engine"),
        ],
        "sobre_duns": "DUNS 942242668 — Dun & Bradstreet certification valid in 190+ countries, enabling B2B contracts and international joint ventures.",
        "duns_titulo": "International Credibility",
        "duns_texto": "The DUNS number is A1ELOS's corporate passport on the international stage. It signals to partners, corporate clients and investors that the company has verifiable identity, traceable history and contractual capacity in any jurisdiction.",
        "duns_numero": "942242668",
        "duns_emitido": "Issued by Dun & Bradstreet — the global standard of business identity recognized in more than 190 countries.",
        "duns_paises": "190+ COUNTRIES",
        "duns_beneficios": [
            ("B2B Contracts", "Qualification for global tenders and suppliers"),
            ("Joint Ventures", "International partnerships with facilitated due diligence"),
            ("Immediate Credibility", "A sign of seriousness for institutional investors"),
        ],
        "mercado_titulo": "Market Opportunity",
        "mercado_texto": "We live in the perfect convergence: digital wellness is exploding globally while numerology and astrology migrate to highly engaging apps. A1ELOS is positioned exactly at this intersection, with 74% of the world population already online (~6 billion people).",
        "mercado_cards": [
            ("Global Wellness", "US$ 6,8 tri → US$ 9,8 tri by 2029 (+7,6% p.a.)"),
            ("Astrology/Numerology Apps", "US$ 3 bi → US$ 9 bi by 2030 · CAGR 20%"),
            ("Wellness Apps", "CAGR 14,9% → US$ 26,2 bi in 2030"),
            ("Online Users", "74% of the world · ~6 billion people"),
        ],
        "mercado_rh_titulo": "New Market: Corporate HR — The 24th Product",
        "mercado_rh_texto": "The 24th product — Team Compatibility HR (R$ 98) — opens A1ELOS's main B2B market: corporate HR. The analysis of energetic compatibility between managers and employees (ideal energy: number 8) positions the platform as a pioneering employer branding and corporate wellness tool, with progressive discounts from 10% to 50% and direct negotiation above 2.000 codes (Diamond Plan).",
        "mercado_rh_vantagens": [
            "Energetic harmony of the department → fewer interpersonal conflicts and greater team cohesion",
            "Alignment of attitudes and mindsets between managers and employees → more fluid communication",
            "Lower turnover and greater talent retention",
            "Positive organizational climate → gains in productivity and well-being",
            "Strengthened employer branding → attraction of talent aligned with the culture",
        ],
        "mercado_rh_cards": [
            ["HR Tech", "US$ 42,34 bi (2025) → US$ 77,74 bi (2031)", "CAGR 10,35% · Mordor Intelligence"],
            ["Employer Branding", "US$ 1,89 bi (2025) → US$ 3,62 bi (2031)", "CAGR 11,19% · Mordor Intelligence"],
            ["Corporate Wellness", "US$ 66,31 bi (2025) → US$ 94,5 bi (2031)", "CAGR 6,12% · Mordor Intelligence"],
        ],
        "problema_titulo": "The Problem We Solve",
        "problema_col_esq_titulo": "Current Market Failures",
        "problema_col_esq": [
            ("Language Barrier", "The vast majority of numerology tools operate only in English, excluding billions of native speakers of other languages."),
            ("Prices Detached from Reality", "Products priced in dollars for emerging markets create economic exclusion — the user does not reject the product, they reject the unaffordable price."),
            ("Lack of Depth", "Generic tools deliver shallow answers without personalization, without cultural context and without practical application to daily life."),
        ],
        "problema_col_dir_titulo": "The Cost of Exclusion",
        "problema_col_dir": "When a platform ignores language and purchasing power, it voluntarily abandons the largest market in the world: the 4+ billion people living in emerging economies who speak non-Anglophone languages. That is the gap A1ELOS occupies with surgical precision.",
        "problema_destaque": "Platforms that ignore local purchasing power lose access to more than 60% of the global addressable market.",
        "solucao_titulo": "Our Solution: 3 Strategic Pillars",
        "solucao_texto": "A1ELOS has built an integrated platform that combines numerical science, artificial intelligence and cultural sensitivity. The solution operates on three complementary fronts, ensuring diversified revenue and high retention.",
        "solucao_colunas": [
            ("Personal Maps", "Deep, personalized numerical analyses for the end user — identity, mission, life cycles and compatibility — delivered in 14 languages with integrated AI."),
            ("Business Numerology", "Numerological diagnostics applied to brands, CNPJs, founding dates and corporate strategy. A differentiated product of high perceived value in the B2B market."),
            ("White-Label B2B", "Platform licensing for partner companies that want to offer numerology under their own brand — with multilingual support and full customization."),
        ],
        "alcance_titulo": "Global Reach: 14 Languages · ~5,3 Billion Speakers",
        "alcance_texto": "A1ELOS covers ~67% of the world population with a truly multilingual platform. Each language represents a distinct cultural market, with pricing calibrated to local purchasing power.",
        "mercados_titulo": "The 3 New Markets: +442 Million Speakers",
        "mercados_texto": "The strategic expansion to Indonesia, Turkey and Vietnam represents a qualitative leap: markets with high economic growth, increasing digital penetration and proven demand for affordable digital wellness solutions.",
        "mercados_cards": [
            ("Indonesia", ["285 mi inhabitants", "80,5% internet penetration", "~255 mi Indonesian speakers", "Wellness: US$ 51,2 bi (2025) → US$ 72,8 bi (2034)"]),
            ("Turkey", ["85,9 mi inhabitants", "GDP PPP per capita US$ 37.301", "~90 mi Turkish speakers", "Above the world average (US$ 27.211)"]),
            ("Vietnam",  ["~100 mi inhabitants", "GDP per capita ~US$ 5.066 (+7,4%/yr)", "~97 mi Vietnamese speakers", "Wellness: US$ 303 mi (2025) → US$ 485 mi (2030)"]),
        ],
        "mercados_rodape": "3 new markets = +442 million new addressable speakers — incorporated into the platform with culturally calibrated pricing.",
        "preco_titulo": "Conscious Pricing Philosophy",
        "preco_esq": "Cultural respect + respect for purchasing power = real addressable market. Same proportion of value. Different prices. Equal dignity for all markets.",
        "preco_dir_titulo": "How It Works in Practice",
        "preco_dir": "A1ELOS applies Purchasing Power Parity (PPP) as its central pricing criterion. The same product delivers the same relative value to the user in Lagos, Jakarta, Hanoi or New York — the price is calibrated so that the financial effort is proportional to local income.",
        "preco_pilares": [
            ("PPP Calibration", "Prices adjusted to each country's purchasing power index"),
            ("Cultural Respect", "Language, currency and local context integrated into the product"),
            ("Superior Conversion", "A fair price generates more conversion and greater long-term retention"),
        ],
        "portfolio_titulo": "Portfolio: 24 Products in 4 Levels",
        "portfolio_texto": "The layered structure ensures that every user profile — from the curious to the professional — finds an offer suited to their level of engagement and financial capacity.",
        "portfolio_tabela": [
           ["Level", "Products", "Price Range (R$)", "Profile"],
           ["Basic", "Express Map, Full Map", "R$ 8 – 17", "Curious, first contact"],
           ["Intermediate", "AI Search, Ballot Name, Electoral No.", "R$ 26 – 53", "Engaged user"],
           ["Advanced", "NGO Name, Artistic Name, Baby Name, Signature, Business Name", "R$ 35 – 44", "Professional, entrepreneur"],
           ["Premium", "Couple Map, Family Map, Team Compatibility HR ★, Collective Bonus", "R$ 98", "High income, corporate use"],
           ["B2B", "Corporate Packages, licenses, gifts", "On request", "Companies and teams"],
        ],
        "portfolio_rodape": "24 products cover the user's entire journey, from first contact to the recurring premium customer — maximizing LTV per language and market. Highlight: Team Compatibility HR (R$ 98) — pioneering product in the corporate HR market, ideal energy 8.",
        "negocio_titulo": "Business Model: 3 Revenue Sources",
        "negocio_texto": "A1ELOS was designed with diversified and scalable revenue: direct sales to the end consumer on a global scale, high-value B2B contracts and recurring geolocated advertising — three engines that feed each other.",
        "negocio_colunas": [
            ("B2C — 14 Languages", "Direct sales of digital products in all currencies, with pricing adapted by PPP. Automatic scale via AI — without a service team proportional to growth."),
            ("B2B — Progressive Discounts", "Corporate packages for HR, employer branding and institutional gifts. Discounts from 10% to 50% by volume. Above 2.000 codes, direct negotiation (Diamond Plan). Contracts backed by DUNS 942242668."),
            ("Geolocated Advertising", "Banners segmented by country, continent or worldwide with automated rotation. High-value monthly recurring revenue — without dependence on product sales volume."),
        ],
        "banners_titulo": "Advertising Banners — Recurring Monthly Revenue",
        "banners_texto": "The A1ELOS platform offers premium advertising space with precise geolocation targeting — country, continent or worldwide. With automatic rotation every 8 seconds and formats optimized for desktop and mobile, the banners deliver measurable visibility to regional and international advertisers.",
        "banners_tabela": [
            ["Segmentation", "Fixed (R$/month)", "Temporary (R$/month)", "Advertiser Profile"],
            ["Country", "R$ 800", "R$ 500", "Local SMEs, regional commerce"],
            ["Continent", "R$ 1.800", "R$ 1.200", "Regional brands, continental expansion"],
            ["World", "R$ 3.500", "R$ 2.500", "Global companies, international apps"],
            ["Exclusive Sponsorship", "R$ 6.000", "R$ 4.500/campaign", "Master sponsors, launches"],
        ],
        "banners_formatos": "728×90 px — Central desktop banner · 320×100 px — Optimized mobile format · 8 seconds — Automatic rotation · Geo-target — Country, continent or worldwide reach",
        "b2b_titulo": "B2B Corporate Packages — High Value, High Volume",
        "b2b_texto": "The B2B Packages turn A1ELOS into an employer branding and corporate wellness tool. At the center of this strategy is the exclusive, continuous product: Team Compatibility HR (R$ 98). Unlike one-off gifts, the compatibility analysis is a people management tool that the company incorporates into its daily routine — calculating departments and teams with the desired energy and synchronizing all members of a department in the same rhythm and harmony. Ideal for small and large companies, it is the service the Human Resources Department uses constantly, supported by fast-growing markets: HR Tech (CAGR 10,35%), Employer Branding (CAGR 11,19%) and Corporate Wellness (CAGR 6,12%).",
        "b2b_planos": [
            ("Basic Plan · 50 codes", "50× Express Map (R$ 8 each). Ideal for employee benefit programs and onboarding actions."),
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
            ["1.000 codes", "45%", "Large corporations", "Customer loyalty"],
            ["2.000 codes", "50%", "Large groups", "Large scale"],
            ["Above 2.000", "Negotiable", "Tailored Diamond Plan", "Volume bonus distribution"],
        ],
        "rh_destaque_titulo": "Team Compatibility HR — The Exclusive Product",
        "rh_destaque_texto": "The analysis of energetic compatibility between managers and employees, and among members of the same team (ideal energy: number 8 — power, leadership and material balance), positions A1ELOS as a pioneer in the corporate HR market. The energetic harmony of the department reduces interpersonal conflicts, aligns attitudes and mindsets, decreases turnover, strengthens the organizational climate and raises productivity — a value that the Collective Bonus, as a one-off gift, does not deliver. It is the product that sustains short-term growth and recurring B2B revenue.",
        "projecoes_titulo": "Financial Projections: 50-Year Horizon",
        "projecoes_texto": "The projections were built on percentage penetration estimates over the potential market of ~5,32 billion speakers, with a conservative conversion of 3% and bonus redemption between 70% and 90%. With the 24th product — Team Compatibility HR (R$ 98) and the Collective/Corporate Bonus channel —, the B2B HR revenue becomes part of the projection, anchored in verified markets: HR Tech (CAGR 10,35%), Employer Branding (CAGR 11,19%) and Corporate Wellness (CAGR 6,12%). The short term (years 1–5) highlights the accelerated growth of the new B2B front; the long term reflects the model's continuous stability until the full assimilation of the addressable market.",
        "projecoes_tabela": [
            ["Horizon", "Conservative (R$)", "Optimistic (R$)"],
            ["Year 1", "R$ 318k", "R$ 810k"],
            ["Year 2", "R$ 630k", "R$ 1,8M"],
            ["Year 3", "R$ 1,20M", "R$ 3,50M"],
            ["Year 4", "R$ 2,2M", "R$ 6,2M"],
            ["Year 5", "R$ 3,70M", "R$ 9,6M"],
        ],
        "projecoes_tabela_50": [
            ["Horizon", "Conservative (R$)", "Optimistic (R$)"],
            ["Year 1", "R$ 318k", "R$ 810k"],
            ["Year 3", "R$ 1,20M", "R$ 3,50M"],
            ["Year 5", "R$ 3,70M", "R$ 9,6M"],
            ["Year 7", "R$ 7,8M", "R$ 20,5M"],
            ["Year 10", "R$ 16,3M", "R$ 44,0M"],
            ["Year 20", "R$ 64M", "R$ 184M"],
            ["Year 30", "R$ 133M", "R$ 359M"],
            ["Year 40", "R$ 202M", "R$ 606M"],
            ["Year 50", "R$ 276M", "R$ 869M"],
        ],
        "projecoes_curto_titulo": "Financial Projections: Short Term (Years 1–5)",
        "projecoes_curto_texto": "The short term highlights the accelerated growth of the new B2B HR front (Team Compatibility + Collective Bonus), almost 12x in 5 years in the conservative scenario — before long-term stabilization.",
        "projecoes_curto_tabela": [
            ["Horizon", "Conservative (R$)", "Optimistic (R$)"],
            ["Year 1", "R$ 318k", "R$ 810k"],
            ["Year 2", "R$ 630k", "R$ 1,8M"],
            ["Year 3", "R$ 1,20M", "R$ 3,50M"],
            ["Year 4", "R$ 2,2M", "R$ 6,2M"],
            ["Year 5", "R$ 3,70M", "R$ 9,6M"],
         ],
        "tracao_titulo": "Traction and Proven Results",
        "tracao_texto": "A1ELOS already operates with product metrics that validate the model — high retention, premium rating and a growing base of B2B partners demonstrate that the platform delivers real value to the end user and to the corporate market.",
        "tracao_kpis": [
            ("12K+", "Active Users", "Organic base in consistent growth"),
            ("87%", "Retention", "Far above the industry average (~30%)"),
            ("4,8★", "Average Rating", "Proven end-user satisfaction"),
            ("23", "B2B Partners", "Active contracts with companies and HRs"),
        ],
        "roteiro_titulo": "Strategic Roadmap",
        "roteiro_texto": "A1ELOS executes a plan in four progressive phases — from consolidating the current base to global market leadership, with clear exit options for investors.",
        "roteiro_fases": [
            ("Phase 1 · Consolidation", "Strengthening the user base in the already active languages. Conversion, retention and LTV optimization. Seed Round concluded."),
            ("Phase 2 · Expansion", "Official launch in the 3 new markets: Indonesia, Turkey and Vietnam. Acceleration of the B2B channel and geolocated advertising."),
            ("Phase 3 · Global Entry", "Active presence in all 14 languages with localized campaigns. White-label partnerships in 5+ continents. Series A."),
            ("Phase 4 · Leadership", "20+ countries with consolidated operations. Global reference SaaS platform in applied numerology. IPO or strategic exit."),
        ],
        "invest_titulo": "Investment & Contact",
        "invest_texto": "We are ready for private presentations, due diligence and negotiations. Contact us through your preferred channel.",
        "invest_dados": [
            ("Seed Round", "R$ 3,5 million"),
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
        "selo_final": ["DUNS 942242668", "24 PRODUCTS", "14 LANGUAGES", "~5,3 BI SPEAKERS"],
        "graf_cons": "Conservative",
        "graf_otim": "Optimistic",
        "grafico_titulo_linha": "Projected Growth (R$ thousand)",
        "pix_titulo": "Brazil: The Pix Infrastructure",
        "pix_texto": "Pix is Brazil's public instant payment infrastructure. For A1ELOS, it ensures immediate collection, low cost and universal acceptance — the foundation of the B2C operation in the Brazilian market and the gateway to international expansion.",
        "pix_kpis": [
            ("30,1 bi", "Transactions in 2025", "+20% vs 2024 · Febraban"),
            ("76,4%", "of the population uses Pix", "211 million Brazilians · Central Bank"),
            ("R$ 68,2 tri", "moved in the 2nd half of 2025", "78,4 bi transactions · Central Bank"),
            ("~80 bi", "transactions in 2025", "+25,7% vs previous year · Pix Report"),
        ],
        "pix_fonte": "Sources: Central Bank of Brazil (Pix in Numbers) and Febraban (Banking Technology Survey).",
        "ref_titulo": "Bibliographic References",
        "ref_intro": "Sources used for the market data, projections and indicators of this presentation.",
        "ref_lista": [
            ("Global Wellness Institute", "Global wellness economy: US$ 6,8 tri (2024) → US$ 9,8 tri (2029)."),
            ("MarkNtel Advisors", "Astrology and numerology apps: US$ 3 bi → US$ 9 bi by 2030 (CAGR ~20%)."),
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
        "falantes_col": "Hablantes (mi)",
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
        "grafico_anos": ["Año 1", "Año 3", "Año 5"],
        "grafico_titulo": "Proyección Conservadora (R$ mil)",
        "grafico_titulo_linha": "Crecimiento Proyectado (R$ mil)",
        "fale_conosco": "Contáctenos",
        "sumario_intro": "Esta presentación está estructurada para guiar a inversores y socios por todos los aspectos estratégicos de A1ELOS Global Numerology — desde la tesis de mercado hasta el modelo de ingresos recurrentes.",
        "sumario_cards": [
            ("01", "Sobre A1ELOS", "Holding, portafolio y credencial DUNS"),
            ("02", "Oportunidad de Mercado", "Economía global de bienestar US$ 6,8 tri"),
            ("03", "Solución y Alcance Global", "14 idiomas, ~5,3 bi de hablantes"),
            ("04", "Nuevos Mercados", "Indonesia, Turquía, Vietnam y RH Corporativo"),
            ("05", "Portafolio y Precios", "24 productos calibrados por poder adquisitivo"),
            ("06", "Ingresos Recurrentes", "Banners publicitarios y Paquetes B2B"),
            ("07", "Proyecciones e Inversión", "Horizonte de 50 años · Ronda Seed R$ 3,5M"),
        ],
        "sobre_titulo": "Sobre A1ELOS",
        "sobre_texto": "A1ELOS es un holding de tecnología y conocimiento que une inteligencia artificial, numerología aplicada y estrategia cultural para crear productos digitales de alto impacto a escala global. Nuestra misión: democratizar el autoconocimiento numérico con respeto cultural y respeto al poder adquisitivo de cada mercado.",
        "sobre_kpis": [
            ("23", "Productos Activos", "En 4 niveles de acceso"),
            ("14", "Idiomas", "~67% de la población mundial"),
            ("5,3B", "Hablantes", "Mercado direccionable real"),
            ("IA", "Integrada", "Motor de personalización"),
        ],
        "sobre_duns": "DUNS 942242668 — Certificación Dun & Bradstreet válida en más de 190 países, habilitando contratos B2B y joint ventures internacionales.",
        "duns_titulo": "Credibilidad Internacional",
        "duns_texto": "El número DUNS es el pasaporte corporativo de A1ELOS en el escenario internacional. Señala a socios, clientes corporativos e inversores que la empresa posee identidad verificable, historial rastreable y capacidad contractual en cualquier jurisdicción.",
        "duns_numero": "942242668",
        "duns_emitido": "Emitido por Dun & Bradstreet — el estándar global de identidad empresarial reconocido en más de 190 países.",
        "duns_paises": "190+ PAÍSES",
        "duns_beneficios": [
            ("Contratos B2B", "Habilitación para licitaciones y proveedores globales"),
            ("Joint Ventures", "Asociaciones internacionales con due diligence facilitada"),
            ("Credibilidad Inmediata", "Señal de seriedad para inversores institucionales"),
        ],
        "mercado_titulo": "Oportunidad de Mercado",
        "mercado_texto": "Vivimos la convergencia perfecta: el bienestar digital explota globalmente mientras la numerología y la astrología migran a apps de alto engagement. A1ELOS está posicionada exactamente en esa intersección, con el 74% de la población mundial ya en línea (~6 mil millones de personas).",
        "mercado_cards": [
            ("Bienestar Global", "US$ 6,8 tri → US$ 9,8 tri hasta 2029 (+7,6% anual)"),
            ("Apps Astrología/Numerología", "US$ 3 bi → US$ 9 bi hasta 2030 · CAGR 20%"),
            ("Apps de Bienestar", "CAGR 14,9% → US$ 26,2 bi en 2030"),
            ("Usuarios en Línea", "74% del mundo · ~6 mil millones de personas"),
        ],
        "mercado_rh_titulo": "Nuevo Mercado: RH Corporativo — el 24º Producto",
        "mercado_rh_texto": "El 24º producto — Compatibilidad de Equipos RH (R$ 98) — abre el principal mercado B2B de A1ELOS: el RH corporativo. El análisis de compatibilidad energética entre gestores y colaboradores (energía ideal: número 8) posiciona la plataforma como herramienta pionera de employer branding y bienestar corporativo, con descuentos progresivos del 10% al 50% y negociación directa por encima de 2.000 códigos (Plan Diamante).",
        "mercado_rh_vantagens": [
            "Armonía energética del sector → reducción de fricciones interpersonales y mayor cohesión del equipo",
            "Alineación de posturas y pensamientos entre gestores y colaboradores → comunicación más fluida",
            "Menor rotación (turnover) y mayor retención de talentos",
            "Clima organizacional positivo → ganancia de productividad y bienestar",
            "Employer branding fortalecido → atracción de talentos alineados con la cultura",
        ],
        "mercado_rh_cards": [
            ["HR Tech", "US$ 42,34 bi (2025) → US$ 77,74 bi (2031)", "CAGR 10,35% · Mordor Intelligence"],
            ["Employer Branding", "US$ 1,89 bi (2025) → US$ 3,62 bi (2031)", "CAGR 11,19% · Mordor Intelligence"],
            ["Corporate Wellness", "US$ 66,31 bi (2025) → US$ 94,5 bi (2031)", "CAGR 6,12% · Mordor Intelligence"],
        ],
        "problema_titulo": "El Problema que Resolvemos",
        "problema_col_esq_titulo": "Fallas del Mercado Actual",
        "problema_col_esq": [
            ("Barrera de Idioma", "La gran mayoría de las herramientas de numerología opera solo en inglés, excluyendo miles de millones de hablantes nativos de otros idiomas."),
            ("Precios Desconectados de la Realidad", "Productos cobrados en dólares para mercados emergentes generan exclusión económica — el usuario no rechaza el producto, rechaza el precio inaccesible."),
            ("Falta de Profundidad", "Herramientas genéricas entregan respuestas superficiales sin personalización, sin contexto cultural y sin aplicación práctica al día a día."),
        ],
        "problema_col_dir_titulo": "El Costo de la Exclusión",
        "problema_col_dir": "Cuando una plataforma ignora idioma y poder adquisitivo, abandona voluntariamente el mayor mercado del mundo: los más de 4 mil millones de personas que viven en economías emergentes y hablan idiomas no anglófonos. Ese es el gap que A1ELOS ocupa con precisión quirúrgica.",
        "problema_destaque": "Las plataformas que ignoran el poder adquisitivo local pierden acceso a más del 60% del mercado direccionable global.",
        "solucao_titulo": "Nuestra Solución: 3 Pilares Estratégicos",
        "solucao_texto": "A1ELOS construyó una plataforma integrada que combina ciencia numérica, inteligencia artificial y sensibilidad cultural. La solución opera en tres frentes complementarios, garantizando ingresos diversificados y alta retención.",
        "solucao_colunas": [
            ("Mapas Personales", "Análisis numéricos profundos y personalizados para el usuario final — identidad, misión, ciclos de vida y compatibilidad — entregados en 14 idiomas con IA integrada."),
            ("Numerología Empresarial", "Diagnósticos numerológicos aplicados a marcas, CNPJs, fechas de fundación y estrategia corporativa. Producto diferenciado de alto valor percibido en el mercado B2B."),
            ("White-Label B2B", "Licenciamiento de la plataforma para empresas socias que desean ofrecer numerología bajo su propia marca — con soporte multilingüe y personalización completa."),
        ],
        "alcance_titulo": "Alcance Global: 14 Idiomas · ~5,3 Mil Millones de Hablantes",
        "alcance_texto": "A1ELOS cubre ~67% de la población mundial con una plataforma genuinamente multilingüe. Cada idioma representa un mercado cultural distinto, con precios calibrados al poder adquisitivo local.",
        "mercados_titulo": "Los 3 Nuevos Mercados: +442 Millones de Hablantes",
        "mercados_texto": "La expansión estratégica hacia Indonesia, Turquía y Vietnam representa un salto cualitativo: mercados con alto crecimiento económico, penetración digital creciente y demanda comprobada de soluciones de bienestar digital accesibles.",
        "mercados_cards": [
            ("Indonesia", ["285 mi habitantes", "80,5% penetración de internet", "~255 mi hablantes de indonesio", "Bienestar: US$ 51,2 bi (2025) → US$ 72,8 bi (2034)"]),
            ("Turquía", ["85,9 mi habitantes", "PIB PPP per cápita US$ 37.301", "~90 mi hablantes de turco", "Por encima de la media mundial (US$ 27.211)"]),
            ("Vietnam",  ["~100 mi habitantes", "PIB per cápita ~US$ 5.066 (+7,4%/año)", "~97 mi hablantes de vietnamita", "Bienestar: US$ 303 mi (2025) → US$ 485 mi (2030)"]),
        ],
        "mercados_rodape": "3 mercados nuevos = +442 millones de nuevos hablantes direccionables — incorporados a la plataforma con precios calibrados culturalmente.",
        "preco_titulo": "Filosofía de Precio Consciente",
        "preco_esq": "Respeto cultural + respeto al poder adquisitivo = mercado direccionable real. Misma proporción de valor. Precios diferentes. Dignidad igual para todos los mercados.",
        "preco_dir_titulo": "Cómo Funciona en la Práctica",
        "preco_dir": "A1ELOS aplica la Paridad de Poder de Compra (PPC) como criterio central de precios. El mismo producto entrega el mismo valor relativo al usuario en Lagos, Yakarta, Hanói o Nueva York — el precio se calibra para que el esfuerzo financiero sea proporcional al ingreso local.",
        "preco_pilares": [
            ("Calibración por PPC", "Precios ajustados al índice de poder adquisitivo de cada país"),
            ("Respeto Cultural", "Idioma, moneda y contexto local integrados al producto"),
            ("Conversión Superior", "El precio justo genera más conversión y mayor retención a largo plazo"),
        ],
        "portfolio_titulo": "Portafolio: 24 Productos en 4 Niveles",
        "portfolio_texto": "La estructura en capas garantiza que cada perfil de usuario — del curioso al profesional — encuentre una oferta adecuada a su nivel de engagement y capacidad financiera.",
        "portfolio_tabela": [
           ["Nivel", "Productos", "Rango de Precio (R$)", "Perfil"],
           ["Básico", "Mapa Express, Mapa Completo", "R$ 8 – 17", "Curioso, primer contacto"],
           ["Intermedio", "Búsqueda IA, Nombre de Urna, Nº Electoral", "R$ 26 – 53", "Usuario comprometido"],
           ["Avanzado", "Nombre de ONG, Nombre Artístico, Nombre de Bebé, Firma, Nombre de Negocio", "R$ 35 – 44", "Profesional, emprendedor"],
           ["Premium", "Mapa de Pareja, Mapa Familiar, Compatibilidad de Equipos RH ★, Bono Colectivo", "R$ 98", "Alta renta, uso corporativo"],
           ["B2B", "Paquetes empresariales, licencias, regalos", "Bajo consulta", "Empresas y equipos"],
        ],
        "portfolio_rodape": "24 productos cubren todo el recorrido del usuario, del primer contacto al cliente premium recurrente — maximizando el LTV por idioma y mercado. Destacado: Compatibilidad de Equipos RH (R$ 98) — producto pionero en el mercado de RH corporativo, energía ideal 8.",
        "negocio_titulo": "Modelo de Negocio: 3 Fuentes de Ingresos",
        "negocio_texto": "A1ELOS fue diseñado con ingresos diversificados y escalables: ventas directas al consumidor final a escala global, contratos B2B de alto valor y publicidad geolocalizada recurrente — tres motores que se alimentan mutuamente.",
        "negocio_colunas": [
            ("B2C — 14 Idiomas", "Venta directa de productos digitales en todas las monedas, con precios adaptados por PPC. Escala automática vía IA — sin equipo de atención proporcional al crecimiento."),
            ("B2B — Descuentos Progresivos", "Paquetes corporativos para RH, employer branding y regalos institucionales. Descuentos del 10% al 50% según volumen. Por encima de 2.000 códigos, negociación directa (Plan Diamante). Contratos respaldados por el DUNS 942242668."),
            ("Publicidad Geolocalizada", "Banners segmentados por país, continente o mundial con rotación automatizada. Ingresos recurrentes mensuales de alto valor — sin dependencia del volumen de ventas de producto."),
        ],
        "banners_titulo": "Banners Publicitarios — Ingresos Recurrentes Mensuales",
        "banners_texto": "La plataforma A1ELOS ofrece espacios publicitarios premium con segmentación precisa por geolocalización — país, continente o mundial. Con rotación automática cada 8 segundos y formatos optimizados para desktop y móvil, los banners entregan visibilidad medible a anunciantes regionales e internacionales.",
        "banners_tabela": [
            ["Segmentación", "Fijo (R$/mes)", "Temporal (R$/mes)", "Perfil del Anunciante"],
            ["País", "R$ 800", "R$ 500", "PYMES locales, comercio regional"],
            ["Continente", "R$ 1.800", "R$ 1.200", "Marcas regionales, expansión continental"],
            ["Mundo", "R$ 3.500", "R$ 2.500", "Empresas globales, apps internacionales"],
            ["Patrocinio Exclusivo", "R$ 6.000", "R$ 4.500/campaña", "Patrocinadores master, lanzamientos"],
        ],
        "banners_formatos": "728×90 px — Banner central desktop · 320×100 px — Formato móvil optimizado · 8 segundos — Rotación automática · Geo-target — País, continente o alcance mundial",
        "b2b_titulo": "Paquetes Empresariales B2B — Alto Valor, Alto Volumen",
        "b2b_texto": "Los Paquetes B2B convierten a A1ELOS en una herramienta de employer branding y bienestar corporativo. En el centro de esa estrategia está el producto exclusivo y continuo: la Compatibilidad de Equipos RH (R$ 98). A diferencia de los regalos puntuales, el análisis de compatibilidad es una herramienta de gestión de personas que la empresa incorpora a su día a día — calculando sectores y equipos con la energía deseada y sincronizando a todos los miembros de un sector en la misma sintonía y armonía. Ideal para pequeñas y grandes empresas, es el servicio que el Departamento de Recursos Humanos usa de forma constante, apoyado en mercados en fuerte crecimiento: HR Tech (CAGR 10,35%), Employer Branding (CAGR 11,19%) y Corporate Wellness (CAGR 6,12%).",
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
        "rh_destaque_titulo": "Compatibilidad de Equipos RH — El Producto Exclusivo",
        "rh_destaque_texto": "El análisis de compatibilidad energética entre gestores y colaboradores, y entre miembros de un mismo equipo (energía ideal: número 8 — poder, liderazgo y equilibrio material), posiciona a A1ELOS como pionera en el mercado de RH corporativo. La armonía energética del sector reduce las fricciones interpersonales, alinea posturas y pensamientos, disminuye la rotación (turnover), fortalece el clima organizacional y eleva la productividad — un valor que el Bono Colectivo, como regalo puntual, no entrega. Es el producto que sostiene el crecimiento a corto plazo y los ingresos B2B recurrentes.",
        "projecoes_titulo": "Proyecciones Financieras: Horizonte de 50 Años",
        "projecoes_texto": "Las proyecciones se construyeron con base en estimaciones porcentuales de penetración sobre el mercado potencial de ~5,32 mil millones de hablantes, con conversión conservadora del 3% y canje de bonos entre el 70% y el 90%. Con el 24º producto — Compatibilidad de Equipos RH (R$ 98) y el canal Bono Colectivo/Empresarial —, los ingresos B2B de RH pasan a componer la proyección, anclada en mercados verificados: HR Tech (CAGR 10,35%), Employer Branding (CAGR 11,19%) y Corporate Wellness (CAGR 6,12%). El corto plazo (años 1–5) evidencia el crecimiento acelerado del nuevo frente B2B; el largo plazo refleja la estabilidad continua del modelo hasta la asimilación plena del mercado direccionable.",
        "projecoes_tabela": [
            ["Horizonte", "Conservador (R$)", "Optimista (R$)"],
            ["Año 1", "R$ 318k", "R$ 810k"],
            ["Año 2", "R$ 630k", "R$ 1,8M"],
            ["Año 3", "R$ 1,20M", "R$ 3,50M"],
            ["Año 4", "R$ 2,2M", "R$ 6,2M"],
            ["Año 5", "R$ 3,70M", "R$ 9,6M"],
        ],
        "projecoes_tabela_50": [
            ["Horizonte", "Conservador (R$)", "Optimista (R$)"],
            ["Año 1", "R$ 318k", "R$ 810k"],
            ["Año 3", "R$ 1,20M", "R$ 3,50M"],
            ["Año 5", "R$ 3,70M", "R$ 9,6M"],
            ["Año 7", "R$ 7,8M", "R$ 20,5M"],
            ["Año 10", "R$ 16,3M", "R$ 44,0M"],
            ["Año 20", "R$ 64M", "R$ 184M"],
            ["Año 30", "R$ 133M", "R$ 359M"],
            ["Año 40", "R$ 202M", "R$ 606M"],
            ["Año 50", "R$ 276M", "R$ 869M"],
        ],
        "projecoes_curto_titulo": "Proyecciones Financieras: Corto Plazo (Años 1–5)",
        "projecoes_curto_texto": "El corto plazo evidencia el crecimiento acelerado del nuevo frente B2B de RH (Compatibilidad de Equipos + Bono Colectivo), casi 12x en 5 años en el escenario conservador — antes de la estabilización a largo plazo.",
        "projecoes_curto_tabela": [
            ["Horizonte", "Conservador (R$)", "Optimista (R$)"],
            ["Año 1", "R$ 318k", "R$ 810k"],
            ["Año 2", "R$ 630k", "R$ 1,8M"],
            ["Año 3", "R$ 1,20M", "R$ 3,50M"],
            ["Año 4", "R$ 2,2M", "R$ 6,2M"],
            ["Año 5", "R$ 3,70M", "R$ 9,6M"],
         ],
        "tracao_titulo": "Tracción y Resultados Comprobados",
        "tracao_texto": "A1ELOS ya opera con métricas de producto que validan el modelo — alta retención, evaluación premium y una base creciente de socios B2B demuestran que la plataforma entrega valor real al usuario final y al mercado corporativo.",
        "tracao_kpis": [
            ("12K+", "Usuarios Activos", "Base orgánica en crecimiento consistente"),
            ("87%", "Retención", "Muy por encima de la media de la industria (~30%)"),
            ("4,8★", "Evaluación Media", "Satisfacción comprobada del usuario final"),
            ("23", "Socios B2B", "Contratos activos con empresas y RHs"),
        ],
        "roteiro_titulo": "Hoja de Ruta Estratégica",
        "roteiro_texto": "A1ELOS ejecuta un plan en cuatro fases progresivas — de la consolidación de la base actual al liderazgo global del mercado, con opciones claras de salida para los inversores.",
        "roteiro_fases": [
            ("Fase 1 · Consolidación", "Fortalecimiento de la base de usuarios en los idiomas ya activos. Optimización de conversión, retención y LTV. Ronda Seed concluida."),
            ("Fase 2 · Expansión", "Lanzamiento oficial en los 3 nuevos mercados: Indonesia, Turquía y Vietnam. Aceleración del canal B2B y publicidad geolocalizada."),
            ("Fase 3 · Entrada Global", "Presencia activa en los 14 idiomas con campañas localizadas. Alianzas white-label en 5+ continentes. Serie A."),
            ("Fase 4 · Liderazgo", "20+ países con operaciones consolidadas. Plataforma SaaS de referencia global en numerología aplicada. IPO o salida estratégica."),
        ],
        "invest_titulo": "Inversión y Contacto",
        "invest_texto": "Estamos listos para presentaciones privadas, due diligence y negociaciones. Contacte por el canal de su preferencia.",
        "invest_dados": [
            ("Ronda Seed", "R$ 3,5 millones"),
            ("Valuación Pre-Money", "R$ 14 millones"),
            ("Equity Ofrecido", "Hasta 20%"),
        ],
        "invest_contato": [
            ("Email Inversores", "a1elos.consultoria@gmail.com"),
            ("Email General", "contato@a1elos.com"),
            ("Website", "www.a1elos.com"),
            ("DUNS", "942242668 — Dun & Bradstreet"),
        ],
        "invest_alocacao": "Asignación del Capital: 45% Tecnología · 30% Marketing · 25% Operaciones",
        "frase_final": "Los números nunca mienten.",
        "selo_final": ["DUNS 942242668", "24 PRODUCTOS", "14 IDIOMAS", "~5,3 BI HABLANTES"],
        "graf_cons": "Conservador",
        "graf_otim": "Optimista",
        "grafico_titulo_linha": "Crecimiento Proyectado (R$ mil)",
        "pix_titulo": "Brasil: La Infraestructura Pix",
        "pix_texto": "El Pix es la infraestructura pública de pagos instantáneos de Brasil. Para A1ELOS, garantiza cobro inmediato, bajo costo y aceptación universal — el cimiento de la operación B2C en el mercado brasileño y la puerta de entrada a la expansión internacional.",
        "pix_kpis": [
            ("30,1 bi", "Transacciones en 2025", "+20% vs 2024 · Febraban"),
            ("76,4%", "de la población usa Pix", "211 millones de brasileños · Banco Central"),
            ("R$ 68,2 tri", "movilizados en el 2º sem. 2025", "78,4 bi de transacciones · Banco Central"),
            ("~80 bi", "transacciones en 2025", "+25,7% vs año anterior · Informe del Pix"),
        ],
        "pix_fonte": "Fuentes: Banco Central de Brasil (Pix en Números) y Febraban (Encuesta de Tecnología Bancaria).",
        "ref_titulo": "Referencias Bibliográficas",
        "ref_intro": "Fuentes utilizadas para los datos de mercado, proyecciones e indicadores de esta presentación.",
        "ref_lista": [
            ("Global Wellness Institute", "Economía global del bienestar: US$ 6,8 tri (2024) → US$ 9,8 tri (2029)."),
            ("MarkNtel Advisors", "Apps de astrología y numerología: US$ 3 bi → US$ 9 bi hasta 2030 (CAGR ~20%)."),
            ("FMI · Banco Mundial", "PIB y paridad de poder de compra (PPP) por país."),
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
        "sumario_titulo": "Sommario Esecutivo",
        "duns_porque": "Perché il DUNS è importante?",
        "preco_consciente": "Prezzo Consapevole",
        "idioma_col": "Lingua",
        "falantes_col": "Parlanti (mi)",
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
        "participacao": "Quota",
        "b2c_linha": "B2C — 14 Lingue",
        "b2b_linha": "B2B — Sconti Progressivi",
        "pub_linha": "Pubblicità Geolocalizzata",
        "tabela_descontos": "Tabella degli Sconti Progressivi",
        "grafico_anos": ["Anno 1", "Anno 3", "Anno 5"],
        "grafico_titulo": "Proiezione Conservativa (R$ migliaia)",
        "grafico_titulo_linha": "Crescita Proiettata (R$ migliaia)",
        "fale_conosco": "Contattaci",
        "sumario_intro": "Questa presentazione è strutturata per guidare investitori e partner attraverso tutti gli aspetti strategici di A1ELOS Global Numerology — dalla tesi di mercato al modello di ricavi ricorrenti.",
        "sumario_cards": [
            ("01", "Su A1ELOS", "Holding, portafoglio e credenziale DUNS"),
            ("02", "Opportunità di Mercato", "Economia globale del benessere US$ 6,8 tri"),
            ("03", "Soluzione e Portata Globale", "14 lingue, ~5,3 bi di parlanti"),
            ("04", "Nuovi Mercati", "Indonesia, Turchia, Vietnam e HR Aziendale"),
            ("05", "Portafoglio e Prezzi", "24 prodotti calibrati per potere d'acquisto"),
            ("06", "Ricavi Ricorrenti", "Banner pubblicitari e Pacchetti B2B"),
            ("07", "Proiezioni e Investimento", "Orizzonte di 50 anni · Round Seed R$ 3,5M"),
        ],
        "sobre_titulo": "Su A1ELOS",
        "sobre_texto": "A1ELOS è una holding di tecnologia e conoscenza che unisce intelligenza artificiale, numerologia applicata e strategia culturale per creare prodotti digitali ad alto impatto su scala globale. La nostra missione: democratizzare la conoscenza di sé numerica con rispetto culturale e rispetto per il potere d'acquisto di ogni mercato.",
        "sobre_kpis": [
            ("23", "Prodotti Attivi", "In 4 livelli di accesso"),
            ("14", "Lingue", "~67% della popolazione mondiale"),
            ("5,3B", "Parlanti", "Mercato indirizzabile reale"),
            ("IA", "Integrata", "Motore di personalizzazione"),
        ],
        "sobre_duns": "DUNS 942242668 — Certificazione Dun & Bradstreet valida in oltre 190 paesi, che abilita contratti B2B e joint venture internazionali.",
        "duns_titulo": "Credibilità Internazionale",
        "duns_texto": "Il numero DUNS è il passaporto aziendale di A1ELOS sulla scena internazionale. Segnala a partner, clienti aziendali e investitori che l'azienda possiede identità verificabile, storia tracciabile e capacità contrattuale in qualsiasi giurisdizione.",
        "duns_numero": "942242668",
        "duns_emitido": "Emesso da Dun & Bradstreet — lo standard globale di identità aziendale riconosciuto in oltre 190 paesi.",
        "duns_paises": "190+ PAESI",
        "duns_beneficios": [
            ("Contratti B2B", "Abilitazione per gare e fornitori globali"),
            ("Joint Venture", "Partnership internazionali con due diligence facilitata"),
            ("Credibilità Immediata", "Segnale di serietà per gli investitori istituzionali"),
        ],
        "mercado_titulo": "Opportunità di Mercato",
        "mercado_texto": "Viviamo la convergenza perfetta: il benessere digitale esplode a livello globale mentre la numerologia e l'astrologia migrano verso app ad alto coinvolgimento. A1ELOS è posizionata esattamente in questa intersezione, con il 74% della popolazione mondiale già online (~6 miliardi di persone).",
        "mercado_cards": [
            ("Benessere Globale", "US$ 6,8 tri → US$ 9,8 tri entro il 2029 (+7,6% annuo)"),
            ("App Astrologia/Numerologia", "US$ 3 bi → US$ 9 bi entro il 2030 · CAGR 20%"),
            ("App di Benessere", "CAGR 14,9% → US$ 26,2 bi nel 2030"),
            ("Utenti Online", "74% del mondo · ~6 miliardi di persone"),
        ],
        "mercado_rh_titulo": "Nuovo Mercato: HR Aziendale — il 24º Prodotto",
        "mercado_rh_texto": "Il 24º prodotto — Compatibilità di Squadra HR (R$ 98) — apre il principale mercato B2B di A1ELOS: l'HR aziendale. L'analisi della compatibilità energetica tra manager e collaboratori (energia ideale: numero 8) posiziona la piattaforma come strumento pionieristico di employer branding e benessere aziendale, con sconti progressivi dal 10% al 50% e negoziazione diretta oltre i 2.000 codici (Piano Diamante).",
        "mercado_rh_vantagens": [
            "Armonia energetica del settore → riduzione degli attriti interpersonali e maggiore coesione del team",
            "Allineamento di atteggiamenti e pensieri tra manager e collaboratori → comunicazione più fluida",
            "Minore turnover e maggiore retention dei talenti",
            "Clima organizzativo positivo → guadagno di produttività e benessere",
            "Employer branding rafforzato → attrazione di talenti allineati alla cultura",
        ],
        "mercado_rh_cards": [
            ["HR Tech", "US$ 42,34 bi (2025) → US$ 77,74 bi (2031)", "CAGR 10,35% · Mordor Intelligence"],
            ["Employer Branding", "US$ 1,89 bi (2025) → US$ 3,62 bi (2031)", "CAGR 11,19% · Mordor Intelligence"],
            ["Corporate Wellness", "US$ 66,31 bi (2025) → US$ 94,5 bi (2031)", "CAGR 6,12% · Mordor Intelligence"],
        ],
        "problema_titulo": "Il Problema che Risolviamo",
        "problema_col_esq_titulo": "Fallimenti dell'Attuale Mercato",
        "problema_col_esq": [
            ("Barriera Linguistica", "La stragrande maggioranza degli strumenti di numerologia opera solo in inglese, escludendo miliardi di parlanti nativi di altre lingue."),
            ("Prezzi Scollegati dalla Realtà", "Prodotti venduti in dollari per i mercati emergenti generano esclusione economica — l'utente non rifiuta il prodotto, rifiuta il prezzo inaccessibile."),
            ("Mancanza di Profondità", "Strumenti generici offrono risposte superficiali senza personalizzazione, senza contesto culturale e senza applicazione pratica alla vita quotidiana."),
        ],
        "problema_col_dir_titulo": "Il Costo dell'Esclusione",
        "problema_col_dir": "Quando una piattaforma ignora lingua e potere d'acquisto, abbandona volontariamente il mercato più grande del mondo: i 4+ miliardi di persone che vivono in economie emergenti e parlano lingue non anglofone. Questo è il gap che A1ELOS occupa con precisione chirurgica.",
        "problema_destaque": "Le piattaforme che ignorano il potere d'acquisto locale perdono l'accesso a oltre il 60% del mercato globale indirizzabile.",
        "solucao_titulo": "La Nostra Soluzione: 3 Pilastri Strategici",
        "solucao_texto": "A1ELOS ha costruito una piattaforma integrata che combina scienza numerica, intelligenza artificiale e sensibilità culturale. La soluzione opera su tre fronti complementari, garantendo ricavi diversificati e alta retention.",
        "solucao_colunas": [
            ("Mappe Personali", "Analisi numeriche profonde e personalizzate per l'utente finale — identità, missione, cicli di vita e compatibilità — consegnate in 14 lingue con IA integrata."),
            ("Numerologia Aziendale", "Diagnostica numerologica applicata a marchi, CNPJ, date di fondazione e strategia aziendale. Prodotto differenziato di alto valore percepito nel mercato B2B."),
            ("White-Label B2B", "Licenza della piattaforma per aziende partner che vogliono offrire numerologia sotto il proprio marchio — con supporto multilingue e personalizzazione completa."),
        ],
        "alcance_titulo": "Portata Globale: 14 Lingue · ~5,3 Miliardi di Parlanti",
        "alcance_texto": "A1ELOS copre ~67% della popolazione mondiale con una piattaforma genuinamente multilingue. Ogni lingua rappresenta un mercato culturale distinto, con prezzi calibrati sul potere d'acquisto locale.",
        "mercados_titulo": "I 3 Nuovi Mercati: +442 Milioni di Parlanti",
        "mercados_texto": "L'espansione strategica verso Indonesia, Turchia e Vietnam rappresenta un salto qualitativo: mercati con alta crescita economica, penetrazione digitale crescente e domanda comprovata di soluzioni di benessere digitale accessibili.",
        "mercados_cards": [
            ("Indonesia", ["285 mi abitanti", "80,5% penetrazione internet", "~255 mi parlanti di indonesiano", "Benessere: US$ 51,2 bi (2025) → US$ 72,8 bi (2034)"]),
            ("Turchia", ["85,9 mi abitanti", "PIL PPP pro capite US$ 37.301", "~90 mi parlanti di turco", "Sopra la media mondiale (US$ 27.211)"]),
            ("Vietnam",  ["~100 mi abitanti", "PIL pro capite ~US$ 5.066 (+7,4%/anno)", "~97 mi parlanti di vietnamita", "Benessere: US$ 303 mi (2025) → US$ 485 mi (2030)"]),
        ],
        "mercados_rodape": "3 nuovi mercati = +442 milioni di nuovi parlanti indirizzabili — integrati nella piattaforma con prezzi calibrati culturalmente.",
        "preco_titulo": "Filosofia del Prezzo Consapevole",
        "preco_esq": "Rispetto culturale + rispetto del potere d'acquisto = mercato indirizzabile reale. Stessa proporzione di valore. Prezzi diversi. Dignità uguale per tutti i mercati.",
        "preco_dir_titulo": "Come Funziona in Pratica",
        "preco_dir": "A1ELOS applica la Parità del Potere d'Acquisto (PPA) come criterio centrale di prezzo. Lo stesso prodotto offre lo stesso valore relativo all'utente a Lagos, Jakarta, Hanoi o New York — il prezzo è calibrato affinché lo sforzo finanziario sia proporzionale al reddito locale.",
        "preco_pilares": [
            ("Calibrazione PPA", "Prezzi adeguati all'indice di potere d'acquisto di ogni paese"),
            ("Rispetto Culturale", "Lingua, valuta e contesto locale integrati nel prodotto"),
            ("Conversione Superiore", "Il prezzo giusto genera più conversione e maggiore retention a lungo termine"),
        ],
        "portfolio_titulo": "Portafoglio: 24 Prodotti in 4 Livelli",
        "portfolio_texto": "La struttura a strati garantisce che ogni profilo di utente — dal curioso al professionista — trovi un'offerta adeguata al proprio livello di coinvolgimento e capacità finanziaria.",
        "portfolio_tabela": [
           ["Livello", "Prodotti", "Fascia di Prezzo (R$)", "Profilo"],
           ["Base", "Mappa Express, Mappa Completa", "R$ 8 – 17", "Curioso, primo contatto"],
           ["Intermedio", "Ricerca IA, Nome di Urna, Nº Elettorale", "R$ 26 – 53", "Utente coinvolto"],
           ["Avanzato", "Nome di ONG, Nome Artistico, Nome di Bambino, Firma, Nome di Impresa", "R$ 35 – 44", "Professionista, imprenditore"],
           ["Premium", "Mappa di Coppia, Mappa Familiare, Compatibilità di Squadra HR ★, Bonus Collettivo", "R$ 98", "Alto reddito, uso aziendale"],
           ["B2B", "Pacchetti aziendali, licenze, regali", "Su richiesta", "Aziende e team"],
        ],
        "portfolio_rodape": "24 prodotti coprono l'intero percorso dell'utente, dal primo contatto al cliente premium ricorrente — massimizzando il LTV per lingua e mercato. In evidenza: Compatibilità di Squadra HR (R$ 98) — prodotto pionieristico nel mercato HR aziendale, energia ideale 8.",
        "negocio_titulo": "Modello di Business: 3 Fonti di Ricavo",
        "negocio_texto": "A1ELOS è stata progettata con ricavi diversificati e scalabili: vendite dirette al consumatore finale su scala globale, contratti B2B di alto valore e pubblicità geolocalizzata ricorrente — tre motori che si alimentano a vicenda.",
        "negocio_colunas": [
            ("B2C — 14 Lingue", "Vendita diretta di prodotti digitali in tutte le valute, con prezzi adattati per PPA. Scala automatica via IA — senza team di assistenza proporzionale alla crescita."),
            ("B2B — Sconti Progressivi", "Pacchetti aziendali per HR, employer branding e regali istituzionali. Sconti dal 10% al 50% in base al volume. Oltre 2.000 codici, negoziazione diretta (Piano Diamante). Contratti supportati dal DUNS 942242668."),
            ("Pubblicità Geolocalizzata", "Banner segmentati per paese, continente o mondiale con rotazione automatizzata. Ricavi mensili ricorrenti di alto valore — senza dipendenza dal volume di vendita dei prodotti."),
        ],
        "banners_titulo": "Banner Pubblicitari — Ricavi Mensili Ricorrenti",
        "banners_texto": "La piattaforma A1ELOS offre spazi pubblicitari premium con segmentazione precisa per geolocalizzazione — paese, continente o mondiale. Con rotazione automatica ogni 8 secondi e formati ottimizzati per desktop e mobile, i banner offrono visibilità misurabile ad inserzionisti regionali e internazionali.",
        "banners_tabela": [
            ["Segmentazione", "Fisso (R$/mese)", "Temporaneo (R$/mese)", "Profilo Inserzionista"],
            ["Paese", "R$ 800", "R$ 500", "PMI locali, commercio regionale"],
            ["Continente", "R$ 1.800", "R$ 1.200", "Marchi regionali, espansione continentale"],
            ["Mondo", "R$ 3.500", "R$ 2.500", "Aziende globali, app internazionali"],
            ["Sponsorizzazione Esclusiva", "R$ 6.000", "R$ 4.500/campagna", "Sponsor master, lanci"],
        ],
        "banners_formatos": "728×90 px — Banner centrale desktop · 320×100 px — Formato mobile ottimizzato · 8 secondi — Rotazione automatica · Geo-target — Paese, continente o portata mondiale",
        "b2b_titulo": "Pacchetti Aziendali B2B — Alto Valore, Alto Volume",
        "b2b_texto": "I Pacchetti B2B trasformano A1ELOS in uno strumento di employer branding e benessere aziendale. Al centro di questa strategia c'è il prodotto esclusivo e continuo: la Compatibilità di Squadra HR (R$ 98). A differenza dei regali puntuali, l'analisi di compatibilità è uno strumento di gestione delle persone che l'azienda incorpora nella sua routine quotidiana — calcolando settori e team con l'energia desiderata e sincronizzando tutti i membri di un settore nella stessa sintonia e armonia. Ideale per piccole e grandi aziende, è il servizio che il Dipartimento Risorse Umane usa costantemente, supportato da mercati in forte crescita: HR Tech (CAGR 10,35%), Employer Branding (CAGR 11,19%) e Corporate Wellness (CAGR 6,12%).",
        "b2b_planos": [
            ("Piano Base · 50 codici", "50× Mappa Express (R$ 8 ciascuna). Ideale per programmi di benefit ai dipendenti e azioni di integrazione."),
            ("Piano Intermedio · 100 codici", "50× Mappa Express + 50× Ricerca IA (R$ 17). Perfetto per team e strategia di employer branding."),
            ("Piano Premium · 200 codici", "100× Mappa Express + 100× Mappa Completa (R$ 17). Massima profondità analitica per grandi gruppi."),
        ],
        "b2b_tabela": [
            ["A partire da", "Sconto", "Profilo", "Uso Raccomandato"],
            ["10 codici", "10%", "Piccoli team", "Azione puntuale di benessere"],
            ["50 codici", "20%", "Team in crescita", "Programmi ricorrenti"],
            ["100 codici", "25%", "PMI", "Benefit trimestrale"],
            ["200 codici", "30%", "Aziende medie", "Programmi completi"],
            ["500 codici", "40%", "Aziende medie", "Regalo annuale ai dipendenti"],
            ["1.000 codici", "45%", "Grandi aziende", "Fidelizzazione clienti"],
            ["2.000 codici", "50%", "Grandi gruppi", "Larga scala"],
            ["Oltre 2.000", "Negoziabile", "Piano Diamante su misura", "Distribuzione bonus in volume"],
        ],
        "rh_destaque_titulo": "Compatibilità di Squadra HR — Il Prodotto Esclusivo",
        "rh_destaque_texto": "L'analisi della compatibilità energetica tra manager e collaboratori, e tra i membri dello stesso team (energia ideale: numero 8 — potere, leadership ed equilibrio materiale), posiziona A1ELOS come pioniera nel mercato HR aziendale. L'armonia energetica del settore riduce gli attriti interpersonali, allinea atteggiamenti e pensieri, diminuisce il turnover, rafforza il clima organizzativo e aumenta la produttività — un valore che il Bonus Collettivo, come regalo puntuale, non offre. È il prodotto che sostiene la crescita a breve termine e i ricavi B2B ricorrenti.",
        "projecoes_titulo": "Proiezioni Finanziarie: Orizzonte di 50 Anni",
        "projecoes_texto": "Le proiezioni sono state costruite su stime percentuali di penetrazione sul mercato potenziale di ~5,32 miliardi di parlanti, con conversione conservativa del 3% e riscatto dei bonus tra il 70% e il 90%. Con il 24º prodotto — Compatibilità di Squadra HR (R$ 98) e il canale Bonus Collettivo/Aziendale —, i ricavi B2B HR entrano a far parte della proiezione, ancorata a mercati verificati: HR Tech (CAGR 10,35%), Employer Branding (CAGR 11,19%) e Corporate Wellness (CAGR 6,12%). Il breve termine (anni 1–5) evidenzia la crescita accelerata del nuovo fronte B2B; il lungo termine riflette la stabilità continua del modello fino alla piena assimilazione del mercato indirizzabile.",
        "projecoes_tabela": [
            ["Orizzonte", "Conservativo (R$)", "Ottimista (R$)"],
            ["Anno 1", "R$ 318k", "R$ 810k"],
            ["Anno 2", "R$ 630k", "R$ 1,8M"],
            ["Anno 3", "R$ 1,20M", "R$ 3,50M"],
            ["Anno 4", "R$ 2,2M", "R$ 6,2M"],
            ["Anno 5", "R$ 3,70M", "R$ 9,6M"],
        ],
        "projecoes_tabela_50": [
            ["Orizzonte", "Conservativo (R$)", "Ottimista (R$)"],
            ["Anno 1", "R$ 318k", "R$ 810k"],
            ["Anno 3", "R$ 1,20M", "R$ 3,50M"],
            ["Anno 5", "R$ 3,70M", "R$ 9,6M"],
            ["Anno 7", "R$ 7,8M", "R$ 20,5M"],
            ["Anno 10", "R$ 16,3M", "R$ 44,0M"],
            ["Anno 20", "R$ 64M", "R$ 184M"],
            ["Anno 30", "R$ 133M", "R$ 359M"],
            ["Anno 40", "R$ 202M", "R$ 606M"],
            ["Anno 50", "R$ 276M", "R$ 869M"],
        ],
        "projecoes_curto_titulo": "Proiezioni Finanziarie: Breve Termine (Anni 1–5)",
        "projecoes_curto_texto": "Il breve termine evidenzia la crescita accelerata del nuovo fronte B2B HR (Compatibilità di Squadra + Bonus Collettivo), quasi 12x in 5 anni nello scenario conservativo — prima della stabilizzazione a lungo termine.",
        "projecoes_curto_tabela": [
            ["Orizzonte", "Conservativo (R$)", "Ottimista (R$)"],
            ["Anno 1", "R$ 318k", "R$ 810k"],
            ["Anno 2", "R$ 630k", "R$ 1,8M"],
            ["Anno 3", "R$ 1,20M", "R$ 3,50M"],
            ["Anno 4", "R$ 2,2M", "R$ 6,2M"],
            ["Anno 5", "R$ 3,70M", "R$ 9,6M"],
         ],
        "tracao_titulo": "Trazione e Risultati Comprovati",
        "tracao_texto": "A1ELOS opera già con metriche di prodotto che validano il modello — alta retention, valutazione premium e una base crescente di partner B2B dimostrano che la piattaforma offre valore reale all'utente finale e al mercato aziendale.",
        "tracao_kpis": [
            ("12K+", "Utenti Attivi", "Base organica in crescita costante"),
            ("87%", "Retention", "Molto sopra la media del settore (~30%)"),
            ("4,8★", "Valutazione Media", "Soddisfazione comprovata dell'utente finale"),
            ("23", "Partner B2B", "Contratti attivi con aziende e HR"),
        ],
        "roteiro_titulo": "Roadmap Strategica",
        "roteiro_texto": "A1ELOS esegue un piano in quattro fasi progressive — dal consolidamento della base attuale alla leadership globale del mercato, con chiare opzioni di uscita per gli investitori.",
        "roteiro_fases": [
            ("Fase 1 · Consolidamento", "Rafforzamento della base utenti nelle lingue già attive. Ottimizzazione di conversione, retention e LTV. Round Seed concluso."),
            ("Fase 2 · Espansione", "Lancio ufficiale nei 3 nuovi mercati: Indonesia, Turchia e Vietnam. Accelerazione del canale B2B e pubblicità geolocalizzata."),
            ("Fase 3 · Ingresso Globale", "Presenza attiva in tutte le 14 lingue con campagne localizzate. Partnership white-label in 5+ continenti. Serie A."),
            ("Fase 4 · Leadership", "20+ paesi con operazioni consolidate. Piattaforma SaaS di riferimento globale in numerologia applicata. IPO o uscita strategica."),
        ],
        "invest_titulo": "Investimento e Contatto",
        "invest_texto": "Siamo pronti per presentazioni private, due diligence e negoziazioni. Contattaci tramite il canale preferito.",
        "invest_dados": [
            ("Round Seed", "R$ 3,5 milioni"),
            ("Valuazione Pre-Money", "R$ 14 milioni"),
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
        "selo_final": ["DUNS 942242668", "24 PRODOTTI", "14 LINGUE", "~5,3 BI PARLANTI"],
        "graf_cons": "Conservativo",
        "graf_otim": "Ottimista",
        "grafico_titulo_linha": "Crescita Proiettata (R$ migliaia)",
        "pix_titulo": "Brasile: L'Infrastruttura Pix",
        "pix_texto": "Il Pix è l'infrastruttura pubblica di pagamenti istantanei del Brasile. Per A1ELOS, garantisce incasso immediato, basso costo e accettazione universale — il fondamento dell'operazione B2C nel mercato brasiliano e la porta d'ingresso all'espansione internazionale.",
        "pix_kpis": [
            ("30,1 bi", "Transazioni nel 2025", "+20% vs 2024 · Febraban"),
            ("76,4%", "della popolazione usa Pix", "211 milioni di brasiliani · Banca Centrale"),
            ("R$ 68,2 tri", "movimentati nel 2º sem. 2025", "78,4 bi di transazioni · Banca Centrale"),
            ("~80 bi", "transazioni nel 2025", "+25,7% vs anno precedente · Rapporto Pix"),
        ],
        "pix_fonte": "Fonti: Banca Centrale del Brasile (Pix in Numeri) e Febraban (Indagine sulla Tecnologia Bancaria).",
        "ref_titulo": "Riferimenti Bibliografici",
        "ref_intro": "Fonti utilizzate per i dati di mercato, le proiezioni e gli indicatori di questa presentazione.",
        "ref_lista": [
            ("Global Wellness Institute", "Economia globale del benessere: US$ 6,8 tri (2024) → US$ 9,8 tri (2029)."),
            ("MarkNtel Advisors", "App di astrologia e numerologia: US$ 3 bi → US$ 9 bi entro il 2030 (CAGR ~20%)."),
            ("FMI · Banca Mondiale", "PIL e parità del potere d'acquisto (PPP) per paese."),
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
        "falantes_col": "Locuteurs (mi)",
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
        "participacao": "Part",
        "b2c_linha": "B2C — 14 Langues",
        "b2b_linha": "B2B — Remises Progressives",
        "pub_linha": "Publicité Géolocalisée",
        "tabela_descontos": "Tableau des Remises Progressives",
        "grafico_anos": ["Année 1", "Année 3", "Année 5"],
        "grafico_titulo": "Projection Conservatrice (R$ milliers)",
        "grafico_titulo_linha": "Croissance Projetée (R$ milliers)",
        "fale_conosco": "Contactez-Nous",
        "sumario_intro": "Cette présentation est structurée pour guider les investisseurs et partenaires à travers tous les aspects stratégiques d'A1ELOS Global Numerology — de la thèse de marché au modèle de revenus récurrents.",
        "sumario_cards": [
            ("01", "À propos d'A1ELOS", "Holding, portefeuille et crédential DUNS"),
            ("02", "Opportunité de Marché", "Économie mondiale du bien-être US$ 6,8 billions"),
            ("03", "Solution et Portée Mondiale", "14 langues, ~5,3 Mds de locuteurs"),
            ("04", "Nouveaux Marchés", "Indonésie, Turquie, Vietnam et RH d'Entreprise"),
            ("05", "Portefeuille et Prix", "24 produits calibrés par pouvoir d'achat"),
            ("06", "Revenus Récurrents", "Bannières publicitaires et Packs B2B"),
            ("07", "Projections et Investissement", "Horizon de 50 ans · Tour Seed R$ 3,5M"),
        ],
        "sobre_titulo": "À propos d'A1ELOS",
        "sobre_texto": "A1ELOS est un holding de technologie et de connaissance qui unit intelligence artificielle, numérologie appliquée et stratégie culturelle pour créer des produits numériques à fort impact à l'échelle mondiale. Notre mission : démocratiser la connaissance de soi numérique avec respect culturel et respect du pouvoir d'achat de chaque marché.",
        "sobre_kpis": [
            ("23", "Produits Actifs", "Sur 4 niveaux d'accès"),
            ("14", "Langues", "~67 % de la population mondiale"),
            ("5,3Mds", "Locuteurs", "Marché adressable réel"),
            ("IA", "Intégrée", "Moteur de personnalisation"),
        ],
        "sobre_duns": "DUNS 942242668 — Certification Dun & Bradstreet valable dans plus de 190 pays, habilitant les contrats B2B et les joint-ventures internationales.",
        "duns_titulo": "Crédibilité Internationale",
        "duns_texto": "Le numéro DUNS est le passeport corporatif d'A1ELOS sur la scène internationale. Il signale aux partenaires, clients professionnels et investisseurs que l'entreprise possède une identité vérifiable, un historique traçable et une capacité contractuelle dans toute juridiction.",
        "duns_numero": "942242668",
        "duns_emitido": "Émis par Dun & Bradstreet — la norme mondiale d'identité d'entreprise reconnue dans plus de 190 pays.",
        "duns_paises": "190+ PAYS",
        "duns_beneficios": [
            ("Contrats B2B", "Habilitation aux appels d'offres et fournisseurs mondiaux"),
            ("Joint-Ventures", "Partenariats internationaux avec due diligence facilitée"),
            ("Crédibilité Immédiate", "Signe de sérieux pour les investisseurs institutionnels"),
        ],
        "mercado_titulo": "Opportunité de Marché",
        "mercado_texto": "Nous vivons la convergence parfaite : le bien-être numérique explose au niveau mondial tandis que la numérologie et l'astrologie migrent vers des apps à fort engagement. A1ELOS est positionnée exactement à cette intersection, avec 74 % de la population mondiale déjà en ligne (~6 milliards de personnes).",
        "mercado_cards": [
            ("Bien-Être Mondial", "US$ 6,8 billions → US$ 9,8 billions d'ici 2029 (+7,6 %/an)"),
            ("Apps Astrologie/Numérologie", "US$ 3 milliards → US$ 9 milliards d'ici 2030 · TCAC 20 %"),
            ("Apps de Bien-Être", "TCAC 14,9 % → US$ 26,2 milliards en 2030"),
            ("Utilisateurs en Ligne", "74 % du monde · ~6 milliards de personnes"),
        ],
        "mercado_rh_titulo": "Nouveau Marché : RH d'Entreprise — le 24e Produit",
        "mercado_rh_texto": "Le 24e produit — Compatibilité d'Équipes RH (R$ 98) — ouvre le principal marché B2B d'A1ELOS : les RH d'entreprise. L'analyse de compatibilité énergétique entre managers et collaborateurs (énergie idéale : numéro 8) positionne la plateforme comme outil pionnier d'employer branding et de bien-être au travail, avec des remises progressives de 10 % à 50 % et négociation directe au-delà de 2.000 codes (Plan Diamant).",
        "mercado_rh_vantagens": [
            "Harmonie énergétique du secteur → réduction des frictions interpersonnelles et cohésion d'équipe accrue",
            "Alignement des postures et des pensées entre managers et collaborateurs → communication plus fluide",
            "Rotation (turnover) réduite et meilleure rétention des talents",
            "Climat organisationnel positif → gain de productivité et de bien-être",
            "Employer branding renforcé → attraction de talents alignés sur la culture",
        ],
        "mercado_rh_cards": [
            ["HR Tech", "US$ 42,34 Mds (2025) → US$ 77,74 Mds (2031)", "TCAC 10,35 % · Mordor Intelligence"],
            ["Employer Branding", "US$ 1,89 Md (2025) → US$ 3,62 Mds (2031)", "TCAC 11,19 % · Mordor Intelligence"],
            ["Corporate Wellness", "US$ 66,31 Mds (2025) → US$ 94,5 Mds (2031)", "TCAC 6,12 % · Mordor Intelligence"],
        ],
        "problema_titulo": "Le Problème que Nous Résolvons",
        "problema_col_esq_titulo": "Défaillances du Marché Actuel",
        "problema_col_esq": [
            ("Barrière de la Langue", "La grande majorité des outils de numérologie fonctionne uniquement en anglais, excluant des milliards de locuteurs natifs d'autres langues."),
            ("Prix Déconnectés de la Réalité", "Des produits facturés en dollars pour les marchés émergents créent une exclusion économique — l'utilisateur ne rejette pas le produit, il rejette le prix inaccessible."),
            ("Manque de Profondeur", "Les outils génériques offrent des réponses superficielles sans personnalisation, sans contexte culturel et sans application pratique au quotidien."),
        ],
        "problema_col_dir_titulo": "Le Coût de l'Exclusion",
        "problema_col_dir": "Lorsqu'une plateforme ignore la langue et le pouvoir d'achat, elle abandonne volontairement le plus grand marché du monde : les 4+ milliards de personnes vivant dans des économies émergentes et parlant des langues non anglophones. C'est l'espace qu'A1ELOS occupe avec une précision chirurgicale.",
        "problema_destaque": "Les plateformes qui ignorent le pouvoir d'achat local perdent l'accès à plus de 60 % du marché mondial adressable.",
        "solucao_titulo": "Notre Solution : 3 Piliers Stratégiques",
        "solucao_texto": "A1ELOS a construit une plateforme intégrée qui allie science des nombres, intelligence artificielle et sensibilité culturelle. La solution opère sur trois fronts complémentaires, garantissant des revenus diversifiés et une rétention élevée.",
        "solucao_colunas": [
            ("Cartes Personnelles", "Analyses numériques profondes et personnalisées pour l'utilisateur final — identité, mission, cycles de vie et compatibilité — livrées en 14 langues avec IA intégrée."),
            ("Numérologie d'Entreprise", "Diagnostics numérologiques appliqués aux marques, CNPJ, dates de fondation et stratégie d'entreprise. Produit différencié à forte valeur perçue sur le marché B2B."),
            ("White-Label B2B", "Licence de la plateforme pour les entreprises partenaires qui souhaitent offrir la numérologie sous leur propre marque — avec support multilingue et personnalisation complète."),
        ],
        "alcance_titulo": "Portée Mondiale : 14 Langues · ~5,3 Milliards de Locuteurs",
        "alcance_texto": "A1ELOS couvre ~67 % de la population mondiale avec une plateforme véritablement multilingue. Chaque langue représente un marché culturel distinct, avec des prix calibrés sur le pouvoir d'achat local.",
        "mercados_titulo": "Les 3 Nouveaux Marchés : +442 Millions de Locuteurs",
        "mercados_texto": "L'expansion stratégique vers l'Indonésie, la Turquie et le Vietnam représente un saut qualitatif : des marchés à forte croissance économique, à pénétration numérique croissante et à demande avérée de solutions de bien-être numérique accessibles.",
        "mercados_cards": [
            ("Indonésie", ["285 M d'habitants", "80,5 % de pénétration internet", "~255 M de locuteurs indonésiens", "Bien-être : US$ 51,2 Mds (2025) → US$ 72,8 Mds (2034)"]),
            ("Turquie", ["85,9 M d'habitants", "PIB PPP par habitant US$ 37.301", "~90 M de locuteurs turcs", "Au-dessus de la moyenne mondiale (US$ 27.211)"]),
            ("Vietnam",  ["~100 M d'habitants", "PIB par habitant ~US$ 5.066 (+7,4 %/an)", "~97 M de locuteurs vietnamiens", "Bien-être : US$ 303 M (2025) → US$ 485 M (2030)"]),
        ],
        "mercados_rodape": "3 nouveaux marchés = +442 millions de nouveaux locuteurs adressables — intégrés à la plateforme avec une tarification calibrée culturellement.",
        "preco_titulo": "Philosophie du Prix Conscient",
        "preco_esq": "Respect culturel + respect du pouvoir d'achat = marché adressable réel. Même proportion de valeur. Prix différents. Dignité égale pour tous les marchés.",
        "preco_dir_titulo": "Comment ça Marche en Pratique",
        "preco_dir": "A1ELOS applique la Parité de Pouvoir d'Achat (PPA) comme critère central de tarification. Le même produit apporte la même valeur relative à l'utilisateur à Lagos, Jakarta, Hanoï ou New York — le prix est calibré pour que l'effort financier soit proportionnel au revenu local.",
        "preco_pilares": [
            ("Calibrage PPA", "Prix ajustés à l'indice de pouvoir d'achat de chaque pays"),
            ("Respect Culturel", "Langue, monnaie et contexte local intégrés au produit"),
            ("Conversion Supérieure", "Un prix juste génère plus de conversions et une meilleure rétention à long terme"),
        ],
        "portfolio_titulo": "Portefeuille : 24 Produits en 4 Niveaux",
        "portfolio_texto": "La structure en couches garantit que chaque profil d'utilisateur — du curieux au professionnel — trouve une offre adaptée à son niveau d'engagement et à sa capacité financière.",
        "portfolio_tabela": [
           ["Niveau", "Produits", "Fourchette de Prix (R$)", "Profil"],
           ["Basique", "Carte Express, Carte Complète", "R$ 8 – 17", "Curieux, premier contact"],
           ["Intermédiaire", "Recherche IA, Nom d'Urne, Nº Électoral", "R$ 26 – 53", "Utilisateur engagé"],
           ["Avancé", "Nom d'ONG, Nom Artistique, Nom de Bébé, Signature, Nom d'Entreprise", "R$ 35 – 44", "Professionnel, entrepreneur"],
           ["Premium", "Carte de Couple, Carte de Famille, Compatibilité d'Équipes RH ★, Bonus Collectif", "R$ 98", "Hauts revenus, usage professionnel"],
           ["B2B", "Packs Entreprises, licences, cadeaux", "Sur demande", "Entreprises et équipes"],
        ],
        "portfolio_rodape": "24 produits couvrent tout le parcours de l'utilisateur, du premier contact au client premium récurrent — maximisant le LTV par langue et par marché. En vedette : Compatibilité d'Équipes RH (R$ 98) — produit pionnier du marché RH d'entreprise, énergie idéale 8.",
        "negocio_titulo": "Modèle d'Affaires : 3 Sources de Revenus",
        "negocio_texto": "A1ELOS a été conçue avec des revenus diversifiés et évolutifs : ventes directes au consommateur final à l'échelle mondiale, contrats B2B à forte valeur et publicité géolocalisée récurrente — trois moteurs qui s'alimentent mutuellement.",
        "negocio_colunas": [
            ("B2C — 14 Langues", "Vente directe de produits numériques dans toutes les devises, avec des prix adaptés par PPA. Échelle automatique via l'IA — sans équipe de support proportionnelle à la croissance."),
            ("B2B — Remises Progressives", "Packs d'entreprise pour les RH, l'employer branding et les cadeaux institutionnels. Remises de 10 % à 50 % selon le volume. Au-delà de 2.000 codes, négociation directe (Plan Diamant). Contrats soutenus par le DUNS 942242668."),
            ("Publicité Géolocalisée", "Bannières segmentées par pays, continent ou monde avec rotation automatisée. Revenus mensuels récurrents à forte valeur — sans dépendance au volume de ventes de produits."),
        ],
        "banners_titulo": "Bannières Publicitaires — Revenus Mensuels Récurrents",
        "banners_texto": "La plateforme A1ELOS offre des espaces publicitaires premium avec une segmentation précise par géolocalisation — pays, continent ou monde. Avec une rotation automatique toutes les 8 secondes et des formats optimisés pour desktop et mobile, les bannières offrent une visibilité mesurable aux annonceurs régionaux et internationaux.",
        "banners_tabela": [
            ["Segmentation", "Fixe (R$/mois)", "Temporaire (R$/mois)", "Profil de l'Annonceur"],
            ["Pays", "R$ 800", "R$ 500", "PME locales, commerce régional"],
            ["Continent", "R$ 1.800", "R$ 1.200", "Marques régionales, expansion continentale"],
            ["Monde", "R$ 3.500", "R$ 2.500", "Entreprises mondiales, apps internationales"],
            ["Parrainage Exclusif", "R$ 6.000", "R$ 4.500/campagne", "Sponsors master, lancements"],
        ],
        "banners_formatos": "728×90 px — Bannière centrale desktop · 320×100 px — Format mobile optimisé · 8 secondes — Rotation automatique · Geo-ciblage — Pays, continent ou portée mondiale",
        "b2b_titulo": "Packs Entreprises B2B — Haute Valeur, Grand Volume",
        "b2b_texto": "Les Packs B2B transforment A1ELOS en outil d'employer branding et de bien-être au travail. Au cœur de cette stratégie se trouve le produit exclusif et continu : la Compatibilité d'Équipes RH (R$ 98). Contrairement aux cadeaux ponctuels, l'analyse de compatibilité est un outil de gestion des personnes que l'entreprise intègre à son quotidien — calculant secteurs et équipes avec l'énergie souhaitée et synchronisant tous les membres d'un secteur dans la même tonalité et harmonie. Idéal pour les petites et grandes entreprises, c'est le service que le Département des Ressources Humaines utilise en permanence, soutenu par des marchés en forte croissance : HR Tech (TCAC 10,35 %), Employer Branding (TCAC 11,19 %) et Corporate Wellness (TCAC 6,12 %).",
        "b2b_planos": [
            ("Plan Basique · 50 codes", "50× Carte Express (R$ 8 chacune). Idéal pour les programmes d'avantages employés et les actions d'intégration."),
            ("Plan Intermédiaire · 100 codes", "50× Carte Express + 50× Recherche IA (R$ 17). Parfait pour les équipes et la stratégie d'employer branding."),
            ("Plan Premium · 200 codes", "100× Carte Express + 100× Carte Complète (R$ 17). Profondeur analytique maximale pour les grands groupes."),
        ],
        "b2b_tabela": [
            ["À partir de", "Remise", "Profil", "Utilisation Recommandée"],
            ["10 codes", "10 %", "Petites équipes", "Action ponctuelle de bien-être"],
            ["50 codes", "20 %", "Équipes en croissance", "Programmes récurrents"],
            ["100 codes", "25 %", "PME", "Avantage trimestriel"],
            ["200 codes", "30 %", "Entreprises moyennes", "Programmes complets"],
            ["500 codes", "40 %", "Entreprises moyennes", "Cadeau annuel aux employés"],
            ["1.000 codes", "45 %", "Grandes entreprises", "Fidélisation des clients"],
            ["2.000 codes", "50 %", "Grands groupes", "Grande échelle"],
            ["Plus de 2.000", "Négociable", "Plan Diamant sur mesure", "Distribution de bonus en volume"],
        ],
        "rh_destaque_titulo": "Compatibilité d'Équipes RH — Le Produit Exclusif",
        "rh_destaque_texto": "L'analyse de compatibilité énergétique entre managers et collaborateurs, et entre membres d'une même équipe (énergie idéale : numéro 8 — pouvoir, leadership et équilibre matériel), positionne A1ELOS comme pionnière du marché RH d'entreprise. L'harmonie énergétique du secteur réduit les frictions interpersonnelles, aligne postures et pensées, diminue la rotation (turnover), renforce le climat organisationnel et élève la productivité — une valeur que le Bonus Collectif, en tant que cadeau ponctuel, n'apporte pas. C'est le produit qui soutient la croissance à court terme et les revenus B2B récurrents.",
        "projecoes_titulo": "Projections Financières : Horizon de 50 Ans",
        "projecoes_texto": "Les projections ont été construites sur des estimations de pénétration en pourcentage du marché potentiel de ~5,32 milliards de locuteurs, avec une conversion conservatrice de 3 % et un échange de bonus entre 70 % et 90 %. Avec le 24e produit — Compatibilité d'Équipes RH (R$ 98) et le canal Bonus Collectif/Entreprise —, les revenus B2B RH intègrent la projection, ancrée sur des marchés vérifiés : HR Tech (TCAC 10,35 %), Employer Branding (TCAC 11,19 %) et Corporate Wellness (TCAC 6,12 %). Le court terme (années 1–5) met en évidence la croissance accélérée du nouveau front B2B ; le long terme reflète la stabilité continue du modèle jusqu'à l'assimilation complète du marché adressable.",
        "projecoes_tabela": [
            ["Horizon", "Conservateur (R$)", "Optimiste (R$)"],
            ["Année 1", "R$ 318k", "R$ 810k"],
            ["Année 2", "R$ 630k", "R$ 1,8M"],
            ["Année 3", "R$ 1,20M", "R$ 3,50M"],
            ["Année 4", "R$ 2,2M", "R$ 6,2M"],
            ["Année 5", "R$ 3,70M", "R$ 9,6M"],
        ],
        "projecoes_tabela_50": [
            ["Horizon", "Conservateur (R$)", "Optimiste (R$)"],
            ["Année 1", "R$ 318k", "R$ 810k"],
            ["Année 3", "R$ 1,20M", "R$ 3,50M"],
            ["Année 5", "R$ 3,70M", "R$ 9,6M"],
            ["Année 7", "R$ 7,8M", "R$ 20,5M"],
            ["Année 10", "R$ 16,3M", "R$ 44,0M"],
            ["Année 20", "R$ 64M", "R$ 184M"],
            ["Année 30", "R$ 133M", "R$ 359M"],
            ["Année 40", "R$ 202M", "R$ 606M"],
            ["Année 50", "R$ 276M", "R$ 869M"],
        ],
        "projecoes_curto_titulo": "Projections Financières : Court Terme (Années 1–5)",
        "projecoes_curto_texto": "Le court terme met en évidence la croissance accélérée du nouveau front B2B RH (Compatibilité d'Équipes + Bonus Collectif), près de 12× en 5 ans dans le scénario conservateur — avant la stabilisation à long terme.",
        "projecoes_curto_tabela": [
            ["Horizon", "Conservateur (R$)", "Optimiste (R$)"],
            ["Année 1", "R$ 318k", "R$ 810k"],
            ["Année 2", "R$ 630k", "R$ 1,8M"],
            ["Année 3", "R$ 1,20M", "R$ 3,50M"],
            ["Année 4", "R$ 2,2M", "R$ 6,2M"],
            ["Année 5", "R$ 3,70M", "R$ 9,6M"],
         ],
        "tracao_titulo": "Traction et Résultats Prouvés",
        "tracao_texto": "A1ELOS opère déjà avec des métriques produit qui valident le modèle — rétention élevée, notation premium et une base croissante de partenaires B2B démontrent que la plateforme apporte une valeur réelle à l'utilisateur final et au marché professionnel.",
        "tracao_kpis": [
            ("12K+", "Utilisateurs Actifs", "Base organique en croissance constante"),
            ("87 %", "Rétention", "Bien au-dessus de la moyenne du secteur (~30 %)"),
            ("4,8★", "Note Moyenne", "Satisfaction prouvée de l'utilisateur final"),
            ("23", "Partenaires B2B", "Contrats actifs avec entreprises et RH"),
        ],
        "roteiro_titulo": "Feuille de Route Stratégique",
        "roteiro_texto": "A1ELOS exécute un plan en quatre phases progressives — de la consolidation de la base actuelle au leadership mondial du marché, avec des options de sortie claires pour les investisseurs.",
        "roteiro_fases": [
            ("Phase 1 · Consolidation", "Renforcement de la base d'utilisateurs dans les langues déjà actives. Optimisation de la conversion, de la rétention et du LTV. Tour de table Seed conclu."),
            ("Phase 2 · Expansion", "Lancement officiel sur les 3 nouveaux marchés : Indonésie, Turquie et Vietnam. Accélération du canal B2B et publicité géolocalisée."),
            ("Phase 3 · Entrée Mondiale", "Présence active dans les 14 langues avec des campagnes localisées. Partenariats white-label sur 5+ continents. Série A."),
            ("Phase 4 · Leadership", "20+ pays avec des opérations consolidées. Plateforme SaaS de référence mondiale en numérologie appliquée. IPO ou sortie stratégique."),
        ],
        "invest_titulo": "Investissement et Contact",
        "invest_texto": "Nous sommes prêts pour les présentations privées, la due diligence et les négociations. Contactez-nous par le canal de votre choix.",
        "invest_dados": [
            ("Tour de table Seed", "R$ 3,5 millions"),
            ("Valorisation Pré-Money", "R$ 14 millions"),
            ("Equity Offert", "Jusqu'à 20 %"),
        ],
        "invest_contato": [
            ("Email Investisseurs", "a1elos.consultoria@gmail.com"),
            ("Email Général", "contato@a1elos.com"),
            ("Site Web", "www.a1elos.com"),
            ("DUNS", "942242668 — Dun & Bradstreet"),
        ],
        "invest_alocacao": "Allocation du Capital : 45 % Technologie · 30 % Marketing · 25 % Opérations",
        "frase_final": "Les chiffres ne mentent jamais.",
        "selo_final": ["DUNS 942242668", "24 PRODUITS", "14 LANGUES", "~5,3 MDS LOCUTEURS"],
        "graf_cons": "Conservateur",
        "graf_otim": "Optimiste",
        "grafico_titulo_linha": "Croissance Projetée (R$ milliers)",
        "pix_titulo": "Brésil : L'Infrastructure Pix",
        "pix_texto": "Le Pix est l'infrastructure publique de paiement instantané du Brésil. Pour A1ELOS, il garantit un encaissement immédiat, un faible coût et une acceptation universelle — le socle de l'opération B2C sur le marché brésilien et la porte d'entrée vers l'expansion internationale.",
        "pix_kpis": [
            ("30,1 Mds", "Transactions en 2025", "+20 % vs 2024 · Febraban"),
            ("76,4 %", "de la population utilise Pix", "211 millions de Brésiliens · Banque Centrale"),
            ("R$ 68,2 billions", "movimentés au 2e sem. 2025", "78,4 Mds de transactions · Banque Centrale"),
            ("~80 Mds", "transactions en 2025", "+25,7 % vs année précédente · Rapport Pix"),
        ],
        "pix_fonte": "Sources : Banque Centrale du Brésil (Pix en Chiffres) et Febraban (Enquête sur la Technologie Bancaire).",
        "ref_titulo": "Références Bibliographiques",
        "ref_intro": "Sources utilisées pour les données de marché, les projections et les indicateurs de cette présentation.",
        "ref_lista": [
            ("Global Wellness Institute", "Économie mondiale du bien-être : US$ 6,8 billions (2024) → US$ 9,8 billions (2029)."),
            ("MarkNtel Advisors", "Apps d'astrologie et de numérologie : US$ 3 milliards → US$ 9 milliards d'ici 2030 (TCAC ~20 %)."),
            ("FMI · Banque Mondiale", "PIB et parité de pouvoir d'achat (PPA) par pays."),
            ("Banque Centrale du Brésil", "Statistiques officielles du Pix : transactions, volume et utilisateurs."),
            ("Febraban", "Enquête sur la Technologie Bancaire — croissance du Pix en 2025."),
            ("IBGE", "Population et indicateurs socioéconomiques du Brésil."),
        ],
        },
           
"de": {
        "titulo": "A1ELOS Global Numerology",
        "subtitulo": "Die Wissenschaft der Zahlen, angewandt auf Ihren Erfolg",
        "capa_nota": "Strategische Präsentation für Investoren und Partner",
        "confidencial": "VERTRAULICH",
        "ano": "2026",
        "sumario_titulo": "Executive Summary",
        "duns_porque": "Warum ist der DUNS wichtig?",
        "preco_consciente": "Bewusster Preis",
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
        "grafico_anos": ["Jahr 1", "Jahr 3", "Jahr 5"],
        "grafico_titulo": "Konservative Prognose (R$ Tausend)",
        "grafico_titulo_linha": "Projiziertes Wachstum (R$ Tausend)",
        "fale_conosco": "Kontaktieren Sie uns",
        "sumario_intro": "Diese Präsentation ist strukturiert, um Investoren und Partner durch alle strategischen Aspekte von A1ELOS Global Numerology zu führen — von der Marktthese bis zum Modell wiederkehrender Einnahmen.",
        "sumario_cards": [
            ("01", "Über A1ELOS", "Holding, Portfolio und DUNS-Zertifizierung"),
            ("02", "Marktchance", "Globale Wellness-Wirtschaft US$ 6,8 Bio."),
            ("03", "Lösung und Globale Reichweite", "14 Sprachen, ~5,3 Mrd. Sprecher"),
            ("04", "Neue Märkte", "Indonesien, Türkei, Vietnam und Unternehmens-HR"),
            ("05", "Portfolio und Preise", "24 Produkte nach Kaufkraft kalibriert"),
            ("06", "Wiederkehrende Einnahmen", "Werbe-Banner und B2B-Pakete"),
            ("07", "Prognosen und Investition", "50-Jahres-Horizont · Seed-Runde R$ 3,5M"),
        ],
        "sobre_titulo": "Über A1ELOS",
        "sobre_texto": "A1ELOS ist ein Technologie- und Wissens-Holding, das künstliche Intelligenz, angewandte Numerologie und kulturelle Strategie vereint, um digitale Produkte mit großer Wirkung auf globaler Ebene zu schaffen. Unsere Mission: numerische Selbsterkenntnis zu demokratisieren — mit kulturellem Respekt und Respekt vor der Kaufkraft jedes Marktes.",
        "sobre_kpis": [
            ("23", "Aktive Produkte", "In 4 Zugriffsstufen"),
            ("14", "Sprachen", "~67 % der Weltbevölkerung"),
            ("5,3 Mrd.", "Sprecher", "Realer adressierbarer Markt"),
            ("KI", "Integriert", "Personalisierungs-Engine"),
        ],
        "sobre_duns": "DUNS 942242668 — Dun-&-Bradstreet-Zertifizierung, gültig in über 190 Ländern, die B2B-Verträge und internationale Joint Ventures ermöglicht.",
        "duns_titulo": "Internationale Glaubwürdigkeit",
        "duns_texto": "Die DUNS-Nummer ist der Unternehmenspass von A1ELOS auf der internationalen Bühne. Sie signalisiert Partnern, Firmenkunden und Investoren, dass das Unternehmen über verifizierbare Identität, nachvollziehbare Historie und Vertragsfähigkeit in jeder Rechtsordnung verfügt.",
        "duns_numero": "942242668",
        "duns_emitido": "Ausgestellt von Dun & Bradstreet — dem globalen Standard für Unternehmensidentität, anerkannt in über 190 Ländern.",
        "duns_paises": "190+ LÄNDER",
        "duns_beneficios": [
            ("B2B-Verträge", "Befähigung für globale Ausschreibungen und Lieferanten"),
            ("Joint Ventures", "Internationale Partnerschaften mit erleichterter Due Diligence"),
            ("Sofortige Glaubwürdigkeit", "Zeichen der Seriosität für institutionelle Investoren"),
        ],
        "mercado_titulo": "Marktchance",
        "mercado_texto": "Wir leben in der perfekten Konvergenz: digitales Wohlbefinden explodiert weltweit, während Numerologie und Astrologie zu Apps mit hohem Engagement migrieren. A1ELOS ist genau an dieser Schnittstelle positioniert — mit 74 % der Weltbevölkerung bereits online (~6 Milliarden Menschen).",
        "mercado_cards": [
            ("Globales Wohlbefinden", "US$ 6,8 Bio. → US$ 9,8 Bio. bis 2029 (+7,6 % p. a.)"),
            ("Astrologie/Numerologie-Apps", "US$ 3 Mrd. → US$ 9 Mrd. bis 2030 · CAGR 20 %"),
            ("Wellness-Apps", "CAGR 14,9 % → US$ 26,2 Mrd. im Jahr 2030"),
            ("Online-Nutzer", "74 % der Welt · ~6 Milliarden Menschen"),
        ],
        "mercado_rh_titulo": "Neuer Markt: Unternehmens-HR — das 24. Produkt",
        "mercado_rh_texto": "Das 24. Produkt — Team-Kompatibilität HR (R$ 98) — eröffnet den wichtigsten B2B-Markt von A1ELOS: das Unternehmens-HR. Die Analyse der energetischen Kompatibilität zwischen Führungskräften und Mitarbeitern (ideale Energie: Zahl 8) positioniert die Plattform als wegweisendes Instrument für Employer Branding und betriebliches Wohlbefinden, mit progressiven Rabatten von 10 % bis 50 % und direkter Verhandlung ab 2.000 Codes (Diamant-Plan).",
        "mercado_rh_vantagens": [
            "Energetische Harmonie der Abteilung → weniger zwischenmenschliche Reibungen und mehr Teamzusammenhalt",
            "Ausrichtung von Haltungen und Gedanken zwischen Führungskräften und Mitarbeitern → flüssigere Kommunikation",
            "Geringere Fluktuation und höhere Talentbindung",
            "Positives Betriebsklima → Zugewinn an Produktivität und Wohlbefinden",
            "Gestärktes Employer Branding → Anziehung von Talenten, die zur Kultur passen",
        ],
        "mercado_rh_cards": [
            ["HR Tech", "US$ 42,34 Mrd. (2025) → US$ 77,74 Mrd. (2031)", "CAGR 10,35 % · Mordor Intelligence"],
            ["Employer Branding", "US$ 1,89 Mrd. (2025) → US$ 3,62 Mrd. (2031)", "CAGR 11,19 % · Mordor Intelligence"],
            ["Corporate Wellness", "US$ 66,31 Mrd. (2025) → US$ 94,5 Mrd. (2031)", "CAGR 6,12 % · Mordor Intelligence"],
        ],
        "problema_titulo": "Das Problem, das wir lösen",
        "problema_col_esq_titulo": "Versagen des aktuellen Marktes",
        "problema_col_esq": [
            ("Sprachbarriere", "Die überwiegende Mehrheit der Numerologie-Tools funktioniert nur auf Englisch und schließt Milliarden von Muttersprachlern anderer Sprachen aus."),
            ("Preise ohne Bezug zur Realität", "Produkte, die für Schwellenländer in Dollar berechnet werden, erzeugen wirtschaftliche Ausgrenzung — der Nutzer lehnt nicht das Produkt ab, sondern den unerschwinglichen Preis."),
            ("Mangel an Tiefe", "Generische Tools liefern oberflächliche Antworten ohne Personalisierung, ohne kulturellen Kontext und ohne praktische Anwendung im Alltag."),
        ],
        "problema_col_dir_titulo": "Die Kosten der Ausgrenzung",
        "problema_col_dir": "Wenn eine Plattform Sprache und Kaufkraft ignoriert, verlässt sie freiwillig den größten Markt der Welt: die über 4 Milliarden Menschen, die in Schwellenländern leben und nicht-englischsprachige Sprachen sprechen. Das ist die Lücke, die A1ELOS mit chirurgischer Präzision besetzt.",
        "problema_destaque": "Plattformen, die die lokale Kaufkraft ignorieren, verlieren den Zugang zu mehr als 60 % des globalen adressierbaren Marktes.",
        "solucao_titulo": "Unsere Lösung: 3 Strategische Säulen",
        "solucao_texto": "A1ELOS hat eine integrierte Plattform aufgebaut, die Zahlenwissenschaft, künstliche Intelligenz und kulturelle Sensibilität verbindet. Die Lösung arbeitet auf drei komplementären Ebenen und sichert diversifizierte Einnahmen und hohe Bindung.",
        "solucao_colunas": [
            ("Persönliche Karten", "Tiefe, personalisierte numerische Analysen für den Endnutzer — Identität, Mission, Lebenszyklen und Kompatibilität — in 14 Sprachen mit integrierter KI."),
            ("Unternehmens-Numerologie", "Numerologische Diagnosen für Marken, CNPJs, Gründungsdaten und Unternehmensstrategie. Differenziertes Produkt mit hohem wahrgenommenen Wert im B2B-Markt."),
            ("White-Label B2B", "Lizenzierung der Plattform für Partnerunternehmen, die Numerologie unter eigener Marke anbieten möchten — mit mehrsprachigem Support und vollständiger Anpassung."),
        ],
        "alcance_titulo": "Globale Reichweite: 14 Sprachen · ~5,3 Milliarden Sprecher",
        "alcance_texto": "A1ELOS deckt ~67 % der Weltbevölkerung mit einer wirklich mehrsprachigen Plattform ab. Jede Sprache repräsentiert einen eigenen kulturellen Markt mit Preisen, die an die lokale Kaufkraft kalibriert sind.",
        "mercados_titulo": "Die 3 Neuen Märkte: +442 Millionen Sprecher",
        "mercados_texto": "Die strategische Expansion nach Indonesien, in die Türkei und nach Vietnam ist ein qualitativer Sprung: Märkte mit hohem Wirtschaftswachstum, wachsender digitaler Durchdringung und nachgewiesener Nachfrage nach erschwinglichen digitalen Wellness-Lösungen.",
        "mercados_cards": [
            ("Indonesien", ["285 Mio. Einwohner", "80,5 % Internet-Durchdringung", "~255 Mio. Indonesisch-Sprecher", "Wellness: US$ 51,2 Mrd. (2025) → US$ 72,8 Mrd. (2034)"]),
            ("Türkei", ["85,9 Mio. Einwohner", "BIP PPP pro Kopf US$ 37.301", "~90 Mio. Türkisch-Sprecher", "Über dem Weltdurchschnitt (US$ 27.211)"]),
            ("Vietnam",  ["~100 Mio. Einwohner", "BIP pro Kopf ~US$ 5.066 (+7,4 %/Jahr)", "~97 Mio. Vietnamesisch-Sprecher", "Wellness: US$ 303 Mio. (2025) → US$ 485 Mio. (2030)"]),
        ],
        "mercados_rodape": "3 neue Märkte = +442 Millionen neue adressierbare Sprecher — mit kulturell kalibrierter Preisgestaltung in die Plattform integriert.",
        "preco_titulo": "Philosophie des Bewussten Preises",
        "preco_esq": "Kultureller Respekt + Respekt vor der Kaufkraft = realer adressierbarer Markt. Gleicher Wertanteil. Unterschiedliche Preise. Gleiche Würde für alle Märkte.",
        "preco_dir_titulo": "So funktioniert es in der Praxis",
        "preco_dir": "A1ELOS wendet die Kaufkraftparität (KKP) als zentrales Preiskriterium an. Dasselbe Produkt bietet dem Nutzer in Lagos, Jakarta, Hanoi oder New York denselben relativen Wert — der Preis wird so kalibriert, dass die finanzielle Belastung proportional zum lokalen Einkommen ist.",
        "preco_pilares": [
            ("KKP-Kalibrierung", "Preise an den Kaufkraftindex jedes Landes angepasst"),
            ("Kultureller Respekt", "Sprache, Währung und lokaler Kontext im Produkt integriert"),
            ("Überlegene Konversion", "Ein fairer Preis erzeugt mehr Konversion und höhere langfristige Bindung"),
        ],
        "portfolio_titulo": "Portfolio: 24 Produkte in 4 Stufen",
        "portfolio_texto": "Die gestaffelte Struktur stellt sicher, dass jedes Nutzerprofil — vom Neugierigen bis zum Profi — ein Angebot findet, das zu seinem Engagement und seiner finanziellen Leistungsfähigkeit passt.",
        "portfolio_tabela": [
           ["Stufe", "Produkte", "Preisspanne (R$)", "Profil"],
           ["Basis", "Express-Karte, Vollständige Karte", "R$ 8 – 17", "Neugierig, erster Kontakt"],
           ["Mittel", "KI-Suche, Urnenname, Wahl-Nr.", "R$ 26 – 53", "Engagierter Nutzer"],
           ["Fortgeschritten", "NGO-Name, Künstlername, Babyname, Unterschrift, Firmenname", "R$ 35 – 44", "Profi, Unternehmer"],
           ["Premium", "Paarkarte, Familienkarte, Team-Kompatibilität HR ★, Kollektiv-Bonus", "R$ 98", "Hohes Einkommen, Unternehmensnutzung"],
           ["B2B", "Firmenpakete, Lizenzen, Geschenke", "Auf Anfrage", "Unternehmen und Teams"],
        ],
        "portfolio_rodape": "24 Produkte decken die gesamte Nutzerreise ab, vom ersten Kontakt bis zum wiederkehrenden Premium-Kunden — maximiert den LTV pro Sprache und Markt. Highlight: Team-Kompatibilität HR (R$ 98) — wegweisendes Produkt im Unternehmens-HR-Markt, ideale Energie 8.",
        "negocio_titulo": "Geschäftsmodell: 3 Einnahmequellen",
        "negocio_texto": "A1ELOS wurde mit diversifizierten und skalierbaren Einnahmen konzipiert: Direktverkäufe an den Endverbraucher auf globaler Ebene, B2B-Verträge mit hohem Wert und wiederkehrende geolokalisierte Werbung — drei Motoren, die sich gegenseitig speisen.",
        "negocio_colunas": [
            ("B2C — 14 Sprachen", "Direktverkauf digitaler Produkte in allen Währungen mit per KKP angepassten Preisen. Automatische Skalierung über KI — ohne zum Wachstum proportionales Serviceteam."),
            ("B2B — Progressive Rabatte", "Firmenpakete für HR, Employer Branding und institutionelle Geschenke. Rabatte von 10 % bis 50 % je nach Volumen. Ab 2.000 Codes direkte Verhandlung (Diamant-Plan). Verträge gestützt durch DUNS 942242668."),
            ("Geolokalisierte Werbung", "Banner segmentiert nach Land, Kontinent oder weltweit mit automatisierter Rotation. Monatliche wiederkehrende Einnahmen von hohem Wert — ohne Abhängigkeit vom Produktverkaufsvolumen."),
        ],
        "banners_titulo": "Werbe-Banner — Wiederkehrende Monatliche Einnahmen",
        "banners_texto": "Die A1ELOS-Plattform bietet Premium-Werbeflächen mit präziser Geolokalisierungs-Segmentierung — Land, Kontinent oder weltweit. Mit automatischer Rotation alle 8 Sekunden und für Desktop und Mobile optimierten Formaten liefern die Banner messbare Sichtbarkeit für regionale und internationale Werbetreibende.",
        "banners_tabela": [
            ["Segmentierung", "Fest (R$/Monat)", "Temporär (R$/Monat)", "Werbetreibenden-Profil"],
            ["Land", "R$ 800", "R$ 500", "Lokale KMU, regionaler Handel"],
            ["Kontinent", "R$ 1.800", "R$ 1.200", "Regionale Marken, kontinentale Expansion"],
            ["Welt", "R$ 3.500", "R$ 2.500", "Globale Unternehmen, internationale Apps"],
            ["Exklusives Sponsoring", "R$ 6.000", "R$ 4.500/Kampagne", "Master-Sponsoren, Markteinführungen"],
        ],
        "banners_formatos": "728×90 px — Zentrales Desktop-Banner · 320×100 px — Optimiertes Mobile-Format · 8 Sekunden — Automatische Rotation · Geo-Targeting — Land, Kontinent oder weltweite Reichweite",
        "b2b_titulo": "B2B-Firmenpakete — Hoher Wert, Großes Volumen",
        "b2b_texto": "Die B2B-Pakete machen A1ELOS zu einem Werkzeug für Employer Branding und betriebliches Wohlbefinden. Im Zentrum dieser Strategie steht das exklusive, kontinuierliche Produkt: die Team-Kompatibilität HR (R$ 98). Anders als einmalige Geschenke ist die Kompatibilitätsanalyse ein Personalmanagement-Instrument, das das Unternehmen in seinen Alltag integriert — Abteilungen und Teams mit der gewünschten Energie berechnet und alle Mitglieder einer Abteilung in derselben Wellenlänge und Harmonie synchronisiert. Ideal für kleine und große Unternehmen, ist es der Dienst, den die Personalabteilung ständig nutzt, gestützt auf stark wachsende Märkte: HR Tech (CAGR 10,35 %), Employer Branding (CAGR 11,19 %) und Corporate Wellness (CAGR 6,12 %).",
        "b2b_planos": [
            ("Basis-Plan · 50 Codes", "50× Express-Karte (je R$ 8). Ideal für Mitarbeiter-Vorteilsprogramme und Integrationsmaßnahmen."),
            ("Mittlerer Plan · 100 Codes", "50× Express-Karte + 50× KI-Suche (R$ 17). Perfekt für Teams und Employer-Branding-Strategie."),
            ("Premium-Plan · 200 Codes", "100× Express-Karte + 100× Vollständige Karte (R$ 17). Maximale analytische Tiefe für große Gruppen."),
        ],
        "b2b_tabela": [
            ["Ab", "Rabatt", "Profil", "Empfohlene Verwendung"],
            ["10 Codes", "10 %", "Kleine Teams", "Einmalige Wellness-Aktion"],
            ["50 Codes", "20 %", "Wachsende Teams", "Wiederkehrende Programme"],
            ["100 Codes", "25 %", "KMU", "Vierteljährlicher Vorteil"],
            ["200 Codes", "30 %", "Mittlere Unternehmen", "Vollständige Programme"],
            ["500 Codes", "40 %", "Mittlere Unternehmen", "Jährliches Geschenk an Mitarbeiter"],
            ["1.000 Codes", "45 %", "Große Konzerne", "Kundenbindung"],
            ["2.000 Codes", "50 %", "Große Gruppen", "Großer Maßstab"],
            ["Über 2.000", "Verhandelbar", "Maßgeschneiderter Diamant-Plan", "Bonus-Verteilung in großem Umfang"],
        ],
        "rh_destaque_titulo": "Team-Kompatibilität HR — Das Exklusive Produkt",
        "rh_destaque_texto": "Die Analyse der energetischen Kompatibilität zwischen Führungskräften und Mitarbeitern sowie zwischen Mitgliedern desselben Teams (ideale Energie: Zahl 8 — Macht, Führung und materielles Gleichgewicht) positioniert A1ELOS als Pionier im Unternehmens-HR-Markt. Die energetische Harmonie der Abteilung reduziert zwischenmenschliche Reibungen, richtet Haltungen und Gedanken aus, verringert die Fluktuation, stärkt das Betriebsklima und erhöht die Produktivität — ein Wert, den der Kollektiv-Bonus als einmaliges Geschenk nicht liefert. Es ist das Produkt, das das kurzfristige Wachstum und die wiederkehrenden B2B-Einnahmen trägt.",
        "projecoes_titulo": "Finanzprognosen: 50-Jahres-Horizont",
        "projecoes_texto": "Die Prognosen wurden auf der Grundlage prozentualer Penetrationsschätzungen über den potenziellen Markt von ~5,32 Milliarden Sprechern erstellt, mit einer konservativen Konversion von 3 % und einer Bonus-Einlösung zwischen 70 % und 90 %. Mit dem 24. Produkt — Team-Kompatibilität HR (R$ 98) und dem Kanal Kollektiv-/Unternehmens-Bonus — fließen die B2B-HR-Einnahmen in die Prognose ein, verankert in verifizierten Märkten: HR Tech (CAGR 10,35 %), Employer Branding (CAGR 11,19 %) und Corporate Wellness (CAGR 6,12 %). Der kurze Zeitraum (Jahre 1–5) zeigt das beschleunigte Wachstum der neuen B2B-Front; der lange Zeitraum spiegelt die kontinuierliche Stabilität des Modells bis zur vollständigen Assimilation des adressierbaren Marktes wider.",
        "projecoes_tabela": [
            ["Horizont", "Konservativ (R$)", "Optimistisch (R$)"],
            ["Jahr 1", "R$ 318k", "R$ 810k"],
            ["Jahr 2", "R$ 630k", "R$ 1,8M"],
            ["Jahr 3", "R$ 1,20M", "R$ 3,50M"],
            ["Jahr 4", "R$ 2,2M", "R$ 6,2M"],
            ["Jahr 5", "R$ 3,70M", "R$ 9,6M"],
        ],
        "projecoes_tabela_50": [
            ["Horizont", "Konservativ (R$)", "Optimistisch (R$)"],
            ["Jahr 1", "R$ 318k", "R$ 810k"],
            ["Jahr 3", "R$ 1,20M", "R$ 3,50M"],
            ["Jahr 5", "R$ 3,70M", "R$ 9,6M"],
            ["Jahr 7", "R$ 7,8M", "R$ 20,5M"],
            ["Jahr 10", "R$ 16,3M", "R$ 44,0M"],
            ["Jahr 20", "R$ 64M", "R$ 184M"],
            ["Jahr 30", "R$ 133M", "R$ 359M"],
            ["Jahr 40", "R$ 202M", "R$ 606M"],
            ["Jahr 50", "R$ 276M", "R$ 869M"],
        ],
        "projecoes_curto_titulo": "Finanzprognosen: Kurzer Zeitraum (Jahre 1–5)",
        "projecoes_curto_texto": "Der kurze Zeitraum zeigt das beschleunigte Wachstum der neuen B2B-HR-Front (Team-Kompatibilität + Kollektiv-Bonus), fast 12x in 5 Jahren im konservativen Szenario — vor der langfristigen Stabilisierung.",
        "projecoes_curto_tabela": [
            ["Horizont", "Konservativ (R$)", "Optimistisch (R$)"],
            ["Jahr 1", "R$ 318k", "R$ 810k"],
            ["Jahr 2", "R$ 630k", "R$ 1,8M"],
            ["Jahr 3", "R$ 1,20M", "R$ 3,50M"],
            ["Jahr 4", "R$ 2,2M", "R$ 6,2M"],
            ["Jahr 5", "R$ 3,70M", "R$ 9,6M"],
         ],
        "tracao_titulo": "Traction und Bewährte Ergebnisse",
        "tracao_texto": "A1ELOS arbeitet bereits mit Produktkennzahlen, die das Modell validieren — hohe Bindung, Premium-Bewertung und eine wachsende Basis von B2B-Partnern zeigen, dass die Plattform dem Endnutzer und dem Unternehmensmarkt echten Wert bietet.",
        "tracao_kpis": [
            ("12K+", "Aktive Nutzer", "Organische Basis in stetigem Wachstum"),
            ("87 %", "Bindung", "Weit über dem Branchendurchschnitt (~30 %)"),
            ("4,8★", "Durchschnittliche Bewertung", "Nachgewiesene Zufriedenheit der Endnutzer"),
            ("23", "B2B-Partner", "Aktive Verträge mit Unternehmen und HR-Abteilungen"),
        ],
        "roteiro_titulo": "Strategische Roadmap",
        "roteiro_texto": "A1ELOS führt einen Plan in vier progressiven Phasen aus — von der Konsolidierung der aktuellen Basis bis zur globalen Marktführerschaft, mit klaren Exit-Optionen für Investoren.",
        "roteiro_fases": [
            ("Phase 1 · Konsolidierung", "Stärkung der Nutzerbasis in den bereits aktiven Sprachen. Optimierung von Konversion, Bindung und LTV. Seed-Runde abgeschlossen."),
            ("Phase 2 · Expansion", "Offizieller Start in den 3 neuen Märkten: Indonesien, Türkei und Vietnam. Beschleunigung des B2B-Kanals und geolokalisierte Werbung."),
            ("Phase 3 · Globaler Eintritt", "Aktive Präsenz in allen 14 Sprachen mit lokalisierten Kampagnen. White-Label-Partnerschaften auf 5+ Kontinenten. Serie A."),
            ("Phase 4 · Führung", "20+ Länder mit konsolidierten Operationen. Globale Referenz-SaaS-Plattform für angewandte Numerologie. IPO oder strategischer Exit."),
        ],
        "invest_titulo": "Investition und Kontakt",
        "invest_texto": "Wir sind bereit für private Präsentationen, Due Diligence und Verhandlungen. Kontaktieren Sie uns über den Kanal Ihrer Wahl.",
        "invest_dados": [
            ("Seed-Runde", "R$ 3,5 Millionen"),
            ("Pre-Money-Bewertung", "R$ 14 Millionen"),
            ("Angebotenes Eigenkapital", "Bis zu 20 %"),
        ],
        "invest_contato": [
            ("Investoren-E-Mail", "a1elos.consultoria@gmail.com"),
            ("Allgemeine E-Mail", "contato@a1elos.com"),
            ("Website", "www.a1elos.com"),
            ("DUNS", "942242668 — Dun & Bradstreet"),
        ],
        "invest_alocacao": "Kapitalallokation: 45 % Technologie · 30 % Marketing · 25 % Betrieb",
        "frase_final": "Zahlen lügen niemals.",
        "selo_final": ["DUNS 942242668", "24 PRODUKTE", "14 SPRACHEN", "~5,3 MRD. SPRECHER"],
        "graf_cons": "Konservativ",
        "graf_otim": "Optimistisch",
        "grafico_titulo_linha": "Projiziertes Wachstum (R$ Tausend)",
        "pix_titulo": "Brasilien: Die Pix-Infrastruktur",
        "pix_texto": "Pix ist Brasiliens öffentliche Infrastruktur für Sofortzahlungen. Für A1ELOS gewährleistet es sofortige Inkassierung, niedrige Kosten und universelle Akzeptanz — das Fundament des B2C-Geschäfts im brasilianischen Markt und das Tor zur internationalen Expansion.",
        "pix_kpis": [
            ("30,1 Mrd.", "Transaktionen im Jahr 2025", "+20 % vs. 2024 · Febraban"),
            ("76,4 %", "der Bevölkerung nutzt Pix", "211 Millionen Brasilianer · Zentralbank"),
            ("R$ 68,2 Bio.", "bewegt im 2. Halbjahr 2025", "78,4 Mrd. Transaktionen · Zentralbank"),
            ("~80 Mrd.", "Transaktionen im Jahr 2025", "+25,7 % vs. Vorjahr · Pix-Bericht"),
        ],
        "pix_fonte": "Quellen: Zentralbank von Brasilien (Pix in Zahlen) und Febraban (Umfrage zur Banktechnologie).",
        "ref_titulo": "Bibliografische Referenzen",
        "ref_intro": "Quellen, die für die Marktdaten, Prognosen und Indikatoren dieser Präsentation verwendet wurden.",
        "ref_lista": [
            ("Global Wellness Institute", "Globale Wellness-Wirtschaft: US$ 6,8 Bio. (2024) → US$ 9,8 Bio. (2029)."),
            ("MarkNtel Advisors", "Astrologie- und Numerologie-Apps: US$ 3 Mrd. → US$ 9 Mrd. bis 2030 (CAGR ~20 %)."),
            ("IWF · Weltbank", "BIP und Kaufkraftparität (KKP) nach Land."),
            ("Zentralbank von Brasilien", "Offizielle Pix-Statistiken: Transaktionen, Volumen und Nutzer."),
            ("Febraban", "Umfrage zur Banktechnologie — Wachstum von Pix im Jahr 2025."),
            ("IBGE", "Bevölkerung und sozioökonomische Indikatoren Brasiliens."),
        ],
        },

"ja": {
        "titulo": "A1ELOS Global Numerology",
        "subtitulo": "数字の科学をあなたの成功に",
        "capa_nota": "投資家とパートナーのための戦略的プレゼンテーション",
        "confidencial": "機密",
        "ano": "2026",
        "sumario_titulo": "エグゼクティブサマリー",
        "duns_porque": "DUNSが重要な理由",
        "preco_consciente": "意識的価格設定",
        "idioma_col": "言語",
        "falantes_col": "話者（百万人）",
        "linhas_idiomas": [
           ["英語", "1.528"],
           ["中国語（北京語）", "1.184"],
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
        "fonte_receita": "収入源",
        "participacao": "割合",
        "b2c_linha": "B2C — 14言語",
        "b2b_linha": "B2B — 段階的割引",
        "pub_linha": "位置情報広告",
        "tabela_descontos": "段階的割引表",
        "grafico_anos": ["1年目", "3年目", "5年目"],
        "grafico_titulo": "保守的予測（R$千）",
        "grafico_titulo_linha": "予測成長（R$千）",
        "fale_conosco": "お問い合わせ",
        "sumario_intro": "このプレゼンテーションは、投資家とパートナーがA1ELOS Global Numerologyの戦略的側面—市場仮説から継続的収益モデルまで—をすべて理解できるように構成されています。",
        "sumario_cards": [
            ("01", "A1ELOSについて", "持株会社、ポートフォリオ、DUNS資格"),
            ("02", "市場機会", "世界のウェルネス経済 US$ 6,8兆"),
            ("03", "ソリューションとグローバル展開", "14言語、約53億人の話者"),
            ("04", "新市場", "インドネシア、トルコ、ベトナム、法人人事"),
            ("05", "ポートフォリオと価格", "購買力に応じて調整された24の製品"),
            ("06", "継続的収益", "広告バナーとB2Bパッケージ"),
            ("07", "予測と投資", "50年の展望 · シードラウンド R$ 3,5M"),
        ],
        "sobre_titulo": "A1ELOSについて",
        "sobre_texto": "A1ELOSは、人工知能、応用数秘術、文化的戦略を統合し、世界中に大きな影響を与えるデジタル製品を生み出すテクノロジーと知識の持株会社です。私たちの使命：文化的尊重と各市場の購買力への尊重をもって、数秘術による自己理解を民主化すること。",
        "sobre_kpis": [
            ("23", "アクティブな製品", "4つのアクセスレベル"),
            ("14", "言語", "世界人口の約67%"),
            ("53億", "話者", "実際の潜在市場"),
            ("AI", "統合", "パーソナライゼーションエンジン"),
        ],
        "sobre_duns": "DUNS 942242668 — Dun & Bradstreet認定で、190か国以上で有効。B2B契約と国際的な合弁事業を可能にします。",
        "duns_titulo": "国際的な信用力",
        "duns_texto": "DUNS番号は、国際舞台におけるA1ELOSの企業パスポートです。検証可能なアイデンティティ、追跡可能な履歴、あらゆる管轄区域での契約能力を備えていることを、パートナー、法人顧客、投資家に示します。",
        "duns_numero": "942242668",
        "duns_emitido": "Dun & Bradstreet発行 — 190か国以上で認められた世界的な企業アイデンティティ基準。",
        "duns_paises": "190か国以上",
        "duns_beneficios": [
            ("B2B契約", "国際的な入札とサプライヤーの資格"),
            ("合弁事業", "デューデリジェンスが容易な国際パートナーシップ"),
            ("即時の信用力", "機関投資家への真剣さのシグナル"),
        ],
        "mercado_titulo": "市場機会",
        "mercado_texto": "私たちは完璧な収束の中にいます：デジタルウェルネスが世界的に爆発的に成長する一方で、数秘術と占星術はエンゲージメントの高いアプリへと移行しています。A1ELOSはまさにこの交差点に位置し、世界人口の74%がすでにオンライン（約60億人）です。",
        "mercado_cards": [
            ("世界のウェルネス", "US$ 6,8兆 → 2029年までにUS$ 9,8兆（年率+7,6%）"),
            ("占星術・数秘術アプリ", "US$ 3十億 → 2030年までにUS$ 9十億 · CAGR 20%"),
            ("ウェルネスアプリ", "CAGR 14,9% → 2030年までにUS$ 26,2十億"),
            ("オンラインユーザー", "世界の74% · 約60億人"),
        ],
        "mercado_rh_titulo": "新市場：法人人事 — 24番目の製品",
        "mercado_rh_texto": "24番目の製品—チーム互換性人事（R$ 98）—は、A1ELOSの主要B2B市場である法人人事を開拓します。マネージャーと従業員間のエネルギー的互換性の分析（理想のエネルギー：数字8）は、プラットフォームを画期的なエンプロイヤーブランディングおよび法人ウェルネスツールとして位置づけ、10%から50%の段階的割引と2.000コード以上の直接交渉（ダイヤモンドプラン）を備えています。",
        "mercado_rh_vantagens": [
            "部門のエネルギー的調和 → 対人摩擦の軽減とチームの結束強化",
            "マネージャーと従業員間の姿勢と思考の整合 → よりスムーズなコミュニケーション",
            "離職率（ターンオーバー）の低下と人材定着率の向上",
            "良好な組織風土 → 生産性とウェルネスの向上",
            "強化されたエンプロイヤーブランディング → 文化に合った人材の誘致",
        ],
        "mercado_rh_cards": [
            ["HRテック", "US$ 42,34十億（2025年）→ US$ 77,74十億（2031年）", "CAGR 10,35% · Mordor Intelligence"],
            ["エンプロイヤーブランディング", "US$ 1,89十億（2025年）→ US$ 3,62十億（2031年）", "CAGR 11,19% · Mordor Intelligence"],
            ["法人ウェルネス", "US$ 66,31十億（2025年）→ US$ 94,5十億（2031年）", "CAGR 6,12% · Mordor Intelligence"],
        ],
        "problema_titulo": "私たちが解決する問題",
        "problema_col_esq_titulo": "現在の市場の欠陥",
        "problema_col_esq": [
            ("言語の壁", "数秘術ツールの圧倒的多数は英語のみで動作し、他の言語の母語話者何十億人も排除しています。"),
            ("現実とかけ離れた価格", "新興市場向けにドル建てで請求される製品は経済的排除を生みます—ユーザーは製品を拒否するのではなく、手の届かない価格を拒否するのです。"),
            ("深みの欠如", "一般的なツールは、パーソナライゼーションも、文化的文脈も、日常生活への実用的応用もない浅い回答を提供します。"),
        ],
        "problema_col_dir_titulo": "排除のコスト",
        "problema_col_dir": "プラットフォームが言語と購買力を無視するとき、それは世界最大の市場を自ら放棄します：新興経済に暮らし、非英語圏の言語を話す40億人以上の人々。これこそが、A1ELOSが外科的精度で占めるギャップです。",
        "problema_destaque": "現地の購買力を無視するプラットフォームは、世界の潜在市場の60%以上へのアクセスを失います。",
        "solucao_titulo": "私たちのソリューション：3つの戦略的柱",
        "solucao_texto": "A1ELOSは、数秘術の科学、人工知能、文化的感受性を組み合わせた統合プラットフォームを構築しました。ソリューションは3つの補完的な前線で機能し、多様な収益と高い定着率を保証します。",
        "solucao_colunas": [
            ("パーソナルマップ", "エンドユーザー向けの深くパーソナライズされた数値分析—アイデンティティ、使命、ライフサイクル、互換性—14言語、統合AIで提供。"),
            ("ビジネス数秘術", "ブランド、CNPJ、設立日、企業戦略に適用される数秘術的診断。B2B市場で認識価値の高い差別化製品。"),
            ("ホワイトラベルB2B", "自社ブランドで数秘術を提供したいパートナー企業向けのプラットフォームライセンス—多言語サポートと完全なカスタマイズ付き。"),
        ],
        "alcance_titulo": "グローバル展開：14言語 · 約53億人の話者",
        "alcance_texto": "A1ELOSは、真に多言語対応のプラットフォームで世界人口の約67%をカバーしています。各言語は異なる文化的市場を表し、現地の購買力に合わせて価格が調整されています。",
        "mercados_titulo": "3つの新市場：+4億4,200万人の話者",
        "mercados_texto": "インドネシア、トルコ、ベトナムへの戦略的拡大は質的飛躍を表します：高い経済成長、増大するデジタル普及率、そして手頃なデジタルウェルネスソリューションへの実証済みの需要を持つ市場です。",
        "mercados_cards": [
            ("インドネシア", ["2億8,500万人の人口", "インターネット普及率80,5%", "インドネシア語話者 約2億5,500万人", "ウェルネス：US$ 51,2十億（2025年）→ US$ 72,8十億（2034年）"]),
            ("トルコ", ["8.590万人の人口", "一人当たりGDP PPP US$ 37.301", "トルコ語話者 約9.000万人", "世界平均（US$ 27.211）を上回る"]),
            ("ベトナム",  ["約1億人の人口", "一人当たりGDP 約US$ 5.066（年+7,4%）", "ベトナム語話者 約9.700万人", "ウェルネス：US$ 303百万（2025年）→ US$ 485百万（2030年）"]),
        ],
        "mercados_rodape": "3つの新市場 = 新たにアクセス可能な話者+4億4,200万人 — 文化的に調整された価格設定でプラットフォームに統合。",
        "preco_titulo": "意識的価格設定の哲学",
        "preco_esq": "文化的尊重 + 購買力への尊重 = 実際の潜在市場。同じ価値の比率。異なる価格。すべての市場に等しい尊厳。",
        "preco_dir_titulo": "実際の仕組み",
        "preco_dir": "A1ELOSは購買力平価（PPP）を中心的な価格設定基準として適用します。同じ製品がラゴス、ジャカルタ、ハノイ、ニューヨークのユーザーに同じ相対的価値を提供します—価格は、金銭的努力が現地所得に比例するように調整されています。",
        "preco_pilares": [
            ("PPP調整", "各国の購買力指数に合わせた価格"),
            ("文化的尊重", "言語、通貨、ローカルコンテキストを製品に統合"),
            ("優れたコンバージョン", "公正な価格はより多くのコンバージョンと長期的な定着をもたらす"),
        ],
        "portfolio_titulo": "ポートフォリオ：4レベル、24製品",
        "portfolio_texto": "階層構造により、好奇心の人からプロフェッショナルまで、あらゆるユーザープロファイルが自分の関与度と財務能力に適したオファーを見つけられます。",
        "portfolio_tabela": [
           ["レベル", "製品", "価格帯（R$)", "プロファイル"],
           ["ベーシック", "エクスプレスマップ、フルマップ", "R$ 8 – 17", "好奇心旺盛、初回"],
           ["インターミディエイト", "AI検索、選挙名、投票番号", "R$ 26 – 53", "熱心なユーザー"],
           ["アドバンスト", "NGO名、芸名、赤ちゃんの名前、署名、ビジネス名", "R$ 35 – 44", "プロフェッショナル、起業家"],
           ["プレミアム", "カップルマップ、ファミリーマップ、チーム互換性人事 ★、団体ボーナス", "R$ 98", "高所得、法人利用"],
           ["B2B", "法人パッケージ、ライセンス、ギフト", "要相談", "企業とチーム"],
        ],
        "portfolio_rodape": "24の製品は、初回接触からリピートプレミアム顧客まで、ユーザーの旅全体をカバーし、言語と市場ごとのLTVを最大化します。注目：チーム互換性人事（R$ 98）—法人人事市場の開拓者製品、理想のエネルギー8。",
        "negocio_titulo": "ビジネスモデル：3つの収入源",
        "negocio_texto": "A1ELOSは多様でスケーラブルな収益で設計されています：グローバル規模でのエンドユーザーへの直接販売、高価値のB2B契約、継続的な位置情報広告—相互に支え合う3つのエンジンです。",
        "negocio_colunas": [
            ("B2C — 14言語", "あらゆる通貨でのデジタル製品の直接販売、PPPに基づく価格調整。AIによる自動スケール—成長に比例したサポートチーム不要。"),
            ("B2B — 段階的割引", "人事、エンプロイヤーブランディング、法人ギフト向けの法人パッケージ。ボリュームに応じて10%から50%の割引。2.000コード超は直接交渉（ダイヤモンドプラン）。契約はDUNS 942242668によって裏付け。"),
            ("位置情報広告", "国、大陸、全世界でセグメント化されたバナー、自動ローテーション。製品販売量に依存しない高価値の毎月の継続収益。"),
        ],
        "banners_titulo": "広告バナー — 毎月の継続収益",
        "banners_texto": "A1ELOSプラットフォームは、国、大陸、全世界を対象とした正確な位置情報セグメンテーションを備えたプレミアム広告スペースを提供します。8秒ごとの自動ローテーションとデスクトップ・モバイル向けに最適化された形式により、バナーは地域および国際的な広告主に測定可能な可視性を提供します。",
        "banners_tabela": [
            ["セグメンテーション", "固定（R$/月）", "一時（R$/月）", "広告主プロファイル"],
            ["国", "R$ 800", "R$ 500", "地元の中小企業、地域商業"],
            ["大陸", "R$ 1.800", "R$ 1.200", "地域ブランド、大陸拡大"],
            ["世界", "R$ 3.500", "R$ 2.500", "グローバル企業、国際アプリ"],
            ["独占スポンサーシップ", "R$ 6.000", "R$ 4.500/キャンペーン", "マスタースポンサー、ローンチ"],
        ],
        "banners_formatos": "728×90 px — デスクトップ中央バナー · 320×100 px — 最適化されたモバイル形式 · 8秒 — 自動ローテーション · ジオターゲティング — 国、大陸、または全世界",
        "b2b_titulo": "B2B法人パッケージ — 高価値、大量",
        "b2b_texto": "B2BパッケージはA1ELOSをエンプロイヤーブランディングと法人ウェルネスのツールに変えます。この戦略の中心にあるのは、独占的で継続的な製品：チーム互換性人事（R$ 98）です。一時的なギフトとは異なり、互換性分析は企業が日常業務に組み込む人材管理ツールです—部門とチームを望ましいエネルギーで計算し、部門の全メンバーを同じ波長と調和で同期させます。小規模・大企業を問わず理想的で、人事部が継続的に使用するサービスであり、急成長市場に支えられています：HRテック（CAGR 10,35%）、エンプロイヤーブランディング（CAGR 11,19%）、法人ウェルネス（CAGR 6,12%）。",
        "b2b_planos": [
            ("ベーシックプラン · 50コード", "エクスプレスマップ50点（各R$ 8）。従業員福利厚生プログラムと統合施策に最適。"),
            ("インターミディエイトプラン · 100コード", "エクスプレスマップ50点 + AI検索50点（R$ 17）。チームとエンプロイヤーブランディング戦略に最適。"),
            ("プレミアムプラン · 200コード", "エクスプレスマップ100点 + フルマップ100点（R$ 17）。大規模グループ向けの最大の分析深度。"),
        ],
        "b2b_tabela": [
            ["開始コード数", "割引", "プロファイル", "推奨用途"],
            ["10コード", "10%", "小規模チーム", "一度きりのウェルネス施策"],
            ["50コード", "20%", "成長中のチーム", "継続的なプログラム"],
            ["100コード", "25%", "中小企業", "四半期ごとの福利厚生"],
            ["200コード", "30%", "中規模企業", "完全なプログラム"],
            ["500コード", "40%", "中規模企業", "従業員への年次ギフト"],
            ["1.000コード", "45%", "大企業", "顧客ロイヤルティ"],
            ["2.000コード", "50%", "大規模グループ", "大規模展開"],
            ["2.000コード超", "交渉可能", "オーダーメイドのダイヤモンドプラン", "大量のボーナス配布"],
        ],
        "rh_destaque_titulo": "チーム互換性人事 — 独占製品",
        "rh_destaque_texto": "マネージャーと従業員間、および同じチームのメンバー間のエネルギー的互換性の分析（理想のエネルギー：数字8—力、リーダーシップ、物質的バランス）は、A1ELOSを法人人事市場の先駆者として位置づけます。部門のエネルギー的調和は対人摩擦を減らし、姿勢と思考を整合させ、離職率を下げ、組織風土を強化し、生産性を高めます—一度きりのギフトとしての団体ボーナスが提供しない価値です。それは短期成長と継続的なB2B収益を支える製品です。",
        "projecoes_titulo": "財務予測：50年の展望",
        "projecoes_texto": "予測は、約53億2.000万人の話者の潜在的市場に対するパーセンテージ浸透率の推定に基づいて構築され、保守的コンバージョン率3%、ボーナス引き換え率70%から90%を前提としています。24番目の製品—チーム互換性人事（R$ 98）と団体・法人ボーナスチャネルにより、人事B2B収益が予測に組み込まれ、検証済み市場に裏付けられています：HRテック（CAGR 10,35%）、エンプロイヤーブランディング（CAGR 11,19%）、法人ウェルネス（CAGR 6,12%）。短期（1〜5年）は新たなB2B前線の加速的成長を示し、長期は潜在市場の完全な吸収までのモデルの継続的安定性を反映しています。",
        "projecoes_tabela": [
            ["展望", "保守的（R$)", "楽観的（R$)"],
            ["1年目", "R$ 318k", "R$ 810k"],
            ["2年目", "R$ 630k", "R$ 1,8M"],
            ["3年目", "R$ 1,20M", "R$ 3,50M"],
            ["4年目", "R$ 2,2M", "R$ 6,2M"],
            ["5年目", "R$ 3,70M", "R$ 9,6M"],
        ],
        "projecoes_tabela_50": [
            ["展望", "保守的（R$)", "楽観的（R$)"],
            ["1年目", "R$ 318k", "R$ 810k"],
            ["3年目", "R$ 1,20M", "R$ 3,50M"],
            ["5年目", "R$ 3,70M", "R$ 9,6M"],
            ["7年目", "R$ 7,8M", "R$ 20,5M"],
            ["10年目", "R$ 16,3M", "R$ 44,0M"],
            ["20年目", "R$ 64M", "R$ 184M"],
            ["30年目", "R$ 133M", "R$ 359M"],
            ["40年目", "R$ 202M", "R$ 606M"],
            ["50年目", "R$ 276M", "R$ 869M"],
        ],
        "projecoes_curto_titulo": "財務予測：短期（1〜5年）",
        "projecoes_curto_texto": "短期は、新たな人事B2B前線（チーム互換性 + 団体ボーナス）の加速的成長を示します。保守的シナリオでは5年間でほぼ12倍—長期安定化の前に。",
        "projecoes_curto_tabela": [
            ["展望", "保守的（R$)", "楽観的（R$)"],
            ["1年目", "R$ 318k", "R$ 810k"],
            ["2年目", "R$ 630k", "R$ 1,8M"],
            ["3年目", "R$ 1,20M", "R$ 3,50M"],
            ["4年目", "R$ 2,2M", "R$ 6,2M"],
            ["5年目", "R$ 3,70M", "R$ 9,6M"],
         ],
        "tracao_titulo": "牽引力と実証された実績",
        "tracao_texto": "A1ELOSはモデルを検証する製品指標で既に運営されています—高い定着率、プレミアム評価、成長するB2Bパートナー基盤は、プラットフォームがエンドユーザーと法人市場に真の価値を提供することを示しています。",
        "tracao_kpis": [
            ("12K+", "アクティブユーザー", "一貫して成長するオーガニック基盤"),
            ("87%", "定着率", "業界平均（約30%）を大幅に上回る"),
            ("4,8★", "平均評価", "エンドユーザーの実証済み満足度"),
            ("23", "B2Bパートナー", "企業および人事とのアクティブ契約"),
        ],
        "roteiro_titulo": "戦略的ロードマップ",
        "roteiro_texto": "A1ELOSは、現在の基盤の統合からグローバル市場リーダーシップまで、投資家に明確な出口オプションを備えた4つの段階的なフェーズで計画を実行します。",
        "roteiro_fases": [
            ("フェーズ1 · 統合", "既存言語でのユーザー基盤の強化。コンバージョン、定着率、LTVの最適化。シードラウンド完了。"),
            ("フェーズ2 · 拡大", "3つの新市場での正式ローンチ：インドネシア、トルコ、ベトナム。B2Bチャネルと位置情報広告の加速。"),
            ("フェーズ3 · グローバル参入", "ローカライズされたキャンペーンで全14言語に積極展開。5以上の大陸でのホワイトラベル提携。シリーズA。"),
            ("フェーズ4 · リーダーシップ", "20以上の国で事業を統合。応用数秘術における世界的な参照SaaSプラットフォーム。IPOまたは戦略的出口。"),
        ],
        "invest_titulo": "投資とお問い合わせ",
        "invest_texto": "私たちはプライベートプレゼンテーション、デューデリジェンス、交渉の準備ができています。お好みのチャネルからご連絡ください。",
        "invest_dados": [
            ("シードラウンド", "R$ 3,5百万"),
            ("プレマネー評価額", "R$ 14百万"),
            ("提供株式", "最大20%"),
        ],
        "invest_contato": [
            ("投資家メール", "a1elos.consultoria@gmail.com"),
            ("一般メール", "contato@a1elos.com"),
            ("ウェブサイト", "www.a1elos.com"),
            ("DUNS", "942242668 — Dun & Bradstreet"),
        ],
        "invest_alocacao": "資金配分：テクノロジー45% · マーケティング30% · オペレーション25%",
        "frase_final": "数字は決して嘘をつかない。",
        "selo_final": ["DUNS 942242668", "24製品", "14言語", "約53億人の話者"],
        "graf_cons": "保守的",
        "graf_otim": "楽観的",
        "grafico_titulo_linha": "予測成長（R$千）",
        "pix_titulo": "ブラジル：Pixインフラストラクチャ",
        "pix_texto": "Pixはブラジルの公共の即時決済インフラです。A1ELOSにとって、即時回収、低コスト、普遍的受け入れを保証します—ブラジル市場でのB2C運営の基盤であり、国際展開への玄関口です。",
        "pix_kpis": [
            ("30,1十億", "2025年の取引", "+20% vs 2024 · Febraban"),
            ("76,4%", "の人口がPixを使用", "ブラジル人2億1.100万人 · 中央銀行"),
            ("R$ 68,2兆", "2025年下半期に動かした額", "78,4十億件の取引 · 中央銀行"),
            ("約80十億", "2025年の取引", "前年比+25,7% · Pixレポート"),
        ],
        "pix_fonte": "出典：ブラジル中央銀行（Pixの数字）およびFebraban（銀行技術調査）。",
        "ref_titulo": "参考文献",
        "ref_intro": "このプレゼンテーションの市場データ、予測、指標に使用された出典。",
        "ref_lista": [
            ("Global Wellness Institute", "世界のウェルネス経済：US$ 6,8兆（2024年）→ US$ 9,8兆（2029年）。"),
            ("MarkNtel Advisors", "占星術・数秘術アプリ：US$ 3十億 → 2030年までにUS$ 9十億（CAGR約20%）。"),
            ("IMF · 世界銀行", "国別のGDPと購買力平価（PPP）。"),
            ("ブラジル中央銀行", "Pixの公式統計：取引、量、ユーザー。"),
            ("Febraban", "銀行技術調査 — 2025年のPix成長。"),
            ("IBGE", "ブラジルの人口と社会経済指標。"),
        ],
        },     
           
"zh": {
        "titulo": "A1ELOS Global Numerology",
        "subtitulo": "数字科学，助您成功",
        "capa_nota": "面向投资者与合作伙伴的战略演示",
        "confidencial": "机密",
        "ano": "2026",
        "sumario_titulo": "执行摘要",
        "duns_porque": "DUNS为何重要？",
        "preco_consciente": "自觉定价",
        "idioma_col": "语言",
        "falantes_col": "使用者（百万）",
        "linhas_idiomas": [
           ["英语", "1.528"],
           ["普通话", "1.184"],
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
        "b2c_linha": "B2C — 14种语言",
        "b2b_linha": "B2B — 阶梯式折扣",
        "pub_linha": "地理定位广告",
        "tabela_descontos": "阶梯式折扣表",
        "grafico_anos": ["第1年", "第3年", "第5年"],
        "grafico_titulo": "保守预测（R$千）",
        "grafico_titulo_linha": "预计增长（R$千）",
        "fale_conosco": "联系我们",
        "sumario_intro": "本演示旨在引导投资者和合作伙伴了解A1ELOS Global Numerology的所有战略层面——从市场论点一直到经常性收入模式。",
        "sumario_cards": [
            ("01", "关于A1ELOS", "控股公司、产品组合与DUNS资质"),
            ("02", "市场机遇", "全球健康经济 US$ 6,8万亿"),
            ("03", "解决方案与全球覆盖", "14种语言，~53亿使用者"),
            ("04", "新市场", "印度尼西亚、土耳其、越南与企业人事"),
            ("05", "产品组合与价格", "按购买力校准的24款产品"),
            ("06", "经常性收入", "广告横幅与B2B套餐"),
            ("07", "预测与投资", "50年展望 · 种子轮 R$ 3,5M"),
        ],
        "sobre_titulo": "关于A1ELOS",
        "sobre_texto": "A1ELOS是一家技术与知识控股公司，融合人工智能、应用数字命理学与文化战略，在全球范围内创造具有高影响力的数字产品。我们的使命：在对文化以及各市场购买力尊重的前提下，普及数字化的自我认知。",
        "sobre_kpis": [
            ("23", "在售产品", "4个访问级别"),
            ("14", "语言", "约占全球人口67%"),
            ("53亿", "使用者", "真实可达市场"),
            ("AI", "已集成", "个性化引擎"),
        ],
        "sobre_duns": "DUNS 942242668 — 邓白氏认证，在190多个国家有效，支持B2B合同与国际合资企业。",
        "duns_titulo": "国际信誉",
        "duns_texto": "DUNS编号是A1ELOS在国际舞台上的企业护照。它向合作伙伴、企业客户和投资者表明，公司拥有可验证的身份、可追溯的历史以及在任何司法辖区的合同能力。",
        "duns_numero": "942242668",
        "duns_emitido": "由邓白氏（Dun & Bradstreet）签发——全球公认的企业身份标准，在190多个国家得到认可。",
        "duns_paises": "190多个国家",
        "duns_beneficios": [
            ("B2B合同", "获得全球招投标和供应商资格"),
            ("合资企业", "尽调更便捷的国际合作伙伴关系"),
            ("即时信誉", "向机构投资者传递认真态度的信号"),
        ],
        "mercado_titulo": "市场机遇",
        "mercado_texto": "我们正处于完美交汇点：数字健康在全球爆发式增长，而数字命理学和占星学正迁移至高互动应用。A1ELOS正位于这一交叉点上，全球74%的人口已经上网（约60亿人）。",
        "mercado_cards": [
            ("全球健康", "US$ 6,8万亿 → 2029年达US$ 9,8万亿（年增+7,6%）"),
            ("占星/数字命理应用", "US$ 3十亿 → 2030年达US$ 9十亿 · CAGR 20%"),
            ("健康应用", "CAGR 14,9% → 2030年达US$ 26,2十亿"),
            ("在线用户", "全球74% · 约60亿人"),
        ],
        "mercado_rh_titulo": "新市场：企业人事 — 第24款产品",
        "mercado_rh_texto": "第24款产品—团队相容性人事（R$ 98）—打开了A1ELOS主要的B2B市场：企业人事。管理者与员工之间能量相容性分析（理想能量：数字8）使该平台成为雇主品牌与企业健康的开创性工具，提供10%至50%的阶梯式折扣，超过2.000个代码可直接协商（钻石计划）。",
        "mercado_rh_vantagens": [
            "部门能量和谐 → 减少人际摩擦，增强团队凝聚力",
            "管理者与员工态度与思维的统一 → 沟通更顺畅",
            "降低离职率（turnover），提升人才留存",
            "积极的组织氛围 → 提升生产力与幸福感",
            "雇主品牌强化 → 吸引与文化契合的人才",
        ],
        "mercado_rh_cards": [
            ["HR科技", "US$ 42,34十亿（2025年）→ US$ 77,74十亿（2031年）", "CAGR 10,35% · Mordor Intelligence"],
            ["雇主品牌", "US$ 1,89十亿（2025年）→ US$ 3,62十亿（2031年）", "CAGR 11,19% · Mordor Intelligence"],
            ["企业健康", "US$ 66,31十亿（2025年）→ US$ 94,5十亿（2031年）", "CAGR 6,12% · Mordor Intelligence"],
        ],
        "problema_titulo": "我们解决的问题",
        "problema_col_esq_titulo": "当前市场的缺陷",
        "problema_col_esq": [
            ("语言障碍", "绝大多数数字命理工具仅以英文运行，将其他语言的数十亿母语使用者排除在外。"),
            ("价格脱离现实", "面向新兴市场以美元计价的产品造成经济排斥——用户拒绝的不是产品，而是难以承受的价格。"),
            ("缺乏深度", "通用工具只提供肤浅的回答，既无个性化，也无文化背景，更无日常生活的实际应用。"),
        ],
        "problema_col_dir_titulo": "排斥的代价",
        "problema_col_dir": "当一个平台忽视语言与购买力时，它等于自愿放弃世界上最大的市场：生活在新兴经济体中、使用非英语语言的40多亿人。这正是A1ELOS以精准外科式手段占据的空白。",
        "problema_destaque": "忽视当地购买力的平台将失去全球60%以上可达市场的机会。",
        "solucao_titulo": "我们的解决方案：三大战略支柱",
        "solucao_texto": "A1ELOS构建了一个融合数字科学、人工智能与文化敏感性的集成平台。该解决方案在三条互补战线上运作，确保收入多元化和高留存率。",
        "solucao_colunas": [
            ("个人命盘", "为终端用户提供深入、个性化的数字分析——身份、使命、人生周期和相容性——以14种语言交付，集成AI。"),
            ("企业数字命理", "将数字命理诊断应用于品牌、CNPJ、成立日期和企业战略。在B2B市场具有高感知价值的差异化产品。"),
            ("白标B2B", "向希望以自有品牌提供数字命理服务的合作企业授权平台——支持多语言和完全定制。"),
        ],
        "alcance_titulo": "全球覆盖：14种语言 · 约53亿使用者",
        "alcance_texto": "A1ELOS通过一个真正多语言的平台覆盖全球约67%的人口。每种语言代表一个独特的文化市场，价格根据当地购买力进行校准。",
        "mercados_titulo": "三大新市场：+4亿4,200万使用者",
        "mercados_texto": "向印度尼西亚、土耳其和越南的战略扩张代表了一次质的飞跃：这些市场经济增长强劲、数字渗透率不断提升，且对可负担的数字健康解决方案有切实需求。",
        "mercados_cards": [
            ("印度尼西亚", ["2亿8,500万居民", "互联网普及率80,5%", "约2亿5,500万印度尼西亚语使用者", "健康：US$ 51,2十亿（2025年）→ US$ 72,8十亿（2034年）"]),
            ("土耳其", ["8.590万居民", "人均GDP购买力平价 US$ 37.301", "约9.000万土耳其语使用者", "高于世界平均水平（US$ 27.211）"]),
            ("越南",  ["约1亿居民", "人均GDP约US$ 5.066（年增+7,4%）", "约9.700万越南语使用者", "健康：US$ 303百万（2025年）→ US$ 485百万（2030年）"]),
        ],
        "mercados_rodape": "3个新市场 = 新增4亿4,200万可达使用者——以文化校准的定价融入平台。",
        "preco_titulo": "自觉定价理念",
        "preco_esq": "文化尊重 + 对购买力的尊重 = 真实可达市场。相同的价值比例。不同的价格。所有市场享有同等的尊严。",
        "preco_dir_titulo": "实际运作方式",
        "preco_dir": "A1ELOS将购买力平价（PPP）作为核心定价标准。同一款产品在拉各斯、雅加达、河内或纽约为使用者提供相同的相对价值——价格经过校准，使财务负担与当地收入成比例。",
        "preco_pilares": [
            ("购买力平价校准", "根据各国的购买力指数调整价格"),
            ("文化尊重", "将语言、货币和当地背景融入产品"),
            ("卓越转化率", "公平的价格带来更多转化和更高的长期留存"),
        ],
        "portfolio_titulo": "产品组合：4个级别、24款产品",
        "portfolio_texto": "分层结构确保每个用户画像——从好奇者到专业人士——都能找到适合其参与度和财务能力的方案。",
        "portfolio_tabela": [
           ["级别", "产品", "价格区间（R$)", "用户画像"],
           ["基础", "速览命盘、完整命盘", "R$ 8 – 17", "好奇者、初次接触"],
           ["中级", "AI搜索、选票用名、选民编号", "R$ 26 – 53", "活跃用户"],
           ["高级", "非政府组织名、艺名、宝宝名、签名、企业名", "R$ 35 – 44", "专业人士、创业者"],
           ["尊享", "情侣命盘、家庭命盘、团队相容性人事 ★、集体福利", "R$ 98", "高收入、企业使用"],
           ["B2B", "企业套餐、授权、赠品", "面议", "企业与团队"],
        ],
        "portfolio_rodape": "24款产品覆盖用户的整个旅程，从初次接触到复购尊享客户——最大化每种语言和市场的LTV。亮点：团队相容性人事（R$ 98）——企业人事市场的开创性产品，理想能量8。",
        "negocio_titulo": "商业模式：三大收入来源",
        "negocio_texto": "A1ELOS以多元化和可扩展的收入进行设计：面向全球终端消费者的直销、高价值B2B合同以及经常性地理定位广告——三个相互滋养的引擎。",
        "negocio_colunas": [
            ("B2C — 14种语言", "以所有货币直接销售数字产品，价格按PPP调整。通过AI实现自动扩展——无需与增长成比例的服务团队。"),
            ("B2B — 阶梯式折扣", "面向人事、雇主品牌和机构赠品的企业套餐。按量提供10%至50%的折扣。超过2.000个代码可直接协商（钻石计划）。合同由DUNS 942242668背书。"),
            ("地理定位广告", "按国家、大洲或全球细分并自动轮播的广告横幅。高价值、每月经常性收入——不依赖产品销量。"),
        ],
        "banners_titulo": "广告横幅 — 每月经常性收入",
        "banners_texto": "A1ELOS平台提供精准地理定位细分的优质广告位——国家、大洲或全球。每8秒自动轮播，优化桌面端和移动端格式，为地区和国际广告主提供可衡量的曝光。",
        "banners_tabela": [
            ["细分", "固定（R$/月）", "临时（R$/月）", "广告主画像"],
            ["国家", "R$ 800", "R$ 500", "本地中小企业、区域商业"],
            ["大洲", "R$ 1.800", "R$ 1.200", "区域品牌、大洲扩张"],
            ["全球", "R$ 3.500", "R$ 2.500", "跨国企业、国际应用"],
            ["独家赞助", "R$ 6.000", "R$ 4.500/活动", "主赞助商、新品发布"],
        ],
        "banners_formatos": "728×90 px — 桌面端中央横幅 · 320×100 px — 优化移动端格式 · 8秒 — 自动轮播 · 地理定向 — 国家、大洲或全球覆盖",
        "b2b_titulo": "B2B企业套餐 — 高价值、大规格",
        "b2b_texto": "B2B套餐将A1ELOS转变为企业雇主品牌和健康工具。这一战略的核心是独家的持续性产品：团队相容性人事（R$ 98）。与一次性赠品不同，相容性分析是企业融入日常运营的人员管理工具——按所需能量计算部门和团队，使部门所有成员在同一节奏与和谐中同步。无论大小企业均适用，是人力资源部门持续使用的服务，并有高速增长的市场支撑：HR科技（CAGR 10,35%）、雇主品牌（CAGR 11,19%）和企业健康（CAGR 6,12%）。",
        "b2b_planos": [
            ("基础套餐 · 50个代码", "速览命盘50份（每份R$ 8）。适合员工福利计划和入职活动。"),
            ("中级套餐 · 100个代码", "速览命盘50份 + AI搜索50份（R$ 17）。适合团队和雇主品牌战略。"),
            ("尊享套餐 · 200个代码", "速览命盘100份 + 完整命盘100份（R$ 17）。为大型团体提供最大分析深度。"),
        ],
        "b2b_tabela": [
            ["起订量", "折扣", "画像", "推荐用途"],
            ["10个代码", "10%", "小型团队", "一次性健康活动"],
            ["50个代码", "20%", "成长型团队", "经常性计划"],
            ["100个代码", "25%", "中小企业", "季度福利"],
            ["200个代码", "30%", "中型企业", "完整计划"],
            ["500个代码", "40%", "中型企业", "员工年度赠礼"],
            ["1.000个代码", "45%", "大型企业", "客户忠诚度"],
            ["2.000个代码", "50%", "大型集团", "大规模"],
            ["超过2.000", "可协商", "量身定制钻石计划", "批量发放福利"],
        ],
        "rh_destaque_titulo": "团队相容性人事 — 独家产品",
        "rh_destaque_texto": "管理者与员工之间、以及同一团队成员之间的能量相容性分析（理想能量：数字8——权力、领导力与物质平衡）将A1ELOS定位为企业人事市场的先驱。部门的能量和谐减少人际摩擦，统一态度与思维，降低离职率，强化组织氛围并提升生产力——这是作为一次性赠品的集体福利无法提供的价值。正是这款产品支撑着短期增长和经常性B2B收入。",
        "projecoes_titulo": "财务预测：50年展望",
        "projecoes_texto": "预测基于对约53亿2.000万使用者的潜在市场的百分比渗透率估算，采用3%的保守转化率和70%至90%的福利兑换率。随着第24款产品——团队相容性人事（R$ 98）以及集体/企业福利渠道——的加入，人事B2B收入被纳入预测，并以经过验证的市场为支撑：HR科技（CAGR 10,35%）、雇主品牌（CAGR 11,19%）和企业健康（CAGR 6,12%）。短期（第1–5年）体现了新B2B战线的加速增长；长期则反映模型在全面消化可达市场之前的持续稳定。",
        "projecoes_tabela": [
            ["展望", "保守（R$)", "乐观（R$)"],
            ["第1年", "R$ 318k", "R$ 810k"],
            ["第2年", "R$ 630k", "R$ 1,8M"],
            ["第3年", "R$ 1,20M", "R$ 3,50M"],
            ["第4年", "R$ 2,2M", "R$ 6,2M"],
            ["第5年", "R$ 3,70M", "R$ 9,6M"],
        ],
        "projecoes_tabela_50": [
            ["展望", "保守（R$)", "乐观（R$)"],
            ["第1年", "R$ 318k", "R$ 810k"],
            ["第3年", "R$ 1,20M", "R$ 3,50M"],
            ["第5年", "R$ 3,70M", "R$ 9,6M"],
            ["第7年", "R$ 7,8M", "R$ 20,5M"],
            ["第10年", "R$ 16,3M", "R$ 44,0M"],
            ["第20年", "R$ 64M", "R$ 184M"],
            ["第30年", "R$ 133M", "R$ 359M"],
            ["第40年", "R$ 202M", "R$ 606M"],
            ["第50年", "R$ 276M", "R$ 869M"],
        ],
        "projecoes_curto_titulo": "财务预测：短期（第1–5年）",
        "projecoes_curto_texto": "短期体现了新的人事B2B战线（团队相容性 + 集体福利）的加速增长，在保守情景下5年内增长近12倍——在长期稳定之前。",
        "projecoes_curto_tabela": [
            ["展望", "保守（R$)", "乐观（R$)"],
            ["第1年", "R$ 318k", "R$ 810k"],
            ["第2年", "R$ 630k", "R$ 1,8M"],
            ["第3年", "R$ 1,20M", "R$ 3,50M"],
            ["第4年", "R$ 2,2M", "R$ 6,2M"],
            ["第5年", "R$ 3,70M", "R$ 9,6M"],
         ],
        "tracao_titulo": "市场牵引力与已验证成果",
        "tracao_texto": "A1ELOS已经以验证模型的产品指标运营——高留存率、卓越评分和不断增长的B2B合作伙伴基础表明，该平台为终端用户和企业市场提供了真正的价值。",
        "tracao_kpis": [
            ("12K+", "活跃用户", "稳步增长的有机用户基础"),
            ("87%", "留存率", "远高于行业平均水平（约30%）"),
            ("4,8★", "平均评分", "终端用户满意度已验证"),
            ("23", "B2B合作伙伴", "与企业及人事部门的有效合同"),
        ],
        "roteiro_titulo": "战略路线图",
        "roteiro_texto": "A1ELOS以四个渐进阶段执行计划——从巩固现有基础到全球市场领导地位，为投资者提供明确的退出选项。",
        "roteiro_fases": [
            ("阶段1 · 巩固", "强化已启用语言中的用户基础。优化转化率、留存率和LTV。种子轮已完成。"),
            ("阶段2 · 扩张", "在3个新市场正式发布：印度尼西亚、土耳其和越南。加速B2B渠道和地理定位广告。"),
            ("阶段3 · 全球进入", "在全球14种语言中开展本地化营销活动。在5+大洲建立白标合作伙伴。A轮。"),
            ("阶段4 · 领导地位", "在20多个国家实现运营整合。成为应用数字命理领域的全球参考SaaS平台。IPO或战略退出。"),
        ],
        "invest_titulo": "投资与联系",
        "invest_texto": "我们已准备好进行非公开演示、尽职调查和谈判。请通过您偏好的渠道联系我们。",
        "invest_dados": [
            ("种子轮", "R$ 3,5百万"),
            ("投资前估值", "R$ 14百万"),
            ("出让股权", "最高20%"),
        ],
        "invest_contato": [
            ("投资者邮箱", "a1elos.consultoria@gmail.com"),
            ("一般邮箱", "contato@a1elos.com"),
            ("网站", "www.a1elos.com"),
            ("DUNS", "942242668 — 邓白氏"),
        ],
        "invest_alocacao": "资本配置：技术45% · 营销30% · 运营25%",
        "frase_final": "数字从不撒谎。",
        "selo_final": ["DUNS 942242668", "24款产品", "14种语言", "约53亿使用者"],
        "graf_cons": "保守",
        "graf_otim": "乐观",
        "grafico_titulo_linha": "预计增长（R$千）",
        "pix_titulo": "巴西：Pix基础设施",
        "pix_texto": "Pix是巴西的公共即时支付基础设施。对A1ELOS而言，它保证了即时收款、低成本与普遍接受——这是巴西市场B2C运营的基石，也是走向国际扩张的大门。",
        "pix_kpis": [
            ("30,1十亿", "2025年交易量", "较2024年+20% · Febraban"),
            ("76,4%", "的人口使用Pix", "2亿1.100万巴西人 · 央行"),
            ("R$ 68,2万亿", "2025年下半年流动金额", "78,4十亿笔交易 · 央行"),
            ("约80十亿", "2025年交易量", "较上年+25,7% · Pix报告"),
        ],
        "pix_fonte": "来源：巴西中央银行（Pix数据）和Febraban（银行技术调查）。",
        "ref_titulo": "参考文献",
        "ref_intro": "本演示的市场数据、预测和指标所使用的来源。",
        "ref_lista": [
            ("Global Wellness Institute", "全球健康经济：US$ 6,8万亿（2024年）→ US$ 9,8万亿（2029年）。"),
            ("MarkNtel Advisors", "占星与数字命理应用：US$ 3十亿 → 2030年达US$ 9十亿（CAGR约20%）。"),
            ("国际货币基金组织 · 世界银行", "各国GDP与购买力平价（PPP）。"),
            ("巴西中央银行", "Pix的官方统计：交易量、交易额与用户。"),
            ("Febraban", "银行技术调查 — 2025年Pix的增长。"),
            ("IBGE", "巴西人口与社会经济指标。"),
        ],
        },

"ru": {
        "titulo": "A1ELOS Global Numerology",
        "subtitulo": "Наука чисел, применённая к вашему успеху",
        "capa_nota": "Стратегическая презентация для инвесторов и партнёров",
        "confidencial": "КОНФИДЕНЦИАЛЬНО",
        "ano": "2026",
        "sumario_titulo": "Резюме для руководителей",
        "duns_porque": "Почему важен DUNS?",
        "preco_consciente": "Осознанное ценообразование",
        "idioma_col": "Язык",
        "falantes_col": "Носители (млн)",
        "linhas_idiomas": [
           ["Английский", "1.528"],
           ["Мандарин", "1.184"],
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
        "grafico_anos": ["1 год", "3 год", "5 год"],
        "grafico_titulo": "Консервативный прогноз (R$ тыс.)",
        "grafico_titulo_linha": "Прогнозируемый рост (R$ тыс.)",
        "fale_conosco": "Свяжитесь с нами",
        "sumario_intro": "Эта презентация структурирована так, чтобы провести инвесторов и партнёров по всем стратегическим аспектам A1ELOS Global Numerology — от рыночной концепции до модели повторяющегося дохода.",
        "sumario_cards": [
            ("01", "Об A1ELOS", "Холдинг, портфель и аккредитация DUNS"),
            ("02", "Рыночная возможность", "Мировая экономика благополучия US$ 6,8 трлн"),
            ("03", "Решение и глобальный охват", "14 языков, ~5,3 млрд носителей"),
            ("04", "Новые рынки", "Индонезия, Турция, Вьетнам и корпоративное HR"),
            ("05", "Портфель и цены", "24 продукта, откалиброванных по покупательной способности"),
            ("06", "Повторяющийся доход", "Рекламные баннеры и B2B-пакеты"),
            ("07", "Прогнозы и инвестиции", "Горизонт 50 лет · Посевной раунд R$ 3,5 млн"),
        ],
        "sobre_titulo": "Об A1ELOS",
        "sobre_texto": "A1ELOS — технологический и интеллектуальный холдинг, объединяющий искусственный интеллект, прикладную нумерологию и культурную стратегию для создания цифровых продуктов с высоким эффектом в глобальном масштабе. Наша миссия: демократизировать цифровое самопознание с уважением к культуре и покупательной способности каждого рынка.",
        "sobre_kpis": [
            ("23", "Активных продуктов", "На 4 уровнях доступа"),
            ("14", "языков", "~67% населения мира"),
            ("5,3 млрд", "носителей", "Реальный адресуемый рынок"),
            ("ИИ", "Интегрирован", "Движок персонализации"),
        ],
        "sobre_duns": "DUNS 942242668 — Сертификация Dun & Bradstreet, действующая в 190+ странах, обеспечивающая B2B-контракты и международные совместные предприятия.",
        "duns_titulo": "Международная надёжность",
        "duns_texto": "Номер DUNS — это корпоративный паспорт A1ELOS на международной арене. Он сигнализирует партнёрам, корпоративным клиентам и инвесторам, что компания обладает проверяемой идентичностью, отслеживаемой историей и договорной способностью в любой юрисдикции.",
        "duns_numero": "942242668",
        "duns_emitido": "Выдан Dun & Bradstreet — мировым стандартом деловой идентичности, признанным более чем в 190 странах.",
        "duns_paises": "190+ СТРАН",
        "duns_beneficios": [
            ("B2B-контракты", "Право участия в международных тендерах и поставках"),
            ("Совместные предприятия", "Международные партнёрства с упрощённой процедурой due diligence"),
            ("Мгновенная надёжность", "Признак серьёзности для институциональных инвесторов"),
        ],
        "mercado_titulo": "Рыночная возможность",
        "mercado_texto": "Мы живём в идеальной конвергенции: цифровое благополучие взрывается в мире, а нумерология и астрология переходят в приложения с высоким вовлечением. A1ELOS находится точно на этом пересечении: 74% населения мира уже онлайн (~6 миллиардов человек).",
        "mercado_cards": [
            ("Глобальное благополучие", "US$ 6,8 трлн → US$ 9,8 трлн к 2029 (+7,6% в год)"),
            ("Приложения астрологии/нумерологии", "US$ 3 млрд → US$ 9 млрд к 2030 · CAGR 20%"),
            ("Приложения благополучия", "CAGR 14,9% → US$ 26,2 млрд в 2030"),
            ("Пользователи онлайн", "74% мира · ~6 миллиардов человек"),
        ],
        "mercado_rh_titulo": "Новый рынок: корпоративное HR — 24-й продукт",
        "mercado_rh_texto": "24-й продукт — Совместимость команд HR (R$ 98) — открывает главный B2B-рынок A1ELOS: корпоративное HR. Анализ энергетической совместимости между руководителями и сотрудниками (идеальная энергия: число 8) позиционирует платформу как новаторский инструмент employer branding и корпоративного благополучия, с прогрессивными скидками от 10% до 50% и прямыми переговорами свыше 2.000 кодов (план «Бриллиант»).",
        "mercado_rh_vantagens": [
            "Энергетическая гармония отдела → меньше межличностных трений и выше сплочённость команды",
            "Согласование позиций и мыслей между руководителями и сотрудниками → более плавная коммуникация",
            "Снижение текучести кадров и более высокая удержание талантов",
            "Позитивный организационный климат → рост продуктивности и благополучия",
            "Усиленный employer branding → привлечение талантов, соответствующих культуре",
        ],
        "mercado_rh_cards": [
            ["HR Tech", "US$ 42,34 млрд (2025) → US$ 77,74 млрд (2031)", "CAGR 10,35% · Mordor Intelligence"],
            ["Employer Branding", "US$ 1,89 млрд (2025) → US$ 3,62 млрд (2031)", "CAGR 11,19% · Mordor Intelligence"],
            ["Corporate Wellness", "US$ 66,31 млрд (2025) → US$ 94,5 млрд (2031)", "CAGR 6,12% · Mordor Intelligence"],
        ],
        "problema_titulo": "Проблема, которую мы решаем",
        "problema_col_esq_titulo": "Недостатки текущего рынка",
        "problema_col_esq": [
            ("Языковой барьер", "Подавляющее большинство нумерологических инструментов работает только на английском, исключая миллиарды носителей других языков."),
            ("Цены, оторванные от реальности", "Продукты, оцениваемые в долларах для развивающихся рынков, создают экономическое исключение — пользователь отвергает не продукт, а недоступную цену."),
            ("Отсутствие глубины", "Универсальные инструменты дают поверхностные ответы без персонализации, без культурного контекста и без практического применения в повседневной жизни."),
        ],
        "problema_col_dir_titulo": "Цена исключения",
        "problema_col_dir": "Когда платформа игнорирует язык и покупательную способность, она добровольно отказывается от крупнейшего рынка мира: более 4 миллиардов человек, живущих в развивающихся экономиках и говорящих на неанглоязычных языках. Именно эту нишу A1ELOS занимает с хирургической точностью.",
        "problema_destaque": "Платформы, игнорирующие местную покупательную способность, теряют доступ к более чем 60% глобального адресуемого рынка.",
        "solucao_titulo": "Наше решение: 3 стратегические опоры",
        "solucao_texto": "A1ELOS построила интегрированную платформу, сочетающую науку чисел, искусственный интеллект и культурную чувствительность. Решение работает на трёх взаимодополняющих фронтах, обеспечивая диверсифицированный доход и высокую удержание.",
        "solucao_colunas": [
            ("Личные карты", "Глубокий персонализированный числовой анализ для конечного пользователя — идентичность, миссия, жизненные циклы и совместимость — на 14 языках с интегрированным ИИ."),
            ("Бизнес-нумерология", "Нумерологическая диагностика брендов, CNPJ, дат основания и корпоративной стратегии. Дифференцированный продукт с высокой воспринимаемой ценностью на B2B-рынке."),
            ("White-Label B2B", "Лицензирование платформы для компаний-партнёров, желающих предлагать нумерологию под собственным брендом — с многоязычной поддержкой и полной настройкой."),
        ],
        "alcance_titulo": "Глобальный охват: 14 языков · ~5,3 млрд носителей",
        "alcance_texto": "A1ELOS охватывает ~67% населения мира поистине многоязычной платформой. Каждый язык представляет отдельный культурный рынок с ценами, откалиброванными по местной покупательной способности.",
        "mercados_titulo": "3 новых рынка: +442 млн носителей",
        "mercados_texto": "Стратегическая экспансия в Индонезию, Турцию и Вьетнам — качественный скачок: рынки с высоким экономическим ростом, растущим цифровым проникновением и подтверждённым спросом на доступные цифровые решения для благополучия.",
        "mercados_cards": [
            ("Индонезия", ["285 млн жителей", "80,5% проникновение интернета", "~255 млн носителей индонезийского", "Благополучие: US$ 51,2 млрд (2025) → US$ 72,8 млрд (2034)"]),
            ("Турция", ["85,9 млн жителей", "ВВП ППС на душу населения US$ 37.301", "~90 млн носителей турецкого", "Выше мирового среднего (US$ 27.211)"]),
            ("Вьетнам",  ["~100 млн жителей", "ВВП на душу ~US$ 5.066 (+7,4%/год)", "~97 млн носителей вьетнамского", "Благополучие: US$ 303 млн (2025) → US$ 485 млн (2030)"]),
        ],
        "mercados_rodape": "3 новых рынка = +442 млн новых адресуемых носителей — интегрированы в платформу с культурно откалиброванным ценообразованием.",
        "preco_titulo": "Философия осознанного ценообразования",
        "preco_esq": "Культурное уважение + уважение к покупательной способности = реальный адресуемый рынок. Та же пропорция ценности. Разные цены. Равное достоинство для всех рынков.",
        "preco_dir_titulo": "Как это работает на практике",
        "preco_dir": "A1ELOS применяет паритет покупательной способности (ППС) как центральный критерий ценообразования. Один и тот же продукт приносит одинаковую относительную ценность пользователю в Лагосе, Джакарте, Ханое или Нью-Йорке — цена откалибрована так, чтобы финансовое усилие было пропорционально местному доходу.",
        "preco_pilares": [
            ("Калибровка по ППС", "Цены, скорректированные по индексу покупательной способности каждой страны"),
            ("Культурное уважение", "Язык, валюта и местный контекст интегрированы в продукт"),
            ("Превосходная конверсия", "Справедливая цена даёт больше конверсий и более высокую долгосрочную удержание"),
        ],
        "portfolio_titulo": "Портфель: 24 продукта на 4 уровнях",
        "portfolio_texto": "Многоуровневая структура гарантирует, что каждый профиль пользователя — от любопытного до профессионала — найдёт предложение, соответствующее уровню вовлечённости и финансовым возможностям.",
        "portfolio_tabela": [
           ["Уровень", "Продукты", "Ценовой диапазон (R$)", "Профиль"],
           ["Базовый", "Экспресс-карта, Полная карта", "R$ 8 – 17", "Любопытный, первый контакт"],
           ["Средний", "Поиск ИИ, Имя для бюллетеня, № избирателя", "R$ 26 – 53", "Вовлечённый пользователь"],
           ["Продвинутый", "Имя НКО, Артистическое имя, Имя ребёнка, Подпись, Имя бизнеса", "R$ 35 – 44", "Профессионал, предприниматель"],
           ["Премиум", "Карта пары, Семейная карта, Совместимость команд HR ★, Коллективный бонус", "R$ 98", "Высокий доход, корпоративное использование"],
           ["B2B", "Корпоративные пакеты, лицензии, подарки", "По запросу", "Компании и команды"],
        ],
        "portfolio_rodape": "24 продукта покрывают весь путь пользователя, от первого контакта до повторного премиум-клиента — максимальный LTV на каждый язык и рынок. Главное: Совместимость команд HR (R$ 98) — новаторский продукт на рынке корпоративного HR, идеальная энергия 8.",
        "negocio_titulo": "Бизнес-модель: 3 источника дохода",
        "negocio_texto": "A1ELOS спроектирован с диверсифицированным и масштабируемым доходом: прямые продажи конечному потребителю в глобальном масштабе, B2B-контракты высокой ценности и повторяющаяся геолокализованная реклама — три двигателя, которые взаимно питают друг друга.",
        "negocio_colunas": [
            ("B2C — 14 языков", "Прямые продажи цифровых продуктов во всех валютах с ценами, адаптированными по ППС. Автоматическое масштабирование через ИИ — без команды поддержки, пропорциональной росту."),
            ("B2B — Прогрессивные скидки", "Корпоративные пакеты для HR, employer branding и институциональных подарков. Скидки от 10% до 50% в зависимости от объёма. Свыше 2.000 кодов — прямые переговоры (план «Бриллиант»). Контракты обеспечены DUNS 942242668."),
            ("Геолокализованная реклама", "Баннеры с сегментацией по стране, континенту или миру с автоматической ротацией. Высокий ежемесячный повторяющийся доход — без зависимости от объёма продаж продуктов."),
        ],
        "banners_titulo": "Рекламные баннеры — ежемесячный повторяющийся доход",
        "banners_texto": "Платформа A1ELOS предлагает премиальные рекламные площади с точной геолокационной сегментацией — страна, континент или мир. С автоматической ротацией каждые 8 секунд и форматами, оптимизированными для десктопа и мобильных, баннеры обеспечивают измеримую видимость региональным и международным рекламодателям.",
        "banners_tabela": [
            ["Сегментация", "Фикс (R$/мес)", "Временный (R$/мес)", "Профиль рекламодателя"],
            ["Страна", "R$ 800", "R$ 500", "Местный МСБ, региональная торговля"],
            ["Континент", "R$ 1.800", "R$ 1.200", "Региональные бренды, континентальная экспансия"],
            ["Мир", "R$ 3.500", "R$ 2.500", "Глобальные компании, международные приложения"],
            ["Эксклюзивное спонсорство", "R$ 6.000", "R$ 4.500/кампания", "Главные спонсоры, запуски"],
        ],
        "banners_formatos": "728×90 px — центральный десктоп-баннер · 320×100 px — оптимизированный мобильный формат · 8 секунд — автоматическая ротация · Гео-таргетинг — страна, континент или мировой охват",
        "b2b_titulo": "B2B-пакеты для бизнеса — высокая ценность, большой объём",
        "b2b_texto": "B2B-пакеты превращают A1ELOS в инструмент employer branding и корпоративного благополучия. В центре этой стратегии — эксклюзивный непрерывный продукт: Совместимость команд HR (R$ 98). В отличие от разовых подарков, анализ совместимости — это инструмент управления персоналом, который компания встраивает в повседневную деятельность — рассчитывая отделы и команды с желаемой энергией и синхронизируя всех членов отдела в одной тональности и гармонии. Идеален для малых и крупных компаний, это услуга, которую Отдел кадров использует постоянно, опираясь на быстрорастущие рынки: HR Tech (CAGR 10,35%), Employer Branding (CAGR 11,19%) и Corporate Wellness (CAGR 6,12%).",
        "b2b_planos": [
            ("Базовый план · 50 кодов", "50× Экспресс-карта (по R$ 8). Идеально для программ льгот сотрудникам и интеграционных мероприятий."),
            ("Средний план · 100 кодов", "50× Экспресс-карта + 50× Поиск ИИ (R$ 17). Идеально для команд и стратегии employer branding."),
            ("Премиум план · 200 кодов", "100× Экспресс-карта + 100× Полная карта (R$ 17). Максимальная аналитическая глубина для больших групп."),
        ],
        "b2b_tabela": [
            ["От", "Скидка", "Профиль", "Рекомендуемое использование"],
            ["10 кодов", "10%", "Небольшие команды", "Разовое мероприятие благополучия"],
            ["50 кодов", "20%", "Растущие команды", "Повторяющиеся программы"],
            ["100 кодов", "25%", "МСБ", "Ежеквартальная льгота"],
            ["200 кодов", "30%", "Средние компании", "Полные программы"],
            ["500 кодов", "40%", "Средние компании", "Ежегодный подарок сотрудникам"],
            ["1.000 кодов", "45%", "Крупные корпорации", "Лояльность клиентов"],
            ["2.000 кодов", "50%", "Крупные группы", "Большой масштаб"],
            ["Свыше 2.000", "Договорно", "Индивидуальный план «Бриллиант»", "Массовое распределение бонусов"],
        ],
        "rh_destaque_titulo": "Совместимость команд HR — эксклюзивный продукт",
        "rh_destaque_texto": "Анализ энергетической совместимости между руководителями и сотрудниками, а также между членами одной команды (идеальная энергия: число 8 — власть, лидерство и материальный баланс) позиционирует A1ELOS как пионера на рынке корпоративного HR. Энергетическая гармония отдела снижает межличностные трения, согласует позиции и мысли, уменьшает текучесть кадров, укрепляет организационный климат и повышает продуктивность — ценность, которую Коллективный бонус как разовый подарок не даёт. Именно этот продукт поддерживает краткосрочный рост и повторяющийся B2B-доход.",
        "projecoes_titulo": "Финансовые прогнозы: горизонт 50 лет",
        "projecoes_texto": "Прогнозы построены на процентных оценках проникновения по потенциальному рынку ~5,32 млрд носителей, с консервативной конверсией 3% и погашением бонусов между 70% и 90%. С 24-м продуктом — Совместимость команд HR (R$ 98) и каналом Коллективный/Корпоративный бонус — B2B-доход HR включается в прогноз, опирающийся на проверенные рынки: HR Tech (CAGR 10,35%), Employer Branding (CAGR 11,19%) и Corporate Wellness (CAGR 6,12%). Краткосрочный период (годы 1–5) отражает ускоренный рост нового B2B-фронта; долгосрочный — непрерывную стабильность модели до полного усвоения адресуемого рынка.",
        "projecoes_tabela": [
            ["Горизонт", "Консервативный (R$)", "Оптимистичный (R$)"],
            ["1 год", "R$ 318k", "R$ 810k"],
            ["2 год", "R$ 630k", "R$ 1,8M"],
            ["3 год", "R$ 1,20M", "R$ 3,50M"],
            ["4 год", "R$ 2,2M", "R$ 6,2M"],
            ["5 год", "R$ 3,70M", "R$ 9,6M"],
        ],
        "projecoes_tabela_50": [
            ["Горизонт", "Консервативный (R$)", "Оптимистичный (R$)"],
            ["1 год", "R$ 318k", "R$ 810k"],
            ["3 год", "R$ 1,20M", "R$ 3,50M"],
            ["5 год", "R$ 3,70M", "R$ 9,6M"],
            ["7 год", "R$ 7,8M", "R$ 20,5M"],
            ["10 год", "R$ 16,3M", "R$ 44,0M"],
            ["20 год", "R$ 64M", "R$ 184M"],
            ["30 год", "R$ 133M", "R$ 359M"],
            ["40 год", "R$ 202M", "R$ 606M"],
            ["50 год", "R$ 276M", "R$ 869M"],
        ],
        "projecoes_curto_titulo": "Финансовые прогнозы: краткосрочный период (годы 1–5)",
        "projecoes_curto_texto": "Краткосрочный период отражает ускоренный рост нового B2B-фронта HR (Совместимость команд + Коллективный бонус) — почти 12x за 5 лет в консервативном сценарии — до долгосрочной стабилизации.",
        "projecoes_curto_tabela": [
            ["Горизонт", "Консервативный (R$)", "Оптимистичный (R$)"],
            ["1 год", "R$ 318k", "R$ 810k"],
            ["2 год", "R$ 630k", "R$ 1,8M"],
            ["3 год", "R$ 1,20M", "R$ 3,50M"],
            ["4 год", "R$ 2,2M", "R$ 6,2M"],
            ["5 год", "R$ 3,70M", "R$ 9,6M"],
         ],
        "tracao_titulo": "Тяга и подтверждённые результаты",
        "tracao_texto": "A1ELOS уже работает с продуктовыми метриками, валидирующими модель — высокая удержание, премиальный рейтинг и растущая база B2B-партнёров доказывают, что платформа приносит реальную ценность конечному пользователю и корпоративному рынку.",
        "tracao_kpis": [
            ("12K+", "Активных пользователей", "Органическая база в устойчивом росте"),
            ("87%", "Удержание", "Намного выше среднего по отрасли (~30%)"),
            ("4,8★", "Средний рейтинг", "Подтверждённая удовлетворённость конечных пользователей"),
            ("23", "B2B-партнёра", "Активные контракты с компаниями и отделами HR"),
        ],
        "roteiro_titulo": "Стратегическая дорожная карта",
        "roteiro_texto": "A1ELOS реализует план в четыре прогрессивных этапа — от консолидации текущей базы до глобального лидерства на рынке, с чёткими вариантами выхода для инвесторов.",
        "roteiro_fases": [
            ("Этап 1 · Консолидация", "Укрепление базы пользователей на уже активных языках. Оптимизация конверсии, удержания и LTV. Посевной раунд завершён."),
            ("Этап 2 · Экспансия", "Официальный запуск на 3 новых рынках: Индонезия, Турция и Вьетнам. Ускорение B2B-канала и геолокализованной рекламы."),
            ("Этап 3 · Глобальный вход", "Активное присутствие на всех 14 языках с локализованными кампаниями. White-label партнёрства на 5+ континентах. Серия A."),
            ("Этап 4 · Лидерство", "20+ стран с консолидированными операциями. Глобальная эталонная SaaS-платформа в прикладной нумерологии. IPO или стратегический выход."),
        ],
        "invest_titulo": "Инвестиции и контакты",
        "invest_texto": "Мы готовы к частным презентациям, due diligence и переговорам. Свяжитесь с нами удобным для вас каналом.",
        "invest_dados": [
            ("Посевной раунд", "R$ 3,5 млн"),
            ("Оценка Pre-Money", "R$ 14 млн"),
            ("Предлагаемая доля", "До 20%"),
        ],
        "invest_contato": [
            ("Эл. почта инвесторов", "a1elos.consultoria@gmail.com"),
            ("Общая эл. почта", "contato@a1elos.com"),
            ("Веб-сайт", "www.a1elos.com"),
            ("DUNS", "942242668 — Dun & Bradstreet"),
        ],
        "invest_alocacao": "Распределение капитала: 45% технологии · 30% маркетинг · 25% операции",
        "frase_final": "Числа никогда не лгут.",
        "selo_final": ["DUNS 942242668", "24 ПРОДУКТА", "14 ЯЗЫКОВ", "~5,3 МЛРД НОСИТЕЛЕЙ"],
        "graf_cons": "Консервативный",
        "graf_otim": "Оптимистичный",
        "grafico_titulo_linha": "Прогнозируемый рост (R$ тыс.)",
        "pix_titulo": "Бразилия: инфраструктура Pix",
        "pix_texto": "Pix — это государственная инфраструктура мгновенных платежей Бразилии. Для A1ELOS она гарантирует немедленное получение средств, низкую стоимость и универсальное признание — основу B2C-операции на бразильском рынке и ворота в международную экспансию.",
        "pix_kpis": [
            ("30,1 млрд", "транзакций в 2025", "+20% к 2024 · Febraban"),
            ("76,4%", "населения использует Pix", "211 миллионов бразильцев · Центробанк"),
            ("R$ 68,2 трлн", "переведено во 2-м полугодии 2025", "78,4 млрд транзакций · Центробанк"),
            ("~80 млрд", "транзакций в 2025", "+25,7% к прошлому году · отчёт Pix"),
        ],
        "pix_fonte": "Источники: Центральный банк Бразилии (Pix в цифрах) и Febraban (исследование банковских технологий).",
        "ref_titulo": "Библиографические ссылки",
        "ref_intro": "Источники, использованные для рыночных данных, прогнозов и показателей этой презентации.",
        "ref_lista": [
            ("Global Wellness Institute", "Мировая экономика благополучия: US$ 6,8 трлн (2024) → US$ 9,8 трлн (2029)."),
            ("MarkNtel Advisors", "Приложения астрологии и нумерологии: US$ 3 млрд → US$ 9 млрд к 2030 (CAGR ~20%)."),
            ("МВФ · Всемирный банк", "ВВП и паритет покупательной способности (ППС) по странам."),
            ("Центральный банк Бразилии", "Официальная статистика Pix: транзакции, объём и пользователи."),
            ("Febraban", "Исследование банковских технологий — рост Pix в 2025."),
            ("IBGE", "Население и социально-экономические показатели Бразилии."),
        ],
        },           

"he": {
        "titulo": "A1ELOS Global Numerology",
        "subtitulo": "מדע המספרים מוחל על ההצלחה שלך",
        "capa_nota": "מצגת אסטרטגית למשקיעים ולשותפים",
        "confidencial": "חסוי",
        "ano": "2026",
        "sumario_titulo": "סיכום מנהלים",
        "duns_porque": "למה חשוב ה-DUNS?",
        "preco_consciente": "תמחור מודע",
        "idioma_col": "שפה",
        "falantes_col": "דוברים (מיליון)",
        "linhas_idiomas": [
           ["אנגלית", "1.528"],
           ["מנדרינית", "1.184"],
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
        "b2b_linha": "B2B — הנחות מדורגות",
        "pub_linha": "פרסום גיאו-ממוקד",
        "tabela_descontos": "טבלת הנחות מדורגות",
        "grafico_anos": ["שנה 1", "שנה 3", "שנה 5"],
        "grafico_titulo": "תחזית שמרנית (R$ אלפים)",
        "grafico_titulo_linha": "צמיחה צפויה (R$ אלפים)",
        "fale_conosco": "דברו איתנו",
        "sumario_intro": "מצגת זו בנויה כדי להנחות משקיעים ושותפים בכל ההיבטים האסטרטגיים של A1ELOS Global Numerology — מתזת השוק ועד מודל ההכנסות החוזרות.",
        "sumario_cards": [
            ("01", "על A1ELOS", "אחזקה, תיק מוצרים והסמכת DUNS"),
            ("02", "הזדמנות שוק", "כלכלת הבריאות העולמית US$ 6,8 טריליון"),
            ("03", "פתרון והיקף גלובלי", "14 שפות, ~5,3 מיליארד דוברים"),
            ("04", "שווקים חדשים", "אינדונזיה, טורקיה, וייטנאם ומשאבי אנוש ארגוניים"),
            ("05", "תיק מוצרים ומחירים", "24 מוצרים מכוילים לפי כוח קנייה"),
            ("06", "הכנסות חוזרות", "באנרים פרסומיים וחבילות B2B"),
            ("07", "תחזיות והשקעה", "אופק של 50 שנה · סבב Seed R$ 3,5M"),
        ],
        "sobre_titulo": "על A1ELOS",
        "sobre_texto": "A1ELOS היא חברת אחזקות טכנולוגיה וידע המאחדת בינה מלאכותית, נומרולוגיה יישומית ואסטרטגיה תרבותית כדי ליצור מוצרים דיגיטליים בעלי השפעה גבוהה בקנה מידה עולמי. המשימה שלנו: לדמוקרטיזציה של ידע עצמי נומרי עם כבוד תרבותי וכבוד לכוח הקנייה של כל שוק.",
        "sobre_kpis": [
            ("23", "מוצרים פעילים", "ב-4 רמות גישה"),
            ("14", "שפות", "~67% מאוכלוסיית העולם"),
            ("5,3 מיליארד", "דוברים", "שוק הניתן לכתובת אמיתי"),
            ("AI", "משולב", "מנוע התאמה אישית"),
        ],
        "sobre_duns": "DUNS 942242668 — הסמכת Dun & Bradstreet בתוקף ביותר מ-190 מדינות, המאפשרת חוזי B2B ומיזמים משותפים בינלאומיים.",
        "duns_titulo": "אמינות בינלאומית",
        "duns_texto": "מספר ה-DUNS הוא הדרכון הארגוני של A1ELOS על הבמה הבינלאומית. הוא מאותת לשותפים, ללקוחות ארגוניים ולמשקיעים שלחברה יש זהות הניתנת לאימות, היסטוריה הניתנת למעקב ויכולת חוזית בכל תחום שיפוט.",
        "duns_numero": "942242668",
        "duns_emitido": "הונפק על ידי Dun & Bradstreet — התקן העולמי לזהות עסקית המוכר ביותר מ-190 מדינות.",
        "duns_paises": "190+ מדינות",
        "duns_beneficios": [
            ("חוזי B2B", "הסמכה למכרזים ולספקים גלובליים"),
            ("מיזמים משותפים", "שותפויות בינלאומיות עם due diligence מקל"),
            ("אמינות מיידית", "סימן רצינות למשקיעים מוסדיים"),
        ],
        "mercado_titulo": "הזדמנות שוק",
        "mercado_texto": "אנו חיים בהתכנסות מושלמת: הבריאות הדיגיטלית מתפוצצת ברחבי העולם בעוד נומרולוגיה ואסטרולוגיה עוברות לאפליקציות בעלות מעורבות גבוהה. A1ELOS ממוקמת בדיוק בצומת הזה, עם 74% מאוכלוסיית העולם כבר מקוונת (~6 מיליארד אנשים).",
        "mercado_cards": [
            ("בריאות גלובלית", "US$ 6,8 טריליון → US$ 9,8 טריליון עד 2029 (שיעור שנתי +7,6%)"),
            ("אפליקציות אסטרולוגיה/נומרולוגיה", "US$ 3 מיליארד → US$ 9 מיליארד עד 2030 · CAGR 20%"),
            ("אפליקציות בריאות", "CAGR 14,9% → US$ 26,2 מיליארד ב-2030"),
            ("משתמשים מקוונים", "74% מהעולם · ~6 מיליארד אנשים"),
        ],
        "mercado_rh_titulo": "שוק חדש: משאבי אנוש ארגוניים — המוצר ה-24",
        "mercado_rh_texto": "המוצר ה-24 — תאימות צוותים HR (R$ 98) — פותח את השוק המרכזי של A1ELOS ב-B2B: משאבי אנוש ארגוניים. ניתוח התאימות האנרגטית בין מנהלים לעובדים (אנרגיה אידיאלית: מספר 8) ממקם את הפלטפורמה ככלי חלוצי של מיתוג מעסיק ורווחה ארגונית, עם הנחות מדורגות של 10% עד 50% ומשא ומתן ישיר מעל 2.000 קודים (תוכנית היהלום).",
        "mercado_rh_vantagens": [
            "הרמוניה אנרגטית של המחלקה → פחות חיכוכים בין אישיים וקוהזיה גבוהה יותר של הצוות",
            "יישור עמדות ומחשבות בין מנהלים לעובדים → תקשורת זורמת יותר",
            "תחלופת עובדים נמוכה יותר ושימור כישרונות גבוה יותר",
            "אקלים ארגוני חיובי → רווח בפריון וברווחה",
            "מיתוג מעסיק מחוזק → משיכת כישרונות המותאמים לתרבות",
        ],
        "mercado_rh_cards": [
            ["HR Tech", "US$ 42,34 מיליארד (2025) → US$ 77,74 מיליארד (2031)", "CAGR 10,35% · Mordor Intelligence"],
            ["Employer Branding", "US$ 1,89 מיליארד (2025) → US$ 3,62 מיליארד (2031)", "CAGR 11,19% · Mordor Intelligence"],
            ["Corporate Wellness", "US$ 66,31 מיליארד (2025) → US$ 94,5 מיליארד (2031)", "CAGR 6,12% · Mordor Intelligence"],
        ],
        "problema_titulo": "הבעיה שאנחנו פותרים",
        "problema_col_esq_titulo": "כשלי השוק הנוכחי",
        "problema_col_esq": [
            ("מחסום שפה", "הרוב המכריע של כלי הנומרולוגיה פועל רק באנגלית, ומדיר מיליארדי דוברי שפת אם של שפות אחרות."),
            ("מחירים מנותקים מהמציאות", "מוצרים המתומחרים בדולרים עבור שווקים מתפתחים יוצרים הדרה כלכלית — המשתמש לא דוחה את המוצר, הוא דוחה את המחיר הבלתי ניתן להשגה."),
            ("חוסר עומק", "כלים גנריים מספקים תשובות שטחיות ללא התאמה אישית, ללא הקשר תרבותי וללא יישום מעשי בחיי היומיום."),
        ],
        "problema_col_dir_titulo": "המחיר של ההדרה",
        "problema_col_dir": "כאשר פלטפורמה מתעלמת משפה ומכוח קנייה, היא נוטשת מרצונה את השוק הגדול בעולם: יותר מ-4 מיליארד אנשים החיים בכלכלות מתפתחות ומדברים שפות שאינן אנגלית. זהו הפער ש-A1ELOS תופסת בדייקנות כירורגית.",
        "problema_destaque": "פלטפורמות שמתעלמות מכוח קנייה מקומי מאבדות גישה ליותר מ-60% מהשוק הגלובלי הניתן לכתובת.",
        "solucao_titulo": "הפתרון שלנו: 3 עמודי תווך אסטרטגיים",
        "solucao_texto": "A1ELOS בנתה פלטפורמה משולבת המשלבת מדע מספרים, בינה מלאכותית ורגישות תרבותית. הפתרון פועל בשלוש חזיתות משלימות, ומבטיח הכנסות מגוונות ושימור גבוה.",
        "solucao_colunas": [
            ("מפות אישיות", "ניתוחים מספריים עמוקים ומותאמים אישית למשתמש הקצה — זהות, ייעוד, מחזורי חיים ותאימות — המועברים ב-14 שפות עם AI משולב."),
            ("נומרולוגיה עסקית", "אבחונים נומרולוגיים המופעלים על מותגים, CNPJ, תאריכי הקמה ואסטרטגיה ארגונית. מוצר מובחן בעל ערך נתפס גבוה בשוק B2B."),
            ("White-Label B2B", "רישוי הפלטפורמה לחברות שותפות המעוניינות להציע נומרולוגיה תחת המותג שלהן — עם תמיכה רב-לשונית והתאמה מלאה."),
        ],
        "alcance_titulo": "היקף גלובלי: 14 שפות · ~5,3 מיליארד דוברים",
        "alcance_texto": "A1ELOS מכסה ~67% מאוכלוסיית העולם עם פלטפורמה רב-לשונית באמת. כל שפה מייצגת שוק תרבותי מובחן, עם מחירים מכוילים לכוח הקנייה המקומי.",
        "mercados_titulo": "3 השווקים החדשים: +442 מיליון דוברים",
        "mercados_texto": "ההתרחבות האסטרטגית לאינדונזיה, טורקיה ווייטנאם מהווה קפיצת מדרגה איכותית: שווקים עם צמיחה כלכלית גבוהה, חדירה דיגיטלית הולכת וגדלה וביקוש מוכח לפתרונות בריאות דיגיטליים נגישים.",
        "mercados_cards": [
            ("אינדונזיה", ["285 מיליון תושבים", "80,5% חדירת אינטרנט", "~255 מיליון דוברי אינדונזית", "בריאות: US$ 51,2 מיליארד (2025) → US$ 72,8 מיליארד (2034)"]),
            ("טורקיה", ["85,9 מיליון תושבים", "תמ\"ג PPP לנפש US$ 37.301", "~90 מיליון דוברי טורקית", "מעל הממוצע העולמי (US$ 27.211)"]),
            ("וייטנאם",  ["~100 מיליון תושבים", "תמ\"ג לנפש ~US$ 5.066 (שיעור שנתי +7,4%)", "~97 מיליון דוברי וייטנאמית", "בריאות: US$ 303 מיליון (2025) → US$ 485 מיליון (2030)"]),
        ],
        "mercados_rodape": "3 שווקים חדשים = +442 מיליון דוברים חדשים הניתנים לכתובת — משולבים בפלטפורמה עם תמחור מכויל תרבותית.",
        "preco_titulo": "הפילוסופיה של תמחור מודע",
        "preco_esq": "כבוד תרבותי + כבוד לכוח קנייה = שוק אמיתי הניתן לכתובת. אותו יחס ערך. מחירים שונים. כבוד שווה לכל השווקים.",
        "preco_dir_titulo": "איך זה עובד בפועל",
        "preco_dir": "A1ELOS מיישמת שוויון כוח קנייה (PPP) כקריטריון מרכזי לתמחור. אותו מוצר מספק אותו ערך יחסי למשתמש בלאגוס, ג'קרטה, האנוי או ניו יורק — המחיר מכויל כך שהמאמץ הכלכלי יהיה פרופורציונלי להכנסה המקומית.",
        "preco_pilares": [
            ("כיול PPP", "מחירים המותאמים למדד כוח הקנייה של כל מדינה"),
            ("כבוד תרבותי", "שפה, מטבע והקשר מקומי משולבים במוצר"),
            ("המרה מעולה", "מחיר הוגן מייצר יותר המרות ושימור גבוה יותר לטווח ארוך"),
        ],
        "portfolio_titulo": "תיק מוצרים: 24 מוצרים ב-4 רמות",
        "portfolio_texto": "המבנה השכבתי מבטיח שכל פרופיל משתמש — מהסקרן ועד המקצועי — ימצא הצעה המתאימה לרמת המעורבות וליכולת הכלכלית שלו.",
        "portfolio_tabela": [
           ["רמה", "מוצרים", "טווח מחירים (R$)", "פרופיל"],
           ["בסיסי", "מפה אקספרס, מפה מלאה", "R$ 8 – 17", "סקרן, קשר ראשון"],
           ["בינוני", "חיפוש AI, שם בקלפי, מספר בוחר", "R$ 26 – 53", "משתמש מעורב"],
           ["מתקדם", "שם לעמותה, שם במה, שם לתינוק, חתימה, שם עסקי", "R$ 35 – 44", "מקצוען, יזם"],
           ["פרימיום", "מפת זוג, מפת משפחה, תאימות צוותים HR ★, בונוס קולקטיבי", "R$ 98", "הכנסה גבוהה, שימוש ארגוני"],
           ["B2B", "חבילות ארגוניות, רישיונות, מתנות", "לפי פנייה", "חברות וצוותים"],
        ],
        "portfolio_rodape": "24 מוצרים מכסים את כל מסע המשתמש, מקשר ראשון ועד לקוח פרימיום חוזר — ממקסמים LTV לכל שפה ושוק. הדגשה: תאימות צוותים HR (R$ 98) — מוצר חלוצי בשוק משאבי האנוש הארגוני, אנרגיה אידיאלית 8.",
        "negocio_titulo": "מודל עסקי: 3 מקורות הכנסה",
        "negocio_texto": "A1ELOS תוכננה עם הכנסות מגוונות וניתנות להרחבה: מכירות ישירות לצרכן הקצה בקנה מידה עולמי, חוזי B2B בעלי ערך גבוה ופרסום גיאו-ממוקד חוזר — שלושה מנועים המזינים זה את זה.",
        "negocio_colunas": [
            ("B2C — 14 שפות", "מכירה ישירה של מוצרים דיגיטליים בכל המטבעות, עם מחירים מותאמים לפי PPP. קנה מידה אוטומטי דרך AI — ללא צוות שירות פרופורציונלי לצמיחה."),
            ("B2B — הנחות מדורגות", "חבילות ארגוניות למשאבי אנוש, מיתוג מעסיק ומתנות מוסדיות. הנחות של 10% עד 50% לפי נפח. מעל 2.000 קודים, משא ומתן ישיר (תוכנית היהלום). חוזים מגובים על ידי DUNS 942242668."),
            ("פרסום גיאו-ממוקד", "באנרים מפולחים לפי מדינה, יבשת או עולם עם רוטציה אוטומטית. הכנסה חוזרת חודשית בעלת ערך גבוה — ללא תלות בנפח מכירות המוצר."),
        ],
        "banners_titulo": "באנרים פרסומיים — הכנסה חוזרת חודשית",
        "banners_texto": "פלטפורמת A1ELOS מציעה שטחי פרסום פרימיום עם פילוח מדויק לפי מיקום גיאוגרפי — מדינה, יבשת או עולם. עם רוטציה אוטומטית כל 8 שניות ופורמטים אופטימליים למחשב ולנייד, הבאנרים מספקים חשיפה מדידה למפרסמים אזוריים ובינלאומיים.",
        "banners_tabela": [
            ["פילוח", "קבוע (R$/חודש)", "זמני (R$/חודש)", "פרופיל מפרסם"],
            ["מדינה", "R$ 800", "R$ 500", "עסקים קטנים ובינוניים מקומיים, מסחר אזורי"],
            ["יבשת", "R$ 1.800", "R$ 1.200", "מותגים אזוריים, התרחבות יבשתית"],
            ["עולם", "R$ 3.500", "R$ 2.500", "חברות גלובליות, אפליקציות בינלאומיות"],
            ["חסות בלעדית", "R$ 6.000", "R$ 4.500/קמפיין", "ספונסרים ראשיים, השקות"],
        ],
        "banners_formatos": "728×90 px — באנר מרכזי למחשב · 320×100 px — פורמט נייד אופטימלי · 8 שניות — רוטציה אוטומטית · מיקוד גיאוגרפי — מדינה, יבשת או היקף עולמי",
        "b2b_titulo": "חבילות B2B עסקיות — ערך גבוה, נפח גבוה",
        "b2b_texto": "חבילות ה-B2B הופכות את A1ELOS לכלי של מיתוג מעסיק ורווחה ארגונית. במרכז האסטרטגיה הזו עומד המוצר הבלעדי והרציף: תאימות צוותים HR (R$ 98). בניגוד למתנות חד-פעמיות, ניתוח התאימות הוא כלי ניהול אנשים שהחברה משלבת בשגרת יומה — מחשבת מחלקות וצוותים עם האנרגיה הרצויה ומסנכרנת את כל חברי המחלקה באותה תדר והרמוניה. אידיאלי לחברות קטנות וגדולות, זהו השירות שמחלקת משאבי האנוש משתמשת בו באופן קבוע, הנתמך בשווקים בצמיחה גבוהה: HR Tech (CAGR 10,35%), Employer Branding (CAGR 11,19%) ו-Corporate Wellness (CAGR 6,12%).",
        "b2b_planos": [
            ("תוכנית בסיסית · 50 קודים", "50× מפה אקספרס (R$ 8 כל אחת). אידיאלית לתוכניות הטבות לעובדים ולפעולות קליטה."),
            ("תוכנית בינונית · 100 קודים", "50× מפה אקספרס + 50× חיפוש AI (R$ 17). מושלמת לצוותים ולאסטרטגיית מיתוג מעסיק."),
            ("תוכנית פרימיום · 200 קודים", "100× מפה אקספרס + 100× מפה מלאה (R$ 17). עומק אנליטי מקסימלי לקבוצות גדולות."),
        ],
        "b2b_tabela": [
            ["החל מ-", "הנחה", "פרופיל", "שימוש מומלץ"],
            ["10 קודים", "10%", "צוותים קטנים", "פעולת בריאות חד-פעמית"],
            ["50 קודים", "20%", "צוותים גדלים", "תוכניות חוזרות"],
            ["100 קודים", "25%", "SME", "הטבה רבעונית"],
            ["200 קודים", "30%", "חברות בינוניות", "תוכניות מלאות"],
            ["500 קודים", "40%", "חברות בינוניות", "מתנה שנתית לעובדים"],
            ["1.000 קודים", "45%", "תאגידים גדולים", "נאמנות לקוחות"],
            ["2.000 קודים", "50%", "קבוצות גדולות", "קנה מידה רחב"],
            ["מעל 2.000", "ניתן למשא ומתן", "תוכנית יהלום מותאמת", "חלוקת בונוסים בכמות"],
        ],
        "rh_destaque_titulo": "תאימות צוותים HR — המוצר הבלעדי",
        "rh_destaque_texto": "ניתוח התאימות האנרגטית בין מנהלים לעובדים, ובין חברי אותה צוות (אנרגיה אידיאלית: מספר 8 — כוח, מנהיגות ואיזון חומרי), ממקם את A1ELOS כחלוצה בשוק משאבי האנוש הארגוני. ההרמוניה האנרגטית של המחלקה מפחיתה חיכוכים בין אישיים, מיישרת עמדות ומחשבות, מקטינה את תחלופת העובדים, מחזקת את האקלים הארגוני ומעלה את הפריון — ערך שהבונוס הקולקטיבי, כמתנה חד-פעמית, אינו מספק. זהו המוצר התומך בצמיחה לטווח קצר ובהכנסות B2B חוזרות.",
        "projecoes_titulo": "תחזיות פיננסיות: אופק של 50 שנה",
        "projecoes_texto": "התחזיות נבנו על בסיס הערכות אחוזי חדירה על השוק הפוטנציאלי של ~5,32 מיליארד דוברים, עם המרה שמרנית של 3% ופדיון בונוסים בין 70% ל-90%. עם המוצר ה-24 — תאימות צוותים HR (R$ 98) וערוץ הבונוס הקולקטיבי/ארגוני —, הכנסות ה-B2B של משאבי אנוש נכללות בתחזית, המעוגנת בשווקים מאומתים: HR Tech (CAGR 10,35%), Employer Branding (CAGR 11,19%) ו-Corporate Wellness (CAGR 6,12%). הטווח הקצר (שנים 1–5) מדגיש את הצמיחה המואצת של החזית B2B החדשה; הטווח הארוך משקף את היציבות הרציפה של המודל עד להטמעה מלאה של השוק הניתן לכתובת.",
        "projecoes_tabela": [
            ["אופק", "שמרני (R$)", "אופטימי (R$)"],
            ["שנה 1", "R$ 318k", "R$ 810k"],
            ["שנה 2", "R$ 630k", "R$ 1,8M"],
            ["שנה 3", "R$ 1,20M", "R$ 3,50M"],
            ["שנה 4", "R$ 2,2M", "R$ 6,2M"],
            ["שנה 5", "R$ 3,70M", "R$ 9,6M"],
        ],
        "projecoes_tabela_50": [
            ["אופק", "שמרני (R$)", "אופטימי (R$)"],
            ["שנה 1", "R$ 318k", "R$ 810k"],
            ["שנה 3", "R$ 1,20M", "R$ 3,50M"],
            ["שנה 5", "R$ 3,70M", "R$ 9,6M"],
            ["שנה 7", "R$ 7,8M", "R$ 20,5M"],
            ["שנה 10", "R$ 16,3M", "R$ 44,0M"],
            ["שנה 20", "R$ 64M", "R$ 184M"],
            ["שנה 30", "R$ 133M", "R$ 359M"],
            ["שנה 40", "R$ 202M", "R$ 606M"],
            ["שנה 50", "R$ 276M", "R$ 869M"],
        ],
        "projecoes_curto_titulo": "תחזיות פיננסיות: טווח קצר (שנים 1–5)",
        "projecoes_curto_texto": "הטווח הקצר מדגיש את הצמיחה המואצת של החזית B2B החדשה של משאבי אנוש (תאימות צוותים + בונוס קולקטיבי), כמעט פי 12 ב-5 שנים בתרחיש השמרני — לפני היציבות של הטווח הארוך.",
        "projecoes_curto_tabela": [
            ["אופק", "שמרני (R$)", "אופטימי (R$)"],
            ["שנה 1", "R$ 318k", "R$ 810k"],
            ["שנה 2", "R$ 630k", "R$ 1,8M"],
            ["שנה 3", "R$ 1,20M", "R$ 3,50M"],
            ["שנה 4", "R$ 2,2M", "R$ 6,2M"],
            ["שנה 5", "R$ 3,70M", "R$ 9,6M"],
         ],
        "tracao_titulo": "מומנטום ותוצאות מוכחות",
        "tracao_texto": "A1ELOS כבר פועלת עם מדדי מוצר המאמתים את המודל — שימור גבוה, דירוג פרימיום ובסיס גדל של שותפי B2B מוכיחים שהפלטפורמה מספקת ערך אמיתי למשתמש הקצה ולשוק הארגוני.",
        "tracao_kpis": [
            ("12K+", "משתמשים פעילים", "בסיס אורגני בצמיחה עקבית"),
            ("87%", "שימור", "הרבה מעל ממוצע התעשייה (~30%)"),
            ("4,8★", "דירוג ממוצע", "שביעות רצון מוכחת של המשתמש הקצה"),
            ("23", "שותפי B2B", "חוזים פעילים עם חברות ומחלקות משאבי אנוש"),
        ],
        "roteiro_titulo": "מפת דרכים אסטרטגית",
        "roteiro_texto": "A1ELOS מבצעת תוכנית בארבעה שלבים מתקדמים — מגיבוש הבסיס הנוכחי ועד למנהיגות השוק הגלובלית, עם אפשרויות יציאה ברורות למשקיעים.",
        "roteiro_fases": [
            ("שלב 1 · גיבוש", "חיזוק בסיס המשתמשים בשפות הפעילות כבר. אופטימיזציה של המרה, שימור ו-LTV. סבב Seed הושלם."),
            ("שלב 2 · התרחבות", "השקה רשמית ב-3 השווקים החדשים: אינדונזיה, טורקיה ווייטנאם. האצת ערוץ ה-B2B והפרסום הגיאו-ממוקד."),
            ("שלב 3 · כניסה גלובלית", "נוכחות פעילה בכל 14 השפות עם קמפיינים מקומיים. שותפויות White-Label ב-5+ יבשות. סבב A."),
            ("שלב 4 · מנהיגות", "20+ מדינות עם פעילות מאוחדת. פלטפורמת SaaS עולמית מובילה בנומרולוגיה יישומית. הנפקה או יציאה אסטרטגית."),
        ],
        "invest_titulo": "השקעה ויצירת קשר",
        "invest_texto": "אנחנו מוכנים למצגות פרטיות, due diligence ומשא ומתן. צרו קשר בערוץ המועדף עליכם.",
        "invest_dados": [
            ("סבב Seed", "R$ 3,5 מיליון"),
            ("הערכת שווי Pre-Money", "R$ 14 מיליון"),
            ("הון מוצע", "עד 20%"),
        ],
        "invest_contato": [
            ("מייל משקיעים", "a1elos.consultoria@gmail.com"),
            ("מייל כללי", "contato@a1elos.com"),
            ("אתר", "www.a1elos.com"),
            ("DUNS", "942242668 — Dun & Bradstreet"),
        ],
        "invest_alocacao": "חלוקת הון: 45% טכנולוגיה · 30% שיווק · 25% תפעול",
        "frase_final": "המספרים אף פעם לא משקרים.",
        "selo_final": ["DUNS 942242668", "24 מוצרים", "14 שפות", "~5,3 מיליארד דוברים"],
        "graf_cons": "שמרני",
        "graf_otim": "אופטימי",
        "grafico_titulo_linha": "צמיחה צפויה (R$ אלפים)",
        "pix_titulo": "ברזיל: תשתית ה-Pix",
        "pix_texto": "Pix היא תשתית התשלומים המיידיים הציבורית של ברזיל. עבור A1ELOS, היא מבטיחה גבייה מיידית, עלות נמוכה וקבלה אוניברסלית — הבסיס לפעילות B2C בשוק הברזילאי והשער להתרחבות בינלאומית.",
        "pix_kpis": [
            ("30,1 מיליארד", "עסקאות ב-2025", "+20% לעומת 2024 · Febraban"),
            ("76,4%", "מהאוכלוסייה משתמשת ב-Pix", "211 מיליון ברזילאים · הבנק המרכזי"),
            ("R$ 68,2 טריליון", "הועבר במחצית השנייה של 2025", "78,4 מיליארד עסקאות · הבנק המרכזי"),
            ("~80 מיליארד", "עסקאות ב-2025", "+25,7% לעומת שנה קודמת · דוח Pix"),
        ],
        "pix_fonte": "מקורות: הבנק המרכזי של ברזיל (Pix במספרים) ו-Febraban (סקר טכנולוגיות בנקאות).",
        "ref_titulo": "הפניות ביבליוגרפיות",
        "ref_intro": "מקורות ששימשו לנתוני השוק, לתחזיות ולמדדים של מצגת זו.",
        "ref_lista": [
            ("Global Wellness Institute", "כלכלת הבריאות העולמית: US$ 6,8 טריליון (2024) → US$ 9,8 טריליון (2029)."),
            ("MarkNtel Advisors", "אפליקציות אסטרולוגיה ונומרולוגיה: US$ 3 מיליארד → US$ 9 מיליארד עד 2030 (CAGR ~20%)."),
            ("קרן המטבע הבינלאומית · הבנק העולמי", "תמ\"ג ושוויון כוח קנייה (PPP) לפי מדינה."),
            ("הבנק המרכזי של ברזיל", "סטטיסטיקות רשמיות של Pix: עסקאות, נפח ומשתמשים."),
            ("Febraban", "סקר טכנולוגיות בנקאות — צמיחת ה-Pix ב-2025."),
            ("IBGE", "אוכלוסייה ומדדים סוציו-אקונומיים של ברזיל."),
        ],
        },

"ar": {
        "titulo": "A1ELOS Global Numerology",
        "subtitulo": "علم الأرقام مطبق على نجاحك",
        "capa_nota": "عرض تقديمي استراتيجي للمستثمرين والشركاء",
        "confidencial": "سري",
        "ano": "2026",
        "sumario_titulo": "الملخص التنفيذي",
        "duns_porque": "لماذا يهم DUNS؟",
        "preco_consciente": "تسعير واعٍ",
        "idioma_col": "اللغة",
        "falantes_col": "المتحدثون (مليون)",
        "linhas_idiomas": [
           ["الإنجليزية", "1.528"],
           ["الماندرين", "1.184"],
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
        "b2b_linha": "B2B — خصومات تصاعدية",
        "pub_linha": "إعلانات محددة الموقع",
        "tabela_descontos": "جدول الخصومات التصاعدية",
        "grafico_anos": ["السنة 1", "السنة 3", "السنة 5"],
        "grafico_titulo": "توقعات متحفظة (R$ ألف)",
        "grafico_titulo_linha": "النمو المتوقع (R$ ألف)",
        "fale_conosco": "تواصل معنا",
        "sumario_intro": "هذا العرض منظم ليقود المستثمرين والشركاء عبر جميع الجوانب الاستراتيجية لـ A1ELOS Global Numerology — من فرضية السوق إلى نموذج الإيرادات المتكررة.",
        "sumario_cards": [
            ("01", "عن A1ELOS", "شركة قابضة، محفظة واعتماد DUNS"),
            ("02", "فرصة السوق", "الاقتصاد العالمي للعافية US$ 6,8 تريليون"),
            ("03", "الحل والنطاق العالمي", "14 لغة، ~5,3 مليار متحدث"),
            ("04", "أسواق جديدة", "إندونيسيا وتركيا وفيتنام والموارد البشرية للشركات"),
            ("05", "المحفظة والأسعار", "24 منتجًا معايرًا حسب القوة الشرائية"),
            ("06", "إيرادات متكررة", "لافتات إعلانية وحزم B2B"),
            ("07", "التوقعات والاستثمار", "أفق 50 عامًا · جولة تأسيسية R$ 3,5M"),
        ],
        "sobre_titulo": "عن A1ELOS",
        "sobre_texto": "A1ELOS هي شركة قابضة للتقنية والمعرفة تجمع بين الذكاء الاصطناعي وعلم الأرقام التطبيقي والاستراتيجية الثقافية لإنشاء منتجات رقمية عالية التأثير على نطاق عالمي. مهمتنا: إضفاء الطابع الديمقراطي على المعرفة الذاتية الرقمية مع احترام الثقافة واحترام القوة الشرائية لكل سوق.",
        "sobre_kpis": [
            ("23", "منتجات نشطة", "عبر 4 مستويات وصول"),
            ("14", "لغة", "حوالي 67% من سكان العالم"),
            ("5,3 مليار", "متحدث", "سوق حقيقي قابل للوصول"),
            ("الذكاء الاصطناعي", "مدمج", "محرك تخصيص"),
        ],
        "sobre_duns": "DUNS 942242668 — شهادة Dun & Bradstreet سارية في أكثر من 190 دولة، تتيح عقود B2B والمشاريع المشتركة الدولية.",
        "duns_titulo": "المصداقية الدولية",
        "duns_texto": "رقم DUNS هو جواز السفر المؤسسي لـ A1ELOS على المسرح الدولي. إنه يشير للشركاء والعملاء من الشركات والمستثمرين إلى أن الشركة تمتلك هوية قابلة للتحقق، وتاريخًا يمكن تتبعه، وقدرة تعاقدية في أي اختصاص قضائي.",
        "duns_numero": "942242668",
        "duns_emitido": "صادر عن Dun & Bradstreet — المعيار العالمي للهوية التجارية المعترف به في أكثر من 190 دولة.",
        "duns_paises": "أكثر من 190 دولة",
        "duns_beneficios": [
            ("عقود B2B", "التأهيل للمناقصات والموردين العالميين"),
            ("المشاريع المشتركة", "شراكات دولية مع سهولة العناية الواجبة"),
            ("مصداقية فورية", "علامة جدية لدى المستثمرين المؤسسيين"),
        ],
        "mercado_titulo": "فرصة السوق",
        "mercado_texto": "نعيش التقاءً مثاليًا: العافية الرقمية تنمو بشكل انفجاري عالميًا بينما ينتقل علم الأرقام وعلم التنجيم إلى تطبيقات عالية التفاعل. A1ELOS في موقع دقيق عند هذا التقاطع، مع 74% من سكان العالم متصلين بالفعل (~6 مليارات شخص).",
        "mercado_cards": [
            ("العافية العالمية", "US$ 6,8 تريليون → US$ 9,8 تريليون بحلول 2029 (+7,6% سنويًا)"),
            ("تطبيقات التنجيم/الأرقام", "US$ 3 مليار → US$ 9 مليار بحلول 2030 · نمو سنوي مركب 20%"),
            ("تطبيقات العافية", "نمو سنوي مركب 14,9% → US$ 26,2 مليار في 2030"),
            ("المستخدمون عبر الإنترنت", "74% من العالم · ~6 مليارات شخص"),
        ],
        "mercado_rh_titulo": "سوق جديد: الموارد البشرية للشركات — المنتج الرابع والعشرون",
        "mercado_rh_texto": "المنتج الرابع والعشرون — توافق الفرق HR (R$ 98) — يفتح سوق B2B الرئيسي لـ A1ELOS: الموارد البشرية للشركات. تحليل التوافق الطاقي بين المديرين والموظفين (الطاقة المثالية: الرقم 8) يضع المنصة كأداة رائدة في العلامة التجارية لصاحب العمل وعافية الشركات، مع خصومات تصاعدية من 10% إلى 50% وتفاوض مباشر فوق 2.000 رمز (خطة الماس).",
        "mercado_rh_vantagens": [
            "الانسجام الطاقي للقسم → تقليل الاحتكاكات الشخصية وتماسك أعلى للفريق",
            "مواءمة المواقف والأفكار بين المديرين والموظفين → تواصل أكثر سلاسة",
            "انخفاض معدل دوران الموظفين وارتفاع الاحتفاظ بالمواهب",
            "مناخ تنظيمي إيجابي → مكسب في الإنتاجية والعافية",
            "علامة تجارية أقوى لصاحب العمل → جذب مواهب متوافقة مع الثقافة",
        ],
        "mercado_rh_cards": [
            ["HR Tech", "US$ 42,34 مليار (2025) → US$ 77,74 مليار (2031)", "نمو سنوي مركب 10,35% · Mordor Intelligence"],
            ["Employer Branding", "US$ 1,89 مليار (2025) → US$ 3,62 مليار (2031)", "نمو سنوي مركب 11,19% · Mordor Intelligence"],
            ["Corporate Wellness", "US$ 66,31 مليار (2025) → US$ 94,5 مليار (2031)", "نمو سنوي مركب 6,12% · Mordor Intelligence"],
        ],
        "problema_titulo": "المشكلة التي نحلها",
        "problema_col_esq_titulo": "إخفاقات السوق الحالي",
        "problema_col_esq": [
            ("حاجز اللغة", "الغالبية العظمى من أدوات علم الأرقام تعمل باللغة الإنجليزية فقط، مما يستبعد مليارات المتحدثين الأصليين بلغات أخرى."),
            ("أسعار منفصلة عن الواقع", "المنتجات المسعرة بالدولار للأسواق الناشئة تخلق استبعادًا اقتصاديًا — المستخدم لا يرفض المنتج، بل يرفض السعر غير المتاح."),
            ("غياب العمق", "الأدوات العامة تقدم إجابات سطحية دون تخصيص، ودون سياق ثقافي، ودون تطبيق عملي في الحياة اليومية."),
        ],
        "problema_col_dir_titulo": "تكلفة الاستبعاد",
        "problema_col_dir": "عندما تتجاهل منصة ما اللغة والقوة الشرائية، فإنها تتخلى طواعية عن أكبر سوق في العالم: أكثر من 4 مليارات شخص يعيشون في اقتصادات ناشئة ويتحدثون لغات غير الإنجليزية. هذه هي الفجوة التي تشغلها A1ELOS بدقة جراحية.",
        "problema_destaque": "المنصات التي تتجاهل القوة الشرائية المحلية تفقد الوصول إلى أكثر من 60% من السوق العالمي القابل للوصول.",
        "solucao_titulo": "حلنا: 3 ركائز استراتيجية",
        "solucao_texto": "بنَت A1ELOS منصة متكاملة تجمع بين علم الأرقام والذكاء الاصطناعي والحساسية الثقافية. يعمل الحل على ثلاث جبهات متكاملة، مما يضمن إيرادات متنوعة واحتفاظًا عاليًا.",
        "solucao_colunas": [
            ("الخرائط الشخصية", "تحليلات رقمية عميقة ومخصصة للمستخدم النهائي — الهوية، المهمة، دورات الحياة والتوافق — تُسلَّم بـ 14 لغة مع ذكاء اصطناعي مدمج."),
            ("علم أرقام الأعمال", "تشخيصات رقمية مطبقة على العلامات التجارية وCNPJ وتواريخ التأسيس والاستراتيجية المؤسسية. منتج متمايز ذو قيمة مدركة عالية في سوق B2B."),
            ("White-Label B2B", "ترخيص المنصة لشركات شريكة تريد تقديم علم الأرقام تحت علامتها التجارية الخاصة — بدعم متعدد اللغات وتخصيص كامل."),
        ],
        "alcance_titulo": "النطاق العالمي: 14 لغة · ~5,3 مليار متحدث",
        "alcance_texto": "تغطي A1ELOS حوالي 67% من سكان العالم بمنصة متعددة اللغات حقًا. كل لغة تمثل سوقًا ثقافيًا متميزًا، مع تسعير معاير للقوة الشرائية المحلية.",
        "mercados_titulo": "3 أسواق جديدة: +442 مليون متحدث",
        "mercados_texto": "التوسع الاستراتيجي إلى إندونيسيا وتركيا وفيتنام يمثل قفزة نوعية: أسواق ذات نمو اقتصادي مرتفع، وانتشار رقمي متزايد، وطلب مثبت على حلول العافية الرقمية الميسورة.",
        "mercados_cards": [
            ("إندونيسيا", ["285 مليون نسمة", "80,5% انتشار الإنترنت", "~255 مليون متحدث بالإندونيسية", "العافية: US$ 51,2 مليار (2025) → US$ 72,8 مليار (2034)"]),
            ("تركيا", ["85,9 مليون نسمة", "الناتج المحلي PPP للفرد US$ 37.301", "~90 مليون متحدث بالتركية", "فوق المتوسط العالمي (US$ 27.211)"]),
            ("فيتنام",  ["~100 مليون نسمة", "الناتج المحلي للفرد ~US$ 5.066 (+7,4%/سنة)", "~97 مليون متحدث بالفيتنامية", "العافية: US$ 303 مليون (2025) → US$ 485 مليون (2030)"]),
        ],
        "mercados_rodape": "3 أسواق جديدة = +442 مليون متحدث جديد قابل للوصول — مدمجون في المنصة بتسعير معاير ثقافيًا.",
        "preco_titulo": "فلسفة التسعير الواعي",
        "preco_esq": "احترام الثقافة + احترام القوة الشرائية = سوق حقيقي قابل للوصول. نفس نسبة القيمة. أسعار مختلفة. كرامة متساوية لجميع الأسواق.",
        "preco_dir_titulo": "كيف يعمل عمليًا",
        "preco_dir": "تطبق A1ELOS تعادل القوة الشرائية (PPP) كمعيار مركزي للتسعير. نفس المنتج يقدم نفس القيمة النسبية للمستخدم في لاغوس أو جاكرتا أو هانوي أو نيويورك — السعر معاير بحيث يكون الجهد المالي متناسبًا مع الدخل المحلي.",
        "preco_pilares": [
            ("معايرة PPP", "أسعار معدلة وفق مؤشر القوة الشرائية لكل دولة"),
            ("احترام الثقافة", "اللغة والعملة والسياق المحلي مدمجة في المنتج"),
            ("تحويل متفوق", "السعر العادل يولّد تحويلات أكثر واحتفاظًا أعلى على المدى الطويل"),
        ],
        "portfolio_titulo": "المحفظة: 24 منتجًا في 4 مستويات",
        "portfolio_texto": "البنية الطبقية تضمن أن كل ملف مستخدم — من الفضولي إلى المحترف — يجد عرضًا مناسبًا لمستوى تفاعله وقدرته المالية.",
        "portfolio_tabela": [
           ["المستوى", "المنتجات", "نطاق السعر (R$)", "الملف"],
           ["أساسي", "خريطة سريعة، خريطة كاملة", "R$ 8 – 17", "فضولي، اتصال أول"],
           ["متوسط", "بحث بالذكاء الاصطناعي، اسم بالاقتراع، رقم ناخب", "R$ 26 – 53", "مستخدم متفاعل"],
           ["متقدم", "اسم منظمة، اسم فني، اسم طفل، توقيع، اسم عمل", "R$ 35 – 44", "محترف، رائد أعمال"],
           ["بريميوم", "خريطة زوجين، خريطة عائلة، توافق الفرق HR ★، مكافأة جماعية", "R$ 98", "دخل مرتفع، استخدام مؤسسي"],
           ["B2B", "حزم مؤسسية، تراخيص، هدايا", "عند الطلب", "شركات وفرق"],
        ],
        "portfolio_rodape": "24 منتجًا تغطي رحلة المستخدم بأكملها، من أول اتصال إلى العميل المميز المتكرر — مع تعظيم LTV لكل لغة وسوق. التمييز: توافق الفرق HR (R$ 98) — منتج رائد في سوق الموارد البشرية للشركات، طاقة مثالية 8.",
        "negocio_titulo": "نموذج الأعمال: 3 مصادر إيرادات",
        "negocio_texto": "صُممت A1ELOS بإيرادات متنوعة وقابلة للتوسع: مبيعات مباشرة للمستهلك النهائي على نطاق عالمي، وعقود B2B عالية القيمة، وإعلانات محددة الموقع متكررة — ثلاثة محركات تغذي بعضها البعض.",
        "negocio_colunas": [
            ("B2C — 14 لغة", "بيع مباشر للمنتجات الرقمية بجميع العملات، بأسعار معدلة حسب PPP. توسع تلقائي عبر الذكاء الاصطناعي — دون فريق خدمة متناسب مع النمو."),
            ("B2B — خصومات تصاعدية", "حزم مؤسسية للموارد البشرية والعلامة التجارية لصاحب العمل والهدايا المؤسسية. خصومات من 10% إلى 50% حسب الحجم. فوق 2.000 رمز، تفاوض مباشر (خطة الماس). عقود مدعومة بـ DUNS 942242668."),
            ("إعلانات محددة الموقع", "لافتات مقسمة حسب الدولة أو القارة أو العالم بتناوب تلقائي. إيرادات شهرية متكررة عالية القيمة — دون اعتماد على حجم مبيعات المنتج."),
        ],
        "banners_titulo": "اللافتات الإعلانية — إيرادات شهرية متكررة",
        "banners_texto": "توفر منصة A1ELOS مساحات إعلانية متميزة بتقسيم دقيق حسب الموقع الجغرافي — الدولة أو القارة أو العالم. مع تناوب تلقائي كل 8 ثوانٍ وتنسيقات محسّنة للحاسوب والجوال، توفر اللافتات رؤية قابلة للقياس للمعلنين الإقليميين والدوليين.",
        "banners_tabela": [
            ["التقسيم", "ثابت (R$/شهر)", "مؤقت (R$/شهر)", "ملف المعلن"],
            ["دولة", "R$ 800", "R$ 500", "شركات محلية صغيرة ومتوسطة، تجارة إقليمية"],
            ["قارة", "R$ 1.800", "R$ 1.200", "علامات إقليمية، توسع قاري"],
            ["العالم", "R$ 3.500", "R$ 2.500", "شركات عالمية، تطبيقات دولية"],
            ["رعاية حصرية", "R$ 6.000", "R$ 4.500/حملة", "رعاة رئيسيون، إطلاقات"],
        ],
        "banners_formatos": "728×90 بكسل — لافتة مركزية للحاسوب · 320×100 بكسل — تنسيق جوال محسّن · 8 ثوانٍ — تناوب تلقائي · استهداف جغرافي — الدولة أو القارة أو النطاق العالمي",
        "b2b_titulo": "حزم B2B المؤسسية — قيمة عالية، حجم كبير",
        "b2b_texto": "تحوّل حزم B2B شركة A1ELOS إلى أداة للعلامة التجارية لصاحب العمل وعافية الشركات. في مركز هذه الاستراتيجية يوجد المنتج الحصري والمستمر: توافق الفرق HR (R$ 98). على عكس الهدايا المنفردة، فإن تحليل التوافق هو أداة إدارة أفراد تدمجها الشركة في روتينها اليومي — تحسب الأقسام والفرق بالطاقة المرغوبة وتزامن جميع أعضاء القسم على نفس التناغم والانسجام. مثالي للشركات الصغيرة والكبيرة، وهو الخدمة التي يستخدمها قسم الموارد البشرية باستمرار، مدعومة بأسواق تنمو بقوة: HR Tech (نمو سنوي مركب 10,35%)، Employer Branding (نمو سنوي مركب 11,19%) وCorporate Wellness (نمو سنوي مركب 6,12%).",
        "b2b_planos": [
            ("الخطة الأساسية · 50 رمزًا", "50× خريطة سريعة (R$ 8 لكل واحدة). مثالية لبرامج مزايا الموظفين وأنشطة الاندماج."),
            ("الخطة المتوسطة · 100 رمز", "50× خريطة سريعة + 50× بحث بالذكاء الاصطناعي (R$ 17). مثالية للفرق واستراتيجية العلامة التجارية لصاحب العمل."),
            ("خطة بريميوم · 200 رمز", "100× خريطة سريعة + 100× خريطة كاملة (R$ 17). أقصى عمق تحليلي للمجموعات الكبيرة."),
        ],
        "b2b_tabela": [
            ["بدءًا من", "الخصم", "الملف", "الاستخدام الموصى به"],
            ["10 رموز", "10%", "فرق صغيرة", "نشاط عافية لمرة واحدة"],
            ["50 رمزًا", "20%", "فرق نامية", "برامج متكررة"],
            ["100 رمز", "25%", "شركات صغيرة ومتوسطة", "ميزة ربع سنوية"],
            ["200 رمز", "30%", "شركات متوسطة", "برامج كاملة"],
            ["500 رمز", "40%", "شركات متوسطة", "هدية سنوية للموظفين"],
            ["1.000 رمز", "45%", "شركات كبيرة", "ولاء العملاء"],
            ["2.000 رمز", "50%", "مجموعات كبيرة", "نطاق واسع"],
            ["فوق 2.000", "قابل للتفاوض", "خطة الماس حسب الطلب", "توزيع مكافآت بكميات"],
        ],
        "rh_destaque_titulo": "توافق الفرق HR — المنتج الحصري",
        "rh_destaque_texto": "تحليل التوافق الطاقي بين المديرين والموظفين، وبين أعضاء نفس الفريق (الطاقة المثالية: الرقم 8 — القوة والقيادة والتوازن المادي)، يضع A1ELOS كرائدة في سوق الموارد البشرية للشركات. الانسجام الطاقي للقسم يقلل الاحتكاكات الشخصية، ويوائم المواقف والأفكار، ويخفض دوران الموظفين، ويقوي المناخ التنظيمي ويرفع الإنتاجية — قيمة لا توفرها المكافأة الجماعية كهدية منفردة. إنه المنتج الذي يدعم النمو قصير المدى والإيرادات المتكررة B2B.",
        "projecoes_titulo": "التوقعات المالية: أفق 50 عامًا",
        "projecoes_texto": "بُنيت التوقعات بناءً على تقديرات نسبة الاختراق على السوق المحتمل (~5,32 مليار متحدث)، مع تحويل متحفظ 3% واسترداد مكافآت بين 70% و90%. مع المنتج الرابع والعشرين — توافق الفرق HR (R$ 98) وقناة المكافأة الجماعية/المؤسسية —، تدخل إيرادات B2B للموارد البشرية في التوقعات، المرتكزة على أسواق موثقة: HR Tech (نمو سنوي مركب 10,35%)، Employer Branding (نمو سنوي مركب 11,19%) وCorporate Wellness (نمو سنوي مركب 6,12%). المدى القصير (السنوات 1–5) يبرز النمو المتسارع للجبهة الجديدة B2B؛ والمدى الطويل يعكس الاستقرار المستمر للنموذج حتى الاستيعاب الكامل للسوق القابل للوصول.",
        "projecoes_tabela": [
            ["الأفق", "متحفظ (R$)", "متفائل (R$)"],
            ["السنة 1", "R$ 318k", "R$ 810k"],
            ["السنة 2", "R$ 630k", "R$ 1,8M"],
            ["السنة 3", "R$ 1,20M", "R$ 3,50M"],
            ["السنة 4", "R$ 2,2M", "R$ 6,2M"],
            ["السنة 5", "R$ 3,70M", "R$ 9,6M"],
        ],
        "projecoes_tabela_50": [
            ["الأفق", "متحفظ (R$)", "متفائل (R$)"],
            ["السنة 1", "R$ 318k", "R$ 810k"],
            ["السنة 3", "R$ 1,20M", "R$ 3,50M"],
            ["السنة 5", "R$ 3,70M", "R$ 9,6M"],
            ["السنة 7", "R$ 7,8M", "R$ 20,5M"],
            ["السنة 10", "R$ 16,3M", "R$ 44,0M"],
            ["السنة 20", "R$ 64M", "R$ 184M"],
            ["السنة 30", "R$ 133M", "R$ 359M"],
            ["السنة 40", "R$ 202M", "R$ 606M"],
            ["السنة 50", "R$ 276M", "R$ 869M"],
        ],
        "projecoes_curto_titulo": "التوقعات المالية: المدى القصير (السنوات 1–5)",
        "projecoes_curto_texto": "المدى القصير يبرز النمو المتسارع للجبهة الجديدة B2B للموارد البشرية (توافق الفرق + مكافأة جماعية)، ما يقرب من 12 ضعفًا في 5 سنوات في السيناريو المتحفظ — قبل الاستقرار طويل المدى.",
        "projecoes_curto_tabela": [
            ["الأفق", "متحفظ (R$)", "متفائل (R$)"],
            ["السنة 1", "R$ 318k", "R$ 810k"],
            ["السنة 2", "R$ 630k", "R$ 1,8M"],
            ["السنة 3", "R$ 1,20M", "R$ 3,50M"],
            ["السنة 4", "R$ 2,2M", "R$ 6,2M"],
            ["السنة 5", "R$ 3,70M", "R$ 9,6M"],
         ],
        "tracao_titulo": "الزخم والنتائج المثبتة",
        "tracao_texto": "تعمل A1ELOS بالفعل بمقاييس منتج تتحقق من النموذج — احتفاظ مرتفع، وتقييم متميز، وقاعدة نامية من شركاء B2B — مما يثبت أن المنصة تقدم قيمة حقيقية للمستخدم النهائي وللسوق المؤسسي.",
        "tracao_kpis": [
            ("12K+", "مستخدمون نشطون", "قاعدة عضوية في نمو ثابت"),
            ("87%", "احتفاظ", "أعلى بكثير من متوسط الصناعة (~30%)"),
            ("4,8★", "تقييم متوسط", "رضا مثبت للمستخدم النهائي"),
            ("23", "شريك B2B", "عقود نشطة مع شركات وأقسام موارد بشرية"),
        ],
        "roteiro_titulo": "خارطة الطريق الاستراتيجية",
        "roteiro_texto": "تنفذ A1ELOS خطة من أربع مراحل تصاعدية — من توطيد القاعدة الحالية إلى الريادة العالمية في السوق، مع خيارات خروج واضحة للمستثمرين.",
        "roteiro_fases": [
            ("المرحلة 1 · التوطيد", "تقوية قاعدة المستخدمين في اللغات النشطة بالفعل. تحسين التحويل والاحتفاظ وLTV. اكتملت الجولة التأسيسية."),
            ("المرحلة 2 · التوسع", "إطلاق رسمي في الأسواق الثلاثة الجديدة: إندونيسيا وتركيا وفيتنام. تسريع قناة B2B والإعلانات محددة الموقع."),
            ("المرحلة 3 · الدخول العالمي", "حضور نشط في اللغات الأربع عشرة بحملات مترجمة. شراكات العلامة البيضاء في أكثر من 5 قارات. السلسلة A."),
            ("المرحلة 4 · الريادة", "أكثر من 20 دولة بعمليات موحدة. منصة SaaS عالمية مرجعية في علم الأرقام التطبيقي. طرح عام أو خروج استراتيجي."),
        ],
        "invest_titulo": "الاستثمار والتواصل",
        "invest_texto": "نحن مستعدون للعروض الخاصة والعناية الواجبة والمفاوضات. تواصل معنا عبر القناة المفضلة لديك.",
        "invest_dados": [
            ("الجولة التأسيسية", "R$ 3,5 مليون"),
            ("التقييم قبل المال", "R$ 14 مليون"),
            ("الحصة المطروحة", "حتى 20%"),
        ],
        "invest_contato": [
            ("بريد المستثمرين", "a1elos.consultoria@gmail.com"),
            ("البريد العام", "contato@a1elos.com"),
            ("الموقع", "www.a1elos.com"),
            ("DUNS", "942242668 — Dun & Bradstreet"),
        ],
        "invest_alocacao": "توزيع رأس المال: 45% تقنية · 30% تسويق · 25% عمليات",
        "frase_final": "الأرقام لا تكذب أبدًا.",
        "selo_final": ["DUNS 942242668", "24 منتجًا", "14 لغة", "~5,3 مليار متحدث"],
        "graf_cons": "متحفظ",
        "graf_otim": "متفائل",
        "grafico_titulo_linha": "النمو المتوقع (R$ ألف)",
        "pix_titulo": "البرازيل: البنية التحتية Pix",
        "pix_texto": "Pix هي البنية التحتية العامة للمدفوعات الفورية في البرازيل. بالنسبة لـ A1ELOS، تضمن تحصيلًا فوريًا وتكلفة منخفضة وقبولًا عالميًا — أساس عملية B2C في السوق البرازيلية وبوابة التوسع الدولي.",
        "pix_kpis": [
            ("30,1 مليار", "معاملة في 2025", "+20% مقارنة بـ 2024 · Febraban"),
            ("76,4%", "من السكان يستخدمون Pix", "211 مليون برازيلي · البنك المركزي"),
            ("R$ 68,2 تريليون", "تم تحريكها في النصف الثاني من 2025", "78,4 مليار معاملة · البنك المركزي"),
            ("~80 مليار", "معاملة في 2025", "+25,7% مقارنة بالعام السابق · تقرير Pix"),
        ],
        "pix_fonte": "المصادر: البنك المركزي البرازيلي (Pix بالأرقام) وFebraban (مسح التقنية المصرفية).",
        "ref_titulo": "المراجع الببليوغرافية",
        "ref_intro": "المصادر المستخدمة لبيانات السوق والتوقعات والمؤشرات في هذا العرض.",
        "ref_lista": [
            ("Global Wellness Institute", "الاقتصاد العالمي للعافية: US$ 6,8 تريليون (2024) → US$ 9,8 تريليون (2029)."),
            ("MarkNtel Advisors", "تطبيقات التنجيم وعلم الأرقام: US$ 3 مليار → US$ 9 مليار بحلول 2030 (نمو سنوي مركب ~20%)."),
            ("صندوق النقد الدولي · البنك الدولي", "الناتج المحلي وتعادل القوة الشرائية (PPP) حسب الدولة."),
            ("البنك المركزي البرازيلي", "إحصاءات Pix الرسمية: المعاملات والحجم والمستخدمون."),
            ("Febraban", "مسح التقنية المصرفية — نمو Pix في 2025."),
            ("IBGE", "سكان البرازيل ومؤشراتها الاجتماعية والاقتصادية."),
        ],
        },           
           
"id": {
        "titulo": "A1ELOS Global Numerology",
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
        "grafico_anos": ["Tahun 1", "Tahun 3", "Tahun 5"],
        "grafico_titulo": "Proyeksi Konservatif (R$ ribu)",
        "grafico_titulo_linha": "Pertumbuhan Diproyeksikan (R$ ribu)",
        "fale_conosco": "Hubungi Kami",
        "sumario_intro": "Presentasi ini disusun untuk memandu investor dan mitra melalui semua aspek strategis A1ELOS Global Numerology — dari tesis pasar hingga model pendapatan berulang.",
        "sumario_cards": [
            ("01", "Tentang A1ELOS", "Holding, portofolio dan kredensial DUNS"),
            ("02", "Peluang Pasar", "Ekonomi kesejahteraan global US$ 6,8 triliun"),
            ("03", "Solusi dan Jangkauan Global", "14 bahasa, ~5,3 miliar penutur"),
            ("04", "Pasar Baru", "Indonesia, Turki, Vietnam dan HR Korporat"),
            ("05", "Portofolio dan Harga", "24 produk dikalibrasi berdasarkan daya beli"),
            ("06", "Pendapatan Berulang", "Banner iklan dan Paket B2B"),
            ("07", "Proyeksi dan Investasi", "Cakrawala 50 tahun · Putaran Seed R$ 3,5M"),
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
        "mercado_rh_titulo": "Pasar Baru: HR Korporat — Produk ke-24",
        "mercado_rh_texto": "Produk ke-24 — Kompatibilitas Tim HR (R$ 98) — membuka pasar B2B utama A1ELOS: HR korporat. Analisis kompatibilitas energik antara manajer dan karyawan (energi ideal: angka 8) memposisikan platform sebagai alat employer branding dan kesejahteraan korporat yang pelopor, dengan diskon progresif 10% hingga 50% dan negosiasi langsung di atas 2.000 kode (Paket Berlian).",
        "mercado_rh_vantagens": [
            "Harmoni energik sektor → pengurangan gesekan antarpribadi dan kohesi tim yang lebih tinggi",
            "Penyelarasan sikap dan pikiran antara manajer dan karyawan → komunikasi lebih lancar",
            "Turnover lebih rendah dan retensi talenta lebih tinggi",
            "Iklim organisasi positif → peningkatan produktivitas dan kesejahteraan",
            "Employer branding diperkuat → menarik talenta yang selaras dengan budaya",
        ],
        "mercado_rh_cards": [
            ["HR Tech", "US$ 42,34 miliar (2025) → US$ 77,74 miliar (2031)", "CAGR 10,35% · Mordor Intelligence"],
            ["Employer Branding", "US$ 1,89 miliar (2025) → US$ 3,62 miliar (2031)", "CAGR 11,19% · Mordor Intelligence"],
            ["Corporate Wellness", "US$ 66,31 miliar (2025) → US$ 94,5 miliar (2031)", "CAGR 6,12% · Mordor Intelligence"],
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
        "portfolio_titulo": "Portofolio: 24 Produk dalam 4 Tingkat",
        "portfolio_texto": "Struktur berlapis memastikan setiap profil pengguna — dari yang penasaran hingga profesional — menemukan penawaran yang sesuai dengan tingkat keterlibatan dan kapasitas finansialnya.",
        "portfolio_tabela": [
           ["Tingkat", "Produk", "Kisaran Harga (R$)", "Profil"],
           ["Dasar", "Peta Ekspres, Peta Lengkap", "R$ 8 – 17", "Penasaran, kontak pertama"],
           ["Menengah", "Pencarian AI, Nama Surat Suara, No. Pemilu", "R$ 26 – 53", "Pengguna terlibat"],
           ["Lanjut", "Nama NGO, Nama Panggung, Nama Bayi, Tanda Tangan, Nama Bisnis", "R$ 35 – 44", "Profesional, wirausahawan"],
           ["Premium", "Peta Pasangan, Peta Keluarga, Kompatibilitas Tim HR ★, Bonus Kolektif", "R$ 98", "Pendapatan tinggi, penggunaan korporat"],
           ["B2B", "Paket bisnis, lisensi, hadiah", "Sesuai permintaan", "Perusahaan dan tim"],
        ],
        "portfolio_rodape": "24 produk mencakup seluruh perjalanan pengguna, dari kontak pertama hingga pelanggan premium berulang — memaksimalkan LTV per bahasa dan pasar. Sorotan: Kompatibilitas Tim HR (R$ 98) — produk pelopor di pasar HR korporat, energi ideal 8.",
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
        "b2b_texto": "Paket B2B mengubah A1ELOS menjadi alat employer branding dan kesejahteraan korporat. Di pusat strategi ini adalah produk eksklusif dan berkelanjutan: Kompatibilitas Tim HR (R$ 98). Berbeda dengan hadiah sekali pakai, analisis kompatibilitas adalah alat manajemen orang yang diintegrasikan perusahaan ke dalam rutinitas hariannya — menghitung sektor dan tim dengan energi yang diinginkan dan menyinkronkan semua anggota sektor dalam ritme dan harmoni yang sama. Ideal untuk perusahaan kecil dan besar, ini adalah layanan yang digunakan Departemen Sumber Daya Manusia secara terus-menerus, didukung oleh pasar yang tumbuh pesat: HR Tech (CAGR 10,35%), Employer Branding (CAGR 11,19%) dan Corporate Wellness (CAGR 6,12%).",
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
        "rh_destaque_titulo": "Kompatibilitas Tim HR — Produk Eksklusif",
        "rh_destaque_texto": "Analisis kompatibilitas energik antara manajer dan karyawan, dan antara anggota tim yang sama (energi ideal: angka 8 — kekuatan, kepemimpinan dan keseimbangan materi), memposisikan A1ELOS sebagai pelopor di pasar HR korporat. Harmoni energik sektor mengurangi gesekan antarpribadi, menyelaraskan sikap dan pikiran, menurunkan turnover, memperkuat iklim organisasi dan meningkatkan produktivitas — nilai yang tidak diberikan oleh Bonus Kolektif sebagai hadiah sekali pakai. Inilah produk yang menopang pertumbuhan jangka pendek dan pendapatan B2B berulang.",
        "projecoes_titulo": "Proyeksi Keuangan: Cakrawala 50 Tahun",
        "projecoes_texto": "Proyeksi dibangun berdasarkan estimasi persentase penetrasi atas pasar potensial ~5,32 miliar penutur, dengan konversi konservatif 3% dan penukaran bonus antara 70% dan 90%. Dengan produk ke-24 — Kompatibilitas Tim HR (R$ 98) dan kanal Bonus Kolektif/Korporat —, pendapatan B2B HR masuk ke dalam proyeksi, berlabuh pada pasar yang terverifikasi: HR Tech (CAGR 10,35%), Employer Branding (CAGR 11,19%) dan Corporate Wellness (CAGR 6,12%). Jangka pendek (tahun 1–5) menyoroti pertumbuhan pesat lini B2B baru; jangka panjang mencerminkan stabilitas berkelanjutan model hingga penyerapan penuh pasar yang dapat dijangkau.",
        "projecoes_tabela": [
            ["Cakrawala", "Konservatif (R$)", "Optimis (R$)"],
            ["Tahun 1", "R$ 318k", "R$ 810k"],
            ["Tahun 2", "R$ 630k", "R$ 1,8M"],
            ["Tahun 3", "R$ 1,20M", "R$ 3,50M"],
            ["Tahun 4", "R$ 2,2M", "R$ 6,2M"],
            ["Tahun 5", "R$ 3,70M", "R$ 9,6M"],
        ],
        "projecoes_tabela_50": [
            ["Cakrawala", "Konservatif (R$)", "Optimis (R$)"],
            ["Tahun 1", "R$ 318k", "R$ 810k"],
            ["Tahun 3", "R$ 1,20M", "R$ 3,50M"],
            ["Tahun 5", "R$ 3,70M", "R$ 9,6M"],
            ["Tahun 7", "R$ 7,8M", "R$ 20,5M"],
            ["Tahun 10", "R$ 16,3M", "R$ 44,0M"],
            ["Tahun 20", "R$ 64M", "R$ 184M"],
            ["Tahun 30", "R$ 133M", "R$ 359M"],
            ["Tahun 40", "R$ 202M", "R$ 606M"],
            ["Tahun 50", "R$ 276M", "R$ 869M"],
        ],
        "projecoes_curto_titulo": "Proyeksi Keuangan: Jangka Pendek (Tahun 1–5)",
        "projecoes_curto_texto": "Jangka pendek menyoroti pertumbuhan pesat lini B2B HR baru (Kompatibilitas Tim + Bonus Kolektif), hampir 12x dalam 5 tahun pada skenario konservatif — sebelum stabilisasi jangka panjang.",
        "projecoes_curto_tabela": [
            ["Cakrawala", "Konservatif (R$)", "Optimis (R$)"],
            ["Tahun 1", "R$ 318k", "R$ 810k"],
            ["Tahun 2", "R$ 630k", "R$ 1,8M"],
            ["Tahun 3", "R$ 1,20M", "R$ 3,50M"],
            ["Tahun 4", "R$ 2,2M", "R$ 6,2M"],
            ["Tahun 5", "R$ 3,70M", "R$ 9,6M"],
         ],
        "tracao_titulo": "Traction dan Hasil yang Terbukti",
        "tracao_texto": "A1ELOS sudah beroperasi dengan metrik produk yang memvalidasi model — retensi tinggi, peringkat premium dan basis mitra B2B yang berkembang menunjukkan bahwa platform memberikan nilai nyata kepada pengguna akhir dan pasar korporat.",
        "tracao_kpis": [
            ("12K+", "Pengguna Aktif", "Basis organik dalam pertumbuhan konsisten"),
            ("87%", "Retensi", "Jauh di atas rata-rata industri (~30%)"),
            ("4,8★", "Peringkat Rata-rata", "Kepuasan pengguna akhir yang terbukti"),
            ("23", "Mitra B2B", "Kontrak aktif dengan perusahaan dan HR"),
        ],
        "roteiro_titulo": "Peta Jalan Strategis",
        "roteiro_texto": "A1ELOS menjalankan rencana dalam empat fase progresif — dari konsolidasi basis saat ini hingga kepemimpinan pasar global, dengan opsi keluar yang jelas bagi investor.",
        "roteiro_fases": [
            ("Fase 1 · Konsolidasi", "Penguatan basis pengguna di bahasa yang sudah aktif. Optimasi konversi, retensi dan LTV. Putaran Seed selesai."),
            ("Fase 2 · Ekspansi", "Peluncuran resmi di 3 pasar baru: Indonesia, Turki dan Vietnam. Akselerasi kanal B2B dan iklan geolokasi."),
            ("Fase 3 · Masuk Global", "Kehadiran aktif di semua 14 bahasa dengan kampanye terlokalisasi. Kemitraan white-label di 5+ benua. Seri A."),
            ("Fase 4 · Kepemimpinan", "20+ negara dengan operasi terkonsolidasi. Platform SaaS referensi global dalam numerologi terapan. IPO atau keluar strategis."),
        ],
        "invest_titulo": "Investasi dan Kontak",
        "invest_texto": "Kami siap untuk presentasi privat, due diligence dan negosiasi. Hubungi kami melalui kanal pilihan Anda.",
        "invest_dados": [
            ("Putaran Seed", "R$ 3,5 juta"),
            ("Valuasi Pre-Money", "R$ 14 juta"),
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
        "selo_final": ["DUNS 942242668", "24 PRODUK", "14 BAHASA", "~5,3 MILIAR PENUTUR"],
        "graf_cons": "Konservatif",
        "graf_otim": "Optimis",
        "grafico_titulo_linha": "Pertumbuhan Diproyeksikan (R$ ribu)",
        "pix_titulo": "Brasil: Infrastruktur Pix",
        "pix_texto": "Pix adalah infrastruktur pembayaran instan publik Brasil. Bagi A1ELOS, Pix menjamin penagihan segera, biaya rendah dan penerimaan universal — fondasi operasi B2C di pasar Brasil dan pintu masuk ekspansi internasional.",
        "pix_kpis": [
            ("30,1 miliar", "Transaksi pada 2025", "+20% vs 2024 · Febraban"),
            ("76,4%", "dari populasi menggunakan Pix", "211 juta warga Brasil · Bank Sentral"),
            ("R$ 68,2 triliun", "digunakan pada semester 2 2025", "78,4 miliar transaksi · Bank Sentral"),
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
        "titulo": "A1ELOS Global Numerology",
        "subtitulo": "Sayıların bilimi başarınıza uygulandı",
        "capa_nota": "Yatırımcılar ve Ortaklar için Stratejik Sunum",
        "confidencial": "GİZLİ",
        "ano": "2026",
        "sumario_titulo": "Yönetici Özeti",
        "duns_porque": "DUNS neden önemli?",
        "preco_consciente": "Bilinçli Fiyatlandırma",
        "idioma_col": "Dil",
        "falantes_col": "Konuşanlar (milyon)",
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
        "grafico_anos": ["1. Yıl", "3. Yıl", "5. Yıl"],
        "grafico_titulo": "Muhafazakâr Projeksiyon (R$ bin)",
        "grafico_titulo_linha": "Öngörülen Büyüme (R$ bin)",
        "fale_conosco": "Bize Ulaşın",
        "sumario_intro": "Bu sunum, yatırımcıları ve ortakları A1ELOS Global Numerology'nin tüm stratejik yönleri boyunca yönlendirmek için yapılandırılmıştır — pazar tezinden yinelenen gelir modeline kadar.",
        "sumario_cards": [
            ("01", "A1ELOS Hakkında", "Holding, portföy ve DUNS kimlik belgesi"),
            ("02", "Pazar Fırsatı", "Küresel sağlıklı yaşam ekonomisi US$ 6,8 trilyon"),
            ("03", "Çözüm ve Küresel Erişim", "14 dil, ~5,3 milyar konuşan"),
            ("04", "Yeni Pazarlar", "Endonezya, Türkiye, Vietnam ve Kurumsal İK"),
            ("05", "Portföy ve Fiyatlar", "Satın alma gücüne göre kalibre edilmiş 24 ürün"),
            ("06", "Yinelenen Gelir", "Reklam bannerları ve B2B Paketleri"),
            ("07", "Projeksiyonlar ve Yatırım", "50 yıllık ufuk · Tohum Turu R$ 3,5M"),
        ],
        "sobre_titulo": "A1ELOS Hakkında",
        "sobre_texto": "A1ELOS, küresel ölçekte yüksek etkili dijital ürünler yaratmak için yapay zekâyı, uygulamalı numerolojiyi ve kültürel stratejiyi birleştiren bir teknoloji ve bilgi holdingidir. Misyonumuz: kültürel saygı ve her pazarın satın alma gücüne saygı ile sayısal öz bilgiyi demokratikleştirmek.",
        "sobre_kpis": [
            ("23", "Aktif Ürün", "4 erişim seviyesinde"),
            ("14", "Dil", "Dünya nüfusunun ~%67'si"),
            ("5,3 M", "Konuşan", "Gerçek adreslenebilir pazar"),
            ("AI", "Entegre", "Kişiselleştirme motoru"),
        ],
        "sobre_duns": "DUNS 942242668 — Dun & Bradstreet sertifikası 190'dan fazla ülkede geçerli olup B2B sözleşmelerini ve uluslararası ortak girişimleri mümkün kılar.",
        "duns_titulo": "Uluslararası Güvenilirlik",
        "duns_texto": "DUNS numarası, A1ELOS'un uluslararası sahnedeki kurumsal pasaportudur. Şirketin doğrulanabilir kimliğe, izlenebilir geçmişe ve herhangi bir yargı alanında sözleşme kapasitesine sahip olduğunu ortaklara, kurumsal müşterilere ve yatırımcılara işaret eder.",
        "duns_numero": "942242668",
        "duns_emitido": "Dun & Bradstreet tarafından verilmiştir — 190'dan fazla ülkede tanınan küresel iş kimliği standardı.",
        "duns_paises": "190+ ÜLKE",
        "duns_beneficios": [
            ("B2B Sözleşmeleri", "Küresel ihaleler ve tedarikçiler için yeterlilik"),
            ("Ortak Girişimler", "Kolaylaştırılmış durum tespiti ile uluslararası ortaklıklar"),
            ("Anında Güvenilirlik", "Kurumsal yatırımcılar için ciddiyet işareti"),
        ],
        "mercado_titulo": "Pazar Fırsatı",
        "mercado_texto": "Mükemmel yakınsamayı yaşıyoruz: dijital sağlıklı yaşam küresel olarak patlarken numeroloji ve astroloji yüksek etkileşimli uygulamalara taşınıyor. A1ELOS tam bu kesişim noktasında konumlanmıştır; dünya nüfusunun %74'ü zaten çevrimiçi (~6 milyar kişi).",
        "mercado_cards": [
            ("Küresel Sağlıklı Yaşam", "US$ 6,8 trilyon → 2029'a kadar US$ 9,8 trilyon (yıllık +%7,6)"),
            ("Astroloji/Numeroloji Uygulamaları", "US$ 3 milyar → 2030'a kadar US$ 9 milyar · CAGR %20"),
            ("Sağlıklı Yaşam Uygulamaları", "CAGR %14,9 → 2030'da US$ 26,2 milyar"),
            ("Çevrimiçi Kullanıcılar", "Dünyanın %74'ü · ~6 milyar kişi"),
        ],
        "mercado_rh_titulo": "Yeni Pazar: Kurumsal İK — 24. Ürün",
        "mercado_rh_texto": "24. ürün — Ekip Uyumu İK (R$ 98) — A1ELOS'un ana B2B pazarını açar: kurumsal İK. Yöneticiler ve çalışanlar arasındaki enerjik uyum analizi (ideal enerji: 8 sayısı), platformu öncü bir işveren markası ve kurumsal sağlıklı yaşam aracı olarak konumlandırır; %10 ila %50 aşamalı indirimler ve 2.000 kodun üzerinde doğrudan müzakere (Elmas Planı) ile.",
        "mercado_rh_vantagens": [
            "Bölümün enerjik uyumu → kişiler arası sürtüşmelerin azalması ve daha yüksek ekip uyumu",
            "Yöneticiler ve çalışanlar arasında tutum ve düşüncelerin hizalanması → daha akıcı iletişim",
            "Daha düşük personel devri ve daha yüksek yetenek elde tutma",
            "Olumlu organizasyonel iklim → üretkenlik ve sağlıklı yaşam kazancı",
            "Güçlendirilmiş işveren markası → kültürle uyumlu yeteneklerin çekilmesi",
        ],
        "mercado_rh_cards": [
            ["HR Tech", "US$ 42,34 milyar (2025) → US$ 77,74 milyar (2031)", "CAGR %10,35 · Mordor Intelligence"],
            ["Employer Branding", "US$ 1,89 milyar (2025) → US$ 3,62 milyar (2031)", "CAGR %11,19 · Mordor Intelligence"],
            ["Corporate Wellness", "US$ 66,31 milyar (2025) → US$ 94,5 milyar (2031)", "CAGR %6,12 · Mordor Intelligence"],
        ],
        "problema_titulo": "Çözdüğümüz Sorun",
        "problema_col_esq_titulo": "Mevcut Pazarın Eksiklikleri",
        "problema_col_esq": [
            ("Dil Engeli", "Numeroloji araçlarının ezici çoğunluğu yalnızca İngilizce çalışır ve diğer dillerin milyarlarca anadil konuşucusunu dışlar."),
            ("Gerçeklikten Kopuk Fiyatlar", "Gelişmekte olan pazarlar için dolar cinsinden fiyatlanan ürünler ekonomik dışlanma yaratır — kullanıcı ürünü değil, erişilemeyen fiyatı reddeder."),
            ("Derinlik Eksikliği", "Genel araçlar, kişiselleştirme olmadan, kültürel bağlam olmadan ve günlük hayata pratik uygulama olmadan yüzeysel yanıtlar verir."),
        ],
        "problema_col_dir_titulo": "Dışlanmanın Bedeli",
        "problema_col_dir": "Bir platform dil ve satın alma gücünü görmezden geldiğinde, dünyanın en büyük pazarını gönüllü olarak terk eder: gelişmekte olan ekonomilerde yaşayan ve İngilizce olmayan dilleri konuşan 4 milyardan fazla insan. A1ELOS'un cerrahi hassasiyetle doldurduğu boşluk tam da budur.",
        "problema_destaque": "Yerel satın alma gücünü görmezden gelen platformlar, küresel adreslenebilir pazarın %60'ından fazlasına erişimi kaybeder.",
        "solucao_titulo": "Çözümümüz: 3 Stratejik Sütun",
        "solucao_texto": "A1ELOS, sayı bilimini, yapay zekâyı ve kültürel duyarlılığı birleştiren entegre bir platform inşa etmiştir. Çözüm, üç tamamlayıcı cephede çalışır; çeşitlendirilmiş gelir ve yüksek elde tutma sağlar.",
        "solucao_colunas": [
            ("Kişisel Haritalar", "Son kullanıcı için derin, kişiselleştirilmiş sayısal analizler — kimlik, misyon, yaşam döngüleri ve uyum — entegre AI ile 14 dilde sunulur."),
            ("İş Numerolojisi", "Markalara, CNPJ'lere, kuruluş tarihlerine ve kurumsal stratejiye uygulanan numerolojik teşhisler. B2B pazarında yüksek algılanan değere sahip farklılaştırılmış ürün."),
            ("White-Label B2B", "Kendi markaları altında numeroloji sunmak isteyen ortak şirketler için platform lisansı — çok dilli destek ve tam kişiselleştirme ile."),
        ],
        "alcance_titulo": "Küresel Erişim: 14 Dil · ~5,3 Milyar Konuşan",
        "alcance_texto": "A1ELOS, gerçekten çok dilli bir platformla dünya nüfusunun ~%67'sini kapsar. Her dil, yerel satın alma gücüne göre kalibre edilmiş fiyatlarla ayrı bir kültürel pazarı temsil eder.",
        "mercados_titulo": "3 Yeni Pazar: +442 Milyon Konuşan",
        "mercados_texto": "Endonezya, Türkiye ve Vietnam'a stratejik genişleme niteliksel bir sıçramayı temsil eder: yüksek ekonomik büyüme, artan dijital nüfuz ve uygun fiyatlı dijital sağlıklı yaşam çözümlerine kanıtlanmış talep gösteren pazarlar.",
        "mercados_cards": [
            ("Endonezya", ["285 milyon nüfus", "%80,5 internet nüfuzu", "~255 milyon Endonezce konuşan", "Sağlıklı yaşam: US$ 51,2 milyar (2025) → US$ 72,8 milyar (2034)"]),
            ("Türkiye", ["85,9 milyon nüfus", "Kişi başı GSYİH PPP US$ 37.301", "~90 milyon Türkçe konuşan", "Dünya ortalamasının üzerinde (US$ 27.211)"]),
            ("Vietnam",  ["~100 milyon nüfus", "Kişi başı GSYİH ~US$ 5.066 (yıllık +%7,4)", "~97 milyon Vietnamca konuşan", "Sağlıklı yaşam: US$ 303 milyon (2025) → US$ 485 milyon (2030)"]),
        ],
        "mercados_rodape": "3 yeni pazar = +442 milyon yeni adreslenebilir konuşan — kültürel olarak kalibre edilmiş fiyatlandırma ile platforma entegre edildi.",
        "preco_titulo": "Bilinçli Fiyatlandırma Felsefesi",
        "preco_esq": "Kültürel saygı + satın alma gücüne saygı = gerçek adreslenebilir pazar. Aynı değer oranı. Farklı fiyatlar. Tüm pazarlar için eşit onur.",
        "preco_dir_titulo": "Pratikte Nasıl Çalışır",
        "preco_dir": "A1ELOS, merkezi fiyatlandırma kriteri olarak Satın Alma Gücü Paritesi'ni (PPP) uygular. Aynı ürün, Lagos, Jakarta, Hanoi veya New York'taki kullanıcıya aynı göreli değeri sunar — fiyat, finansal çabanın yerel gelirle orantılı olması için kalibre edilir.",
        "preco_pilares": [
            ("PPP Kalibrasyonu", "Her ülkenin satın alma gücü endeksine göre ayarlanan fiyatlar"),
            ("Kültürel Saygı", "Dil, para birimi ve yerel bağlam ürüne entegre edilir"),
            ("Üstün Dönüşüm", "Adil fiyat daha fazla dönüşüm ve daha yüksek uzun vadeli elde tutma sağlar"),
        ],
        "portfolio_titulo": "Portföy: 4 Seviyede 24 Ürün",
        "portfolio_texto": "Katmanlı yapı, her kullanıcı profili — meraklıdan profesyonele — etkileşim düzeyine ve finansal kapasitesine uygun bir teklif bulmasını sağlar.",
        "portfolio_tabela": [
           ["Seviye", "Ürünler", "Fiyat Aralığı (R$)", "Profil"],
           ["Temel", "Ekspres Harita, Tam Harita", "R$ 8 – 17", "Meraklı, ilk temas"],
           ["Orta", "AI Arama, Sandık Adı, Seçmen No.", "R$ 26 – 53", "Etkileşimli kullanıcı"],
           ["İleri", "STK Adı, Sahne Adı, Bebek Adı, İmza, İşletme Adı", "R$ 35 – 44", "Profesyonel, girişimci"],
           ["Premium", "Çift Haritası, Aile Haritası, Ekip Uyumu İK ★, Kolektif Bonus", "R$ 98", "Yüksek gelir, kurumsal kullanım"],
           ["B2B", "Kurumsal paketler, lisanslar, hediyeler", "Talep üzerine", "Şirketler ve ekipler"],
        ],
        "portfolio_rodape": "24 ürün, kullanıcının ilk temastan yinelenen premium müşteriye kadar tüm yolculuğunu kapsar — dil ve pazar başına LTV'yi maksimize eder. Öne çıkan: Ekip Uyumu İK (R$ 98) — kurumsal İK pazarında öncü ürün, ideal enerji 8.",
        "negocio_titulo": "İş Modeli: 3 Gelir Kaynağı",
        "negocio_texto": "A1ELOS, çeşitlendirilmiş ve ölçeklenebilir gelirle tasarlanmıştır: küresel ölçekte son tüketiciye doğrudan satışlar, yüksek değerli B2B sözleşmeleri ve yinelenen coğrafi konumlu reklam — birbirini besleyen üç motor.",
        "negocio_colunas": [
            ("B2C — 14 Dil", "Tüm para birimlerinde dijital ürünlerin doğrudan satışı, PPP'ye göre uyarlanmış fiyatlarla. AI ile otomatik ölçek — büyümeyle orantılı hizmet ekibi olmadan."),
            ("B2B — Aşamalı İndirimler", "İK, işveren markası ve kurumsal hediyeler için kurumsal paketler. Hacme göre %10 ila %50 indirim. 2.000 kodun üzerinde doğrudan müzakere (Elmas Planı). Sözleşmeler DUNS 942242668 tarafından desteklenir."),
            ("Coğrafi Konumlu Reklam", "Ülkeye, kıtaya veya dünyaya göre segmentlere ayrılmış, otomatik rotasyonlu bannerlar. Yüksek değerli aylık yinelenen gelir — ürün satış hacmine bağımlılık olmadan."),
        ],
        "banners_titulo": "Reklam Bannerları — Yinelenen Aylık Gelir",
        "banners_texto": "A1ELOS platformu, coğrafi konumla hassas segmentasyon sunan premium reklam alanları sunar — ülke, kıta veya dünya. Her 8 saniyede otomatik rotasyon ve masaüstü ve mobil için optimize edilmiş formatlarla, bannerlar bölgesel ve uluslararası reklamverenlere ölçülebilir görünürlük sağlar.",
        "banners_tabela": [
            ["Segmentasyon", "Sabit (R$/ay)", "Geçici (R$/ay)", "Reklamveren Profili"],
            ["Ülke", "R$ 800", "R$ 500", "Yerel KOBİ'ler, bölgesel ticaret"],
            ["Kıta", "R$ 1.800", "R$ 1.200", "Bölgesel markalar, kıta genişlemesi"],
            ["Dünya", "R$ 3.500", "R$ 2.500", "Küresel şirketler, uluslararası uygulamalar"],
            ["Özel Sponsorluk", "R$ 6.000", "R$ 4.500/kampanya", "Ana sponsorlar, lansmanlar"],
        ],
        "banners_formatos": "728×90 px — Masaüstü merkez banner · 320×100 px — Optimize edilmiş mobil format · 8 saniye — Otomatik rotasyon · Coğrafi hedefleme — Ülke, kıta veya dünya çapında erişim",
        "b2b_titulo": "B2B Kurumsal Paketler — Yüksek Değer, Yüksek Hacim",
        "b2b_texto": "B2B Paketleri, A1ELOS'u bir işveren markası ve kurumsal sağlıklı yaşam aracına dönüştürür. Bu stratejinin merkezinde özel ve sürekli ürün yer alır: Ekip Uyumu İK (R$ 98). Tek seferlik hediyelerden farklı olarak, uyum analizi şirketin günlük rutinine entegre ettiği bir insan yönetimi aracıdır — bölümleri ve ekipleri istenen enerjiyle hesaplar ve bir bölümün tüm üyelerini aynı ritim ve uyum içinde senkronize eder. Küçük ve büyük şirketler için idealdir; İnsan Kaynakları Departmanı'nın sürekli kullandığı hizmettir ve hızla büyüyen pazarlarla desteklenir: HR Tech (CAGR %10,35), Employer Branding (CAGR %11,19) ve Corporate Wellness (CAGR %6,12).",
        "b2b_planos": [
            ("Temel Plan · 50 kod", "50× Ekspres Harita (her biri R$ 8). Çalışan yan hak programları ve oryantasyon eylemleri için idealdir."),
            ("Orta Plan · 100 kod", "50× Ekspres Harita + 50× AI Arama (R$ 17). Ekipler ve işveren markası stratejisi için mükemmeldir."),
            ("Premium Plan · 200 kod", "100× Ekspres Harita + 100× Tam Harita (R$ 17). Büyük gruplar için maksimum analitik derinlik."),
        ],
        "b2b_tabela": [
            ["Başlangıç", "İndirim", "Profil", "Önerilen Kullanım"],
            ["10 kod", "%10", "Küçük ekipler", "Tek seferlik sağlıklı yaşam eylemi"],
            ["50 kod", "%20", "Büyüyen ekipler", "Yinelenen programlar"],
            ["100 kod", "%25", "KOBİ'ler", "Üç aylık yan hak"],
            ["200 kod", "%30", "Orta ölçekli şirketler", "Tam programlar"],
            ["500 kod", "%40", "Orta ölçekli şirketler", "Çalışanlara yıllık hediye"],
            ["1.000 kod", "%45", "Büyük şirketler", "Müşteri sadakati"],
            ["2.000 kod", "%50", "Büyük gruplar", "Geniş ölçek"],
            ["2.000'in üzerinde", "Müzakere edilebilir", "Özel Elmas Planı", "Toplu bonus dağıtımı"],
        ],
        "rh_destaque_titulo": "Ekip Uyumu İK — Özel Ürün",
        "rh_destaque_texto": "Yöneticiler ve çalışanlar arasındaki ve aynı ekibin üyeleri arasındaki enerjik uyum analizi (ideal enerji: 8 sayısı — güç, liderlik ve maddi denge), A1ELOS'u kurumsal İK pazarında öncü olarak konumlandırır. Bölümün enerjik uyumu kişiler arası sürtüşmeleri azaltır, tutum ve düşünceleri hizalar, personel devrini düşürür, organizasyonel iklimi güçlendirir ve üretkenliği artırır — tek seferlik hediye olarak Kolektif Bonus'un sunmadığı bir değer. Kısa vadeli büyümeyi ve yinelenen B2B gelirini taşıyan ürün budur.",
        "projecoes_titulo": "Finansal Projeksiyonlar: 50 Yıllık Ufuk",
        "projecoes_texto": "Projeksiyonlar, ~5,32 milyar konuşanın potansiyel pazarı üzerindeki yüzde nüfuz tahminlerine dayanmaktadır; %3 muhafazakâr dönüşüm ve %70 ile %90 arasında bonus kullanımı ile. 24. ürün — Ekip Uyumu İK (R$ 98) ve Kolektif/Kurumsal Bonus kanalı ile — İK B2B geliri, doğrulanmış pazarlara dayanan projeksiyona dahil olur: HR Tech (CAGR %10,35), Employer Branding (CAGR %11,19) ve Corporate Wellness (CAGR %6,12). Kısa vadeli (1–5. yıllar) yeni B2B cephesinin hızlanan büyümesini vurgular; uzun vadeli, modelin adreslenebilir pazarı tamamen özümseyene kadar sürekli istikrarını yansıtır.",
        "projecoes_tabela": [
            ["Ufuk", "Muhafazakâr (R$)", "İyimser (R$)"],
            ["1. Yıl", "R$ 318k", "R$ 810k"],
            ["2. Yıl", "R$ 630k", "R$ 1,8M"],
            ["3. Yıl", "R$ 1,20M", "R$ 3,50M"],
            ["4. Yıl", "R$ 2,2M", "R$ 6,2M"],
            ["5. Yıl", "R$ 3,70M", "R$ 9,6M"],
        ],
        "projecoes_tabela_50": [
            ["Ufuk", "Muhafazakâr (R$)", "İyimser (R$)"],
            ["1. Yıl", "R$ 318k", "R$ 810k"],
            ["3. Yıl", "R$ 1,20M", "R$ 3,50M"],
            ["5. Yıl", "R$ 3,70M", "R$ 9,6M"],
            ["7. Yıl", "R$ 7,8M", "R$ 20,5M"],
            ["10. Yıl", "R$ 16,3M", "R$ 44,0M"],
            ["20. Yıl", "R$ 64M", "R$ 184M"],
            ["30. Yıl", "R$ 133M", "R$ 359M"],
            ["40. Yıl", "R$ 202M", "R$ 606M"],
            ["50. Yıl", "R$ 276M", "R$ 869M"],
        ],
        "projecoes_curto_titulo": "Finansal Projeksiyonlar: Kısa Vade (1–5. Yıllar)",
        "projecoes_curto_texto": "Kısa vade, yeni İK B2B cephesinin (Ekip Uyumu + Kolektif Bonus) hızlanan büyümesini vurgular — muhafazakâr senaryoda 5 yılda neredeyse 12 kat — uzun vadeli istikrardan önce.",
        "projecoes_curto_tabela": [
            ["Ufuk", "Muhafazakâr (R$)", "İyimser (R$)"],
            ["1. Yıl", "R$ 318k", "R$ 810k"],
            ["2. Yıl", "R$ 630k", "R$ 1,8M"],
            ["3. Yıl", "R$ 1,20M", "R$ 3,50M"],
            ["4. Yıl", "R$ 2,2M", "R$ 6,2M"],
            ["5. Yıl", "R$ 3,70M", "R$ 9,6M"],
         ],
        "tracao_titulo": "Çekiş ve Kanıtlanmış Sonuçlar",
        "tracao_texto": "A1ELOS, modeli doğrulayan ürün metrikleriyle zaten faaliyet göstermektedir — yüksek elde tutma, premium puanlama ve büyüyen B2B ortak tabanı, platformun son kullanıcıya ve kurumsal pazara gerçek değer sunduğunu kanıtlar.",
        "tracao_kpis": [
            ("12K+", "Aktif Kullanıcı", "Tutarlı büyüyen organik taban"),
            ("%87", "Elde Tutma", "Sektör ortalamasının (~%30) çok üzerinde"),
            ("4,8★", "Ortalama Puan", "Kanıtlanmış son kullanıcı memnuniyeti"),
            ("23", "B2B Ortağı", "Şirketler ve İK departmanlarıyla aktif sözleşmeler"),
        ],
        "roteiro_titulo": "Stratejik Yol Haritası",
        "roteiro_texto": "A1ELOS, mevcut tabanın konsolidasyonundan küresel pazar liderliğine, yatırımcılar için net çıkış seçenekleriyle dört aşamalı bir plan yürütür.",
        "roteiro_fases": [
            ("Aşama 1 · Konsolidasyon", "Zaten aktif olan dillerde kullanıcı tabanının güçlendirilmesi. Dönüşüm, elde tutma ve LTV optimizasyonu. Tohum Turu tamamlandı."),
            ("Aşama 2 · Genişleme", "3 yeni pazarda resmi lansman: Endonezya, Türkiye ve Vietnam. B2B kanalının ve coğrafi konumlu reklamın hızlandırılması."),
            ("Aşama 3 · Küresel Giriş", "Yerelleştirilmiş kampanyalarla 14 dilin tamamında aktif varlık. 5+ kıtada white-label ortaklıkları. Seri A."),
            ("Aşama 4 · Liderlik", "Konsolide operasyonlarla 20+ ülke. Uygulamalı numerolojide küresel referans SaaS platformu. IPO veya stratejik çıkış."),
        ],
        "invest_titulo": "Yatırım ve İletişim",
        "invest_texto": "Özel sunumlar, durum tespiti ve müzakereler için hazırız. Tercih ettiğiniz kanaldan bize ulaşın.",
        "invest_dados": [
            ("Tohum Turu", "R$ 3,5 milyon"),
            ("Pre-Money Değerleme", "R$ 14 milyon"),
            ("Sunulan Özsermaye", "En fazla %20"),
        ],
        "invest_contato": [
            ("Yatırımcı E-postası", "a1elos.consultoria@gmail.com"),
            ("Genel E-posta", "contato@a1elos.com"),
            ("Web Sitesi", "www.a1elos.com"),
            ("DUNS", "942242668 — Dun & Bradstreet"),
        ],
        "invest_alocacao": "Sermaye Tahsisi: %45 Teknoloji · %30 Pazarlama · %25 Operasyon",
        "frase_final": "Sayılar asla yalan söylemez.",
        "selo_final": ["DUNS 942242668", "24 ÜRÜN", "14 DİL", "~5,3 MİLYAR KONUŞAN"],
        "graf_cons": "Muhafazakâr",
        "graf_otim": "İyimser",
        "grafico_titulo_linha": "Öngörülen Büyüme (R$ bin)",
        "pix_titulo": "Brezilya: Pix Altyapısı",
        "pix_texto": "Pix, Brezilya'nın kamu anlık ödeme altyapısıdır. A1ELOS için anında tahsilat, düşük maliyet ve evrensel kabul garanti eder — Brezilya pazarındaki B2C operasyonunun temeli ve uluslararası genişlemenin kapısı.",
        "pix_kpis": [
            ("30,1 milyar", "2025'te işlem", "2024'e göre +%20 · Febraban"),
            ("%76,4", "nüfus Pix kullanıyor", "211 milyon Brezilyalı · Merkez Bankası"),
            ("R$ 68,2 trilyon", "2025'in 2. yarısında hareket ettirildi", "78,4 milyar işlem · Merkez Bankası"),
            ("~80 milyar", "2025'te işlem", "Önceki yıla göre +%25,7 · Pix Raporu"),
        ],
        "pix_fonte": "Kaynaklar: Brezilya Merkez Bankası (Pix Rakamlarla) ve Febraban (Bankacılık Teknolojisi Araştırması).",
        "ref_titulo": "Bibliyografik Referanslar",
        "ref_intro": "Bu sunumun pazar verileri, projeksiyonları ve göstergeleri için kullanılan kaynaklar.",
        "ref_lista": [
            ("Global Wellness Institute", "Küresel sağlıklı yaşam ekonomisi: US$ 6,8 trilyon (2024) → US$ 9,8 trilyon (2029)."),
            ("MarkNtel Advisors", "Astroloji ve numeroloji uygulamaları: US$ 3 milyar → 2030'a kadar US$ 9 milyar (CAGR ~%20)."),
            ("IMF · Dünya Bankası", "Ülkelere göre GSYİH ve satın alma gücü paritesi (PPP)."),
            ("Brezilya Merkez Bankası", "Pix'in resmi istatistikleri: işlemler, hacim ve kullanıcılar."),
            ("Febraban", "Bankacılık Teknolojisi Araştırması — 2025'te Pix büyümesi."),
            ("IBGE", "Brezilya'nın nüfusu ve sosyoekonomik göstergeleri."),
        ],
        },

"vi": {
        "titulo": "A1ELOS Global Numerology",
        "subtitulo": "Khoa học về các con số ứng dụng vào thành công của bạn",
        "capa_nota": "Bài thuyết trình chiến lược cho Nhà đầu tư và Đối tác",
        "confidencial": "BẢO MẬT",
        "ano": "2026",
        "sumario_titulo": "Tóm tắt điều hành",
        "duns_porque": "Vì sao DUNS quan trọng?",
        "preco_consciente": "Định giá có ý thức",
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
        "fonte_receita": "Nguồn doanh thu",
        "participacao": "Tỷ trọng",
        "b2c_linha": "B2C — 14 ngôn ngữ",
        "b2b_linha": "B2B — Chiết khấu lũy tiến",
        "pub_linha": "Quảng cáo định vị địa lý",
        "tabela_descontos": "Bảng chiết khấu lũy tiến",
        "grafico_anos": ["Năm 1", "Năm 3", "Năm 5"],
        "grafico_titulo": "Dự báo thận trọng (R$ nghìn)",
        "grafico_titulo_linha": "Tăng trưởng dự kiến (R$ nghìn)",
        "fale_conosco": "Liên hệ với chúng tôi",
        "sumario_intro": "Bài thuyết trình này được cấu trúc để hướng dẫn các nhà đầu tư và đối tác qua mọi khía cạnh chiến lược của A1ELOS Global Numerology — từ luận điểm thị trường đến mô hình doanh thu định kỳ.",
        "sumario_cards": [
            ("01", "Về A1ELOS", "Công ty mẹ, danh mục và chứng chỉ DUNS"),
            ("02", "Cơ hội thị trường", "Nền kinh tế sức khỏe toàn cầu US$ 6,8 nghìn tỷ"),
            ("03", "Giải pháp và Phạm vi toàn cầu", "14 ngôn ngữ, ~5,3 tỷ người nói"),
            ("04", "Thị trường mới", "Indonesia, Thổ Nhĩ Kỳ, Việt Nam và Nhân sự doanh nghiệp"),
            ("05", "Danh mục và Giá cả", "24 sản phẩm được hiệu chỉnh theo sức mua"),
            ("06", "Doanh thu định kỳ", "Banner quảng cáo và Gói B2B"),
            ("07", "Dự báo và Đầu tư", "Tầm nhìn 50 năm · Vòng hạt giống R$ 3,5M"),
        ],
        "sobre_titulo": "Về A1ELOS",
        "sobre_texto": "A1ELOS là công ty mẹ về công nghệ và tri thức kết hợp trí tuệ nhân tạo, thần số học ứng dụng và chiến lược văn hóa để tạo ra các sản phẩm số có tác động cao trên quy mô toàn cầu. Sứ mệnh của chúng tôi: dân chủ hóa tri thức bản thân bằng số với sự tôn trọng văn hóa và tôn trọng sức mua của từng thị trường.",
        "sobre_kpis": [
            ("23", "Sản phẩm hoạt động", "Trong 4 cấp truy cập"),
            ("14", "Ngôn ngữ", "~67% dân số thế giới"),
            ("5,3 tỷ", "Người nói", "Thị trường thực có thể tiếp cận"),
            ("AI", "Tích hợp", "Công cụ cá nhân hóa"),
        ],
        "sobre_duns": "DUNS 942242668 — Chứng nhận Dun & Bradstreet có hiệu lực tại hơn 190 quốc gia, cho phép hợp đồng B2B và liên doanh quốc tế.",
        "duns_titulo": "Uy tín quốc tế",
        "duns_texto": "Số DUNS là hộ chiếu doanh nghiệp của A1ELOS trên trường quốc tế. Nó báo hiệu cho các đối tác, khách hàng doanh nghiệp và nhà đầu tư rằng công ty có danh tính có thể xác minh, lịch sử có thể truy vết và năng lực hợp đồng tại bất kỳ khu vực tài phán nào.",
        "duns_numero": "942242668",
        "duns_emitido": "Do Dun & Bradstreet cấp — tiêu chuẩn toàn cầu về danh tính doanh nghiệp được công nhận tại hơn 190 quốc gia.",
        "duns_paises": "190+ QUỐC GIA",
        "duns_beneficios": [
            ("Hợp đồng B2B", "Đủ điều kiện tham gia đấu thầu và nhà cung cấp toàn cầu"),
            ("Liên doanh", "Quan hệ đối tác quốc tế với thẩm định thuận lợi"),
            ("Uy tín tức thì", "Dấu hiệu nghiêm túc đối với nhà đầu tư tổ chức"),
        ],
        "mercado_titulo": "Cơ hội thị trường",
        "mercado_texto": "Chúng ta đang sống trong sự hội tụ hoàn hảo: sức khỏe số bùng nổ trên toàn cầu trong khi thần số học và chiêm tinh học chuyển sang các ứng dụng tương tác cao. A1ELOS định vị chính xác tại điểm giao thoa này, với 74% dân số thế giới đã trực tuyến (~6 tỷ người).",
        "mercado_cards": [
            ("Sức khỏe toàn cầu", "US$ 6,8 nghìn tỷ → US$ 9,8 nghìn tỷ vào 2029 (+7,6%/năm)"),
            ("Ứng dụng Chiêm tinh/Thần số", "US$ 3 tỷ → US$ 9 tỷ vào 2030 · CAGR 20%"),
            ("Ứng dụng Sức khỏe", "CAGR 14,9% → US$ 26,2 tỷ vào 2030"),
            ("Người dùng trực tuyến", "74% thế giới · ~6 tỷ người"),
        ],
        "mercado_rh_titulo": "Thị trường mới: Nhân sự doanh nghiệp — Sản phẩm thứ 24",
        "mercado_rh_texto": "Sản phẩm thứ 24 — Tương thích đội ngũ HR (R$ 98) — mở ra thị trường B2B chính của A1ELOS: nhân sự doanh nghiệp. Phân tích tương thích năng lượng giữa quản lý và nhân viên (năng lượng lý tưởng: số 8) định vị nền tảng như công cụ tiên phong về thương hiệu nhà tuyển dụng và sức khỏe doanh nghiệp, với chiết khấu lũy tiến từ 10% đến 50% và đàm phán trực tiếp trên 2.000 mã (Kế hoạch Kim cương).",
        "mercado_rh_vantagens": [
            "Hài hòa năng lượng của bộ phận → giảm xung đột giữa các cá nhân và tăng sự gắn kết đội ngũ",
            "Căn chỉnh thái độ và suy nghĩ giữa quản lý và nhân viên → giao tiếp trôi chảy hơn",
            "Giảm tỷ lệ nghỉ việc (turnover) và giữ chân nhân tài tốt hơn",
            "Môi trường tổ chức tích cực → tăng năng suất và sức khỏe",
            "Thương hiệu nhà tuyển dụng mạnh hơn → thu hút nhân tài phù hợp với văn hóa",
        ],
        "mercado_rh_cards": [
            ["HR Tech", "US$ 42,34 tỷ (2025) → US$ 77,74 tỷ (2031)", "CAGR 10,35% · Mordor Intelligence"],
            ["Employer Branding", "US$ 1,89 tỷ (2025) → US$ 3,62 tỷ (2031)", "CAGR 11,19% · Mordor Intelligence"],
            ["Corporate Wellness", "US$ 66,31 tỷ (2025) → US$ 94,5 tỷ (2031)", "CAGR 6,12% · Mordor Intelligence"],
        ],
        "problema_titulo": "Vấn đề chúng tôi giải quyết",
        "problema_col_esq_titulo": "Khiếm khuyết của thị trường hiện tại",
        "problema_col_esq": [
            ("Rào cản ngôn ngữ", "Đại đa số công cụ thần số học chỉ hoạt động bằng tiếng Anh, loại trừ hàng tỷ người bản ngữ của các ngôn ngữ khác."),
            ("Giá tách rời thực tế", "Sản phẩm định giá bằng đô la cho thị trường mới nổi tạo ra sự loại trừ kinh tế — người dùng không từ chối sản phẩm, mà từ chối mức giá không thể tiếp cận."),
            ("Thiếu chiều sâu", "Công cụ chung chung đưa ra câu trả lời hời hợt không cá nhân hóa, không bối cảnh văn hóa và không ứng dụng thực tế vào đời sống hàng ngày."),
        ],
        "problema_col_dir_titulo": "Cái giá của sự loại trừ",
        "problema_col_dir": "Khi một nền tảng bỏ qua ngôn ngữ và sức mua, nó tự nguyện từ bỏ thị trường lớn nhất thế giới: hơn 4 tỷ người sống trong các nền kinh tế mới nổi và nói các ngôn ngữ không phải tiếng Anh. Đó chính là khoảng trống mà A1ELOS lấp đầy với độ chính xác phẫu thuật.",
        "problema_destaque": "Các nền tảng bỏ qua sức mua địa phương mất quyền truy cập vào hơn 60% thị trường toàn cầu có thể tiếp cận.",
        "solucao_titulo": "Giải pháp của chúng tôi: 3 Trụ cột chiến lược",
        "solucao_texto": "A1ELOS đã xây dựng một nền tảng tích hợp kết hợp khoa học con số, trí tuệ nhân tạo và sự nhạy cảm văn hóa. Giải pháp hoạt động trên ba mặt trận bổ trợ, đảm bảo doanh thu đa dạng và tỷ lệ giữ chân cao.",
        "solucao_colunas": [
            ("Bản đồ cá nhân", "Phân tích số học sâu sắc và được cá nhân hóa cho người dùng cuối — danh tính, sứ mệnh, chu kỳ cuộc đời và sự tương thích — được giao bằng 14 ngôn ngữ với AI tích hợp."),
            ("Thần số doanh nghiệp", "Chẩn đoán thần số học ứng dụng cho thương hiệu, CNPJ, ngày thành lập và chiến lược doanh nghiệp. Sản phẩm khác biệt có giá trị nhận thức cao trên thị trường B2B."),
            ("White-Label B2B", "Cấp phép nền tảng cho các công ty đối tác muốn cung cấp thần số học dưới thương hiệu riêng — với hỗ trợ đa ngôn ngữ và tùy chỉnh hoàn toàn."),
        ],
        "alcance_titulo": "Phạm vi toàn cầu: 14 ngôn ngữ · ~5,3 tỷ người nói",
        "alcance_texto": "A1ELOS bao phủ ~67% dân số thế giới bằng một nền tảng thực sự đa ngôn ngữ. Mỗi ngôn ngữ đại diện cho một thị trường văn hóa riêng biệt, với giá được hiệu chỉnh theo sức mua địa phương.",
        "mercados_titulo": "3 thị trường mới: +442 triệu người nói",
        "mercados_texto": "Việc mở rộng chiến lược sang Indonesia, Thổ Nhĩ Kỳ và Việt Nam đại diện cho một bước nhảy vọt về chất: các thị trường có tăng trưởng kinh tế cao, độ phủ kỹ thuật số ngày càng tăng và nhu cầu đã được chứng minh về các giải pháp sức khỏe số giá phải chăng.",
        "mercados_cards": [
            ("Indonesia", ["285 triệu dân", "80,5% độ phủ internet", "~255 triệu người nói tiếng Indonesia", "Sức khỏe: US$ 51,2 tỷ (2025) → US$ 72,8 tỷ (2034)"]),
            ("Thổ Nhĩ Kỳ", ["85,9 triệu dân", "GDP PPP bình quân đầu người US$ 37.301", "~90 triệu người nói tiếng Thổ Nhĩ Kỳ", "Trên mức trung bình thế giới (US$ 27.211)"]),
            ("Việt Nam",  ["~100 triệu dân", "GDP bình quân đầu người ~US$ 5.066 (+7,4%/năm)", "~97 triệu người nói tiếng Việt", "Sức khỏe: US$ 303 triệu (2025) → US$ 485 triệu (2030)"]),
        ],
        "mercados_rodape": "3 thị trường mới = +442 triệu người nói mới có thể tiếp cận — được tích hợp vào nền tảng với định giá được hiệu chỉnh theo văn hóa.",
        "preco_titulo": "Triết lý định giá có ý thức",
        "preco_esq": "Tôn trọng văn hóa + tôn trọng sức mua = thị trường thực có thể tiếp cận. Cùng tỷ lệ giá trị. Giá khác nhau. Phẩm giá bình đẳng cho mọi thị trường.",
        "preco_dir_titulo": "Cách hoạt động trên thực tế",
        "preco_dir": "A1ELOS áp dụng Ngang giá Sức mua (PPP) làm tiêu chí định giá trung tâm. Cùng một sản phẩm mang lại giá trị tương đối như nhau cho người dùng ở Lagos, Jakarta, Hà Nội hay New York — giá được hiệu chỉnh để nỗ lực tài chính tỷ lệ với thu nhập địa phương.",
        "preco_pilares": [
            ("Hiệu chỉnh PPP", "Giá được điều chỉnh theo chỉ số sức mua của từng quốc gia"),
            ("Tôn trọng văn hóa", "Ngôn ngữ, tiền tệ và bối cảnh địa phương được tích hợp vào sản phẩm"),
            ("Chuyển đổi vượt trội", "Giá công bằng tạo ra nhiều chuyển đổi hơn và giữ chân lâu dài tốt hơn"),
        ],
        "portfolio_titulo": "Danh mục: 24 sản phẩm trong 4 cấp",
        "portfolio_texto": "Cấu trúc phân tầng đảm bảo mọi hồ sơ người dùng — từ người tò mò đến chuyên gia — tìm được đề xuất phù hợp với mức độ tương tác và năng lực tài chính.",
        "portfolio_tabela": [
           ["Cấp", "Sản phẩm", "Khoảng giá (R$)", "Hồ sơ"],
           ["Cơ bản", "Bản đồ Nhanh, Bản đồ Đầy đủ", "R$ 8 – 17", "Tò mò, tiếp xúc đầu tiên"],
           ["Trung cấp", "Tìm kiếm AI, Tên trong phiếu bầu, Số cử tri", "R$ 26 – 53", "Người dùng tương tác"],
           ["Nâng cao", "Tên tổ chức, Tên nghệ danh, Tên em bé, Chữ ký, Tên doanh nghiệp", "R$ 35 – 44", "Chuyên gia, doanh nhân"],
           ["Cao cấp", "Bản đồ Cặp đôi, Bản đồ Gia đình, Tương thích đội ngũ HR ★, Thưởng tập thể", "R$ 98", "Thu nhập cao, sử dụng doanh nghiệp"],
           ["B2B", "Gói doanh nghiệp, giấy phép, quà tặng", "Theo yêu cầu", "Công ty và đội ngũ"],
        ],
        "portfolio_rodape": "24 sản phẩm bao phủ toàn bộ hành trình người dùng, từ tiếp xúc đầu tiên đến khách hàng cao cấp định kỳ — tối đa hóa LTV theo từng ngôn ngữ và thị trường. Điểm nhấn: Tương thích đội ngũ HR (R$ 98) — sản phẩm tiên phong trên thị trường nhân sự doanh nghiệp, năng lượng lý tưởng 8.",
        "negocio_titulo": "Mô hình kinh doanh: 3 nguồn doanh thu",
        "negocio_texto": "A1ELOS được thiết kế với doanh thu đa dạng và có thể mở rộng: bán trực tiếp cho người tiêu dùng cuối trên quy mô toàn cầu, hợp đồng B2B giá trị cao và quảng cáo định vị địa lý định kỳ — ba động cơ nuôi dưỡng lẫn nhau.",
        "negocio_colunas": [
            ("B2C — 14 ngôn ngữ", "Bán trực tiếp sản phẩm số bằng mọi loại tiền tệ, với giá điều chỉnh theo PPP. Mở rộng tự động qua AI — không cần đội ngũ hỗ trợ tỷ lệ với tăng trưởng."),
            ("B2B — Chiết khấu lũy tiến", "Gói doanh nghiệp cho nhân sự, thương hiệu nhà tuyển dụng và quà tặng tổ chức. Chiết khấu từ 10% đến 50% theo khối lượng. Trên 2.000 mã, đàm phán trực tiếp (Kế hoạch Kim cương). Hợp đồng được DUNS 942242668 bảo trợ."),
            ("Quảng cáo định vị địa lý", "Banner được phân khúc theo quốc gia, châu lục hoặc toàn cầu với luân chuyển tự động. Doanh thu định kỳ hàng tháng giá trị cao — không phụ thuộc vào khối lượng bán sản phẩm."),
        ],
        "banners_titulo": "Banner quảng cáo — Doanh thu định kỳ hàng tháng",
        "banners_texto": "Nền tảng A1ELOS cung cấp không gian quảng cáo cao cấp với phân khúc chính xác theo vị trí địa lý — quốc gia, châu lục hoặc toàn cầu. Với luân chuyển tự động mỗi 8 giây và định dạng tối ưu cho máy tính và di động, các banner mang lại tầm nhìn có thể đo lường cho nhà quảng cáo khu vực và quốc tế.",
        "banners_tabela": [
            ["Phân khúc", "Cố định (R$/tháng)", "Tạm thời (R$/tháng)", "Hồ sơ nhà quảng cáo"],
            ["Quốc gia", "R$ 800", "R$ 500", "DN vừa và nhỏ địa phương, thương mại khu vực"],
            ["Châu lục", "R$ 1.800", "R$ 1.200", "Thương hiệu khu vực, mở rộng châu lục"],
            ["Toàn cầu", "R$ 3.500", "R$ 2.500", "Công ty toàn cầu, ứng dụng quốc tế"],
            ["Tài trợ độc quyền", "R$ 6.000", "R$ 4.500/chiến dịch", "Nhà tài trợ chính, ra mắt sản phẩm"],
        ],
        "banners_formatos": "728×90 px — Banner trung tâm máy tính · 320×100 px — Định dạng di động tối ưu · 8 giây — Luân chuyển tự động · Nhắm mục tiêu địa lý — Quốc gia, châu lục hoặc phạm vi toàn cầu",
        "b2b_titulo": "Gói doanh nghiệp B2B — Giá trị cao, Khối lượng lớn",
        "b2b_texto": "Các Gói B2B biến A1ELOS thành công cụ thương hiệu nhà tuyển dụng và sức khỏe doanh nghiệp. Trọng tâm của chiến lược này là sản phẩm độc quyền và liên tục: Tương thích đội ngũ HR (R$ 98). Khác với quà tặng một lần, phân tích tương thích là công cụ quản lý con người mà doanh nghiệp tích hợp vào hoạt động hàng ngày — tính toán các bộ phận và đội ngũ với năng lượng mong muốn và đồng bộ hóa mọi thành viên của một bộ phận trong cùng một nhịp điệu và hòa hợp. Lý tưởng cho doanh nghiệp nhỏ và lớn, đây là dịch vụ Phòng Nhân sự sử dụng liên tục, được hỗ trợ bởi các thị trường tăng trưởng mạnh: HR Tech (CAGR 10,35%), Employer Branding (CAGR 11,19%) và Corporate Wellness (CAGR 6,12%).",
        "b2b_planos": [
            ("Gói Cơ bản · 50 mã", "50× Bản đồ Nhanh (mỗi bản R$ 8). Lý tưởng cho chương trình phúc lợi nhân viên và hoạt động hội nhập."),
            ("Gói Trung cấp · 100 mã", "50× Bản đồ Nhanh + 50× Tìm kiếm AI (R$ 17). Hoàn hảo cho đội ngũ và chiến lược thương hiệu nhà tuyển dụng."),
            ("Gói Cao cấp · 200 mã", "100× Bản đồ Nhanh + 100× Bản đồ Đầy đủ (R$ 17). Độ sâu phân tích tối đa cho các nhóm lớn."),
        ],
        "b2b_tabela": [
            ["Bắt đầu từ", "Chiết khấu", "Hồ sơ", "Sử dụng khuyến nghị"],
            ["10 mã", "10%", "Đội ngũ nhỏ", "Hoạt động sức khỏe một lần"],
            ["50 mã", "20%", "Đội ngũ đang phát triển", "Chương trình định kỳ"],
            ["100 mã", "25%", "DN vừa và nhỏ", "Phúc lợi hàng quý"],
            ["200 mã", "30%", "Doanh nghiệp vừa", "Chương trình đầy đủ"],
            ["500 mã", "40%", "Doanh nghiệp vừa", "Quà tặng hàng năm cho nhân viên"],
            ["1.000 mã", "45%", "Tập đoàn lớn", "Giữ chân khách hàng"],
            ["2.000 mã", "50%", "Tập đoàn lớn", "Quy mô lớn"],
            ["Trên 2.000", "Có thể thương lượng", "Kế hoạch Kim cương riêng", "Phân phối thưởng theo khối lượng"],
        ],
        "rh_destaque_titulo": "Tương thích đội ngũ HR — Sản phẩm độc quyền",
        "rh_destaque_texto": "Phân tích tương thích năng lượng giữa quản lý và nhân viên, và giữa các thành viên của cùng một đội (năng lượng lý tưởng: số 8 — quyền lực, lãnh đạo và cân bằng vật chất), định vị A1ELOS là người tiên phong trên thị trường nhân sự doanh nghiệp. Sự hài hòa năng lượng của bộ phận giảm xung đột giữa các cá nhân, căn chỉnh thái độ và suy nghĩ, giảm tỷ lệ nghỉ việc, củng cố môi trường tổ chức và nâng cao năng suất — giá trị mà Thưởng tập thể, như một món quà một lần, không mang lại. Đây là sản phẩm duy trì tăng trưởng ngắn hạn và doanh thu B2B định kỳ.",
        "projecoes_titulo": "Dự báo tài chính: Tầm nhìn 50 năm",
        "projecoes_texto": "Các dự báo được xây dựng dựa trên ước tính tỷ lệ thâm nhập trên thị trường tiềm năng ~5,32 tỷ người nói, với tỷ lệ chuyển đổi thận trọng 3% và tỷ lệ đổi thưởng từ 70% đến 90%. Với sản phẩm thứ 24 — Tương thích đội ngũ HR (R$ 98) và kênh Thưởng tập thể/Doanh nghiệp —, doanh thu B2B nhân sự được đưa vào dự báo, neo vào các thị trường đã xác minh: HR Tech (CAGR 10,35%), Employer Branding (CAGR 11,19%) và Corporate Wellness (CAGR 6,12%). Ngắn hạn (năm 1–5) cho thấy tăng trưởng tăng tốc của mặt trận B2B mới; dài hạn phản ánh sự ổn định liên tục của mô hình cho đến khi hấp thụ hoàn toàn thị trường có thể tiếp cận.",
        "projecoes_tabela": [
            ["Tầm nhìn", "Thận trọng (R$)", "Lạc quan (R$)"],
            ["Năm 1", "R$ 318k", "R$ 810k"],
            ["Năm 2", "R$ 630k", "R$ 1,8M"],
            ["Năm 3", "R$ 1,20M", "R$ 3,50M"],
            ["Năm 4", "R$ 2,2M", "R$ 6,2M"],
            ["Năm 5", "R$ 3,70M", "R$ 9,6M"],
        ],
        "projecoes_tabela_50": [
            ["Tầm nhìn", "Thận trọng (R$)", "Lạc quan (R$)"],
            ["Năm 1", "R$ 318k", "R$ 810k"],
            ["Năm 3", "R$ 1,20M", "R$ 3,50M"],
            ["Năm 5", "R$ 3,70M", "R$ 9,6M"],
            ["Năm 7", "R$ 7,8M", "R$ 20,5M"],
            ["Năm 10", "R$ 16,3M", "R$ 44,0M"],
            ["Năm 20", "R$ 64M", "R$ 184M"],
            ["Năm 30", "R$ 133M", "R$ 359M"],
            ["Năm 40", "R$ 202M", "R$ 606M"],
            ["Năm 50", "R$ 276M", "R$ 869M"],
        ],
        "projecoes_curto_titulo": "Dự báo tài chính: Ngắn hạn (Năm 1–5)",
        "projecoes_curto_texto": "Ngắn hạn cho thấy tăng trưởng tăng tốc của mặt trận B2B nhân sự mới (Tương thích đội ngũ + Thưởng tập thể), gần gấp 12 lần trong 5 năm theo kịch bản thận trọng — trước khi ổn định dài hạn.",
        "projecoes_curto_tabela": [
            ["Tầm nhìn", "Thận trọng (R$)", "Lạc quan (R$)"],
            ["Năm 1", "R$ 318k", "R$ 810k"],
            ["Năm 2", "R$ 630k", "R$ 1,8M"],
            ["Năm 3", "R$ 1,20M", "R$ 3,50M"],
            ["Năm 4", "R$ 2,2M", "R$ 6,2M"],
            ["Năm 5", "R$ 3,70M", "R$ 9,6M"],
         ],
        "tracao_titulo": "Đà tăng trưởng và Kết quả đã chứng minh",
        "tracao_texto": "A1ELOS đã hoạt động với các chỉ số sản phẩm xác thực mô hình — tỷ lệ giữ chân cao, xếp hạng cao cấp và nền tảng đối tác B2B ngày càng tăng chứng minh nền tảng mang lại giá trị thực cho người dùng cuối và thị trường doanh nghiệp.",
        "tracao_kpis": [
            ("12K+", "Người dùng hoạt động", "Nền tảng hữu cơ tăng trưởng ổn định"),
            ("87%", "Giữ chân", "Vượt xa mức trung bình ngành (~30%)"),
            ("4,8★", "Xếp hạng trung bình", "Sự hài lòng đã chứng minh của người dùng cuối"),
            ("23", "Đối tác B2B", "Hợp đồng hoạt động với doanh nghiệp và phòng nhân sự"),
        ],
        "roteiro_titulo": "Lộ trình chiến lược",
        "roteiro_texto": "A1ELOS thực hiện kế hoạch trong bốn giai đoạn tiến triển — từ củng cố nền tảng hiện tại đến vị thế dẫn đầu thị trường toàn cầu, với các phương án thoát rõ ràng cho nhà đầu tư.",
        "roteiro_fases": [
            ("Giai đoạn 1 · Củng cố", "Tăng cường nền tảng người dùng ở các ngôn ngữ đã hoạt động. Tối ưu hóa chuyển đổi, giữ chân và LTV. Vòng hạt giống hoàn tất."),
            ("Giai đoạn 2 · Mở rộng", "Ra mắt chính thức tại 3 thị trường mới: Indonesia, Thổ Nhĩ Kỳ và Việt Nam. Tăng tốc kênh B2B và quảng cáo định vị địa lý."),
            ("Giai đoạn 3 · Thâm nhập toàn cầu", "Hiện diện tích cực ở cả 14 ngôn ngữ với chiến dịch bản địa hóa. Quan hệ đối tác white-label tại 5+ châu lục. Vòng Series A."),
            ("Giai đoạn 4 · Dẫn đầu", "20+ quốc gia với hoạt động hợp nhất. Nền tảng SaaS tham chiếu toàn cầu về thần số học ứng dụng. IPO hoặc thoái vốn chiến lược."),
        ],
        "invest_titulo": "Đầu tư và Liên hệ",
        "invest_texto": "Chúng tôi sẵn sàng cho các buổi thuyết trình riêng, thẩm định và đàm phán. Liên hệ với chúng tôi qua kênh bạn ưa thích.",
        "invest_dados": [
            ("Vòng hạt giống", "R$ 3,5 triệu"),
            ("Định giá Pre-Money", "R$ 14 triệu"),
            ("Vốn cổ phần chào bán", "Đến 20%"),
        ],
        "invest_contato": [
            ("Email nhà đầu tư", "a1elos.consultoria@gmail.com"),
            ("Email chung", "contato@a1elos.com"),
            ("Website", "www.a1elos.com"),
            ("DUNS", "942242668 — Dun & Bradstreet"),
        ],
        "invest_alocacao": "Phân bổ vốn: 45% Công nghệ · 30% Tiếp thị · 25% Vận hành",
        "frase_final": "Các con số không bao giờ nói dối.",
        "selo_final": ["DUNS 942242668", "24 SẢN PHẨM", "14 NGÔN NGỮ", "~5,3 TỶ NGƯỜI NÓI"],
        "graf_cons": "Thận trọng",
        "graf_otim": "Lạc quan",
        "grafico_titulo_linha": "Tăng trưởng dự kiến (R$ nghìn)",
        "pix_titulo": "Brazil: Cơ sở hạ tầng Pix",
        "pix_texto": "Pix là cơ sở hạ tầng thanh toán tức thời công cộng của Brazil. Đối với A1ELOS, nó đảm bảo thu tiền ngay lập tức, chi phí thấp và chấp nhận phổ quát — nền tảng của hoạt động B2C tại thị trường Brazil và cánh cửa mở ra mở rộng quốc tế.",
        "pix_kpis": [
            ("30,1 tỷ", "Giao dịch trong 2025", "+20% so với 2024 · Febraban"),
            ("76,4%", "dân số sử dụng Pix", "211 triệu người Brazil · Ngân hàng Trung ương"),
            ("R$ 68,2 nghìn tỷ", "luân chuyển trong nửa cuối 2025", "78,4 tỷ giao dịch · Ngân hàng Trung ương"),
            ("~80 tỷ", "giao dịch trong 2025", "+25,7% so với năm trước · Báo cáo Pix"),
        ],
        "pix_fonte": "Nguồn: Ngân hàng Trung ương Brazil (Pix bằng số) và Febraban (Khảo sát Công nghệ Ngân hàng).",
        "ref_titulo": "Tài liệu tham khảo",
        "ref_intro": "Các nguồn được sử dụng cho dữ liệu thị trường, dự báo và chỉ số của bài thuyết trình này.",
        "ref_lista": [
            ("Global Wellness Institute", "Nền kinh tế sức khỏe toàn cầu: US$ 6,8 nghìn tỷ (2024) → US$ 9,8 nghìn tỷ (2029)."),
            ("MarkNtel Advisors", "Ứng dụng chiêm tinh và thần số học: US$ 3 tỷ → US$ 9 tỷ vào 2030 (CAGR ~20%)."),
            ("IMF · Ngân hàng Thế giới", "GDP và ngang giá sức mua (PPP) theo quốc gia."),
            ("Ngân hàng Trung ương Brazil", "Thống kê chính thức về Pix: giao dịch, khối lượng và người dùng."),
            ("Febraban", "Khảo sát Công nghệ Ngân hàng — tăng trưởng Pix trong 2025."),
            ("IBGE", "Dân số và chỉ số kinh tế xã hội của Brazil."),
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

    # SLIDE 15b — PROJEÇÕES CURTO PRAZO (1–5 anos)
    cab(c["projecoes_curto_titulo"], 15)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["projecoes_curto_texto"], _fonte(lang), 11, 18 * mm, y,
                largura - 36 * mm, COR_CINZA, 5.5 * mm)
    y -= 8 * mm
    # Tabela curto prazo
    tbl = Table(c["projecoes_curto_tabela"], colWidths=[40*mm, 55*mm, 55*mm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), COR_DOURADO),
        ("TEXTCOLOR", (0,0), (-1,0), white),
        ("FONTNAME", (0,0), (-1,0), _fonte(lang, True)),
        ("FONTSIZE", (0,0), (-1,0), 10),
        ("FONTNAME", (0,1), (-1,-1), _fonte(lang)),
        ("FONTSIZE", (0,1), (-1,-1), 9),
        ("GRID", (0,0), (-1,-1), 0.5, COR_DOURADO),
        ("ALIGN", (1,0), (-1,-1), "CENTER"),
        ("BACKGROUND", (0,1), (-1,-1), COR_FUNDO),
    ]))
    tbl.wrapOn(doc, largura - 36*mm, 60*mm)
    tbl.drawOn(doc, 18*mm, y - 60*mm)
    # Gráfico de barras (conservador x otimista)
    by = y - 70 * mm
    doc.setFillColor(COR_CINZA)
    doc.setFont(_fonte(lang), 9)
    doc.drawString(18 * mm, by, "Conservador")
    doc.setFillColor(COR_DOURADO)
    doc.drawRightString(largura - 18 * mm, by, "Otimista")
    by -= 6 * mm
    maximo = 9.6  # R$ M (ano 5 otimista)
    for i, (ano, cons, otim) in enumerate(c["projecoes_curto_tabela"][1:]):
        by -= 12 * mm
        doc.setFillColor(COR_CINZA)
        doc.setFont(_fonte(lang), 9)
        doc.drawString(18 * mm, by, ano)
        cons_m = float(cons.replace("R$ ", "").replace("k", "e3").replace(",", "").replace("M", "e6"))
        otim_m = float(otim.replace("R$ ", "").replace("k", "e3").replace(",", "").replace("M", "e6"))
        barra_w = (largura - 90 * mm) / 2
        # barra conservador
        doc.setFillColor(HexColor("#8a6d2f"))
        doc.rect(45 * mm, by, barra_w * (cons_m / (maximo * 1e6)), 6 * mm, fill=1, stroke=0)
        # barra otimista
        doc.setFillColor(HexColor("#C9A94E"))
        doc.rect(45 * mm + barra_w + 10 * mm, by, barra_w * (otim_m / (maximo * 1e6)), 6 * mm, fill=1, stroke=0)
    rodape(pagina)
    doc.showPage()
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
CONTEUDO = APRESENTACAO_TEXTOS
