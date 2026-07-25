# -*- coding: utf-8 -*-
import os, uuid, stripe, logging, traceback, json, smtplib, secrets
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
STRIPE_KEY = os.getenv("STRIPE_SECRET_KEY", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", "arvigne@gmail.com")
SMTP_PASS = os.getenv("SMTP_PASSWORD", "")
BASE_URL = os.getenv("BASE_URL", "https://global-numerology.onrender.com")
DB_URL = os.getenv("DATABASE_URL", "sqlite:///./numerologia.db")
if STRIPE_KEY:
    stripe.api_key = STRIPE_KEY

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Payment(Base):
    __tablename__ = "payments"
    id = Column(String, primary_key=True)
    name = Column(String, default="")
    email = Column(String, default="")
    birth_date = Column(String, default="")
    product = Column(String, default="pdf8")
    lang = Column(String, default="pt")
    status = Column(String, default="pending")
    payment_method = Column(String, default="card")
    download_token = Column(String, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

try:
    from fastapi.staticfiles import StaticFiles
    static_dir = os.path.join(os.path.dirname(__file__), ".")
    if os.path.exists(os.path.join(static_dir, "Logo.png")):
        app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
except Exception:
    pass

TABELA = {c: (i % 9 or 9) for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 1)}

def reduzir(n, permitir_mestre=True):
    while n > 9:
        if permitir_mestre and n in (11, 22, 33):
            return n
        n = sum(int(d) for d in str(n))
    return n

def calc_mapa(nome, data_str):
    import dateutil.parser as dp
    bd = dp.parse(data_str).date()
    lp = reduzir(bd.day + bd.month + bd.year)
    nu = nome.upper().replace(" ", "")
    total_e = total_v = total_p = 0
    for ch in nu:
        val = TABELA.get(ch, 0)
        total_e += val
        if ch in "AEIOU":
            total_v += val
        else:
            total_p += val
    return {"life_path": lp, "expression": reduzir(total_e), "soul_urge": reduzir(total_v), "personality": reduzir(total_p), "destiny": reduzir(reduzir(total_e) + lp)}

class PayReq(BaseModel):
    name: str
    email: str = ""
    product: Optional[str] = "pdf8"
    price: Optional[float] = 0
    birth_date: Optional[str] = None
    lang: Optional[str] = "pt"
    payment_method: Optional[str] = "card"

def send_email(to, subject, body, pdf_path=None):
    if not SMTP_PASS or not FROM_EMAIL:
        return False
    try:
        msg = MIMEMultipart()
        msg["From"] = FROM_EMAIL
        msg["To"] = to
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain", "utf-8"))
        if pdf_path and os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", "attachment", filename="Documento_A1ELOS.pdf")
            msg.attach(part)
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(FROM_EMAIL, SMTP_PASS)
            server.send_message(msg)
        return True
    except Exception as e:
        logger.error(f"Falha email: {e}")
        return False

@app.get("/", response_class=HTMLResponse)
def root():
    try:
        p = os.path.join(os.path.dirname(__file__), "index.html")
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                return HTMLResponse(f.read())
    except Exception:
        pass
    return HTMLResponse("<h1>Global Numerology API ativa</h1>")

@app.get("/api/health")
def health():
    return {"status": "ok", "stripe": bool(STRIPE_KEY)}

@app.post("/calculate")
def calculate(req: PayReq):
    if len(req.name.strip()) < 2:
        raise HTTPException(400, "Nome curto")
    if not req.birth_date:
        raise HTTPException(400, "Data obrigatoria")
    try:
        res = calc_mapa(req.name, req.birth_date)
        cid = uuid.uuid4().hex[:8]
        if req.email and req.email.strip():
            try:
                from reportlab.lib.pagesizes import A4
                from reportlab.lib import colors
                from reportlab.lib.enums import TA_CENTER, TA_LEFT
                from reportlab.lib.styles import ParagraphStyle
                from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
                GOLD = colors.HexColor("#B8860B")
                LGRAY = colors.HexColor("#f0f0f0")
                DARK = colors.HexColor("#222")
                GRAY = colors.HexColor("#888")
                def est(n, f, s, c, a, sb=0, sa=0):
                    return ParagraphStyle(n, fontName=f, fontSize=s, textColor=c, alignment=a, spaceBefore=sb, spaceAfter=sa, leading=s*1.5)
                pf = f"/tmp/p8_{uuid.uuid4().hex[:8]}.pdf"
                doc = SimpleDocTemplate(pf, pagesize=A4, leftMargin=50, rightMargin=50, topMargin=45, bottomMargin=45)
                el = []
                el.append(Spacer(1, 30))
                el.append(Paragraph("MAPA NUMEROLOGICO", est("T", "Helvetica-Bold", 20, GOLD, TA_CENTER, sa=40)))
                el.append(Paragraph(req.name.upper(), est("N", "Helvetica-Bold", 16, DARK, TA_CENTER, sa=4)))
                el.append(Paragraph(req.birth_date, est("D", "Helvetica", 12, GRAY, TA_CENTER, sa=20)))
                td = [["Numero", "Valor"], ["Caminho de Vida", str(res["life_path"])], ["Expressao", str(res["expression"])], ["Motivacao", str(res["soul_urge"])], ["Personalidade", str(res["personality"])], ["Destino", str(res["destiny"])]]
                tbl = Table(td, colWidths=[200, 150])
                tbl.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), GOLD), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("FONTSIZE", (0, 0), (-1, -1), 12), ("GRID", (0, 0), (-1, -1), 0.5, colors.grey), ("ALIGN", (1, 0), (1, -1), "CENTER"), ("BACKGROUND", (0, 1), (-1, -1), LGRAY)]))
                el.append(tbl)
                el.append(Paragraph("Copyright A1ELOS", est("F", "Helvetica", 10, GRAY, TA_CENTER, sb=40)))
                doc.build(el)
                send_email(req.email.strip(), "Seu Mapa Express!", f"Ola {req.name},\n\nSeu mapa foi gerado.\n\nA1ELOS", pf)
                if os.path.exists(pf):
                    os.remove(pf)
            except Exception as e:
                logger.error(f"Falha email gratis: {e}")
        return {"id": cid, **res}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Calc: {e}")
        raise HTTPException(500, "Erro no calculo")

@app.post("/api/pay/stripe")
def pay_stripe(req: PayReq):
    if not STRIPE_KEY:
        raise HTTPException(503, "Stripe nao configurado")
    if not req.price or req.price <= 0:
        raise HTTPException(400, "Preco invalido")
    try:
        amt = int(float(req.price) * 100)
        pm_types = ["boleto"] if req.payment_method == "boleto" else ["card"]
        pm_options = {"boleto": {"expires_after_days": 3}} if req.payment_method == "boleto" else {"card": {"installments": {"enabled": True}}}
        cs = stripe.checkout.Session.create(mode="payment", payment_method_types=pm_types, line_items=[{"price_data": {"currency": "brl", "product_data": {"name": f"Mapa-{req.product}"}, "unit_amount": amt}, "quantity": 1}], customer_email=req.email or None, metadata={"product": req.product, "name": req.name, "birth_date": req.birth_date or "", "lang": req.lang or "pt", "payment_method": req.payment_method}, success_url=f"{BASE_URL}/api/pay/success?session_id={CHECKOUT_SESSION_ID}", cancel_url=f"{BASE_URL}/api/pay/cancel", payment_method_options=pm_options)
        return {"payment_url": cs.url, "id": cs.id}
    except Exception as e:
        logger.error(f"Stripe: {e}")
        raise HTTPException(500, "Erro ao criar pagamento")

@app.get("/api/pay/success")
def pay_success(request: Request):
    sid = request.query_params.get("session_id", "")
    if not sid:
        return HTMLResponse("<h1>Sessao invalida</h1>")
    try:
        s = stripe.checkout.Session.retrieve(sid)
        meta = getattr(s, "metadata", {}) or {}
        if hasattr(meta, "to_dict"):
            meta = meta.to_dict()
        name = meta.get("name", "Cliente")
        bd = meta.get("birth_date", "2000-01-01")
        prod = meta.get("product", "pdf8")
        email = getattr(s, "customer_details", None)
        email_val = getattr(email, "email", "") if email else ""
        data = calc_mapa(name, bd)
        html = f"<html><body style='background:#0a0a0a;color:#fff;font-family:sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh'><div style='text-align:center'><h1 style='color:#C9A94E'>OK Confirmado!</h1><p>Documento enviado para {email_val}</p><a href='/' style='display:inline-block;padding:12px 30px;background:#C9A94E;color:#000;text-decoration:none;border-radius:50px'>Voltar</a></div></body></html>"
        return HTMLResponse(html)
    except Exception as e:
        logger.error(f"Erro: {e}")
        return HTMLResponse(f"<h1>Falha: {e}</h1>")

@app.get("/api/pay/cancel")
def pay_cancel():
    return HTMLResponse("<h1>Cancelado</h1><p><a href='/'>Voltar</a></p>")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "10000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
