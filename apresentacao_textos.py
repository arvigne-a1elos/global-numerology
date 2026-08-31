# -*- coding: utf-8 -*-
# ============================================================
# apresentacao_textos.py
# Gerador de Apresentação Empresarial A1ELOS — LAYOUT EDITORIAL
# FASE 1: Português completo (textos expandidos + layout rico)
# Próximas fases: tradução para os outros 13 idiomas
# ============================================================
import os, math, logging
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import Table, TableStyle
from reportlab.lib.utils import ImageReader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
LOGO_PATH = os.path.join(STATIC_DIR, "Logo.png")

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
    try:
        for nome, arq in [("DejaVu", "DejaVuSans.ttf"),
                          ("DejaVu-Bold", "DejaVuSans-Bold.ttf")]:
            caminho = os.path.join(STATIC_DIR, arq)
            if os.path.exists(caminho):
                pdfmetrics.registerFont(TTFont(nome, caminho))
                _FONTES_EXTRA[nome] = True
    except Exception as e:
        logger.warning("Fontes extras: %s", e)

def _fonte(lang, negrito=False):
    if lang == "zh":
        return "STSong-Light"
    if lang == "ja":
        return "HeiseiMin-W3"
    if lang in ("ru", "ar", "he", "id", "tr", "vi"):
        if negrito and _FONTES_EXTRA.get("DejaVu-Bold"):
            return "DejaVu-Bold"
        if _FONTES_EXTRA.get("DejaVu"):
            return "DejaVu"
    return FONTES["bold" if negrito else "normal"]

# ------------------------------------------------------------
# CONTEÚDO — PORTUGUÊS EXPANDIDO (FASE 1)
# ------------------------------------------------------------
CONTEUDO = {
    "pt": {
        "titulo": "A1ELOS Global Numerology",
        "subtitulo": "A ciência dos números aplicada ao seu sucesso",
        "capa_nota": "Apresentação para Investidores e Parceiros Estratégicos",
        "confidencial": "CONFIDENCIAL",
        "ano": "2026",

        # SUMÁRIO EXECUTIVO
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

        # SOBRE
        "sobre_titulo": "Sobre a A1ELOS",
        "sobre_texto": "A A1ELOS é uma holding de tecnologia e conhecimento que une inteligência artificial, numerologia aplicada e estratégia cultural para criar produtos digitais de alto impacto em escala global. Nossa missão: democratizar o autoconhecimento numérico com respeito cultural e respeito ao poder aquisitivo de cada mercado.",
        "sobre_kpis": [
            ("23", "Produtos Ativos", "Em 4 níveis de acesso"),
            ("14", "Idiomas", "~67% da população mundial"),
            ("5,3B", "Falantes", "Mercado endereçável real"),
            ("IA", "Integrada", "Motor de personalização"),
        ],
        "sobre_duns": "DUNS 942242668 — Certificação Dun & Bradstreet válida em 190+ países, habilitando contratos B2B e joint ventures internacionais.",

        # CREDIBILIDADE
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

        # MERCADO
        "mercado_titulo": "Oportunidade de Mercado",
        "mercado_texto": "Vivemos a convergência perfeita: o bem-estar digital explode globalmente enquanto a numerologia e astrologia migram para apps de alto engajamento. A A1ELOS está posicionada exatamente nessa interseção, com 74% da população mundial já online (~6 bilhões de pessoas).",
        "mercado_cards": [
            ("Bem-Estar Global", "US$ 6,8 tri → US$ 9,8 tri até 2029 (+7,6% a.a.)"),
            ("Apps Astrologia/Numerologia", "US$ 3 bi → US$ 9 bi até 2030 · CAGR 20%"),
            ("Apps de Bem-Estar", "CAGR 14,9% → US$ 26,2 bi em 2030"),
            ("Usuários Online", "74% do mundo · ~6 bilhões de pessoas"),
        ],

        # PROBLEMA
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

        # SOLUÇÃO
        "solucao_titulo": "Nossa Solução: 3 Pilares Estratégicos",
        "solucao_texto": "A A1ELOS construiu uma plataforma integrada que combina ciência numérica, inteligência artificial e sensibilidade cultural. A solução opera em três frentes complementares, garantindo receita diversificada e alta retenção.",
        "solucao_colunas": [
            ("Mapas Pessoais", "Análises numéricas profundas e personalizadas para o usuário final — identidade, missão, ciclos de vida e compatibilidade — entregues em 14 idiomas com IA integrada."),
            ("Numerologia Empresarial", "Diagnósticos numerológicos aplicados a marcas, CNPJs, datas de fundação e estratégia corporativa. Produto diferenciado de alto valor percebido pelo mercado B2B."),
            ("White-Label B2B", "Licenciamento da plataforma para empresas parceiras que desejam oferecer numerologia sob sua própria marca — com suporte multilíngue e personalização completa."),
        ],

        # ALCANCE
        "alcance_titulo": "Alcance Global: 14 Idiomas · ~5,3 Bilhões de Falantes",
        "alcance_texto": "A A1ELOS cobre ~67% da população mundial com uma plataforma genuinamente multilíngue. Cada idioma representa um mercado cultural distinto, com precificação calibrada ao poder aquisitivo local.",

        # NOVOS MERCADOS
        "mercados_titulo": "Os 3 Novos Mercados: +442 Milhões de Falantes",
        "mercados_texto": "A expansão estratégica para Indonésia, Turquia e Vietnã representa um salto qualitativo: mercados com alto crescimento econômico, penetração digital crescente e demanda comprovada por soluções de bem-estar digital acessíveis.",
        "mercados_cards": [
            ("Indonésia", ["285 mi habitantes", "80,5% penetração de internet", "~255 mi falantes de Indonésio", "Bem-estar: US$ 51,2 bi (2025) → US$ 72,8 bi (2034)"]),
            ("Turquia", ["85,9 mi habitantes", "PIB PPP per capita US$ 37.301", "~90 mi falantes de Turco", "Acima da média mundial (US$ 27.211)"]),
            ("Vietnã",  ["~100 mi habitantes", "PIB per capita ~US$ 5.066 (+7,4%/ano)", "~97 mi falantes de Vietnamita", "Bem-estar: US$ 303 mi (2025) → US$ 485 mi (2030)"]),
        ],
        "mercados_rodape": "3 mercados novos = +442 milhões de novos falantes endereçáveis — incorporados à plataforma com precificação culturalmente calibrada.",

        # PREÇO
        "preco_titulo": "Filosofia de Preço Consciente",
        "preco_esq": "Respeito cultural + respeito ao poder aquisitivo = mercado endereçável real. Mesma proporção de valor. Preços diferentes. Dignidade igual para todos os mercados.",
        "preco_dir_titulo": "Como Funciona na Prática",
        "preco_dir": "A A1ELOS aplica Paridade de Poder de Compra (PPC) como critério central de precificação. O mesmo produto entrega o mesmo valor relativo ao usuário em Lagos, Jacarta, Hanói ou Nova York — o preço é calibrado para que o esforço financeiro seja proporcional à renda local.",
        "preco_pilares": [
            ("Calibração por PPC", "Preços ajustados ao índice de poder aquisitivo de cada país"),
            ("Respeito Cultural", "Idioma, moeda e contexto local integrados ao produto"),
            ("Conversão Superior", "Preço justo gera mais conversão e maior retenção de longo prazo"),
        ],

        # PORTFÓLIO
        "portfolio_titulo": "Portfólio: 23 Produtos em 4 Níveis",
        "portfolio_texto": "A estrutura em camadas garante que cada perfil de usuário — do curioso ao profissional — encontre uma oferta adequada ao seu nível de engajamento e capacidade financeira.",
        "portfolio_tabela": [
            ["Nível", "Produtos", "Faixa de Preço (R$)", "Perfil"],
            ["Entrada", "Mapa Express, Consulta Rápida", "R$ 8", "Curioso, primeiro contato"],
            ["Intermediário", "Pesquisa IA, Mapa Completo, Compatibilidade", "R$ 17", "Usuário engajado"],
            ["Avançado", "Numerologia Empresarial, Ciclos, Missão", "R$ 26–35", "Profissional, empreendedor"],
            ["Premium", "Diagnóstico Completo, White-Label Pessoal", "R$ 44–98", "Alta renda, uso corporativo"],
            ["B2B / Corporativo", "Pacotes empresariais, licenças, brindes", "Sob consulta", "Empresas e RH"],
        ],
        "portfolio_rodape": "23 produtos cobrem toda a jornada do usuário, do primeiro contato ao cliente recorrente premium — maximizando LTV por idioma e mercado.",

        # NEGÓCIO
        "negocio_titulo": "Modelo de Negócio: 3 Fontes de Receita",
        "negocio_texto": "A A1ELOS foi desenhada com receita diversificada e escalável: vendas diretas ao consumidor final em escala global, contratos B2B de alto valor e publicidade geolocalizada recorrente — três motores que se alimentam mutuamente.",
        "negocio_colunas": [
            ("B2C — 14 Idiomas", "Venda direta de produtos digitais em todas as moedas, com precificação adaptada por PPC. Escala automática via IA — sem equipe de atendimento proporcional ao crescimento."),
            ("B2B — Descontos Progressivos", "Pacotes corporativos para RH, employer branding e brindes institucionais. Descontos de 10% a 70% conforme volume. Contratos respaldados pelo DUNS 942242668."),
            ("Publicidade Geolocalizada", "Banners segmentados por país, continente ou mundial com rotação automatizada. Receita recorrente mensal de alto valor — sem dependência de volume de vendas de produto."),
        ],

        # BANNERS
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

        # B2B
        "b2b_titulo": "Pacotes Empresariais B2B — Alto Valor, Alto Volume",
        "b2b_texto": "Os Pacotes B2B transformam a A1ELOS em uma ferramenta de employer branding e bem-estar corporativo. Empresas adquirem códigos de acesso em volume para distribuir como brindes a colaboradores ou clientes — respaldadas pelo DUNS 942242668 para contratos corporativos formais.",
        "b2b_planos": [
            ("Plano Básico · 50 Códigos", "50× Mapa Express (R$ 8 cada). Ideal para programas de bem-estar de colaboradores e ações de onboarding."),
            ("Plano Intermediário · 100 Códigos", "50× Express + 50× Pesquisa IA (R$ 17). Perfeito para RH e estratégias de employer branding."),
            ("Plano Premium · 200 Códigos", "100× Express + 100× Mapa Completo (R$ 17). Máxima profundidade analítica para grandes equipes."),
        ],
        "b2b_tabela": [
            ["A partir de", "Desconto", "Perfil", "Uso Recomendado"],
            ["10 códigos", "10%", "Pequenas equipes", "Ação pontual de bem-estar"],
            ["100 códigos", "30%", "PMEs", "Programa de benefícios trimestral"],
            ["500 códigos", "50%", "Médias empresas", "Brinde anual a colaboradores"],
            ["1.000 códigos", "70%", "Grandes corporações", "Programa de fidelização de clientes"],
        ],

        # PROJEÇÕES
        "projecoes_titulo": "Projeções Financeiras: Horizonte de 50 Anos",
        "projecoes_texto": "As projeções foram construídas com base em dois cenários — conservador e otimista — refletindo diferentes taxas de penetração de mercado, velocidade de expansão B2B e crescimento orgânico por idioma.",
        "projecoes_tabela": [
            ["Horizonte", "Conservador (R$)", "Otimista (R$)"],
            ["Ano 1", "R$ 33k", "R$ 130k"],
            ["Ano 3", "R$ 120k", "R$ 450k"],
            ["Ano 5", "R$ 500k", "R$ 1,5M"],
            ["Ano 10", "R$ 3M", "R$ 8M"],
            ["Ano 20", "R$ 15M", "R$ 40M"],
            ["Ano 30", "R$ 35M", "R$ 90M"],
            ["Ano 40", "R$ 55M", "R$ 150M"],
            ["Ano 50", "R$ 75M", "R$ 250M"],
        ],

        # TRAÇÃO
        "tracao_titulo": "Tração e Resultados Comprovados",
        "tracao_texto": "A A1ELOS já opera com métricas de produto que validam o modelo — alta retenção, avaliação premium e uma base crescente de parceiros B2B demonstram que a plataforma entrega valor real ao usuário final e ao mercado corporativo.",
        "tracao_kpis": [
            ("12K+", "Usuários Ativos", "Base orgânica em crescimento consistente"),
            ("87%", "Retenção", "Muito acima da média da indústria (~30%)"),
            ("4,8★", "Avaliação Média", "Satisfação comprovada do usuário final"),
            ("23", "Parceiros B2B", "Contratos ativos com empresas e RHs"),
        ],

        # ROTEIRO
        "roteiro_titulo": "Roteiro Estratégico",
        "roteiro_texto": "A A1ELOS executa um plano em quatro fases progressivas — da consolidação da base atual à liderança global de mercado, com opções claras de saída para investidores.",
        "roteiro_fases": [
            ("Fase 1 · Consolidação", "Fortalecimento da base de usuários nos idiomas já ativos. Otimização de conversão, retenção e LTV. Rodada Seed concluída."),
            ("Fase 2 · Expansão", "Lançamento oficial nos 3 novos mercados: Indonésia 🇮🇩, Turquia 🇹🇷 e Vietnã 🇻🇳. Aceleração do canal B2B e publicidade geolocalizada."),
            ("Fase 3 · Entrada Global", "Presença ativa em todos os 14 idiomas com campanhas localizadas. Parcerias white-label em 5+ continentes. Série A."),
            ("Fase 4 · Liderança", "20+ países com operações consolidadas. Plataforma SaaS de referência global em numerologia aplicada. IPO ou exit estratégico."),
        ],

        # INVESTIMENTO
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

        # FINAL
        "frase_final": "Os números nunca mentem.",
        "selo_final": ["DUNS 942242668", "23 PRODUTOS", "14 IDIOMAS", "~5,3 BI FALANTES"],
    }
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
# AUXILIARES DE DESENHO
# ------------------------------------------------------------
def _texto_wrap(doc, texto, fonte, tam, x, y, largura_max, cor, entrelinha):
    doc.setFillColor(cor)
    doc.setFont(fonte, tam)
    palavras = texto.split()
    linha = ""
    for p in palavras:
        teste = (linha + " " + p).strip()
        if doc.stringWidth(teste, fonte, tam) <= largura_max:
            linha = teste
        else:
            doc.drawString(x, y, linha)
            y -= entrelinha
            linha = p
    if linha:
        doc.drawString(x, y, linha)
        y -= entrelinha
    return y

def _caixa(doc, x, y, w, h, cor_fundo=None, cor_borda=None, raio=0):
    if cor_fundo:
        doc.setFillColor(cor_fundo)
        doc.rect(x, y, w, h, stroke=0, fill=1)
    if cor_borda:
        doc.setStrokeColor(cor_borda)
        doc.setLineWidth(0.8)
        doc.rect(x, y, w, h, stroke=1, fill=0)

def _bandeira(doc, x, y, w, h, pais):
    """Desenha uma mini-bandeira com retângulos (id, tr, vn)."""
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

def _rodape(doc, largura, altura, lang, c, pagina):
    doc.setFillColor(COR_CINZA_CLARO)
    doc.setFont(_fonte(lang), 8)
    doc.drawCentredString(largura / 2, 10 * mm,
                          f"{c['titulo']} · DUNS 942242668 · {c['confidencial']} {c['ano']}")
    doc.setFillColor(COR_DOURADO)
    doc.setFont(_fonte(lang, True), 9)
    doc.drawRightString(largura - 15 * mm, 10 * mm, str(pagina))

# ------------------------------------------------------------
# CAPA
# ------------------------------------------------------------
def _capa(doc, largura, altura, lang, modo):
    c = CONTEUDO.get(lang, CONTEUDO["pt"])
    doc.setFillColor(COR_PRETO)
    doc.rect(0, 0, largura, altura, stroke=0, fill=1)
    # Logo
    if os.path.exists(LOGO_PATH):
        try:
            iw, ih = ImageReader(LOGO_PATH).getSize()
            lw = min(largura * 0.28, iw)
            lh = lw * ih / iw
            doc.drawImage(LOGO_PATH, (largura - lw) / 2, altura * 0.60,
                          width=lw, height=lh, mask="auto")
        except Exception:
            pass
    doc.setFillColor(COR_DOURADO)
    doc.setFont(_fonte(lang, True), 30 if modo == "texto" else 34)
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

# ------------------------------------------------------------
# PÁGINAS DE CONTEÚDO (layout editorial)
# ------------------------------------------------------------
def _titulo_pagina(doc, largura, altura, lang, titulo, indice=None):
    doc.setFillColor(COR_AZUL)
    doc.rect(0, altura - 18 * mm, largura, 18 * mm, stroke=0, fill=1)
    doc.setFillColor(white)
    doc.setFont(_fonte(lang, True), 16)
    doc.drawString(18 * mm, altura - 12 * mm, titulo)
    if indice is not None:
        doc.setFont(_fonte(lang, True), 11)
        doc.drawRightString(largura - 18 * mm, altura - 12 * mm, "%02d" % indice)

def _kpis_grid(doc, largura, altura, lang, kpis, y, colunas=4):
    margem = 18 * mm
    gap = 6 * mm
    w = (largura - 2 * margem - (colunas - 1) * gap) / colunas
    h = 30 * mm
    x0 = margem
    for i, item in enumerate(kpis):
        if len(item) == 3:
            num, rot, sub = item
        else:
            num, rot = item
            sub = ""
        x = x0 + i * (w + gap)
        _caixa(doc, x, y - h, w, h, COR_FUNDO, COR_DOURADO)
        if len(item) == 2:
            # Card de texto (mercado): título pequeno + texto quebrado
            doc.setFillColor(COR_AZUL)
            doc.setFont(_fonte(lang, True), 9)
            _texto_wrap(doc, num, _fonte(lang, True), 9, x + 4 * mm, y - h + 22 * mm,
                        w - 8 * mm, COR_AZUL, 4 * mm)
            doc.setFillColor(COR_CINZA)
            doc.setFont(_fonte(lang), 7.5)
            _texto_wrap(doc, rot, _fonte(lang), 7.5, x + 4 * mm, y - h + 14 * mm,
                        w - 8 * mm, COR_CINZA, 3.5 * mm)
        else:
            doc.setFillColor(COR_DOURADO)
            doc.setFont(_fonte(lang, True), 22)
            doc.drawCentredString(x + w / 2, y - h + 18 * mm, num)
            doc.setFillColor(COR_PRETO)
            doc.setFont(_fonte(lang, True), 10)
            doc.drawCentredString(x + w / 2, y - h + 10 * mm, rot)
            if sub:
                doc.setFillColor(COR_CINZA)
                doc.setFont(_fonte(lang), 8)
                _texto_wrap(doc, sub, _fonte(lang), 8, x + 4 * mm, y - h + 5 * mm,
                            w - 8 * mm, COR_CINZA, 3.5 * mm)
    return y - h - 6 * mm
def _tabela_editorial(doc, x, y, largura, dados, colunas_pct, tam=9):
    tbl = Table(dados, colWidths=[largura * p for p in colunas_pct])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), COR_AZUL),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), _fonte("pt", True)),
        ("FONTSIZE", (0, 0), (-1, -1), tam),
        ("TEXTCOLOR", (0, 1), (-1, -1), COR_PRETO),
        ("GRID", (0, 0), (-1, -1), 0.4, COR_CINZA_CLARO),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, COR_FUNDO]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    w, h = tbl.wrapOn(doc, largura, 600)
    tbl.drawOn(doc, x, y - h)
    return y - h

# ------------------------------------------------------------
# GERADOR TEXTO (documento editorial)
# ------------------------------------------------------------
def gerar_pdf_texto(lang="pt", caminho_saida=None):
    _registrar_cid()
    _registrar_fontes_extra()
    if lang not in CONTEUDO:
        lang = "pt"
    c = CONTEUDO[lang]
    if not caminho_saida:
        caminho_saida = os.path.join(STATIC_DIR, f"apresentacao_{lang}.pdf")
    largura, altura = A4
    doc = canvas.Canvas(caminho_saida, pagesize=A4)
    pagina = 1

    # CAPA
    _capa(doc, largura, altura, lang, "texto")
    doc.showPage()
    pagina += 1

    # SUMÁRIO EXECUTIVO
    _titulo_pagina(doc, largura, altura, lang, "Sumário Executivo", 1)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["sumario_intro"], _fonte(lang), 11, 18 * mm, y,
                    largura - 36 * mm, COR_CINZA, 5 * mm)
    y -= 8 * mm
    cards = c["sumario_cards"]
    margem = 18 * mm
    gap = 6 * mm
    w = (largura - 2 * margem - 2 * gap) / 3
    h = 26 * mm
    for i, (num, tit, sub) in enumerate(cards):
        col = i % 3
        lin = i // 3
        x = margem + col * (w + gap)
        yy = y - lin * (h + 6 * mm)
        _caixa(doc, x, yy - h, w, h, COR_FUNDO, COR_DOURADO)
        doc.setFillColor(COR_DOURADO)
        doc.setFont(_fonte(lang, True), 18)
        doc.drawString(x + 6 * mm, yy - h + 16 * mm, num)
        doc.setFillColor(COR_PRETO)
        doc.setFont(_fonte(lang, True), 10)
        doc.drawString(x + 6 * mm, yy - h + 10 * mm, tit)
        doc.setFillColor(COR_CINZA)
        doc.setFont(_fonte(lang), 8)
        _texto_wrap(doc, sub, _fonte(lang), 8, x + 6 * mm, yy - h + 5 * mm,
                    w - 12 * mm, COR_CINZA, 3.5 * mm)
    _rodape(doc, largura, altura, lang, c, pagina)
    doc.showPage()
    pagina += 1

    # SOBRE + KPIs
    _titulo_pagina(doc, largura, altura, lang, c["sobre_titulo"], 2)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["sobre_texto"], _fonte(lang), 11.5, 18 * mm, y,
                    largura - 36 * mm, COR_PRETO, 6 * mm)
    y -= 6 * mm
    y = _kpis_grid(doc, largura, altura, lang, c["sobre_kpis"], y, 4)
    y -= 4 * mm
    _caixa(doc, 18 * mm, y - 16 * mm, largura - 36 * mm, 16 * mm, HexColor("#EEF2FA"), COR_AZUL)
    doc.setFillColor(COR_AZUL)
    doc.setFont(_fonte(lang, True), 9)
    _texto_wrap(doc, c["sobre_duns"], _fonte(lang, True), 9, 22 * mm, y - 11 * mm,
                largura - 44 * mm, COR_AZUL, 4 * mm)
    _rodape(doc, largura, altura, lang, c, pagina)
    doc.showPage()
    pagina += 1

    # CREDIBILIDADE (2 colunas)
    _titulo_pagina(doc, largura, altura, lang, c["duns_titulo"], 3)
    y = altura - 32 * mm
    col_w = (largura - 36 * mm - 8 * mm) / 2
    # Esquerda: DUNS gigante
    _caixa(doc, 18 * mm, y - 70 * mm, col_w, 70 * mm, COR_PRETO, COR_DOURADO)
    doc.setFillColor(COR_DOURADO)
    doc.setFont(_fonte(lang, True), 28)
    doc.drawCentredString(18 * mm + col_w / 2, y - 30 * mm, c["duns_numero"])
    doc.setFillColor(white)
    doc.setFont(_fonte(lang), 10)
    _texto_wrap(doc, c["duns_emitido"], _fonte(lang), 10, 24 * mm, y - 44 * mm,
                col_w - 12 * mm, white, 4.5 * mm)
    doc.setFillColor(COR_DOURADO)
    doc.setFont(_fonte(lang, True), 14)
    doc.drawCentredString(18 * mm + col_w / 2, y - 62 * mm, c["duns_paises"])
    # Direita: benefícios
    xr = 18 * mm + col_w + 8 * mm
    doc.setFillColor(COR_PRETO)
    doc.setFont(_fonte(lang, True), 12)
    doc.drawString(xr, y - 8 * mm, "Por que o DUNS importa?")
    yy = y - 16 * mm
    yy = _texto_wrap(doc, c["duns_texto"], _fonte(lang), 10, xr, yy,
                     col_w, COR_CINZA, 4.5 * mm)
    yy -= 6 * mm
    for tit, sub in c["duns_beneficios"]:
        _caixa(doc, xr, yy - 20 * mm, col_w, 20 * mm, COR_FUNDO, COR_DOURADO)
        doc.setFillColor(COR_AZUL)
        doc.setFont(_fonte(lang, True), 10)
        doc.drawString(xr + 5 * mm, yy - 14 * mm, tit)
        doc.setFillColor(COR_CINZA)
        doc.setFont(_fonte(lang), 8)
        _texto_wrap(doc, sub, _fonte(lang), 8, xr + 5 * mm, yy - 10 * mm,
                    col_w - 10 * mm, COR_CINZA, 3.5 * mm)
        yy -= 24 * mm
    _rodape(doc, largura, altura, lang, c, pagina)
    doc.showPage()
    pagina += 1

    # MERCADO
    _titulo_pagina(doc, largura, altura, lang, c["mercado_titulo"], 4)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["mercado_texto"], _fonte(lang), 11.5, 18 * mm, y,
                    largura - 36 * mm, COR_PRETO, 6 * mm)
    y -= 6 * mm
    y = _kpis_grid(doc, largura, altura, lang, c["mercado_cards"], y, 4)
    _rodape(doc, largura, altura, lang, c, pagina)
    doc.showPage()
    pagina += 1

    # PROBLEMA (2 colunas)
    _titulo_pagina(doc, largura, altura, lang, c["problema_titulo"], 5)
    y = altura - 32 * mm
    col_w = (largura - 36 * mm - 8 * mm) / 2
    # Esquerda
    doc.setFillColor(COR_PRETO)
    doc.setFont(_fonte(lang, True), 12)
    doc.drawString(18 * mm, y - 8 * mm, c["problema_col_esq_titulo"])
    yy = y - 16 * mm
    for tit, sub in c["problema_col_esq"]:
        _caixa(doc, 18 * mm, yy - 26 * mm, col_w, 26 * mm, COR_FUNDO, COR_DOURADO)
        doc.setFillColor(COR_AZUL)
        doc.setFont(_fonte(lang, True), 10)
        doc.drawString(22 * mm, yy - 20 * mm, tit)
        doc.setFillColor(COR_CINZA)
        doc.setFont(_fonte(lang), 8)
        _texto_wrap(doc, sub, _fonte(lang), 8, 22 * mm, yy - 15 * mm,
                    col_w - 8 * mm, COR_CINZA, 3.5 * mm)
        yy -= 30 * mm
    # Direita
    xr = 18 * mm + col_w + 8 * mm
    doc.setFillColor(COR_PRETO)
    doc.setFont(_fonte(lang, True), 12)
    doc.drawString(xr, y - 8 * mm, c["problema_col_dir_titulo"])
    yy = y - 16 * mm
    yy = _texto_wrap(doc, c["problema_col_dir"], _fonte(lang), 10, xr, yy,
                     col_w, COR_CINZA, 4.5 * mm)
    yy -= 8 * mm
    _caixa(doc, xr, yy - 34 * mm, col_w, 34 * mm, HexColor("#FFF3E0"), COR_DOURADO)
    doc.setFillColor(COR_PRETO)
    doc.setFont(_fonte(lang, True), 10)
    _texto_wrap(doc, c["problema_destaque"], _fonte(lang, True), 10, xr + 6 * mm,
                yy - 26 * mm, col_w - 12 * mm, COR_PRETO, 4.5 * mm)
    _rodape(doc, largura, altura, lang, c, pagina)
    doc.showPage()
    pagina += 1

    # SOLUÇÃO (3 colunas)
    _titulo_pagina(doc, largura, altura, lang, c["solucao_titulo"], 6)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["solucao_texto"], _fonte(lang), 11.5, 18 * mm, y,
                    largura - 36 * mm, COR_PRETO, 6 * mm)
    y -= 8 * mm
    col_w = (largura - 36 * mm - 2 * 8 * mm) / 3
    for i, (tit, sub) in enumerate(c["solucao_colunas"]):
        x = 18 * mm + i * (col_w + 8 * mm)
        _caixa(doc, x, y - 60 * mm, col_w, 60 * mm, COR_FUNDO, COR_DOURADO)
        doc.setFillColor(COR_AZUL)
        doc.setFont(_fonte(lang, True), 11)
        _texto_wrap(doc, tit, _fonte(lang, True), 11, x + 5 * mm, y - 12 * mm,
                    col_w - 10 * mm, COR_AZUL, 5 * mm)
        doc.setFillColor(COR_CINZA)
        doc.setFont(_fonte(lang), 9)
        _texto_wrap(doc, sub, _fonte(lang), 9, x + 5 * mm, y - 22 * mm,
                    col_w - 10 * mm, COR_CINZA, 4.5 * mm)
    _rodape(doc, largura, altura, lang, c, pagina)
    doc.showPage()
    pagina += 1

    # ALCANCE + TABELA IDIOMAS
    _titulo_pagina(doc, largura, altura, lang, c["alcance_titulo"], 7)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["alcance_texto"], _fonte(lang), 11, 18 * mm, y,
                    largura - 36 * mm, COR_CINZA, 5 * mm)
    y -= 8 * mm
    dados = [["Idioma", "Falantes (mi)"]] + LINHAS_IDIOMAS + [["TOTAL", "~5.320"]]
    y = _tabela_editorial(doc, 18 * mm, y, largura - 36 * mm, dados, [0.6, 0.4], 9)
    _rodape(doc, largura, altura, lang, c, pagina)
    doc.showPage()
    pagina += 1

    # 3 NOVOS MERCADOS (3 colunas com bandeiras)
    _titulo_pagina(doc, largura, altura, lang, c["mercados_titulo"], 8)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["mercados_texto"], _fonte(lang), 11, 18 * mm, y,
                    largura - 36 * mm, COR_CINZA, 5 * mm)
    y -= 8 * mm
    col_w = (largura - 36 * mm - 2 * 8 * mm) / 3
        paises = ["id", "tr", "vn"]
    for i, (tit, itens) in enumerate(c["mercados_cards"]):
        x = 18 * mm + i * (col_w + 8 * mm)
        _caixa(doc, x, y - 70 * mm, col_w, 70 * mm, COR_FUNDO, COR_DOURADO)
        _bandeira(doc, x + 5 * mm, y - 22 * mm, 11 * mm, 7.5 * mm, paises[i])
        doc.setFillColor(COR_AZUL)
        doc.setFont(_fonte(lang, True), 12)
        doc.drawString(x + 19 * mm, y - 12 * mm, tit)
        yy = y - 20 * mm
        for item in itens:
            doc.setFillColor(COR_CINZA)
            doc.setFont(_fonte(lang), 9)
            yy = _texto_wrap(doc, "•  " + item, _fonte(lang), 9, x + 5 * mm, yy,
                             col_w - 10 * mm, COR_CINZA, 4.5 * mm)
    y -= 78 * mm
    _caixa(doc, 18 * mm, y - 18 * mm, largura - 36 * mm, 18 * mm, HexColor("#EEF2FA"), COR_AZUL)
    doc.setFillColor(COR_AZUL)
    doc.setFont(_fonte(lang, True), 9)
    _texto_wrap(doc, c["mercados_rodape"], _fonte(lang, True), 9, 22 * mm, y - 11 * mm,
                largura - 44 * mm, COR_AZUL, 4 * mm)
    _rodape(doc, largura, altura, lang, c, pagina)
    doc.showPage()
    pagina += 1

    # PREÇO (2 colunas)
    _titulo_pagina(doc, largura, altura, lang, c["preco_titulo"], 9)
    y = altura - 32 * mm
    col_w = (largura - 36 * mm - 8 * mm) / 2
    _caixa(doc, 18 * mm, y - 50 * mm, col_w, 50 * mm, COR_PRETO, COR_DOURADO)
    doc.setFillColor(COR_DOURADO)
    doc.setFont(_fonte(lang, True), 12)
    doc.drawString(22 * mm, y - 14 * mm, "Preço Consciente")
    doc.setFillColor(white)
    doc.setFont(_fonte(lang), 10)
    _texto_wrap(doc, c["preco_esq"], _fonte(lang), 10, 22 * mm, y - 22 * mm,
                col_w - 8 * mm, white, 4.5 * mm)
    xr = 18 * mm + col_w + 8 * mm
    doc.setFillColor(COR_PRETO)
    doc.setFont(_fonte(lang, True), 12)
    doc.drawString(xr, y - 8 * mm, c["preco_dir_titulo"])
    yy = y - 16 * mm
    yy = _texto_wrap(doc, c["preco_dir"], _fonte(lang), 10, xr, yy, col_w,
                     COR_CINZA, 4.5 * mm)
    yy -= 6 * mm
    for tit, sub in c["preco_pilares"]:
        _caixa(doc, xr, yy - 20 * mm, col_w, 20 * mm, COR_FUNDO, COR_DOURADO)
        doc.setFillColor(COR_AZUL)
        doc.setFont(_fonte(lang, True), 10)
        doc.drawString(xr + 5 * mm, yy - 14 * mm, tit)
        doc.setFillColor(COR_CINZA)
        doc.setFont(_fonte(lang), 8)
        _texto_wrap(doc, sub, _fonte(lang), 8, xr + 5 * mm, yy - 10 * mm,
                    col_w - 10 * mm, COR_CINZA, 3.5 * mm)
        yy -= 24 * mm
    _rodape(doc, largura, altura, lang, c, pagina)
    doc.showPage()
    pagina += 1

    # PORTFÓLIO (tabela 4 colunas)
    _titulo_pagina(doc, largura, altura, lang, c["portfolio_titulo"], 10)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["portfolio_texto"], _fonte(lang), 11, 18 * mm, y,
                    largura - 36 * mm, COR_CINZA, 5 * mm)
    y -= 8 * mm
    y = _tabela_editorial(doc, 18 * mm, y, largura - 36 * mm,
                          c["portfolio_tabela"], [0.22, 0.38, 0.18, 0.22], 9)
    y -= 6 * mm
    doc.setFillColor(COR_CINZA)
    doc.setFont(_fonte(lang), 9)
    _texto_wrap(doc, c["portfolio_rodape"], _fonte(lang), 9, 18 * mm, y,
                largura - 36 * mm, COR_CINZA, 4 * mm)
    _rodape(doc, largura, altura, lang, c, pagina)
    doc.showPage()
    pagina += 1

    # NEGÓCIO (3 colunas)
    _titulo_pagina(doc, largura, altura, lang, c["negocio_titulo"], 11)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["negocio_texto"], _fonte(lang), 11, 18 * mm, y,
                    largura - 36 * mm, COR_CINZA, 5 * mm)
    y -= 8 * mm
    col_w = (largura - 36 * mm - 2 * 8 * mm) / 3
    for i, (tit, sub) in enumerate(c["negocio_colunas"]):
        x = 18 * mm + i * (col_w + 8 * mm)
        _caixa(doc, x, y - 60 * mm, col_w, 60 * mm, COR_FUNDO, COR_DOURADO)
        doc.setFillColor(COR_AZUL)
        doc.setFont(_fonte(lang, True), 11)
        _texto_wrap(doc, tit, _fonte(lang, True), 11, x + 5 * mm, y - 12 * mm,
                    col_w - 10 * mm, COR_AZUL, 5 * mm)
        doc.setFillColor(COR_CINZA)
        doc.setFont(_fonte(lang), 9)
        _texto_wrap(doc, sub, _fonte(lang), 9, x + 5 * mm, y - 22 * mm,
                    col_w - 10 * mm, COR_CINZA, 4.5 * mm)
    _rodape(doc, largura, altura, lang, c, pagina)
    doc.showPage()
    pagina += 1

    # BANNERS (tabela 4 colunas)
    _titulo_pagina(doc, largura, altura, lang, c["banners_titulo"], 12)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["banners_texto"], _fonte(lang), 11, 18 * mm, y,
                    largura - 36 * mm, COR_CINZA, 5 * mm)
    y -= 8 * mm
    y = _tabela_editorial(doc, 18 * mm, y, largura - 36 * mm,
                          c["banners_tabela"], [0.24, 0.20, 0.24, 0.32], 9)
    y -= 8 * mm
    _caixa(doc, 18 * mm, y - 20 * mm, largura - 36 * mm, 20 * mm, HexColor("#EEF2FA"), COR_AZUL)
    doc.setFillColor(COR_AZUL)
    doc.setFont(_fonte(lang), 9)
    _texto_wrap(doc, c["banners_formatos"], _fonte(lang), 9, 22 * mm, y - 12 * mm,
                largura - 44 * mm, COR_AZUL, 4 * mm)
    _rodape(doc, largura, altura, lang, c, pagina)
    doc.showPage()
    pagina += 1

    # B2B (3 planos + tabela)
    _titulo_pagina(doc, largura, altura, lang, c["b2b_titulo"], 13)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["b2b_texto"], _fonte(lang), 11, 18 * mm, y,
                    largura - 36 * mm, COR_CINZA, 5 * mm)
    y -= 8 * mm
    col_w = (largura - 36 * mm - 2 * 8 * mm) / 3
    for i, (tit, sub) in enumerate(c["b2b_planos"]):
        x = 18 * mm + i * (col_w + 8 * mm)
        _caixa(doc, x, y - 38 * mm, col_w, 38 * mm, COR_FUNDO, COR_DOURADO)
        doc.setFillColor(COR_AZUL)
        doc.setFont(_fonte(lang, True), 10)
        _texto_wrap(doc, tit, _fonte(lang, True), 10, x + 5 * mm, y - 10 * mm,
                    col_w - 10 * mm, COR_AZUL, 4.5 * mm)
        doc.setFillColor(COR_CINZA)
        doc.setFont(_fonte(lang), 8)
        _texto_wrap(doc, sub, _fonte(lang), 8, x + 5 * mm, y - 18 * mm,
                    col_w - 10 * mm, COR_CINZA, 3.8 * mm)
    y -= 46 * mm
    doc.setFillColor(COR_PRETO)
    doc.setFont(_fonte(lang, True), 11)
    doc.drawString(18 * mm, y - 6 * mm, "Tabela de Descontos Progressivos")
    y -= 12 * mm
    _tabela_editorial(doc, 18 * mm, y, largura - 36 * mm,
                      c["b2b_tabela"], [0.22, 0.18, 0.28, 0.32], 9)
    _rodape(doc, largura, altura, lang, c, pagina)
    doc.showPage()
    pagina += 1

    # PROJEÇÕES (tabela)
    _titulo_pagina(doc, largura, altura, lang, c["projecoes_titulo"], 14)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["projecoes_texto"], _fonte(lang), 11, 18 * mm, y,
                    largura - 36 * mm, COR_CINZA, 5 * mm)
    y -= 8 * mm
    _tabela_editorial(doc, 18 * mm, y, largura - 36 * mm,
                      c["projecoes_tabela"], [0.3, 0.35, 0.35], 9)
    _rodape(doc, largura, altura, lang, c, pagina)
    doc.showPage()
    pagina += 1

    # TRAÇÃO (KPIs)
    _titulo_pagina(doc, largura, altura, lang, c["tracao_titulo"], 15)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["tracao_texto"], _fonte(lang), 11, 18 * mm, y,
                    largura - 36 * mm, COR_CINZA, 5 * mm)
    y -= 6 * mm
    _kpis_grid(doc, largura, altura, lang, c["tracao_kpis"], y, 4)
    _rodape(doc, largura, altura, lang, c, pagina)
    doc.showPage()
    pagina += 1

    # ROTEIRO (4 fases em grid)
    _titulo_pagina(doc, largura, altura, lang, c["roteiro_titulo"], 16)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["roteiro_texto"], _fonte(lang), 11, 18 * mm, y,
                    largura - 36 * mm, COR_CINZA, 5 * mm)
    y -= 8 * mm
    col_w = (largura - 36 * mm - 8 * mm) / 2
    for i, (tit, sub) in enumerate(c["roteiro_fases"]):
        col = i % 2
        lin = i // 2
        x = 18 * mm + col * (col_w + 8 * mm)
        yy = y - lin * (44 * mm + 6 * mm)
        _caixa(doc, x, yy - 44 * mm, col_w, 44 * mm, COR_FUNDO, COR_DOURADO)
        doc.setFillColor(COR_AZUL)
        doc.setFont(_fonte(lang, True), 11)
        doc.drawString(x + 5 * mm, yy - 14 * mm, tit)
        doc.setFillColor(COR_CINZA)
        doc.setFont(_fonte(lang), 9)
        _texto_wrap(doc, sub, _fonte(lang), 9, x + 5 * mm, yy - 22 * mm,
                    col_w - 10 * mm, COR_CINZA, 4.5 * mm)
    _rodape(doc, largura, altura, lang, c, pagina)
    doc.showPage()
    pagina += 1

    # INVESTIMENTO (2 colunas)
    _titulo_pagina(doc, largura, altura, lang, c["invest_titulo"], 17)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["invest_texto"], _fonte(lang), 11, 18 * mm, y,
                    largura - 36 * mm, COR_CINZA, 5 * mm)
    y -= 8 * mm
    col_w = (largura - 36 * mm - 8 * mm) / 2
    # Esquerda: dados de investimento
    _caixa(doc, 18 * mm, y - 60 * mm, col_w, 60 * mm, COR_PRETO, COR_DOURADO)
    yy = y - 14 * mm
    for tit, val in c["invest_dados"]:
        doc.setFillColor(COR_DOURADO)
        doc.setFont(_fonte(lang, True), 10)
        doc.drawString(22 * mm, yy, tit)
        doc.setFillColor(white)
        doc.setFont(_fonte(lang, True), 14)
        doc.drawString(22 * mm, yy - 7 * mm, val)
        yy -= 18 * mm
    # Direita: contatos
    xr = 18 * mm + col_w + 8 * mm
    doc.setFillColor(COR_PRETO)
    doc.setFont(_fonte(lang, True), 12)
    doc.drawString(xr, y - 8 * mm, "Fale Conosco")
    yy = y - 16 * mm
    for tit, val in c["invest_contato"]:
        doc.setFillColor(COR_AZUL)
        doc.setFont(_fonte(lang, True), 10)
        doc.drawString(xr, yy, tit)
        doc.setFillColor(COR_CINZA)
        doc.setFont(_fonte(lang), 10)
        doc.drawString(xr, yy - 6 * mm, val)
        yy -= 14 * mm
    y -= 70 * mm
    _caixa(doc, 18 * mm, y - 16 * mm, largura - 36 * mm, 16 * mm, HexColor("#EEF2FA"), COR_AZUL)
    doc.setFillColor(COR_AZUL)
    doc.setFont(_fonte(lang, True), 9)
    doc.drawCentredString(largura / 2, y - 10 * mm, c["invest_alocacao"])
    _rodape(doc, largura, altura, lang, c, pagina)
    doc.showPage()
    pagina += 1

    # PÁGINA FINAL
    doc.setFillColor(COR_PRETO)
    doc.rect(0, 0, largura, altura, stroke=0, fill=1)
    doc.setFillColor(COR_DOURADO)
    doc.setFont(_fonte(lang, True), 20)
    doc.drawCentredString(largura / 2, altura * 0.60, c["frase_final"])
    # Selo
    selo = c["selo_final"]
    margem = 18 * mm
    gap = 6 * mm
    n = len(selo)
    w = (largura - 2 * margem - (n - 1) * gap) / n
    for i, item in enumerate(selo):
        x = margem + i * (w + gap)
        _caixa(doc, x, altura * 0.40, w, 20 * mm, None, COR_DOURADO)
        doc.setFillColor(COR_DOURADO)
        doc.setFont(_fonte(lang, True), 10)
        doc.drawCentredString(x + w / 2, altura * 0.47, item)
    _rodape(doc, largura, altura, lang, c, pagina)
    doc.showPage()

    doc.save()
    logger.info("PDF texto editorial gerado: %s", caminho_saida)
    return caminho_saida

# ------------------------------------------------------------
# GERADOR SLIDES (deck)
# ------------------------------------------------------------

def gerar_pdf_slides(lang="pt", caminho_saida=None):
    """Gera o deck em paisagem (landscape A4) com layout editorial completo."""

    def _sem_emoji(obj):
        """Remove emojis de bandeira (fora do BMP) que o Helvetica não renderiza."""
        if isinstance(obj, dict):
            return {k: _sem_emoji(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [_sem_emoji(v) for v in obj]
        if isinstance(obj, tuple):
            return tuple(_sem_emoji(v) for v in obj)
        if isinstance(obj, str):
            return "".join(ch for ch in obj if ord(ch) < 0x10000)
        return obj

    _registrar_cid()
    _registrar_fontes_extra()
    if lang not in CONTEUDO:
        lang = "pt"
    c = _sem_emoji(CONTEUDO[lang])
    if not caminho_saida:
        caminho_saida = os.path.join(STATIC_DIR, f"apresentacao_slides_{lang}.pdf")
    largura, altura = landscape(A4)
    doc = canvas.Canvas(caminho_saida, pagesize=landscape(A4))
    pagina = 1

    def cab(titulo, indice):
        doc.setFillColor(COR_AZUL)
        doc.rect(0, altura - 20 * mm, largura, 20 * mm, stroke=0, fill=1)
        doc.setFillColor(white)
        tam = 20 if len(titulo) <= 40 else 15
        _texto_wrap(doc, titulo, _fonte(lang, True), tam, 15 * mm, altura - 13 * mm,
                    largura - 40 * mm, white, 9 * mm)
        doc.setFillColor(COR_DOURADO)
        doc.setFont(_fonte(lang, True), 12)
        doc.drawRightString(largura - 15 * mm, altura - 13 * mm, "%02d" % indice)

    def rodape(num):
        _rodape(doc, largura, altura, lang, c, num)

    # ===== SLIDE 1 — CAPA =====
    _capa(doc, largura, altura, lang, "slides")
    doc.showPage()
    pagina += 1

    # ===== SLIDE 2 — SUMÁRIO EXECUTIVO (01) =====
    cab("Sumário Executivo", 1)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["sumario_intro"], _fonte(lang), 12, 18 * mm, y,
                    largura - 36 * mm, COR_CINZA, 6 * mm)
    y -= 8 * mm
    cards = c["sumario_cards"]
    margem = 18 * mm
    gap = 8 * mm
    n_col = 4
    w = (largura - 2 * margem - (n_col - 1) * gap) / n_col
    h = 34 * mm
    for i, (num, tit, sub) in enumerate(cards):
        col = i % n_col
        lin = i // n_col
        x = margem + col * (w + gap)
        yy = y - lin * (h + 8 * mm)
        _caixa(doc, x, yy - h, w, h, COR_FUNDO, COR_DOURADO)
        doc.setFillColor(COR_DOURADO)
        doc.setFont(_fonte(lang, True), 16)
        doc.drawString(x + 6 * mm, yy - h + 20 * mm, num)
        doc.setFillColor(COR_PRETO)
        doc.setFont(_fonte(lang, True), 10)
        _texto_wrap(doc, tit, _fonte(lang, True), 10, x + 6 * mm, yy - h + 12 * mm,
                    w - 12 * mm, COR_PRETO, 5 * mm)
        doc.setFillColor(COR_CINZA)
        _texto_wrap(doc, sub, _fonte(lang), 8, x + 6 * mm, yy - h + 6 * mm,
                    w - 12 * mm, COR_CINZA, 4 * mm)
    rodape(pagina)
    doc.showPage()
    pagina += 1

    # ===== SLIDE 3 — SOBRE A A1ELOS (02) =====
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
    pagina += 1

    # ===== SLIDE 4 — CREDIBILIDADE INTERNACIONAL (03) =====
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
    doc.drawString(xr, y - 8 * mm, "Por que o DUNS importa?")
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

    # ===== SLIDE 5 — OPORTUNIDADE DE MERCADO (04) =====
    cab(c["mercado_titulo"], 4)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["mercado_texto"], _fonte(lang), 12, 18 * mm, y,
                    largura - 36 * mm, COR_PRETO, 6 * mm)
    y -= 10 * mm
    cards = c["mercado_cards"]
    n_col = 4
    w = (largura - 2 * margem - (n_col - 1) * gap) / n_col
    h = 40 * mm
    for i, (tit, sub) in enumerate(cards):
        x = margem + i * (w + gap)
        _caixa(doc, x, y - h, w, h, COR_FUNDO, COR_DOURADO)
        doc.setFillColor(COR_AZUL)
        doc.setFont(_fonte(lang, True), 10)
        _texto_wrap(doc, tit, _fonte(lang, True), 10, x + 5 * mm, y - 12 * mm,
                    w - 10 * mm, COR_AZUL, 4.5 * mm)
        doc.setFillColor(COR_CINZA)
        doc.setFont(_fonte(lang), 8.5)
        _texto_wrap(doc, sub, _fonte(lang), 8.5, x + 5 * mm, y - 20 * mm,
                    w - 10 * mm, COR_CINZA, 4 * mm)
    rodape(pagina)
    doc.showPage()
    pagina += 1

    # ===== SLIDE 6 — O PROBLEMA (05) =====
    cab(c["problema_titulo"], 5)
    y = altura - 32 * mm
    col_w = (largura - 36 * mm - 10 * mm) / 2
    doc.setFillColor(COR_PRETO)
    doc.setFont(_fonte(lang, True), 13)
    doc.drawString(18 * mm, y - 8 * mm, c["problema_col_esq_titulo"])
    yy = y - 16 * mm
    for tit, sub in c["problema_col_esq"]:
        _caixa(doc, 18 * mm, yy - 30 * mm, col_w, 30 * mm, COR_FUNDO, COR_DOURADO)
        doc.setFillColor(COR_AZUL)
        doc.setFont(_fonte(lang, True), 10)
        doc.drawString(22 * mm, yy - 23 * mm, tit)
        doc.setFillColor(COR_CINZA)
        doc.setFont(_fonte(lang), 8)
        _texto_wrap(doc, sub, _fonte(lang), 8, 22 * mm, yy - 17 * mm,
                    col_w - 8 * mm, COR_CINZA, 3.5 * mm)
        yy -= 34 * mm
    xr = 18 * mm + col_w + 10 * mm
    doc.setFillColor(COR_PRETO)
    doc.setFont(_fonte(lang, True), 13)
    doc.drawString(xr, y - 8 * mm, c["problema_col_dir_titulo"])
    yy = y - 16 * mm
    yy = _texto_wrap(doc, c["problema_col_dir"], _fonte(lang), 10, xr, yy,
                     col_w, COR_CINZA, 4.5 * mm)
    yy -= 10 * mm
    _caixa(doc, xr, yy - 40 * mm, col_w, 40 * mm, HexColor("#FFF3E0"), COR_DOURADO)
    doc.setFillColor(COR_PRETO)
    doc.setFont(_fonte(lang, True), 10)
    _texto_wrap(doc, c["problema_destaque"], _fonte(lang, True), 10, xr + 6 * mm,
                yy - 30 * mm, col_w - 12 * mm, COR_PRETO, 4.5 * mm)
    rodape(pagina)
    doc.showPage()
    pagina += 1

    # ===== SLIDE 7 — SOLUÇÃO (06) =====
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

    # ===== SLIDE 8 — ALCANCE GLOBAL + TABELA IDIOMAS (07) =====
    cab(c["alcance_titulo"], 7)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["alcance_texto"], _fonte(lang), 12, 18 * mm, y,
                    largura - 36 * mm, COR_CINZA, 6 * mm)
    y -= 10 * mm
    dados = [["Idioma", "Falantes (mi)"]] + LINHAS_IDIOMAS + [["TOTAL", "~5.320"]]
    _tabela_editorial(doc, 18 * mm, y, largura - 36 * mm, dados, [0.6, 0.4], 9)
    rodape(pagina)
    doc.showPage()
    pagina += 1

    # ===== SLIDE 9 — 3 NOVOS MERCADOS (08) =====
    cab(c["mercados_titulo"], 8)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["mercados_texto"], _fonte(lang), 11, 18 * mm, y,
                    largura - 36 * mm, COR_CINZA, 5.5 * mm)
    y -= 10 * mm
    col_w = (largura - 36 * mm - 2 * 10 * mm) / 3
    for i, (tit, itens) in enumerate(c["mercados_cards"]):
        x = 18 * mm + i * (col_w + 10 * mm)
        _caixa(doc, x, y - 95 * mm, col_w, 95 * mm, COR_FUNDO, COR_DOURADO)
        doc.setFillColor(COR_AZUL)
        doc.setFont(_fonte(lang, True), 13)
        doc.drawString(x + 6 * mm, y - 14 * mm, tit)
        yy = y - 24 * mm
        for item in itens:
            doc.setFillColor(COR_CINZA)
            doc.setFont(_fonte(lang), 9)
            yy = _texto_wrap(doc, "•  " + item, _fonte(lang), 9, x + 6 * mm, yy,
                             col_w - 12 * mm, COR_CINZA, 4.5 * mm)
    y -= 105 * mm
    _caixa(doc, 18 * mm, y - 18 * mm, largura - 36 * mm, 18 * mm, HexColor("#EEF2FA"), COR_AZUL)
    doc.setFillColor(COR_AZUL)
    doc.setFont(_fonte(lang, True), 9)
    _texto_wrap(doc, c["mercados_rodape"], _fonte(lang, True), 9, 22 * mm, y - 12 * mm,
                largura - 44 * mm, COR_AZUL, 4 * mm)
    rodape(pagina)
    doc.showPage()
    pagina += 1

    # ===== SLIDE 10 — FILOSOFIA DE PREÇO (09) =====
    cab(c["preco_titulo"], 9)
    y = altura - 32 * mm
    col_w = (largura - 36 * mm - 10 * mm) / 2
    _caixa(doc, 18 * mm, y - 60 * mm, col_w, 60 * mm, COR_PRETO, COR_DOURADO)
    doc.setFillColor(COR_DOURADO)
    doc.setFont(_fonte(lang, True), 13)
    doc.drawString(22 * mm, y - 16 * mm, "Preço Consciente")
    doc.setFillColor(white)
    doc.setFont(_fonte(lang), 10)
    _texto_wrap(doc, c["preco_esq"], _fonte(lang), 10, 22 * mm, y - 26 * mm,
                col_w - 8 * mm, white, 4.5 * mm)
    xr = 18 * mm + col_w + 10 * mm
    doc.setFillColor(COR_PRETO)
    doc.setFont(_fonte(lang, True), 13)
    doc.drawString(xr, y - 8 * mm, c["preco_dir_titulo"])
    yy = y - 16 * mm
    yy = _texto_wrap(doc, c["preco_dir"], _fonte(lang), 10, xr, yy,
                     col_w, COR_CINZA, 4.5 * mm)
    yy -= 8 * mm
    for tit, sub in c["preco_pilares"]:
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

    # ===== SLIDE 11 — PORTFÓLIO (10) =====
    cab(c["portfolio_titulo"], 10)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["portfolio_texto"], _fonte(lang), 12, 18 * mm, y,
                    largura - 36 * mm, COR_CINZA, 6 * mm)
    y -= 10 * mm
    y = _tabela_editorial(doc, 18 * mm, y, largura - 36 * mm,
                          c["portfolio_tabela"], [0.22, 0.38, 0.18, 0.22], 9)
    y -= 8 * mm
    doc.setFillColor(COR_CINZA)
    doc.setFont(_fonte(lang), 9)
    _texto_wrap(doc, c["portfolio_rodape"], _fonte(lang), 9, 18 * mm, y,
                largura - 36 * mm, COR_CINZA, 4 * mm)
    rodape(pagina)
    doc.showPage()
    pagina += 1

    # ===== SLIDE 12 — MODELO DE NEGÓCIO (11) =====
    cab(c["negocio_titulo"], 11)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["negocio_texto"], _fonte(lang), 12, 18 * mm, y,
                    largura - 36 * mm, COR_CINZA, 6 * mm)
    y -= 10 * mm
    col_w = (largura - 36 * mm - 2 * 10 * mm) / 3
    for i, (tit, sub) in enumerate(c["negocio_colunas"]):
        x = 18 * mm + i * (col_w + 10 * mm)
        _caixa(doc, x, y - 85 * mm, col_w, 85 * mm, COR_FUNDO, COR_DOURADO)
        doc.setFillColor(COR_AZUL)
        doc.setFont(_fonte(lang, True), 11)
        _texto_wrap(doc, tit, _fonte(lang, True), 11, x + 6 * mm, y - 15 * mm,
                    col_w - 12 * mm, COR_AZUL, 5 * mm)
        doc.setFillColor(COR_CINZA)
        doc.setFont(_fonte(lang), 9)
        _texto_wrap(doc, sub, _fonte(lang), 9, x + 6 * mm, y - 26 * mm,
                    col_w - 12 * mm, COR_CINZA, 4.5 * mm)
    rodape(pagina)
    doc.showPage()
    pagina += 1

    # ===== SLIDE 13 — BANNERS (12) =====
    cab(c["banners_titulo"], 12)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["banners_texto"], _fonte(lang), 11, 18 * mm, y,
                    largura - 36 * mm, COR_CINZA, 5.5 * mm)
    y -= 10 * mm
    y = _tabela_editorial(doc, 18 * mm, y, largura - 36 * mm,
                          c["banners_tabela"], [0.24, 0.20, 0.24, 0.32], 9)
    y -= 10 * mm
    _caixa(doc, 18 * mm, y - 24 * mm, largura - 36 * mm, 24 * mm, HexColor("#EEF2FA"), COR_AZUL)
    doc.setFillColor(COR_AZUL)
    doc.setFont(_fonte(lang), 9)
    _texto_wrap(doc, c["banners_formatos"], _fonte(lang), 9, 22 * mm, y - 15 * mm,
                largura - 44 * mm, COR_AZUL, 4 * mm)
    rodape(pagina)
    doc.showPage()
    pagina += 1

    # ===== SLIDE 14 — PACOTES B2B (13) =====
    cab(c["b2b_titulo"], 13)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["b2b_texto"], _fonte(lang), 11, 18 * mm, y,
                    largura - 36 * mm, COR_CINZA, 5.5 * mm)
    y -= 10 * mm
    col_w = (largura - 36 * mm - 2 * 10 * mm) / 3
    for i, (tit, sub) in enumerate(c["b2b_planos"]):
        x = 18 * mm + i * (col_w + 10 * mm)
        _caixa(doc, x, y - 48 * mm, col_w, 48 * mm, COR_FUNDO, COR_DOURADO)
        doc.setFillColor(COR_AZUL)
        doc.setFont(_fonte(lang, True), 10)
        _texto_wrap(doc, tit, _fonte(lang, True), 10, x + 6 * mm, y - 13 * mm,
                    col_w - 12 * mm, COR_AZUL, 4.5 * mm)
        doc.setFillColor(COR_CINZA)
        doc.setFont(_fonte(lang), 8)
        _texto_wrap(doc, sub, _fonte(lang), 8, x + 6 * mm, y - 22 * mm,
                    col_w - 12 * mm, COR_CINZA, 3.8 * mm)
    y -= 58 * mm
    doc.setFillColor(COR_PRETO)
    doc.setFont(_fonte(lang, True), 12)
    doc.drawString(18 * mm, y - 6 * mm, "Tabela de Descontos Progressivos")
    y -= 14 * mm
    _tabela_editorial(doc, 18 * mm, y, largura - 36 * mm,
                      c["b2b_tabela"], [0.22, 0.18, 0.28, 0.32], 9)
    rodape(pagina)
    doc.showPage()
    pagina += 1

    # ===== SLIDE 15 — PROJEÇÕES FINANCEIRAS (14) =====
    cab(c["projecoes_titulo"], 14)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["projecoes_texto"], _fonte(lang), 12, 18 * mm, y,
                    largura - 36 * mm, COR_CINZA, 6 * mm)
    y -= 10 * mm
    _tabela_editorial(doc, 18 * mm, y, largura - 36 * mm,
                      c["projecoes_tabela"], [0.3, 0.35, 0.35], 10)
    rodape(pagina)
    doc.showPage()
    pagina += 1

    # ===== SLIDE 16 — TRAÇÃO E RESULTADOS (15) =====
    cab(c["tracao_titulo"], 15)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["tracao_texto"], _fonte(lang), 12, 18 * mm, y,
                    largura - 36 * mm, COR_CINZA, 6 * mm)
    y -= 12 * mm
    _kpis_grid(doc, largura, altura, lang, c["tracao_kpis"], y, 4)
    rodape(pagina)
    doc.showPage()
    pagina += 1

    # ===== SLIDE 17 — ROTEIRO ESTRATÉGICO (16) =====
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

    # ===== SLIDE 18 — INVESTIMENTO E CONTATO (17) =====
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
    doc.drawString(xr, y - 8 * mm, "Fale Conosco")
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

    # ===== SLIDE 19 — PÁGINA FINAL =====
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
        doc.drawCentredString(x + w / 2, altura * 0.475, item)
    rodape(pagina)
    doc.showPage()

    doc.save()
    logger.info("PDF slides editorial gerado: %s", caminho_saida)
    return caminho_saida

# ------------------------------------------------------------
# ENTRADA PRINCIPAL
# ------------------------------------------------------------
def gerar_apresentacao(lang="pt", modo="texto"):
    if modo == "slides":
        return gerar_pdf_slides(lang)
    return gerar_pdf_texto(lang)

def gerar_todas():
    import sys
    args = [a for a in sys.argv[1:]]
    if not args:
        alvos = [(l, m) for l in CONTEUDO for m in ("texto", "slides")]
    else:
        lang = args[0]
        modo = args[1] if len(args) > 1 else "texto"
        alvos = [(lang, modo)]
    for l, m in alvos:
        try:
            p = gerar_apresentacao(l, m)
            print("OK", l, m, p)
        except Exception as e:
            print("ERRO", l, m, e)

if __name__ == "__main__":
    gerar_todas()
