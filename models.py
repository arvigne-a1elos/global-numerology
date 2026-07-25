# -*- coding: utf-8 -*-
# models.py - Modelos do banco de dados SQLAlchemy

from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

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
