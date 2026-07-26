import os, json, uuid, logging, math
from datetime import date, datetime
from typing import Optional

import stripe
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
import base64

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── Config ──────────────────────────────────────────
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUB = os.getenv("STRIPE_PUBLISHABLE_KEY", "")
SENDGRID_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@a1elos.com.br")
SITE_URL   = os.getenv("SITE_URL", "https://global-numerology.onrender.com")

# ── App ─────────────────────────────────────────────
app = FastAPI(title="Global Numerology")

# ── Static ──────────────────────────────────────────
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ── Modelos ─────────────────────────────────────────
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

# ── Números Mestres ─────────────────────────────────
NUM_MASTER = {11, 22, 33}

def red(n):
    while n > 9 and n not in NUM_MASTER:
        n = sum(int(d) for d in str(n))
    return n

def soma_data(dia, mes, ano):
    return red(dia) + red(mes) + red(ano)

def calc_mapa(nome, data_nasc):
    nome = nome.strip().upper()
    parts = data_nasc.replace("/", "-").split("-")
    d, m, a = int(parts[0]), int(parts[1]), int(parts[2])

    vog = "A1E5I9O6U3"
    con = {"B":2,"C":3,"D":4,"F":6,"G":7,"H":8,"J":1,"K":2,"L":3,"M":4,"N":5,"P":7,"Q":8,"R":9,"S":1,"T":2,"V":4,"W":5,"X":6,"Y":7,"Z":8}

    sv = 0
    sc = 0
    for ch in nome:
        if ch in vog:
            sv += int(vog[vog.index(ch)+1])
        elif ch in con:
            sc += con[ch]

    vida = soma_data(d, m, a)
    dest = red(vida + red(sc + sv))
    exp = red(sc + sv)
    mot = red(sv)
    pers = red(sc)

    # dicionários
    vib_dict = {
        "1": "Liderança, independência, pioneirismo, determinação, autoconfiança.",
        "2": "Cooperação, sensibilidade, equilíbrio, diplomacia, intuição.",
        "3": "Criatividade, comunicação, otimismo, expressão, entusiasmo.",
        "4": "Disciplina, praticidade, estabilidade, lealdade, trabalho.",
        "5": "Liberdade, versatilidade, aventura, mudança, adaptabilidade.",
        "6": "Responsabilidade, amor, harmonia, cuidado, justiça.",
        "7": "Sabedoria, análise, espiritualidade, perfeccionismo, introspecção.",
        "8": "Poder, realização, ambição, autoridade, sucesso material.",
        "9": "Comp放松ão, humanitarismo, idealismo, generosidade, altruísmo.",
        "11": "Intuição elevada, sensibilidade espiritual, inspiração, idealismo.",
        "22": "Construtor do impossível, visão prática, mestre da matéria.",
        "33": "Mestre da comp放松ão, amor universal, cura espiritual."
    }
    signo_map = {
        (3,21,4,20):"Áries", (4,21,5,20):"Touro", (5,21,6,20):"Gêmeos",
        (6,21,7,22):"Câncer", (7,23,8,22):"Leão", (8,23,9,22):"Virgem",
        (9,23,10,22):"Libra", (10,23,11,21):"Escorpião", (11,22,12,21):"Sagitário",
        (12,22,1,20):"Capricórnio", (1,21,2,19):"Aquário", (2,20,3,20):"Peixes"
    }

    def calc_idade(d,m,a):
        hoje = date.today()
        nasc = date(a,m,d)
        idade = hoje.year - nasc.year
        if hoje.month < nasc.month or (hoje.month==nasc.month and hoje.day<nasc.day):
            idade -= 1
        return idade

    def calc_signo(d,m):
        for (mi,di,mf,df),s in signo_map.items():
            if (m==mi and d>=di) or (m==mf and d<=df):
                return s
        return "Capricórnio"

    idade = calc_idade(d,m,a)
    signo = calc_signo(d,m)

    anos_pessoais = {}
    ano_atual = datetime.now().year
    for i in range(5):
        ap = red(d + m + (ano_atual + i))
        anos_pessoais[ano_atual + i] = str(ap)

    res = {
        "life_path": str(vida), "expression": str(exp), "soul_urge": str(mot),
        "personality": str(pers), "destiny": str(dest),
        "vib_life_path": vib_dict.get(str(vida), ""),
        "vib_expression": vib_dict.get(str(exp), ""),
        "vib_soul_urge": vib_dict.get(str(mot), ""),
        "vib_personality": vib_dict.get(str(pers), ""),
        "vib_destiny": vib_dict.get(str(dest), ""),
        "age": idade, "sign": signo,
        "personal_years": anos_pessoais,
        "full_name": nome, "birth_date": data_nasc
    }
    return res

# ── Email ───────────────────────────────────────────
def send_email(to, subject, text, pdf_path=None):
    if not SENDGRID_KEY:
        logger.warning("SendGrid sem chave")
        return
    msg = Mail(from_email=FROM_EMAIL, to_emails=to, subject=subject, plain_text_content=text)
    if pdf_path and os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        msg.add_attachment(Attachment(
            FileContent(data), FileName("Mapa.pdf"), FileType("application/pdf"), Disposition("attachment")
        ))
    try:
        SendGridAPIClient(SENDGRID_KEY).send(msg)
    except Exception as e:
        logger.error(f"SendGrid: {e}")

# ── Rotas ───────────────────────────────────────────
@app.get("/")
def index():
    return RedirectResponse(url="/static/index.html")

@app.get("/config")
def config():
    return {"stripe_pk": STRIPE_PUB}

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
                G = colors.HexColor("#B8860B")
                L = colors.HexColor("#f0f0f0")
                D = colors.HexColor("#222")
                def es(n, f, s, c, a, sb=0, sa=0):
                    return ParagraphStyle(n, fontName=f, fontSize=s, textColor=c, alignment=a, spaceBefore=sb, spaceAfter=sa, leading=s*1.5)
                pf = f"/tmp/pdf_{uuid.uuid4().hex[:8]}.pdf"
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

@app.post("/calculate/urna")
def calc_urna(req: UrnaPayReq):
    res = calc_mapa(req.nome_completo, req.data_nascimento)
    res["nome_urna"] = req.nome_urna
    res["type"] = "urna"
    return res

@app.post("/calculate/eleitoral")
def calc_eleitoral(req: EleitoralPayReq):
    numbers = [int(c) for c in req.numero_titulo if c.isdigit()][:12]
    while len(numbers) < 12:
        numbers.append(0)
    res = calc_mapa(req.nome_completo, req.data_nascimento)
    res["numero_titulo"] = req.numero_titulo
    res["titulo_sum"] = sum(numbers)
    res["titulo_reduced"] = red(sum(numbers))
    res["type"] = "eleitoral"
    return res

# ── Stripe Checkout ─────────────────────────────────
def _create_checkout(price, name, metadata, req_data=None):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card", "boleto"],
            line_items=[{"price_data": {"currency": "brl", "product_data": {"name": name}, "unit_amount": price}, "quantity": 1}],
            mode="payment",
            success_url=f"{SITE_URL}/static/sucesso.html",
            cancel_url=f"{SITE_URL}/static/cancelado.html",
            metadata=metadata or {},
        )
        return {"id": session.id, "url": session.url}
    except Exception as e:
        logger.error(f"Stripe: {e}")
        raise HTTPException(500, "Erro no pagamento")

@app.post("/pay/express")
def pay_express(req: PayReq):
    return _create_checkout(800, "Mapa Numerologico Express", {"type":"express","name":req.name,"birth":req.birth_date})

@app.post("/pay/complete")
def pay_complete(req: PayReq):
    return _create_checkout(1700, "Mapa Numerologico Completo", {"type":"complete","name":req.name,"birth":req.birth_date})

@app.post("/pay/urna")
def pay_urna(req: UrnaPayReq):
    return _create_checkout(2600, "Nome de Urna", {"type":"urna","name":req.nome_completo,"birth":req.data_nascimento,"urna":req.nome_urna})

@app.post("/pay/eleitoral")
def pay_eleitoral(req: EleitoralPayReq):
    return _create_checkout(2600, "Numero Eleitoral", {"type":"eleitoral","name":req.nome_completo,"birth":req.data_nascimento,"titulo":req.numero_titulo})

# ── Webhook Stripe ──────────────────────────────────
@app.post("/stripe-webhook")
async def stripe_webhook(req: Request):
    payload = await req.body()
    sig = req.headers.get("stripe-signature", "")
    whsec = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    if whsec:
        try:
            event = stripe.Webhook.construct_event(payload, sig, whsec)
        except Exception:
            raise HTTPException(400, "Invalid signature")
    else:
        data = json.loads(payload)
        event = {"type": data.get("type", ""), "data": data.get("data", {})}
    if event["type"] == "checkout.session.completed":
        sess = event["data"]["object"]
        logger.info(f"Pagamento OK: {sess.get('id')}")
    return {"ok": True}