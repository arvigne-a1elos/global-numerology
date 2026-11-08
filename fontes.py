# -*- coding: utf-8 -*-
# ================================================================
# fontes.py — FONTE ÚNICA DE VERDADE das fontes de PDF (A1ELOS)
# REGRA DE OURO: nenhum outro arquivo do projeto decide fonte.
# Todo gerador de PDF chama: fonte_para(lang) e preparar_texto(txt, lang).
# ================================================================
import os, logging
logger = logging.getLogger(__name__)

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

# --- Registro já feito? evita registrar duas vezes ---
_REGISTRADO = False

# Candidatos de caminho de fonte TTF (ordem: local -> projeto -> sistema)
_CAMINHOS = {
    "DejaVu": [
        "static/fonts/DejaVuSans.ttf", "fonts/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ],
    "DejaVu-Bold": [
        "static/fonts/DejaVuSans-Bold.ttf", "fonts/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ],
    "NotoSansVi": [
        "static/fonts/NotoSans-Regular.ttf", "fonts/NotoSans-Regular.ttf",
    ],
    "NotoSansVi-Bold": [
        "static/fonts/NotoSans-Bold.ttf", "fonts/NotoSans-Bold.ttf",
    ],
    "NotoSansHebrew": [
        "static/fonts/NotoSansHebrew-Regular.ttf", "fonts/NotoSansHebrew-Regular.ttf",
    ],
    "NotoNaskhArabic": [
        "static/fonts/NotoNaskhArabic-Regular.ttf", "fonts/NotoNaskhArabic-Regular.ttf",
    ],
}

def _registrar_ttf(nome_fonte, nome_registro):
    for p in _CAMINHOS.get(nome_fonte, []):
        try:
            if os.path.exists(p):
                pdfmetrics.registerFont(TTFont(nome_registro, p, subfontIndex=0))
                return True
        except Exception:
            continue
    return False

def registrar_tudo():
    """Registra TODAS as fontes dos 14 idiomas. Chame 1x na inicialização."""
    global _REGISTRADO
    if _REGISTRADO:
        return
    # Latinos + cirílico (ru) + turco (tr) + vietnamita (parcial)
    _registrar_ttf("DejaVu", "DejaVu")
    _registrar_ttf("DejaVu-Bold", "DejaVu-Bold")
    # Vietnamita completo (diacríticos ư, ữ, ộ...)
    _registrar_ttf("NotoSansVi", "NotoSansVi")
    _registrar_ttf("NotoSansVi-Bold", "NotoSansVi-Bold")
    # Hebraico
    _registrar_ttf("NotoSansHebrew", "NotoSansHebrew")
    # Árabe
    _registrar_ttf("NotoNaskhArabic", "NotoNaskhArabic")
    # CJK — fontes CID embutidas no ReportLab (sempre existem)
    for cid in ("HeiseiKakuGo-W5", "HeiseiMin-W3", "STSong-Light"):
        try:
            pdfmetrics.registerFont(UnicodeCIDFont(cid))
        except Exception:
            pass
    _REGISTRADO = True
    logger.info("fontes.py: registro de fontes dos 14 idiomas concluído")

# ===== MAPA ÚNICO: idioma -> (regular, bold) =====
FONTE_POR_IDIOMA = {
    "pt": ("DejaVu", "DejaVu-Bold"),
    "en": ("DejaVu", "DejaVu-Bold"),
    "es": ("DejaVu", "DejaVu-Bold"),
    "it": ("DejaVu", "DejaVu-Bold"),
    "fr": ("DejaVu", "DejaVu-Bold"),
    "de": ("DejaVu", "DejaVu-Bold"),
    "id": ("DejaVu", "DejaVu-Bold"),
    "tr": ("DejaVu", "DejaVu-Bold"),
    "ru": ("DejaVu", "DejaVu-Bold"),
    "vi": ("NotoSansVi", "NotoSansVi-Bold"),       # cai em DejaVu se Noto não existir
    "he": ("NotoSansHebrew", "NotoSansHebrew"),
    "ar": ("NotoNaskhArabic", "NotoNaskhArabic"),
    "ja": ("HeiseiKakuGo-W5", "HeiseiKakuGo-W5"),
    "zh": ("STSong-Light", "STSong-Light"),
}
IDIOMAS_RTL = {"he", "ar"}

def fonte_para(lang):
    """Única função de consulta de fonte. Nunca retorna Helvetica."""
    registrar_tudo()
    reg, bold = FONTE_POR_IDIOMA.get(lang, ("DejaVu", "DejaVu-Bold"))
    # Rede de segurança: se a fonte pedida não foi registrada, cai em DejaVu
    try:
        pdfmetrics.getFont(reg)
    except Exception:
        reg, bold = "DejaVu", "DejaVu-Bold"
    return reg, bold

# ===== SHAPING/BIDI para árabe e hebraico =====
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    _BIDI_OK = True
except Exception:
    _BIDI_OK = False

def preparar_texto(texto, lang):
    """Texto para desenhar no PDF. Árabe/hebraico recebem reshaping + bidi."""
    if not texto or lang not in IDIOMAS_RTL or not _BIDI_OK:
        return texto
    try:
        return get_display(arabic_reshaper.reshape(str(texto)))
    except Exception:
        return texto