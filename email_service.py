# -*- coding: utf-8 -*-
# email_service.py - Envio de emails via SendGrid
import os, logging, base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail, Email, Content, Attachment,
    FileContent, FileName, FileType, Disposition
)

logger = logging.getLogger(__name__)
SENDGRID_KEY = os.getenv("SENDGRID_API_KEY", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", "arvigne@gmail.com")
FROM_NAME = "Mapa Numerologico | A1ELOS"

def enviar(para, assunto, corpo, anexo=None):
    """Envia email com PDF opcional. Retorna True/False."""
    if not SENDGRID_KEY:
        logger.warning("SendGrid não configurado")
        return False
    try:
        sg = SendGridAPIClient(SENDGRID_KEY)
        mail = Mail(Email(FROM_EMAIL, FROM_NAME), para, assunto, Content("text/plain", corpo))
        if anexo and os.path.exists(anexo):
            with open(anexo, "rb") as f:
                enc = base64.b64encode(f.read()).decode()
            mail.attachment = Attachment(
                FileContent(enc), FileName("Documento_A1ELOS.pdf"),
                FileType("application/pdf"), Disposition("attachment"),
            )
        sg.send(mail)
        logger.info(f"Email enviado para {para}")
        return True
    except Exception as e:
        logger.error(f"Falha email: {e}")
        return False
