# -*- coding: utf-8 -*-
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
    return {"life_path": lp, "expression": expr, "soul_urge": alma, "personality": pers, "destiny": dest}