function tradOpcao(chave) {
  var lang = getLang();
  var t = OPCOES_TRAD[lang] || OPCOES_TRAD.pt;
  return t[chave] || OPCOES_FALLBACK[chave] || chave;
function tradCard(chave){ var l=getLang(); var t=CARDS_TRAD[l]||CARDS_TRAD.pt; return t[chave]||chave; }
function tradMontar(chave){ var l=getLang(); var t=MONTAR_TRAD[l]||MONTAR_TRAD.pt; return t[chave]||chave; }
function tradEnergia(n){ var l=getLang(); var t=ENERGIA_TRAD[l]||ENERGIA_TRAD.pt; return t["e"+n]||"Energia "+n; }

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

