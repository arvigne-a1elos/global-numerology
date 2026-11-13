# -*- coding: utf-8 -*-
# main.py - A1ELOS Global Numerology API
# VERSÃO CONSOLIDADA CORRIGIDA - TODAS AS ROTAS DOS 23 PRODUTOS
import stripe
import tempfile
import os, json, uuid, logging, secrets, string, base64, traceback, time, io
from produtos.mapa import reduzir, calc_mapa, calc_grid, analisar_express, analisar_completo, analisar_vida
from produtos.calendario import analisar_calendario
# Blindagem: um import faltando não pode derrubar o site inteiro
try:
    from pdf_service import gerar_pdf_calendario
    from gerador_pdf import gerar_pdf
except ImportError:
    def gerar_pdf_calendario(*args, **kwargs):
        logger.error("gerar_pdf_calendario indisponivel em pdf_service; calendario nao gerado, site permanece no ar.")
        return None
from produtos.nome import analisar_nome
from produtos.urna import validar_nomes_urna
from produtos.eleitoral import gerar_numeros
from produtos.imovel import analisar_imovel
from produtos.casal import analisar_casal
from produtos.familia import analisar_familia
from produtos.equipe import analisar_equipe
from produtos.coletivo import desconto_bc
from produtos.ong import analisar_ong
import os, json, uuid, logging, secrets, string, base64, traceback
from datetime import date, datetime
from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile, File, Form
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
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from produtos.calendario import analisar_periodo
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse, Response
from referencia.precos import VALORES, SIMBOLO, PRECO_DISPLAY, PRODUTO_FAIXA, preco_local, preco_display
# ===== FONTES CJK (ja/zh) — restaura glifos kanji nos PDFs (07/11/2026) =====
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
try:
    pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))   # japonês
    pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))      # chinês
except Exception:
    pass
# ===== SEMANTICA (energias, vidas, formas e cores) - IMPORT OPCIONAL =====
# O main NUNCA quebra se o módulo ainda não existir: import protegido.
try:
    from referencia.semantica import (obter_texto_energia, obter_texto_vida,
                                      renderizar_forma_cor, obter_descricao_mestre)
    SEMANTICA_OK = True
except Exception:
    SEMANTICA_OK = False
# ===== MOEDAS POR IDIOMA (ISO 4217, para o Stripe) =====
MOEDA = {
    "pt": "brl", "en": "usd", "es": "eur", "it": "eur", "fr": "eur", "de": "eur",
    "ja": "jpy", "zh": "cny", "ru": "rub", "id": "idr", "tr": "try",
    "vi": "vnd", "he": "ils", "ar": "sar"
}

# ===== APP (OBRIGATÓRIO ANTES DE QUALQUER ROTA) =====
app = FastAPI(title="Global Numerology")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

STRIPE_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_PUB = os.getenv("STRIPE_PUBLISHABLE_KEY", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@a1elos.com.br")
FROM_NAME = "A1ELOS Numerologia Global"
BASE_URL = (os.getenv("BASE_URL") or os.getenv("SITE_URL") or "https://global-numerology.onrender.com").rstrip("/")
DB_URL = os.getenv("DATABASE_URL", "sqlite:///./numerologia.db")
ADMIN_EMAIL = "arvigne@gmail.com"

if STRIPE_KEY:
    stripe.api_key = STRIPE_KEY

# ===== CONFIG DE DESCONTO DO BÔNUS COLETIVO (espelho documental do app.js) =====
# ATENÇÃO: este dicionário é APENAS documentação de referência.
# O frontend (app.js) NÃO consulta estes valores, e o backend NÃO os usa
# para calcular desconto. A fonte de verdade em tempo de execução é o
# window.CONFIG_DESCONTO do app.js.
# Se alterar as faixas aqui, altere também no app.js — e vice-versa.
CONFIG_DESCONTO = {
    "faixas": [
        {"min": 10, "pct": 10}, {"min": 50, "pct": 15}, {"min": 100, "pct": 20},
        {"min": 200, "pct": 30}, {"min": 500, "pct": 40}, {"min": 1000, "pct": 45},
        {"min": 2000, "pct": 50},
    ],
    "teto_automatico": 2000,
    "pct_teto_negociacao": 70,
}

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

try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    logger.error(f"DB init adiado: {e}")

# ===== FONTES POR IDIOMA (14 idiomas) =====
# Toda a lógica de registro vive em fontes.py (híbrido TTF -> CID).
from fontes import registrar_tudo, fonte_para

try:
    registrar_tudo()
    logger.info("Fontes dos 14 idiomas registradas")
except Exception as e:
    logger.warning("Falha ao registrar fontes: %s", e)


def _fonte_do_idioma(lang):
    """Devolve (regular, bold) para o idioma, sempre registrado."""
    return fonte_para(lang)


FONTE_POR_IDIOMA = {
    # Latinos
    'pt': ('DejaVu', 'DejaVu-Bold'),
    'en': ('DejaVu', 'DejaVu-Bold'),
    'es': ('DejaVu', 'DejaVu-Bold'),
    'fr': ('DejaVu', 'DejaVu-Bold'),
    'de': ('DejaVu', 'DejaVu-Bold'),
    'it': ('DejaVu', 'DejaVu-Bold'),
    'id': ('DejaVu', 'DejaVu-Bold'),
    'ru': ('DejaVu', 'DejaVu-Bold'),
    'tr': ('DejaVu', 'DejaVu-Bold'),
    'vi': ('DejaVu', 'DejaVu-Bold'),
    # RTL
    'he': ('NotoSansHebrew', 'NotoSansHebrew-Bold'),
    'ar': ('NotoNaskhArabic', 'NotoNaskhArabic-Bold'),
    # CJK — TTF real
    'ja': ('HeiseiKakuGo-W5', 'HeiseiKakuGo-W5'),
    'zh': ('STSong-Light', 'STSong-Light'),
}

IDIOMAS_RTL = {'he', 'ar'}

# ===== NOMES DOS 24 PRODUTOS (14 IDIOMAS) =====
PRODUTOS = {
    "pt": {"express": "Mapa Express", "vida": "Qual Vida/Ano", "completo": "Mapa Completo",
        "ia": "Pesquisa IA de Nomes", "urna": "Validacao Nome de Urna", "eleitoral": "Numero Eleitoral",
        "imovel": "Numero do Imovel", "calendario": "Calendario Mensal Energetico",
        "artistico": "Validacao Nome Artistico", "bebe": "Planejamento Nome de Bebe",
        "assinatura": "Validacao de Assinaturas", "negocio": "Nome para Negocio/Produto",
        "casal": "Mapa do Casal", "familia": "Mapa Familia Premium", "coletivo": "Bonus Coletivo/Empresarial",
        "nome_pet": "Nome do Pet", "nickname": "Nickname Digital", "nome_dominio": "Nome do Dominio",
        "nome_canal": "Nome do Canal", "nome_equipe": "Nome da Equipe", 
        "nome_ong": "Nome de ONG, Associacao, Instituto ou Fundacao", "compatibilidade_equipes": "Compatibilidade de Equipes",
        "nome_projeto": "Nome do Projeto", "nome_evento": "Nome do Evento"},
    "en": {"express": "Express Map", "vida": "Life Phase & Year", "completo": "Complete Map",
        "ia": "AI Name Search", "urna": "Ballot Name Validation", "eleitoral": "Electoral Number",
        "imovel": "Property Number", "calendario": "Monthly Energy Calendar",
        "artistico": "Artistic Name Validation", "bebe": "Baby Name Planning",
        "assinatura": "Signature Validation", "negocio": "Business & Product Name",
        "casal": "Couple Map", "familia": "Premium Family Map", "coletivo": "Corporate Bonus",
        "nome_pet": "Pet Name", "nickname": "Digital Nickname", "nome_dominio": "Domain Name",
        "nome_canal": "Channel Name", "nome_equipe": "Team Name", "nome_projeto": "Project Name", "nome_evento": "Event Name",
        "nome_ong": "NGO, Association, Institute or Foundation Name", "compatibilidade_equipes": "Team Compatibility"},
    "es": {"express": "Mapa Exprés", "vida": "Ciclo de Vida y Año", "completo": "Mapa Completo",
        "ia": "Búsqueda IA de Nombres", "urna": "Validación Nombre de Urna", "eleitoral": "Número Electoral",
        "imovel": "Número de la Propiedad", "calendario": "Calendario Mensual Energético",
        "artistico": "Validación Nombre Artístico", "bebe": "Planificación Nombre de Bebé",
        "assinatura": "Validación de Firmas", "negocio": "Nombre para Negocio/Producto",
        "casal": "Mapa de Pareja", "familia": "Mapa Familiar Premium", "coletivo": "Bono Corporativo",
        "nome_pet": "Nombre de la Mascota", "nickname": "Apodo Digital", "nome_dominio": "Nombre de Dominio",
        "nome_canal": "Nombre del Canal", "nome_equipe": "Nombre del Equipo", 
        "nome_projeto": "Nombre del Proyecto", "nome_evento": "Nombre del Evento",
        "nome_ong": "Nombre de ONG, Asociacion, Instituto o Fundacion", "compatibilidade_equipes": "Compatibilidad de Equipos"}, 
    "it": {"express": "Mappa Espressa", "vida": "Fase di Vita e Anno", "completo": "Mappa Completa",
        "ia": "Ricerca IA Nomi", "urna": "Validazione Nome della Scheda", "eleitoral": "Numero Elettorale",
        "imovel": "Numero dell'Immobile", "calendario": "Calendario Mensile Energetico",
        "artistico": "Validazione Nome d'Arte", "bebe": "Pianificazione Nome del Bambino",
        "assinatura": "Validazione delle Firme", "negocio": "Nome per Business/Prodotto",
        "casal": "Mappa di Coppia", "familia": "Mappa Famiglia Premium", "coletivo": "Bonus Aziendale",
        "nome_pet": "Nome dell'Animale", "nickname": "Nickname Digitale", "nome_dominio": "Nome del Dominio",
        "nome_canal": "Nome del Canale", "nome_equipe": "Nome della Squadra", 
        "nome_projeto": "Nome del Progetto", "nome_evento": "Nome dell'Evento",
        "nome_ong": "Nome di ONG, Associazione, Istituto o Fondazione", "compatibilidade_equipes": "Compatibilità di Squadra"},
    "fr": {"express": "Carte Express", "vida": "Phase de Vie et Année", "completo": "Carte Complète",
        "ia": "Recherche IA de Noms", "urna": "Validation Nom du Bulletin", "eleitoral": "Numéro Électoral",
        "imovel": "Numéro du Bien", "calendario": "Calendrier Mensuel Énergétique",
        "artistico": "Validation Nom de Scène", "bebe": "Planification Prénom de Bébé",
        "assinatura": "Validation des Signatures", "negocio": "Nom pour Entreprise/Produit",
        "casal": "Carte du Couple", "familia": "Carte Famille Premium", "coletivo": "Bonus d'Entreprise",
        "nome_pet": "Nom de l'Animal", "nickname": "Pseudo Numerique", "nome_dominio": "Nom de Domaine",
        "nome_canal": "Nom de la Chaine", "nome_equipe": "Nom de l'Equipe", 
        "nome_projeto": "Nom du Projet", "nome_evento": "Nom de l'Evenement",
        "nome_ong": "Nom d'ONG, Association, Institut ou Fondation", "compatibilidade_equipes": "Compatibilité d'Équipe"},
    "de": {"express": "Express-Karte", "vida": "Lebensphase & Jahr", "completo": "Vollständige Karte",
        "ia": "KI-Namenssuche", "urna": "Stimmzettelname-Validierung", "eleitoral": "Wahlnummer",
        "imovel": "Immobiliennummer", "calendario": "Monatlicher Energiekalender",
        "artistico": "Künstlername-Validierung", "bebe": "Babynamen-Planung",
        "assinatura": "Unterschrifts-Validierung", "negocio": "Name für Unternehmen/Produkt",
        "casal": "Paar-Karte", "familia": "Premium-Familien-Karte", "coletivo": "Unternehmensbonus",
        "nome_pet": "Haustiername", "nickname": "Digitaler Spitzname", "nome_dominio": "Domainname",
        "nome_canal": "Kanalname", "nome_equipe": "Teamname", 
        "nome_projeto": "Projektname", "nome_evento": "Veranstaltungsname", 
        "nome_ong": "Name von NGO, Verein, Institut oder Stiftung", "compatibilidade_equipes": "Team-Kompatibilität"},
    "ja": {"express": "エクスプレスマップ", "vida": "ライフステージと年", "completo": "完全マップ",
        "ia": "AI名前検索", "urna": "投票用紙名の検証", "eleitoral": "選挙番号",
        "imovel": "不動産番号", "calendario": "月間エネルギーカレンダー",
        "artistico": "芸名の検証", "bebe": "赤ちゃんの名前計画",
        "assinatura": "署名の検証", "negocio": "ビジネス・商品名",
        "casal": "カップルマップ", "familia": "プレミアム家族マップ", "coletivo": "法人ボーナス",
        "nome_pet": "ペットの名前", "nickname": "デジタルニックネーム", "nome_dominio": "ドメイン名",
        "nome_canal": "チャンネル名", "nome_equipe": "チーム名", 
        "nome_projeto": "プロジェクト名", "nome_evento": "イベント名", 
        "nome_ong": "NGO・協会・研究所・財団の名前", "compatibilidade_equipes": "チーム相性診断"},
    "zh": {"express": "快速地图", "vida": "生命阶段与年份", "completo": "完整地图",
        "ia": "AI名字搜索", "urna": "选票名称验证", "eleitoral": "选举号码",
        "imovel": "房产号码", "calendario": "每月能量日历",
        "artistico": "艺名验证", "bebe": "宝宝取名规划",
        "assinatura": "签名验证", "negocio": "企业/产品名称",
        "casal": "情侣地图", "familia": "高级家庭地图", "coletivo": "企业奖励",
        "nome_pet": "宠物名字", "nickname": "数字昵称", "nome_dominio": "域名",
        "nome_canal": "频道名称", "nome_equipe": "团队名称", 
        "nome_projeto": "项目名称", "nome_evento": "活动名称", 
        "nome_ong": "非政府组织、协会、研究所或基金会名称", "compatibilidade_equipes": "团队兼容性"},
    "ru": {"express": "Экспресс-карта", "vida": "Жизненный этап и год", "completo": "Полная карта",
        "ia": "ИИ-поиск имён", "urna": "Проверка названия бюллетеня", "eleitoral": "Избирательный номер",
        "imovel": "Номер недвижимости", "calendario": "Ежемесячный энергетический календарь",
        "artistico": "Проверка сценического имени", "bebe": "Планирование имени ребёнка",
        "assinatura": "Проверка подписей", "negocio": "Название для бизнеса/продукта",
        "casal": "Карта пары", "familia": "Премиальная семейная карта", "coletivo": "Корпоративный бонус",
        "nome_pet": "Имя питомца", "nickname": "Цифровой никнейм", "nome_dominio": "Имя домена",
        "nome_canal": "Название канала", "nome_equipe": "Название команды", 
        "nome_projeto": "Название проекта", "nome_evento": "Название события", 
        "nome_ong": "Название НКО, ассоциации, института или фонда", "compatibilidade_equipes": "Совместимость команды"},
    "he": {"express": "מפה מהירה", "vida": "שלב חיים ושנה", "completo": "מפה מלאה",
        "ia": "חיפוש שמות AI", "urna": "אימות שם פתק", "eleitoral": "מספר בחירות",
        "imovel": "מספר נכס", "calendario": "לוח אנרגיה חודשי",
        "artistico": "אימות שם במה", "bebe": "תכנון שם לתינוק",
        "assinatura": "אימות חתימות", "negocio": "שם לעסק/מוצר",
        "nome_pet": "שם חיית המחמד", "nickname": "כינוי דיגיטלי", "nome_dominio": "שם דומיין",
        "nome_canal": "שם הערוץ", "nome_equipe": "שם הצוות", 
        "nome_projeto": "שם הפרויקט", "nome_evento": "שם האירוע",
        "casal": "מפת זוג", "familia": "מפת משפחה פרימיום", "coletivo": "בונוס ארגוני",
        "nome_ong": "שם עמותה, ארגון, מכון או קרן", "compatibilidade_equipes": "תאימות צוות"},
    "ar": {"express": "خريطة سريعة", "vida": "مرحلة الحياة والسنة", "completo": "خريطة كاملة",
        "ia": "بحث الأسماء بالذكاء الاصطناعي", "urna": "التحقق من اسم الاقتراع", "eleitoral": "الرقم الانتخابي",
        "imovel": "رقم العقار", "calendario": "التقويم الشهري للطاقة",
        "artistico": "التحقق من الاسم الفني", "bebe": "تخطيط اسم الطفل",
        "assinatura": "التحقق من التوقيعات", "negocio": "اسم للأعمال/المنتج",
        "casal": "خريطة الزوجين", "familia": "خريطة العائلة المميزة", "coletivo": "مكافأة الشركات",
        "nome_pet": "اسم الحيوان الأليف", "nickname": "اللقب الرقمي", "nome_dominio": "اسم النطاق",
        "nome_canal": "اسم القناة", "nome_equipe": "اسم الفريق", 
        "nome_projeto": "اسم المشروع", "nome_evento": "اسم الفعالية",
        "nome_ong": "اسم منظمة أو جمعية أو معهد أو مؤسسة", "compatibilidade_equipes": "توافق الفريق"},
    "id": {"express": "Peta Ekspres", "vida": "Fase Kehidupan & Tahun", "completo": "Peta Lengkap",
        "ia": "Pencarian Nama AI", "urna": "Validasi Nama Surat Suara", "eleitoral": "Nomor Elektoral",
        "imovel": "Nomor Properti", "calendario": "Kalender Energi Bulanan",
        "artistico": "Validasi Nama Artistik", "bebe": "Perencanaan Nama Bayi",
        "assinatura": "Validasi Tanda Tangan", "negocio": "Nama untuk Bisnis/Produk",
        "casal": "Peta Pasangan", "familia": "Peta Keluarga Premium", "coletivo": "Bonus Kolektif/Perusahaan",
        "nome_pet": "Nama Hewan Peliharaan", "nickname": "Nama Panggilan Digital", "nome_dominio": "Nama Domain",
        "nome_canal": "Nama Kanal", "nome_equipe": "Nama Tim", 
        "nome_projeto": "Nama Proyek", "nome_evento": "Nama Acara",
        "nome_ong": "Nama LSM, Asosiasi, Lembaga atau Yayasan", "compatibilidade_equipes": "Kompatibilitas Tim"},     
    "tr": {"express": "Ekspres Harita", "vida": "Yaşam Evresi ve Yıl", "completo": "Tam Harita",
        "ia": "AI İsim Arama", "urna": "Oy Pusulası İsim Doğrulama", "eleitoral": "Seçim Numarası",
        "imovel": "Mülk Numarası", "calendario": "Aylık Enerji Takvimi",
        "artistico": "Sahne Adı Doğrulama", "bebe": "Bebek İsmi Planlama",
        "assinatura": "İmza Doğrulama", "negocio": "İşletme/Ürün Adı",
        "casal": "Çift Haritası", "familia": "Premium Aile Haritası", "coletivo": "Kurumsal Bonus",
        "nome_pet": "Evcil Hayvan Adı", "nickname": "Dijital Takma Ad", "nome_dominio": "Alan Adı",
        "nome_canal": "Kanal Adı", "nome_equipe": "Ekip Adı", 
        "nome_projeto": "Proje Adı", "nome_evento": "Etkinlik Adı",
        "nome_ong": "STK, Dernek, Enstitü veya Vakıf Adı", "compatibilidade_equipes": "Ekip Uyumu"},     
    "vi": {"express": "Bản Đồ Nhanh", "vida": "Giai Đoạn Cuộc Đời & Năm", "completo": "Bản Đồ Đầy Đủ",
        "ia": "Tìm Kiếm Tên AI", "urna": "Xác Minh Tên Phiếu Bầu", "eleitoral": "Số Bầu Cử",
        "imovel": "Số Bất Động Sản", "calendario": "Lịch Năng Lượng Hàng Tháng",
        "artistico": "Xác Minh Nghệ Danh", "bebe": "Lên Kế Hoạch Tên Cho Bé",
        "assinatura": "Xác Minh Chữ Ký", "negocio": "Tên Cho Doanh Nghiệp/Sản Phẩm",
        "casal": "Bản Đồ Cặp Đôi", "familia": "Bản Đồ Gia Đình Cao Cấp", "coletivo": "Thưởng Tập Thể/Doanh Nghiệp",
        "nome_pet": "Tên Thú Cưng", "nickname": "Biệt Danh Kỹ Thuật Số", "nome_dominio": "Tên Miền",
        "nome_canal": "Tên Kênh", "nome_equipe": "Tên Đội Nhóm", 
        "nome_projeto": "Tên Dự Án", "nome_evento": "Tên Sự Kiện",
        "nome_ong": "Tên Tổ Chức, Hiệp Hội, Viện hoặc Quỹ", "compatibilidade_equipes": "Tương hợp đội nhóm"}     
    }

# ===== PRICE IDS STRIPE (24 produtos, 14 idiomas) =====
PRICE_IDS = {
    "pt": {"express": "price_1UYwFBBMLa84bVJ0hg3okec9", "completo": "price_1UYwFHBMLa84bVJ0lSkkfPio", "urna": "price_1UYwFIBMLa84bVJ03wsbVVic", "eleitoral": "price_1UYwFJBMLa84bVJ0BkuErjgP", "vida": "price_1UYwFBBMLa84bVJ0vg0EjgNN", "ia": "price_1UYwFCBMLa84bVJ0P0nZ4pFB", "nickname": "price_1UYwFDBMLa84bVJ0QJi6PCgw", "nome_pet": "price_1UYwFDBMLa84bVJ0sOD7h3T9", "nome_dominio": "price_1UYwFEBMLa84bVJ0j2LlhqbU", "nome_canal": "price_1UYwFEBMLa84bVJ0bF6qXCKu", "nome_equipe": "price_1UYwFFBMLa84bVJ0Shpkyw96", "nome_projeto": "price_1UYwFGBMLa84bVJ0XdBqUTrp", "nome_evento": "price_1UYwFGBMLa84bVJ0QfuJBUl0", "calendario": "price_1UYwFIBMLa84bVJ0crXpzaiH", "imovel": "price_1UYwFJBMLa84bVJ0AA2X3uUE", "nome_ong": "price_1UYwFKBMLa84bVJ08siEYga5", "artistico": "price_1UYwFLBMLa84bVJ0J4L8W9Zu", "bebe": "price_1UYwFLBMLa84bVJ0vqTuXTTk", "assinatura": "price_1UYwFMBMLa84bVJ0ZZ3Cb47M", "negocio": "price_1UYwFNBMLa84bVJ01Gq3Mh9v", "casal": "price_1UYwFNBMLa84bVJ0aDUxjZpS", "familia": "price_1UYwFOBMLa84bVJ0w7bMvX9g", "compatibilidade_equipes": "price_1UYwFOBMLa84bVJ0m2TQVP84", "diagnostico": "price_1UYwFPBMLa84bVJ04gkCuwW2"},
    "en": {"express": "price_1UYwFQBMLa84bVJ0ElmWZtFp", "completo": "price_1UYwFWBMLa84bVJ0sHap7k9h", "urna": "price_1UYwFXBMLa84bVJ0LgxBia4M", "eleitoral": "price_1UYwFYBMLa84bVJ0i4dSEQRI", "vida": "price_1UYwFQBMLa84bVJ0EgzrtEvh", "ia": "price_1UYwFRBMLa84bVJ0k03CfWUv", "nickname": "price_1UYwFSBMLa84bVJ0GFmZof6y", "nome_pet": "price_1UYwFRBMLa84bVJ00ikeCVAL", "nome_dominio": "price_1UYwFTBMLa84bVJ0SsXYWPTO", "nome_canal": "price_1UYwFTBMLa84bVJ050NKCp9j", "nome_equipe": "price_1UYwFUBMLa84bVJ0HzNgfHUN", "nome_projeto": "price_1UYwFVBMLa84bVJ0JXHdYqve", "nome_evento": "price_1UYwFVBMLa84bVJ0G5SWEBoj", "calendario": "price_1UYwFWBMLa84bVJ0d49s3xAe", "imovel": "price_1UYwFYBMLa84bVJ0x7cwvVvI", "nome_ong": "price_1UYwFZBMLa84bVJ0Y1Cmlk66", "artistico": "price_1UYwFaBMLa84bVJ05Y04uPvx", "bebe": "price_1UYwFaBMLa84bVJ0Px7HCIyg", "assinatura": "price_1UYwFbBMLa84bVJ01qVR2kS8", "negocio": "price_1UYwFbBMLa84bVJ0F7Iuj2f0", "casal": "price_1UYwFcBMLa84bVJ0k6EFFO6I", "familia": "price_1UYwFdBMLa84bVJ0kbd5FArN", "compatibilidade_equipes": "price_1UYwFdBMLa84bVJ0cSpic9cg", "diagnostico": "price_1UYwFeBMLa84bVJ02rsyEXPW"},
    "es": {"express": "price_1UYwFfBMLa84bVJ0S368q7UP", "completo": "price_1UYwFlBMLa84bVJ0dsBt8hQN", "urna": "price_1UYwFmBMLa84bVJ0Xt4zYTva", "eleitoral": "price_1UYwFnBMLa84bVJ0t49K4AX5", "vida": "price_1UYwFfBMLa84bVJ0ZzRQs7fW", "ia": "price_1UYwFgBMLa84bVJ0eyXoeXYv", "nickname": "price_1UYwFhBMLa84bVJ0VSWbqGcy", "nome_pet": "price_1UYwFgBMLa84bVJ0W4xAr920", "nome_dominio": "price_1UYwFiBMLa84bVJ0ED6NlX3v", "nome_canal": "price_1UYwFiBMLa84bVJ0AWoey3Jn", "nome_equipe": "price_1UYwFjBMLa84bVJ0sWIhZ0i7", "nome_projeto": "price_1UYwFjBMLa84bVJ0boLMWThq", "nome_evento": "price_1UYwFkBMLa84bVJ00T8n865t", "calendario": "price_1UYwFlBMLa84bVJ0RAblvXLJ", "imovel": "price_1UYwFnBMLa84bVJ0naX8CGZ3", "nome_ong": "price_1UYwFoBMLa84bVJ0ibOe2Brw", "artistico": "price_1UYwFoBMLa84bVJ0ub7ynYgI", "bebe": "price_1UYwFpBMLa84bVJ0S1RrBYwe", "assinatura": "price_1UYwFqBMLa84bVJ01zGvk4rS", "negocio": "price_1UYwFqBMLa84bVJ04mPULJPb", "casal": "price_1UYwFrBMLa84bVJ0xE7HCvHu", "familia": "price_1UYwFrBMLa84bVJ0uOTNwdkr", "compatibilidade_equipes": "price_1UYwFsBMLa84bVJ0tRoik8zt", "diagnostico": "price_1UYwFtBMLa84bVJ0yLZJLvfB"},
    "it": {"express": "price_1UYwFtBMLa84bVJ0e2KlyrcA", "completo": "price_1UYwFzBMLa84bVJ084oN3ZRb", "urna": "price_1UYwG1BMLa84bVJ033G9V6wv", "eleitoral": "price_1UYwG1BMLa84bVJ0zTfFBRpD", "vida": "price_1UYwFuBMLa84bVJ0sUomLltJ", "ia": "price_1UYwFvBMLa84bVJ0dVZBHnNb", "nickname": "price_1UYwFwBMLa84bVJ0WvSvepg8", "nome_pet": "price_1UYwFvBMLa84bVJ0bhWFDk06", "nome_dominio": "price_1UYwFwBMLa84bVJ0Okow94iT", "nome_canal": "price_1UYwFxBMLa84bVJ0JNUPQotC", "nome_equipe": "price_1UYwFyBMLa84bVJ0VCuOaZiw", "nome_projeto": "price_1UYwFyBMLa84bVJ0BDLTjJyx", "nome_evento": "price_1UYwFzBMLa84bVJ0T9pZnqOO", "calendario": "price_1UYwG0BMLa84bVJ0uo6zlfu8", "imovel": "price_1UYwG2BMLa84bVJ0BoXFuM9c", "nome_ong": "price_1UYwG3BMLa84bVJ0hzyZxRe3", "artistico": "price_1UYwG3BMLa84bVJ0EoDx2XGD", "bebe": "price_1UYwG4BMLa84bVJ0Ccx2SgS8", "assinatura": "price_1UYwG4BMLa84bVJ0aFJd8mVB", "negocio": "price_1UYwG5BMLa84bVJ00DCfZQCz", "casal": "price_1UYwG6BMLa84bVJ0kuvzLo4V", "familia": "price_1UYwG6BMLa84bVJ0ztC88RrC", "compatibilidade_equipes": "price_1UYwG7BMLa84bVJ0IROUJbNC", "diagnostico": "price_1UYwG7BMLa84bVJ0v4PJjc67"},
    "fr": {"express": "price_1UYwG8BMLa84bVJ0DRVG80av", "completo": "price_1UYwGEBMLa84bVJ0GgDsoQXi", "urna": "price_1UYwGGBMLa84bVJ0kiowysei", "eleitoral": "price_1UYwGGBMLa84bVJ0A1r1PuHQ", "vida": "price_1UYwG9BMLa84bVJ04vK50Of8", "ia": "price_1UYwG9BMLa84bVJ0aHjlrZto", "nickname": "price_1UYwGBBMLa84bVJ0tYPmxMHa", "nome_pet": "price_1UYwGABMLa84bVJ0MPmLYS9V", "nome_dominio": "price_1UYwGBBMLa84bVJ02Qchs3sO", "nome_canal": "price_1UYwGCBMLa84bVJ08AMNcmCK", "nome_equipe": "price_1UYwGCBMLa84bVJ0EocNrr4Q", "nome_projeto": "price_1UYwGDBMLa84bVJ0WnXU7MyL", "nome_evento": "price_1UYwGEBMLa84bVJ0RbMnh21L", "calendario": "price_1UYwGFBMLa84bVJ0NWESJfzT", "imovel": "price_1UYwGHBMLa84bVJ0v9kJU83m", "nome_ong": "price_1UYwGHBMLa84bVJ0MKQkvt3c", "artistico": "price_1UYwGIBMLa84bVJ04b43DPwp", "bebe": "price_1UYwGJBMLa84bVJ0BfiONjIA", "assinatura": "price_1UYwGJBMLa84bVJ0mhxdHBDO", "negocio": "price_1UYwGKBMLa84bVJ0jkOxIYDG", "casal": "price_1UYwGKBMLa84bVJ0MOZ4PqMt", "familia": "price_1UYwGLBMLa84bVJ0v4VpeguF", "compatibilidade_equipes": "price_1UYwGMBMLa84bVJ0rCVNHTLU", "diagnostico": "price_1UYwGMBMLa84bVJ03tRrm62G"},
    "de": {"express": "price_1UYwGNBMLa84bVJ0N52dkcBP", "completo": "price_1UYwGTBMLa84bVJ0cimEZxGC", "urna": "price_1UYwGUBMLa84bVJ0JBhynUUR", "eleitoral": "price_1UYwGVBMLa84bVJ0xY8AVMRY", "vida": "price_1UYwGOBMLa84bVJ0d9B03lfM", "ia": "price_1UYwGOBMLa84bVJ09CANYrGU", "nickname": "price_1UYwGPBMLa84bVJ0KMo58LXK", "nome_pet": "price_1UYwGPBMLa84bVJ0tLrkTr8Y", "nome_dominio": "price_1UYwGQBMLa84bVJ0vGFIo7SO", "nome_canal": "price_1UYwGRBMLa84bVJ0vjWBagex", "nome_equipe": "price_1UYwGRBMLa84bVJ06she7vNQ", "nome_projeto": "price_1UYwGSBMLa84bVJ00ApdYrYQ", "nome_evento": "price_1UYwGTBMLa84bVJ0J6yZ69of", "calendario": "price_1UYwGUBMLa84bVJ0wYFTQPli", "imovel": "price_1UYwGWBMLa84bVJ0ZdtGxGY6", "nome_ong": "price_1UYwGWBMLa84bVJ0IAyz08bc", "artistico": "price_1UYwGXBMLa84bVJ0CKlTnt0z", "bebe": "price_1UYwGXBMLa84bVJ0w3FJOGOv", "assinatura": "price_1UYwGYBMLa84bVJ0UT6lWdOP", "negocio": "price_1UYwGZBMLa84bVJ0sOwJWeER", "casal": "price_1UYwGZBMLa84bVJ0K9ueqc7t", "familia": "price_1UYwGaBMLa84bVJ0FBREDjgl", "compatibilidade_equipes": "price_1UYwGaBMLa84bVJ0AEPvGg5a", "diagnostico": "price_1UYwGbBMLa84bVJ058Ky3sOm"},
    "ja": {"express": "price_1UYwGcBMLa84bVJ0WZ1jGG14", "completo": "price_1UYwGiBMLa84bVJ0WqSkQ6BE", "urna": "price_1UYwGjBMLa84bVJ0XuHC5pkO", "eleitoral": "price_1UYwGkBMLa84bVJ0ZA6aOpKj", "vida": "price_1UYwGcBMLa84bVJ00EVFYvcG", "ia": "price_1UYwGdBMLa84bVJ0CPtRln1a", "nickname": "price_1UYwGeBMLa84bVJ0zAYRgowU", "nome_pet": "price_1UYwGdBMLa84bVJ0Fz2J0u9B", "nome_dominio": "price_1UYwGfBMLa84bVJ0wJBoaVYx", "nome_canal": "price_1UYwGfBMLa84bVJ0tGN2AsfH", "nome_equipe": "price_1UYwGgBMLa84bVJ0PM64zRy3", "nome_projeto": "price_1UYwGhBMLa84bVJ0MypR5Rje", "nome_evento": "price_1UYwGhBMLa84bVJ0RBjEwQBf", "calendario": "price_1UYwGiBMLa84bVJ0qLU5BHw1", "imovel": "price_1UYwGkBMLa84bVJ0M4qoBzuI", "nome_ong": "price_1UYwGlBMLa84bVJ0xukwPYXt", "artistico": "price_1UYwGmBMLa84bVJ0eE2hREsp", "bebe": "price_1UYwGmBMLa84bVJ0QgqvLdvM", "assinatura": "price_1UYwGnBMLa84bVJ0hEsnsBEC", "negocio": "price_1UYwGnBMLa84bVJ0O67aFpIK", "casal": "price_1UYwGoBMLa84bVJ0GvXVru7U", "familia": "price_1UYwGpBMLa84bVJ0fzsmXdLR", "compatibilidade_equipes": "price_1UYwGpBMLa84bVJ0VRl37f0b", "diagnostico": "price_1UYwGqBMLa84bVJ08TpwcaXs"},
    "zh": {"express": "price_1UYwGrBMLa84bVJ0R05vzcma", "completo": "price_1UYwGxBMLa84bVJ0vMUIJbFe", "urna": "price_1UYwGyBMLa84bVJ0b4ZGQOBG", "eleitoral": "price_1UYwGzBMLa84bVJ0vSGPS2VI", "vida": "price_1UYwGrBMLa84bVJ0j0hpmyte", "ia": "price_1UYwGsBMLa84bVJ0q4J0zABW", "nickname": "price_1UYwGtBMLa84bVJ0f0ApBcxl", "nome_pet": "price_1UYwGsBMLa84bVJ0DaEV9bWG", "nome_dominio": "price_1UYwGuBMLa84bVJ0C17voyFI", "nome_canal": "price_1UYwGuBMLa84bVJ0M6dSUETW", "nome_equipe": "price_1UYwGvBMLa84bVJ0rQPNL3yn", "nome_projeto": "price_1UYwGvBMLa84bVJ0ROgizQIm", "nome_evento": "price_1UYwGwBMLa84bVJ0SoPtUAjA", "calendario": "price_1UYwGxBMLa84bVJ0Lj3HQnL3", "imovel": "price_1UYwGzBMLa84bVJ08RLrffUl", "nome_ong": "price_1UYwH0BMLa84bVJ0gPjF4dAm", "artistico": "price_1UYwH0BMLa84bVJ0pYNKBTVH", "bebe": "price_1UYwH1BMLa84bVJ0rGKCWKqe", "assinatura": "price_1UYwH2BMLa84bVJ0Z55fDEMR", "negocio": "price_1UYwH2BMLa84bVJ0au85SICS", "casal": "price_1UYwH3BMLa84bVJ0xaWXZUcZ", "familia": "price_1UYwH4BMLa84bVJ0l3bVj1vC", "compatibilidade_equipes": "price_1UYwH4BMLa84bVJ0qhxC2cza", "diagnostico": "price_1UYwH5BMLa84bVJ0SNTi6GX4"},
    "ru": {"express": "price_1UYwH5BMLa84bVJ072br6l0h", "completo": "price_1UYwHCBMLa84bVJ0RT2bKMwN", "urna": "price_1UYwHDBMLa84bVJ0TIefEAUc", "eleitoral": "price_1UYwHDBMLa84bVJ0GI1ASXW4", "vida": "price_1UYwH6BMLa84bVJ0r5w3f5Kj", "ia": "price_1UYwH7BMLa84bVJ0pcvblCMW", "nickname": "price_1UYwH8BMLa84bVJ0r8h25B9j", "nome_pet": "price_1UYwH7BMLa84bVJ0khC7G53j", "nome_dominio": "price_1UYwH9BMLa84bVJ09qytIhUE", "nome_canal": "price_1UYwH9BMLa84bVJ0OwRW9uUT", "nome_equipe": "price_1UYwHABMLa84bVJ0VfbGlzyu", "nome_projeto": "price_1UYwHABMLa84bVJ0gAKnlCql", "nome_evento": "price_1UYwHBBMLa84bVJ0ywf0MiOc", "calendario": "price_1UYwHCBMLa84bVJ0OfgSaJdN", "imovel": "price_1UYwHEBMLa84bVJ0mHv3ZHJe", "nome_ong": "price_1UYwHFBMLa84bVJ0RfAIlPi9", "artistico": "price_1UYwHFBMLa84bVJ0ZyUF3taw", "bebe": "price_1UYwHGBMLa84bVJ0QWZji7Ov", "assinatura": "price_1UYwHHBMLa84bVJ0iqDJFAkM", "negocio": "price_1UYwHHBMLa84bVJ0EeqqyOiq", "casal": "price_1UYwHIBMLa84bVJ0VQDNqtrt", "familia": "price_1UYwHIBMLa84bVJ0P2vn3FWN", "compatibilidade_equipes": "price_1UYwHJBMLa84bVJ0skfp6n4V", "diagnostico": "price_1UYwHKBMLa84bVJ04PZLt6Nh"},
    "id": {"express": "price_1UYwHKBMLa84bVJ0pHgAdfcG", "completo": "price_1UYwHRBMLa84bVJ0nn22eNXO", "urna": "price_1UYwHSBMLa84bVJ0Uj07Jkt2", "eleitoral": "price_1UYwHSBMLa84bVJ0LHGRkDjo", "vida": "price_1UYwHLBMLa84bVJ0eTEcqcEH", "ia": "price_1UYwHMBMLa84bVJ0SInL1tVM", "nickname": "price_1UYwHNBMLa84bVJ02ZC9OY9s", "nome_pet": "price_1UYwHMBMLa84bVJ0WN9w2KnC", "nome_dominio": "price_1UYwHNBMLa84bVJ0nSe26RSR", "nome_canal": "price_1UYwHOBMLa84bVJ0Yri0wcLZ", "nome_equipe": "price_1UYwHPBMLa84bVJ0i0RO82IL", "nome_projeto": "price_1UYwHPBMLa84bVJ0WGPABzlY", "nome_evento": "price_1UYwHQBMLa84bVJ0EBpEOqNP", "calendario": "price_1UYwHRBMLa84bVJ0XnsjcPpp", "imovel": "price_1UYwHTBMLa84bVJ014648wGB", "nome_ong": "price_1UYwHUBMLa84bVJ0JvLqUXeE", "artistico": "price_1UYwHUBMLa84bVJ0pMRjWDB5", "bebe": "price_1UYwHVBMLa84bVJ0Ge87QJu3", "assinatura": "price_1UYwHVBMLa84bVJ0yqfRxBgz", "negocio": "price_1UYwHWBMLa84bVJ0RzFYTHvQ", "casal": "price_1UYwHXBMLa84bVJ0ZvprQgKi", "familia": "price_1UYwHXBMLa84bVJ0U6GGC4ur", "compatibilidade_equipes": "price_1UYwHYBMLa84bVJ0PqxX2eqO", "diagnostico": "price_1UYwHZBMLa84bVJ0x9SYwKMy"},
    "tr": {"express": "price_1UYwHZBMLa84bVJ0WcXZd7ET", "completo": "price_1UYwHfBMLa84bVJ0AwQGQajP", "urna": "price_1UYwHgBMLa84bVJ01sfM4UxB", "eleitoral": "price_1UYwHhBMLa84bVJ0QrSNhUNS", "vida": "price_1UYwHaBMLa84bVJ06RuGBz97", "ia": "price_1UYwHaBMLa84bVJ0EyLd7LRS", "nickname": "price_1UYwHcBMLa84bVJ03U0nZ3kS", "nome_pet": "price_1UYwHbBMLa84bVJ060C8v5B4", "nome_dominio": "price_1UYwHcBMLa84bVJ0iuA9bDEk", "nome_canal": "price_1UYwHdBMLa84bVJ0KidBIqwu", "nome_equipe": "price_1UYwHdBMLa84bVJ0iPVdhLu7", "nome_projeto": "price_1UYwHeBMLa84bVJ0NmfCemQI", "nome_evento": "price_1UYwHfBMLa84bVJ0BxnqsZnD", "calendario": "price_1UYwHgBMLa84bVJ0qym9NvMw", "imovel": "price_1UYwHiBMLa84bVJ0EoYG7FZ4", "nome_ong": "price_1UYwHiBMLa84bVJ0j4ncuwQJ", "artistico": "price_1UYwHjBMLa84bVJ01ghdQ2PY", "bebe": "price_1UYwHkBMLa84bVJ0c4YallVa", "assinatura": "price_1UYwHkBMLa84bVJ0th50hlx0", "negocio": "price_1UYwHlBMLa84bVJ0Sz1lLD19", "casal": "price_1UYwHlBMLa84bVJ00PbJRQOJ", "familia": "price_1UYwHmBMLa84bVJ0iZGkR6HR", "compatibilidade_equipes": "price_1UYwHnBMLa84bVJ0zlKHRdUt", "diagnostico": "price_1UYwHnBMLa84bVJ0Nt9E7t26"},
    "vi": {"express": "price_1UYwHoBMLa84bVJ0npLcHGq1", "completo": "price_1UYwHuBMLa84bVJ0leID7aax", "urna": "price_1UYwHvBMLa84bVJ0qdAw4RF6", "eleitoral": "price_1UYwHwBMLa84bVJ01Aj8AHRz", "vida": "price_1UYwHpBMLa84bVJ0reE1QsLR", "ia": "price_1UYwHpBMLa84bVJ0f3x91RnF", "nickname": "price_1UYwHqBMLa84bVJ0GvxyV3tu", "nome_pet": "price_1UYwHqBMLa84bVJ0nDlfdeGI", "nome_dominio": "price_1UYwHrBMLa84bVJ0qNo9xk6z", "nome_canal": "price_1UYwHsBMLa84bVJ0FdeEUPyJ", "nome_equipe": "price_1UYwHsBMLa84bVJ0huu4Asqq", "nome_projeto": "price_1UYwHtBMLa84bVJ0qotuhYsu", "nome_evento": "price_1UYwHuBMLa84bVJ0V5wDr2be", "calendario": "price_1UYwHvBMLa84bVJ0TfUhOdHq", "imovel": "price_1UYwHxBMLa84bVJ0zhGAQwJv", "nome_ong": "price_1UYwHxBMLa84bVJ0aUg9UEeh", "artistico": "price_1UYwHyBMLa84bVJ0KzgwNIs2", "bebe": "price_1UYwHyBMLa84bVJ0rsyn93Yk", "assinatura": "price_1UYwHzBMLa84bVJ0p9awi1hn", "negocio": "price_1UYwI0BMLa84bVJ0FdryGWPo", "casal": "price_1UYwI0BMLa84bVJ0p7mq8KNY", "familia": "price_1UYwI1BMLa84bVJ0QnjNKgRA", "compatibilidade_equipes": "price_1UYwI2BMLa84bVJ0LJIdGIGW", "diagnostico": "price_1UYwI2BMLa84bVJ0mnqXR9dZ"},
    "he": {"express": "price_1UYwI3BMLa84bVJ04SI6pjZK", "completo": "price_1UYwI9BMLa84bVJ0oY5ot9Pf", "urna": "price_1UYwIABMLa84bVJ036DUZZOf", "eleitoral": "price_1UYwIBBMLa84bVJ0DYbWnc2p", "vida": "price_1UYwI3BMLa84bVJ0OGHzhk4n", "ia": "price_1UYwI4BMLa84bVJ0AEeSzAOk", "nickname": "price_1UYwI5BMLa84bVJ0ENu2snMU", "nome_pet": "price_1UYwI5BMLa84bVJ0pD9W5lcE", "nome_dominio": "price_1UYwI6BMLa84bVJ0iiY11mkx", "nome_canal": "price_1UYwI6BMLa84bVJ0a64NGBTm", "nome_equipe": "price_1UYwI7BMLa84bVJ0tXTWUgF8", "nome_projeto": "price_1UYwI8BMLa84bVJ0qXVi4KkZ", "nome_evento": "price_1UYwI8BMLa84bVJ04SGolXod", "calendario": "price_1UYwIABMLa84bVJ0HaUeY0jg", "imovel": "price_1UYwIBBMLa84bVJ0ZgXFoy7v", "nome_ong": "price_1UYwICBMLa84bVJ0oPkQtv6t", "artistico": "price_1UYwIDBMLa84bVJ0ASC6ZDri", "bebe": "price_1UYwIDBMLa84bVJ0YGW7hms2", "assinatura": "price_1UYwIEBMLa84bVJ0gCcRIiRQ", "negocio": "price_1UYwIEBMLa84bVJ0ynjXQcjM", "casal": "price_1UYwIFBMLa84bVJ0IOrOvMAm", "familia": "price_1UYwIGBMLa84bVJ0AjueoLns", "compatibilidade_equipes": "price_1UYwIGBMLa84bVJ01ESdgjK0", "diagnostico": "price_1UYwIHBMLa84bVJ05qsOy3yv"},
    "ar": {"express": "price_1UYwIHBMLa84bVJ0s1IROyIK", "completo": "price_1UYwIOBMLa84bVJ0ExVkvgRN", "urna": "price_1UYwIPBMLa84bVJ0LwK8CaqV", "eleitoral": "price_1UYwIPBMLa84bVJ05p1aeZU9", "vida": "price_1UYwIIBMLa84bVJ0aX3Sm58b", "ia": "price_1UYwIJBMLa84bVJ0yZHFvpvy", "nickname": "price_1UYwIKBMLa84bVJ0kQR1FnD0", "nome_pet": "price_1UYwIJBMLa84bVJ0HlABJN3G", "nome_dominio": "price_1UYwILBMLa84bVJ0tERMKjkF", "nome_canal": "price_1UYwILBMLa84bVJ0VNAH3i6c", "nome_equipe": "price_1UYwIMBMLa84bVJ0UwnO4HIC", "nome_projeto": "price_1UYwIMBMLa84bVJ0AQNSKMEk", "nome_evento": "price_1UYwINBMLa84bVJ0SyLprIFE", "calendario": "price_1UYwIOBMLa84bVJ0hyFhpi0T", "imovel": "price_1UYwIQBMLa84bVJ0TReNgnVm", "nome_ong": "price_1UYwIRBMLa84bVJ0K7wTz53V", "artistico": "price_1UYwIRBMLa84bVJ0zSgJfBMB", "bebe": "price_1UYwISBMLa84bVJ0NdIfymIX", "assinatura": "price_1UYwITBMLa84bVJ0BB7DfuRW", "negocio": "price_1UYwITBMLa84bVJ06geUajEw", "casal": "price_1UYwIUBMLa84bVJ0EGcKDiGU", "familia": "price_1UYwIUBMLa84bVJ0xkShjFnp", "compatibilidade_equipes": "price_1UYwIVBMLa84bVJ0TRRVLqkq", "diagnostico": "price_1UYwIWBMLa84bVJ021j2XSgY"},
}

PRODUTO_TARGET = {
    "express": "calculadora", "vida": "produtos", "completo": "calculadora",
    "ia": "produtos", "urna": "form-urna", "eleitoral": "form-eleitoral",
    "imovel": "produtos", "calendario": "produtos", "artistico": "produtos",
    "bebe": "produtos", "assinatura": "produtos", "negocio": "produtos",
    "casal": "produtos", "familia": "produtos", "coletivo": "corporativo",
    "compatibilidade_equipes": "produtos",   # ← NOVO 24º produto (mesmo padrão de casal/família)
    "nome_pet": "calculadora", "nickname": "calculadora", "nome_dominio": "calculadora",
    "nome_canal": "calculadora", "nome_equipe": "calculadora", "nome_ong": "calculadora",
    "nome_projeto": "calculadora", "nome_evento": "calculadora"
}

# ===== ALIAS PARA COMPATIBILIDADE (checkout coletivo) =====
PRODUCT_NAMES = PRODUTOS

# ===== MODELOS PYDANTIC =====
class PayReq(BaseModel):
    nome: str
    nascimento: str
    email: Optional[str] = ""
    lang: str = "pt"

class UrnaPayReq(BaseModel):
    nome_completo: str
    nome_urna: str = ""
    email: Optional[str] = ""
    lang: str = "pt"
    cargo: str = "vereador"
    genero: str = "masculino"
    energia: str = ""
    nome1: str = ""
    nome2: str = ""
    nome3: str = ""
    nome4: str = ""
    nome5: str = ""

class EleitoralPayReq(BaseModel):
    nome_completo: str
    numero: str
    email: Optional[str] = ""
    lang: str = "pt"
    cargo: str = "vereador"

class SugestaoReq(BaseModel):
    nome: str
    email: Optional[str] = ""
    mensagem: str

class BonusReq(BaseModel):
    nome: str
    email: Optional[str] = ""
    motivo: str

class NegociacaoReq(BaseModel):
    nome: str
    empresa: str = ""
    email: str
    quantidade: str = ""
    mensagem: str = ""

class AtivarBonusReq(BaseModel):
    codigo: str

class BannerContrato(BaseModel):
    id: str
    marca: str
    url_anunciante: str
    imagem_url: str
    escopo: str  # "pais", "continente" ou "mundo"
    pais: str = ""
    continente: str = ""
    posicao: str = "topo"  # topo, lateral, central
    tipo: str = "fixo"     # fixo ou temporario
    data_inicio: str = ""
    data_fim: str = ""
    ativo: bool = True

# ===== CONSTANTES DE ESTILO (PDFs) =====
GOLD = colors.HexColor("#B8860B")
LGRAY = colors.HexColor("#f0f0f0")
DARK = colors.HexColor("#222")
GRAY = colors.HexColor("#888")
FONTE = "Helvetica"
FN = "Helvetica-Bold"

def estilo(tam, bold, cor, alinh=TA_LEFT, antes=0, depois=0, fonte=None, lang="pt"):
    regular, negrito = FONTE_POR_IDIOMA.get(lang, ("Helvetica", "Helvetica-Bold"))
    fn = fonte or (negrito if bold else regular)
    if lang in IDIOMAS_RTL and alinh == TA_LEFT:
        alinh = TA_RIGHT
    return ParagraphStyle(
        "estilo", fontName=fn, fontSize=tam, textColor=cor,
        alignment=alinh, spaceBefore=antes, spaceAfter=depois,
        leading=tam * 1.4
    )


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

# ===== ENERGIAS POR PRODUTO =====
# Ideal (★): padrão pré-selecionado, mas o cliente SEMPRE pode mudar
# Chaves seguem os IDs reais usados no frontend (produtos.html/app.js)
IDEAL_ENERGIA = {
    "urna": "8",        # Validação Nome de Urna (poder)
    "eleitoral": "8",   # Número Eleitoral (poder)
    "artistico": "2",   # Validação Nome Artístico (cooperação, expressão)
    "nome_ong": "6",    # ONG, Instituto, Associação, Fundação (amor altruísta)
    "assinatura": "8",  # Validação de Assinaturas (poder)
    "negocio": "8",     # Nome para Negócio/Produto (poder)
    "ia": "8",          # Pesquisa IA de Nomes (poder/assertividade)
    "bebe": "8",        # Planejamento Nome de Bebê (poder/afirmação)
    "nome_pet": "5",    # Nome do Pet (afeto, sensibilidade)
    "nickname": "8",    # Nickname Digital (presença, autoridade)
    "nome_dominio": "8",# Nome do Domínio (marca forte)
    "nome_canal": "8",  # Nome do Canal (alcance, autoridade)
    "nome_equipe": "8", # Nome da Equipe (união de propósito)
    "nome_projeto": "8",# Nome do Projeto (execução, força)
    "nome_evento": "3", # Nome do Evento (expressão, brilho)
}

ROTULOS_PDF = {
    'pt': {'numero': 'Número', 'valor': 'Valor', 'life_path': 'Caminho de Vida', 'expression': 'Expressão', 'soul_urge': 'Impulso da Alma', 'personality': 'Personalidade', 'destiny': 'Destino'},
    'en': {'numero': 'Number', 'valor': 'Value', 'life_path': 'Life Path', 'expression': 'Expression', 'soul_urge': 'Soul Urge', 'personality': 'Personality', 'destiny': 'Destiny'},
    'es': {'numero': 'Número', 'valor': 'Valor', 'life_path': 'Camino de Vida', 'expression': 'Expresión', 'soul_urge': 'Impulso del Alma', 'personality': 'Personalidad', 'destiny': 'Destino'},
    'it': {'numero': 'Numero', 'valor': 'Valore', 'life_path': 'Sentiero di Vita', 'expression': 'Espressione', 'soul_urge': 'Impulso dell Anima', 'personality': 'Personalità', 'destiny': 'Destino'},
    'fr': {'numero': 'Numéro', 'valor': 'Valeur', 'life_path': 'Chemin de Vie', 'expression': 'Expression', 'soul_urge': 'Impulsion de l Âme', 'personality': 'Personnalité', 'destiny': 'Destinée'},
    'de': {'numero': 'Zahl', 'valor': 'Wert', 'life_path': 'Lebensweg', 'expression': 'Ausdruck', 'soul_urge': 'Seelenimpuls', 'personality': 'Persönlichkeit', 'destiny': 'Schicksal'},
    'ja': {'numero': '数', 'valor': '値', 'life_path': 'ライフパス', 'expression': '表現数', 'soul_urge': '魂の欲求', 'personality': '個性数', 'destiny': '運命数'},
    'zh': {'numero': '数字', 'valor': '数值', 'life_path': '生命路径数', 'expression': '表达数', 'soul_urge': '灵魂数', 'personality': '个性数', 'destiny': '命数'},
    'ru': {'numero': 'Число', 'valor': 'Значение', 'life_path': 'Число жизненного пути', 'expression': 'Число выражения', 'soul_urge': 'Число души', 'personality': 'Число личности', 'destiny': 'Число судьбы'},
    'he': {'numero': 'מספר', 'valor': 'ערך', 'life_path': 'מספר דרך החיים', 'expression': 'מספר הבעה', 'soul_urge': 'מספר הנשמה', 'personality': 'מספר האישיות', 'destiny': 'מספר הגורל'},
    'ar': {'numero': 'الرقم', 'valor': 'القيمة', 'life_path': 'رقم مسار الحياة', 'expression': 'رقم التعبير', 'soul_urge': 'رقم الروح', 'personality': 'رقم الشخصية', 'destiny': 'رقم القدر'},
    'id': {'numero': 'Angka', 'valor': 'Nilai', 'life_path': 'Jalur Kehidupan', 'expression': 'Ekspresi', 'soul_urge': 'Panggilan Jiwa', 'personality': 'Kepribadian', 'destiny': 'Takdir'},
    'tr': {'numero': 'Sayı', 'valor': 'Değer', 'life_path': 'Yaşam Yolu', 'expression': 'İfade', 'soul_urge': 'Ruh Arzusu', 'personality': 'Kişilik', 'destiny': 'Kader'},
    'vi': {'numero': 'Số', 'valor': 'Giá trị', 'life_path': 'Đường đời', 'expression': 'Biểu hiện', 'soul_urge': 'Khát vọng tâm hồn', 'personality': 'Tính cách', 'destiny': 'Số mệnh'},
}

# Fixa (sem seletor): energia gravada no metadata para o PDF usar na explicação.
# O GRAU DE COMPATIBILIDADE de casal/família continua vindo SOMENTE da tabela Cissay.
# Aqui o 5 alimenta a camada textual (energia 5 = campo afetivo, paixão, envolvimento).
ENERGIA_FIXA = {
    "casal": "5",    # Mapa do Casal: energia 5 para explicação afetiva
    "familia": "5",  # Mapa Família Premium: idem
}

# ===== GERADOR DE PDF (usa gerador_pdf.py se existir; senão fallback interno) =====
def _gerar_pdf_local(prod, data, lang, nome, bd, dado=""):
    path = os.path.join(tempfile.gettempdir(), f"p_{prod}_{uuid.uuid4().hex[:8]}.pdf")
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=50, rightMargin=50,
                            topMargin=40, bottomMargin=30)
    e = []
    titulo = PRODUTOS.get(lang, PRODUTOS["pt"]).get(prod, prod).upper()
    e.append(Spacer(1, 15))
    e.append(Paragraph(titulo, estilo(18, True, GOLD, TA_CENTER, 0, 6)))
    e.append(Paragraph(nome.upper(), estilo(12, True, DARK, TA_CENTER, 0, 2)))
    e.append(Paragraph(bd or dado, estilo(9, False, GRAY, TA_CENTER, 0, 10)))
    if isinstance(data, dict):
        r = ROTULOS_PDF.get(lang, ROTULOS_PDF["pt"])
        td = [[r["numero"], r["valor"]]]
        rotulos = [("life_path", r["life_path"]), ("expression", r["expression"]),
                   ("soul_urge", r["soul_urge"]), ("personality", r["personality"]),
                   ("destiny", r["destiny"])]
        for k, l in rotulos:
            if k in data:
                td.append([l, str(data[k])])
        if len(td) > 1:
            tbl = Table(td, colWidths=[200, 100])
            tbl.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), GOLD),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
                ("BACKGROUND", (0, 1), (-1, -1), LGRAY),
            ]))
            e.append(tbl)

        # Descrição do Caminho de Vida (semântica em 14 idiomas)
        if SEMANTICA_OK and data.get("life_path"):
            valor = data["life_path"]
            if valor in (11, 22, 33):
                desc = obter_descricao_mestre(valor, lang)
            else:
                desc = obter_texto_energia(valor, lang)
            if desc:
                e.append(Spacer(1, 6))
                e.append(Paragraph(
                    f"<b>{rotulos[0][1]} {valor}:</b> {desc}",
                    estilo(10, False, DARK)))
        # Forma e Cor da energia pessoal (camada FORMAS_CORES)
        if SEMANTICA_OK and data.get("life_path"):
            fc = renderizar_forma_cor(data["life_path"], lang)
            if fc.get("forma") and fc.get("cor"):
                e.append(Paragraph(
                    f"<b>Forma:</b> {fc['forma']}<br/><b>Cor:</b> {fc['cor']}<br/><b>Sentido:</b> {fc['texto']}",
                    estilo(9, False, GRAY)))
    e.append(Spacer(1, 10))
    e.append(Paragraph("(c) A1ELOS", estilo(7, False, GRAY, TA_CENTER)))
    doc.build(e)
    return path

# ===== DISPATCHER GERAR_PDF (restaurado 07/11/2026 — era perdido na edicao) =====
def gerar_pdf(prod, data, lang, nome, bd, dado=""):
    pf = None
    try:
        import gerador_pdf
        pf = gerador_pdf.gerar_pdf(prod, data, lang, nome, bd, dado)
    except Exception:
        pf = None
    if pf and os.path.exists(pf):
        return pf
    return _gerar_pdf_local(prod, data, lang, nome, bd, dado)

NOTA_SIGILO = {
    # Português
    "pt": ("DOCUMENTO EXCLUSIVO E CONFIDENCIAL",
           "Este material foi gerado exclusivamente para você, apenas para os seus olhos. "
           "A A1ELOS não armazena cópias deste documento em seus servidores. "
           "Se perdê-lo, será necessário gerar um novo — não haverá cópia para recuperar."),
    # Inglês
    "en": ("EXCLUSIVE AND CONFIDENTIAL DOCUMENT",
           "This material was generated exclusively for you, for your eyes only. "
           "A1ELOS does not store copies of this document on its servers. "
           "If lost, a new one must be generated — there will be no copy to recover."),
    # Espanhol
    "es": ("DOCUMENTO EXCLUSIVO Y CONFIDENCIAL",
           "Este material fue generado exclusivamente para usted, solo para sus ojos. "
           "A1ELOS no almacena copias de este documento en sus servidores. "
           "Si lo pierde, deberá generar uno nuevo — no habrá copia para recuperar."),
    # Italiano
    "it": ("DOCUMENTO ESCLUSIVO E RISERVATO",
           "Questo materiale è stato generato esclusivamente per lei, solo per i suoi occhi. "
           "A1ELOS non archivia copie di questo documento sui propri server. "
           "Se lo perde, sarà necessario generarne uno nuovo — non ci sarà copia da recuperare."),
    # Francês
    "fr": ("DOCUMENT EXCLUSIF ET CONFIDENTIEL",
           "Ce document a été généré exclusivement pour vous, uniquement pour vos yeux. "
           "A1ELOS ne stocke aucune copie de ce document sur ses serveurs. "
           "En cas de perte, un nouveau document devra être généré — aucune copie ne pourra être récupérée."),
    # Alemão
    "de": ("EXKLUSIVES UND VERTRAULICHES DOKUMENT",
           "Dieses Material wurde ausschließlich für Sie erstellt, nur für Ihre Augen. "
           "A1ELOS speichert keine Kopien dieses Dokuments auf seinen Servern. "
           "Bei Verlust muss ein neues Dokument erstellt werden — es wird keine Kopie zur Wiederherstellung geben."),
    # Japonês
    "ja": ("専用機密文書",
           "この資料はお客様一人のために特別に作成されました。お客様だけのものです。"
           "A1ELOSはこの文書のコピーをサーバーに保存しません。"
           "紛失した場合は新しく作成し直す必要があります。復元用のコピーは存在しません。"),
    # Chinês
    "zh": ("专属机密文件",
           "本资料专为您一人生成，仅供您本人查阅。"
           "A1ELOS不会在服务器上存储本文件的任何副本。"
           "如若遗失，需重新生成——将没有任何副本可供恢复。"),
    # Russo
    "ru": ("ЭКСКЛЮЗИВНЫЙ И КОНФИДЕНЦИАЛЬНЫЙ ДОКУМЕНТ",
           "Этот материал был подготовлен исключительно для вас и только для ваших глаз. "
           "A1ELOS не хранит копии этого документа на своих серверах. "
           "В случае утери потребуется создать новый документ — восстановить копию будет невозможно."),
    # Hebraico
    "he": ("מסמך בלעדי וחסוי",
           "חומר זה הופק במיוחד עבורך, לעיניך בלבד. "
           "A1ELOS אינה שומרת עותקים של מסמך זה בשרתיה. "
           "אם תאבד אותו, יהיה צורך להפיק מסמך חדש — לא תהיה עותק לשחזור."),
    # Árabe
    "ar": ("وثيقة حصرية وسرية",
           "تم إنشاء هذه المادة خصيصًا لك، لعينيك وحدك. "
           "لا تحتفظ A1ELOS بنسخ من هذه الوثيقة على خوادمها. "
           "إذا فقدتها، فسيكون من الضروري إنشاء وثيقة جديدة — لن توجد نسخة يمكن استعادتها."),
    # Indonésio
    "id": ("DOKUMEN EKSKLUSIF DAN RAHASIA",
           "Materi ini dibuat secara eksklusif untuk Anda, hanya untuk mata Anda sendiri. "
           "A1ELOS tidak menyimpan salinan dokumen ini di servernya. "
           "Jika hilang, dokumen baru harus dibuat — tidak akan ada salinan untuk dipulihkan."),
    # Turco
    "tr": ("ÖZEL VE GİZLİ BELGE",
           "Bu materyal yalnızca sizin için, yalnızca sizin gözleriniz için oluşturuldu. "
           "A1ELOS bu belgenin kopyalarını sunucularında saklamaz. "
           "Kaybederseniz yeni bir belge oluşturulması gerekecektir — kurtarılacak bir kopya olmayacaktır."),
    # Vietnamita
    "vi": ("TÀI LIỆU ĐỘC QUYỀN VÀ BÍ MẬT",
           "Tài liệu này được tạo riêng cho bạn, chỉ dành cho mắt của bạn. "
           "A1ELOS không lưu trữ bất kỳ bản sao nào của tài liệu này trên máy chủ của mình. "
           "Nếu thất lạc, bạn sẽ cần tạo tài liệu mới — sẽ không có bản sao nào để khôi phục."),
}
RTL = {'he', 'ar'}

# ===== Tradução da página de confirmação (14 idiomas) =====
PAG_SUCESSO_TRAD = {
    "pt": {"titulo": "✅ Confirmado!", "ola": "Olá", "gerado": "foi gerado.",
           "btn": "📥 BAIXAR PDF", "voltar": "Voltar",
           "escaneie": "Ou escaneie (ou clique) para abrir o documento", "baixar2": "⬇️ Baixar PDF"},
    "en": {"titulo": "✅ Confirmed!", "ola": "Hello", "gerado": "has been generated.",
           "btn": "📥 DOWNLOAD PDF", "voltar": "Back",
           "escaneie": "Or scan (or click) to open the document", "baixar2": "⬇️ Download PDF"},
    "es": {"titulo": "✅ ¡Confirmado!", "ola": "Hola", "gerado": "fue generado.",
           "btn": "📥 DESCARGAR PDF", "voltar": "Volver",
           "escaneie": "O escanee (o haga clic) para abrir el documento", "baixar2": "⬇️ Descargar PDF"},
    "it": {"titulo": "✅ Confermato!", "ola": "Ciao", "gerado": "è stato generato.",
           "btn": "📥 SCARICA PDF", "voltar": "Indietro",
           "escaneie": "Oppure scansiona (o clicca) per aprire il documento", "baixar2": "⬇️ Scarica PDF"},
    "fr": {"titulo": "✅ Confirmé !", "ola": "Bonjour", "gerado": "a été généré.",
           "btn": "📥 TÉLÉCHARGER PDF", "voltar": "Retour", 
           "escaneie": "Ou scannez (ou cliquez) pour ouvrir le document", "baixar2": "⬇️ Télécharger PDF"},
    "de": {"titulo": "✅ Bestätigt!", "ola": "Hallo", "gerado": "wurde erstellt.",
           "btn": "📥 PDF HERUNTERLADEN", "voltar": "Zurück",
           "escaneie": "Oder scannen (oder klicken), um das Dokument zu öffnen", "baixar2": "⬇️ PDF herunterladen"},
    "ja": {"titulo": "✅ 確認されました！", "ola": "", "gerado": "が生成されました。",
           "btn": "📥 PDFをダウンロード", "voltar": "戻る",
           "escaneie": "スキャンまたはクリックでドキュメントを開く", "baixar2": "⬇️ PDFをダウンロード"},
    "zh": {"titulo": "✅ 已确认！", "ola": "您好", "gerado": "已生成。",
           "btn": "📥 下载PDF", "voltar": "返回",
           "escaneie": "或扫描（或点击）以打开文档", "baixar2": "⬇️ 下载PDF"},
    "ru": {"titulo": "✅ Подтверждено!", "ola": "Здравствуйте", "gerado": "сгенерирован.",
           "btn": "📥 СКАЧАТЬ PDF", "voltar": "Назад",
           "escaneie": "Или отсканируйте (или нажмите), чтобы открыть документ", "baixar2": "⬇️ Скачать PDF"},
    "id": {"titulo": "✅ Dikonfirmasi!", "ola": "Halo", "gerado": "telah dibuat.",
           "btn": "📥 UNDUH PDF", "voltar": "Kembali",
           "escaneie": "Atau pindai (atau klik) untuk membuka dokumen", "baixar2": "⬇️ Unduh PDF"},
    "tr": {"titulo": "✅ Onaylandı!", "ola": "Merhaba", "gerado": "oluşturuldu.",
           "btn": "📥 PDF İNDİR", "voltar": "Geri",
           "escaneie": "Belgeyi açmak için tarayın (veya tıklayın)", "baixar2": "⬇️ PDF İndir"},
    "vi": {"titulo": "✅ Đã xác nhận!", "ola": "Xin chào", "gerado": "đã được tạo.",
           "btn": "📥 TẢI PDF", "voltar": "Quay lại",
           "escaneie": "Hoặc quét (hoặc nhấp) để mở tài liệu", "baixar2": "⬇️ Tải PDF"},
    "he": {"titulo": "✅ אושר!", "ola": "שלום", "gerado": "הופק.",
           "btn": "📥 הורד PDF", "voltar": "חזרה",
           "escaneie": "או סרוק (או לחץ) לפתיחת המסמך", "baixar2": "⬇️ הורד PDF"},
    "ar": {"titulo": "✅ تم التأكيد!", "ola": "مرحباً", "gerado": "تم إنشاؤه.",
           "btn": "📥 تحميل PDF", "voltar": "رجوع",
           "escaneie": "أو امسح (أو انقر) لفتح المستند", "baixar2": "⬇️ تحميل PDF"},
}

def _pagina_sucesso_local(pdf_path, nome, prod_nome, lang="pt", nome_arq=""):
    b64 = ""
    T2 = PAG_SUCESSO_TRAD.get(lang, PAG_SUCESSO_TRAD["pt"])
    if pdf_path and os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
    btn = ""
    if b64:
        btn = (f'<a href="data:application/pdf;base64,{b64}" download="A1ELOS_{prod_nome}.pdf" '
               f'style="display:inline-block;padding:18px 50px;background:#C9A94E;color:#000;'
               f'text-decoration:none;border-radius:50px;font-weight:700;font-size:1.2rem;margin:25px 0">{T2["btn"]}</a>')
    t, txt = NOTA_SIGILO.get(lang, NOTA_SIGILO["pt"])
    dir_attr = ' dir="rtl"' if lang in RTL else ''
    nota = (f'<div style="max-width:560px;margin:38px auto 0;padding:20px 24px;'
            f'border:1px solid #C9A94E55;border-left:3px solid #C9A94E;'
            f'border-radius:6px;background:#141414;text-align:left">'
            f'<p style="color:#C9A94E;font-size:.75rem;letter-spacing:.14em;'
            f'font-weight:700;margin:0 0 10px">{t}</p>'
            f'<p{dir_attr} style="color:#b8b8b8;font-size:.9rem;line-height:1.65;margin:0">{txt}</p></div>')
    beacon = ""
    if nome_arq:
        beacon = (
            '<script>window.addEventListener("beforeunload",function(){'
            'navigator.sendBeacon("/api/sessao-encerrada",'
            'new Blob([JSON.stringify({arq:"' + nome_arq + '"}),'
            '{type:"application/json"}]))});</script>'
        )
    saudacao = f'{T2["ola"]} <b>{nome}</b>, seu {prod_nome} {T2["gerado"]}' if T2["ola"] \
               else f'<b>{nome}</b>様の{prod_nome}{T2["gerado"]}'
    return (f'<html><body style="background:#0a0a0a;color:#fff;text-align:center;padding:40px;'
            f'font-family:sans-serif"><h1 style="color:#C9A94E">{T2["titulo"]}</h1>'
            f'<p>{saudacao}</p>{btn}{nota}{beacon}'
            f'<a href="/" style="color:#C9A94E">{T2["voltar"]}</a></body></html>')

pagina_sucesso = _pagina_sucesso_local

DIR_RELATORIOS = os.path.join(STATIC_DIR, "relatorios")
ARQ_TTL_MINUTOS = 30
os.makedirs(DIR_RELATORIOS, exist_ok=True)

def _limpar_expirados() -> int:
    """Remove PDFs e PNGs mais velhos que o TTL. Rede de segurança do sendBeacon."""
    agora, removidos = time.time(), 0
    if not os.path.isdir(DIR_RELATORIOS):
        return 0
    for arq in os.listdir(DIR_RELATORIOS):
        if not arq.lower().endswith((".pdf", ".png")):
            continue
        try:
            caminho = os.path.join(DIR_RELATORIOS, arq)
            if agora - os.path.getmtime(caminho) > ARQ_TTL_MINUTOS * 60:
                os.remove(caminho)
                removidos += 1
        except Exception:
            pass
    if removidos:
        logger.info(f"Limpeza TTL: {removidos} arquivo(s) removido(s)")
    return removidos

def _apagar_agora(nome_arq: str) -> bool:
    """Apaga um arquivo específico, com proteção contra path traversal."""
    if not nome_arq or ".." in nome_arq or "/" in nome_arq or "\\" in nome_arq:
        return False
    try:
        caminho = os.path.join(DIR_RELATORIOS, nome_arq)
        if os.path.isfile(caminho):
            os.remove(caminho)
            return True
    except Exception as e:
        logger.error(f"Apagar {nome_arq}: {e}")
    return False

@app.post("/api/sessao-encerrada")
async def sessao_encerrada(request: Request):
    try:
        body = await request.json()
        if _apagar_agora(body.get("arq", "")):
            logger.info(f"Apagado ao encerrar: {body.get('arq')}")
    except Exception:
        pass
    return {"ok": True}

# ===== EMAIL SIMPLES =====
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

def gerar_pdf_ong(dados, lang="pt", nome_exib=""):
    path = os.path.join(tempfile.gettempdir(), f"p_ong_{uuid.uuid4().hex[:8]}.pdf")
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=50, rightMargin=50,
                            topMargin=40, bottomMargin=30)
    e = []
    e.append(Spacer(1, 15))
    e.append(Paragraph("VALIDAÇÃO DE NOME DE ENTIDADE", estilo(16, True, GOLD, TA_CENTER, 0, 6)))
    nat = (dados.get("natureza") or "ong").upper()
    tip = (dados.get("tipo") or "").replace("_", " ").upper()
    esc = (dados.get("escopo") or "nacional").upper()
    e.append(Paragraph(f"Natureza: {nat}  |  Tipo: {tip}  |  Escopo: {esc}",
                       estilo(9, False, GRAY, TA_CENTER, 0, 4)))
    e.append(Paragraph(f"Energia pesquisada: {dados.get('energia_alvo', 6)}  |  "
                       f"Ideal do produto: {dados.get('energia_ideal', 6)} ★",
                       estilo(10, True, DARK, TA_CENTER, 0, 10)))
    linhas = [["Item", "Nome", "E. Nome", "Sigla", "E. Sigla", "Melhor"]]
    for i, it in enumerate(dados.get("nomes", []), 1):
        linhas.append([
            str(i),
            it.get("nome") or "-",
            str(it.get("energia_nome") or "-"),
            it.get("sigla") or "-",
            str(it.get("energia_sigla") or "-"),
            (it.get("melhor") or "-").upper(),
        ])
    for i, it in enumerate(dados.get("sugestoes", []), 1):
        linhas.append([
            f"IA {i}",
            it.get("nome") or "-",
            str(it.get("energia_nome") or "-"),
            it.get("sigla") or "-",
            str(it.get("energia_sigla") or "-"),
            "SUGESTÃO",
        ])
    tbl = Table(linhas, colWidths=[45, 185, 60, 90, 60, 85])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GOLD),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("BACKGROUND", (0, 1), (-1, -1), LGRAY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    e.append(tbl)
    if dados.get("recomendacao"):
        e.append(Spacer(1, 10))
        e.append(Paragraph("<b>Recomendação:</b> " + dados["recomendacao"],
                           estilo(10, False, DARK)))
    e.append(Spacer(1, 10))
    e.append(Paragraph("(c) A1ELOS", estilo(7, False, GRAY, TA_CENTER)))
    doc.build(e)
    return path

def gerar_sugestao_ia(produto, energia, lang="pt"):
    """Gera 1 nome de bônus cuja energia bate com a escolhida."""
    BASES = {
        "nome_pet": ["Luna", "Thor", "Mel", "Bidu", "Nina", "Aiko"],
        "nickname": ["Nova", "Zyon", "Kira", "Aura", "Lux", "Vega"],
        "nome_dominio": ["Nova", "Prime", "Aura", "Vera", "Zen", "Core"],
        "nome_canal": ["Vibe", "Flow", "Pulse", "Echo", "Lume", "Nexo"],
        "nome_equipe": ["Nexo", "Vetta", "Alfa", "Core", "Sintra", "Orbe"],
        "nome_projeto": ["Aurora", "Horizonte", "Lume", "Raiz", "Prisma", "Vetta"],
        "nome_evento": ["Gala", "Festa", "Lume", "Viva", "Aurora", "Pulse"],
        "artistico": ["Aurora", "Lume", "Vega", "Nina", "Aiko", "Zyon"],
        "bebe": ["Luna", "Aurora", "Nina", "Aiko", "Vega", "Lux"],
        "assinatura": ["Vega", "Core", "Alfa", "Nexo", "Lux", "Orbe"],
        "negocio": ["Prime", "Core", "Vetta", "Alfa", "Zen", "Nexo"],
    }
    alvo = int(energia or 0)
    base = BASES.get(produto, ["A1ELOS"])
    for nome in base:
        if energia_texto(nome) == alvo:
            return {"nome": nome, "energia": energia_texto(nome), "bonus": True}
    return {"nome": base[0], "energia": energia_texto(base[0]), "bonus": True}

def energia_texto(texto):
    """Fonte única: usa a tabela e a redução de referencia/cissay.py."""
    if not texto:
        return None
    soma = energia_nome(texto)
    if soma == 0:
        return None
    return reduzir(soma)

# ===== PRODUTOS DA PESQUISA IA (7 — Card da IA) =====
PRODUTOS_IA = ["pet", "dominio", "canal", "equipe", "projeto", "evento", "nickname"]

def _criar_sessao(produto, lang="pt", email="", nome="", birth="", meta_extra=None):
    if lang not in PRICE_IDS or produto not in PRICE_IDS[lang]:
        raise HTTPException(status_code=400, detail="Idioma ou produto invalido")
    price_id = PRICE_IDS[lang].get(produto, "")
    nome_prod = PRODUTOS.get(lang, PRODUTOS["pt"]).get(produto, produto)
    meta = {"tipo": produto, "lang": lang, "nome": nome, "birth": birth, "email": email}
    if meta_extra:
        meta.update(meta_extra)
    # Energia padrão: ideal (★) se existir; senão fixa; senão mantém a escolhida
    if produto in IDEAL_ENERGIA and not meta.get("energia"):
        meta["energia"] = IDEAL_ENERGIA[produto]
    elif produto in ENERGIA_FIXA and not meta.get("energia"):
        meta["energia"] = ENERGIA_FIXA[produto]
    pay_types = ["card", "boleto"] if MOEDA.get(lang, "brl") == "brl" else ["card"]
    locale = lang if lang in ["pt", "en", "es", "fr", "de", "it", "ja", "zh", "id", "tr", "vi"] else "auto"

    if produto == "urna":
        success_url = f"{BASE_URL}/api/pay/urna-success?session_id={{CHECKOUT_SESSION_ID}}"
    elif produto == "eleitoral":
        success_url = f"{BASE_URL}/api/pay/eleitoral-success?session_id={{CHECKOUT_SESSION_ID}}"
    else:
        success_url = f"{BASE_URL}/api/pay/success?session_id={{CHECKOUT_SESSION_ID}}"

    try:
        if price_id and price_id.startswith("price_"):
            session = stripe.checkout.Session.create(
                mode="payment", 
                line_items=[{"price": price_id, "quantity": 1}],
                customer_email=email or None,
                locale=locale, metadata=meta,
                payment_method_options={"card": {"installments": {"enabled": True}}} if MOEDA.get(lang, "brl") == "brl" else None,
                success_url=success_url,
                cancel_url=f"{BASE_URL}/api/pay/cancel")
        else:
            session = stripe.checkout.Session.create(
                mode="payment",
                line_items=[{"price_data": {"currency": MOEDA.get(lang, "brl"),
                    "product_data": {"name": nome_prod},
                    "unit_amount": preco_local(produto, lang)}, "quantity": 1}],
                customer_email=email or None,
                locale=locale, metadata=meta,
                payment_method_options={"card": {"installments": {"enabled": True}}} if MOEDA.get(lang, "brl") == "brl" else None,
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
    if not stripe.api_key:
        raise HTTPException(503, "Stripe nao configurado")
    produto = _ALIAS_PRODUTO.get(produto, produto)
    lang = req.lang or "pt"
    return _criar_sessao(produto, lang, req.email, req.nome, req.nascimento)

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

    # meta criada FORA do if, no corpo da função (correção do bug)
    energia = getattr(req, "energia", "") or "8"
    meta = {"tipo": "urna", "lang": req.lang or "pt", "nome_completo": req.nome_completo,
            "cargo": req.cargo, "genero": req.genero, "energia": energia,
            "email": req.email, "nome": req.nome_completo}
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

# ============================================================
# ROTAS DE APRESENTAÇÃO (PDF por idioma — sob demanda)
# ============================================================
IDIOMAS_APRES = ["pt", "en", "es", "it", "fr", "de", "ja", "zh",
                 "ru", "id", "tr", "vi", "he", "ar"]

def _gerar_apresentacao(lang="pt", modo="texto"):
    try:
        import apresentacao_textos as ap
        if modo == "slides":
            caminho = ap.gerar_pdf_slides(lang)
        else:
            caminho = ap.gerar_pdf_texto(lang)
        if caminho and os.path.exists(caminho):
            with open(caminho, "rb") as f:
                return f.read(), os.path.basename(caminho)
        logger.error(f"Apresentacao {lang}/{modo}: caminho invalido: {caminho!r}")
        raise HTTPException(status_code=500,
                            detail=f"Nao foi possivel gerar a apresentacao em {lang} ({modo}).")
    except HTTPException:
        raise
    except Exception:
        logger.exception("Erro ao gerar apresentacao %s/%s", lang, modo)
        raise HTTPException(status_code=500, detail="Erro ao gerar a apresentacao.")

@app.get("/api/apresentacao")
async def api_apresentacao(lang: str = "pt"):
    dados, nome = _gerar_apresentacao(lang, "texto")
    return Response(content=dados, media_type="application/pdf",
                    headers={"Content-Disposition": f'attachment; filename="{nome}"',
                             "Cache-Control": "no-store"})

from fastapi.responses import FileResponse, JSONResponse
from apresentacao_slides_v2 import gerar_apresentacao_slides

@app.get("/api/apresentacao-slides")
async def apresentacao_slides(lang: str = "pt"):
    try:
        caminho = gerar_apresentacao_slides(lang)
        return FileResponse(caminho, media_type="application/pdf",
                            filename="apresentacao_slides_%s.pdf" % lang)
    except Exception as e:
        import traceback
        logging.getLogger("uvicorn.error").error(traceback.format_exc())
        return JSONResponse(status_code=500,
                            content={"detail": "Erro ao gerar slides: %s" % e})
  
# ===== CHECKOUT COLETIVO (desconto progressivo) =====
@app.get("/criar-checkout-coletivo")
async def criar_checkout_coletivo(lang: str = "pt", items: str = "[]"):
    if not stripe.api_key:
        raise HTTPException(503, "Stripe nao configurado")
    try:
        itens = json.loads(items)
    except Exception:
        raise HTTPException(400, "items invalidos")
    if not itens:
        raise HTTPException(400, "Nenhum item")
    qtd_total = sum(int(it.get("qtd", 0)) for it in itens if it.get("qtd"))
    if qtd_total > CONFIG_DESCONTO["teto_automatico"]:
        raise HTTPException(400, "Quantidade acima do limite automatico de desconto. "
                                 "Entre em contato para negociar condicoes especiais.")
    desc = desconto_bc(qtd_total)
    if desc is None:
        desc = 0
    else:
        desc = min(desc, CONFIG_DESCONTO["faixas"][-1]["pct"])  # nunca acima de 50%
    line_items = []
    for it in itens:
        pid = it.get("id")
        qtd = int(it.get("qtd", 0))
        if not pid or qtd <= 0 or pid == "coletivo":
            continue
        unit = preco_local(pid, lang)
        if desc > 0:
            unit = int(round(unit * (1 - desc)))
        line_items.append({"price_data": {"currency": MOEDA.get(lang, "brl"),
            "product_data": {"name": PRODUCT_NAMES.get(lang, PRODUCT_NAMES["pt"]).get(pid, pid)},
            "unit_amount": unit}, "quantity": qtd})
    if not line_items:
        raise HTTPException(400, "Itens invalidos")
    pay_types = ["card", "boleto"] if MOEDA.get(lang, "brl") == "brl" else ["card"]
    locale = lang if lang in ["pt", "en", "es", "fr", "de", "it", "ja", "zh", "id", "tr", "vi"] else "auto"
    session = stripe.checkout.Session.create(
        mode="payment", 
        line_items=line_items,
        locale=locale,
        metadata={"tipo": "coletivo", "lang": lang, "desconto": str(int(desc * 100)),
                  "itens": json.dumps(itens)},
        success_url=BASE_URL + "/static/sucesso.html?session_id={CHECKOUT_SESSION_ID}&lang=" + lang,
        cancel_url=BASE_URL + "/static/cancelado.html")
    return RedirectResponse(url=session.url)

@app.get("/api/precos")
async def api_precos():
 return {
   "valores": VALORES,
   "simbolo": SIMBOLO,
   "display": PRECO_DISPLAY,
   "faixa": PRODUTO_FAIXA,
 }   

# ===== REDIRECIONADOR CURTO PARA O QR CODE =====
@app.get("/r/{sid}")
def r_curto(sid: str, download: int = 0):
    return RedirectResponse(url=f"/api/relatorio/{sid}?download={download}")
    
# ===== LINK PERMANENTE DO RELATORIO (regenera sob demanda) =====
@app.get("/api/relatorio/{session_id}")
def api_relatorio(session_id: str, download: int = 0):
    try:
        s = stripe.checkout.Session.retrieve(session_id)
        meta = getattr(s, "metadata", {}) or {}
        if hasattr(meta, "to_dict"):
            meta = meta.to_dict()
        if getattr(s, "payment_status", "") != "paid":
            return HTMLResponse("Pagamento nao confirmado", status_code=403)

        pf = regenerar_pdf_por_meta(meta)
        conteudo = None
        if pf and os.path.exists(pf):
            with open(pf, "rb") as f:
                conteudo = f.read()
            try:
                os.remove(pf)
            except Exception:
                pass

        if not conteudo:
            return HTMLResponse("Documento indisponivel", status_code=404)

        prod = meta.get("tipo", "express")
        lang = meta.get("lang", "pt")
        disp = "attachment" if download else "inline"
        return Response(content=conteudo, media_type="application/pdf",
                        headers={"Content-Disposition": f'{disp}; filename="A1ELOS_{prod}_{lang}.pdf"',
                                 "Cache-Control": "no-store"})
    except Exception as e:
        logger.error(f"Relatorio {session_id}: {e}")
        return HTMLResponse("Documento indisponivel", status_code=404)
        
@app.get("/api/pay/success")
def pay_success(request: Request):
    sid = request.query_params.get("session_id", "")
    if not sid:
        return HTMLResponse("ERRO")
    url_rel = BASE_URL + "/r/" + sid      # ~35 caracteres em vez de ~70
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
        dado = meta.get("dado", "")
        dado2 = meta.get("dado2", "")
        nome_exib = nome if prod == "calendario" else (nome or dado or "Cliente")          
        if not bd:
            bd = "2000-01-01"

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
        pf = regenerar_pdf_por_meta(meta)

        qr_b64, nome_arq = "", ""
        if pf and os.path.exists(pf):
            try:
                os.makedirs(DIR_RELATORIOS, exist_ok=True)
                _limpar_expirados()
                nome_arq = f"{uuid.uuid4().hex}.pdf"          # UUID, sem identificar
                novo = os.path.join(DIR_RELATORIOS, nome_arq)
                with open(pf, "rb") as f_orig, open(novo, "wb") as f_novo:
                    f_novo.write(f_orig.read())
                logger.info(f"QR aponta para: {url_rel}")    
                qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=2)
                qr.add_data(url_rel)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                qr_b64 = base64.b64encode(buf.getvalue()).decode()
            except Exception as qe:
                logger.error(f"QRCode: {qe}")
        html = pagina_sucesso(pf, nome_exib, pn, lang, nome_arq=nome_arq)

        # Injeta o QRCode junto do botão de download (fallback silencioso)
        if qr_b64:
            T2 = PAG_SUCESSO_TRAD.get(lang, PAG_SUCESSO_TRAD["pt"])
            aviso_qr = (
                '<p style="color:#C9A94E;font-size:0.85rem;max-width:320px;'
                'margin:8px auto;line-height:1.5">'
                '📷 Melhor leitura com o Google Lens · '
                '📷 Best scanned with Google Lens · '
                '📷 Mejor leerlo con Google Lens · '
                '📷 Am besten mit Google Lens scannen · '
                '📷 Mieux lu avec Google Lens · '
                '📷 Meglio con Google Lens · '
                '📷 Лучше считывать через Google Lens · '
                '📷 请用 Google Lens 扫描 · '
                '📷 Google Lens での読み取りがおすすめ · '
                '📷 Google Lens से स्कैन करें · '
                '📷 עדיף לסרוק עם Google Lens · '
                '📷 الأفضل القراءة عبر Google Lens · '
                '📷 Scannen met Google Lens werkt beter · '
                '📷 Google Lens ile okutun'
                '</p>'
            )
            bloco_qr = (
                '<div style="margin:25px auto;text-align:center">'
                f'<p style="color:#C9A94E;font-size:1rem">{T2["escaneie"]}</p>'
                f'<a class="btn" href="{url_rel}?download=1">{T2["baixar2"]}</a>'
                '<br>'
                f'<img src="data:image/png;base64,{qr_b64}" alt="QR Code do relatorio" '
                'style="width:220px;height:220px;border-radius:8px;margin-top:12px">'
                + aviso_qr +
                '</div>'
            )
            if "</body>" in html:
                html = html.replace("</body>", bloco_qr + "</body>")
            else:
                html = html + bloco_qr
            
        return HTMLResponse(html)

    except Exception as e:
        logger.error(f"pay_success {sid}: {e}")
        return HTMLResponse("ERRO AO PROCESSAR PAGAMENTO", status_code=500)

# ===== GERAÇÃO REUTILIZÁVEL DE PDF A PARTIR DOS METADADOS =====
def regenerar_pdf_por_meta(meta):
    """Gera o PDF do produto a partir dos metadados da sessão Stripe.
    Reutilizada pelo pay_success e pela rota permanente /api/relatorio/{session_id}."""
    nome = meta.get("nome", "Cliente")
    bd = meta.get("birth", "")
    prod = meta.get("tipo", "express")
    lang = meta.get("lang", "pt")
    dado = meta.get("dado", "")
    dado2 = meta.get("dado2", "")
    dado3 = meta.get("dado3", "")
    if not bd:
        bd = "2000-01-01"
    energia = meta.get("energia", "")
    nome_exib = nome if prod == "calendario" else (dado or nome)

    def _analisar_nome_duplo():
        nomes = [n for n in (dado, dado2) if n] or [nome]
        res = analisar_nome(nomes[0], energia)
        res["nomes"] = nomes
        res["sugestao_ia"] = gerar_sugestao_ia(prod, energia, lang)
        return res

    def _analisar_casal_com_datas():
        nomes = [x.strip() for x in (dado or nome).split("&")[:2]]
        datas = [x.strip() for x in (meta.get("detalhe", "") or "").split("&")[:2]]
        n1 = nomes[0] if len(nomes) > 0 else ""
        n2 = nomes[1] if len(nomes) > 1 else ""
        d1 = datas[0] if len(datas) > 0 else ""
        d2 = datas[1] if len(datas) > 1 else ""
        return analisar_casal(n1, d1, n2, d2)

    def _analisar_multi_com_datas(fn, dado, detalhe, nome):
        nomes = [x.strip() for x in (dado or nome).split("|")]
        datas = [x.strip() for x in (detalhe or "").split("|")]
        linhas = []
        for i, n in enumerate(nomes):
            if not n:
                continue
            d = datas[i] if i < len(datas) else ""
            linhas.append(f"{n}; {d}" if d else n)
        return fn("\n".join(linhas))
        
    CALC_ESPECIFICO = {
        "imovel": lambda: analisar_imovel(dado, dado2, dado3, lang),
        "casal":     lambda: _analisar_casal_com_datas(),
        "familia": lambda: _analisar_multi_com_datas(analisar_familia, dado, meta.get("detalhe",""), nome),
        "compatibilidade_equipes": lambda: _analisar_multi_com_datas(analisar_equipe, dado, meta.get("detalhe",""), nome),
        "nome_pet":  _analisar_nome_duplo,
        "nickname":  _analisar_nome_duplo,
        "nome_dominio": _analisar_nome_duplo,
        "nome_canal": _analisar_nome_duplo,
        "nome_equipe": _analisar_nome_duplo,
        "nome_projeto": _analisar_nome_duplo,
        "nome_evento": _analisar_nome_duplo,
        "artistico": _analisar_nome_duplo,
        "bebe":      _analisar_nome_duplo,
        "assinatura": _analisar_nome_duplo,
        "negocio":   _analisar_nome_duplo,
        "nome_ong":  lambda: analisar_ong({
            "nome1": meta.get("nome1") or meta.get("dado", ""),
            "sigla1": meta.get("sigla1", ""),
            "nome2": meta.get("nome2", ""),
            "sigla2": meta.get("sigla2", ""),
            "nome3": meta.get("nome3", ""),
            "sigla3": meta.get("sigla3", ""),
            "natureza": meta.get("natureza", "ong"),
            "tipo_entidade": meta.get("tipo_entidade", ""),
            "escopo": meta.get("escopo", "nacional"),
            "energia": energia,
        }),
    }

    # DISPATCH: usa o cálculo específico quando existir
    if prod in CALC_ESPECIFICO:
        try:
            data = CALC_ESPECIFICO[prod]()
        except Exception as e:
            logger.error(f"calc {prod}: {e}")
            data = calc_mapa(nome, bd)
        data["dado"] = dado or ""
    elif prod == "calendario":
        try:
            _d = (dado or "").strip()
            if len(_d) >= 7 and _d[4] == "-":
                _d = _d[:7]                          # '2026-10-28' → '2026-10'
            res_cal = analisar_calendario(nome, _d, bd)
            data = dict(res_cal)
            data["titulo"] = "Calendário Mensal Energético"
            data["nascimento"] = bd or ""
        except Exception as e:
            logger.error(f"Calendario calc: {e}")
            data = {"titulo": "Calendário Mensal Energético", "nascimento": dado or ""}
    else:                                    
        data = calc_mapa(nome, bd)           
        data["dado"] = dado or ""           
    logger.info(f"PDF dados {prod}: {list((data or {}).keys())}")
    if prod == "calendario":
        pf = gerar_pdf_calendario(data, lang, nome_exib)
    elif prod == "nome_ong":
        pf = gerar_pdf_ong(data, lang, nome_exib)
    else:
        pf = gerar_pdf(prod, data, lang, nome_exib, bd, dado=dado)
    return pf          
    
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
        lang = meta.get("lang", "pt")
        genero = meta.get("genero", "masculino")
        res, ideal, sugs = validar_nomes_urna(nomes, cr, lang=lang, genero=genero, nome_base=nc)
        cl = CARGO_INFO.get(cr, {}).get("label", cr)
        dados_urna = {"nome_completo": nc, "cargo_label": cl,
                      "resultados": res, "sugestoes": sugs, "ideal": ideal}
        pf = gerar_pdf("urna", dados_urna, lang, nc, "")
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
        cl_map = {"vereador": "Vereador", "dep_estadual": "Dep. Estadual",
                  "dep_federal": "Dep. Federal", "senador": "Senador"}
        cl2 = cl_map.get(cr, cr)
        sugs = gerar_numeros(sg, cr)
        ni = None
        if ne_str and len(ne_str) >= 3:
            try:
                ni = {"numero": ne_str, "energia": reduzir(sum(int(d) for d in ne_str))}
            except Exception:
                pass
        lang = meta.get("lang", "pt")
        dados_ele = {"sigla": ss, "cargo_label": cl2,
                     "sugestoes": sugs, "numero_existente": ni}
        pf = gerar_pdf("eleitoral", dados_ele, lang, f"Candidato {cl2}", "")
        html = pagina_sucesso(pf, f"Candidato {cl2}",
                              PRODUTOS.get(lang, PRODUTOS["pt"]).get("eleitoral", "Eleitoral"), lang)
        if pf and os.path.exists(pf):
            os.remove(pf)
        return HTMLResponse(html)
    except Exception:
        return HTMLResponse("ERRO")

# ===== HEALTH CHECK PARA O RENDER (evita o "Timed Out") =====
@app.get("/", include_in_schema=False)
async def index():
    return RedirectResponse(url="/static/index.html")

@app.head("/", include_in_schema=False)
async def index_head():
    return Response(status_code=200)

@app.get("/health", include_in_schema=False)
async def health():
    return {"status": "ok"}

@app.head("/health", include_in_schema=False)
async def health_head():
    return Response(status_code=200)

# ===== ROTA /criar-checkout (usada pelo site) =====
@app.get("/criar-checkout")

async def criar_checkout_direto(lang: str = "pt", produto: str = "express",
                                qtd: int = 0, total: float = 0, itens: str = "",
                                nome: str = "", nascimento: str = "",
                                nome_completo: str = "", cargo: str = "vereador",
                                genero: str = "masculino",
                                numero: str = "", email: str = "",
                                nome1: str = "", nome2: str = "", nome3: str = "",
                                nome4: str = "", nome5: str = "",
                                sigla1: str = "", sigla2: str = "", sigla3: str = "",
                                natureza: str = "ong", tipo_entidade: str = "",
                                escopo: str = "nacional",
                                energia: str = "", dado: str = "", dado2: str = "", dado3: str = "",
                                tipo: str = "", numero_existente: str = "",
                                area: str = "", detalhe: str = "", apelido: str = ""):    
    if not stripe.api_key:
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
                "nome_completo": nome_completo, "numero_existente": numero_existente}
    elif produto == "nome_ong":
        n_principal = nome1 or nome2 or nome3
        meta = {"nome": n_principal, "dado": n_principal,
                "nome1": nome1, "sigla1": sigla1,
                "nome2": nome2, "sigla2": sigla2,
                "nome3": nome3, "sigla3": sigla3,
                "natureza": natureza, "tipo_entidade": tipo_entidade,
                "escopo": escopo}
    else:
        meta = {"energia": energia, "dado": dado, "dado2": dado2, "dado3": dado3, "tipo": tipo,
                "area": area, "detalhe": detalhe}
        if apelido:
            meta["nome"] = apelido          # apelido vira o nome de exibição
    meta["tipo"] = meta.get("tipo") or produto
    meta["nome"] = meta.get("nome") or nome
    meta["nascimento"] = meta.get("nascimento") or nascimento
    meta["birth"] = meta.get("birth") or nascimento   # chave lida pelo regenerar_pdf
    s = _criar_sessao(produto, lang, email, nome, nascimento, meta)
    return RedirectResponse(url=s["url"])
# ===== SUCESSO POS-PAGAMENTO =====
DADO_PRODUTOS = {"nome_pet", "nickname", "nome_dominio", "nome_canal",
                 "nome_equipe", "nome_projeto", "nome_evento"}

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
        res = calc_mapa(req.nome, req.nascimento)
        cid = uuid.uuid4().hex[:8]
        db.add(Calc(id=cid, name=req.nome, birth_date=req.nascimento, email=req.email or "", **res))
        db.commit()
        res["download_pdf"] = False
        return {"id": cid, **res}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Falha ao gerar apresentacao: %s", e)
        raise HTTPException(status_code=500, detail="Erro ao gerar a apresentação.")
    finally:
        db.close()

ZERO_DECIMAL = {"ja", "vi"}  # moedas sem centavos no Stripe

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

@app.get("/config")
def config():
    return {"stripe_pk": STRIPE_PUB}

@app.get("/api/health")
def health_api():
    return {"status": "ok", "stripe": bool(STRIPE_KEY)}

# ===== WEBHOOK STRIPE =====
@app.post("/stripe_webhook")
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

    if event["type"] == "checkout.session.completed":
        try:
            session = event["data"]["object"]
            meta = getattr(session, "metadata", None) or {}
            if hasattr(meta, "to_dict"):
                meta = meta.to_dict()
            logger.info(f"Pagamento confirmado: {getattr(session, 'id', '')} tipo={meta.get('tipo', '?')}")
        except Exception as e:
            logger.error(f"Webhook leitura: {e}")

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

# ===== VALIDAÇÃO DE CÓDIGOS (Opção C - base-32 + check digit) =====
COD_ALFABETO = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"

def _checksum(base):
    soma = sum(COD_ALFABETO.index(ch) for ch in base)
    return COD_ALFABETO[soma % len(COD_ALFABETO)]

def _gerar_codigo_bonus():
    base = "".join(secrets.choice(COD_ALFABETO) for _ in range(7))
    return f"A1-{base[:4]}-{base[4:]}{_checksum(base)}"

def _gerar_codigos_para_itens(itens):
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
    return {"ok": True, "target": target, "produto": info.get("produto"),
            "energia": info.get("energia", ""), "liberacao": info.get("liberacao", "compra")}

async def gerar_codigos_coletivo(req: BonusReq):
    if not req.motivo:
        raise HTTPException(400, "Motivo obrigatorio")
    itens = [{"id": "express", "qtd": 1}]
    gerados = _gerar_codigos_para_itens(itens)
    return {"ok": True, "gerados": gerados, "motivo": req.motivo}

@app.post("/sugestao")
async def receber_sugestao(
    nome: str = Form(...),
    email: str = Form(...),
    mensagem: str = Form(...),
    documento: UploadFile = File(None),
):
    if not email or "@" not in email:
        raise HTTPException(status_code=400, detail="E-mail obrigatório para resposta e envio do bônus.")
    anexo = None
    if documento and documento.filename:
        if not documento.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Apenas PDF é aceito.")
        anexo = await documento.read()
    corpo = f"Sugestão de {nome} ({email}):\n\n{mensagem}"
    _enviar_email_simples(ADMIN_EMAIL, "Nova Sugestão A1ELOS", corpo)
    return {"ok": True}

def _cod_valido(codigo: str) -> bool:
    c = "".join(ch for ch in (codigo or "").upper() if ch.isalnum())
    if len(c) != 10 or c[:2] != "A1": return False
    return _checksum(c[2:9]) == c[9]

@app.post("/api/negociacao")
async def negociar_bonus(req: NegociacaoReq):
    corpo = (f"PEDIDO SOB CONSULTA — BÔNUS COLETIVO (desconto progressivo)\n\n"
             f"Nome: {req.nome}\nEmpresa: {req.empresa}\nE-mail: {req.email}\n"
             f"Quantidade estimada: {req.quantidade}\n\n"
             f"Mensagem: {req.mensagem or '-'}")
    ok = _enviar_email_simples(ADMIN_EMAIL, "Novo pedido sob consulta - Bônus Coletivo A1ELOS", corpo)
    return {"ok": ok}

# ===== SISTEMA DE PUBLICIDADE GEOLOCALIZADA (resgatado do main anterior) =====
ARQ_BANNERS = "static/banners.json"
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
        return {"ok": False, "banners": []}
    continente = PAIS_CONTINENTE.get(pais.upper(), "")
    hoje = date.today().isoformat()
    ativos = []
    for b in banners:
        if not b.get("ativo") or b.get("posicao") != posicao:
            continue
        if b.get("tipo") == "temporario":
            if b.get("data_fim") and hoje > b["data_fim"]:
                continue
            if b.get("data_inicio") and hoje < b["data_inicio"]:
                continue
        ativos.append(b)
    if not ativos:
        return {"ok": False, "banners": []}
    def grau(b):
        if b.get("escopo") == "pais":
            return 3 if b.get("pais") == pais.upper() else 0
        if b.get("escopo") == "continente":
            return 2 if b.get("continente") == continente else 0
        return 1
    ativos.sort(key=grau, reverse=True)
    grau_max = grau(ativos[0])
    ativos = [b for b in ativos if grau(b) == grau_max]
    return {"ok": True, "banners": ativos, "banner": ativos[0]}
