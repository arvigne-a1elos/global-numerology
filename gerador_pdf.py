# gerador_pdf.py - A1ELOS Global Numerology
# ORQUESTRADOR: escolhe o template certo, enriquece os dados com a semântica
# (energias, vidas, formas/cores, números-mestre) e chama o pdf_service.
# Papel: gerar_pdf(produto, dados, lang, nome, nascimento) -> caminho do PDF
# Sem cálculo (produtos.*), sem textos (referencia.semantica), sem renderização (pdf_service).
import os, uuid, base64, io, logging
import qrcode
from numerologia_core import gerar_leitura
from pdf_service import pdf8, pdf17, pdf_urna, pdf_eleitoral, pdf_produto
from dicionarios import PDF_TEXTS, PRODUTOS, TRAD
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
BASE_URL = os.getenv("BASE_URL", os.getenv("SITE_URL", "https://global-numerology.onrender.com"))
def _opt(nome):
    """Resolve um template só se existir no pdf_service. Nunca derruba o import."""
    try:
        import pdf_service
        fn = getattr(pdf_service, nome, None)
        if callable(fn):
            return fn
        logger.warning("Template ausente no pdf_service: %s", nome)
    except Exception as e:
        logger.warning("Falha ao resolver %s: %s", nome, e)
    return None


pdf_casal  = _opt("pdf_casal")
pdf_familia = _opt("pdf_familia")
pdf_equipe = _opt("pdf_equipe")

# ===== SEMANTICA (energias, vidas, formas e cores) - IMPORT OPCIONAL =====
# O gerador NUNCA quebra se o módulo ainda não existir.
try:
    from referencia.semantica import (obter_texto_energia, obter_texto_vida,
                                      renderizar_forma_cor, obter_descricao_mestre)
    SEMANTICA_OK = True
except Exception:
    SEMANTICA_OK = False
    
# ===== ENRIQUECE OS DADOS COM A SEMANTICA (14 idiomas) =====
def _enriquecer_semantica(data, lang):
    """Injeta desc_life e forma_cor no dict de dados, se houver life_path."""
    if not SEMANTICA_OK or not isinstance(data, dict) or not data.get("life_path"):
        return data
    try:
        valor = data["life_path"]
        if valor in (11, 22, 33):
            desc = obter_descricao_mestre(valor, lang)
        else:
            desc = obter_texto_energia(valor, lang)
        if desc:
            data["desc_life"] = desc
        fc = renderizar_forma_cor(valor, lang)
        if fc.get("forma") and fc.get("cor"):
            data["forma_cor"] = fc
    except Exception as e:
        logger.error(f"Falha semantica: {e}")
    return data
    
# ===== ENTREGA PDF + QRCODE =====
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
    alvo = f"{BASE_URL.rstrip('/')}/{arquivo_pdf}" if pdf_ok else BASE_URL
    try:
        img = qrcode.make(alvo)
        img.save(arquivo_qr)
        logger.info(f"QRCode gerado: {arquivo_qr} -> {alvo}")
    except Exception as e:
        logger.error(f"Falha ao gerar QRCode: {e}")
        arquivo_qr = None
    return {"pdf": arquivo_pdf, "qr": arquivo_qr, "url": alvo, "pdf_ok": pdf_ok}
    
# ===== PAGINA DE SUCESSO =====
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
# ===== PRODUTOS DA IA DE NOMES (7 cards) =====
IA_NOMES = {
    "nome_pet", "nickname", "nome_dominio", "nome_canal",
    "nome_equipe", "nome_projeto", "nome_evento",
}

# ===== FUNÇÃO ÚNICA DO ORQUESTRADOR =====
def gerar_pdf(produto, dados, lang, nome, nascimento, dado="",
              dado2="", dado3="", energia=0, tipo="", sexo=""):
    """Escolhe o template certo do pdf_service, enriquece com semântica (14 idiomas)
    e devolve o caminho do PDF gerado."""
    lang = lang or "pt"
    dados = dict(dados or {})
    dados["sexo"] = res.get("sexo", "")              

    # tolera os dois formatos: parâmetro direto ou chave no dict
    dado    = dado    or dados.get("dado")    or ""
    dado2   = dado2   or dados.get("dado2")   or ""
    dado3   = dado3   or dados.get("dado3")   or ""
    tipo    = tipo    or dados.get("tipo")    or ""
    energia = energia or dados.get("energia") or 0
    try:
        energia = int(str(energia).split(".")[0])
    except Exception:
        energia = 0

    # ---- 1. PRODUTOS DA IA DE NOMES: 3 nomes + sugestao (4a opcao) ----
    if produto in IA_NOMES:
        
        try:
            from nome_energia import avaliar_nomes, precisa_romanizar
        except Exception as e:
            logger.error(f"nome_energia indisponivel: {e}")
            sexo = sexo or dados.get("sexo") or ""
            avaliar_nomes = None
            precisa_romanizar = None

        nomes = [n.strip() for n in (dado, dado2, dado3) if n and n.strip()]

        if avaliar_nomes:
            res = avaliar_nomes(nomes, tipo or "outro", energia, lang, sexo)
        else:
            # fallback: entrega os nomes sem calculo, marcando a falha
            res = {"energia_alvo": energia, "tipo": tipo, "idioma": lang,
                   "entradas": [{"nome": n, "energia": 0, "soma": 0,
                                 "bate": False, "romanizar": False} for n in nomes],
                   "escolhido": nomes[0] if nomes else "",
                   "sugestao": None, "sugestao_idioma": None,
                   "sugestao_real": None, "total_opcoes": len(nomes)}

        dados["ia_nomes"] = res
        dados["tipo"] = tipo
        dados["energia"] = energia
        dados["nomes_entrada"] = nomes
        dados["nome_escolhido"] = res.get("escolhido") or (nomes[0] if nomes else "")

        # nascimento nao existe nesses produtos: usa string vazia para nao
        # imprimir "2000-01-01" nem disparar calculo de data
        return pdf_produto(produto, dados, dados["nome_escolhido"], "", lang,
                           dados["nome_escolhido"])

    # ---- 2. Mapa Express (8) / Mapa Completo (17) ----
    if produto in ("express", "completo"):
        data = _enriquecer_semantica(dados, lang)
        if produto == "express":
            return pdf8(data, nome, nascimento, lang)
        return pdf17(data, nome, nascimento, lang)

    # ---- 3. Nome de Urna ----
    if produto == "urna":
        return pdf_urna(dados.get("nome_completo") or nome,
                        dados.get("cargo_label") or "",
                        dados.get("resultados") or [],
                        dados.get("sugestoes") or [],
                        lang)

    # ---- 4. Número Eleitoral ----
    if produto == "eleitoral":
        return pdf_eleitoral(dados.get("sigla") or "",
                             dados.get("cargo_label") or "",
                             dados.get("sugestoes") or [],
                             dados.get("numero_existente"),
                             lang)

    # ---- 5. Calendário Mensal Energético ----
    if produto == "calendario":
        leitura = gerar_leitura(
            data_nasc=dados["nascimento"],   # DD/MM/AAAA completo
            ano_ref=dados["ano_ref"],
            mes_ref=dados["mes_ref"],
            nome=nome,
        )
        return pdf_produto("calendario", leitura, nome, nascimento, lang, dado)

        # ---- 6. PRODUTOS DE RELAÇÃO (usam template próprio se existir) ----
    if produto == "casal":
        if pdf_casal:
            return pdf_casal(dados, lang)
        logger.warning("pdf_casal ausente: usando pdf_produto generico")
        return pdf_produto(produto, _enriquecer_semantica(dados, lang), nome, nascimento, lang, dado)

    if produto == "familia":
        if pdf_familia:
            return pdf_familia(dados, lang)
        logger.warning("pdf_familia ausente: usando pdf_produto generico")
        return pdf_produto(produto, _enriquecer_semantica(dados, lang), nome, nascimento, lang, dado)

    if produto == "compatibilidade_equipes":
        if pdf_equipe:
            return pdf_equipe(dados, lang)
        logger.warning("pdf_equipe ausente: usando pdf_produto generico")
        return pdf_produto(produto, _enriquecer_semantica(dados, lang), nome, nascimento, lang, dado)

    # ---- 7. Demais produtos: template genérico com semântica ----
    data = _enriquecer_semantica(dados, lang)
    return pdf_produto(produto, data, nome, nascimento, lang, dado)
