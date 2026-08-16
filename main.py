# -*- coding: utf-8 -*-
# main.py - A1ELOS Global Numerology API
# VERSÃO FINAL LIMPA E CORRIGIDA - 09/08/2026
import os, json, uuid, logging, secrets, string, base64, traceback
from datetime import date, datetime
from typing import Optional
import stripe
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from gerador_pdf import gerar_pdf, pagina_sucesso, _entregar_arquivo
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import qrcode
import dateutil.parser as dp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

STRIPE_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_PUB = os.getenv("STRIPE_PUBLISHABLE_KEY", "")
FROM_NAME = "A1ELOS Numerologia Global"
BASE_URL = os.getenv("BASE_URL", os.getenv("SITE_URL", "https://global-numerology.onrender.com"))
DB_URL = os.getenv("DATABASE_URL", "sqlite:///./numerologia.db")
ADMIN_EMAIL = "arvigne@gmail.com"
if STRIPE_KEY:
    stripe.api_key = STRIPE_KEY

# ===== BANCO DE DADOS =====
engine_kwargs = {}
if DB_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}
engine = create_engine(DB_URL, **engine_kwargs)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class Calc(Base):
    __tablename__ = "calculations"
    id = Column(String, primary_key=True)
    name = Column(String)
    birth_date = Column(String)
    email = Column(String, nullable=True)
    life_path = Column(Integer)
    expression = Column(Integer)
    soul_urge = Column(Integer)
    personality = Column(Integer)
    destiny = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

class Order(Base):
    __tablename__ = "orders"
    id = Column(String, primary_key=True)
    email = Column(String)
    product = Column(String)
    price = Column(Float)
    status = Column(String, default="pending")
    payment_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# Cria as tabelas SEM travar a subida do app (evita timeout de porta no Render)
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    logger.error(f"DB init adiado (banco indisponivel): {e}")

# ===== APP =====
app = FastAPI(title="Global Numerology")
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ===== 12 IDIOMAS E MOEDAS =====
IDIOMAS = ["pt", "en", "es", "it", "fr", "de", "ja", "zh", "ru", "hi", "he", "ar"]
MOEDA = {
    "pt": "brl", "en": "usd", "es": "eur", "it": "eur", "fr": "eur", "de": "eur",
    "ja": "jpy", "zh": "cny", "ru": "rub", "hi": "inr", "he": "ils", "ar": "sar"
}
SIMBOLO = {
    "pt": "R$", "en": "US$", "es": "€", "it": "€", "fr": "€", "de": "€",
    "ja": "¥", "zh": "¥", "ru": "₽", "hi": "₹", "he": "₪", "ar": "﷼"
}
# ===== FAIXAS DE PREÇO =====
PRODUTO_FAIXA = {
    "express": 0, "vida": 0, "completo": 1, "ia": 1,
    "urna": 2, "eleitoral": 2, "imovel": 2, "calendario": 2,
    "artistico": 3, "bebe": 3, "assinatura": 3,
    "negocio": 4, "casal": 4, "familia": 5,
    "nome_pet": 0, "nickname": 0, "nome_dominio": 0, "nome_canal": 0,
    "nome_equipe": 0, "nome_ong": 0, "nome_projeto": 0, "nome_evento": 0
}
VALORES = {
    "pt": [800, 1700, 2600, 3500, 4400, 9800],
    "en": [150, 350, 500, 700, 900, 2000],
    "es": [150, 350, 500, 700, 900, 2000],
    "it": [150, 350, 500, 700, 900, 2000],
    "fr": [150, 350, 500, 700, 900, 2000],
    "de": [150, 350, 500, 700, 900, 2000],
    "ja": [250, 550, 800, 1100, 1400, 3200],
    "zh": [1200, 2500, 4000, 5500, 7000, 16000],
    "ru": [13000, 28000, 43000, 58000, 73000, 160000],
    "hi": [12000, 28000, 43000, 58000, 73000, 160000],
    "he": [500, 1300, 1900, 2600, 3300, 7300],
    "ar": [600, 1300, 1900, 2600, 3300, 7300]
}
def preco_local(produto, lang):
    return VALORES[lang][PRODUTO_FAIXA[produto]]

# ===== NOMES DOS 15 PRODUTOS =====
PRODUTOS = {
    "pt": {"express": "Mapa Express", "vida": "Qual Vida/Ano", "completo": "Mapa Completo",
        "ia": "Pesquisa IA de Nomes", "urna": "Validacao Nome de Urna", "eleitoral": "Numero Eleitoral",
        "imovel": "Numero do Imovel", "calendario": "Calendario Mensal Energetico",
        "artistico": "Validacao Nome Artistico", "bebe": "Planejamento Nome de Bebe",
        "assinatura": "Validacao de Assinaturas", "negocio": "Nome para Negocio/Produto",
        "casal": "Mapa do Casal", "familia": "Mapa Familia Premium", "coletivo": "Bonus Coletivo/Empresarial",
        "nome_pet": "Nome do Pet", "nickname": "Nickname Digital", "nome_dominio": "Nome do Dominio",
        "nome_canal": "Nome do Canal", "nome_equipe": "Nome da Equipe", "nome_ong": "Nome de ONG, Associacao, Instituto ou Fundacao",
        "nome_projeto": "Nome do Projeto", "nome_evento": "Nome do Evento"},
    "en": {"express": "Express Map", "vida": "Life Phase & Year", "completo": "Complete Map",
        "ia": "AI Name Search", "urna": "Ballot Name Validation", "eleitoral": "Electoral Number",
        "imovel": "Property Number", "calendario": "Monthly Energy Calendar",
        "artistico": "Artistic Name Validation", "bebe": "Baby Name Planning",
        "assinatura": "Signature Validation", "negocio": "Business & Product Name",
        "casal": "Couple Map", "familia": "Premium Family Map", "coletivo": "Corporate Bonus",
        "nome_pet": "Pet Name", "nickname": "Digital Nickname", "nome_dominio": "Domain Name",
        "nome_canal": "Channel Name", "nome_equipe": "Team Name", "nome_ong": "NGO, Association, Institute or Foundation Name",
        "nome_projeto": "Project Name", "nome_evento": "Event Name"},
    "es": {"express": "Mapa Exprés", "vida": "Ciclo de Vida y Año", "completo": "Mapa Completo",
        "ia": "Búsqueda IA de Nombres", "urna": "Validación Nombre de Urna", "eleitoral": "Número Electoral",
        "imovel": "Número de la Propiedad", "calendario": "Calendario Mensual Energético",
        "artistico": "Validación Nombre Artístico", "bebe": "Planificación Nombre de Bebé",
        "assinatura": "Validación de Firmas", "negocio": "Nombre para Negocio/Producto",
        "casal": "Mapa de Pareja", "familia": "Mapa Familiar Premium", "coletivo": "Bono Corporativo",
        "nome_pet": "Nombre de la Mascota", "nickname": "Apodo Digital", "nome_dominio": "Nombre de Dominio",
        "nome_canal": "Nombre del Canal", "nome_equipe": "Nombre del Equipo", "nome_ong": "Nombre de ONG, Asociacion, Instituto o Fundacion",
        "nome_projeto": "Nombre del Proyecto", "nome_evento": "Nombre del Evento"},
    "it": {"express": "Mappa Espressa", "vida": "Fase di Vita e Anno", "completo": "Mappa Completa",
        "ia": "Ricerca IA Nomi", "urna": "Validazione Nome della Scheda", "eleitoral": "Numero Elettorale",
        "imovel": "Numero dell'Immobile", "calendario": "Calendario Mensile Energetico",
        "artistico": "Validazione Nome d'Arte", "bebe": "Pianificazione Nome del Bambino",
        "assinatura": "Validazione delle Firme", "negocio": "Nome per Business/Prodotto",
        "casal": "Mappa di Coppia", "familia": "Mappa Famiglia Premium", "coletivo": "Bonus Aziendale",
        "nome_pet": "Nome dell'Animale", "nickname": "Nickname Digitale", "nome_dominio": "Nome del Dominio",
        "nome_canal": "Nome del Canale", "nome_equipe": "Nome della Squadra", "nome_ong": "Nome di ONG, Associazione, Istituto o Fondazione",
        "nome_projeto": "Nome del Progetto", "nome_evento": "Nome dell'Evento"},
    "fr": {"express": "Carte Express", "vida": "Phase de Vie et Année", "completo": "Carte Complète",
        "ia": "Recherche IA de Noms", "urna": "Validation Nom du Bulletin", "eleitoral": "Numéro Électoral",
        "imovel": "Numéro du Bien", "calendario": "Calendrier Mensuel Énergétique",
        "artistico": "Validation Nom de Scène", "bebe": "Planification Prénom de Bébé",
        "assinatura": "Validation des Signatures", "negocio": "Nom pour Entreprise/Produit",
        "casal": "Carte du Couple", "familia": "Carte Famille Premium", "coletivo": "Bonus d'Entreprise",
        "nome_pet": "Nom de l'Animal", "nickname": "Pseudo Numerique", "nome_dominio": "Nom de Domaine",
        "nome_canal": "Nom de la Chaine", "nome_equipe": "Nom de l'Equipe", "nome_ong": "Nom d'ONG, Association, Institut ou Fondation",
        "nome_projeto": "Nom du Projet", "nome_evento": "Nom de l'Evenement"},
    "de": {"express": "Express-Karte", "vida": "Lebensphase & Jahr", "completo": "Vollständige Karte",
        "ia": "KI-Namenssuche", "urna": "Stimmzettelname-Validierung", "eleitoral": "Wahlnummer",
        "imovel": "Immobiliennummer", "calendario": "Monatlicher Energiekalender",
        "artistico": "Künstlername-Validierung", "bebe": "Babynamen-Planung",
        "assinatura": "Unterschrifts-Validierung", "negocio": "Name für Unternehmen/Produkt",
        "casal": "Paar-Karte", "familia": "Premium-Familien-Karte", "coletivo": "Unternehmensbonus",
        "nome_pet": "Haustiername", "nickname": "Digitaler Spitzname", "nome_dominio": "Domainname",
        "nome_canal": "Kanalname", "nome_equipe": "Teamname", "nome_ong": "Name von NGO, Verein, Institut oder Stiftung",
        "nome_projeto": "Projektname", "nome_evento": "Veranstaltungsname"},
    "ja": {"express": "エクスプレスマップ", "vida": "ライフステージと年", "completo": "完全マップ",
        "ia": "AI名前検索", "urna": "投票用紙名の検証", "eleitoral": "選挙番号",
        "imovel": "不動産番号", "calendario": "月間エネルギーカレンダー",
        "artistico": "芸名の検証", "bebe": "赤ちゃんの名前計画",
        "assinatura": "署名の検証", "negocio": "ビジネス・商品名",
        "casal": "カップルマップ", "familia": "プレミアム家族マップ", "coletivo": "法人ボーナス",
        "nome_pet": "ペットの名前", "nickname": "デジタルニックネーム", "nome_dominio": "ドメイン名",
        "nome_canal": "チャンネル名", "nome_equipe": "チーム名", "nome_ong": "NGO・協会・研究所・財団の名前",
        "nome_projeto": "プロジェクト名", "nome_evento": "イベント名"},
    "zh": {"express": "快速地图", "vida": "生命阶段与年份", "completo": "完整地图",
        "ia": "AI名字搜索", "urna": "选票名称验证", "eleitoral": "选举号码",
        "imovel": "房产号码", "calendario": "每月能量日历",
        "artistico": "艺名验证", "bebe": "宝宝取名规划",
        "assinatura": "签名验证", "negocio": "企业/产品名称",
        "casal": "情侣地图", "familia": "高级家庭地图", "coletivo": "企业奖励",
        "nome_pet": "宠物名字", "nickname": "数字昵称", "nome_dominio": "域名",
        "nome_canal": "频道名称", "nome_equipe": "团队名称", "nome_ong": "非政府组织、协会、研究所或基金会名称",
        "nome_projeto": "项目名称", "nome_evento": "活动名称"},
    "ru": {"express": "Экспресс-карта", "vida": "Жизненный этап и год", "completo": "Полная карта",
        "ia": "ИИ-поиск имён", "urna": "Проверка названия бюллетеня", "eleitoral": "Избирательный номер",
        "imovel": "Номер недвижимости", "calendario": "Ежемесячный энергетический календарь",
        "artistico": "Проверка сценического имени", "bebe": "Планирование имени ребёнка",
        "assinatura": "Проверка подписей", "negocio": "Название для бизнеса/продукта",
        "casal": "Карта пары", "familia": "Премиальная семейная карта", "coletivo": "Корпоративный бонус",
        "nome_pet": "Имя питомца", "nickname": "Цифровой никнейм", "nome_dominio": "Имя домена",
        "nome_canal": "Название канала", "nome_equipe": "Название команды", "nome_ong": "Название НКО, ассоциации, института или фонда",
        "nome_projeto": "Название проекта", "nome_evento": "Название события"},
    "hi": {"express": "त्वरित मानचित्र", "vida": "जीवन चरण और वर्ष", "completo": "पूर्ण मानचित्र",
        "ia": "AI नाम खोज", "urna": "मतपत्र नाम सत्यापन", "eleitoral": "निर्वाचन संख्या",
        "imovel": "संपत्ति संख्या", "calendario": "मासिक ऊर्जा कैलेंडर",
        "artistico": "कलात्मक नाम सत्यापन", "bebe": "शिशु नाम योजना",
        "assinatura": "हस्ताक्षर सत्यापन", "negocio": "व्यवसाय/उत्पाद नाम",
        "casal": "युगल मानचित्र", "familia": "प्रीमियम परिवार मानचित्र", "coletivo": "कॉर्पोरेट बोनस",
        "nome_pet": "पालतू नाम", "nickname": "डिजिटल उपनाम", "nome_dominio": "डोमेन नाम",
        "nome_canal": "चैनल नाम", "nome_equipe": "टीम नाम", "nome_ong": "एनजीओ, संघ, संस्थान या फाउंडेशन का नाम",
        "nome_projeto": "परियोजना नाम", "nome_evento": "कार्यक्रम नाम"},
    "he": {"express": "מפה מהירה", "vida": "שלב חיים ושנה", "completo": "מפה מלאה",
        "ia": "חיפוש שמות AI", "urna": "אימות שם פתק", "eleitoral": "מספר בחירות",
        "imovel": "מספר נכס", "calendario": "לוח אנרגיה חודשי",
        "artistico": "אימות שם במה", "bebe": "תכנון שם לתינוק",
        "assinatura": "אימות חתימות", "negocio": "שם לעסק/מוצר",
        "nome_pet": "שם חיית המחמד", "nickname": "כינוי דיגיטלי", "nome_dominio": "שם דומיין",
        "nome_canal": "שם הערוץ", "nome_equipe": "שם הצוות", "nome_ong": "שם עמותה, ארגון, מכון או קרן",
        "nome_projeto": "שם הפרויקט", "nome_evento": "שם האירוע",
        "casal": "מפת זוג", "familia": "מפת משפחה פרימיום", "coletivo": "בונוס ארגוני"},
    "ar": {"express": "خريطة سريعة", "vida": "مرحلة الحياة والسنة", "completo": "خريطة كاملة",
        "ia": "بحث الأسماء بالذكاء الاصطناعي", "urna": "التحقق من اسم الاقتراع", "eleitoral": "الرقم الانتخابي",
        "imovel": "رقم العقار", "calendario": "تقويم الطاقة الشهري",
        "artistico": "التحقق من الاسم الفني", "bebe": "تخطيط اسم الطفل",
        "assinatura": "التحقق من التوقيعات", "negocio": "اسم للأعمال/المنتج",
        "casal": "خريطة الزوجين", "familia": "خريطة العائلة المميزة", "coletivo": "مكافأة الشركات",
        "nome_pet": "اسم الحيوان الأليف", "nickname": "اللقب الرقمي", "nome_dominio": "اسم النطاق",
        "nome_canal": "اسم القناة", "nome_equipe": "اسم الفريق", "nome_ong": "اسم منظمة أو جمعية أو معهد أو مؤسسة",
        "nome_projeto": "اسم المشروع", "nome_evento": "اسم الفعالية"}
}

# ===== TEXTOS DOS PDFS (12 IDIOMAS) =====
PDF_TEXTS = {
    "pt": {"t_express": "MAPA EXPRESS", "t_completo": "MAPA COMPLETO", "t_urna": "VALIDACAO DE NOME DE URNA", "t_eleitoral": "NUMERO ELEITORAL",
           "numero": "Numero", "valor": "Valor", "caminho": "Caminho de Vida", "expressao": "Expressao", "motivacao": "Motivacao", "personalidade": "Personalidade", "destino": "Destino",
           "cargo": "Cargo", "sugestoes": "Sugestoes:", "op8": "Opcoes com Energia 8 - IDEAL:", "op_alt": "Opcoes Alternativas:", "num_existente": "Numero existente",
           "ciclos": "Ciclo 1 (0-{a}a) | Ciclo 2 ({b}-{c}a) | Ciclo 3 ({d}+a)", "desafios": "Desafios: {x} | {y} | Principal {z}", "ano_pessoal": "Ano Pessoal {ano}: {v}",
           "grade": "Grade: Presentes {p} | Carencias {c}", "baixar": "BAIXAR PDF", "confirmado": "Confirmado!", "gerado": "Ola {nome}, seu {prod} foi gerado.",
           "voltar": "Voltar", "qr_titulo": "Seu PDF nao pode ser gerado.", "qr_instrucao": "Escaneie o QRCode abaixo para acessar seu documento.", "entrega": "Documento sigiloso - entrega por PDF/QRCode."},
    "en": {"t_express": "EXPRESS MAP", "t_completo": "COMPLETE MAP", "t_urna": "BALLOT NAME VALIDATION", "t_eleitoral": "ELECTORAL NUMBER",
           "numero": "Number", "valor": "Value", "caminho": "Life Path", "expressao": "Expression", "motivacao": "Soul Urge", "personalidade": "Personality", "destino": "Destiny",
           "cargo": "Position", "sugestoes": "Suggestions:", "op8": "Options with Energy 8 - IDEAL:", "op_alt": "Alternative Options:", "num_existente": "Existing number",
           "ciclos": "Cycle 1 (0-{a}) | Cycle 2 ({b}-{c}) | Cycle 3 ({d}+)", "desafios": "Challenges: {x} | {y} | Main {z}", "ano_pessoal": "Personal Year {ano}: {v}",
           "grade": "Grid: Present {p} | Missing {c}", "baixar": "DOWNLOAD PDF", "confirmado": "Confirmed!", "gerado": "Hello {nome}, your {prod} has been generated.",
           "voltar": "Back", "qr_titulo": "Your PDF could not be generated.", "qr_instrucao": "Scan the QR code below to access your document.", "entrega": "Confidential document - delivered via PDF/QRCode."},
    "es": {"t_express": "MAPA EXPRES", "t_completo": "MAPA COMPLETO", "t_urna": "VALIDACION NOMBRE DE URNA", "t_eleitoral": "NUMERO ELECTORAL",
           "numero": "Numero", "valor": "Valor", "caminho": "Camino de la Vida", "expressao": "Expresion", "motivacao": "Motivacion", "personalidade": "Personalidad", "destino": "Destino",
           "cargo": "Cargo", "sugestoes": "Sugerencias:", "op8": "Opciones con Energia 8 - IDEAL:", "op_alt": "Opciones Alternativas:", "num_existente": "Numero existente",
           "ciclos": "Ciclo 1 (0-{a}) | Ciclo 2 ({b}-{c}) | Ciclo 3 ({d}+)", "desafios": "Desafios: {x} | {y} | Principal {z}", "ano_pessoal": "Ano Personal {ano}: {v}",
           "grade": "Cuadricula: Presentes {p} | Ausentes {c}", "baixar": "DESCARGAR PDF", "confirmado": "Confirmado!", "gerado": "Hola {nome}, tu {prod} fue generado.",
           "voltar": "Volver", "qr_titulo": "Tu PDF no pudo generarse.", "qr_instrucao": "Escanea el codigo QR para acceder a tu documento.", "entrega": "Documento confidencial - entrega por PDF/QRCode."},
    "it": {"t_express": "MAPPA ESPRESSA", "t_completo": "MAPPA COMPLETA", "t_urna": "VALIDAZIONE NOME DELLA SCHEDA", "t_eleitoral": "NUMERO ELETTORALE",
           "numero": "Numero", "valor": "Valore", "caminho": "Sentiero della Vita", "expressao": "Espressione", "motivacao": "Spinta dell'Anima", "personalidade": "Personalita", "destino": "Destino",
           "cargo": "Carica", "sugestoes": "Suggerimenti:", "op8": "Opzioni con Energia 8 - IDEALE:", "op_alt": "Opzioni Alternative:", "num_existente": "Numero esistente",
           "ciclos": "Ciclo 1 (0-{a}) | Ciclo 2 ({b}-{c}) | Ciclo 3 ({d}+)", "desafios": "Sfide: {x} | {y} | Principale {z}", "ano_pessoal": "Anno Personale {ano}: {v}",
           "grade": "Griglia: Presenti {p} | Mancanti {c}", "baixar": "SCARICA PDF", "confirmado": "Confermato!", "gerado": "Ciao {nome}, il tuo {prod} e stato generato.",
           "voltar": "Indietro", "qr_titulo": "Il tuo PDF non puo essere generato.", "qr_instrucao": "Scansiona il QR code per accedere al documento.", "entrega": "Documento riservato - consegna via PDF/QRCode."},
    "fr": {"t_express": "CARTE EXPRESS", "t_completo": "CARTE COMPLETE", "t_urna": "VALIDATION NOM DU BULLETIN", "t_eleitoral": "NUMERO ELECTORAL",
           "numero": "Numero", "valor": "Valeur", "caminho": "Chemin de Vie", "expressao": "Expression", "motivacao": "Elan de l'Ame", "personalidade": "Personnalite", "destino": "Destin",
           "cargo": "Poste", "sugestoes": "Suggestions :", "op8": "Options avec Energie 8 - IDEAL :", "op_alt": "Options Alternatives :", "num_existente": "Numero existant",
           "ciclos": "Cycle 1 (0-{a}) | Cycle 2 ({b}-{c}) | Cycle 3 ({d}+)", "desafios": "Defis : {x} | {y} | Principal {z}", "ano_pessoal": "Annee Personnelle {ano} : {v}",
           "grade": "Grille : Presents {p} | Manquants {c}", "baixar": "TELECHARGER PDF", "confirmado": "Confirme !", "gerado": "Bonjour {nome}, votre {prod} a ete genere.",
           "voltar": "Retour", "qr_titulo": "Votre PDF n'a pas pu etre genere.", "qr_instrucao": "Scannez le QR code pour acceder a votre document.", "entrega": "Document confidentiel - livraison par PDF/QRCode."},
    "de": {"t_express": "EXPRESS-KARTE", "t_completo": "VOLLSTANDIGE KARTE", "t_urna": "STIMMZETTELNAME-VALIDIERUNG", "t_eleitoral": "WAHLNUMMER",
           "numero": "Zahl", "valor": "Wert", "caminho": "Lebensweg", "expressao": "Ausdruck", "motivacao": "Seelenwunsch", "personalidade": "Personlichkeit", "destino": "Schicksal",
           "cargo": "Position", "sugestoes": "Vorschlage:", "op8": "Optionen mit Energie 8 - IDEAL:", "op_alt": "Alternative Optionen:", "num_existente": "Bestehende Nummer",
           "ciclos": "Zyklus 1 (0-{a}) | Zyklus 2 ({b}-{c}) | Zyklus 3 ({d}+)", "desafios": "Herausforderungen: {x} | {y} | Haupt {z}", "ano_pessoal": "Persoenliches Jahr {ano}: {v}",
           "grade": "Raster: Vorhanden {p} | Fehlend {c}", "baixar": "PDF HERUNTERLADEN", "confirmado": "Bestaetigt!", "gerado": "Hallo {nome}, Ihr {prod} wurde erstellt.",
           "voltar": "Zurueck", "qr_titulo": "Ihr PDF konnte nicht erstellt werden.", "qr_instrucao": "Scannen Sie den QR-Code, um auf Ihr Dokument zuzugreifen.", "entrega": "Vertrauliches Dokument - Lieferung per PDF/QRCode."},
    "ja": {"t_express": "エクスプレスマップ", "t_completo": "完全マップ", "t_urna": "投票用紙名の検証", "t_eleitoral": "選挙番号",
           "numero": "数字", "valor": "値", "caminho": "ライフパス", "expressao": "表現", "motivacao": "魂の欲求", "personalidade": "性格", "destino": "運命",
           "cargo": "役職", "sugestoes": "提案:", "op8": "エネルギー8のオプション - 理想的:", "op_alt": "代替オプション:", "num_existente": "既存の番号",
           "ciclos": "サイクル1 (0-{a}) | サイクル2 ({b}-{c}) | サイクル3 ({d}+)", "desafios": "課題: {x} | {y} | 主要 {z}", "ano_pessoal": "パーソナルイヤー {ano}: {v}",
           "grade": "グリッド: あり {p} | 欠け {c}", "baixar": "PDFをダウンロード", "confirmado": "確認済み!", "gerado": "{nome} さん、{prod} が生成されました。",
           "voltar": "戻る", "qr_titulo": "PDFを生成できませんでした。", "qr_instrucao": "下のQRコードをスキャンして文書にアクセスしてください。", "entrega": "機密文書 - PDF/QRコードで納品。"},
    "zh": {"t_express": "快速地图", "t_completo": "完整地图", "t_urna": "选票名称验证", "t_eleitoral": "选举号码",
           "numero": "数字", "valor": "数值", "caminho": "生命路径", "expressao": "表达", "motivacao": "灵魂冲动", "personalidade": "个性", "destino": "命运",
           "cargo": "职位", "sugestoes": "建议:", "op8": "能量8选项 - 理想:", "op_alt": "备选方案:", "num_existente": "现有号码",
           "ciclos": "周期1 (0-{a}) | 周期2 ({b}-{c}) | 周期3 ({d}+)", "desafios": "挑战: {x} | {y} | 主要 {z}", "ano_pessoal": "个人年份 {ano}: {v}",
           "grade": "网格: 存在 {p} | 缺失 {c}", "baixar": "下载PDF", "confirmado": "已确认!", "gerado": "您好 {nome}，您的{prod}已生成。",
           "voltar": "返回", "qr_titulo": "无法生成PDF。", "qr_instrucao": "扫描下方二维码访问您的文档。", "entrega": "保密文档 - 通过PDF/二维码交付。"},
    "ru": {"t_express": "ЭКСПРЕСС-КАРТА", "t_completo": "ПОЛНАЯ КАРТА", "t_urna": "ПРОВЕРКА НАЗВАНИЯ БЮЛЛЕТЕНЯ", "t_eleitoral": "ИЗБИРАТЕЛЬНЫЙ НОМЕР",
           "numero": "Число", "valor": "Значение", "caminho": "Путь Жизни", "expressao": "Выражение", "motivacao": "Порыв Души", "personalidade": "Личность", "destino": "Судьба",
           "cargo": "Должность", "sugestoes": "Предложения:", "op8": "Варианты с Энергией 8 - ИДЕАЛ:", "op_alt": "Альтернативные варианты:", "num_existente": "Существующий номер",
           "ciclos": "Цикл 1 (0-{a}) | Цикл 2 ({b}-{c}) | Цикл 3 ({d}+)", "desafios": "Вызовы: {x} | {y} | Главный {z}", "ano_pessoal": "Личный год {ano}: {v}",
           "grade": "Сетка: Есть {p} | Нет {c}", "baixar": "СКАЧАТЬ PDF", "confirmado": "Подтверждено!", "gerado": "Здравствуйте {nome}, ваш {prod} создан.",
           "voltar": "Назад", "qr_titulo": "Не удалось создать PDF.", "qr_instrucao": "Отсканируйте QR-код ниже, чтобы получить доступ к документу.", "entrega": "Конфиденциальный документ - доставка через PDF/QRCode."},
    "hi": {"t_express": "त्वरित मानचित्र", "t_completo": "पूर्ण मानचित्र", "t_urna": "मतपत्र नाम सत्यापन", "t_eleitoral": "निर्वाचन संख्या",
           "numero": "अंक", "valor": "मान", "caminho": "जीवन पथ", "expressao": "अभिव्यक्ति", "motivacao": "आत्मा की इच्छा", "personalidade": "व्यक्तित्व", "destino": "भाग्य",
           "cargo": "पद", "sugestoes": "सुझाव:", "op8": "ऊर्जा 8 विकल्प - आदर्श:", "op_alt": "वैकल्पिक विकल्प:", "num_existente": "मौजूदा संख्या",
           "ciclos": "चक्र 1 (0-{a}) | चक्र 2 ({b}-{c}) | चक्र 3 ({d}+)", "desafios": "चुनौतियाँ: {x} | {y} | मुख्य {z}", "ano_pessoal": "व्यक्तिगत वर्ष {ano}: {v}",
           "grade": "ग्रिड: मौजूद {p} | अनुपस्थित {c}", "baixar": "PDF डाउनलोड करें", "confirmado": "पुष्टि हुई!", "gerado": "नमस्ते {nome}, आपका {prod} तैयार है।",
           "voltar": "वापस", "qr_titulo": "आपका PDF नहीं बन सका।", "qr_instrucao": "नीचे QR कोड स्कैन करके अपने दस्तावेज़ तक पहुँचें।", "entrega": "गोपनीय दस्तावेज़ - PDF/QRCode द्वारा डिलीवरी।"},
    "he": {"t_express": "מפה מהירה", "t_completo": "מפה מלאה", "t_urna": "אימות שם פתק", "t_eleitoral": "מספר בחירות",
           "numero": "מספר", "valor": "ערך", "caminho": "נתיב החיים", "expressao": "ביטוי", "motivacao": "דחף הנשמה", "personalidade": "אישיות", "destino": "גורל",
           "cargo": "תפקיד", "sugestoes": "הצעות:", "op8": "אפשרויות עם אנרגיה 8 - אידיאלי:", "op_alt": "אפשרויות חלופיות:", "num_existente": "מספר קיים",
           "ciclos": "מחזור 1 (0-{a}) | מחזור 2 ({b}-{c}) | מחזור 3 ({d}+)", "desafios": "אתגרים: {x} | {y} | עיקרי {z}", "ano_pessoal": "שנה אישית {ano}: {v}",
           "grade": "רשת: קיימים {p} | חסרים {c}", "baixar": "הורד PDF", "confirmado": "אושר!", "gerado": "שלום {nome}, ה-{prod} שלך נוצר.",
           "voltar": "חזור", "qr_titulo": "לא ניתן היה ליצור את ה-PDF.", "qr_instrucao": "סרוק את קוד ה-QR למטה כדי לגשת למסמך שלך.", "entrega": "מסמך חסוי - מסירה באמצעות PDF/QRCode."},
    "ar": {"t_express": "خريطة سريعة", "t_completo": "خريطة كاملة", "t_urna": "التحقق من اسم الاقتراع", "t_eleitoral": "الرقم الانتخابي",
           "numero": "الرقم", "valor": "القيمة", "caminho": "مسار الحياة", "expressao": "التعبير", "motivacao": "دافع الروح", "personalidade": "الشخصية", "destino": "القدر",
           "cargo": "المنصب", "sugestoes": "اقتراحات:", "op8": "خيارات بالطاقة 8 - مثالي:", "op_alt": "خيارات بديلة:", "num_existente": "الرقم الموجود",
           "ciclos": "دورة 1 (0-{a}) | دورة 2 ({b}-{c}) | دورة 3 ({d}+)", "desafios": "التحديات: {x} | {y} | الرئيسي {z}", "ano_pessoal": "السنة الشخصية {ano}: {v}",
           "grade": "الشبكة: موجودة {p} | ناقصة {c}", "baixar": "تحميل PDF", "confirmado": "تم التأكيد!", "gerado": "مرحباً {nome}، تم إنشاء {prod} الخاص بك.",
           "voltar": "رجوع", "qr_titulo": "تعذر إنشاء ملف PDF الخاص بك.", "qr_instrucao": "امسح رمز QR أدناه للوصول إلى مستندك.", "entrega": "مستند سري - التسليم عبر PDF/QRCode."}
}
# ===== PRICE IDS STRIPE =====
PRICE_IDS = {
    "pt": {"express": "price_1TxocVBMLa84bVJ0EL0kb9Dn", "completo": "price_1TxohlBMLa84bVJ0jVj9307b",
           "urna": "price_1TxollBMLa84bVJ0Wk5zIak6", "eleitoral": "price_1TxopFBMLa84bVJ0jvtJExVj",
           "vida": "PRICE_ID_PT_VIDA", "ia": "PRICE_ID_PT_IA", "imovel": "PRICE_ID_PT_IMOVEL",
           "calendario": "PRICE_ID_PT_CALENDARIO", "artistico": "PRICE_ID_PT_ARTISTICO",
           "bebe": "PRICE_ID_PT_BEBE", "assinatura": "PRICE_ID_PT_ASSINATURA",
           "negocio": "PRICE_ID_PT_NEGOCIO", "casal": "PRICE_ID_PT_CASAL", "familia": "PRICE_ID_PT_FAMILIA",
           "nome_pet": "PRICE_ID_PT_NOME_PET", "nickname": "PRICE_ID_PT_NICKNAME",
           "nome_dominio": "PRICE_ID_PT_NOME_DOMINIO", "nome_canal": "PRICE_ID_PT_NOME_CANAL",
           "nome_equipe": "PRICE_ID_PT_NOME_EQUIPE", "nome_ong": "PRICE_ID_PT_NOME_ONG",
           "nome_projeto": "PRICE_ID_PT_NOME_PROJETO", "nome_evento": "PRICE_ID_PT_NOME_EVENTO"},
    "en": {"express": "price_1TxotnBMLa84bVJ00SGo4kjO", "completo": "price_1TxoxfBMLa84bVJ0VgQVddZX",
           "urna": "price_1Txp1jBMLa84bVJ06W4559rN", "eleitoral": "price_1Txp5aBMLa84bVJ0GqrvBrIk",
           "vida": "PRICE_ID_EN_VIDA", "ia": "PRICE_ID_EN_IA", "imovel": "PRICE_ID_EN_IMOVEL",
           "calendario": "PRICE_ID_EN_CALENDARIO", "artistico": "PRICE_ID_EN_ARTISTICO",
           "bebe": "PRICE_ID_EN_BEBE", "assinatura": "PRICE_ID_EN_ASSINATURA",
           "negocio": "PRICE_ID_EN_NEGOCIO", "casal": "PRICE_ID_EN_CASAL", "familia": "PRICE_ID_EN_FAMILIA",
           "nome_pet": "PRICE_ID_EN_NOME_PET", "nickname": "PRICE_ID_EN_NICKNAME",
           "nome_dominio": "PRICE_ID_EN_NOME_DOMINIO", "nome_canal": "PRICE_ID_EN_NOME_CANAL",
           "nome_equipe": "PRICE_ID_EN_NOME_EQUIPE", "nome_ong": "PRICE_ID_EN_NOME_ONG",
           "nome_projeto": "PRICE_ID_EN_NOME_PROJETO", "nome_evento": "PRICE_ID_EN_NOME_EVENTO"},
    "es": {"express": "price_1TyD2oBMLa84bVJ0HvSTMozS", "completo": "price_1TyD6NBMLa84bVJ0s5y2OtSr",
           "urna": "price_1TyDB0BMLa84bVJ0baUEGa2P", "eleitoral": "price_1TyDCsBMLa84bVJ0NRp5uOKU",
           "vida": "PRICE_ID_ES_VIDA", "ia": "PRICE_ID_ES_IA", "imovel": "PRICE_ID_ES_IMOVEL",
           "calendario": "PRICE_ID_ES_CALENDARIO", "artistico": "PRICE_ID_ES_ARTISTICO",
           "bebe": "PRICE_ID_ES_BEBE", "assinatura": "PRICE_ID_ES_ASSINATURA",
           "negocio": "PRICE_ID_ES_NEGOCIO", "casal": "PRICE_ID_ES_CASAL", "familia": "PRICE_ID_ES_FAMILIA",
           "nome_pet": "PRICE_ID_ES_NOME_PET", "nickname": "PRICE_ID_ES_NICKNAME",
           "nome_dominio": "PRICE_ID_ES_NOME_DOMINIO", "nome_canal": "PRICE_ID_ES_NOME_CANAL",
           "nome_equipe": "PRICE_ID_ES_NOME_EQUIPE", "nome_ong": "PRICE_ID_ES_NOME_ONG",
           "nome_projeto": "PRICE_ID_ES_NOME_PROJETO", "nome_evento": "PRICE_ID_ES_NOME_EVENTO"},
    "it": {"express": "Mappa Espressa", "vida": "Fase di Vita e Anno", "completo": "Mappa Completa",
           "ia": "Ricerca IA Nomi", "urna": "Validazione Nome della Scheda", "eleitoral": "Numero Elettorale",
           "imovel": "Numero dell'Immobile", "calendario": "Calendario Mensile Energetico",
           "artistico": "Validazione Nome d'Arte", "bebe": "Pianificazione Nome del Bambino",
           "assinatura": "Validazione delle Firme", "negocio": "Nome per Business/Prodotto",
           "casal": "Mappa di Coppia", "familia": "Mappa Famiglia Premium", "coletivo": "Bonus Aziendale",
           "nome_pet": "Nome dell'Animale", "nickname": "Nickname Digitale", "nome_dominio": "Nome del Dominio",
           "nome_canal": "Nome del Canale", "nome_equipe": "Nome della Squadra", "nome_ong": "Nome di ONG, Associazione, Istituto o Fondazione",
           "nome_projeto": "Nome del Progetto", "nome_evento": "Nome dell'Evento"},
    "fr": {"express": "price_1TyDnQBMLa84bVJ0K9DBz2mk", "completo": "price_1TyDrjBMLa84bVJ0cstgcPbY",
           "urna": "price_1TyDw1BMLa84bVJ0EV0OnINW", "eleitoral": "price_1TyDxsBMLa84bVJ0n2t4jOfZ",
           "vida": "PRICE_ID_FR_VIDA", "ia": "PRICE_ID_FR_IA", "imovel": "PRICE_ID_FR_IMOVEL",
           "calendario": "PRICE_ID_FR_CALENDARIO", "artistico": "PRICE_ID_FR_ARTISTICO",
           "bebe": "PRICE_ID_FR_BEBE", "assinatura": "PRICE_ID_FR_ASSINATURA",
           "negocio": "PRICE_ID_FR_NEGOCIO", "casal": "PRICE_ID_FR_CASAL", "familia": "PRICE_ID_FR_FAMILIA",
           "nome_pet": "PRICE_ID_FR_NOME_PET", "nickname": "PRICE_ID_FR_NICKNAME",
           "nome_dominio": "PRICE_ID_FR_NOME_DOMINIO", "nome_canal": "PRICE_ID_FR_NOME_CANAL",
           "nome_equipe": "PRICE_ID_FR_NOME_EQUIPE", "nome_ong": "PRICE_ID_FR_NOME_ONG",
           "nome_projeto": "PRICE_ID_FR_NOME_PROJETO", "nome_evento": "PRICE_ID_FR_NOME_EVENTO"},
    "de": {"express": "price_1TyFJaBMLa84bVJ0BDPNQUjz", "completo": "price_1TyFLKBMLa84bVJ0RT0bkKpW",
           "urna": "price_1TyFO2BMLa84bVJ0FIoh7co1", "eleitoral": "price_1TyFTxBMLa84bVJ0qw6LQvVI",
           "vida": "PRICE_ID_DE_VIDA", "ia": "PRICE_ID_DE_IA", "imovel": "PRICE_ID_DE_IMOVEL",
           "calendario": "PRICE_ID_DE_CALENDARIO", "artistico": "PRICE_ID_DE_ARTISTICO",
           "bebe": "PRICE_ID_DE_BEBE", "assinatura": "PRICE_ID_DE_ASSINATURA",
           "negocio": "PRICE_ID_DE_NEGOCIO", "casal": "PRICE_ID_DE_CASAL", "familia": "PRICE_ID_DE_FAMILIA",
           "nome_pet": "PRICE_ID_DE_NOME_PET", "nickname": "PRICE_ID_DE_NICKNAME",
           "nome_dominio": "PRICE_ID_DE_NOME_DOMINIO", "nome_canal": "PRICE_ID_DE_NOME_CANAL",
           "nome_equipe": "PRICE_ID_DE_NOME_EQUIPE", "nome_ong": "PRICE_ID_DE_NOME_ONG",
           "nome_projeto": "PRICE_ID_DE_NOME_PROJETO", "nome_evento": "PRICE_ID_DE_NOME_EVENTO"},
    "ja": {"express": "price_1TyJ5HBMLa84bVJ00nZLnuV1", "completo": "price_1TyJJgBMLa84bVJ0fkO5nSFT",
           "urna": "price_1TyJOzBMLa84bVJ0BAPegYVD", "eleitoral": "price_1TyJRwBMLa84bVJ0PLA1CIuH",
           "vida": "PRICE_ID_JA_VIDA", "ia": "PRICE_ID_JA_IA", "imovel": "PRICE_ID_JA_IMOVEL",
           "calendario": "PRICE_ID_JA_CALENDARIO", "artistico": "PRICE_ID_JA_ARTISTICO",
           "bebe": "PRICE_ID_JA_BEBE", "assinatura": "PRICE_ID_JA_ASSINATURA",
           "negocio": "PRICE_ID_JA_NEGOCIO", "casal": "PRICE_ID_JA_CASAL", "familia": "PRICE_ID_JA_FAMILIA",
           "nome_pet": "PRICE_ID_JA_NOME_PET", "nickname": "PRICE_ID_JA_NICKNAME",
           "nome_dominio": "PRICE_ID_JA_NOME_DOMINIO", "nome_canal": "PRICE_ID_JA_NOME_CANAL",
           "nome_equipe": "PRICE_ID_JA_NOME_EQUIPE", "nome_ong": "PRICE_ID_JA_NOME_ONG",
           "nome_projeto": "PRICE_ID_JA_NOME_PROJETO", "nome_evento": "PRICE_ID_JA_NOME_EVENTO"},
    "zh": {"express": "price_1TyKXeBMLa84bVJ07Q6w0j6G", "completo": "price_1TyKZfBMLa84bVJ0bgYSm8e2",
           "urna": "price_1TyKdWBMLa84bVJ0TIP0Knbi", "eleitoral": "price_1TyKitBMLa84bVJ0lFgyKya0",
           "vida": "PRICE_ID_ZH_VIDA", "ia": "PRICE_ID_ZH_IA", "imovel": "PRICE_ID_ZH_IMOVEL",
           "calendario": "PRICE_ID_ZH_CALENDARIO", "artistico": "PRICE_ID_ZH_ARTISTICO",
           "bebe": "PRICE_ID_ZH_BEBE", "assinatura": "PRICE_ID_ZH_ASSINATURA",
           "negocio": "PRICE_ID_ZH_NEGOCIO", "casal": "PRICE_ID_ZH_CASAL", "familia": "PRICE_ID_ZH_FAMILIA",
           "nome_pet": "PRICE_ID_ZH_NOME_PET", "nickname": "PRICE_ID_ZH_NICKNAME",
           "nome_dominio": "PRICE_ID_ZH_NOME_DOMINIO", "nome_canal": "PRICE_ID_ZH_NOME_CANAL",
           "nome_equipe": "PRICE_ID_ZH_NOME_EQUIPE", "nome_ong": "PRICE_ID_ZH_NOME_ONG",
           "nome_projeto": "PRICE_ID_ZH_NOME_PROJETO", "nome_evento": "PRICE_ID_ZH_NOME_EVENTO"},
    "ru": {"express": "Экспресс-карта", "vida": "Жизненный этап и год", "completo": "Полная карта",
           "ia": "ИИ-поиск имён", "urna": "Проверка названия бюллетеня", "eleitoral": "Избирательный номер",
           "imovel": "Номер недвижимости", "calendario": "Ежемесячный энергетический календарь",
           "artistico": "Проверка сценического имени", "bebe": "Планирование имени ребёнка",
           "assinatura": "Проверка подписей", "negocio": "Название для бизнеса/продукта",
           "casal": "Карта пары", "familia": "Премиальная семейная карта", "coletivo": "Корпоративный бонус",
           "nome_pet": "Имя питомца", "nickname": "Цифровой никнейм", "nome_dominio": "Имя домена",
           "nome_canal": "Название канала", "nome_equipe": "Название команды", "nome_ong": "Название НКО, ассоциации, института или фонда",
           "nome_projeto": "Название проекта", "nome_evento": "Название события"},
    "hi": {"express": "त्वरित मानचित्र", "vida": "जीवन चरण और वर्ष", "completo": "पूर्ण मानचित्र",
           "ia": "AI नाम खोज", "urna": "मतपत्र नाम सत्यापन", "eleitoral": "निर्वाचन संख्या",
           "imovel": "संपत्ति संख्या", "calendario": "मासिक ऊर्जा कैलेंडर",
           "artistico": "कलात्मक नाम सत्यापन", "bebe": "शिशु नाम योजना",
           "assinatura": "हस्ताक्षर सत्यापन", "negocio": "व्यवसाय/उत्पाद नाम",
           "casal": "युगल मानचित्र", "familia": "प्रीमियम परिवार मानचित्र", "coletivo": "कॉर्पोरेट बोनस",
           "nome_pet": "पालतू नाम", "nickname": "डिजिटल उपनाम", "nome_dominio": "डोमेन नाम",
           "nome_canal": "चैनल नाम", "nome_equipe": "टीम नाम", "nome_ong": "एनजीओ, संघ, संस्थान या फाउंडेशन का नाम",
           "nome_projeto": "परियोजना नाम", "nome_evento": "कार्यक्रम नाम"},
    "he": {"express": "price_1TyIKeBMLa84bVJ0W02dbXOt", "completo": "price_1TyIO0BMLa84bVJ08P0j9THk",
           "urna": "price_1TyIPbBMLa84bVJ08GnGksRk", "eleitoral": "price_1TyISQBMLa84bVJ0sb7xjIyV",
           "vida": "PRICE_ID_HE_VIDA", "ia": "PRICE_ID_HE_IA", "imovel": "PRICE_ID_HE_IMOVEL",
           "calendario": "PRICE_ID_HE_CALENDARIO", "artistico": "PRICE_ID_HE_ARTISTICO",
           "bebe": "PRICE_ID_HE_BEBE", "assinatura": "PRICE_ID_HE_ASSINATURA",
           "negocio": "PRICE_ID_HE_NEGOCIO", "casal": "PRICE_ID_HE_CASAL", "familia": "PRICE_ID_HE_FAMILIA",
           "nome_pet": "PRICE_ID_HE_NOME_PET", "nickname": "PRICE_ID_HE_NICKNAME",
           "nome_dominio": "PRICE_ID_HE_NOME_DOMINIO", "nome_canal": "PRICE_ID_HE_NOME_CANAL",
           "nome_equipe": "PRICE_ID_HE_NOME_EQUIPE", "nome_ong": "PRICE_ID_HE_NOME_ONG",
           "nome_projeto": "PRICE_ID_HE_NOME_PROJETO", "nome_evento": "PRICE_ID_HE_NOME_EVENTO"},
    "ar": {"express": "خريطة سريعة", "vida": "مرحلة الحياة والسنة", "completo": "خريطة كاملة",
           "ia": "بحث الأسماء بالذكاء الاصطناعي", "urna": "التحقق من اسم الاقتراع", "eleitoral": "الرقم الانتخابي",
           "imovel": "رقم العقار", "calendario": "تقويم الطاقة الشهري",
           "artistico": "التحقق من الاسم الفني", "bebe": "تخطيط اسم الطفل",
           "assinatura": "التحقق من التوقيعات", "negocio": "اسم للأعمال/المنتج",
           "casal": "خريطة الزوجين", "familia": "خريطة العائلة المميزة", "coletivo": "مكافأة الشركات",
           "nome_pet": "اسم الحيوان الأليف", "nickname": "اللقب الرقمي", "nome_dominio": "اسم النطاق",
           "nome_canal": "اسم القناة", "nome_equipe": "اسم الفريق", "nome_ong": "اسم منظمة أو جمعية أو معهد أو مؤسسة",
           "nome_projeto": "اسم المشروع", "nome_evento": "اسم الفعالية"}
}
PRODUTO_TARGET = {
    "express": "calculadora", "vida": "produtos", "completo": "calculadora",
    "ia": "produtos", "urna": "form-urna", "eleitoral": "form-eleitoral",
    "imovel": "produtos", "calendario": "produtos", "artistico": "produtos",
    "bebe": "produtos", "assinatura": "produtos", "negocio": "produtos",
    "casal": "produtos", "familia": "produtos", "coletivo": "corporativo",
    "nome_pet": "calculadora", "nickname": "calculadora", "nome_dominio": "calculadora",
    "nome_canal": "calculadora", "nome_equipe": "calculadora", "nome_ong": "calculadora",
    "nome_projeto": "calculadora", "nome_evento": "calculadora"  
}
# ===== MODELOS PYDANTIC =====
class PayReq(BaseModel):
    nome: str
    nascimento: str
    email: Optional[str] = ""   # campo preservado, sem uso
    lang: str = "pt"

class UrnaPayReq(BaseModel):
    nome_completo: str
    nome_urna: str
    email: Optional[str] = ""   # preservado
    lang: str = "pt"
    cargo: str = "vereador"
    nome1: str = ""
    nome2: str = ""
    nome3: str = ""
    nome4: str = ""
    nome5: str = ""

class EleitoralPayReq(BaseModel):
    nome_completo: str
    numero: str
    email: Optional[str] = ""   # preservado
    lang: str = "pt"
    cargo: str = "vereador"

class SugestaoReq(BaseModel):
    nome: str
    email: Optional[str] = ""   # preservado
    mensagem: str

class BonusReq(BaseModel):
    nome: str
    email: Optional[str] = ""   # preservado
    motivo: str

class AtivarBonusReq(BaseModel):
    codigo: str

# ===== CONSTANTES DE ESTILO (PDFs) =====
GOLD = colors.HexColor("#B8860B")
LGRAY = colors.HexColor("#f0f0f0")
DARK = colors.HexColor("#222")
GRAY = colors.HexColor("#888")
FONTE = "Helvetica"
FN = "Helvetica-Bold"
CARGO_INFO = {
    "vereador": {"label": "Vereador"},
    "dep_estadual": {"label": "Deputado Estadual"},
    "dep_federal": {"label": "Deputado Federal"},
    "senador": {"label": "Senador"},
}
ENERGIAS = {
    1: "Lideranca", 2: "Cooperacao", 3: "Criatividade",
    4: "Trabalho", 5: "Liberdade", 6: "Familia",
    7: "Sabedoria", 8: "Poder e Prosperidade (IDEAL)", 9: "Humanitarismo",
}
# ===== CALCULO NUMEROLOGICO =====
def r1(n):
    while n > 9 and n not in (11, 22, 33):
        n = sum(int(d) for d in str(n))
    return n
def calc_nome(nome):
    t = {c: (i % 9 or 9) for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 1)}
    limpo = nome.upper().replace(" ", "").replace(".", "").replace("-", "").replace(",", "")
    total = sum(t.get(c, 0) for c in limpo if c in t)
    return r1(total), total
def calc(nome, data_str):
    bd = dp.parse(data_str).date()
    lp = r1(bd.day + bd.month + bd.year)
    t = {c: (i % 9 or 9) for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 1)}
    nu = nome.upper().replace(" ", "")
    te = tv = tp = 0
    for ch in nu:
        val = t.get(ch, 0)
        te += val
        if ch in "AEIOU":
            tv += val
        else:
            tp += val
    return {"life_path": lp, "expression": r1(te), "soul_urge": r1(tv),
            "personality": r1(tp), "destiny": r1(r1(te) + lp)}
def calc_grid(nome):
    t = {c: (i % 9 or 9) for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 1)}
    g = {i: 0 for i in range(1, 10)}
    for ch in nome.upper().replace(" ", ""):
        v = t.get(ch, 0)
        if v in range(1, 10):
            g[v] += 1
    return g
def validar_nomes_urna(nomes, cargo_key):
    results = []
    lv = {c: (i % 9 or 9) for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 1)}
    for nome in nomes:
        if not nome.strip():
            continue
        limpo = nome.upper().replace(" ", "").replace(".", "").replace("-", "").replace(",", "")
        letras = []
        st = 0
        for c in limpo:
            v = lv.get(c, 0)
            letras.append({"letra": c, "valor": v})
            st += v
        en = r1(st)
        if en == 8:
            expl = f"Nome {nome.strip().title()} tem ENERGIA 8! Ideal para candidatura."
        else:
            expl = f"Nome {nome.strip().title()} tem energia {en}. {ENERGIAS.get(en, '')}."
        results.append({"nome": nome.strip().title(), "energia": en,
                        "soma": st, "eh_ideal": en == 8,
                        "explicacao": expl, "letras": letras})
    ideal = any(r["eh_ideal"] for r in results)
    sugs = []
    if not ideal:
        for nome in nomes:
            if not nome.strip():
                continue
            lbl = CARGO_INFO.get(cargo_key, {}).get("label", "")
            if not lbl:
                continue
            for nt in [f"{lbl[:3]} {nome.strip()}", f"{nome.strip()} - {lbl.lower()[:3]}"]:
                en, _ = calc_nome(nt)
                sugs.append({"nome": nt.title(), "energia": en, "eh_ideal": en == 8})
                if len(sugs) >= 3:
                    break
            if len(sugs) >= 3:
                break
    return results, ideal, sugs[:3]
def gerar_numeros(sigla, cargo, qtd=5):
    dc = {"vereador": 5, "dep_estadual": 5, "dep_federal": 4, "senador": 3}
    td = dc.get(cargo, 5)
    ss = str(sigla).zfill(2)[:2]
    sm = int(ss[0]) + int(ss[1])
    lv = td - 2
    res = []
    tent = set()
    def busca(alvo):
        enc = []
        for x in range(10 ** lv):
            if len(enc) + len(res) >= qtd:
                break
            dl = str(x).zfill(lv)
            en = r1(sm + sum(int(d) for d in dl))
            if en == alvo:
                n = ss + dl
                if n not in tent:
                    if x in range(1, 10) and alvo != r1(sm):
                        continue
                    tent.add(n)
                    st = sm + sum(int(d) for d in dl)
                    enc.append({"numero": n, "energia": alvo, "ideal": alvo == 8,
                                "sigla": ss, "digitos_livres": dl,
                                "soma_sigla": sm, "soma_total": st})
        return enc
    res.extend(busca(8))
    if len(res) < qtd:
        res.extend(busca(3))
    if len(res) < qtd:
        for e in [7, 1, 9, 5, 6, 4, 2]:
            if len(res) >= qtd:
                break
            res.extend(busca(e))
    return res[:qtd]
def estilo(tam, negrito=False, cor=DARK, alinhamento=TA_LEFT, antes=0, depois=4):
    return ParagraphStyle("S", fontName=FN if negrito else FONTE,
                         fontSize=tam, textColor=cor,
                         alignment=alinhamento, spaceBefore=antes,
                         spaceAfter=depois)

# ===== DESCONTO PROGRESSIVO (server-side) =====
def desconto_bc(qtd_total, empresarial=False):
    if empresarial:
        if qtd_total >= 3000: return 0.70
        if qtd_total >= 2000: return 0.60
    if qtd_total >= 2000: return 0.50
    if qtd_total >= 1000: return 0.45
    if qtd_total >= 500: return 0.40
    if qtd_total >= 200: return 0.30
    if qtd_total >= 100: return 0.25
    if qtd_total >= 50: return 0.20
    if qtd_total >= 10: return 0.10
    return 0.0
# ===== CRIACAO DE SESSAO STRIPE =====
def _criar_sessao(produto, lang="pt", email="", nome="", birth="", meta_extra=None):
    if lang not in PRICE_IDS or produto not in PRICE_IDS[lang]:
        raise HTTPException(status_code=400, detail="Idioma ou produto invalido")
    price_id = PRICE_IDS[lang].get(produto, "")
    nome_prod = PRODUTOS.get(lang, PRODUTOS["pt"]).get(produto, produto)
    meta = {"tipo": produto, "lang": lang, "nome": nome, "birth": birth, "email": email}
    if meta_extra:
        meta.update(meta_extra)
    pay_types = ["card", "boleto"] if MOEDA.get(lang, "brl") == "brl" else ["card"]
    locale = lang if lang in ["pt", "en", "es", "fr", "de", "it", "ja", "zh"] else "auto"
    if produto == "urna":
        success_url = f"{BASE_URL}/api/pay/urna-success?session_id={{CHECKOUT_SESSION_ID}}"
    elif produto == "eleitoral":
        success_url = f"{BASE_URL}/api/pay/eleitoral-success?session_id={{CHECKOUT_SESSION_ID}}"
    else:
        success_url = f"{BASE_URL}/api/pay/success?session_id={{CHECKOUT_SESSION_ID}}"
    try:
        if price_id and price_id.startswith("price_"):
            session = stripe.checkout.Session.create(
                mode="payment", payment_method_types=pay_types,
                line_items=[{"price": price_id, "quantity": 1}],
                customer_email=email or None,
                locale=locale, metadata=meta,
                success_url=success_url,
                cancel_url=f"{BASE_URL}/api/pay/cancel")
        else:
            session = stripe.checkout.Session.create(
                mode="payment", payment_method_types=pay_types,
                line_items=[{"price_data": {"currency": MOEDA.get(lang, "brl"),
                    "product_data": {"name": nome_prod},
                    "unit_amount": preco_local(produto, lang)}, "quantity": 1}],
                customer_email=email or None,
                locale=locale, metadata=meta,
                success_url=success_url,
                cancel_url=f"{BASE_URL}/api/pay/cancel")
        return {"id": session.id, "url": session.url}
    except Exception as e:
        logger.error(f"Stripe: {e}")
        raise HTTPException(500, "Erro ao criar pagamento")
# ===== ROTA GENERICA /pay/{produto} =====
_ALIAS_PRODUTO = {"complete": "completo"}
@app.post("/pay/{produto}")
def pay_produto(produto: str, req: PayReq):
    if not STRIPE_KEY:
        raise HTTPException(503, "Stripe nao configurado")
    produto = _ALIAS_PRODUTO.get(produto, produto)
    nome = req.nome
    nasc = req.nascimento
    lang = req.lang or "pt"
    return _criar_sessao(produto, lang, req.email, nome, nasc)
# ===== CHECKOUT NOME DE URNA =====
@app.post("/pay/urna")
def pay_urna(req: UrnaPayReq):
    if not STRIPE_KEY:
        raise HTTPException(503, "Stripe nao configurado")
    if len(req.nome_completo.strip()) < 3:
        raise HTTPException(400, "Nome obrigatorio")
    nomes = [n.strip() for n in [req.nome1, req.nome2, req.nome3, req.nome4, req.nome5] if n.strip()]
    if not nomes:
        raise HTTPException(400, "Pelo menos 1 nome")
    meta = {"tipo": "urna", "lang": req.lang or "pt", "nome_completo": req.nome_completo,
            "cargo": req.cargo, "email": req.email, "nome": req.nome_completo}
    for i, n in enumerate(nomes, 1):
        meta[f"nome{i}"] = n
    return _criar_sessao("urna", req.lang or "pt", req.email, req.nome_completo, "", meta)
# ===== CHECKOUT NUMERO ELEITORAL =====
@app.post("/pay/eleitoral")
def pay_eleitoral(req: EleitoralPayReq):
    if not STRIPE_KEY:
        raise HTTPException(503, "Stripe nao configurado")
    if not req.numero or len(req.numero) < 2:
        raise HTTPException(400, "Numero obrigatorio")
    meta = {"tipo": "eleitoral", "lang": req.lang or "pt", "sigla": req.numero,
            "cargo": req.cargo, "email": req.email, "numero_existente": "",
            "nome_completo": req.nome_completo}
    return _criar_sessao("eleitoral", req.lang or "pt", req.email, req.nome_completo, "", meta)
# ===== CHECKOUT COLETIVO (com desconto progressivo) =====
@app.get("/criar-checkout-coletivo")
async def criar_checkout_coletivo(lang: str = "pt", items: str = "[]"):
    if not STRIPE_KEY:
        raise HTTPException(503, "Stripe nao configurado")
    try:
        itens = json.loads(items)
    except Exception:
        raise HTTPException(400, "items invalidos")
    if not itens:
        raise HTTPException(400, "Nenhum item")
    qtd_total = sum(int(it.get("qtd", 0)) for it in itens if it.get("qtd"))
    desc = desconto_bc(qtd_total)
    line_items = []
    for it in itens:
        pid = it.get("id")
        qtd = int(it.get("qtd", 0))
        if not pid or qtd <= 0 or pid == "coletivo":
            continue
                # Sempre price_data: garante que o desconto progressivo seja cobrado de fato
        unit = preco_local(pid, lang)
        if desc > 0:
            unit = int(round(unit * (1 - desc)))
        line_items.append({"price_data": {"currency": MOEDA.get(lang, "brl"),
            "product_data": {"name": PRODUTOS.get(lang, PRODUTOS["pt"]).get(pid, pid)},
            "unit_amount": unit}, "quantity": qtd})
    if not line_items:
        raise HTTPException(400, "Itens invalidos")
    pay_types = ["card", "boleto"] if MOEDA.get(lang, "brl") == "brl" else ["card"]
    locale = lang if lang in ["pt", "en", "es", "fr", "de", "it", "ja", "zh"] else "auto"
    session = stripe.checkout.Session.create(
        mode="payment", payment_method_types=pay_types,
        line_items=line_items,
        locale=locale,
        metadata={"tipo": "coletivo", "lang": lang, "desconto": str(int(desc * 100)),
                  "itens": json.dumps(itens)},
        success_url=f"{BASE_URL}/api/pay/success?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{BASE_URL}/api/pay/cancel")
    return RedirectResponse(url=session.url)
    # ===== ROTA /criar-checkout (usada pelo site: comprar, pagarUrna, pagarEleitoral, confirmarBC) =====
@app.get("/criar-checkout")
async def criar_checkout_direto(lang: str = "pt", produto: str = "express",
                                qtd: int = 0, total: float = 0, itens: str = "",
                                nome: str = "", nascimento: str = "",
                                nome_completo: str = "", cargo: str = "vereador",
                                numero: str = "",
                                nome1: str = "", nome2: str = "", nome3: str = "",
                                nome4: str = "", nome5: str = "",
                                energia: str = ""):
    if not STRIPE_KEY:
        raise HTTPException(503, "Stripe nao configurado")
    if produto == "coletivo":
        return await criar_checkout_coletivo(lang=lang, items=itens or "[]")
    if produto not in PRODUTO_FAIXA:
        raise HTTPException(400, "Produto invalido")
    meta = {}
    if produto == "urna":
        meta = {"nome_completo": nome_completo, "cargo": cargo, "nome": nome_completo,
                "nome1": nome1, "nome2": nome2, "nome3": nome3,
                "nome4": nome4, "nome5": nome5}
    elif produto == "eleitoral":
        meta = {"sigla": numero, "cargo": cargo,
                "nome_completo": nome_completo, "numero_existente": ""}
    else:
        meta = {"energia": energia}    
    s = _criar_sessao(produto, lang, "", nome, nascimento, meta)
    return RedirectResponse(url=s["url"])
# ===== SUCESSO POS-PAGAMENTO =====
@app.get("/api/pay/success")
def pay_success(request: Request):
    sid = request.query_params.get("session_id", "")
    if not sid:
        return HTMLResponse("ERRO")
    try:
        s = stripe.checkout.Session.retrieve(sid)
        meta = getattr(s, "metadata", {}) or {}
        if hasattr(meta, "to_dict"):
            meta = meta.to_dict()
        nome = meta.get("nome", "Cliente")
        email = meta.get("email", "") or getattr(s, "customer_email", "") or ""
        bd = meta.get("birth", "")
        prod = meta.get("tipo", "express")
        lang = meta.get("lang", "pt")
        if not bd:
            bd = "2000-01-01"
        data = calc(nome, bd)
        db = SessionLocal()
        try:
            db.add(Order(id=uuid.uuid4().hex[:12], email=email or "sem-email",
                         product=prod, price=float(getattr(s, "amount_total", 0) or 0) / 100,
                         status="paid", payment_id=sid))
            db.commit()
        except Exception:
            pass
        finally:
            db.close()
        pn = PRODUTOS.get(lang, PRODUTOS["pt"]).get(prod, prod)
        if prod == "completo":
           pf = pdf17(data, nome, bd, lang)
        elif prod == "urna":
           pf = pdf_produto("urna", nome, bd, lang)
        elif prod == "eleitoral":
           pf = pdf_produto("eleitoral", nome, bd, lang)
        elif prod == "express":
           pf = pdf8(data, nome, bd, lang)
        else:
           pf = pdf_produto(prod, nome, bd, lang)
        html = pagina_sucesso(pf, nome, pn, lang)
        if pf and os.path.exists(pf):
            os.remove(pf)
        return HTMLResponse(html)
    except Exception as e:
        logger.error(f"Success: {e}")
        return HTMLResponse("ERRO")
@app.get("/api/pay/urna-success")
def pay_urna_success(request: Request):
    sid = request.query_params.get("session_id", "")
    if not sid:
        return HTMLResponse("ERRO")
    try:
        s = stripe.checkout.Session.retrieve(sid)
        meta = getattr(s, "metadata", {}) or {}
        if hasattr(meta, "to_dict"):
            meta = meta.to_dict()
        nc = meta.get("nome_completo", "")
        cr = meta.get("cargo", "vereador")
        nomes = [meta.get(f"nome{i}", "") for i in range(1, 6) if meta.get(f"nome{i}", "")]
        if not nomes:
            return HTMLResponse("ERRO")
        res, _, sugs = validar_nomes_urna(nomes, cr)
        cl = CARGO_INFO.get(cr, {}).get("label", cr)
        lang = meta.get("lang", "pt")
        pf = pdf_urna(nc, cl, res, sugs, lang)
        html = pagina_sucesso(pf, nc, PRODUTOS.get(lang, PRODUTOS["pt"]).get("urna", "Urna"), lang)
        if pf and os.path.exists(pf):
            os.remove(pf)
        return HTMLResponse(html)
    except Exception:
        return HTMLResponse("ERRO")
@app.get("/api/pay/eleitoral-success")
def pay_eleitoral_success(request: Request):
    sid = request.query_params.get("session_id", "")
    if not sid:
        return HTMLResponse("ERRO")
    try:
        s = stripe.checkout.Session.retrieve(sid)
        meta = getattr(s, "metadata", {}) or {}
        if hasattr(meta, "to_dict"):
            meta = meta.to_dict()
        sg = int(meta.get("sigla", "0"))
        cr = meta.get("cargo", "vereador")
        ne_str = meta.get("numero_existente", "")
        ss = str(sg).zfill(2)
        cl_map = {"vereador": "Vereador", "dep_estadual": "Dep. Estadual", "dep_federal": "Dep. Federal", "senador": "Senador"}
        cl2 = cl_map.get(cr, cr)
        sugs = gerar_numeros(sg, cr)
        ni = None
        if ne_str and len(ne_str) >= 3:
            try:
                ni = {"numero": ne_str, "energia": r1(sum(int(d) for d in ne_str))}
            except Exception:
                pass
        lang = meta.get("lang", "pt")
        pf = pdf_eleitoral(ss, cl2, sugs, ni, lang)
        html = pagina_sucesso(pf, f"Candidato {cl2}", PRODUTOS.get(lang, PRODUTOS["pt"]).get("eleitoral", "Eleitoral"), lang)
        if pf and os.path.exists(pf):
            os.remove(pf)
        return HTMLResponse(html)
    except Exception:
        return HTMLResponse("ERRO")
@app.get("/api/pay/cancel")
def pay_cancel():
    return HTMLResponse("<h1>Cancelado</h1><a href='/'>Voltar</a>")
# ===== CALCULO GRATIS =====
@app.post("/calculate")
def calculate(req: PayReq):
    db = SessionLocal()
    try:
        if len(req.nome.strip()) < 2:
           raise HTTPException(400, "Nome curto")
        if not req.nascimento:
           raise HTTPException(400, "Data obrigatoria")
        res = calc(req.nome, req.nascimento)
        cid = uuid.uuid4().hex[:8]
        db.add(Calc(id=cid, name=req.nome, birth_date=req.nascimento, email=req.email or "", **res))
        db.commit()
        res["download_pdf"] = False
        return {"id": cid, **res}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Calc: {e}")
        raise HTTPException(500, "Erro")
    finally:
        db.close()
@app.post("/calculate/urna")
def calc_urna(req: UrnaPayReq):
    nomes = [n.strip() for n in [req.nome1, req.nome2, req.nome3, req.nome4, req.nome5] if n.strip()]
    res, ideal, sugs = validar_nomes_urna(nomes, req.cargo)
    return {"resultados": res, "ideal": ideal, "sugestoes": sugs}
@app.post("/calculate/eleitoral")
def calc_eleitoral(req: EleitoralPayReq):
    sigla = int(req.numero) if req.numero.isdigit() else 0
    sugs = gerar_numeros(sigla, req.cargo)
    return {"sugestoes": sugs}
# ===== ROTAS BASE =====
@app.get("/")
def root():
    try:
        return HTMLResponse(open(os.path.join(os.path.dirname(__file__), "static", "index.html"),
                                 "r", encoding="utf-8").read())
    except Exception:
        try:
            return HTMLResponse(open(os.path.join(os.path.dirname(__file__), "index.html"),
                                     "r", encoding="utf-8").read())
        except Exception:
            return HTMLResponse("<h1>API ativa</h1>")
@app.get("/config")
def config():
    return {"stripe_pk": STRIPE_PUB}

@app.get("/api/health")
def health():
    return {"status": "ok", "stripe": bool(STRIPE_KEY)}
# ===== WEBHOOK STRIPE =====
@app.post("/stripe-webhook")
async def stripe_webhook(req: Request):
    payload = await req.body()
    sig = req.headers.get("stripe-signature", "")
    whsec = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    if whsec:
        try:
          event = stripe.Webhook.construct_event(payload, sig, whsec)
        except Exception:
            raise HTTPException(400, "Assinatura invalida")
    else:
        data = json.loads(payload)
        event = {"type": data.get("type", ""), "data": data.get("data", {})}
    if event["type"] == "checkout.session.completed":         # ← 4 espaços (CERTO)
        session = event["data"]["object"]
        meta = session.get("metadata", {})
        tipo = meta.get("tipo", "express")
        if tipo == "coletivo":
            try:
                items = json.loads(meta.get("itens", "[]"))
                gerados = _gerar_codigos_para_itens(items)
                logger.info(f"Coletivo: {len(gerados)} codigos gerados")
            except Exception as e:
                logger.error(f"Erro codigos coletivo: {e}")
        nome = meta.get("nome", "Cliente")
        lang = meta.get("lang", "pt")
        logger.info(f"Pagamento confirmado: {session['id']} -> {tipo}")
        entrega = _entregar_arquivo(tipo, nome, lang)   # entrega via PDF/QRCode com fallback
        logger.info(f"Entrega: {entrega}")
    return {"status": "success"}
# ===== SISTEMA DE BONUS =====
ARQ_BONUS = "bonus_codes.json"
def _carregar_codigos():
    try:
        with open(ARQ_BONUS, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
def _salvar_codigos(dados):
    with open(ARQ_BONUS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
def _gerar_codigo_bonus():
    chars = string.ascii_uppercase + string.digits
    p1 = "".join(secrets.choice(chars) for _ in range(4))
    p2 = "".join(secrets.choice(chars) for _ in range(4))
    return f"A1-{p1}-{p2}"
def _gerar_codigos_para_itens(itens):
    """Gera e salva os códigos A1-XXXX-XXXX de um pedido coletivo."""
    codigos = _carregar_codigos()
    gerados = []
    for item in itens:
        pid = item.get("id")
        qtd = int(item.get("qtd", 0))
        for _ in range(qtd):
            cod = _gerar_codigo_bonus()
            codigos[cod] = {"produto": pid, "usado": False}
            gerados.append({"codigo": cod, "produto": pid})
    _salvar_codigos(codigos)
    return gerados    
@app.post("/ativar-bonus")
async def ativar_bonus(req: AtivarBonusReq):
    codigos = _carregar_codigos()
    info = codigos.get(req.codigo)
    if not info:
        return {"ok": False, "msg": "Codigo nao encontrado"}
    if info.get("usado"):
        return {"ok": False, "msg": "Codigo ja utilizado"}
    info["usado"] = True
    info["data_uso"] = datetime.now().isoformat()
    _salvar_codigos(codigos)
    target = PRODUTO_TARGET.get(info.get("produto"), "inicio")
    return {"ok": True, "target": target, "produto": info.get("produto")}
@app.post("/gerar-codigos-coletivo")
async def gerar_codigos_coletivo(req: Request):
    corpo = await req.json()
    itens = corpo.get("itens", [])
    gerados = _gerar_codigos_para_itens(itens)
    return {"ok": True, "total": len(gerados), "codigos": gerados}
# ===== CAIXA DE SUGESTOES + BONUS =====
@app.post("/sugestao")
async def receber_sugestao(req: SugestaoReq):
    try:
        with open("sugestoes.json", "a") as f:
            f.write(json.dumps({"nome": req.nome, "mensagem": req.mensagem,
                                "data": datetime.now().isoformat()}, ensure_ascii=False) + "\n")
    except Exception as e:
        logger.error(f"Erro sugestao: {e}")
    return {"ok": True}

@app.post("/bonus")
async def solicitar_bonus(req: BonusReq):
    try:
        with open("bonus_solicitacoes.json", "a") as f:
            f.write(json.dumps({"nome": req.nome, "motivo": req.motivo,
                                "data": datetime.now().isoformat()}, ensure_ascii=False) + "\n")
    except Exception as e:
        logger.error(f"Erro bonus: {e}")
    return {"ok": True}
# ===== SISTEMA DE PUBLICIDADE GEOLOCALIZADA =====
ARQ_BANNERS = "banners.json"
PAIS_CONTINENTE = {
    "BR":"SA","AR":"SA","CL":"SA","CO":"SA","PE":"SA","UY":"SA","PY":"SA","BO":"SA","EC":"SA","VE":"SA",
    "US":"NA","CA":"NA","MX":"NA",
    "PT":"EU","ES":"EU","FR":"EU","DE":"EU","IT":"EU","GB":"EU","RU":"EU","NL":"EU","BE":"EU","CH":"EU","AT":"EU","IE":"EU",
    "CN":"AS","JP":"AS","IN":"AS","KR":"AS","SA":"AS","AE":"AS","IL":"AS","TR":"AS","ID":"AS","PK":"AS","BD":"AS",
    "EG":"AF","NG":"AF","ZA":"AF","KE":"AF","MA":"AF",
    "AU":"OC","NZ":"OC"
}
def _carregar_banners():
    try:
        with open(ARQ_BANNERS, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
def _salvar_banners(banners):
    with open(ARQ_BANNERS, "w", encoding="utf-8") as f:
        json.dump(banners, f, ensure_ascii=False, indent=2)
@app.get("/api/banner")
async def get_banner(posicao: str = "topo", pais: str = "BR"):
    banners = _carregar_banners()
    if not banners:
        return {"ok": False, "banner": None}
    continente = PAIS_CONTINENTE.get(pais.upper(), "")
    hoje = date.today().isoformat()
    for b in banners:
        if not b.get("ativo") or b.get("posicao") != posicao:
            continue
        if b.get("tipo") == "temporario":
            if b.get("data_fim") and hoje > b["data_fim"]:
                continue
            if b.get("data_inicio") and hoje < b["data_inicio"]:
                continue
        if b.get("escopo") == "pais" and b.get("pais") == pais.upper():
            return {"ok": True, "banner": b}
        if b.get("escopo") == "continente" and b.get("continente") == continente:
            return {"ok": True, "banner": b}
        if b.get("escopo") == "mundo":
            return {"ok": True, "banner": b}
    return {"ok": False, "banner": None}
# ===== INICIALIZACAO =====
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "10000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
