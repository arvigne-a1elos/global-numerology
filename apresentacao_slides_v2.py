# -*- coding: utf-8 -*-
# apresentacao_slides_v2.py — Gerador estável de slides A1ELOS Global Numerology
# VERSÃO 2.1 — 16/10/2026
# Correções desta versão (nada de conteúdo muda):
#   1) Cards em 2 linhas (título em cima, descrição embaixo) + grid de largura exata
#      => fim dos cortes na borda direita (págs. 4, 6, 8, 9, 11)
#   2) Gráfico de projeções com altura calculada (fim da sobreposição na pág. 14);
#      Tração migrou para a pág. 15; Referências migraram para a pág. 17
#   3) SEGUNDA LOGO no cabeçalho: static/A1ELOS.png no lado direito
#   4) Textos lidos do apresentacao_textos.py (prioridade: idioma > pt > padrão interno)
# 17 páginas fixas · 14 idiomas · numeração "X de 17" · sem sobreposição · sem evasão
# Dependências: reportlab (opcional p/ árabe: arabic-reshaper python-bidi)

import os, logging
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                KeepInFrame, PageBreak, Image)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing, Rect, String

# ===== 1. FONTES =====
_CAND = {
    "dejavu":   ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                 "/usr/share/fonts/dejavu/DejaVuSans.ttf"],
    "dejavu_b": ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                 "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf"],
    "cjk":      ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
                 "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"],
    "arab":     ["/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf",
                 "/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf"],
    "hebr":     ["/usr/share/fonts/truetype/noto/NotoSansHebrew-Regular.ttf"],
}
def _primeiro(cands):
    for p in cands:
        if os.path.exists(p): return p
    return None

def _registrar_fontes():
    reg = bold = cjk = arab = hebr = None
    p = _primeiro(_CAND["dejavu"])
    if p: pdfmetrics.registerFont(TTFont("A1Base", p)); reg = "A1Base"
    p = _primeiro(_CAND["dejavu_b"])
    if p: pdfmetrics.registerFont(TTFont("A1BaseB", p)); bold = "A1BaseB"
    p = _primeiro(_CAND["cjk"])
    if p:
        try:
            pdfmetrics.registerFont(TTFont("A1CJK", p, subfontIndex=0)); cjk = "A1CJK"
        except Exception:
            try:
                pdfmetrics.registerFont(TTFont("A1CJK", p)); cjk = "A1CJK"
            except Exception: cjk = None
    p = _primeiro(_CAND["arab"])
    if p: pdfmetrics.registerFont(TTFont("A1AR", p)); arab = "A1AR"
    p = _primeiro(_CAND["hebr"])
    if p: pdfmetrics.registerFont(TTFont("A1HE", p)); hebr = "A1HE"
    return reg, bold, cjk, arab, hebr

REG, BOLD, F_CJK, F_AR, F_HE = _registrar_fontes()
REG = REG or "Helvetica"; BOLD = BOLD or "Helvetica-Bold"

FONTES_IDIOMA = {
    "pt": (REG, BOLD, False), "en": (REG, BOLD, False), "es": (REG, BOLD, False),
    "it": (REG, BOLD, False), "fr": (REG, BOLD, False), "de": (REG, BOLD, False),
    "id": (REG, BOLD, False), "tr": (REG, BOLD, False), "vi": (REG, BOLD, False),
    "ja": (F_CJK or REG, F_CJK or REG, False), "zh": (F_CJK or REG, F_CJK or REG, False),
    "he": (F_HE or REG, F_HE or REG, True), "ar": (F_AR or REG, F_AR or REG, True),
}
IDIOMAS = list(FONTES_IDIOMA.keys())

def _rtl(texto, lang):
    if lang not in ("ar", "he"): return texto
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        return get_display(arabic_reshaper.reshape(texto))
    except Exception:
        return texto

# ===== 2. GEOMETRIA =====
LARG, ALT = landscape(A4)
MARG = 13 * mm
LARG_UTIL = LARG - 2 * MARG
TOPO_BANDA = 16 * mm
PE_BANDA = 13 * mm
ALT_UTIL = ALT - TOPO_BANDA - PE_BANDA - 6 * mm

# ===== 3. CORES =====
OURO      = colors.HexColor("#C9A94E")
OURO_ESC  = colors.HexColor("#8A7430")
TINTA     = colors.HexColor("#1A1A1A")
CINZA     = colors.HexColor("#666666")
LINHA     = colors.HexColor("#D9CFA8")
ZEBRA     = colors.HexColor("#F7F3E6")
FUNDO_BOX = colors.HexColor("#FBF7EA")

# ===== 4. PADRÃO INTERNO (pt) — usado SOMENTE quando o apresentacao_textos não tem a chave =====
PADRAO_PT = {
    "capa_titulo": "A1ELOS Global Numerology",
    "capa_sub": "A ciência dos números aplicada ao seu sucesso",
    "capa_nota": "Apresentação Estratégica para Investidores e Parceiros",
    "capa_linha": "24 Produtos · 14 Idiomas · ~5,3 bilhões de falantes · IA integrada",
    "capa_conf": "CONFIDENCIAL · DUNS 942242668 · 2026",
    "sum_titulo": "Sumário Executivo",
    "sum_intro": "Esta apresentação guia investidores e parceiros por todos os aspectos estratégicos da A1ELOS Global Numerology — da tese de mercado ao modelo de receita recorrente.",
    "sum_itens": [("01","Sobre a A1ELOS","Holding, portfólio e credencial DUNS"),
                  ("02","Oportunidade de Mercado","Bem-estar global US$ 6,8 tri + RH Corporativo"),
                  ("03","Solução e Alcance Global","14 idiomas, ~5,3 bi de falantes"),
                  ("04","Novos Mercados","Indonésia, Turquia, Vietnã e RH"),
                  ("05","Portfólio e Preços","24 produtos por poder aquisitivo"),
                  ("06","Receita Recorrente","Banners e Pacotes B2B"),
                  ("07","Projeções e Investimento","Anos 1–5 · Rodada Seed R$ 3,5M")],
    "sobre_titulo": "Sobre a A1ELOS",
    "sobre_texto": "A A1ELOS é uma holding de tecnologia e conhecimento que une inteligência artificial, numerologia aplicada e estratégia cultural para criar produtos digitais de alto impacto em escala global. Missão: democratizar o autoconhecimento numérico com respeito cultural e ao poder aquisitivo de cada mercado.",
    "sobre_kpis": [("24","Produtos Ativos"),("14","Idiomas"),("5,3B","Falantes"),("IA","Integrada")],
    "sobre_duns": "DUNS 942242668 — Certificação Dun & Bradstreet válida em 190+ países, habilitando contratos B2B e joint ventures internacionais.",
    "mercado_titulo": "Oportunidade de Mercado",
    "mercado_texto": "Vivemos a convergência perfeita: o bem-estar digital explode globalmente enquanto a numerologia e astrologia migram para apps de alto engajamento. A A1ELOS está posicionada exatamente nessa interseção, com 74% da população mundial já online (~6 bilhões de pessoas).",
    "mercado_cards": [("Bem-Estar Global","US$ 6,8 tri → US$ 9,8 tri até 2029 (+7,6% a.a.)"),
                      ("Apps Astrologia/Numerologia","US$ 3 bi → US$ 9 bi até 2030 · CAGR 20%"),
                      ("Apps de Bem-Estar","CAGR 14,9% → US$ 26,2 bi em 2030"),
                      ("Usuários Online","74% do mundo · ~6 bilhões de pessoas")],
    "mercado_rh_titulo": "Novo Mercado: RH Corporativo — o 24º Produto",
    "mercado_rh_cards": [("HR Tech","US$ 42,34 bi (2025) → US$ 77,74 bi (2031) · CAGR 10,35%"),
                         ("Employer Branding","US$ 1,89 bi (2025) → US$ 3,62 bi (2031) · CAGR 11,19%"),
                         ("Corporate Wellness","US$ 66,31 bi (2025) → US$ 94,5 bi (2031) · CAGR 6,12%")],
    "problema_titulo": "O Problema que Resolvemos",
    "problema_col_esq_titulo": "Falhas do Mercado Atual",
    "problema_col_esq": [("Barreira de Idioma","A maioria das ferramentas opera apenas em inglês, excluindo bilhões de falantes nativos."),
                         ("Preços Descolados da Realidade","Cobrança em dólar exclui mercados emergentes — o usuário não rejeita o produto, rejeita o preço inacessível."),
                         ("Ausência de Profundidade","Ferramentas genéricas entregam respostas superficiais, sem contexto cultural e sem aplicação prática.")],
    "problema_col_dir_titulo": "O Custo da Exclusão",
    "problema_col_dir": "Quando uma plataforma ignora idioma e poder aquisitivo, ela abandona o maior mercado do mundo: os 4+ bilhões de pessoas em economias emergentes.",
    "problema_destaque": "Plataformas que ignoram poder aquisitivo local perdem acesso a mais de 60% do mercado endereçável global.",
    "solucao_titulo": "Nossa Solução: 3 Pilares Estratégicos",
    "solucao_texto": "A A1ELOS combina ciência numérica, inteligência artificial e sensibilidade cultural em uma plataforma integrada, com receita diversificada e alta retenção.",
    "solucao_colunas": [("Mapas Pessoais","Análises numéricas profundas e personalizadas — identidade, missão, ciclos de vida e compatibilidade — em 14 idiomas com IA integrada."),
                ("Numerologia Empresarial","Diagnósticos aplicados a marcas, CNPJs, datas de fundação e estratégia corporativa — alto valor percebido no B2B."),
                ("White-Label B2B","Licenciamento da plataforma para empresas parceiras oferecerem numerologia sob sua própria marca.")],
    "alcance_titulo": "Alcance Global: 14 Idiomas · ~5,3 Bilhões de Falantes",
    "alcance_texto": "A A1ELOS cobre ~67% da população mundial com uma plataforma genuinamente multilíngue, com precificação calibrada ao poder aquisitivo local.",
    "idioma_col": "Idioma", "falantes_col": "Falantes (mi)", "total_linha": "TOTAL",
    "linhas_idiomas": [["Inglês","1.528"],["Mandarim","1.184"],["Espanhol","558"],["Francês","396"],
                       ["Árabe","335"],["Português","270"],["Russo","255"],["Indonésio","255"],
                       ["Alemão","134"],["Japonês","123"],["Vietnamita","97"],["Turco","90"],
                       ["Italiano","85"],["Hebraico","9"]],
    "novos_titulo": "Os 3 Novos Mercados: +442 Milhões de Falantes",
    "novos_texto": "Expansão para mercados com alto crescimento econômico, penetração digital crescente e demanda comprovada por bem-estar digital acessível.",
    "novos_cards": [("Indonésia","285 mi habitantes · 80,5% de internet · ~255 mi falantes · Bem-estar: US$ 51,2 bi → US$ 72,8 bi (2034)"),
                    ("Turquia","85,9 mi habitantes · PIB PPP per capita US$ 37.301 (acima da média mundial) · ~90 mi falantes"),
                    ("Vietnã","~100 mi habitantes · PIB per capita ~US$ 5.066 (+7,4%/ano) · ~97 mi falantes · Bem-estar: US$ 303 mi → US$ 485 mi (2030)")],
    "mercados_rodape": "3 mercados novos = +442 milhões de novos falantes endereçáveis — incorporados com precificação culturalmente calibrada.",
    "preco_titulo": "Filosofia de Preço Consciente",
    "preco_texto": "Respeito cultural + respeito ao poder aquisitivo = mercado endereçável real. O esforço financeiro é proporcional à renda local (Paridade de Poder de Compra).",
    "preco_cards": [("Calibração por PPC","Preços ajustados ao índice de poder aquisitivo de cada país"),
                    ("Respeito Cultural","Idioma, moeda e contexto local integrados ao produto"),
                    ("Conversão Superior","Preço justo gera mais conversão e maior retenção de longo prazo")],
    "portfolio_titulo": "Portfólio: 24 Produtos em 4 Níveis",
    "portfolio_texto": "Cada perfil de usuário encontra uma oferta adequada ao seu nível de engajamento e capacidade financeira. Relatórios PDF premium com QRCode e análise IA.",
    "portfolio_tabela": [["Nível","Produtos","Faixa","Perfil"],
                         ["Básico","Mapa Express, Mapa Completo","R$ 8–17","Primeiro contato"],
                         ["Intermediário","Pesquisa IA, Nome de Urna, Nº Eleitoral","R$ 8–26","Usuário engajado"],
                         ["Avançado","Nome de ONG, Artístico, Bebê, Assinatura, Negócio","R$ 35–44","Profissional"],
                         ["Premium","Casal, Família, Compatibilidade de Equipes RH ★, Coletivo","R$ 98","Corporativo"],
                         ["B2B","Pacotes Empresariais, licenças, brindes","Sob consulta","Empresas"]],
    "portfolio_rodape": "24 produtos cobrem toda a jornada do usuário — maximizando LTV por idioma e mercado. Destaque: Compatibilidade de Equipes RH (R$ 98), energia ideal 8.",
    "destaque_titulo": "Destaque: Compatibilidade de Equipes (RH)",
    "destaque_selo": "NOVO PRODUTO · RH · R$ 98 · ENERGIA IDEAL: 8",
    "destaque_texto": "Desenvolvido para Departamentos de Recursos Humanos que buscam alinhar líderes e colaboradores, aumentar a produtividade e reduzir conflitos internos.",
    "destaque_cards": [("Chefe × Membros","Compatibilidade energética entre o líder e cada membro individualmente."),
                       ("Membros × Membros","Afinidades e tensões energéticas entre todos os colaboradores."),
                       ("Compatibilidade de Pares","Relatório para duplas estratégicas: parceiros, sócios ou co-líderes."),
                       ("PDF + QRCode","Relatório premium com marca d'água dourada e análise IA completa.")],
    "modelo_titulo": "Modelo de Negócio: 3 Fontes de Receita",
    "modelo_itens": [("B2C — 14 Idiomas","Venda direta em todas as moedas, com PPC. Escala automática via IA. Participação: 60%"),
                     ("B2B — Descontos Progressivos","Pacotes para RH, employer branding e brindes. 10% a 50% conforme volume. Participação: 25%"),
                     ("Publicidade Geolocalizada","Banners por país, continente ou mundial, com rotação automatizada. Participação: 15%")],
    "banners_titulo": "Banners Publicitários — Receita Recorrente Mensal",
    "banners_tabela": [["Segmentação","Fixo (R$/mês)","Temporário (R$/mês)","Perfil"],
                       ["País","R$ 800","R$ 500","PMEs locais"],
                       ["Continente","R$ 1.800","R$ 1.200","Marcas regionais"],
                       ["Mundo","R$ 3.500","R$ 2.500","Empresas globais"],
                       ["Patrocínio Exclusivo","R$ 6.000","R$ 4.500/campanha","Patrocinadores master"]],
    "banners_nota": "728×90 px desktop · 320×100 px mobile · rotação a cada 8 segundos · geo-alvo país/continente/mundo",
    "b2b_titulo": "Pacotes Empresariais B2B + Descontos Progressivos",
    "b2b_texto": "Planos para programas de benefícios, integração de equipes e fidelização. Acima de 2.000 códigos: Plano Diamante, negociação direta (até 70%).",
    "b2b_tabela": [["A partir de","Desconto","Perfil","Uso recomendado"],
                   ["10 códigos","10%","Pequenas equipes","Ação pontual de bem-estar"],
                   ["50 códigos","20%","Equipes em crescimento","Programas recorrentes"],
                   ["100 códigos","25%","PMEs","Benefício trimestral"],
                   ["200 códigos","30%","Empresas médias","Programas completos"],
                   ["500 códigos","40%","Médias empresas","Brinde anual"],
                   ["1.000 códigos","45%","Grandes corporações","Fidelização de clientes"],
                   ["2.000 códigos","50%","Grandes grupos","Larga escala"],
                   ["Acima de 2.000","Negociável","Plano Diamante","Distribuição em volume"]],
    "projecoes_titulo": "Projeções Financeiras: Curto Prazo (Anos 1–5)",
    "projecoes_texto": "Base: penetração percentual sobre ~5,32 bilhões de falantes, conversão conservadora de 3% e resgate de bônus entre 70% e 90%. Ancorada em mercados verificados: HR Tech, Employer Branding e Corporate Wellness.",
    "projecoes": [("Ano 1","R$ 318k","R$ 810k"),("Ano 2","R$ 630k","R$ 1,8M"),
                  ("Ano 3","R$ 1,20M","R$ 3,50M"),("Ano 4","R$ 2,2M","R$ 6,2M"),
                  ("Ano 5","R$ 3,70M","R$ 9,6M")],
    "graf_cons": "Conservador", "graf_otim": "Otimista",
    "tracao_titulo": "Tração e Resultados Comprovados",
    "tracao_metricas": [("12K+","Usuários Ativos"),("87%","Retenção"),("4,8★","Avaliação Média"),("23","Parceiros B2B")],
    "roteiro_titulo": "Roteiro Estratégico",
    "roteiro_texto": "Um plano em quatro fases progressivas — da consolidação da base atual à liderança global de mercado.",
    "roteiro_itens": [("Fase 1 · Consolidação","Base de usuários nos idiomas ativos. Otimização de conversão, retenção e LTV. Rodada Seed concluída."),
                      ("Fase 2 · Expansão","Lançamento em Indonésia, Turquia e Vietnã. Aceleração do canal B2B e publicidade."),
                      ("Fase 3 · Entrada Global","Presença nos 14 idiomas com campanhas localizadas. White-label em 5+ continentes. Série A."),
                      ("Fase 4 · Liderança","20+ países consolidados. SaaS de referência global. IPO ou exit estratégico.")],
    "invest_titulo": "Investimento & Contato",
    "invest_texto": "Prontos para apresentações privadas, due diligence e negociações.",
    "invest_metricas": [("R$ 3,5 mi","Rodada Seed"),("R$ 14 mi","Valuation Pré-Money"),("Até 20%","Equity Ofertado")],
    "invest_contato": [("E-mail Investidores","a1elos.consultoria@gmail.com"),
                       ("E-mail Geral","contato@a1elos.com"),
                       ("Website","www.a1elos.com"),
                       ("DUNS","942242668 — Dun & Bradstreet")],
    "invest_aloc": "Alocação do Capital: 45% Tecnologia · 30% Marketing · 25% Operações",
    "pix_titulo": "Brasil: A Infraestrutura Pix",
    "pix_texto": "O Pix garante cobrança imediata, baixo custo e aceitação universal — o alicerce da operação B2C no Brasil.",
    "pix_metricas": [("30,1 bi","Transações em 2025"),("76,4%","da população usa Pix"),
                     ("R$ 68,2 tri","movimentados no 2º sem. 2025"),("~80 bi","transações em 2025")],
    "pix_fontes": "Fontes: Banco Central do Brasil (Pix em Números) e Febraban (Pesquisa de Tecnologia Bancária).",
    "ref_titulo": "Referências Bibliográficas",
    "ref_intro": "Fontes utilizadas para os dados de mercado, projeções e indicadores desta apresentação.",
    "ref_itens": [("Global Wellness Institute","Bem-estar global: US$ 6,8 tri (2024) → US$ 9,8 tri (2029)."),
                  ("MarkNtel Advisors","Apps de astrologia/numerologia: US$ 3 bi → US$ 9 bi até 2030 (CAGR ~20%)."),
                  ("FMI · Banco Mundial","PIB e paridade do poder de compra (PPP) por país."),
                  ("Banco Central do Brasil","Estatísticas oficiais do Pix."),
                  ("Febraban","Pesquisa de Tecnologia Bancária — crescimento do Pix em 2025."),
                  ("IBGE","População e indicadores socioeconômicos do Brasil.")],
    "final_frase": "Os números nunca mentem.",
    "final_linha": "DUNS 942242668 · 24 PRODUTOS · 14 IDIOMAS · ~5,3 BI FALANTES",
}

# ===== 4b. LEITURA DOS TEXTOS: apresentacao_textos.py > PADRAO_PT =====
_CONTEUDO = None
def _conteudo():
    global _CONTEUDO
    if _CONTEUDO is None:
        try:
            from apresentacao_textos import CONTEUDO as _C
            _CONTEUDO = dict(_C)
        except Exception:
            _CONTEUDO = {}
        try:
            from apresentacao_traducoes_v2 import TRADUCOES as _T
            for _l, _b in _T.items():
                _CONTEUDO[_l] = {**_CONTEUDO.get(_l, {}), **_b}
        except Exception:
            pass
    return _CONTEUDO

def C(lang, *chaves):
    """Tenta cada chave em CONTEUDO[lang], depois CONTEUDO['pt']; fallback PADRAO_PT na última chave."""
    cd = _conteudo()
    for ch in chaves:
        v = cd.get(lang, {}).get(ch)
        if v is not None: return v
        v = cd.get("pt", {}).get(ch)
        if v is not None: return v
    return PADRAO_PT.get(chaves[-1], "")

def _seq(v):
    return list(v) if isinstance(v, (list, tuple)) else []

# ===== HARDENING =====
def _norm_pairs(itens):
    saida = []
    for it in (itens or []):
        if isinstance(it, str):
            saida.append((it, ""))
        elif isinstance(it, (list, tuple)):
            if len(it) >= 3:
                saida.append((str(it[0]), "%s · %s" % (it[1], it[2])))
            elif len(it) == 2:
                v = it[1]
                if isinstance(v, (list, tuple)):
                    v = " · ".join(str(x) for x in v)
                saida.append((str(it[0]), str(v)))
            elif len(it) == 1:
                saida.append((str(it[0]), ""))
        elif isinstance(it, dict):
            saida.append((str(it.get("titulo") or it.get("nome") or ""),
                          str(it.get("texto") or it.get("valor") or it.get("desc") or "")))
    return saida

def _norm_metrics(itens):
    saida = []
    for it in (itens or []):
        if isinstance(it, str):
            saida.append((it, ""))
        elif isinstance(it, (list, tuple)) and len(it) >= 2:
            saida.append((str(it[0]), str(it[1])))
        elif isinstance(it, (list, tuple)) and len(it) == 1:
            saida.append((str(it[0]), ""))
    return saida

def _norm_rows(dados):
    if not dados:
        return [[""]]
    ncol = max(len(r) if isinstance(r, (list, tuple)) else 1 for r in dados)
    out = []
    for r in dados:
        if isinstance(r, (list, tuple)):
            r = [str(c) for c in r] + [""] * (ncol - len(r))
        else:
            r = [str(r)] + [""] * (ncol - 1)
        out.append(r[:ncol])
    return out

def _norm_metrics3(p):
    saida = []
    for it in (p or []):
        if isinstance(it, (list, tuple)):
            saida.append((str(it[0]), str(it[1]) if len(it) > 1 else "",
                          str(it[2]) if len(it) > 2 else ""))
        elif isinstance(it, str):
            saida.append((it, "", ""))
    return saida

def _anos_proj(lang):
    dados = _seq(C(lang, "projecoes_curto_tabela", "projecoes_tabela", "projecoes"))
    saida = []
    for r in dados:
        if isinstance(r, (list, tuple)) and len(r) >= 3 and str(r[0]).lower() != "horizonte":
            saida.append([str(r[0]), str(r[1]), str(r[2])])
    return saida or [list(x) for x in PADRAO_PT["projecoes"]]

def _tabela_alcance(lang):
    idi = _seq(C(lang, "linhas_idiomas"))
    if idi and all(isinstance(x, (list, tuple)) and len(x) >= 2 for x in idi):
        ci = str(C(lang, "idioma_col") or "Idioma")
        cf = str(C(lang, "falantes_col") or "Falantes (mi)")
        linhas, i = [], 0
        while i < len(idi):
            a = idi[i]
            b = idi[i + 1] if i + 1 < len(idi) else ["", ""]
            linhas.append([str(a[0]), str(a[1]), str(b[0]), str(b[1])])
            i += 2
        linhas.append([str(C(lang, "total_linha") or "TOTAL"), str(C(lang, "total_dado") or "~5.320 (milhões)"), str(C(lang, "falantes_col") or "Falantes"), "—"])
        return [[ci, cf, ci, cf]] + linhas
    return PADRAO_PT["alcance_tabela"]

# ===== 5. ESTILOS =====
def _estilo(fonte, tam, cor=TINTA, al=TA_LEFT, bold=False, leading=None, rtl=False):
    return ParagraphStyle("s", fontName=(BOLD if bold else fonte), fontSize=tam,
                          leading=leading or tam * 1.25, textColor=cor, alignment=al,
                          wordWrap=("RTL" if rtl else "CJK" if fonte == F_CJK else None))

# ===== 6. COMPONENTES =====
def _kif(fluxo):
    fluxo = [f for f in fluxo if f is not None]
    if not fluxo:
        fluxo = [Spacer(1, 1)]
    return KeepInFrame(LARG_UTIL, ALT_UTIL - 8 * mm, fluxo, mode="shrink")

def _titulo(lang, texto):
    f, _, rtl = FONTES_IDIOMA.get(lang, (REG, BOLD, False))
    return [Paragraph(_rtl(str(texto), lang), _estilo(f, 20, OURO_ESC, bold=True, rtl=rtl)),
            Table([[""]], colWidths=[LARG_UTIL], rowHeights=[1.2],
                  style=TableStyle([("BACKGROUND",(0,0),(-1,-1),OURO)])),
            Spacer(1, 4 * mm)]

def _para(lang, texto, tam=9.5, cor=TINTA, al=TA_LEFT, bold=False, esp=None):
    f, _, rtl = FONTES_IDIOMA.get(lang, (REG, BOLD, False))
    return Paragraph(_rtl(str(texto or ""), lang), _estilo(f, tam, cor, al, bold, esp))

def _cards(lang, itens, colunas=2, tam_titulo=10, tam_desc=8):
    # CORREÇÃO v2.1: cartão em 2 LINHAS (título / descrição) e grid de largura exata.
    itens = _norm_pairs(itens)
    f, _, rtl = FONTES_IDIOMA.get(lang, (REG, BOLD, False))
    al = TA_RIGHT if rtl else TA_LEFT
    larg_col = LARG_UTIL / colunas
    linhas, linha = [], []
    for t, d in itens:
        cel = Table([[Paragraph(_rtl(t, lang), _estilo(f, tam_titulo, OURO_ESC, al, True))],
                     [Paragraph(_rtl(d, lang), _estilo(f, tam_desc, TINTA, al, leading=tam_desc*1.35))]],
                    colWidths=[larg_col - 3*mm], style=TableStyle([
                        ("BACKGROUND",(0,0),(-1,-1),FUNDO_BOX),
                        ("BOX",(0,0),(-1,-1),0.8,OURO),
                        ("LEFTPADDING",(0,0),(-1,-1),2.5*mm),("RIGHTPADDING",(0,0),(-1,-1),2.5*mm),
                        ("TOPPADDING",(0,0),(-1,0),2.2*mm),("BOTTOMPADDING",(0,0),(-1,0),1.0*mm),
                        ("TOPPADDING",(0,1),(-1,1),0.4*mm),("BOTTOMPADDING",(0,1),(-1,1),2.2*mm)]))
        linha.append(cel)
        if len(linha) == colunas: linhas.append(linha); linha = []
    if linha:
        while len(linha) < colunas: linha.append("")
        linhas.append(linha)
    g = Table(linhas, colWidths=[larg_col] * colunas, hAlign="LEFT",
              style=TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),
                                ("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),
                                ("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),1.8*mm)]))
    return KeepInFrame(LARG_UTIL, ALT_UTIL * 0.9, [g], mode="shrink")

def _tabela(lang, dados, larguras=None, tam=8, zebra=True):
    dados = _norm_rows(dados)
    f, _, rtl = FONTES_IDIOMA.get(lang, (REG, BOLD, False))
    al = TA_RIGHT if rtl else TA_LEFT
    if larguras and len(larguras) != len(dados[0]):
        larguras = None
    if not larguras:
        larguras = [LARG_UTIL / len(dados[0])] * len(dados[0])
    escala = LARG_UTIL / sum(larguras); larguras = [w * escala for w in larguras]
    corpo = [[Paragraph(_rtl(str(c), lang), _estilo(f, tam, colors.white, al, True))
              for c in dados[0]]]
    for r in dados[1:]:
        corpo.append([Paragraph(_rtl(str(c), lang), _estilo(f, tam, TINTA, al)) for c in r])
    est = [("BACKGROUND",(0,0),(-1,0),OURO_ESC),
           ("GRID",(0,0),(-1,-1),0.4,LINHA),
           ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
           ("LEFTPADDING",(0,0),(-1,-1),2*mm),("RIGHTPADDING",(0,0),(-1,-1),2*mm),
           ("TOPPADDING",(0,0),(-1,-1),1.4*mm),("BOTTOMPADDING",(0,0),(-1,-1),1.4*mm)]
    if zebra:
        for i in range(1, len(corpo)):
            if i % 2 == 0: est.append(("BACKGROUND",(0,i),(-1,i),ZEBRA))
    t = Table(corpo, colWidths=larguras, repeatRows=1, style=TableStyle(est), hAlign="LEFT")
    return KeepInFrame(LARG_UTIL, ALT_UTIL * 0.9, [t], mode="shrink")

def _metricas(lang, itens, tam_num=17, tam_lab=7.5):
    itens = _norm_metrics(itens)
    if not itens: return Spacer(1, 0)
    f, _, rtl = FONTES_IDIOMA.get(lang, (REG, BOLD, False))
    larg = LARG_UTIL / len(itens)
    linha = [Table([[Paragraph(_rtl(v, lang), _estilo(f, tam_num, OURO_ESC, TA_CENTER, True))],
                    [Paragraph(_rtl(l, lang), _estilo(f, tam_lab, CINZA, TA_CENTER))]],
                   colWidths=[larg - 3*mm], style=TableStyle([
                       ("BACKGROUND",(0,0),(-1,-1),FUNDO_BOX),("BOX",(0,0),(-1,-1),0.8,OURO),
                       ("TOPPADDING",(0,0),(-1,0),2*mm),("BOTTOMPADDING",(0,-1),(-1,-1),2*mm)]))
            for v, l in itens]
    g = Table([linha], colWidths=[larg]*len(itens), style=TableStyle(
        [("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),1.5*mm),
         ("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0)]))
    return KeepInFrame(LARG_UTIL, 40*mm, [g], mode="shrink")

def _duas_colunas(lang, esq_t, esq_fluxo, dir_t, dir_fluxo):
    larg = (LARG_UTIL - 4*mm) / 2
    g = Table([[esq_fluxo, dir_fluxo]], colWidths=[larg, larg], style=TableStyle(
        [("VALIGN",(0,0),(-1,-1),"TOP"),
         ("LINEBEFORE",(1,0),(1,0),0.6,LINHA),
         ("LEFTPADDING",(1,0),(1,0),3*mm),("RIGHTPADDING",(0,0),(0,0),3*mm)]))
    return KeepInFrame(LARG_UTIL, ALT_UTIL * 0.85, [g], mode="shrink")

def _lista_pares(lang, itens, tam=8.5):
    itens = _norm_pairs(itens)
    f, _, rtl = FONTES_IDIOMA.get(lang, (REG, BOLD, False))
    fluxo = []
    for t, d in itens:
        fluxo.append(Paragraph(_rtl("◆ " + t, lang), _estilo(f, tam, OURO_ESC, bold=True)))
        if d:
            fluxo.append(Paragraph(_rtl(d, lang), _estilo(f, tam - 0.5, TINTA)))
        fluxo.append(Spacer(1, 2*mm))
    return fluxo

def _barras(lang, projecoes):
    # CORREÇÃO v2.1: altura calculada a partir do nº de anos (fim da sobreposição).
    projecoes = _norm_metrics3(projecoes)
    if not projecoes: return Spacer(1, 0)
    f, _, rtl = FONTES_IDIOMA.get(lang, (REG, BOLD, False))
    def _num(s):
        s = str(s).strip()
        limpo = "".join(ch for ch in s if ch.isdigit() or ch in "kKmM,.")
        mult = 1.0
        if ("M" in limpo) or ("m" in limpo):
            mult = 1000000.0
            limpo = limpo.replace("M", "").replace("m", "")
        elif ("k" in limpo) or ("K" in limpo):
            mult = 1000.0
            limpo = limpo.replace("k", "").replace("K", "")
        if mult > 1.0 and ("," in limpo or "." in limpo):
            pos = max(limpo.rfind(","), limpo.rfind("."))
            inteiro = limpo[:pos].replace(".", "").replace(",", "")
            frac = limpo[pos + 1:]
            limpo = inteiro + "." + frac
        else:
            limpo = limpo.replace(".", "").replace(",", "")
        try:
            return float(limpo) * mult
        except Exception:
            return 0.0

# ===== 7. CABEÇALHO / RODAPÉ — DUAS LOGOS =====
_LOGO_CANDIDATOS = ["static/logo.png", "static/Logo-A1ELOS.png", "static/logo-a1elos.png",
                    "static/img/logo.png", "logo.png"]
_LOGO2_CANDIDATOS = ["static/A1ELOS.png", "static/Logo-A1ELOS.png", "static/logo-a1elos.png",
                     "static/logo.png", "logo.png"]

def _logo(canvas, x, y, tam=9*mm):
    for p in _LOGO_CANDIDATOS:
        if os.path.exists(p):
            try: canvas.drawImage(p, x, y, tam, tam, preserveAspectRatio=True, mask="auto"); return
            except Exception: break
    canvas.saveState()
    canvas.setFillColor(OURO); canvas.circle(x + tam/2, y + tam/2, tam/2, fill=1, stroke=0)
    canvas.setFillColor(colors.white); canvas.setFont(BOLD, 8)
    canvas.drawCentredString(x + tam/2, y + tam/2 - 2.6, "A1")
    canvas.restoreState()

def _logo2(canvas, tam=8*mm):
    """SEGUNDA LOGO — lado direito do cabeçalho (static/A1ELOS.png)."""
    x = LARG - MARG - tam
    y = ALT - TOPO_BANDA + 1.5*mm
    for p in _LOGO2_CANDIDATOS:
        if os.path.exists(p):
            try:
                canvas.drawImage(p, x, y, tam, tam, preserveAspectRatio=True, mask="auto")
                return
            except Exception:
                break
    canvas.saveState()
    canvas.setFillColor(OURO); canvas.circle(x + tam/2, y + tam/2, tam/2, fill=1, stroke=0)
    canvas.setFillColor(colors.white); canvas.setFont(BOLD, 7)
    canvas.drawCentredString(x + tam/2, y + tam/2 - 2.2, "A1")
    canvas.restoreState()

def _page_decor(canvas, doc, lang):
    canvas.saveState()
    total = getattr(doc, "_total_paginas", 17)
    pagina = canvas.getPageNumber()
    if pagina > 1:
        _logo(canvas, MARG, ALT - TOPO_BANDA + 1.5*mm)          # logo 1 (esquerda)
        canvas.setFillColor(TINTA); canvas.setFont(BOLD, 11)
        canvas.drawString(MARG + 12*mm, ALT - TOPO_BANDA + 4.2*mm, "A1ELOS Global Numerology")
        canvas.setFillColor(CINZA); canvas.setFont(REG, 7.5)
        canvas.drawString(MARG + 12*mm, ALT - TOPO_BANDA + 1.2*mm, "DUNS 942242668 · CONFIDENCIAL")
        _logo2(canvas)                                          # logo 2 (direita) — A1ELOS.png
        canvas.setFillColor(OURO_ESC); canvas.setFont(BOLD, 7.5)
        canvas.drawRightString(LARG - MARG - 11*mm, ALT - TOPO_BANDA + 2.8*mm, "D&B · 190+ PAÍSES")
        canvas.setStrokeColor(OURO); canvas.setLineWidth(1)
        canvas.line(MARG, ALT - TOPO_BANDA, LARG - MARG, ALT - TOPO_BANDA)
    canvas.setStrokeColor(LINHA); canvas.setLineWidth(0.6)
    canvas.line(MARG, PE_BANDA + 4*mm, LARG - MARG, PE_BANDA + 4*mm)
    canvas.setFillColor(CINZA); canvas.setFont(REG, 6.8)
    canvas.drawString(MARG, PE_BANDA + 1.2*mm,
        "A1ELOS Global Numerology · DUNS 942242668 · CONFIDENCIAL 2026")
    canvas.drawString(MARG, PE_BANDA - 2.4*mm,
        "a1elos.consultoria@gmail.com · arvigne@a1elos.com.br · a1elos.com.br/contato")
    canvas.setFillColor(OURO_ESC); canvas.setFont(BOLD, 7.5)
    canvas.drawRightString(LARG - MARG, PE_BANDA + 1.2*mm, "%d de %d" % (pagina, total))
    canvas.restoreState()

# ===== 8. PLANO DE PÁGINAS (17 fixas) =====
def _plano(lang):
    P = []
    P.append({"tipo":"capa"})
    P.append({"tipo":"geral","titulo":C(lang,"sumario_titulo","sum_titulo"),
              "intro":C(lang,"sumario_intro","sum_intro"),
              "corpo":[("tabela",(_seq(C(lang,"sumario_header")) or [["#","Seção","Conteúdo"]]) + _seq(C(lang,"sumario_cards","sum_itens")),
                       [1.0, 3.2, 7.2], 8.5)]})
    P.append({"tipo":"geral","titulo":C(lang,"sobre_titulo"),"intro":C(lang,"sobre_texto"),
              "corpo":[("metricas",C(lang,"sobre_kpis","sobre_metricas")),
                       ("texto",C(lang,"sobre_duns"))]})
    P.append({"tipo":"geral","titulo":C(lang,"mercado_titulo"),"intro":C(lang,"mercado_texto"),
              "corpo":[("cards",_seq(C(lang,"mercado_cards")),4),
                       ("subtitulo",C(lang,"mercado_rh_titulo")),
                       ("cards",_seq(C(lang,"mercado_rh_cards")),3)]})
    P.append({"tipo":"duas","titulo":C(lang,"problema_titulo"),
              "esq_titulo":C(lang,"problema_col_esq_titulo"),
              "esq_itens":_seq(C(lang,"problema_col_esq")),
              "dir_titulo":C(lang,"problema_col_dir_titulo"),
              "dir_texto":C(lang,"problema_col_dir"),
              "destaque":C(lang,"problema_destaque")})
    P.append({"tipo":"geral","titulo":C(lang,"solucao_titulo"),"intro":C(lang,"solucao_texto"),
              "corpo":[("cards",_seq(C(lang,"solucao_colunas")),3)]})
    P.append({"tipo":"geral","titulo":C(lang,"alcance_titulo"),"intro":C(lang,"alcance_texto"),
              "corpo":[("tabela",_tabela_alcance(lang),[3,2,3,2],8)]})
    P.append({"tipo":"geral","titulo":C(lang,"mercados_titulo","novos_titulo"),
              "intro":C(lang,"mercados_texto","novos_texto"),
              "corpo":[("cards",_seq(C(lang,"mercados_cards","novos_cards")),3),
                       ("texto",C(lang,"mercados_rodape"),8,TINTA)]})
    P.append({"tipo":"geral","titulo":C(lang,"preco_titulo"),
              "intro":C(lang,"preco_esq","preco_texto"),
              "corpo":[("cards",_seq(C(lang,"preco_pilares","preco_cards")),3)]})
    P.append({"tipo":"geral","titulo":C(lang,"portfolio_titulo"),"intro":C(lang,"portfolio_texto"),
              "corpo":[("tabela",_seq(C(lang,"portfolio_tabela")),[1.7, 5.4, 1.6, 2.2],8),
                       ("texto",C(lang,"portfolio_rodape"),7.5,CINZA)]})
    P.append({"tipo":"destaque","titulo":C(lang,"rh_destaque_titulo","destaque_titulo"),
              "selo":C(lang,"destaque_selo"),
              "texto":C(lang,"rh_destaque_texto","destaque_texto"),
              "cards":_seq(C(lang,"destaque_cards"))})
    P.append({"tipo":"geral","titulo":C(lang,"negocio_titulo","modelo_titulo"),"intro":None,
              "corpo":[("pares",_seq(C(lang,"negocio_colunas","modelo_itens"))),
                       ("subtitulo",C(lang,"banners_titulo")),
                       ("tabela",_seq(C(lang,"banners_tabela")),[2.6, 1.6, 2.0, 3.2],7.5),
                       ("texto",C(lang,"banners_formatos","banners_nota"),7,CINZA)]})
    P.append({"tipo":"geral","titulo":C(lang,"b2b_titulo"),"intro":C(lang,"b2b_texto"),
              "corpo":[("tabela",_seq(C(lang,"b2b_tabela")),[2.2, 1.6, 2.6, 3.4],7.5)]})
    P.append({"tipo":"geral","titulo":C(lang,"projecoes_curto_titulo","projecoes_titulo"),
              "intro":C(lang,"projecoes_curto_texto","projecoes_texto"),
              "corpo":[("barras",_anos_proj(lang)),
                       ("tabela",(_seq(C(lang,"projecoes_header")) or [["Horizonte","Conservador (R$)","Otimista (R$)"]]) + _anos_proj(lang),
                        [2, 2.6, 2.6], 8)]})
    P.append({"tipo":"geral","titulo":C(lang,"roteiro_titulo"),"intro":C(lang,"roteiro_texto"),
              "corpo":[("pares",_seq(C(lang,"roteiro_fases","roteiro_itens"))),
                       ("subtitulo",C(lang,"tracao_titulo")),
                       ("metricas",_seq(C(lang,"tracao_kpis","tracao_metricas")))]})
    P.append({"tipo":"geral","titulo":C(lang,"invest_titulo"),"intro":C(lang,"invest_texto"),
              "corpo":[("metricas",_seq(C(lang,"invest_dados","invest_metricas"))),
                       ("pares",_seq(C(lang,"invest_contato"))),
                       ("texto",C(lang,"invest_alocacao","invest_aloc"),7.2,CINZA),
                       ("subtitulo",C(lang,"pix_titulo")),
                       ("texto",C(lang,"pix_texto"),7.5),
                       ("metricas",_seq(C(lang,"pix_kpis","pix_metricas"))),
                       ("texto",C(lang,"pix_fonte","pix_fontes"),6.5,CINZA)]})
    P.append({"tipo":"refs_final"})
    return P

# ===== 9. RENDERIZAÇÃO =====
def _render_corpo(lang, corpo):
    fluxo = [Spacer(1, 2*mm)]
    for item in corpo:
        tipo = item[0]
        if tipo == "cards":      fluxo.append(_cards(lang, item[1], item[2] if len(item)>2 else 2)); fluxo.append(Spacer(1, 3*mm))
        elif tipo == "tabela":   fluxo.append(_tabela(lang, item[1], item[2] if len(item)>2 else None,
                                                      item[3] if len(item)>3 else 8)); fluxo.append(Spacer(1, 3*mm))
        elif tipo == "metricas": fluxo.append(_metricas(lang, item[1],
                                                      item[2] if len(item)>2 else 17)); fluxo.append(Spacer(1, 3*mm))
        elif tipo == "texto":
            t, tam, cor = item[1], (item[2] if len(item)>2 else 8.5), (item[3] if len(item)>3 else TINTA)
            if t:
                fluxo.append(_para(lang, t, tam, cor)); fluxo.append(Spacer(1, 2*mm))
        elif tipo == "subtitulo":
            f, _, rtl = FONTES_IDIOMA.get(lang, (REG, BOLD, False))
            fluxo.append(Paragraph(_rtl(str(item[1]), lang), _estilo(f, 12, OURO_ESC, bold=True)))
            fluxo.append(Spacer(1, 2*mm))
        elif tipo == "pares":    fluxo.extend(_lista_pares(lang, item[1]))
        elif tipo == "barras":   fluxo.append(_barras(lang, item[1])); fluxo.append(Spacer(1, 3*mm))
    return fluxo

def _render_pagina(lang, spec):
    if spec["tipo"] == "capa": return []
    if spec["tipo"] == "refs_final":
        f, _, rtl = FONTES_IDIOMA.get(lang, (REG, BOLD, False))
        saida = _titulo(lang, C(lang,"ref_titulo"))
        intro = C(lang,"ref_intro")
        if isinstance(intro, str) and intro:
            saida += [_para(lang, intro, 8.5, CINZA), Spacer(1, 2.5*mm)]
        refs = _seq(C(lang,"ref_lista","ref_itens"))
        if refs:
            meio = (len(refs)+1)//2
            fe = _lista_pares(lang, refs[:meio], 7.5)
            fd = _lista_pares(lang, refs[meio:], 7.5)
            saida += [_duas_colunas(lang, None, fe, None, fd)]
        selo = C(lang, "selo_final")
        selo_txt = " · ".join(str(x) for x in selo) if isinstance(selo, (list, tuple)) and selo \
                   else str(C(lang, "final_linha") or PADRAO_PT["final_linha"])
        saida += [Spacer(1, 9*mm),
                  Table([[""]], colWidths=[LARG_UTIL*0.5], rowHeights=[1], hAlign="CENTER",
                        style=TableStyle([("BACKGROUND",(0,0),(-1,-1),OURO)])),
                  Spacer(1, 9*mm),
                  Paragraph(_rtl(str(C(lang,"frase_final","final_frase")), lang),
                            _estilo(f, 22, OURO_ESC, TA_CENTER, True, 27)),
                  Spacer(1, 7*mm),
                  Paragraph(_rtl(selo_txt, lang), _estilo(f, 9.5, TINTA, TA_CENTER, True)),
                  Spacer(1, 6*mm),
                  Paragraph("1 · 2 · 3 · 4 · 5 · 6 · 7 · 8 · 9", _estilo(f, 9, OURO, TA_CENTER))]
        return [_kif(saida)]
    if spec["tipo"] == "destaque":
        f, _, rtl = FONTES_IDIOMA.get(lang, (REG, BOLD, False))
        selo = Table([[Paragraph(_rtl(str(spec["selo"]), lang), _estilo(f, 9, colors.white, TA_CENTER, True))]],
                     colWidths=[LARG_UTIL*0.6], style=TableStyle([
                         ("BACKGROUND",(0,0),(-1,-1),OURO_ESC),
                         ("TOPPADDING",(0,0),(-1,-1),2*mm),("BOTTOMPADDING",(0,0),(-1,-1),2*mm)]))
        return _titulo(lang, spec["titulo"]) + [Spacer(1,2*mm), selo, Spacer(1,3*mm),
                _para(lang, spec["texto"], 9.5), Spacer(1,4*mm),
                _cards(lang, spec["cards"], 2)]
    if spec["tipo"] == "duas":
        fe = [_para(lang, spec["esq_titulo"], 11, OURO_ESC, True), Spacer(1,2*mm)] + \
             _lista_pares(lang, spec["esq_itens"], 8.5)
        fd = [_para(lang, spec["dir_titulo"], 11, OURO_ESC, True), Spacer(1,2*mm),
              _para(lang, spec["dir_texto"], 8.5)]
        dest = spec.get("destaque")
        if isinstance(dest, str) and dest:
            fd += [Spacer(1, 3*mm), _para(lang, dest, 8.5, OURO_ESC, True)]
        return _titulo(lang, spec["titulo"]) + [Spacer(1,3*mm),
                _duas_colunas(lang, None, fe, None, fd)]
    saida = _titulo(lang, spec["titulo"])
    if spec.get("intro"):
        saida += [_para(lang, spec["intro"], 9), Spacer(1, 2.5*mm)]
    saida += _render_corpo(lang, spec["corpo"])
    return [_kif(saida)]

def _render_capa(lang):
    f, fb, rtl = FONTES_IDIOMA.get(lang, (REG, BOLD, False))
    c = []
    c.append(Spacer(1, 26*mm))
    try:
        p_logo = _primeiro(_LOGO_CANDIDATOS)
        if p_logo:
            c.append(Image(p_logo, 60*mm, 60*mm * 0.32, preserveAspectRatio=True, mask="auto"))
        else:
            c.append(_para(lang, "A1ELOS", 26, OURO, TA_CENTER, True))
    except Exception:
        c.append(_para(lang, "A1ELOS", 26, OURO, TA_CENTER, True))
    c.append(Spacer(1, 7*mm))
    c.append(Paragraph(_rtl(str(C(lang,"titulo","capa_titulo")), lang),
                       _estilo(f, 26, TINTA, TA_CENTER, True, 32)))
    c.append(Spacer(1, 3*mm))
    c.append(Paragraph(_rtl(str(C(lang,"subtitulo","capa_sub")), lang),
                       _estilo(f, 14, OURO_ESC, TA_CENTER)))
    nota = C(lang, "capa_nota")
    if isinstance(nota, str) and nota:
        c.append(Spacer(1, 3*mm))
        c.append(Paragraph(_rtl(nota, lang), _estilo(f, 10.5, TINTA, TA_CENTER)))
    c.append(Spacer(1, 9*mm))
    c.append(Table([[""]], colWidths=[LARG_UTIL*0.5], rowHeights=[1], hAlign="CENTER",
                   style=TableStyle([("BACKGROUND",(0,0),(-1,-1),OURO)])))
    c.append(Spacer(1, 9*mm))
    c.append(Paragraph(_rtl(str(C(lang,"capa_linha")), lang), _estilo(f, 10.5, TINTA, TA_CENTER)))
    c.append(Spacer(1, 12*mm))
    c.append(Paragraph(_rtl(str(C(lang,"capa_conf")), lang), _estilo(f, 9, CINZA, TA_CENTER, True)))
    return c

# ===== 10. GERADOR PRINCIPAL =====
def gerar_apresentacao_slides(lang="pt", caminho=None):
    lang = lang if lang in IDIOMAS else "pt"
    caminho = caminho or "/tmp/apresentacao_slides_%s.pdf" % lang
    plano = _plano(lang)
    total = len(plano)

    class _Doc(SimpleDocTemplate):
        def afterInit(self): self._total_paginas = total

    doc = _Doc(caminho, pagesize=(LARG, ALT),
               leftMargin=MARG, rightMargin=MARG,
               topMargin=TOPO_BANDA + 4*mm, bottomMargin=PE_BANDA + 6*mm,
               title="A1ELOS Global Numerology — Apresentação", author="A1ELOS")
    historia = []
    for spec in plano:
        if spec["tipo"] == "capa":      historia += _render_capa(lang)
        else:                           historia += _render_pagina(lang, spec)
        if spec is not plano[-1]: historia.append(PageBreak())
    historia = [f for f in historia if f is not None]
    try:
        doc.build(historia, onFirstPage=lambda c,d: _page_decor(c,d,lang),
                  onLaterPages=lambda c,d: _page_decor(c,d,lang))
    except Exception:
        logging.getLogger(__name__).exception("A1ELOS slides — falha (lang=%s)" % lang)
        raise
    return caminho

if __name__ == "__main__":
    for l in IDIOMAS:
        print(gerar_apresentacao_slides(l))
