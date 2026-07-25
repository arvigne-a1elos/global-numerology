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

def validar_nomes_urna(nomes, cargo_key):
    labels = {"vereador": "Vereador", "dep_estadual": "Dep. Estadual", "dep_federal": "Dep. Federal", "senador": "Senador"}
    results = []
    for nome in nomes:
        if not nome.strip():
            continue
        en, st = calc_nome(nome)
        results.append({"nome": nome.strip().title(), "energia": en, "soma": st, "eh_ideal": en == 8, "explicacao": f"Nome {nome.strip().title()} tem energia {en}. {'Ideal!' if en == 8 else 'O 8 e o ideal.'}"})
    ideal = any(r["eh_ideal"] for r in results)
    sugs = []
    if not ideal:
        prefixo = labels.get(cargo_key, "")[:3]
        for nome in nomes:
            if not nome.strip():
                continue
            for tentativa in [f"{prefixo} {nome.strip()}", f"{nome.strip()} - {prefixo.lower()[:3]}"]:
                en, _ = calc_nome(tentativa)
                sugs.append({"nome": tentativa.title(), "energia": en, "eh_ideal": en == 8})
                if len(sugs) >= 3:
                    break
            if len(sugs) >= 3:
                break
    return results, ideal, sugs[:3]

def gerar_numeros(sigla, cargo, qtd=5):
    digitos = {"vereador": 5, "dep_estadual": 5, "dep_federal": 4, "senador": 3}
    td = digitos.get(cargo, 5)
    ss = str(sigla).zfill(2)[:2]
    sm = int(ss[0]) + int(ss[1])
    lv = td - 2
    res = []
    tent = set()
    energias = {8: "Poder e Prosperidade (IDEAL)", 7: "Sabedoria", 3: "Criacao", 1: "Lideranca", 9: "Humanitarismo", 5: "Liberdade", 6: "Familia", 4: "Trabalho", 2: "Associacao"}
    def busca(alvo):
        enc = []
        for x in range(10 ** lv):
            if len(enc) + len(res) >= qtd:
                break
            dl = str(x).zfill(lv)
            en = reduzir(sm + sum(int(d) for d in dl))
            if en == alvo:
                n = ss + dl
                if n not in tent:
                    tent.add(n)
                    enc.append({"numero": n, "energia": alvo, "ideal": alvo == 8, "sigla": ss, "digitos_livres": dl, "nome_energia": energias.get(alvo, ""), "explicacao_calculo": f"Sigla {ss} ({ss[0]}+{ss[1]}={sm}) + digitos {dl} = {en}"})
        return enc
    res.extend(busca(8))
    for e in [3, 7, 1, 9, 5, 6, 4, 2]:
        if len(res) >= qtd:
            break
        res.extend(busca(e))
    return res[:qtd]

class PayReq(BaseModel):
    name: str
    email: str = ""
    product: Optional[str] = "pdf8"
    price: Optional[float] = 0
    birth_date: Optional[str] = None
    lang: Optional[str] = "pt"
    payment_method: Optional[str] = "card"

class UrnaPayReq(BaseModel):
    nome_completo: str
    cargo: str
    nome1: str
    nome2: str = ""
    nome3: str = ""
    nome4: str = ""
    nome5: str = ""
    email: str

class EleitoralPayReq(BaseModel):
    sigla: int
    cargo: str
    numero_existente: Optional[str] = ""
    email: str

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
                pf = f"/tmp/pdf_{uuid.uuid4().hex[:8]}.pdf"
                from reportlab.lib.pagesizes import A4
                from reportlab.lib import colors
                from reportlab.lib.enums import TA_CENTER, TA_LEFT
                from reportlab.lib.styles import ParagraphStyle
                from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
                G = colors.HexColor("#B8860B")
                L = colors.HexColor("#f0f0f0")
                D = colors.HexColor("#222")
                def es(n, f, s, c, a, sb=0, sa=0):
                    return ParagraphStyle(n, fontName=f, fontSize=s, textColor=c, alignment=a, spaceBefore=sb, spaceAfter=sa, leading=s*1.5)
                doc = SimpleDocTemplate(pf, pagesize=A4, leftMargin=50, rightMargin=50, topMargin=45, bottomMargin=45)
                el = []
                el.append(Spacer(1, 30))
                el.append(Paragraph("MAPA NUMEROLOGICO", es("T", "Helvetica-Bold", 20, G, TA_CENTER, sa=40)))
                el.append(Paragraph(req.name.upper(), es("N", "Helvetica-Bold", 16, D, TA_CENTER, sa=4)))
                el.append(Paragraph(req.birth_date, es("D", "Helvetica", 12, colors.HexColor("#888"), TA_CENTER, sa=20)))
                td = [["Numero", "Valor"], ["Caminho de Vida", str(res["life_path"])], ["Expressao", str(res["expression"])], ["Motivacao", str(res["soul_urge"])], ["Personalidade", str(res["personality"])], ["Destino", str(res["destiny"])]]
                tbl = Table(td, colWidths=[200, 150])
                tbl.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), G), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("FONTSIZE", (0, 0), (-1, -1), 12), ("GRID", (0, 0), (-1, -1), 0.5, colors.grey), ("ALIGN", (1, 0), (1, -1), "CENTER"), ("BACKGROUND", (0, 1), (-1, -1), L)]))
                el.append(tbl)
                el.append(Paragraph("Copyright A1ELOS", es("F", "Helvetica", 10, colors.HexColor("#888"), TA_CENTER, sb=40)))
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
        cs = stripe.checkout.Session.create(
            mode="payment", payment_method_types=pm_types,
            line_items=[{"price_data": {"currency": "brl", "product_data": {"name": f"Mapa-{req.product}"}, "unit_amount": amt}, "quantity": 1}],
            customer_email=req.email or None,
            metadata={"product": req.product, "name": req.name, "birth_date": req.birth_date or "", "lang": req.lang or "pt", "payment_method": req.payment_method},
            success_url=f"{BASE_URL}/api/pay/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{BASE_URL}/api/pay/cancel",
            payment_method_options=pm_options)
        if req.payment_method == "boleto":
            try:
                db = SessionLocal()
                db.add(Payment(id=cs.id, name=req.name, email=req.email or "", birth_date=req.birth_date or "", product=req.product, lang=req.lang or "pt", status="pending", payment_method="boleto"))
                db.commit()
                db.close()
            except Exception as e:
                logger.error(f"DB boleto: {e}")
        return {"payment_url": cs.url, "id": cs.id}
    except Exception as e:
        logger.error(f"Stripe: {e}")
        raise HTTPException(500, "Erro ao criar pagamento")

OK_HTML = "<html><body style='background:#0a0a0a;color:#fff;font-family:sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh'><div style='text-align:center'><h1 style='color:#C9A94E'>OK Confirmado!</h1><p>Documento enviado para seu email.</p><p>Verifique o spam.</p><a href='/' style='display:inline-block;padding:12px 30px;background:#C9A94E;color:#000;text-decoration:none;border-radius:50px'>Voltar</a></div></body></html>"
ERR_HTML = "<html><body style='background:#0a0a0a;color:#fff;font-family:sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh'><div style='text-align:center'><h1 style='color:#e74c3c'>{msg}</h1><a href='/' style='display:inline-block;padding:12px 30px;background:#C9A94E;color:#000;text-decoration:none;border-radius:50px'>Voltar</a></div></body></html>"
CANCEL_HTML = "<html><body style='background:#0a0a0a;color:#fff;font-family:sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh'><div style='text-align:center'><h1 style='color:#e67e22'>Cancelado</h1><a href='/' style='display:inline-block;padding:12px 30px;background:#C9A94E;color:#000;text-decoration:none;border-radius:50px'>Voltar</a></div></body></html>"

@app.get("/api/pay/success")
def pay_success(request: Request):
    sid = request.query_params.get("session_id", "")
    if not sid:
        return HTMLResponse(ERR_HTML.format(msg="Sessao invalida"))
    try:
        s = stripe.checkout.Session.retrieve(sid)
        meta = getattr(s, "metadata", {}) or {}
        if hasattr(meta, "to_dict"):
            meta = meta.to_dict()
        name = meta.get("name", "Cliente")
        bd = meta.get("birth_date", "2000-01-01")
        prod = meta.get("product", "pdf8")
        pm = meta.get("payment_method", "card")
        email = getattr(s, "customer_details", None)
        email_val = getattr(email, "email", "") if email else ""
        if pm == "boleto":
            return HTMLResponse(f"<html><body style='background:#0a0a0a;color:#fff;font-family:sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh'><div style='text-align:center'><h1 style='color:#C9A94E'>Boleto Gerado!</h1><p>Pagamento via boleto. Assim que confirmado, enviaremos para {email_val}.</p><a href='/' style='display:inline-block;padding:12px 30px;background:#C9A94E;color:#000;text-decoration:none;border-radius:50px'>Voltar</a></div></body></html>")
    except Exception as e:
        logger.error(f"Erro: {e}")
        return HTMLResponse(ERR_HTML.format(msg="Falha no pagamento"))
    try:
        data = calc_mapa(name, bd)
        pf = f"/tmp/pdf_{uuid.uuid4().hex[:8]}.pdf"
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
        doc = SimpleDocTemplate(pf, pagesize=A4, leftMargin=50, rightMargin=50, topMargin=45, bottomMargin=45)
        el = []
        el.append(Spacer(1, 30))
        tit = "MAPA NUMEROLOGICO COMPLETO" if prod == "pdf17" else "MAPA NUMEROLOGICO EXPRESS"
        el.append(Paragraph(tit, es("T", "Helvetica-Bold", 20, G, TA_CENTER, sa=40)))
        el.append(Paragraph(name.upper(), es("N", "Helvetica-Bold", 16, D, TA_CENTER, sa=4)))
        el.append(Paragraph(bd, es("D", "Helvetica", 12, colors.HexColor("#888"), TA_CENTER, sa=20)))
        td = [["Numero", "Valor"], ["Caminho de Vida", str(data["life_path"])], ["Expressao", str(data["expression"])], ["Motivacao", str(data["soul_urge"])], ["Personalidade", str(data["personality"])], ["Destino", str(data["destiny"])]]
        tbl = Table(td, colWidths=[200, 150])
        tbl.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), G), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("FONTSIZE", (0, 0), (-1, -1), 12), ("GRID", (0, 0), (-1, -1), 0.5, colors.grey), ("ALIGN", (1, 0), (1, -1), "CENTER"), ("BACKGROUND", (0, 1), (-1, -1), L)]))
        el.append(tbl)
        el.append(Paragraph("Copyright A1ELOS", es("F", "Helvetica", 10, colors.HexColor("#888"), TA_CENTER, sb=40)))
        doc.build(el)
        sent = send_email(email_val, "Seu Mapa Numerologico!", f"Ola {name},\n\nDocumento anexo.\nVerifique o spam.\n\nA1ELOS", pf)
        if os.path.exists(pf):
            os.remove(pf)
        if sent:
            return HTMLResponse(OK_HTML)
        return HTMLResponse(ERR_HTML.format(msg="Pagamento OK, mas erro no envio do email"))
    except Exception as e:
        logger.error(f"ERRO: {e}")
        logger.error(traceback.format_exc())
        return HTMLResponse(ERR_HTML.format(msg="Erro ao gerar. Contate arvigne@gmail.com"))

@app.get("/api/pay/cancel")
def pay_cancel():
    return HTMLResponse(CANCEL_HTML)

@app.post("/api/pay/urna-session")
def pay_urna_session(req: UrnaPayReq):
    if not STRIPE_KEY:
        raise HTTPException(503, "Stripe nao configurado")
    if not req.email:
        raise HTTPException(400, "Email obrigatorio")
    nomes = [n.strip() for n in [req.nome1, req.nome2, req.nome3, req.nome4, req.nome5] if n.strip()]
    if not nomes:
        raise HTTPException(400, "Pelo menos 1 nome")
    meta = {"product": "urna26", "nome_completo": req.nome_completo, "cargo": req.cargo, "email": req.email}
    for i, n in enumerate(nomes, 1):
        meta[f"nome{i}"] = n
    cs = stripe.checkout.Session.create(mode="payment", payment_method_types=["card"], line_items=[{"price_data": {"currency": "brl", "product_data": {"name": "Validacao Nome"}, "unit_amount": 2600}, "quantity": 1}], customer_email=req.email, metadata=meta, success_url=f"{BASE_URL}/api/pay/urna-success?session_id={{CHECKOUT_SESSION_ID}}", cancel_url=f"{BASE_URL}/api/pay/cancel")
    return {"payment_url": cs.url, "id": cs.id}

@app.get("/api/pay/urna-success")
def pay_urna_success(request: Request):
    sid = request.query_params.get("session_id", "")
    if not sid:
        return HTMLResponse(ERR_HTML.format(msg="Sessao invalida"))
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
            return HTMLResponse(ERR_HTML.format(msg="Dados nao encontrados"))
        res, _, sugs = validar_nomes_urna(nomes, cr)
        labels = {"vereador": "Vereador", "dep_estadual": "Dep. Estadual", "dep_federal": "Dep. Federal", "senador": "Senador"}
        cl = labels.get(cr, cr)
        pf = f"/tmp/urna_{uuid.uuid4().hex[:8]}.pdf"
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        G = colors.HexColor("#B8860B")
        D = colors.HexColor("#222")
        def es(n, f, s, c, a, sb=0, sa=0):
            return ParagraphStyle(n, fontName=f, fontSize=s, textColor=c, alignment=a, spaceBefore=sb, spaceAfter=sa, leading=s*1.5)
        doc = SimpleDocTemplate(pf, pagesize=A4, leftMargin=50, rightMargin=50, topMargin=45, bottomMargin=45)
        el = []
        el.append(Spacer(1, 25))
        el.append(Paragraph("VALIDACAO DE NOME DE URNA", es("T", "Helvetica-Bold", 20, G, TA_CENTER, sa=20)))
        el.append(Paragraph(nc.title(), es("N", "Helvetica-Bold", 16, D, TA_CENTER, sa=4)))
        el.append(Paragraph(f"Cargo: {cl}", es("D", "Helvetica", 12, colors.HexColor("#888"), TA_CENTER, sa=20)))
        for r in res:
            el.append(Paragraph(f'<b>{r["nome"]}</b> - Energia {r["energia"]} - {r["explicacao"]}', es("J", "Helvetica", 12, D, TA_LEFT, sa=8)))
        if sugs:
            el.append(Paragraph("Sugestoes:", es("S", "Helvetica-Bold", 16, G, TA_LEFT, sb=20, sa=8)))
            for s in sugs[:3]:
                el.append(Paragraph(f'<b>{s["nome"]}</b> - Energia {s["energia"]}', es("X", "Helvetica", 12, D, TA_LEFT, sa=4)))
        el.append(Paragraph("Copyright A1ELOS", es("F", "Helvetica", 10, colors.HexColor("#888"), TA_CENTER, sb=40)))
        doc.build(el)
        send_email(em, "Validacao Nome - A1ELOS", f"Ola,\n\nPDF com validacao anexo.\nVerifique spam.\n\nA1ELOS", pf)
        if os.path.exists(pf):
            os.remove(pf)
        return HTMLResponse(OK_HTML)
    except Exception:
        logger.error(traceback.format_exc())
        return HTMLResponse(ERR_HTML.format(msg="Erro ao gerar. Contate arvigne@gmail.com"))

@app.post("/api/pay/eleitoral-session")
def pay_eleitoral_session(req: EleitoralPayReq):
    if not STRIPE_KEY:
        raise HTTPException(503, "Stripe nao configurado")
    if req.sigla < 10 or req.sigla > 99:
        raise HTTPException(400, "Sigla: 2 digitos")
    if req.cargo not in ["vereador", "dep_estadual", "dep_federal", "senador"]:
        raise HTTPException(400, "Cargo invalido")
    cs = stripe.checkout.Session.create(mode="payment", payment_method_types=["card"], line_items=[{"price_data": {"currency": "brl", "product_data": {"name": "Numero Eleitoral"}, "unit_amount": 2600}, "quantity": 1}], customer_email=req.email, metadata={"product": "eleitoral26", "sigla": str(req.sigla), "cargo": req.cargo, "email": req.email, "numero_existente": req.numero_existente or ""}, success_url=f"{BASE_URL}/api/pay/eleitoral-success?session_id={{CHECKOUT_SESSION_ID}}", cancel_url=f"{BASE_URL}/api/pay/cancel")
    return {"payment_url": cs.url, "id": cs.id}

@app.get("/api/pay/eleitoral-success")
def pay_eleitoral_success(request: Request):
    sid = request.query_params.get("session_id", "")
    if not sid:
        return HTMLResponse(ERR_HTML.format(msg="Sessao invalida"))
    try:
        s = stripe.checkout.Session.retrieve(sid)
        meta = getattr(s, "metadata", {}) or {}
        if hasattr(meta, "to_dict"):
            meta = meta.to_dict()
        sg = int(meta.get("sigla", "0"))
        cr = meta.get("cargo", "vereador")
        em = meta.get("email", "") or getattr(s, "customer_email", "")
        if not em:
            return HTMLResponse(ERR_HTML.format(msg="Email nao encontrado"))
        ss = str(sg).zfill(2)
        labels = {"vereador": "Vereador", "dep_estadual": "Dep. Estadual", "dep_federal": "Dep. Federal", "senador": "Senador"}
        cl = labels.get(cr, cr)
        sugs = gerar_numeros(sg, cr)
        ne_str = meta.get("numero_existente", "")
        ni = None
        if ne_str and len(ne_str) >= 3:
            try:
                en = reduzir(sum(int(d) for d in ne_str))
                ni = {"numero": ne_str, "energia": en}
            except Exception:
                pass
        pf = f"/tmp/eleit_{uuid.uuid4().hex[:8]}.pdf"
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        G = colors.HexColor("#B8860B")
        D = colors.HexColor("#222")
        def es(n, f, s, c, a, sb=0, sa=0):
            return ParagraphStyle(n, fontName=f, fontSize=s, textColor=c, alignment=a, spaceBefore=sb, spaceAfter=sa, leading=s*1.5)
        doc = SimpleDocTemplate(pf, pagesize=A4, leftMargin=50, rightMargin=50, topMargin=45, bottomMargin=45)
        el = []
        el.append(Spacer(1, 25))
        el.append(Paragraph("NUMERO ELEITORAL", es("T", "Helvetica-Bold", 20, G, TA_CENTER, sa=20)))
        el.append(Paragraph(f"Cargo: {cl} | Sigla: {ss}", es("D", "Helvetica", 12, colors.HexColor("#888"), TA_CENTER, sa=20)))
        el.append(Paragraph("<b>Por que a energia 8?</b>", es("SE", "Helvetica-Bold", 16, G, TA_LEFT, sb=20, sa=8)))
        el.append(Paragraph("O numero 8 representa Poder, Prosperidade e Realizacao material - vibracao ideal para candidatos politicos.", es("J", "Helvetica", 12, D, TA_LEFT, sa=8)))
        el.append(Paragraph("<b>Sugestoes:</b>", es("SE", "Helvetica-Bold", 16, G, TA_LEFT, sb=20, sa=8)))
        for su in sugs:
            el.append(Paragraph(f'<b>{su["numero"]}</b> - Energia {su["energia"]} - {su.get("nome_energia", "")}', es("X", "Helvetica", 12, D, TA_LEFT, sa=4)))
            if "explicacao_calculo" in su:
                el.append(Paragraph(f'<i>Calculo: {su["explicacao_calculo"]}</i>', es("C", "Helvetica", 10, colors.HexColor("#888"), TA_LEFT, sa=2)))
        if ni:
            el.append(Paragraph(f'<b>Numero Existente:</b> {ni["numero"]} | Energia {ni["energia"]}', es("J", "Helvetica", 12, D, TA_LEFT, sb=20, sa=4)))
        el.append(Paragraph("Copyright A1ELOS", es("F", "Helvetica", 10, colors.HexColor("#888"), TA_CENTER, sb=40)))
        doc.build(el)
        send_email(em, "Numero Eleitoral - A1ELOS", f"Ola,\n\nPDF com sugestoes para {cl} anexo.\nVerifique spam.\n\nA1ELOS", pf)
        if os.path.exists(pf):
            os.remove(pf)
        return HTMLResponse(OK_HTML)
    except Exception:
        logger.error(traceback.format_exc())
        return HTMLResponse(ERR_HTML.format(msg="Erro ao gerar. Contate arvigne@gmail.com"))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "10000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
