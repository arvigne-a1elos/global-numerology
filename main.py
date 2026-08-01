# -*- coding: utf-8 -*-
# main.py - Global Numerology API (completo, autossuficiente)
import os, json, uuid, logging
from datetime import date, datetime
from typing import Optional
import stripe
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUB = os.getenv("STRIPE_PUBLISHABLE_KEY", "")
SENDGRID_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@a1elos.com.br")
SITE_URL = os.getenv("SITE_URL", "https://global-numerology.onrender.com")

# ===== 48 PREÇOS STRIPE - 12 IDIOMAS × 4 PRODUTOS =====
PRICE_IDS = {
    "de": {"express": "price_1TyFJaBMLa84bVJ0BDPNQUjz", "completo": "price_1TyFLKBMLa84bVJ0RT0bkKpW", "urna": "price_1TyFO2BMLa84bVJ0FIoh7co1", "eleitoral": "price_1TyFTxBMLa84bVJ0qw6LQvVI"},
    "ar": {"express": "price_1TyHXkBMLa84bVJ0DDl7y8rT", "completo": "price_1TyHerBMLa84bVJ0UIFTeKLW", "urna": "price_1TyHpxBMLa84bVJ0Z9Ck3rk3", "eleitoral": "price_1TyHrvBMLa84bVJ0RWjoe4Gz"},
    "zh": {"express": "price_1TyKXeBMLa84bVJ07Q6w0j6G", "completo": "price_1TyKZfBMLa84bVJ0bgYSm8e2", "urna": "price_1TyKdWBMLa84bVJ0TIP0Knbi", "eleitoral": "price_1TyKitBMLa84bVJ0lFgyKya0"},
    "es": {"express": "price_1TyD2oBMLa84bVJ0HvSTMozS", "completo": "price_1TyD6NBMLa84bVJ0s5y2OtSr", "urna": "price_1TyDB0BMLa84bVJ0baUEGa2P", "eleitoral": "price_1TyDCsBMLa84bVJ0NRp5uOKU"},
    "fr": {"express": "price_1TyDnQBMLa84bVJ0K9DBz2mk", "completo": "price_1TyDrjBMLa84bVJ0cstgcPbY", "urna": "price_1TyDw1BMLa84bVJ0EV0OnINW", "eleitoral": "price_1TyDxsBMLa84bVJ0n2t4jOfZ"},
    "he": {"express": "price_1TyIKeBMLa84bVJ0W02dbXOt", "completo": "price_1TyIO0BMLa84bVJ08P0j9THk", "urna": "price_1TyIPbBMLa84bVJ08GnGksRk", "eleitoral": "price_1TyISQBMLa84bVJ0sb7xjIyV"},
    "hi": {"express": "price_1TyG1uBMLa84bVJ0NY4TpZnO", "completo": "price_1TyG84BMLa84bVJ05zeaelyO", "urna": "price_1TyGD5BMLa84bVJ0hEnIEwaS", "eleitoral": "price_1TyGFYBMLa84bVJ0zZTHtAuT"},
    "en": {"express": "price_1TxotnBMLa84bVJ00SGo4kjO", "completo": "price_1TxoxfBMLa84bVJ0VgQVddZX", "urna": "price_1Txp1jBMLa84bVJ06W4559rN", "eleitoral": "price_1Txp5aBMLa84bVJ0GqrvBrIk"},
    "it": {"express": "price_1TyEtPBMLa84bVJ02T3hWgMD", "completo": "price_1TyEwfBMLa84bVJ0Fh9etZKk", "urna": "price_1TyEz0BMLa84bVJ0Qkjg7Y0X", "eleitoral": "price_1TyF2PBMLa84bVJ0lropcWH8"},
    "ja": {"express": "price_1TyJ5HBMLa84bVJ00nZLnuV1", "completo": "price_1TyJJgBMLa84bVJ0fkO5nSFT", "urna": "price_1TyJOzBMLa84bVJ0BAPegYVD", "eleitoral": "price_1TyJRwBMLa84bVJ0PLA1CIuH"},
    "pt": {"express": "price_1TxocVBMLa84bVJ0EL0kb9Dn", "completo": "price_1TxohlBMLa84bVJ0jVj9307b", "urna": "price_1TxollBMLa84bVJ0Wk5zIak6", "eleitoral": "price_1TxopFBMLa84bVJ0jvtJExVj"},
    "ru": {"express": "price_1TyJxhBMLa84bVJ0aQxWf1Tp", "completo": "price_1TyK1CBMLa84bVJ0SsvJjSqb", "urna": "price_1TyK3NBMLa84bVJ0GCSVqMe0", "eleitoral": "price_1TyK7hBMLa84bVJ004FNS2fZ"}
}

PRODUTOS = {
    "pt": {"express": "Mapa Express", "completo": "Mapa Completo", "urna": "Nome de Urna", "eleitoral": "Número Eleitoral"},
    "en": {"express": "Express Map", "completo": "Complete Map", "urna": "Ballot Name", "eleitoral": "Electoral Number"},
    "es": {"express": "Mapa Exprés", "completo": "Mapa Completo", "urna": "Nombre de Urna", "eleitoral": "Número Electoral"},
    "fr": {"express": "Carte Express", "completo": "Carte Complète", "urna": "Nom du Bulletin", "eleitoral": "Numéro Électoral"},
    "it": {"express": "Mappa Espressa", "completo": "Mappa Completa", "urna": "Nome della Scheda", "eleitoral": "Numero Elettorale"},
    "de": {"express": "Express-Karte", "completo": "Vollständige Karte", "urna": "Stimmzettelname", "eleitoral": "Wahlnummer"},
    "ru": {"express": "Экспресс-карта", "completo": "Полная карта", "urna": "Название бюллетеня", "eleitoral": "Избирательный номер"},
    "zh": {"express": "快速地图", "completo": "完整地图", "urna": "选票名称", "eleitoral": "选举号码"},
    "ja": {"express": "エクスプレスマップ", "completo": "完全マップ", "urna": "投票用紙名", "eleitoral": "選挙番号"},
    "hi": {"express": "त्वरित मानचित्र", "completo": "पूर्ण मानचित्र", "urna": "मतपत्र का नाम", "eleitoral": "निर्वाचन संख्या"},
    "he": {"express": "מפה מהירה", "completo": "מפה מלאה", "urna": "שם פתק ההצבעה", "eleitoral": "מספר בחירות"},
    "ar": {"express": "خريطة سريعة", "completo": "خريطة كاملة", "urna": "اسم الاقتراع", "eleitoral": "الرقم الانتخابي"}
}

app = FastAPI(title="Global Numerology")

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

class PayReq(BaseModel):
    name: str
    birth_date: str
    email: Optional[str] = ""
    phone: Optional[str] = ""

class UrnaPayReq(BaseModel):
    nome_completo: str
    data_nascimento: str
    nome_urna: str
    email: Optional[str] = ""
    phone: Optional[str] = ""

class EleitoralPayReq(BaseModel):
    nome_completo: str
    data_nascimento: str
    numero_titulo: str
    email: Optional[str] = ""
    phone: Optional[str] = ""

def reduzir(n, permitir_mestre=True):
    while n > 9:
        if permitir_mestre and n in (11, 22, 33):
            return n
        n = sum(int(d) for d in str(n))
    return n

def calc_mapa(nome, data_nasc):
    from dateutil.parser import parse as dp
    bd = dp(data_nasc).date()
    d, m, a = bd.day, bd.month, bd.year
    vida = reduzir(d + m + a)
    t = {c: (i % 9 or 9) for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 1)}
    nu = nome.upper().replace(" ", "")
    total_e = total_v = total_p = 0
    for ch in nu:
        val = t.get(ch, 0)
        total_e += val
        if ch in "AEIOU":
            total_v += val
        else:
            total_p += val
    exp = reduzir(total_e)
    mot = reduzir(total_v)
    pers = reduzir(total_p)
    dest = reduzir(vida + exp)
    vib = {
        1: "Liderança, independência, pioneirismo.",
        2: "Cooperação, sensibilidade, equilíbrio.",
        3: "Criatividade, comunicação, otimismo.",
        4: "Disciplina, praticidade, estabilidade.",
        5: "Liberdade, versatilidade, aventura.",
        6: "Responsabilidade, amor, harmonia.",
        7: "Sabedoria, análise, espiritualidade.",
        8: "Poder, realização, ambição.",
        9: "Compaixão, humanitarismo, idealismo.",
        11: "Intuição elevada, inspiração.",
        22: "Construtor do impossível.",
        33: "Mestre da compaixão."
    }
    signos = [
        (3,21,4,20,"Áries"), (4,21,5,20,"Touro"), (5,21,6,20,"Gêmeos"),
        (6,21,7,22,"Câncer"), (7,23,8,22,"Leão"), (8,23,9,22,"Virgem"),
        (9,23,10,22,"Libra"), (10,23,11,21,"Escorpião"), (11,22,12,21,"Sagitário"),
        (12,22,1,20,"Capricórnio"), (1,21,2,19,"Aquário"), (2,20,3,20,"Peixes")
    ]
    idade = date.today().year - a - ((date.today().month, date.today().day) < (m, d))
    def calc_signo(d, m):
        for mi, di, mf, df, s in signos:
            if (m == mi and d >= di) or (m == mf and d <= df):
                return s
        return "Capricórnio"
    ano_atual = datetime.now().year
    anos_p = {}
    for i in range(5):
        anos_p[ano_atual + i] = str(reduzir(d + m + (ano_atual + i)))
    return {
        "life_path": str(vida), "expression": str(exp),
        "soul_urge": str(mot), "personality": str(pers), "destiny": str(dest),
        "vib_life_path": vib.get(vida, ""), "vib_expression": vib.get(exp, ""),
        "vib_soul_urge": vib.get(mot, ""), "vib_personality": vib.get(pers, ""),
        "vib_destiny": vib.get(dest, ""),
        "age": idade, "sign": calc_signo(d, m),
        "personal_years": anos_p, "full_name": nome.upper(),
        "birth_date": data_nasc
    }

def gerar_pdf_enviar(nome, data_str, res, email):
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
    import base64
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    G = colors.HexColor("#B8860B")
    L = colors.HexColor("#f0f0f0")
    D = colors.HexColor("#222")
    def es(n, f, s, c, a, sb=0, sa=0):
        return ParagraphStyle(n, fontName=f, fontSize=s, textColor=c, alignment=a, spaceBefore=sb, spaceAfter=sa, leading=s*1.5)
    pf = f"/tmp/pdf_{uuid.uuid4().hex[:8]}.pdf"
    doc = SimpleDocTemplate(pf, pagesize=A4, leftMargin=50, rightMargin=50)
    el = [Spacer(1, 30)]
    el.append(Paragraph("MAPA NUMEROLOGICO", es("T", "Helvetica-Bold", 20, G, TA_CENTER, sa=40)))
    el.append(Paragraph(nome.upper(), es("N", "Helvetica-Bold", 16, D, TA_CENTER, sa=4)))
    el.append(Paragraph(data_str, es("D", "Helvetica", 12, colors.HexColor("#888"), TA_CENTER, sa=20)))
    td = [["Número", "Valor"],["Caminho de Vida", res["life_path"]],["Expressão", res["expression"]],["Motivação", res["soul_urge"]],["Personalidade", res["personality"]],["Destino", res["destiny"]]]
    tbl = Table(td, colWidths=[200, 150])
    tbl.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),G),("TEXTCOLOR",(0,0),(-1,0),colors.white),("FONTSIZE",(0,0),(-1,-1),12),("GRID",(0,0),(-1,-1),0.5,colors.grey),("ALIGN",(1,0),(1,-1),"CENTER"),("BACKGROUND",(0,1),(-1,-1),L)]))
    el.append(tbl)
    el.append(Paragraph("Copyright A1ELOS", es("F", "Helvetica", 10, colors.HexColor("#888"), TA_CENTER, sb=40)))
    doc.build(el)
    msg = Mail(from_email=FROM_EMAIL, to_emails=email, subject="Seu Mapa Numerológico", plain_text_content=f"Olá {nome},\n\nSeu mapa foi gerado.\n\nA1ELOS")
    with open(pf, "rb") as f:
        data_b64 = base64.b64encode(f.read()).decode()
    msg.add_attachment(Attachment(FileContent(data_b64), FileName("Mapa.pdf"), FileType("application/pdf"), Disposition("attachment")))
    if SENDGRID_KEY:
        SendGridAPIClient(SENDGRID_KEY).send(msg)
    if os.path.exists(pf):
        os.remove(pf)

def sugerir_produtos(idioma: str, produto_atual: str):
    sugestoes = []
    todos = ["express", "completo", "urna", "eleitoral"]
    for p in todos:
        if p != produto_atual:
            sugestoes.append({
                "id": p,
                "nome": PRODUTOS[idioma][p],
                "link": f"/criar-checkout?lang={idioma}&produto={p}"
            })
    return sugestoes[:2]

@app.get("/")
def index():
    return RedirectResponse(url="/static/index.html")

@app.get("/config")
def config():
    return {"stripe_pk": STRIPE_PUB}

@app.get("/criar-checkout")
async def criar_checkout(lang: str = "pt", produto: str = "express"):
    if lang not in PRICE_IDS or produto not in PRICE_IDS[lang]:
        raise HTTPException(status_code=400, detail="Idioma ou produto inválido")
    
    price_id = PRICE_IDS[lang][produto]
    
    session = stripe.checkout.Session.create(
        payment_method_types=["card", "boleto"],
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
        locale=lang if lang in ["pt", "en", "es", "fr", "de", "it", "ja", "zh"] else "auto",
        success_url=f"{SITE_URL}/static/sucesso.html?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{SITE_URL}/static/cancelado.html",
    )
    return {"url": session.url}

@app.post("/calculate")
def calculate(req: PayReq):
    if len(req.name.strip()) < 2:
        raise HTTPException(400, "Nome curto")
    if not req.birth_date:
        raise HTTPException(400, "Data obrigatória")
    try:
        res = calc_mapa(req.name, req.birth_date)
        cid = uuid.uuid4().hex[:8]
        if req.email and req.email.strip():
            try:
                gerar_pdf_enviar(req.name, req.birth_date, res, req.email.strip())
            except Exception as e:
                logger.error(f"Falha email grátis: {e}")
        return {"id": cid, **res}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro calc: {e}")
        raise HTTPException(500, "Erro no cálculo")

@app.post("/calculate/urna")
def calc_urna(req: UrnaPayReq):
    res = calc_mapa(req.nome_completo, req.data_nascimento)
    res["nome_urna"] = req.nome_urna
    return res

@app.post("/calculate/eleitoral")
def calc_eleitoral(req: EleitoralPayReq):
    nums = [int(c) for c in req.numero_titulo if c.isdigit()][:12]
    while len(nums) < 12:
        nums.append(0)
    res = calc_mapa(req.nome_completo, req.data_nascimento)
    res["numero_titulo"] = req.numero_titulo
    res["titulo_sum"] = sum(nums)
    res["titulo_reduced"] = reduzir(sum(nums))
    return res

def _checkout(price, name, metadata):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card", "boleto"],
            line_items=[{"price_data":{"currency":"brl","product_data":{"name":name},"unit_amount":price},"quantity":1}],
            mode="payment",
            success_url=f"{SITE_URL}/static/sucesso.html",
            cancel_url=f"{SITE_URL}/static/cancelado.html",
            metadata=metadata)
        return {"id": session.id, "url": session.url}
    except Exception as e:
        logger.error(f"Stripe: {e}")
        raise HTTPException(500, "Erro ao criar pagamento")

@app.post("/pay/express")
def pay_express(req: PayReq):
    return _checkout(800, "Mapa Numerológico Express", {"type":"express","name":req.name,"birth":req.birth_date})

@app.post("/pay/complete")
def pay_complete(req: PayReq):
    return _checkout(1700, "Mapa Numerológico Completo", {"type":"complete","name":req.name,"birth":req.birth_date})

@app.post("/pay/urna")
def pay_urna(req: UrnaPayReq):
    return _checkout(2600, "Nome de Urna", {"type":"urna","name":req.nome_completo,"birth":req.data_nascimento,"urna":req.nome_urna})

@app.post("/pay/eleitoral")
def pay_eleitoral(req: EleitoralPayReq):
    return _checkout(2600, "Número Eleitoral", {"type":"eleitoral","name":req.nome_completo,"birth":req.data_nascimento,"titulo":req.numero_titulo})

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
        event = {"type": data.get("type",""), "data": data.get("data",{})}
    if event["type"] == "checkout.session.completed":
        sess = event["data"]["object"]
        logger.info(f"Pagamento confirmado: {sess.get('id')}")
    return {"ok": True}

# ===== CAIXA DE SUGESTÕES + BÔNUS (A1ELOS) =====
import os, secrets, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pydantic import BaseModel

ADMIN_EMAIL = "arvigne@gmail.com"   # não revelar no frontend

class SugestaoReq(BaseModel):
    mensagem: str

class BonusReq(BaseModel):
    nome: str
    email: str
    produto: str
    mensagem: str

def _enviar_email(destinatario: str, assunto: str, corpo: str):
    msg = MIMEMultipart()
    msg["From"] = os.getenv("SMTP_USER", "no-reply@a1elos.com")
    msg["To"] = destinatario
    msg["Subject"] = assunto
    msg.attach(MIMEText(corpo, "plain", "utf-8"))
    with smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT", 587))) as s:
        s.starttls()
        s.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
        s.send_message(msg)

@app.post("/sugestao")
async def receber_sugestao(req: SugestaoReq):
    try:
        _enviar_email(ADMIN_EMAIL, "Nova sugestão/reclamação — A1ELOS",
                      "Mensagem:\n" + req.mensagem +
                      "\n\n(Se educada e útil, cliente ganha 1 pesquisa IA grátis.)")
        return {"ok": True}
    except Exception:
        return {"ok": False}

@app.post("/bonus")
async def solicitar_bonus(req: BonusReq):
    codigo = "BONUS-" + secrets.token_hex(3).upper()
    try:
        corpo = (f"Cliente: {req.nome}\nEmail: {req.email}\nProduto: {req.produto}\n"
                 f"Código gerado: {codigo}\nRelato:\n{req.mensagem}\n\n"
                 "Ação: garantir o produto comprado, liberar nova pesquisa/PDF e, "
                 "se persistir, enviar o PDF após a correção. "
                 "Cliente ganha 1 serviço IA grátis como complemento.")
        _enviar_email(ADMIN_EMAIL, "Pedido de BÔNUS — pane no pagamento", corpo)
        _enviar_email(req.email, "A1ELOS — Seu código bônus",
                      f"Olá, {req.nome}!\nSeu código: {codigo}\n"
                      "Use-o na próxima tentativa para garantir seu produto. "
                      "Se o problema persistir, responderemos por este email "
                      "assim que o sistema for corrigido.\n\nA1ELOS")
        return {"ok": True, "codigo": codigo}
    except Exception:
        return {"ok": False}
