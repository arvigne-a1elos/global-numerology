/* ===== PRECO_BASE / SIMB / PRECO_DISPLAY (GLOBAL — uma única vez) ===== */
var PRECO_BASE = {
  pt:[8,17,26,35,44,98], en:[20,44,71,89,116,251], es:[11,26,35,53,62,134],
  it:[11,26,35,53,62,134], fr:[11,26,35,53,62,134], de:[11,26,35,53,62,134],
  ja:[1400,3000,4600,6200,7700,17000], zh:[26,53,71,98,125,260],
  ru:[440,800,1250,1700,2150,4400], id:[11000,23000,36000,48000,60000,134000],
  tr:[58,123,188,254,319,710], vi:[25000,53000,81000,109000,137000,305000],
  he:[44,98,143,197,242,530], ar:[35,71,107,143,170,377]
};
var SIMB = {pt:'R$',en:'US$',es:'€',it:'€',fr:'€',de:'€',ja:'¥',zh:'¥',ru:'₽',id:'Rp',tr:'₺',vi:'₫',he:'₪',ar:'﷼'};
var PRECO_DISPLAY = {};
Object.keys(PRECO_BASE).forEach(function(l){
  var zero = (l==='ja'||l==='vi');
  PRECO_DISPLAY[l] = PRECO_BASE[l].map(function(v){
    var txt = zero ? String(v) : v.toFixed(2).replace('.', ',');
    return SIMB[l]+' '+txt;
  });
});

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

  function pesquisar(produto) {
  if (produto === "express" || produto === "completo") {
    var sec = document.getElementById("calculadora") || document.getElementById("calcSection");
    if (sec) sec.scrollIntoView({ behavior:"smooth", block:"center" });
    return;
  }
  if (CONF_COLETA[produto]) {
  if (typeof comprar === "function") { comprar(produto); return; }
  return;
}
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

/* ===== CARDS_TRAD — Cards dos 8 produtos (14 idiomas) =====*/
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
  id:{ nome_pet:"Nama Hewan Peliharaan", nome_pet_desc:"Energi dari nama hewan peliharaan Anda.",
       nickname:"Nama Panggilan Digital", nickname_desc:"Getaran nama panggilan Anda di media sosial.",
       nome_dominio:"Nama Domain", nome_dominio_desc:"Energi dari nama domain Anda.",
       nome_canal:"Nama Kanal", nome_canal_desc:"Energi dari nama kanal Anda.",
       nome_equipe:"Nama Tim", nome_equipe_desc:"Getaran dari nama tim Anda.",
       nome_ong:"Nama LSM", nome_ong_desc:"Energi dari nama organisasi Anda.",
       nome_projeto:"Nama Proyek", nome_projeto_desc:"Energi dari nama proyek Anda.",
       nome_evento:"Nama Acara", nome_evento_desc:"Getaran dari nama acara Anda.",
       buscar:"Cari" },
  tr:{ nome_pet:"Evcil Hayvan Adı", nome_pet_desc:"Evcil hayvanınızın adının enerjisi.",
       nickname:"Dijital Takma Ad", nickname_desc:"Çevrimiçi takma adınızın titreşimi.",
       nome_dominio:"Alan Adı", nome_dominio_desc:"Alan adınızın enerjisi.",
       nome_canal:"Kanal Adı", nome_canal_desc:"Kanal adınızın enerjisi.",
       nome_equipe:"Ekip Adı", nome_equipe_desc:"Ekip adınızın titreşimi.",
       nome_ong:"STK Adı", nome_ong_desc:"Kuruluşunuzun adının enerjisi.",
       nome_projeto:"Proje Adı", nome_projeto_desc:"Projenizin adının enerjisi.",
       nome_evento:"Etkinlik Adı", nome_evento_desc:"Etkinliğinizin adının titreşimi.",
       buscar:"Ara" },
  vi:{ nome_pet:"Tên Thú Cưng", nome_pet_desc:"Năng lượng của tên thú cưng của bạn.",
       nickname:"Biệt Danh Kỹ Thuật Số", nickname_desc:"Rung động của biệt danh trực tuyến của bạn.",
       nome_dominio:"Tên Miền", nome_dominio_desc:"Năng lượng của tên miền của bạn.",
       nome_canal:"Tên Kênh", nome_canal_desc:"Năng lượng của tên kênh của bạn.",
       nome_equipe:"Tên Đội Nhóm", nome_equipe_desc:"Rung động của tên đội nhóm của bạn.",
       nome_ong:"Tên Tổ Chức", nome_ong_desc:"Năng lượng của tên tổ chức của bạn.",
       nome_projeto:"Tên Dự Án", nome_projeto_desc:"Năng lượng của tên dự án của bạn.",
       nome_evento:"Tên Sự Kiện", nome_evento_desc:"Rung động của tên sự kiện của bạn.",
       buscar:"Tìm Kiếm" },
};
/* =====  MONTAR_TRAD — Montar Sob Medida (14 idiomas) =====*/
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
  id:{ titulo:"Rakit Sesuai Keinginan", subtitulo:"Pilih produk dan energi yang diinginkan.",
       produto:"Produk", energia:"Energi", quantidade:"Jumlah", preco:"Harga",
       adicionar:"Tambah", remover:"Hapus", finalizar:"Selesaikan",
       bruto:"Nilai Kotor", desconto:"Diskon Diterapkan", total:"Total",
       vazio:"Keranjang Anda kosong" },
  tr:{ titulo:"Özel Oluştur", subtitulo:"İstediğiniz ürünleri ve enerjiyi seçin.",
       produto:"Ürün", energia:"Enerji", quantidade:"Miktar", preco:"Fiyat",
       adicionar:"Ekle", remover:"Kaldır", finalizar:"Tamamla",
       bruto:"Brüt Değer", desconto:"Uygulanan İndirim", total:"Toplam",
       vazio:"Sepetiniz boş" },
  vi:{ titulo:"Tạo Theo Yêu Cầu", subtitulo:"Chọn sản phẩm và năng lượng mong muốn.",
       produto:"Sản Phẩm", energia:"Năng Lượng", quantidade:"Số Lượng", preco:"Giá",
       adicionar:"Thêm", remover:"Xóa", finalizar:"Hoàn Tất",
       bruto:"Tổng Thô", desconto:"Giảm Giá Áp Dụng", total:"Tổng",
       vazio:"Giỏ hàng của bạn trống" }
};
/* =====  ENERGIA_TRAD — Nomes das 9 energias (14 idiomas) =====*/
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
  id:{ e1:"Pemimpin", e2:"Diplomat", e3:"Kreativitas", e4:"Struktur", e5:"Kebebasan", e6:"Harmoni", e7:"Spiritualitas", e8:"Kekuatan", e9:"Kemanusiaan" },
  tr:{ e1:"Lider", e2:"Diplomat", e3:"Yaratıcılık", e4:"Yapı", e5:"Özgürlük", e6:"Uyum", e7:"Maneviyat", e8:"Güç", e9:"İnsaniyet" },
  vi:{ e1:"Lãnh đạo", e2:"Nhà ngoại giao", e3:"Sáng tạo", e4:"Cấu trúc", e5:"Tự do", e6:"Hòa hợp", e7:"Tâm linh", e8:"Sức mạnh", e9:"Nhân đạo" }
};

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
  he:{nome_pet:"שם חיית המחמד",nickname:"כינוי דיגיטלי",nome_dominio:"שם דומיין",nome_canal:"שם הערוץ",nome_equipe:"שם הצוות",nome_ong:"שם העמותה",nome_projeto:"שם הפרויקט",nome_evento:"שם האירוע"},
  ar:{nome_pet:"اسم الحيوان الأليف",nickname:"اللقب الرقمي",nome_dominio:"اسم النطاق",nome_canal:"اسم القناة",nome_equipe:"اسم الفريق",nome_ong:"اسم المنظمة",nome_projeto:"اسم المشروع",nome_evento:"اسم الفعالية"},
  id:{nome_pet:"Nama Hewan Peliharaan",nickname:"Nama Panggilan Digital",nome_dominio:"Nama Domain",nome_canal:"Nama Kanal",nome_equipe:"Nama Tim",nome_ong:"Nama LSM",nome_projeto:"Nama Proyek",nome_evento:"Nama Acara"},
  tr:{nome_pet:"Evcil Hayvan Adı",nickname:"Dijital Takma Ad",nome_dominio:"Alan Adı",nome_canal:"Kanal Adı",nome_equipe:"Ekip Adı",nome_ong:"STK Adı",nome_projeto:"Proje Adı",nome_evento:"Etkinlik Adı"},
  vi:{nome_pet:"Tên Thú Cưng",nickname:"Biệt Danh Kỹ Thuật Số",nome_dominio:"Tên Miền",nome_canal:"Tên Kênh",nome_equipe:"Tên Đội Nhóm",nome_ong:"Tên Tổ Chức",nome_projeto:"Tên Dự Án",nome_evento:"Tên Sự Kiện"}
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

function tradOpcao(chave) {
  var lang = getLang();
  var t = OPCOES_TRAD[lang] || OPCOES_TRAD.pt;
  return t[chave] || OPCOES_FALLBACK[chave] || chave; }
function tradCard(chave){ var l=getLang(); var t=CARDS_TRAD[l]||CARDS_TRAD.pt; return t[chave]||chave; }
function tradMontar(chave){ var l=getLang(); var t=MONTAR_TRAD[l]||MONTAR_TRAD.pt; return t[chave]||chave; }
function tradEnergia(n){ var l=getLang(); var t=ENERGIA_TRAD[l]||ENERGIA_TRAD.pt; return t["e"+n]||"Energia "+n; }

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
  pesquisar(prod);
};
 });
}
/*===== OPCOES_TRAD — rótulos das opções (14 idiomas) =====*/
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
  id:{ youtube:"YouTube", podcast:"Podcast", tiktok:"TikTok", twitch:"Twitch", gamer:"Gamer", profissional:"Profesional", criador:"Pencipta", artista:"Artis", ong:"LSM", instituto:"Lembaga", associacao:"Asosiasi", fundacao:"Yayasan", show:"Pertunjukan", congresso:"Kongres", festa:"Pesta", curso:"Kursus", palestra:"Ceramah", pessoal:"Pribadi", social:"Sosial", empresarial:"Bisnis", cultural:"Budaya", esportiva:"Olahraga", banda:"Band", loja:"Toko", empresa:"Perusahaan", blog:"Blog", portfolio:"Portofolio", cao:"Anjing", gato:"Kucing", passaro:"Burung", reptil:"Reptil", projeto:"Proyek", esporte:"Olahraga", noticias:"Berita", politica:"Politik", beleza:"Kecantikan", musica:"Musik", cultura:"Budaya", comercio:"Perdagangan", industria:"Industri", servicos:"Layanan", outro:"LAINNYA/APA?" },
  tr:{ youtube:"YouTube", podcast:"Podcast", tiktok:"TikTok", twitch:"Twitch", gamer:"Oyuncu", profissional:"Profesyonel", criador:"İçerik Üreticisi", artista:"Sanatçı", ong:"STK", instituto:"Enstitü", associacao:"Dernek", fundacao:"Vakıf", show:"Gösteri", congresso:"Kongre", festa:"Parti", curso:"Kurs", palestra:"Konferans", pessoal:"Kişisel", social:"Sosyal", empresarial:"İş", cultural:"Kültürel", esportiva:"Spor", banda:"Müzik Grubu", loja:"Mağaza", empresa:"Şirket", blog:"Blog", portfolio:"Portfolyo", cao:"Köpek", gato:"Kedi", passaro:"Kuş", reptil:"Sürüngen", projeto:"Proje", esporte:"Spor", noticias:"Haberler", politica:"Siyaset", beleza:"Güzellik", musica:"Müzik", cultura:"Kültür", comercio:"Ticaret", industria:"Endüstri", servicos:"Hizmetler", outro:"DİĞER/NE?" },  
  vi:{ youtube:"YouTube", podcast:"Podcast", tiktok:"TikTok", twitch:"Twitch", gamer:"Game thủ", profissional:"Chuyên nghiệp", criador:"Người sáng tạo", artista:"Nghệ sĩ", ong:"Tổ chức phi chính phủ", instituto:"Viện", associacao:"Hiệp hội", fundacao:"Quỹ", show:"Buổi diễn", congresso:"Đại hội", festa:"Tiệc", curso:"Khóa học", palestra:"Bài giảng", pessoal:"Cá nhân", social:"Xã hội", empresarial:"Kinh doanh", cultural:"Văn hóa", esportiva:"Thể thao", banda:"Ban nhạc", loja:"Cửa hàng", empresa:"Công ty", blog:"Blog", portfolio:"Hồ sơ năng lực", cao:"Chó", gato:"Mèo", passaro:"Chim", reptil:"Bò sát", projeto:"Dự án", esporte:"Thể thao", noticias:"Tin tức", politica:"Chính trị", beleza:"Làm đẹp", musica:"Âm nhạc", cultura:"Văn hóa", comercio:"Thương mại", industria:"Công nghiệp", servicos:"Dịch vụ", outro:"KHÁC/GÌ?" }
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
      if (prod) itens.push({ id: id, nome: prod[1], preco: precoUnitarioBC(id), qtd: BC_QUANTIDADES[id] });
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

function traduzirTudo() {
  if (_traduzindo) return;
  _traduzindo = true;
  try {
    var lang = getLang();
    var t = translations[lang] || translations.pt;
    document.querySelectorAll('[data-i18n]').forEach(function(el) {
      var k = el.getAttribute('data-i18n');
      if (t[k]) el.innerText = t[k];
    });
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
      if (preco && PRECO_DISPLAY[lang] && PRODUTO_FAIXA[prod] !== undefined) preco.innerText = PRECO_DISPLAY[lang][PRODUTO_FAIXA[prod]];
      var feats = FEAT_TRAD[lang] && FEAT_TRAD[lang][prod];
      if (feats) card.querySelectorAll('.features li').forEach(function(li, i) {
        if (feats[i]) li.innerText = feats[i];
      });
      var desc = card.querySelector('.desc');
      if (desc && PRODUTOS_TRAD[lang] && PRODUTOS_TRAD[lang]['desc_' + prod]) {
        desc.innerText = PRODUTOS_TRAD[lang]['desc_' + prod];
      }
    });
    document.querySelectorAll('#bcTabelaCorpo tr[data-prod]').forEach(function(tr) {
      var prod = tr.getAttribute('data-prod');
      var nome = tr.querySelector('.bc-prod-nome');
      if (nome && PRODUTOS_TRAD[lang] && PRODUTOS_TRAD[lang][prod]) nome.innerText = PRODUTOS_TRAD[lang][prod];
      var preco = tr.querySelector('.bc-prod-preco');
      if (preco && PRECO_DISPLAY[lang] && PRODUTO_FAIXA[prod] !== undefined) preco.innerText = PRECO_DISPLAY[lang][PRODUTO_FAIXA[prod]];
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
    _traduzindo = false;
  }
}
