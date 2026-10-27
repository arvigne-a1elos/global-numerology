# -*- coding: utf-8 -*-
"""
fontes.py — Registro ÚNICO de fontes para os 14 idiomas.
Híbrido: tenta TTF real; se não encontrar o arquivo, cai no CID embutido do ReportLab.

Substitui, com uma só implementação:
  main.py (linhas 143-150)
  apresentacao_textos.py (linhas 28-30, 43-63, 624, 646)
  apresentacao_slides_v2.py (linhas 27-95)
  pdf_service.py (linhas 695-710)
"""
import os
import logging
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
# 1. PASTA DE FONTES (resolvida uma vez, à prova de reorganização)
# ------------------------------------------------------------------
_PASTA_FONTES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")

# ------------------------------------------------------------------
# 2. MAPA POR IDIOMA — (regular, bold)
#    TTF primeiro; CID é o plano B, definido em CID_FALLBACK.
# ------------------------------------------------------------------
FONTES_TTF = {
    # Latinos
    "pt": ("DejaVu", "DejaVuSans"),   # se o arquivo for DejaVuSans.ttf
    "en": ("DejaVu", "DejaVuSans"),
    "es": ("DejaVu", "DejaVuSans"),
    "fr": ("DejaVu", "DejaVuSans"),
    "de": ("DejaVu", "DejaVuSans"),
    "it": ("DejaVu", "DejaVuSans"),
    "ru": ("DejaVu", "DejaVuSans"),
    "tr": ("DejaVu", "DejaVuSans"),
    "vi": ("DejaVu", "DejaVuSans"),
    "id": ("DejaVu", "DejaVuSans"),
    # RTL
    "ar": ("NotoNaskhArabic", "NotoNaskhArabic"),
    "he": ("NotoSansHebrew",  "NotoSansHebrew"),
    # CJK
    "ja": ("NotoSansJP",      "NotoSansJP"),
    "zh": ("NotoSansSC",      "NotoSansSC"),
}

# Plano B: fontes CID embutidas no ReportLab (não exigem arquivo)
CID_FALLBACK = {
    "ja": "HeiseiMin-W3",
    "zh": "STSong-Light",
}

# Nomes de registro fixos — mantidos para compatibilidade com o código antigo
ALIAS = {
    "base":  "A1Base",
    "base_b": "A1BaseB",
    "cjk":   "A1CJK",
    "cjk_b": "A1CJKB",
    "cjk2":  "A1CJK2",
    "ar":    "A1AR",
    "he":    "A1HE",
}

_REGISTRADOS = {}   # cache: nome -> True

# ------------------------------------------------------------------
# 3. UTILITÁRIOS INTERNOS
# ------------------------------------------------------------------
def _achar_arquivo(nome_base):
    """
    Procura <base>.ttf, <base>-Regular.ttf ou <base>-Bold.ttf em fonts/ e subpastas.
    Tolerante: aceita o sufixo -Regular quando o nome-base puro não existe.
    """
    candidatos = [
        nome_base + ".ttf",
        nome_base + "-Regular.ttf",
        nome_base + "-Bold.ttf",
    ]
    if not os.path.isdir(_PASTA_FONTES):
        return None
    for pasta, _subs, arquivos in os.walk(_PASTA_FONTES):
        for cand in candidatos:
            if cand in arquivos:
                return os.path.join(pasta, cand)
    return None

def _registrar_ttf(nome_registro, nome_arquivo):
    """Registra um TTF, tolerando .ttc (subfontIndex). Devolve True se registrou."""
    if nome_registro in _REGISTRADOS:
        return True
    caminho = _achar_arquivo(nome_arquivo)
    if not caminho:
        return False
    try:
        pdfmetrics.registerFont(TTFont(nome_registro, caminho))
        _REGISTRADOS[nome_registro] = True
        return True
    except Exception:
        # pode ser .ttc — tenta como coleção
        try:
            pdfmetrics.registerFont(TTFont(nome_registro, caminho, subfontIndex=0))
            _REGISTRADOS[nome_registro] = True
            return True
        except Exception as e:
            logger.warning("fontes: falha ao registrar %s (%s): %s",
                           nome_registro, caminho, e)
            return False


def _registrar_cid(nome_registro, familia_cid):
    """Registra uma fonte CID embutida. Devolve True se registrou."""
    if nome_registro in _REGISTRADOS:
        return True
    try:
        pdfmetrics.registerFont(UnicodeCIDFont(familia_cid))
        _REGISTRADOS[nome_registro] = True
        return True
    except Exception as e:
        logger.warning("fontes: falha no CID %s (%s): %s",
                       nome_registro, familia_cid, e)
        return False

def registrar_tudo():
    """
    Registra TODAS as fontes disponíveis (TTF e CID) de uma só vez.
    Idempotente: pode ser chamada quantas vezes quiser.
    Chamar no arranque do app, antes de qualquer geração de PDF.
    """
    registrados = 0

    # ---- Latinos (registra uma única vez — todos usam a mesma DejaVu) ----
    registro, arquivo_base = FONTES_TTF["pt"]
    if _registrar_ttf(registro, arquivo_base):
        registrados += 1
    if _registrar_ttf(registro + "-Bold", arquivo_base + "-Bold"):
        registrados += 1

    # ---- RTL ----
    for lang in ("ar", "he"):
        registro, arquivo_base = FONTES_TTF[lang]
        _registrar_ttf(registro, arquivo_base)
        _registrar_ttf(registro + "-Bold", arquivo_base + "-Bold")

    # ---- CJK: TTF primeiro, CID como plano B ----
    for lang, alias_cjk in (("ja", ALIAS["cjk"]), ("zh", ALIAS["cjk2"])):
        registro, arquivo_base = FONTES_TTF[lang]
        registrou = _registrar_ttf(registro, arquivo_base)
        _registrar_ttf(registro + "-Bold", arquivo_base + "-Bold")

        # se o TTF do regular falhou, tenta o CID
        if not registrou:
            cid = CID_FALLBACK.get(lang)
            if cid:

# ------------------------------------------------------------------
# 5. CONSULTA POR IDIOMA
# ------------------------------------------------------------------
LATINOS = ("pt", "en", "es", "fr", "de", "it", "ru", "tr", "vi", "id")

# Mapa registro -> idioma (inverso do FONTES_TTF, para consulta)
_POR_REGISTRO = {
    "pt": "DejaVu",
    "ar": "NotoNaskhArabic",
    "he": "NotoSansHebrew",
    "ja": "NotoSansJP",
    "zh": "NotoSansSC",
}

def fonte_para(lang):
    """
    Devolve (nome_regular, nome_bold) já REGISTRADOS para o idioma pedido.
    Nunca devolve nome inexistente: se o TTF faltou e há CID, devolve o CID.
    """
    lang = (lang or "pt").lower()

    # Latinos
    if lang in LATINOS:
        reg = "DejaVu"
        bold = "DejaVu-Bold"
        return (reg, bold if bold in _REGISTRADOS else reg)

    # RTL
    if lang == "ar":
        reg = "NotoNaskhArabic"
        bold = "NotoNaskhArabic-Bold"
        return (reg, bold if bold in _REGISTRADOS else reg)
    if lang == "he":
        reg = "NotoSansHebrew"
        bold = "NotoSansHebrew-Bold"
        return (reg, bold if bold in _REGISTRADOS else reg)

    # CJK
    if lang == "ja":
        reg = "NotoSansJP"
        if reg not in _REGISTRADOS:
            reg = CID_FALLBACK.get("ja", "HeiseiMin-W3")
        bold = "NotoSansJP-Bold"
        return (reg, bold if bold in _REGISTRADOS else reg)
    if lang == "zh":
        reg = "NotoSansSC"
        if reg not in _REGISTRADOS:
            reg = CID_FALLBACK.get("zh", "STSong-Light")
        bold = "NotoSansSC-Bold"
        return (reg, bold if bold in _REGISTRADOS else reg)

    # Desconhecido → latino
    return fonte_para("pt")

def registrar_fontes():
    """ASSINATURA LEGADA — delega para registrar_tudo()."""
    return registrar_tudo()              
                _registrar_cid(alias_cjk, cid)

    logger.info("fontes: registro concluído — %d fontes ativas", len(_REGISTRADOS))
    return dict(_REGISTRADOS)
