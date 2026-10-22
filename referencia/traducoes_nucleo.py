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
import os, json

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
    """Confere cobertura chaves x idiomas. Lista de faltas vazia = OK."""
    faltas = []
    for lang in IDIOMAS:
        d = camada.get(lang) or {}
        for ch in chaves_obrigatorias:
            if ch not in d:
                faltas.append("%s/%s/%s" % (nome, lang, ch))
    return faltas

# ================= GERADOR (emite o translations.js) =================
CHAVES_24 = ["express","vida","completo","ia","urna","eleitoral","imovel","calendario",
             "artistico","bebe","assinatura","negocio","casal","familia","coletivo",
             "compatibilidade_equipes","nome_pet","nickname","nome_dominio","nome_canal",
             "nome_equipe","nome_ong","nome_projeto","nome_evento"]

def validar():
    print("== VALIDACAO DO NUCLEO ==")
    ok = True
    checks = [
        ("PRODUTOS_TRAD", PRODUTOS_TRAD, CHAVES_24),
        ("ENERGIA_TITULOS", ENERGIA_TITULOS, [1,2,3,4,5,6,7,8,9]),
        ("ENERGIAS_TXT", ENERGIAS_TXT, [1,2,3,4,5,6,7,8,9]),
        ("AMOR_TXT", AMOR_TXT, [5,6]),
        ("CAL_TXT", CAL_TXT, ["p_calendario","desc_calendario","f_cal_univ","f_cal_pess","f_cal_ano_emb","calc_nome","f_cal_data","f_cal_ano","f_mes","ph_nome_completo","MESES"]),
        ("EXTRA_TRAD", EXTRA_TRAD, ["f_genero","f_grafias","f_nome_org","ph_nome_org","f_nome_candidato","f_num_atual","ph_sigla","f_sobrenome_familia","f_pessoa1","f_pessoa2","ph_energia","confirmar_btn","cancelar_btn"]),
        ("PRECO_DISPLAY", PRECO_DISPLAY, None),   # tratado abaixo (6 faixas x 14)
        ("FEAT_TRAD", FEAT_TRAD, CHAVES_24),
        ("BC_TEXTS", BC_TEXTS, ["qtd_total", "codigos"]),
        ("SERVICOS_TRAD", SERVICOS_TRAD, None),   # 4 servicos x 14
        ("MESES_TRAD", MESES_TRAD, None),  # derivado; checa presenca dos 14
        ("PDF_TEXTS", PDF_TEXTS, ["t_express","t_completo","t_urna","t_eleitoral","numero","valor","caminho","expressao","motivacao","personalidade","destino","cargo","sugestoes","op8","op_alt","num_existente","ciclos","desafios","ano_pessoal","grade","baixar","confirmado","gerado","voltar","qr_titulo","qr_instrucao","entrega"]),
        ("PDF_SECOES", PDF_SECOES, ["numeros_principais","caminho_ciclos","desafios_realizacoes","como_calculamos","por_que_energia_8","energia_8_ideal","alternativas"]),
    ]

    for nome, camada, chaves in checks:
        if chaves is None:
            faltam = [l for l in IDIOMAS if not camada.get(l)]
            print("%-16s %s" % (nome, "OK 14 idiomas" if not faltam else "FALTAM: " + ", ".join(faltam)))
            if faltam: ok = False
            continue
        f = validar_camada(nome, camada, chaves)
        print("%-16s %s" % (nome, "OK 14 idiomas" if not f else "FALTAM: " + ", ".join(f[:15])))
        if f: ok = False
    print("precos.py        %s" % ("OK (importado)" if _PRECOS_OK else "NAO ENCONTRADO — verifique referencia/precos.py"))
    faltas_desc = [l for l in IDIOMAS if not DESC_COLETIVO.get(l)]
    print("%-16s %s" % ("DESC_COLETIVO", "OK 14 idiomas" if not faltas_desc else "FALTAM: " + ", ".join(faltas_desc)))
    _derivar_tabelas()
    faltas_sv = [l for l in IDIOMAS if len(SERVICOS_TRAD.get(l) or []) != 4]
    print("%-16s %s" % ("SERVICOS_TRAD", "OK 14 idiomas (derivado)" if not faltas_sv else "FALTAM: " + ", ".join(faltas_sv)))
    if faltas_desc or faltas_sv: ok = False
    faltas_bv = [l for l in IDIOMAS if not BOAS_VINDAS.get(l)]
    faltas_pe = [l for l in IDIOMAS if len(PERIODOS.get(l) or ()) != 3]
    faltas_rh = [l for l in IDIOMAS if len(REALIZ_HEAD.get(l) or ()) != 2]
    print("%-16s %s" % ("BOAS_VINDAS", "OK 14" if not faltas_bv else "FALTAM: " + ", ".join(faltas_bv)))
    print("%-16s %s" % ("PERIODOS", "OK 14" if not faltas_pe else "FALTAM: " + ", ".join(faltas_pe)))
    print("%-16s %s" % ("REALIZ_HEAD", "OK 14" if not faltas_rh else "FALTAM: " + ", ".join(faltas_rh)))
    if faltas_bv or faltas_pe or faltas_rh: ok = False        
    return ok

def gerar_translations_js(caminho="referencia/translations_gerado.js"):
    """SEGURANCA: emite para referencia/ (nunca sobrescreve o
    static/translations.js em producao)."""
    _derivacao_meses()
    _derivar_tabelas()
    for lang in IDIOMAS:
        meses = MESES_TRAD.get(lang)
        if meses and lang in UI_TRAD:
            for i, nome in enumerate(meses):
                UI_TRAD[lang]["mes_%02d" % (i + 1)] = nome
    partes = []
    partes.append("// ===== GERADO POR referencia/traducoes_nucleo.py — NAO EDITAR AQUI =====")
    partes.append("window.PRODUTOS_TRAD = " + _j(PRODUTOS_TRAD) + ";")
    partes.append("window.ENERGIA_TITULOS = " + _j(ENERGIA_TITULOS) + ";")
    if ENERGIAS_TXT:
        partes.append("window.ENERGIAS_DESC = " + _j(ENERGIAS_TXT) + ";")
    if UI_TRAD:
        partes.append("window.translations = " + _j(UI_TRAD) + ";")
    if EXTRA_TRAD:
        partes.append("window.EXTRA_TRAD = " + _j(EXTRA_TRAD) + ";")
    if MESES_TRAD:
        partes.append("window.MESES_TRAD = " + _j(MESES_TRAD) + ";")
    if PRECO_DISPLAY:
        partes.append("window.PRECO_DISPLAY = " + _j(PRECO_DISPLAY) + ";")
    if PRODUTO_FAIXA:
        partes.append("window.PRODUTO_FAIXA = " + _j(PRODUTO_FAIXA) + ";")
    if SIMBOLO:
        partes.append("window.SIMBOLO = " + _j(SIMBOLO) + ";")
    for nome, camada in [("FEAT_TRAD", FEAT_TRAD), ("DESC_COLETIVO", DESC_COLETIVO),
                         ("BC_TEXTS", BC_TEXTS), ("SERVICOS_TRAD", SERVICOS_TRAD),
                         ("PDF_TEXTS", PDF_TEXTS), ("PDF_SECOES", PDF_SECOES),
                         ("BOAS_VINDAS", BOAS_VINDAS), ("PERIODOS", PERIODOS),
                         ("REALIZ_HEAD", REALIZ_HEAD)]:
        if camada:
            partes.append("window.%s = %s;" % (nome, _j(camada)))
    with open(caminho, "w", encoding="utf-8") as arq:
        arq.write("\n".join(partes) + "\n")
    print("Gerado (area segura):", caminho)
    
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

# ================================================================
# BLOCO 2 — ENERGIAS UNIFICADAS (canon 22/10/2026)
# Canon: 4=Estrutura | 7=Espiritualidade | 9=Humanitarismo
# Fontes: ENERGIAS_TXT + AMOR_TXT (dicionarios.py, verbatim)
#         + ENERGIA_TITULOS (translations.js) alinhado ao canon.
# Substitui a divergência ENERGIAS_TRAD x ENERGIA_TITULOS.
# ================================================================

ENERGIA_TITULOS = {
    "pt": {1:"Liderança",2:"Cooperação",3:"Criatividade",4:"Estrutura",5:"Liberdade",6:"Harmonia",7:"Espiritualidade",8:"Poder",9:"Humanitarismo"},
    "en": {1:"Leadership",2:"Cooperation",3:"Creativity",4:"Structure",5:"Freedom",6:"Harmony",7:"Spirituality",8:"Power",9:"Humanitarianism"},
    "es": {1:"Liderazgo",2:"Cooperación",3:"Creatividad",4:"Estructura",5:"Libertad",6:"Armonía",7:"Espiritualidad",8:"Poder",9:"Humanitarismo"},
    "it": {1:"Leadership",2:"Cooperazione",3:"Creatività",4:"Struttura",5:"Libertà",6:"Armonia",7:"Spiritualità",8:"Potere",9:"Umanitarismo"},
    "fr": {1:"Leadership",2:"Coopération",3:"Créativité",4:"Structure",5:"Liberté",6:"Harmonie",7:"Spiritualité",8:"Pouvoir",9:"Humanitarisme"},
    "de": {1:"Führung",2:"Kooperation",3:"Kreativität",4:"Struktur",5:"Freiheit",6:"Harmonie",7:"Spiritualität",8:"Macht",9:"Humanitarismus"},
    "ja": {1:"リーダーシップ",2:"協力",3:"創造性",4:"構造",5:"自由",6:"調和",7:"精神性",8:"力",9:"人道主義"},
    "zh": {1:"领导力",2:"合作",3:"创造力",4:"结构",5:"自由",6:"和谐",7:"灵性",8:"力量",9:"人道主义"},
    "ru": {1:"Лидерство",2:"Сотрудничество",3:"Творчество",4:"Структура",5:"Свобода",6:"Гармония",7:"Духовность",8:"Сила",9:"Гуманизм"},
    "he": {1:"מנהיגות",2:"שיתוף פעולה",3:"יצירתיות",4:"מבנה",5:"חופש",6:"הרמוניה",7:"רוחניות",8:"כוח",9:"הומניטריות"},
    "ar": {1:"القيادة",2:"التعاون",3:"الإبداع",4:"الهيكل",5:"الحرية",6:"الانسجام",7:"الروحانية",8:"القوة",9:"الإنسانية"},
    "id": {1:"Kepemimpinan",2:"Kerja Sama",3:"Kreativitas",4:"Struktur",5:"Kebebasan",6:"Harmoni",7:"Spiritualitas",8:"Kekuatan",9:"Humanitarianisme"},
    "tr": {1:"Liderlik",2:"İşbirliği",3:"Yaratıcılık",4:"Yapı",5:"Özgürlük",6:"Uyum",7:"Maneviyat",8:"Güç",9:"İnsaniyet"},
    "vi": {1:"Lãnh đạo",2:"Hợp tác",3:"Sáng tạo",4:"Cấu trúc",5:"Tự do",6:"Hòa hợp",7:"Tâm linh",8:"Sức mạnh",9:"Nhân đạo"},
}

ENERGIAS_TXT = {
    1: {
        "pt":"Liderança: coragem, pioneirismo e inspiração.",
        "en":"Leadership: courage, pioneering and inspiration.",
        "es":"Liderazgo: coraje, pionerismo e inspiración.",
        "it":"Leadership: coraggio, spirito pionieristico e ispirazione.",
        "fr":"Leadership : courage, esprit pionnier et inspiration.",
        "de":"Führung: Mut, Pioniergeist und Inspiration.",
        "ja":"リーダーシップ：勇気、開拓者精神、ひらめき。",
        "zh":"领导力：勇气、开拓精神与灵感。",
        "ru":"Лидерство: смелость, первопроходчество и вдохновение.",
        "he":"מנהיגות: אומץ, חלוציות והשראה.",
        "ar":"القيادة: شجاعة وريادة وإلهام.",
        "id":"Kepemimpinan: keberanian, jiwa perintis, dan inspirasi.",
        "tr":"Liderlik: cesaret, öncülük ve ilham.",
        "vi":"Lãnh đạo: lòng dũng cảm, tinh thần tiên phong và cảm hứng.",
    },
    2: {
        "pt":"Cooperação: diplomacia, sensibilidade e união.",
        "en":"Cooperation: diplomacy, sensitivity and union.",
        "es":"Cooperación: diplomacia, sensibilidad y unión.",
        "it":"Cooperazione: diplomazia, sensibilità e unione.",
        "fr":"Coopération : diplomatie, sensibilité et union.",
        "de":"Zusammenarbeit: Diplomatie, Feingefühl und Einheit.",
        "ja":"協力：外交、感受性、団結。",
        "zh":"合作：外交、敏感与团结。",
        "ru":"Сотрудничество: дипломатия, чуткость и единство.",
        "he":"שיתוף פעולה: דיפלומטיה, רגישות ואחדות.",
        "ar":"التعاون: دبلوماسية وحساسية واتحاد.",
        "id":"Kerja Sama: diplomasi, kepekaan, dan persatuan.",
        "tr":"İşbirliği: diplomasi, hassasiyet ve birlik.",
        "vi":"Hợp tác: ngoại giao, nhạy cảm và đoàn kết.",
    },
    3: {
        "pt":"Criatividade: expressão, comunicação e otimismo.",
        "en":"Creativity: expression, communication and optimism.",
        "es":"Creatividad: expresión, comunicación y optimismo.",
        "it":"Creatività: espressione, comunicazione e ottimismo.",
        "fr":"Créativité : expression, communication et optimisme.",
        "de":"Kreativität: Ausdruck, Kommunikation und Optimismus.",
        "ja":"創造性：表現、コミュニケーション、楽観。",
        "zh":"创造力：表达、沟通与乐观。",
        "ru":"Творчество: выражение, общение и оптимизм.",
        "he":"יצירתיות: ביטוי, תקשורת ואופטימיות.",
        "ar":"الإبداع: تعبير وتواصل وتفاؤل.",
        "id":"Kreativitas: ekspresi, komunikasi, dan optimisme.",
        "tr":"Yaratıcılık: ifade, iletişim ve iyimserlik.",
        "vi":"Sáng tạo: biểu đạt, giao tiếp và lạc quan.",
    },
    4: {
        "pt":"Estrutura: organização, disciplina e segurança.",
        "en":"Structure: organization, discipline and security.",
        "es":"Estructura: organización, disciplina y seguridad.",
        "it":"Struttura: organizzazione, disciplina e sicurezza.",
        "fr":"Structure : organisation, discipline et sécurité.",
        "de":"Struktur: Organisation, Disziplin und Sicherheit.",
        "ja":"構造：組織、規律、安全。",
        "zh":"结构：组织、纪律与安全。",
        "ru":"Структура: организация, дисциплина и безопасность.",
        "he":"מבנה: ארגון, משמעת וביטחון.",
        "ar":"البنية: تنظيم وانضباط وأمان.",
        "id":"Struktur: organisasi, disiplin, dan keamanan.",
        "tr":"Yapı: organizasyon, disiplin ve güvenlik.",
        "vi":"Cấu trúc: tổ chức, kỷ luật và an toàn.",
    },
    5: {
        "pt":"Liberdade: aventura, adaptabilidade e versatilidade. O 5 fala do amor romântico/paixão.",
        "en":"Freedom: adventure, adaptability and versatility. 5 speaks of romantic/passionate love.",
        "es":"Libertad: aventura, adaptabilidad y versatilidad. El 5 habla del amor romántico/pasión.",
        "it":"Libertà: avventura, adattabilità e versatilità. Il 5 parla dell'amore romantico/passione.",
        "fr":"Liberté : aventure, adaptabilité et polyvalence. Le 5 parle de l'amour romantique/passion.",
        "de":"Freiheit: Abenteuer, Anpassungsfähigkeit und Vielseitigkeit. Die 5 spricht von romantischer/leidenschaftlicher Liebe.",
        "ja":"自由：冒険、適応力、多才。5はロマンチックな愛・情熱を語ります。",
        "zh":"自由：冒险、适应与多才。5代表浪漫/激情之爱。",
        "ru":"Свобода: приключения, адаптивность и универсальность. 5 говорит о романтической/страстной любви.",
        "he":"חופש: הרפתקאות, יכולת הסתגלות ורב-גוניות. 5 מדבר על אהבה רומנטית/תשוקה.",
        "ar":"الحرية: مغامرة وتكيف وتعدد مواهب. 5 يتحدث عن الحب الرومانسي/الشغف.",
        "id":"Kebebasan: petualangan, kemampuan beradaptasi, dan keserbagunaan. 5 berbicara tentang cinta romantis/gairah.",
        "tr":"Özgürlük: macera, uyum sağlama ve çok yönlülük. 5, romantik/tutkulu aşktan söz eder.",
        "vi":"Tự do: phiêu lưu, khả năng thích nghi và linh hoạt. Số 5 nói về tình yêu lãng mạn/đam mê.",
    },
    6: {
        "pt":"Harmonia: amor humano, compaixão e responsabilidade. O 6 fala do amor espiritual/humanitário.",
        "en":"Harmony: human love, compassion and responsibility. 6 speaks of spiritual/humanitarian love.",
        "es":"Armonía: amor humano, compasión y responsabilidad. El 6 habla del amor espiritual/humanitario.",
        "it":"Armonia: amore umano, compassione e responsabilità. Il 6 parla dell'amore spirituale/umanitario.",
        "fr":"Harmonie : amour humain, compassion et responsabilité. Le 6 parle de l'amour spirituel/humanitaire.",
        "de":"Harmonie: menschliche Liebe, Mitgefühl und Verantwortung. Die 6 spricht von spiritueller/humanitärer Liebe.",
        "ja":"調和：人間愛、慈愛、責任。6は精神的な愛・人道を語ります。",
        "zh":"和谐：人文之爱、同情与责任。6代表精神/人道之爱。",
        "ru":"Гармония: человеческая любовь, сострадание и ответственность. 6 говорит о духовной/гуманитарной любви.",
        "he":"הרמוניה: אהבה אנושית, חמלה ואחריות. 6 מדבר על אהבה רוחנית/הומניטרית.",
        "ar":"الانسجام: حب إنساني ورحمة ومسؤولية. 6 يتحدث عن الحب الروحي/الإنساني.",
        "id":"Harmoni: cinta manusiawi, kasih sayang, dan tanggung jawab. 6 berbicara tentang cinta spiritual/kemanusiaan.",
        "tr":"Uyum: insani sevgi, şefkat ve sorumluluk. 6, manevi/insani aşktan söz eder.",
        "vi":"Hòa hợp: tình yêu nhân văn, lòng trắc ẩn và trách nhiệm. Số 6 nói về tình yêu tâm linh/nhân đạo.",
    },
    7: {
        "pt":"Espiritualidade: introspecção, sabedoria e profundidade.",
        "en":"Spirituality: introspection, wisdom and depth.",
        "es":"Espiritualidad: introspección, sabiduría y profundidad.",
        "it":"Spiritualità: introspezione, saggezza e profondità.",
        "fr":"Spiritualité : introspection, sagesse et profondeur.",
        "de":"Spiritualität: Innenschau, Weisheit und Tiefe.",
        "ja":"精神性：内省、知恵、深み。",
        "zh":"灵性：内省、智慧与深度。",
        "ru":"Духовность: самоанализ, мудрость и глубина.",
        "he":"רוחניות: התבוננות פנימית, חוכמה ועומק.",
        "ar":"الروحانية: استبطان وحكمة وعمق.",
        "id":"Spiritualitas: introspeksi, kebijaksanaan, dan kedalaman.",
        "tr":"Maneviyat: içe dönüş, bilgelik ve derinlik.",
        "vi":"Tâm linh: nội tâm, trí tuệ và chiều sâu.",
    },
    8: {
        "pt":"Poder: realização, autoridade e prosperidade.",
        "en":"Power: achievement, authority and prosperity.",
        "es":"Poder: logro, autoridad y prosperidad.",
        "it":"Potere: realizzazione, autorità e prosperità.",
        "fr":"Pouvoir : accomplissement, autorité et prospérité.",
        "de":"Macht: Leistung, Autorität und Wohlstand.",
        "ja":"力：達成、権威、豊かさ。",
        "zh":"力量：成就、权威与丰盛。",
        "ru":"Сила: достижение, власть и процветание.",
        "he":"כוח: הישג, סמכות ושפע.",
        "ar":"القوة: إنجاز وسلطة وازدهار.",
        "id":"Kekuatan: pencapaian, otoritas, dan kemakmuran.",
        "tr":"Güç: başarı, otorite ve refah.",
        "vi":"Sức mạnh: thành tựu, quyền uy và thịnh vượng.",
    },
    9: {
        "pt":"Humanitarismo: compaixão, conclusão e serviço ao todo.",
        "en":"Humanitarianism: compassion, completion and service to all.",
        "es":"Humanitarismo: compasión, conclusión y servicio al todo.",
        "it":"Umanitarismo: compassione, compimento e servizio al tutto.",
        "fr":"Humanitarisme : compassion, achèvement et service au tout.",
        "de":"Humanitarismus: Mitgefühl, Vollendung und Dienst am Ganzen.",
        "ja":"人道主義：思いやり、完結、全体への奉仕。",
        "zh":"人道主义：同情、圆满与服务整体。",
        "ru":"Гуманизм: сострадание, завершение и служение целому.",
        "he":"הומניטריות: חמלה, השלמה ושירות לכלל.",
        "ar":"الإنسانية: رحمة وإنجاز وخدمة الكل.",
        "id":"Humanitarianisme: kasih sayang, penyelesaian, dan pelayanan kepada keseluruhan.",
        "tr":"İnsaniyet: şefkat, tamamlama ve bütüne hizmet.",
        "vi":"Nhân đạo: lòng trắc ẩn, hoàn thành và phục vụ tổng thể.",
    },
}

AMOR_TXT = {
    "pt": {5:"No amor, o 5 é paixão e sensualidade: atração intensa, sedução e desejo de liberdade afetiva.",
           6:"No amor, o 6 é amor humano e solidário: cuidado, compaixão, família e responsabilidade afetiva."},
    "en": {5:"In love, 5 is passion and sensuality: intense attraction, seduction and a desire for affective freedom.",
           6:"In love, 6 is human and solidary love: care, compassion, family and affective responsibility."},
    "es": {5:"En el amor, el 5 es pasión y sensualidad: atracción intensa, seducción y deseo de libertad afectiva.",
           6:"En el amor, el 6 es amor humano y solidario: cuidado, compasión, familia y responsabilidad afectiva."},
    "it": {5:"In amore, il 5 è passione e sensualità: attrazione intensa, seduzione e desiderio di libertà affettiva.",
           6:"In amore, il 6 è amore umano e solidale: cura, compassione, famiglia e responsabilità affettiva."},
    "fr": {5:"En amour, le 5 est passion et sensualité : attraction intense, séduction et désir de liberté affective.",
           6:"En amour, le 6 est amour humain et solidaire : soin, compassion, famille et responsabilité affective."},
    "de": {5:"In der Liebe ist die 5 Leidenschaft und Sinnlichkeit: intensive Anziehung, Verführung und Freiheitsdrang.",
           6:"In der Liebe ist die 6 menschliche und solidarische Liebe: Fürsorge, Mitgefühl, Familie und Verantwortung."},
    "ja": {5:"恋愛において5は情熱と官能性：激しい魅力、誘惑、そして自由な愛の欲求。",
           6:"恋愛において6は人間的で連帯する愛：思いやり、慈愛、家族、そして感情的な責任。"},
    "zh": {5:"在爱情中，5是激情与感官：强烈的吸引、诱惑以及对情感自由的渴望。",
           6:"在爱情中，6是人文与团结之爱：关怀、同情、家庭与情感责任。"},
    "ru": {5:"В любви 5 — это страсть и чувственность: сильное влечение, соблазн и стремление к свободе чувств.",
           6:"В любви 6 — это человеческая и солидарная любовь: забота, сострадание, семья и эмоциональная ответственность."},
    "he": {5:"באהבה, 5 הוא תשוקה וחושניות: משיכה עוצמתית, פיתוי ורצון לחופש רגשי.",
           6:"באהבה, 6 הוא אהבה אנושית ומלאת סולידריות: אכפתיות, חמלה, משפחה ואחריות רגשית."},
    "ar": {5:"في الحب، 5 هو شغف وحسية: انجذاب شديد وإغراء ورغبة في الحرية العاطفية.",
           6:"في الحب، 6 هو حب إنساني وتضامني: رعاية ورحمة وأسرة ومسؤولية عاطفية."},
    "id": {5:"Dalam cinta, 5 adalah gairah dan sensualitas: daya tarik yang kuat, godaan, dan keinginan akan kebebasan afektif.",
           6:"Dalam cinta, 6 adalah cinta manusiawi dan solidaritas: kepedulian, kasih sayang, keluarga, dan tanggung jawab afetif."},
    "tr": {5:"Aşkta 5, tutku ve şehvettir: yoğun çekim, baştan çıkarma ve duygusal özgürlük arzusu.",
           6:"Aşkta 6, insani ve dayanışmacı sevgidir: şefkat, merhamet, aile ve duygusal sorumluluk."},
    "vi": {5:"Trong tình yêu, 5 là đam mê và gợi cảm: sự hấp dẫn mãnh liệt, quyến rũ và khao khát tự do tình cảm.",
           6:"Trong tình yêu, 6 là tình yêu nhân văn và đoàn kết: sự quan tâm, lòng trắc ẩn, gia đình và trách nhiệm tình cảm."},
}

# ================================================================
# BLOCO 3 — CAMADA DE UI
# CAL_TXT completo (14 idiomas): camada do Calendário Mensal,
# fim da perda de rota que derrubava a montagem do card.
# EXTRA_TRAD completo (14 idiomas): labels de formulário.
# MESES_TRAD DERIVA de CAL_TXT: fim da triplicação
# (app.js + translations.js + bloco calendário).
# UI_TRAD é populado por colheita byte-perfect do translations.js
# em produção (impossível perder informação na transcrição).
# ================================================================

CAL_TXT = {
    "pt": {"p_calendario":"Calendário Mensal Energético","desc_calendario":"Energia do mês + a SUA energia pessoal naquele mês, com o Ano Pessoal embutido na pesquisa. Descubra os melhores períodos para decisões importantes.","f_cal_univ":"✅ Energia do mês","f_cal_pess":"✅ Sua energia no mês","f_cal_ano_emb":"✅ Ano Pessoal embutido","calc_nome":"Nome completo","f_cal_data":"Data de nascimento","f_cal_ano":"Ano de pesquisa","f_mes":"Mês de referência","ph_nome_completo":"Nome completo","MESES":["Janeiro","Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]},
    "en": {"p_calendario":"Energetic Monthly Calendar","desc_calendario":"The month's energy + YOUR personal energy in that month, with the Personal Year built into the search. Find the best periods for important decisions.","f_cal_univ":"✅ Month's energy","f_cal_pess":"✅ Your energy in the month","f_cal_ano_emb":"✅ Personal Year included","calc_nome":"Full name","f_cal_data":"Date of birth","f_cal_ano":"Search year","f_mes":"Reference month","ph_nome_completo":"Full name","MESES":["January","February","March","April","May","June","July","August","September","October","November","December"]},
    "es": {"p_calendario":"Calendario Mensual Energético","desc_calendario":"La energía del mes + TU energía personal en ese mes, con el Año Personal incluido en la búsqueda. Descubre los mejores períodos para decisiones importantes.","f_cal_univ":"✅ Energía del mes","f_cal_pess":"✅ Tu energía en el mes","f_cal_ano_emb":"✅ Año Personal incluido","calc_nome":"Nombre completo","f_cal_data":"Fecha de nacimiento","f_cal_ano":"Año de búsqueda","f_mes":"Mes de referencia","ph_nome_completo":"Nombre completo","MESES":["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]},
    "it": {"p_calendario":"Calendario Mensile Energetico","desc_calendario":"L'energia del mese + la TUA energia personale in quel mese, con l'Anno Personale incluso nella ricerca. Scopri i migliori periodi per decisioni importanti.","f_cal_univ":"✅ Energia del mese","f_cal_pess":"✅ La tua energia nel mese","f_cal_ano_emb":"✅ Anno Personale incluso","calc_nome":"Nome completo","f_cal_data":"Data di nascita","f_cal_ano":"Anno di ricerca","f_mes":"Mese di riferimento","ph_nome_completo":"Nome completo","MESES":["Gennaio","Febbraio","Marzo","Aprile","Maggio","Giugno","Luglio","Agosto","Settembre","Ottobre","Novembre","Dicembre"]},
    "fr": {"p_calendario":"Calendrier Mensuel Énergétique","desc_calendario":"L'énergie du mois + VOTRE énergie personnelle ce mois-là, avec l'Année Personnelle incluse dans la recherche. Découvrez les meilleures périodes pour les décisions importantes.","f_cal_univ":"✅ Énergie du mois","f_cal_pess":"✅ Votre énergie dans le mois","f_cal_ano_emb":"✅ Année Personnelle incluse","calc_nome":"Nom complet","f_cal_data":"Date de naissance","f_cal_ano":"Année de recherche","f_mes":"Mois de référence","ph_nome_completo":"Nom complet","MESES":["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Août","Septembre","Octobre","Novembre","Décembre"]},
    "de": {"p_calendario":"Energetischer Monatskalender","desc_calendario":"Die Energie des Monats + IHRE persönliche Energie in diesem Monat, mit integriertem Persönlichen Jahr. Finden Sie die besten Zeiträume für wichtige Entscheidungen.","f_cal_univ":"✅ Energie des Monats","f_cal_pess":"✅ Ihre Energie im Monat","f_cal_ano_emb":"✅ Persönliches Jahr inklusive","calc_nome":"Vollständiger Name","f_cal_data":"Geburtsdatum","f_cal_ano":"Suchjahr","f_mes":"Referenzmonat","ph_nome_completo":"Vollständiger Name","MESES":["Januar","Februar","März","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"]},
    "ja": {"p_calendario":"月間エネルギーカレンダー","desc_calendario":"その月のエネルギー＋あなた自身のその月の個人エネルギー。パーソナルイヤーも検索に含まれます。重要な決断に最適な時期を見つけましょう。","f_cal_univ":"✅ 月のエネルギー","f_cal_pess":"✅ あなたのその月のエネルギー","f_cal_ano_emb":"✅ パーソナルイヤー付き","calc_nome":"氏名（フルネーム）","f_cal_data":"生年月日","f_cal_ano":"検索年","f_mes":"対象月","ph_nome_completo":"フルネーム","MESES":["1月","2月","3月","4月","5月","6月","7月","8月","9月","10月","11月","12月"]},
    "zh": {"p_calendario":"月度能量日历","desc_calendario":"当月能量 + 您在该月的个人能量，检索中内置个人年。发现做出重要决定的最佳时期。","f_cal_univ":"✅ 当月能量","f_cal_pess":"✅ 您在该月的能量","f_cal_ano_emb":"✅ 含个人年","calc_nome":"完整姓名","f_cal_data":"出生日期","f_cal_ano":"查询年份","f_mes":"参考月份","ph_nome_completo":"完整姓名","MESES":["1月","2月","3月","4月","5月","6月","7月","8月","9月","10月","11月","12月"]},
    "ru": {"p_calendario":"Энергетический месячный календарь","desc_calendario":"Энергия месяца + ВАША личная энергия в этом месяце, с включённым Личным годом в исследование. Узнайте лучшие периоды для важных решений.","f_cal_univ":"✅ Энергия месяца","f_cal_pess":"✅ Ваша энергия в месяце","f_cal_ano_emb":"✅ Личный год включён","calc_nome":"Полное имя","f_cal_data":"Дата рождения","f_cal_ano":"Год анализа","f_mes":"Месяц анализа","ph_nome_completo":"Полное имя","MESES":["Январь","Февраль","Март","Апрель","Май","Июнь","Июль","Август","Сентябрь","Октябрь","Ноябрь","Декабрь"]},
    "he": {"p_calendario":"לוח שנה אנרגטי חודשי","desc_calendario":"האנרגיה של החודש + האנרגיה האישית שלך באותו חודש, עם השנה האישית הכלולה בחיפוש. גלה את התקופות הטובות ביותר להחלטות חשובות.","f_cal_univ":"✅ אנרגיית החודש","f_cal_pess":"✅ האנרגיה שלך בחודש","f_cal_ano_emb":"✅ השנה האישית כלולה","calc_nome":"שם מלא","f_cal_data":"תאריך לידה","f_cal_ano":"שנת חיפוש","f_mes":"חודש ייחוס","ph_nome_completo":"שם מלא","MESES":["ינואר","פברואר","מרץ","אפריל","מאי","יוני","יולי","אוגוסט","ספטמבר","אוקטובר","נובמבר","דצמבר"]},
    "ar": {"p_calendario":"التقويم الشهري الطاقي","desc_calendario":"طاقة الشهر + طاقتك الشخصية في ذلك الشهر، مع السنة الشخصية مدمجة في البحث. اكتشف أفضل الفترات لاتخاذ القرارات المهمة.","f_cal_univ":"✅ طاقة الشهر","f_cal_pess":"✅ طاقتك في الشهر","f_cal_ano_emb":"✅ السنة الشخصية مدمجة","calc_nome":"الاسم الكامل","f_cal_data":"تاريخ الميلاد","f_cal_ano":"سنة البحث","f_mes":"شهر المرجع","ph_nome_completo":"الاسم الكامل","MESES":["يناير","فبراير","مارس","أبريل","مايو","يونيو","يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"]},
    "id": {"p_calendario":"Kalender Energi Bulanan","desc_calendario":"Energi bulan + energi pribadi ANDA di bulan tersebut, dengan Tahun Pribadi disertakan dalam pencarian. Temukan periode terbaik untuk keputusan penting.","f_cal_univ":"✅ Energi bulan","f_cal_pess":"✅ Energi Anda di bulan itu","f_cal_ano_emb":"✅ Termasuk Tahun Pribadi","calc_nome":"Nama lengkap","f_cal_data":"Tanggal lahir","f_cal_ano":"Tahun pencarian","f_mes":"Bulan acuan","ph_nome_completo":"Nama lengkap","MESES":["Januari","Februari","Maret","April","Mei","Juni","Juli","Agustus","September","Oktober","November","Desember"]},
    "tr": {"p_calendario":"Enerjetik Aylık Takvim","desc_calendario":"Ayın enerjisi + o aydaki KİŞİSEL enerjiniz, aramada Kişisel Yıl dahil. Önemli kararlar için en uygun dönemleri keşfedin.","f_cal_univ":"✅ Ayın enerjisi","f_cal_pess":"✅ O aydaki enerjiniz","f_cal_ano_emb":"✅ Kişisel Yıl dahil","calc_nome":"Tam ad","f_cal_data":"Doğum tarihi","f_cal_ano":"Arama yılı","f_mes":"Referans ay","ph_nome_completo":"Tam ad","MESES":["Ocak","Şubat","Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos","Eylül","Ekim","Kasım","Aralık"]},
    "vi": {"p_calendario":"Lịch Năng lượng Hàng tháng","desc_calendario":"Năng lượng của tháng + năng lượng cá nhân CỦA BẠN trong tháng đó, kèm Năm Cá nhân trong tìm kiếm. Khám phá thời điểm tốt nhất cho các quyết định quan trọng.","f_cal_univ":"✅ Năng lượng của tháng","f_cal_pess":"✅ Năng lượng của bạn trong tháng","f_cal_ano_emb":"✅ Kèm Năm Cá nhân","calc_nome":"Họ tên đầy đủ","f_cal_data":"Ngày sinh","f_cal_ano":"Năm tìm kiếm","f_mes":"Tháng tham chiếu","ph_nome_completo":"Họ tên đầy đủ","MESES":["Tháng 1","Tháng 2","Tháng 3","Tháng 4","Tháng 5","Tháng 6","Tháng 7","Tháng 8","Tháng 9","Tháng 10","Tháng 11","Tháng 12"]},
}

EXTRA_TRAD = {
    "pt": {"f_genero":"Gênero","f_grafias":"Grafias do nome","f_nome_org":"Nome da ONG / Associação / Instituto / Fundação","ph_nome_org":"Nome da organização","f_nome_candidato":"Nome completo do candidato","f_num_atual":"Número atual (opcional, para análise de vibração)","ph_sigla":"Sigla","f_sobrenome_familia":"Sobrenome da família","f_pessoa1":"Nome da primeira pessoa","f_pessoa2":"Nome da segunda pessoa","ph_energia":"1 a 9","confirmar_btn":"Confirmar","cancelar_btn":"Cancelar"},
    "en": {"f_genero":"Gender","f_grafias":"Name spellings","f_nome_org":"NGO, Association, Institute or Foundation name","ph_nome_org":"Organization name","f_nome_candidato":"Candidate's full name","f_num_atual":"Current number (optional, for vibration analysis)","ph_sigla":"Abbreviation","f_sobrenome_familia":"Family surname","f_pessoa1":"First person's name","f_pessoa2":"Second person's name","ph_energia":"1 to 9","confirmar_btn":"Confirm","cancelar_btn":"Cancel"},
    "es": {"f_genero":"Género","f_grafias":"Grafías del nombre","f_nome_org":"Nombre de la ONG, Asociación, Instituto o Fundación","ph_nome_org":"Nombre de la organización","f_nome_candidato":"Nombre completo del candidato","f_num_atual":"Número actual (opcional, para análisis de vibración)","ph_sigla":"Sigla","f_sobrenome_familia":"Apellido de la familia","f_pessoa1":"Nombre de la primera persona","f_pessoa2":"Nombre de la segunda persona","ph_energia":"1 a 9","confirmar_btn":"Confirmar","cancelar_btn":"Cancelar"},
    "it": {"f_genero":"Genere","f_grafias":"Grafie del nome","f_nome_org":"Nome di ONG, Associazione, Istituto o Fondazione","ph_nome_org":"Nome dell'organizzazione","f_nome_candidato":"Nome completo del candidato","f_num_atual":"Numero attuale (facoltativo, per l'analisi della vibrazione)","ph_sigla":"Sigla","f_sobrenome_familia":"Cognome della famiglia","f_pessoa1":"Nome della prima persona","f_pessoa2":"Nome della seconda persona","ph_energia":"1 a 9","confirmar_btn":"Conferma","cancelar_btn":"Annulla"},
    "fr": {"f_genero":"Genre","f_grafias":"Graphies du nom","f_nome_org":"Nom d'ONG, association, institut ou fondation","ph_nome_org":"Nom de l'organisation","f_nome_candidato":"Nom complet du candidat","f_num_atual":"Numéro actuel (facultatif, pour l'analyse de la vibration)","ph_sigla":"Sigle","f_sobrenome_familia":"Nom de famille","f_pessoa1":"Nom de la première personne","f_pessoa2":"Nom de la deuxième personne","ph_energia":"1 à 9","confirmar_btn":"Confirmer","cancelar_btn":"Annuler"},
    "de": {"f_genero":"Geschlecht","f_grafias":"Namensschreibweisen","f_nome_org":"Name von NGO, Verein, Institut oder Stiftung","ph_nome_org":"Name der Organisation","f_nome_candidato":"Vollständiger Name des Kandidaten","f_num_atual":"Aktuelle Nummer (optional, für die Schwingungsanalyse)","ph_sigla":"Kürzel","f_sobrenome_familia":"Familienname","f_pessoa1":"Name der ersten Person","f_pessoa2":"Name der zweiten Person","ph_energia":"1 bis 9","confirmar_btn":"Bestätigen","cancelar_btn":"Abbrechen"},
    "ja": {"f_genero":"性別","f_grafias":"名前の表記","f_nome_org":"NGO・協会・研究所・財団の名前","ph_nome_org":"組織名","f_nome_candidato":"候補者のフルネーム","f_num_atual":"現在の番号（任意、振動分析用）","ph_sigla":"略称","f_sobrenome_familia":"家族の姓","f_pessoa1":"1人目の名前","f_pessoa2":"2人目の名前","ph_energia":"1〜9","confirmar_btn":"確認","cancelar_btn":"キャンセル"},
    "zh": {"f_genero":"性别","f_grafias":"名称写法","f_nome_org":"非政府组织、协会、研究所或基金会名称","ph_nome_org":"组织名称","f_nome_candidato":"候选人全名","f_num_atual":"当前号码（可选，用于振动分析）","ph_sigla":"缩写","f_sobrenome_familia":"家庭姓氏","f_pessoa1":"第一个人的名字","f_pessoa2":"第二个人的名字","ph_energia":"1到9","confirmar_btn":"确认","cancelar_btn":"取消"},
    "ru": {"f_genero":"Пол","f_grafias":"Написания имени","f_nome_org":"Название НКО, ассоциации, института или фонда","ph_nome_org":"Название организации","f_nome_candidato":"Полное имя кандидата","f_num_atual":"Текущий номер (необязательно, для анализа вибрации)","ph_sigla":"Сокращение","f_sobrenome_familia":"Фамилия семьи","f_pessoa1":"Имя первого человека","f_pessoa2":"Имя второго человека","ph_energia":"от 1 до 9","confirmar_btn":"Подтвердить","cancelar_btn":"Отмена"},
    "he": {"f_genero":"מגדר","f_grafias":"כתיב השם","f_nome_org":"שם עמותה, ארגון, מכון או קרן","ph_nome_org":"שם הארגון","f_nome_candidato":"שמו המלא של המועמד","f_num_atual":"המספר הנוכחי (אופציונלי, לניתוח תנודה)","ph_sigla":"ראשי תיבות","f_sobrenome_familia":"שם משפחה","f_pessoa1":"שמו של האדם הראשון","f_pessoa2":"שמו של האדם השני","ph_energia":"1-9","confirmar_btn":"אישור","cancelar_btn":"ביטול"},
    "ar": {"f_genero":"الجنس","f_grafias":"كتابة الاسم","f_nome_org":"اسم منظمة أو جمعية أو معهد أو مؤسسة","ph_nome_org":"اسم المنظمة","f_nome_candidato":"الاسم الكامل للمرشح","f_num_atual":"الرقم الحالي (اختياري، لتحليل الاهتزاز)","ph_sigla":"اختصار","f_sobrenome_familia":"لقب العائلة","f_pessoa1":"اسم الشخص الأول","f_pessoa2":"اسم الشخص الثاني","ph_energia":"1 إلى 9","confirmar_btn":"تأكيد","cancelar_btn":"إلغاء"},
    "id": {"f_genero":"Jenis kelamin","f_grafias":"Ejaan nama","f_nome_org":"Nama LSM, Asosiasi, Lembaga atau Yayasan","ph_nome_org":"Nama organisasi","f_nome_candidato":"Nama lengkap kandidat","f_num_atual":"Nomor saat ini (opsional, untuk analisis getaran)","ph_sigla":"Singkatan","f_sobrenome_familia":"Nama belakang keluarga","f_pessoa1":"Nama orang pertama","f_pessoa2":"Nama orang kedua","ph_energia":"1 sampai 9","confirmar_btn":"Konfirmasi","cancelar_btn":"Batal"},
    "tr": {"f_genero":"Cinsiyet","f_grafias":"İsim yazımları","f_nome_org":"STK, Dernek, Enstitü veya Vakıf Adı","ph_nome_org":"Kuruluş adı","f_nome_candidato":"Adayın tam adı","f_num_atual":"Mevcut numara (isteğe bağlı, titreşim analizi için)","ph_sigla":"Kısaltma","f_sobrenome_familia":"Aile soyadı","f_pessoa1":"Birinci kişinin adı","f_pessoa2":"İkinci kişinin adı","ph_energia":"1 ile 9","confirmar_btn":"Onayla","cancelar_btn":"İptal"},
    "vi": {"f_genero":"Giới tính","f_grafias":"Cách viết tên","f_nome_org":"Tên Tổ chức, Hiệp hội, Viện hoặc Quỹ","ph_nome_org":"Tên tổ chức","f_nome_candidato":"Họ tên đầy đủ của ứng viên","f_num_atual":"Số hiện tại (tùy chọn, để phân tích rung động)","ph_sigla":"Tên viết tắt","f_sobrenome_familia":"Họ của gia đình","f_pessoa1":"Tên người thứ nhất","f_pessoa2":"Tên người thứ hai","ph_energia":"1 đến 9","confirmar_btn":"Xác nhận","cancelar_btn":"Hủy"},
}

MESES_TRAD = {}   # derivado de CAL_TXT (fonte única dos meses)
UI_TRAD = {}      # populado por colheita byte-perfect (função abaixo)

def _derivacao_meses():
    """MESES_TRAD deriva de CAL_TXT: uma só fonte, zero duplicação."""
    for lang in IDIOMAS:
        meses = (CAL_TXT.get(lang) or {}).get("MESES")
        if meses:
            MESES_TRAD[lang] = list(meses)

def colher_ui(caminho="referencia/ui_harvest.json"):
    """Colheita byte-perfect: núcleo vence, colheita preenche o restante."""
    _derivacao_meses()
    _derivar_tabelas()
    if not os.path.exists(caminho):
        print("ui_harvest.json nao encontrado; CAL/EXTRA/FEAT(pt)/BC/DESC/SERVICOS ja validos.")
        return False
    dados = json.load(open(caminho, encoding="utf-8"))
    # UI + EXTRA (como no Bloco 3)
    for lang in IDIOMAS:
        vivo = (dados.get("translations") or {}).get(lang) or {}
        base = dict(vivo)
        for ch, val in (CAL_TXT.get(lang) or {}).items():
            if ch == "MESES":
                continue
            base[ch] = val
        UI_TRAD[lang] = base
        extra = dict((dados.get("EXTRA_TRAD") or {}).get(lang) or {})
        extra.update(EXTRA_TRAD.get(lang) or {})
        EXTRA_TRAD[lang] = extra
        if not MESES_TRAD.get(lang):
            vm = (dados.get("MESES_TRAD") or {}).get(lang)
            if vm: MESES_TRAD[lang] = list(vm)
    # Tabelas: núcleo vence, colheita preenche os demais idiomas
    feat_vivo = dados.get("FEAT_TRAD") or {}
    for lang in IDIOMAS:
        vivo = dict(feat_vivo.get(lang) or {})
        vivo.update(FEAT_TRAD.get(lang) or {})
        FEAT_TRAD[lang] = vivo
    desc_vivo = dados.get("DESC_COLETIVO") or {}
    for lang in IDIOMAS:
        if not DESC_COLETIVO.get(lang) and desc_vivo.get(lang):
            DESC_COLETIVO[lang] = desc_vivo[lang]
    bc_vivo = dados.get("BC_TEXTS") or {}
    for lang in IDIOMAS:
        if not BC_TEXTS.get(lang) and bc_vivo.get(lang):
            BC_TEXTS[lang] = bc_vivo[lang]
    print("Colheita concluida: UI_TRAD %d idiomas; FEAT_TRAD %d idiomas." % (len(UI_TRAD), len(FEAT_TRAD)))
    return True

# ================================================================
# BLOCO 4 — PREÇOS E TABELAS
# Regra: PREÇOS NUNCA SÃO DIGITADOS AQUI. Derivam de precos.py
# (fonte única). Fim do conflito PRECO_DISPLAY antigo x novo.
# FEAT_TRAD pt = canon dos cards do produtos.html (decisão 22/10).
# SERVICOS_TRAD é DERIVADO (nomes de PRODUTOS_TRAD x preços de
# PRECO_DISPLAY): zero preços duplicados em qualquer idioma.
# ================================================================

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
try:
    from precos import PRECO_DISPLAY, PRODUTO_FAIXA, VALORES, SIMBOLO
    _PRECOS_OK = True
except ImportError:
    _PRECOS_OK = False
    PRECO_DISPLAY, PRODUTO_FAIXA, VALORES, SIMBOLO = {}, {}, {}, {}

# ===== FEAT_TRAD — pt = canon produtos.html; demais via colheita =====
FEAT_TRAD = {
    "pt": {
        "express": ["✅ Caminho da Vida","✅ Expressão, Alma, Personalidade","✅ Destino","📲 PDF + QRCode"],
        "vida": ["✅ Fase de Vida atual","✅ Ano Pessoal","✅ Tendências do ciclo","📲 PDF + QRCode"],
        "ia": ["✅ 7 tipos de nome","✅ Análise energética","✅ Sugestões com IA","📲 PDF + QRCode"],
        "nome_pet": ["✅ Nome do pet analisado","✅ Energia do nome","✅ Sintonia com a família","📲 PDF + QRCode"],
        "nickname": ["✅ Nickname analisado","✅ Energia do nome","✅ Imagem no mundo online","📲 PDF + QRCode"],
        "nome_dominio": ["✅ Domínio analisado","✅ Energia do nome","✅ Força para a marca","📲 PDF + QRCode"],
        "nome_canal": ["✅ Canal analisado","✅ Energia do nome","✅ Conexão com a audiência","📲 PDF + QRCode"],
        "nome_equipe": ["✅ Equipe analisada","✅ Energia do nome","✅ União entre os membros","📲 PDF + QRCode"],
        "nome_projeto": ["✅ Projeto analisado","✅ Energia do nome","✅ Impulso para o sucesso","📲 PDF + QRCode"],
        "nome_evento": ["✅ Evento analisado","✅ Energia do nome","✅ Atmosfera para os participantes","📲 PDF + QRCode"],
        "completo": ["✅ 5 números detalhados","✅ 3 Ciclos de Vida","✅ Desafios e Realizações","✅ Grade de Inclusão","📲 PDF + QRCode"],
        "calendario": ["✅ Energia do mês","✅ Sua energia no mês","✅ Ano Pessoal embutido","📲 PDF + QRCode"],
        "urna": ["✅ 5 nomes testados","✅ Sugestões com energia 8","✅ Cálculo letra a letra","📲 PDF + QRCode"],
        "eleitoral": ["✅ 5 números sugeridos","✅ Prioridade energia 8 (Poder)","✅ Cálculo completo","📲 PDF + QRCode"],
        "imovel": ["✅ Número do imóvel analisado","✅ Energia do ambiente","✅ Sugestões de harmonização","📲 PDF + QRCode"],
        "nome_ong": ["✅ ONG analisada","✅ Energia do nome","✅ Causa potencializada","📲 PDF + QRCode"],
        "artistico": ["✅ Nomes testados","✅ Sugestões de palco","✅ Energia do nome","📲 PDF + QRCode"],
        "bebe": ["✅ Sugestões de nomes","✅ Análise energética","✅ Compatibilidade com sobrenome","📲 PDF + QRCode"],
        "assinatura": ["✅ Assinatura atual analisada","✅ Variações sugeridas","✅ Energia da assinatura","📲 PDF + QRCode"],
        "negocio": ["✅ Nomes testados","✅ Sugestões empresariais","✅ Energia do nome","📲 PDF + QRCode"],
        "casal": ["✅ Compatibilidade","✅ Pontos fortes do casal","✅ Desafios da relação","📲 PDF + QRCode"],
        "familia": ["✅ Todos os membros","✅ Sinergia familiar","✅ Orientação por membro","📲 PDF + QRCode"],
        "compatibilidade_equipes": ["✅ Chefe × membros","✅ Membros × membros","✅ Compatibilidade de pares","📲 PDF + QRCode"],
        "coletivo": ["✅ Planos prontos","✅ Sob medida","✅ Descontos progressivos","✅ Códigos de presente"],
    },
}

# ===== DESC_COLETIVO (14 idiomas, verbatim do translations.js) =====
DESC_COLETIVO = {
    "pt":"Contrate brindes numerológicos para seus clientes ou funcionários. Descontos de 10% a 70%.",
    "en":"Hire numerology gifts for your clients or employees. Discounts from 10% to 70%.",
    "es":"Contrata regalos numerológicos para tus clientes o empleados. Descuentos del 10% al 70%.",
    "it":"Assumi regali numerologici per i tuoi clienti o dipendenti. Sconti dal 10% al 70%.",
    "fr":"Engagez des cadeaux numérologiques pour vos clients ou employés. Réductions de 10% à 70%.",
    "de":"Engagieren Sie numerologische Geschenke für Ihre Kunden oder Mitarbeiter. Rabatte von 10% bis 70%.",
    "ja":"顧客や従業員向けの数秘術ギフトを手配します。10%〜70%の割引。",
    "zh":"为您的客户或员工安排数字命理礼物。折扣从10%到70%。",
    "ru":"Закажите нумерологические подарки для клиентов или сотрудников. Скидки от 10% до 70%.",
    "he":"הזמינו מתנות נומרולוגיות ללקוחות או לעובדים שלכם. הנחות מ-10% עד 70%.",
    "ar":"اطلب هدايا الأعداد لعملائك أو موظفيك. خصومات من 10% إلى 70%.",
    "id":"Pesan hadis numerologi untuk klien atau karyawan Anda. Diskon dari 10% hingga 70%.",
    "tr":"Müşterilerin veya çalışanlarınız için numeroloji hediyeleri sipariş edin. %10 ile %70 arasında indirim.",
    "vi":"Đặt mua quà tặng thần số học cho khách hàng hoặc nhân viên của bạn. Giảm giá từ 10% đến 70%.",
}

# ===== BC_TEXTS (tabela BC, 14 idiomas) =====
BC_TEXTS = {
    "pt":{"qtd_total":"Quantidade total:","codigos":"códigos"},
    "en":{"qtd_total":"Total quantity:","codigos":"codes"},
    "es":{"qtd_total":"Cantidad total:","codigos":"códigos"},
    "it":{"qtd_total":"Quantità totale:","codigos":"codici"},
    "fr":{"qtd_total":"Quantité totale:","codigos":"codes"},
    "de":{"qtd_total":"Gesamtmenge:","codigos":"Codes"},
    "ja":{"qtd_total":"合計数量:","codigos":"コード"},
    "zh":{"qtd_total":"总数量:","codigos":"个代码"},
    "ru":{"qtd_total":"Общее количество:","codigos":"кодов"},
    "he":{"qtd_total":"כמות כוללת:","codigos":"קודים"},
    "ar":{"qtd_total":"الكمية الإجمالية:","codigos":"رمز"},
    "id":{"qtd_total":"Jumlah total:","codigos":"kode"},
    "tr":{"qtd_total":"Toplam miktar:","codigos":"kod"},
    "vi":{"qtd_total":"Tổng số lượng:","codigos":"mã"},
}

# ===== SERVICOS_TRAD — DERIVADO (nomes x preços, sem digitação) =====
_SERVICOS_BASE = [("express", 0), ("completo", 1), ("urna", 2), ("eleitoral", 2)]
SERVICOS_TRAD = {}

def _derivar_tabelas():
    """SERVICOS_TRAD = nomes (PRODUTOS_TRAD) x preços (PRECO_DISPLAY de precos.py)."""
    for lang in IDIOMAS:
        disp = PRECO_DISPLAY.get(lang) or PRECO_DISPLAY.get("pt") or []
        linhas = []
        for prod, faixa in _SERVICOS_BASE:
            nome = (PRODUTOS_TRAD.get(lang) or {}).get(prod) or PRODUTOS_TRAD["pt"][prod]
            preco = disp[faixa] if faixa < len(disp) else ""
            linhas.append([nome, preco])
        SERVICOS_TRAD[lang] = linhas

# ===== 5. BLOCO 5 (PDFs e semântica) — cole aqui =====
# ================================================================
# BLOCO 5 — TEXTOS DOS PDFS (14 idiomas, verbatim do dicionarios.py)
# Fonte dos laudos entregues aos clientes. AMOR_TXT (Bloco 2) e
# SIG/CAM/DES/VIB (pt com fallback, por ondas) completam o pacote.
# ================================================================

PDF_TEXTS = {
    "pt": {"t_express":"MAPA EXPRESS","t_completo":"MAPA COMPLETO","t_urna":"VALIDACAO DE NOME DE URNA","t_eleitoral":"NUMERO ELEITORAL","numero":"Numero","valor":"Valor","caminho":"Caminho de Vida","expressao":"Expressao","motivacao":"Motivacao","personalidade":"Personalidade","destino":"Destino","cargo":"Cargo","sugestoes":"Sugestoes:","op8":"Opcoes com Energia 8 - IDEAL:","op_alt":"Opcoes Alternativas:","num_existente":"Numero existente","ciclos":"Ciclo 1 (0-{a}a) | Ciclo 2 ({b}-{c}a) | Ciclo 3 ({d}+a)","desafios":"Desafios: {x} | {y} | Principal {z}","ano_pessoal":"Ano Pessoal {ano}: {v}","grade":"Grade: Presentes {p} | Carencias {c}","baixar":"BAIXAR PDF","confirmado":"Confirmado!","gerado":"Ola {nome}, seu {prod} foi gerado.","voltar":"Voltar","qr_titulo":"Seu PDF nao pode ser gerado.","qr_instrucao":"Escaneie o QRCode abaixo para acessar seu documento.","entrega":"Documento sigiloso - entrega por PDF/QRCode."},
    "en": {"t_express":"EXPRESS MAP","t_completo":"COMPLETE MAP","t_urna":"BALLOT NAME VALIDATION","t_eleitoral":"ELECTORAL NUMBER","numero":"Number","valor":"Value","caminho":"Life Path","expressao":"Expression","motivacao":"Soul Urge","personalidade":"Personality","destino":"Destiny","cargo":"Position","sugestoes":"Suggestions:","op8":"Options with Energy 8 - IDEAL:","op_alt":"Alternative Options:","num_existente":"Existing number","ciclos":"Cycle 1 (0-{a}) | Cycle 2 ({b}-{c}) | Cycle 3 ({d}+)","desafios":"Challenges: {x} | {y} | Main {z}","ano_pessoal":"Personal Year {ano}: {v}","grade":"Grid: Present {p} | Missing {c}","baixar":"DOWNLOAD PDF","confirmado":"Confirmed!","gerado":"Hello {nome}, your {prod} has been generated.","voltar":"Back","qr_titulo":"Your PDF could not be generated.","qr_instrucao":"Scan the QR code below to access your document.","entrega":"Confidential document - delivered via PDF/QRCode."},
    "es": {"t_express":"MAPA EXPRES","t_completo":"MAPA COMPLETO","t_urna":"VALIDACION NOMBRE DE URNA","t_eleitoral":"NUMERO ELECTORAL","numero":"Numero","valor":"Valor","caminho":"Camino de la Vida","expressao":"Expresion","motivacao":"Motivacion","personalidade":"Personalidad","destino":"Destino","cargo":"Cargo","sugestoes":"Sugerencias:","op8":"Opciones con Energia 8 - IDEAL:","op_alt":"Opciones Alternativas:","num_existente":"Numero existente","ciclos":"Ciclo 1 (0-{a}) | Ciclo 2 ({b}-{c}) | Ciclo 3 ({d}+)","desafios":"Desafios: {x} | {y} | Principal {z}","ano_pessoal":"Ano Personal {ano}: {v}","grade":"Cuadricula: Presentes {p} | Ausentes {c}","baixar":"DESCARGAR PDF","confirmado":"Confirmado!","gerado":"Hola {nome}, tu {prod} fue generado.","voltar":"Volver","qr_titulo":"Tu PDF no pudo generarse.","qr_instrucao":"Escanea el codigo QR para acceder a tu documento.","entrega":"Documento confidencial - entrega por PDF/QRCode."},
    "it": {"t_express":"MAPPA ESPRESSA","t_completo":"MAPPA COMPLETA","t_urna":"VALIDAZIONE NOME DELLA SCHEDA","t_eleitoral":"NUMERO ELETTORALE","numero":"Numero","valor":"Valore","caminho":"Sentiero della Vita","expressao":"Espressione","motivacao":"Spinta dell'Anima","personalidade":"Personalita","destino":"Destino","cargo":"Carica","sugestoes":"Suggerimenti:","op8":"Opzioni con Energia 8 - IDEALE:","op_alt":"Opzioni Alternative:","num_existente":"Numero esistente","ciclos":"Ciclo 1 (0-{a}) | Ciclo 2 ({b}-{c}) | Ciclo 3 ({d}+)","desafios":"Sfide: {x} | {y} | Principale {z}","ano_pessoal":"Anno Personale {ano}: {v}","grade":"Griglia: Presenti {p} | Mancanti {c}","baixar":"SCARICA PDF","confirmado":"Confermato!","gerado":"Ciao {nome}, il tuo {prod} e stato generato.","voltar":"Indietro","qr_titulo":"Il tuo PDF non puo essere generato.","qr_instrucao":"Scansiona il QR code per accedere al documento.","entrega":"Documento riservato - consegna via PDF/QRCode."},
    "fr": {"t_express":"CARTE EXPRESS","t_completo":"CARTE COMPLETE","t_urna":"VALIDATION NOM DU BULLETIN","t_eleitoral":"NUMERO ELECTORAL","numero":"Numero","valor":"Valeur","caminho":"Chemin de Vie","expressao":"Expression","motivacao":"Elan de l'Ame","personalidade":"Personnalite","destino":"Destin","cargo":"Poste","sugestoes":"Suggestions :","op8":"Options avec Energie 8 - IDEAL :","op_alt":"Options Alternatives :","num_existente":"Numero existant","ciclos":"Cycle 1 (0-{a}) | Cycle 2 ({b}-{c}) | Cycle 3 ({d}+)","desafios":"Defis : {x} | {y} | Principal {z}","ano_pessoal":"Annee Personnelle {ano} : {v}","grade":"Grille : Presents {p} | Manquants {c}","baixar":"TELECHARGER PDF","confirmado":"Confirme !","gerado":"Bonjour {nome}, votre {prod} a ete genere.","voltar":"Retour","qr_titulo":"Votre PDF n'a pas pu etre genere.","qr_instrucao":"Scannez le QR code pour acceder a votre document.","entrega":"Document confidentiel - livraison par PDF/QRCode."},
    "de": {"t_express":"EXPRESS-KARTE","t_completo":"VOLLSTANDIGE KARTE","t_urna":"STIMMZETTELNAME-VALIDIERUNG","t_eleitoral":"WAHLNUMMER","numero":"Zahl","valor":"Wert","caminho":"Lebensweg","expressao":"Ausdruck","motivacao":"Seelenwunsch","personalidade":"Personlichkeit","destino":"Schicksal","cargo":"Position","sugestoes":"Vorschlage:","op8":"Optionen mit Energie 8 - IDEAL:","op_alt":"Alternative Optionen:","num_existente":"Bestehende Nummer","ciclos":"Zyklus 1 (0-{a}) | Zyklus 2 ({b}-{c}) | Zyklus 3 ({d}+)","desafios":"Herausforderungen: {x} | {y} | Haupt {z}","ano_pessoal":"Persoenliches Jahr {ano}: {v}","grade":"Raster: Vorhanden {p} | Fehlend {c}","baixar":"PDF HERUNTERLADEN","confirmado":"Bestaetigt!","gerado":"Hallo {nome}, Ihr {prod} wurde erstellt.","voltar":"Zurueck","qr_titulo":"Ihr PDF konnte nicht erstellt werden.","qr_instrucao":"Scannen Sie den QR-Code, um auf Ihr Dokument zuzugreifen.","entrega":"Vertrauliches Dokument - Lieferung per PDF/QRCode."},
    "ja": {"t_express":"エクスプレスマップ","t_completo":"完全マップ","t_urna":"投票用紙名の検証","t_eleitoral":"選挙番号","numero":"数字","valor":"値","caminho":"ライフパス","expressao":"表現","motivacao":"魂の欲求","personalidade":"性格","destino":"運命","cargo":"役職","sugestoes":"提案:","op8":"エネルギー8のオプション - 理想的:","op_alt":"代替オプション:","num_existente":"既存の番号","ciclos":"サイクル1 (0-{a}) | サイクル2 ({b}-{c}) | サイクル3 ({d}+)","desafios":"課題: {x} | {y} | 主要 {z}","ano_pessoal":"パーソナルイヤー {ano}: {v}","grade":"グリッド: あり {p} | 欠け {c}","baixar":"PDFをダウンロード","confirmado":"確認済み!","gerado":"{nome} さん、{prod} が生成されました。","voltar":"戻る","qr_titulo":"PDFを生成できませんでした。","qr_instrucao":"下のQRコードをスキャンして文書にアクセスしてください。","entrega":"機密文書 - PDF/QRコードで納品。"},
    "zh": {"t_express":"快速地图","t_completo":"完整地图","t_urna":"选票名称验证","t_eleitoral":"选举号码","numero":"数字","valor":"数值","caminho":"生命路径","expressao":"表达","motivacao":"灵魂冲动","personalidade":"个性","destino":"命运","cargo":"职位","sugestoes":"建议:","op8":"能量8选项 - 理想:","op_alt":"备选方案:","num_existente":"现有号码","ciclos":"周期1 (0-{a}) | 周期2 ({b}-{c}) | 周期3 ({d}+)","desafios":"挑战: {x} | {y} | 主要 {z}","ano_pessoal":"个人年份 {ano}: {v}","grade":"网格: 存在 {p} | 缺失 {c}","baixar":"下载PDF","confirmado":"已确认!","gerado":"您好 {nome}，您的{prod}已生成。","voltar":"返回","qr_titulo":"无法生成PDF。","qr_instrucao":"扫描下方二维码访问您的文档。","entrega":"保密文档 - 通过PDF/二维码交付。"},
    "ru": {"t_express":"ЭКСПРЕСС-КАРТА","t_completo":"ПОЛНАЯ КАРТА","t_urna":"ПРОВЕРКА НАЗВАНИЯ БЮЛЛЕТЕНЯ","t_eleitoral":"ИЗБИРАТЕЛЬНЫЙ НОМЕР","numero":"Число","valor":"Значение","caminho":"Путь Жизни","expressao":"Выражение","motivacao":"Порыв Души","personalidade":"Личность","destino":"Судьба","cargo":"Должность","sugestoes":"Предложения:","op8":"Варианты с Энергией 8 - ИДЕАЛ:","op_alt":"Альтернативные варианты:","num_existente":"Существующий номер","ciclos":"Цикл 1 (0-{a}) | Цикл 2 ({b}-{c}) | Цикл 3 ({d}+)","desafios":"Вызовы: {x} | {y} | Главный {z}","ano_pessoal":"Личный год {ano}: {v}","grade":"Сетка: Есть {p} | Нет {c}","baixar":"СКАЧАТЬ PDF","confirmado":"Подтверждено!","gerado":"Здравствуйте {nome}, ваш {prod} создан.","voltar":"Назад","qr_titulo":"Не удалось создать PDF.","qr_instrucao":"Отсканируйте QR-код ниже, чтобы получить доступ к документу.","entrega":"Конфиденциальный документ - доставка через PDF/QRCode."},
    "he": {"t_express":"מפה מהירה","t_completo":"מפה מלאה","t_urna":"אימות שם פתק","t_eleitoral":"מספר בחירות","numero":"מספר","valor":"ערך","caminho":"נתיב החיים","expressao":"ביטוי","motivacao":"דחף הנשמה","personalidade":"אישיות","destino":"גורל","cargo":"תפקיד","sugestoes":"הצעות:","op8":"אפשרויות עם אנרגיה 8 - אידיאלי:","op_alt":"אפשרויות חלופיות:","num_existente":"מספר קיים","ciclos":"מחזור 1 (0-{a}) | מחזור 2 ({b}-{c}) | מחזור 3 ({d}+)","desafios":"אתגרים: {x} | {y} | עיקרי {z}","ano_pessoal":"שנה אישית {ano}: {v}","grade":"רשת: קיימים {p} | חסרים {c}","baixar":"הורד PDF","confirmado":"אושר!","gerado":"שלום {nome}, ה-{prod} שלך נוצר.","voltar":"חזור","qr_titulo":"לא ניתן היה ליצור את ה-PDF.","qr_instrucao":"סרוק את קוד ה-QR למטה כדי לגשת למסמך שלך.","entrega":"מסמך חסוי - מסירה באמצעות PDF/QRCode."},
    "ar": {"t_express":"خريطة سريعة","t_completo":"خريطة كاملة","t_urna":"التحقق من اسم الاقتراع","t_eleitoral":"الرقم الانتخابي","numero":"الرقم","valor":"القيمة","caminho":"مسار الحياة","expressao":"التعبير","motivacao":"دافع الروح","personalidade":"الشخصية","destino":"القدر","cargo":"المنصب","sugestoes":"اقتراحات:","op8":"خيارات بالطاقة 8 - مثالي:","op_alt":"خيارات بديلة:","num_existente":"الرقم الموجود","ciclos":"دورة 1 (0-{a}) | دورة 2 ({b}-{c}) | دورة 3 ({d}+)","desafios":"التحديات: {x} | {y} | الرئيسي {z}","ano_pessoal":"السنة الشخصية {ano}: {v}","grade":"الشبكة: موجودة {p} | ناقصة {c}","baixar":"تحميل PDF","confirmado":"تم التأكيد!","gerado":"مرحباً {nome}، تم إنشاء {prod} الخاص بك.","voltar":"رجوع","qr_titulo":"تعذر إنشاء ملف PDF الخاص بك.","qr_instrucao":"امسح رمز QR أدناه للوصول إلى مستندك.","entrega":"مستند سري - التسليم عبر PDF/QRCode."},
    "id": {"t_express":"PETA EKSPRES","t_completo":"PETA LENGKAP","t_urna":"VALIDASI NAMA SURAT SUARA","t_eleitoral":"NOMOR PEMILIHAN","numero":"Nomor","valor":"Nilai","caminho":"Jalan Hidup","expressao":"Ekspresi","motivacao":"Dorongan Jiwa","personalidade":"Kepribadian","destino":"Takdir","cargo":"Jabatan","sugestoes":"Saran:","op8":"Opsi dengan Energi 8 - IDEAL:","op_alt":"Opsi Alternatif:","num_existente":"Nomor yang ada","ciclos":"Siklus 1 (0-{a}) | Siklus 2 ({b}-{c}) | Siklus 3 ({d}+)","desafios":"Tantangan: {x} | {y} | Utama {z}","ano_pessoal":"Tahun Pribadi {ano}: {v}","grade":"Kisi: Ada {p} | Kurang {c}","baixar":"UNDUH PDF","confirmado":"Dikonfirmasi!","gerado":"Halo {nome}, {prod} Anda telah dibuat.","voltar":"Kembali","qr_titulo":"PDF Anda tidak dapat dibuat.","qr_instrucao":"Pindai kode QR di bawah untuk mengakses dokumen Anda.","entrega":"Dokumen rahasia - pengiriman via PDF/QRCode."},
    "tr": {"t_express":"EKSPRES HARITA","t_completo":"TAM HARITA","t_urna":"OY PUSULASI ADI DOĞRULAMA","t_eleitoral":"SEÇİM NUMARASI","numero":"Sayı","valor":"Değer","caminho":"Yaşam Yolu","expressao":"İfade","motivacao":"Ruh Arzusu","personalidade":"Kişilik","destino":"Kader","cargo":"Görev","sugestoes":"Öneriler:","op8":"Enerji 8'li Seçenekler - İDEAL:","op_alt":"Alternatif Seçenekler:","num_existente":"Mevcut numara","ciclos":"Döngü 1 (0-{a}) | Döngü 2 ({b}-{c}) | Döngü 3 ({d}+)","desafios":"Zorluklar: {x} | {y} | Ana {z}","ano_pessoal":"Kişisel Yıl {ano}: {v}","grade":"Izgara: Mevcut {p} | Eksik {c}","baixar":"PDF İNDİR","confirmado":"Onaylandı!","gerado":"Merhaba {nome}, {prod} oluşturuldu.","voltar":"Geri","qr_titulo":"PDF'niz oluşturulamadı.","qr_instrucao":"Erişmek için aşağıdaki QR kodunu tarayın.","entrega":"Gizli belge - PDF/QRCode ile teslim."},
    "vi": {"t_express":"BẢN ĐỒ NHANH","t_completo":"BẢN ĐỒ ĐẦY ĐỦ","t_urna":"XÁC MINH TÊN PHIẾU BẦU","t_eleitoral":"SỐ BẦU CỬ","numero":"Số","valor":"Giá trị","caminho":"Đường đời","expressao":"Biểu hiện","motivacao":"Khao khát tâm","personalidade":"Tính cách","destino":"Số phận","cargo":"Chức vụ","sugestoes":"Gợi ý:","op8":"Tùy chọn Năng lượng 8 - LÝ TƯỞNG:","op_alt":"Tùy chọn Thay thế:","num_existente":"Số hiện có","ciclos":"Chu kỳ 1 (0-{a}) | Chu kỳ 2 ({b}-{c}) | Chu kỳ 3 ({d}+)","desafios":"Thách thức: {x} | {y} | Chính {z}","ano_pessoal":"Năm Cá nhân {ano}: {v}","grade":"Lưới: Có {p} | Thiếu {c}","baixar":"TẢI PDF","confirmado":"Đã xác nhận!","gerado":"Xin chào {nome}, {prod} của bạn đã được tạo.","voltar":"Quay lại","qr_titulo":"Không thể tạo PDF của bạn.","qr_instrucao":"Quét mã QR bên dưới để truy cập tài liệu của bạn.","entrega":"Tài liệu bí mật - giao qua PDF/QRCode."},
}

PDF_SECOES = {
    "pt": {"numeros_principais":"Seus Números Principais","caminho_ciclos":"Caminho da Vida e Ciclos","desafios_realizacoes":"Desafios e Realizações","como_calculamos":"Como calculamos?","por_que_energia_8":"Por que a energia 8?","energia_8_ideal":"Energia 8 — IDEAL:","alternativas":"Alternativas:"},
    "en": {"numeros_principais":"Your Main Numbers","caminho_ciclos":"Life Path and Cycles","desafios_realizacoes":"Challenges and Achievements","como_calculamos":"How do we calculate?","por_que_energia_8":"Why energy 8?","energia_8_ideal":"Energy 8 — IDEAL:","alternativas":"Alternatives:"},
    "es": {"numeros_principais":"Tus Números Principales","caminho_ciclos":"Camino de la Vida y Ciclos","desafios_realizacoes":"Desafíos y Logros","como_calculamos":"¿Cómo calculamos?","por_que_energia_8":"¿Por qué la energía 8?","energia_8_ideal":"Energía 8 — IDEAL:","alternativas":"Alternativas:"},
    "it": {"numeros_principais":"I Tuoi Numeri Principali","caminho_ciclos":"Percorso di Vita e Cicli","desafios_realizacoes":"Sfide e Traguardi","como_calculamos":"Come calcoliamo?","por_que_energia_8":"Perché l'energia 8?","energia_8_ideal":"Energia 8 — IDEALE:","alternativas":"Alternative:"},
    "fr": {"numeros_principais":"Vos Nombres Principaux","caminho_ciclos":"Chemin de Vie et Cycles","desafios_realizacoes":"Défis et Réalisations","como_calculamos":"Comment calculons-nous ?","por_que_energia_8":"Pourquoi l'énergie 8 ?","energia_8_ideal":"Énergie 8 — IDÉAL :","alternativas":"Alternatives :"},
    "de": {"numeros_principais":"Ihre Hauptzahlen","caminho_ciclos":"Lebensweg und Zyklen","desafios_realizacoes":"Herausforderungen und Erfolge","como_calculamos":"Wie berechnen wir?","por_que_energia_8":"Warum Energie 8?","energia_8_ideal":"Energie 8 — IDEAL:","alternativas":"Alternativen:"},
    "ja": {"numeros_principais":"あなたの主要な数字","caminho_ciclos":"ライフパスと周期","desafios_realizacoes":"課題と達成","como_calculamos":"どう計算しますか？","por_que_energia_8":"なぜエネルギー8なのか？","energia_8_ideal":"エネルギー8 — 理想的:","alternativas":"代替案:"},
    "zh": {"numeros_principais":"你的主要数字","caminho_ciclos":"生命道路与周期","desafios_realizacoes":"挑战与成就","como_calculamos":"我们如何计算？","por_que_energia_8":"为什么是能量8？","energia_8_ideal":"能量8 — 理想:","alternativas":"备选方案:"},
    "ru": {"numeros_principais":"Ваши главные числа","caminho_ciclos":"Путь жизни и циклы","desafios_realizacoes":"Вызовы и достижения","como_calculamos":"Как мы считаем?","por_que_energia_8":"Почему энергия 8?","energia_8_ideal":"Энергия 8 — ИДЕАЛ:","alternativas":"Альтернативы:"},
    "he": {"numeros_principais":"המספרים העיקריים שלך","caminho_ciclos":"נתיב החיים ומחזורים","desafios_realizacoes":"אתגרים והישגים","como_calculamos":"איך אנחנו מחשבים?","por_que_energia_8":"למה אנרגיה 8?","energia_8_ideal":"אנרגיה 8 — אידיאלי:","alternativas":"חלופות:"},
    "ar": {"numeros_principais":"أرقامك الرئيسية","caminho_ciclos":"مسار الحياة والدورات","desafios_realizacoes":"التحديات والإنجازات","como_calculamos":"كيف نحسب؟","por_que_energia_8":"لماذا الطاقة 8؟","energia_8_ideal":"الطاقة 8 — مثالي:","alternativas":"بدائل:"},
    "id": {"numeros_principais":"Angka Utama Anda","caminho_ciclos":"Jalan Hidup dan Siklus","desafios_realizacoes":"Tantangan dan Pencapaian","como_calculamos":"Bagaimana kami menghitung?","por_que_energia_8":"Mengapa energi 8?","energia_8_ideal":"Energi 8 — IDEAL:","alternativas":"Alternatif:"},
    "tr": {"numeros_principais":"Ana Numaralarınız","caminho_ciclos":"Yaşam Yolu ve Döngüler","desafios_realizacoes":"Zorluklar ve Başarılar","como_calculamos":"Nasıl hesaplıyoruz?","por_que_energia_8":"Neden enerji 8?","energia_8_ideal":"Enerji 8 — İDEAL:","alternativas":"Alternatifler:"},
    "vi": {"numeros_principais":"Các Số Chính của Bạn","caminho_ciclos":"Đường đời và Chu kỳ","desafios_realizacoes":"Thách thức và Thành đạt","como_calculamos":"Chúng tôi tính như thế nào?","por_que_energia_8":"Tại sao là năng lượng 8?","energia_8_ideal":"Năng lượng 8 — LÝ TƯỞNG:","alternativas":"Phương án thay thế:"},
}

BOAS_VINDAS = {
    "pt":"Seja bem-vindo(a)! Este relatório revela as energias que moldam a sua essência. Que a sabedoria dos números ilumine o seu caminho.",
    "en":"Welcome! This report reveals the energies that shape your essence. May the wisdom of numbers illuminate your path.",
    "es":"¡Bienvenido(a)! Este informe revela las energías que moldean tu esencia. Que la sabiduría de los números ilumine tu camino.",
    "it":"Benvenuto/a! Questo report rivela le energie che plasmano la tua essenza. Che la saggezza dei numeri illumini il tuo cammino.",
    "fr":"Bienvenue ! Ce rapport révèle les énergies qui façonnent votre essence. Que la sagesse des nombres éclaire votre chemin.",
    "de":"Willkommen! Dieser Bericht offenbart die Energien, die Ihr Wesen prägen. Möge die Weisheit der Zahlen Ihren Weg erhellen.",
    "ja":"ようこそ！このレポートは、あなたの本質を形作るエネルギーを明らかにします。数字の叡智があなたの道を照らしますように。",
    "zh":"欢迎！这份报告揭示了塑造您本质的能量。愿数字的智慧照亮您的道路。",
    "ru":"Добро пожаловать! Этот отчёт раскрывает энергии, формирующие вашу сущность. Пусть мудрость чисел осветит ваш путь.",
    "he":"ברוכים הבאים! דוח זה חושף את האנרגיות המעצבות את מהותכם. שתאיר חכמת המספרים את דרככם.",
    "ar":"مرحباً بك! يكشف هذا التقرير الطاقات التي تشكل جوهرك. لتنير حكمة الأرقام طريقك.",
    "id":"Selamat datang! Laporan ini mengungkap energi yang membentuk esensi Anda. Semoga kebijaksanaan angka mencerahkan jalan Anda.",
    "tr":"Hoş geldiniz! Bu rapor özünüzü şekillendiren enerjileri ortaya koyar. Sayıların bilgeliği yolunuzu aydınlatsın.",
    "vi":"Chào bạn! Báo cáo này tiết lộ những năng lượng định hình bản chất của bạn. Cầu trí tuệ của các con số soi sáng con đường của bạn.",
}

PERIODOS = {
    "pt":("0 a 28/36 anos","28/36 a 54/63 anos","54/63 anos em diante"),
    "en":("0 to 28/36 years","28/36 to 54/63 years","54/63 years and beyond"),
    "es":("0 a 28/36 años","28/36 a 54/63 años","54/63 años en adelante"),
    "it":("0-28/36 anni","28/36-54/63 anni","54/63 anni in poi"),
    "fr":("0 à 28/36 ans","28/36 à 54/63 ans","54/63 ans et plus"),
    "de":("0 bis 28/36 Jahre","28/36 bis 54/63 Jahre","54/63 Jahre und mehr"),
    "ja":("0〜28/36歳","28/36〜54/63歳","54/63歳以上"),
    "zh":("0至28/36岁","28/36至54/63岁","54/63岁以上"),
    "ru":("0-28/36 лет","28/36-54/63 лет","54/63 лет и старше"),
    "he":("0-28/36 שנים","28/36-54/63 שנים","54/63 ומעלה"),
    "ar":("0-28/36 سنة","28/36-54/63 سنة","54/63 سنة فأكثر"),
    "id":("0-28/36 tahun","28/36-54/63 tahun","54/63 tahun ke atas"),
    "tr":("0-28/36 yıl","28/36-54/63 yıl","54/63 yıl ve üzeri"),
    "vi":("0-28/36 tuổi","28/36-54/63 tuổi","54/63 tuổi trở lên"),
}

REALIZ_HEAD = {
    "pt":("Fase","Período"),"en":("Phase","Period"),"es":("Fase","Período"),
    "it":("Fase","Periodo"),"fr":("Phase","Période"),"de":("Phase","Zeitraum"),
    "ja":("段階","期間"),"zh":("阶段","时期"),"ru":("Этап","Период"),
    "he":("שלב","תקופה"),"ar":("المرحلة","الفترة"),"id":("Fase","Periode"),
    "tr":("Aşama","Dönem"),"vi":("Giai đoạn","Thời kỳ"),
}

# ================= EXECUÇÃO DIRETA =================
# Rode: python referencia/traducoes_nucleo.py
# (a partir da raiz do projeto, pasta numerologia-app)
if __name__ == "__main__":
    colher_ui()
    validar()
