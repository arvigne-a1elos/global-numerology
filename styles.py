# -*- coding: utf-8 -*-
# styles.py - Estilos tipográficos para geração de PDF (ReportLab)

from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT

# Cores
GOLD = colors.HexColor("#C9A94E")
DARK = colors.HexColor("#1A1A1A")
GRAY = colors.HexColor("#9E9E9E")
WHITE = colors.white

# Tamanhos
TAM_T = 22
TAM_S = 14
TAM_C = 11

# Espaçamentos
ES = 8
ET = 14

def estilo(nome, size, bold, cor, align, space_before, space_after):
    return ParagraphStyle(
        nome,
        fontName="Helvetica-Bold" if bold else "Helvetica",
        fontSize=size,
        textColor=cor,
        alignment=align,
        spaceBefore=space_before,
        spaceAfter=space_after,
        leading=size * 1.4,
    )
