# -*- coding: utf-8 -*-
# main.py - A1ELOS Global Numerology API
# VERSÃO FINAL LIMPA E UNIFICADA - 02/08/2026
# Fusão: main exitoso (4 produtos) + 15 produtos/12 idiomas/bônus/banners

import os, json, uuid, logging, secrets, string, base64, traceback
from datetime import date, datetime
from typing import Optional
import stripe
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, Content, Attachment, FileContent, FileName, FileType, Disposition
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import dateutil.parser as dp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

STRIPE_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_PUB = os.getenv("STRIPE_PUBLISHABLE_KEY", "")
SENDGRID_KEY = os.getenv("SENDGRID_API_KEY", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@a1elos.com.br")
FROM_NAME = "A1ELOS Numerologia Global"
BASE_URL = os.getenv("BASE_URL", os.getenv("SITE_URL", "https://global-numerology.onrender.com"))
DB_URL = os.getenv("DATABASE_URL", "sqlite:///./numerologia.db")
ADMIN_EMAIL = "arvigne@gmail.com"

if STRIPE_KEY:
    stripe.api_key = STRIPE_KEY

# ===== BANCO DE DADOS (funciona com SQLite E PostgreSQL) =====
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

Base.metadata.create_all(bind=engine)

# ===== APP (criado ANTES de qualquer rota) =====
app = FastAPI(title="A1ELOS Global Numerology")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])

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

# ===== FAIXAS DE PREÇO (promocionais de abertura) =====
PRODUTO_FAIXA = {
    "express": 0, "vida": 0, "completo": 1, "ia": 1,
    "urna": 2, "eleitoral": 2, "imovel": 2, "calendario": 2,
    "artistico": 3, "bebe": 3, "assinatura": 3,
    "negocio": 4, "casal": 4, "familia": 5
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

# ===== NOMES DOS 15 PRODUTOS EM 12 IDIOMAS =====
PRODUTOS = {
    "pt": {"express": "Mapa Express", "vida": "Qual Vida/Ano", "completo": "Mapa Completo",
        "ia": "Pesquisa IA de Nomes", "urna": "Validação Nome de Urna", "eleitoral": "Número Eleitoral",
        "imovel": "Número do Imóvel", "calendario": "Calendário Mensal Energético",
        "artistico": "Validação Nome Artístico", "bebe": "Planejamento Nome de Bebê",
        "assinatura": "Validação de Assinaturas", "negocio": "Nome para Negócio/Produto",
        "casal": "Mapa do Casal", "familia": "Mapa Família Premium", "coletivo": "Bônus Coletivo/Empresarial"},
    "en": {"express": "Express Map", "vida": "Life Phase & Year", "completo": "Complete Map",
        "ia": "AI Name Search", "urna": "Ballot Name Validation", "eleitoral": "Electoral Number",
        "imovel": "Property Number", "calendario": "Monthly Energy Calendar",
        "artistico": "Artistic Name Validation", "bebe": "Baby Name Planning",
        "assinatura": "Signature Validation", "negocio": "Business & Product Name",
        "casal": "Couple Map", "familia": "Premium Family Map", "coletivo": "Corporate Bonus"},
    "es": {"express": "Mapa Exprés", "vida": "Ciclo de Vida y Año", "completo": "Mapa Completo",
        "ia": "Búsqueda IA de Nombres", "urna": "Validación Nombre de Urna", "eleitoral": "Número Electoral",
        "imovel": "Número de la Propiedad", "calendario": "Calendario Mensual Energético",
        "artistico": "Validación Nombre Artístico", "bebe": "Planificación Nombre de Bebé",
        "assinatura": "Validación de Firmas", "negocio": "Nombre para Negocio/Producto",
        "casal": "Mapa de Pareja", "familia": "Mapa Familiar Premium", "coletivo": "Bono Corporativo"},
    "it": {"express": "Mappa Espressa", "vida": "Fase di Vita e Anno", "completo": "Mappa Completa",
        "ia": "Ricerca IA Nomi", "urna": "Validazione Nome della Scheda", "eleitoral": "Numero Elettorale",
        "imovel": "Numero dell'Immobile", "calendario": "Calendario Mensile Energetico",
        "artistico": "Validazione Nome d'Arte", "bebe": "Pianificazione Nome del Bambino",
        "assinatura": "Validazione delle Firme", "negocio": "Nome per Business/Prodotto",
        "casal": "Mappa di Coppia", "familia": "Mappa Famiglia Premium", "coletivo": "Bonus Aziendale"},
    "fr": {"express": "Carte Express", "vida": "Phase de Vie et Année", "completo": "Carte Complète",
        "ia": "Recherche IA de Noms", "urna": "Validation Nom du Bulletin", "eleitoral": "Numéro Électoral",
        "imovel": "Numéro du Bien", "calendario": "Calendrier Mensuel Énergétique",
        "artistico": "Validation Nom de Scène", "bebe": "Planification Prénom de Bébé",
        "assinatura": "Validation des Signatures", "negocio": "Nom pour Entreprise/Produit",
        "casal": "Carte du Couple", "familia": "Carte Famille Premium", "coletivo": "Bonus d'Entreprise"},
    "de": {"express": "Express-Karte", "vida": "Lebensphase & Jahr", "completo": "Vollständige Karte",
        "ia": "KI-Namenssuche", "urna": "Stimmzettelname-Validierung", "eleitoral": "Wahlnummer",
        "imovel": "Immobiliennummer", "calendario": "Monatlicher Energiekalender",
        "artistico": "Künstlername-Validierung", "bebe": "Babynamen-Planung",
        "assinatura": "Unterschrifts-Validierung", "negocio": "Name für Unternehmen/Produkt",
        "casal": "Paar-Karte", "familia": "Premium-Familien-Karte", "coletivo": "Unternehmensbonus"},
    "ja": {"express": "エクスプレスマップ", "vida": "ライフステージと年", "completo": "完全マップ",
        "ia": "AI名前検索", "urna": "投票用紙名の検証", "eleitoral": "選挙番号",
        "imovel": "不動産番号", "calendario": "月間エネルギーカレンダー",
        "artistico": "芸名の検証", "bebe": "赤ちゃんの名前計画",
        "assinatura": "署名の検証", "negocio": "ビジネス・商品名",
        "casal": "カップルマップ", "familia": "プレミアム家族マップ", "coletivo": "法人ボーナス"},
    "zh": {"express": "快速地图", "vida": "生命阶段与年份", "completo": "完整地图",
        "ia": "AI名字搜索", "urna": "选票名称验证", "eleitoral": "选举号码",
        "imovel": "房产号码", "calendario": "每月能量日历",
        "artistico": "艺名验证", "bebe": "宝宝取名规划",
        "assinatura": "签名验证", "negocio": "企业/产品名称",
        "casal": "情侣地图", "familia": "高级家庭地图", "coletivo": "企业奖励"},
    "ru": {"express": "Экспресс-карта", "vida": "Жизненный этап и год", "completo": "Полная карта",
        "ia": "ИИ-поиск имён", "urna": "Проверка названия бюллетеня", "eleitoral": "Избирательный номер",
        "imovel": "Номер недвижимости", "calendario": "Ежемесячный энергетический календарь",
        "artistico": "Проверка сценического имени", "bebe": "Планирование имени ребёнка",
        "assinatura": "Проверка подписей", "negocio": "Название для бизнеса/продукта",
        "casal": "Карта пары", "familia": "Премиальная семейная карта", "coletivo": "Корпоративный бонус"},
    "hi": {"express": "त्वरित मानचित्र", "vida": "जीवन चरण और वर्ष", "completo": "पूर्ण मानचित्र",
        "ia": "AI नाम खोज", "urna": "मतपत्र नाम सत्यापन", "eleitoral": "निर्वाचन संख्या",
        "imovel": "संपत्ति संख्या", "calendario": "मासिक ऊर्जा कैलेंडर",
        "artistico": "कलात्मक नाम सत्यापन", "bebe": "शिशु नाम योजना",
        "assinatura": "हस्ताक्षर सत्यापन", "negocio": "व्यवसाय/उत्पाद नाम",
        "casal": "युगल मानचित्र", "familia": "प्रीमियम परिवार मानचित्र", "coletivo": "कॉर्पोरेट बोनस"},
    "he": {"express": "מפה מהירה", "vida": "שלב חיים ושנה", "completo": "מפה מלאה",
        "ia": "חיפוש שמות AI", "urna": "אימות שם פתק", "eleitoral": "מספר בחירות",
        "imovel": "מספר נכס", "calendario": "לוח אנרגיה חודשי",
        "artistico": "אימות שם במה", "bebe": "תכנון שם לתינוק",
        "assinatura": "אימות חתימות", "negocio": "שם לעסק/מוצר",
        "casal": "מפת זוג", "familia": "מפת משפחה פרימיום", "coletivo": "בונוס ארגוני"},
    "ar": {"express": "خريطة سريعة", "vida": "مرحلة الحياة والسنة", "completo": "خريطة كاملة",
        "ia": "بحث الأسماء بالذكاء الاصطناعي", "urna": "التحقق من اسم الاقتراع", "eleitoral": "الرقم الانتخابي",
        "imovel": "رقم العقار", "calendario": "تقويم الطاقة الشهري",
        "artistico": "التحقق من الاسم الفني", "bebe": "تخطيط اسم الطفل",
        "assinatura": "التحقق من التوقيعات", "negocio": "اسم للأعمال/المنتج",
        "casal": "خريطة الزوجين", "familia": "خريطة العائلة المميزة", "coletivo": "مكافأة الشركات"}
}

# ===== PRICE IDS STRIPE (4 reais x 12 idiomas + 11 placeholders) =====
PRICE_IDS = {
    "pt": {"express": "price_1TxocVBMLa84bVJ0EL0kb9Dn", "completo": "price_1TxohlBMLa84bVJ0jVj9307b",
           "urna": "price_1TxollBMLa84bVJ0Wk5zIak6", "eleitoral": "price_1TxopFBMLa84bVJ0jvtJExVj",
           "vida": "PRICE_ID_PT_VIDA", "ia": "PRICE_ID_PT_IA", "imovel": "PRICE_ID_PT_IMOVEL",
           "calendario": "PRICE_ID_PT_CALENDARIO", "artistico": "PRICE_ID_PT_ARTISTICO",
           "bebe": "PRICE_ID_PT_BEBE", "assinatura": "PRICE_ID_PT_ASSINATURA",
           "negocio": "PRICE_ID_PT_NEGOCIO", "casal": "PRICE_ID_PT_CASAL", "familia": "PRICE_ID_PT_FAMILIA"},
    "en": {"express": "price_1TxotnBMLa84bVJ00SGo4kjO", "completo": "price_1TxoxfBMLa84bVJ0VgQVddZX",
           "urna": "price_1Txp1jBMLa84bVJ06W4559rN", "eleitoral": "price_1Txp5aBMLa84bVJ0GqrvBrIk",
           "vida": "PRICE_ID_EN_VIDA", "ia": "PRICE_ID_EN_IA", "imovel": "PRICE_ID_EN_IMOVEL",
           "calendario": "PRICE_ID_EN_CALENDARIO", "artistico": "PRICE_ID_EN_ARTISTICO",
           "bebe": "PRICE_ID_EN_BEBE", "assinatura": "PRICE_ID_EN_ASSINATURA",
           "negocio": "PRICE_ID_EN_NEGOCIO", "casal": "PRICE_ID_EN_CASAL", "familia": "PRICE_ID_EN_FAMILIA"},
    "es": {"express": "price_1TyD2oBMLa84bVJ0HvSTMozS", "completo": "price_1TyD6NBMLa84bVJ0s5y2OtSr",
           "urna": "price_1TyDB0BMLa84bVJ0baUEGa2P", "eleitoral": "price_1TyDCsBMLa84bVJ0NRp5uOKU",
           "vida": "PRICE_ID_ES_VIDA", "ia": "PRICE_ID_ES_IA", "imovel": "PRICE_ID_ES_IMOVEL",
           "calendario": "PRICE_ID_ES_CALENDARIO", "artistico": "PRICE_ID_ES_ARTISTICO",
           "bebe": "PRICE_ID_ES_BEBE", "assinatura": "PRICE_ID_ES_ASSINATURA",
           "negocio": "PRICE_ID_ES_NEGOCIO", "casal": "PRICE_ID_ES_CASAL", "familia": "PRICE_ID_ES_FAMILIA"},
    "it": {"express": "price_1TyEtPBMLa84bVJ02T3hWgMD", "completo": "price_1TyEwfBMLa84bVJ0Fh9etZKk",
           "urna": "price_1TyEz0BMLa84bVJ0Qkjg7Y0X", "eleitoral": "price_1TyF2PBMLa84bVJ0lropcWH8",
           "vida": "PRICE_ID_IT_VIDA", "ia": "PRICE_ID_IT_IA", "imovel": "PRICE_ID_IT_IMOVEL",
           "calendario": "PRICE_ID_IT_CALENDARIO", "artistico": "PRICE_ID_IT_ARTISTICO",
           "bebe": "PRICE_ID_IT_BEBE", "assinatura": "PRICE_ID_IT_ASSINATURA",
           "negocio": "PRICE_ID_IT_NEGOCIO", "casal": "PRICE_ID_IT_CASAL", "familia": "PRICE_ID_IT_FAMILIA"},
    "fr": {"express": "price_1TyDnQBMLa84bVJ0K9DBz2mk", "completo": "price_1TyDrjBMLa84bVJ0cstgcPbY",
           "urna": "price_1TyDw1BMLa84bVJ0EV0OnINW", "eleitoral": "price_1TyDxsBMLa84bVJ0n2t4jOfZ",
           "vida": "PRICE_ID_FR_VIDA", "ia": "PRICE_ID_FR_IA", "imovel": "PRICE_ID_FR_IMOVEL",
           "calendario": "PRICE_ID_FR_CALENDARIO", "artistico": "PRICE_ID_FR_ARTISTICO",
           "bebe": "PRICE_ID_FR_BEBE", "assinatura": "PRICE_ID_FR_ASSINATURA",
           "negocio": "PRICE_ID_FR_NEGOCIO", "casal": "PRICE_ID_FR_CASAL", "familia": "PRICE_ID_FR_FAMILIA"},
    "de": {"express": "price_1TyFJaBMLa84bVJ0BDPNQUjz", "completo": "price_1TyFLKBMLa84bVJ0RT0bkKpW",
           "urna": "price_1TyFO2BMLa84bVJ0FIoh7co1", "eleitoral": "price_1TyFTxBMLa84bVJ0qw6LQvVI",
           "vida": "PRICE_ID_DE_VIDA", "ia": "PRICE_ID_DE_IA", "imovel": "PRICE_ID_DE_IMOVEL",
           "calendario": "PRICE_ID_DE_CALENDARIO", "artistico": "PRICE_ID_DE_ARTISTICO",
           "bebe": "PRICE_ID_DE_BEBE", "assinatura": "PRICE_ID_DE_ASSINATURA",
           "negocio": "PRICE_ID_DE_NEGOCIO", "casal": "PRICE_ID_DE_CASAL", "familia": "PRICE_ID_DE_FAMILIA"},
    "ja": {"express": "price_1TyJ5HBMLa84bVJ00nZLnuV1", "completo": "price_1TyJJgBMLa84bVJ0fkO5nSFT",
           "urna": "price_1TyJOzBMLa84bVJ0BAPegYVD", "eleitoral": "price_1TyJRwBMLa84bVJ0PLA1CIuH",
           "vida": "PRICE_ID_JA_VIDA", "ia": "PRICE_ID_JA_IA", "imovel": "PRICE_ID_JA_IMOVEL",
           "calendario": "PRICE_ID_JA_CALENDARIO", "artistico": "PRICE_ID_JA_ARTISTICO",
           "bebe": "PRICE_ID_JA_BEBE", "assinatura": "PRICE_ID_JA_ASSINATURA",
           "negocio": "PRICE_ID_JA_NEGOCIO", "casal": "PRICE_ID_JA_CASAL", "familia": "PRICE_ID_JA_FAMILIA"},
    "zh": {"express": "price_1TyKXeBMLa84bVJ07Q6w0j6G", "completo": "price_1TyKZfBMLa84bVJ0bgYSm8e2",
           "urna": "price_1TyKdWBMLa84bVJ0TIP0Knbi", "eleitoral": "price_1TyKitBMLa84bVJ0lFgyKya0",
           "vida": "PRICE_ID_ZH_VIDA", "ia": "PRICE_ID_ZH_IA", "imovel": "PRICE_ID_ZH_IMOVEL",
           "calendario": "PRICE_ID_ZH_CALENDARIO", "artistico": "PRICE_ID_ZH_ARTISTICO",
           "bebe": "PRICE_ID_ZH_BEBE", "assinatura": "PRICE_ID_ZH_ASSINATURA",
           "negocio": "PRICE_ID_ZH_NEGOCIO", "casal": "PRICE_ID_ZH_CASAL", "familia": "PRICE_ID_ZH_FAMILIA"},
    "ru": {"express": "price_1TyJxhBMLa84bVJ0aQxWf1Tp", "completo": "price_1TyK1CBMLa84bVJ0SsvJjSqb",
           "urna": "price_1TyK3NBMLa84bVJ0GCSVqMe0", "eleitoral": "price_1TyK7hBMLa84bVJ004FNS2fZ",
           "vida": "PRICE_ID_RU_VIDA", "ia": "PRICE_ID_RU_IA", "imovel": "PRICE_ID_RU_IMOVEL",
           "calendario": "PRICE_ID_RU_CALENDARIO", "artistico": "PRICE_ID_RU_ARTISTICO",
           "bebe": "PRICE_ID_RU_BEBE", "assinatura": "PRICE_ID_RU_ASSINATURA",
           "negocio": "PRICE_ID_RU_NEGOCIO", "casal": "PRICE_ID_RU_CASAL", "familia": "PRICE_ID_RU_FAMILIA"},
    "hi": {"express": "price_1TyG1uBMLa84bVJ0NY4TpZnO", "completo": "price_1TyG84BMLa84bVJ05zeaelyO",
           "urna": "price_1TyGD5BMLa84bVJ0hEnIEwaS", "eleitoral": "price_1TyGFYBMLa84bVJ0zZTHtAuT",
           "vida": "PRICE_ID_HI_VIDA", "ia": "PRICE_ID_HI_IA", "imovel": "PRICE_ID_HI_IMOVEL",
           "calendario": "PRICE_ID_HI_CALENDARIO", "artistico": "PRICE_ID_HI_ARTISTICO",
           "bebe": "PRICE_ID_HI_BEBE", "assinatura": "PRICE_ID_HI_ASSINATURA",
           "negocio": "PRICE_ID_HI_NEGOCIO", "casal": "PRICE_ID_HI_CASAL", "familia": "PRICE_ID_HI_FAMILIA"},
    "he": {"express": "price_1TyIKeBMLa84bVJ0W02dbXOt", "completo": "price_1TyIO0BMLa84bVJ08P0j9THk",
           "urna": "price_1TyIPbBMLa84bVJ08GnGksRk", "eleitoral": "price_1TyISQBMLa84bVJ0sb7xjIyV",
           "vida": "PRICE_ID_HE_VIDA", "ia": "PRICE_ID_HE_IA", "imovel": "PRICE_ID_HE_IMOVEL",
           "calendario": "PRICE_ID_HE_CALENDARIO", "artistico": "PRICE_ID_HE_ARTISTICO",
           "bebe": "PRICE_ID_HE_BEBE", "assinatura": "PRICE_ID_HE_ASSINATURA",
           "negocio": "PRICE_ID_HE_NEGOCIO", "casal": "PRICE_ID_HE_CASAL", "familia": "PRICE_ID_HE_FAMILIA"},
    "ar": {"express": "price_1TyHXkBMLa84bVJ0DDl7y8rT", "completo": "price_1TyHerBMLa84bVJ0UIFTeKLW",
           "urna": "price_1TyHpxBMLa84bVJ0Z9Ck3rk3", "eleitoral": "price_1TyHrvBMLa84bVJ0RWjoe4Gz",
           "vida": "PRICE_ID_AR_VIDA", "ia": "PRICE_ID_AR_IA", "imovel": "PRICE_ID_AR_IMOVEL",
           "calendario": "PRICE_ID_AR_CALENDARIO", "artistico": "PRICE_ID_AR_ARTISTICO",
           "bebe": "PRICE_ID_AR_BEBE", "assinatura": "PRICE_ID_AR_ASSINATURA",
           "negocio": "PRICE_ID_AR_NEGOCIO", "casal": "PRICE_ID_AR_CASAL", "familia": "PRICE_ID_AR_FAMILIA"}
}

PRODUTO_TARGET = {
    "express": "mapa", "vida": "vida", "completo": "mapa", "ia": "pesquisa-ia",
    "urna": "urna", "eleitoral": "eleitoral", "imovel": "imovel", "calendario": "calendario",
    "artistico": "artistico", "bebe": "bebe", "assinatura": "assinatura",
    "negocio": "negocio", "casal": "casal", "familia": "familia", "coletivo": "corporativo"
}

# ===== MODELOS PYDANTIC =====
class PayReq(BaseModel):
    name: str = ""
    email: str = ""
    product: Optional[str] = "express"
    price: Optional[float] = 0
    calculation_id: Optional[str] = None
    birth_date: Optional[str] = ""
    lang: Optional[str] = "pt"

class UrnaPayReq(BaseModel):
    nome_completo: str
    cargo: str = "vereador"
    nome1: str = ""
    nome2: str = ""
    nome3: str = ""
    nome4: str = ""
    nome5: str = ""
    email: str = ""
    lang: Optional[str] = "pt"

class EleitoralPayReq(BaseModel):
    sigla: int
    cargo: str = "vereador"
    numero_existente: Optional[str] = ""
    email: str = ""
    lang: Optional[str] = "pt"

class SugestaoReq(BaseModel):
    nome: str = ""
    email: str = ""
    mensagem: str

class BonusReq(BaseModel):
    nome: str
    email: str
    produto: str = ""
    mensagem: str = ""

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

# ===== CÁLCULO NUMEROLÓGICO =====
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

# ===== PDF EXPRESS (R$ 8) =====
def pdf8(data, nome, bd):
    path = f"/tmp/p8_{uuid.uuid4().hex[:8]}.pdf"
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=50, rightMargin=50,
                            topMargin=40, bottomMargin=30)
    e = []
    e.append(Spacer(1, 15))
    e.append(Paragraph("MAPA EXPRESS", estilo(20, True, GOLD, TA_CENTER, 0, 6)))
    e.append(Paragraph(nome.upper(), estilo(12, True, DARK, TA_CENTER, 0, 2)))
    e.append(Paragraph(bd, estilo(9, False, GRAY, TA_CENTER, 0, 10)))
    td = [["Numero", "Valor"]] + [[l, str(data[k])] for k, l in [
        ("life_path", "Caminho de Vida"), ("expression", "Expressao"),
        ("soul_urge", "Motivacao"), ("personality", "Personalidade"),
        ("destiny", "Destino")]]
    tbl = Table(td, colWidths=[200, 100])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GOLD),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
        ("BACKGROUND", (0, 1), (-1, -1), LGRAY),
    ]))
    e.append(tbl)
    e.append(Spacer(1, 10))
    e.append(Paragraph("(c) A1ELOS", estilo(7, False, GRAY, TA_CENTER)))
    doc.build(e)
    return path

# ===== PDF COMPLETO (R$ 17) =====
def pdf17(data, nome, bd_str):
    path = f"/tmp/p17_{uuid.uuid4().hex[:8]}.pdf"
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=50, rightMargin=50,
                            topMargin=35, bottomMargin=25)
    e = []
    lp = data["life_path"]
    e.append(Spacer(1, 15))
    e.append(Paragraph("MAPA COMPLETO", estilo(20, True, GOLD, TA_CENTER, 0, 6)))
    e.append(Paragraph(nome.upper(), estilo(12, True, DARK, TA_CENTER, 0, 2)))
    e.append(Paragraph(bd_str, estilo(9, False, GRAY, TA_CENTER, 0, 10)))
    e.append(Paragraph(f"Caminho de Vida {lp}", estilo(11, False, DARK, TA_CENTER)))
    e.append(Spacer(1, 8))
    td = [["Numero", "Valor"]] + [[l, str(data[k])] for k, l in [
        ("life_path", "Caminho de Vida"), ("expression", "Expressao"),
        ("soul_urge", "Motivacao"), ("personality", "Personalidade"),
        ("destiny", "Destino")]]
    tbl = Table(td, colWidths=[200, 100])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GOLD),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
        ("BACKGROUND", (0, 1), (-1, -1), LGRAY),
    ]))
    e.append(tbl)
    e.append(Spacer(1, 10))
    bb = dp.parse(bd_str.split(" ")[0] if " " in bd_str else bd_str).date()
    d, m, a = bb.day, bb.month, bb.year
    fe = max(36 - min(lp, 36), 25)
    e.append(Paragraph(f"Ciclo 1 (0-{fe}a) | Ciclo 2 ({fe+1}-{fe+27}a) | Ciclo 3 ({fe+28}+a)", estilo(10, False, DARK)))
    d1 = r1(abs(d - m))
    d2 = r1(abs(m - r1(a)))
    dp_ = r1(abs(d1 - d2))
    e.append(Paragraph(f"Desafios: {d1} | {d2} | Principal {dp_}", estilo(10, False, DARK)))
    ap = r1(d + m + datetime.utcnow().year)
    e.append(Paragraph(f"Ano Pessoal {datetime.utcnow().year}: {ap}", estilo(10, False, DARK)))
    grid = calc_grid(nome)
    pres = [str(n) for n in range(1, 10) if grid.get(n, 0) > 0]
    aus = [str(n) for n in range(1, 10) if grid.get(n, 0) == 0]
    e.append(Paragraph(f"Grade: Presentes {', '.join(pres) or '-'} | Carencias {', '.join(aus) or '-'}", estilo(10, False, DARK)))
    e.append(Spacer(1, 15))
    e.append(Paragraph("(c) A1ELOS", estilo(7, False, GRAY, TA_CENTER)))
    doc.build(e)
    return path

# ===== PDF NOME DE URNA (R$ 26) =====
def pdf_urna(nc, cl, resultados, sugestoes):
    path = f"/tmp/u_{uuid.uuid4().hex[:8]}.pdf"
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=50, rightMargin=50,
                            topMargin=40, bottomMargin=30)
    e = []
    e.append(Spacer(1, 15))
    e.append(Paragraph("VALIDACAO DE NOME DE URNA", estilo(20, True, GOLD, TA_CENTER)))
    e.append(Paragraph(nc.title(), estilo(12, True, DARK, TA_CENTER)))
    e.append(Paragraph(f"Cargo: {cl}", estilo(9, False, GRAY, TA_CENTER)))
    for r in resultados:
        ic = "OK" if r["eh_ideal"] else "X"
        e.append(Paragraph(f'{ic} {r["nome"]} - Energia {r["energia"]}', estilo(11, True, DARK)))
        if r["letras"]:
            ls = ", ".join([f'{l["letra"]}={l["valor"]}' for l in r["letras"]])
            e.append(Paragraph(f"{ls} -> {r['soma']} -> {r['energia']}", estilo(9, False, GRAY)))
        e.append(Paragraph(r["explicacao"], estilo(10, False, DARK)))
    if sugestoes:
        e.append(Spacer(1, 10))
        e.append(Paragraph("Sugestoes:", estilo(16, True, GOLD)))
        for s in sugestoes[:3]:
            e.append(Paragraph(f'{s["nome"]} - Energia {s["energia"]}', estilo(11, False, DARK)))
    e.append(Paragraph("(c) A1ELOS", estilo(7, False, GRAY, TA_CENTER)))
    doc.build(e)
    return path

# ===== PDF NÚMERO ELEITORAL (R$ 26) =====
def pdf_eleitoral(ss, cl, sugestoes, ni=None):
    path = f"/tmp/e_{uuid.uuid4().hex[:8]}.pdf"
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=50, rightMargin=50,
                            topMargin=40, bottomMargin=30)
    e = []
    e.append(Spacer(1, 15))
    e.append(Paragraph("NUMERO ELEITORAL", estilo(20, True, GOLD, TA_CENTER)))
    e.append(Paragraph(f"Cargo: {cl} | Sigla: {ss}", estilo(9, False, GRAY, TA_CENTER)))
    e.append(Spacer(1, 10))
    ids = [s for s in sugestoes if s.get("ideal")]
    fbs = [s for s in sugestoes if not s.get("ideal")]
    if ids:
        e.append(Paragraph("Opcoes com Energia 8 - IDEAL:", estilo(11, True, DARK)))
        for s in ids:
            e.append(Paragraph(f'{s["numero"]} - Energia 8!', estilo(11, False, colors.HexColor("#4CAF50"))))
    if fbs:
        e.append(Paragraph("Opcoes Alternativas:", estilo(11, True, DARK)))
        for s in fbs:
            e.append(Paragraph(f'{s["numero"]} - Energia {s["energia"]}', estilo(11, False, DARK)))
    if ni:
        e.append(Paragraph(f'Numero: {ni["numero"]} - Energia: {ni["energia"]}', estilo(11, False, DARK)))
    e.append(Paragraph("(c) A1ELOS", estilo(7, False, GRAY, TA_CENTER)))
    doc.build(e)
    return path

# ===== PDF GENÉRICO (11 produtos novos) =====
def pdf_produto(produto, nome, bd_str, lang="pt"):
    path = f"/tmp/p_{uuid.uuid4().hex[:8]}.pdf"
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=50, rightMargin=50,
                            topMargin=40, bottomMargin=30)
    titulo = PRODUTOS.get(lang, PRODUTOS["pt"]).get(produto, produto).upper()
    data = calc(nome, bd_str)
    e = []
    e.append(Spacer(1, 15))
    e.append(Paragraph(titulo, estilo(18, True, GOLD, TA_CENTER, 0, 6)))
    e.append(Paragraph(nome.upper(), estilo(12, True, DARK, TA_CENTER, 0, 2)))
    e.append(Paragraph(bd_str, estilo(9, False, GRAY, TA_CENTER, 0, 10)))
    td = [["Numero", "Valor"]] + [[l, str(data[k])] for k, l in [
        ("life_path", "Caminho de Vida"), ("expression", "Expressao"),
        ("soul_urge", "Motivacao"), ("personality", "Personalidade"),
        ("destiny", "Destino")]]
    tbl = Table(td, colWidths=[200, 100])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GOLD),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
        ("BACKGROUND", (0, 1), (-1, -1), LGRAY),
    ]))
    e.append(tbl)
    e.append(Spacer(1, 10))
    e.append(Paragraph("(c) A1ELOS", estilo(7, False, GRAY, TA_CENTER)))
    doc.build(e)
    return path

# ===== ENVIO DE EMAIL (SendGrid com anexo) =====
def enviar_email(para, assunto, corpo, anexo=None):
    if not SENDGRID_KEY:
        return False
    try:
        sg = SendGridAPIClient(SENDGRID_KEY)
        mail = Mail(Email(FROM_EMAIL, FROM_NAME), para, assunto, Content("text/plain", corpo))
        if anexo and os.path.exists(anexo):
            with open(anexo, "rb") as f:
                enc = base64.b64encode(f.read()).decode()
            mail.attachment = Attachment(FileContent(enc), FileName("Documento.pdf"),
                                         FileType("application/pdf"), Disposition("attachment"))
        sg.send(mail)
        return True
    except Exception as e:
        logger.error(f"SendGrid: {e}")
        return False

# ===== EMAIL SIMPLES (SMTP - sugestões e bônus) =====
def _enviar_email_simples(destinatario, assunto, corpo):
    try:
        msg = MIMEMultipart()
        msg["From"] = FROM_EMAIL
        msg["To"] = destinatario
        msg["Subject"] = assunto
        msg.attach(MIMEText(corpo, "plain", "utf-8"))
        with smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT", 587))) as s:
            s.starttls()
            s.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
            s.send_message(msg)
        return True
    except Exception as e:
        logger.error(f"SMTP: {e}")
        return False

# ===== PÁGINA DE SUCESSO COM DOWNLOAD DO PDF =====
def pagina_sucesso(pdf_path, nome, prod_nome):
    b64 = ""
    if pdf_path and os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
    btn = ""
    if b64:
        btn = (f'<a href="data:application/pdf;base64,{b64}" download="Documento.pdf" '
               f'style="display:inline-block;padding:18px 50px;background:#C9A94E;color:#000;'
               f'text-decoration:none;border-radius:50px;font-weight:700;font-size:1.2rem;margin:25px 0">📥 BAIXAR PDF</a>')
    return (f'<html><body style="background:#0a0a0a;color:#fff;text-align:center;padding:40px;'
            f'font-family:sans-serif"><h1 style="color:#C9A94E">✅ Confirmado!</h1>'
            f'<p>Ola <b>{nome}</b>, seu {prod_nome} foi gerado.</p>{btn}'
            f'<a href="/" style="color:#C9A94E">Voltar</a></body></html>')

# ===== CRIAÇÃO DE SESSÃO STRIPE (dinâmica) =====
def _criar_sessao(produto, lang="pt", email="", nome="", birth="", meta_extra=None):
    if lang not in PRICE_IDS or produto not in PRICE_IDS[lang]:
        raise HTTPException(status_code=400, detail="Idioma ou produto inválido")
    price_id = PRICE_IDS[lang].get(produto, "")
    nome_prod = PRODUTOS.get(lang, PRODUTOS["pt"]).get(produto, produto)
    meta = {"tipo": produto, "lang": lang, "nome": nome, "birth": birth, "email": email}
    if meta_extra:
        meta.update(meta_extra)
    pay_types = ["card", "boleto"] if MOEDA.get(lang, "brl") == "brl" else ["card"]
    locale = lang if lang in ["pt", "en", "es", "fr", "de", "it", "ja", "zh"] else "auto"
    try:
        if price_id and price_id.startswith("price_"):
            session = stripe.checkout.Session.create(
                mode="payment", payment_method_types=pay_types,
                line_items=[{"price": price_id, "quantity": 1}],
                customer_email=email or None,
                locale=locale, metadata=meta,
                success_url=f"{BASE_URL}/api/pay/success?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{BASE_URL}/api/pay/cancel")
        else:
            session = stripe.checkout.Session.create(
                mode="payment", payment_method_types=pay_types,
                line_items=[{"price_data": {"currency": MOEDA.get(lang, "brl"),
                    "product_data": {"name": nome_prod},
                    "unit_amount": preco_local(produto, lang)}, "quantity": 1}],
                customer_email=email or None,
                locale=locale, metadata=meta,
                success_url=f"{BASE_URL}/api/pay/success?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{BASE_URL}/api/pay/cancel")
        return {"id": session.id, "url": session.url}
    except Exception as e:
        logger.error(f"Stripe: {e}")
        raise HTTPException(500, "Erro ao criar pagamento")

# ===== CHECKOUT GENÉRICO (POST) =====
@app.post("/api/pay/stripe")
def pay_stripe(req: PayReq):
    if not STRIPE_KEY:
        raise HTTPException(503, "Stripe não configurado")
    produto = req.product or "express"
    lang = req.lang or "pt"
    return _criar_sessao(produto, lang, req.email, req.name, req.birth_date or "")

# ===== CHECKOUT GENÉRICO (GET - compatível com o index.html) =====
@app.get("/criar-checkout")
async def criar_checkout(lang: str = "pt", produto: str = "express"):
    res = _criar_sessao(produto, lang)
    return RedirectResponse(url=res["url"])

# ===== SUCESSO PÓS-PAGAMENTO =====
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
            pf = pdf17(data, nome, bd)
        elif prod == "urna":
            pf = pdf_produto("urna", nome, bd, lang)
        elif prod == "eleitoral":
            pf = pdf_produto("eleitoral", nome, bd, lang)
        elif prod == "express":
            pf = pdf8(data, nome, bd)
        else:
            pf = pdf_produto(prod, nome, bd, lang)
               html = pagina_sucesso(pf, nome, pn)
        if pf and os.path.exists(pf):
            os.remove(pf)
        return HTMLResponse(html)
    except Exception as e:
        logger.error(f"Success: {e}")
        return HTMLResponse("ERRO")

# ===== CHECKOUT NOME DE URNA =====
@app.post("/api/pay/urna-session")
def pay_urna_session(req: UrnaPayReq):
    if not STRIPE_KEY:
        raise HTTPException(503, "Stripe não configurado")
    if not req.email:
        raise HTTPException(400, "Email obrigatorio")
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
        em = meta.get("email", "") or getattr(s, "customer_email", "")
        nomes = [meta.get(f"nome{i}", "") for i in range(1, 6) if meta.get(f"nome{i}", "")]
        if not nomes:
            return HTMLResponse("ERRO")
        res, _, sugs = validar_nomes_urna(nomes, cr)
        cl = CARGO_INFO.get(cr, {}).get("label", cr)
        pf = pdf_urna(nc, cl, res, sugs)
               html = pagina_sucesso(pf, nc, "Validacao de Nome de Urna")
        if pf and os.path.exists(pf):
            os.remove(pf)
        return HTMLResponse(html)
    except Exception:
        return HTMLResponse("ERRO")

# ===== CHECKOUT NÚMERO ELEITORAL =====
@app.post("/api/pay/eleitoral-session")
def pay_eleitoral_session(req: EleitoralPayReq):
    if not STRIPE_KEY:
        raise HTTPException(503, "Stripe não configurado")
    if not req.email:
        raise HTTPException(400, "Email obrigatorio")
    if req.sigla < 10 or req.sigla > 99:
        raise HTTPException(400, "Sigla 2 digitos")
    if req.cargo not in ["vereador", "dep_estadual", "dep_federal", "senador"]:
        raise HTTPException(400, "Cargo invalido")
    meta = {"tipo": "eleitoral", "lang": req.lang or "pt", "sigla": str(req.sigla),
            "cargo": req.cargo, "email": req.email, "numero_existente": req.numero_existente or ""}
    return _criar_sessao("eleitoral", req.lang or "pt", req.email, "", "", meta)

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
        em = meta.get("email", "") or getattr(s, "customer_email", "")
        if not em:
            return HTMLResponse("ERRO")
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
        pf = pdf_eleitoral(ss, cl2, sugs, ni)
                html = pagina_sucesso(pf, f"Candidato {cl2}", "Numero Eleitoral")
        if pf and os.path.exists(pf):
            os.remove(pf)
        return HTMLResponse(html)
    except Exception:
        return HTMLResponse("ERRO")

@app.get("/api/pay/cancel")
def pay_cancel():
    return HTMLResponse("<h1>Cancelado</h1><a href='/'>Voltar</a>")

# ===== CÁLCULO GRÁTIS =====
@app.post("/calculate")
def calculate(req: PayReq):
    db = SessionLocal()
    try:
        if len(req.name.strip()) < 2:
            raise HTTPException(400, "Nome curto")
        if not req.birth_date:
            raise HTTPException(400, "Data obrigatoria")
        res = calc(req.name, req.birth_date)
        cid = uuid.uuid4().hex[:8]
        db.add(Calc(id=cid, name=req.name, birth_date=req.birth_date, email=req.email or "", **res))
        db.commit()
                        # Entrega imediata na tela — sem email, sem armazenamento (sigilo do cliente)
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
    sugs = gerar_numeros(req.sigla, req.cargo)
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
    return {"status": "ok", "stripe": bool(STRIPE_KEY), "sendgrid": bool(SENDGRID_KEY)}

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
            raise HTTPException(400, "Assinatura inválida")
    else:
        data = json.loads(payload)
        event = {"type": data.get("type", ""), "data": data.get("data", {})}
    if event["type"] == "checkout.session.completed":
        sess = event["data"]["object"]
        logger.info(f"Pagamento confirmado: {sess.get('id')}")
    return {"ok": True}

# ===== SISTEMA DE BÔNUS =====
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

@app.post("/ativar-bonus")
async def ativar_bonus(req: AtivarBonusReq):
    codigos = _carregar_codigos()
    info = codigos.get(req.codigo)
    if not info:
        return {"ok": False, "msg": "Código não encontrado"}
    if info.get("usado"):
        return {"ok": False, "msg": "Código já utilizado"}
    info["usado"] = True
    info["data_uso"] = datetime.now().isoformat()
    _salvar_codigos(codigos)
    target = PRODUTO_TARGET.get(info.get("produto"), "inicio")
    return {"ok": True, "target": target, "produto": info.get("produto")}

@app.post("/gerar-codigos-coletivo")
async def gerar_codigos_coletivo(req: Request):
    corpo = await req.json()
    itens = corpo.get("itens", [])
    codigos = _carregar_codigos()
    gerados = []
    for item in itens:
        for _ in range(item["qtd"]):
            cod = _gerar_codigo_bonus()
            codigos[cod] = {"produto": item["produto"], "usado": False}
            gerados.append({"codigo": cod, "produto": item["produto"]})
    _salvar_codigos(codigos)
    return {"ok": True, "total": len(gerados), "codigos": gerados}

# ===== CAIXA DE SUGESTÕES + BÔNUS =====
@app.post("/sugestao")
async def receber_sugestao(req: SugestaoReq):
    try:
        _enviar_email_simples(ADMIN_EMAIL, "Nova sugestão/reclamação — A1ELOS",
                              f"Sugestão de {req.nome} ({req.email}):\n\n{req.mensagem}")
        return {"ok": True}
    except Exception:
        return {"ok": False}

@app.post("/bonus")
async def solicitar_bonus(req: BonusReq):
    codigo = "BONUS-" + secrets.token_hex(3).upper()
    try:
        corpo = (f"Cliente: {req.nome}\nEmail: {req.email}\nProduto: {req.produto}\n"
                 f"Código gerado: {codigo}\nRelato:\n{req.mensagem}")
        _enviar_email_simples(ADMIN_EMAIL, "Pedido de BÔNUS — pane no pagamento", corpo)
        _enviar_email_simples(req.email, "A1ELOS — Seu código bônus",
                              f"Olá, {req.nome}!\nSeu código: {codigo}\n\nA1ELOS")
        return {"ok": True, "codigo": codigo}
    except Exception:
        return {"ok": False}

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

# ===== INICIALIZAÇÃO =====
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "10000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
