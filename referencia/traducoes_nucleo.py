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
