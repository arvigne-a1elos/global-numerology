// ===== A1ELOS GLOBAL NUMEROLOGY - PRODUTOS.JS (VERSÃO BLINDADA v3) =====
// REGRA DE OURO: NENHUMA declaração var/let/const em nível de topo.
// Todos os dados globais usam window.NOME — IMPOSSÍVEL dar
// "Identifier has already been declared", mesmo se colado 2x.

/* ===== PREÇOS GLOBAIS ===== */
window.PRECO_BASE = window.PRECO_BASE || {
  pt:[8,17,26,35,44,98], en:[20,44,71,89,116,251], es:[11,26,35,53,62,134],
  it:[11,26,35,53,62,134], fr:[11,26,35,53,62,134], de:[11,26,35,53,62,134],
  ja:[1400,3000,4600,6200,7700,17000], zh:[26,53,71,98,125,260],
  ru:[440,800,1250,1700,2150,4400], id:[11000,23000,36000,48000,60000,134000],
  tr:[58,123,188,254,319,710], vi:[25000,53000,81000,109000,137000,305000],
  he:[44,98,143,197,242,530], ar:[35,71,107,143,170,377]
};
window.SIMB = window.SIMB || {pt:'R$',en:'US$',es:'€',it:'€',fr:'€',de:'€',ja:'¥',zh:'¥',ru:'₽',id:'Rp',tr:'₺',vi:'₫',he:'₪',ar:'﷼'};
if (!window.PRECO_DISPLAY) {
  window.PRECO_DISPLAY = {};
  Object.keys(window.PRECO_BASE).forEach(function(l){
    var zero = (l==='ja'||l==='vi');
    window.PRECO_DISPLAY[l] = window.PRECO_BASE[l].map(function(v){
      var txt = zero ? String(v) : v.toFixed(2).replace('.', ',');
      return window.SIMB[l]+' '+txt;
    });
  });
}

window._traduzindo = window._traduzindo || false;
window.BC_QUANTIDADES = window.BC_QUANTIDADES || {};

/* ===== CONF_COLETA ===== */
window.CONF_COLETA = window.CONF_COLETA || {
  nome_canal:   { labelTipo:"f_tipo_canal",   tipos:["youtube","podcast","tiktok","twitch"],        temArea:true,  areas:["esporte","noticias","politica","beleza"], temDetalhe:false },
  nickname:     { labelTipo:"f_tipo_nickname", tipos:["gamer","profissional","criador","artista"],  temArea:false, areas:[], temDetalhe:false },
  nome_ong:     { labelTipo:"f_tipo_ong",      tipos:["ong","instituto","associacao","fundacao"],   temArea:false, areas:[], temDetalhe:false },
  nome_evento:  { labelTipo:"f_tipo_evento",   tipos:["show","congresso","festa","curso","palestra"],temArea:true,  areas:["musica","esporte","cultura","politica","beleza"], temDetalhe:false },
  nome_projeto: { labelTipo:"f_tipo_projeto",  tipos:["pessoal","social","empresarial","cultural"], temArea:false, areas:[], temDetalhe:false },
  nome_equipe:  { labelTipo:"f_tipo_equipe",   tipos:["empresarial","projeto","esportiva","banda"], temArea:false, areas:[], temDetalhe:false },
  nome_dominio: { labelTipo:"f_tipo_site",     tipos:["loja","empresa","blog","portfolio"],         temArea:true,  areas:["comercio","industria","servicos","pessoal"], temDetalhe:false },
  nome_pet:     { labelTipo:"f_tipo_pet",      tipos:["cao","gato","passaro","reptil"],             temArea:false, areas:[], temDetalhe:true }
};

/* ===== PESQUISAR (scroll/abertura por produto — 8 novos produtos) ===== */
function pesquisar(produto) {
  if (produto === "express" || produto === "completo") {
    var sec = document.getElementById("calculadora") || document.getElementById("calcSection");
    if (sec) sec.scrollIntoView({ behavior: "smooth", block: "center" });
    return;
  }
  if (window.CONF_COLETA && window.CONF_COLETA[produto]) {
    if (typeof comprar === "function") { comprar(produto); return; }
    return;
  }
  var alvo = document.getElementById("form-" + produto);
  if (alvo) {
    alvo.scrollIntoView({ behavior: "smooth", block: "center" });
    alvo.style.transition = "box-shadow .5s";
    alvo.style.boxShadow = "0 0 0 3px var(--gold)";
    setTimeout(function(){ alvo.style.boxShadow = ""; }, 2000);
    return;
  }
  var calc = document.getElementById("calculadora") || document.getElementById("calcSection");
  if (calc) calc.scrollIntoView({ behavior: "smooth" });
}

/* ===== PRODUTOS_TRAD (23 produtos, 14 idiomas) ===== */
window.PRODUTOS_TRAD = window.PRODUTOS_TRAD || {
 pt:{express:"Mapa Express",vida:"Qual Vida/Ano",completo:"Mapa Completo",ia:"Pesquisa IA de Nomes",urna:"Validação Nome de Urna",eleitoral:"Número Eleitoral",imovel:"Número do Imóvel",calendario:"Calendário Mensal Energético",artistico:"Validação Nome Artístico",bebe:"Planejamento Nome de Bebê",assinatura:"Validação de Assinaturas",negocio:"Nome para Negócio/Produto",casal:"Mapa do Casal",familia:"Mapa Família Premium",coletivo:"Bônus Coletivo/Empresarial",nome_pet:"Nome do Pet",nickname:"Nickname Digital",nome_dominio:"Nome do Domínio",nome_canal:"Nome do Canal",nome_equipe:"Nome da Equipe",nome_ong:"Nome de ONG, Associação, Instituto ou Fundação",nome_projeto:"Nome do Projeto",nome_evento:"Nome do Evento"},
 en:{express:"Express Map",vida:"Life Phase & Year",completo:"Complete Map",ia:"AI Name Search",urna:"Ballot Name Validation",eleitoral:"Electoral Number",imovel:"Property Number",calendario:"Monthly Energy Calendar",artistico:"Artistic Name Validation",bebe:"Baby Name Planning",assinatura:"Signature Validation",negocio:"Business & Product Name",casal:"Couple Map",familia:"Premium Family Map",coletivo:"Corporate Bonus",nome_pet:"Pet Name",nickname:"Digital Nickname",nome_dominio:"Domain Name",nome_canal:"Channel Name",nome_equipe:"Team Name",nome_ong:"NGO, Association, Institute or Foundation Name",nome_projeto:"Project Name",nome_evento:"Event Name"},
 es:{express:"Mapa Exprés",vida:"Ciclo de Vida y Año",completo:"Mapa Completo",ia:"Búsqueda IA de Nombres",urna:"Validación Nombre de Urna",eleitoral:"Número Electoral",imovel:"Número de la Propiedad",calendario:"Calendario Mensual Energético",artistico:"Validación Nombre Artístico",bebe:"Planificación Nombre de Bebé",assinatura:"Validación de Firmas",negocio:"Nombre para Negocio/Producto",casal:"Mapa de Pareja",familia:"Mapa Familiar Premium",coletivo:"Bono Corporativo",nome_pet:"Nombre de la Mascota",nickname:"Apodo Digital",nome_dominio:"Nombre de Dominio",nome_canal:"Nombre del Canal",nome_equipe:"Nombre del Equipo",nome_ong:"Nombre de ONG, Asociacion, Instituto o Fundacion",nome_projeto:"Nombre del Proyecto",nome_evento:"Nombre del Evento"},
 it:{express:"Mappa Espressa",vida:"Fase di Vita e Anno",completo:"Mappa Completa",ia:"Ricerca IA Nomi",urna:"Validazione Nome della Scheda",eleitoral:"Numero Elettorale",imovel:"Numero dell'Immobile",calendario:"Calendario Mensile Energetico",artistico:"Validazione Nome d'Arte",bebe:"Pianificazione Nome del Bambino",assinatura:"Validazione delle Firme",negocio:"Nome per Business/Prodotto",casal:"Mappa di Coppia",familia:"Mappa Famiglia Premium",coletivo:"Bonus Aziendale",nome_pet:"Nome dell'Animale",nickname:"Nickname Digitale",nome_dominio:"Nome del Dominio",nome_canal:"Nome del Canale",nome_equipe:"Nome del Team",nome_ong:"Nome di ONG, Associazione, Istituto o Fondazione",nome_projeto:"Nome del Progetto",nome_evento:"Nome dell'Evento"},
 fr:{express:"Carte Express",vida:"Phase de Vie et Année",completo:"Carte Complète",ia:"Recherche IA de Noms",urna:"Validation Nom du Bulletin",eleitoral:"Numéro Électoral",imovel:"Numéro du Bien",calendario:"Calendrier Mensuel Énergétique",artistico:"Validation Nom de Scène",bebe:"Planification Prénom de Bébé",assinatura:"Validation des Signatures",negocio:"Nom pour Entreprise/Produit",casal:"Carte du Couple",familia:"Carte Famille Premium",coletivo:"Bonus d'Entreprise",nome_pet:"Nom de l'Animal",nickname:"Pseudo Numerique",nome_dominio:"Nom de Domaine",nome_canal:"Nom de la Chaine",nome_equipe:"Nom de l'Equipe",nome_ong:"Nom d'ONG, Association, Institut ou Fondation",nome_projeto:"Nom du Projet",nome_evento:"Nom de l'Evenement"},
 de:{express:"Express-Karte",vida:"Lebensphase & Jahr",completo:"Vollständige Karte",ia:"KI-Namenssuche",urna:"Stimmzettelname-Validierung",eleitoral:"Wahlnummer",imovel:"Immobiliennummer",calendario:"Monatlicher Energiekalender",artistico:"Künstlername-Validierung",bebe:"Babynamen-Planung",assinatura:"Unterschrifts-Validierung",negocio:"Name für Unternehmen/Produkt",casal:"Paar-Karte",familia:"Premium-Familien-Karte",coletivo:"Unternehmensbonus",nome_pet:"Haustiername",nickname:"Digitaler Spitzname",nome_dominio:"Domainname",nome_canal:"Kanalname",nome_equipe:"Teamname",nome_ong:"Name von NGO, Verein, Institut oder Stiftung",nome_projeto:"Projektname",nome_evento:"Veranstaltungsname"},
 ja:{express:"エクスプレスマップ",vida:"ライフステージと年",completo:"完全マップ",ia:"AI名前検索",urna:"投票用紙名の検証",eleitoral:"選挙番号",imovel:"不動産番号",calendario:"月間エネルギーカレンダー",artistico:"芸名の検証",bebe:"赤ちゃんの名前計画",assinatura:"署名の検証",negocio:"ビジネス・商品名",casal:"カップルマップ",familia:"プレミアム家族マップ",coletivo:"法人ボーナス",nome_pet:"ペットの名前",nickname:"デジタルニックネーム",nome_dominio:"ドメイン名",nome_canal:"チャンネル名",nome_equipe:"チーム名",nome_ong:"NGO・協会・研究所・財団の名前",nome_projeto:"プロジェクト名",nome_evento:"イベント名"},
 zh:{express:"快速地图",vida:"生命阶段与年份",completo:"完整地图",ia:"AI名字搜索",urna:"选票名称验证",eleitoral:"选举号码",imovel:"房产号码",calendario:"每月能量日历",artistico:"艺名验证",bebe:"宝宝取名规划",assinatura:"签名验证",negocio:"企业/产品名称",casal:"情侣地图",familia:"高级家庭地图",coletivo:"企业奖励",nome_pet:"宠物名字",nickname:"数字昵称",nome_dominio:"域名",nome_canal:"频道名称",nome_equipe:"团队名称",nome_ong:"非政府组织、协会、研究所或基金会名称",nome_projeto:"项目名称",nome_evento:"活动名称"},
 ru:{express:"Экспресс-карта",vida:"Жизненный этап и год",completo:"Полная карта",ia:"ИИ-поиск имён",urna:"Проверка названия бюллетеня",eleitoral:"Избирательный номер",imovel:"Номер недвижимости",calendario:"Ежемесячный энергетический календарь",artistico:"Проверка сценического имени",bebe:"Планирование имени ребёнка",assinatura:"Проверка подписей",negocio:"Название для бизнеса/продукта",casal:"Карта пары",familia:"Премиальная семейная карта",coletivo:"Корпоративный бонус",nome_pet:"Имя питомца",nickname:"Цифровой никнейм",nome_dominio:"Имя домена",nome_canal:"Название канала",nome_equipe:"Название команды",nome_ong:"Название НКО, ассоциации, института или фонда",nome_projeto:"Название проекта",nome_evento:"Название события"},
 id:{express:"Peta Ekspres",vida:"Fase Kehidupan & Tahun",completo:"Peta Lengkap",ia:"Pencarian Nama AI",urna:"Validasi Nama Surat Suara",eleitoral:"Nomor Elektoral",imovel:"Nomor Properti",calendario:"Kalender Energi Bulanan",artistico:"Validasi Nama Artistik",bebe:"Perencanaan Nama Bayi",assinatura:"Validasi Tanda Tangan",negocio:"Nama untuk Bisnis/Produk",casal:"Peta Pasangan",familia:"Peta Keluarga Premium",coletivo:"Bonus Kolektif/Perusahaan",nome_pet:"Nama Hewan Peliharaan",nickname:"Nama Panggilan Digital",nome_dominio:"Nama Domain",nome_canal:"Nama Kanal",nome_equipe:"Nama Tim",nome_ong:"Nama LSM, Asosiasi, Lembaga atau Yayasan",nome_projeto:"Nama Proyek",nome_evento:"Nama Acara"},
 tr:{express:"Ekspres Harita",vida:"Yaşam Evresi ve Yıl",completo:"Tam Harita",ia:"AI İsim Arama",urna:"Oy Pusulası İsim Doğrulama",eleitoral:"Seçim Numarası",imovel:"Mülk Numarası",calendario:"Aylık Enerji Takvimi",artistico:"Sahne Adı Doğrulama",bebe:"Bebek İsmi Planlama",assinatura:"İmza Doğrulama",negocio:"İşletme/Ürün Adı",casal:"Çift Haritası",familia:"Premium Aile Haritası",coletivo:"Kurumsal Bonus",nome_pet:"Evcil Hayvan Adı",nickname:"Dijital Takma Ad",nome_dominio:"Alan Adı",nome_canal:"Kanal Adı",nome_equipe:"Ekip Adı",nome_ong:"STK, Dernek, Enstitü veya Vakıf Adı",nome_projeto:"Proje Adı",nome_evento:"Etkinlik Adı"},
 vi:{express:"Bản Đồ Nhanh",vida:"Giai Đoạn Cuộc Đời & Năm",completo:"Bản Đồ Đầy Đủ",ia:"Tìm Kiếm Tên AI",urna:"Xác Minh Tên Phiếu Bầu",eleitoral:"Số Bầu Cử",imovel:"Số Bất Động Sản",calendario:"Lịch Năng Lượng Hàng Tháng",artistico:"Xác Minh Nghệ Danh",bebe:"Lên Kế Hoạch Tên Cho Bé",assinatura:"Xác Minh Chữ Ký",negocio:"Tên Cho Doanh Nghiệp/Sản Phẩm",casal:"Bản Đồ Cặp Đôi",familia:"Bản Đồ Gia Đình Cao Cấp",coletivo:"Thưởng Tập Thể/Doanh Nghiệp",nome_pet:"Tên Thú Cưng",nickname:"Biệt Danh Kỹ Thuật Số",nome_dominio:"Tên Miền",nome_canal:"Tên Kênh",nome_equipe:"Tên Đội Nhóm",nome_ong:"Tên Tổ Chức, Hiệp Hội, Viện hoặc Quỹ",nome_projeto:"Tên Dự Án",nome_evento:"Tên Sự Kiện"},
 he:{express:"מפה מהירה",vida:"שלב חיים ושנה",completo:"מפה מלאה",ia:"חיפוש שמות AI",urna:"אימות שם פתק",eleitoral:"מספר בחירות",imovel:"מספר נכס",calendario:"לוח אנרגיה חודשי",artistico:"אימות שם במה",bebe:"תכנון שם לתינוק",assinatura:"אימות חתימות",negocio:"שם לעסק/מוצר",casal:"מפת זוג",familia:"מפת משפחה פרימיום",coletivo:"בונוס ארגוני",nome_pet:"שם חיית המחמד",nickname:"כינוי דיגיטלי",nome_dominio:"שם דומיין",nome_canal:"שם הערוץ",nome_equipe:"שם הצוות",nome_ong:"שם עמותה, ארגון, מכון או קרן",nome_projeto:"שם הפרויקט",nome_evento:"שם האירוע"},
 ar:{express:"خريطة سريعة",vida:"مرحلة الحياة والسنة",completo:"خريطة كاملة",ia:"بحث الأسماء بالذكاء الاصطناعي",urna:"التحقق من اسم الاقتراع",eleitoral:"الرقم الانتخابي",imovel:"رقم العقار",calendario:"التقويم الشهري للطاقة",artistico:"التحقق من الاسم الفني",bebe:"تخطيط اسم الطفل",assinatura:"التحقق من التوقيعات",negocio:"اسم للأعمال/المنتج",casal:"خريطة الزوجين",familia:"خريطة العائلة المميزة",coletivo:"مكافأة الشركات",nome_pet:"اسم الحيوان الأليف",nickname:"اللقب الرقمي",nome_dominio:"اسم النطاق",nome_canal:"اسم القناة",nome_equipe:"اسم الفريق",nome_ong:"اسم منظمة أو جمعية أو معهد أو مؤسسة",nome_projeto:"اسم المشروع",nome_evento:"اسم الفعالية"}
};

/* ===== PRODUTO_FAIXA ===== */
window.PRODUTO_FAIXA = window.PRODUTO_FAIXA || {
  express:0, vida:0, nome_pet:0, nickname:0, nome_dominio:0, nome_canal:0, nome_equipe:0, nome_ong:0, nome_projeto:0, nome_evento:0,
  completo:1, ia:1, urna:2, eleitoral:2, imovel:2, calendario:2,
  artistico:3, bebe:3, assinatura:3, negocio:4, casal:4, familia:5, coletivo:5
};

/* ===== FEAT_TRAD v1 — FEATURES DOS 23 CARDS EM 14 IDIOMAS ===== */
window.FEAT_TRAD = window.FEAT_TRAD || {};
if (!window.FEAT_TRAD.pt) {
  (function () {
    var F = {
      pt: {
        cam_vida:"✅ Caminho da Vida", expr_alma_pers:"✅ Expressão, Alma, Personalidade", destino:"✅ Destino",
        fase_atual:"✅ Fase de Vida atual", ano_pessoal:"✅ Ano Pessoal", tendencias:"✅ Tendências do ciclo",
        n5_detalhados:"✅ 5 números detalhados", ciclos3:"✅ 3 Ciclos de Vida", desafios_real:"✅ Desafios e Realizações",
        grade_inclusao:"✅ Grade de Inclusão", sug_ia:"✅ Sugestões com IA", analise_energ_nomes:"✅ Análise energética de nomes",
        comparativo:"✅ Comparativo de opções", n5_nomes_test:"✅ 5 nomes testados", sug_energia8:"✅ Sugestões com energia 8",
        calc_letra:"✅ Cálculo letra a letra", n5_sugeridos:"✅ 5 números sugeridos", prior_energia8:"✅ Prioridade energia 8 (Poder)",
        calc_completo:"✅ Cálculo completo", imovel_anal:"✅ Número do imóvel analisado", energia_ambiente:"✅ Energia do ambiente",
        sug_harmon:"✅ Sugestões de harmonização", vibracao_diaria:"✅ Vibração diária", dias_favoraveis:"✅ Dias favoráveis",
        orient_mensal:"✅ Orientação mensal", nomes_testados:"✅ Nomes testados", sug_palco:"✅ Sugestões de palco",
        energia_nome:"✅ Energia do nome", sug_nomes:"✅ Sugestões de nomes", analise_energ:"✅ Análise energética",
        comp_sobrenome:"✅ Compatibilidade com sobrenome", assin_atual:"✅ Assinatura atual analisada", variacoes:"✅ Variações sugeridas",
        energia_assin:"✅ Energia da assinatura", sug_empresariais:"✅ Sugestões empresariais", compatibilidade:"✅ Compatibilidade",
        pontos_fortes:"✅ Pontos fortes do casal", desafios_relacao:"✅ Desafios da relação", todos_membros:"✅ Todos os membros",
        sinergia:"✅ Sinergia familiar", orient_membro:"✅ Orientação por membro", planos_prontos:"✅ Planos prontos",
        sob_medida:"✅ Sob medida", descontos_prog:"✅ Descontos progressivos", codigos_presente:"✅ Códigos de presente",
        pet_anal:"✅ Nome do pet analisado", sintonia_familia:"✅ Sintonia com a família", nick_anal:"✅ Nickname analisado",
        imagem_online:"✅ Imagem no mundo online", dominio_anal:"✅ Domínio analisado", forca_marca:"✅ Força para a marca",
        canal_anal:"✅ Canal analisado", conexao_audiencia:"✅ Conexão com a audiência", equipe_anal:"✅ Equipe analisada",
        uniao_membros:"✅ União entre os membros", ong_anal:"✅ ONG analisada", causa_potencial:"✅ Causa potencializada",
        projeto_anal:"✅ Projeto analisado", impulso_sucesso:"✅ Impulso para o sucesso", evento_anal:"✅ Evento analisado",
        atmosfera:"✅ Atmosfera para os participantes", pdf:"📲 PDF + QRCode"
      },
      en: {
        cam_vida:"✅ Life Path", expr_alma_pers:"✅ Expression, Soul, Personality", destino:"✅ Destiny",
        fase_atual:"✅ Current Life Phase", ano_pessoal:"✅ Personal Year", tendencias:"✅ Cycle Trends",
        n5_detalhados:"✅ 5 detailed numbers", ciclos3:"✅ 3 Life Cycles", desafios_real:"✅ Challenges and Achievements",
        grade_inclusao:"✅ Inclusion Grid", sug_ia:"✅ AI Suggestions", analise_energ_nomes:"✅ Energy analysis of names",
        comparativo:"✅ Options comparison", n5_nomes_test:"✅ 5 names tested", sug_energia8:"✅ Suggestions with energy 8",
        calc_letra:"✅ Letter-by-letter calculation", n5_sugeridos:"✅ 5 suggested numbers", prior_energia8:"✅ Energy 8 priority (Power)",
        calc_completo:"✅ Complete calculation", imovel_anal:"✅ Property number analyzed", energia_ambiente:"✅ Environment energy",
        sug_harmon:"✅ Harmonization suggestions", vibracao_diaria:"✅ Daily vibration", dias_favoraveis:"✅ Favorable days",
        orient_mensal:"✅ Monthly guidance", nomes_testados:"✅ Names tested", sug_palco:"✅ Stage suggestions",
        energia_nome:"✅ Name energy", sug_nomes:"✅ Name suggestions", analise_energ:"✅ Energy analysis",
        comp_sobrenome:"✅ Last name compatibility", assin_atual:"✅ Current signature analyzed", variacoes:"✅ Suggested variations",
        energia_assin:"✅ Signature energy", sug_empresariais:"✅ Business suggestions", compatibilidade:"✅ Compatibility",
        pontos_fortes:"✅ Couple's strengths", desafios_relacao:"✅ Relationship challenges", todos_membros:"✅ All members",
        sinergia:"✅ Family synergy", orient_membro:"✅ Per-member guidance", planos_prontos:"✅ Ready-made plans",
        sob_medida:"✅ Custom-made", descontos_prog:"✅ Progressive discounts", codigos_presente:"✅ Gift codes",
        pet_anal:"✅ Pet name analyzed", sintonia_familia:"✅ Family connection", nick_anal:"✅ Nickname analyzed",
        imagem_online:"✅ Online image", dominio_anal:"✅ Domain analyzed", forca_marca:"✅ Brand strength",
        canal_anal:"✅ Channel analyzed", conexao_audiencia:"✅ Audience connection", equipe_anal:"✅ Team analyzed",
        uniao_membros:"✅ Unity among members", ong_anal:"✅ NGO analyzed", causa_potencial:"✅ Amplified cause",
        projeto_anal:"✅ Project analyzed", impulso_sucesso:"✅ Success boost", evento_anal:"✅ Event analyzed",
        atmosfera:"✅ Atmosphere for participants", pdf:"📲 PDF + QR Code"
      },
      es: {
        cam_vida:"✅ Camino de Vida", expr_alma_pers:"✅ Expresión, Alma, Personalidad", destino:"✅ Destino",
        fase_atual:"✅ Fase de Vida actual", ano_pessoal:"✅ Año Personal", tendencias:"✅ Tendencias del ciclo",
        n5_detalhados:"✅ 5 números detallados", ciclos3:"✅ 3 Ciclos de Vida", desafios_real:"✅ Desafíos y Realizaciones",
        grade_inclusao:"✅ Cuadrícula de Inclusión", sug_ia:"✅ Sugerencias con IA", analise_energ_nomes:"✅ Análisis energético de nombres",
        comparativo:"✅ Comparativo de opciones", n5_nomes_test:"✅ 5 nombres probados", sug_energia8:"✅ Sugerencias con energía 8",
        calc_letra:"✅ Cálculo letra a letra", n5_sugeridos:"✅ 5 números sugeridos", prior_energia8:"✅ Prioridad energía 8 (Poder)",
        calc_completo:"✅ Cálculo completo", imovel_anal:"✅ Número de la propiedad analizado", energia_ambiente:"✅ Energía del ambiente",
        sug_harmon:"✅ Sugerencias de armonización", vibracao_diaria:"✅ Vibración diaria", dias_favoraveis:"✅ Días favorables",
        orient_mensal:"✅ Orientación mensual", nomes_testados:"✅ Nombres probados", sug_palco:"✅ Sugerencias de escenario",
        energia_nome:"✅ Energía del nombre", sug_nomes:"✅ Sugerencias de nombres", analise_energ:"✅ Análisis energético",
        comp_sobrenome:"✅ Compatibilidad con apellido", assin_atual:"✅ Firma actual analizada", variacoes:"✅ Variaciones sugeridas",
        energia_assin:"✅ Energía de la firma", sug_empresariais:"✅ Sugerencias empresariales", compatibilidade:"✅ Compatibilidad",
        pontos_fortes:"✅ Fortalezas de la pareja", desafios_relacao:"✅ Desafíos de la relación", todos_membros:"✅ Todos los miembros",
        sinergia:"✅ Sinergia familiar", orient_membro:"✅ Orientación por miembro", planos_prontos:"✅ Planos listos",
        sob_medida:"✅ A medida", descontos_prog:"✅ Descuentos progresivos", codigos_presente:"✅ Códigos de regalo",
        pet_anal:"✅ Nombre de la mascota analizado", sintonia_familia:"✅ Conexión con la familia", nick_anal:"✅ Apodo analizado",
        imagem_online:"✅ Imagen en el mundo online", dominio_anal:"✅ Dominio analizado", forca_marca:"✅ Fuerza para la marca",
        canal_anal:"✅ Canal analizado", conexao_audiencia:"✅ Conexión con la audiencia", equipe_anal:"✅ Equipo analizado",
        uniao_membros:"✅ Unión entre los miembros", ong_anal:"✅ ONG analizada", causa_potencial:"✅ Causa potenciada",
        projeto_anal:"✅ Proyecto analizado", impulso_sucesso:"✅ Impulso para el éxito", evento_anal:"✅ Evento analizado",
        atmosfera:"✅ Ambiente para los participantes", pdf:"📲 PDF + Código QR"
      },
      it: {
        cam_vida:"✅ Percorso di Vita", expr_alma_pers:"✅ Espressione, Anima, Personalità", destino:"✅ Destino",
        fase_atual:"✅ Fase di Vita attuale", ano_pessoal:"✅ Anno Personale", tendencias:"✅ Tendenze del ciclo",
        n5_detalhados:"✅ 5 numeri dettagliati", ciclos3:"✅ 3 Cicli di Vita", desafios_real:"✅ Sfide e Realizzazioni",
        grade_inclusao:"✅ Griglia di Inclusione", sug_ia:"✅ Suggerimenti con IA", analise_energ_nomes:"✅ Analisi energetica dei nomi",
        comparativo:"✅ Confronto di opzioni", n5_nomes_test:"✅ 5 nomi testati", sug_energia8:"✅ Suggerimenti con energia 8",
        calc_letra:"✅ Calcolo lettera per lettera", n5_sugeridos:"✅ 5 numeri suggeriti", prior_energia8:"✅ Priorità energia 8 (Potere)",
        calc_completo:"✅ Calcolo completo", imovel_anal:"✅ Numero dell'immobile analizzato", energia_ambiente:"✅ Energia dell'ambiente",
        sug_harmon:"✅ Suggerimenti di armonizzazione", vibracao_diaria:"✅ Vibrazione giornaliera", dias_favoraveis:"✅ Giorni favorevoli",
        orient_mensal:"✅ Orientamento mensile", nomes_testados:"✅ Nomi testati", sug_palco:"✅ Suggerimenti di palcoscenico",
        energia_nome:"✅ Energia del nome", sug_nomes:"✅ Suggerimenti di nomi", analise_energ:"✅ Analisi energetica",
        comp_sobrenome:"✅ Compatibilità con il cognome", assin_atual:"✅ Firma attuale analizzata", variacoes:"✅ Variazioni suggerite",
        energia_assin:"✅ Energia della firma", sug_empresariais:"✅ Suggerimenti aziendali", compatibilidade:"✅ Compatibilità",
        pontos_fortes:"✅ Punti di forza della coppia", desafios_relacao:"✅ Sfide della relazione", todos_membros:"✅ Tutti i membri",
        sinergia:"✅ Sinergia familiare", orient_membro:"✅ Orientamento per membro", planos_prontos:"✅ Piani pronti",
        sob_medida:"✅ Su misura", descontos_prog:"✅ Sconti progressivi", codigos_presente:"✅ Codici regalo",
        pet_anal:"✅ Nome dell'animale analizzato", sintonia_familia:"✅ Sintonia con la famiglia", nick_anal:"✅ Nickname analizzato",
        imagem_online:"✅ Immagine nel mondo online", dominio_anal:"✅ Dominio analizzato", forca_marca:"✅ Forza per il marchio",
        canal_anal:"✅ Canale analizzato", conexao_audiencia:"✅ Connessione con il pubblico", equipe_anal:"✅ Team analizzato",
        uniao_membros:"✅ Unione tra i membri", ong_anal:"✅ ONG analizzata", causa_potencial:"✅ Causa potenziata",
        projeto_anal:"✅ Progetto analizzato", impulso_sucesso:"✅ Spinta verso il successo", evento_anal:"✅ Evento analizzato",
        atmosfera:"✅ Atmosfera per i partecipanti", pdf:"📲 PDF + Codice QR"
      },
      fr: {
        cam_vida:"✅ Chemin de Vie", expr_alma_pers:"✅ Expression, Âme, Personnalité", destino:"✅ Destinée",
        fase_atual:"✅ Phase de Vie actuelle", ano_pessoal:"✅ Année Personnelle", tendencias:"✅ Tendances du cycle",
        n5_detalhados:"✅ 5 nombres détaillés", ciclos3:"✅ 3 Cycles de Vie", desafios_real:"✅ Défis et Réalisations",
        grade_inclusao:"✅ Grille d'Inclusion", sug_ia:"✅ Suggestions avec IA", analise_energ_nomes:"✅ Analyse énergétique des noms",
        comparativo:"✅ Comparatif d'options", n5_nomes_test:"✅ 5 noms testés", sug_energia8:"✅ Suggestions avec énergie 8",
        calc_letra:"✅ Calcul lettre par lettre", n5_sugeridos:"✅ 5 nombres suggérés", prior_energia8:"✅ Priorité énergie 8 (Pouvoir)",
        calc_completo:"✅ Calcul complet", imovel_anal:"✅ Numéro du bien analysé", energia_ambiente:"✅ Énergie de l'environnement",
        sug_harmon:"✅ Suggestions d'harmonisation", vibracao_diaria:"✅ Vibration quotidienne", dias_favoraveis:"✅ Jours favorables",
        orient_mensal:"✅ Orientation mensuelle", nomes_testados:"✅ Noms testés", sug_palco:"✅ Suggestions de scène",
        energia_nome:"✅ Énergie du nom", sug_nomes:"✅ Suggestions de noms", analise_energ:"✅ Analyse énergétique",
        comp_sobrenome:"✅ Compatibilité avec le nom de famille", assin_atual:"✅ Signature actuelle analysée", variacoes:"✅ Variations suggérées",
        energia_assin:"✅ Énergie de la signature", sug_empresariais:"✅ Suggestions commerciales", compatibilidade:"✅ Compatibilité",
        pontos_fortes:"✅ Points forts du couple", desafios_relacao:"✅ Défis de la relation", todos_membros:"✅ Tous les membres",
        sinergia:"✅ Synergie familiale", orient_membro:"✅ Orientation par membre", planos_prontos:"✅ Plans prêts",
        sob_medida:"✅ Sur mesure", descontos_prog:"✅ Remises progressives", codigos_presente:"✅ Codes cadeau",
        pet_anal:"✅ Nom de l'animal analysé", sintonia_familia:"✅ Connexion avec la famille", nick_anal:"✅ Pseudo analysé",
        imagem_online:"✅ Image dans le monde en ligne", dominio_anal:"✅ Domaine analysé", forca_marca:"✅ Force pour la marque",
        canal_anal:"✅ Chaîne analysée", conexao_audiencia:"✅ Connexion avec l'audience", equipe_anal:"✅ Équipe analysée",
        uniao_membros:"✅ Union entre les membres", ong_anal:"✅ ONG analysée", causa_potencial:"✅ Cause amplifiée",
        projeto_anal:"✅ Projet analysé", impulso_sucesso:"✅ Élan vers le succès", evento_anal:"✅ Événement analysé",
        atmosfera:"✅ Atmosphère pour les participants", pdf:"📲 PDF + Code QR"
      },
      de: {
        cam_vida:"✅ Lebensweg", expr_alma_pers:"✅ Ausdruck, Seele, Persönlichkeit", destino:"✅ Schicksal",
        fase_atual:"✅ Aktuelle Lebensphase", ano_pessoal:"✅ Persönliches Jahr", tendencias:"✅ Zyklustrends",
        n5_detalhados:"✅ 5 detaillierte Zahlen", ciclos3:"✅ 3 Lebenszyklen", desafios_real:"✅ Herausforderungen und Errungenschaften",
        grade_inclusao:"✅ Inklusionsraster", sug_ia:"✅ Vorschläge mit KI", analise_energ_nomes:"✅ Energieanalyse von Namen",
        comparativo:"✅ Optionsvergleich", n5_nomes_test:"✅ 5 Namen getestet", sug_energia8:"✅ Vorschläge mit Energie 8",
        calc_letra:"✅ Buchstabe für Buchstabe berechnet", n5_sugeridos:"✅ 5 vorgeschlagene Zahlen", prior_energia8:"✅ Priorität Energie 8 (Macht)",
        calc_completo:"✅ Vollständige Berechnung", imovel_anal:"✅ Immobiliennummer analysiert", energia_ambiente:"✅ Energie der Umgebung",
        sug_harmon:"✅ Harmonisierungshinweise", vibracao_diaria:"✅ Tägliche Schwingung", dias_favoraveis:"✅ Günstige Tage",
        orient_mensal:"✅ Monatliche Orientierung", nomes_testados:"✅ Namen getestet", sug_palco:"✅ Bühnennamen-Vorschläge",
        energia_nome:"✅ Namensenergie", sug_nomes:"✅ Namensvorschläge", analise_energ:"✅ Energieanalyse",
        comp_sobrenome:"✅ Kompatibilität mit Nachnamen", assin_atual:"✅ Aktuelle Unterschrift analysiert", variacoes:"✅ Vorgeschlagene Variationen",
        energia_assin:"✅ Energie der Unterschrift", sug_empresariais:"✅ Geschäftliche Vorschläge", compatibilidade:"✅ Kompatibilität",
        pontos_fortes:"✅ Stärken des Paares", desafios_relacao:"✅ Herausforderungen der Beziehung", todos_membros:"✅ Alle Mitglieder",
        sinergia:"✅ Familiensynergie", orient_membro:"✅ Orientierung pro Mitglied", planos_prontos:"✅ Fertige Pläne",
        sob_medida:"✅ Maßgeschneidert", descontos_prog:"✅ Gestaffelte Rabatte", codigos_presente:"✅ Geschenk-Codes",
        pet_anal:"✅ Haustiername analysiert", sintonia_familia:"✅ Verbindung zur Familie", nick_anal:"✅ Spitzname analysiert",
        imagem_online:"✅ Online-Image", dominio_anal:"✅ Domain analysiert", forca_marca:"✅ Stärke für die Marke",
        canal_anal:"✅ Kanal analysiert", conexao_audiencia:"✅ Verbindung zum Publikum", equipe_anal:"✅ Team analysiert",
        uniao_membros:"✅ Zusammenhalt der Mitglieder", ong_anal:"✅ NGO analysiert", causa_potencial:"✅ Verstärkte Wirkung der Sache",
        projeto_anal:"✅ Projekt analysiert", impulso_sucesso:"✅ Schub für den Erfolg", evento_anal:"✅ Veranstaltung analysiert",
        atmosfera:"✅ Atmosphäre für die Teilnehmer", pdf:"📲 PDF + QR-Code"
      },
      ru: {
        cam_vida:"✅ Путь Жизни", expr_alma_pers:"✅ Экспрессия, Душа, Личность", destino:"✅ Судьба",
        fase_atual:"✅ Текущий этап жизни", ano_pessoal:"✅ Персональный год", tendencias:"✅ Тенденции цикла",
        n5_detalhados:"✅ 5 подробных чисел", ciclos3:"✅ 3 жизненных цикла", desafios_real:"✅ Вызовы и достижения",
        grade_inclusao:"✅ Сетка включения", sug_ia:"✅ Рекомендации с ИИ", analise_energ_nomes:"✅ Энергетический анализ имён",
        comparativo:"✅ Сравнение вариантов", n5_nomes_test:"✅ 5 проверенных имён", sug_energia8:"✅ Рекомендации с энергией 8",
        calc_letra:"✅ Расчёт по буквам", n5_sugeridos:"✅ 5 предложенных чисел", prior_energia8:"✅ Приоритет энергии 8 (Власть)",
        calc_completo:"✅ Полный расчёт", imovel_anal:"✅ Номер недвижимости проанализирован", energia_ambiente:"✅ Энергия окружения",
        sug_harmon:"✅ Рекомендации по гармонизации", vibracao_diaria:"✅ Ежедневная вибрация", dias_favoraveis:"✅ Благоприятные дни",
        orient_mensal:"✅ Ежемесячные рекомендации", nomes_testados:"✅ Имена проверены", sug_palco:"✅ Сценические варианты",
        energia_nome:"✅ Энергия имени", sug_nomes:"✅ Варианты имён", analise_energ:"✅ Энергетический анализ",
        comp_sobrenome:"✅ Совместимость с фамилией", assin_atual:"✅ Текущая подпись проанализирована", variacoes:"✅ Предложенные варианты",
        energia_assin:"✅ Энергия подписи", sug_empresariais:"✅ Бизнес-рекомендации", compatibilidade:"✅ Совместимость",
        pontos_fortes:"✅ Сильные стороны пары", desafios_relacao:"✅ Вызовы в отношениях", todos_membros:"✅ Все члены",
        sinergia:"✅ Семейная синергия", orient_membro:"✅ Рекомендации для каждого члена", planos_prontos:"✅ Готовые планы",
        sob_medida:"✅ Индивидуально", descontos_prog:"✅ Прогрессивные скидки", codigos_presente:"✅ Подарочные коды",
        pet_anal:"✅ Имя питомца проанализировано", sintonia_familia:"✅ Связь с семьёй", nick_anal:"✅ Никнейм проанализирован",
        imagem_online:"✅ Образ в онлайн-мире", dominio_anal:"✅ Домен проанализирован", forca_marca:"✅ Сила для бренда",
        canal_anal:"✅ Канал проанализирован", conexao_audiencia:"✅ Связь с аудиторией", equipe_anal:"✅ Команда проанализирована",
        uniao_membros:"✅ Единство между членами", ong_anal:"✅ НКО проанализирована", causa_potencial:"✅ Дело усилено",
        projeto_anal:"✅ Проект проанализирован", impulso_sucesso:"✅ Импульс к успеху", evento_anal:"✅ Событие проанализировано",
        atmosfera:"✅ Атмосфера для участников", pdf:"📲 PDF + QR-код"
      },
      zh: {
        cam_vida:"✅ 生命道路", expr_alma_pers:"✅ 表现、灵魂、个性", destino:"✅ 命运",
        fase_atual:"✅ 当前人生阶段", ano_pessoal:"✅ 个人年份", tendencias:"✅ 周期趋势",
        n5_detalhados:"✅ 5个详细数字", ciclos3:"✅ 3个生命周期", desafios_real:"✅ 挑战与成就",
        grade_inclusao:"✅ 包含网格", sug_ia:"✅ AI建议", analise_energ_nomes:"✅ 名字能量分析",
        comparativo:"✅ 选项比较", n5_nomes_test:"✅ 测试5个名字", sug_energia8:"✅ 能量8的建议",
        calc_letra:"✅ 逐字母计算", n5_sugeridos:"✅ 5个推荐数字", prior_energia8:"✅ 能量8优先（力量）",
        calc_completo:"✅ 完整计算", imovel_anal:"✅ 房产号码分析", energia_ambiente:"✅ 环境能量",
        sug_harmon:"✅ 协调建议", vibracao_diaria:"✅ 每日振动", dias_favoraveis:"✅ 吉日",
        orient_mensal:"✅ 月度指引", nomes_testados:"✅ 名字已测试", sug_palco:"✅ 舞台名字建议",
        energia_nome:"✅ 名字能量", sug_nomes:"✅ 名字建议", analise_energ:"✅ 能量分析",
        comp_sobrenome:"✅ 姓氏兼容性", assin_atual:"✅ 当前签名分析", variacoes:"✅ 建议变体",
        energia_assin:"✅ 签名能量", sug_empresariais:"✅ 商业建议", compatibilidade:"✅ 兼容性",
        pontos_fortes:"✅ 情侣优势", desafios_relacao:"✅ 关系挑战", todos_membros:"✅ 所有成员",
        sinergia:"✅ 家庭协同", orient_membro:"✅ 按成员指引", planos_prontos:"✅ 现成方案",
        sob_medida:"✅ 定制", descontos_prog:"✅ 阶梯折扣", codigos_presente:"✅ 礼品码",
        pet_anal:"✅ 宠物名字分析", sintonia_familia:"✅ 与家庭的连接", nick_anal:"✅ 昵称分析",
        imagem_online:"✅ 网络形象", dominio_anal:"✅ 域名分析", forca_marca:"✅ 品牌力量",
        canal_anal:"✅ 频道分析", conexao_audiencia:"✅ 与观众连接", equipe_anal:"✅ 团队分析",
        uniao_membros:"✅ 成员团结", ong_anal:"✅ 组织分析", causa_potencial:"✅ 事业增强",
        projeto_anal:"✅ 项目分析", impulso_sucesso:"✅ 成功助推", evento_anal:"✅ 活动分析",
        atmosfera:"✅ 参与者氛围", pdf:"📲 PDF + 二维码"
      },
      ja: {
        cam_vida:"✅ ライフパス", expr_alma_pers:"✅ 表現・魂・性格", destino:"✅ 運命",
        fase_atual:"✅ 現在のライフステージ", ano_pessoal:"✅ パーソナルイヤー", tendencias:"✅ サイクルの傾向",
        n5_detalhados:"✅ 詳細な5つの数字", ciclos3:"✅ 3つのライフサイクル", desafios_real:"✅ 課題と達成",
        grade_inclusao:"✅ インクルージョングリッド", sug_ia:"✅ AIによる提案", analise_energ_nomes:"✅ 名前のエネルギー分析",
        comparativo:"✅ 選択肢の比較", n5_nomes_test:"✅ 5つの名前をテスト", sug_energia8:"✅ エネルギー8の提案",
        calc_letra:"✅ 文字ごとの計算", n5_sugeridos:"✅ 提案された5つの数字", prior_energia8:"✅ エネルギー8優先（力）",
        calc_completo:"✅ 完全な計算", imovel_anal:"✅ 不動産番号を分析", energia_ambiente:"✅ 環境のエネルギー",
        sug_harmon:"✅ 調和の提案", vibracao_diaria:"✅ 毎日の振動", dias_favoraveis:"✅ 吉日",
        orient_mensal:"✅ 毎月のガイダンス", nomes_testados:"✅ テスト済みの名前", sug_palco:"✅ ステージ名の提案",
        energia_nome:"✅ 名前のエネルギー", sug_nomes:"✅ 名前の提案", analise_energ:"✅ エネルギー分析",
        comp_sobrenome:"✅ 姓との相性", assin_atual:"✅ 現在の署名を分析", variacoes:"✅ 提案されたバリエーション",
        energia_assin:"✅ 署名のエネルギー", sug_empresariais:"✅ ビジネス提案", compatibilidade:"✅ 相性",
        pontos_fortes:"✅ カップルの強み", desafios_relacao:"✅ 関係の課題", todos_membros:"✅ 全メンバー",
        sinergia:"✅ 家族のシナジー", orient_membro:"✅ メンバー別ガイダンス", planos_prontos:"✅ 既製プラン",
        sob_medida:"✅ カスタムメイド", descontos_prog:"✅ 段階的割引", codigos_presente:"✅ ギフトコード",
        pet_anal:"✅ ペット名を分析", sintonia_familia:"✅ 家族とのつながり", nick_anal:"✅ ニックネームを分析",
        imagem_online:"✅ オンライン上のイメージ", dominio_anal:"✅ ドメインを分析", forca_marca:"✅ ブランドの力",
        canal_anal:"✅ チャンネルを分析", conexao_audiencia:"✅ 視聴者とのつながり", equipe_anal:"✅ チームを分析",
        uniao_membros:"✅ メンバー間の結束", ong_anal:"✅ NGOを分析", causa_potencial:"✅ 活動を強化",
        projeto_anal:"✅ プロジェクトを分析", impulso_sucesso:"✅ 成功への後押し", evento_anal:"✅ イベントを分析",
        atmosfera:"✅ 参加者のための雰囲気", pdf:"📲 PDF + QRコード"
      },
      id: {
        cam_vida:"✅ Jalan Hidup", expr_alma_pers:"✅ Ekspresi, Jiwa, Kepribadian", destino:"✅ Takdir",
        fase_atual:"✅ Fase Kehidupan Saat Ini", ano_pessoal:"✅ Tahun Pribadi", tendencias:"✅ Tren Siklus",
        n5_detalhados:"✅ 5 angka terperinci", ciclos3:"✅ 3 Siklus Kehidupan", desafios_real:"✅ Tantangan dan Pencapaian",
        grade_inclusao:"✅ Grid Inklusi", sug_ia:"✅ Saran dengan AI", analise_energ_nomes:"✅ Analisis energi nama",
        comparativo:"✅ Perbandingan opsi", n5_nomes_test:"✅ 5 nama diuji", sug_energia8:"✅ Saran dengan energi 8",
        calc_letra:"✅ Perhitungan huruf demi huruf", n5_sugeridos:"✅ 5 angka yang disarankan", prior_energia8:"✅ Prioritas energi 8 (Kekuatan)",
        calc_completo:"✅ Perhitungan lengkap", imovel_anal:"✅ Nomor properti dianalisis", energia_ambiente:"✅ Energi lingkungan",
        sug_harmon:"✅ Saran harmonisasi", vibracao_diaria:"✅ Getaran harian", dias_favoraveis:"✅ Hari-hari baik",
        orient_mensal:"✅ Panduan bulanan", nomes_testados:"✅ Nama diuji", sug_palco:"✅ Saran panggung",
        energia_nome:"✅ Energi nama", sug_nomes:"✅ Saran nama", analise_energ:"✅ Analisis energi",
        comp_sobrenome:"✅ Kecocokan dengan nama keluarga", assin_atual:"✅ Tanda tangan saat ini dianalisis", variacoes:"✅ Variasi yang disarankan",
        energia_assin:"✅ Energi tanda tangan", sug_empresariais:"✅ Saran bisnis", compatibilidade:"✅ Kecocokan",
        pontos_fortes:"✅ Kekuatan pasangan", desafios_relacao:"✅ Tantangan hubungan", todos_membros:"✅ Semua anggota",
        sinergia:"✅ Sinergi keluarga", orient_membro:"✅ Panduan per anggota", planos_prontos:"✅ Paket siap pakai",
        sob_medida:"✅ Sesuai permintaan", descontos_prog:"✅ Diskon bertingkat", codigos_presente:"✅ Kode hadiah",
        pet_anal:"✅ Nama hewan peliharaan dianalisis", sintonia_familia:"✅ Koneksi dengan keluarga", nick_anal:"✅ Nama panggilan dianalisis",
        imagem_online:"✅ Citra di dunia online", dominio_anal:"✅ Domain dianalisis", forca_marca:"✅ Kekuatan untuk merek",
        canal_anal:"✅ Kanal dianalisis", conexao_audiencia:"✅ Koneksi dengan audiens", equipe_anal:"✅ Tim dianalisis",
        uniao_membros:"✅ Persatuan antar anggota", ong_anal:"✅ LSM dianalisis", causa_potencial:"✅ Penyebab diperkuat",
        projeto_anal:"✅ Proyek dianalisis", impulso_sucesso:"✅ Dorongan menuju sukses", evento_anal:"✅ Acara dianalisis",
        atmosfera:"✅ Atmosfer untuk peserta", pdf:"📲 PDF + Kode QR"
      },
      tr: {
        cam_vida:"✅ Yaşam Yolu", expr_alma_pers:"✅ İfade, Ruh, Kişilik", destino:"✅ Kader",
        fase_atual:"✅ Mevcut Yaşam Evresi", ano_pessoal:"✅ Kişisel Yıl", tendencias:"✅ Döngü eğilimleri",
        n5_detalhados:"✅ 5 ayrıntılı sayı", ciclos3:"✅ 3 Yaşam Döngüsü", desafios_real:"✅ Zorluklar ve Başarılar",
        grade_inclusao:"✅ Dahil Etme Izgarası", sug_ia:"✅ Yapay zekâ ile öneriler", analise_energ_nomes:"✅ İsimlerin enerji analizi",
        comparativo:"✅ Seçenek karşılaştırması", n5_nomes_test:"✅ 5 isim test edildi", sug_energia8:"✅ 8 enerjisiyle öneriler",
        calc_letra:"✅ Harf harf hesaplama", n5_sugeridos:"✅ 5 önerilen sayı", prior_energia8:"✅ 8 enerjisi önceliği (Güç)",
        calc_completo:"✅ Eksiksiz hesaplama", imovel_anal:"✅ Mülk numarası analiz edildi", energia_ambiente:"✅ Ortam enerjisi",
        sug_harmon:"✅ Uyum önerileri", vibracao_diaria:"✅ Günlük titreşim", dias_favoraveis:"✅ Uğurlu günler",
        orient_mensal:"✅ Aylık yönlendirme", nomes_testados:"✅ İsimler test edildi", sug_palco:"✅ Sahne ismi önerileri",
        energia_nome:"✅ İsim enerjisi", sug_nomes:"✅ İsim önerileri", analise_energ:"✅ Enerji analizi",
        comp_sobrenome:"✅ Soyadı uyumu", assin_atual:"✅ Mevcut imza analiz edildi", variacoes:"✅ Önerilen varyasyonlar",
        energia_assin:"✅ İmzanın enerjisi", sug_empresariais:"✅ İş önerileri", compatibilidade:"✅ Uyum",
        pontos_fortes:"✅ Çiftin güçlü yönleri", desafios_relacao:"✅ İlişkinin zorlukları", todos_membros:"✅ Tüm üyeler",
        sinergia:"✅ Aile sinerjisi", orient_membro:"✅ Üye başına yönlendirme", planos_prontos:"✅ Hazır planlar",
        sob_medida:"✅ Özel yapım", descontos_prog:"✅ Kademeli indirimler", codigos_presente:"✅ Hediye kodları",
        pet_anal:"✅ Evcil hayvan adı analiz edildi", sintonia_familia:"✅ Aileyle bağ", nick_anal:"✅ Takma ad analiz edildi",
        imagem_online:"✅ Çevrimiçi imaj", dominio_anal:"✅ Alan adı analiz edildi", forca_marca:"✅ Marka gücü",
        canal_anal:"✅ Kanal analiz edildi", conexao_audiencia:"✅ İzleyiciyle bağ", equipe_anal:"✅ Ekip analiz edildi",
        uniao_membros:"✅ Üyeler arası birlik", ong_anal:"✅ STK analiz edildi", causa_potencial:"✅ Dava güçlendirildi",
        projeto_anal:"✅ Proje analiz edildi", impulso_sucesso:"✅ Başarı için itici güç", evento_anal:"✅ Etkinlik analiz edildi",
        atmosfera:"✅ Katılımcılar için atmosfer", pdf:"📲 PDF + QR Kod"
      },
      vi: {
        cam_vida:"✅ Đường Đời", expr_alma_pers:"✅ Biểu Đạt, Tâm Hồn, Tính Cách", destino:"✅ Định Mệnh",
        fase_atual:"✅ Giai Đoạn Cuộc Sống Hiện Tại", ano_pessoal:"✅ Năm Cá Nhân", tendencias:"✅ Xu Hướng Chu Kỳ",
        n5_detalhados:"✅ 5 con số chi tiết", ciclos3:"✅ 3 Chu Kỳ Cuộc Đời", desafios_real:"✅ Thử Thách và Thành Tựu",
        grade_inclusao:"✅ Lưới Bao Gồm", sug_ia:"✅ Gợi ý bằng AI", analise_energ_nomes:"✅ Phân tích năng lượng tên",
        comparativo:"✅ So sánh lựa chọn", n5_nomes_test:"✅ 5 tên đã thử", sug_energia8:"✅ Gợi ý với năng lượng 8",
        calc_letra:"✅ Tính từng chữ cái", n5_sugeridos:"✅ 5 con số gợi ý", prior_energia8:"✅ Ưu tiên năng lượng 8 (Quyền Lực)",
        calc_completo:"✅ Tính toán đầy đủ", imovel_anal:"✅ Số bất động sản được phân tích", energia_ambiente:"✅ Năng lượng môi trường",
        sug_harmon:"✅ Gợi ý hài hòa", vibracao_diaria:"✅ Rung động hàng ngày", dias_favoraveis:"✅ Ngày thuận lợi",
        orient_mensal:"✅ Hướng dẫn hàng tháng", nomes_testados:"✅ Tên đã thử", sug_palco:"✅ Gợi ý nghệ danh",
        energia_nome:"✅ Năng lượng tên", sug_nomes:"✅ Gợi ý tên", analise_energ:"✅ Phân tích năng lượng",
        comp_sobrenome:"✅ Tương hợp với họ", assin_atual:"✅ Chữ ký hiện tại được phân tích", variacoes:"✅ Các biến thể gợi ý",
        energia_assin:"✅ Năng lượng chữ ký", sug_empresariais:"✅ Gợi ý kinh doanh", compatibilidade:"✅ Sự tương hợp",
        pontos_fortes:"✅ Điểm mạnh của cặp đôi", desafios_relacao:"✅ Thử thách của mối quan hệ", todos_membros:"✅ Tất cả thành viên",
        sinergia:"✅ Sự cộng hưởng gia đình", orient_membro:"✅ Hướng dẫn theo thành viên", planos_prontos:"✅ Gói có sẵn",
        sob_medida:"✅ Theo yêu cầu", descontos_prog:"✅ Giảm giá theo bậc", codigos_presente:"✅ Mã quà tặng",
        pet_anal:"✅ Tên thú cưng được phân tích", sintonia_familia:"✅ Kết nối với gia đình", nick_anal:"✅ Biệt danh được phân tích",
        imagem_online:"✅ Hình ảnh trên thế giới trực tuyến", dominio_anal:"✅ Tên miền được phân tích", forca_marca:"✅ Sức mạnh cho thương hiệu",
        canal_anal:"✅ Kênh được phân tích", conexao_audiencia:"✅ Kết nối với khán giả", equipe_anal:"✅ Đội nhóm được phân tích",
        uniao_membros:"✅ Đoàn kết giữa các thành viên", ong_anal:"✅ Tổ chức được phân tích", causa_potencial:"✅ Sứ mệnh được khuếch đại",
        projeto_anal:"✅ Dự án được phân tích", impulso_sucesso:"✅ Động lực cho thành công", evento_anal:"✅ Sự kiện được phân tích",
        atmosfera:"✅ Không khí cho người tham dự", pdf:"📲 PDF + Mã QR"
      },
      he: {
        cam_vida:"✅ מסלול חיים", expr_alma_pers:"✅ ביטוי, נשמה, אישיות", destino:"✅ גורל",
        fase_atual:"✅ שלב חיים נוכחי", ano_pessoal:"✅ שנה אישית", tendencias:"✅ מגמות המחזור",
        n5_detalhados:"✅ 5 מספרים מפורטים", ciclos3:"✅ 3 מחזורי חיים", desafios_real:"✅ אתגרים והישגים",
        grade_inclusao:"✅ רשת הכללה", sug_ia:"✅ הצעות עם AI", analise_energ_nomes:"✅ ניתוח אנרגטי של שמות",
        comparativo:"✅ השוואת אפשרויות", n5_nomes_test:"✅ 5 שמות שנבדקו", sug_energia8:"✅ הצעות עם אנרגיה 8",
        calc_letra:"✅ חישוב אות אחר אות", n5_sugeridos:"✅ 5 מספרים מוצעים", prior_energia8:"✅ עדיפות אנרגיה 8 (כוח)",
        calc_completo:"✅ חישוב מלא", imovel_anal:"✅ מספר הנכס נותח", energia_ambiente:"✅ אנרגיית הסביבה",
        sug_harmon:"✅ הצעות להרמוניה", vibracao_diaria:"✅ רטט יומי", dias_favoraveis:"✅ ימים מועדפים",
        orient_mensal:"✅ הדרכה חודשית", nomes_testados:"✅ שמות שנבדקו", sug_palco:"✅ הצעות לבמה",
        energia_nome:"✅ אנרגיית השם", sug_nomes:"✅ הצעות לשמות", analise_energ:"✅ ניתוח אנרגטי",
        comp_sobrenome:"✅ התאמה לשם משפחה", assin_atual:"✅ החתימה הנוכחית נותחה", variacoes:"✅ וריאציות מוצעות",
        energia_assin:"✅ אנרגיית החתימה", sug_empresariais:"✅ הצעות עסקיות", compatibilidade:"✅ תאימות",
        pontos_fortes:"✅ נקודות החוזק של הזוג", desafios_relacao:"✅ אתגרי הקשר", todos_membros:"✅ כל החברים",
        sinergia:"✅ סינרגיה משפחתית", orient_membro:"✅ הדרכה לכל חבר", planos_prontos:"✅ תוכניות מוכנות",
        sob_medida:"✅ בהתאמה אישית", descontos_prog:"✅ הנחות מדורגות", codigos_presente:"✅ קודי מתנה",
        pet_anal:"✅ שם חיית המחמד נותח", sintonia_familia:"✅ קשר עם המשפחה", nick_anal:"✅ הכינוי נותח",
        imagem_online:"✅ התדמית בעולם המקוון", dominio_anal:"✅ הדומיין נותח", forca_marca:"✅ כוח למותג",
        canal_anal:"✅ הערוץ נותח", conexao_audiencia:"✅ קשר עם הקהל", equipe_anal:"✅ הצוות נותח",
        uniao_membros:"✅ אחדות בין החברים", ong_anal:"✅ הארגון נותח", causa_potencial:"✅ המטרה מוגברת",
        projeto_anal:"✅ הפרויקט נותח", impulso_sucesso:"✅ דחיפה להצלחה", evento_anal:"✅ האירוע נותח",
        atmosfera:"✅ אווירה למשתתפים", pdf:"📲 PDF + קוד QR"
      },
      ar: {
        cam_vida:"✅ مسار الحياة", expr_alma_pers:"✅ التعبير والروح والشخصية", destino:"✅ القدر",
        fase_atual:"✅ مرحلة الحياة الحالية", ano_pessoal:"✅ السنة الشخصية", tendencias:"✅ اتجاهات الدورة",
        n5_detalhados:"✅ 5 أرقام مفصلة", ciclos3:"✅ 3 دورات حياة", desafios_real:"✅ التحديات والإنجازات",
        grade_inclusao:"✅ شبكة الإدماج", sug_ia:"✅ اقتراحات بالذكاء الاصطناعي", analise_energ_nomes:"✅ تحليل طاقة الأسماء",
        comparativo:"✅ مقارنة الخيارات", n5_nomes_test:"✅ 5 أسماء مختبرة", sug_energia8:"✅ اقتراحات بطاقة 8",
        calc_letra:"✅ حساب حرف بحرف", n5_sugeridos:"✅ 5 أرقام مقترحة", prior_energia8:"✅ أولوية الطاقة 8 (القوة)",
        calc_completo:"✅ حساب كامل", imovel_anal:"✅ تم تحليل رقم العقار", energia_ambiente:"✅ طاقة البيئة",
        sug_harmon:"✅ اقتراحات الانسجام", vibracao_diaria:"✅ الاهتزاز اليومي", dias_favoraveis:"✅ الأيام المواتية",
        orient_mensal:"✅ توجيه شهري", nomes_testados:"✅ أسماء مختبرة", sug_palco:"✅ اقتراحات للمسرح",
        energia_nome:"✅ طاقة الاسم", sug_nomes:"✅ اقتراحات أسماء", analise_energ:"✅ تحليل الطاقة",
        comp_sobrenome:"✅ التوافق مع اسم العائلة", assin_atual:"✅ تم تحليل التوقيع الحالي", variacoes:"✅ صيغ مقترحة",
        energia_assin:"✅ طاقة التوقيع", sug_empresariais:"✅ اقتراحات تجارية", compatibilidade:"✅ التوافق",
        pontos_fortes:"✅ نقاط قوة الثنائي", desafios_relacao:"✅ تحديات العلاقة", todos_membros:"✅ جميع الأعضاء",
        sinergia:"✅ التآزر العائلي", orient_membro:"✅ توجيه لكل عضو", planos_prontos:"✅ خطط جاهزة",
        sob_medida:"✅ حسب الطلب", descontos_prog:"✅ خصومات تصاعدية", codigos_presente:"✅ أكواد هدايا",
        pet_anal:"✅ تم تحليل اسم الحيوان الأليف", sintonia_familia:"✅ الارتباط بالعائلة", nick_anal:"✅ تم تحليل اللقب",
        imagem_online:"✅ الصورة في العالم الرقمي", dominio_anal:"✅ تم تحليل النطاق", forca_marca:"✅ قوة للعلامة التجارية",
        canal_anal:"✅ تم تحليل القناة", conexao_audiencia:"✅ التواصل مع الجمهور", equipe_anal:"✅ تم تحليل الفريق",
        uniao_membros:"✅ الوحدة بين الأعضاء", ong_anal:"✅ تم تحليل المنظمة", causa_potencial:"✅ تعزيز القضية",
        projeto_anal:"✅ تم تحليل المشروع", impulso_sucesso:"✅ دفع نحو النجاح", evento_anal:"✅ تم تحليل الحدث",
        atmosfera:"✅ أجواء للمشاركين", pdf:"📲 PDF + رمز QR"
      }
    };
    var M = {
      express:["cam_vida","expr_alma_pers","destino","pdf"],
      vida:["fase_atual","ano_pessoal","tendencias","pdf"],
      completo:["n5_detalhados","ciclos3","desafios_real","grade_inclusao","pdf"],
      ia:["sug_ia","analise_energ_nomes","comparativo","pdf"],
      urna:["n5_nomes_test","sug_energia8","calc_letra","pdf"],
      eleitoral:["n5_sugeridos","prior_energia8","calc_completo","pdf"],
      imovel:["imovel_anal","energia_ambiente","sug_harmon","pdf"],
      calendario:["vibracao_diaria","dias_favoraveis","orient_mensal","pdf"],
      artistico:["nomes_testados","sug_palco","energia_nome","pdf"],
      bebe:["sug_nomes","analise_energ","comp_sobrenome","pdf"],
      assinatura:["assin_atual","variacoes","energia_assin","pdf"],
      negocio:["nomes_testados","sug_empresariais","energia_nome","pdf"],
      casal:["compatibilidade","pontos_fortes","desafios_relacao","pdf"],
      familia:["todos_membros","sinergia","orient_membro","pdf"],
      coletivo:["planos_prontos","sob_medida","descontos_prog","codigos_presente"],
      nome_pet:["pet_anal","energia_nome","sintonia_familia","pdf"],
      nickname:["nick_anal","energia_nome","imagem_online","pdf"],
      nome_dominio:["dominio_anal","energia_nome","forca_marca","pdf"],
      nome_canal:["canal_anal","energia_nome","conexao_audiencia","pdf"],
      nome_equipe:["equipe_anal","energia_nome","uniao_membros","pdf"],
      nome_ong:["ong_anal","energia_nome","causa_potencial","pdf"],
      nome_projeto:["projeto_anal","energia_nome","impulso_sucesso","pdf"],
      nome_evento:["evento_anal","energia_nome","atmosfera","pdf"]
    };
    Object.keys(F).forEach(function (lang) {
      var f = F[lang];
      window.FEAT_TRAD[lang] = {};
      Object.keys(M).forEach(function (prod) {
        window.FEAT_TRAD[lang][prod] = M[prod].map(function (k) { return f[k] || F.pt[k]; });
      });
    });
  })();
}

/* ===== CARDS_TRAD (8 produtos, 14 idiomas) ===== */
window.CARDS_TRAD = window.CARDS_TRAD || {
  pt:{ nome_pet:"Nome do Pet", nome_pet_desc:"A energia do nome do seu animal de estimação.", nickname:"Nickname Digital", nickname_desc:"A vibração do seu nickname nas redes.", nome_dominio:"Nome do Domínio", nome_dominio_desc:"A energia do nome do seu domínio.", nome_canal:"Nome do Canal", nome_canal_desc:"A energia do nome do seu canal.", nome_equipe:"Nome da Equipe", nome_equipe_desc:"A vibração do nome da sua equipe.", nome_ong:"Nome de ONG", nome_ong_desc:"A energia do nome da sua organização.", nome_projeto:"Nome do Projeto", nome_projeto_desc:"A energia do nome do seu projeto.", nome_evento:"Nome do Evento", nome_evento_desc:"A vibração do nome do seu evento.", buscar:"Buscar" },
  en:{ nome_pet:"Pet Name", nome_pet_desc:"The energy of your pet's name.", nickname:"Digital Nickname", nickname_desc:"The vibration of your nickname online.", nome_dominio:"Domain Name", nome_dominio_desc:"The energy of your domain name.", nome_canal:"Channel Name", nome_canal_desc:"The energy of your channel name.", nome_equipe:"Team Name", nome_equipe_desc:"The vibration of your team's name.", nome_ong:"NGO Name", nome_ong_desc:"The energy of your organization's name.", nome_projeto:"Project Name", nome_projeto_desc:"The energy of your project name.", nome_evento:"Event Name", nome_evento_desc:"The vibration of your event's name.", buscar:"Search" },
  es:{ nome_pet:"Nombre de la Mascota", nome_pet_desc:"La energía del nombre de tu mascota.", nickname:"Apodo Digital", nickname_desc:"La vibración de tu apodo en redes.", nome_dominio:"Nombre del Dominio", nome_dominio_desc:"La energía del nombre de tu dominio.", nome_canal:"Nombre del Canal", nome_canal_desc:"La energía del nombre de tu canal.", nome_equipe:"Nombre del Equipo", nome_equipe_desc:"La vibración del nombre de tu equipo.", nome_ong:"Nombre de la ONG", nome_ong_desc:"La energía del nombre de tu organización.", nome_projeto:"Nombre del Proyecto", nome_projeto_desc:"La energía del nombre de tu proyecto.", nome_evento:"Nombre del Evento", nome_evento_desc:"La vibración del nombre de tu evento.", buscar:"Buscar" },
  fr:{ nome_pet:"Nom de l'animal", nome_pet_desc:"L'énergie du nom de votre animal.", nickname:"Surnom numérique", nickname_desc:"La vibration de votre surnom en ligne.", nome_dominio:"Nom de domaine", nome_dominio_desc:"L'énergie du nom de votre domaine.", nome_canal:"Nom de la chaîne", nome_canal_desc:"L'énergie du nom de votre chaîne.", nome_equipe:"Nom de l'équipe", nome_equipe_desc:"La vibration du nom de votre équipe.", nome_ong:"Nom de l'ONG", nome_ong_desc:"L'énergie du nom de votre organisation.", nome_projeto:"Nom du projet", nome_projeto_desc:"L'énergie du nom de votre projet.", nome_evento:"Nom de l'événement", nome_evento_desc:"La vibration du nom de votre événement.", buscar:"Rechercher" },
  it:{ nome_pet:"Nome dell'animale", nome_pet_desc:"L'energia del nome del tuo animale.", nickname:"Soprannome digitale", nickname_desc:"La vibrazione del tuo soprannome online.", nome_dominio:"Nome del dominio", nome_dominio_desc:"L'energia del nome del tuo dominio.", nome_canal:"Nome del canale", nome_canal_desc:"L'energia del nome del tuo canale.", nome_equipe:"Nome del team", nome_equipe_desc:"La vibrazione del nome del tuo team.", nome_ong:"Nome dell'ONG", nome_ong_desc:"L'energia del nome della tua organizzazione.", nome_projeto:"Nome del progetto", nome_projeto_desc:"L'energia del nome del tuo progetto.", nome_evento:"Nome dell'evento", nome_evento_desc:"La vibrazione del nome del tuo evento.", buscar:"Cerca" },
  de:{ nome_pet:"Haustiername", nome_pet_desc:"Die Energie des Namens Ihres Haustiers.", nickname:"Digitaler Spitzname", nickname_desc:"Die Schwingung Ihres Spitznamens online.", nome_dominio:"Domainname", nome_dominio_desc:"Die Energie Ihres Domainnamens.", nome_canal:"Kanalname", nome_canal_desc:"Die Energie Ihres Kanalnamens.", nome_equipe:"Teamname", nome_equipe_desc:"Die Schwingung des Namens Ihres Teams.", nome_ong:"NGO-Name", nome_ong_desc:"Die Energie des Namens Ihrer Organisation.", nome_projeto:"Projektname", nome_projeto_desc:"Die Energie Ihres Projektnamens.", nome_evento:"Veranstaltungsname", nome_evento_desc:"Die Schwingung des Namens Ihrer Veranstaltung.", buscar:"Suchen" },
  ru:{ nome_pet:"Имя питомца", nome_pet_desc:"Энергия имени вашего питомца.", nickname:"Цифровой никнейм", nickname_desc:"Вибрация вашего никнейма в сети.", nome_dominio:"Доменное имя", nome_dominio_desc:"Энергия вашего доменного имени.", nome_canal:"Название канала", nome_canal_desc:"Энергия названия вашего канала.", nome_equipe:"Название команды", nome_equipe_desc:"Вибрация названия вашей команды.", nome_ong:"Название НПО", nome_ong_desc:"Энергия названия вашей организации.", nome_projeto:"Название проекта", nome_projeto_desc:"Энергия названия вашего проекта.", nome_evento:"Название события", nome_evento_desc:"Вибрация названия вашего события.", buscar:"Поиск" },
  zh:{ nome_pet:"宠物名称", nome_pet_desc:"您的宠物名字的能量。", nickname:"数字昵称", nickname_desc:"您的网络昵称的振动。", nome_dominio:"域名", nome_dominio_desc:"您的域名的能量。", nome_canal:"频道名称", nome_canal_desc:"您的频道名称的能量。", nome_equipe:"团队名称", nome_equipe_desc:"您的团队名称的振动。", nome_ong:"非政府组织名称", nome_ong_desc:"您的组织名称的能量。", nome_projeto:"项目名称", nome_projeto_desc:"您的项目名称的能量。", nome_evento:"活动名称", nome_evento_desc:"您的活动名称的振动。", buscar:"搜索" },
  ja:{ nome_pet:"ペット名", nome_pet_desc:"ペットの名前のエネルギー。", nickname:"デジタルニックネーム", nickname_desc:"オンラインのニックネームの振動。", nome_dominio:"ドメイン名", nome_dominio_desc:"ドメイン名のエネルギー。", nome_canal:"チャンネル名", nome_canal_desc:"チャンネル名のエネルギー。", nome_equipe:"チーム名", nome_equipe_desc:"チーム名の振動。", nome_ong:"NGO名", nome_ong_desc:"組織名のエネルギー。", nome_projeto:"プロジェクト名", nome_projeto_desc:"プロジェクト名のエネルギー。", nome_evento:"イベント名", nome_evento_desc:"イベント名の振動。", buscar:"検索" },
  ar:{ nome_pet:"اسم الحيوان الأليف", nome_pet_desc:"طاقة اسم حيوانك الأليف.", nickname:"الاسم المستعار الرقمي", nickname_desc:"اهتزاز اسمك المستعار على الإنترنت.", nome_dominio:"اسم النطاق", nome_dominio_desc:"طاقة اسم النطاق الخاص بك.", nome_canal:"اسم القناة", nome_canal_desc:"طاقة اسم قناتك.", nome_equipe:"اسم الفريق", nome_equipe_desc:"اهتزاز اسم فريقك.", nome_ong:"اسم المنظمة", nome_ong_desc:"طاقة اسم مؤسستك.", nome_projeto:"اسم المشروع", nome_projeto_desc:"طاقة اسم مشروعك.", nome_evento:"اسم الفعالية", nome_evento_desc:"اهتزاز اسم فعاليتك.", buscar:"بحث" },
  he:{ nome_pet:"שם חיית המחמד", nome_pet_desc:"האנרגיה של שם חיית המחמד שלך.", nickname:"כינוי דיגיטלי", nickname_desc:"הרטט של הכינוי שלך ברשת.", nome_dominio:"שם הדומיין", nome_dominio_desc:"האנרגיה של שם הדומיין שלך.", nome_canal:"שם הערוץ", nome_canal_desc:"האנרגיה של שם הערוץ שלך.", nome_equipe:"שם הצוות", nome_equipe_desc:"הרטט של שם הצוות שלך.", nome_ong:"שם הארגון", nome_ong_desc:"האנרגיה של שם הארגון שלך.", nome_projeto:"שם הפרויקט", nome_projeto_desc:"האנרגיה של שם הפרויקט שלך.", nome_evento:"שם האירוע", nome_evento_desc:"הרטט של שם האירוע שלך.", buscar:"חיפוש" },
  id:{ nome_pet:"Nama Hewan Peliharaan", nome_pet_desc:"Energi dari nama hewan peliharaan Anda.", nickname:"Nama Panggilan Digital", nickname_desc:"Getaran nama panggilan Anda di media sosial.", nome_dominio:"Nama Domain", nome_dominio_desc:"Energi dari nama domain Anda.", nome_canal:"Nama Kanal", nome_canal_desc:"Energi dari nama kanal Anda.", nome_equipe:"Nama Tim", nome_equipe_desc:"Getaran dari nama tim Anda.", nome_ong:"Nama LSM", nome_ong_desc:"Energi dari nama organisasi Anda.", nome_projeto:"Nama Proyek", nome_projeto_desc:"Energi dari nama proyek Anda.", nome_evento:"Nama Acara", nome_evento_desc:"Getaran dari nama acara Anda.", buscar:"Cari" },
  tr:{ nome_pet:"Evcil Hayvan Adı", nome_pet_desc:"Evcil hayvanınızın adının enerjisi.", nickname:"Dijital Takma Ad", nickname_desc:"Çevrimiçi takma adınızın titreşimi.", nome_dominio:"Alan Adı", nome_dominio_desc:"Alan adınızın enerjisi.", nome_canal:"Kanal Adı", nome_canal_desc:"Kanal adınızın enerjisi.", nome_equipe:"Ekip Adı", nome_equipe_desc:"Ekip adınızın titreşimi.", nome_ong:"STK Adı", nome_ong_desc:"Kuruluşunuzun adının enerjisi.", nome_projeto:"Proje Adı", nome_projeto_desc:"Projenizin adının enerjisi.", nome_evento:"Etkinlik Adı", nome_evento_desc:"Etkinliğinizin adının titreşimi.", buscar:"Ara" },
  vi:{ nome_pet:"Tên Thú Cưng", nome_pet_desc:"Năng lượng của tên thú cưng của bạn.", nickname:"Biệt Danh Kỹ Thuật Số", nickname_desc:"Rung động của biệt danh trực tuyến của bạn.", nome_dominio:"Tên Miền", nome_dominio_desc:"Năng lượng của tên miền của bạn.", nome_canal:"Tên Kênh", nome_canal_desc:"Năng lượng của tên kênh của bạn.", nome_equipe:"Tên Đội Nhóm", nome_equipe_desc:"Rung động của tên đội nhóm của bạn.", nome_ong:"Tên Tổ Chức", nome_ong_desc:"Năng lượng của tên tổ chức của bạn.", nome_projeto:"Tên Dự Án", nome_projeto_desc:"Năng lượng của tên dự án của bạn.", nome_evento:"Tên Sự Kiện", nome_evento_desc:"Rung động của tên sự kiện của bạn.", buscar:"Tìm Kiếm" }
};

/* ===== MONTAR_TRAD ===== */
window.MONTAR_TRAD = window.MONTAR_TRAD || {
  pt:{ titulo:"Montar Sob Medida", subtitulo:"Escolha os produtos e a energia desejada.", produto:"Produto", energia:"Energia", quantidade:"Quantidade", preco:"Preço", adicionar:"Adicionar", remover:"Remover", finalizar:"Finalizar", bruto:"Valor Bruto", desconto:"Desconto Aplicado", total:"Total", vazio:"Seu carrinho está vazio" },
  en:{ titulo:"Build Custom", subtitulo:"Choose the products and desired energy.", produto:"Product", energia:"Energy", quantidade:"Quantity", preco:"Price", adicionar:"Add", remover:"Remove", finalizar:"Checkout", bruto:"Gross Amount", desconto:"Applied Discount", total:"Total", vazio:"Your cart is empty" },
  es:{ titulo:"Montar a Medida", subtitulo:"Elige los productos y la energía deseada.", produto:"Producto", energia:"Energía", quantidade:"Cantidad", preco:"Precio", adicionar:"Añadir", remover:"Eliminar", finalizar:"Finalizar", bruto:"Importe Bruto", desconto:"Descuento Aplicado", total:"Total", vazio:"Tu carrito está vacío" },
  fr:{ titulo:"Composer sur Mesure", subtitulo:"Choisissez les produits et l'énergie souhaitée.", produto:"Produit", energia:"Énergie", quantidade:"Quantité", preco:"Prix", adicionar:"Ajouter", remover:"Retirer", finalizar:"Finaliser", bruto:"Montant Brut", desconto:"Remise Appliquée", total:"Total", vazio:"Votre panier est vide" },
  it:{ titulo:"Componi su Misura", subtitulo:"Scegli i prodotti e l'energia desiderata.", produto:"Prodotto", energia:"Energia", quantidade:"Quantità", preco:"Prezzo", adicionar:"Aggiungi", remover:"Rimuovi", finalizar:"Finalizza", bruto:"Importo Lordo", desconto:"Sconto Applicato", total:"Totale", vazio:"Il tuo carrello è vuoto" },
  de:{ titulo:"Individuell Zusammenstellen", subtitulo:"Wählen Sie die Produkte und die gewünschte Energie.", produto:"Produkt", energia:"Energie", quantidade:"Menge", preco:"Preis", adicionar:"Hinzufügen", remover:"Entfernen", finalizar:"Abschließen", bruto:"Bruttobetrag", desconto:"Angewendeter Rabatt", total:"Gesamt", vazio:"Ihr Warenkorb ist leer" },
  ru:{ titulo:"Собрать на Заказ", subtitulo:"Выберите продукты и желаемую энергию.", produto:"Продукт", energia:"Энергия", quantidade:"Количество", preco:"Цена", adicionar:"Добавить", remover:"Удалить", finalizar:"Оформить", bruto:"Валовая сумма", desconto:"Примененная скидка", total:"Итого", vazio:"Ваша корзина пуста" },
  zh:{ titulo:"定制组合", subtitulo:"选择产品和所需能量。", produto:"产品", energia:"能量", quantidade:"数量", preco:"价格", adicionar:"添加", remover:"移除", finalizar:"结算", bruto:"总额", desconto:"已应用折扣", total:"总计", vazio:"您的购物车是空的" },
  ja:{ titulo:"カスタム作成", subtitulo:"製品と希望のエネルギーを選択してください。", produto:"製品", energia:"エネルギー", quantidade:"数量", preco:"価格", adicionar:"追加", remover:"削除", finalizar:"確定", bruto:"総額", desconto:"適用割引", total:"合計", vazio:"カートは空です" },
  ar:{ titulo:"تخصيص حسب الطلب", subtitulo:"اختر المنتجات والطاقة المطلوبة.", produto:"المنتج", energia:"الطاقة", quantidade:"الكمية", preco:"السعر", adicionar:"إضافة", remover:"إزالة", finalizar:"إتمام", bruto:"المبلغ الإجمالي", desconto:"الخصم المطبق", total:"الإجمالي", vazio:"سلة التسوق فارغة" },
  he:{ titulo:"הרכבה אישית", subtitulo:"בחרו את המוצרים ואת האנרגיה הרצויה.", produto:"מוצר", energia:"אנרגיה", quantidade:"כמות", preco:"מחיר", adicionar:"הוסף", remover:"הסר", finalizar:"סיים", bruto:"סכום ברוטו", desconto:"הנחה מיושמת", total:"סה״כ", vazio:"העגלה שלך ריקה" },
  id:{ titulo:"Rakit Sesuai Keinginan", subtitulo:"Pilih produk dan energi yang diinginkan.", produto:"Produk", energia:"Energi", quantidade:"Jumlah", preco:"Harga", adicionar:"Tambah", remover:"Hapus", finalizar:"Selesaikan", bruto:"Nilai Kotor", desconto:"Diskon Diterapkan", total:"Total", vazio:"Keranjang Anda kosong" },
  tr:{ titulo:"Özel Oluştur", subtitulo:"İstediğiniz ürünleri ve enerjiyi seçin.", produto:"Ürün", energia:"Enerji", quantidade:"Miktar", preco:"Fiyat", adicionar:"Ekle", remover:"Kaldır", finalizar:"Tamamla", bruto:"Brüt Değer", desconto:"Uygulanan İndirim", total:"Toplam", vazio:"Sepetiniz boş" },
  vi:{ titulo:"Tạo Theo Yêu Cầu", subtitulo:"Chọn sản phẩm và năng lượng mong muốn.", produto:"Sản Phẩm", energia:"Năng Lượng", quantidade:"Số Lượng", preco:"Giá", adicionar:"Thêm", remover:"Xóa", finalizar:"Hoàn Tất", bruto:"Tổng Thô", desconto:"Giảm Giá Áp Dụng", total:"Tổng", vazio:"Giỏ hàng của bạn trống" }
};

/* ===== ENERGIA_TRAD (9 energias, 14 idiomas) ===== */
window.ENERGIA_TRAD = window.ENERGIA_TRAD || {
  pt:{ e1:"Líder", e2:"Diplomata", e3:"Criatividade", e4:"Estrutura", e5:"Liberdade", e6:"Harmonia", e7:"Espiritualidade", e8:"Poder", e9:"Humanitarismo" },
  en:{ e1:"Leader", e2:"Diplomat", e3:"Creativity", e4:"Structure", e5:"Freedom", e6:"Harmony", e7:"Spirituality", e8:"Power", e9:"Humanitarianism" },
  es:{ e1:"Líder", e2:"Diplomático", e3:"Creatividad", e4:"Estructura", e5:"Libertad", e6:"Armonía", e7:"Espiritualidad", e8:"Poder", e9:"Humanitarismo" },
  fr:{ e1:"Leader", e2:"Diplomate", e3:"Créativité", e4:"Structure", e5:"Liberté", e6:"Harmonie", e7:"Spiritualité", e8:"Pouvoir", e9:"Humanitarisme" },
  it:{ e1:"Leader", e2:"Diplomatico", e3:"Creatività", e4:"Struttura", e5:"Libertà", e6:"Armonia", e7:"Spiritualità", e8:"Potere", e9:"Umanitarismo" },
  de:{ e1:"Führer", e2:"Diplomat", e3:"Kreativität", e4:"Struktur", e5:"Freiheit", e6:"Harmonie", e7:"Spiritualität", e8:"Macht", e9:"Humanitarismus" },
  ru:{ e1:"Лидер", e2:"Дипломат", e3:"Творчество", e4:"Структура", e5:"Свобода", e6:"Гармония", e7:"Духовность", e8:"Власть", e9:"Гуманизм" },
  zh:{ e1:"领导者", e2:"外交官", e3:"创造力", e4:"结构", e5:"自由", e6:"和谐", e7:"灵性", e8:"权力", e9:"人道主义" },
  ja:{ e1:"リーダー", e2:"外交官", e3:"創造性", e4:"構造", e5:"自由", e6:"調和", e7:"精神性", e8:"力", e9:"人道主義" },
  ar:{ e1:"قائد", e2:"دبلوماسي", e3:"إبداع", e4:"بنية", e5:"حرية", e6:"انسجام", e7:"روحانية", e8:"قوة", e9:"إنسانية" },
  he:{ e1:"מנהיג", e2:"דיפלומט", e3:"יצירתיות", e4:"מבנה", e5:"חופש", e6:"הרמוניה", e7:"רוחניות", e8:"כוח", e9:"הומניטריות" },
  id:{ e1:"Pemimpin", e2:"Diplomat", e3:"Kreativitas", e4:"Struktur", e5:"Kebebasan", e6:"Harmoni", e7:"Spiritualitas", e8:"Kekuatan", e9:"Kemanusiaan" },
  tr:{ e1:"Lider", e2:"Diplomat", e3:"Yaratıcılık", e4:"Yapı", e5:"Özgürlük", e6:"Uyum", e7:"Maneviyat", e8:"Güç", e9:"İnsaniyet" },
  vi:{ e1:"Lãnh đạo", e2:"Nhà ngoại giao", e3:"Sáng tạo", e4:"Cấu trúc", e5:"Tự do", e6:"Hòa hợp", e7:"Tâm linh", e8:"Sức mạnh", e9:"Nhân đạo" }
};
window.ENERGIA_TITULOS = window.ENERGIA_TITULOS || {};
if (!window.ENERGIA_TITULOS.pt) {
  Object.keys(window.ENERGIA_TRAD).forEach(function(l){ window.ENERGIA_TITULOS[l] = window.ENERGIA_TRAD[l]; });
}
window.ENERGIAS_DESC = window.ENERGIAS_DESC || {};
window.ENERGIAS_BTN = window.ENERGIAS_BTN || { pt:"Pesquisar", en:"Search", es:"Buscar", fr:"Rechercher", it:"Cerca", de:"Suchen", ru:"Поиск", zh:"搜索", ja:"検索", ar:"بحث", he:"חיפוש", id:"Cari", tr:"Ara", vi:"Tìm Kiếm" };

/* ===== DADO_LABEL ===== */
window.DADO_LABEL = window.DADO_LABEL || {
  pt:{nome_pet:"Nome do Pet",nickname:"Nickname Digital",nome_dominio:"Nome do Domínio",nome_canal:"Nome do Canal",nome_equipe:"Nome da Equipe",nome_ong:"Nome da ONG",nome_projeto:"Nome do Projeto",nome_evento:"Nome do Evento"},
  en:{nome_pet:"Pet Name",nickname:"Digital Nickname",nome_dominio:"Domain Name",nome_canal:"Channel Name",nome_equipe:"Team Name",nome_ong:"NGO Name",nome_projeto:"Project Name",nome_evento:"Event Name"},
  es:{nome_pet:"Nombre de Mascota",nickname:"Nickname Digital",nome_dominio:"Nombre de Dominio",nome_canal:"Nombre de Canal",nome_equipe:"Nombre del Equipo",nome_ong:"Nombre de la ONG",nome_projeto:"Nombre del Proyecto",nome_evento:"Nombre del Evento"},
  it:{nome_pet:"Nome dell'Animale",nickname:"Nickname Digitale",nome_dominio:"Nome del Dominio",nome_canal:"Nome del Canale",nome_equipe:"Nome del Team",nome_ong:"Nome dell'ONG",nome_projeto:"Nome del Progetto",nome_evento:"Nome dell'Evento"},
  fr:{nome_pet:"Nom de l'Animal",nickname:"Pseudo Digital",nome_dominio:"Nom de Domaine",nome_canal:"Nom de Chaîne",nome_equipe:"Nom de l'Équipe",nome_ong:"Nom de l'ONG",nome_projeto:"Nom du Projet",nome_evento:"Nom de l'Événement"},
  de:{nome_pet:"Haustiername",nickname:"Digitaler Nickname",nome_dominio:"Domainname",nome_canal:"Kanalname",nome_equipe:"Teamname",nome_ong:"NGO-Name",nome_projeto:"Projektname",nome_evento:"Veranstaltungsname"},
  ja:{nome_pet:"ペットの名前",nickname:"デジタルニックネーム",nome_dominio:"ドメイン名",nome_canal:"チャンネル名",nome_equipe:"チーム名",nome_ong:"NGO名",nome_projeto:"プロジェクト名",nome_evento:"イベント名"},
  zh:{nome_pet:"宠物名字",nickname:"数字昵称",nome_dominio:"域名",nome_canal:"频道名称",nome_equipe:"团队名称",nome_ong:"NGO名称",nome_projeto:"项目名称",nome_evento:"活动名称"},
  ru:{nome_pet:"Имя питомца",nickname:"Цифровой никнейм",nome_dominio:"Имя домена",nome_canal:"Название канала",nome_equipe:"Название команды",nome_ong:"Название НКО",nome_projeto:"Название проекта",nome_evento:"Название события"},
  he:{nome_pet:"שם חיית המחמד",nickname:"כינוי דיגיטלי",nome_dominio:"שם דומיין",nome_canal:"שם הערוץ",nome_equipe:"שם הצוות",nome_ong:"שם העמותה",nome_projeto:"שם הפרויקט",nome_evento:"שם האירוע"},
  ar:{nome_pet:"اسم الحيوان الأليف",nickname:"اللقب الرقمي",nome_dominio:"اسم النطاق",nome_canal:"اسم القناة",nome_equipe:"اسم الفريق",nome_ong:"اسم المنظمة",nome_projeto:"اسم المشروع",nome_evento:"اسم الفعالية"},
  id:{nome_pet:"Nama Hewan Peliharaan",nickname:"Nama Panggilan Digital",nome_dominio:"Nama Domain",nome_canal:"Nama Kanal",nome_equipe:"Nama Tim",nome_ong:"Nama LSM",nome_projeto:"Nama Proyek",nome_evento:"Nama Acara"},
  tr:{nome_pet:"Evcil Hayvan Adı",nickname:"Dijital Takma Ad",nome_dominio:"Alan Adı",nome_canal:"Kanal Adı",nome_equipe:"Ekip Adı",nome_ong:"STK Adı",nome_projeto:"Proje Adı",nome_evento:"Etkinlik Adı"},
  vi:{nome_pet:"Tên Thú Cưng",nickname:"Biệt Danh Kỹ Thuật Số",nome_dominio:"Tên Miền",nome_canal:"Tên Kênh",nome_equipe:"Tên Đội Nhóm",nome_ong:"Tên Tổ Chức",nome_projeto:"Tên Dự Án",nome_evento:"Tên Sự Kiện"}
};

/* ===== DADO_TIPOS ===== */
window.DADO_TIPOS = window.DADO_TIPOS || {
  nome_pet: { label:"Tipo de Pet", opcoes:["Gato","Cão","Pássaro","Réptil","Outro"] },
  nickname: { label:"Tipo de Perfil", opcoes:["Gamer","Criador","Profissional","Artista","Outro"] },
  nome_dominio: { label:"Tipo de Site", opcoes:["Blog","Loja","Portfólio","Empresa","Outro"] },
  nome_canal: { label:"Tipo de Canal", opcoes:["YouTube","Podcast","Twitch","TikTok","Outro"] },
  nome_equipe: { label:"Tipo de Equipe", opcoes:["Esportiva","Empresarial","Projeto","Banda","Outro"] },
  nome_ong: { label:"Tipo de Instituição", opcoes:["ONG","Associação","Instituto","Fundação","Outro"] },
  nome_projeto: { label:"Tipo de Projeto", opcoes:["Pessoal","Empresarial","Social","Cultural","Outro"] },
  nome_evento: { label:"Tipo de Evento", opcoes:["Congresso","Curso","Festa","Palestra","Outro"] }
};

/* ===== OPCOES_FALLBACK ===== */
window.OPCOES_FALLBACK = window.OPCOES_FALLBACK || {
  loja:"Loja", empresa:"Empresa", blog:"Blog", portfolio:"Portfólio",
  comercio:"Comércio", industria:"Indústria", servicos:"Serviços", pessoal:"Pessoal/Individual",
  cao:"Cão", gato:"Gato", passaro:"Pássaro", reptil:"Réptil",
  show:"Show", congresso:"Congresso", festa:"Festa", curso:"Curso", palestra:"Palestra",
  musica:"Música", esporte:"Esporte", cultura:"Cultura", politica:"Política", beleza:"Beleza",
  social:"Social", cultural:"Cultural", esportiva:"Esportiva", banda:"Banda",
  youtube:"YouTube", podcast:"Podcast", tiktok:"TikTok", twitch:"Twitch", noticias:"Notícias",
  gamer:"Gamer", profissional:"Profissional", criador:"Criador", artista:"Artista",
  ong:"ONG", instituto:"Instituto", associacao:"Associação", fundacao:"Fundação"
};

/* ===== OPCOES_TRAD (14 idiomas) ===== */
window.OPCOES_TRAD = window.OPCOES_TRAD || {
  pt:{ youtube:"YouTube", podcast:"Podcast", tiktok:"TikTok", twitch:"Twitch", gamer:"Gamer", profissional:"Profissional", criador:"Criador", artista:"Artista", ong:"ONG", instituto:"Instituto", associacao:"Associação", fundacao:"Fundação", show:"Show", congresso:"Congresso", festa:"Festa", curso:"Curso", palestra:"Palestra", pessoal:"Pessoal", social:"Social", empresarial:"Empresarial", cultural:"Cultural", esportiva:"Esportiva", banda:"Banda", loja:"Loja", empresa:"Empresa", blog:"Blog", portfolio:"Portfólio", cao:"Cão", gato:"Gato", passaro:"Pássaro", reptil:"Réptil", projeto:"Projeto", esporte:"Esporte", noticias:"Notícias", politica:"Política", beleza:"Beleza", musica:"Música", cultura:"Cultura", comercio:"Comércio", industria:"Indústria", servicos:"Serviços", outro:"OUTRO/QUAL?" },
  en:{ youtube:"YouTube", podcast:"Podcast", tiktok:"TikTok", twitch:"Twitch", gamer:"Gamer", profissional:"Professional", criador:"Creator", artista:"Artist", ong:"NGO", instituto:"Institute", associacao:"Association", fundacao:"Foundation", show:"Show", congresso:"Congress", festa:"Party", curso:"Course", palestra:"Talk", pessoal:"Personal", social:"Social", empresarial:"Business", cultural:"Cultural", esportiva:"Sports", banda:"Band", loja:"Store", empresa:"Company", blog:"Blog", portfolio:"Portfolio", cao:"Dog", gato:"Cat", passaro:"Bird", reptil:"Reptile", projeto:"Project", esporte:"Sports", noticias:"News", politica:"Politics", beleza:"Beauty", musica:"Music", cultura:"Culture", comercio:"Commerce", industria:"Industry", servicos:"Services", outro:"OTHER/WHAT?" },
  es:{ youtube:"YouTube", podcast:"Podcast", tiktok:"TikTok", twitch:"Twitch", gamer:"Gamer", profissional:"Profesional", criador:"Creador", artista:"Artista", ong:"ONG", instituto:"Instituto", associacao:"Asociación", fundacao:"Fundación", show:"Show", congresso:"Congreso", festa:"Fiesta", curso:"Curso", palestra:"Charla", pessoal:"Personal", social:"Social", empresarial:"Empresarial", cultural:"Cultural", esportiva:"Deportiva", banda:"Banda", loja:"Tienda", empresa:"Empresa", blog:"Blog", portfolio:"Portafolio", cao:"Perro", gato:"Gato", passaro:"Pájaro", reptil:"Reptil", projeto:"Proyecto", esporte:"Deporte", noticias:"Noticias", politica:"Política", beleza:"Belleza", musica:"Música", cultura:"Cultura", comercio:"Comercio", industria:"Industria", servicos:"Servicios", outro:"OTRO/¿CUÁL?" },
  fr:{ youtube:"YouTube", podcast:"Podcast", tiktok:"TikTok", twitch:"Twitch", gamer:"Gamer", profissional:"Professionnel", criador:"Créateur", artista:"Artiste", ong:"ONG", instituto:"Institut", associacao:"Association", fundacao:"Fondation", show:"Show", congresso:"Congrès", festa:"Fête", curso:"Cours", palestra:"Conférence", pessoal:"Personnel", social:"Social", empresarial:"Commercial", cultural:"Culturel", esportiva:"Sportive", banda:"Groupe", loja:"Boutique", empresa:"Entreprise", blog:"Blog", portfolio:"Portfolio", cao:"Chien", gato:"Chat", passaro:"Oiseau", reptil:"Reptile", projeto:"Projet", esporte:"Sport", noticias:"Actualités", politica:"Politique", beleza:"Beauté", musica:"Musique", cultura:"Culture", comercio:"Commerce", industria:"Industrie", servicos:"Services", outro:"AUTRE/QUOI?" },
  it:{ youtube:"YouTube", podcast:"Podcast", tiktok:"TikTok", twitch:"Twitch", gamer:"Gamer", profissional:"Professionale", criador:"Creatore", artista:"Artista", ong:"ONG", instituto:"Istituto", associacao:"Associazione", fundacao:"Fondazione", show:"Show", congresso:"Congresso", festa:"Festa", curso:"Corso", palestra:"Conferenza", pessoal:"Personale", social:"Sociale", empresarial:"Aziendale", cultural:"Culturale", esportiva:"Sportiva", banda:"Band", loja:"Negozio", empresa:"Azienda", blog:"Blog", portfolio:"Portfolio", cao:"Cane", gato:"Gatto", passaro:"Uccello", reptil:"Rettile", projeto:"Progetto", esporte:"Sport", noticias:"Notizie", politica:"Politica", beleza:"Bellezza", musica:"Musica", cultura:"Cultura", comercio:"Commercio", industria:"Industria", servicos:"Servizi", outro:"ALTRO/COSA?" },
  de:{ youtube:"YouTube", podcast:"Podcast", tiktok:"TikTok", twitch:"Twitch", gamer:"Gamer", profissional:"Professionell", criador:"Ersteller", artista:"Künstler", ong:"NGO", instituto:"Institut", associacao:"Verein", fundacao:"Stiftung", show:"Show", congresso:"Kongress", festa:"Party", curso:"Kurs", palestra:"Vortrag", pessoal:"Persönlich", social:"Sozial", empresarial:"Geschäftlich", cultural:"Kulturell", esportiva:"Sportlich", banda:"Band", loja:"Geschäft", empresa:"Unternehmen", blog:"Blog", portfolio:"Portfolio", cao:"Hund", gato:"Katze", passaro:"Vogel", reptil:"Reptil", projeto:"Projekt", esporte:"Sport", noticias:"Nachrichten", politica:"Politik", beleza:"Schönheit", musica:"Musik", cultura:"Kultur", comercio:"Handel", industria:"Industrie", servicos:"Dienstleistungen", outro:"ANDERE/WAS?" },
  ru:{ youtube:"YouTube", podcast:"Подкаст", tiktok:"TikTok", twitch:"Twitch", gamer:"Геймер", profissional:"Профессиональный", criador:"Создатель", artista:"Артист", ong:"НПО", instituto:"Институт", associacao:"Ассоциация", fundacao:"Фонд", show:"Шоу", congresso:"Конгресс", festa:"Вечеринка", curso:"Курс", palestra:"Лекция", pessoal:"Личный", social:"Социальный", empresarial:"Деловой", cultural:"Культурный", esportiva:"Спортивная", banda:"Группа", loja:"Магазин", empresa:"Компания", blog:"Блог", portfolio:"Портфолио", cao:"Собака", gato:"Кошка", passaro:"Птица", reptil:"Рептилия", projeto:"Проект", esporte:"Спорт", noticias:"Новости", politica:"Политика", beleza:"Красота", musica:"Музыка", cultura:"Культура", comercio:"Торговля", industria:"Промышленность", servicos:"Услуги", outro:"ДРУГОЕ/КАКОЕ?" },
  zh:{ youtube:"YouTube", podcast:"播客", tiktok:"TikTok", twitch:"Twitch", gamer:"玩家", profissional:"专业", criador:"创作者", artista:"艺术家", ong:"非政府组织", instituto:"研究所", associacao:"协会", fundacao:"基金会", show:"演出", congresso:"大会", festa:"派对", curso:"课程", palestra:"讲座", pessoal:"个人", social:"社交", empresarial:"商业", cultural:"文化", esportiva:"体育", banda:"乐队", loja:"商店", empresa:"公司", blog:"博客", portfolio:"作品集", cao:"狗", gato:"猫", passaro:"鸟", reptil:"爬行动物", projeto:"项目", esporte:"体育", noticias:"新闻", politica:"政治", beleza:"美容", musica:"音乐", cultura:"文化", comercio:"商业", industria:"工业", servicos:"服务", outro:"其他/什么?" },
  ja:{ youtube:"YouTube", podcast:"ポッドキャスト", tiktok:"TikTok", twitch:"Twitch", gamer:"ゲーマー", profissional:"プロフェッショナル", criador:"クリエイター", artista:"アーティスト", ong:"NGO", instituto:"研究所", associacao:"協会", fundacao:"財団", show:"ショー", congresso:"会議", festa:"パーティー", curso:"コース", palestra:"講演", pessoal:"個人", social:"ソーシャル", empresarial:"ビジネス", cultural:"文化的", esportiva:"スポーツ", banda:"バンド", loja:"店", empresa:"会社", blog:"ブログ", portfolio:"ポートフォリオ", cao:"犬", gato:"猫", passaro:"鳥", reptil:"爬虫類", projeto:"プロジェクト", esporte:"スポーツ", noticias:"ニュース", politica:"政治", beleza:"美容", musica:"音楽", cultura:"文化", comercio:"商業", industria:"産業", servicos:"サービス", outro:"その他/何?" },
  ar:{ youtube:"يوتيوب", podcast:"بودكاست", tiktok:"تيك توك", twitch:"تويتش", gamer:"لاعب", profissional:"محترف", criador:"منشئ", artista:"فنان", ong:"منظمة", instituto:"معهد", associacao:"جمعية", fundacao:"مؤسسة", show:"عرض", congresso:"مؤتمر", festa:"حفلة", curso:"دورة", palestra:"محاضرة", pessoal:"شخصي", social:"اجتماعي", empresarial:"تجاري", cultural:"ثقافي", esportiva:"رياضية", banda:"فرقة", loja:"متجر", empresa:"شركة", blog:"مدونة", portfolio:"أعمال", cao:"كلب", gato:"قطة", passaro:"طائر", reptil:"زاحف", projeto:"مشروع", esporte:"رياضة", noticias:"أخبار", politica:"سياسة", beleza:"جمال", musica:"موسيقى", cultura:"ثقافة", comercio:"تجارة", industria:"صناعة", servicos:"خدمات", outro:"آخر/ماذا؟" },
  he:{ youtube:"יוטיוב", podcast:"פודקאסט", tiktok:"טיקטוק", twitch:"טוויץ'", gamer:"גיימר", profissional:"מקצועי", criador:"יוצר", artista:"אמן", ong:"ארגון", instituto:"מכון", associacao:"עמותה", fundacao:"קרן", show:"מופע", congresso:"קונגרס", festa:"מסיבה", curso:"קורס", palestra:"הרצאה", pessoal:"אישי", social:"חברתי", empresarial:"עסקי", cultural:"תרבותי", esportiva:"ספורטיבית", banda:"להקה", loja:"חנות", empresa:"חברה", blog:"בלוג", portfolio:"תיק עבודות", cao:"כלב", gato:"חתול", passaro:"ציפור", reptil:"זוחל", projeto:"פרויקט", esporte:"ספורט", noticias:"חדשות", politica:"פוליטיקה", beleza:"יופי", musica:"מוזיקה", cultura:"תרבות", comercio:"מסחר", industria:"תעשייה", servicos:"שירותים", outro:"אחר/מה?" },
  id:{ youtube:"YouTube", podcast:"Podcast", tiktok:"TikTok", twitch:"Twitch", gamer:"Gamer", profissional:"Profesional", criador:"Pencipta", artista:"Artis", ong:"LSM", instituto:"Lembaga", associacao:"Asosiasi", fundacao:"Yayasan", show:"Pertunjukan", congresso:"Kongres", festa:"Pesta", curso:"Kursus", palestra:"Ceramah", pessoal:"Pribadi", social:"Sosial", empresarial:"Bisnis", cultural:"Budaya", esportiva:"Olahraga", banda:"Band", loja:"Toko", empresa:"Perusahaan", blog:"Blog", portfolio:"Portofolio", cao:"Anjing", gato:"Kucing", passaro:"Burung", reptil:"Reptil", projeto:"Proyek", esporte:"Olahraga", noticias:"Berita", politica:"Politik", beleza:"Kecantikan", musica:"Musik", cultura:"Budaya", comercio:"Perdagangan", industria:"Industri", servicos:"Layanan", outro:"LAINNYA/APA?" },
  tr:{ youtube:"YouTube", podcast:"Podcast", tiktok:"TikTok", twitch:"Twitch", gamer:"Oyuncu", profissional:"Profesyonel", criador:"İçerik Üreticisi", artista:"Sanatçı", ong:"STK", instituto:"Enstitü", associacao:"Dernek", fundacao:"Vakıf", show:"Gösteri", congresso:"Kongre", festa:"Parti", curso:"Kurs", palestra:"Konferans", pessoal:"Kişisel", social:"Sosyal", empresarial:"İş", cultural:"Kültürel", esportiva:"Spor", banda:"Müzik Grubu", loja:"Mağaza", empresa:"Şirket", blog:"Blog", portfolio:"Portfolyo", cao:"Köpek", gato:"Kedi", passaro:"Kuş", reptil:"Sürüngen", projeto:"Proje", esporte:"Spor", noticias:"Haberler", politica:"Siyaset", beleza:"Güzellik", musica:"Müzik", cultura:"Kültür", comercio:"Ticaret", industria:"Endüstri", servicos:"Hizmetler", outro:"DİĞER/NE?" },
  vi:{ youtube:"YouTube", podcast:"Podcast", tiktok:"TikTok", twitch:"Twitch", gamer:"Game thủ", profissional:"Chuyên nghiệp", criador:"Người sáng tạo", artista:"Nghệ sĩ", ong:"Tổ chức phi chính phủ", instituto:"Viện", associacao:"Hiệp hội", fundacao:"Quỹ", show:"Buổi diễn", congresso:"Đại hội", festa:"Tiệc", curso:"Khóa học", palestra:"Bài giảng", pessoal:"Cá nhân", social:"Xã hội", empresarial:"Kinh doanh", cultural:"Văn hóa", esportiva:"Thể thao", banda:"Ban nhạc", loja:"Cửa hàng", empresa:"Công ty", blog:"Blog", portfolio:"Hồ sơ năng lực", cao:"Chó", gato:"Mèo", passaro:"Chim", reptil:"Bò sát", projeto:"Dự án", esporte:"Thể thao", noticias:"Tin tức", politica:"Chính trị", beleza:"Làm đẹp", musica:"Âm nhạc", cultura:"Văn hóa", comercio:"Thương mại", industria:"Công nghiệp", servicos:"Dịch vụ", outro:"KHÁC/GÌ?" }
};

/* ===== FUNÇÕES AUXILIARES ===== */
function tradOpcao(chave) {
  var lang = getLang();
  var t = window.OPCOES_TRAD[lang] || window.OPCOES_TRAD.pt;
  return t[chave] || window.OPCOES_FALLBACK[chave] || chave;
}
function tradCard(chave){ var l=getLang(); var t=window.CARDS_TRAD[l]||window.CARDS_TRAD.pt; return t[chave]||chave; }
function tradMontar(chave){ var l=getLang(); var t=window.MONTAR_TRAD[l]||window.MONTAR_TRAD.pt; return t[chave]||chave; }
function tradEnergia(n){ var l=getLang(); var t=window.ENERGIA_TRAD[l]||window.ENERGIA_TRAD.pt; return t["e"+n]||"Energia "+n; }

/* ===== BÔNUS COLETIVO (22 produtos) ===== */
window.BC_PRODUTOS = window.BC_PRODUTOS || [
  ["express","Mapa Express",8,"🔮"],["vida","Qual Vida/Ano",8,"🔢"],["completo","Mapa Completo",17,"📘"],
  ["ia","Pesquisa IA de Nomes",17,"🤖"],["urna","Validação Nome de Urna",26,"🗳️"],["eleitoral","Número Eleitoral",26,"🔢"],
  ["imovel","Número do Imóvel",26,"🏠"],["calendario","Calendário Mensal Energético",26,"📅"],
  ["artistico","Validação Nome Artístico",35,"🎭"],["bebe","Planejamento Nome de Bebê",35,"👶"],["assinatura","Validação de Assinaturas",35,"✍️"],
  ["negocio","Nome para Negócio/Produto",44,"🏪"],["casal","Mapa do Casal",44,"💞"],["familia","Mapa Família Premium",98,"🌟"],
  ["nome_pet","Nome do Pet",8,"🐾"],["nickname","Nickname Digital",8,"🎮"],["nome_dominio","Nome do Domínio",8,"🌐"],
  ["nome_canal","Nome do Canal",8,"🎥"],["nome_equipe","Nome da Equipe",8,"🧭"],["nome_ong","Nome de ONG, Associação, Instituto ou Fundação",8,"🏛️"],
  ["nome_projeto","Nome do Projeto",8,"📋"],["nome_evento","Nome do Evento",8,"🎪"]
];

/* ===== TABELA BC ===== */
function montarTabelaBC() {
  var corpo = document.getElementById("bcTabelaCorpo");
  if (!corpo) return;
  corpo.innerHTML = "";
  window.BC_PRODUTOS.forEach(function(p) {
    var tr = document.createElement("tr");
    tr.setAttribute("data-prod", p[0]);
    tr.innerHTML = '<td><span class="bc-prod-nome">' + p[3] + ' ' + p[1] + '</span></td>'
      + '<td style="text-align:center;color:var(--gold)" class="bc-prod-preco">R$ ' + p[2] + '</td>'
      + '<td style="text-align:center"><input type="number" min="0" max="1000" value="0" data-prod="' + p[0] + '" oninput="atualizarResumoBC()"></td>';
    corpo.appendChild(tr);
  });
}
function precoUnitarioBC(prodId) {
  var p = window.BC_PRODUTOS.find(function(x){ return x[0] === prodId; });
  return p ? p[2] : 0;
}
function atualizarResumoBC() {
  var t = (typeof translations !== 'undefined' && translations[getLang()]) ? translations[getLang()] : {};
  var total = 0, qtdTotal = 0;
  document.querySelectorAll('#bcTabelaCorpo input[data-prod]').forEach(function(inp){
    var prod = inp.getAttribute('data-prod');
    var q = parseInt(inp.value, 10) || 0;
    window.BC_QUANTIDADES[prod] = q;
    total += q * precoUnitarioBC(prod);
    qtdTotal += q;
  });
  var pct = (typeof descontoBC === 'function') ? descontoBC(qtdTotal) : 0;
  var finalV = total - Math.round(total * pct / 100);
  var el = document.getElementById('bcResumo');
  if (el) {
    el.innerHTML = '<strong>' + (t.bc_total || 'Total bruto') + ':</strong> ' + total
      + ' &nbsp;|&nbsp; ' + (t.bc_discount || 'Desconto') + ': ' + pct + '%'
      + ' &nbsp;|&nbsp; <strong>' + (t.bc_final || 'Total final') + ':</strong> ' + finalV;
  }
}

/* ===== MENU DE ENERGIAS ===== */
window.ENERGIA_PRODUTOS = window.ENERGIA_PRODUTOS || [["express","🔮"],["completo","📘"],["ia","🤖"],["nome_pet","🐾"],["nickname","🎮"],["nome_dominio","🌐"],["nome_canal","🎥"],["nome_equipe","🧭"],["nome_ong","🏛️"],["nome_projeto","📋"],["nome_evento","🎪"]];
function pesquisarEnergia(n) {
  abrirMenuEnergia(n, getLang());
}
function fecharMenuEnergia() {
  var o = document.getElementById("menuEnergia");
  if (o) { o.classList.remove("active"); o.style.display = "none"; }
}
function abrirMenuEnergia(n, lang) {
  var t = translations[lang] || translations.pt;
  var titulo = (window.ENERGIA_TITULOS[lang] && window.ENERGIA_TITULOS[lang][String(n)]) ? window.ENERGIA_TITULOS[lang][String(n)] : ("Energia " + n);
  var overlay = document.getElementById("menuEnergia");
  if (!overlay) {
    overlay = document.createElement("div");
    overlay.id = "menuEnergia";
    overlay.className = "modal-overlay";
    overlay.innerHTML = '<div class="modal-box">'
      + '<h3 id="menuEnergiaTitulo"></h3>'
      + '<p id="menuEnergiaSub"></p>'
      + '<div id="menuEnergiaLista" class="modal-grid"></div>'
      + '<div class="modal-actions"><button id="menuEnergiaFechar" class="btn btn-outline">' + (t.fechar || "Fechar") + '</button></div>'
      + '</div>';
    document.body.appendChild(overlay);
    overlay.addEventListener("click", function(e){ if (e.target === overlay) fecharMenuEnergia(); });
    document.getElementById("menuEnergiaFechar").onclick = fecharMenuEnergia;
  }
  document.getElementById("menuEnergiaTitulo").textContent = (t.energia_label || "Energia") + " " + n + " — " + titulo;
  document.getElementById("menuEnergiaSub").textContent = t.energia_escolha || "Escolha um produto para pesquisar com esta energia:";
  var lista = document.getElementById("menuEnergiaLista");
  lista.innerHTML = "";
  window.ENERGIA_PRODUTOS.forEach(function(p) {
    var prod = p[0], icone = p[1];
    var nome = (window.PRODUTOS_TRAD[lang] && window.PRODUTOS_TRAD[lang][prod]) ? window.PRODUTOS_TRAD[lang][prod] : prod;
    var b = document.createElement("button");
    b.className = "btn btn-full";
    b.innerHTML = icone + " " + nome;
    b.onclick = function(){
      fecharMenuEnergia();
      var t2 = translations[lang] || translations.pt;
      if (prod === "express" || prod === "completo" || prod === "ia") {
        var nome = (document.getElementById("calcNome") ? document.getElementById("calcNome").value : "").trim();
        var nasc = (document.getElementById("calcNasc") ? document.getElementById("calcNasc").value : "").trim();
        if (!nome || !nasc) {
          alert(t2.preencha_dados || "Preencha nome e data de nascimento primeiro.");
          var sec = document.getElementById("calculadora") || document.getElementById("calcSection");
          if (sec) sec.scrollIntoView({ behavior: "smooth" });
          return;
        }
        window.location.href = "/criar-checkout?lang=" + lang + "&produto=" + prod
          + "&nome=" + encodeURIComponent(nome) + "&nascimento=" + encodeURIComponent(nasc)
          + "&energia=" + n;
        return;
      }
      window._energiaPresel = n;
      if (typeof pesquisar === "function") { pesquisar(prod); } else { if (typeof comprar === "function") comprar(prod); }
    };
    lista.appendChild(b);
  });
  overlay.style.display = "flex";
  overlay.classList.add("active");
}

/* ===== SELETOR DE ENERGIA ===== */
function fecharSeletorEnergia() {
  var o = document.getElementById("modalEnergiaSel");
  if (o) o.classList.remove("active");
}
function abrirSeletorEnergia(produto, lang) {
  var t = translations[lang] || translations.pt;
  var titulo = (window.PRODUTOS_TRAD[lang] && window.PRODUTOS_TRAD[lang][produto]) ? window.PRODUTOS_TRAD[lang][produto] : produto;
  var overlay = document.getElementById("modalEnergiaSel");
  if (!overlay) {
    overlay = document.createElement("div");
    overlay.id = "modalEnergiaSel";
    overlay.className = "modal-overlay";
    overlay.innerHTML = '<div class="modal-box">'
      + '<h3 id="modalEnergiaSelTitulo" style="color:var(--gold)"></h3>'
      + '<p style="color:#ccc;font-size:.9rem">' + (t.energia_escolha || "Escolha a energia para pesquisar:") + '</p>'
      + '<div id="modalEnergiaSelLista" class="modal-grid"></div>'
      + '<div class="modal-actions"><button id="modalEnergiaSelFechar" class="btn btn-outline">' + (t.fechar || "Fechar") + '</button></div>'
      + '</div>';
    document.body.appendChild(overlay);
    overlay.addEventListener("click", function(e){ if (e.target === overlay) fecharSeletorEnergia(); });
    document.getElementById("modalEnergiaSelFechar").onclick = fecharSeletorEnergia;
  }
  document.getElementById("modalEnergiaSelTitulo").textContent = titulo;
  var lista = document.getElementById("modalEnergiaSelLista");
  lista.innerHTML = "";
  var titulos = window.ENERGIA_TITULOS[lang] || window.ENERGIA_TITULOS["pt"];
  for (var i = 1; i <= 9; i++) {
    var nomeE = titulos[String(i)] || ("Energia " + i);
    var b = document.createElement("button");
    b.className = "btn btn-full";
    b.textContent = i + " - " + nomeE;
    b.onclick = function(){ fecharSeletorEnergia(); if (typeof irParaCompra === "function") irParaCompra(produto, lang, this.textContent.split(" - ")[0]); };
    lista.appendChild(b);
  }
  overlay.classList.add("active");
}

/* ===== PASSOS DO MODAL ===== */
function montarPassoEnergia(produto, lang) {
  var t = translations[lang] || translations.pt;
  document.getElementById("modalPassoTipo").style.display = "none";
  document.getElementById("modalPassoEnergia").style.display = "block";
  document.getElementById("modalPassoNome").style.display = "none";
  document.getElementById("modalEnergiaLabel").textContent = (t.energia_label || "Energia") + " (1-9):";
  var box = document.getElementById("modalEnergiaOpcoes");
  box.innerHTML = "";
  for (var i = 1; i <= 9; i++) {
    var nomeE = (window.ENERGIA_TITULOS[lang] && window.ENERGIA_TITULOS[lang][String(i)]) ? window.ENERGIA_TITULOS[lang][String(i)] : String(i);
    var b = document.createElement("button");
    b.className = "btn btn-full";
    b.textContent = i + " - " + nomeE;
    b.onclick = function(){ if (window._modalDado) window._modalDado.energia = i; montarPassoNome(produto, lang); };
    box.appendChild(b);
  }
}
function montarPassoNome(produto, lang) {
  var t = translations[lang] || translations.pt;
  document.getElementById("modalPassoTipo").style.display = "none";
  document.getElementById("modalPassoEnergia").style.display = "none";
  document.getElementById("modalPassoNome").style.display = "block";
  var label = (window.DADO_LABEL[lang] && window.DADO_LABEL[lang][produto]) ? window.DADO_LABEL[lang][produto] : window.DADO_LABEL.pt[produto];
  document.getElementById("modalNomeLabel").textContent = label + ":";
  document.getElementById("modalDadoInput").value = "";
  document.getElementById("modalDadoInput").focus();
}

/* ===== GRADE DE ENERGIAS ===== */
function montarEnergias() {
  var lang = getLang();
  var container = document.getElementById("energiasGrid")
    || document.getElementById("energias")
    || document.querySelector(".energias-grid");
  if (!container) return;
  var titulos = window.ENERGIA_TITULOS[lang] || window.ENERGIA_TITULOS["pt"];
  var descs = window.ENERGIAS_DESC[lang] || window.ENERGIAS_DESC["pt"] || {};
  var btn = window.ENERGIAS_BTN[lang] || "Pesquisar";
  var html = "";
  for (var i = 1; i <= 9; i++) {
    html += '<div class="energia-card">'
      + '<div class="energia-num">' + i + '</div>'
      + '<div class="energia-nome">' + (titulos[String(i)] || ("Energia " + i)) + '</div>'
      + '<div class="energia-desc">' + (descs[String(i)] || "") + '</div>'
      + '<button class="btn btn-full" onclick="pesquisarEnergia(' + i + ')">' + btn + '</button>'
      + '</div>';
  }
  container.innerHTML = html;
}

/* ===== CONFIRMAR BÔNUS COLETIVO ===== */
function confirmarBC() {
  var itens = [];
  for (var id in window.BC_QUANTIDADES) {
    if (window.BC_QUANTIDADES[id] > 0) {
      var prod = window.BC_PRODUTOS.find(function(p) { return p[0] === id; });
      if (prod) itens.push({ id: id, nome: prod[1], preco: precoUnitarioBC(id), qtd: window.BC_QUANTIDADES[id] });
    }
  }
  var t = translations[getLang()] || translations.pt;
  if (itens.length === 0) { alert(t.alert_bc_vazio || "Selecione pelo menos 1 serviço."); return; }
  var bruto = itens.reduce(function(a, i) { return a + i.preco * i.qtd; }, 0);
  var qtdTotal = itens.reduce(function(a, i) { return a + i.qtd; }, 0);
  var pct = (typeof descontoBC === "function") ? descontoBC(qtdTotal) : 0;
  var final = bruto - Math.round(bruto * pct / 100);
  var simbolo = (window.PRECO_DISPLAY && window.PRECO_DISPLAY[getLang()] && window.PRECO_DISPLAY[getLang()][0])
    ? window.PRECO_DISPLAY[getLang()][0].replace(/[0-9.,\s]/g, '').trim() : 'R$';
  var linhas = itens.map(function(i) {
    return (t.bc_linha || "{nome}: {qtd}x {simbolo} {preco} = {simbolo} {total}")
      .replace('{nome}', i.nome).replace('{qtd}', i.qtd).replace('{simbolo}', simbolo)
      .replace('{preco}', i.preco).replace('{total}', (i.qtd * i.preco));
  }).join("\n");
  var msg = (t.bc_resumo_titulo || "RESUMO DO PEDIDO") + "\n\n" + linhas + "\n\n"
    + (t.bc_total || "Total bruto:") + " " + simbolo + " " + bruto + "\n"
    + (t.bc_discount || "Desconto aplicado:") + " (" + pct + "%): " + simbolo + " " + Math.round(bruto * pct / 100) + "\n"
    + (t.bc_final || "Total final:") + " " + simbolo + " " + final + "\n\n"
    + (t.bc_confirmar_pag || "Confirmar e ir para pagamento?");
  if (!confirm(msg)) return;
  window.location.href = '/criar-checkout?lang=' + getLang() + '&produto=coletivo&qtd=' + qtdTotal + '&total=' + final + '&itens=' + encodeURIComponent(JSON.stringify(itens));
}

/* ===== TRADUZIR TUDO ===== */
function traduzirTudo() {
  if (window._traduzindo) return;
  window._traduzindo = true;
  try {
    var lang = getLang();
    var t = translations[lang] || translations.pt;
    document.querySelectorAll('[data-i18n]').forEach(function(el) {
      var k = el.getAttribute('data-i18n');
      if (t[k]) el.innerText = t[k];
    });
    if (typeof renderizarNumeros === 'function' && typeof ultimosNumeros !== 'undefined' && ultimosNumeros && ultimosNumeros.length) {
    if (typeof atualizarMesesData === "function") atualizarMesesData();  
      renderizarNumeros();
    }
    document.querySelectorAll('[data-i18n-ph]').forEach(function(el) {
      var k = el.getAttribute('data-i18n-ph');
      var v = t[k] || t.calc_nome;
      if (v) el.placeholder = v;
    });
    document.querySelectorAll('.product-card[data-prod]').forEach(function(card) {
      var prod = card.getAttribute('data-prod');
      var nome = card.querySelector('.prod-nome');
      if (nome && window.PRODUTOS_TRAD[lang] && window.PRODUTOS_TRAD[lang][prod]) nome.innerText = window.PRODUTOS_TRAD[lang][prod];
      var preco = card.querySelector('.prod-preco');
      if (preco && window.PRECO_DISPLAY && window.PRECO_DISPLAY[lang] && window.PRODUTO_FAIXA[prod] !== undefined) {
        preco.innerText = window.PRECO_DISPLAY[lang][window.PRODUTO_FAIXA[prod]];
      }
      var feats = window.FEAT_TRAD[lang] && window.FEAT_TRAD[lang][prod];
      if (feats) card.querySelectorAll('.features li').forEach(function(li, i) {
        if (feats[i]) li.innerText = feats[i];
      });
      var desc = card.querySelector('.desc');
      if (desc && window.PRODUTOS_TRAD[lang] && window.PRODUTOS_TRAD[lang]['desc_' + prod]) {
        desc.innerText = window.PRODUTOS_TRAD[lang]['desc_' + prod];
      }
    });
    document.querySelectorAll('#bcTabelaCorpo tr[data-prod]').forEach(function(tr) {
      var prod = tr.getAttribute('data-prod');
      var nome = tr.querySelector('.bc-prod-nome');
      if (nome && window.PRODUTOS_TRAD[lang] && window.PRODUTOS_TRAD[lang][prod]) nome.innerText = window.PRODUTOS_TRAD[lang][prod];
      var preco = tr.querySelector('.bc-prod-preco');
      if (preco && window.PRECO_DISPLAY && window.PRECO_DISPLAY[lang] && window.PRODUTO_FAIXA[prod] !== undefined) {
        preco.innerText = window.PRECO_DISPLAY[lang][window.PRODUTO_FAIXA[prod]];
      }
    });
    document.querySelectorAll('[data-i18n-bc]').forEach(function(el) {
      var k = el.getAttribute('data-i18n-bc');
      var mapa = { servico: t.bc_servico || "Serviço", preco: t.bc_preco || "Preço", qtd: t.bc_qtd || "Quantidade" };
      if (mapa[k]) el.innerText = mapa[k];
    });
    if (typeof atualizarLinkInvestidores === "function") {
      atualizarLinkInvestidores();
    }
  } finally {
    window._traduzindo = false;
  }
}
