# -*- coding: utf-8 -*-
# main.py - Global Numerology API Unificada
# Todos os 4 produtos: Mapa Express (R$8), Mapa Completo (R$17),
# Nome de Urna (R$26), Nº Eleitoral (R$26)
# Seletor de pagamento: Cartão ou Boleto

import os, uuid, stripe, logging, traceback, json, smtplib, secrets
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ── LOGGING ──
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── CONFIG ──
STRIPE_KEY = os.getenv("STRIPE_SECRET_KEY", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", "arvigne@gmail.com")
SMTP_PASS = os.getenv("SMTP_PASSWORD", "")
BASE_URL = os.getenv("BASE_URL", "https://global-numerology.onrender.com")
DB_URL = os.getenv("DATABASE_URL", "sqlite:///./numerologia.db")

if STRIPE_KEY:
    stripe.api_key = STRIPE_KEY

# ── BANCO ──
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
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

# ── APP ──
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])

# ── TABELA DE VALORES ──
TABELA = {c: (i % 9 or 9) for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 1)}

# ── FUNÇÕES DE CÁLCULO ──
def reduzir(n, permitir_mestre=True):
    while n > 9:
        if permitir_mestre and n in (11, 22, 33):
            return n
        n = sum(int(d) for d in str(n))
    return n

def calc_nome(nome):
    limpo = nome.upper().replace(" ", "").replace(".", "").replace("-", "").replace(",", "")
    total = sum(TABELA.get(c, 0) for c in limpo if c in TABELA)
    return reduzir(total), total

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
    expr = reduzir(total_e)
    alma = reduzir(total_v)
    pers = reduzir(total_p)
    dest = reduzir(expr + lp)
    return {"life_path": lp, "expression": expr, "soul_urge": alma,
            "personality": pers, "destiny": dest}

def validar_nomes_urna(nomes, cargo_key):
    labels = {"vereador": "Vereador", "dep_estadual": "Dep. Estadual",
              "dep_federal": "Dep. Federal", "senador": "Senador"}
    results = []
    for nome in nomes:
        if not nome.strip():
            continue
        en, st = calc_nome(nome)
        results.append({
            "nome": nome.strip().title(), "energia": en, "soma": st,
            "eh_ideal": en == 8,
            "explicacao": f"Nome {nome.strip().title()} tem energia {en}. {'Ideal!' if en == 8 else 'O 8 é o ideal.'}",
        })
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
    energias = {8: "Poder e Prosperidade (IDEAL)", 7: "Sabedoria", 3: "Criação",
                1: "Liderança", 9: "Humanitarismo", 5: "Liberdade",
                6: "Família", 4: "Trabalho", 2: "Associação"}

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
                    dl_sum = "+".join(dl)
                    st = sm + sum(int(d) for d in dl)
                    enc.append({
                        "numero": n, "energia": alvo, "ideal": alvo == 8,
                        "sigla": ss, "digitos_livres": dl,
                        "nome_energia": energias.get(alvo, ""),
                        "explicacao_calculo": f"Sigla {ss} ({ss[0]}+{ss[1]}={sm}) + dígitos {dl} ({dl_sum}={st-lv}) = {st} -> {alvo}",
                    })
        return enc

    res.extend(busca(8))
    for e in [3, 7, 1, 9, 5, 6, 4, 2]:
        if len(res) >= qtd:
            break
        res.extend(busca(e))
    return res[:qtd]

# ── GERADORES DE PDF ──
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
import dateutil.parser as dp

GOLD = colors.HexColor("#B8860B")
LGRAY = colors.HexColor("#f0f0f0")
DARK = colors.HexColor("#222")
GRAY = colors.HexColor("#888")
FONTE = "Helvetica"
FN = "Helvetica-Bold"
TAM_T = 20
TAM_C = 14
EL = TAM_C * 1.5
ET = TAM_T * 2.0

def _est(nome, fonte, size, cor, alinhamento, sb=0, sa=0):
    return ParagraphStyle(nome, fontName=fonte, fontSize=size,
                          textColor=cor, alignment=alinhamento,
                          spaceBefore=sb, spaceAfter=sa, leading=size * 1.5)

def pdf8(data, nome, bd):
    path = f"/tmp/p8_{uuid.uuid4().hex[:8]}.pdf"
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=50, rightMargin=50,
                            topMargin=45, bottomMargin=45)
    e = []
    TX = {1: "Líder nato, pioneiro.", 2: "Diplomata, sensível.",
          3: "Criativo, comunicador.", 4: "Prático, disciplinado.",
          5: "Livre, aventureiro.", 6: "Amoroso, responsável.",
          7: "Sábio, espiritual.", 8: "Poderoso, próspero.",
          9: "Humanitário, generoso.", 11: "Mestre intuitivo.",
          22: "Mestre construtor."}
    e.append(Spacer(1, 30))
    e.append(Paragraph("MAPA NUMEROLÓGICO",
                       _est("T", FN, TAM_T, GOLD, TA_CENTER, sa=ET)))
    e.append(Paragraph("EXPRESS",
                       _est("S", FONTE, 18, GOLD, TA_CENTER, sa=ET)))
    e.append(Paragraph(nome.upper(),
                       _est("N", FN, TAM_C + 2, DARK, TA_CENTER, sa=4)))
    e.append(Paragraph(bd,
                       _est("D", FONTE, TAM_C - 2, GRAY, TA_CENTER, sa=EL)))
    td = [["Número", "Valor"],
          ["Caminho de Vida", str(data["life_path"])],
          ["Expressão", str(data["expression"])],
          ["Motivação da Alma", str(data["soul_urge"])],
          ["Personalidade", str(data["personality"])],
          ["Destino", str(data["destiny"])]]
    tbl = Table(td, colWidths=[200, 150])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GOLD),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), TAM_C - 2),
        ("FONTNAME", (0, 0), (-1, -1), FONTE),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (1, 0), (1, -1), "CENTER"),
        ("BACKGROUND", (0, 1), (-1, -1), LGRAY),
        ("TEXTCOLOR", (0, 1), (-1, -1), DARK),
    ]))
    e.append(tbl)
    e.append(Spacer(1, EL))
    for k, l in [("life_path", "Caminho de Vida"), ("expression", "Expressão"),
                 ("soul_urge", "Motivação"), ("personality", "Personalidade"),
                 ("destiny", "Destino")]:
        v = data[k]
        e.append(Paragraph(f"<b>{l} {v}:</b> {TX.get(v, 'Único.')}",
                           _est("X", FONTE, TAM_C, DARK, TA_LEFT, sa=EL * 0.5)))
    e.append(Paragraph("© A1ELOS",
                       _est("F", FONTE, 10, GRAY, TA_CENTER, sb=EL * 2)))
    doc.build(e)
    return path

def pdf17(data, nome, bd_str, lang="pt"):
    path = f"/tmp/p17_{uuid.uuid4().hex[:8]}.pdf"
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=50, rightMargin=50,
                            topMargin=45, bottomMargin=45)
    e = []
    lp = data["life_path"]
    bd = dp.parse(bd_str.split(" ")[0] if " " in bd_str else bd_str).date()
    d, m, a = bd.day, bd.month, bd.year

    e.append(Spacer(1, 30))
    e.append(Paragraph("M A P A   N U M E R O L Ó G I C O",
                       _est("T", FN, TAM_T, GOLD, TA_CENTER, sa=4)))
    e.append(Paragraph("C O M P L E T O",
                       _est("U", FONTE, 18, GOLD, TA_CENTER, sa=ET)))
    e.append(Paragraph(nome.upper(),
                       _est("N", FN, TAM_C + 2, DARK, TA_CENTER, sa=4)))
    e.append(Paragraph(bd_str,
                       _est("D", FONTE, TAM_C - 2, GRAY, TA_CENTER, sa=EL)))

    td = [["Número", "Valor", "Significado"],
          ["Caminho de Vida", str(lp), f"Seu caminho de vida"],
          ["Expressão", str(data["expression"]), f"Sua expressão"],
          ["Motivação", str(data["soul_urge"]), f"Sua motivação"],
          ["Personalidade", str(data["personality"]), f"Sua personalidade"],
          ["Destino", str(data["destiny"]), f"Seu destino"]]
    tbl = Table(td, colWidths=[125, 45, 280])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GOLD),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), TAM_C - 2),
        ("FONTNAME", (0, 0), (-1, -1), FONTE),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (1, 0), (1, -1), "CENTER"),
        ("BACKGROUND", (0, 1), (-1, -1), LGRAY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
    ]))
    e.append(tbl)

    # Ciclos
    fe = max(36 - min(lp, 36), 25)
    c1 = reduzir(lp + data["expression"])
    c2 = reduzir(data["expression"] + data["soul_urge"])
    c3 = reduzir(data["soul_urge"] + data["personality"])
    e.append(Paragraph("<b>Ciclos da Vida</b>",
                       _est("SE", FN, 18, GOLD, TA_LEFT, sb=EL, sa=ET)))
    e.append(Paragraph(f"<b>1º Formativo (0-{fe}a) Regente {c1}</b>",
                       _est("J", FONTE, TAM_C - 1, DARK, TA_JUSTIFY, sa=EL * 0.4)))
    e.append(Paragraph(f"<b>2º Produtivo ({fe+1}-{fe+27}a) Regente {c2}</b>",
                       _est("J", FONTE, TAM_C - 1, DARK, TA_JUSTIFY, sa=EL * 0.4)))
    e.append(Paragraph(f"<b>3º Colheita ({fe+28}+a) Regente {c3}</b>",
                       _est("J", FONTE, TAM_C - 1, DARK, TA_JUSTIFY, sa=EL * 0.4)))

    # Desafios
    d1 = reduzir(abs(d - m))
    d2 = reduzir(abs(m - reduzir(a)))
    dp_ = reduzir(abs(d1 - d2))
    e.append(Paragraph("<b>Desafios</b>",
                       _est("SE", FN, 18, GOLD, TA_LEFT, sb=EL, sa=ET)))
    e.append(Paragraph(f"<b>Menor 1 {d1}</b>",
                       _est("J", FONTE, TAM_C - 1, DARK, TA_JUSTIFY, sa=EL * 0.4)))
    e.append(Paragraph(f"<b>Menor 2 {d2}</b>",
                       _est("J", FONTE, TAM_C - 1, DARK, TA_JUSTIFY, sa=EL * 0.4)))
    e.append(Paragraph(f"<b>Principal {dp_}</b>",
                       _est("J", FONTE, TAM_C - 1, DARK, TA_JUSTIFY, sa=EL * 0.4)))

    # Realizações
    r1v = reduzir(d + m)
    r2v = reduzir(d + a)
    r3v = reduzir(r1v + r2v)
    r4v = reduzir(d + m + a)
    e.append(Paragraph("<b>Realizações</b>",
                       _est("SE", FN, 18, GOLD, TA_LEFT, sb=EL, sa=ET)))
    e.append(Paragraph(f"<b>1ª ({r1v}) Juventude</b>",
                       _est("J", FONTE, TAM_C - 1, DARK, TA_JUSTIFY, sa=EL * 0.4)))
    e.append(Paragraph(f"<b>2ª ({r2v}) Vida Adulta</b>",
                       _est("J", FONTE, TAM_C - 1, DARK, TA_JUSTIFY, sa=EL * 0.4)))
    e.append(Paragraph(f"<b>3ª ({r3v}) Maturidade</b>",
                       _est("J", FONTE, TAM_C - 1, DARK, TA_JUSTIFY, sa=EL * 0.4)))

    e.append(Paragraph("© A1ELOS",
                       _est("F", FONTE, 10, GRAY, TA_CENTER, sb=EL * 2)))
    doc.build(e)
    return path

def pdf_urna(nc, cl, resultados, sugestoes):
    path = f"/tmp/u_{uuid.uuid4().hex[:8]}.pdf"
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=50, rightMargin=50,
                            topMargin=45, bottomMargin=45)
    e = []
    e.append(Spacer(1, 25))
    e.append(Paragraph("VALIDAÇÃO DE NOME DE URNA",
                       _est("T", FN, TAM_T, GOLD, TA_CENTER, sa=ET * 0.5)))
    e.append(Paragraph(nc.title(),
                       _est("N", FN, TAM_C + 2, DARK, TA_CENTER, sa=4)))
    e.append(Paragraph(f"Cargo: {cl}",
                       _est("D", FONTE, TAM_C - 2, GRAY, TA_CENTER, sa=EL)))
    for r in resultados:
        ic = "✅" if r["eh_ideal"] else "❌"
        co = "#4CAF50" if r["eh_ideal"] else "#e74c3c"
        e.append(Paragraph(
            f"{ic} <b>{r['nome']}</b> — Energia <b><font color='{co}'>{r['energia']}</font></b>",
            _est("B", FN, TAM_C - 1, DARK, TA_LEFT, sa=EL * 0.3)))
        e.append(Paragraph(r["explicacao"],
                           _est("J", FONTE, TAM_C - 1, DARK, TA_JUSTIFY, sa=EL * 0.4)))
    if sugestoes:
        e.append(Paragraph("Sugestões:",
                           _est("SU", FN, 18, GOLD, TA_LEFT, sb=EL, sa=ET)))
        for s in sugestoes[:3]:
            e.append(Paragraph(f'<b>{s["nome"]}</b> — Energia {s["energia"]}',
                               _est("X", FONTE, TAM_C, DARK, TA_LEFT, sa=EL * 0.3)))
    e.append(Paragraph("© A1ELOS",
                       _est("F", FONTE, 8, GRAY, TA_CENTER)))
    doc.build(e)
    return path

def pdf_eleitoral(ss, cl, sugestoes, ne=None):
    path = f"/tmp/e_{uuid.uuid4().hex[:8]}.pdf"
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=50, rightMargin=50,
                            topMargin=45, bottomMargin=45)
    e = []
    e.append(Spacer(1, 25))
    e.append(Paragraph("NÚMERO ELEITORAL",
                       _est("T", FN, TAM_T, GOLD, TA_CENTER, sa=ET * 0.5)))
    e.append(Paragraph(f"Cargo: {cl} | Sigla: {ss}",
                       _est("D", FONTE, TAM_C - 2, GRAY, TA_CENTER, sa=EL)))
    e.append(Paragraph("<b>Por que a energia 8?</b>",
                       _est("SE", FN, 18, GOLD, TA_LEFT, sb=EL, sa=ET)))
    e.append(Paragraph("O número 8 representa Poder, Prosperidade e Realização material — vibração ideal para candidatos políticos.",
                       _est("J", FONTE, TAM_C - 1, DARK, TA_JUSTIFY, sa=EL * 0.4)))
    e.append(Paragraph("<b>Sugestões:</b>",
                       _est("SE", FN, 18, GOLD, TA_LEFT, sb=EL, sa=ET)))
    for s in sugestoes:
        tag = "✅" if s.get("ideal") else "•"
        e.append(Paragraph(f'{tag} <b>{s["numero"]}</b> — Energia {s["energia"]} — {s.get("nome_energia", "")}',
                           _est("X", FONTE, TAM_C, DARK, TA_LEFT, sa=EL * 0.3)))
        if "explicacao_calculo" in s:
            e.append(Paragraph(f'<i>Cálculo: {s["explicacao_calculo"]}</i>',
                               _est("C", FONTE, TAM_C - 2, GRAY, TA_LEFT, sa=EL * 0.2)))
    if ne:
        e.append(Paragraph("<b>Número Existente:</b>",
                           _est("SE", FN, 18, GOLD, TA_LEFT, sb=EL, sa=ET)))
        e.append(Paragraph(f'Número: {ne["numero"]} | Energia: {ne["energia"]}',
                           _est("J", FONTE, TAM_C - 1, DARK, TA_JUSTIFY, sa=EL * 0.4)))
    e.append(Paragraph("© A1ELOS",
                       _est("F", FONTE, 8, GRAY, TA_CENTER, sb=EL)))
    doc.build(e)
    return path

# ── PÁGINAS HTML ──
OK = "<html><body style='background:#0a0a0a;color:#fff;font-family:sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh'><div style='text-align:center'><h1 style='color:#C9A94E'>✅ Confirmado!</h1><p>Documento enviado para seu email.</p><p>Verifique o spam.</p><a href='/' style='display:inline-block;padding:12px 30px;background:#C9A94E;color:#000;text-decoration:none;border-radius:50px'>Voltar</a></div></body></html>"
ERR = "<html><body style='background:#0a0a0a;color:#fff;font-family:sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh'><div style='text-align:center'><h1 style='color:#e74c3c'>{msg}</h1><a href='/' style='display:inline-block;padding:12px 30px;background:#C9A94E;color:#000;text-decoration:none;border-radius:50px'>Voltar</a></div></body></html>"
CANCEL = "<html><body style='background:#0a0a0a;color:#fff;font-family:sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh'><div style='text-align:center'><h1 style='color:#e67e22'>⏸️ Cancelado</h1><a href='/' style='display:inline-block;padding:12px 30px;background:#C9A94E;color:#000;text-decoration:none;border-radius:50px'>Voltar</a></div></body></html>"

BOLETO_PAGE = """<!DOCTYPE html><html lang="pt"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Boleto Gerado</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:system-ui,sans-serif;background:#0a0a0a;color:#fff;display:flex;align-items:center;justify-content:center;min-height:100vh;padding:2rem}}
.card{{background:#111;border:1px solid #222;border-radius:16px;padding:3rem;max-width:520px;text-align:center}}
h1{{color:#C9A94E;font-size:1.6rem;margin-bottom:0.5rem}}
p{{color:#999;line-height:1.7;font-size:1rem;margin:0.5rem 0}}
.email{{color:#C9A94E;font-weight:600}}
</style></head><body><div class="card">
<div style="font-size:3rem;margin-bottom:1rem">📄</div>
<h1>Boleto Gerado!</h1>
<p>Seu boleto foi emitido. Após a confirmação (até <strong>3 dias úteis</strong>), enviaremos o PDF para:</p>
<p class="email">{email}</p>
<a href="/" style="display:inline-block;margin-top:1.5rem;padding:14px 36px;background:#C9A94E;color:#000;text-decoration:none;border-radius:50px;font-weight:600">Voltar ao Início</a>
</div></body></html>"""

# ── Pydantic Models ──
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

# ═══════════════════════════════════════
# ROTA 1: Frontend
# ═══════════════════════════════════════
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
    return {"status": "ok", "stripe": bool(STRIPE_KEY)}

# ═══════════════════════════════════════
# ROTA 2: Calcular Mapa Grátis
# ═══════════════════════════════════════
@app.post("/calculate")
def calculate(req: PayReq):
    if len(req.name.strip()) < 2:
        raise HTTPException(400, "Nome curto")
    if not req.birth_date:
        raise HTTPException(400, "Data obrigatória")
    try:
        res = calc_mapa(req.name, req.birth_date)
        cid = uuid.uuid4().hex[:8]
        # Envia Mapa Express grátis se tiver email
        if req.email:
            try:
                pf = pdf8(res, req.name, req.birth_date)
                _send_email(req.email, "Seu Mapa Express!",
                           f"Olá {req.name},\n\nSeu mapa foi gerado.\n\nA1ELOS", pf)
                if pf and os.path.exists(pf):
                    os.remove(pf)
            except:
                pass
        return {"id": cid, **res, "email_sent": True}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Calc: {e}")
        raise HTTPException(500, "Erro")

# ═══════════════════════════════════════
# ROTA 3: Pagamento Stripe (Produtos 1-2)
# ═══════════════════════════════════════
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
        bd = meta.get("birth_date", "2000-01-01")
        prod = meta.get("product", "pdf8")
        lang = meta.get("lang", "pt")
        pm = meta.get("payment_method", "card")
        email = getattr(s, "customer_details", None)
        email_val = getattr(email, "email", "") if email else ""

        # Boleto
        if pm == "boleto":
            return HTMLResponse(BOLETO_PAGE.format(email=email_val or "seu email"))
    except Exception as e:
        logger.error(f"Erro: {e}")
        return HTMLResponse(ERR.format(msg="Falha no pagamento"))

    try:
        data = calc_mapa(name, bd)
        if prod == "pdf17":
            pf = pdf17(data, name, bd, lang)
            subj = "Seu Mapa Numerológico Completo!"
        else:
            pf = pdf8(data, name, bd)
            subj = "Seu Mapa Numerológico!"
        sent = False
        if pf:
            sent = _send_email(email_val, subj,
                              f"Olá {name},\n\nDocumento anexo.\nVerifique o spam.\n\nA1ELOS", pf)
        if pf and os.path.exists(pf):
            os.remove(pf)
        if sent:
            return HTMLResponse(OK)
        return HTMLResponse(ERR.format(msg="Pagamento OK, mas erro no envio do email"))
    except Exception as e:
        logger.error(f"ERRO: {e}")
        logger.error(traceback.format_exc())
        return HTMLResponse(ERR.format(msg="Erro ao gerar. Contate arvigne@gmail.com"))

@app.get("/api/pay/cancel")
def pay_cancel():
    return HTMLResponse(CANCEL)

# ═══════════════════════════════════════
# ROTA 4: Nome de Urna (Produto 3)
# ═══════════════════════════════════════
@app.post("/api/pay/urna-session")
def pay_urna_session(req: UrnaPayReq):
    if not STRIPE_KEY:
        raise HTTPException(503, "Stripe não configurado")
    if not req.email:
        raise HTTPException(400, "Email obrigatório")
    nomes = [n.strip() for n in [req.nome1, req.nome2, req.nome3, req.nome4, req.nome5] if n.strip()]
    if not nomes:
        raise HTTPException(400, "Pelo menos 1 nome")

    meta = {"product": "urna26", "nome_completo": req.nome_completo,
            "cargo": req.cargo, "email": req.email}
    for i, n in enumerate(nomes, 1):
        meta[f"nome{i}"] = n

    cs = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
        line_items=[{"price_data": {"currency": "brl",
                      "product_data": {"name": "Validação Nome"},
                      "unit_amount": 2600}, "quantity": 1}],
        customer_email=req.email,
        metadata=meta,
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
    nomes = [meta.get(f"nome{i}", "") for i in range(1, 6) if meta.get(f"nome{i}", "")]
    if not nomes:
        return HTMLResponse(ERR.format(msg="Dados não encontrados"))
    try:
        res, _, sugs = validar_nomes_urna(nomes, cr)
        labels = {"vereador": "Vereador", "dep_estadual": "Dep. Estadual",
                  "dep_federal": "Dep. Federal", "senador": "Senador"}
        cl = labels.get(cr, cr)
        pf = pdf_urna(nc, cl, res, sugs)
        pn = nc.split()[0] if nc else ""
        _send_email(em, "Validação Nome - A1ELOS",
                   f"Olá {pn},\n\nPDF com validação anexo.\nVerifique spam.\n\nA1ELOS", pf)
        if pf and os.path.exists(pf):
            os.remove(pf)
        return HTMLResponse(OK)
    except:
        logger.error(traceback.format_exc())
        return HTMLResponse(ERR.format(msg="Erro ao gerar. Contate arvigne@gmail.com"))

# ═══════════════════════════════════════
# ROTA 5: Nº Eleitoral (Produto 4)
# ═══════════════════════════════════════
@app.post("/api/pay/eleitoral-session")
def pay_eleitoral_session(req: EleitoralPayReq):
    if not STRIPE_KEY:
        raise HTTPException(503, "Stripe não configurado")
    if req.sigla < 10 or req.sigla > 99:
        raise HTTPException(400, "Sigla: 2 dígitos")
    if req.cargo not in ["vereador", "dep_estadual", "dep_federal", "senador"]:
        raise HTTPException(400, "Cargo inválido")

    cs = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
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

    ss = str(sg).zfill(2)
    labels = {"vereador": "Vereador", "dep_estadual": "Dep. Estadual",
              "dep_federal": "Dep. Federal", "senador": "Senador"}
    cl = labels.get(cr, cr)
    sugs = gerar_numeros(sg, cr)

    ne_str = meta.get("numero_existente", "")
    ni = None
    if ne_str and len(ne_str) >= 3:
        try:
            en = reduzir(sum(int(d) for d in ne_str))
            ni = {"numero": ne_str, "energia": en}
        except:
            pass

    try:
        pf = pdf_eleitoral(ss, cl, sugs, ni)
        _send_email(em, "Número Eleitoral - A1ELOS",
                   f"Olá,\n\nPDF com sugestões para {cl} anexo.\nVerifique spam.\n\nA1ELOS", pf)
        if pf and os.path.exists(pf):
            os.remove(pf)
        return HTMLResponse(OK)
    except:
        logger.error(traceback.format_exc())
        return HTMLResponse(ERR.format(msg="Erro ao gerar. Contate arvigne@gmail.com"))

# ═══════════════════════════════════════
# WEBHOOK Stripe (Boleto)
# ═══════════════════════════════════════
@app.post("/api/pay/stripe/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")
    wh_secret = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    try:
        if wh_secret:
            event = stripe.Webhook.construct_event(payload, sig_header, wh_secret)
        else:
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
        if meta.get("payment_method") == "boleto":
            _process_boleto(session_id, meta)
    return {"status": "ok"}

def _process_boleto(session_id, meta):
    db = Session()
    try:
        payment = db.query(Payment).filter(Payment.id == session_id).first()
        if not payment or payment.status == "completed":
            return
        name = payment.name or meta.get("name", "Cliente")
        bd = payment.birth_date or meta.get("birth_date", "2000-01-01")
        prod = payment.product or meta.get("product", "pdf8")
        lang = payment.lang or meta.get("lang", "pt")
        email = payment.email or meta.get("email", "")
        if not email:
            return
        data = calc_mapa(name, bd)
        if prod == "pdf17":
            pdf_path = pdf17(data, name, bd, lang)
        else:
            pdf_path = pdf8(data, name, bd)
        if not pdf_path or not os.path.exists(pdf_path):
            return
        token = secrets.token_hex(24)
        payment.status = "completed"
        payment.download_token = token
        payment.completed_at = datetime.utcnow()
        db.commit()
        dl = f"{BASE_URL}/api/pay/download/{token}"
        _send_email(email, f"Seu mapa está pronto!",
                   f"Olá {name},\n\nPagamento confirmado!\nBaixe seu PDF:\n{dl}\n\nLink exclusivo por 30 dias.\n\nA1ELOS")
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
    except Exception as e:
        logger.error(f"Process boleto: {e}")
    finally:
        db.close()

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

# ── FUNÇÃO DE EMAIL ──
def _send_email(to, subject, body, pdf_path=None):
    if not SMTP_PASS or not FROM_EMAIL:
        logger.warning("SMTP não configurado")
        return False
    try:
        msg = MIMEMultipart()
        msg["From"] = FROM_EMAIL
        msg["To"] = to
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain", "utf-8"))
        if pdf_path and os.path.exists(pdf_path):
            from email.mime.base import MIMEBase
            from email import encoders
            with open(pdf_path, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", "attachment", filename="Documento_A1ELOS.pdf")
            msg.attach(part)
        with smtplib.SMTP("smtp.gmail.com", 587) as s:
            s.starttls()
            s.login(FROM_EMAIL, SMTP_PASS)
            s.send_message(msg)
        logger.info(f"Email enviado para {to}")
        return True
    except Exception as e:
        logger.error(f"Falha email: {e}")
        return False

# ── INICIALIZAÇÃO ──
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "10000"))
    uvicorn.run(app, host="0.0.0.0", port=port)