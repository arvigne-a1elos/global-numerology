# -*- coding: utf-8 -*-
# ================================================================
# referencia/traducoes_nucleo.py
# FONTE ÚNICA DE TRADUÇÕES — A1ELOS GLOBAL NUMEROLOGY
# Regras de manutenção:
#   1. NADA de tradução em app.js / translations.js / dicionarios.py
#      será editado diretamente a partir de agora. Edita-se AQUI.
#   2. O gerador emite o static/translations.js que o site consome.
#   3. SEÇÃO DISCO = esqueleto reutilizável em outros projetos.
#      SEÇÃO NAVE = conteúdo específico deste site.
# ================================================================

# ================= SEÇÃO DISCO (ESQUELETO) =================
IDIOMAS = ["pt","en","es","it","fr","de","ja","zh","ru","he","ar","id","tr","vi"]
FALLBACK = "pt"

def _j(obj):
    """Serializa uma camada para embutir no translations.js gerado."""
    import json
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))

def _reg(camada, chave, lang):
    """Acesso a qualquer camada com fallback automático para pt."""
    d = camada.get(lang) or camada.get(FALLBACK) or {}
    v = d.get(chave)
    if v is None:
        v = (camada.get(FALLBACK) or {}).get(chave, chave)
    return v

def validar_camada(nome, camada, chaves_obrigatorias):
    """Confere cobertura chaves x idiomas. Retorna lista de faltas (vazio = ok)."""
    faltas = []
    for lang in IDIOMAS:
        d = camada.get(lang) or {}
        for ch in chaves_obrigatorias:
            if ch not in d:
                faltas.append("%s/%s/%s" % (nome, lang, ch))
    return faltas

# ================ SEÇÃO NAVE (A1ELOS) ================
# ===== 1. NOMES DOS 24 PRODUTOS (UI web) — unificação de
# translations + PRODUTOS_TRAD + PRODUTOS(dicionarios.py) + Bloco 14 =====
PRODUTOS_TRAD = {
 "pt": {"express":"Mapa Express","vida":"Qual Vida/Ano","completo":"Mapa Completo","ia":"Pesquisa IA de Nomes","urna":"Validação Nome de Urna","eleitoral":"Número Eleitoral","imovel":"Número do Imóvel","calendario":"Calendário Mensal Energético","artistico":"Validação Nome Artístico","bebe":"Planejamento Nome de Bebê","assinatura":"Validação de Assinaturas","negocio":"Nome para Negócio/Produto","casal":"Mapa do Casal","familia":"Mapa Família Premium","coletivo":"Bônus Coletivo/Empresarial","compatibilidade_equipes":"Compatibilidade de Equipes (RH)","nome_pet":"Nome do Pet","nickname":"Nickname Digital","nome_dominio":"Nome do Domínio","nome_canal":"Nome do Canal","nome_equipe":"Nome da Equipe","nome_ong":"Nome de ONG, Associação, Instituto ou Fundação","nome_projeto":"Nome do Projeto","nome_evento":"Nome do Evento"},
 "en": {"express":"Express Map","vida":"Life Phase & Year","completo":"Complete Map","ia":"AI Name Search","urna":"Ballot Name Validation","eleitoral":"Electoral Number","imovel":"Property Number","calendario":"Monthly Energy Calendar","artistico":"Artistic Name Validation","bebe":"Baby Name Planning","assinatura":"Signature Validation","negocio":"Business & Product Name","casal":"Couple Map","familia":"Premium Family Map","coletivo":"Corporate Bonus","compatibilidade_equipes":"Team Compatibility (HR)","nome_pet":"Pet Name","nickname":"Digital Nickname","nome_dominio":"Domain Name","nome_canal":"Channel Name","nome_equipe":"Team Name","nome_ong":"NGO, Association, Institute or Foundation Name","nome_projeto":"Project Name","nome_evento":"Event Name"},
 "es": {"express":"Mapa Exprés","vida":"Ciclo de Vida y Año","completo":"Mapa Completo","ia":"Búsqueda IA de Nombres","urna":"Validación Nombre de Urna","eleitoral":"Número Electoral","imovel":"Número de la Propiedad","calendario":"Calendario Mensual Energético","artistico":"Validación Nombre Artístico","bebe":"Planificación Nombre de Bebé","assinatura":"Validación de Firmas","negocio":"Nombre para Negocio/Producto","casal":"Mapa de Pareja","familia":"Mapa Familiar Premium","coletivo":"Bono Corporativo","compatibilidade_equipes":"Compatibilidad de Equipos (RRHH)","nome_pet":"Nombre de la Mascota","nickname":"Apodo Digital","nome_dominio":"Nombre de Dominio","nome_canal":"Nombre del Canal","nome_equipe":"Nombre del Equipo","nome_ong":"Nombre de ONG, Asociación, Instituto o Fundación","nome_projeto":"Nombre del Proyecto","nome_evento":"Nombre del Evento"},
 "it": {"express":"Mappa Espressa","vida":"Fase di Vita e Anno","completo":"Mappa Completa","ia":"Ricerca IA Nomi","urna":"Validazione Nome della Scheda","eleitoral":"Numero Elettorale","imovel":"Numero dell'Immobile","calendario":"Calendario Mensile Energetico","artistico":"Validazione Nome d'Arte","bebe":"Pianificazione Nome del Bambino","assinatura":"Validazione delle Firme","negocio":"Nome per Business/Prodotto","casal":"Mappa di Coppia","familia":"Mappa Famiglia Premium","coletivo":"Bonus Aziendale","compatibilidade_equipes":"Compatibilità di Squadre (HR)","nome_pet":"Nome dell'Animale","nickname":"Nickname Digitale","nome_dominio":"Nome del Dominio","nome_canal":"Nome del Canale","nome_equipe":"Nome della Squadra","nome_ong":"Nome di ONG, Associazione, Istituto o Fondazione","nome_projeto":"Nome del Progetto","nome_evento":"Nome dell'Evento"},
 "fr": {"express":"Carte Express","vida":"Phase de Vie et Année","completo":"Carte Complète","ia":"Recherche IA de Noms","urna":"Validation Nom du Bulletin","eleitoral":"Numéro Électoral","imovel":"Numéro du Bien","calendario":"Calendrier Mensuel Énergétique","artistico":"Validation Nom de Scène","bebe":"Planification Prénom de Bébé","assinatura":"Validation des Signatures","negocio":"Nom pour Entreprise/Produit","casal":"Carte du Couple","familia":"Carte Famille Premium","coletivo":"Bonus d'Entreprise","compatibilidade_equipes":"Compatibilité des Équipes (RH)","nome_pet":"Nom de l'Animal","nickname":"Pseudo Numérique","nome_dominio":"Nom de Domaine","nome_canal":"Nom de la Chaîne","nome_equipe":"Nom de l'Équipe","nome_ong":"Nom d'ONG, Association, Institut ou Fondation","nome_projeto":"Nom du Projet","nome_evento":"Nom de l'Événement"},
 "de": {"express":"Express-Karte","vida":"Lebensphase & Jahr","completo":"Vollständige Karte","ia":"KI-Namenssuche","urna":"Stimmzettelname-Validierung","eleitoral":"Wahlnummer","imovel":"Immobiliennummer","calendario":"Monatlicher Energiekalender","artistico":"Künstlername-Validierung","bebe":"Babynamen-Planung","assinatura":"Unterschrifts-Validierung","negocio":"Name für Unternehmen/Produkt","casal":"Paar-Karte","familia":"Premium-Familien-Karte","coletivo":"Unternehmensbonus","compatibilidade_equipes":"Teamkompatibilität (HR)","nome_pet":"Haustiername","nickname":"Digitaler Spitzname","nome_dominio":"Domainname","nome_canal":"Kanalname","nome_equipe":"Teamname","nome_ong":"Name von NGO, Verein, Institut oder Stiftung","nome_projeto":"Projektname","nome_evento":"Veranstaltungsname"},
 "ja": {"express":"エクスプレスマップ","vida":"ライフステージと年","completo":"完全マップ","ia":"AI名前検索","urna":"投票用紙名の検証","eleitoral":"選挙番号","imovel":"不動産番号","calendario":"月間エネルギーカレンダー","artistico":"芸名の検証","bebe":"赤ちゃんの名前計画","assinatura":"署名の検証","negocio":"ビジネス・商品名","casal":"カップルマップ","familia":"プレミアム家族マップ","coletivo":"法人ボーナス","compatibilidade_equipes":"チーム相性（人事）","nome_pet":"ペットの名前","nickname":"デジタルニックネーム","nome_dominio":"ドメイン名","nome_canal":"チャンネル名","nome_equipe":"チーム名","nome_ong":"NGO・協会・研究所・財団の名前","nome_projeto":"プロジェクト名","nome_evento":"イベント名"},
 "zh": {"express":"快速地图","vida":"生命阶段与年份","completo":"完整地图","ia":"AI名字搜索","urna":"选票名称验证","eleitoral":"选举号码","imovel":"房产号码","calendario":"每月能量日历","artistico":"艺名验证","bebe":"宝宝取名规划","assinatura":"签名验证","negocio":"企业/产品名称","casal":"情侣地图","familia":"高级家庭地图","coletivo":"企业奖励","compatibilidade_equipes":"团队兼容性（人力资源）","nome_pet":"宠物名字","nickname":"数字昵称","nome_dominio":"域名","nome_canal":"频道名称","nome_equipe":"团队名称","nome_ong":"非政府组织、协会、研究所或基金会名称","nome_projeto":"项目名称","nome_evento":"活动名称"},
 "ru": {"express":"Экспресс-карта","vida":"Жизненный этап и год","completo":"Полная карта","ia":"ИИ-поиск имён","urna":"Проверка названия бюллетеня","eleitoral":"Избирательный номер","imovel":"Номер недвижимости","calendario":"Ежемесячный энергетический календарь","artistico":"Проверка сценического имени","bebe":"Планирование имени ребёнка","assinatura":"Проверка подписей","negocio":"Название для бизнеса/продукта","casal":"Карта пары","familia":"Премиальная семейная карта","coletivo":"Корпоративный бонус","compatibilidade_equipes":"Совместимость команд (HR)","nome_pet":"Имя питомца","nickname":"Цифровой никнейм","nome_dominio":"Имя домена","nome_canal":"Название канала","nome_equipe":"Название команды","nome_ong":"Название НКО, ассоциации, института или фонда","nome_projeto":"Название проекта","nome_evento":"Название события"},
 "he": {"express":"מפה מהירה","vida":"שלב חיים ושנה","completo":"מפה מלאה","ia":"חיפוש שמות AI","urna":"אימות שם פתק","eleitoral":"מספר בחירות","imovel":"מספר נכס","calendario":"לוח אנרגיה חודשי","artistico":"אימות שם במה","bebe":"תכנון שם לתינוק","assinatura":"אימות חתימות","negocio":"שם לעסק/מוצר","casal":"מפת זוג","familia":"מפת משפחה פרימיום","coletivo":"בונוס ארגוני","compatibilidade_equipes":"תאימות צוות","nome_pet":"שם חיית המחמד","nickname":"כינוי דיגיטלי","nome_dominio":"שם דומיין","nome_canal":"שם הערוץ","nome_equipe":"שם הצוות","nome_ong":"שם עמותה, ארגון, מכון או קרן","nome_projeto":"שם הפרויקט","nome_evento":"שם האירוע"},
 "ar": {"express":"خريطة سريعة","vida":"مرحلة الحياة والسنة","completo":"خريطة كاملة","ia":"بحث الأسماء بالذكاء الاصطناعي","urna":"التحقق من اسم الاقتراع","eleitoral":"الرقم الانتخابي","imovel":"رقم العقار","calendario":"تقويم الطاقة الشهري","artistico":"التحقق من الاسم الفني","bebe":"تخطيط اسم الطفل","assinatura":"التحقق من التوقيعات","negocio":"اسم للأعمال/المنتج","casal":"خريطة الزوجين","familia":"خريطة العائلة المميزة","coletivo":"مكافأة الشركات","compatibilidade_equipes":"توافق الفريق","nome_pet":"اسم الحيوان الأليف","nickname":"اللقب الرقمي","nome_dominio":"اسم النطاق","nome_canal":"اسم القناة","nome_equipe":"اسم الفريق","nome_ong":"اسم منظمة أو جمعية أو معهد أو مؤسسة","nome_projeto":"اسم المشروع","nome_evento":"اسم الفعالية"},
 "id": {"express":"Peta Ekspres","vida":"Tahap Hidup & Tahun","completo":"Peta Lengkap","ia":"Pencarian Nama AI","urna":"Validasi Nama Surat Suara","eleitoral":"Nomor Pemilihan","imovel":"Nomor Properti","calendario":"Kalender Energi Bulanan","artistico":"Validasi Nama Artistik","bebe":"Perencanaan Nama Bayi","assinatura":"Validasi Tanda Tangan","negocio":"Nama untuk Bisnis/Produk","casal":"Peta Pasangan","familia":"Peta Keluarga Premium","coletivo":"Bonus Kolektif/Perusahaan","compatibilidade_equipes":"Kompatibilitas Tim (HR)","nome_pet":"Nama Hewan Peliharaan","nickname":"Nama Panggilan Digital","nome_dominio":"Nama Domain","nome_canal":"Nama Saluran","nome_equipe":"Nama Tim","nome_ong":"Nama LSM, Asosiasi, Lembaga atau Yayasan","nome_projeto":"Nama Proyek","nome_evento":"Nama Acara"},
 "tr": {"express":"Ekspres Harita","vida":"Yaşam Evresi & Yıl","completo":"Tam Harita","ia":"AI İsim Arama","urna":"Oy Pusulası İsim Doğrulama","eleitoral":"Seçim Numarası","imovel":"Mülk Numarası","calendario":"Aylık Enerji Takvimi","artistico":"Sahne Adı Doğrulama","bebe":"Bebek İsmi Planlama","assinatura":"İmza Doğrulama","negocio":"İşletme/Ürün Adı","casal":"Çift Haritası","familia":"Premium Aile Haritası","coletivo":"Kurumsal Bonus","compatibilidade_equipes":"Ekip Uyumu (İK)","nome_pet":"Evcil Hayvan Adı","nickname":"Dijital Takma Ad","nome_dominio":"Alan Adı","nome_canal":"Kanal Adı","nome_equipe":"Ekip Adı","nome_ong":"STK, Dernek, Enstitü veya Vakıf Adı","nome_projeto":"Proje Adı","nome_evento":"Etkinlik Adı"},
 "vi": {"express":"Bản Đồ Nhanh","vida":"Giai Đoạn Cuộc Đời & Năm","completo":"Bản Đồ Đầy Đủ","ia":"Tìm Kiếm Tên AI","urna":"Xác Minh Tên Phiếu Bầu","eleitoral":"Số Bầu Cử","imovel":"Số Bất Động Sản","calendario":"Lịch Năng Lượng Hàng Tháng","artistico":"Xác Minh Nghệ Danh","bebe":"Lên Kế Hoạch Tên Cho Bé","assinatura":"Xác Minh Chữ Ký","negocio":"Tên Cho Doanh Nghiệp/Sản Phẩm","casal":"Bản Đồ Cặp Đôi","familia":"Bản Đồ Gia Đình Cao Cấp","coletivo":"Thưởng Tập Thể/Doanh Nghiệp","compatibilidade_equipes":"Tương Hợp Đội Nhóm (Nhân sự)","nome_pet":"Tên Thú Cưng","nickname":"Biệt Danh Kỹ Thuật Số","nome_dominio":"Tên Miền","nome_canal":"Tên Kênh","nome_equipe":"Tên Đội Nhóm","nome_ong":"Tên Tổ Chức, Hiệp Hội, Viện hoặc Quỹ","nome_projeto":"Tên Dự Án","nome_evento":"Tên Sự Kiện"},
}

# ===== 2. BLOCO 2 (energias unificadas) — cole aqui =====
ENERGIA_TITULOS = {}   # Bloco 2
ENERGIAS_TXT   = {}    # Bloco 2
AMOR_TXT       = {}    # Bloco 2

# ===== 3. BLOCO 3 (UI) — cole aqui =====
UI_TRAD  = {}          # Bloco 3 (hero, nav, botões, alerts, formulários, EXTRA_TRAD)
CAL_TXT  = {}          # Bloco 3 (p_calendario, desc_calendario, f_cal_*, mes_01..12)

# ===== 4. BLOCO 4 (preços e tabelas) — cole aqui =====
FEAT_TRAD      = {}    # Bloco 4
DESC_COLETIVO  = {}    # Bloco 4
BC_TEXTS       = {}    # Bloco 4
SERVICOS_TRAD  = {}    # Bloco 4
# PRODUTO_FAIXA e PRECO_DISPLAY não são digitados aqui:
# derivam de referencia/precos.py (fonte única, sem duplicar).

# ===== 5. BLOCO 5 (PDFs e semântica) — cole aqui =====
PDF_TEXTS   = {}       # Bloco 5
PDF_SECOES  = {}       # Bloco 5
BOAS_VINDAS = {}       # Bloco 5
PERIODOS    = {}       # Bloco 5
REALIZ_HEAD = {}       # Bloco 5

# ================= GERADOR (emite o translations.js) =================
CHAVES_24 = ["express","vida","completo","ia","urna","eleitoral","imovel","calendario",
             "artistico","bebe","assinatura","negocio","casal","familia","coletivo",
             "compatibilidade_equipes","nome_pet","nickname","nome_dominio","nome_canal",
             "nome_equipe","nome_ong","nome_projeto","nome_evento"]

def validar():
    print("== VALIDAÇÃO DO NÚCLEO ==")
    f = validar_camada("PRODUTOS_TRAD", PRODUTOS_TRAD, CHAVES_24)
    print("PRODUTOS_TRAD 24x14:", "OK (sem faltas)" if not f else "FALTAM: " + ", ".join(f[:20]))
    return not f

def gerar_translations_js(caminho="static/translations.js"):
    """Emite o translations.js com as MESMAS variáveis globais do site atual.
    Camadas ainda vazias não são emitidas; as existentes no arquivo antigo
    continuam valendo até cada bloco ser concluído (migração segura)."""
    partes = []
    partes.append("// ===== GERADO POR referencia/traducoes_nucleo.py — NÃO EDITAR AQUI =====")
    partes.append("window.PRODUTOS_TRAD = " + _j(PRODUTOS_TRAD) + ";")
    for nome, camada in [("ENERGIA_TITULOS", ENERGIA_TITULOS), ("ENERGIAS_TXT", ENERGIAS_TXT),
                         ("AMOR_TXT", AMOR_TXT), ("UI_TRAD", UI_TRAD), ("CAL_TXT", CAL_TXT),
                         ("FEAT_TRAD", FEAT_TRAD), ("DESC_COLETIVO", DESC_COLETIVO),
                         ("BC_TEXTS", BC_TEXTS), ("SERVICOS_TRAD", SERVICOS_TRAD),
                         ("PDF_TEXTS", PDF_TEXTS), ("PDF_SECOES", PDF_SECOES),
                         ("BOAS_VINDAS", BOAS_VINDAS), ("PERIODOS", PERIODOS),
                         ("REALIZ_HEAD", REALIZ_HEAD)]:
        if camada:
            partes.append("window.%s = %s;" % (nome, _j(camada)))
    with open(caminho, "w", encoding="utf-8") as arq:
        arq.write("\n".join(partes) + "\n")
    print("Gerado:", caminho)

if __name__ == "__main__":
    validar()
