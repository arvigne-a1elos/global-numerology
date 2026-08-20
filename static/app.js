// ===== A1ELOS GLOBAL NUMEROLOGY - APP.JS (VERSÃO CONSOLIDADA) =====
// Preserva todas as funções existentes + adiciona:
//  - Modal de dado específico (8 produtos novos) com múltiplos passos
//  - Menu de produtos por energia
//  - BC_PRODUTOS com 23 produtos
// ================================================================

// ===== TRADUZ TUDO =====
function traduzirTudo() {
  var lang = getLang();
  var t = translations[lang] || translations.pt;
  document.querySelectorAll('[data-i18n]').forEach(function(el) {
    var k = el.getAttribute('data-i18n');
    if (t[k]) el.innerText = t[k];
  });
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
    if (feats) card.querySelectorAll('.features li').forEach(function(li, i) { if (feats[i]) li.innerText = feats[i]; });
  });
  if (typeof montarEnergias === "function") montarEnergias();
  var BC_HEAD_KEY = { servico:'bc_tbl_service', preco:'bc_tbl_price', qtd:'bc_tbl_qty' };
  document.querySelectorAll('[data-i18n-bc]').forEach(function(el) {
    var k = el.getAttribute('data-i18n-bc');
    var v = t[BC_HEAD_KEY[k]] || t[k];
    if (v) el.innerText = v;
  });
  document.querySelectorAll('#bcTabelaCorpo tr[data-prod]').forEach(function(tr) {
    var prod = tr.getAttribute('data-prod');
    var nome = tr.querySelector('.bc-prod-nome');
    if (nome && PRODUTOS_TRAD[lang] && PRODUTOS_TRAD[lang][prod]) nome.innerText = PRODUTOS_TRAD[lang][prod];
    var preco = tr.querySelector('.bc-prod-preco');
    if (preco && PRODUTO_FAIXA[prod] !== undefined && PRECO_DISPLAY[lang]) preco.innerText = PRECO_DISPLAY[lang][PRODUTO_FAIXA[prod]];
  });
  if (typeof atualizarResumoBC === 'function') atualizarResumoBC();
}

// ===== MONTAR SELETOR DE IDIOMAS (12 bandeiras) =====
function montarSeletorIdioma() {
  var container = document.getElementById('langSelector');
  if (!container) return;
  if (container.children.length > 0) return;
  var lista = [
    {id:'pt', b:'🇧🇷'},{id:'en', b:'🇺🇸'},{id:'es', b:'🇪🇸'},{id:'it', b:'🇮🇹'},
    {id:'fr', b:'🇫🇷'},{id:'de', b:'🇩🇪'},{id:'ja', b:'🇯🇵'},{id:'zh', b:'🇨🇳'},
    {id:'ru', b:'🇷🇺'},{id:'hi', b:'🇮🇳'},{id:'he', b:'🇮🇱'},{id:'ar', b:'🇸🇦'}
  ];
  var atual = getLang();
  lista.forEach(function(l) {
    var b = document.createElement('button');
    b.className = 'lang-btn' + (l.id === atual ? ' active' : '');
    b.title = l.id.toUpperCase();
    b.innerHTML = l.b;
    b.onclick = function() {
      setLanguage(l.id);
      if (typeof traduzirTudo === 'function') traduzirTudo();
      var ativos = container.querySelectorAll('.lang-btn');
      for (var i = 0; i < ativos.length; i++) ativos[i].classList.remove('active');
      b.classList.add('active');
    };
    container.appendChild(b);
  });
}

// ===== COMPRAR (abre modal do dado específico para os 8 produtos) =====
var DADO_APLICA = ["nome_pet","nickname","nome_dominio","nome_canal","nome_equipe","nome_ong","nome_projeto","nome_evento"];

function comprar(produto) {
  var lang = getLang();
  var t = translations[lang] || translations.pt;
  // Produtos que precisam de dado específico → abre modal
  if (DADO_APLICA.indexOf(produto) !== -1) {
    abrirModalDado(produto, lang);
    return;
  }
  // Demais produtos → fluxo atual (nome + nascimento)
  var nome = (document.getElementById("calcNome") ? document.getElementById("calcNome").value : "").trim();
  var nasc = (document.getElementById("calcNasc") ? document.getElementById("calcNasc").value : "").trim();
  if (!nome || !nasc) {
    alert(t.preencha_dados || "Preencha nome e data de nascimento primeiro.");
    var sec = document.getElementById("calcSection") || document.getElementById("calculadora");
    if (sec) sec.scrollIntoView({ behavior: "smooth" });
    return;
  }
  window.location.href = '/criar-checkout?lang=' + lang + '&produto=' + produto
    + '&nome=' + encodeURIComponent(nome) + '&nascimento=' + encodeURIComponent(nasc);
}

// ===== MODAL DO DADO ESPECÍFICO (múltiplos passos) =====
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

// ===== DADOS DE TIPO POR PRODUTO (para o modal de múltiplos passos) =====
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

function abrirModalDado(produto, lang) {
  var t = translations[lang] || translations.pt;
  var label = (DADO_LABEL[lang] && DADO_LABEL[lang][produto]) ? DADO_LABEL[lang][produto] : DADO_LABEL.pt[produto];
  var titulo = (PRODUTOS_TRAD[lang] && PRODUTOS_TRAD[lang][produto]) ? PRODUTOS_TRAD[lang][produto] : label;
  var overlay = document.getElementById("modalDado");
  if (!overlay) {
    overlay = document.createElement("div");
    overlay.id = "modalDado";
    overlay.className = "modal-overlay";
    overlay.innerHTML = '<div class="modal-box">'
      + '<h3 id="modalDadoTitulo"></h3>'
      + '<p id="modalDadoLabel"></p>'
      // Passo 1: tipo
      + '<div id="modalPassoTipo"><p id="modalTipoLabel" style="color:#ccc;margin-bottom:8px"></p><div id="modalTipoOpcoes" class="modal-grid"></div></div>'
      // Passo 2: energia (1-9)
      + '<div id="modalPassoEnergia" style="display:none"><p id="modalEnergiaLabel" style="color:#ccc;margin-bottom:8px"></p><div id="modalEnergiaOpcoes" class="modal-grid"></div></div>'
      // Passo 3: nome
      + '<div id="modalPassoNome" style="display:none"><p id="modalNomeLabel" style="color:#ccc;margin-bottom:8px"></p><input id="modalDadoInput" type="text" class="modal-input"></div>'
      + '<div class="modal-actions">'
      + '<button id="modalDadoOk" class="btn">' + (t.confirmar || "Confirmar") + '</button>'
      + '<button id="modalDadoCancel" class="btn btn-outline">' + (t.cancelar || "Cancelar") + '</button>'
      + '</div></div>';
    document.body.appendChild(overlay);
    overlay.addEventListener("click", function(e){ if (e.target === overlay) fecharModalDado(); });
    document.getElementById("modalDadoCancel").onclick = fecharModalDado;
    document.getElementById("modalDadoOk").onclick = function(){ confirmarModalDado(produto, lang); };
  }
  document.getElementById("modalDadoTitulo").textContent = titulo;
  document.getElementById("modalDadoLabel").textContent = label;
  // Monta passos
  window._modalDado = { produto: produto, lang: lang, tipo: "", energia: "" };
  montarPassoTipo(produto, lang);
  overlay.classList.add("active");
}
function montarPassoTipo(produto, lang) {
  var t = translations[lang] || translations.pt;
  var tipos = DADO_TIPOS[produto] || { label: "Tipo", opcoes: [] };
  document.getElementById("modalPassoTipo").style.display = "block";
  document.getElementById("modalPassoEnergia").style.display = "none";
  document.getElementById("modalPassoNome").style.display = "none";
  document.getElementById("modalTipoLabel").textContent = tipos.label + ":";
  var box = document.getElementById("modalTipoOpcoes");
  box.innerHTML = "";
  tipos.opcoes.forEach(function(op) {
    var b = document.createElement("button");
    b.className = "btn btn-full";
    b.textContent = op;
    b.onclick = function(){ _modalDado.tipo = op; montarPassoEnergia(produto, lang); };
    box.appendChild(b);
  });
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
function fecharModalDado() {
  var o = document.getElementById("modalDado");
  if (o) o.classList.remove("active");
}
function confirmarModalDado(produto, lang) {
  var dado = document.getElementById("modalDadoInput").value.trim();
  if (!dado) {
    alert((translations[lang] || translations.pt).preencha_dado || "Preencha o dado solicitado.");
    return;
  }
  var tipo = _modalDado.tipo || "";
  var energia = _modalDado.energia || "";
  fecharModalDado();
  window.location.href = '/criar-checkout?lang=' + lang + '&produto=' + produto
    + '&dado=' + encodeURIComponent(dado)
    + '&tipo=' + encodeURIComponent(tipo)
    + '&energia=' + encodeURIComponent(energia);
}

// ===== ENERGIAS (abre menu de produtos da energia) =====
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
    b.onclick = function(){ fecharMenuEnergia(); comprar(prod); };
    lista.appendChild(b);
  });
  overlay.classList.add("active");
}
function fecharMenuEnergia() {
  var o = document.getElementById("menuEnergia");
  if (o) o.classList.remove("active");
}

// ===== BÔNUS COLETIVO / EMPRESARIAL (23 produtos) =====
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

// ===== INICIALIZAÇÃO =====
function init() {
  var savedLang = localStorage.getItem('lang');
  var browserLang = navigator.language.split('-')[0];
  var defaultLang = savedLang || (translations[browserLang] ? browserLang : 'pt');
  montarSeletorIdioma();
  setLanguage(defaultLang);
  montarTabelaBC();
  atualizarResumoBC();
  montarEnergias();
  traduzirTudo();
}
