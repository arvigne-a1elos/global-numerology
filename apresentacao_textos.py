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
from reportlab.platypus import Table, TableStyle, Paragraph

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
LOGO_PATH = os.path.join(STATIC_DIR, "logo.png")
if not os.path.exists(LOGO_PATH):
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
        "capa_nota": "Apresentação Estratégica para Investidores e Parceiros",
        "confidencial": "CONFIDENCIAL",
        "ano": "2026",
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
            ["Entrada", "Mapa Express, Consulta Rápida", "R$ 8", "Curioso, primeiro contato"],
            ["Intermediário", "Pesquisa IA, Mapa Completo, Compatibilidade", "R$ 17", "Usuário engajado"],
            ["Avançado", "Numerologia Empresarial, Ciclos, Missão", "R$ 26–35", "Profissional, empreendedor"],
            ["Premium", "Diagnóstico Completo, White-Label Pessoal", "R$ 44–98", "Alta renda, uso corporativo"],
            ["B2B / Corporativo", "Pacotes empresariais, licenças, brindes", "Sob consulta", "Empresas e RH"],
        ],
        "portfolio_rodape": "23 produtos cobrem toda a jornada do usuário, do primeiro contato ao cliente recorrente premium — maximizando LTV por idioma e mercado.",
        "negocio_titulo": "Modelo de Negócio: 3 Fontes de Receita",
        "negocio_texto": "A A1ELOS foi desenhada com receita diversificada e escalável: vendas diretas ao consumidor final em escala global, contratos B2B de alto valor e publicidade geolocalizada recorrente — três motores que se alimentam mutuamente.",
        "negocio_colunas": [
            ("B2C — 14 Idiomas", "Venda direta de produtos digitais em todas as moedas, com precificação adaptada por PPC. Escala automática via IA — sem equipe de atendimento proporcional ao crescimento."),
            ("B2B — Descontos Progressivos", "Pacotes corporativos para RH, employer branding e brindes institucionais. Descontos de 10% a 70% conforme volume. Contratos respaldados pelo DUNS 942242668."),
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
    },

    "en": {
        "titulo": "A1ELOS Global Numerology",
        "subtitulo": "The science of numbers applied to your success",
        "capa_nota": "Strategic Presentation for Investors and Partners",
        "confidencial": "CONFIDENTIAL",
        "ano": "2026",
        "sumario_intro": "This presentation is structured to guide investors and partners through every strategic aspect of A1ELOS Global Numerology — from the market thesis to the recurring revenue model.",
        "sumario_cards": [
            ("01", "About A1ELOS", "Holding, portfolio and DUNS credential"),
            ("02", "Market Opportunity", "Global wellness economy US$ 6.8 trillion"),
            ("03", "Solution and Global Reach", "14 languages, ~5.3 billion speakers"),
            ("04", "3 New Markets", "Indonesia, Turkey and Vietnam"),
            ("05", "Portfolio and Pricing", "23 products calibrated by purchasing power"),
            ("06", "Recurring Revenue", "Advertising banners and B2B Packages"),
            ("07", "Projections and Investment", "50-year horizon · Seed Round US$ 650k"),
        ],
        "sobre_titulo": "About A1ELOS",
        "sobre_texto": "A1ELOS is a technology and knowledge holding that unites artificial intelligence, applied numerology and cultural strategy to create high-impact digital products on a global scale. Our mission: to democratize numerical self-knowledge with cultural respect and respect for the purchasing power of each market.",
        "sobre_kpis": [
            ("23", "Active Products", "In 4 access levels"),
            ("14", "Languages", "~67% of the world population"),
            ("5.3B", "Speakers", "Real addressable market"),
            ("AI", "Integrated", "Personalization engine"),
        ],
        "sobre_duns": "DUNS 942242668 — Dun & Bradstreet certification valid in 190+ countries, enabling B2B contracts and international joint ventures.",
        "duns_titulo": "International Credibility",
        "duns_texto": "The DUNS number is A1ELOS's corporate passport on the international scene. It signals to partners, corporate clients and investors that the company has verifiable identity, traceable history and contractual capacity in any jurisdiction.",
        "duns_numero": "942242668",
        "duns_emitido": "Issued by Dun & Bradstreet — the global standard of corporate identity recognized in more than 190 countries.",
        "duns_paises": "190+ COUNTRIES",
        "duns_beneficios": [
            ("B2B Contracts", "Enabling for global tenders and suppliers"),
            ("Joint Ventures", "International partnerships with facilitated due diligence"),
            ("Immediate Credibility", "A sign of seriousness for institutional investors"),
        ],
        "mercado_titulo": "Market Opportunity",
        "mercado_texto": "We live the perfect convergence: digital wellness explodes globally while numerology and astrology migrate to high-engagement apps. A1ELOS is positioned exactly at this intersection, with 74% of the world population already online (~6 billion people).",
        "mercado_cards": [
            ("Global Wellness", "US$ 6.8T → US$ 9.8T by 2029 (+7.6% p.a.)"),
            ("Astrology/Numerology Apps", "US$ 3B → US$ 9B by 2030 · CAGR 20%"),
            ("Wellness Apps", "CAGR 14.9% → US$ 26.2B by 2030"),
            ("Online Users", "74% of the world · ~6 billion people"),
        ],
        "problema_titulo": "The Problem We Solve",
        "problema_col_esq_titulo": "Current Market Failures",
        "problema_col_esq": [
            ("Language Barrier", "The vast majority of numerology tools operate only in English, excluding billions of native speakers in other languages."),
            ("Prices Detached from Reality", "Products charged in dollars for emerging markets generate economic exclusion — the user does not reject the product, they reject the inaccessible price."),
            ("Lack of Depth", "Generic tools deliver superficial answers without personalization, without cultural context and without practical application to daily life."),
        ],
        "problema_col_dir_titulo": "The Cost of Exclusion",
        "problema_col_dir": "When a platform ignores language and purchasing power, it voluntarily abandons the largest market in the world: the 4+ billion people living in emerging economies who speak non-Anglophone languages. This is the gap A1ELOS occupies with surgical precision.",
        "problema_destaque": "Platforms that ignore local purchasing power lose access to more than 60% of the global addressable market.",
        "solucao_titulo": "Our Solution: 3 Strategic Pillars",
        "solucao_texto": "A1ELOS built an integrated platform that combines numerical science, artificial intelligence and cultural sensitivity. The solution operates on three complementary fronts, ensuring diversified revenue and high retention.",
        "solucao_colunas": [
            ("Personal Maps", "Deep and personalized numerical analyses for the end user — identity, mission, life cycles and compatibility — delivered in 14 languages with integrated AI."),
            ("Business Numerology", "Numerological diagnostics applied to brands, CNPJs, founding dates and corporate strategy. A differentiated product with high perceived value in the B2B market."),
            ("White-Label B2B", "Platform licensing for partner companies that want to offer numerology under their own brand — with multilingual support and complete customization."),
        ],
        "alcance_titulo": "Global Reach: 14 Languages · ~5.3 Billion Speakers",
        "alcance_texto": "A1ELOS covers ~67% of the world population with a genuinely multilingual platform. Each language represents a distinct cultural market, with pricing calibrated to local purchasing power.",
        "mercados_titulo": "The 3 New Markets: +442 Million Speakers",
        "mercados_texto": "The strategic expansion into Indonesia, Turkey and Vietnam represents a qualitative leap: markets with high economic growth, growing digital penetration and proven demand for accessible digital wellness solutions.",
        "mercados_cards": [
            ("Indonesia", ["285M inhabitants", "80.5% internet penetration", "~255M Indonesian speakers", "Wellness: US$ 51.2B (2025) → US$ 72.8B (2034)"]),
            ("Turkey", ["85.9M inhabitants", "GDP PPP per capita US$ 37,301", "~90M Turkish speakers", "Above the world average (US$ 27,211)"]),
            ("Vietnam",  ["~100M inhabitants", "GDP per capita ~US$ 5,066 (+7.4%/yr)", "~97M Vietnamese speakers", "Wellness: US$ 303M (2025) → US$ 485M (2030)"]),
        ],
        "mercados_rodape": "3 new markets = +442 million new addressable speakers — incorporated into the platform with culturally calibrated pricing.",
        "preco_titulo": "Conscious Pricing Philosophy",
        "preco_esq": "Cultural respect + respect for purchasing power = real addressable market. Same proportion of value. Different prices. Equal dignity for all markets.",
        "preco_dir_titulo": "How It Works in Practice",
        "preco_dir": "A1ELOS applies Purchasing Power Parity (PPP) as its central pricing criterion. The same product delivers the same relative value to the user in Lagos, Jakarta, Hanoi or New York — the price is calibrated so the financial effort is proportional to local income.",
        "preco_pilares": [
            ("PPP Calibration", "Prices adjusted to the purchasing power index of each country"),
            ("Cultural Respect", "Language, currency and local context integrated into the product"),
            ("Superior Conversion", "Fair pricing generates more conversion and greater long-term retention"),
        ],
        "portfolio_titulo": "Portfolio: 23 Products in 4 Levels",
        "portfolio_texto": "The layered structure ensures that every user profile — from the curious to the professional — finds an offer suited to their level of engagement and financial capacity.",
        "portfolio_tabela": [
            ["Level", "Products", "Price Range (US$)", "Profile"],
            ["Entry", "Express Map, Quick Consultation", "US$ 20", "Curious, first contact"],
            ["Intermediate", "AI Research, Full Map, Compatibility", "US$ 44", "Engaged user"],
            ["Advanced", "Business Numerology, Cycles, Mission", "US$ 71–89", "Professional, entrepreneur"],
            ["Premium", "Complete Diagnosis, Personal White-Label", "US$ 116–251", "High income, corporate use"],
            ["B2B / Corporate", "Business packages, licenses, gifts", "On request", "Companies and HR"],
        ],
        "portfolio_rodape": "23 products cover the entire user journey, from first contact to recurring premium customer — maximizing LTV by language and market.",
        "negocio_titulo": "Business Model: 3 Revenue Streams",
        "negocio_texto": "A1ELOS was designed with diversified and scalable revenue: direct sales to the end consumer on a global scale, high-value B2B contracts and recurring geolocated advertising — three engines that feed each other.",
        "negocio_colunas": [
            ("B2C — 14 Languages", "Direct sale of digital products in all currencies, with pricing adapted by PPP. Automatic scaling via AI — without a support team proportional to growth."),
            ("B2B — Progressive Discounts", "Corporate packages for HR, employer branding and institutional gifts. Discounts from 10% to 70% by volume. Contracts backed by DUNS 942242668."),
            ("Geolocated Advertising", "Banners segmented by country, continent or worldwide with automated rotation. High-value recurring monthly revenue — without dependence on product sales volume."),
        ],
        "banners_titulo": "Advertising Banners — Monthly Recurring Revenue",
        "banners_texto": "The A1ELOS platform offers premium advertising spaces with precise segmentation by geolocation — country, continent or worldwide. With automatic rotation every 8 seconds and formats optimized for desktop and mobile, the banners deliver measurable visibility to regional and international advertisers.",
        "banners_tabela": [
            ["Segmentation", "Fixed (US$/month)", "Temporary (US$/month)", "Advertiser Profile"],
            ["Country", "US$ 150", "US$ 95", "Local SMEs, regional commerce"],
            ["Continent", "US$ 340", "US$ 230", "Regional brands, continental expansion"],
            ["World", "US$ 660", "US$ 470", "Global companies, international apps"],
            ["Exclusive Sponsorship", "US$ 1,130", "US$ 850/campaign", "Master sponsors, launches"],
        ],
        "banners_formatos": "728×90 px — Central desktop banner · 320×100 px — Optimized mobile format · 8 seconds — Automatic rotation · Geo-target — Country, continent or worldwide reach",
        "b2b_titulo": "B2B Corporate Packages — High Value, High Volume",
        "b2b_texto": "The B2B Packages turn A1ELOS into an employer branding and corporate wellness tool. Companies purchase access codes in volume to distribute as gifts to employees or clients — backed by DUNS 942242668 for formal corporate contracts.",
        "b2b_planos": [
            ("Basic Plan · 50 Codes", "50× Express Map (US$ 20 each). Ideal for employee wellness programs and onboarding actions."),
            ("Intermediate Plan · 100 Codes", "50× Express + 50× AI Research (US$ 44). Perfect for HR and employer branding strategies."),
            ("Premium Plan · 200 Codes", "100× Express + 100× Full Map (US$ 44). Maximum analytical depth for large teams."),
        ],
        "b2b_tabela": [
            ["From", "Discount", "Profile", "Recommended Use"],
            ["10 codes", "10%", "Small teams", "Punctual wellness action"],
            ["100 codes", "30%", "SMEs", "Quarterly benefits program"],
            ["500 codes", "50%", "Medium companies", "Annual employee gift"],
            ["1,000 codes", "70%", "Large corporations", "Customer loyalty program"],
        ],
        "projecoes_titulo": "Financial Projections: 50-Year Horizon",
        "projecoes_texto": "The projections were built on two scenarios — conservative and optimistic — reflecting different market penetration rates, B2B expansion speed and organic growth by language.",
        "projecoes_tabela": [
            ["Horizon", "Conservative (US$)", "Optimistic (US$)"],
            ["Year 1", "US$ 6k", "US$ 24k"],
            ["Year 3", "US$ 22k", "US$ 84k"],
            ["Year 5", "US$ 94k", "US$ 280k"],
            ["Year 10", "US$ 560k", "US$ 1.5M"],
            ["Year 20", "US$ 2.8M", "US$ 7.5M"],
            ["Year 30", "US$ 6.5M", "US$ 16.8M"],
            ["Year 40", "US$ 10.3M", "US$ 28M"],
            ["Year 50", "US$ 14M", "US$ 46.8M"],
        ],
        "tracao_titulo": "Traction and Proven Results",
        "tracao_texto": "A1ELOS already operates with product metrics that validate the model — high retention, premium rating and a growing base of B2B partners demonstrate that the platform delivers real value to the end user and the corporate market.",
        "tracao_kpis": [
            ("12K+", "Active Users", "Consistent organic growth base"),
            ("87%", "Retention", "Well above industry average (~30%)"),
            ("4.8★", "Average Rating", "Proven end-user satisfaction"),
            ("23", "B2B Partners", "Active contracts with companies and HR"),
        ],
        "roteiro_titulo": "Strategic Roadmap",
        "roteiro_texto": "A1ELOS executes a plan in four progressive phases — from the consolidation of the current base to global market leadership, with clear exit options for investors.",
        "roteiro_fases": [
            ("Phase 1 · Consolidation", "Strengthening the user base in the already active languages. Conversion, retention and LTV optimization. Seed Round completed."),
            ("Phase 2 · Expansion", "Official launch in the 3 new markets: Indonesia, Turkey and Vietnam. Acceleration of the B2B channel and geolocated advertising."),
            ("Phase 3 · Global Entry", "Active presence in all 14 languages with localized campaigns. White-label partnerships in 5+ continents. Series A."),
            ("Phase 4 · Leadership", "20+ countries with consolidated operations. Reference global SaaS platform in applied numerology. IPO or strategic exit."),
        ],
        "invest_titulo": "Investment & Contact",
        "invest_texto": "We are ready for private presentations, due diligence and negotiations. Contact us through your preferred channel.",
        "invest_dados": [
            ("Seed Round", "US$ 650k"),
            ("Pre-Money Valuation", "US$ 2.6M"),
            ("Equity Offered", "Up to 20%"),
        ],
        "invest_contato": [
            ("Investor Email", "a1elos.consultoria@gmail.com"),
            ("General Email", "contato@a1elos.com"),
            ("Website", "www.a1elos.com"),
            ("DUNS", "942242668 — Dun & Bradstreet"),
        ],
        "invest_alocacao": "Capital Allocation: 45% Technology · 30% Marketing · 25% Operations",
        "frase_final": "Numbers never lie.",
        "selo_final": ["DUNS 942242668", "23 PRODUCTS", "14 LANGUAGES", "~5.3B SPEAKERS"],
        "graf_cons": "Conservative",
        "graf_otim": "Optimistic",
        "grafico_titulo_linha": "Projected Growth (US$ thousands)",
    },

    "es": {
        "titulo": "A1ELOS Numerología Global",
        "subtitulo": "La ciencia de los números aplicada a tu éxito",
        "capa_nota": "Presentación Estratégica para Inversores y Socios",
        "confidencial": "CONFIDENCIAL",
        "ano": "2026",
        "sumario_intro": "Esta presentación está estructurada para guiar a inversores y socios por todos los aspectos estratégicos de A1ELOS Numerología Global — desde la tesis de mercado hasta el modelo de ingresos recurrentes.",
        "sumario_cards": [
            ("01", "Sobre A1ELOS", "Holding, portafolio y credencial DUNS"),
            ("02", "Oportunidad de Mercado", "Economía global de bienestar US$ 6,8 billones"),
            ("03", "Solución y Alcance Global", "14 idiomas, ~5,3 mil millones de hablantes"),
            ("04", "3 Nuevos Mercados", "Indonesia, Turquía y Vietnam"),
            ("05", "Portafolio y Precios", "23 productos calibrados por poder adquisitivo"),
            ("06", "Ingresos Recurrentes", "Banners publicitarios y Paquetes B2B"),
            ("07", "Proyecciones e Inversión", "Horizonte de 50 años · Ronda Seed € 120k"),
        ],
        "sobre_titulo": "Sobre A1ELOS",
        "sobre_texto": "A1ELOS es una holding de tecnología y conocimiento que une inteligencia artificial, numerología aplicada y estrategia cultural para crear productos digitales de alto impacto a escala global. Nuestra misión: democratizar el autoconocimiento numérico con respeto cultural y respeto al poder adquisitivo de cada mercado.",
        "sobre_kpis": [
            ("23", "Productos Activos", "En 4 niveles de acceso"),
            ("14", "Idiomas", "~67% de la población mundial"),
            ("5,3B", "Hablantes", "Mercado direccionable real"),
            ("IA", "Integrada", "Motor de personalización"),
        ],
        "sobre_duns": "DUNS 942242668 — Certificación Dun & Bradstreet válida en 190+ países, habilitando contratos B2B y joint ventures internacionales.",
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
        "mercado_texto": "Vivimos la convergencia perfecta: el bienestar digital explota globalmente mientras la numerología y la astrología migran a apps de alto engagement. A1ELOS está posicionada exactamente en esa intersección, con el 74% de la población mundial ya en línea (~6 mil millones de personas).",
        "mercado_cards": [
            ("Bienestar Global", "US$ 6,8 B → US$ 9,8 B hasta 2029 (+7,6% anual)"),
            ("Apps Astrología/Numerología", "US$ 3 B → US$ 9 B hasta 2030 · CAGR 20%"),
            ("Apps de Bienestar", "CAGR 14,9% → US$ 26,2 B en 2030"),
            ("Usuarios en Línea", "74% del mundo · ~6 mil millones de personas"),
        ],
        "problema_titulo": "El Problema que Resolvemos",
        "problema_col_esq_titulo": "Fallos del Mercado Actual",
        "problema_col_esq": [
            ("Barrera de Idioma", "La gran mayoría de las herramientas de numerología opera solo en inglés, excluyendo a miles de millones de hablantes nativos en otros idiomas."),
            ("Precios Desconectados de la Realidad", "Productos cobrados en dólares para mercados emergentes generan exclusión económica — el usuario no rechaza el producto, rechaza el precio inaccesible."),
            ("Falta de Profundidad", "Herramientas genéricas entregan respuestas superficiales sin personalización, sin contexto cultural y sin aplicación práctica al día a día."),
        ],
        "problema_col_dir_titulo": "El Costo de la Exclusión",
        "problema_col_dir": "Cuando una plataforma ignora el idioma y el poder adquisitivo, abandona voluntariamente el mayor mercado del mundo: los 4+ mil millones de personas que viven en economías emergentes y hablan lenguas no anglófonas. Este es el vacío que A1ELOS ocupa con precisión quirúrgica.",
        "problema_destaque": "Las plataformas que ignoran el poder adquisitivo local pierden acceso a más del 60% del mercado direccionable global.",
        "solucao_titulo": "Nuestra Solución: 3 Pilares Estratégicos",
        "solucao_texto": "A1ELOS construyó una plataforma integrada que combina ciencia numérica, inteligencia artificial y sensibilidad cultural. La solución opera en tres frentes complementarios, garantizando ingresos diversificados y alta retención.",
        "solucao_colunas": [
            ("Mapas Personales", "Análisis numéricos profundos y personalizados para el usuario final — identidad, misión, ciclos de vida y compatibilidad — entregados en 14 idiomas con IA integrada."),
            ("Numerología Empresarial", "Diagnósticos numerológicos aplicados a marcas, CNPJs, fechas de fundación y estrategia corporativa. Producto diferenciado de alto valor percibido en el mercado B2B."),
            ("White-Label B2B", "Licenciamiento de la plataforma para empresas socias que deseen ofrecer numerología bajo su propia marca — con soporte multilingüe y personalización completa."),
        ],
        "alcance_titulo": "Alcance Global: 14 Idiomas · ~5,3 Mil Millones de Hablantes",
        "alcance_texto": "A1ELOS cubre ~67% de la población mundial con una plataforma genuinamente multilingüe. Cada idioma representa un mercado cultural distinto, con precios calibrados al poder adquisitivo local.",
        "mercados_titulo": "Los 3 Nuevos Mercados: +442 Millones de Hablantes",
        "mercados_texto": "La expansión estratégica hacia Indonesia, Turquía y Vietnam representa un salto cualitativo: mercados con alto crecimiento económico, penetración digital creciente y demanda comprobada de soluciones de bienestar digital accesibles.",
        "mercados_cards": [
            ("Indonesia", ["285M habitantes", "80,5% penetración de internet", "~255M hablantes de indonesio", "Bienestar: US$ 51,2 B (2025) → US$ 72,8 B (2034)"]),
            ("Turquía", ["85,9M habitantes", "PIB PPC per cápita US$ 37.301", "~90M hablantes de turco", "Por encima del promedio mundial (US$ 27.211)"]),
            ("Vietnam",  ["~100M habitantes", "PIB per cápita ~US$ 5.066 (+7,4%/año)", "~97M hablantes de vietnamita", "Bienestar: US$ 303M (2025) → US$ 485M (2030)"]),
        ],
        "mercados_rodape": "3 nuevos mercados = +442 millones de nuevos hablantes direccionables — incorporados a la plataforma con precios culturalmente calibrados.",
        "preco_titulo": "Filosofía de Precio Consciente",
        "preco_esq": "Respeto cultural + respeto al poder adquisitivo = mercado direccionable real. Misma proporción de valor. Precios diferentes. Dignidad igual para todos los mercados.",
        "preco_dir_titulo": "Cómo Funciona en la Práctica",
        "preco_dir": "A1ELOS aplica la Paridad de Poder Adquisitivo (PPC) como criterio central de precios. El mismo producto entrega el mismo valor relativo al usuario en Lagos, Yakarta, Hanói o Nueva York — el precio se calibra para que el esfuerzo financiero sea proporcional al ingreso local.",
        "preco_pilares": [
            ("Calibración por PPC", "Precios ajustados al índice de poder adquisitivo de cada país"),
            ("Respeto Cultural", "Idioma, moneda y contexto local integrados al producto"),
            ("Conversión Superior", "Precio justo genera más conversión y mayor retención a largo plazo"),
        ],
        "portfolio_titulo": "Portafolio: 23 Productos en 4 Niveles",
        "portfolio_texto": "La estructura en capas garantiza que cada perfil de usuario — del curioso al profesional — encuentre una oferta adecuada a su nivel de engagement y capacidad financiera.",
        "portfolio_tabela": [
            ["Nivel", "Productos", "Rango de Precio (€)", "Perfil"],
            ["Entrada", "Mapa Express, Consulta Rápida", "€ 11", "Curioso, primer contacto"],
            ["Intermedio", "Investigación IA, Mapa Completo, Compatibilidad", "€ 26", "Usuario comprometido"],
            ["Avanzado", "Numerología Empresarial, Ciclos, Misión", "€ 35–53", "Profesional, emprendedor"],
            ["Premium", "Diagnóstico Completo, White-Label Personal", "€ 62–134", "Alta renta, uso corporativo"],
            ["B2B / Corporativo", "Paquetes empresariales, licencias, regalos", "Bajo consulta", "Empresas y RRHH"],
        ],
        "portfolio_rodape": "23 productos cubren todo el recorrido del usuario, del primer contacto al cliente premium recurrente — maximizando el LTV por idioma y mercado.",
        "negocio_titulo": "Modelo de Negocio: 3 Fuentes de Ingresos",
        "negocio_texto": "A1ELOS fue diseñada con ingresos diversificados y escalables: ventas directas al consumidor final a escala global, contratos B2B de alto valor y publicidad geolocalizada recurrente — tres motores que se alimentan mutuamente.",
        "negocio_colunas": [
            ("B2C — 14 Idiomas", "Venta directa de productos digitales en todas las monedas, con precios adaptados por PPC. Escala automática vía IA — sin equipo de soporte proporcional al crecimiento."),
            ("B2B — Descuentos Progresivos", "Paquetes corporativos para RRHH, employer branding y regalos institucionales. Descuentos del 10% al 70% según volumen. Contratos respaldados por DUNS 942242668."),
            ("Publicidad Geolocalizada", "Banners segmentados por país, continente o mundial con rotación automatizada. Ingresos recurrentes mensuales de alto valor — sin dependencia del volumen de ventas de producto."),
        ],
        "banners_titulo": "Banners Publicitarios — Ingresos Recurrentes Mensuales",
        "banners_texto": "La plataforma A1ELOS ofrece espacios publicitarios premium con segmentación precisa por geolocalización — país, continente o mundial. Con rotación automática cada 8 segundos y formatos optimizados para desktop y mobile, los banners entregan visibilidad medible a anunciantes regionales e internacionales.",
        "banners_tabela": [
            ["Segmentación", "Fijo (€/mes)", "Temporal (€/mes)", "Perfil del Anunciante"],
            ["País", "€ 150", "€ 95", "PYMES locales, comercio regional"],
            ["Continente", "€ 340", "€ 230", "Marcas regionales, expansión continental"],
            ["Mundo", "€ 660", "€ 470", "Empresas globales, apps internacionales"],
            ["Patrocinio Exclusivo", "€ 1.130", "€ 850/campaña", "Patrocinadores master, lanzamientos"],
        ],
        "banners_formatos": "728×90 px — Banner central desktop · 320×100 px — Formato mobile optimizado · 8 segundos — Rotación automática · Geo-target — País, continente o alcance mundial",
        "b2b_titulo": "Paquetes Empresariales B2B — Alto Valor, Alto Volumen",
        "b2b_texto": "Los Paquetes B2B convierten a A1ELOS en una herramienta de employer branding y bienestar corporativo. Las empresas adquieren códigos de acceso en volumen para distribuir como regalos a colaboradores o clientes — respaldados por DUNS 942242668 para contratos corporativos formales.",
        "b2b_planos": [
            ("Plan Básico · 50 Códigos", "50× Mapa Express (€ 11 cada). Ideal para programas de bienestar de colaboradores y acciones de onboarding."),
            ("Plan Intermedio · 100 Códigos", "50× Express + 50× Investigación IA (€ 26). Perfecto para RRHH y estrategias de employer branding."),
            ("Plan Premium · 200 Códigos", "100× Express + 100× Mapa Completo (€ 26). Máxima profundidad analítica para grandes equipos."),
        ],
        "b2b_tabela": [
            ["A partir de", "Descuento", "Perfil", "Uso Recomendado"],
            ["10 códigos", "10%", "Equipos pequeños", "Acción puntual de bienestar"],
            ["100 códigos", "30%", "PYMES", "Programa de beneficios trimestral"],
            ["500 códigos", "50%", "Medianas empresas", "Regalo anual a colaboradores"],
            ["1.000 códigos", "70%", "Grandes corporaciones", "Programa de fidelización de clientes"],
        ],
        "projecoes_titulo": "Proyecciones Financieras: Horizonte de 50 Años",
        "projecoes_texto": "Las proyecciones se construyeron sobre dos escenarios — conservador y optimista — reflejando diferentes tasas de penetración de mercado, velocidad de expansión B2B y crecimiento orgánico por idioma.",
        "projecoes_tabela": [
            ["Horizonte", "Conservador (€)", "Optimista (€)"],
            ["Año 1", "€ 6k", "€ 24k"],
            ["Año 3", "€ 22k", "€ 84k"],
            ["Año 5", "€ 94k", "€ 280k"],
            ["Año 10", "€ 560k", "€ 1,5M"],
            ["Año 20", "€ 2,8M", "€ 7,5M"],
            ["Año 30", "€ 6,5M", "€ 16,8M"],
            ["Año 40", "€ 10,3M", "€ 28M"],
            ["Año 50", "€ 14M", "€ 46,8M"],
        ],
        "tracao_titulo": "Tracción y Resultados Comprobados",
        "tracao_texto": "A1ELOS ya opera con métricas de producto que validan el modelo — alta retención, evaluación premium y una base creciente de socios B2B demuestran que la plataforma entrega valor real al usuario final y al mercado corporativo.",
        "tracao_kpis": [
            ("12K+", "Usuarios Activos", "Base orgánica en crecimiento consistente"),
            ("87%", "Retención", "Muy por encima del promedio de la industria (~30%)"),
            ("4,8★", "Evaluación Media", "Satisfacción comprobada del usuario final"),
            ("23", "Socios B2B", "Contratos activos con empresas y RRHH"),
        ],
        "roteiro_titulo": "Ruta Estratégica",
        "roteiro_texto": "A1ELOS ejecuta un plan en cuatro fases progresivas — desde la consolidación de la base actual hasta el liderazgo global de mercado, con opciones claras de salida para inversores.",
        "roteiro_fases": [
            ("Fase 1 · Consolidación", "Fortalecimiento de la base de usuarios en los idiomas ya activos. Optimización de conversión, retención y LTV. Ronda Seed concluida."),
            ("Fase 2 · Expansión", "Lanzamiento oficial en los 3 nuevos mercados: Indonesia, Turquía y Vietnam. Aceleración del canal B2B y publicidad geolocalizada."),
            ("Fase 3 · Entrada Global", "Presencia activa en los 14 idiomas con campañas localizadas. Alianzas white-label en 5+ continentes. Serie A."),
            ("Fase 4 · Liderazgo", "20+ países con operaciones consolidadas. Plataforma SaaS de referencia global en numerología aplicada. IPO o salida estratégica."),
        ],
        "invest_titulo": "Inversión & Contacto",
        "invest_texto": "Estamos listos para presentaciones privadas, due diligence y negociaciones. Contáctanos por el canal de tu preferencia.",
        "invest_dados": [
            ("Ronda Seed", "€ 120k"),
            ("Valuación Pre-Money", "€ 500k"),
            ("Equity Ofrecido", "Hasta 20%"),
        ],
        "invest_contato": [
            ("Email Inversores", "a1elos.consultoria@gmail.com"),
            ("Email General", "contato@a1elos.com"),
            ("Sitio Web", "www.a1elos.com"),
            ("DUNS", "942242668 — Dun & Bradstreet"),
        ],
        "invest_alocacao": "Asignación de Capital: 45% Tecnología · 30% Marketing · 25% Operaciones",
        "frase_final": "Los números nunca mienten.",
        "selo_final": ["DUNS 942242668", "23 PRODUCTOS", "14 IDIOMAS", "~5,3 B HABLANTES"],
        "graf_cons": "Conservador",
        "graf_otim": "Optimista",
        "grafico_titulo_linha": "Crecimiento Proyectado (€ miles)",
    },

    "it": {
        "titulo": "A1ELOS Numerologia Globale",
        "subtitulo": "La scienza dei numeri applicata al tuo successo",
        "capa_nota": "Presentazione Strategica per Investitori e Partner",
        "confidencial": "RISERVATO",
        "ano": "2026",
        "sumario_intro": "Questa presentazione è strutturata per guidare investitori e partner attraverso ogni aspetto strategico di A1ELOS Numerologia Globale — dalla tesi di mercato al modello di ricavi ricorrenti.",
        "sumario_cards": [
            ("01", "Informazioni su A1ELOS", "Holding, portafoglio e credenziale DUNS"),
            ("02", "Opportunità di Mercato", "Economia globale del benessere US$ 6,8 trilioni"),
            ("03", "Soluzione e Portata Globale", "14 lingue, ~5,3 miliardi di parlanti"),
            ("04", "3 Nuovi Mercati", "Indonesia, Turchia e Vietnam"),
            ("05", "Portafoglio e Prezzi", "23 prodotti calibrati per potere d'acquisto"),
            ("06", "Ricavi Ricorrenti", "Banner pubblicitari e Pacchetti B2B"),
            ("07", "Proiezioni e Investimento", "Orizzonte di 50 anni · Round Seed € 120k"),
        ],
        "sobre_titulo": "Informazioni su A1ELOS",
        "sobre_texto": "A1ELOS è una holding di tecnologia e conoscenza che unisce intelligenza artificiale, numerologia applicata e strategia culturale per creare prodotti digitali ad alto impatto su scala globale. La nostra missione: democratizzare la conoscenza di sé numerica con rispetto culturale e rispetto del potere d'acquisto di ogni mercato.",
        "sobre_kpis": [
            ("23", "Prodotti Attivi", "In 4 livelli di accesso"),
            ("14", "Lingue", "~67% della popolazione mondiale"),
            ("5,3B", "Parlanti", "Mercato reale indirizzabile"),
            ("IA", "Integrata", "Motore di personalizzazione"),
        ],
        "sobre_duns": "DUNS 942242668 — Certificazione Dun & Bradstreet valida in 190+ paesi, che abilita contratti B2B e joint venture internazionali.",
        "duns_titulo": "Credibilità Internazionale",
        "duns_texto": "Il numero DUNS è il passaporto aziendale di A1ELOS sulla scena internazionale. Segnala a partner, clienti aziendali e investitori che l'azienda possiede identità verificabile, storia tracciabile e capacità contrattuale in qualsiasi giurisdizione.",
        "duns_numero": "942242668",
        "duns_emitido": "Emesso da Dun & Bradstreet — lo standard globale di identità aziendale riconosciuto in più di 190 paesi.",
        "duns_paises": "190+ PAESI",
        "duns_beneficios": [
            ("Contratti B2B", "Abilitazione per gare globali e fornitori"),
            ("Joint Venture", "Partnership internazionali con due diligence facilitata"),
            ("Credibilità Immediata", "Un segno di serietà per gli investitori istituzionali"),
        ],
        "mercado_titulo": "Opportunità di Mercato",
        "mercado_texto": "Viviamo la convergenza perfetta: il benessere digitale esplode a livello globale mentre numerologia e astrologia migrano verso app ad alto coinvolgimento. A1ELOS è posizionata esattamente in questa intersezione, con il 74% della popolazione mondiale già online (~6 miliardi di persone).",
        "mercado_cards": [
            ("Benessere Globale", "US$ 6,8 B → US$ 9,8 B entro 2029 (+7,6% annuo)"),
            ("App Astrologia/Numerologia", "US$ 3 B → US$ 9 B entro 2030 · CAGR 20%"),
            ("App di Benessere", "CAGR 14,9% → US$ 26,2 B nel 2030"),
            ("Utenti Online", "74% del mondo · ~6 miliardi di persone"),
        ],
        "problema_titulo": "Il Problema che Risolviamo",
        "problema_col_esq_titulo": "Fallimenti del Mercato Attuale",
        "problema_col_esq": [
            ("Barriera Linguistica", "La stragrande maggioranza degli strumenti di numerologia opera solo in inglese, escludendo miliardi di parlanti nativi in altre lingue."),
            ("Prezzi Scollegati dalla Realtà", "Prodotti addebitati in dollari per i mercati emergenti generano esclusione economica — l'utente non rifiuta il prodotto, rifiuta il prezzo inaccessibile."),
            ("Mancanza di Profondità", "Gli strumenti generici forniscono risposte superficiali senza personalizzazione, senza contesto culturale e senza applicazione pratica alla vita quotidiana."),
        ],
        "problema_col_dir_titulo": "Il Costo dell'Esclusione",
        "problema_col_dir": "Quando una piattaforma ignora lingua e potere d'acquisto, abbandona volontariamente il mercato più grande del mondo: i 4+ miliardi di persone che vivono in economie emergenti e parlano lingue non anglofone. Questo è il divario che A1ELOS occupa con precisione chirurgica.",
        "problema_destaque": "Le piattaforme che ignorano il potere d'acquisto locale perdono l'accesso a oltre il 60% del mercato globale indirizzabile.",
        "solucao_titulo": "La Nostra Soluzione: 3 Pilastri Strategici",
        "solucao_texto": "A1ELOS ha costruito una piattaforma integrata che combina scienza numerica, intelligenza artificiale e sensibilità culturale. La soluzione opera su tre fronti complementari, garantendo ricavi diversificati e alta fidelizzazione.",
        "solucao_colunas": [
            ("Mappe Personali", "Analisi numeriche profonde e personalizzate per l'utente finale — identità, missione, cicli di vita e compatibilità — fornite in 14 lingue con IA integrata."),
            ("Numerologia Aziendale", "Diagnosi numerologiche applicate a marchi, CNPJ, date di fondazione e strategia aziendale. Prodotto differenziato ad alto valore percepito nel mercato B2B."),
            ("White-Label B2B", "Licenza della piattaforma per aziende partner che desiderano offrire numerologia sotto il proprio marchio — con supporto multilingue e personalizzazione completa."),
        ],
        "alcance_titulo": "Portata Globale: 14 Lingue · ~5,3 Miliardi di Parlanti",
        "alcance_texto": "A1ELOS copre ~67% della popolazione mondiale con una piattaforma genuinamente multilingue. Ogni lingua rappresenta un mercato culturale distinto, con prezzi calibrati al potere d'acquisto locale.",
        "mercados_titulo": "I 3 Nuovi Mercati: +442 Milioni di Parlanti",
        "mercados_texto": "L'espansione strategica verso Indonesia, Turchia e Vietnam rappresenta un salto qualitativo: mercati con alta crescita economica, crescente penetrazione digitale e domanda comprovata di soluzioni di benessere digitale accessibili.",
        "mercados_cards": [
            ("Indonesia", ["285M abitanti", "80,5% di penetrazione internet", "~255M parlanti indonesiano", "Benessere: US$ 51,2 B (2025) → US$ 72,8 B (2034)"]),
            ("Turchia", ["85,9M abitanti", "PIL PPA pro capite US$ 37.301", "~90M parlanti turco", "Sopra la media mondiale (US$ 27.211)"]),
            ("Vietnam",  ["~100M abitanti", "PIL pro capite ~US$ 5.066 (+7,4%/anno)", "~97M parlanti vietnamita", "Benessere: US$ 303M (2025) → US$ 485M (2030)"]),
        ],
        "mercados_rodape": "3 nuovi mercati = +442 milioni di nuovi parlanti indirizzabili — integrati nella piattaforma con prezzi culturalmente calibrati.",
        "preco_titulo": "Filosofia del Prezzo Consapevole",
        "preco_esq": "Rispetto culturale + rispetto del potere d'acquisto = mercato reale indirizzabile. Stessa proporzione di valore. Prezzi diversi. Dignità uguale per tutti i mercati.",
        "preco_dir_titulo": "Come Funziona in Pratica",
        "preco_dir": "A1ELOS applica la Parità di Potere d'Acquisto (PPA) come criterio centrale di prezzo. Lo stesso prodotto offre lo stesso valore relativo all'utente a Lagos, Giacarta, Hanoi o New York — il prezzo è calibrato affinché lo sforzo finanziario sia proporzionale al reddito locale.",
        "preco_pilares": [
            ("Calibrazione PPA", "Prezzi adeguati all'indice di potere d'acquisto di ogni paese"),
            ("Rispetto Culturale", "Lingua, valuta e contesto locale integrati nel prodotto"),
            ("Conversione Superiore", "Un prezzo giusto genera più conversione e maggiore fidelizzazione a lungo termine"),
        ],
        "portfolio_titulo": "Portafoglio: 23 Prodotti in 4 Livelli",
        "portfolio_texto": "La struttura a livelli garantisce che ogni profilo utente — dal curioso al professionista — trovi un'offerta adatta al proprio livello di coinvolgimento e capacità finanziaria.",
        "portfolio_tabela": [
            ["Livello", "Prodotti", "Fascia di Prezzo (€)", "Profilo"],
            ["Ingresso", "Mappa Express, Consultazione Rapida", "€ 11", "Curioso, primo contatto"],
            ["Intermedio", "Ricerca IA, Mappa Completa, Compatibilità", "€ 26", "Utente coinvolto"],
            ["Avanzato", "Numerologia Aziendale, Cicli, Missione", "€ 35–53", "Professionista, imprenditore"],
            ["Premium", "Diagnosi Completa, White-Label Personale", "€ 62–134", "Alto reddito, uso aziendale"],
            ["B2B / Aziendale", "Pacchetti aziendali, licenze, regali", "Su richiesta", "Aziende e HR"],
        ],
        "portfolio_rodape": "23 prodotti coprono l'intero percorso dell'utente, dal primo contatto al cliente premium ricorrente — massimizzando l'LTV per lingua e mercato.",
        "negocio_titulo": "Modello di Business: 3 Fonti di Ricavo",
        "negocio_texto": "A1ELOS è stata progettata con ricavi diversificati e scalabili: vendite dirette al consumatore finale su scala globale, contratti B2B ad alto valore e pubblicità geolocalizzata ricorrente — tre motori che si alimentano a vicenda.",
        "negocio_colunas": [
            ("B2C — 14 Lingue", "Vendita diretta di prodotti digitali in tutte le valute, con prezzi adattati per PPA. Scalabilità automatica via IA — senza team di supporto proporzionale alla crescita."),
            ("B2B — Sconti Progressivi", "Pacchetti aziendali per HR, employer branding e regali istituzionali. Sconti dal 10% al 70% in base al volume. Contratti supportati da DUNS 942242668."),
            ("Pubblicità Geolocalizzata", "Banner segmentati per paese, continente o mondiale con rotazione automatizzata. Ricavi ricorrenti mensili ad alto valore — senza dipendenza dal volume di vendita dei prodotti."),
        ],
        "banners_titulo": "Banner Pubblicitari — Ricavi Ricorrenti Mensili",
        "banners_texto": "La piattaforma A1ELOS offre spazi pubblicitari premium con segmentazione precisa per geolocalizzazione — paese, continente o mondiale. Con rotazione automatica ogni 8 secondi e formati ottimizzati per desktop e mobile, i banner offrono visibilità misurabile ad inserzionisti regionali e internazionali.",
        "banners_tabela": [
            ["Segmentazione", "Fisso (€/mese)", "Temporaneo (€/mese)", "Profilo Inserzionista"],
            ["Paese", "€ 150", "€ 95", "PMI locali, commercio regionale"],
            ["Continente", "€ 340", "€ 230", "Marchi regionali, espansione continentale"],
            ["Mondo", "€ 660", "€ 470", "Aziende globali, app internazionali"],
            ["Sponsorizzazione Esclusiva", "€ 1.130", "€ 850/campagna", "Sponsor master, lanci"],
        ],
        "banners_formatos": "728×90 px — Banner centrale desktop · 320×100 px — Formato mobile ottimizzato · 8 secondi — Rotazione automatica · Geo-target — Paese, continente o portata mondiale",
        "b2b_titulo": "Pacchetti Aziendali B2B — Alto Valore, Alto Volume",
        "b2b_texto": "I Pacchetti B2B trasformano A1ELOS in uno strumento di employer branding e benessere aziendale. Le aziende acquistano codici di accesso in volume per distribuirli come regali a dipendenti o clienti — supportati da DUNS 942242668 per contratti aziendali formali.",
        "b2b_planos": [
            ("Piano Base · 50 Codici", "50× Mappa Express (€ 11 ciascuna). Ideale per programmi di benessere dei dipendenti e azioni di onboarding."),
            ("Piano Intermedio · 100 Codici", "50× Express + 50× Ricerca IA (€ 26). Perfetto per HR e strategie di employer branding."),
            ("Piano Premium · 200 Codici", "100× Express + 100× Mappa Completa (€ 26). Massima profondità analitica per grandi team."),
        ],
        "b2b_tabela": [
            ["Da", "Sconto", "Profilo", "Uso Consigliato"],
            ["10 codici", "10%", "Piccoli team", "Azione puntuale di benessere"],
            ["100 codici", "30%", "PMI", "Programma di benefit trimestrale"],
            ["500 codici", "50%", "Medie aziende", "Regalo annuale ai dipendenti"],
            ["1.000 codici", "70%", "Grandi aziende", "Programma di fidelizzazione clienti"],
        ],
        "projecoes_titulo": "Proiezioni Finanziarie: Orizzonte di 50 Anni",
        "projecoes_texto": "Le proiezioni sono state costruite su due scenari — conservativo e ottimistico — riflettendo diversi tassi di penetrazione del mercato, velocità di espansione B2B e crescita organica per lingua.",
        "projecoes_tabela": [
            ["Orizzonte", "Conservativo (€)", "Ottimistico (€)"],
            ["Anno 1", "€ 6k", "€ 24k"],
            ["Anno 3", "€ 22k", "€ 84k"],
            ["Anno 5", "€ 94k", "€ 280k"],
            ["Anno 10", "€ 560k", "€ 1,5M"],
            ["Anno 20", "€ 2,8M", "€ 7,5M"],
            ["Anno 30", "€ 6,5M", "€ 16,8M"],
            ["Anno 40", "€ 10,3M", "€ 28M"],
            ["Anno 50", "€ 14M", "€ 46,8M"],
        ],
        "tracao_titulo": "Trazione e Risultati Comprovati",
        "tracao_texto": "A1ELOS opera già con metriche di prodotto che validano il modello — alta fidelizzazione, valutazione premium e una base crescente di partner B2B dimostrano che la piattaforma offre valore reale all'utente finale e al mercato aziendale.",
        "tracao_kpis": [
            ("12K+", "Utenti Attivi", "Base organica in crescita costante"),
            ("87%", "Fidelizzazione", "Ben sopra la media del settore (~30%)"),
            ("4,8★", "Valutazione Media", "Soddisfazione comprovata dell'utente finale"),
            ("23", "Partner B2B", "Contratti attivi con aziende e HR"),
        ],
        "roteiro_titulo": "Roadmap Strategica",
        "roteiro_texto": "A1ELOS esegue un piano in quattro fasi progressive — dal consolidamento della base attuale alla leadership globale di mercato, con chiare opzioni di uscita per gli investitori.",
        "roteiro_fases": [
            ("Fase 1 · Consolidamento", "Rafforzamento della base utenti nelle lingue già attive. Ottimizzazione di conversione, fidelizzazione e LTV. Round Seed concluso."),
            ("Fase 2 · Espansione", "Lancio ufficiale nei 3 nuovi mercati: Indonesia, Turchia e Vietnam. Accelerazione del canale B2B e pubblicità geolocalizzata."),
            ("Fase 3 · Ingresso Globale", "Presenza attiva in tutte le 14 lingue con campagne localizzate. Partnership white-label in 5+ continenti. Serie A."),
            ("Fase 4 · Leadership", "20+ paesi con operazioni consolidate. Piattaforma SaaS di riferimento globale in numerologia applicata. IPO o uscita strategica."),
        ],
        "invest_titulo": "Investimento & Contatto",
        "invest_texto": "Siamo pronti per presentazioni private, due diligence e negoziazioni. Contattaci tramite il canale preferito.",
        "invest_dados": [
            ("Round Seed", "€ 120k"),
            ("Valuazione Pre-Money", "€ 500k"),
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
        "selo_final": ["DUNS 942242668", "23 PRODOTTI", "14 LINGUE", "~5,3 B PARLANTI"],
        "graf_cons": "Conservativo",
        "graf_otim": "Ottimista",
        "grafico_titulo_linha": "Crescita Proiettata (€ migliaia)",
    },
    
    "fr": {
        "titulo": "A1ELOS Numérologie Globale",
        "subtitulo": "La science des nombres appliquée à votre succès",
        "capa_nota": "Présentation Stratégique pour Investisseurs et Partenaires",
        "confidencial": "CONFIDENTIEL",
        "ano": "2026",
        "sumario_intro": "Cette présentation est structurée pour guider investisseurs et partenaires à travers tous les aspects stratégiques d'A1ELOS Numérologie Globale — de la thèse de marché au modèle de revenus récurrents.",
        "sumario_cards": [
            ("01", "À propos d'A1ELOS", "Holding, portefeuille et crédential DUNS"),
            ("02", "Opportunité de Marché", "Économie mondiale du bien-être US$ 6,8 trillions"),
            ("03", "Solution et Portée Globale", "14 langues, ~5,3 milliards de locuteurs"),
            ("04", "3 Nouveaux Marchés", "Indonésie, Turquie et Vietnam"),
            ("05", "Portefeuille et Prix", "23 produits calibrés par pouvoir d'achat"),
            ("06", "Revenus Récurrents", "Bannières publicitaires et Forfaits B2B"),
            ("07", "Projections et Investissement", "Horizon de 50 ans · Tour de table Seed € 120k"),
        ],
        "sobre_titulo": "À propos d'A1ELOS",
        "sobre_texto": "A1ELOS est une holding de technologie et de connaissance qui unit intelligence artificielle, numérologie appliquée et stratégie culturelle pour créer des produits numériques à fort impact à l'échelle mondiale. Notre mission : démocratiser la connaissance de soi numérique avec respect culturel et respect du pouvoir d'achat de chaque marché.",
        "sobre_kpis": [
            ("23", "Produits Actifs", "En 4 niveaux d'accès"),
            ("14", "Langues", "~67% de la population mondiale"),
            ("5,3B", "Locuteurs", "Marché adressable réel"),
            ("IA", "Intégrée", "Moteur de personnalisation"),
        ],
        "sobre_duns": "DUNS 942242668 — Certification Dun & Bradstreet valable dans 190+ pays, habilitant les contrats B2B et les joint ventures internationales.",
        "duns_titulo": "Crédibilité Internationale",
        "duns_texto": "Le numéro DUNS est le passeport corporatif d'A1ELOS sur la scène internationale. Il signale aux partenaires, clients corporatifs et investisseurs que l'entreprise possède une identité vérifiable, un historique traçable et une capacité contractuelle dans toute juridiction.",
        "duns_numero": "942242668",
        "duns_emitido": "Émis par Dun & Bradstreet — la norme mondiale d'identité d'entreprise reconnue dans plus de 190 pays.",
        "duns_paises": "190+ PAYS",
        "duns_beneficios": [
            ("Contrats B2B", "Habilitation pour les appels d'offres et fournisseurs mondiaux"),
            ("Joint Ventures", "Partenariats internationaux avec due diligence facilitée"),
            ("Crédibilité Immédiate", "Un signe de sérieux pour les investisseurs institutionnels"),
        ],
        "mercado_titulo": "Opportunité de Marché",
        "mercado_texto": "Nous vivons la convergence parfaite : le bien-être numérique explose mondialement tandis que la numérologie et l'astrologie migrent vers des apps à fort engagement. A1ELOS est positionnée exactement à cette intersection, avec 74% de la population mondiale déjà en ligne (~6 milliards de personnes).",
        "mercado_cards": [
            ("Bien-être Mondial", "US$ 6,8 B → US$ 9,8 B d'ici 2029 (+7,6% par an)"),
            ("Apps Astrologie/Numérologie", "US$ 3 B → US$ 9 B d'ici 2030 · CAGR 20%"),
            ("Apps de Bien-être", "CAGR 14,9% → US$ 26,2 B en 2030"),
            ("Utilisateurs en Ligne", "74% du monde · ~6 milliards de personnes"),
        ],
        "problema_titulo": "Le Problème que Nous Résolvons",
        "problema_col_esq_titulo": "Échecs du Marché Actuel",
        "problema_col_esq": [
            ("Barrière de Langue", "La grande majorité des outils de numérologie fonctionne uniquement en anglais, excluant des milliards de locuteurs natifs dans d'autres langues."),
            ("Prix Déconnectés de la Réalité", "Des produits facturés en dollars pour les marchés émergents génèrent une exclusion économique — l'utilisateur ne rejette pas le produit, il rejette le prix inaccessible."),
            ("Manque de Profondeur", "Les outils génériques livrent des réponses superficielles sans personnalisation, sans contexte culturel et sans application pratique au quotidien."),
        ],
        "problema_col_dir_titulo": "Le Coût de l'Exclusion",
        "problema_col_dir": "Lorsqu'une plateforme ignore la langue et le pouvoir d'achat, elle abandonne volontairement le plus grand marché du monde : les 4+ milliards de personnes vivant dans des économies émergentes qui parlent des langues non anglophones. C'est l'écart qu'A1ELOS occupe avec une précision chirurgicale.",
        "problema_destaque": "Les plateformes qui ignorent le pouvoir d'achat local perdent l'accès à plus de 60% du marché adressable mondial.",
        "solucao_titulo": "Notre Solution : 3 Piliers Stratégiques",
        "solucao_texto": "A1ELOS a construit une plateforme intégrée qui combine science numérique, intelligence artificielle et sensibilité culturelle. La solution opère sur trois fronts complémentaires, garantissant des revenus diversifiés et une forte rétention.",
        "solucao_colunas": [
            ("Cartes Personnelles", "Analyses numériques profondes et personnalisées pour l'utilisateur final — identité, mission, cycles de vie et compatibilité — livrées en 14 langues avec IA intégrée."),
            ("Numérologie d'Entreprise", "Diagnostics numérologiques appliqués aux marques, CNPJs, dates de fondation et stratégie corporative. Produit différencié à forte valeur perçue sur le marché B2B."),
            ("White-Label B2B", "Licence de la plateforme pour les entreprises partenaires souhaitant offrir la numérologie sous leur propre marque — avec support multilingue et personnalisation complète."),
        ],
        "alcance_titulo": "Portée Globale : 14 Langues · ~5,3 Milliards de Locuteurs",
        "alcance_texto": "A1ELOS couvre ~67% de la population mondiale avec une plateforme véritablement multilingue. Chaque langue représente un marché culturel distinct, avec des prix calibrés au pouvoir d'achat local.",
        "mercados_titulo": "Les 3 Nouveaux Marchés : +442 Millions de Locuteurs",
        "mercados_texto": "L'expansion stratégique vers l'Indonésie, la Turquie et le Vietnam représente un saut qualitatif : des marchés à forte croissance économique, pénétration numérique croissante et demande prouvée de solutions de bien-être numérique accessibles.",
        "mercados_cards": [
            ("Indonésie", ["285M habitants", "80,5% de pénétration internet", "~255M locuteurs indonésiens", "Bien-être : US$ 51,2 B (2025) → US$ 72,8 B (2034)"]),
            ("Turquie", ["85,9M habitants", "PIB PPA par habitant US$ 37.301", "~90M locuteurs turcs", "Au-dessus de la moyenne mondiale (US$ 27.211)"]),
            ("Vietnam",  ["~100M habitants", "PIB par habitant ~US$ 5.066 (+7,4%/an)", "~97M locuteurs vietnamiens", "Bien-être : US$ 303M (2025) → US$ 485M (2030)"]),
        ],
        "mercados_rodape": "3 nouveaux marchés = +442 millions de nouveaux locuteurs adressables — intégrés à la plateforme avec des prix culturellement calibrés.",
        "preco_titulo": "Philosophie de Prix Conscient",
        "preco_esq": "Respect culturel + respect du pouvoir d'achat = marché adressable réel. Même proportion de valeur. Prix différents. Dignité égale pour tous les marchés.",
        "preco_dir_titulo": "Comment Ça Fonctionne en Pratique",
        "preco_dir": "A1ELOS applique la Parité de Pouvoir d'Achat (PPA) comme critère central de tarification. Le même produit livre la même valeur relative à l'utilisateur à Lagos, Jakarta, Hanoï ou New York — le prix est calibré pour que l'effort financier soit proportionnel au revenu local.",
        "preco_pilares": [
            ("Calibrage par PPA", "Prix ajustés à l'indice de pouvoir d'achat de chaque pays"),
            ("Respect Culturel", "Langue, monnaie et contexte local intégrés au produit"),
            ("Conversion Supérieure", "Un prix juste génère plus de conversion et une meilleure rétention à long terme"),
        ],
        "portfolio_titulo": "Portefeuille : 23 Produits en 4 Niveaux",
        "portfolio_texto": "La structure en couches garantit que chaque profil d'utilisateur — du curieux au professionnel — trouve une offre adaptée à son niveau d'engagement et à sa capacité financière.",
        "portfolio_tabela": [
            ["Niveau", "Produits", "Fourchette de Prix (€)", "Profil"],
            ["Entrée", "Carte Express, Consultation Rapide", "€ 11", "Curieux, premier contact"],
            ["Intermédiaire", "Recherche IA, Carte Complète, Compatibilité", "€ 26", "Utilisateur engagé"],
            ["Avancé", "Numérologie d'Entreprise, Cycles, Mission", "€ 35–53", "Professionnel, entrepreneur"],
            ["Premium", "Diagnostic Complet, White-Label Personnel", "€ 62–134", "Haut revenu, usage corporate"],
            ["B2B / Entreprise", "Forfaits entreprise, licences, cadeaux", "Sur demande", "Entreprises et RH"],
        ],
        "portfolio_rodape": "23 produits couvrent tout le parcours de l'utilisateur, du premier contact au client premium récurrent — maximisant le LTV par langue et marché.",
        "negocio_titulo": "Modèle d'Affaires : 3 Sources de Revenus",
        "negocio_texto": "A1ELOS a été conçue avec des revenus diversifiés et évolutifs : ventes directes au consommateur final à l'échelle mondiale, contrats B2B à forte valeur et publicité géolocalisée récurrente — trois moteurs qui s'alimentent mutuellement.",
        "negocio_colunas": [
            ("B2C — 14 Langues", "Vente directe de produits numériques dans toutes les devises, avec prix adaptés par PPA. Échelle automatique via IA — sans équipe de support proportionnelle à la croissance."),
            ("B2B — Remises Progressives", "Forfaits corporatifs pour RH, employer branding et cadeaux institutionnels. Remises de 10% à 70% selon le volume. Contrats appuyés par DUNS 942242668."),
            ("Publicité Géolocalisée", "Bannières segmentées par pays, continent ou mondial avec rotation automatisée. Revenus récurrents mensuels à forte valeur — sans dépendance au volume de ventes de produits."),
        ],
        "banners_titulo": "Bannières Publicitaires — Revenus Récurrents Mensuels",
        "banners_texto": "La plateforme A1ELOS offre des espaces publicitaires premium avec segmentation précise par géolocalisation — pays, continent ou mondial. Avec rotation automatique toutes les 8 secondes et formats optimisés pour desktop et mobile, les bannières livrent une visibilité mesurable aux annonceurs régionaux et internationaux.",
        "banners_tabela": [
            ["Segmentation", "Fixe (€/mois)", "Temporaire (€/mois)", "Profil de l'Annonceur"],
            ["Pays", "€ 150", "€ 95", "PME locales, commerce régional"],
            ["Continent", "€ 340", "€ 230", "Marques régionales, expansion continentale"],
            ["Monde", "€ 660", "€ 470", "Entreprises mondiales, apps internationales"],
            ["Parrainage Exclusif", "€ 1.130", "€ 850/campagne", "Parrains master, lancements"],
        ],
        "banners_formatos": "728×90 px — Bannière centrale desktop · 320×100 px — Format mobile optimisé · 8 secondes — Rotation automatique · Geo-ciblage — Pays, continent ou portée mondiale",
        "b2b_titulo": "Forfaits Entreprise B2B — Haute Valeur, Haut Volume",
        "b2b_texto": "Les Forfaits B2B transforment A1ELOS en outil d'employer branding et de bien-être corporatif. Les entreprises achètent des codes d'accès en volume pour les distribuer comme cadeaux aux employés ou clients — appuyés par DUNS 942242668 pour les contrats corporatifs formels.",
        "b2b_planos": [
            ("Plan de Base · 50 Codes", "50× Carte Express (€ 11 chacun). Idéal pour les programmes de bien-être des employés et les actions d'onboarding."),
            ("Plan Intermédiaire · 100 Codes", "50× Express + 50× Recherche IA (€ 26). Parfait pour les RH et les stratégies d'employer branding."),
            ("Plan Premium · 200 Codes", "100× Express + 100× Carte Complète (€ 26). Profondeur analytique maximale pour les grandes équipes."),
        ],
        "b2b_tabela": [
            ["À partir de", "Remise", "Profil", "Utilisation Recommandée"],
            ["10 codes", "10%", "Petites équipes", "Action ponctuelle de bien-être"],
            ["100 codes", "30%", "PME", "Programme de bénéfices trimestriel"],
            ["500 codes", "50%", "Moyennes entreprises", "Cadeau annuel aux employés"],
            ["1.000 codes", "70%", "Grandes corporations", "Programme de fidélisation client"],
        ],
        "projecoes_titulo": "Projections Financières : Horizon de 50 Ans",
        "projecoes_texto": "Les projections ont été construites sur deux scénarios — conservateur et optimiste — reflétant différents taux de pénétration du marché, vitesse d'expansion B2B et croissance organique par langue.",
        "projecoes_tabela": [
            ["Horizon", "Conservateur (€)", "Optimiste (€)"],
            ["Année 1", "€ 6k", "€ 24k"],
            ["Année 3", "€ 22k", "€ 84k"],
            ["Année 5", "€ 94k", "€ 280k"],
            ["Année 10", "€ 560k", "€ 1,5M"],
            ["Année 20", "€ 2,8M", "€ 7,5M"],
            ["Année 30", "€ 6,5M", "€ 16,8M"],
            ["Année 40", "€ 10,3M", "€ 28M"],
            ["Année 50", "€ 14M", "€ 46,8M"],
        ],
        "tracao_titulo": "Traction et Résultats Prouvés",
        "tracao_texto": "A1ELOS opère déjà avec des métriques produit qui valident le modèle — forte rétention, évaluation premium et une base croissante de partenaires B2B démontrent que la plateforme livre une valeur réelle à l'utilisateur final et au marché corporatif.",
        "tracao_kpis": [
            ("12K+", "Utilisateurs Actifs", "Base organique en croissance constante"),
            ("87%", "Rétention", "Bien au-dessus de la moyenne de l'industrie (~30%)"),
            ("4,8★", "Évaluation Moyenne", "Satisfaction prouvée de l'utilisateur final"),
            ("23", "Partenaires B2B", "Contrats actifs avec entreprises et RH"),
        ],
        "roteiro_titulo": "Feuille de Route Stratégique",
        "roteiro_texto": "A1ELOS exécute un plan en quatre phases progressives — de la consolidation de la base actuelle au leadership mondial du marché, avec des options de sortie claires pour les investisseurs.",
        "roteiro_fases": [
            ("Phase 1 · Consolidation", "Renforcement de la base d'utilisateurs dans les langues déjà actives. Optimisation de la conversion, de la rétention et du LTV. Tour de table Seed conclu."),
            ("Phase 2 · Expansion", "Lancement officiel dans les 3 nouveaux marchés : Indonésie, Turquie et Vietnam. Accélération du canal B2B et publicité géolocalisée."),
            ("Phase 3 · Entrée Mondiale", "Présence active dans les 14 langues avec campagnes localisées. Partenariats white-label dans 5+ continents. Série A."),
            ("Phase 4 · Leadership", "20+ pays avec opérations consolidées. Plateforme SaaS de référence mondiale en numérologie appliquée. IPO ou sortie stratégique."),
        ],
        "invest_titulo": "Investissement & Contact",
        "invest_texto": "Nous sommes prêts pour des présentations privées, due diligence et négociations. Contactez-nous par le canal de votre choix.",
        "invest_dados": [
            ("Tour de table Seed", "€ 120k"),
            ("Valorisation Pré-Money", "€ 500k"),
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
        "selo_final": ["DUNS 942242668", "23 PRODUITS", "14 LANGUES", "~5,3 B LOCUTEURS"],
        "graf_cons": "Conservateur",
        "graf_otim": "Optimiste",
        "grafico_titulo_linha": "Croissance Projetée (€ milliers)",
    },

    "de": {
        "titulo": "A1ELOS Globale Numerologie",
        "subtitulo": "Die Wissenschaft der Zahlen, angewendet auf Ihren Erfolg",
        "capa_nota": "Strategische Präsentation für Investoren und Partner",
        "confidencial": "VERTRAULICH",
        "ano": "2026",
        "sumario_intro": "Diese Präsentation ist strukturiert, um Investoren und Partner durch alle strategischen Aspekte der A1ELOS Globalen Numerologie zu führen — von der Marktthese bis zum wiederkehrenden Umsatzmodell.",
        "sumario_cards": [
            ("01", "Über A1ELOS", "Holding, Portfolio und DUNS-Zertifizierung"),
            ("02", "Marktchance", "Globale Wellness-Wirtschaft US$ 6,8 Billionen"),
            ("03", "Lösung und Globale Reichweite", "14 Sprachen, ~5,3 Milliarden Sprecher"),
            ("04", "3 Neue Märkte", "Indonesien, Türkei und Vietnam"),
            ("05", "Portfolio und Preise", "23 Produkte nach Kaufkraft kalibriert"),
            ("06", "Wiederkehrende Einnahmen", "Werbe-Banner und B2B-Pakete"),
            ("07", "Prognosen und Investition", "50-Jahres-Horizont · Seed-Runde € 120k"),
        ],
        "sobre_titulo": "Über A1ELOS",
        "sobre_texto": "A1ELOS ist eine Technologie- und Wissensholding, die künstliche Intelligenz, angewandte Numerologie und Kulturstrategie vereint, um digitale Produkte mit hoher Wirkung auf globaler Ebene zu schaffen. Unsere Mission: numerische Selbsterkenntnis mit kulturellem Respekt und Respekt vor der Kaufkraft jedes Marktes zu demokratisieren.",
        "sobre_kpis": [
            ("23", "Aktive Produkte", "In 4 Zugriffsstufen"),
            ("14", "Sprachen", "~67% der Weltbevölkerung"),
            ("5,3B", "Sprecher", "Echter adressierbarer Markt"),
            ("KI", "Integriert", "Personalisierungs-Engine"),
        ],
        "sobre_duns": "DUNS 942242668 — Dun & Bradstreet-Zertifizierung gültig in 190+ Ländern, die B2B-Verträge und internationale Joint Ventures ermöglicht.",
        "duns_titulo": "Internationale Glaubwürdigkeit",
        "duns_texto": "Die DUNS-Nummer ist der Unternehmenspass von A1ELOS auf der internationalen Bühne. Sie signalisiert Partnern, Firmenkunden und Investoren, dass das Unternehmen über verifizierbare Identität, nachvollziehbare Geschichte und Vertragsfähigkeit in jeder Jurisdiktion verfügt.",
        "duns_numero": "942242668",
        "duns_emitido": "Ausgestellt von Dun & Bradstreet — dem globalen Standard der Unternehmensidentität, anerkannt in mehr als 190 Ländern.",
        "duns_paises": "190+ LÄNDER",
        "duns_beneficios": [
            ("B2B-Verträge", "Ermöglichung globaler Ausschreibungen und Lieferanten"),
            ("Joint Ventures", "Internationale Partnerschaften mit erleichterter Due Diligence"),
            ("Sofortige Glaubwürdigkeit", "Ein Zeichen der Ernsthaftigkeit für institutionelle Investoren"),
        ],
        "mercado_titulo": "Marktchance",
        "mercado_texto": "Wir erleben die perfekte Konvergenz: digitales Wohlbefinden explodiert weltweit, während Numerologie und Astrologie zu Apps mit hohem Engagement migrieren. A1ELOS ist genau an dieser Schnittstelle positioniert, mit 74% der Weltbevölkerung bereits online (~6 Milliarden Menschen).",
        "mercado_cards": [
            ("Globales Wohlbefinden", "US$ 6,8 B → US$ 9,8 B bis 2029 (+7,6% pro Jahr)"),
            ("Astrologie/Numerologie-Apps", "US$ 3 B → US$ 9 B bis 2030 · CAGR 20%"),
            ("Wellness-Apps", "CAGR 14,9% → US$ 26,2 B bis 2030"),
            ("Online-Nutzer", "74% der Welt · ~6 Milliarden Menschen"),
        ],
        "problema_titulo": "Das Problem, das Wir Lösen",
        "problema_col_esq_titulo": "Aktuelle Marktfehler",
        "problema_col_esq": [
            ("Sprachbarriere", "Die überwiegende Mehrheit der Numerologie-Tools funktioniert nur auf Englisch und schließt Milliarden von Muttersprachlern in anderen Sprachen aus."),
            ("Preise Losgelöst von der Realität", "In Dollar abgerechnete Produkte für Schwellenmärkte erzeugen wirtschaftliche Ausgrenzung — der Nutzer lehnt nicht das Produkt ab, sondern den unzugänglichen Preis."),
            ("Mangel an Tiefe", "Generische Tools liefern oberflächliche Antworten ohne Personalisierung, ohne kulturellen Kontext und ohne praktische Anwendung im Alltag."),
        ],
        "problema_col_dir_titulo": "Die Kosten der Ausgrenzung",
        "problema_col_dir": "Wenn eine Plattform Sprache und Kaufkraft ignoriert, verlässt sie freiwillig den größten Markt der Welt: die 4+ Milliarden Menschen in Schwellenländern, die nicht-englischsprachige Sprachen sprechen. Diese Lücke besetzt A1ELOS mit chirurgischer Präzision.",
        "problema_destaque": "Plattformen, die lokale Kaufkraft ignorieren, verlieren den Zugang zu mehr als 60% des globalen adressierbaren Marktes.",
        "solucao_titulo": "Unsere Lösung: 3 Strategische Säulen",
        "solucao_texto": "A1ELOS hat eine integrierte Plattform aufgebaut, die numerische Wissenschaft, künstliche Intelligenz und kulturelle Sensibilität verbindet. Die Lösung operiert auf drei komplementären Ebenen und sichert diversifizierte Einnahmen und hohe Bindung.",
        "solucao_colunas": [
            ("Persönliche Karten", "Tiefe und personalisierte numerische Analysen für den Endnutzer — Identität, Mission, Lebenszyklen und Kompatibilität — in 14 Sprachen mit integrierter KI."),
            ("Unternehmensnumerologie", "Numerologische Diagnosen für Marken, CNPJs, Gründungsdaten und Unternehmensstrategie. Differenziertes Produkt mit hohem wahrgenommenem Wert im B2B-Markt."),
            ("White-Label B2B", "Lizenzierung der Plattform für Partnerunternehmen, die Numerologie unter eigener Marke anbieten möchten — mit mehrsprachigem Support und vollständiger Anpassung."),
        ],
        "alcance_titulo": "Globale Reichweite: 14 Sprachen · ~5,3 Milliarden Sprecher",
        "alcance_texto": "A1ELOS deckt ~67% der Weltbevölkerung mit einer wirklich mehrsprachigen Plattform ab. Jede Sprache repräsentiert einen eigenen kulturellen Markt mit an die lokale Kaufkraft kalibrierten Preisen.",
        "mercados_titulo": "Die 3 Neuen Märkte: +442 Millionen Sprecher",
        "mercados_texto": "Die strategische Expansion nach Indonesien, in die Türkei und nach Vietnam stellt einen qualitativen Sprung dar: Märkte mit hohem Wirtschaftswachstum, wachsender digitaler Durchdringung und nachgewiesener Nachfrage nach zugänglichen digitalen Wellness-Lösungen.",
        "mercados_cards": [
            ("Indonesien", ["285M Einwohner", "80,5% Internetdurchdringung", "~255M indonesische Sprecher", "Wellness: US$ 51,2 B (2025) → US$ 72,8 B (2034)"]),
            ("Türkei", ["85,9M Einwohner", "BIP KKP pro Kopf US$ 37.301", "~90M türkische Sprecher", "Über dem Weltdurchschnitt (US$ 27.211)"]),
            ("Vietnam",  ["~100M Einwohner", "BIP pro Kopf ~US$ 5.066 (+7,4%/Jahr)", "~97M vietnamesische Sprecher", "Wellness: US$ 303M (2025) → US$ 485M (2030)"]),
        ],
        "mercados_rodape": "3 neue Märkte = +442 Millionen neue adressierbare Sprecher — mit kulturell kalibrierten Preisen in die Plattform integriert.",
        "preco_titulo": "Philosophie des Bewussten Preises",
        "preco_esq": "Kultureller Respekt + Respekt vor der Kaufkraft = echter adressierbarer Markt. Gleicher Wertanteil. Unterschiedliche Preise. Gleiche Würde für alle Märkte.",
        "preco_dir_titulo": "So Funktioniert es in der Praxis",
        "preco_dir": "A1ELOS wendet die Kaufkraftparität (KKP) als zentrales Preiskriterium an. Dasselbe Produkt liefert dem Nutzer in Lagos, Jakarta, Hanoi oder New York denselben relativen Wert — der Preis wird so kalibriert, dass die finanzielle Anstrengung proportional zum lokalen Einkommen ist.",
        "preco_pilares": [
            ("KKP-Kalibrierung", "Preise an den Kaufkraftindex jedes Landes angepasst"),
            ("Kultureller Respekt", "Sprache, Währung und lokaler Kontext in das Produkt integriert"),
            ("Überlegene Konversion", "Faire Preise erzeugen mehr Konversion und höhere langfristige Bindung"),
        ],
        "portfolio_titulo": "Portfolio: 23 Produkte in 4 Stufen",
        "portfolio_texto": "Die gestufte Struktur stellt sicher, dass jedes Nutzerprofil — vom Neugierigen bis zum Profi — ein Angebot findet, das zu seinem Engagement und seiner finanziellen Kapazität passt.",
        "portfolio_tabela": [
            ["Stufe", "Produkte", "Preisspanne (€)", "Profil"],
            ["Einstieg", "Express-Map, Schnellberatung", "€ 11", "Neugierig, erster Kontakt"],
            ["Mittel", "KI-Recherche, Vollständige Map, Kompatibilität", "€ 26", "Engagierter Nutzer"],
            ["Fortgeschritten", "Unternehmensnumerologie, Zyklen, Mission", "€ 35–53", "Profi, Unternehmer"],
            ["Premium", "Vollständige Diagnose, Persönliches White-Label", "€ 62–134", "Hohes Einkommen, Firmennutzung"],
            ["B2B / Unternehmen", "Firmenpakete, Lizenzen, Geschenke", "Auf Anfrage", "Unternehmen und HR"],
        ],
        "portfolio_rodape": "23 Produkte decken die gesamte Nutzerreise ab, vom ersten Kontakt bis zum wiederkehrenden Premium-Kunden — maximierung des LTV pro Sprache und Markt.",
        "negocio_titulo": "Geschäftsmodell: 3 Einnahmequellen",
        "negocio_texto": "A1ELOS wurde mit diversifizierten und skalierbaren Einnahmen konzipiert: Direktverkäufe an den Endverbraucher auf globaler Ebene, B2B-Verträge mit hohem Wert und wiederkehrende geolokalisierte Werbung — drei Motoren, die sich gegenseitig speisen.",
        "negocio_colunas": [
            ("B2C — 14 Sprachen", "Direktverkauf digitaler Produkte in allen Währungen, mit an KKP angepassten Preisen. Automatische Skalierung via KI — ohne Support-Team proportional zum Wachstum."),
            ("B2B — Progressive Rabatte", "Unternehmenspakete für HR, Employer Branding und institutionelle Geschenke. Rabatte von 10% bis 70% je nach Volumen. Verträge durch DUNS 942242668 gestützt."),
            ("Geolokalisierte Werbung", "Banner nach Land, Kontinent oder weltweit mit automatisierter Rotation. Wiederkehrende monatliche Einnahmen mit hohem Wert — ohne Abhängigkeit vom Produktverkaufsvolumen."),
        ],
        "banners_titulo": "Werbe-Banner — Wiederkehrende Monatliche Einnahmen",
        "banners_texto": "Die A1ELOS-Plattform bietet Premium-Werbeplätze mit präziser Segmentierung nach Geolokalisierung — Land, Kontinent oder weltweit. Mit automatischer Rotation alle 8 Sekunden und für Desktop und Mobile optimierten Formaten liefern die Banner messbare Sichtbarkeit für regionale und internationale Werbetreibende.",
        "banners_tabela": [
            ["Segmentierung", "Fix (€/Monat)", "Temporär (€/Monat)", "Werbetreibenden-Profil"],
            ["Land", "€ 150", "€ 95", "Lokale KMU, regionaler Handel"],
            ["Kontinent", "€ 340", "€ 230", "Regionale Marken, kontinentale Expansion"],
            ["Welt", "€ 660", "€ 470", "Globale Unternehmen, internationale Apps"],
            ["Exklusives Sponsoring", "€ 1.130", "€ 850/Kampagne", "Master-Sponsoren, Launches"],
        ],
        "banners_formatos": "728×90 px — Zentrales Desktop-Banner · 320×100 px — Optimiertes Mobile-Format · 8 Sekunden — Automatische Rotation · Geo-Targeting — Land, Kontinent oder weltweite Reichweite",
        "b2b_titulo": "B2B-Unternehmenspakete — Hoher Wert, Hohes Volumen",
        "b2b_texto": "Die B2B-Pakete machen A1ELOS zu einem Werkzeug für Employer Branding und betriebliches Wohlbefinden. Unternehmen kaufen Zugangscodes in großen Mengen, um sie als Geschenke an Mitarbeiter oder Kunden zu verteilen — gestützt durch DUNS 942242668 für formelle Unternehmensverträge.",
        "b2b_planos": [
            ("Basisplan · 50 Codes", "50× Express-Map (€ 11 pro Stück). Ideal für Mitarbeiter-Wellnessprogramme und Onboarding-Maßnahmen."),
            ("Mittelplan · 100 Codes", "50× Express + 50× KI-Recherche (€ 26). Perfekt für HR und Employer-Branding-Strategien."),
            ("Premium-Plan · 200 Codes", "100× Express + 100× Vollständige Map (€ 26). Maximale analytische Tiefe für große Teams."),
        ],
        "b2b_tabela": [
            ["Ab", "Rabatt", "Profil", "Empfohlene Nutzung"],
            ["10 Codes", "10%", "Kleine Teams", "Punktuelle Wellness-Aktion"],
            ["100 Codes", "30%", "KMU", "Quartalsweises Leistungsprogramm"],
            ["500 Codes", "50%", "Mittlere Unternehmen", "Jährliches Mitarbeitergeschenk"],
            ["1.000 Codes", "70%", "Große Konzerne", "Kundenbindungsprogramm"],
        ],
        "projecoes_titulo": "Finanzprognosen: 50-Jahres-Horizont",
        "projecoes_texto": "Die Prognosen wurden auf zwei Szenarien aufgebaut — konservativ und optimistisch — die unterschiedliche Marktdurchdringungsraten, B2B-Expansionsgeschwindigkeit und organisches Wachstum pro Sprache widerspiegeln.",
        "projecoes_tabela": [
            ["Horizont", "Konservativ (€)", "Optimistisch (€)"],
            ["Jahr 1", "€ 6k", "€ 24k"],
            ["Jahr 3", "€ 22k", "€ 84k"],
            ["Jahr 5", "€ 94k", "€ 280k"],
            ["Jahr 10", "€ 560k", "€ 1,5M"],
            ["Jahr 20", "€ 2,8M", "€ 7,5M"],
            ["Jahr 30", "€ 6,5M", "€ 16,8M"],
            ["Jahr 40", "€ 10,3M", "€ 28M"],
            ["Jahr 50", "€ 14M", "€ 46,8M"],
        ],
        "tracao_titulo": "Traction und Bewährte Ergebnisse",
        "tracao_texto": "A1ELOS operiert bereits mit Produktkennzahlen, die das Modell validieren — hohe Bindung, Premium-Bewertung und eine wachsende Basis von B2B-Partnern zeigen, dass die Plattform dem Endnutzer und dem Unternehmensmarkt echten Wert liefert.",
        "tracao_kpis": [
            ("12K+", "Aktive Nutzer", "Konsistente organische Wachstumsbasis"),
            ("87%", "Bindung", "Weit über dem Branchendurchschnitt (~30%)"),
            ("4,8★", "Durchschnittsbewertung", "Bewährte Endnutzerzufriedenheit"),
            ("23", "B2B-Partner", "Aktive Verträge mit Unternehmen und HR"),
        ],
        "roteiro_titulo": "Strategische Roadmap",
        "roteiro_texto": "A1ELOS führt einen Plan in vier progressiven Phasen aus — von der Konsolidierung der aktuellen Basis bis zur globalen Marktführerschaft, mit klaren Exit-Optionen für Investoren.",
        "roteiro_fases": [
            ("Phase 1 · Konsolidierung", "Stärkung der Nutzerbasis in den bereits aktiven Sprachen. Optimierung von Konversion, Bindung und LTV. Seed-Runde abgeschlossen."),
            ("Phase 2 · Expansion", "Offizieller Start in den 3 neuen Märkten: Indonesien, Türkei und Vietnam. Beschleunigung des B2B-Kanals und geolokalisierte Werbung."),
            ("Phase 3 · Globaler Eintritt", "Aktive Präsenz in allen 14 Sprachen mit lokalisierten Kampagnen. White-Label-Partnerschaften in 5+ Kontinenten. Serie A."),
            ("Phase 4 · Führung", "20+ Länder mit konsolidierten Operationen. Referenz-SaaS-Plattform für angewandte Numerologie weltweit. IPO oder strategischer Exit."),
        ],
        "invest_titulo": "Investition & Kontakt",
        "invest_texto": "Wir sind bereit für private Präsentationen, Due Diligence und Verhandlungen. Kontaktieren Sie uns über Ihren bevorzugten Kanal.",
        "invest_dados": [
            ("Seed-Runde", "€ 120k"),
            ("Pre-Money-Bewertung", "€ 500k"),
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
        "selo_final": ["DUNS 942242668", "23 PRODUKTE", "14 SPRACHEN", "~5,3 B SPRECHER"],
        "graf_cons": "Konservativ",
        "graf_otim": "Optimistisch",
        "grafico_titulo_linha": "Projiziertes Wachstum (€ Tausend)",
    },

    "ru": {
        "titulo": "A1ELOS Глобальная Нумерология",
        "subtitulo": "Наука чисел, применённая к вашему успеху",
        "capa_nota": "Стратегическая презентация для инвесторов и партнёров",
        "confidencial": "КОНФИДЕНЦИАЛЬНО",
        "ano": "2026",
        "sumario_intro": "Эта презентация структурирована, чтобы провести инвесторов и партнёров через все стратегические аспекты A1ELOS Глобальной Нумерологии — от рыночной тезы до модели повторяющихся доходов.",
        "sumario_cards": [
            ("01", "О A1ELOS", "Холдинг, портфель и сертификат DUNS"),
            ("02", "Рыночная возможность", "Мировая экономика благополучия US$ 6,8 трлн"),
            ("03", "Решение и глобальный охват", "14 языков, ~5,3 млрд говорящих"),
            ("04", "3 новых рынка", "Индонезия, Турция и Вьетнам"),
            ("05", "Портфель и цены", "23 продукта, откалиброванных по покупательной способности"),
            ("06", "Повторяющиеся доходы", "Рекламные баннеры и B2B-пакеты"),
            ("07", "Прогнозы и инвестиции", "Горизонт 50 лет · Раунд Seed ₽ 2,4 млн"),
        ],
        "sobre_titulo": "О A1ELOS",
        "sobre_texto": "A1ELOS — это технологический и интеллектуальный холдинг, объединяющий искусственный интеллект, прикладную нумерологию и культурную стратегию для создания цифровых продуктов с высоким влиянием в глобальном масштабе. Наша миссия: демократизировать числовое самопознание с культурным уважением и уважением к покупательной способности каждого рынка.",
        "sobre_kpis": [
            ("23", "Активных продуктов", "В 4 уровнях доступа"),
            ("14", "Языков", "~67% населения мира"),
            ("5,3B", "Говорящих", "Реальный адресуемый рынок"),
            ("ИИ", "Интегрирован", "Движок персонализации"),
        ],
        "sobre_duns": "DUNS 942242668 — Сертификация Dun & Bradstreet, действующая в 190+ странах, позволяющая заключать B2B-контракты и международные совместные предприятия.",
        "duns_titulo": "Международная надёжность",
        "duns_texto": "Номер DUNS — это корпоративный паспорт A1ELOS на международной арене. Он сигнализирует партнёрам, корпоративным клиентам и инвесторам, что компания обладает проверяемой идентичностью, прослеживаемой историей и контрактной способностью в любой юрисдикции.",
        "duns_numero": "942242668",
        "duns_emitido": "Выдан Dun & Bradstreet — мировым стандартом корпоративной идентичности, признанным в более чем 190 странах.",
        "duns_paises": "190+ СТРАН",
        "duns_beneficios": [
            ("B2B-контракты", "Доступ к глобальным тендерам и поставщикам"),
            ("Совместные предприятия", "Международные партнёрства с упрощённой проверкой"),
            ("Немедленная надёжность", "Признак серьёзности для институциональных инвесторов"),
        ],
        "mercado_titulo": "Рыночная возможность",
        "mercado_texto": "Мы живём в идеальной конвергенции: цифровое благополучие взрывается во всём мире, а нумерология и астрология мигрируют в приложения с высоким вовлечением. A1ELOS позиционирована именно на этом пересечении: 74% населения мира уже онлайн (~6 млрд человек).",
        "mercado_cards": [
            ("Глобальное благополучие", "US$ 6,8 трлн → US$ 9,8 трлн к 2029 (+7,6% в год)"),
            ("Приложения астрологии/нумерологии", "US$ 3 млрд → US$ 9 млрд к 2030 · CAGR 20%"),
            ("Приложения благополучия", "CAGR 14,9% → US$ 26,2 млрд к 2030"),
            ("Пользователи онлайн", "74% мира · ~6 млрд человек"),
        ],
        "problema_titulo": "Проблема, которую мы решаем",
        "problema_col_esq_titulo": "Текущие провалы рынка",
        "problema_col_esq": [
            ("Языковой барьер", "Подавляющее большинство инструментов нумерологии работает только на английском, исключая миллиарды носителей других языков."),
            ("Цены, оторванные от реальности", "Продукты, выставленные в долларах для развивающихся рынков, создают экономическое исключение — пользователь отвергает не продукт, а недоступную цену."),
            ("Отсутствие глубины", "Общие инструменты дают поверхностные ответы без персонализации, без культурного контекста и без практического применения в повседневной жизни."),
        ],
        "problema_col_dir_titulo": "Цена исключения",
        "problema_col_dir": "Когда платформа игнорирует язык и покупательную способность, она добровольно отказывается от крупнейшего рынка мира: 4+ миллиардов человек в развивающихся экономиках, говорящих на неанглоязычных языках. Именно эту нишу A1ELOS занимает с хирургической точностью.",
        "problema_destaque": "Платформы, игнорирующие местную покупательную способность, теряют доступ к более чем 60% глобального адресуемого рынка.",
        "solucao_titulo": "Наше решение: 3 стратегических столпа",
        "solucao_texto": "A1ELOS построила интегрированную платформу, сочетающую числовую науку, искусственный интеллект и культурную чувствительность. Решение работает на трёх взаимодополняющих направлениях, обеспечивая диверсифицированный доход и высокое удержание.",
        "solucao_colunas": [
            ("Личные карты", "Глубокие и персонализированные числовые анализы для конечного пользователя — идентичность, миссия, жизненные циклы и совместимость — на 14 языках с интегрированным ИИ."),
            ("Деловая нумерология", "Нумерологические диагнозы для брендов, CNPJ, дат основания и корпоративной стратегии. Дифференцированный продукт с высокой воспринимаемой ценностью на B2B-рынке."),
            ("White-Label B2B", "Лицензирование платформы для компаний-партнёров, желающих предлагать нумерологию под собственным брендом — с многоязычной поддержкой и полной настройкой."),
        ],
        "alcance_titulo": "Глобальный охват: 14 языков · ~5,3 млрд говорящих",
        "alcance_texto": "A1ELOS охватывает ~67% населения мира с по-настоящему многоязычной платформой. Каждый язык представляет отдельный культурный рынок с ценами, откалиброванными по местной покупательной способности.",
        "mercados_titulo": "3 новых рынка: +442 млн говорящих",
        "mercados_texto": "Стратегическое расширение в Индонезию, Турцию и Вьетнам представляет качественный скачок: рынки с высоким экономическим ростом, растущим цифровым проникновением и доказанным спросом на доступные цифровые решения для благополучия.",
        "mercados_cards": [
            ("Индонезия", ["285 млн жителей", "80,5% проникновение интернета", "~255 млн говорящих на индонезийском", "Благополучие: US$ 51,2 млрд (2025) → US$ 72,8 млрд (2034)"]),
            ("Турция", ["85,9 млн жителей", "ВВП ППС на душу US$ 37.301", "~90 млн говорящих на турецком", "Выше среднемирового (US$ 27.211)"]),
            ("Вьетнам",  ["~100 млн жителей", "ВВП на душу ~US$ 5.066 (+7,4%/год)", "~97 млн говорящих на вьетнамском", "Благополучие: US$ 303 млн (2025) → US$ 485 млн (2030)"]),
        ],
        "mercados_rodape": "3 новых рынка = +442 млн новых адресуемых говорящих — интегрированы в платформу с культурно откалиброванными ценами.",
        "preco_titulo": "Философия осознанного ценообразования",
        "preco_esq": "Культурное уважение + уважение к покупательной способности = реальный адресуемый рынок. Та же пропорция ценности. Разные цены. Равное достоинство для всех рынков.",
        "preco_dir_titulo": "Как это работает на практике",
        "preco_dir": "A1ELOS применяет паритет покупательной способности (ППС) как центральный критерий ценообразования. Один и тот же продукт даёт одинаковую относительную ценность пользователю в Лагосе, Джакарте, Ханое или Нью-Йорке — цена калибруется так, чтобы финансовое усилие было пропорционально местному доходу.",
        "preco_pilares": [
            ("Калибровка по ППС", "Цены, скорректированные по индексу покупательной способности каждой страны"),
            ("Культурное уважение", "Язык, валюта и местный контекст, интегрированные в продукт"),
            ("Высшая конверсия", "Справедливая цена даёт больше конверсии и большее долгосрочное удержание"),
        ],
        "portfolio_titulo": "Портфель: 23 продукта в 4 уровнях",
        "portfolio_texto": "Многоуровневая структура гарантирует, что каждый профиль пользователя — от любопытного до профессионала — найдёт предложение, соответствующее его уровню вовлечённости и финансовым возможностям.",
        "portfolio_tabela": [
            ["Уровень", "Продукты", "Диапазон цен (₽)", "Профиль"],
            ["Вход", "Экспресс-карта, Быстрая консультация", "₽ 440", "Любопытный, первый контакт"],
            ["Средний", "ИИ-исследование, Полная карта, Совместимость", "₽ 800", "Активный пользователь"],
            ["Продвинутый", "Деловая нумерология, Циклы, Миссия", "₽ 1.250–1.700", "Профессионал, предприниматель"],
            ["Премиум", "Полная диагностика, Персональный white-label", "₽ 2.150–4.400", "Высокий доход, корпоративное использование"],
            ["B2B / Корпоративный", "Корпоративные пакеты, лицензии, подарки", "По запросу", "Компании и HR"],
        ],
        "portfolio_rodape": "23 продукта покрывают весь путь пользователя — от первого контакта до постоянного премиум-клиента, максимизируя LTV по языку и рынку.",
        "negocio_titulo": "Бизнес-модель: 3 источника дохода",
        "negocio_texto": "A1ELOS спроектирована с диверсифицированным и масштабируемым доходом: прямые продажи конечному потребителю в глобальном масштабе, B2B-контракты с высокой стоимостью и повторяющаяся геолокализованная реклама — три двигателя, которые питают друг друга.",
        "negocio_colunas": [
            ("B2C — 14 языков", "Прямая продажа цифровых продуктов во всех валютах с ценами, адаптированными по ППС. Автоматическое масштабирование через ИИ — без команды поддержки, пропорциональной росту."),
            ("B2B — прогрессивные скидки", "Корпоративные пакеты для HR, employer branding и институциональных подарков. Скидки от 10% до 70% в зависимости от объёма. Контракты, поддержанные DUNS 942242668."),
            ("Геолокализованная реклама", "Баннеры, сегментированные по стране, континенту или миру с автоматической ротацией. Повторяющийся ежемесячный доход высокой стоимости — без зависимости от объёма продаж продукта."),
        ],
        "banners_titulo": "Рекламные баннеры — повторяющийся ежемесячный доход",
        "banners_texto": "Платформа A1ELOS предлагает премиальные рекламные площадки с точной сегментацией по геолокации — страна, континент или весь мир. С автоматической ротацией каждые 8 секунд и форматами, оптимизированными для десктопа и мобильных, баннеры обеспечивают измеримую видимость для региональных и международных рекламодателей.",
        "banners_tabela": [
            ["Сегментация", "Фикс (₽/мес)", "Временный (₽/мес)", "Профиль рекламодателя"],
            ["Страна", "₽ 8.000", "₽ 5.000", "Местные МСП, региональная торговля"],
            ["Континент", "₽ 18.000", "₽ 12.000", "Региональные бренды, континентальная экспансия"],
            ["Мир", "₽ 35.000", "₽ 25.000", "Глобальные компании, международные приложения"],
            ["Эксклюзивное спонсорство", "₽ 60.000", "₽ 45.000/кампания", "Мастер-спонсоры, запуски"],
        ],
        "banners_formatos": "728×90 px — Центральный десктоп-баннер · 320×100 px — Оптимизированный мобильный формат · 8 секунд — Автоматическая ротация · Гео-таргетинг — Страна, континент или мировой охват",
        "b2b_titulo": "B2B-корпоративные пакеты — высокая ценность, высокий объём",
        "b2b_texto": "B2B-пакеты превращают A1ELOS в инструмент employer branding и корпоративного благополучия. Компании приобретают коды доступа оптом для распространения в качестве подарков сотрудникам или клиентам — поддержанные DUNS 942242668 для формальных корпоративных контрактов.",
        "b2b_planos": [
            ("Базовый план · 50 кодов", "50× Экспресс-карта (₽ 440 каждая). Идеально для программ благополучия сотрудников и действий по онбордингу."),
            ("Средний план · 100 кодов", "50× Экспресс + 50× ИИ-исследование (₽ 800). Идеально для HR и стратегий employer branding."),
            ("Премиум-план · 200 кодов", "100× Экспресс + 100× Полная карта (₽ 800). Максимальная аналитическая глубина для больших команд."),
        ],
        "b2b_tabela": [
            ["От", "Скидка", "Профиль", "Рекомендуемое использование"],
            ["10 кодов", "10%", "Малые команды", "Точечное действие по благополучию"],
            ["100 кодов", "30%", "МСП", "Квартальная программа льгот"],
            ["500 кодов", "50%", "Средние компании", "Ежегодный подарок сотрудникам"],
            ["1.000 кодов", "70%", "Крупные корпорации", "Программа лояльности клиентов"],
        ],
        "projecoes_titulo": "Финансовые прогнозы: горизонт 50 лет",
        "projecoes_texto": "Прогнозы построены на двух сценариях — консервативном и оптимистичном — отражающих разные темпы проникновения на рынок, скорость B2B-экспансии и органический рост по языкам.",
        "projecoes_tabela": [
            ["Горизонт", "Консервативный (₽)", "Оптимистичный (₽)"],
            ["Год 1", "₽ 320k", "₽ 1,3M"],
            ["Год 3", "₽ 1,2M", "₽ 4,5M"],
            ["Год 5", "₽ 5M", "₽ 15M"],
            ["Год 10", "₽ 30M", "₽ 80M"],
            ["Год 20", "₽ 150M", "₽ 400M"],
            ["Год 30", "₽ 350M", "₽ 900M"],
            ["Год 40", "₽ 550M", "₽ 1,5B"],
            ["Год 50", "₽ 750M", "₽ 2,5B"],
        ],
        "tracao_titulo": "Тяга и подтверждённые результаты",
        "tracao_texto": "A1ELOS уже работает с продуктовыми метриками, которые подтверждают модель — высокое удержание, премиальная оценка и растущая база B2B-партнёров демонстрируют, что платформа приносит реальную ценность конечному пользователю и корпоративному рынку.",
        "tracao_kpis": [
            ("12K+", "Активных пользователей", "Стабильная органическая база роста"),
            ("87%", "Удержание", "Значительно выше среднего по отрасли (~30%)"),
            ("4,8★", "Средняя оценка", "Подтверждённое удовлетворение конечного пользователя"),
            ("23", "B2B-партнёра", "Активные контракты с компаниями и HR"),
        ],
        "roteiro_titulo": "Стратегическая дорожная карта",
        "roteiro_texto": "A1ELOS выполняет план в четыре прогрессивные фазы — от консолидации текущей базы до глобального лидерства на рынке, с чёткими вариантами выхода для инвесторов.",
        "roteiro_fases": [
            ("Фаза 1 · Консолидация", "Укрепление базы пользователей на уже активных языках. Оптимизация конверсии, удержания и LTV. Раунд Seed завершён."),
            ("Фаза 2 · Экспансия", "Официальный запуск на 3 новых рынках: Индонезия, Турция и Вьетнам. Ускорение B2B-канала и геолокализованной рекламы."),
            ("Фаза 3 · Глобальный вход", "Активное присутствие на всех 14 языках с локализованными кампаниями. Партнёрства white-label на 5+ континентах. Серия A."),
            ("Фаза 4 · Лидерство", "20+ стран с консолидированными операциями. Эталонная глобальная SaaS-платформа в прикладной нумерологии. IPO или стратегический выход."),
        ],
        "invest_titulo": "Инвестиции и контакты",
        "invest_texto": "Мы готовы к частным презентациям, due diligence и переговорам. Свяжитесь с нами по предпочтительному каналу.",
        "invest_dados": [
            ("Раунд Seed", "₽ 2,4 млн"),
            ("Оценка Pre-Money", "₽ 9,6 млн"),
            ("Предлагаемая доля", "До 20%"),
        ],
        "invest_contato": [
            ("Email для инвесторов", "a1elos.consultoria@gmail.com"),
            ("Общий email", "contato@a1elos.com"),
            ("Веб-сайт", "www.a1elos.com"),
            ("DUNS", "942242668 — Dun & Bradstreet"),
        ],
        "invest_alocacao": "Распределение капитала: 45% Технологии · 30% Маркетинг · 25% Операции",
        "frase_final": "Числа никогда не лгут.",
        "selo_final": ["DUNS 942242668", "23 ПРОДУКТА", "14 ЯЗЫКОВ", "~5,3 МЛРД ГОВОРЯЩИХ"],
        "graf_cons": "Консервативный",
        "graf_otim": "Оптимистичный",
        "grafico_titulo_linha": "Прогнозируемый рост (₽ тыс.)",
    },

    "ja": {
        "titulo": "A1ELOS グローバル数秘術",
        "subtitulo": "数字の科学をあなたの成功に",
        "capa_nota": "投資家・パートナー向け戦略プレゼンテーション",
        "confidencial": "機密",
        "ano": "2026",
        "sumario_intro": "このプレゼンテーションは、投資家とパートナーをA1ELOSグローバル数秘術のあらゆる戦略的側面——市場テーゼから継続的収益モデルまで——へと導くために構成されています。",
        "sumario_cards": [
            ("01", "A1ELOSについて", "ホールディング、ポートフォリオ、DUNS認証"),
            ("02", "市場機会", "世界のウェルネス経済 6.8兆ドル"),
            ("03", "ソリューションとグローバル展開", "14言語、約53億人の話者"),
            ("04", "3つの新市場", "インドネシア、トルコ、ベトナム"),
            ("05", "ポートフォリオと価格", "購買力に合わせて調整された23製品"),
            ("06", "継続的収益", "広告バナーとB2Bパッケージ"),
            ("07", "予測と投資", "50年の展望 · シードラウンド ¥ 1,400万"),
        ],
        "sobre_titulo": "A1ELOSについて",
        "sobre_texto": "A1ELOSは、人工知能、応用数秘術、文化戦略を融合したテクノロジーと知識のホールディングです。グローバル規模でインパクトのあるデジタル製品を生み出します。私たちの使命：文化的尊重と各市場の購買力への尊重をもって、数秘的な自己理解を民主化することです。",
        "sobre_kpis": [
            ("23", "アクティブ製品", "4つのアクセスレベル"),
            ("14", "言語", "世界人口の約67%"),
            ("53億", "話者", "実際の到達可能市場"),
            ("AI", "統合", "パーソナライズエンジン"),
        ],
        "sobre_duns": "DUNS 942242668 — Dun & Bradstreet認証は190以上の国で有効で、B2B契約と国際合弁事業を可能にします。",
        "duns_titulo": "国際的な信頼性",
        "duns_texto": "DUNS番号は、国際舞台におけるA1ELOSの企業パスポートです。検証可能な身元、追跡可能な履歴、あらゆる管轄区域での契約能力を備えていることを、パートナー、法人顧客、投資家に示します。",
        "duns_numero": "942242668",
        "duns_emitido": "Dun & Bradstreet発行——190以上の国で認められた世界的な企業アイデンティティの基準。",
        "duns_paises": "190以上の国",
        "duns_beneficios": [
            ("B2B契約", "グローバルな入札とサプライヤーへの資格"),
            ("合弁事業", "デューデリジェンスが容易な国際提携"),
            ("即時の信頼性", "機関投資家への真剣さの証"),
        ],
        "mercado_titulo": "市場機会",
        "mercado_texto": "私たちは完璧な収束を生きています：デジタルウェルネスが世界的に爆発し、数秘術と占星術が高エンゲージメントのアプリへ移行しています。A1ELOSはまさにこの交差点に位置し、世界人口の74%がすでにオンラインです（約60億人）。",
        "mercado_cards": [
            ("世界のウェルネス", "6.8兆ドル → 2029年までに9.8兆（年+7.6%）"),
            ("占星術/数秘術アプリ", "30億ドル → 2030年までに90億 · CAGR 20%"),
            ("ウェルネスアプリ", "CAGR 14.9% → 2030年に262億"),
            ("オンラインユーザー", "世界の74% · 約60億人"),
        ],
        "problema_titulo": "私たちが解決する問題",
        "problema_col_esq_titulo": "現在の市場の欠陥",
        "problema_col_esq": [
            ("言語の壁", "数秘術ツールの圧倒的多数は英語のみで動作し、他言語の何十億もの母語話者を排除しています。"),
            ("現実から乖離した価格", "新興市場向けにドル建てで請求される製品は経済的排除を生みます——ユーザーは製品を拒否するのではなく、手の届かない価格を拒否します。"),
            ("深みの欠如", "一般的なツールは、パーソナライズも文化文脈も日常生活への実用性もない表面的な回答を提供します。"),
        ],
        "problema_col_dir_titulo": "排除のコスト",
        "problema_col_dir": "プラットフォームが言語と購買力を無視すると、世界最大の市場を自発的に放棄します：非英語圏の言語を話す新興経済の40億人以上。これこそがA1ELOSが外科的精度で占めるギャップです。",
        "problema_destaque": "地域の購買力を無視するプラットフォームは、世界の到達可能市場の60%以上へのアクセスを失います。",
        "solucao_titulo": "私たちのソリューション：3つの戦略的柱",
        "solucao_texto": "A1ELOSは、数秘科学、人工知能、文化的感性を組み合わせた統合プラットフォームを構築しました。ソリューションは3つの補完的な側面で機能し、多様な収益と高い維持率を保証します。",
        "solucao_colunas": [
            ("パーソナルマップ", "エンドユーザー向けの深くパーソナライズされた数秘分析——アイデンティティ、使命、ライフサイクル、相性——を統合AIで14言語で提供。"),
            ("ビジネス数秘術", "ブランド、CNPJ、創業日、企業戦略に適用される数秘診断。B2B市場で高い認知価値を持つ差別化製品。"),
            ("ホワイトラベルB2B", "自社ブランドで数秘術を提供したいパートナー企業へのプラットフォームライセンス——多言語サポートと完全なカスタマイズ。"),
        ],
        "alcance_titulo": "グローバル展開：14言語 · 約53億人の話者",
        "alcance_texto": "A1ELOSは真に多言語のプラットフォームで世界人口の約67%をカバーします。各言語は異なる文化市場を表し、価格は地域の購買力に合わせて調整されています。",
        "mercados_titulo": "3つの新市場：+4億4,200万人の話者",
        "mercados_texto": "インドネシア、トルコ、ベトナムへの戦略的拡大は質的飛躍を表します：経済成長が高く、デジタル浸透が進み、手頃なデジタルウェルネスソリューションへの実証済みの需要がある市場です。",
        "mercados_cards": [
            ("インドネシア", ["2.85億人の住民", "インターネット普及率80.5%", "約2.55億人のインドネシア語話者", "ウェルネス：512億ドル（2025）→ 728億（2034）"]),
            ("トルコ", ["8,590万人の住民", "一人当たりPPP GDP 37,301ドル", "約9,000万人のトルコ語話者", "世界平均（27,211ドル）を上回る"]),
            ("ベトナム",  ["約1億人の住民", "一人当たりGDP 約5,066ドル（年+7.4%）", "約9,700万人のベトナム語話者", "ウェルネス：3.03億ドル（2025）→ 4.85億（2030）"]),
        ],
        "mercados_rodape": "3つの新市場 = 新たに4億4,200万人の到達可能な話者——文化的に調整された価格でプラットフォームに統合。",
        "preco_titulo": "意識的な価格設定の哲学",
        "preco_esq": "文化的尊重 + 購買力への尊重 = 真の到達可能市場。同じ価値の割合。異なる価格。すべての市場に平等な尊厳。",
        "preco_dir_titulo": "実際の仕組み",
        "preco_dir": "A1ELOSは購買力平価（PPP）を中心的な価格設定基準として適用します。同じ製品がラゴス、ジャカルタ、ハノイ、ニューヨークのユーザーに同じ相対的価値を提供します——価格は財務的努力が地域の所得に比例するように調整されます。",
        "preco_pilares": [
            ("PPPによる調整", "各国の購買力指数に合わせて価格を調整"),
            ("文化的尊重", "言語、通貨、地域の文脈を製品に統合"),
            ("優れた転換率", "公正な価格はより高い転換率と長期的な維持をもたらす"),
        ],
        "portfolio_titulo": "ポートフォリオ：4レベルで23製品",
        "portfolio_texto": "階層構造により、好奇心旺盛な人からプロフェッショナルまで、あらゆるユーザープロファイルが自分のエンゲージメントレベルと財務能力に合ったオファーを見つけられます。",
        "portfolio_tabela": [
            ["レベル", "商品", "価格帯 (¥)", "プロフィール"],
            ["エントリー", "エクスプレスマップ、クイック相談", "¥ 1.400", "好奇心旺盛、初回接触"],
            ["ミドル", "AIリサーチ、フルマップ、相性診断", "¥ 3.000", "関与するユーザー"],
            ["アドバンス", "ビジネス数秘術、サイクル、使命", "¥ 4.600–6.200", "プロフェッショナル、起業家"],
            ["プレミアム", "完全診断、パーソナルホワイトラベル", "¥ 7.700–17.000", "高所得、法人利用"],
            ["B2B / 法人", "法人パッケージ、ライセンス、ギフト", "要相談", "企業と人事"],
        ],
        "portfolio_rodape": "23製品がユーザーの全旅程をカバーし、初回接触から継続的なプレミアム顧客まで、言語と市場ごとにLTVを最大化します。",
        "negocio_titulo": "ビジネスモデル：3つの収益源",
        "negocio_texto": "A1ELOSは多様でスケーラブルな収益で設計されています：グローバル規模での最終消費者への直接販売、高価値のB2B契約、継続的な地理ターゲット広告——相互に支え合う3つのエンジン。",
        "negocio_colunas": [
            ("B2C — 14言語", "すべての通貨でデジタル製品を直接販売し、PPPに基づき価格調整。AIによる自動スケーリング——成長に比例したサポートチームなし。"),
            ("B2B — 段階的割引", "人事、雇用主ブランディング、法人ギフト向けの法人パッケージ。数量に応じて10%から70%の割引。DUNS 942242668による裏付け。"),
            ("地理ターゲット広告", "国、大陸、または世界でセグメント化されたバナーを自動ローテーション。製品販売量に依存しない高価値の継続的月収。"),
        ],
        "banners_titulo": "広告バナー——継続的月収",
        "banners_texto": "A1ELOSプラットフォームは、地理的位置による精密なセグメンテーション——国、大陸、または世界——でプレミアム広告スペースを提供します。8秒ごとの自動ローテーションとデスクトップ・モバイル最適化フォーマットにより、バナーは地域・国際広告主に測定可能な可視性を提供します。",
        "banners_tabela": [
            ["セグメンテーション", "固定 (¥/月)", "一時 (¥/月)", "広告主プロフィール"],
            ["国", "¥ 8,000", "¥ 5,000", "地元中小企業、地域商業"],
            ["大陸", "¥ 18,000", "¥ 12,000", "地域ブランド、大陸展開"],
            ["世界", "¥ 35,000", "¥ 25,000", "グローバル企業、国際アプリ"],
            ["独占スポンサー", "¥ 60,000", "¥ 45,000/キャンペーン", "マスタースポンサー、発表"],
        ],
        "banners_formatos": "728×90px — デスクトップ中央バナー · 320×100px — 最適化モバイル形式 · 8秒 — 自動ローテーション · ジオターゲット — 国、大陸、または世界規模",
        "b2b_titulo": "B2B法人パッケージ——高価値、高数量",
        "b2b_texto": "B2BパッケージはA1ELOSを雇用主ブランディングと法人ウェルネスのツールに変えます。企業は従業員や顧客へのギフトとして配布するためにアクセスコードを大量購入します——正式な法人契約のためのDUNS 942242668による裏付け。",
        "b2b_planos": [
            ("ベーシックプラン · 50コード", "50× エクスプレスマップ（各¥ 1,400）。従業員ウェルネスプログラムとオンボーディングに最適。"),
            ("ミドルプラン · 100コード", "50× エクスプレス + 50× AIリサーチ（¥ 3,000）。人事と雇用主ブランディング戦略に最適。"),
            ("プレミアムプラン · 200コード", "100× エクスプレス + 100× フルマップ（¥ 3,000）。大規模チーム向けの最大の分析深度。"),
        ],
        "b2b_tabela": [
            ["から", "割引", "プロフィール", "推奨用途"],
            ["10コード", "10%", "小規模チーム", "単発のウェルネス活動"],
            ["100コード", "30%", "中小企業", "四半期福利厚生プログラム"],
            ["500コード", "50%", "中堅企業", "年次従業員ギフト"],
            ["1,000コード", "70%", "大企業", "顧客ロイヤルティプログラム"],
        ],
        "projecoes_titulo": "財務予測：50年の展望",
        "projecoes_texto": "予測は、市場浸透率、B2B拡大速度、言語別の有機的成長の違いを反映した2つのシナリオ——保守的と楽観的——に基づいて構築されました。",
        "projecoes_tabela": [
            ["展望", "保守的 (¥)", "楽観的 (¥)"],
            ["1年目", "¥ 60万", "¥ 240万"],
            ["3年目", "¥ 220万", "¥ 840万"],
            ["5年目", "¥ 940万", "¥ 2,800万"],
            ["10年目", "¥ 5,600万", "¥ 1.5億"],
            ["20年目", "¥ 2.8億", "¥ 7.5億"],
            ["30年目", "¥ 6.5億", "¥ 16.8億"],
            ["40年目", "¥ 10.3億", "¥ 28億"],
            ["50年目", "¥ 14億", "¥ 46.8億"],
        ],
        "tracao_titulo": "実績と証明された結果",
        "tracao_texto": "A1ELOSはモデルを検証する製品指標で既に運営されています——高い維持率、プレミアム評価、成長するB2Bパートナー基盤は、プラットフォームがエンドユーザーと企業市場に真の価値を提供することを示しています。",
        "tracao_kpis": [
            ("1.2万+", "アクティブユーザー", "一貫した有機的成長基盤"),
            ("87%", "維持率", "業界平均（約30%）を大幅に上回る"),
            ("4.8★", "平均評価", "証明されたエンドユーザー満足度"),
            ("23", "B2Bパートナー", "企業・人事とのアクティブ契約"),
        ],
        "roteiro_titulo": "戦略ロードマップ",
        "roteiro_texto": "A1ELOSは、現在の基盤の統合からグローバル市場リーダーシップまで、投資家に明確な出口オプションを提供する4つの段階的フェーズで計画を実行します。",
        "roteiro_fases": [
            ("フェーズ1 · 統合", "既にアクティブな言語でのユーザー基盤の強化。転換率、維持率、LTVの最適化。シードラウンド完了。"),
            ("フェーズ2 · 拡大", "3つの新市場での正式ローンチ：インドネシア、トルコ、ベトナム。B2Bチャネルと地理ターゲット広告の加速。"),
            ("フェーズ3 · グローバル参入", "ローカライズされたキャンペーンで全14言語に積極的に展開。5以上の大陸でホワイトラベル提携。シリーズA。"),
            ("フェーズ4 · リーダーシップ", "20以上の国で統合された事業。応用数秘術における世界的な参照SaaSプラットフォーム。IPOまたは戦略的出口。"),
        ],
        "invest_titulo": "投資と連絡先",
        "invest_texto": "私たちはプライベートプレゼンテーション、デューデリジェンス、交渉の準備ができています。お好みのチャネルでご連絡ください。",
        "invest_dados": [
            ("シードラウンド", "¥ 1,400万"),
            ("プレマネー評価額", "¥ 5,600万"),
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
        "selo_final": ["DUNS 942242668", "23製品", "14言語", "約53億話者"],
        "graf_cons": "保守的",
        "graf_otim": "楽観的",
        "grafico_titulo_linha": "予測成長（千円）",
    },

    "zh": {
        "titulo": "A1ELOS 全球数字命理",
        "subtitulo": "数字科学，助力您的成功",
        "capa_nota": "面向投资者与合作伙伴的战略演示",
        "confidencial": "机密",
        "ano": "2026",
        "sumario_intro": "本演示旨在引导投资者和合作伙伴了解A1ELOS全球数字命理的各个战略方面——从市场论点再到经常性收入模式。",
        "sumario_cards": [
            ("01", "关于A1ELOS", "控股公司、产品组合与DUNS资质"),
            ("02", "市场机遇", "全球健康经济达6.8万亿美元"),
            ("03", "解决方案与全球覆盖", "14种语言，约53亿使用者"),
            ("04", "3个新市场", "印度尼西亚、土耳其和越南"),
            ("05", "产品组合与定价", "23款按购买力校准的产品"),
            ("06", "经常性收入", "广告横幅与B2B套餐"),
            ("07", "预测与投资", "50年展望 · 种子轮 ¥ 52万"),
        ],
        "sobre_titulo": "关于A1ELOS",
        "sobre_texto": "A1ELOS是一家集人工智能、应用数字命理与文化战略于一体的科技与知识控股公司，致力于在全球范围内打造高影响力的数字产品。我们的使命：以文化尊重和对每个市场购买力的尊重，实现数字自我认知的普及。",
        "sobre_kpis": [
            ("23", "活跃产品", "4个访问级别"),
            ("14", "语言", "约占全球人口67%"),
            ("53亿", "使用者", "真实可及市场"),
            ("AI", "集成", "个性化引擎"),
        ],
        "sobre_duns": "DUNS 942242668 — Dun & Bradstreet认证在190多个国家有效，支持B2B合同和国际合资企业。",
        "duns_titulo": "国际信誉",
        "duns_texto": "DUNS号码是A1ELOS在国际舞台上的企业护照。它向合作伙伴、企业客户和投资者表明，公司拥有可验证的身份、可追溯的历史以及在任何司法管辖区的合同能力。",
        "duns_numero": "942242668",
        "duns_emitido": "由Dun & Bradstreet颁发——全球公认的企业身份标准，在190多个国家得到认可。",
        "duns_paises": "190多个国家",
        "duns_beneficios": [
            ("B2B合同", "获得全球招标和供应商资格"),
            ("合资企业", "尽职调查更便捷的国际合作"),
            ("即时信誉", "对机构投资者而言是严肃性的标志"),
        ],
        "mercado_titulo": "市场机遇",
        "mercado_texto": "我们正处于完美的交汇点：数字健康在全球爆发，而数字命理和占星正迁移至高参与度的应用。A1ELOS恰好定位在这一交汇处，全球已有74%的人口上网（约60亿人）。",
        "mercado_cards": [
            ("全球健康", "6.8万亿美元 → 2029年达9.8万亿（年增7.6%）"),
            ("占星/数字命理应用", "30亿美元 → 2030年达90亿 · 年复合增长20%"),
            ("健康应用", "年复合增长14.9% → 2030年达262亿"),
            ("在线用户", "全球74% · 约60亿人"),
        ],
        "problema_titulo": "我们解决的问题",
        "problema_col_esq_titulo": "当前市场缺陷",
        "problema_col_esq": [
            ("语言障碍", "绝大多数数字命理工具仅以英语运作，将其他语言的数十亿母语使用者排除在外。"),
            ("价格脱离现实", "面向新兴市场的产品以美元计价，造成经济排斥——用户拒绝的不是产品，而是无法承受的价格。"),
            ("缺乏深度", "通用工具提供肤浅的答案，没有个性化、没有文化背景，也没有日常生活的实际应用。"),
        ],
        "problema_col_dir_titulo": "排斥的代价",
        "problema_col_dir": "当平台忽视语言和购买力时，它自愿放弃了世界上最大的市场：生活在新兴经济体、使用非英语语言的40多亿人。这正是A1ELOS以精准方式占据的空白。",
        "problema_destaque": "忽视本地购买力的平台将失去全球可及市场60%以上的份额。",
        "solucao_titulo": "我们的解决方案：三大战略支柱",
        "solucao_texto": "A1ELOS构建了一个集数字科学、人工智能和文化敏感性于一体的集成平台。解决方案在三个互补方向运作，确保收入多元化和高留存率。",
        "solucao_colunas": [
            ("个人命盘", "为最终用户提供深入、个性化的数字分析——身份、使命、生命周期和兼容性——以14种语言交付并集成AI。"),
            ("企业数字命理", "将数字命理诊断应用于品牌、CNPJ、创立日期和企业战略。在B2B市场具有高感知价值的差异化产品。"),
            ("白标B2B", "为希望以自有品牌提供数字命理的合作伙伴公司提供平台授权——支持多语言和完全定制。"),
        ],
        "alcance_titulo": "全球覆盖：14种语言 · 约53亿使用者",
        "alcance_texto": "A1ELOS以真正多语言的平台覆盖全球约67%的人口。每种语言代表一个独特的文化市场，价格根据当地购买力进行校准。",
        "mercados_titulo": "3个新市场：新增4.42亿使用者",
        "mercados_texto": "向印度尼西亚、土耳其和越南的战略扩张代表着质的飞跃：这些市场经济增长强劲、数字渗透率不断提高，且对可负担的数字健康解决方案有经证实的需求。",
        "mercados_cards": [
            ("印度尼西亚", ["2.85亿居民", "互联网普及率80.5%", "约2.55亿印尼语使用者", "健康：512亿美元（2025）→ 728亿（2034）"]),
            ("土耳其", ["8590万居民", "人均购买力平价GDP 37,301美元", "约9000万土耳其语使用者", "高于世界平均水平（27,211美元）"]),
            ("越南",  ["约1亿居民", "人均GDP约5,066美元（年增7.4%）", "约9700万越南语使用者", "健康：3.03亿美元（2025）→ 4.85亿（2030）"]),
        ],
        "mercados_rodape": "3个新市场 = 新增4.42亿可及使用者——以文化校准的价格纳入平台。",
        "preco_titulo": "有意识的定价理念",
        "preco_esq": "文化尊重 + 对购买力的尊重 = 真实可及市场。相同的价值比例。不同的价格。所有市场享有同等尊严。",
        "preco_dir_titulo": "实际运作方式",
        "preco_dir": "A1ELOS将购买力平价（PPP）作为核心定价标准。同一产品为拉各斯、雅加达、河内或纽约的用户提供相同的相对价值——价格经过校准，使财务负担与当地收入成比例。",
        "preco_pilares": [
            ("按PPP校准", "价格根据每个国家的购买力指数调整"),
            ("文化尊重", "语言、货币和本地情境融入产品"),
            ("更高转化率", "公平定价带来更高转化率和更好的长期留存"),
        ],
        "portfolio_titulo": "产品组合：4个级别共23款产品",
        "portfolio_texto": "分层结构确保每位用户——从好奇者到专业人士——都能找到适合其参与度和财务能力的方案。",
        "portfolio_tabela": [
            ["级别", "产品", "价格范围 (¥)", "用户画像"],
            ["入门", "快速地图、快速咨询", "¥ 26", "好奇、首次接触"],
            ["中级", "AI研究、完整地图、兼容性", "¥ 53", "活跃用户"],
            ["高级", "企业数字命理、周期、使命", "¥ 71–98", "专业人士、创业者"],
            ["尊享", "完整诊断、个人白标", "¥ 125–260", "高收入、企业使用"],
            ["B2B / 企业", "企业套餐、许可证、礼品", "面议", "企业和人力资源"],
        ],
        "portfolio_rodape": "23款产品覆盖用户全程，从首次接触到经常性尊享客户——按语言和市场最大化LTV。",
        "negocio_titulo": "商业模式：三大收入来源",
        "negocio_texto": "A1ELOS的设计实现了多元化和可扩展的收入：面向全球最终消费者的直接销售、高价值B2B合同以及经常性地理定位广告——三个相互促进的引擎。",
        "negocio_colunas": [
            ("B2C — 14种语言", "以所有货币直接销售数字产品，价格按PPP调整。通过AI自动扩展——无需与增长成比例的支持团队。"),
            ("B2B — 渐进式折扣", "面向人力资源、雇主品牌和机构礼品的公司套餐。按量享10%至70%折扣。合同由DUNS 942242668背书。"),
            ("地理定位广告", "按国家、大洲或全球细分的横幅，自动轮换。高价值经常性月收入——不依赖产品销售数量。"),
        ],
        "banners_titulo": "广告横幅——经常性月收入",
        "banners_texto": "A1ELOS平台提供高级广告空间，按地理位置精准细分——国家、大洲或全球。每8秒自动轮换，并针对桌面和移动端优化格式，横幅为区域和国际广告商提供可衡量的曝光度。",
        "banners_tabela": [
            ["细分", "固定 (¥/月)", "临时 (¥/月)", "广告商画像"],
            ["国家", "¥ 800", "¥ 500", "本地中小企业、区域商业"],
            ["大洲", "¥ 1.800", "¥ 1.200", "区域品牌、大洲扩张"],
            ["全球", "¥ 3.500", "¥ 2.500", "全球企业、国际应用"],
            ["独家赞助", "¥ 6.000", "¥ 4.500/活动", "主赞助商、发布活动"],
        ],
        "banners_formatos": "728×90像素 — 桌面中央横幅 · 320×100像素 — 优化移动格式 · 8秒 — 自动轮换 · 地理定向 — 国家、大洲或全球覆盖",
        "b2b_titulo": "B2B企业套餐——高价值、大数量",
        "b2b_texto": "B2B套餐将A1ELOS转变为企业雇主品牌和福利工具。企业批量购买访问码，作为礼品分发给员工或客户——由DUNS 942242668为正式企业合同背书。",
        "b2b_planos": [
            ("基础套餐 · 50个码", "50× 快速地图（每个¥ 26）。适合员工福利计划和入职活动。"),
            ("中级套餐 · 100个码", "50× 快速 + 50× AI研究（¥ 53）。适合人力资源和雇主品牌战略。"),
            ("尊享套餐 · 200个码", "100× 快速 + 100× 完整地图（¥ 53）。为大型团队提供最大分析深度。"),
        ],
        "b2b_tabela": [
            ["起订量", "折扣", "画像", "推荐用途"],
            ["10个码", "10%", "小型团队", "一次性福利活动"],
            ["100个码", "30%", "中小企业", "季度福利计划"],
            ["500个码", "50%", "中型企业", "年度员工礼品"],
            ["1,000个码", "70%", "大型企业", "客户忠诚度计划"],
        ],
        "projecoes_titulo": "财务预测：50年展望",
        "projecoes_texto": "预测基于两种情景——保守和乐观——反映不同的市场渗透率、B2B扩张速度和按语言的有机增长。",
        "projecoes_tabela": [
            ["展望", "保守 (¥)", "乐观 (¥)"],
            ["第1年", "¥ 6万", "¥ 24万"],
            ["第3年", "¥ 22万", "¥ 84万"],
            ["第5年", "¥ 94万", "¥ 280万"],
            ["第10年", "¥ 560万", "¥ 1,500万"],
            ["第20年", "¥ 2,800万", "¥ 7,500万"],
            ["第30年", "¥ 6,500万", "¥ 1.68亿"],
            ["第40年", "¥ 1.03亿", "¥ 2.8亿"],
            ["第50年", "¥ 1.4亿", "¥ 4.68亿"],
        ],
        "tracao_titulo": "牵引力与经证实的成果",
        "tracao_texto": "A1ELOS已通过验证模型的产品指标运营——高留存率、高级评价和不断增长的B2B合作伙伴基础表明，平台为最终用户和企业市场带来真实价值。",
        "tracao_kpis": [
            ("1.2万+", "活跃用户", "稳定的有机增长基础"),
            ("87%", "留存率", "远高于行业平均水平（约30%）"),
            ("4.8★", "平均评分", "经证实的最终用户满意度"),
            ("23", "B2B合作伙伴", "与企业和人力资源的活跃合同"),
        ],
        "roteiro_titulo": "战略路线图",
        "roteiro_texto": "A1ELOS分四个渐进阶段执行计划——从当前基础的巩固到全球市场领导地位，为投资者提供明确的退出选择。",
        "roteiro_fases": [
            ("第一阶段 · 巩固", "加强已活跃语言的基础用户群。优化转化率、留存率和LTV。种子轮已完成。"),
            ("第二阶段 · 扩张", "在3个新市场正式启动：印度尼西亚、土耳其和越南。加速B2B渠道和地理定位广告。"),
            ("第三阶段 · 全球进入", "以本地化活动在全部14种语言中积极存在。在5大洲建立白标合作。A轮。"),
            ("第四阶段 · 领导地位", "20多个国家拥有成熟运营。应用数字命理领域的全球参考SaaS平台。IPO或战略退出。"),
        ],
        "invest_titulo": "投资与联系",
        "invest_texto": "我们已准备好进行私人演示、尽职调查和谈判。请通过您偏好的渠道联系我们。",
        "invest_dados": [
            ("种子轮", "¥ 52万"),
            ("投资前估值", "¥ 210万"),
            ("出让股权", "最高20%"),
        ],
        "invest_contato": [
            ("投资者邮箱", "a1elos.consultoria@gmail.com"),
            ("通用邮箱", "contato@a1elos.com"),
            ("网站", "www.a1elos.com"),
            ("DUNS", "942242668 — Dun & Bradstreet"),
        ],
        "invest_alocacao": "资金分配：45% 技术 · 30% 营销 · 25% 运营",
        "frase_final": "数字从不撒谎。",
        "selo_final": ["DUNS 942242668", "23款产品", "14种语言", "约53亿使用者"],
        "graf_cons": "保守",
        "graf_otim": "乐观",
        "grafico_titulo_linha": "预计增长（千元）",
    },

    "he": {
        "titulo": "A1ELOS נומרולוגיה גלובלית",
        "subtitulo": "מדע המספרים מיושם להצלחתך",
        "capa_nota": "מצגת אסטרטגית למשקיעים ושותפים",
        "confidencial": "סודי",
        "ano": "2026",
        "sumario_intro": "מצגת זו בנויה כדי להדריך משקיעים ושותפים בכל ההיבטים האסטרטגיים של A1ELOS נומרולוגיה גלובלית — מתזת השוק ועד מודל ההכנסות החוזרות.",
        "sumario_cards": [
            ("01", "אודות A1ELOS", "חברת אחזקות, פורטפוליו ואישור DUNS"),
            ("02", "הזדמנות שוק", "כלכלת הבריאות העולמית 6.8 טריליון דולר"),
            ("03", "פתרון והיקף גלובלי", "14 שפות, ~5.3 מיליארד דוברים"),
            ("04", "3 שווקים חדשים", "אינדונזיה, טורקיה ווייטנאם"),
            ("05", "פורטפוליו ומחירים", "23 מוצרים מכוילים לפי כוח קנייה"),
            ("06", "הכנסות חוזרות", "באנרים פרסומיים וחבילות B2B"),
            ("07", "תחזיות והשקעה", "אופק של 50 שנה · סבב סיד ₪ 440 אלף"),
        ],
        "sobre_titulo": "אודות A1ELOS",
        "sobre_texto": "A1ELOS היא חברת אחזקות טכנולוגיה וידע המאחדת בינה מלאכותית, נומרולוגיה יישומית ואסטרטגיה תרבותית ליצירת מוצרים דיגיטליים בעלי השפעה גבוהה בקנה מידה עולמי. המשימה שלנו: לדמוקרטיזציה של ידע עצמי נומרי עם כבוד תרבותי וכבוד לכוח הקנייה של כל שוק.",
        "sobre_kpis": [
            ("23", "מוצרים פעילים", "ב-4 רמות גישה"),
            ("14", "שפות", "~67% מאוכלוסיית העולם"),
            ("5.3B", "דוברים", "שוק אמיתי ניתן לגישה"),
            ("AI", "משולב", "מנוע התאמה אישית"),
        ],
        "sobre_duns": "DUNS 942242668 — הסמכת Dun & Bradstreet תקפה ביותר מ-190 מדינות, המאפשרת חוזי B2B ומיזמים משותפים בינלאומיים.",
        "duns_titulo": "אמינות בינלאומית",
        "duns_texto": "מספר ה-DUNS הוא הדרכון הארגוני של A1ELOS בזירה הבינלאומית. הוא מאותת לשותפים, ללקוחות ארגוניים ולמשקיעים שלחברה זהות ניתנת לאימות, היסטוריה ניתנת למעקב ויכולת חוזית בכל תחום שיפוט.",
        "duns_numero": "942242668",
        "duns_emitido": "הונפק על ידי Dun & Bradstreet — התקן העולמי לזהות ארגונית המוכר ביותר מ-190 מדינות.",
        "duns_paises": "190+ מדינות",
        "duns_beneficios": [
            ("חוזי B2B", "הסמכה למכרזים וספקים גלובליים"),
            ("מיזמים משותפים", "שותפויות בינלאומיות עם בדיקת נאותות מקלה"),
            ("אמינות מיידית", "סימן רצינות למשקיעים מוסדיים"),
        ],
        "mercado_titulo": "הזדמנות שוק",
        "mercado_texto": "אנו חיים בהתכנסות מושלמת: בריאות דיגיטלית מתפוצצת בעולם בעוד נומרולוגיה ואסטרולוגיה עוברות לאפליקציות בעלות מעורבות גבוהה. A1ELOS ממוקמת בדיוק בצומת הזה, עם 74% מאוכלוסיית העולם כבר מחוברים (~6 מיליארד אנשים).",
        "mercado_cards": [
            ("בריאות עולמית", "6.8 טריליון → 9.8 טריליון עד 2029 (+7.6% לשנה)"),
            ("אפליקציות אסטרולוגיה/נומרולוגיה", "3 מיליארד → 9 מיליארד עד 2030 · צמיחה 20%"),
            ("אפליקציות בריאות", "צמיחה 14.9% → 26.2 מיליארד עד 2030"),
            ("משתמשים מקוונים", "74% מהעולם · ~6 מיליארד אנשים"),
        ],
        "problema_titulo": "הבעיה שאנו פותרים",
        "problema_col_esq_titulo": "כשלי השוק הנוכחיים",
        "problema_col_esq": [
            ("מחסום שפה", "הרוב המכריע של כלי הנומרולוגיה פועל רק באנגלית, ומדיר מיליארדי דוברי שפת אם בשפות אחרות."),
            ("מחירים מנותקים מהמציאות", "מוצרים המחויבים בדולרים לשווקים מתפתחים יוצרים הדרה כלכלית — המשתמש אינו דוחה את המוצר, אלא את המחיר הבלתי נגיש."),
            ("חוסר עומק", "כלים גנריים מספקים תשובות שטחיות ללא התאמה אישית, ללא הקשר תרבותי וללא יישום מעשי בחיי היום-יום."),
        ],
        "problema_col_dir_titulo": "מחיר ההדרה",
        "problema_col_dir": "כאשר פלטפורמה מתעלמת משפה ומכוח קנייה, היא נוטת מרצון את השוק הגדול בעולם: יותר מ-4 מיליארד אנשים החיים בכלכלות מתפתחות ומדברים שפות שאינן אנגליות. זהו הפער ש-A1ELOS תופסת בדיוק כירורגי.",
        "problema_destaque": "פלטפורמות שמתעלמות מכוח קנייה מקומי מאבדות גישה ליותר מ-60% מהשוק העולמי הניתן לגישה.",
        "solucao_titulo": "הפתרון שלנו: 3 עמודי תווך אסטרטגיים",
        "solucao_texto": "A1ELOS בנתה פלטפורמה משולבת המשלבת מדע מספרי, בינה מלאכותית ורגישות תרבותית. הפתרון פועל בשלוש חזיתות משלימות, ומבטיח הכנסות מגוונות ושימור גבוה.",
        "solucao_colunas": [
            ("מפות אישיות", "ניתוחים מספריים עמוקים ומותאמים אישית למשתמש הקצה — זהות, שליחות, מחזורי חיים ותאימות — המועברים ב-14 שפות עם בינה מלאכותית משולבת."),
            ("נומרולוגיה עסקית", "אבחונים נומרולוגיים המיושמים על מותגים, CNPJ, תאריכי הקמה ואסטרטגיה ארגונית. מוצר מובחן בעל ערך נתפס גבוה בשוק ה-B2B."),
            ("White-Label B2B", "רישוי הפלטפורמה לחברות שותפות המעוניינות להציע נומרולוגיה תחת המותג שלהן — עם תמיכה רב-לשונית והתאמה מלאה."),
        ],
        "alcance_titulo": "היקף גלובלי: 14 שפות · ~5.3 מיליארד דוברים",
        "alcance_texto": "A1ELOS מכסה ~67% מאוכלוסיית העולם עם פלטפורמה רב-לשונית אמיתית. כל שפה מייצגת שוק תרבותי מובחן, עם מחירים מכוילים לכוח הקנייה המקומי.",
        "mercados_titulo": "3 השווקים החדשים: +442 מיליון דוברים",
        "mercados_texto": "ההתרחבות האסטרטגית לאינדונזיה, טורקיה ווייטנאם מייצגת קפיצה איכותית: שווקים עם צמיחה כלכלית גבוהה, חדירה דיגיטלית גוברת וביקוש מוכח לפתרונות בריאות דיגיטליים נגישים.",
        "mercados_cards": [
            ("אינדונזיה", ["285 מיליון תושבים", "חדירת אינטרנט 80.5%", "~255 מיליון דוברי אינדונזית", "בריאות: 51.2 מיליארד (2025) → 72.8 מיליארד (2034)"]),
            ("טורקיה", ["85.9 מיליון תושבים", "תמ\"ג PPP לנפש 37,301 דולר", "~90 מיליון דוברי טורקית", "מעל הממוצע העולמי (27,211 דולר)"]),
            ("וייטנאם",  ["~100 מיליון תושבים", "תמ\"ג לנפש ~5,066 דולר (+7.4%/שנה)", "~97 מיליון דוברי וייטנאמית", "בריאות: 303 מיליון (2025) → 485 מיליון (2030)"]),
        ],
        "mercados_rodape": "3 שווקים חדשים = +442 מיליון דוברים חדשים הניתנים לגישה — משולבים בפלטפורמה עם מחירים מכוילים תרבותית.",
        "preco_titulo": "פילוסופיית תמחור מודעת",
        "preco_esq": "כבוד תרבותי + כבוד לכוח קנייה = שוק אמיתי ניתן לגישה. אותו יחס ערך. מחירים שונים. כבוד שווה לכל השווקים.",
        "preco_dir_titulo": "איך זה עובד בפועל",
        "preco_dir": "A1ELOS מיישמת שוויון כוח קנייה (PPP) כקריטריון תמחור מרכזי. אותו מוצר מספק את אותו ערך יחסי למשתמש בלאגוס, ג'קרטה, האנוי או ניו יורק — המחיר מכויל כך שהמאמץ הכספי יהיה פרופורציונלי להכנסה המקומית.",
        "preco_pilares": [
            ("כיול לפי PPP", "מחירים מותאמים למדד כוח הקנייה של כל מדינה"),
            ("כבוד תרבותי", "שפה, מטבע והקשר מקומי משולבים במוצר"),
            ("המרה גבוהה יותר", "מחיר הוגן מייצר יותר המרות ושימור גבוה יותר לטווח ארוך"),
        ],
        "portfolio_titulo": "פורטפוליו: 23 מוצרים ב-4 רמות",
        "portfolio_texto": "המבנה השכבתי מבטיח שכל פרופיל משתמש — מהסקרן ועד המקצוען — ימצא הצעה המתאימה לרמת המעורבות וליכולת הפיננסית שלו.",
        "portfolio_tabela": [
            ["רמה", "מוצרים", "טווח מחירים (₪)", "פרופיל"],
            ["כניסה", "מפה אקספרס, ייעוץ מהיר", "₪ 44", "סקרן, מגע ראשון"],
            ["בינוני", "מחקר AI, מפה מלאה, תאימות", "₪ 98", "משתמש מעורב"],
            ["מתקדם", "נומרולוגיה עסקית, מחזורים, שליחות", "₪ 143–197", "מקצוען, יזם"],
            ["פרימיום", "אבחון מלא, White-Label אישי", "₪ 242–530", "הכנסה גבוהה, שימוש עסקי"],
            ["B2B / עסקי", "חבילות עסקיות, רישיונות, מתנות", "לפי בקשה", "חברות ומשאבי אנוש"],
        ],
        "portfolio_rodape": "23 מוצרים מכסים את כל מסע המשתמש, מהמגע הראשון ועד לקוח הפרימיום החוזר — ממקסמים LTV לכל שפה ושוק.",
        "negocio_titulo": "מודל עסקי: 3 מקורות הכנסה",
        "negocio_texto": "A1ELOS תוכננה עם הכנסות מגוונות וניתנות להרחבה: מכירות ישירות לצרכן הסופי בקנה מידה עולמי, חוזי B2B בעלי ערך גבוה ופרסום גיאוגרפי חוזר — שלושה מנועים המזינים זה את זה.",
        "negocio_colunas": [
            ("B2C — 14 שפות", "מכירה ישירה של מוצרים דיגיטליים בכל המטבעות, עם מחירים מותאמים לפי PPP. הרחבה אוטומטית דרך AI — ללא צוות תמיכה פרופורציונלי לצמיחה."),
            ("B2B — הנחות פרוגרסיביות", "חבילות ארגוניות למשאבי אנוש, מיתוג מעסיק ומתנות מוסדיות. הנחות מ-10% עד 70% לפי נפח. חוזים הנתמכים ב-DUNS 942242668."),
            ("פרסום גיאוגרפי", "באנרים מחולקים לפי מדינה, יבשת או עולם עם רוטציה אוטומטית. הכנסות חוזרות חודשיות בעלות ערך גבוה — ללא תלות בנפח מכירות המוצר."),
        ],
        "banners_titulo": "באנרים פרסומיים — הכנסות חוזרות חודשיות",
        "banners_texto": "פלטפורמת A1ELOS מציעה שטחי פרסום פרימיום עם חלוקה מדויקת לפי מיקום גיאוגרפי — מדינה, יבשת או עולם. עם רוטציה אוטומטית כל 8 שניות ופורמטים מותאמים לשולחן העבודה ולמובייל, הבאנרים מספקים חשיפה מדידה למפרסמים אזוריים ובינלאומיים.",
        "banners_tabela": [
            ["חלוקה", "קבוע (₪/חודש)", "זמני (₪/חודש)", "פרופיל מפרסם"],
            ["מדינה", "₪ 800", "₪ 500", "עסקים קטנים מקומיים, מסחר אזורי"],
            ["יבשת", "₪ 1,800", "₪ 1,200", "מותגים אזוריים, התרחבות יבשתית"],
            ["עולם", "₪ 3,500", "₪ 2,500", "חברות גלובליות, אפליקציות בינלאומיות"],
            ["חסות בלעדית", "₪ 6,000", "₪ 4,500/קמפיין", "נותני חסות ראשיים, השקות"],
        ],
        "banners_formatos": "728×90 פיקסלים — באנר שולחן עבודה מרכזי · 320×100 פיקסלים — פורמט מובייל מותאם · 8 שניות — רוטציה אוטומטית · מיקוד גיאוגרפי — מדינה, יבשת או היקף עולמי",
        "b2b_titulo": "חבילות B2B ארגוניות — ערך גבוה, נפח גבוה",
        "b2b_texto": "חבילות ה-B2B הופכות את A1ELOS לכלי למיתוג מעסיק ובריאות ארגונית. חברות רוכשות קודי גישה בכמות גדולה לחלוקה כמתנות לעובדים או ללקוחות — הנתמכים ב-DUNS 942242668 לחוזים ארגוניים רשמיים.",
        "b2b_planos": [
            ("תוכנית בסיס · 50 קודים", "50× מפת אקספרס (₪ 44 כל אחת). אידיאלית לתוכניות בריאות עובדים ופעולות אונבורדינג."),
            ("תוכנית בינונית · 100 קודים", "50× אקספרס + 50× מחקר AI (₪ 98). מושלמת למשאבי אנוש ואסטרטגיות מיתוג מעסיק."),
            ("תוכנית פרימיום · 200 קודים", "100× אקספרס + 100× מפה מלאה (₪ 98). עומק אנליטי מקסימלי לצוותים גדולים."),
        ],
        "b2b_tabela": [
            ["מ-", "הנחה", "פרופיל", "שימוש מומלץ"],
            ["10 קודים", "10%", "צוותים קטנים", "פעולת בריאות נקודתית"],
            ["100 קודים", "30%", "עסקים קטנים", "תוכנית הטבות רבעונית"],
            ["500 קודים", "50%", "חברות בינוניות", "מתנה שנתית לעובדים"],
            ["1,000 קודים", "70%", "תאגידים גדולים", "תוכנית נאמנות לקוחות"],
        ],
        "projecoes_titulo": "תחזיות פיננסיות: אופק של 50 שנה",
        "projecoes_texto": "התחזיות נבנו על שני תרחישים — שמרני ואופטימי — המשקפים שיעורי חדירת שוק שונים, מהירות התרחבות B2B וצמיחה אורגנית לכל שפה.",
        "projecoes_tabela": [
            ["אופק", "שמרני (₪)", "אופטימי (₪)"],
            ["שנה 1", "₪ 600 אלף", "₪ 2.4 מיליון"],
            ["שנה 3", "₪ 2.2 מיליון", "₪ 8.4 מיליון"],
            ["שנה 5", "₪ 9.4 מיליון", "₪ 28 מיליון"],
            ["שנה 10", "₪ 56 מיליון", "₪ 150 מיליון"],
            ["שנה 20", "₪ 280 מיליון", "₪ 750 מיליון"],
            ["שנה 30", "₪ 650 מיליון", "₪ 1.68 מיליארד"],
            ["שנה 40", "₪ 1.03 מיליארד", "₪ 2.8 מיליארד"],
            ["שנה 50", "₪ 1.4 מיליארד", "₪ 4.68 מיליארד"],
        ],
        "tracao_titulo": "מומנטום ותוצאות מוכחות",
        "tracao_texto": "A1ELOS כבר פועלת עם מדדי מוצר המאמתים את המודל — שימור גבוה, דירוג פרימיום ובסיס גדל של שותפי B2B מוכיחים שהפלטפורמה מספקת ערך אמיתי למשתמש הקצה ולשוק הארגוני.",
        "tracao_kpis": [
            ("12K+", "משתמשים פעילים", "בסיס צמיחה אורגני עקבי"),
            ("87%", "שימור", "הרבה מעל ממוצע התעשייה (~30%)"),
            ("4.8★", "דירוג ממוצע", "שביעות רצון מוכחת של משתמש הקצה"),
            ("23", "שותפי B2B", "חוזים פעילים עם חברות ומשאבי אנוש"),
        ],
        "roteiro_titulo": "מפת דרכים אסטרטגית",
        "roteiro_texto": "A1ELOS מבצעת תוכנית בארבעה שלבים מתקדמים — מגיבוש הבסיס הנוכחי ועד למנהיגות שוק גלובלית, עם אפשרויות יציאה ברורות למשקיעים.",
        "roteiro_fases": [
            ("שלב 1 · גיבוש", "חיזוק בסיס המשתמשים בשפות הפעילות כבר. אופטימיזציה של המרה, שימור ו-LTV. סבב סיד הושלם."),
            ("שלב 2 · התרחבות", "השקה רשמית ב-3 השווקים החדשים: אינדונזיה, טורקיה ווייטנאם. האצת ערוץ ה-B2B והפרסום הגיאוגרפי."),
            ("שלב 3 · כניסה גלובלית", "נוכחות פעילה בכל 14 השפות עם קמפיינים מקומיים. שותפויות White-Label ב-5+ יבשות. סדרה A."),
            ("שלב 4 · מנהיגות", "20+ מדינות עם פעילות מגובשת. פלטפורמת SaaS גלובלית מובילה בנומרולוגיה יישומית. הנפקה או יציאה אסטרטגית."),
        ],
        "invest_titulo": "השקעה ויצירת קשר",
        "invest_texto": "אנחנו מוכנים למצגות פרטיות, בדיקת נאותות ומשא ומתן. צור קשר בערוץ המועדף עליך.",
        "invest_dados": [
            ("סבב סיד", "₪ 440 אלף"),
            ("שווי לפני הכסף", "₪ 1.76 מיליון"),
            ("ההון המוצע", "עד 20%"),
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
        "grafico_titulo_linha": "צמיחה חזויה (₪ אלפים)",
    },

    "ar": {
        "titulo": "A1ELOS علم الأرقام العالمي",
        "subtitulo": "علم الأرقام المطبق على نجاحك",
        "capa_nota": "عرض استراتيجي للمستثمرين والشركاء",
        "confidencial": "سري",
        "ano": "2026",
        "sumario_intro": "تم تنظيم هذا العرض لتوجيه المستثمرين والشركاء عبر جميع الجوانب الاستراتيجية لعلم الأرقام العالمي A1ELOS — من أطروحة السوق إلى نموذج الإيرادات المتكررة.",
        "sumario_cards": [
            ("01", "حول A1ELOS", "القابضة والمحفظة واعتماد DUNS"),
            ("02", "فرصة السوق", "اقتصاد العافية العالمي 6.8 تريليون دولار"),
            ("03", "الحل والانتشار العالمي", "14 لغة، ~5.3 مليار متحدث"),
            ("04", "3 أسواق جديدة", "إندونيسيا وتركيا وفيتنام"),
            ("05", "المحفظة والأسعار", "23 منتجًا معايرًا حسب القوة الشرائية"),
            ("06", "الإيرادات المتكررة", "لافتات إعلانية وباقات B2B"),
            ("07", "التوقعات والاستثمار", "أفق 50 عامًا · جولة بذرة ﷼ 350 ألف"),
        ],
        "sobre_titulo": "حول A1ELOS",
        "sobre_texto": "A1ELOS هي شركة قابضة للتكنولوجيا والمعرفة تجمع بين الذكاء الاصطناعي وعلم الأرقام التطبيقي والاستراتيجية الثقافية لإنشاء منتجات رقمية عالية التأثير على نطاق عالمي. مهمتنا: إضفاء الطابع الديمقراطي على المعرفة الذاتية الرقمية مع الاحترام الثقافي واحترام القوة الشرائية لكل سوق.",
        "sobre_kpis": [
            ("23", "منتج نشط", "في 4 مستويات وصول"),
            ("14", "لغة", "~67% من سكان العالم"),
            ("5.3B", "متحدث", "سوق حقيقي قابل للوصول"),
            ("AI", "مدمج", "محرك التخصيص"),
        ],
        "sobre_duns": "DUNS 942242668 — شهادة Dun & Bradstreet سارية في أكثر من 190 دولة، تتيح عقود B2B والمشاريع المشتركة الدولية.",
        "duns_titulo": "المصداقية الدولية",
        "duns_texto": "رقم DUNS هو جواز السفر المؤسسي لـ A1ELOS على الساحة الدولية. إنه يشير للشركاء والعملاء من الشركات والمستثمرين إلى أن الشركة تمتلك هوية قابلة للتحقق وتاريخًا يمكن تتبعه وقدرة تعاقدية في أي ولاية قضائية.",
        "duns_numero": "942242668",
        "duns_emitido": "صادر عن Dun & Bradstreet — المعيار العالمي لهوية الشركات المعترف به في أكثر من 190 دولة.",
        "duns_paises": "190+ دولة",
        "duns_beneficios": [
            ("عقود B2B", "التمكين للمناقصات والموردين العالميين"),
            ("المشاريع المشتركة", "شراكات دولية مع سهولة العناية الواجبة"),
            ("مصداقية فورية", "علامة جدية للمستثمرين المؤسسيين"),
        ],
        "mercado_titulo": "فرصة السوق",
        "mercado_texto": "نعيش التقاء مثاليًا: العافية الرقمية تنفجر عالميًا بينما ينتقل علم الأرقام وعلم التنجيم إلى تطبيقات عالية التفاعل. A1ELOS في موقع دقيق عند هذا التقاطع، مع 74% من سكان العالم متصلين بالفعل (~6 مليارات شخص).",
        "mercado_cards": [
            ("العافية العالمية", "6.8 تريليون → 9.8 تريليون بحلول 2029 (+7.6% سنويًا)"),
            ("تطبيقات التنجيم/الأرقام", "3 مليارات → 9 مليارات بحلول 2030 · نمو سنوي 20%"),
            ("تطبيقات العافية", "نمو سنوي 14.9% → 26.2 مليار بحلول 2030"),
            ("المستخدمون عبر الإنترنت", "74% من العالم · ~6 مليارات شخص"),
        ],
        "problema_titulo": "المشكلة التي نحلها",
        "problema_col_esq_titulo": "إخفاقات السوق الحالية",
        "problema_col_esq": [
            ("حاجز اللغة", "الغالبية العظمى من أدوات علم الأرقام تعمل بالإنجليزية فقط، مستبعدة مليارات المتحدثين الأصليين بلغات أخرى."),
            ("أسعار منفصلة عن الواقع", "المنتجات المسعرة بالدولار للأسواق الناشئة تولد إقصاءً اقتصاديًا — المستخدم لا يرفض المنتج، بل يرفض السعر غير المتاح."),
            ("نقص العمق", "الأدوات العامة تقدم إجابات سطحية دون تخصيص ودون سياق ثقافي ودون تطبيق عملي في الحياة اليومية."),
        ],
        "problema_col_dir_titulo": "تكلفة الإقصاء",
        "problema_col_dir": "عندما تتجاهل منصة اللغة والقوة الشرائية، فإنها تتخلى طواعية عن أكبر سوق في العالم: أكثر من 4 مليارات شخص يعيشون في اقتصادات ناشئة ويتحدثون لغات غير ناطقة بالإنجليزية. هذه هي الفجوة التي تحتلها A1ELOS بدقة جراحية.",
        "problema_destaque": "المنصات التي تتجاهل القوة الشرائية المحلية تفقد الوصول إلى أكثر من 60% من السوق العالمي القابل للوصول.",
        "solucao_titulo": "حلنا: 3 ركائز استراتيجية",
        "solucao_texto": "بنى A1ELOS منصة متكاملة تجمع بين العلم الرقمي والذكاء الاصطناعي والحساسية الثقافية. يعمل الحل على ثلاث جبهات متكاملة، مما يضمن إيرادات متنوعة وارتفاع الاحتفاظ.",
        "solucao_colunas": [
            ("خرائط شخصية", "تحليلات رقمية عميقة ومخصصة للمستخدم النهائي — الهوية والرسالة ودورات الحياة والتوافق — مقدمة بـ14 لغة مع ذكاء اصطناعي مدمج."),
            ("علم أرقام الأعمال", "تشخيصات رقمية مطبقة على العلامات التجارية وCNPJ وتواريخ التأسيس والاستراتيجية المؤسسية. منتج متمايز بقيمة مدركة عالية في سوق B2B."),
            ("العلامة البيضاء B2B", "ترخيص المنصة للشركات الشريكة التي ترغب في تقديم علم الأرقام تحت علامتها التجارية الخاصة — مع دعم متعدد اللغات وتخصيص كامل."),
        ],
        "alcance_titulo": "الانتشار العالمي: 14 لغة · ~5.3 مليار متحدث",
        "alcance_texto": "يغطي A1ELOS ~67% من سكان العالم بمنصة متعددة اللغات حقًا. كل لغة تمثل سوقًا ثقافيًا متميزًا، مع أسعار معايرة حسب القوة الشرائية المحلية.",
        "mercados_titulo": "الأسواق الثلاثة الجديدة: +442 مليون متحدث",
        "mercados_texto": "يمثل التوسع الاستراتيجي إلى إندونيسيا وتركيا وفيتنام قفزة نوعية: أسواق ذات نمو اقتصادي مرتفع واختراق رقمي متزايد وطلب مثبت على حلول العافية الرقمية المتاحة.",
        "mercados_cards": [
            ("إندونيسيا", ["285 مليون نسمة", "اختراق الإنترنت 80.5%", "~255 مليون متحدث بالإندونيسية", "العافية: 51.2 مليار (2025) → 72.8 مليار (2034)"]),
            ("تركيا", ["85.9 مليون نسمة", "ناتج محلي PPP للفرد 37,301 دولار", "~90 مليون متحدث بالتركية", "فوق المتوسط العالمي (27,211 دولار)"]),
            ("فيتنام",  ["~100 مليون نسمة", "ناتج محلي للفرد ~5,066 دولار (+7.4%/سنة)", "~97 مليون متحدث بالفيتنامية", "العافية: 303 مليون (2025) → 485 مليون (2030)"]),
        ],
        "mercados_rodape": "3 أسواق جديدة = +442 مليون متحدث جديد قابل للوصول — مدمجون في المنصة بأسعار معايرة ثقافيًا.",
        "preco_titulo": "فلسفة التسعير الواعي",
        "preco_esq": "الاحترام الثقافي + احترام القوة الشرائية = سوق حقيقي قابل للوصول. نفس نسبة القيمة. أسعار مختلفة. كرامة متساوية لجميع الأسواق.",
        "preco_dir_titulo": "كيف يعمل عمليًا",
        "preco_dir": "يطبق A1ELOS تعادل القوة الشرائية (PPP) كمعيار تسعير مركزي. نفس المنتج يقدم نفس القيمة النسبية للمستخدم في لاغوس أو جاكرتا أو هانوي أو نيويورك — يُعاير السعر بحيث يتناسب الجهد المالي مع الدخل المحلي.",
        "preco_pilares": [
            ("المعايرة حسب PPP", "أسعار معدلة حسب مؤشر القوة الشرائية لكل دولة"),
            ("الاحترام الثقافي", "اللغة والعملة والسياق المحلي مدمجة في المنتج"),
            ("تحويل أعلى", "السعر العادل يولد تحويلًا أعلى واحتفاظًا أكبر على المدى الطويل"),
        ],
        "portfolio_titulo": "المحفظة: 23 منتجًا في 4 مستويات",
        "portfolio_texto": "تضمن البنية الطبقية أن يجد كل ملف مستخدم — من الفضولي إلى المحترف — عرضًا مناسبًا لمستوى تفاعله وقدرته المالية.",
        "portfolio_tabela": [
            ["المستوى", "المنتجات", "نطاق السعر (﷼)", "الملف الشخصي"],
            ["الدخول", "خريطة إكسبرس، استشارة سريعة", "﷼ 35", "فضولي، أول تواصل"],
            ["متوسط", "بحث AI، خريطة كاملة، توافق", "﷼ 71", "مستخدم متفاعل"],
            ["متقدم", "علم الأرقام للأعمال، دورات، رسالة", "﷼ 107–143", "محترف، رائد أعمال"],
            ["بريميوم", "تشخيص كامل، علامة بيضاء شخصية", "﷼ 170–377", "دخل مرتفع، استخدام مؤسسي"],
            ["B2B / مؤسسي", "حزم الأعمال، تراخيص، هدايا", "عند الطلب", "الشركات والموارد البشرية"],
        ],
        "portfolio_rodape": "23 منتجًا تغطي رحلة المستخدم الكاملة، من أول تواصل إلى العميل المميز المتكرر — تعظيم LTV لكل لغة وسوق.",
        "negocio_titulo": "نموذج الأعمال: 3 مصادر إيرادات",
        "negocio_texto": "تم تصميم A1ELOS بإيرادات متنوعة وقابلة للتوسع: مبيعات مباشرة للمستهلك النهائي على نطاق عالمي، وعقود B2B عالية القيمة، وإعلانات جغرافية متكررة — ثلاثة محركات تغذي بعضها البعض.",
        "negocio_colunas": [
            ("B2C — 14 لغة", "بيع مباشر للمنتجات الرقمية بجميع العملات، بأسعار معدلة حسب PPP. توسع تلقائي عبر الذكاء الاصطناعي — دون فريق دعم يتناسب مع النمو."),
            ("B2B — خصومات تصاعدية", "حزم مؤسسية للموارد البشرية والعلامة التجارية لصاحب العمل والهدايا المؤسسية. خصومات من 10% إلى 70% حسب الحجم. عقود مدعومة بـ DUNS 942242668."),
            ("إعلانات جغرافية", "لافتات مقسمة حسب الدولة أو القارة أو العالم مع دوران تلقائي. إيرادات شهرية متكررة عالية القيمة — دون الاعتماد على حجم مبيعات المنتج."),
        ],
        "banners_titulo": "اللافتات الإعلانية — إيرادات شهرية متكررة",
        "banners_texto": "تقدم منصة A1ELOS مساحات إعلانية متميزة مع تقسيم دقيق حسب الموقع الجغرافي — الدولة أو القارة أو العالم. مع دوران تلقائي كل 8 ثوانٍ وتنسيقات محسّنة لسطح المكتب والجوال، توفر اللافتات رؤية قابلة للقياس للمعلنين الإقليميين والدوليين.",
        "banners_tabela": [
            ["التقسيم", "ثابت (﷼/شهر)", "مؤقت (﷼/شهر)", "ملف المعلن"],
            ["دولة", "﷼ 800", "﷼ 500", "شركات محلية صغيرة، تجارة إقليمية"],
            ["قارة", "﷼ 1,800", "﷼ 1,200", "علامات إقليمية، توسع قاري"],
            ["العالم", "﷼ 3,500", "﷼ 2,500", "شركات عالمية، تطبيقات دولية"],
            ["رعاية حصرية", "﷼ 6,000", "﷼ 4,500/حملة", "رعاة رئيسيون، إطلاقات"],
        ],
        "banners_formatos": "728×90 بكسل — لافتة سطح المكتب المركزية · 320×100 بكسل — تنسيق جوال محسّن · 8 ثوانٍ — دوران تلقائي · استهداف جغرافي — دولة أو قارة أو نطاق عالمي",
        "b2b_titulo": "حزم B2B المؤسسية — قيمة عالية، حجم كبير",
        "b2b_texto": "تحول حزم B2B A1ELOS إلى أداة للعلامة التجارية لصاحب العمل والعافية المؤسسية. تشتري الشركات رموز الوصول بكميات كبيرة لتوزيعها كهدايا على الموظفين أو العملاء — مدعومة بـ DUNS 942242668 للعقود المؤسسية الرسمية.",
        "b2b_planos": [
            ("الخطة الأساسية · 50 رمزًا", "50× خريطة إكسبرس (﷼ 35 لكل منها). مثالية لبرامج عافية الموظفين وإجراءات الإعداد."),
            ("الخطة المتوسطة · 100 رمز", "50× إكسبرس + 50× بحث AI (﷼ 71). مثالية للموارد البشرية واستراتيجيات العلامة التجارية لصاحب العمل."),
            ("الخطة المميزة · 200 رمز", "100× إكسبرس + 100× خريطة كاملة (﷼ 71). أقصى عمق تحليلي للفرق الكبيرة."),
        ],
        "b2b_tabela": [
            ["من", "الخصم", "الملف", "الاستخدام الموصى به"],
            ["10 رموز", "10%", "فرق صغيرة", "إجراء عافية محدد"],
            ["100 رمز", "30%", "شركات صغيرة", "برنامج مزايا ربع سنوي"],
            ["500 رمز", "50%", "شركات متوسطة", "هدية سنوية للموظفين"],
            ["1,000 رمز", "70%", "شركات كبيرة", "برنامج ولاء العملاء"],
        ],
        "projecoes_titulo": "التوقعات المالية: أفق 50 عامًا",
        "projecoes_texto": "بُنيت التوقعات على سيناريوهين — متحفظ ومتفائل — يعكسان معدلات اختراق سوق مختلفة وسرعة توسع B2B ونموًا عضويًا لكل لغة.",
        "projecoes_tabela": [
            ["الأفق", "متحفظ (﷼)", "متفائل (﷼)"],
            ["السنة 1", "﷼ 600 ألف", "﷼ 2.4 مليون"],
            ["السنة 3", "﷼ 2.2 مليون", "﷼ 8.4 مليون"],
            ["السنة 5", "﷼ 9.4 مليون", "﷼ 28 مليون"],
            ["السنة 10", "﷼ 56 مليون", "﷼ 150 مليون"],
            ["السنة 20", "﷼ 280 مليون", "﷼ 750 مليون"],
            ["السنة 30", "﷼ 650 مليون", "﷼ 1.68 مليار"],
            ["السنة 40", "﷼ 1.03 مليار", "﷼ 2.8 مليار"],
            ["السنة 50", "﷼ 1.4 مليار", "﷼ 4.68 مليار"],
        ],
        "tracao_titulo": "الزخم والنتائج المثبتة",
        "tracao_texto": "يعمل A1ELOS بالفعل بمقاييس منتج تثبت النموذج — الاحتفاظ المرتفع والتقييم المميز وقاعدة متنامية من شركاء B2B تثبت أن المنصة تقدم قيمة حقيقية للمستخدم النهائي والسوق المؤسسي.",
        "tracao_kpis": [
            ("12K+", "مستخدم نشط", "قاعدة نمو عضوي ثابتة"),
            ("87%", "الاحتفاظ", "أعلى بكثير من متوسط الصناعة (~30%)"),
            ("4.8★", "متوسط التقييم", "رضا مثبت للمستخدم النهائي"),
            ("23", "شريك B2B", "عقود نشطة مع الشركات والموارد البشرية"),
        ],
        "roteiro_titulo": "خارطة الطريق الاستراتيجية",
        "roteiro_texto": "ينفذ A1ELOS خطة في أربع مراحل تصاعدية — من توحيد القاعدة الحالية إلى الريادة العالمية في السوق، مع خيارات خروج واضحة للمستثمرين.",
        "roteiro_fases": [
            ("المرحلة 1 · التوحيد", "تعزيز قاعدة المستخدمين في اللغات النشطة بالفعل. تحسين التحويل والاحتفاظ وLTV. اكتملت جولة البذرة."),
            ("المرحلة 2 · التوسع", "الإطلاق الرسمي في الأسواق الثلاثة الجديدة: إندونيسيا وتركيا وفيتنام. تسريع قناة B2B والإعلانات الجغرافية."),
            ("المرحلة 3 · الدخول العالمي", "حضور نشط في جميع اللغات الـ14 بحملات محلية. شراكات العلامة البيضاء في 5+ قارات. السلسلة A."),
            ("المرحلة 4 · الريادة", "أكثر من 20 دولة بعمليات موحدة. منصة SaaS مرجعية عالمية في علم الأرقام التطبيقي. إدراج أو خروج استراتيجي."),
        ],
        "invest_titulo": "الاستثمار والتواصل",
        "invest_texto": "نحن جاهزون للعروض الخاصة والعناية الواجبة والمفاوضات. تواصل معنا عبر القناة المفضلة لديك.",
        "invest_dados": [
            ("جولة البذرة", "﷼ 350 ألف"),
            ("التقييم قبل المال", "﷼ 1.4 مليون"),
            ("الحصة المعروضة", "حتى 20%"),
        ],
        "invest_contato": [
            ("بريد المستثمرين", "a1elos.consultoria@gmail.com"),
            ("البريد العام", "contato@a1elos.com"),
            ("الموقع", "www.a1elos.com"),
            ("DUNS", "942242668 — Dun & Bradstreet"),
        ],
        "invest_alocacao": "تخصيص رأس المال: 45% تقنية · 30% تسويق · 25% عمليات",
        "frase_final": "الأرقام لا تكذب أبدًا.",
        "selo_final": ["DUNS 942242668", "23 منتجًا", "14 لغة", "~5.3 مليار متحدث"],
        "graf_cons": "محافظ",
        "graf_otim": "متفائل",
        "grafico_titulo_linha": "النمو المتوقع (آلاف ر.س)",
    },

    "id": {
        "titulo": "A1ELOS Numerologi Global",
        "subtitulo": "Ilmu angka yang diterapkan untuk kesuksesan Anda",
        "capa_nota": "Presentasi Strategis untuk Investor dan Mitra",
        "confidencial": "RAHASIA",
        "ano": "2026",
        "sumario_intro": "Presentasi ini disusun untuk memandu investor dan mitra melalui semua aspek strategis A1ELOS Numerologi Global — dari tesis pasar hingga model pendapatan berulang.",
        "sumario_cards": [
            ("01", "Tentang A1ELOS", "Holding, portofolio dan kredensial DUNS"),
            ("02", "Peluang Pasar", "Ekonomi kesejahteraan global US$ 6,8 triliun"),
            ("03", "Solusi dan Jangkauan Global", "14 bahasa, ~5,3 miliar penutur"),
            ("04", "3 Pasar Baru", "Indonesia, Turki dan Vietnam"),
            ("05", "Portofolio dan Harga", "23 produk dikalibrasi berdasarkan daya beli"),
            ("06", "Pendapatan Berulang", "Banner iklan dan Paket B2B"),
            ("07", "Proyeksi dan Investasi", "Cakrawala 50 tahun · Putaran Seed Rp 11 miliar"),
        ],
        "sobre_titulo": "Tentang A1ELOS",
        "sobre_texto": "A1ELOS adalah holding teknologi dan pengetahuan yang menyatukan kecerdasan buatan, numerologi terapan dan strategi budaya untuk menciptakan produk digital berdampak tinggi dalam skala global. Misi kami: mendemokratisasi pengetahuan diri numerik dengan rasa hormat budaya dan rasa hormat terhadap daya beli setiap pasar.",
        "sobre_kpis": [
            ("23", "Produk Aktif", "Dalam 4 tingkat akses"),
            ("14", "Bahasa", "~67% populasi dunia"),
            ("5,3B", "Penutur", "Pasar nyata yang dapat dijangkau"),
            ("AI", "Terintegrasi", "Mesin personalisasi"),
        ],
        "sobre_duns": "DUNS 942242668 — Sertifikasi Dun & Bradstreet berlaku di 190+ negara, memungkinkan kontrak B2B dan usaha patungan internasional.",
        "duns_titulo": "Kredibilitas Internasional",
        "duns_texto": "Nomor DUNS adalah paspor korporat A1ELOS di kancah internasional. Ini memberi sinyal kepada mitra, klien korporat dan investor bahwa perusahaan memiliki identitas terverifikasi, sejarah yang dapat dilacak dan kapasitas kontraktual di yurisdiksi mana pun.",
        "duns_numero": "942242668",
        "duns_emitido": "Diterbitkan oleh Dun & Bradstreet — standar global identitas perusahaan yang diakui di lebih dari 190 negara.",
        "duns_paises": "190+ NEGARA",
        "duns_beneficios": [
            ("Kontrak B2B", "Kualifikasi untuk tender dan pemasok global"),
            ("Usaha Patungan", "Kemitraan internasional dengan uji tuntas yang difasilitasi"),
            ("Kredibilitas Segera", "Tanda keseriusan bagi investor institusional"),
        ],
        "mercado_titulo": "Peluang Pasar",
        "mercado_texto": "Kita hidup dalam konvergensi sempurna: kesejahteraan digital meledak secara global sementara numerologi dan astrologi bermigrasi ke aplikasi dengan keterlibatan tinggi. A1ELOS diposisikan tepat di persimpangan ini, dengan 74% populasi dunia sudah online (~6 miliar orang).",
        "mercado_cards": [
            ("Kesejahteraan Global", "US$ 6,8 T → US$ 9,8 T pada 2029 (+7,6%/tahun)"),
            ("Aplikasi Astrologi/Numerologi", "US$ 3 M → US$ 9 M pada 2030 · CAGR 20%"),
            ("Aplikasi Kesejahteraan", "CAGR 14,9% → US$ 26,2 M pada 2030"),
            ("Pengguna Online", "74% dunia · ~6 miliar orang"),
        ],
        "problema_titulo": "Masalah yang Kami Selesaikan",
        "problema_col_esq_titulo": "Kegagalan Pasar Saat Ini",
        "problema_col_esq": [
            ("Hambatan Bahasa", "Mayoritas besar alat numerologi hanya beroperasi dalam bahasa Inggris, mengecualikan miliaran penutur asli dalam bahasa lain."),
            ("Harga Terlepas dari Realitas", "Produk yang ditagih dalam dolar untuk pasar berkembang menciptakan eksklusi ekonomi — pengguna tidak menolak produk, tetapi menolak harga yang tidak terjangkau."),
            ("Kurangnya Kedalaman", "Alat generik memberikan jawaban dangkal tanpa personalisasi, tanpa konteks budaya dan tanpa aplikasi praktis dalam kehidupan sehari-hari."),
        ],
        "problema_col_dir_titulo": "Biaya Eksklusi",
        "problema_col_dir": "Ketika platform mengabaikan bahasa dan daya beli, ia secara sukarela meninggalkan pasar terbesar di dunia: 4+ miliar orang yang hidup di ekonomi berkembang dan berbicara bahasa non-Inggris. Ini adalah celah yang A1ELOS isi dengan presisi bedah.",
        "problema_destaque": "Platform yang mengabaikan daya beli lokal kehilangan akses ke lebih dari 60% pasar global yang dapat dijangkau.",
        "solucao_titulo": "Solusi Kami: 3 Pilar Strategis",
        "solucao_texto": "A1ELOS membangun platform terintegrasi yang menggabungkan ilmu numerik, kecerdasan buatan dan kepekaan budaya. Solusi beroperasi di tiga lini komplementer, menjamin pendapatan terdiversifikasi dan retensi tinggi.",
        "solucao_colunas": [
            ("Peta Pribadi", "Analisis numerik mendalam dan personal untuk pengguna akhir — identitas, misi, siklus hidup dan kompatibilitas — disampaikan dalam 14 bahasa dengan AI terintegrasi."),
            ("Numerologi Bisnis", "Diagnosis numerologi yang diterapkan pada merek, CNPJ, tanggal pendirian dan strategi korporat. Produk terdiferensiasi dengan nilai persepsi tinggi di pasar B2B."),
            ("White-Label B2B", "Lisensi platform untuk perusahaan mitra yang ingin menawarkan numerologi di bawah merek mereka sendiri — dengan dukungan multibahasa dan kustomisasi lengkap."),
        ],
        "alcance_titulo": "Jangkauan Global: 14 Bahasa · ~5,3 Miliar Penutur",
        "alcance_texto": "A1ELOS mencakup ~67% populasi dunia dengan platform yang benar-benar multibahasa. Setiap bahasa mewakili pasar budaya yang berbeda, dengan harga dikalibrasi ke daya beli lokal.",
        "mercados_titulo": "3 Pasar Baru: +442 Juta Penutur",
        "mercados_texto": "Ekspansi strategis ke Indonesia, Turki dan Vietnam mewakili lompatan kualitatif: pasar dengan pertumbuhan ekonomi tinggi, penetrasi digital yang meningkat dan permintaan terbukti akan solusi kesejahteraan digital yang terjangkau.",
        "mercados_cards": [
            ("Indonesia", ["285 juta penduduk", "80,5% penetrasi internet", "~255 juta penutur bahasa Indonesia", "Kesejahteraan: US$ 51,2 M (2025) → US$ 72,8 M (2034)"]),
            ("Turki", ["85,9 juta penduduk", "PDB PPP per kapita US$ 37.301", "~90 juta penutur bahasa Turki", "Di atas rata-rata dunia (US$ 27.211)"]),
            ("Vietnam",  ["~100 juta penduduk", "PDB per kapita ~US$ 5.066 (+7,4%/tahun)", "~97 juta penutur bahasa Vietnam", "Kesejahteraan: US$ 303 juta (2025) → US$ 485 juta (2030)"]),
        ],
        "mercados_rodape": "3 pasar baru = +442 juta penutur baru yang dapat dijangkau — diintegrasikan ke platform dengan harga yang dikalibrasi secara budaya.",
        "preco_titulo": "Filosofi Harga Sadar",
        "preco_esq": "Rasa hormat budaya + rasa hormat terhadap daya beli = pasar nyata yang dapat dijangkau. Proporsi nilai yang sama. Harga berbeda. Martabat setara untuk semua pasar.",
        "preco_dir_titulo": "Cara Kerjanya dalam Praktik",
        "preco_dir": "A1ELOS menerapkan Paritas Daya Beli (PPP) sebagai kriteria penetapan harga sentral. Produk yang sama memberikan nilai relatif yang sama kepada pengguna di Lagos, Jakarta, Hanoi atau New York — harga dikalibrasi sehingga upaya finansial proporsional dengan pendapatan lokal.",
        "preco_pilares": [
            ("Kalibrasi PPP", "Harga disesuaikan dengan indeks daya beli setiap negara"),
            ("Rasa Hormat Budaya", "Bahasa, mata uang dan konteks lokal terintegrasi ke produk"),
            ("Konversi Unggul", "Harga adil menghasilkan lebih banyak konversi dan retensi jangka panjang yang lebih besar"),
        ],
        "portfolio_titulo": "Portofolio: 23 Produk dalam 4 Tingkat",
        "portfolio_texto": "Struktur berlapis memastikan setiap profil pengguna — dari yang penasaran hingga profesional — menemukan penawaran yang sesuai dengan tingkat keterlibatan dan kapasitas finansialnya.",
        "portfolio_tabela": [
            ["Tingkat", "Produk", "Kisaran Harga (Rp)", "Profil"],
            ["Pemula", "Peta Ekspres, Konsultasi Cepat", "Rp 11.000", "Penasaran, kontak pertama"],
            ["Menengah", "Riset AI, Peta Lengkap, Kompatibilitas", "Rp 23.000", "Pengguna terlibat"],
            ["Lanjutan", "Numerologi Bisnis, Siklus, Misi", "Rp 36.000–48.000", "Profesional, wirausaha"],
            ["Premium", "Diagnosis Lengkap, White-Label Pribadi", "Rp 60.000–134.000", "Pendapatan tinggi, penggunaan korporat"],
            ["B2B / Korporat", "Paket bisnis, lisensi, hadiah", "Sesuai permintaan", "Perusahaan dan HR"],
        ],
        "portfolio_rodape": "23 produk mencakup seluruh perjalanan pengguna, dari kontak pertama hingga pelanggan premium berulang — memaksimalkan LTV per bahasa dan pasar.",
        "negocio_titulo": "Model Bisnis: 3 Sumber Pendapatan",
        "negocio_texto": "A1ELOS dirancang dengan pendapatan yang terdiversifikasi dan skalabel: penjualan langsung ke konsumen akhir dalam skala global, kontrak B2B bernilai tinggi dan iklan geolokasi berulang — tiga mesin yang saling mengisi.",
        "negocio_colunas": [
            ("B2C — 14 Bahasa", "Penjualan langsung produk digital dalam semua mata uang, dengan harga disesuaikan oleh PPP. Skala otomatis via AI — tanpa tim dukungan yang proporsional dengan pertumbuhan."),
            ("B2B — Diskon Progresif", "Paket korporat untuk HR, employer branding dan hadiah institusional. Diskon 10% hingga 70% sesuai volume. Kontrak didukung DUNS 942242668."),
            ("Iklan Geolokasi", "Banner disegmentasi per negara, benua atau dunia dengan rotasi otomatis. Pendapatan bulanan berulang bernilai tinggi — tanpa ketergantungan pada volume penjualan produk."),
        ],
        "banners_titulo": "Banner Iklan — Pendapatan Bulanan Berulang",
        "banners_texto": "Platform A1ELOS menawarkan ruang iklan premium dengan segmentasi presisi berdasarkan geolokasi — negara, benua atau dunia. Dengan rotasi otomatis setiap 8 detik dan format yang dioptimalkan untuk desktop dan mobile, banner memberikan visibilitas terukur kepada pengiklan regional dan internasional.",
        "banners_tabela": [
            ["Segmentasi", "Tetap (Rp/bulan)", "Sementara (Rp/bulan)", "Profil Pengiklan"],
            ["Negara", "Rp 800.000", "Rp 500.000", "UMKM lokal, perdagangan regional"],
            ["Benua", "Rp 1.800.000", "Rp 1.200.000", "Merek regional, ekspansi benua"],
            ["Dunia", "Rp 3.500.000", "Rp 2.500.000", "Perusahaan global, aplikasi internasional"],
            ["Sponsor Eksklusif", "Rp 6.000.000", "Rp 4.500.000/kampanye", "Sponsor utama, peluncuran"],
        ],
        "banners_formatos": "728×90 px — Banner desktop pusat · 320×100 px — Format mobile dioptimalkan · 8 detik — Rotasi otomatis · Geo-target — Negara, benua atau jangkauan dunia",
        "b2b_titulo": "Paket Korporat B2B — Nilai Tinggi, Volume Tinggi",
        "b2b_texto": "Paket B2B mengubah A1ELOS menjadi alat employer branding dan kesejahteraan korporat. Perusahaan membeli kode akses dalam volume untuk didistribusikan sebagai hadiah kepada karyawan atau klien — didukung DUNS 942242668 untuk kontrak korporat formal.",
        "b2b_planos": [
            ("Paket Dasar · 50 Kode", "50× Peta Ekspres (Rp 11.000 masing-masing). Ideal untuk program kesejahteraan karyawan dan aksi onboarding."),
            ("Paket Menengah · 100 Kode", "50× Ekspres + 50× Riset AI (Rp 23.000). Sempurna untuk HR dan strategi employer branding."),
            ("Paket Premium · 200 Kode", "100× Ekspres + 100× Peta Lengkap (Rp 23.000). Kedalaman analitis maksimal untuk tim besar."),
        ],
        "b2b_tabela": [
            ["Dari", "Diskon", "Profil", "Penggunaan yang Direkomendasikan"],
            ["10 kode", "10%", "Tim kecil", "Aksi kesejahteraan sekali waktu"],
            ["100 kode", "30%", "UKM", "Program tunjangan triwulanan"],
            ["500 kode", "50%", "Perusahaan menengah", "Hadiah tahunan karyawan"],
            ["1.000 kode", "70%", "Korporasi besar", "Program loyalitas pelanggan"],
        ],
        "projecoes_titulo": "Proyeksi Keuangan: Cakrawala 50 Tahun",
        "projecoes_texto": "Proyeksi dibangun pada dua skenario — konservatif dan optimistis — mencerminkan tingkat penetrasi pasar yang berbeda, kecepatan ekspansi B2B dan pertumbuhan organik per bahasa.",
        "projecoes_tabela": [
            ["Cakrawala", "Konservatif (Rp)", "Optimistis (Rp)"],
            ["Tahun 1", "Rp 600 juta", "Rp 2,4 miliar"],
            ["Tahun 3", "Rp 2,2 miliar", "Rp 8,4 miliar"],
            ["Tahun 5", "Rp 9,4 miliar", "Rp 28 miliar"],
            ["Tahun 10", "Rp 56 miliar", "Rp 150 miliar"],
            ["Tahun 20", "Rp 280 miliar", "Rp 750 miliar"],
            ["Tahun 30", "Rp 650 miliar", "Rp 1,68 triliun"],
            ["Tahun 40", "Rp 1,03 triliun", "Rp 2,8 triliun"],
            ["Tahun 50", "Rp 1,4 triliun", "Rp 4,68 triliun"],
        ],
        "tracao_titulo": "Traction dan Hasil Terbukti",
        "tracao_texto": "A1ELOS sudah beroperasi dengan metrik produk yang memvalidasi model — retensi tinggi, peringkat premium dan basis mitra B2B yang berkembang menunjukkan bahwa platform memberikan nilai nyata kepada pengguna akhir dan pasar korporat.",
        "tracao_kpis": [
            ("12K+", "Pengguna Aktif", "Basis pertumbuhan organik yang konsisten"),
            ("87%", "Retensi", "Jauh di atas rata-rata industri (~30%)"),
            ("4,8★", "Peringkat Rata-rata", "Kepuasan pengguna akhir yang terbukti"),
            ("23", "Mitra B2B", "Kontrak aktif dengan perusahaan dan HR"),
        ],
        "roteiro_titulo": "Peta Jalan Strategis",
        "roteiro_texto": "A1ELOS menjalankan rencana dalam empat fase progresif — dari konsolidasi basis saat ini hingga kepemimpinan pasar global, dengan opsi keluar yang jelas bagi investor.",
        "roteiro_fases": [
            ("Fase 1 · Konsolidasi", "Memperkuat basis pengguna di bahasa yang sudah aktif. Mengoptimalkan konversi, retensi dan LTV. Putaran Seed selesai."),
            ("Fase 2 · Ekspansi", "Peluncuran resmi di 3 pasar baru: Indonesia, Turki dan Vietnam. Akselerasi kanal B2B dan iklan geolokasi."),
            ("Fase 3 · Masuk Global", "Kehadiran aktif di semua 14 bahasa dengan kampanye terlokalisasi. Kemitraan white-label di 5+ benua. Seri A."),
            ("Fase 4 · Kepemimpinan", "20+ negara dengan operasi terkonsolidasi. Platform SaaS referensi global dalam numerologi terapan. IPO atau keluar strategis."),
        ],
        "invest_titulo": "Investasi & Kontak",
        "invest_texto": "Kami siap untuk presentasi privat, uji tuntas dan negosiasi. Hubungi kami melalui kanal pilihan Anda.",
        "invest_dados": [
            ("Putaran Seed", "Rp 11 miliar"),
            ("Valuasi Pre-Money", "Rp 44 miliar"),
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
        "selo_final": ["DUNS 942242668", "23 PRODUK", "14 BAHASA", "~5,3 M PENUTUR"],
        "graf_cons": "Konservatif",
        "graf_otim": "Optimis",
        "grafico_titulo_linha": "Pertumbuhan Diproyeksikan (Rp ribu)",
    },

        "tr": {
        "titulo": "A1ELOS Küresel Numeroloji",
        "subtitulo": "Sayıların bilimi başarınıza uygulandı",
        "capa_nota": "Yatırımcılar ve Ortaklar için Stratejik Sunum",
        "confidencial": "GİZLİ",
        "ano": "2026",
        "sumario_intro": "Bu sunum, yatırımcıları ve ortakları A1ELOS Küresel Numerolojinin tüm stratejik yönleri boyunca yönlendirmek için yapılandırılmıştır — pazar tezinden tekrarlayan gelir modeline kadar.",
        "sumario_cards": [
            ("01", "A1ELOS Hakkında", "Holding, portföy ve DUNS kimlik bilgisi"),
            ("02", "Pazar Fırsatı", "Küresel sağlıklı yaşam ekonomisi US$ 6,8 trilyon"),
            ("03", "Çözüm ve Küresel Erişim", "14 dil, ~5,3 milyar konuşmacı"),
            ("04", "3 Yeni Pazar", "Endonezya, Türkiye ve Vietnam"),
            ("05", "Portföy ve Fiyatlar", "Satın alma gücüne göre kalibre edilmiş 23 ürün"),
            ("06", "Tekrarlayan Gelir", "Reklam bannerları ve B2B Paketleri"),
            ("07", "Projeksiyonlar ve Yatırım", "50 yıllık ufuk · Tohum Turu TL 580 bin"),
        ],
        "sobre_titulo": "A1ELOS Hakkında",
        "sobre_texto": "A1ELOS, küresel ölçekte yüksek etkili dijital ürünler yaratmak için yapay zekayı, uygulamalı numerolojiyi ve kültürel stratejiyi birleştiren bir teknoloji ve bilgi holdingidir. Misyonumuz: kültürel saygı ve her pazarın satın alma gücüne saygı ile sayısal öz-bilgiyi demokratikleştirmek.",
        "sobre_kpis": [
            ("23", "Aktif Ürün", "4 erişim seviyesinde"),
            ("14", "Dil", "Dünya nüfusunun ~%67'si"),
            ("5,3B", "Konuşmacı", "Gerçek erişilebilir pazar"),
            ("Yapay Zeka", "Entegre", "Kişiselleştirme motoru"),
        ],
        "sobre_duns": "DUNS 942242668 — Dun & Bradstreet sertifikası 190+ ülkede geçerlidir, B2B sözleşmelerini ve uluslararası ortak girişimleri mümkün kılar.",
        "duns_titulo": "Uluslararası Güvenilirlik",
        "duns_texto": "DUNS numarası, A1ELOS'un uluslararası sahnedeki kurumsal pasaportudur. Ortaklara, kurumsal müşterilere ve yatırımcılara şirketin doğrulanabilir kimliğe, izlenebilir geçmişe ve her yargı bölgesinde sözleşme kapasitesine sahip olduğunu gösterir.",
        "duns_numero": "942242668",
        "duns_emitido": "Dun & Bradstreet tarafından verilmiştir — 190'dan fazla ülkede tanınan küresel kurumsal kimlik standardı.",
        "duns_paises": "190+ ÜLKE",
        "duns_beneficios": [
            ("B2B Sözleşmeleri", "Küresel ihaleler ve tedarikçiler için yetkilendirme"),
            ("Ortak Girişimler", "Kolaylaştırılmış durum tespiti ile uluslararası ortaklıklar"),
            ("Anında Güvenilirlik", "Kurumsal yatırımcılar için ciddiyet işareti"),
        ],
        "mercado_titulo": "Pazar Fırsatı",
        "mercado_texto": "Mükemmel yakınsamayı yaşıyoruz: dijital sağlıklı yaşam küresel olarak patlarken numeroloji ve astroloji yüksek etkileşimli uygulamalara taşınıyor. A1ELOS tam bu kesişim noktasında konumlanmıştır; dünya nüfusunun %74'ü zaten çevrimiçidir (~6 milyar insan).",
        "mercado_cards": [
            ("Küresel Sağlıklı Yaşam", "US$ 6,8 T → 2029'da US$ 9,8 T (+%7,6/yıl)"),
            ("Astroloji/Numeroloji Uygulamaları", "US$ 3 M → 2030'da US$ 9 M · Bileşik %20"),
            ("Sağlıklı Yaşam Uygulamaları", "Bileşik %14,9 → 2030'da US$ 26,2 M"),
            ("Çevrimiçi Kullanıcılar", "Dünyanın %74'ü · ~6 milyar insan"),
        ],
        "problema_titulo": "Çözdüğümüz Sorun",
        "problema_col_esq_titulo": "Mevcut Pazarın Eksiklikleri",
        "problema_col_esq": [
            ("Dil Engeli", "Numeroloji araçlarının büyük çoğunluğu yalnızca İngilizce çalışır ve diğer dillerdeki milyarlarca anadil konuşmacısını dışlar."),
            ("Gerçeklikten Kopuk Fiyatlar", "Gelişmekte olan pazarlar için dolar cinsinden faturalanan ürünler ekonomik dışlanma yaratır — kullanıcı ürünü değil, erişilemeyen fiyatı reddeder."),
            ("Derinlik Eksikliği", "Jenerik araçlar, kişiselleştirme olmadan, kültürel bağlam olmadan ve günlük hayata pratik uygulama olmadan yüzeysel yanıtlar sunar."),
        ],
        "problema_col_dir_titulo": "Dışlanmanın Bedeli",
        "problema_col_dir": "Bir platform dili ve satın alma gücünü görmezden geldiğinde, dünyanın en büyük pazarını gönüllü olarak terk eder: gelişmekte olan ekonomilerde yaşayan ve İngilizce dışı dilleri konuşan 4+ milyar insan. A1ELOS'un cerrahi hassasiyetle doldurduğu boşluk budur.",
        "problema_destaque": "Yerel satın alma gücünü görmezden gelen platformlar, küresel erişilebilir pazarın %60'ından fazlasına erişimi kaybeder.",
        "solucao_titulo": "Çözümümüz: 3 Stratejik Sütun",
        "solucao_texto": "A1ELOS, sayısal bilimi, yapay zekayı ve kültürel duyarlılığı birleştiren entegre bir platform kurmuştur. Çözüm, çeşitlendirilmiş gelir ve yüksek tutma oranı sağlayan üç tamamlayıcı cephede çalışır.",
        "solucao_colunas": [
            ("Kişisel Haritalar", "Son kullanıcı için derin ve kişiselleştirilmiş sayısal analizler — kimlik, misyon, yaşam döngüleri ve uyumluluk — entegre yapay zeka ile 14 dilde sunulur."),
            ("Kurumsal Numeroloji", "Markalara, CNPJ'lere, kuruluş tarihlerine ve kurumsal stratejiye uygulanan numerolojik teşhisler. B2B pazarında yüksek algılanan değere sahip farklılaştırılmış ürün."),
            ("White-Label B2B", "Numerolojiyi kendi markaları altında sunmak isteyen ortak şirketler için platform lisanslama — çok dilli destek ve tam kişiselleştirme ile."),
        ],
        "alcance_titulo": "Küresel Erişim: 14 Dil · ~5,3 Milyar Konuşmacı",
        "alcance_texto": "A1ELOS, gerçekten çok dilli bir platformla dünya nüfusunun ~%67'sini kapsar. Her dil, yerel satın alma gücüne göre kalibre edilmiş fiyatlarla ayrı bir kültürel pazarı temsil eder.",
        "mercados_titulo": "3 Yeni Pazar: +442 Milyon Konuşmacı",
        "mercados_texto": "Endonezya, Türkiye ve Vietnam'a stratejik genişleme niteliksel bir sıçramayı temsil eder: yüksek ekonomik büyümeye, artan dijital nüfuza ve erişilebilir dijital sağlıklı yaşam çözümlerine kanıtlanmış talebe sahip pazarlar.",
        "mercados_cards": [
            ("Endonezya", ["285 milyon nüfus", "%80,5 internet nüfuzu", "~255 milyon Endonezce konuşan", "Sağlıklı yaşam: US$ 51,2 M (2025) → US$ 72,8 M (2034)"]),
            ("Türkiye", ["85,9 milyon nüfus", "Kişi başı SGP GSYİH US$ 37.301", "~90 milyon Türkçe konuşan", "Dünya ortalamasının üzerinde (US$ 27.211)"]),
            ("Vietnam",  ["~100 milyon nüfus", "Kişi başı GSYİH ~US$ 5.066 (+%7,4/yıl)", "~97 milyon Vietnamca konuşan", "Sağlıklı yaşam: US$ 303 M (2025) → US$ 485 M (2030)"]),
        ],
        "mercados_rodape": "3 yeni pazar = +442 milyon yeni erişilebilir konuşmacı — kültürel olarak kalibre edilmiş fiyatlarla platforma entegre edildi.",
        "preco_titulo": "Bilinçli Fiyatlandırma Felsefesi",
        "preco_esq": "Kültürel saygı + satın alma gücüne saygı = gerçek erişilebilir pazar. Aynı değer oranı. Farklı fiyatlar. Tüm pazarlar için eşit saygınlık.",
        "preco_dir_titulo": "Pratikte Nasıl Çalışır",
        "preco_dir": "A1ELOS, merkezi fiyatlandırma kriteri olarak Satın Alma Gücü Paritesini (PPP) uygular. Aynı ürün, Lagos, Jakarta, Hanoi veya New York'taki kullanıcıya aynı göreli değeri sunar — fiyat, finansal çaba yerel gelirle orantılı olacak şekilde kalibre edilir.",
        "preco_pilares": [
            ("PPP Kalibrasyonu", "Fiyatlar her ülkenin satın alma gücü endeksine göre ayarlanır"),
            ("Kültürel Saygı", "Dil, para birimi ve yerel bağlam ürüne entegre edilir"),
            ("Üstün Dönüşüm", "Adil fiyat daha fazla dönüşüm ve daha yüksek uzun vadeli tutma sağlar"),
        ],
        "portfolio_titulo": "Portföy: 4 Seviyede 23 Ürün",
        "portfolio_texto": "Katmanlı yapı, her kullanıcı profilin — meraklıdan profesyonele — katılım düzeyine ve finansal kapasitesine uygun bir teklif bulmasını sağlar.",
        "portfolio_tabela": [
            ["Seviye", "Ürünler", "Fiyat Aralığı (TL)", "Profil"],
            ["Giriş", "Ekspres Harita, Hızlı Danışma", "TL 58", "Meraklı, ilk temas"],
            ["Orta", "AI Araştırma, Tam Harita, Uyumluluk", "TL 123", "Etkileşimli kullanıcı"],
            ["İleri", "İş Numerolojisi, Döngüler, Misyon", "TL 188–254", "Profesyonel, girişimci"],
            ["Premium", "Tam Teşhis, Kişisel White-Label", "TL 319–710", "Yüksek gelir, kurumsal kullanım"],
            ["B2B / Kurumsal", "Kurumsal paketler, lisanslar, hediyeler", "Talebe göre", "Şirketler ve İK"],
        ],
        "portfolio_rodape": "23 ürün, ilk temastan tekrarlayan premium müşteriye kadar kullanıcı yolculuğunun tamamını kapsar — dil ve pazara göre LTV'yi maksimize eder.",
        "negocio_titulo": "İş Modeli: 3 Gelir Kaynağı",
        "negocio_texto": "A1ELOS, çeşitlendirilmiş ve ölçeklenebilir gelirle tasarlanmıştır: küresel ölçekte son tüketiciye doğrudan satış, yüksek değerli B2B sözleşmeleri ve tekrarlayan coğrafi hedefli reklam — birbirini besleyen üç motor.",
        "negocio_colunas": [
            ("B2C — 14 Dil", "Tüm para birimlerinde dijital ürünlerin doğrudan satışı, PPP ile uyarlanmış fiyatlandırma. AI ile otomatik ölçekleme — büyümeyle orantılı destek ekibi olmadan."),
            ("B2B — Kademeli İndirimler", "İK, işveren markası ve kurumsal hediyeler için kurumsal paketler. Hacme göre %10'dan %70'e indirim. DUNS 942242668 ile desteklenen sözleşmeler."),
            ("Coğrafi Hedefli Reklam", "Ülkeye, kıtaya veya dünyaya göre bölümlenmiş, otomatik rotasyonlu bannerlar. Ürün satış hacmine bağımlılık olmadan yüksek değerli tekrarlayan aylık gelir."),
        ],
        "banners_titulo": "Reklam Bannerları — Aylık Tekrarlayan Gelir",
        "banners_texto": "A1ELOS platformu, coğrafi konuma göre hassas bölümleme ile premium reklam alanları sunar — ülke, kıta veya dünya. Her 8 saniyede otomatik rotasyon ve masaüstü ile mobil için optimize edilmiş formatlarla, bannerlar bölgesel ve uluslararası reklamverenlere ölçülebilir görünürlük sağlar.",
        "banners_tabela": [
            ["Bölümleme", "Sabit (TL/ay)", "Geçici (TL/ay)", "Reklamveren Profili"],
            ["Ülke", "TL 800", "TL 500", "Yerel KOBİ'ler, bölgesel ticaret"],
            ["Kıta", "TL 1.800", "TL 1.200", "Bölgesel markalar, kıta genişlemesi"],
            ["Dünya", "TL 3.500", "TL 2.500", "Küresel şirketler, uluslararası uygulamalar"],
            ["Özel Sponsorluk", "TL 6.000", "TL 4.500/kampanya", "Ana sponsorlar, lansmanlar"],
        ],
        "banners_formatos": "728×90 px — Merkezi masaüstü banner · 320×100 px — Optimize edilmiş mobil format · 8 saniye — Otomatik rotasyon · Coğrafi hedefleme — Ülke, kıta veya dünya çapında erişim",
        "b2b_titulo": "B2B Kurumsal Paketler — Yüksek Değer, Yüksek Hacim",
        "b2b_texto": "B2B Paketleri A1ELOS'u bir işveren markası ve kurumsal sağlıklı yaşam aracına dönüştürür. Şirketler, çalışanlara veya müşterilere hediye olarak dağıtmak üzere erişim kodlarını toplu olarak satın alır — resmi kurumsal sözleşmeler için DUNS 942242668 ile desteklenir.",
        "b2b_planos": [
            ("Temel Plan · 50 Kod", "50× Ekspres Harita (her biri TL 58). Çalışan sağlıklı yaşam programları ve işe alım eylemleri için idealdir."),
            ("Orta Plan · 100 Kod", "50× Ekspres + 50× AI Araştırma (TL 123). İK ve işveren markası stratejileri için mükemmeldir."),
            ("Premium Plan · 200 Kod", "100× Ekspres + 100× Tam Harita (TL 123). Büyük ekipler için maksimum analitik derinlik."),
        ],
        "b2b_tabela": [
            ["Başlangıç", "İndirim", "Profil", "Önerilen Kullanım"],
            ["10 kod", "%10", "Küçük ekipler", "Tek seferlik sağlıklı yaşam eylemi"],
            ["100 kod", "%30", "KOBİ'ler", "Üç aylık yan hak programı"],
            ["500 kod", "%50", "Orta ölçekli şirketler", "Yıllık çalışan hediyesi"],
            ["1.000 kod", "%70", "Büyük kuruluşlar", "Müşteri sadakat programı"],
        ],
        "projecoes_titulo": "Finansal Projeksiyonlar: 50 Yıllık Ufuk",
        "projecoes_texto": "Projeksiyonlar, farklı pazar nüfuz oranlarını, B2B genişleme hızını ve dil başına organik büyümeyi yansıtan iki senaryo üzerine kurulmuştur — muhafazakar ve iyimser.",
        "projecoes_tabela": [
            ["Ufuk", "Muhafazakar (TL)", "İyimser (TL)"],
            ["1. Yıl", "TL 600 bin", "TL 2,4 milyon"],
            ["3. Yıl", "TL 2,2 milyon", "TL 8,4 milyon"],
            ["5. Yıl", "TL 9,4 milyon", "TL 28 milyon"],
            ["10. Yıl", "TL 56 milyon", "TL 150 milyon"],
            ["20. Yıl", "TL 280 milyon", "TL 750 milyon"],
            ["30. Yıl", "TL 650 milyon", "TL 1,68 milyar"],
            ["40. Yıl", "TL 1,03 milyar", "TL 2,8 milyar"],
            ["50. Yıl", "TL 1,4 milyar", "TL 4,68 milyar"],
        ],
        "tracao_titulo": "İvme ve Kanıtlanmış Sonuçlar",
        "tracao_texto": "A1ELOS, modeli doğrulayan ürün metrikleriyle zaten faaliyet gösteriyor — yüksek tutma oranı, premium değerlendirme ve büyüyen B2B ortak tabanı, platformun son kullanıcıya ve kurumsal pazara gerçek değer sunduğunu kanıtlıyor.",
        "tracao_kpis": [
            ("12K+", "Aktif Kullanıcı", "Tutarlı organik büyüme tabanı"),
            ("%87", "Tutma Oranı", "Sektör ortalamasının çok üzerinde (~%30)"),
            ("4,8★", "Ortalama Puan", "Kanıtlanmış son kullanıcı memnuniyeti"),
            ("23", "B2B Ortağı", "Şirketler ve İK ile aktif sözleşmeler"),
        ],
        "roteiro_titulo": "Stratejik Yol Haritası",
        "roteiro_texto": "A1ELOS, mevcut tabanın konsolidasyonundan küresel pazar liderliğine, yatırımcılar için net çıkış seçenekleriyle dört ilerleyici aşamada bir plan uygular.",
        "roteiro_fases": [
            ("1. Aşama · Konsolidasyon", "Zaten aktif olan dillerde kullanıcı tabanını güçlendirme. Dönüşüm, tutma ve LTV optimizasyonu. Tohum Turu tamamlandı."),
            ("2. Aşama · Genişleme", "3 yeni pazarda resmi lansman: Endonezya, Türkiye ve Vietnam. B2B kanalının ve coğrafi hedefli reklamın hızlandırılması."),
            ("3. Aşama · Küresel Giriş", "Yerelleştirilmiş kampanyalarla 14 dilin tamamında aktif varlık. 5+ kıtada white-label ortaklıkları. Seri A."),
            ("4. Aşama · Liderlik", "Konsolide operasyonlarla 20+ ülke. Uygulamalı numerolojide küresel referans SaaS platformu. Halka arz veya stratejik çıkış."),
        ],
        "invest_titulo": "Yatırım & İletişim",
        "invest_texto": "Özel sunumlar, durum tespiti ve müzakereler için hazırız. Tercih ettiğiniz kanaldan bize ulaşın.",
        "invest_dados": [
            ("Tohum Turu", "TL 580 bin"),
            ("Para Öncesi Değerleme", "TL 2,3 milyon"),
            ("Sunulan Sermaye", "En fazla %20"),
        ],
        "invest_contato": [
            ("Yatırımcı E-postası", "a1elos.consultoria@gmail.com"),
            ("Genel E-posta", "contato@a1elos.com"),
            ("Web Sitesi", "www.a1elos.com"),
            ("DUNS", "942242668 — Dun & Bradstreet"),
        ],
        "invest_alocacao": "Sermaye Dağılımı: %45 Teknoloji · %30 Pazarlama · %25 Operasyon",
        "frase_final": "Sayılar asla yalan söylemez.",
        "selo_final": ["DUNS 942242668", "23 ÜRÜN", "14 DİL", "~5,3 M KONUŞMACI"],
        "graf_cons": "Muhafazakar",
        "graf_otim": "İyimser",
        "grafico_titulo_linha": "Projeksiyonlu Büyüme (TL bin)",    
        
        "sumario_titulo": "Yönetici Özeti",
        "duns_porque": "DUNS Neden Önemlidir?",
        "preco_consciente": "Bilinçli Fiyatlandırma",
        "idioma_col": "Dil",
        "falantes_col": "Konuşmacı (milyon)",
        "total_linha": "TOPLAM",
        
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
        
        "fonte_receita": "Gelir Kaynağı",
        "participacao": "Pay",
        "b2c_linha": "B2C — 14 Dil",
        "b2b_linha": "B2B — Kademeli İndirimler",
        "pub_linha": "Coğrafi Hedefli Reklam",
        "tabela_descontos": "Kademeli İndirim Tablosu",
        "grafico_anos": ["1. Yıl", "5. Yıl", "10. Yıl", "20. Yıl", "50. Yıl"],
        "grafico_titulo": "Muhafazakar Projeksiyon (TL bin)",
        "fale_conosco": "Bize Ulaşın",    
    },

        "vi": {
        "titulo": "A1ELOS Thần Số Học Toàn Cầu",
        "subtitulo": "Khoa học về các con số áp dụng cho thành công của bạn",
        "capa_nota": "Bài trình bày chiến lược cho Nhà đầu tư và Đối tác",
        "confidencial": "BẢO MẬT",
        "ano": "2026",
        "sumario_intro": "Bài trình bày này được cấu trúc để hướng dẫn các nhà đầu tư và đối tác qua mọi khía cạnh chiến lược của A1ELOS Thần Số Học Toàn Cầu — từ luận điểm thị trường đến mô hình doanh thu định kỳ.",
        "sumario_cards": [
            ("01", "Về A1ELOS", "Công ty mẹ, danh mục và chứng nhận DUNS"),
            ("02", "Cơ hội thị trường", "Nền kinh tế chăm sóc sức khỏe toàn cầu 6,8 nghìn tỷ USD"),
            ("03", "Giải pháp và phạm vi toàn cầu", "14 ngôn ngữ, ~5,3 tỷ người nói"),
            ("04", "3 thị trường mới", "Indonesia, Thổ Nhĩ Kỳ và Việt Nam"),
            ("05", "Danh mục và giá cả", "23 sản phẩm được hiệu chỉnh theo sức mua"),
            ("06", "Doanh thu định kỳ", "Banner quảng cáo và Gói B2B"),
            ("07", "Dự báo và đầu tư", "Tầm nhìn 50 năm · Vòng Seed ₫ 1,3 tỷ"),
        ],
        "sobre_titulo": "Về A1ELOS",
        "sobre_texto": "A1ELOS là công ty mẹ về công nghệ và tri thức kết hợp trí tuệ nhân tạo, thần số học ứng dụng và chiến lược văn hóa để tạo ra các sản phẩm kỹ thuật số có tác động cao trên quy mô toàn cầu. Sứ mệnh của chúng tôi: dân chủ hóa sự hiểu biết về bản thân qua con số với sự tôn trọng văn hóa và tôn trọng sức mua của từng thị trường.",
        "sobre_kpis": [
            ("23", "Sản phẩm hoạt động", "Trong 4 cấp độ truy cập"),
            ("14", "Ngôn ngữ", "~67% dân số thế giới"),
            ("5,3B", "Người nói", "Thị trường thực có thể tiếp cận"),
            ("AI", "Tích hợp", "Công cụ cá nhân hóa"),
        ],
        "sobre_duns": "DUNS 942242668 — Chứng nhận Dun & Bradstreet có hiệu lực tại 190+ quốc gia, cho phép ký hợp đồng B2B và liên doanh quốc tế.",
        "duns_titulo": "Uy tín quốc tế",
        "duns_texto": "Số DUNS là hộ chiếu doanh nghiệp của A1ELOS trên trường quốc tế. Nó cho các đối tác, khách hàng doanh nghiệp và nhà đầu tư thấy rằng công ty có danh tính xác minh được, lịch sử truy vết được và năng lực hợp đồng tại bất kỳ khu vực pháp lý nào.",
        "duns_numero": "942242668",
        "duns_emitido": "Được cấp bởi Dun & Bradstreet — tiêu chuẩn toàn cầu về danh tính doanh nghiệp được công nhận tại hơn 190 quốc gia.",
        "duns_paises": "190+ QUỐC GIA",
        "duns_beneficios": [
            ("Hợp đồng B2B", "Đủ điều kiện cho đấu thầu và nhà cung cấp toàn cầu"),
            ("Liên doanh", "Quan hệ đối tác quốc tế với thẩm định dễ dàng"),
            ("Uy tín tức thì", "Dấu hiệu nghiêm túc cho các nhà đầu tư tổ chức"),
        ],
        "mercado_titulo": "Cơ hội thị trường",
        "mercado_texto": "Chúng ta đang sống trong sự hội tụ hoàn hảo: chăm sóc sức khỏe kỹ thuật số bùng nổ toàn cầu trong khi thần số học và chiêm tinh chuyển sang các ứng dụng có mức độ tương tác cao. A1ELOS định vị chính xác tại giao điểm này, với 74% dân số thế giới đã trực tuyến (~6 tỷ người).",
        "mercado_cards": [
            ("Sức khỏe toàn cầu", "6,8 nghìn tỷ USD → 9,8 nghìn tỷ đến 2029 (+7,6%/năm)"),
            ("Ứng dụng chiêm tinh/thần số", "3 tỷ USD → 9 tỷ đến 2030 · CAGR 20%"),
            ("Ứng dụng sức khỏe", "CAGR 14,9% → 26,2 tỷ USD vào 2030"),
            ("Người dùng trực tuyến", "74% thế giới · ~6 tỷ người"),
        ],
        "problema_titulo": "Vấn đề chúng tôi giải quyết",
        "problema_col_esq_titulo": "Thất bại của thị trường hiện tại",
        "problema_col_esq": [
            ("Rào cản ngôn ngữ", "Đại đa số công cụ thần số học chỉ hoạt động bằng tiếng Anh, loại trừ hàng tỷ người bản ngữ ở các ngôn ngữ khác."),
            ("Giá tách rời thực tế", "Sản phẩm tính bằng đô la cho thị trường mới nổi tạo ra sự loại trừ kinh tế — người dùng không từ chối sản phẩm, mà từ chối mức giá không thể tiếp cận."),
            ("Thiếu chiều sâu", "Công cụ chung chung đưa ra câu trả lời hời hợt không cá nhân hóa, không bối cảnh văn hóa và không ứng dụng thực tế vào đời sống."),
        ],
        "problema_col_dir_titulo": "Cái giá của sự loại trừ",
        "problema_col_dir": "Khi một nền tảng bỏ qua ngôn ngữ và sức mua, nó tự nguyện từ bỏ thị trường lớn nhất thế giới: hơn 4 tỷ người sống ở các nền kinh tế mới nổi và nói các ngôn ngữ không phải tiếng Anh. Đây chính là khoảng trống mà A1ELOS chiếm giữ với độ chính xác phẫu thuật.",
        "problema_destaque": "Các nền tảng bỏ qua sức mua địa phương mất quyền truy cập vào hơn 60% thị trường toàn cầu có thể tiếp cận.",
        "solucao_titulo": "Giải pháp của chúng tôi: 3 trụ cột chiến lược",
        "solucao_texto": "A1ELOS đã xây dựng một nền tảng tích hợp kết hợp khoa học con số, trí tuệ nhân tạo và sự nhạy cảm văn hóa. Giải pháp hoạt động trên ba hướng bổ sung, đảm bảo doanh thu đa dạng và tỷ lệ giữ chân cao.",
        "solucao_colunas": [
            ("Bản đồ cá nhân", "Phân tích số học sâu sắc và cá nhân hóa cho người dùng cuối — danh tính, sứ mệnh, chu kỳ cuộc đời và sự tương thích — được giao bằng 14 ngôn ngữ với AI tích hợp."),
            ("Thần số học doanh nghiệp", "Chẩn đoán thần số áp dụng cho thương hiệu, CNPJ, ngày thành lập và chiến lược doanh nghiệp. Sản phẩm khác biệt có giá trị cảm nhận cao trên thị trường B2B."),
            ("White-Label B2B", "Cấp phép nền tảng cho các công ty đối tác muốn cung cấp thần số học dưới thương hiệu riêng — với hỗ trợ đa ngôn ngữ và tùy chỉnh hoàn toàn."),
        ],
        "alcance_titulo": "Phạm vi toàn cầu: 14 ngôn ngữ · ~5,3 tỷ người nói",
        "alcance_texto": "A1ELOS bao phủ ~67% dân số thế giới với một nền tảng thực sự đa ngôn ngữ. Mỗi ngôn ngữ đại diện cho một thị trường văn hóa riêng biệt, với giá được hiệu chỉnh theo sức mua địa phương.",
        "mercados_titulo": "3 thị trường mới: +442 triệu người nói",
        "mercados_texto": "Việc mở rộng chiến lược sang Indonesia, Thổ Nhĩ Kỳ và Việt Nam đại diện cho một bước nhảy vọt về chất: các thị trường có tăng trưởng kinh tế cao, thâm nhập kỹ thuật số ngày càng tăng và nhu cầu đã được chứng minh về các giải pháp chăm sóc sức khỏe kỹ thuật số dễ tiếp cận.",
        "mercados_cards": [
            ("Indonesia", ["285 triệu dân", "80,5% thâm nhập internet", "~255 triệu người nói tiếng Indonesia", "Sức khỏe: 51,2 tỷ USD (2025) → 72,8 tỷ (2034)"]),
            ("Thổ Nhĩ Kỳ", ["85,9 triệu dân", "GDP PPP bình quân đầu người 37.301 USD", "~90 triệu người nói tiếng Thổ Nhĩ Kỳ", "Trên mức trung bình thế giới (27.211 USD)"]),
            ("Việt Nam",  ["~100 triệu dân", "GDP bình quân đầu người ~5.066 USD (+7,4%/năm)", "~97 triệu người nói tiếng Việt", "Sức khỏe: 303 triệu USD (2025) → 485 triệu (2030)"]),
        ],
        "mercados_rodape": "3 thị trường mới = +442 triệu người nói mới có thể tiếp cận — được tích hợp vào nền tảng với giá hiệu chỉnh theo văn hóa.",
        "preco_titulo": "Triết lý định giá có ý thức",
        "preco_esq": "Tôn trọng văn hóa + tôn trọng sức mua = thị trường thực có thể tiếp cận. Cùng tỷ lệ giá trị. Giá khác nhau. Phẩm giá bình đẳng cho mọi thị trường.",
        "preco_dir_titulo": "Cách hoạt động trên thực tế",
        "preco_dir": "A1ELOS áp dụng Sức mua tương đương (PPP) làm tiêu chí định giá trung tâm. Cùng một sản phẩm mang lại giá trị tương đối như nhau cho người dùng ở Lagos, Jakarta, Hà Nội hay New York — giá được hiệu chỉnh để nỗ lực tài chính tương xứng với thu nhập địa phương.",
        "preco_pilares": [
            ("Hiệu chỉnh theo PPP", "Giá được điều chỉnh theo chỉ số sức mua của từng quốc gia"),
            ("Tôn trọng văn hóa", "Ngôn ngữ, tiền tệ và bối cảnh địa phương tích hợp vào sản phẩm"),
            ("Chuyển đổi vượt trội", "Giá hợp lý tạo ra nhiều chuyển đổi hơn và giữ chân lâu dài tốt hơn"),
        ],
        "portfolio_titulo": "Danh mục: 23 sản phẩm trong 4 cấp độ",
        "portfolio_texto": "Cấu trúc phân tầng đảm bảo mọi hồ sơ người dùng — từ người tò mò đến chuyên gia — tìm được ưu đãi phù hợp với mức độ tương tác và khả năng tài chính của họ.",
        "portfolio_tabela": [
            ["Seviye", "Ürünler", "Fiyat Aralığı (TL)", "Profil"],
            ["Giriş", "Ekspres Harita, Hızlı Danışma", "TL 58", "Meraklı, ilk temas"],
            ["Orta", "AI Araştırma, Tam Harita, Uyumluluk", "TL 123", "Etkileşimli kullanıcı"],
            ["İleri", "İş Numerolojisi, Döngüler, Misyon", "TL 188–254", "Profesyonel, girişimci"],
            ["Premium", "Tam Teşhis, Kişisel White-Label", "TL 319–710", "Yüksek gelir, kurumsal kullanım"],
            ["B2B / Kurumsal", "Kurumsal paketler, lisanslar, hediyeler", "Talebe göre", "Şirketler ve İK"],
        ],
        "portfolio_rodape": "23 sản phẩm bao phủ toàn bộ hành trình người dùng, từ tiếp xúc đầu tiên đến khách hàng cao cấp định kỳ — tối đa hóa LTV theo ngôn ngữ và thị trường.",
        "negocio_titulo": "Mô hình kinh doanh: 3 nguồn doanh thu",
        "negocio_texto": "A1ELOS được thiết kế với doanh thu đa dạng và có thể mở rộng: bán trực tiếp cho người tiêu dùng cuối trên quy mô toàn cầu, hợp đồng B2B giá trị cao và quảng cáo định vị địa lý định kỳ — ba động cơ nuôi dưỡng lẫn nhau.",
        "negocio_colunas": [
            ("B2C — 14 ngôn ngữ", "Bán trực tiếp sản phẩm kỹ thuật số bằng mọi loại tiền tệ, với giá điều chỉnh theo PPP. Mở rộng tự động qua AI — không cần đội ngũ hỗ trợ tỷ lệ với tăng trưởng."),
            ("B2B — Chiết khấu lũy tiến", "Gói doanh nghiệp cho HR, xây dựng thương hiệu nhà tuyển dụng và quà tặng tổ chức. Chiết khấu từ 10% đến 70% theo khối lượng. Hợp đồng được DUNS 942242668 bảo trợ."),
            ("Quảng cáo định vị địa lý", "Banner phân khúc theo quốc gia, châu lục hoặc toàn cầu với luân phiên tự động. Doanh thu định kỳ hàng tháng giá trị cao — không phụ thuộc vào khối lượng bán sản phẩm."),
        ],
        "banners_titulo": "Banner quảng cáo — Doanh thu định kỳ hàng tháng",
        "banners_texto": "Nền tảng A1ELOS cung cấp không gian quảng cáo cao cấp với phân khúc chính xác theo vị trí địa lý — quốc gia, châu lục hoặc toàn cầu. Với luân phiên tự động mỗi 8 giây và định dạng tối ưu cho máy tính và di động, banner mang lại khả năng hiển thị đo lường được cho nhà quảng cáo khu vực và quốc tế.",
        "banners_tabela": [
            ["Bölümleme", "Sabit (TL/ay)", "Geçici (TL/ay)", "Reklamveren Profili"],
            ["Ülke", "TL 800", "TL 500", "Yerel KOBİ'ler, bölgesel ticaret"],
            ["Kıta", "TL 1.800", "TL 1.200", "Bölgesel markalar, kıta genişlemesi"],
            ["Dünya", "TL 3.500", "TL 2.500", "Küresel şirketler, uluslararası uygulamalar"],
            ["Özel Sponsorluk", "TL 6.000", "TL 4.500/kampanya", "Ana sponsorlar, lansmanlar"],
        ],
        "banners_formatos": "728×90 px — Banner trung tâm máy tính · 320×100 px — Định dạng di động tối ưu · 8 giây — Luân phiên tự động · Nhắm mục tiêu địa lý — Quốc gia, châu lục hoặc phạm vi toàn cầu",
        "b2b_titulo": "Gói doanh nghiệp B2B — Giá trị cao, khối lượng lớn",
        "b2b_texto": "Các Gói B2B biến A1ELOS thành công cụ xây dựng thương hiệu nhà tuyển dụng và chăm sóc sức khỏe doanh nghiệp. Công ty mua mã truy cập với số lượng lớn để phân phát làm quà tặng cho nhân viên hoặc khách hàng — được DUNS 942242668 bảo trợ cho hợp đồng doanh nghiệp chính thức.",
        "b2b_planos": [
            ("Temel Plan · 50 Kod", "50× Ekspres Harita (her biri TL 58). Çalışan sağlıklı yaşam programları ve işe alım eylemleri için idealdir."),
            ("Orta Plan · 100 Kod", "50× Ekspres + 50× AI Araştırma (TL 123). İK ve işveren markası stratejileri için mükemmeldir."),
            ("Premium Plan · 200 Kod", "100× Ekspres + 100× Tam Harita (TL 123). Büyük ekipler için maksimum analitik derinlik."),
        ],
        "b2b_tabela": [
            ["Từ", "Chiết khấu", "Hồ sơ", "Sử dụng được khuyến nghị"],
            ["10 mã", "10%", "Đội nhỏ", "Hoạt động sức khỏe một lần"],
            ["100 mã", "30%", "SME", "Chương trình phúc lợi hàng quý"],
            ["500 mã", "50%", "Công ty vừa", "Quà tặng hàng năm cho nhân viên"],
            ["1.000 mã", "70%", "Tập đoàn lớn", "Chương trình khách hàng thân thiết"],
        ],
        "projecoes_titulo": "Dự báo tài chính: Tầm nhìn 50 năm",
        "projecoes_texto": "Các dự báo được xây dựng trên hai kịch bản — thận trọng và lạc quan — phản ánh các mức độ thâm nhập thị trường khác nhau, tốc độ mở rộng B2B và tăng trưởng hữu cơ theo ngôn ngữ.",
        "projecoes_tabela": [
            ["Ufuk", "Muhafazakar (TL)", "İyimser (TL)"],
            ["1. Yıl", "TL 600 bin", "TL 2,4 milyon"],
            ["3. Yıl", "TL 2,2 milyon", "TL 8,4 milyon"],
            ["5. Yıl", "TL 9,4 milyon", "TL 28 milyon"],
            ["10. Yıl", "TL 56 milyon", "TL 150 milyon"],
            ["20. Yıl", "TL 280 milyon", "TL 750 milyon"],
            ["30. Yıl", "TL 650 milyon", "TL 1,68 milyar"],
            ["40. Yıl", "TL 1,03 milyar", "TL 2,8 milyar"],
            ["50. Yıl", "TL 1,4 milyar", "TL 4,68 milyar"],
        ],
        "tracao_titulo": "Đà phát triển và kết quả đã chứng minh",
        "tracao_texto": "A1ELOS đã hoạt động với các chỉ số sản phẩm xác thực mô hình — giữ chân cao, đánh giá cao cấp và cơ sở đối tác B2B ngày càng tăng chứng minh rằng nền tảng mang lại giá trị thực cho người dùng cuối và thị trường doanh nghiệp.",
        "tracao_kpis": [
            ("12K+", "Người dùng hoạt động", "Cơ sở tăng trưởng hữu cơ nhất quán"),
            ("87%", "Giữ chân", "Vượt xa mức trung bình ngành (~30%)"),
            ("4,8★", "Đánh giá trung bình", "Sự hài lòng đã chứng minh của người dùng cuối"),
            ("23", "Đối tác B2B", "Hợp đồng hoạt động với công ty và HR"),
        ],
        "roteiro_titulo": "Lộ trình chiến lược",
        "roteiro_texto": "A1ELOS thực hiện kế hoạch trong bốn giai đoạn tiến triển — từ củng cố cơ sở hiện tại đến vị trí dẫn đầu thị trường toàn cầu, với các lựa chọn thoát rõ ràng cho nhà đầu tư.",
        "roteiro_fases": [
            ("Giai đoạn 1 · Củng cố", "Tăng cường cơ sở người dùng ở các ngôn ngữ đang hoạt động. Tối ưu hóa chuyển đổi, giữ chân và LTV. Vòng Seed hoàn tất."),
            ("Giai đoạn 2 · Mở rộng", "Ra mắt chính thức tại 3 thị trường mới: Indonesia, Thổ Nhĩ Kỳ và Việt Nam. Tăng tốc kênh B2B và quảng cáo định vị địa lý."),
            ("Giai đoạn 3 · Gia nhập toàn cầu", "Hiện diện tích cực ở cả 14 ngôn ngữ với chiến dịch bản địa hóa. Quan hệ đối tác white-label tại 5+ châu lục. Vòng A."),
            ("Giai đoạn 4 · Dẫn đầu", "20+ quốc gia với hoạt động củng cố. Nền tảng SaaS tham chiếu toàn cầu trong thần số học ứng dụng. IPO hoặc thoát chiến lược."),
        ],
        "invest_titulo": "Đầu tư & Liên hệ",
        "invest_texto": "Chúng tôi sẵn sàng cho các buổi trình bày riêng, thẩm định và đàm phán. Liên hệ với chúng tôi qua kênh bạn ưa thích.",
        "invest_dados": [
            ("Tohum Turu", "TL 580 bin"),
            ("Para Öncesi Değerleme", "TL 2,3 milyon"),
            ("Sunulan Sermaye", "En fazla %20"),
        ],
        "invest_contato": [
            ("Email nhà đầu tư", "a1elos.consultoria@gmail.com"),
            ("Email chung", "contato@a1elos.com"),
            ("Website", "www.a1elos.com"),
            ("DUNS", "942242668 — Dun & Bradstreet"),
        ],
        "invest_alocacao": "Phân bổ vốn: 45% Công nghệ · 30% Tiếp thị · 25% Vận hành",
        "frase_final": "Các con số không bao giờ nói dối.",
        "selo_final": ["DUNS 942242668", "23 SẢN PHẨM", "14 NGÔN NGỮ", "~5,3 TỶ NGƯỜI NÓI"]
        "graf_cons": "Thận trọng",
        "graf_otim": "Lạc quan",
        "grafico_titulo_linha": "Tăng trưởng dự kiến (₫ nghìn)",    
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
# AUXILIARES DE DESENHO
# ------------------------------------------------------------
def _texto_wrap(doc, texto, fonte, tam, x, y, largura_max, cor, entrelinha, y_min=0):
    doc.setFillColor(cor)
    doc.setFont(fonte, tam)
    palavras = texto.split()
    linha = ""
    for p in palavras:
        teste = (linha + " " + p).strip()
        if doc.stringWidth(teste, fonte, tam) <= largura_max:
            linha = teste
        else:
            if y - entrelinha < y_min:
                return y
            doc.drawString(x, y, linha)
            y -= entrelinha
            linha = p
    if linha and y - entrelinha >= y_min:
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
        doc.drawRightString(largura - 30 * mm, altura - 12 * mm, "%02d" % indice)
    # Logo reduzida no canto superior direito
    if os.path.exists(LOGO_PATH):
        try:
            iw, ih = ImageReader(LOGO_PATH).getSize()
            lw = 10 * mm
            lh = lw * ih / iw
            doc.drawImage(LOGO_PATH, largura - 12 * mm - lw, altura - 15 * mm,
                          width=lw, height=lh, mask="auto")
        except Exception:
            pass

def _kpis_grid(doc, largura, altura, lang, kpis, y, colunas=4):
    margem = 18 * mm
    gap = 6 * mm
    w = (largura - 2 * margem - (colunas - 1) * gap) / colunas
    x0 = margem
    max_h = 0
    for i, item in enumerate(kpis):
        dois = (len(item) == 2)
        h = 40 * mm if dois else 30 * mm
        max_h = max(max_h, h)
        x = x0 + i * (w + gap)
        _caixa(doc, x, y - h, w, h, COR_FUNDO, COR_DOURADO)
        if dois:
            doc.setFillColor(COR_AZUL)
            doc.setFont(_fonte(lang, True), 9)
            _texto_wrap(doc, item[0], _fonte(lang, True), 9, x + 4 * mm, y - 10 * mm,
                        w - 8 * mm, COR_AZUL, 4 * mm, y_min=y - h + 4 * mm)
            doc.setFillColor(COR_CINZA)
            doc.setFont(_fonte(lang), 7.5)
            _texto_wrap(doc, item[1], _fonte(lang), 7.5, x + 4 * mm, y - 16 * mm,
                        w - 8 * mm, COR_CINZA, 3.5 * mm, y_min=y - h + 4 * mm)
        else:
            num, rot, sub = item
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
                            w - 8 * mm, COR_CINZA, 3.5 * mm, y_min=y - h + 2 * mm)
    return y - max_h - 6 * mm
    
def _tabela_editorial(doc, x, y, largura, dados, colunas_pct, tam=9, lang="pt"):
    est = ParagraphStyle("cel", fontName=_fonte(lang), fontSize=tam,
                         leading=tam * 1.25, textColor=COR_PRETO)
    est_head = ParagraphStyle("chead", fontName=_fonte(lang, True), fontSize=tam,
                              leading=tam * 1.25, textColor=white)
    corpo = []
    for r, linha in enumerate(dados):
        est_c = est_head if r == 0 else est
        corpo.append([Paragraph(str(cel), est_c) for cel in linha])
    tbl = Table(corpo, colWidths=[largura * p for p in colunas_pct])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), COR_AZUL),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
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
    
def _grafico_barras(doc, x, y, w, h, categorias, valores, titulo, cores=None):
    """Barras com cor distinta por categoria + legenda (cor -> significado)."""
    try:
        n = len(valores)
        if n == 0:
            return
        paleta = cores or CORES_GRAFICO
        cores_barra = [paleta[i % len(paleta)] for i in range(n)]
        max_v = max([abs(v) for v in valores] + [1])
        area_x = x + 20
        area_y = y + 8
        area_w = w - 40 - 110          # reserva direita para a legenda
        area_h = h - 30
        gap = 6
        bar_w = max(6, (area_w - gap * (n - 1)) / n)
        # titulo
        doc.setFillColor(COR_PRETO)
        doc.setFont(_fonte("pt", True), 9)
        doc.drawCentredString(x + w / 2, y + h - 12, titulo)
        # grade e eixo
        doc.setStrokeColor(HexColor("#D8DAE0"))
        doc.setLineWidth(0.5)
        for g_i in range(5):
            gy = area_y + (g_i / 4.0) * (area_h - 6)
            doc.line(area_x, gy, area_x + area_w, gy)
            doc.setFillColor(COR_CINZA_CLARO)
            doc.setFont(_fonte("pt"), 6)
            doc.drawRightString(area_x - 3, gy - 2,
                                format(int(max_v * g_i / 4.0), ",").replace(",", "."))
        # barras coloridas
        for i, v in enumerate(valores):
            bx = area_x + i * (bar_w + gap)
            bh = max((v / max_v) * (area_h - 6), 1)
            doc.setFillColor(cores_barra[i])
            doc.rect(bx, area_y, bar_w, bh, stroke=0, fill=1)
            doc.setFillColor(COR_PRETO)
            doc.setFont(_fonte("pt", True), 6.5)
            doc.drawCentredString(bx + bar_w / 2, area_y + bh + 2,
                                  format(int(v), ",").replace(",", "."))
            # rotulo da categoria (inclinado)
            doc.saveState()
            doc.translate(bx + bar_w / 2, area_y - 2)
            doc.rotate(45)
            doc.setFillColor(COR_CINZA)
            doc.setFont(_fonte("pt"), 7)
            doc.drawCentredString(0, 0, str(categorias[i])[:14])
            doc.restoreState()
        # legenda: cor -> significado
        lx = x + area_w + 28
        ly = y + h - 22
        doc.setFillColor(COR_PRETO)
        doc.setFont(_fonte("pt", True), 8)
        doc.drawString(lx, ly + 6, "Legenda")
        for i, c_ in enumerate(cores_barra):
            doc.setFillColor(c_)
            doc.rect(lx, ly - i * 13, 8, 8, stroke=0, fill=1)
            doc.setFillColor(COR_PRETO)
            doc.setFont(_fonte("pt"), 7)
            doc.drawString(lx + 12, ly - i * 13, str(categorias[i])[:24])
    except Exception as e:
        logger.warning("Grafico barras: %s", e)

def _grafico_pizza(doc, x, y, w, h, rotulos, valores, titulo):
    """Pizza com cor distinta por fatia + legenda (cor -> significado)."""
    try:
        n = len(valores)
        if n == 0:
            return
        total = sum(valores) or 1
        cores_fatia = [CORES_GRAFICO[i % len(CORES_GRAFICO)] for i in range(n)]
        cx = x + min(w * 0.30, 150)
        cy = y + h * 0.44
        raio = min(w * 0.24, h * 0.38)
        doc.setStrokeColor(white)
        doc.setLineWidth(0.9)
        ang = 90.0  # comeca no topo, sentido horario
        for i, v in enumerate(valores):
            ext = -(v / total) * 360.0
            doc.setFillColor(cores_fatia[i])
            p = doc.beginPath()
            p.moveTo(cx, cy)
            p.arc(cx - raio, cy - raio, cx + raio, cy + raio,
                  startAng=ang, extent=ext)
            p.close()
            doc.drawPath(p, stroke=1, fill=1)
            # rotulo dentro da fatia (nome curto + %)
            if abs(ext) >= 10:
                ang_med = math.radians(ang + ext / 2.0)
                lx = cx + raio * 0.62 * math.cos(ang_med)
                ly = cy + raio * 0.62 * math.sin(ang_med)
                c = cores_fatia[i]
                lum = 0.299 * c.red + 0.587 * c.green + 0.114 * c.blue
                doc.setFillColor(white if lum < 0.62 else COR_PRETO)
                doc.setFont(_fonte("pt", True), 7)
                doc.drawCentredString(lx, ly, str(rotulos[i])[:12])
                doc.setFont(_fonte("pt"), 6.5)
                doc.drawCentredString(lx, ly - 8, "%.0f%%" % (v / total * 100))
            ang += ext
        # legenda: cor -> significado (valor + %)
        lx = x + w * 0.62 + 6
        ly = y + h - 18
        doc.setFillColor(COR_PRETO)
        doc.setFont(_fonte("pt", True), 8)
        doc.drawString(lx, ly + 6, "Legenda")
        for i, c_ in enumerate(cores_fatia):
            doc.setFillColor(c_)
            doc.rect(lx, ly - i * 14, 9, 9, stroke=0, fill=1)
            doc.setFillColor(COR_PRETO)
            doc.setFont(_fonte("pt", True), 7.5)
            doc.drawString(lx + 13, ly - i * 14 + 1, str(rotulos[i])[:22])
            doc.setFont(_fonte("pt"), 7)
            doc.drawString(lx + 13, ly - i * 14 - 6,
                           "%s  (%.0f%%)" % (format(int(valores[i]), ",").replace(",", "."),
                                              valores[i] / total * 100 if total else 0))
        # titulo
        doc.setFillColor(COR_PRETO)
        doc.setFont(_fonte("pt", True), 9)
        doc.drawCentredString(x + w / 2, y + h - 8, titulo)
    except Exception as e:
        logger.warning("Grafico pizza: %s", e)

def _grafico_linha(doc, x, y, w, h, categorias, series, titulo, cores=None):
    """Linha do tempo com linhas grossas e coloridas (crescimento)."""
    try:
        n = len(categorias)
        if n == 0:
            return
        paleta = cores or [COR_AZUL, COR_DOURADO, HexColor("#3B82F6")]
        max_v = 1
        for nome, valores in series:
            max_v = max(max_v, max([abs(v) for v in valores]))
        area_x = x + 20
        area_y = y + 8
        area_w = w - 40 - 110
        area_h = h - 30
        # titulo
        doc.setFillColor(COR_PRETO)
        doc.setFont(_fonte("pt", True), 9)
        doc.drawCentredString(x + w / 2, y + h - 12, titulo)
        # grade
        doc.setStrokeColor(HexColor("#D8DAE0"))
        doc.setLineWidth(0.5)
        for g_i in range(5):
            gy = area_y + (g_i / 4.0) * (area_h - 6)
            doc.line(area_x, gy, area_x + area_w, gy)
            doc.setFillColor(COR_CINZA_CLARO)
            doc.setFont(_fonte("pt"), 6)
            doc.drawRightString(area_x - 3, gy - 2,
                                format(int(max_v * g_i / 4.0), ",").replace(",", "."))
        # linhas grossas e coloridas
        for si, (nome, valores) in enumerate(series):
            cor = paleta[si % len(paleta)]
            pts = []
            for i, v in enumerate(valores):
                px = area_x + (i / (n - 1)) * area_w
                py = area_y + (v / max_v) * (area_h - 6)
                pts.append((px, py))
            doc.setStrokeColor(cor)
            doc.setLineWidth(3)
            p = doc.beginPath()
            p.moveTo(*pts[0])
            for pt in pts[1:]:
                p.lineTo(*pt)
            doc.drawPath(p, stroke=1, fill=0)
            for px, py in pts:
                doc.setFillColor(cor)
                doc.circle(px, py, 2.5, stroke=0, fill=1)
        # rotulos das categorias (abaixo, em tom escuro, sem rotacionar)
        for i, cat in enumerate(categorias):
            px = area_x + (i / (n - 1)) * area_w
            doc.setFillColor(COR_PRETO)
            doc.setFont(_fonte("pt", True), 7)
            doc.drawCentredString(px, area_y - 4, str(cat))
        # legenda (sem invadir o grafico)
        lx = x + area_w + 28
        ly = y + h - 22
        doc.setFillColor(COR_PRETO)
        doc.setFont(_fonte("pt", True), 8)
        doc.drawString(lx, ly + 6, "Legenda")
        for si, (nome, valores) in enumerate(series):
            cor = paleta[si % len(paleta)]
            doc.setStrokeColor(cor)
            doc.setLineWidth(3)
            doc.line(lx, ly - si * 13 + 4, lx + 10, ly - si * 13 + 4)
            doc.setFillColor(COR_PRETO)
            doc.setFont(_fonte("pt"), 7)
            doc.drawString(lx + 14, ly - si * 13, str(nome)[:24])
    except Exception as e:
        logger.warning("Grafico linha: %s", e)

# ------------------------------------------------------------
# GERADOR TEXTO (documento editorial)
# ------------------------------------------------------------
def gerar_pdf_texto(lang="pt", caminho_saida=None): 
    logger.info(">>> MARKER PDF TEXTO NOVO v2026-09-04")
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
    _titulo_pagina(doc, largura, altura, lang, c.get("sumario_titulo", "Sumário Executivo"), 1)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["sumario_intro"], _fonte(lang), 11, 18 * mm, y,
                    largura - 36 * mm, COR_CINZA, 5 * mm)
    y -= 4 * mm
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
    y -= 3 * mm
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
    xr = 18 * mm + col_w + 8 * mm
    doc.setFillColor(COR_PRETO)
    doc.setFont(_fonte(lang, True), 12)
    doc.drawString(xr, y - 8 * mm, c.get("duns_porque", "Por que o DUNS importa?"))
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
    y -= 3 * mm
    y = _kpis_grid(doc, largura, altura, lang, c["mercado_cards"], y, 4)
    _rodape(doc, largura, altura, lang, c, pagina)
    doc.showPage()
    pagina += 1
    # PROBLEMA (2 colunas)
    _titulo_pagina(doc, largura, altura, lang, c["problema_titulo"], 5)
    y = altura - 32 * mm
    col_w = (largura - 36 * mm - 8 * mm) / 2
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
    y -= 4 * mm
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
    y -= 4 * mm
    linhas = c.get("linhas_idiomas", LINHAS_IDIOMAS)
    dados = [[c.get("idioma_col", "Idioma"), c.get("falantes_col", "Falantes (mi)")]] \
            + linhas + [[c.get("total_linha", "TOTAL"), "~5.320"]]
    y = _tabela_editorial(doc, 18 * mm, y, largura - 36 * mm, dados, [0.6, 0.4], 9, lang)
    _rodape(doc, largura, altura, lang, c, pagina)
    doc.showPage()
    pagina += 1
    # 3 NOVOS MERCADOS (3 colunas com bandeiras)
    _titulo_pagina(doc, largura, altura, lang, c["mercados_titulo"], 8)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["mercados_texto"], _fonte(lang), 11, 18 * mm, y,
                    largura - 36 * mm, COR_CINZA, 5 * mm)
    y -= 4 * mm
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
    doc.drawString(22 * mm, y - 14 * mm, c.get("preco_consciente", "Preço Consciente"))
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
        _caixa(doc, xr, yy - 26 * mm, col_w, 26 * mm, COR_FUNDO, COR_DOURADO)
        doc.setFillColor(COR_AZUL)
        doc.setFont(_fonte(lang, True), 10)
        doc.drawString(xr + 5 * mm, yy - 18 * mm, tit)
        doc.setFillColor(COR_CINZA)
        doc.setFont(_fonte(lang), 8)
        _texto_wrap(doc, sub, _fonte(lang), 8, xr + 5 * mm, yy - 13 * mm,
                    col_w - 10 * mm, COR_CINZA, 3.5 * mm, y_min=yy - 24 * mm)
        yy -= 30 * mm
    _rodape(doc, largura, altura, lang, c, pagina)
    doc.showPage()
    pagina += 1
    # PORTFÓLIO (tabela 4 colunas)
    _titulo_pagina(doc, largura, altura, lang, c["portfolio_titulo"], 10)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["portfolio_texto"], _fonte(lang), 11, 18 * mm, y,
                    largura - 36 * mm, COR_CINZA, 5 * mm)
    y -= 4 * mm
    y = _tabela_editorial(doc, 18 * mm, y, largura - 36 * mm,
                          c["portfolio_tabela"], [0.22, 0.38, 0.18, 0.22], 9, lang)
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
    y -= 4 * mm
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
    _tabela_editorial(doc, 18 * mm, y - 60 * mm, largura - 36 * mm,
                      [[c.get("fonte_receita", "Fonte de Receita"), c.get("participacao", "Participação")],
                       [c.get("b2c_linha", "B2C — 14 Idiomas"), "60%"],
                       [c.get("b2b_linha", "B2B — Descontos Progressivos"), "25%"],
                       [c.get("pub_linha", "Publicidade Geolocalizada"), "15%"]],
                      [0.7, 0.3], 10, lang)
    _rodape(doc, largura, altura, lang, c, pagina)
    doc.showPage()
    pagina += 1
    # BANNERS (tabela 4 colunas)
    _titulo_pagina(doc, largura, altura, lang, c["banners_titulo"], 12)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["banners_texto"], _fonte(lang), 11, 18 * mm, y,
                    largura - 36 * mm, COR_CINZA, 5 * mm)
    y -= 4 * mm
    y = _tabela_editorial(doc, 18 * mm, y, largura - 36 * mm,
                          c["banners_tabela"], [0.24, 0.20, 0.24, 0.32], 9, lang)
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
    y -= 4 * mm
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
    doc.drawString(18 * mm, y - 6 * mm, c.get("tabela_descontos", "Tabela de Descontos Progressivos"))
    y -= 12 * mm
    _tabela_editorial(doc, 18 * mm, y, largura - 36 * mm,
                      c["b2b_tabela"], [0.22, 0.18, 0.28, 0.32], 9, lang)
    _rodape(doc, largura, altura, lang, c, pagina)
    doc.showPage()
    pagina += 1
    # PROJEÇÕES (tabela)
    _titulo_pagina(doc, largura, altura, lang, c["projecoes_titulo"], 14)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["projecoes_texto"], _fonte(lang), 11, 18 * mm, y,
                    largura - 36 * mm, COR_CINZA, 5 * mm)
    y -= 4 * mm
    _tabela_editorial(doc, 18 * mm, y, largura - 36 * mm,
                      c["projecoes_tabela"], [0.3, 0.35, 0.35], 9, lang)
    _grafico_barras(doc, 18 * mm, y - 100 * mm, largura - 36 * mm, 50 * mm,
                    c.get("grafico_anos", ["Ano 1", "Ano 5", "Ano 10", "Ano 20", "Ano 50"]),
                    [33, 500, 3000, 15000, 75000],
                    c.get("grafico_titulo", "Projeção Conservadora (R$ mil)"))
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
    y -= 4 * mm
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
    y -= 4 * mm
    col_w = (largura - 36 * mm - 8 * mm) / 2
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
    xr = 18 * mm + col_w + 8 * mm
    doc.setFillColor(COR_PRETO)
    doc.setFont(_fonte(lang, True), 12)
    doc.drawString(xr, y - 8 * mm, c.get("fale_conosco", "Fale Conosco"))
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
        # Titulo azul, no topo do card
        doc.setFillColor(COR_AZUL)
        doc.setFont(_fonte(lang, True), 10)
        _texto_wrap(doc, tit, _fonte(lang, True), 10, x + 4 * mm, y - 12 * mm,
                    w - 8 * mm, COR_AZUL, 4.5 * mm, y_min=y - 20 * mm)
        # Subtitulo em PRETO (nao some no fundo), abaixo, sem sobrepor
        doc.setFillColor(COR_PRETO)
        doc.setFont(_fonte(lang), 8.5)
        _texto_wrap(doc, sub, _fonte(lang), 8.5, x + 4 * mm, y - 22 * mm,
                    w - 8 * mm, COR_PRETO, 4 * mm, y_min=y - h + 4 * mm)
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
    linhas = c.get("linhas_idiomas", LINHAS_IDIOMAS)
    dados = [[c.get("idioma_col", "Idioma"), c.get("falantes_col", "Falantes (mi)")]] \
        + linhas + [[c.get("total_linha", "TOTAL"), "~5.320"]]
    _tabela_editorial(doc, 18 * mm, y, largura - 36 * mm, dados, [0.6, 0.4], 9, lang)
    rodape(pagina)
    doc.showPage()
    pagina += 1

    # ===== SLIDE 9 — 3 NOVOS MERCADOS (08) =====
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

    # ===== SLIDE 10 — FILOSOFIA DE PREÇO (09) =====
    cab(c["preco_titulo"], 9)
    y = altura - 32 * mm
    col_w = (largura - 36 * mm - 10 * mm) / 2
    _caixa(doc, 18 * mm, y - 60 * mm, col_w, 60 * mm, COR_PRETO, COR_DOURADO)
    doc.setFillColor(COR_DOURADO)
    doc.setFont(_fonte(lang, True), 13)
    doc.drawString(22 * mm, y - 16 * mm, c.get("preco_consciente", "Preço Consciente"))
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
                          c["portfolio_tabela"], [0.22, 0.38, 0.18, 0.22], 9, lang)
    y -= 8 * mm
    doc.setFillColor(COR_CINZA)
    doc.setFont(_fonte(lang), 9)
    _texto_wrap(doc, c["portfolio_rodape"], _fonte(lang), 9, 18 * mm, y,
                largura - 36 * mm, COR_CINZA, 4 * mm)
    rodape(pagina)
    doc.showPage()
    pagina += 1

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
                  [0.7, 0.3], 10, lang)
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
                          c["banners_tabela"], [0.24, 0.20, 0.24, 0.32], 9, lang)
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
    doc.drawString(18 * mm, y - 6 * mm, c.get("tabela_descontos", "Tabela de Descontos Progressivos"))
    y -= 14 * mm
    _tabela_editorial(doc, 18 * mm, y, largura - 36 * mm,
                      c["b2b_tabela"], [0.22, 0.18, 0.28, 0.32], 9, lang)
    rodape(pagina)
    doc.showPage()
    pagina += 1

    cab(c["projecoes_titulo"], 14)
    y = altura - 32 * mm
    y = _texto_wrap(doc, c["projecoes_texto"], _fonte(lang), 12, 18 * mm, y,
                    largura - 36 * mm, COR_CINZA, 6 * mm)
    y -= 8 * mm
    _tabela_editorial(doc, 18 * mm, y, largura - 36 * mm,
                      c["projecoes_tabela"], [0.3, 0.35, 0.35], 8, lang)
    y -= 75 * mm
    _grafico_linha(doc, 18 * mm, y - 45 * mm, largura - 36 * mm, 45 * mm,
               c.get("grafico_anos", ["Ano 1", "Ano 5", "Ano 10", "Ano 20", "Ano 50"]),
               [(c.get("graf_cons", "Conservador"), [33, 500, 3000, 15000, 75000]),
                (c.get("graf_otim", "Otimista"), [130, 1500, 8000, 40000, 250000])],
               c.get("grafico_titulo_linha", "Crescimento Projetado (R$ mil)"))
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
        doc.drawCentredString(x + w / 2, altura * 0.40 + 11 * mm, item)
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
