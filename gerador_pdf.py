# gerador_pdf.py - A1ELOS Global Numerology
# ORQUESTRADOR: escolhe o template certo, chama o pdf_service e entrega (PDF + QRCode).
# Papel único: gerar_pdf(produto, dados, lang, nome, nascimento) -> {pdf, qr, url, pdf_ok}
# Sem cálculo (calc_service), sem textos (dicionarios), sem renderização (pdf_service).

import os, uuid, base64, io, logging
import qrcode
from pdf_service import pdf8, pdf17, pdf_urna, pdf_eleitoral, pdf_produto
from dicionarios import PDF_TEXTS, PRODUTOS, TRAD

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = os.getenv("BASE_URL", os.getenv("SITE_URL", "https://global-numerology.onrender.com"))

# ===== ENTREGA PDF + QRCODE (movida do main.py) =====
def _entregar_arquivo(tipo, nome, lang="pt", extra=""):
    """Gera PDF + QRCode (sem email). Se o PDF falhar, entrega apenas o QRCode."""
    os.makedirs("static/relatorios", exist_ok=True)
    codigo = uuid.uuid4().hex[:8]
    arquivo_pdf = f"static/relatorios/{tipo}_{codigo}.pdf"
    arquivo_qr = f"static/relatorios/{tipo}_{codigo}.png"
    pdf_ok = False
    try:
        from reportlab.pdfgen import canvas
        c = canvas.Canvas(arquivo_pdf)
        c.setFont("Helvetica-Bold", 18)
        c.drawString(60, 780, f"A1ELOS - {tipo.upper()}")
        c.setFont("Helvetica", 12)
        c.drawString(60, 750, f"{nome} | {lang}")
        c.setFont("Helvetica", 10)
        c.drawString(60, 730, PDF_TEXTS.get(lang, PDF_TEXTS["pt"])["entrega"])
        c.save()
        pdf_ok = True
    except Exception as e:
        logger.error(f"Falha ao gerar PDF: {e}")
        arquivo_pdf = None
    alvo = f"{BASE_URL}/{arquivo_pdf}" if pdf_ok else f"{BASE_URL}/?tipo={tipo}&lang={lang}"
    try:
        img = qrcode.make(alvo)
        img.save(arquivo_qr)
        logger.info(f"QRCode gerado: {arquivo_qr} -> {alvo}")
    except Exception as e:
        logger.error(f"Falha ao gerar QRCode: {e}")
        arquivo_qr = None
    return {"pdf": arquivo_pdf, "qr": arquivo_qr, "url": alvo, "pdf_ok": pdf_ok}

# ===== PAGINA DE SUCESSO (movida do main.py) =====
def pagina_sucesso(pdf_path, nome, prod_nome, lang="pt"):
    T = PDF_TEXTS.get(lang, PDF_TEXTS["pt"])
    base = PDF_TEXTS["pt"]
    FALLBACK = {"baixar": "Baixar PDF", "download": "Baixar PDF",
                "qr_titulo": "Ou escaneie o QR Code:",
                "qr_instrucao": "Aponte a câmera para o QR Code e abra o link",
                "confirmado": "Pagamento Confirmado!",
                "gerado": "Seu documento foi gerado com sucesso.",
                "voltar": "Voltar"}

    def tx(k):
        return (T.get(k) or base.get(k)
                or TRAD.get(lang, {}).get(k) or TRAD["pt"].get(k)
                or FALLBACK.get(k, k))

    b64 = ""
    if pdf_path and os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
    btn = ""
    qr_html = ""
    if b64:
        btn = (f'<a href="data:application/pdf;base64,{b64}" download="Documento.pdf" '
               f'style="display:inline-block;padding:18px 50px;background:#C9A94E;color:#000;'
               f'text-decoration:none;border-radius:50px;font-weight:700;font-size:1.2rem;margin:25px 0">{tx("baixar")}</a>')
    else:
        try:
            buf = io.BytesIO()
            img = qrcode.make(BASE_URL)
            img.save(buf, format="PNG")
            qr_b64 = base64.b64encode(buf.getvalue()).decode()
            qr_html = (f'<p style="color:#C9A94E;font-size:1.1rem">{tx("qr_titulo")}</p>'
                       f'<p style="color:#ccc">{tx("qr_instrucao")}</p>'
                       f'<img src="data:image/png;base64,{qr_b64}" style="width:200px;height:200px;margin:15px 0">')
        except Exception as e:
            logger.error(f"Falha QRCode fallback: {e}")
    return (f'<html><body style="background:#0a0a0a;color:#fff;text-align:center;padding:40px;'
            f'font-family:sans-serif"><h1 style="color:#C9A94E">{tx("confirmado")}</h1>'
            f'<p>{tx("gerado").format(nome=nome, prod=prod_nome)}</p>{btn}{qr_html}'
            f'<a href="/" style="color:#C9A94E">{tx("voltar")}</a></body></html>')

# ===== FUNÇÃO ÚNICA DO ORQUESTRADOR =====
def gerar_pdf(produto, dados, lang="pt", nome="", nascimento=""):
    """Gera o PDF do produto no idioma e retorna o caminho do arquivo.

    dados: dict dos 5 números (calc) para a maioria dos produtos.
    Para urna: dados = {nome_completo, cargo_label, resultados, sugestoes}
    Para eleitoral: dados = {sigla, cargo_label, sugestoes, numero_existente}
    """
    if produto == "express":
        return pdf8(dados, nome, nascimento, lang)
    if produto == "completo":
        return pdf17(dados, nome, nascimento, lang)
    if produto == "urna":
        return pdf_urna(dados["nome_completo"], dados["cargo_label"],
                        dados["resultados"], dados["sugestoes"], lang)
    if produto == "eleitoral":
        return pdf_eleitoral(dados["sigla"], dados["cargo_label"],
                             dados["sugestoes"], dados.get("numero_existente"), lang)
    return pdf_produto(produto, dados, nome, nascimento, lang)
