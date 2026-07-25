# -*- coding: utf-8 -*-
import os, logging, uuid, stripe, base64, json, secrets, smtplib
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
import dateutil.parser as dp
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dicionarios import TRAD, t, get_sig, get_cam, get_des, get_vib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

STRIPE_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", "arvigne@gmail.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
FROM_NAME = "Mapa Numerologico"
BASE_URL = os.getenv("BASE_URL", "https://global-numerology.onrender.com")
DB_URL = os.getenv("DATABASE_URL", "sqlite:///./numerologia.db")
logger.info(f"Stripe={bool(STRIPE_KEY)}")
if STRIPE_KEY:
    stripe.api_key = STRIPE_KEY

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
Session = sessionmaker(bind=engine)

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

class Payment(Base):
    __tablename__ = "payments"
    id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String)
    birth_date = Column(String)
    product = Column(String)
    lang = Column(String, default="pt")
    status = Column(String, default="pending")
    payment_method = Column(String, default="card")
    download_token = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PayReq(BaseModel):
    name: str
    email: Optional[str] = ""
    product: Optional[str] = "pdf8"
    price: Optional[float] = 0
    calculation_id: Optional[str] = None
    birth_date: Optional[str] = None
    lang: Optional[str] = "pt"
    payment_method: Optional[str] = "card"

# ---- FUNÇÕES AUXILIARES ----

def r1(n, permitir_mestre=True):
    while n > 9 and n not in (11, 22, 33):
        n = sum(int(d) for d in str(n))
    return n

def calc(name, bd_str):
    bd = dp.parse(bd_str).date()
    lp = r1(bd.day + bd.month + bd.year)
    nu = name.upper().replace(" ", "")
    let = {c: (i % 9 or 9) for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 1)}
    e, v, c = 0, 0, 0
    for ch in nu:
        val = let.get(ch, 0)
        e += val
        if ch in "AEIOU":
            v += val
        else:
            c += val
    return {
        "life_path": lp,
        "expression": r1(e),
        "soul_urge": r1(v),
        "personality": r1(c),
        "destiny": r1(r1(e) + lp),
    }

def calc_grid(name):
    let = {c: (i % 9 or 9) for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 1)}
    g = {i: 0 for i in range(1, 10)}
    for ch in name.upper().replace(" ", ""):
        v = let.get(ch, 0)
        if 1 <= v <= 9:
            g[v] += 1
    return g

GOLD = colors.HexColor("#C9A94E")
DARK = colors.HexColor("#1A1A1A")
GRAY = colors.HexColor("#9E9E9E")
TAM_T = 22
TAM_S = 14
TAM_C = 11
ES = 8
ET = 14

def est(nome, size, bold, cor, align, sb, sa):
    return ParagraphStyle(
        nome,
        fontName="Helvetica-Bold" if bold else "Helvetica",
        fontSize=size,
        textColor=cor,
        alignment=align,
        spaceBefore=sb,
        spaceAfter=sa,
        leading=size * 1.4,
    )

def pdf8(data, name, bd_str, lang="pt"):
    path = f"/tmp/p8_{uuid.uuid4().hex[:8]}.pdf"
    doc = SimpleDocTemplate(
        path, pagesize=A4, leftMargin=50, rightMargin=50, topMargin=45, bottomMargin=45
    )
    e = []
    TIT = est("TI", TAM_T, True, GOLD, TA_CENTER, 0, ET)
    NM = est("NM", 15, True, DARK, TA_CENTER, 0, 4)
    DT = est("DT", TAM_C - 2, False, GRAY, TA_CENTER, 0, ES)
    SEC = est("SE", TAM_S, True, GOLD, TA_LEFT, ES, ET)
    TXT = est("TX", TAM_C - 1, False, DARK, TA_JUSTIFY, 0, ES * 0.4)
    e.append(Spacer(1, 40))
    e.append(Paragraph(t("seu_perfil", lang), TIT))
    e.append(Paragraph(name.upper(), NM))
    e.append(Paragraph(bd_str, DT))
    for k in ["life_path", "expression", "soul_urge", "personality", "destiny"]:
        v = data[k]
        nm, pos, neg, licao = get_sig(v, lang)
        e.append(Paragraph(f"<b>{t(k, lang)} {v} — {nm}</b>", SEC))
        e.append(Paragraph(f"<b>{t('positivo', lang)}:</b> {pos}", TXT))
        e.append(Paragraph(f"<b>{t('negativo', lang)}:</b> {neg}", TXT))
        e.append(Paragraph(f"<b>{t('licao', lang)}:</b> {licao}", TXT))
    e.append(Paragraph("© A1ELOS Assessoria e Consultoria", est("FF", 9, False, GRAY, TA_CENTER, ES, 0)))
    doc.build(e)
    return path

def pdf17(data, name, bd_str, lang="pt"):
    path = f"/tmp/p17_{uuid.uuid4().hex[:8]}.pdf"
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=50, rightMargin=50, topMargin=45, bottomMargin=45)
    e = []
    lp = data["life_path"]
    kw, desc_cam = get_cam(lp, lang)
    nome_p = name.split()[0] if " " in name else name
    TIT = est("TI", TAM_T, True, GOLD, TA_CENTER, 0, ET)
    NM = est("NM", TAM_C + 2, True, DARK, TA_CENTER, 0, 4)
    DT = est("DT", TAM_C - 2, False, GRAY, TA_CENTER, 0, ES)
    SEC = est("SE", TAM_S, True, GOLD, TA_LEFT, ES, ET)
    JUST = est("J", TAM_C, False, DARK, TA_JUSTIFY, 0, ES * 0.5)
    JUST_P = est("JP", TAM_C - 1, False, DARK, TA_JUSTIFY, 0, ES * 0.4)
    BOLD = est("BL", TAM_C - 1, True, DARK, TA_LEFT, 0, ES * 0.2)
    e.append(Spacer(1, 25))
    e.append(Paragraph(t("completo", lang), TIT))
    e.append(Paragraph(name.upper(), NM))
    e.append(Paragraph(bd_str, DT))
    td = [
        [t("numero", lang), t("valor", lang), t("significado", lang)],
        [t("caminho_vida", lang), str(lp), get_sig(lp, lang)[0]],
        [t("expressao", lang), str(data["expression"]), get_sig(data["expression"], lang)[0]],
        [t("motivacao", lang), str(data["soul_urge"]), get_sig(data["soul_urge"], lang)[0]],
        [t("personalidade", lang), str(data["personality"]), get_sig(data["personality"], lang)[0]],
        [t("destino", lang), str(data["destiny"]), get_sig(data["destiny"], lang)[0]],
    ]
    tbl = Table(td, colWidths=[125, 40, 280])
    tbl.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), GOLD),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 1), (-1, -1), 9),
            ("TEXTCOLOR", (0, 1), (-1, -1), DARK),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ])
    )
    e.append(tbl)
    e.append(PageBreak())
    e.append(Paragraph(f"<b>{t('analise', lang)}</b>", SEC))
    for k, lbl in [
        ("life_path", t("caminho_vida", lang)),
        ("expression", t("expressao", lang)),
        ("soul_urge", t("motivacao", lang)),
        ("personality", t("personalidade", lang)),
        ("destiny", t("destino", lang)),
    ]:
        v = data[k]
        nm, pos, neg, licao = get_sig(v, lang)
        e.append(Paragraph(f"<b>{lbl} {v} — {nm}</b>", BOLD))
        e.append(Paragraph(f"{pos}", JUST_P))
        e.append(Paragraph(f"<b>{t('negativo', lang)}:</b> {neg}", JUST_P))
        e.append(Paragraph(f"<b>{t('licao', lang)}:</b> {licao}", JUST_P))
    fe = max(36 - min(lp, 36), 25)
    c1n = r1(lp + data["expression"])
    c2n = r1(data["expression"] + data["soul_urge"])
    c3n = r1(data["soul_urge"] + data["personality"])
    e.append(Paragraph(f"<b>{t('ciclos', lang)}</b>", SEC))
    e.append(Paragraph(f"<b>1º {t('formativo', lang)} (0-{fe}a) {t('regente', lang)} {c1n}</b>", JUST_P))
    e.append(Paragraph(f"<b>2º {t('produtivo', lang)} ({fe+1}-{fe+27}a) {t('regente', lang)} {c2n}</b>", JUST_P))
    e.append(Paragraph(f"<b>3º {t('colheita', lang)} ({fe+28}+a) {t('regente', lang)} {c3n}</b>", JUST_P))
    e.append(PageBreak())
    bb = dp.parse(bd_str.split(" ")[0] if " " in bd_str else bd_str).date()
    d, m, aa = bb.day, bb.month, bb.year
    d1 = r1(abs(d - m))
    d2 = r1(abs(m - r1(aa)))
    dp_ = r1(abs(d1 - d2))
    e.append(Paragraph(f"<b>{t('desafios', lang)}</b>", SEC))
    e.append(Paragraph(f"<b>{t('menor1', lang)} {d1}:</b> {get_des(d1, lang)}", JUST_P))
    e.append(Paragraph(f"<b>{t('menor2', lang)} {d2}:</b> {get_des(d2, lang)}", JUST_P))
    e.append(Paragraph(f"<b>{t('principal', lang)} {dp_}:</b> {get_des(dp_, lang)}", JUST_P))
    r1v = r1(d + m)
    r2v = r1(d + aa)
    r3v = r1(r1v + r2v)
    r4v = r1(d + m + aa)
    e.append(Paragraph(f"<b>{t('realizacoes', lang)}</b>", SEC))
    e.append(Paragraph(f"<b>1ª ({r1v}) {t('juventude', lang)}</b>", JUST_P))
    e.append(Paragraph(f"<b>2ª ({r2v}) {t('vida_adulta', lang)}</b>", JUST_P))
    e.append(Paragraph(f"<b>3ª ({r3v}) {t('maturidade', lang)}</b>", JUST_P))
    e.append(Paragraph(f"<b>4ª ({r4v}) {t('legado', lang)}</b>", JUST_P))
    vib = r1(d)
    e.append(Paragraph(f"<b>{t('vibracao', lang)}</b>", SEC))
    e.append(Paragraph(f"{get_vib(vib, lang)}", JUST))
    e.append(Paragraph(f"<b>{t('grade', lang)}</b>", SEC))
    grid = calc_grid(name)
    presentes = [str(n) for n in range(1, 10) if grid.get(n, 0) > 0]
    ausentes = [str(n) for n in range(1, 10) if grid.get(n, 0) == 0]
    e.append(Paragraph(
        f"<b>{t('presentes', lang)}:</b> {', '.join(presentes) or t('nenhum', lang)}. "
        f"<b>{t('carencias', lang)}:</b> {', '.join(ausentes) or t('nenhum', lang)}.", JUST
    ))
    if ausentes:
        nomes_aus = [f"{n} ({get_sig(int(n), lang)[0]})" for n in ausentes]
        e.append(Paragraph(f"{t('carencias', lang)} ({', '.join(nomes_aus)}) — qualidades a desenvolver.", JUST))
    e.append(Paragraph(f"<b>{t('nota_final', lang)}</b>", SEC))
    e.append(Paragraph(
        f"{nome_p}, seu mapa revela {t('caminho_vida', lang).lower()} {lp}. "
        f"A numerologia ilumina caminhos, mas o livre arbítrio é sempre seu maior poder.", JUST
    ))
    e.append(Paragraph("© A1ELOS Assessoria e Consultoria", est("FF", 9, False, GRAY, TA_CENTER, ES, 0)))
    doc.build(e)
    return path

def pagina_sucesso(pdf_path, nome, prod_nome, lang="pt"):
    b64 = ""
    if pdf_path and os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
    btn = ""
    if b64:
        nome_arq = prod_nome.replace(" ", "_")
        btn = (
            f'<a href="data:application/pdf;base64,{b64}" download="{nome_arq}.pdf" '
            f'style="display:inline-block;padding:18px 50px;background:#C9A94E;color:#000;'
            f'text-decoration:none;border-radius:50px;font-weight:700;font-size:1.2rem;'
            f'margin:25px 0">📥 {t("download", lang)}</a>'
        )
    return (
        f'<!DOCTYPE html><html lang="{lang}"><head><meta charset="UTF-8">'
        f'<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{t("confirmado", lang)}</title><style>'
        f'*{{margin:0;padding:0;box-sizing:border-box}}'
        f'body{{font-family:system-ui,sans-serif;background:#0a0a0a;color:#fff;'
        f'display:flex;align-items:center;justify-content:center;min-height:100vh;padding:2rem}}'
        f'.card{{background:#111;border:1px solid #222;border-radius:16px;padding:3rem;'
        f'max-width:520px;text-align:center}}'
        f'h1{{color:#C9A94E;font-size:1.6rem;margin-bottom:0.5rem}}'
        f'p{{color:#999;line-height:1.7;font-size:1rem;margin:0.5rem 0}}'
        f'</style></head><body><div class="card">'
        f'<div style="font-size:3rem;margin-bottom:1rem">✨</div>'
        f'<h1>{t("confirmado", lang)}</h1>'
        f'<p>{nome}, {t("gerado", lang)}</p>'
        f'<p><strong>{prod_nome}</strong></p>{btn}'
        f'<p><a href="/" style="color:#888">{t("voltar", lang)}</a></p></div></body></html>'
    )

# ---- ROTAS ----

@app.get("/", response_class=HTMLResponse)
def root():
    try:
        p = os.path.join(os.path.dirname(__file__), "index.html")
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                return HTMLResponse(f.read())
    except:
        pass
    return HTMLResponse("<h1>API ativa</h1>")

@app.get("/api/health")
def health():
    return {"status": "ok", "stripe": bool(STRIPE_KEY)}

@app.post("/calculate")
def calculate(req: PayReq):
    db = Session()
    try:
        if len(req.name.strip()) < 2:
            raise HTTPException(400, "Nome curto")
        if not req.birth_date:
            raise HTTPException(400, "Data obrigatória")
        res = calc(req.name, req.birth_date)
        cid = uuid.uuid4().hex[:8]
        db.add(Calc(id=cid, name=req.name, birth_date=req.birth_date, email=req.email or "", **res))
        db.commit()
        return {"id": cid, **res}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Calc: {e}")
        raise HTTPException(500, "Erro")
    finally:
        db.close()

@app.post("/api/pay/stripe")
def pay_stripe(req: PayReq):
    if not STRIPE_KEY:
        raise HTTPException(503, "Stripe não configurado")
    if not req.price or req.price <= 0:
        raise HTTPException(400, "Preço inválido")
    if req.payment_method == "boleto" and not req.email:
        raise HTTPException(400, "Email obrigatório para boleto")
    try:
        amt = int(float(req.price) * 100)
        if req.payment_method == "boleto":
            pm_types = ["boleto"]
            pm_options = {"boleto": {"expires_after_days": 3}}
        else:
            pm_types = ["card"]
            pm_options = {"card": {"installments": {"enabled": True}}}
        cs = stripe.checkout.Session.create(
            mode="payment",
            payment_method_types=pm_types,
            line_items=[{
                "price_data": {
                    "currency": "brl",
                    "product_data": {"name": f"Mapa-{req.product}"},
                    "unit_amount": amt,
                },
                "quantity": 1,
            }],
            customer_email=req.email or None,
            metadata={
                "product": req.product, "name": req.name,
                "birth_date": req.birth_date or "", "lang": req.lang or "pt",
                "payment_method": req.payment_method,
            },
            success_url=f"{BASE_URL}/api/pay/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{BASE_URL}/api/pay/cancel",
            payment_method_options=pm_options,
        )
        if req.payment_method == "boleto":
            db = Session()
            try:
                db.add(Payment(
                    id=cs.id, name=req.name, email=req.email or "",
                    birth_date=req.birth_date or "", product=req.product,
                    lang=req.lang or "pt", status="pending", payment_method="boleto",
                ))
                db.commit()
            except Exception as e:
                logger.error(f"DB boleto: {e}")
            finally:
                db.close()
        return {"payment_url": cs.url, "id": cs.id}
    except Exception as e:
        logger.error(f"Stripe: {e}")
        raise HTTPException(500, "Erro ao criar pagamento")

@app.get("/api/pay/success")
def pay_success(request: Request):
    sid = request.query_params.get("session_id", "")
    if not sid:
        return HTMLResponse("<h1>Sessão inválida</h1>")
    try:
        s = stripe.checkout.Session.retrieve(sid)
        meta = getattr(s, "metadata", {}) or {}
        if hasattr(meta, "to_dict"):
            meta = meta.to_dict()
        name = meta.get("name", "Cliente")
        bd = meta.get("birth_date", "")
        prod = meta.get("product", "pdf8")
        lang = meta.get("lang", "pt")
        pm = meta.get("payment_method", "card")
        email = getattr(s, "customer_details", None)
        email_val = getattr(email, "email", "") if email else ""
        if pm == "boleto":
            html = f"""<!DOCTYPE html><html lang="pt"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Boleto Gerado</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:system-ui,sans-serif;background:#0a0a0a;color:#fff;display:flex;align-items:center;justify-content:center;min-height:100vh;padding:2rem}}
.card{{background:#111;border:1px solid #222;border-radius:16px;padding:3rem;max-width:520px;text-align:center}}
h1{{color:#C9A94E;font-size:1.6rem;margin-bottom:0.5rem}}
p{{color:#999;line-height:1.7;font-size:1rem;margin:0.5rem 0}}
.email{{color:#C9A94E;font-weight:600}}
.btn{{display:inline-block;margin-top:1.5rem;padding:14px 36px;background:#C9A94E;color:#000;text-decoration:none;border-radius:50px;font-weight:600}}
</style></head><body><div class="card">
<div style="font-size:3rem;margin-bottom:1rem">📄</div>
<h1>Boleto Gerado!</h1>
<p>Seu boleto foi emitido. Após a confirmação do pagamento (em até <strong>3 dias úteis</strong>), enviaremos o link do seu PDF para:</p>
<p class="email">{email_val}</p>
<a href="/" class="btn">Voltar ao Início</a>
</div></body></html>"""
            return HTMLResponse(html)
        if not bd:
            bd = "2000-01-01"
    except Exception as e:
        logger.error(f"Erro: {e}")
        return HTMLResponse("<h1>Falha no pagamento</h1>")
    try:
        data = calc(name, bd)
        if prod == "pdf17":
            pf = pdf17(data, name, bd, lang)
            pn = "Mapa Completo"
        else:
            pf = pdf8(data, name, bd, lang)
            pn = "Mapa Express"
        html = pagina_sucesso(pf, name, pn, lang)
        if pf and os.path.exists(pf):
            os.remove(pf)
        return HTMLResponse(html)
    except Exception as e:
        logger.error(f"Erro PDF: {e}")
        return HTMLResponse("<h1>Erro ao gerar PDF</h1>")

@app.get("/api/pay/cancel")
def pay_cancel():
    return HTMLResponse("<h1>Cancelado</h1><p><a href='/'>Voltar</a></p>")

@app.post("/api/pay/stripe/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")
    if STRIPE_WEBHOOK_SECRET:
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
        except stripe.error.SignatureVerificationError:
            return {"error": "Invalid signature"}
    else:
        try:
            event = json.loads(payload)
        except:
            return {"error": "Invalid payload"}
    event_type = event.get("type") if isinstance(event, dict) else event.type
    session = event["data"]["object"] if isinstance(event, dict) else event.data.object
    session_id = session.get("id") if isinstance(session, dict) else session.id
    if event_type == "checkout.session.async_payment_succeeded":
        meta = session.get("metadata", {}) if isinstance(session, dict) else getattr(session, "metadata", {}) or {}
        if hasattr(meta, "to_dict"):
            meta = meta.to_dict()
        if meta.get("payment_method") == "boleto":
            await _process_boleto_confirm(session_id, meta)
    return {"status": "ok"}

async def _process_boleto_confirm(session_id: str, meta: dict):
    db = Session()
    try:
        payment = db.query(Payment).filter(Payment.id == session_id).first()
        if not payment or payment.status == "completed":
            return
        name = payment.name
        bd = payment.birth_date
        prod = payment.product
        lang = payment.lang
        email = payment.email
        if not bd:
            bd = "2000-01-01"
        data = calc(name, bd)
        if prod == "pdf17":
            pdf_path = pdf17(data, name, bd, lang)
            prod_name = "Mapa Completo"
        else:
            pdf_path = pdf8(data, name, bd, lang)
            prod_name = "Mapa Express"
        if not pdf_path or not os.path.exists(pdf_path):
            logger.error(f"PDF falhou: {session_id}")
            return
        token = secrets.token_hex(24)
        payment.status = "completed"
        payment.download_token = token
        payment.completed_at = datetime.utcnow()
        db.commit()
        _send_email_boleto(email, name, prod_name, token, lang)
        os.remove(pdf_path)
        logger.info(f"Boleto OK: {session_id} -> {email}")
    except Exception as e:
        logger.error(f"Process boleto: {e}")
    finally:
        db.close()

def _send_email_boleto(to_email, name, prod_name, token, lang="pt"):
    smtp_pw = os.getenv("SMTP_PASSWORD", "")
    from_email = os.getenv("FROM_EMAIL", "")
    if not smtp_pw or not from_email:
        logger.warning(f"SMTP ausente — link: {BASE_URL}/api/pay/download/{token}")
        return
    dl = f"{BASE_URL}/api/pay/download/{token}"
    if lang == "pt":
        subj = f"Seu {prod_name} está pronto!"
        body = f"""Olá {name},

O pagamento do seu {prod_name} foi confirmado!
Seu mapa numerológico está disponível no link abaixo:

{dl}

Este link é exclusivo e válido por 30 dias.

Que os números iluminem seu caminho!
Equipe Mapa Numerológico"""
    else:
        subj = f"Your {prod_name} is ready!"
        body = f"""Hello {name},

Your {prod_name} payment has been confirmed!
Download your numerology map at:

{dl}

This link is exclusive and valid for 30 days.

Best regards,
Numerological Map Team"""
    try:
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subj
        msg.attach(MIMEText(body, "plain", "utf-8"))
        with smtplib.SMTP("smtp.gmail.com", 587) as s:
            s.starttls()
            s.login(from_email, smtp_pw)
            s.send_message(msg)
        logger.info(f"Email enviado para {to_email}")
    except Exception as e:
        logger.error(f"Email erro: {e}")

@app.get("/api/pay/download/{token}")
def pay_download(token: str):
    db = Session()
    try:
        payment = db.query(Payment).filter(
            Payment.download_token == token,
            Payment.status == "completed",
        ).first()
        if not payment:
            return HTMLResponse("<h1>Link inválido ou expirado</h1>")
        data = calc(payment.name, payment.birth_date)
        if payment.product == "pdf17":
            pdf_path = pdf17(data, payment.name, payment.birth_date, payment.lang)
            fname = "Mapa_Completo"
        else:
            pdf_path = pdf8(data, payment.name, payment.birth_date, payment.lang)
            fname = "Mapa_Express"
        if not pdf_path or not os.path.exists(pdf_path):
            return HTMLResponse("<h1>Erro ao gerar PDF</h1>")
        with open(pdf_path, "rb") as f:
            content = f.read()
        os.remove(pdf_path)
        return Response(
            content=content,
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{fname}.pdf"'},
        )
    except Exception as e:
        logger.error(f"Download: {e}")
        return HTMLResponse("<h1>Erro no download</h1>")
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "10000"))
    uvicorn.run(app, host="0.0.0.0", port=port)