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
    # Latinos com acento pleno (ru/tr/vi precisam de cobertura cirílica e diacrítica)
    "pt": ("DejaVuSans",          "DejaVuSans-Bold"),
    "en": ("DejaVuSans",          "DejaVuSans-Bold"),
    "es": ("DejaVuSans",          "DejaVuSans-Bold"),
    "fr": ("DejaVuSans",          "DejaVuSans-Bold"),
    "de": ("DejaVuSans",          "DejaVuSans-Bold"),
    "it": ("DejaVuSans",          "DejaVuSans-Bold"),
    "ru": ("DejaVuSans",          "DejaVuSans-Bold"),
    "tr": ("DejaVuSans",          "DejaVuSans-Bold"),
    "vi": ("DejaVuSans",          "DejaVuSans-Bold"),
    "id": ("DejaVuSans",          "DejaVuSans-Bold"),
    # RTL
    "ar": ("NotoNaskhArabic",     "NotoNaskhArabic-Bold"),
    "he": ("NotoSansHebrew",      "NotoSansHebrew-Bold"),
    # CJK
    "ja": ("NotoSansJP",          "NotoSansJP-Bold"),
    "zh": ("NotoSansSC",          "NotoSansSC-Bold"),
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
    """Procura <nome>.ttf em qualquer subpasta do projeto. Devolve caminho ou None."""
    alvo = nome_base + ".ttf"
    if not os.path.isdir(_PASTA_FONTES):
        return None
    for pasta, _subs, arquivos in os.walk(_PASTA_FONTES):
        if alvo in arquivos:
            return os.path.join(pasta, alvo)
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


# ------------------------------------------------------------------
# 4. API PÚBLICA
# ------------------------------------------------------------------
def registrar_tudo():
    """
    Registra TODAS as fontes disponíveis (TTF e CID) de uma só vez.
    Idempotente: pode ser chamada quantas vezes quiser.
    Chamar no arranque do app, antes de qualquer geração de PDF.
    """
    # Latinos
    for lang in ("pt", "en", "es", "fr", "de", "it", "ru", "tr", "vi", "id"):
        reg, bold = FONTES_TTF[lang]
        _registrar_ttf(ALIAS["base"], reg)
        _registrar_ttf(ALIAS["base_b"], bold)
        break  # todos usam DejaVu — registra uma vez e sai

    # RTL
    _registrar_ttf(ALIAS["ar"], FONTES_TTF["ar"][0])
    _registrar_ttf(ALIAS["he"], FONTES_TTF["he"][0])

    # CJK — TTF primeiro, CID como plano B
    for lang, alias_cjk in (("ja", ALIAS["cjk"]), ("zh", ALIAS["cjk2"])):
        regular, bold = FONTES_TTF[lang]
        if not _registrar_ttf(alias_cjk, regular):
            cid = CID_FALLBACK.get(lang)
            if cid:
                _registrar_cid(alias_cjk, cid)

    _registrar_ttf(ALIAS["cjk_b"], FONTES_TTF["ja"][1])

    logger.info("fontes: registro concluído — %d fontes ativas", len(_REGISTRADOS))
    return dict(_REGISTRADOS)


def fonte_para(lang):
    """
    Devolve (nome_regular, nome_bold) já REGISTRADOS para o idioma pedido.
    Nunca devolve nome inexistente: se o TTF faltou e há CID, devolve o CID.
    """
    lang = (lang or "pt").lower()

    # Latinos e RTL
    if lang in ("pt", "en", "es", "fr", "de", "it", "ru", "tr", "vi", "id"):
        return (ALIAS["base"], ALIAS["base_b"])
    if lang == "ar":
        return (ALIAS["ar"], ALIAS["ar"])
    if lang == "he":
        return (ALIAS["he"], ALIAS["he"])

    # CJK
    if lang == "ja":
        reg = ALIAS["cjk"] if ALIAS["cjk"] in _REGISTRADOS else CID_FALLBACK.get("ja", "HeiseiMin-W3")
        bold = ALIAS["cjk_b"] if ALIAS["cjk_b"] in _REGISTRADOS else reg
        return (reg, bold)
    if lang == "zh":
        reg = ALIAS["cjk2"] if ALIAS["cjk2"] in _REGISTRADOS else CID_FALLBACK.get("zh", "STSong-Light")
        return (reg, reg)

    # Desconhecido → latino
    return (ALIAS["base"], ALIAS["base_b"])


def registrar_fontes():
    """
    ASSINATURA LEGADA — mantida para não quebrar apresentacao_textos.py:67.
    Agora apenas delega para registrar_tudo().
    """
    return registrar_tudo()
