# -*- coding: utf-8 -*-
# ============================================================
# apresentacao_textos.py
# Gerador de Apresentação Empresarial A1ELOS
# Formatos: TEXTO (documento) e SLIDES (deck)
# 14 idiomas: pt, en, es, it, fr, de, ru, zh, ja, ar, he, id, tr, vi
# Substitui a versão anterior. 30/08/2026
# ============================================================

import os
import logging
from datetime import date

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, KeepTogether
)
from reportlab.lib.utils import ImageReader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ------------------------------------------------------------
# 1. CONFIGURAÇÃO DE CAMINHOS
# ------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Imagens usadas em TODOS os idiomas (mesmas em todos)
LOGO_PATH = os.path.join(STATIC_DIR, "Logo.png")
WATERMARK_PATH = os.path.join(STATIC_DIR, "watermark.png")  # marca d'água (Vitruviano dourado)

# Se a marca d'água não existir, usa o logo como fallback
if not os.path.exists(WATERMARK_PATH):
    WATERMARK_PATH = LOGO_PATH

# ------------------------------------------------------------
# 2. CORES DA MARCA (azul + preto/dourado)
# ------------------------------------------------------------
COR_AZUL = HexColor("#1E3A8A")
COR_AZUL_MEDIO = HexColor("#3B82F6")
COR_PRETO = HexColor("#1A1A1A")
COR_DOURADO = HexColor("#C9A94E")
COR_CINZA = HexColor("#555555")
COR_CINZA_CLARO = HexColor("#9E9E9E")

# ------------------------------------------------------------
# 3. FONTES (com fallback seguro para não travar)
# ------------------------------------------------------------
def _registrar_fontes():
    """Registra fontes TTF se existirem; senão usa fontes padrão."""
    fontes = {}
    # Latin + Cirílico (ru) + suporte amplo
    dejavu = os.path.join(STATIC_DIR, "DejaVuSans.ttf")
    dejavu_bold = os.path.join(STATIC_DIR, "DejaVuSans-Bold.ttf")
    if os.path.exists(dejavu):
        pdfmetrics.registerFont(TTFont("DejaVu", dejavu))
        fontes["normal"] = "DejaVu"
    else:
        fontes["normal"] = "Helvetica"
    if os.path.exists(dejavu_bold):
        pdfmetrics.registerFont(TTFont("DejaVu-Bold", dejavu_bold))
        fontes["bold"] = "DejaVu-Bold"
    else:
        fontes["bold"] = "Helvetica-Bold"

    # CJK (zh, ja) — fontes CID embutidas do ReportLab
    try:
        pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))  # chinês
        fontes["zh"] = "STSong-Light"
    except Exception:
        fontes["zh"] = fontes["normal"]
    try:
        pdfmetrics.registerFont(UnicodeCIDFont("HeiseiMin-W3"))  # japonês
        fontes["ja"] = "HeiseiMin-W3"
    except Exception:
        fontes["ja"] = fontes["normal"]

    return fontes

FONTES = _registrar_fontes()
# ------------------------------------------------------------
# 4. CONTEÚDO POR IDIOMA
# Estrutura: cada idioma tem título, subtítulo, seções e KPIs.
# ------------------------------------------------------------
CONTEUDO = {
    "pt": {
        "titulo": "A1ELOS Global Numerology",
        "subtitulo": "A ciência dos números aplicada ao seu sucesso",
        "capa_nota": "Apresentação para Investidores e Parceiros",
        "confidencial": "CONFIDENCIAL",
        "ano": "2026",
        "sobre_titulo": "Sobre a A1ELOS",
        "sobre_texto": "Holding de tecnologia e conhecimento que une a tradição milenar da numerologia à Inteligência Artificial, entregando relatórios digitais instantâneos com custo marginal próximo de zero.",
        "sobre_kpis": ["23 Produtos", "14 Idiomas", "~5,3 Bilhões de falantes", "IA Integrada", "DUNS 942242668"],
        "duns_titulo": "Credibilidade Internacional",
        "duns_texto": "O número DUNS 942242668, emitido pela Dun & Bradstreet, é reconhecido em mais de 190 países e habilita contratos corporativos, licitações e joint ventures internacionais.",
        "mercado_titulo": "Oportunidade de Mercado",
        "mercado_texto": "Economia global de bem-estar: US$ 6,8 trilhões (2024) para US$ 9,8 trilhões (2029). Apps de astrologia/numerologia: US$ 3 bi (2024) para US$ 9 bi (2030), CAGR 20%.",
        "problema_titulo": "O Problema",
        "problema_texto": "Ferramentas genéricas falham o usuário e a maioria cobra preços descolados do poder aquisitivo local. A A1ELOS corrige isso.",
        "solucao_titulo": "Nossa Solução",
        "solucao_texto": "Numerologia aplicada em escala: algoritmos proprietários + IA + entrega instantânea de PDFs premium em 14 idiomas.",
        "alcance_titulo": "Alcance Global",
        "alcance_texto": "14 idiomas cobrindo ~5,3 bilhões de falantes (~67% da população mundial).",
        "mercados_titulo": "3 Novos Mercados",
        "mercados_texto": "Indonésia (255 mi falantes), Turquia (90 mi) e Vietnã (97 mi) — +442 milhões de novos falantes com poder aquisitivo mapeado.",
        "preco_titulo": "Preço Consciente",
        "preco_texto": "A mesma proporção de valor para todas as moedas, calibrada pelo poder aquisitivo (PPC) de cada país. Respeita a cultura e o bolso.",
        "portfolio_titulo": "Portfólio",
        "portfolio_texto": "23 produtos em 4 níveis (Entrada R$ 8, Intermediário R$ 17, Avançado R$ 26-35, Premium R$ 44-98) + segmento B2B.",
        "negocio_titulo": "Modelo de Negócio",
        "negocio_texto": "3 fontes de receita: B2C (14 idiomas, todas as moedas), B2B (descontos progressivos), Publicidade geolocalizada.",
        "banners_titulo": "Banners Publicitários",
        "banners_texto": "Receita recorrente mensal: País R$ 800, Continente R$ 1.800, Mundo R$ 3.500, Patrocínio Exclusivo R$ 6.000.",
        "b2b_titulo": "Pacotes Empresariais B2B",
        "b2b_texto": "Brinde para empregados ou clientes. Descontos progressivos: 10% (10 códigos), 30% (100), 50% (500), 70% (1.000).",
        "projecoes_titulo": "Projeções Financeiras",
        "projecoes_texto": "Ano 1: R$ 33k-130k | Ano 5: R$ 500k-1,5M | Ano 10: R$ 3-8M | Ano 20: R$ 15-40M | Ano 50: R$ 75-250M.",
        "tracao_titulo": "Tração e Resultados",
        "tracao_texto": "12K+ usuários ativos, 87% de retenção, 4,8★ de avaliação, 23 parceiros B2B.",
        "roteiro_titulo": "Roteiro Estratégico",
        "roteiro_texto": "Consolidação, Expansão (Indonésia, Turquia, Vietnã), Entrada Global e Liderança (20+ países + IPO).",
        "invest_titulo": "Investimento e Contato",
        "invest_texto": "Rodada Seed R$ 3,5M · Valuation R$ 14M · Equity até 20%. Contato: a1elos.consultoria@gmail.com · www.a1elos.com",
        "frase_final": "Os números nunca mentem — e apontam para uma oportunidade extraordinária."
    },
    "en": {
        "titulo": "A1ELOS Global Numerology",
        "subtitulo": "The science of numbers applied to your success",
        "capa_nota": "Presentation for Investors and Partners",
        "confidencial": "CONFIDENTIAL",
        "ano": "2026",
        "sobre_titulo": "About A1ELOS",
        "sobre_texto": "A technology and knowledge holding that combines the ancient tradition of numerology with Artificial Intelligence, delivering instant digital reports at near-zero marginal cost.",
        "sobre_kpis": ["23 Products", "14 Languages", "~5.3 Billion speakers", "Integrated AI", "DUNS 942242668"],
        "duns_titulo": "International Credibility",
        "duns_texto": "The DUNS number 942242668, issued by Dun & Bradstreet, is recognized in over 190 countries and enables corporate contracts, tenders and international joint ventures.",
        "mercado_titulo": "Market Opportunity",
        "mercado_texto": "Global wellness economy: US$ 6.8 trillion (2024) to US$ 9.8 trillion (2029). Astrology/numerology apps: US$ 3B (2024) to US$ 9B (2030), 20% CAGR.",
        "problema_titulo": "The Problem",
        "problema_texto": "Generic tools fail the user and most charge prices disconnected from local purchasing power. A1ELOS fixes this.",
        "solucao_titulo": "Our Solution",
        "solucao_texto": "Numerology applied at scale: proprietary algorithms + AI + instant delivery of premium PDFs in 14 languages.",
        "alcance_titulo": "Global Reach",
        "alcance_texto": "14 languages covering ~5.3 billion speakers (~67% of the world population).",
        "mercados_titulo": "3 New Markets",
        "mercados_texto": "Indonesia (255M speakers), Turkey (90M) and Vietnam (97M) — +442 million new speakers with mapped purchasing power.",
        "preco_titulo": "Conscious Pricing",
        "preco_texto": "The same value proportion for all currencies, calibrated by the purchasing power (PPP) of each country. Respects culture and wallet.",
        "portfolio_titulo": "Portfolio",
        "portfolio_texto": "23 products in 4 tiers (Entry R$ 8, Intermediate R$ 17, Advanced R$ 26-35, Premium R$ 44-98) plus B2B segment.",
        "negocio_titulo": "Business Model",
        "negocio_texto": "3 revenue streams: B2C (14 languages, all currencies), B2B (progressive discounts), Geo-targeted advertising.",
        "banners_titulo": "Advertising Banners",
        "banners_texto": "Recurring monthly revenue: Country R$ 800, Continent R$ 1,800, World R$ 3,500, Exclusive Sponsorship R$ 6,000.",
        "b2b_titulo": "B2B Corporate Packages",
        "b2b_texto": "Gift for employees or clients. Progressive discounts: 10% (10 codes), 30% (100), 50% (500), 70% (1,000).",
        "projecoes_titulo": "Financial Projections",
        "projecoes_texto": "Year 1: R$ 33k-130k | Year 5: R$ 500k-1.5M | Year 10: R$ 3-8M | Year 20: R$ 15-40M | Year 50: R$ 75-250M.",
        "tracao_titulo": "Traction and Results",
        "tracao_texto": "12K+ active users, 87% retention, 4.8★ rating, 23 B2B partners.",
        "roteiro_titulo": "Strategic Roadmap",
        "roteiro_texto": "Consolidation, Expansion (Indonesia, Turkey, Vietnam), Global Entry and Leadership (20+ countries + IPO).",
        "invest_titulo": "Investment and Contact",
        "invest_texto": "Seed round R$ 3.5M · Valuation R$ 14M · Equity up to 20%. Contact: a1elos.consultoria@gmail.com · www.a1elos.com",
        "frase_final": "Numbers never lie — and they point to an extraordinary opportunity."
    },
    "es": {
        "titulo": "A1ELOS Global Numerology",
        "subtitulo": "La ciencia de los números aplicada a tu éxito",
        "capa_nota": "Presentación para Inversores y Socios",
        "confidencial": "CONFIDENCIAL",
        "ano": "2026",
        "sobre_titulo": "Sobre A1ELOS",
        "sobre_texto": "Holding de tecnología y conocimiento que une la tradición milenaria de la numerología con la Inteligencia Artificial, entregando informes digitales instantáneos a costo marginal casi cero.",
        "sobre_kpis": ["23 Productos", "14 Idiomas", "~5,3 Mil millones de hablantes", "IA Integrada", "DUNS 942242668"],
        "duns_titulo": "Credibilidad Internacional",
        "duns_texto": "El número DUNS 942242668, emitido por Dun & Bradstreet, es reconocido en más de 190 países y habilita contratos corporativos, licitaciones y joint ventures internacionales.",
        "mercado_titulo": "Oportunidad de Mercado",
        "mercado_texto": "Economía global de bienestar: US$ 6,8 billones (2024) a US$ 9,8 billones (2029). Apps de astrología/numerología: US$ 3B (2024) a US$ 9B (2030), CAGR 20%.",
        "problema_titulo": "El Problema",
        "problema_texto": "Las herramientas genéricas fallan al usuario y la mayoría cobra precios desconectados del poder adquisitivo local. A1ELOS lo corrige.",
        "solucao_titulo": "Nuestra Solución",
        "solucao_texto": "Numerología aplicada a escala: algoritmos propietarios + IA + entrega instantánea de PDFs premium en 14 idiomas.",
        "alcance_titulo": "Alcance Global",
        "alcance_texto": "14 idiomas cubriendo ~5,3 mil millones de hablantes (~67% de la población mundial).",
        "mercados_titulo": "3 Nuevos Mercados",
        "mercados_texto": "Indonesia (255M hablantes), Turquía (90M) y Vietnam (97M) — +442 millones de nuevos hablantes con poder adquisitivo mapeado.",
        "preco_titulo": "Precio Consciente",
        "preco_texto": "La misma proporción de valor para todas las monedas, calibrada por el poder adquisitivo (PPC) de cada país. Respeta la cultura y el bolsillo.",
        "portfolio_titulo": "Portafolio",
        "portfolio_texto": "23 productos en 4 niveles (Entrada R$ 8, Intermedio R$ 17, Avanzado R$ 26-35, Premium R$ 44-98) + segmento B2B.",
        "negocio_titulo": "Modelo de Negocio",
        "negocio_texto": "3 fuentes de ingresos: B2C (14 idiomas, todas las monedas), B2B (descuentos progresivos), Publicidad geolocalizada.",
        "banners_titulo": "Banners Publicitarios",
        "banners_texto": "Ingresos recurrentes mensuales: País R$ 800, Continente R$ 1.800, Mundo R$ 3.500, Patrocinio Exclusivo R$ 6.000.",
        "b2b_titulo": "Paquetes Empresariales B2B",
        "b2b_texto": "Obsequio para empleados o clientes. Descuentos progresivos: 10% (10 códigos), 30% (100), 50% (500), 70% (1.000).",
        "projecoes_titulo": "Proyecciones Financieras",
        "projecoes_texto": "Año 1: R$ 33k-130k | Año 5: R$ 500k-1,5M | Año 10: R$ 3-8M | Año 20: R$ 15-40M | Año 50: R$ 75-250M.",
        "tracao_titulo": "Tracción y Resultados",
        "tracao_texto": "12K+ usuarios activos, 87% de retención, 4,8★ de evaluación, 23 socios B2B.",
        "roteiro_titulo": "Hoja de Ruta Estratégica",
        "roteiro_texto": "Consolidación, Expansión (Indonesia, Turquía, Vietnam), Entrada Global y Liderazgo (20+ países + IPO).",
        "invest_titulo": "Inversión y Contacto",
        "invest_texto": "Ronda Seed R$ 3,5M · Valoración R$ 14M · Equity hasta 20%. Contacto: a1elos.consultoria@gmail.com · www.a1elos.com",
        "frase_final": "Los números nunca mienten — y apuntan a una oportunidad extraordinaria."
    },
    "it": {
        "titulo": "A1ELOS Global Numerology",
        "subtitulo": "La scienza dei numeri applicata al tuo successo",
        "capa_nota": "Presentazione per Investitori e Partner",
        "confidencial": "CONFIDENZIALE",
        "ano": "2026",
        "sobre_titulo": "Chi è A1ELOS",
        "sobre_texto": "Holding di tecnologia e conoscenza che unisce la tradizione millenaria della numerologia all'Intelligenza Artificiale, consegnando report digitali istantanei a costo marginale quasi zero.",
        "sobre_kpis": ["23 Prodotti", "14 Lingue", "~5,3 Miliardi di parlanti", "IA Integrata", "DUNS 942242668"],
        "duns_titulo": "Credibilità Internazionale",
        "duns_texto": "Il numero DUNS 942242668, emesso da Dun & Bradstreet, è riconosciuto in oltre 190 paesi e abilita contratti aziendali, gare e joint venture internazionali.",
        "mercado_titulo": "Opportunità di Mercato",
        "mercado_texto": "Economia globale del benessere: US$ 6,8 trilioni (2024) a US$ 9,8 trilioni (2029). App di astrologia/numerologia: US$ 3B (2024) a US$ 9B (2030), CAGR 20%.",
        "problema_titulo": "Il Problema",
        "problema_texto": "Gli strumenti generici falliscono l'utente e la maggior parte applica prezzi scollegati dal potere d'acquisto locale. A1ELOS lo corregge.",
        "solucao_titulo": "La Nostra Soluzione",
        "solucao_texto": "Numerologia applicata su scala: algoritmi proprietari + IA + consegna istantanea di PDF premium in 14 lingue.",
        "alcance_titulo": "Portata Globale",
        "alcance_texto": "14 lingue che coprono ~5,3 miliardi di parlanti (~67% della popolazione mondiale).",
        "mercados_titulo": "3 Nuovi Mercati",
        "mercados_texto": "Indonesia (255M parlanti), Turchia (90M) e Vietnam (97M) — +442 milioni di nuovi parlanti con potere d'acquisto mappato.",
        "preco_titulo": "Prezzo Consapevole",
        "preco_texto": "La stessa proporzione di valore per tutte le valute, calibrata sul potere d'acquisto (PPA) di ogni paese. Rispetta cultura e portafoglio.",
        "portfolio_titulo": "Portafoglio",
        "portfolio_texto": "23 prodotti in 4 livelli (Ingresso R$ 8, Intermedio R$ 17, Avanzato R$ 26-35, Premium R$ 44-98) + segmento B2B.",
        "negocio_titulo": "Modello di Business",
        "negocio_texto": "3 fonti di ricavo: B2C (14 lingue, tutte le valute), B2B (sconti progressivi), Pubblicità geolocalizzata.",
        "banners_titulo": "Banner Pubblicitari",
        "banners_texto": "Ricavi ricorrenti mensili: Paese R$ 800, Continente R$ 1.800, Mondo R$ 3.500, Sponsorizzazione Esclusiva R$ 6.000.",
        "b2b_titulo": "Pacchetti Aziendali B2B",
        "b2b_texto": "Regalo per dipendenti o clienti. Sconti progressivi: 10% (10 codici), 30% (100), 50% (500), 70% (1.000).",
        "projecoes_titulo": "Proiezioni Finanziarie",
        "projecoes_texto": "Anno 1: R$ 33k-130k | Anno 5: R$ 500k-1,5M | Anno 10: R$ 3-8M | Anno 20: R$ 15-40M | Anno 50: R$ 75-250M.",
        "tracao_titulo": "Trazione e Risultati",
        "tracao_texto": "12K+ utenti attivi, 87% di retention, 4,8★ di valutazione, 23 partner B2B.",
        "roteiro_titulo": "Roadmap Strategica",
        "roteiro_texto": "Consolidamento, Espansione (Indonesia, Turchia, Vietnam), Ingresso Globale e Leadership (20+ paesi + IPO).",
        "invest_titulo": "Investimento e Contatto",
        "invest_texto": "Round Seed R$ 3,5M · Valutazione R$ 14M · Equity fino al 20%. Contatto: a1elos.consultoria@gmail.com · www.a1elos.com",
        "frase_final": "I numeri non mentono mai — e indicano un'opportunità straordinaria."
    },
    "fr": {
        "titulo": "A1ELOS Global Numerology",
        "subtitulo": "La science des nombres appliquée à votre succès",
        "capa_nota": "Présentation pour Investisseurs et Partenaires",
        "confidencial": "CONFIDENTIEL",
        "ano": "2026",
        "sobre_titulo": "À propos d'A1ELOS",
        "sobre_texto": "Holding de technologie et de connaissance qui unit la tradition millénaire de la numérologie à l'Intelligence Artificielle, livrant des rapports numériques instantanés à coût marginal quasi nul.",
        "sobre_kpis": ["23 Produits", "14 Langues", "~5,3 Milliards de locuteurs", "IA Intégrée", "DUNS 942242668"],
        "duns_titulo": "Crédibilité Internationale",
        "duns_texto": "Le numéro DUNS 942242668, émis par Dun & Bradstreet, est reconnu dans plus de 190 pays et permet des contrats d'entreprise, des appels d'offres et des joint ventures internationaux.",
        "mercado_titulo": "Opportunité de Marché",
        "mercado_texto": "Économie mondiale du bien-être : 6,8 billions US$ (2024) à 9,8 billions US$ (2029). Apps d'astrologie/numérologie : 3B US$ (2024) à 9B US$ (2030), CAGR 20%.",
        "problema_titulo": "Le Problème",
        "problema_texto": "Les outils génériques échouent face à l'utilisateur et la plupart facturent des prix déconnectés du pouvoir d'achat local. A1ELOS corrige cela.",
        "solucao_titulo": "Notre Solution",
        "solucao_texto": "Numérologie appliquée à grande échelle : algorithmes propriétaires + IA + livraison instantanée de PDF premium en 14 langues.",
        "alcance_titulo": "Portée Mondiale",
        "alcance_texto": "14 langues couvrant ~5,3 milliards de locuteurs (~67% de la population mondiale).",
        "mercados_titulo": "3 Nouveaux Marchés",
        "mercados_texto": "Indonésie (255M locuteurs), Turquie (90M) et Vietnam (97M) — +442 millions de nouveaux locuteurs avec pouvoir d'achat cartographié.",
        "preco_titulo": "Prix Conscient",
        "preco_texto": "La même proportion de valeur pour toutes les devises, calibrée sur le pouvoir d'achat (PPA) de chaque pays. Respecte la culture et le portefeuille.",
        "portfolio_titulo": "Portefeuille",
        "portfolio_texto": "23 produits en 4 niveaux (Entrée R$ 8, Intermédiaire R$ 17, Avancé R$ 26-35, Premium R$ 44-98) + segment B2B.",
        "negocio_titulo": "Modèle d'Affaires",
        "negocio_texto": "3 sources de revenus : B2C (14 langues, toutes les devises), B2B (remises progressives), Publicité géolocalisée.",
        "banners_titulo": "Bannières Publicitaires",
        "banners_texto": "Revenus récurrents mensuels : Pays R$ 800, Continent R$ 1.800, Monde R$ 3.500, Parrainage Exclusif R$ 6.000.",
        "b2b_titulo": "Forfaits Entreprises B2B",
        "b2b_texto": "Cadeau pour employés ou clients. Remises progressives : 10% (10 codes), 30% (100), 50% (500), 70% (1.000).",
        "projecoes_titulo": "Projections Financières",
        "projecoes_texto": "Année 1 : R$ 33k-130k | Année 5 : R$ 500k-1,5M | Année 10 : R$ 3-8M | Année 20 : R$ 15-40M | Année 50 : R$ 75-250M.",
        "tracao_titulo": "Traction et Résultats",
        "tracao_texto": "12K+ utilisateurs actifs, 87% de rétention, 4,8★ de note, 23 partenaires B2B.",
        "roteiro_titulo": "Feuille de Route Stratégique",
        "roteiro_texto": "Consolidation, Expansion (Indonésie, Turquie, Vietnam), Entrée Mondiale et Leadership (20+ pays + IPO).",
        "invest_titulo": "Investissement et Contact",
        "invest_texto": "Round Seed R$ 3,5M · Valorisation R$ 14M · Equity jusqu'à 20%. Contact : a1elos.consultoria@gmail.com · www.a1elos.com",
        "frase_final": "Les nombres ne mentent jamais — et ils pointent vers une opportunité extraordinaire."
    },
    "de": {
        "titulo": "A1ELOS Global Numerology",
        "subtitulo": "Die Wissenschaft der Zahlen, angewendet auf Ihren Erfolg",
        "capa_nota": "Präsentation für Investoren und Partner",
        "confidencial": "VERTRAULICH",
        "ano": "2026",
        "sobre_titulo": "Über A1ELOS",
        "sobre_texto": "Ein Technologie- und Wissensunternehmen, das die jahrtausendealte Tradition der Numerologie mit Künstlicher Intelligenz verbindet und digitale Berichte zu nahezu null Grenzkosten liefert.",
        "sobre_kpis": ["23 Produkte", "14 Sprachen", "~5,3 Milliarden Sprecher", "Integrierte KI", "DUNS 942242668"],
        "duns_titulo": "Internationale Glaubwürdigkeit",
        "duns_texto": "Die DUNS-Nummer 942242668, ausgestellt von Dun & Bradstreet, ist in über 190 Ländern anerkannt und ermöglicht Unternehmensverträge, Ausschreibungen und internationale Joint Ventures.",
        "mercado_titulo": "Marktchance",
        "mercado_texto": "Globale Wellness-Wirtschaft: 6,8 Billionen US$ (2024) auf 9,8 Billionen US$ (2029). Astrologie/Numerologie-Apps: 3 Mrd. US$ (2024) auf 9 Mrd. US$ (2030), CAGR 20%.",
        "problema_titulo": "Das Problem",
        "problema_texto": "Generische Tools versagen beim Nutzer und die meisten verlangen Preise ohne Bezug zur lokalen Kaufkraft. A1ELOS behebt das.",
        "solucao_titulo": "Unsere Lösung",
        "solucao_texto": "Numerologie in großem Maßstab: proprietäre Algorithmen + KI + sofortige Lieferung von Premium-PDFs in 14 Sprachen.",
        "alcance_titulo": "Globale Reichweite",
        "alcance_texto": "14 Sprachen, die ~5,3 Milliarden Sprecher abdecken (~67% der Weltbevölkerung).",
        "mercados_titulo": "3 Neue Märkte",
        "mercados_texto": "Indonesien (255M Sprecher), Türkei (90M) und Vietnam (97M) — +442 Millionen neue Sprecher mit kartierter Kaufkraft.",
        "preco_titulo": "Bewusste Preisgestaltung",
        "preco_texto": "Das gleiche Wertverhältnis für alle Währungen, kalibriert auf die Kaufkraft (KKP) jedes Landes. Respektiert Kultur und Geldbeutel.",
        "portfolio_titulo": "Portfolio",
        "portfolio_texto": "23 Produkte in 4 Stufen (Einstieg R$ 8, Mittel R$ 17, Fortgeschritten R$ 26-35, Premium R$ 44-98) + B2B-Segment.",
        "negocio_titulo": "Geschäftsmodell",
        "negocio_texto": "3 Einnahmequellen: B2C (14 Sprachen, alle Währungen), B2B (gestaffelte Rabatte), Geolokalisierte Werbung.",
        "banners_titulo": "Werbe-Banner",
        "banners_texto": "Wiederkehrende Monatseinnahmen: Land R$ 800, Kontinent R$ 1.800, Welt R$ 3.500, Exklusiv-Sponsoring R$ 6.000.",
        "b2b_titulo": "B2B-Unternehmenspakete",
        "b2b_texto": "Geschenk für Mitarbeiter oder Kunden. Gestaffelte Rabatte: 10% (10 Codes), 30% (100), 50% (500), 70% (1.000).",
        "projecoes_titulo": "Finanzprognosen",
        "projecoes_texto": "Jahr 1: R$ 33k-130k | Jahr 5: R$ 500k-1,5M | Jahr 10: R$ 3-8M | Jahr 20: R$ 15-40M | Jahr 50: R$ 75-250M.",
        "tracao_titulo": "Traction und Ergebnisse",
        "tracao_texto": "12K+ aktive Nutzer, 87% Retention, 4,8★ Bewertung, 23 B2B-Partner.",
        "roteiro_titulo": "Strategische Roadmap",
        "roteiro_texto": "Konsolidierung, Expansion (Indonesien, Türkei, Vietnam), Globaler Eintritt und Führung (20+ Länder + IPO).",
        "invest_titulo": "Investition und Kontakt",
        "invest_texto": "Seed-Runde R$ 3,5M · Bewertung R$ 14M · Equity bis 20%. Kontakt: a1elos.consultoria@gmail.com · www.a1elos.com",
        "frase_final": "Zahlen lügen nie — und sie zeigen auf eine außergewöhnliche Gelegenheit."
    },
        "ru": {
        "titulo": "A1ELOS Global Numerology",
        "subtitulo": "Наука чисел, применённая к вашему успеху",
        "capa_nota": "Презентация для инвесторов и партнёров",
        "confidencial": "КОНФИДЕНЦИАЛЬНО",
        "ano": "2026",
        "sobre_titulo": "О компании A1ELOS",
        "sobre_texto": "Технологический и интеллектуальный холдинг, объединяющий многовековую традицию нумерологии с искусственным интеллектом и доставляющий мгновенные цифровые отчёты с почти нулевой себестоимостью.",
        "sobre_kpis": ["23 продукта", "14 языков", "~5,3 млрд носителей", "Интегрированный ИИ", "DUNS 942242668"],
        "duns_titulo": "Международная надёжность",
        "duns_texto": "Номер DUNS 942242668, выданный Dun & Bradstreet, признан более чем в 190 странах и позволяет заключать корпоративные контракты, участвовать в тендерах и международных совместных предприятиях.",
        "mercado_titulo": "Рыночная возможность",
        "mercado_texto": "Мировая экономика благополучия: 6,8 трлн долл. (2024) до 9,8 трлн долл. (2029). Приложения астрологии/нумерологии: 3 млрд (2024) до 9 млрд (2030), CAGR 20%.",
        "problema_titulo": "Проблема",
        "problema_texto": "Универсальные инструменты не оправдывают ожиданий, а большинство устанавливает цены, не учитывающие местную покупательную способность. A1ELOS исправляет это.",
        "solucao_titulo": "Наше решение",
        "solucao_texto": "Нумерология в масштабе: собственные алгоритмы + ИИ + мгновенная доставка премиальных PDF на 14 языках.",
        "alcance_titulo": "Глобальный охват",
        "alcance_texto": "14 языков, охватывающих ~5,3 млрд носителей (~67% населения мира).",
        "mercados_titulo": "3 новых рынка",
        "mercados_texto": "Индонезия (255 млн), Турция (90 млн) и Вьетнам (97 млн) — +442 млн новых носителей с учётом покупательной способности.",
        "preco_titulo": "Осознанное ценообразование",
        "preco_texto": "Одинаковая пропорция ценности для всех валют, откалиброванная по покупательной способности (ППС) каждой страны. Уважает культуру и кошелёк.",
        "portfolio_titulo": "Портфель",
        "portfolio_texto": "23 продукта в 4 уровнях (Вход R$ 8, Средний R$ 17, Продвинутый R$ 26-35, Премиум R$ 44-98) + сегмент B2B.",
        "negocio_titulo": "Бизнес-модель",
        "negocio_texto": "3 источника дохода: B2C (14 языков, все валюты), B2B (прогрессивные скидки), Геолокализованная реклама.",
        "banners_titulo": "Рекламные баннеры",
        "banners_texto": "Регулярный ежемесячный доход: Страна R$ 800, Континент R$ 1.800, Мир R$ 3.500, Эксклюзивное спонсорство R$ 6.000.",
        "b2b_titulo": "Корпоративные пакеты B2B",
        "b2b_texto": "Подарок для сотрудников или клиентов. Прогрессивные скидки: 10% (10 кодов), 30% (100), 50% (500), 70% (1.000).",
        "projecoes_titulo": "Финансовые прогнозы",
        "projecoes_texto": "Год 1: R$ 33k-130k | Год 5: R$ 500k-1,5M | Год 10: R$ 3-8M | Год 20: R$ 15-40M | Год 50: R$ 75-250M.",
        "tracao_titulo": "Тяга и результаты",
        "tracao_texto": "12K+ активных пользователей, 87% удержания, 4,8★ рейтинг, 23 партнёра B2B.",
        "roteiro_titulo": "Стратегическая дорожная карта",
        "roteiro_texto": "Консолидация, Расширение (Индонезия, Турция, Вьетнам), Глобальный вход и Лидерство (20+ стран + IPO).",
        "invest_titulo": "Инвестиции и контакты",
        "invest_texto": "Посевной раунд R$ 3,5M · Оценка R$ 14M · Доля до 20%. Контакт: a1elos.consultoria@gmail.com · www.a1elos.com",
        "frase_final": "Числа никогда не лгут — и указывают на необычайную возможность."
    },
    "zh": {
        "titulo": "A1ELOS 全球数字命理学",
        "subtitulo": "数字科学，成就您的成功",
        "capa_nota": "投资者与合作伙伴演示",
        "confidencial": "机密",
        "ano": "2026",
        "sobre_titulo": "关于 A1ELOS",
        "sobre_texto": "一家技术与知识控股公司，将数字命理学的千年传统与人工智能相结合，以接近零的边际成本交付即时数字报告。",
        "sobre_kpis": ["23 种产品", "14 种语言", "约53亿使用者", "集成AI", "DUNS 942242668"],
        "duns_titulo": "国际信誉",
        "duns_texto": "由邓白氏（Dun & Bradstreet）颁发的 DUNS 编号 942242668 在190多个国家得到认可，可开展企业合同、国际招标和合资企业。",
        "mercado_titulo": "市场机遇",
        "mercado_texto": "全球健康经济：6.8万亿美元（2024年）增至9.8万亿美元（2029年）。占星/数字命理应用：30亿美元（2024年）增至90亿美元（2030年），年复合增长率20%。",
        "problema_titulo": "问题",
        "problema_texto": "通用工具无法满足用户需求，多数收费脱离当地购买力。A1ELOS 解决了这一点。",
        "solucao_titulo": "我们的解决方案",
        "solucao_texto": "大规模应用数字命理学：专有算法 + AI + 以14种语言即时交付高级PDF。",
        "alcance_titulo": "全球覆盖",
        "alcance_texto": "14种语言覆盖约53亿使用者（约占世界人口的67%）。",
        "mercados_titulo": "3个新市场",
        "mercados_texto": "印度尼西亚（2.55亿使用者）、土耳其（9000万）和越南（9700万）——新增4.42亿使用者，购买力已测绘。",
        "preco_titulo": "理性定价",
        "preco_texto": "所有货币保持相同的价值比例，根据各国购买力（PPP）校准。尊重文化和钱包。",
        "portfolio_titulo": "产品组合",
        "portfolio_texto": "23种产品，4个层级（入门 R$ 8，中级 R$ 17，高级 R$ 26-35，尊享 R$ 44-98）+ B2B 板块。",
        "negocio_titulo": "商业模式",
        "negocio_texto": "3个收入来源：B2C（14种语言，所有货币）、B2B（阶梯折扣）、地域定向广告。",
        "banners_titulo": "广告横幅",
        "banners_texto": "每月经常性收入：国家 R$ 800，大洲 R$ 1,800，全球 R$ 3,500，独家赞助 R$ 6,000。",
        "b2b_titulo": "B2B 企业套餐",
        "b2b_texto": "员工或客户礼品。阶梯折扣：10%（10个代码），30%（100个），50%（500个），70%（1,000个）。",
        "projecoes_titulo": "财务预测",
        "projecoes_texto": "第1年：R$ 33k-130k | 第5年：R$ 500k-150万 | 第10年：R$ 300万-800万 | 第20年：R$ 1500万-4000万 | 第50年：R$ 7500万-2.5亿。",
        "tracao_titulo": "牵引力与成果",
        "tracao_texto": "12,000+ 活跃用户，87% 留存率，4.8★ 评分，23个 B2B 合作伙伴。",
        "roteiro_titulo": "战略路线图",
        "roteiro_texto": "整合、扩张（印度尼西亚、土耳其、越南）、全球进入和领导地位（20+ 国家 + IPO）。",
        "invest_titulo": "投资与联系",
        "invest_texto": "种子轮 R$ 350万 · 估值 R$ 1400万 · 股权最高20%。联系：a1elos.consultoria@gmail.com · www.a1elos.com",
        "frase_final": "数字从不说谎——它们指向一个非凡的机遇。"
    },
    "ja": {
        "titulo": "A1ELOS グローバル数秘術",
        "subtitulo": "数字の科学をあなたの成功に",
        "capa_nota": "投資家・パートナー向けプレゼンテーション",
        "confidencial": "機密",
        "ano": "2026",
        "sobre_titulo": "A1ELOSについて",
        "sobre_texto": "数秘術の千年にわたる伝統と人工知能を融合し、限界費用ほぼゼロで即時のデジタルレポートを提供するテクノロジー・ナレッジホールディングです。",
        "sobre_kpis": ["23製品", "14言語", "約53億人の話者", "統合AI", "DUNS 942242668"],
        "duns_titulo": "国際的な信頼性",
        "duns_texto": "Dun & Bradstreetが発行するDUNS番号942242668は190か国以上で認められ、企業契約、国際入札、合弁事業を可能にします。",
        "mercado_titulo": "市場機会",
        "mercado_texto": "世界のウェルネス経済：6.8兆ドル（2024年）から9.8兆ドル（2029年）。占星術・数秘術アプリ：30億ドル（2024年）から90億ドル（2030年）、CAGR 20%。",
        "problema_titulo": "課題",
        "problema_texto": "汎用ツールはユーザーを失望させ、多くは現地の購買力を無視した価格を設定しています。A1ELOSはこれを解決します。",
        "solucao_titulo": "私たちのソリューション",
        "solucao_texto": "数秘術の大規模応用：独自アルゴリズム + AI + 14言語でのプレミアムPDFの即時提供。",
        "alcance_titulo": "グローバルな到達範囲",
        "alcance_texto": "14言語で約53億人の話者（世界人口の約67%）をカバー。",
        "mercados_titulo": "3つの新市場",
        "mercados_texto": "インドネシア（2.55億人）、トルコ（9000万人）、ベトナム（9700万人）——購買力をマッピングした新規話者4.42億人。",
        "preco_titulo": "意識的な価格設定",
        "preco_texto": "すべての通貨で同じ価値の割合を、各国の購買力（PPP）に合わせて調整。文化と財布を尊重します。",
        "portfolio_titulo": "ポートフォリオ",
        "portfolio_texto": "23製品を4段階（エントリー R$ 8、ミドル R$ 17、アドバンス R$ 26-35、プレミアム R$ 44-98）+ B2Bセグメント。",
        "negocio_titulo": "ビジネスモデル",
        "negocio_texto": "3つの収益源：B2C（14言語、全通貨）、B2B（段階的割引）、地域ターゲット広告。",
        "banners_titulo": "広告バナー",
        "banners_texto": "毎月の経常収益：国 R$ 800、大陸 R$ 1,800、世界 R$ 3,500、独占スポンサー R$ 6,000。",
        "b2b_titulo": "B2B法人パッケージ",
        "b2b_texto": "従業員や顧客へのギフト。段階的割引：10%（10コード）、30%（100）、50%（500）、70%（1,000）。",
        "projecoes_titulo": "財務予測",
        "projecoes_texto": "1年目：R$ 33k-130k | 5年目：R$ 50万-150万 | 10年目：R$ 300万-800万 | 20年目：R$ 1500万-4000万 | 50年目：R$ 7500万-2.5億。",
        "tracao_titulo": "実績と成果",
        "tracao_texto": "12,000+ アクティブユーザー、87% リテンション、4.8★ 評価、23のB2Bパートナー。",
        "roteiro_titulo": "戦略ロードマップ",
        "roteiro_texto": "統合、拡大（インドネシア、トルコ、ベトナム）、グローバル参入、リーダーシップ（20か国以上 + IPO）。",
        "invest_titulo": "投資と連絡先",
        "invest_texto": "シードラウンド R$ 350万 · 評価額 R$ 1400万 · 株式最大20%。連絡先：a1elos.consultoria@gmail.com · www.a1elos.com",
        "frase_final": "数字は決して嘘をつかない——そして非凡な機会を指し示しています。"
    },
    "ar": {
        "titulo": "A1ELOS علم الأعداد العالمي",
        "subtitulo": "علم الأرقام المطبق على نجاحك",
        "capa_nota": "عرض تقديمي للمستثمرين والشركاء",
        "confidencial": "سري",
        "ano": "2026",
        "sobre_titulo": "عن A1ELOS",
        "sobre_texto": "شركة قابضة للتقنية والمعرفة تجمع بين التقاليد العريقة لعلم الأعداد والذكاء الاصطناعي، وتقدم تقارير رقمية فورية بتكلفة هامشية شبه معدومة.",
        "sobre_kpis": ["23 منتجاً", "14 لغة", "~5.3 مليار متحدث", "ذكاء اصطناعي مدمج", "DUNS 942242668"],
        "duns_titulo": "المصداقية الدولية",
        "duns_texto": "رقم DUNS 942242668 الصادر عن Dun & Bradstreet معترف به في أكثر من 190 دولة، ويتيح العقود المؤسسية والمناقصات والمشاريع المشتركة الدولية.",
        "mercado_titulo": "فرصة السوق",
        "mercado_texto": "الاقتصاد العالمي للعافية: 6.8 تريليون دولار (2024) إلى 9.8 تريليون (2029). تطبيقات علم الأعداد/التنجيم: 3 مليارات (2024) إلى 9 مليارات (2030)، نمو سنوي 20%.",
        "problema_titulo": "المشكلة",
        "problema_texto": "الأدوات العامة تخذل المستخدم، ومعظمها يفرض أسعاراً لا تراعي القوة الشرائية المحلية. A1ELOS يصحح ذلك.",
        "solucao_titulo": "حلنا",
        "solucao_texto": "علم الأعداد على نطاق واسع: خوارزميات خاصة + ذكاء اصطناعي + تسليم فوري لملفات PDF متميزة بـ14 لغة.",
        "alcance_titulo": "الانتشار العالمي",
        "alcance_texto": "14 لغة تغطي ~5.3 مليار متحدث (~67% من سكان العالم).",
        "mercados_titulo": "3 أسواق جديدة",
        "mercados_texto": "إندونيسيا (255 مليون متحدث)، تركيا (90 مليون) وفيتنام (97 مليون) — +442 مليون متحدث جديد مع قوة شرائية محسوبة.",
        "preco_titulo": "تسعير واعٍ",
        "preco_texto": "نفس نسبة القيمة لجميع العملات، معايرة حسب القوة الشرائية (PPP) لكل بلد. يحترم الثقافة والميزانية.",
        "portfolio_titulo": "المحفظة",
        "portfolio_texto": "23 منتجاً في 4 مستويات (دخول R$ 8، متوسط R$ 17، متقدم R$ 26-35، متميز R$ 44-98) + قطاع B2B.",
        "negocio_titulo": "نموذج الأعمال",
        "negocio_texto": "3 مصادر إيرادات: B2C (14 لغة، كل العملات)، B2B (خصومات تصاعدية)، إعلانات جغرافية مستهدفة.",
        "banners_titulo": "اللافتات الإعلانية",
        "banners_texto": "إيرادات شهرية متكررة: دولة R$ 800، قارة R$ 1,800، عالم R$ 3,500، رعاية حصرية R$ 6,000.",
        "b2b_titulo": "باقات الشركات B2B",
        "b2b_texto": "هدية للموظفين أو العملاء. خصومات تصاعدية: 10% (10 رموز)، 30% (100)، 50% (500)، 70% (1,000).",
        "projecoes_titulo": "التوقعات المالية",
        "projecoes_texto": "السنة 1: R$ 33k-130k | السنة 5: R$ 500k-1.5M | السنة 10: R$ 3-8M | السنة 20: R$ 15-40M | السنة 50: R$ 75-250M.",
        "tracao_titulo": "الزخم والنتائج",
        "tracao_texto": "+12 ألف مستخدم نشط، 87% احتفاظ، تقييم 4.8★، 23 شريكاً B2B.",
        "roteiro_titulo": "خارطة الطريق الاستراتيجية",
        "roteiro_texto": "توحيد، توسع (إندونيسيا، تركيا، فيتنام)، دخول عالمي وقيادة (+20 دولة + اكتتاب).",
        "invest_titulo": "الاستثمار والتواصل",
        "invest_texto": "جولة أولية R$ 3.5M · تقييم R$ 14M · حصة حتى 20%. التواصل: a1elos.consultoria@gmail.com · www.a1elos.com",
        "frase_final": "الأرقام لا تكذب أبداً — وهي تشير إلى فرصة استثنائية."
    },
    "he": {
        "titulo": "A1ELOS נומרולוגיה גלובלית",
        "subtitulo": "מדע המספרים מיושם להצלחתך",
        "capa_nota": "מצגת למשקיעים ושותפים",
        "confidencial": "סודי",
        "ano": "2026",
        "sobre_titulo": "אודות A1ELOS",
        "sobre_texto": "חברת החזקות לטכנולוגיה וידע המשלבת את המסורת העתיקה של הנומרולוגיה עם בינה מלאכותית, ומספקת דוחות דיגיטליים מיידיים בעלות שולית כמעט אפסית.",
        "sobre_kpis": ["23 מוצרים", "14 שפות", "~5.3 מיליארד דוברים", "בינה מלאכותית משולבת", "DUNS 942242668"],
        "duns_titulo": "אמינות בינלאומית",
        "duns_texto": "מספר DUNS 942242668 שהונפק על ידי Dun & Bradstreet מוכר ביותר מ-190 מדינות ומאפשר חוזים עסקיים, מכרזים ומיזמים משותפים בינלאומיים.",
        "mercado_titulo": "הזדמנות שוק",
        "mercado_texto": "כלכלת הבריאות העולמית: 6.8 טריליון דולר (2024) ל-9.8 טריליון (2029). אפליקציות אסטרולוגיה/נומרולוגיה: 3 מיליארד (2024) ל-9 מיליארד (2030), צמיחה שנתית 20%.",
        "problema_titulo": "הבעיה",
        "problema_texto": "כלים גנריים מאכזבים את המשתמש, ורובם גובים מחירים שאינם מתחשבים בכוח הקנייה המקומי. A1ELOS מתקן זאת.",
        "solucao_titulo": "הפתרון שלנו",
        "solucao_texto": "נומרולוגיה בקנה מידה: אלגוריתמים קנייניים + בינה מלאכותית + אספקה מיידית של PDF יוקרתי ב-14 שפות.",
        "alcance_titulo": "טווח גלובלי",
        "alcance_texto": "14 שפות המכסות ~5.3 מיליארד דוברים (~67% מאוכלוסיית העולם).",
        "mercados_titulo": "3 שווקים חדשים",
        "mercados_texto": "אינדונזיה (255 מיליון דוברים), טורקיה (90 מיליון) ווייטנאם (97 מיליון) — +442 מיליון דוברים חדשים עם כוח קנייה ממופה.",
        "preco_titulo": "תמחור מודע",
        "preco_texto": "אותו יחס ערך לכל המטבעות, מכויל לפי כוח הקנייה (PPP) של כל מדינה. מכבד תרבות וארנק.",
        "portfolio_titulo": "פורטפוליו",
        "portfolio_texto": "23 מוצרים ב-4 רמות (כניסה R$ 8, בינוני R$ 17, מתקדם R$ 26-35, פרימיום R$ 44-98) + פלח B2B.",
        "negocio_titulo": "מודל עסקי",
        "negocio_texto": "3 מקורות הכנסה: B2C (14 שפות, כל המטבעות), B2B (הנחות מדורגות), פרסום ממוקד גיאוגרפית.",
        "banners_titulo": "באנרים פרסומיים",
        "banners_texto": "הכנסה חוזרת חודשית: מדינה R$ 800, יבשת R$ 1,800, עולם R$ 3,500, חסות בלעדית R$ 6,000.",
        "b2b_titulo": "חבילות עסקיות B2B",
        "b2b_texto": "מתנה לעובדים או ללקוחות. הנחות מדורגות: 10% (10 קודים), 30% (100), 50% (500), 70% (1,000).",
        "projecoes_titulo": "תחזיות פיננסיות",
        "projecoes_texto": "שנה 1: R$ 33k-130k | שנה 5: R$ 500k-1.5M | שנה 10: R$ 3-8M | שנה 20: R$ 15-40M | שנה 50: R$ 75-250M.",
        "tracao_titulo": "מומנטום ותוצאות",
        "tracao_texto": "+12 אלף משתמשים פעילים, 87% שימור, דירוג 4.8★, 23 שותפי B2B.",
        "roteiro_titulo": "מפת דרכים אסטרטגית",
        "roteiro_texto": "איחוד, התרחבות (אינדונזיה, טורקיה, וייטנאם), כניסה גלובלית ומנהיגות (+20 מדינות + הנפקה).",
        "invest_titulo": "השקעה ויצירת קשר",
        "invest_texto": "סבב ראשוני R$ 3.5M · שווי R$ 14M · הון עד 20%. יצירת קשר: a1elos.consultoria@gmail.com · www.a1elos.com",
        "frase_final": "המספרים אף פעם לא משקרים — והם מצביעים על הזדמנות יוצאת דופן."
    },
        "id": {
        "titulo": "A1ELOS Numerologi Global",
        "subtitulo": "Ilmu angka yang diterapkan untuk kesuksesan Anda",
        "capa_nota": "Presentasi untuk Investor dan Mitra",
        "confidencial": "RAHASIA",
        "ano": "2026",
        "sobre_titulo": "Tentang A1ELOS",
        "sobre_texto": "Holding teknologi dan pengetahuan yang menggabungkan tradisi kuno numerologi dengan Kecerdasan Buatan, menghadirkan laporan digital instan dengan biaya marjinal hampir nol.",
        "sobre_kpis": ["23 Produk", "14 Bahasa", "~5,3 Miliar penutur", "AI Terintegrasi", "DUNS 942242668"],
        "duns_titulo": "Kredibilitas Internasional",
        "duns_texto": "Nomor DUNS 942242668, diterbitkan oleh Dun & Bradstreet, diakui di lebih dari 190 negara dan memungkinkan kontrak korporasi, tender dan joint venture internasional.",
        "mercado_titulo": "Peluang Pasar",
        "mercado_texto": "Ekonomi kesehatan global: US$ 6,8 triliun (2024) menjadi US$ 9,8 triliun (2029). Aplikasi astrologi/numerologi: US$ 3 miliar (2024) menjadi US$ 9 miliar (2030), CAGR 20%.",
        "problema_titulo": "Masalah",
        "problema_texto": "Alat generik mengecewakan pengguna dan sebagian besar mematok harga yang tidak sesuai daya beli lokal. A1ELOS memperbaikinya.",
        "solucao_titulo": "Solusi Kami",
        "solucao_texto": "Numerologi dalam skala besar: algoritma proprietary + AI + pengiriman instan PDF premium dalam 14 bahasa.",
        "alcance_titulo": "Jangkauan Global",
        "alcance_texto": "14 bahasa mencakup ~5,3 miliar penutur (~67% populasi dunia).",
        "mercados_titulo": "3 Pasar Baru",
        "mercados_texto": "Indonesia (255 juta penutur), Turki (90 juta) dan Vietnam (97 juta) — +442 juta penutur baru dengan daya beli terpetakan.",
        "preco_titulo": "Harga Sadar",
        "preco_texto": "Proporsi nilai yang sama untuk semua mata uang, dikalibrasi dengan daya beli (PPP) setiap negara. Menghormati budaya dan kantong.",
        "portfolio_titulo": "Portofolio",
        "portfolio_texto": "23 produk dalam 4 tingkat (Masuk R$ 8, Menengah R$ 17, Lanjutan R$ 26-35, Premium R$ 44-98) + segmen B2B.",
        "negocio_titulo": "Model Bisnis",
        "negocio_texto": "3 sumber pendapatan: B2C (14 bahasa, semua mata uang), B2B (diskon progresif), Iklan geolokasi.",
        "banners_titulo": "Banner Iklan",
        "banners_texto": "Pendapatan bulanan berulang: Negara R$ 800, Benua R$ 1.800, Dunia R$ 3.500, Sponsor Eksklusif R$ 6.000.",
        "b2b_titulo": "Paket Korporasi B2B",
        "b2b_texto": "Hadiah untuk karyawan atau klien. Diskon progresif: 10% (10 kode), 30% (100), 50% (500), 70% (1.000).",
        "projecoes_titulo": "Proyeksi Keuangan",
        "projecoes_texto": "Tahun 1: R$ 33k-130k | Tahun 5: R$ 500k-1,5M | Tahun 10: R$ 3-8M | Tahun 20: R$ 15-40M | Tahun 50: R$ 75-250M.",
        "tracao_titulo": "Traction dan Hasil",
        "tracao_texto": "12K+ pengguna aktif, 87% retensi, rating 4,8★, 23 mitra B2B.",
        "roteiro_titulo": "Peta Jalan Strategis",
        "roteiro_texto": "Konsolidasi, Ekspansi (Indonesia, Turki, Vietnam), Masuk Global dan Kepemimpinan (20+ negara + IPO).",
        "invest_titulo": "Investasi dan Kontak",
        "invest_texto": "Putaran Seed R$ 3,5M · Valuasi R$ 14M · Ekuitas hingga 20%. Kontak: a1elos.consultoria@gmail.com · www.a1elos.com",
        "frase_final": "Angka tidak pernah berbohong — dan menunjuk pada peluang luar biasa."
    },
    "tr": {
        "titulo": "A1ELOS Küresel Numeroloji",
        "subtitulo": "Sayıların bilimi başarınıza uygulandı",
        "capa_nota": "Yatırımcılar ve Ortaklar için Sunum",
        "confidencial": "GİZLİ",
        "ano": "2026",
        "sobre_titulo": "A1ELOS Hakkında",
        "sobre_texto": "Numerolojinin kadim geleneğini Yapay Zekâ ile birleştiren, neredeyse sıfır marjinal maliyetle anında dijital raporlar sunan bir teknoloji ve bilgi holdingi.",
        "sobre_kpis": ["23 Ürün", "14 Dil", "~5,3 Milyar konuşmacı", "Entegre YZ", "DUNS 942242668"],
        "duns_titulo": "Uluslararası Güvenilirlik",
        "duns_texto": "Dun & Bradstreet tarafından verilen DUNS numarası 942242668, 190'dan fazla ülkede tanınır ve kurumsal sözleşmeler, ihaleler ve uluslararası ortak girişimler sağlar.",
        "mercado_titulo": "Pazar Fırsatı",
        "mercado_texto": "Küresel sağlıklı yaşam ekonomisi: 6,8 trilyon ABD$ (2024) ile 9,8 trilyon (2029). Astroloji/numeroloji uygulamaları: 3 milyar (2024) ile 9 milyar (2030), CAGR %20.",
        "problema_titulo": "Sorun",
        "problema_texto": "Genel araçlar kullanıcıyı hayal kırıklığına uğratır ve çoğu yerel satın alma gücünden kopuk fiyatlar uygular. A1ELOS bunu düzeltir.",
        "solucao_titulo": "Çözümümüz",
        "solucao_texto": "Numeroloji ölçekte uygulanır: özel algoritmalar + YZ + 14 dilde premium PDF'lerin anında teslimi.",
        "alcance_titulo": "Küresel Erişim",
        "alcance_texto": "14 dil, ~5,3 milyar konuşmacıyı kapsar (~dünya nüfusunun %67'si).",
        "mercados_titulo": "3 Yeni Pazar",
        "mercados_texto": "Endonezya (255 milyon konuşmacı), Türkiye (90 milyon) ve Vietnam (97 milyon) — satın alma gücü haritalanmış +442 milyon yeni konuşmacı.",
        "preco_titulo": "Bilinçli Fiyatlandırma",
        "preco_texto": "Tüm para birimleri için aynı değer oranı, her ülkenin satın alma gücüne (PPP) göre ayarlanır. Kültüre ve cüzdana saygı gösterir.",
        "portfolio_titulo": "Portföy",
        "portfolio_texto": "4 seviyede 23 ürün (Giriş R$ 8, Orta R$ 17, İleri R$ 26-35, Premium R$ 44-98) + B2B segmenti.",
        "negocio_titulo": "İş Modeli",
        "negocio_texto": "3 gelir kaynağı: B2C (14 dil, tüm para birimleri), B2B (kademeli indirimler), Coğrafi hedefli reklam.",
        "banners_titulo": "Reklam Bannerları",
        "banners_texto": "Aylık yinelenen gelir: Ülke R$ 800, Kıta R$ 1.800, Dünya R$ 3.500, Özel Sponsorluk R$ 6.000.",
        "b2b_titulo": "B2B Kurumsal Paketler",
        "b2b_texto": "Çalışanlar veya müşteriler için hediye. Kademeli indirimler: %10 (10 kod), %30 (100), %50 (500), %70 (1.000).",
        "projecoes_titulo": "Finansal Projeksiyonlar",
        "projecoes_texto": "Yıl 1: R$ 33k-130k | Yıl 5: R$ 500k-1,5M | Yıl 10: R$ 3-8M | Yıl 20: R$ 15-40M | Yıl 50: R$ 75-250M.",
        "tracao_titulo": "Çekiş ve Sonuçlar",
        "tracao_texto": "12K+ aktif kullanıcı, %87 elde tutma, 4,8★ puan, 23 B2B ortağı.",
        "roteiro_titulo": "Stratejik Yol Haritası",
        "roteiro_texto": "Konsolidasyon, Genişleme (Endonezya, Türkiye, Vietnam), Küresel Giriş ve Liderlik (20+ ülke + IPO).",
        "invest_titulo": "Yatırım ve İletişim",
        "invest_texto": "Tohum turu R$ 3,5M · Değerleme R$ 14M · %20'ye kadar hisse. İletişim: a1elos.consultoria@gmail.com · www.a1elos.com",
        "frase_final": "Sayılar asla yalan söylemez — ve olağanüstü bir fırsata işaret eder."
    },
    "vi": {
        "titulo": "A1ELOS Thần số học Toàn cầu",
        "subtitulo": "Khoa học về các con số áp dụng cho thành công của bạn",
        "capa_nota": "Trình bày cho Nhà đầu tư và Đối tác",
        "confidencial": "BẢO MẬT",
        "ano": "2026",
        "sobre_titulo": "Về A1ELOS",
        "sobre_texto": "Công ty mẹ về công nghệ và tri thức kết hợp truyền thống lâu đời của thần số học với Trí tuệ Nhân tạo, cung cấp báo cáo kỹ thuật số tức thì với chi phí biên gần bằng không.",
        "sobre_kpis": ["23 Sản phẩm", "14 Ngôn ngữ", "~5,3 Tỷ người nói", "AI Tích hợp", "DUNS 942242668"],
        "duns_titulo": "Uy tín Quốc tế",
        "duns_texto": "Số DUNS 942242668 do Dun & Bradstreet cấp, được công nhận tại hơn 190 quốc gia, cho phép hợp đồng doanh nghiệp, đấu thầu và liên doanh quốc tế.",
        "mercado_titulo": "Cơ hội Thị trường",
        "mercado_texto": "Kinh tế sức khỏe toàn cầu: 6,8 nghìn tỷ USD (2024) lên 9,8 nghìn tỷ (2029). Ứng dụng chiêm tinh/thần số: 3 tỷ (2024) lên 9 tỷ (2030), CAGR 20%.",
        "problema_titulo": "Vấn đề",
        "problema_texto": "Công cụ chung chung làm thất vọng người dùng và hầu hết định giá tách rời sức mua địa phương. A1ELOS khắc phục điều này.",
        "solucao_titulo": "Giải pháp của chúng tôi",
        "solucao_texto": "Thần số học áp dụng ở quy mô lớn: thuật toán độc quyền + AI + giao PDF cao cấp tức thì bằng 14 ngôn ngữ.",
        "alcance_titulo": "Phạm vi Toàn cầu",
        "alcance_texto": "14 ngôn ngữ bao phủ ~5,3 tỷ người nói (~67% dân số thế giới).",
        "mercados_titulo": "3 Thị trường Mới",
        "mercados_texto": "Indonesia (255 triệu người nói), Thổ Nhĩ Kỳ (90 triệu) và Việt Nam (97 triệu) — +442 triệu người nói mới với sức mua được lập bản đồ.",
        "preco_titulo": "Định giá Có ý thức",
        "preco_texto": "Cùng tỷ lệ giá trị cho mọi loại tiền tệ, hiệu chỉnh theo sức mua (PPP) của từng quốc gia. Tôn trọng văn hóa và túi tiền.",
        "portfolio_titulo": "Danh mục",
        "portfolio_texto": "23 sản phẩm ở 4 cấp (Cơ bản R$ 8, Trung cấp R$ 17, Nâng cao R$ 26-35, Cao cấp R$ 44-98) + phân khúc B2B.",
        "negocio_titulo": "Mô hình Kinh doanh",
        "negocio_texto": "3 nguồn doanh thu: B2C (14 ngôn ngữ, mọi loại tiền tệ), B2B (chiết khấu lũy tiến), Quảng cáo định vị địa lý.",
        "banners_titulo": "Banner Quảng cáo",
        "banners_texto": "Doanh thu định kỳ hàng tháng: Quốc gia R$ 800, Châu lục R$ 1.800, Thế giới R$ 3.500, Tài trợ Độc quyền R$ 6.000.",
        "b2b_titulo": "Gói Doanh nghiệp B2B",
        "b2b_texto": "Quà tặng cho nhân viên hoặc khách hàng. Chiết khấu lũy tiến: 10% (10 mã), 30% (100), 50% (500), 70% (1.000).",
        "projecoes_titulo": "Dự báo Tài chính",
        "projecoes_texto": "Năm 1: R$ 33k-130k | Năm 5: R$ 500k-1,5M | Năm 10: R$ 3-8M | Năm 20: R$ 15-40M | Năm 50: R$ 75-250M.",
        "tracao_titulo": "Đà tăng trưởng và Kết quả",
        "tracao_texto": "12K+ người dùng hoạt động, 87% giữ chân, đánh giá 4,8★, 23 đối tác B2B.",
        "roteiro_titulo": "Lộ trình Chiến lược",
        "roteiro_texto": "Củng cố, Mở rộng (Indonesia, Thổ Nhĩ Kỳ, Việt Nam), Gia nhập Toàn cầu và Lãnh đạo (20+ quốc gia + IPO).",
        "invest_titulo": "Đầu tư và Liên hệ",
        "invest_texto": "Vòng hạt giống R$ 3,5M · Định giá R$ 14M · Vốn cổ phần tối đa 20%. Liên hệ: a1elos.consultoria@gmail.com · www.a1elos.com",
        "frase_final": "Các con số không bao giờ nói dối — và chúng chỉ ra một cơ hội phi thường."
    }
}

# ------------------------------------------------------------
# 4b. DADOS NUMÉRICOS DAS TABELAS (idênticos em todos os idiomas)
# ------------------------------------------------------------
LINHAS_IDIOMAS = [
    ("Inglês", 1528), ("Mandarim", 1184), ("Espanhol", 558),
    ("Francês", 396), ("Árabe", 335), ("Português", 270),
    ("Russo", 255), ("Indonésio", 255), ("Alemão", 134),
    ("Japonês", 123), ("Vietnamita", 97), ("Turco", 90),
    ("Italiano", 85), ("Hebraico", 9),
]
LINHAS_BANNERS = [[800, "500"], [1800, "1.200"], [3500, "2.500"], [6000, "4.500"]]
LINHAS_B2B = [["10", "10%"], ["100", "30%"], ["500", "50%"], ["1.000", "70%"]]
HORIZONTES = [1, 3, 5, 10, 20, 30, 40, 50]
RANGES = [
    ("33k", "130k"), ("120k", "450k"), ("500k", "1,5M"),
    ("3M", "8M"), ("15M", "40M"), ("35M", "90M"),
    ("55M", "150M"), ("75M", "250M"),
]

TABELAS = {
    "pt": {"h_idioma": "Idioma", "h_falantes": "Falantes (mi)", "h_seg": "Segmentação",
           "h_fixo": "Fixo (R$/mês)", "h_temp": "Temporário (R$/mês)", "h_de": "A partir de",
           "h_desc": "Desconto", "h_hor": "Horizonte", "h_cons": "Conservador (R$)",
           "h_otim": "Otimista (R$)", "h_ano": "Ano",
           "seg": ["País", "Continente", "Mundo", "Patrocínio Exclusivo"]},
    "en": {"h_idioma": "Language", "h_falantes": "Speakers (M)", "h_seg": "Targeting",
           "h_fixo": "Fixed (R$/mo)", "h_temp": "Temporary (R$/mo)", "h_de": "From",
           "h_desc": "Discount", "h_hor": "Horizon", "h_cons": "Conservative (R$)",
           "h_otim": "Optimistic (R$)", "h_ano": "Yr",
           "seg": ["Country", "Continent", "World", "Exclusive Sponsorship"]},
    "es": {"h_idioma": "Idioma", "h_falantes": "Hablantes (M)", "h_seg": "Segmentación",
           "h_fixo": "Fijo (R$/mes)", "h_temp": "Temporal (R$/mes)", "h_de": "A partir de",
           "h_desc": "Descuento", "h_hor": "Horizonte", "h_cons": "Conservador (R$)",
           "h_otim": "Optimista (R$)", "h_ano": "Año",
           "seg": ["País", "Continente", "Mundo", "Patrocinio Exclusivo"]},
    "it": {"h_idioma": "Lingua", "h_falantes": "Parlanti (M)", "h_seg": "Segmentazione",
           "h_fixo": "Fisso (R$/mese)", "h_temp": "Temporaneo (R$/mese)", "h_de": "Da",
           "h_desc": "Sconto", "h_hor": "Orizzonte", "h_cons": "Conservativo (R$)",
           "h_otim": "Ottimista (R$)", "h_ano": "Anno",
           "seg": ["Paese", "Continente", "Mondo", "Sponsor Esclusivo"]},
    "fr": {"h_idioma": "Langue", "h_falantes": "Locuteurs (M)", "h_seg": "Ciblage",
           "h_fixo": "Fixe (R$/mois)", "h_temp": "Temporaire (R$/mois)", "h_de": "À partir de",
           "h_desc": "Remise", "h_hor": "Horizon", "h_cons": "Conservateur (R$)",
           "h_otim": "Optimiste (R$)", "h_ano": "An",
           "seg": ["Pays", "Continent", "Monde", "Parrainage Exclusif"]},
    "de": {"h_idioma": "Sprache", "h_falantes": "Sprecher (Mio.)", "h_seg": "Segmentierung",
           "h_fixo": "Fest (R$/Monat)", "h_temp": "Zeitweilig (R$/Monat)", "h_de": "Ab",
           "h_desc": "Rabatt", "h_hor": "Horizont", "h_cons": "Konservativ (R$)",
           "h_otim": "Optimistisch (R$)", "h_ano": "Jahr",
           "seg": ["Land", "Kontinent", "Welt", "Exklusiv-Sponsoring"]},
    "ru": {"h_idioma": "Язык", "h_falantes": "Носители (млн)", "h_seg": "Сегментация",
           "h_fixo": "Фикс. (R$/мес)", "h_temp": "Врем. (R$/мес)", "h_de": "От",
           "h_desc": "Скидка", "h_hor": "Горизонт", "h_cons": "Консерв. (R$)",
           "h_otim": "Оптим. (R$)", "h_ano": "Год",
           "seg": ["Страна", "Континент", "Мир", "Эксклюзивное спонсорство"]},
    "zh": {"h_idioma": "语言", "h_falantes": "使用者(百万)", "h_seg": "定向",
           "h_fixo": "固定(R$/月)", "h_temp": "临时(R$/月)", "h_de": "从",
           "h_desc": "折扣", "h_hor": "期限", "h_cons": "保守(R$)",
           "h_otim": "乐观(R$)", "h_ano": "年",
           "seg": ["国家", "大洲", "全球", "独家赞助"]},
    "ja": {"h_idioma": "言語", "h_falantes": "話者(百万)", "h_seg": "セグメント",
           "h_fixo": "固定(R$/月)", "h_temp": "臨時(R$/月)", "h_de": "から",
           "h_desc": "割引", "h_hor": "期間", "h_cons": "保守(R$)",
           "h_otim": "楽観(R$)", "h_ano": "年",
           "seg": ["国", "大陸", "世界", "独占スポンサー"]},
    "ar": {"h_idioma": "اللغة", "h_falantes": "المتحدثون (مليون)", "h_seg": "الاستهداف",
           "h_fixo": "ثابت (R$/شهر)", "h_temp": "مؤقت (R$/شهر)", "h_de": "من",
           "h_desc": "خصم", "h_hor": "الأفق", "h_cons": "متحفظ (R$)",
           "h_otim": "متفائل (R$)", "h_ano": "سنة",
           "seg": ["دولة", "قارة", "عالم", "رعاية حصرية"]},
    "he": {"h_idioma": "שפה", "h_falantes": "דוברים (מיליון)", "h_seg": "מיקוד",
           "h_fixo": "קבוע (R$/חודש)", "h_temp": "זמני (R$/חודש)", "h_de": "החל מ-",
           "h_desc": "הנחה", "h_hor": "אופק", "h_cons": "שמרני (R$)",
           "h_otim": "אופטימי (R$)", "h_ano": "שנה",
           "seg": ["מדינה", "יבשת", "עולם", "חסות בלעדית"]},
    "id": {"h_idioma": "Bahasa", "h_falantes": "Penutur (juta)", "h_seg": "Segmentasi",
           "h_fixo": "Tetap (R$/bln)", "h_temp": "Sementara (R$/bln)", "h_de": "Mulai dari",
           "h_desc": "Diskon", "h_hor": "Cakrawala", "h_cons": "Konservatif (R$)",
           "h_otim": "Optimis (R$)", "h_ano": "Tahun",
           "seg": ["Negara", "Benua", "Dunia", "Sponsor Eksklusif"]},
    "tr": {"h_idioma": "Dil", "h_falantes": "Konuşmacı (milyon)", "h_seg": "Hedefleme",
           "h_fixo": "Sabit (R$/ay)", "h_temp": "Geçici (R$/ay)", "h_de": "Şuradan",
           "h_desc": "İndirim", "h_hor": "Ufuk", "h_cons": "Muhafazakâr (R$)",
           "h_otim": "İyimser (R$)", "h_ano": "Yıl",
           "seg": ["Ülke", "Kıta", "Dünya", "Özel Sponsorluk"]},
    "vi": {"h_idioma": "Ngôn ngữ", "h_falantes": "Người nói (triệu)", "h_seg": "Nhắm mục tiêu",
           "h_fixo": "Cố định (R$/tháng)", "h_temp": "Tạm thời (R$/tháng)", "h_de": "Từ",
           "h_desc": "Chiết khấu", "h_hor": "Chân trời", "h_cons": "Bảo thủ (R$)",
           "h_otim": "Lạc quan (R$)", "h_ano": "Năm",
           "seg": ["Quốc gia", "Châu lục", "Thế giới", "Tài trợ độc quyền"]},
}

def gerar_pdf_texto(lang="pt", caminho_saida=None):
    """Gera a apresentação em formato de documento (texto) com capa e tabelas."""
    if lang not in CONTEUDO:
        lang = "pt"
    if not caminho_saida:
        caminho_saida = os.path.join(STATIC_DIR, f"apresentacao_{lang}.pdf")
    c = CONTEUDO[lang]
    tb = TABELAS.get(lang, TABELAS["pt"])
    largura, altura = A4
    doc = canvas.Canvas(caminho_saida, pagesize=A4)

    # Capa (fundo preto + logo + título dourado)
    _capa(doc, largura, altura, lang, "texto")
    doc.showPage()

    secoes = [
        (c["sobre_titulo"], c["sobre_texto"]),
        (c["duns_titulo"], c["duns_texto"]),
        (c["mercado_titulo"], c["mercado_texto"]),
        (c["problema_titulo"], c["problema_texto"]),
        (c["solucao_titulo"], c["solucao_texto"]),
        (c["alcance_titulo"], c["alcance_texto"]),
        (c["mercados_titulo"], c["mercados_texto"]),
        (c["preco_titulo"], c["preco_texto"]),
        (c["portfolio_titulo"], c["portfolio_texto"]),
        (c["negocio_titulo"], c["negocio_texto"]),
        (c["banners_titulo"], c["banners_texto"]),
        (c["b2b_titulo"], c["b2b_texto"]),
        (c["projecoes_titulo"], c["projecoes_texto"]),
        (c["tracao_titulo"], c["tracao_texto"]),
        (c["roteiro_titulo"], c["roteiro_texto"]),
        (c["invest_titulo"], c["invest_texto"]),
    ]
    for titulo, texto in secoes:
        _desenhar_marca_dagua(doc, largura, altura, lang)
        # Faixa azul com o título da seção
        doc.setFillColor(COR_AZUL)
        doc.rect(0, altura - 16 * mm, largura, 16 * mm, stroke=0, fill=1)
        doc.setFillColor(white)
        doc.setFont(FONTES["bold"], 17)
        doc.drawString(18 * mm, altura - 11 * mm, titulo)
        # Corpo do texto
        y = _texto_wrap(doc, texto, _fonte(lang), 12, 18 * mm,
                        altura - 28 * mm, largura - 36 * mm, COR_PRETO, 7 * mm)
        # Tabela dos 14 idiomas
        if titulo == c["alcance_titulo"]:
            linhas = [[tb["h_idioma"], tb["h_falantes"]]] + \
                     [[nome, str(n)] for nome, n in LINHAS_IDIOMAS] + \
                     [["TOTAL", "~5.320"]]
            y = _tabela_pdf(doc, linhas, [0.6, 0.4], 18 * mm, y - 6 * mm,
                            largura - 36 * mm, fonte=_fonte(lang))
        # Tabela de banners
        elif titulo == c["banners_titulo"]:
            linhas = [[tb["h_seg"], tb["h_fixo"], tb["h_temp"]]]
            for i, lab in enumerate(tb["seg"]):
                fixo, temp = LINHAS_BANNERS[i]
                linhas.append([lab, f"R$ {fixo}", f"R$ {temp}"])
            y = _tabela_pdf(doc, linhas, [0.5, 0.25, 0.25], 18 * mm, y - 6 * mm,
                            largura - 36 * mm, fonte=_fonte(lang))
        # Tabela de descontos B2B
        elif titulo == c["b2b_titulo"]:
            linhas = [[tb["h_de"], tb["h_desc"]]] + LINHAS_B2B
            y = _tabela_pdf(doc, linhas, [0.5, 0.5], 18 * mm, y - 6 * mm,
                            largura - 36 * mm, fonte=_fonte(lang))
        # Tabela de projeções (8 horizontes)
        elif titulo == c["projecoes_titulo"]:
            linhas = [[tb["h_hor"], tb["h_cons"], tb["h_otim"]]]
            for i, n in enumerate(HORIZONTES):
                cons, otim = RANGES[i]
                linhas.append([f"{tb['h_ano']} {n}", f"R$ {cons}", f"R$ {otim}"])
            y = _tabela_pdf(doc, linhas, [0.3, 0.35, 0.35], 18 * mm, y - 6 * mm,
                            largura - 36 * mm, fonte=_fonte(lang))
        # Rodapé dourado
        doc.setFillColor(COR_DOURADO)
        doc.setFont(FONTES["bold"], 9)
        doc.drawCentredString(largura / 2, 12 * mm,
                              f"{c['titulo']} · DUNS 942242668 · {c['confidencial']} {c['ano']}")
        doc.showPage()

    doc.save()
    logger.info(f"PDF texto gerado: {caminho_saida}")
    return caminho_saida

# ------------------------------------------------------------
# 4c. FUNÇÕES AUXILIARES DE DESENHO (texto e tabelas)
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

def _tabela_pdf(doc, dados, colunas, x, y, largura, fonte=None, tam=9):
    from reportlab.platypus import Table, TableStyle
    from reportlab.lib.colors import HexColor, white
    fonte = fonte or FONTES["normal"]
    tbl = Table(dados, colWidths=[largura * c for c in colunas])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), COR_AZUL),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), FONTES["bold"]),
        ("FONTSIZE", (0, 0), (-1, -1), tam),
        ("TEXTCOLOR", (0, 1), (-1, -1), COR_PRETO),
        ("GRID", (0, 0), (-1, -1), 0.4, COR_CINZA_CLARO),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#F5F7FB")]),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    w, h = tbl.wrapOn(doc, largura, 600)
    tbl.drawOn(doc, x, y - h)
    return y - h

# ------------------------------------------------------------
# 5. FUNÇÕES AUXILIARES
# ------------------------------------------------------------
def _fonte(lang):
    """Escolhe a fonte adequada ao idioma."""
    if lang in ("zh",):
        return FONTES.get("zh", FONTES["normal"])
    if lang in ("ja",):
        return FONTES.get("ja", FONTES["normal"])
    return FONTES["normal"]

def _estilos(lang):
    """Cria estilos de parágrafo para o idioma."""
    fonte = _fonte(lang)
    fonte_bold = FONTES["bold"] if lang not in ("zh", "ja") else fonte
    return {
        "titulo": ParagraphStyle("titulo", fontName=fonte_bold, fontSize=26,
                                  leading=32, textColor=COR_PRETO, alignment=TA_CENTER),
        "subtitulo": ParagraphStyle("subtitulo", fontName=fonte, fontSize=14,
                                    leading=20, textColor=COR_CINZA, alignment=TA_CENTER),
        "secao": ParagraphStyle("secao", fontName=fonte_bold, fontSize=16,
                                leading=22, textColor=COR_AZUL, spaceBefore=14, spaceAfter=6),
        "corpo": ParagraphStyle("corpo", fontName=fonte, fontSize=11,
                                leading=16, textColor=COR_PRETO, alignment=TA_JUSTIFY),
        "kpi": ParagraphStyle("kpi", fontName=fonte_bold, fontSize=12,
                              leading=16, textColor=COR_DOURADO, alignment=TA_CENTER),
        "nota": ParagraphStyle("nota", fontName=fonte, fontSize=10,
                               leading=14, textColor=COR_CINZA_CLARO, alignment=TA_CENTER),
        "final": ParagraphStyle("final", fontName=fonte_bold, fontSize=13,
                                leading=18, textColor=COR_DOURADO, alignment=TA_CENTER),
    }

def _desenhar_marca_dagua(c, largura, altura, lang):
    """Desenha a marca d'água (logo/imagem) em todas as páginas."""
    try:
        if os.path.exists(WATERMARK_PATH):
            img = ImageReader(WATERMARK_PATH)
            iw, ih = img.getSize()
            escala = 0.35
            w = iw * escala
            h = ih * escala
            c.saveState()
            c.setFillAlpha(0.10)
            c.drawImage(WATERMARK_PATH, (largura - w) / 2, (altura - h) / 2,
                        width=w, height=h, preserveAspectRatio=True, mask='auto')
            c.restoreState()
    except Exception as e:
        logger.warning(f"Marca d'água ignorada: {e}")

def _capa(c, largura, altura, lang, formato):
    """Desenha a página de capa."""
    c.setFillColor(COR_PRETO)
    c.rect(0, 0, largura, altura, stroke=0, fill=1)
    # Logo
    try:
        if os.path.exists(LOGO_PATH):
            img = ImageReader(LOGO_PATH)
            iw, ih = img.getSize()
            escala = 0.12 if formato == "texto" else 0.16
            w = iw * escala
            h = ih * escala
            c.drawImage(LOGO_PATH, (largura - w) / 2, altura * 0.60,
                        width=w, height=h, preserveAspectRatio=True, mask='auto')
    except Exception as e:
        logger.warning(f"Logo ignorado: {e}")
    c.setFillColor(COR_DOURADO)
    c.setFont(FONTES["bold"], 26)
    c.drawCentredString(largura / 2, altura * 0.48, CONTEUDO[lang]["titulo"])
    c.setFont(_fonte(lang), 14)
    c.setFillColor(white)
    c.drawCentredString(largura / 2, altura * 0.42, CONTEUDO[lang]["subtitulo"])
    c.setFont(_fonte(lang), 11)
    c.setFillColor(COR_CINZA_CLARO)
    c.drawCentredString(largura / 2, altura * 0.34, CONTEUDO[lang]["capa_nota"])
    # Selo confidencial
    c.setFillColor(COR_DOURADO)
    c.setFont(FONTES["bold"], 10)
    c.drawCentredString(largura / 2, altura * 0.10,
                        f"{CONTEUDO[lang]['confidencial']}  ·  {CONTEUDO[lang]['ano']}")

# ------------------------------------------------------------
# 6. GERADOR DE PDF EM FORMATO TEXTO (documento)
# ------------------------------------------------------------
def gerar_pdf_texto(lang="pt", caminho_saida=None):
    """Gera a apresentação em formato de documento (texto)."""
    if lang not in CONTEUDO:
        lang = "pt"
    if not caminho_saida:
        caminho_saida = os.path.join(STATIC_DIR, f"apresentacao_{lang}.pdf")
    c = CONTEUDO[lang]
    est = _estilos(lang)
    largura, altura = A4

    doc = SimpleDocTemplate(caminho_saida, pagesize=A4,
                            leftMargin=25*mm, rightMargin=25*mm,
                            topMargin=20*mm, bottomMargin=20*mm,
                            title=f"{c['titulo']} - {c['ano']}",
                            author="A1ELOS")
    elementos = []
    elementos.append(Paragraph(c["titulo"], est["titulo"]))
    elementos.append(Spacer(1, 6))
    elementos.append(Paragraph(c["subtitulo"], est["subtitulo"]))
    elementos.append(Spacer(1, 4))
    elementos.append(Paragraph(f"{c['capa_nota']} · {c['confidencial']} {c['ano']}", est["nota"]))
    elementos.append(Spacer(1, 12))

    # Seções
    secoes = [
        (c["sobre_titulo"], c["sobre_texto"]),
        (c["duns_titulo"], c["duns_texto"]),
        (c["mercado_titulo"], c["mercado_texto"]),
        (c["problema_titulo"], c["problema_texto"]),
        (c["solucao_titulo"], c["solucao_texto"]),
        (c["alcance_titulo"], c["alcance_texto"]),
        (c["mercados_titulo"], c["mercados_texto"]),
        (c["preco_titulo"], c["preco_texto"]),
        (c["portfolio_titulo"], c["portfolio_texto"]),
        (c["negocio_titulo"], c["negocio_texto"]),
        (c["banners_titulo"], c["banners_texto"]),
        (c["b2b_titulo"], c["b2b_texto"]),
        (c["projecoes_titulo"], c["projecoes_texto"]),
        (c["tracao_titulo"], c["tracao_texto"]),
        (c["roteiro_titulo"], c["roteiro_texto"]),
        (c["invest_titulo"], c["invest_texto"]),
    ]
    for titulo, texto in secoes:
        elementos.append(Paragraph(titulo, est["secao"]))
        elementos.append(Paragraph(texto, est["corpo"]))
        elementos.append(Spacer(1, 6))

    # KPIs em tabela
    kpis = [Paragraph(k, est["kpi"]) for k in c["sobre_kpis"]]
    tabela_kpi = Table([kpis], colWidths=[largura/5 - 10*mm]*5)
    tabela_kpi.setStyle(TableStyle([
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("BOX", (0,0), (-1,-1), 1, COR_DOURADO),
        ("INNERGRID", (0,0), (-1,-1), 0.5, COR_CINZA_CLARO),
        ("BACKGROUND", (0,0), (-1,-1), HexColor("#F8F6F0")),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ]))
    elementos.append(Spacer(1, 10))
    elementos.append(tabela_kpi)
    elementos.append(Spacer(1, 16))

    # Frase final
    elementos.append(Paragraph(c["frase_final"], est["final"]))
    elementos.append(Spacer(1, 8))
    elementos.append(Paragraph(f"{c['titulo']} · DUNS 942242668 · 23 produtos · 14 idiomas",
                               est["nota"]))

    # Marca d'água em todas as páginas
    def _fundo(canvas_obj, doc_obj):
        _desenhar_marca_dagua(canvas_obj, largura, altura, lang)
    doc.build(elementos, onFirstPage=_fundo, onLaterPages=_fundo)
    logger.info(f"PDF texto gerado: {caminho_saida}")
    return caminho_saida

# ------------------------------------------------------------
# 7. GERADOR DE PDF EM FORMATO SLIDES (deck)
# ------------------------------------------------------------
def gerar_pdf_slides(lang="pt", caminho_saida=None):
    """Gera a apresentação em formato de slides (paisagem)."""
    if lang not in CONTEUDO:
        lang = "pt"
    if not caminho_saida:
        caminho_saida = os.path.join(STATIC_DIR, f"apresentacao_slides_{lang}.pdf")
    c = CONTEUDO[lang]
    est = _estilos(lang)
    largura, altura = landscape(A4)

    # Slide 1: capa
    _capa(canvas, largura, altura, lang, "slides")  # placeholder, substituído abaixo

    # Usa canvas direto para controle total do layout
    from reportlab.pdfgen import canvas as cv
    doc = cv.Canvas(caminho_saida, pagesize=landscape(A4))
    _capa(doc, largura, altura, lang, "slides")
    doc.showPage()

    # Slides de conteúdo (um por seção)
    secoes = [
        (c["sobre_titulo"], c["sobre_texto"]),
        (c["duns_titulo"], c["duns_texto"]),
        (c["mercado_titulo"], c["mercado_texto"]),
        (c["problema_titulo"], c["problema_texto"]),
        (c["solucao_titulo"], c["solucao_texto"]),
        (c["alcance_titulo"], c["alcance_texto"]),
        (c["mercados_titulo"], c["mercados_texto"]),
        (c["preco_titulo"], c["preco_texto"]),
        (c["portfolio_titulo"], c["portfolio_texto"]),
        (c["negocio_titulo"], c["negocio_texto"]),
        (c["banners_titulo"], c["banners_texto"]),
        (c["b2b_titulo"], c["b2b_texto"]),
        (c["projecoes_titulo"], c["projecoes_texto"]),
        (c["tracao_titulo"], c["tracao_texto"]),
        (c["roteiro_titulo"], c["roteiro_texto"]),
        (c["invest_titulo"], c["invest_texto"]),
    ]
    for titulo, texto in secoes:
        _desenhar_marca_dagua(doc, largura, altura, lang)
        # Barra superior azul
        doc.setFillColor(COR_AZUL)
        doc.rect(0, altura - 14*mm, largura, 14*mm, stroke=0, fill=1)
        doc.setFillColor(white)
        doc.setFont(FONTES["bold"], 20)
        doc.drawString(15*mm, altura - 10*mm, titulo)
        # Corpo
        doc.setFillColor(COR_PRETO)
        doc.setFont(_fonte(lang), 13)
        # Quebra de linha simples
        palavras = texto.split()
        linhas = []
        linha_atual = ""
        largura_max = largura - 30*mm
        for p in palavras:
            teste = (linha_atual + " " + p).strip()
            if doc.stringWidth(teste, _fonte(lang), 13) <= largura_max:
                linha_atual = teste
            else:
                linhas.append(linha_atual)
                linha_atual = p
        if linha_atual:
            linhas.append(linha_atual)
        y = altura - 30*mm
        for linha in linhas[:14]:  # limite de 14 linhas por slide
            doc.drawString(15*mm, y, linha)
            y -= 8*mm
        # Rodapé
        doc.setFillColor(COR_DOURADO)
        doc.setFont(FONTES["bold"], 9)
        doc.drawCentredString(largura/2, 10*mm,
                              f"{c['titulo']} · {c['confidencial']} {c['ano']}")
        doc.showPage()

    doc.save()
    logger.info(f"PDF slides gerado: {caminho_saida}")
    return caminho_saida

# ------------------------------------------------------------
# 8. ENTRADA PRINCIPAL (compatível com a chamada do main.py)
# ------------------------------------------------------------
def gerar_apresentacao(lang="pt", formato="texto"):
    """Gera a apresentação no formato pedido. Retorna o caminho do arquivo."""
    if formato == "slides":
        return gerar_pdf_slides(lang)
    return gerar_pdf_texto(lang)

def gerar_todas():
    """Gera para todos os 14 idiomas, nos dois formatos."""
    idiomas = ["pt", "en", "es", "it", "fr", "de", "ru", "zh", "ja", "ar", "he", "id", "tr", "vi"]
    for lang in idiomas:
        gerar_pdf_texto(lang)
        gerar_pdf_slides(lang)
    logger.info("Todas as apresentações geradas (14 idiomas × 2 formatos).")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        lang = sys.argv[1]
        formato = sys.argv[2] if len(sys.argv) > 2 else "texto"
        gerar_apresentacao(lang, formato)
    else:
        gerar_todas()
