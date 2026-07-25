# -*- coding: utf-8 -*-
# main.py - Rotas da API (LEAN)
import os, logging, uuid, stripe, traceback
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from engine import app, Session, logger
from models import Calc, Payment
from dicionarios import SIG, CAM, DES, VIB, t
from calc_service import calc_mapa, calc_grid, calc_nome, reduzir
from pdf_service import pdf8, pdf17, pdf_urna, pdf_eleitoral
from email_service import enviar
from urna import validar_nomes, CARGO_LABELS, ENERGIAS
from eleitoral import gerar_numeros, ENERGIAS as ENERGIAS_EL

# ── Config Stripe ──
STRIPE_KEY = os.getenv("STRIPE_SECRET_KEY", "")
BASE_URL = os.getenv("BASE_URL", "https://global-numerology.onrender.com")
if STRIPE_KEY:
    stripe.api_key = STRIPE_KEY

# ── Modelos de requisição ──
class PayReq(BaseModel):
    name: str
    email: str = ""
    product: Optional[str] = "pdf8"
    price: Optional[float] = 0
    calculation_id: Optional[str] = None
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

# ── Páginas HTML de resultado ──
OK = "<html><body style='background:#0a0a0a;color:#fff;font-family:sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh'><div style='text-align:center'><h1 style='color:#C9A94E'>✅ Confirmado!</h1><p>Documento enviado para seu email.</p><p>Verifique o spam.</p><a href='/' style='display:inline-block;padding:12px 30px;background:#C9A94E;color:#000;text-decoration:none;border-radius:50px'>Voltar</a></div></body></html>"
ERR = "<html><body style='background:#0a0a0a;color:#fff;font-family:sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh'><div style='text-align:center'><h1 style='color:#e74c3c'>{msg}</h1><a href='/' style='display:inline-block;padding:12px 30px;background:#C9A94E;color:#000;text-decoration:none;border-radius:50px'>Voltar</a></div></body></html>"
CANCEL = "<html><body style='background:#0a0a0a;color:#fff;font-family:sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh'><div style='text-align:center'><h1 style='color:#e67e22'>⏸️ Cancelado</h1><a href='/' style='display:inline-block;padding:12px 30px;background:#C9A94E;color:#000;text-decoration:none;border-radius:50px'>Voltar</a></div></body></html>"

# ════════════════════════════════════════════════
# ROTA 1: Frontend
# ════════════════════════════════════════════════
@app.get("/", response_class=HTMLResponse)
def root():
    try:
        p = os.path.join(os.path.dirname(__file__), "index.html")
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                return HTMLResponse(f.read())
    except:
        pass
    return HTMLResponse("<h1>Global Numerology API ativa</h1>")

@app.get("/api/health")
def health():
    return {"status":"ok","stripe":bool(STRIPE_KEY)}

# ════════════════════════════════════════════════
# ROTA 2: Calcular Mapa Grátis (PRODUTO 1)
# ════════════════════════════════════════════════
@app.post("/calculate")
def calculate(req: PayReq):
    db = Session()
    try:
        if len(req.name.strip()) < 2:
            raise HTTPException(400, "Nome curto")
        if not req.birth_date:
            raise HTTPException(400, "Data obrigatória")
        res = calc_mapa(req.name, req.birth_date)
        cid = uuid.uuid4().hex[:8]
        db.add(Calc(id=cid, name=req.name, birth_date=req.birth_date,
                     email=req.email, **res))
        db.commit()
        if req.email:
            try:
                pf = pdf8(res, req.name, req.birth_date)
                enviar(req.email, "Seu Mapa Express!",
                       f"Olá {req.name},\n\nSeu mapa foi gerado.\n\nA1ELOS", pf)
                if os.path.exists(pf):
                    os.remove(pf)
            except:
                pass
        return {"id": cid, **res, "email_sent": True}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Calc: {e}")
        raise HTTPException(500, "Erro")
    finally:
        db.close()

# ════════════════════════════════════════════════
# ROTA 3: Pagamento Stripe (PRODUTO 1 e 2)
# ════════════════════════════════════════════════
@app.post("/api/pay/stripe")
def pay_stripe(req: PayReq):
    if not STRIPE_KEY:
        raise HTTPException(503, "Stripe não configurado")
    if not req.price or req.price <= 0:
        raise HTTPException(400, "Preço inválido")
    try:
        amt = int(float(req.price) * 100)
        pm_types = ["boleto"] if req.payment_method == "boleto" else ["card"]
        pm_options = {}
        if req.payment_method == "boleto":
            pm_options = {"boleto": {"expires_after_days": 3}}
        else:
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
        return HTMLResponse(ERR.format(msg="Sessão inválida"))
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

        # Boleto = aguardar confirmação
        if pm == "boleto":
            html = f"""<!DOCTYPE html><html lang="pt"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Boleto Gerado</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:system-ui,sans-serif;background:#0a0a0a;color:#fff;display:flex;
align-items:center;justify-content:center;min-height:100vh;padding:2rem}}
.card{{background:#111;border:1px solid #222;border-radius:16px;padding:3rem;
max-width:520px;text-align:center}}
h1{{color:#C9A94E;font-size:1.6rem;margin-bottom:0.5rem}}
p{{color:#999;line-height:1.7;font-size:1rem;margin:0.5rem 0}}
.email{{color:#C9A94E;font-weight:600}}
</style></head><body><div class="card">
<div style="font-size:3rem;margin-bottom:1rem">📄</div>
<h1>Boleto Gerado!</h1>
<p>Seu boleto foi emitido. Após a confirmação (até <strong>3 dias úteis</strong>),
enviaremos o PDF para:</p>
<p class="email">{email_val}</p>
<a href="/" style="display:inline-block;margin-top:1.5rem;padding:14px 36px;
background:#C9A94E;color:#000;text-decoration:none;border-radius:50px;
font-weight:600">Voltar ao Início</a>
</div></body></html>"""
            return HTMLResponse(html)

        if not bd:
            bd = "2000-01-01"
    except Exception as e:
        logger.error(f"Erro: {e}")
        return HTMLResponse(ERR.format(msg="Falha no pagamento"))

    try:
        data = calc_mapa(name, bd)
        if prod == "pdf17":
            pf = pdf17(data, name, bd, lang)
            subj = "Seu Mapa Numerológico Completo!"
            prod_nome = "Mapa Completo"
        else:
            pf = pdf8(data, name, bd)
            subj = "Seu Mapa Numerológico!"
            prod_nome = "Mapa Express"
        sent = False
        if pf:
            sent = enviar(email_val, subj,
                          f"Olá {name},\n\nDocumento anexo.\nVerifique o spam.\n\nA1ELOS", pf)
        if pf and os.path.exists(pf):
            os.remove(pf)
        if sent:
            return HTMLResponse(OK)
        return HTMLResponse(ERR.format(msg="Pagamento OK, erro no envio."))
    except Exception as e:
        logger.error(f"ERRO: {e}")
        logger.error(traceback.format_exc())
        return HTMLResponse(ERR.format(msg="Erro ao gerar. Contate arvigne@gmail.com"))

@app.get("/api/pay/cancel")
def pay_cancel():
    return HTMLResponse(CANCEL)

# ════════════════════════════════════════════════
# ROTA 4: Nome de Urna (PRODUTO 3)
# ════════════════════════════════════════════════
@app.post("/api/pay/urna-session")
def pay_urna_session(req: UrnaPayReq):
    if not STRIPE_KEY:
        raise HTTPException(503, "Stripe não configurado")
    if not req.email:
        raise HTTPException(400, "Email obrigatório")
    nomes = [n.strip() for n in [req.nome1, req.nome2, req.nome3,
                                  req.nome4, req.nome5] if n.strip()]
    if not nomes:
        raise HTTPException(400, "Pelo menos 1 nome")
    meta = {"product": "urna26", "nome_completo": req.nome_completo,
            "cargo": req.cargo, "email": req.email}
    for i, n in enumerate(nomes, 1):
        meta[f"nome{i}"] = n
    cs = stripe.checkout.Session.create(
        mode="payment", payment_method_types=["card"],
        line_items=[{"price_data": {"currency": "brl",
                      "product_data": {"name": "Validação Nome"},
                      "unit_amount": 2600}, "quantity": 1}],
        customer_email=req.email, metadata=meta,
        success_url=f"{BASE_URL}/api/pay/urna-success?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{BASE_URL}/api/pay/cancel",
    )
    return {"payment_url": cs.url, "id": cs.id}

@app.get("/api/pay/urna-success")
def pay_urna_success(request: Request):
    sid = request.query_params.get("session_id", "")
    if not sid:
        return HTMLResponse(ERR.format(msg="Sessão inválida"))
    s = stripe.checkout.Session.retrieve(sid)
    meta = getattr(s, "metadata", {}) or {}
    if hasattr(meta, "to_dict"):
        meta = meta.to_dict()
    nc = meta.get("nome_completo", "")
    cr = meta.get("cargo", "vereador")
    em = meta.get("email", "") or getattr(s, "customer_email", "")
    nomes = [meta.get(f"nome{i}", "") for i in range(1, 6)
             if meta.get(f"nome{i}", "")]
    if not nomes:
        return HTMLResponse(ERR.format(msg="Dados não encontrados"))
    try:
        res, _, sugs = validar_nomes(nomes, cr)
        cl = CARGO_LABELS.get(cr, cr)
        pf = pdf_urna(nc, cl, res, sugs)
        pn = nc.split()[0] if nc else ""
        enviar(em, "Validação Nome - A1ELOS",
               f"Olá {pn},\n\nPDF anexo.\nVerifique spam.\n\nA1ELOS", pf)
        if pf and os.path.exists(pf):
            os.remove(pf)
        return HTMLResponse(OK)
    except:
        logger.error(traceback.format_exc())
        return HTMLResponse(ERR.format(msg="Erro ao gerar. Contate arvigne@gmail.com"))

# ════════════════════════════════════════════════
# ROTA 5: Nº Eleitoral (PRODUTO 4)
# ════════════════════════════════════════════════
@app.post("/api/pay/eleitoral-session")
def pay_eleitoral_session(req: EleitoralPayReq):
    if not STRIPE_KEY:
        raise HTTPException(503, "Stripe não configurado")
    if req.sigla < 10 or req.sigla > 99:
        raise HTTPException(400, "Sigla: 2 dígitos")
    if req.cargo not in ["vereador", "dep_estadual", "dep_federal", "senador"]:
        raise HTTPException(400, "Cargo inválido")
    cs = stripe.checkout.Session.create(
        mode="payment", payment_method_types=["card"],
        line_items=[{"price_data": {"currency": "brl",
                      "product_data": {"name": "Número Eleitoral"},
                      "unit_amount": 2600}, "quantity": 1}],
        customer_email=req.email,
        metadata={"product": "eleitoral26", "sigla": str(req.sigla),
                  "cargo": req.cargo, "email": req.email,
                  "numero_existente": req.numero_existente or ""},
        success_url=f"{BASE_URL}/api/pay/eleitoral-success?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{BASE_URL}/api/pay/cancel",
    )
    return {"payment_url": cs.url, "id": cs.id}

@app.get("/api/pay/eleitoral-success")
def pay_eleitoral_success(request: Request):
    sid = request.query_params.get("session_id", "")
    if not sid:
        return HTMLResponse(ERR.format(msg="Sessão inválida"))
    s = stripe.checkout.Session.retrieve(sid)
    meta = getattr(s, "metadata", {}) or {}
    if hasattr(meta, "to_dict"):
        meta = meta.to_dict()
    sg = int(meta.get("sigla", "0"))
    cr = meta.get("cargo", "vereador")
    em = meta.get("email", "") or getattr(s, "customer_email", "")
    if not em:
        return HTMLResponse(ERR.format(msg="Email não encontrado"))
    ne_str = meta.get("numero_existente", "")
    ss = str(sg).zfill(2)
    cl_map = {"vereador": "Vereador", "dep_estadual": "Dep. Estadual",
              "dep_federal": "Dep. Federal", "senador": "Senador"}
    cl2 = cl_map.get(cr, cr)
    sugs = gerar_numeros(sg, cr)
    ni = None
    if ne_str and len(ne_str) >= 3:
        try:
            en = reduzir(sum(int(d) for d in ne_str))
            ni = {"numero": ne_str, "energia": en,
                  "interpretacao": ENERGIAS_EL.get(en, "")}
        except:
            pass
    try:
        pf = pdf_eleitoral(ss, cl2, sugs, ni)
        enviar(em, "Número Eleitoral - A1ELOS",
               f"Olá,\n\nPDF com sugestões para {cl2} anexo.\nVerifique spam.\n\nA1ELOS", pf)
        if pf and os.path.exists(pf):
            os.remove(pf)
        return HTMLResponse(OK)
    except:
        logger.error(traceback.format_exc())
        return HTMLResponse(ERR.format(msg="Erro ao gerar. Contate arvigne@gmail.com"))

# ════════════════════════════════════════════════
# Webhook Stripe (Boleto)
# ════════════════════════════════════════════════
@app.post("/api/pay/stripe/webhook")
async def stripe_webhook(request: Request):
    import json
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")
    wh_secret = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    if wh_secret:
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, wh_secret)
        except stripe.error.SignatureVerificationError:
            return {"error": "Invalid signature"}
    else:
        try:
            event = json.loads(payload)
        except:
            return {"error": "Invalid payload"}
    event_type = event.get("type") if isinstance(event, dict) else event.type
    if event_type in ["checkout.session.completed",
                       "checkout.session.async_payment_succeeded"]:
        session = event["data"]["object"] if isinstance(event, dict) else event.data.object
        session_id = session.get("id") if isinstance(session, dict) else session.id
        meta = session.get("metadata", {}) if isinstance(session, dict) else getattr(session, "metadata", {}) or {}
        if hasattr(meta, "to_dict"):
            meta = meta.to_dict()
        if meta.get("payment_method") == "boleto" or \
           (isinstance(session, dict) and session.get("payment_method_types", []) == ["boleto"]):
            await _process_boleto(session_id, meta)
    return {"status": "ok"}

async def _process_boleto(session_id: str, meta: dict):
    db = Session()
    try:
        payment = db.query(Payment).filter(Payment.id == session_id).first()
        if not payment or payment.status == "completed":
            return
        name = payment.name or meta.get("name", "")
        bd = payment.birth_date or meta.get("birth_date", "") or "2000-01-01"
        prod = payment.product or meta.get("product", "pdf8")
        lang = payment.lang or meta.get("lang", "pt")
        email = payment.email or meta.get("email", "")
        if not email:
            return
        data = calc_mapa(name, bd)
        if prod == "pdf17":
            pdf_path = pdf17(data, name, bd, lang)
            prod_name = "Mapa Completo"
        else:
            pdf_path = pdf8(data, name, bd)
            prod_name = "Mapa Express"
        if not pdf_path or not os.path.exists(pdf_path):
            return
        import secrets
        token = secrets.token_hex(24)
        payment.status = "completed"
        payment.download_token = token
        payment.completed_at = datetime.utcnow()
        db.commit()
        _send_boleto_email(email, name, prod_name, token, lang)
        os.remove(pdf_path)
    except Exception as e:
        logger.error(f"Process boleto: {e}")
    finally:
        db.close()

def _send_boleto_email(to_email, name, prod_name, token, lang="pt"):
    dl = f"{BASE_URL}/api/pay/download/{token}"
    if lang == "pt":
        subj = f"Seu {prod_name} está pronto!"
        body = (f"Olá {name},\n\nO pagamento do seu {prod_name} foi confirmado!\n"
                f"Baixe seu PDF:\n{dl}\n\nLink exclusivo por 30 dias.\n\nA1ELOS")
    else:
        subj = f"Your {prod_name} is ready!"
        body = (f"Hello {name},\n\nYour {prod_name} payment confirmed!\n"
                f"Download:\n{dl}\n\nLink exclusive for 30 days.\n\nA1ELOS")
    smtp_pw = os.getenv("SMTP_PASSWORD", "")
    from_email = os.getenv("FROM_EMAIL", "")
    if not smtp_pw or not from_email:
        logger.warning(f"SMTP ausente — link manual: {dl}")
        return
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subj
        msg.attach(MIMEText(body, "plain", "utf-8"))
        with smtplib.SMTP("smtp.gmail.com", 587) as s:
            s.starttls()
            s.login(from_email, smtp_pw)
            s.send_message(msg)
    except Exception as e:
        logger.error(f"SMTP erro: {e}")

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
        data = calc_mapa(payment.name, payment.birth_date)
        if payment.product == "pdf17":
            pdf_path = pdf17(data, payment.name, payment.birth_date, payment.lang)
            fname = "Mapa_Completo"
        else:
            pdf_path = pdf8(data, payment.name, payment.birth_date)
            fname = "Mapa_Express"
        if not pdf_path or not os.path.exists(pdf_path):
            return HTMLResponse("<h1>Erro ao gerar PDF</h1>")
        with open(pdf_path, "rb") as f:
            content = f.read()
        os.remove(pdf_path)
        from fastapi.responses import Response
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

# ── Inicialização ──
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "10000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
