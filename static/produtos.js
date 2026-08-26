function tradOpcao(chave) {
  var lang = getLang();
  var t = OPCOES_TRAD[lang] || OPCOES_TRAD.pt;
  return t[chave] || OPCOES_FALLBACK[chave] || chave;
}<!-- PRODUTOS E SERVIÇOS (23) -->
    <section id="produtos">
        <div class="section-header">
            <h2 data-i18n="section_products_title">Produtos e Serviços</h2>
            <p data-i18n="section_products_subtitle">Escolha o produto ideal para sua análise numerológica</p>
        </div>
        <div class="cards-grid" id="produtosGrid">
            <!-- 1. Mapa Express -->
            <div class="product-card" data-prod="express">
                <div class="icon">🔮</div>
                <h3 class="prod-nome" data-i18n="p_express">Mapa Express</h3>
                <div class="price prod-preco">R$ 8</div>
             <p class="desc" data-i18n="desc_express">1 página com os 5 números principais e seu significado resumido. Ideal para uma visão rápida.</p>
             <ul class="features">
              <li>✅ Caminho da Vida</li>
              <li>✅ Expressão, Alma, Personalidade</li>
              <li>✅ Destino</li>
              <li>📲 PDF + QRCode</li>
             </ul>
                <button class="btn btn-full" onclick="pesquisar('express')" data-i18n="pesquisar_btn">pesquisar</button>
            </div>
var CONF_COLETA = {
  nome_canal:   { labelTipo:"f_tipo_canal",   tipos:["youtube","podcast","tiktok","twitch"],        temArea:true,  areas:["esporte","noticias","politica","beleza"], temDetalhe:false },
  nickname:     { labelTipo:"f_tipo_nickname", tipos:["gamer","profissional","criador","artista"],  temArea:false, areas:[], temDetalhe:false },
  nome_ong:     { labelTipo:"f_tipo_ong",      tipos:["ong","instituto","associacao","fundacao"],   temArea:false, areas:[], temDetalhe:false },
  nome_evento:  { labelTipo:"f_tipo_evento",   tipos:["show","congresso","festa","curso","palestra"],temArea:true,  areas:["musica","esporte","cultura","politica","beleza"], temDetalhe:false },
  nome_projeto: { labelTipo:"f_tipo_projeto",  tipos:["pessoal","social","empresarial","cultural"], temArea:false, areas:[], temDetalhe:false },
  nome_equipe:  { labelTipo:"f_tipo_equipe",   tipos:["empresarial","projeto","esportiva","banda"], temArea:false, areas:[], temDetalhe:false },
  nome_dominio: { labelTipo:"f_tipo_site",     tipos:["loja","empresa","blog","portfolio"],         temArea:true,  areas:["comercio","industria","servicos","pessoal"], temDetalhe:false },
  nome_pet:     { labelTipo:"f_tipo_pet",      tipos:["cao","gato","passaro","reptil"],             temArea:false, areas:[], temDetalhe:true }
};
var coletaAtual = null;
function pesquisar(produto) {
  if (produto === "express" || produto === "completo") {
    var sec = document.getElementById("calculadora") || document.getElementById("calcSection");
    if (sec) sec.scrollIntoView({ behavior:"smooth", block:"center" });
    return;
  }
  if (CONF_COLETA[produto]) { abrirModalColeta(produto); return; }
  var alvo = document.getElementById("form-" + produto);
  if (alvo) {
    alvo.scrollIntoView({ behavior:"smooth", block:"center" });
    alvo.style.transition = "box-shadow .5s";
    alvo.style.boxShadow = "0 0 0 3px var(--gold)";
    setTimeout(function(){ alvo.style.boxShadow = ""; }, 2000);
    return;
  }
  var calc = document.getElementById("calculadora") || document.getElementById("calcSection");
  if (calc) calc.scrollIntoView({ behavior:"smooth" });
}

/* ===== CARDS_TRAD — Cards dos 8 produtos (12 idiomas) =====*/
var CARDS_TRAD = {
  pt:{ nome_pet:"Nome do Pet", nome_pet_desc:"A energia do nome do seu animal de estimação.",
       nickname:"Nickname Digital", nickname_desc:"A vibração do seu nickname nas redes.",
       nome_dominio:"Nome do Domínio", nome_dominio_desc:"A energia do nome do seu domínio.",
       nome_canal:"Nome do Canal", nome_canal_desc:"A energia do nome do seu canal.",
       nome_equipe:"Nome da Equipe", nome_equipe_desc:"A vibração do nome da sua equipe.",
       nome_ong:"Nome de ONG", nome_ong_desc:"A energia do nome da sua organização.",
       nome_projeto:"Nome do Projeto", nome_projeto_desc:"A energia do nome do seu projeto.",
       nome_evento:"Nome do Evento", nome_evento_desc:"A vibração do nome do seu evento.",
       buscar:"Buscar" },
  en:{ nome_pet:"Pet Name", nome_pet_desc:"The energy of your pet's name.",
       nickname:"Digital Nickname", nickname_desc:"The vibration of your nickname online.",
       nome_dominio:"Domain Name", nome_dominio_desc:"The energy of your domain name.",
       nome_canal:"Channel Name", nome_canal_desc:"The energy of your channel name.",
       nome_equipe:"Team Name", nome_equipe_desc:"The vibration of your team's name.",
       nome_ong:"NGO Name", nome_ong_desc:"The energy of your organization's name.",
       nome_projeto:"Project Name", nome_projeto_desc:"The energy of your project name.",
       nome_evento:"Event Name", nome_evento_desc:"The vibration of your event's name.",
       buscar:"Search" },
  es:{ nome_pet:"Nombre de la Mascota", nome_pet_desc:"La energía del nombre de tu mascota.",
       nickname:"Apodo Digital", nickname_desc:"La vibración de tu apodo en redes.",
       nome_dominio:"Nombre del Dominio", nome_dominio_desc:"La energía del nombre de tu dominio.",
       nome_canal:"Nombre del Canal", nome_canal_desc:"La energía del nombre de tu canal.",
       nome_equipe:"Nombre del Equipo", nome_equipe_desc:"La vibración del nombre de tu equipo.",
       nome_ong:"Nombre de la ONG", nome_ong_desc:"La energía del nombre de tu organización.",
       nome_projeto:"Nombre del Proyecto", nome_projeto_desc:"La energía del nombre de tu proyecto.",
       nome_evento:"Nombre del Evento", nome_evento_desc:"La vibración del nombre de tu evento.",
       buscar:"Buscar" },
  fr:{ nome_pet:"Nom de l'animal", nome_pet_desc:"L'énergie du nom de votre animal.",
       nickname:"Surnom numérique", nickname_desc:"La vibration de votre surnom en ligne.",
       nome_dominio:"Nom de domaine", nome_dominio_desc:"L'énergie du nom de votre domaine.",
       nome_canal:"Nom de la chaîne", nome_canal_desc:"L'énergie du nom de votre chaîne.",
       nome_equipe:"Nom de l'équipe", nome_equipe_desc:"La vibration du nom de votre équipe.",
       nome_ong:"Nom de l'ONG", nome_ong_desc:"L'énergie du nom de votre organisation.",
       nome_projeto:"Nom du projet", nome_projeto_desc:"L'énergie du nom de votre projet.",
       nome_evento:"Nom de l'événement", nome_evento_desc:"La vibration du nom de votre événement.",
       buscar:"Rechercher" },
  it:{ nome_pet:"Nome dell'animale", nome_pet_desc:"L'energia del nome del tuo animale.",
       nickname:"Soprannome digitale", nickname_desc:"La vibrazione del tuo soprannome online.",
       nome_dominio:"Nome del dominio", nome_dominio_desc:"L'energia del nome del tuo dominio.",
       nome_canal:"Nome del canale", nome_canal_desc:"L'energia del nome del tuo canale.",
       nome_equipe:"Nome del team", nome_equipe_desc:"La vibrazione del nome del tuo team.",
       nome_ong:"Nome dell'ONG", nome_ong_desc:"L'energia del nome della tua organizzazione.",
       nome_projeto:"Nome del progetto", nome_projeto_desc:"L'energia del nome del tuo progetto.",
       nome_evento:"Nome dell'evento", nome_evento_desc:"La vibrazione del nome del tuo evento.",
       buscar:"Cerca" },
  de:{ nome_pet:"Haustiername", nome_pet_desc:"Die Energie des Namens Ihres Haustiers.",
       nickname:"Digitaler Spitzname", nickname_desc:"Die Schwingung Ihres Spitznamens online.",
       nome_dominio:"Domainname", nome_dominio_desc:"Die Energie Ihres Domainnamens.",
       nome_canal:"Kanalname", nome_canal_desc:"Die Energie Ihres Kanalnamens.",
       nome_equipe:"Teamname", nome_equipe_desc:"Die Schwingung des Namens Ihres Teams.",
       nome_ong:"NGO-Name", nome_ong_desc:"Die Energie des Namens Ihrer Organisation.",
       nome_projeto:"Projektname", nome_projeto_desc:"Die Energie Ihres Projektnamens.",
       nome_evento:"Veranstaltungsname", nome_evento_desc:"Die Schwingung des Namens Ihrer Veranstaltung.",
       buscar:"Suchen" },
  ru:{ nome_pet:"Имя питомца", nome_pet_desc:"Энергия имени вашего питомца.",
       nickname:"Цифровой никнейм", nickname_desc:"Вибрация вашего никнейма в сети.",
       nome_dominio:"Доменное имя", nome_dominio_desc:"Энергия вашего доменного имени.",
       nome_canal:"Название канала", nome_canal_desc:"Энергия названия вашего канала.",
       nome_equipe:"Название команды", nome_equipe_desc:"Вибрация названия вашей команды.",
       nome_ong:"Название НПО", nome_ong_desc:"Энергия названия вашей организации.",
       nome_projeto:"Название проекта", nome_projeto_desc:"Энергия названия вашего проекта.",
       nome_evento:"Название события", nome_evento_desc:"Вибрация названия вашего события.",
       buscar:"Поиск" },
  zh:{ nome_pet:"宠物名称", nome_pet_desc:"您的宠物名字的能量。",
       nickname:"数字昵称", nickname_desc:"您的网络昵称的振动。",
       nome_dominio:"域名", nome_dominio_desc:"您的域名的能量。",
       nome_canal:"频道名称", nome_canal_desc:"您的频道名称的能量。",
       nome_equipe:"团队名称", nome_equipe_desc:"您的团队名称的振动。",
       nome_ong:"非政府组织名称", nome_ong_desc:"您的组织名称的能量。",
       nome_projeto:"项目名称", nome_projeto_desc:"您的项目名称的能量。",
       nome_evento:"活动名称", nome_evento_desc:"您的活动名称的振动。",
       buscar:"搜索" },
  ja:{ nome_pet:"ペット名", nome_pet_desc:"ペットの名前のエネルギー。",
       nickname:"デジタルニックネーム", nickname_desc:"オンラインのニックネームの振動。",
       nome_dominio:"ドメイン名", nome_dominio_desc:"ドメイン名のエネルギー。",
       nome_canal:"チャンネル名", nome_canal_desc:"チャンネル名のエネルギー。",
       nome_equipe:"チーム名", nome_equipe_desc:"チーム名の振動。",
       nome_ong:"NGO名", nome_ong_desc:"組織名のエネルギー。",
       nome_projeto:"プロジェクト名", nome_projeto_desc:"プロジェクト名のエネルギー。",
       nome_evento:"イベント名", nome_evento_desc:"イベント名の振動。",
       buscar:"検索" },
  ar:{ nome_pet:"اسم الحيوان الأليف", nome_pet_desc:"طاقة اسم حيوانك الأليف.",
       nickname:"الاسم المستعار الرقمي", nickname_desc:"اهتزاز اسمك المستعار على الإنترنت.",
       nome_dominio:"اسم النطاق", nome_dominio_desc:"طاقة اسم النطاق الخاص بك.",
       nome_canal:"اسم القناة", nome_canal_desc:"طاقة اسم قناتك.",
       nome_equipe:"اسم الفريق", nome_equipe_desc:"اهتزاز اسم فريقك.",
       nome_ong:"اسم المنظمة", nome_ong_desc:"طاقة اسم مؤسستك.",
       nome_projeto:"اسم المشروع", nome_projeto_desc:"طاقة اسم مشروعك.",
       nome_evento:"اسم الفعالية", nome_evento_desc:"اهتزاز اسم فعاليتك.",
       buscar:"بحث" },
  he:{ nome_pet:"שם חיית המחמד", nome_pet_desc:"האנרגיה של שם חיית המחמד שלך.",
       nickname:"כינוי דיגיטלי", nickname_desc:"הרטט של הכינוי שלך ברשת.",
       nome_dominio:"שם הדומיין", nome_dominio_desc:"האנרגיה של שם הדומיין שלך.",
       nome_canal:"שם הערוץ", nome_canal_desc:"האנרגיה של שם הערוץ שלך.",
       nome_equipe:"שם הצוות", nome_equipe_desc:"הרטט של שם הצוות שלך.",
       nome_ong:"שם הארגון", nome_ong_desc:"האנרגיה של שם הארגון שלך.",
       nome_projeto:"שם הפרויקט", nome_projeto_desc:"האנרגיה של שם הפרויקט שלך.",
       nome_evento:"שם האירוע", nome_evento_desc:"הרטט של שם האירוע שלך.",
       buscar:"חיפוש" },
  hi:{ nome_pet:"पालतू जानवर का नाम", nome_pet_desc:"आपके पालतू जानवर के नाम की ऊर्जा।",
       nickname:"डिजिटल उपनाम", nickname_desc:"आपके ऑनलाइन उपनाम की कंपन।",
       nome_dominio:"डोमेन का नाम", nome_dominio_desc:"आपके डोमेन नाम की ऊर्जा।",
       nome_canal:"चैनल का नाम", nome_canal_desc:"आपके चैनल नाम की ऊर्जा।",
       nome_equipe:"टीम का नाम", nome_equipe_desc:"आपकी टीम के नाम की कंपन।",
       nome_ong:"एनजीओ का नाम", nome_ong_desc:"आपके संगठन के नाम की ऊर्जा।",
       nome_projeto:"परियोजना का नाम", nome_projeto_desc:"आपकी परियोजना के नाम की ऊर्जा।",
       nome_evento:"कार्यक्रम का नाम", nome_evento_desc:"आपके कार्यक्रम के नाम की कंपन।",
       buscar:"खोज" }
};
/* =====  MONTAR_TRAD — Montar Sob Medida (12 idiomas) =====*/
var MONTAR_TRAD = {
  pt:{ titulo:"Montar Sob Medida", subtitulo:"Escolha os produtos e a energia desejada.",
       produto:"Produto", energia:"Energia", quantidade:"Quantidade", preco:"Preço",
       adicionar:"Adicionar", remover:"Remover", finalizar:"Finalizar",
       bruto:"Valor Bruto", desconto:"Desconto Aplicado", total:"Total",
       vazio:"Seu carrinho está vazio" },
  en:{ titulo:"Build Custom", subtitulo:"Choose the products and desired energy.",
       produto:"Product", energia:"Energy", quantidade:"Quantity", preco:"Price",
       adicionar:"Add", remover:"Remove", finalizar:"Checkout",
       bruto:"Gross Amount", desconto:"Applied Discount", total:"Total",
       vazio:"Your cart is empty" },
  es:{ titulo:"Montar a Medida", subtitulo:"Elige los productos y la energía deseada.",
       produto:"Producto", energia:"Energía", quantidade:"Cantidad", preco:"Precio",
       adicionar:"Añadir", remover:"Eliminar", finalizar:"Finalizar",
       bruto:"Importe Bruto", desconto:"Descuento Aplicado", total:"Total",
       vazio:"Tu carrito está vacío" },
  fr:{ titulo:"Composer sur Mesure", subtitulo:"Choisissez les produits et l'énergie souhaitée.",
       produto:"Produit", energia:"Énergie", quantidade:"Quantité", preco:"Prix",
       adicionar:"Ajouter", remover:"Retirer", finalizar:"Finaliser",
       bruto:"Montant Brut", desconto:"Remise Appliquée", total:"Total",
       vazio:"Votre panier est vide" },
  it:{ titulo:"Componi su Misura", subtitulo:"Scegli i prodotti e l'energia desiderata.",
       produto:"Prodotto", energia:"Energia", quantidade:"Quantità", preco:"Prezzo",
       adicionar:"Aggiungi", remover:"Rimuovi", finalizar:"Finalizza",
       bruto:"Importo Lordo", desconto:"Sconto Applicato", total:"Totale",
       vazio:"Il tuo carrello è vuoto" },
  de:{ titulo:"Individuell Zusammenstellen", subtitulo:"Wählen Sie die Produkte und die gewünschte Energie.",
       produto:"Produkt", energia:"Energie", quantidade:"Menge", preco:"Preis",
       adicionar:"Hinzufügen", remover:"Entfernen", finalizar:"Abschließen",
       bruto:"Bruttobetrag", desconto:"Angewendeter Rabatt", total:"Gesamt",
       vazio:"Ihr Warenkorb ist leer" },
  ru:{ titulo:"Собрать на Заказ", subtitulo:"Выберите продукты и желаемую энергию.",
       produto:"Продукт", energia:"Энергия", quantidade:"Количество", preco:"Цена",
       adicionar:"Добавить", remover:"Удалить", finalizar:"Оформить",
       bruto:"Валовая сумма", desconto:"Примененная скидка", total:"Итого",
       vazio:"Ваша корзина пуста" },
  zh:{ titulo:"定制组合", subtitulo:"选择产品和所需能量。",
       produto:"产品", energia:"能量", quantidade:"数量", preco:"价格",
       adicionar:"添加", remover:"移除", finalizar:"结算",
       bruto:"总额", desconto:"已应用折扣", total:"总计",
       vazio:"您的购物车是空的" },
  ja:{ titulo:"カスタム作成", subtitulo:"製品と希望のエネルギーを選択してください。",
       produto:"製品", energia:"エネルギー", quantidade:"数量", preco:"価格",
       adicionar:"追加", remover:"削除", finalizar:"確定",
       bruto:"総額", desconto:"適用割引", total:"合計",
       vazio:"カートは空です" },
  ar:{ titulo:"تخصيص حسب الطلب", subtitulo:"اختر المنتجات والطاقة المطلوبة.",
       produto:"المنتج", energia:"الطاقة", quantidade:"الكمية", preco:"السعر",
       adicionar:"إضافة", remover:"إزالة", finalizar:"إتمام",
       bruto:"المبلغ الإجمالي", desconto:"الخصم المطبق", total:"الإجمالي",
       vazio:"سلة التسوق فارغة" },
  he:{ titulo:"הרכבה אישית", subtitulo:"בחרו את המוצרים ואת האנרגיה הרצויה.",
       produto:"מוצר", energia:"אנרגיה", quantidade:"כמות", preco:"מחיר",
       adicionar:"הוסף", remover:"הסר", finalizar:"סיים",
       bruto:"סכום ברוטו", desconto:"הנחה מיושמת", total:"סה״כ",
       vazio:"העגלה שלך ריקה" },
  hi:{ titulo:"कस्टम बनाएं", subtitulo:"उत्पाद और वांछित ऊर्जा चुनें।",
       produto:"उत्पाद", energia:"ऊर्जा", quantidade:"मात्रा", preco:"मूल्य",
       adicionar:"जोड़ें", remover:"हटाएं", finalizar:"समाप्त करें",
       bruto:"सकल राशि", desconto:"लागू छूट", total:"कुल",
       vazio:"आपकी टोकरी खाली है" }
};
/* =====  ENERGIA_TRAD — Nomes das 9 energias (12 idiomas) =====*/
var ENERGIA_TRAD = {
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
  hi:{ e1:"नेता", e2:"राजनयिक", e3:"रचनात्मकता", e4:"संरचना", e5:"स्वतंत्रता", e6:"सद्भाव", e7:"आध्यात्मिकता", e8:"शक्ति", e9:"मानवतावाद" }
};

function tradCard(chave){ var l=getLang(); var t=CARDS_TRAD[l]||CARDS_TRAD.pt; return t[chave]||chave; }
function tradMontar(chave){ var l=getLang(); var t=MONTAR_TRAD[l]||MONTAR_TRAD.pt; return t[chave]||chave; }
function tradEnergia(n){ var l=getLang(); var t=ENERGIA_TRAD[l]||ENERGIA_TRAD.pt; return t["e"+n]||"Energia "+n; }

/* =====  MODAL DO DADO ESPECÍFICO (múltiplos passos) =====*/
var DADO_LABEL = {
  pt:{nome_pet:"Nome do Pet",nickname:"Nickname Digital",nome_dominio:"Nome do Domínio",nome_canal:"Nome do Canal",nome_equipe:"Nome da Equipe",nome_ong:"Nome da ONG",nome_projeto:"Nome do Projeto",nome_evento:"Nome do Evento"},
  en:{nome_pet:"Pet Name",nickname:"Digital Nickname",nome_dominio:"Domain Name",nome_canal:"Channel Name",nome_equipe:"Team Name",nome_ong:"NGO Name",nome_projeto:"Project Name",nome_evento:"Event Name"},
  es:{nome_pet:"Nombre de Mascota",nickname:"Nickname Digital",nome_dominio:"Nombre de Dominio",nome_canal:"Nombre de Canal",nome_equipe:"Nombre del Equipo",nome_ong:"Nombre de la ONG",nome_projeto:"Nombre del Proyecto",nome_evento:"Nombre del Evento"},
  it:{nome_pet:"Nome dell'Animale",nickname:"Nickname Digitale",nome_dominio:"Nome del Dominio",nome_canal:"Nome del Canale",nome_equipe:"Nome del Team",nome_ong:"Nome dell'ONG",nome_projeto:"Nome del Progetto",nome_evento:"Nome dell'Evento"},
  fr:{nome_pet:"Nom de l'Animal",nickname:"Pseudo Digital",nome_dominio:"Nom de Domaine",nome_canal:"Nom de Chaîne",nome_equipe:"Nom de l'Équipe",nome_ong:"Nom de l'ONG",nome_projeto:"Nom du Projet",nome_evento:"Nom de l'Événement"},
  de:{nome_pet:"Haustiername",nickname:"Digitaler Nickname",nome_dominio:"Domainname",nome_canal:"Kanalname",nome_equipe:"Teamname",nome_ong:"NGO-Name",nome_projeto:"Projektname",nome_evento:"Veranstaltungsname"},
  ja:{nome_pet:"ペットの名前",nickname:"デジタルニックネーム",nome_dominio:"ドメイン名",nome_canal:"チャンネル名",nome_equipe:"チーム名",nome_ong:"NGO名",nome_projeto:"プロジェクト名",nome_evento:"イベント名"},
  zh:{nome_pet:"宠物名字",nickname:"数字昵称",nome_dominio:"域名",nome_canal:"频道名称",nome_equipe:"团队名称",nome_ong:"NGO名称",nome_projeto:"项目名称",nome_evento:"活动名称"},
  ru:{nome_pet:"Имя питомца",nickname:"Цифровой никнейм",nome_dominio:"Имя домена",nome_canal:"Название канала",nome_equipe:"Название команды",nome_ong:"Название НКО",nome_projeto:"Название проекта",nome_evento:"Название события"},
  hi:{nome_pet:"पालतू नाम",nickname:"डिजिटल उपनाम",nome_dominio:"डोमेन नाम",nome_canal:"चैनल नाम",nome_equipe:"टीम नाम",nome_ong:"एनजीओ नाम",nome_projeto:"परियोजना नाम",nome_evento:"इवेंट नाम"},
  he:{nome_pet:"שם חיית המחמד",nickname:"כינוי דיגיטלי",nome_dominio:"שם דומיין",nome_canal:"שם הערוץ",nome_equipe:"שם הצוות",nome_ong:"שם העמותה",nome_projeto:"שם הפרויקט",nome_evento:"שם האירוע"},
  ar:{nome_pet:"اسم الحيوان الأليف",nickname:"اللقب الرقمي",nome_dominio:"اسم النطاق",nome_canal:"اسم القناة",nome_equipe:"اسم الفريق",nome_ong:"اسم المنظمة",nome_projeto:"اسم المشروع",nome_evento:"اسم الفعالية"}
};

/* =====  DADOS DE TIPO POR PRODUTO (para o modal de múltiplos passos) =====*/
var DADO_TIPOS = {
  nome_pet: { label:"Tipo de Pet", opcoes:["Gato","Cão","Pássaro","Réptil","Outro"] },
  nickname: { label:"Tipo de Perfil", opcoes:["Gamer","Criador","Profissional","Artista","Outro"] },
  nome_dominio: { label:"Tipo de Site", opcoes:["Blog","Loja","Portfólio","Empresa","Outro"] },
  nome_canal: { label:"Tipo de Canal", opcoes:["YouTube","Podcast","Twitch","TikTok","Outro"] },
  nome_equipe: { label:"Tipo de Equipe", opcoes:["Esportiva","Empresarial","Projeto","Banda","Outro"] },
  nome_ong: { label:"Tipo de Instituição", opcoes:["ONG","Associação","Instituto","Fundação","Outro"] },
  nome_projeto: { label:"Tipo de Projeto", opcoes:["Pessoal","Empresarial","Social","Cultural","Outro"] },
  nome_evento: { label:"Tipo de Evento", opcoes:["Congresso","Curso","Festa","Palestra","Outro"] }
};

/* ============================================================*/
// FORMULÁRIOS DE COLETA — 8 produtos (versão ÚNICA e limpa)
/* ============================================================*/
var OPCOES_FALLBACK = {
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

function abrirModalColeta(produto) {
  var lang = getLang();
  var t = translations[lang] || translations.pt;
  var conf = CONF_COLETA[produto];
  var overlay = document.getElementById("modalColeta");
  if (!overlay) return;
  coletaAtual = produto;
  document.getElementById("coletaTitulo").textContent =
  (PRODUTOS_TRAD[lang] && PRODUTOS_TRAD[lang][produto]) || produto;
  document.getElementById("coletaLabelTipo").textContent = t[conf.labelTipo] || t.f_tipo || "Tipo";
  var wrap = document.getElementById("coletaOpcoesTipo");
  wrap.innerHTML = "";
  conf.tipos.forEach(function(ch){
    var b = document.createElement("button");
    b.type = "button"; b.className = "btn btn-outline coleta-opcao";
    b.setAttribute("data-valor", ch); b.textContent = tradOpcao(ch);
    b.onclick = function(){ selecionarOpcao(wrap, b); };
    wrap.appendChild(b);
  });
  var bOutro = document.createElement("button");
  bOutro.type = "button"; bOutro.className = "btn btn-outline coleta-opcao";
  bOutro.setAttribute("data-valor", "__outro__"); bOutro.textContent = t.f_outro || "OUTRO/QUAL?";
  bOutro.onclick = function(){
    selecionarOpcao(wrap, bOutro);
    document.getElementById("coletaOutroWrap").style.display = "block";
  };
  wrap.appendChild(bOutro);
  document.getElementById("coletaOutroWrap").style.display = "none";
  document.getElementById("coletaOutroTexto").value = "";
  montarGradeEnergia("coletaEnergia");
  var areaWrap = document.getElementById("coletaAreaWrap");
  if (conf.temArea) {
    areaWrap.style.display = "block";
    document.getElementById("coletaLabelArea").textContent = t.f_area || "Área Desejada";
    var aw = document.getElementById("coletaOpcoesArea");
    aw.innerHTML = "";
    conf.areas.forEach(function(ch){
      var b = document.createElement("button");
      b.type = "button"; b.className = "btn btn-outline coleta-opcao";
      b.setAttribute("data-valor", ch); b.textContent = tradOpcao(ch);
      b.onclick = function(){ selecionarOpcao(aw, b); };
      aw.appendChild(b);
    });
    var bAOutro = document.createElement("button");
    bAOutro.type = "button"; bAOutro.className = "btn btn-outline coleta-opcao";
    bAOutro.setAttribute("data-valor", "__outro__"); bAOutro.textContent = t.f_outro || "OUTRO/QUAL?";
    bAOutro.onclick = function(){
      selecionarOpcao(aw, bAOutro);
      document.getElementById("coletaAreaOutroWrap").style.display = "block";
    };
    aw.appendChild(bAOutro);
    document.getElementById("coletaAreaOutroWrap").style.display = "none";
    document.getElementById("coletaAreaOutroTexto").value = "";
  } else {
    areaWrap.style.display = "none";
  }
  var detWrap = document.getElementById("coletaDetalheWrap");
  if (conf.temDetalhe) {
    detWrap.style.display = "block";
    document.getElementById("coletaLabelDetalhe").textContent = t.f_detalhe || "Detalhe / Particularidade";
    document.getElementById("coletaDetalheTexto").value = "";
  } else {
    detWrap.style.display = "none";
  }
  overlay.style.display = "flex";
  if (typeof traduzirTudo === "function") traduzirTudo();
}

function confirmarColeta() {
  if (!coletaAtual) return;
  var lang = getLang();
  var t = translations[lang] || translations.pt;
  var conf = CONF_COLETA[coletaAtual];
  var tipoEl = document.querySelector("#coletaOpcoesTipo .coleta-opcao.ativo");
  var tipo = tipoEl ? tipoEl.getAttribute("data-valor") : "";
  if (tipo === "__outro__") tipo = document.getElementById("coletaOutroTexto").value.trim();
  var enEl = document.querySelector("#coletaEnergia .energia-num.ativo");
  var energia = enEl ? enEl.textContent : "";
  var area = "";
  if (conf.temArea) {
    var areaEl = document.querySelector("#coletaOpcoesArea .coleta-opcao.ativo");
    area = areaEl ? areaEl.getAttribute("data-valor") : "";
    if (area === "__outro__") area = document.getElementById("coletaAreaOutroTexto").value.trim();
  }
  var detalhe = conf.temDetalhe ? document.getElementById("coletaDetalheTexto").value.trim() : "";
  if (!tipo || !energia) { alert(t.preencha_dado || "Preencha os dados solicitados."); return; }
  var qs = "lang=" + encodeURIComponent(lang)
         + "&produto=" + encodeURIComponent(coletaAtual)
         + "&tipo=" + encodeURIComponent(tipo)
         + "&energia=" + encodeURIComponent(energia);
  if (area) qs += "&area=" + encodeURIComponent(area);
  if (detalhe) qs += "&detalhe=" + encodeURIComponent(detalhe);
  fecharModalColeta();
  window.location.href = "/criar-checkout?" + qs;
}
document.addEventListener("DOMContentLoaded", function(){
  var f = document.getElementById("coletaFechar");   if (f) f.onclick = fecharModalColeta;
  var c = document.getElementById("coletaCancelar"); if (c) c.onclick = fecharModalColeta;
  var ok = document.getElementById("coletaConfirmar"); if (ok) ok.onclick = confirmarColeta;
  var ov = document.getElementById("modalColeta");
  if (ov) ov.addEventListener("click", function(e){ if (e.target === ov) fecharModalColeta(); });
});

/* ===== BÔNUS COLETIVO / EMPRESARIAL (23 produtos) =====*/
var BC_PRODUTOS = [
  ["express","Mapa Express",8,"🔮"],["vida","Qual Vida/Ano",8,"🔢"],["completo","Mapa Completo",17,"📘"],
  ["ia","Pesquisa IA de Nomes",17,"🤖"],["urna","Validação Nome de Urna",26,"🗳️"],["eleitoral","Número Eleitoral",26,"🔢"],
  ["imovel","Número do Imóvel",26,"🏠"],["calendario","Calendário Mensal Energético",26,"📅"],
  ["artistico","Validação Nome Artístico",35,"🎭"],["bebe","Planejamento Nome de Bebê",35,"👶"],["assinatura","Validação de Assinaturas",35,"✍️"],
  ["negocio","Nome para Negócio/Produto",44,"🏪"],["casal","Mapa do Casal",44,"💞"],["familia","Mapa Família Premium",98,"🌟"],
  // --- 8 produtos novos (faixa R$ 8) ---
  ["nome_pet","Nome do Pet",8,"🐾"],["nickname","Nickname Digital",8,"🎮"],["nome_dominio","Nome do Domínio",8,"🌐"],
  ["nome_canal","Nome do Canal",8,"🎥"],["nome_equipe","Nome da Equipe",8,"🧭"],["nome_ong","Nome de ONG, Associação, Instituto ou Fundação",8,"🏛️"],
  ["nome_projeto","Nome do Projeto",8,"📋"],["nome_evento","Nome do Evento",8,"🎪"]
];

/* ===== BÔNUS COLETIVO / EMPRESARIAL (funções resgatadas) =====*/
var BC_QUANTIDADES = {};

function montarTabelaBC() {
  var corpo = document.getElementById("bcTabelaCorpo");
  if (!corpo) return;
  corpo.innerHTML = "";
  if (!window.BC_PRODUTOS || !BC_PRODUTOS.length) return;
  BC_PRODUTOS.forEach(function(p) {
    var tr = document.createElement("tr");
    tr.setAttribute("data-prod", p[0]);
    tr.innerHTML = '<td><span class="bc-prod-nome">' + p[3] + ' ' + p[1] + '</span></td>'
      + '<td style="text-align:center;color:var(--gold)" class="bc-prod-preco">R$ ' + p[2] + '</td>'
      + '<td style="text-align:center"><input type="number" min="0" max="1000" value="0" data-prod="' + p[0] + '" oninput="atualizarResumoBC()"></td>';
    corpo.appendChild(tr);
  });
}

function atualizarResumoBC() {
  var bruto = 0, qtdTotal = 0;
  document.querySelectorAll("#bcTabelaCorpo input[data-prod]").forEach(function(inp) {
    var q = parseInt(inp.value) || 0;
    BC_QUANTIDADES[inp.getAttribute("data-prod")] = q;
    var prod = BC_PRODUTOS.find(function(p) { return p[0] === inp.getAttribute("data-prod"); });
    if (prod) { bruto += q * prod[2]; qtdTotal += q; }
  });
  var descontoPct = descontoBC(qtdTotal);
  var desconto = Math.round(bruto * descontoPct / 100);
  var final = bruto - desconto;
  var lang = getLang();
  var bc = BC_TEXTS[lang] || BC_TEXTS.pt;
  var simbolo = PRECO_DISPLAY[lang][0].replace(/[0-9.,\s]/g, '').trim() || 'R$';
  document.getElementById("bcTotalBruto").textContent = simbolo + " " + bruto.toLocaleString("pt-BR");
  document.getElementById("bcDesconto").textContent = simbolo + " " + desconto.toLocaleString("pt-BR") + " (" + descontoPct + "%)";
  document.getElementById("bcTotalFinal").textContent = simbolo + " " + final.toLocaleString("pt-BR");
  document.getElementById("bcFaixaInfo").textContent = bc.qtd_total + " " + qtdTotal + " " + bc.codigos;
}

function pesquisarEnergia(n) {
  var lang = getLang();
  abrirMenuEnergia(n, lang);
}

var ENERGIA_PRODUTOS = [["express","🔮"],["completo","📘"],["ia","🤖"],["nome_pet","🐾"],["nickname","🎮"],["nome_dominio","🌐"],["nome_canal","🎥"],["nome_equipe","🧭"],["nome_ong","🏛️"],["nome_projeto","📋"],["nome_evento","🎪"]];

function abrirMenuEnergia(n, lang) {
  var t = translations[lang] || translations.pt;
  var titulo = (ENERGIA_TITULOS[lang] && ENERGIA_TITULOS[lang][String(n)]) ? ENERGIA_TITULOS[lang][String(n)] : ("Energia " + n);
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
  ENERGIA_PRODUTOS.forEach(function(p) {
    var prod = p[0], icone = p[1];
    var nome = (PRODUTOS_TRAD[lang] && PRODUTOS_TRAD[lang][prod]) ? PRODUTOS_TRAD[lang][prod] : prod;
    var b = document.createElement("button");
    b.className = "btn btn-full";
    b.innerHTML = icone + " " + nome;
    b.onclick = function(){ fecharMenuEnergia(); pesquisar(prod); };
    lista.appendChild(b);
  });
  overlay.classList.add("active");
}
function fecharMenuEnergia() {
  var o = document.getElementById("menuEnergia");
  if (o) o.classList.remove("active");
}

/*===== OPCOES_TRAD — rótulos das opções (12 idiomas) =====*/
var OPCOES_TRAD = {
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
  hi:{ youtube:"यूट्यूब", podcast:"पॉडकास्ट", tiktok:"टिकटॉक", twitch:"ट्विच", gamer:"गेमर", profissional:"पेशेवर", criador:"निर्माता", artista:"कलाकार", ong:"एनजीओ", instituto:"संस्थान", associacao:"संघ", fundacao:"फाउंडेशन", show:"शो", congresso:"सम्मेलन", festa:"पार्टी", curso:"पाठ्यक्रम", palestra:"व्याख्यान", pessoal:"व्यक्तिगत", social:"सामाजिक", empresarial:"व्यावसायिक", cultural:"सांस्कृतिक", esportiva:"खेल", banda:"बैंड", loja:"दुकान", empresa:"कंपनी", blog:"ब्लॉग", portfolio:"पोर्टफोलियो", cao:"कुत्ता", gato:"बिल्ली", passaro:"पक्षी", reptil:"सरीसृप", projeto:"परियोजना", esporte:"खेल", noticias:"समाचार", politica:"राजनीति", beleza:"सुंदरता", musica:"संगीत", cultura:"संस्कृति", comercio:"वाणिज्य", industria:"उद्योग", servicos:"सेवाएं", outro:"अन्य/क्या?" }
};

/* ===== SELETOR DE ENERGIA (para produtos da lista de energias) =====*/
function abrirSeletorEnergia(produto, lang) {
  var t = translations[lang] || translations.pt;
  var titulo = (PRODUTOS_TRAD[lang] && PRODUTOS_TRAD[lang][produto]) ? PRODUTOS_TRAD[lang][produto] : produto;
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
  var titulos = (ENERGIA_TITULOS && ENERGIA_TITULOS[lang]) ? ENERGIA_TITULOS[lang] : ENERGIA_TITULOS["pt"];
  for (var i = 1; i <= 9; i++) {
    var nomeE = titulos[String(i)] || ("Energia " + i);
    var b = document.createElement("button");
    b.className = "btn btn-full";
    b.textContent = i + " - " + nomeE;
    b.onclick = function(){ fecharSeletorEnergia(); irParaCompra(produto, lang, this.textContent.split(" - ")[0]); };
    lista.appendChild(b);
  }
  overlay.classList.add("active");
}
function fecharSeletorEnergia() {
  var o = document.getElementById("modalEnergiaSel");
  if (o) o.classList.remove("active");
}

function montarPassoEnergia(produto, lang) {
  var t = translations[lang] || translations.pt;
  document.getElementById("modalPassoTipo").style.display = "none";
  document.getElementById("modalPassoEnergia").style.display = "block";
  document.getElementById("modalPassoNome").style.display = "none";
  document.getElementById("modalEnergiaLabel").textContent = (t.energia_label || "Energia") + " (1-9):";
  var box = document.getElementById("modalEnergiaOpcoes");
  box.innerHTML = "";
  for (var i = 1; i <= 9; i++) {
    var nomeE = (ENERGIA_TITULOS[lang] && ENERGIA_TITULOS[lang][String(i)]) ? ENERGIA_TITULOS[lang][String(i)] : String(i);
    var b = document.createElement("button");
    b.className = "btn btn-full";
    b.textContent = i + " - " + nomeE;
    b.onclick = function(){ _modalDado.energia = i; montarPassoNome(produto, lang); };
    box.appendChild(b);
  }
}
function montarPassoNome(produto, lang) {
  var t = translations[lang] || translations.pt;
  document.getElementById("modalPassoTipo").style.display = "none";
  document.getElementById("modalPassoEnergia").style.display = "none";
  document.getElementById("modalPassoNome").style.display = "block";
  var label = (DADO_LABEL[lang] && DADO_LABEL[lang][produto]) ? DADO_LABEL[lang][produto] : DADO_LABEL.pt[produto];
  document.getElementById("modalNomeLabel").textContent = label + ":";
  document.getElementById("modalDadoInput").value = "";
  document.getElementById("modalDadoInput").focus();
}

function montarEnergias() {
  var lang = getLang();
  var container = document.getElementById("energiasGrid")
    || document.getElementById("energias")
    || document.querySelector(".energias-grid");
  if (!container) return;
  var titulos = (ENERGIA_TITULOS && ENERGIA_TITULOS[lang]) ? ENERGIA_TITULOS[lang] : ENERGIA_TITULOS["pt"];
  var descs = (ENERGIAS_DESC && ENERGIAS_DESC[lang]) ? ENERGIAS_DESC[lang] : ENERGIAS_DESC["pt"];
  var btn = (ENERGIAS_BTN && ENERGIAS_BTN[lang]) ? ENERGIAS_BTN[lang] : "Pesquisar";
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

function confirmarBC() {
  var itens = [];
  for (var id in BC_QUANTIDADES) {
    if (BC_QUANTIDADES[id] > 0) {
      var prod = BC_PRODUTOS.find(function(p) { return p[0] === id; });
      if (prod) itens.push({ id: id, nome: prod[1], preco: prod[2], qtd: BC_QUANTIDADES[id] });
    }
  }
  var t = translations[getLang()] || translations.pt;
  if (itens.length === 0) { alert(t.alert_bc_vazio || "Selecione pelo menos 1 serviço."); return; }
  var bruto = itens.reduce(function(a, i) { return a + i.preco * i.qtd; }, 0);
  var qtdTotal = itens.reduce(function(a, i) { return a + i.qtd; }, 0);
  var pct = descontoBC(qtdTotal);
  var final = bruto - Math.round(bruto * pct / 100);
  var simbolo = (PRECO_DISPLAY[getLang()] ? PRECO_DISPLAY[getLang()][0].replace(/[0-9.,\s]/g, '').trim() : '') || 'R$';
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

/* ===== TRADUZ TUDO =====*/
var _traduzindo = false;
function traduzirTudo() {
  if (_traduzindo) return;   // ← trava: se já está traduzindo, não re-entra
  _traduzindo = true;
  try {  
  var lang = getLang();
  var t = translations[lang] || translations.pt;
  document.querySelectorAll('[data-i18n]').forEach(function(el) {
    var k = el.getAttribute('data-i18n');
    if (t[k]) el.innerText = t[k];
  });
  }
    if (typeof renderizarNumeros === 'function' && typeof ultimosNumeros !== 'undefined' && ultimosNumeros && ultimosNumeros.length) {
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
  if (nome && PRODUTOS_TRAD[lang] && PRODUTOS_TRAD[lang][prod]) nome.innerText = PRODUTOS_TRAD[lang][prod];

  var preco = card.querySelector('.prod-preco');
  if (preco && PRODUTO_FAIXA[prod] !== undefined && PRECO_DISPLAY[lang]) preco.innerText = PRECO_DISPLAY[lang][PRODUTO_FAIXA[prod]];

  var feats = FEAT_TRAD[lang] && FEAT_TRAD[lang][prod];
  if (feats) card.querySelectorAll('.features li').forEach(function(li, i) {
    if (feats[i]) li.innerText = feats[i];
  });   // ← fecha o forEach das features

  // ✅ NOVO: traduz a descrição (dentro do loop do card)
  var desc = card.querySelector('.desc');
  if (desc && PRODUTOS_TRAD[lang] && PRODUTOS_TRAD[lang]['desc_' + prod]) {
    desc.innerText = PRODUTOS_TRAD[lang]['desc_' + prod];
  }
});   // ← fecha o forEach dos cards
  document.querySelectorAll('#bcTabelaCorpo tr[data-prod]').forEach(function(tr) {
    var prod = tr.getAttribute('data-prod');
    var nome = tr.querySelector('.bc-prod-nome');
    if (nome && PRODUTOS_TRAD[lang] && PRODUTOS_TRAD[lang][prod]) nome.innerText = PRODUTOS_TRAD[lang][prod];
    var preco = tr.querySelector('.bc-prod-preco');
    if (preco && PRODUTO_FAIXA[prod] !== undefined && PRECO_DISPLAY[lang]) preco.innerText = PRECO_DISPLAY[lang][PRODUTO_FAIXA[prod]];
  });
    } finally {
    _traduzindo = false;     
  }

