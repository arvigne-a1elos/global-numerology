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

  // ===== NOVO: re-renderiza a calculadora no idioma trocado =====
  if (typeof renderizarNumeros === "function") renderizarNumeros();
  if (typeof montarEnergias === "function") montarEnergias();
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
// ============================================================
// FORMULÁRIOS DE COLETA — 8 produtos novos (usa as chaves do translations.js)
// ============================================================
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
  var t = translations[getLang()] || translations.pt;
  return t[chave] || OPCOES_FALLBACK[chave] || chave;
}

var CONF_COLETA = {
  nome_canal:   { labelTipo:"f_tipo_canal",   tipos:["youtube","podcast","tiktok","twitch"],             temArea:true,  areas:["esporte","noticias","politica","beleza"], temDetalhe:false },
  nickname:     { labelTipo:"f_tipo_nickname", tipos:["gamer","profissional","criador","artista"],       temArea:false, areas:[], temDetalhe:false },
  nome_ong:     { labelTipo:"f_tipo_ong",      tipos:["ong","instituto","associacao","fundacao"],        temArea:false, areas:[], temDetalhe:false },
  nome_evento:  { labelTipo:"f_tipo_evento",   tipos:["show","congresso","festa","curso","palestra"],    temArea:true,  areas:["musica","esporte","cultura","politica","beleza"], temDetalhe:false },
  nome_projeto: { labelTipo:"f_tipo_projeto",  tipos:["pessoal","social","empresarial","cultural"],      temArea:false, areas:[], temDetalhe:false },
  nome_equipe:  { labelTipo:"f_tipo_equipe",   tipos:["empresarial","projeto","esportiva","banda"],      temArea:false, areas:[], temDetalhe:false },
  nome_dominio: { labelTipo:"f_tipo_site",     tipos:["loja","empresa","blog","portfolio"],              temArea:true,  areas:["comercio","industria","servicos","pessoal"], temDetalhe:false },
  nome_pet:     { labelTipo:"f_tipo_pet",      tipos:["cao","gato","passaro","reptil"],                  temArea:false, areas:[], temDetalhe:true }
};

var coletaAtual = null;

// ===== PESQUISAR (substitua a função antiga por esta) =====
function pesquisar(produto) {
  // 1) Express e Completo → calculadora (confirmado)
  if (produto === "express" || produto === "completo") {
    var sec = document.getElementById("calculadora") || document.getElementById("calcSection");
    if (sec) sec.scrollIntoView({ behavior:"smooth", block:"center" });
    return;
  }
  // 2) 8 produtos novos → modal de coleta
  if (CONF_COLETA[produto]) { abrirModalColeta(produto); return; }
  // 3) Demais produtos → rolar até o formulário próprio (se existir)
  var alvo = document.getElementById("form-" + produto);
  if (alvo) {
    alvo.scrollIntoView({ behavior:"smooth", block:"center" });
    alvo.style.transition = "box-shadow .5s";
    alvo.style.boxShadow = "0 0 0 3px var(--gold)";
    setTimeout(function(){ alvo.style.boxShadow = ""; }, 2000);
    return;
  }
  // fallback → calculadora
  var calc = document.getElementById("calculadora") || document.getElementById("calcSection");
  if (calc) calc.scrollIntoView({ behavior:"smooth" });
}

// ===== Abrir o modal de coleta com os dados do produto =====
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

function selecionarOpcao(container, btn) {
  container.querySelectorAll(".coleta-opcao").forEach(function(b){ b.classList.remove("ativo"); });
  btn.classList.add("ativo");
}

function montarGradeEnergia(idContainer) {
  var c = document.getElementById(idContainer);
  if (!c) return;
  c.innerHTML = "";
  for (var i = 1; i <= 9; i++) {
    (function(n){
      var b = document.createElement("button");
      b.type = "button"; b.className = "btn btn-outline energia-num";
      b.textContent = String(n);
      b.onclick = function(){
        c.querySelectorAll(".energia-num").forEach(function(x){ x.classList.remove("ativo"); });
        b.classList.add("ativo");
      };
      c.appendChild(b);
    })(i);
  }
}

function fecharModalColeta() {
  var o = document.getElementById("modalColeta");
  if (o) o.style.display = "none";
  coletaAtual = null;
}

// ===== Confirmar: coleta os dados e vai para o checkout (Stripe) =====
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

// ===== Ligar os botões do modal (rodar uma vez, ao final) =====
document.addEventListener("DOMContentLoaded", function(){
  var f = document.getElementById("coletaFechar");   if (f) f.onclick = fecharModalColeta;
  var c = document.getElementById("coletaCancelar"); if (c) c.onclick = fecharModalColeta;
  var ok = document.getElementById("coletaConfirmar"); if (ok) ok.onclick = confirmarColeta;
  var ov = document.getElementById("modalColeta");
  if (ov) ov.addEventListener("click", function(e){ if (e.target === ov) fecharModalColeta(); });
});

// Produtos que estão na lista das energias (abrem o seletor de energia)
var PRODUTO_ENERGIA = ["vida","ia","imovel","calendario","artistico","bebe","assinatura","negocio","casal","familia"];

function pesquisar(produto) {
  var lang = getLang();

  // 1) 8 produtos novos → modal de dado específico (já existe)
  if (DADO_APLICA.indexOf(produto) !== -1) {
    abrirModalDado(produto, lang);
    return;
  }

  // 2) Produtos que estão nas energias → abre o seletor de energia
  if (PRODUTO_ENERGIA.indexOf(produto) !== -1) {
    abrirSeletorEnergia(produto, lang);
    return;
  }

  // 3) Demais → rola até o formulário específico do produto
  var target = PESQUISA_TARGET[produto] || "calculadora";
  var el = document.getElementById(target);
  if (el) {
    el.scrollIntoView({ behavior: "smooth", block: "center" });
    el.style.transition = "box-shadow 0.5s";
    el.style.boxShadow = "0 0 0 3px var(--gold)";
    setTimeout(function(){ el.style.boxShadow = ""; }, 2000);
  }
}

// ===== SELETOR DE ENERGIA (para produtos da lista de energias) =====
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
    b.onclick = function(){ fecharMenuEnergia(); pesquisar(prod); };
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

// ===== BÔNUS COLETIVO / EMPRESARIAL (funções resgatadas) =====
var BC_QUANTIDADES = {};

function montarTabelaBC() {
  var corpo = document.getElementById("bcTabelaCorpo");
  if (!corpo) return;
  corpo.innerHTML = "";
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

function descontoBC(qtd) {
  if (qtd >= 2000) return 50;
  if (qtd >= 1000) return 45;
  if (qtd >= 500) return 40;
  if (qtd >= 200) return 30;
  if (qtd >= 100) return 25;
  if (qtd >= 50) return 20;
  if (qtd >= 10) return 10;
  return 0;
}

function usarPlanoPronto(qExpress, qVida, qIa, qCompleto) {
  var mapa = { express: qExpress, vida: qVida, ia: qIa, completo: qCompleto };
  document.querySelectorAll("#bcTabelaCorpo input[data-prod]").forEach(function(inp) {
    var prod = inp.getAttribute("data-prod");
    inp.value = mapa[prod] || 0;
  });
  atualizarResumoBC();
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
// ===== CALCULADORA GRATUITA (5 números) =====
function r1Num(n) {
  while (n > 9 && n !== 11 && n !== 22 && n !== 33) {
    n = String(n).split('').reduce(function(a, d) { return a + parseInt(d, 10); }, 0);
  }
  return n;
}

function calcular5Numeros(nome, nasc) {
  var t = {};
  var letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  for (var i = 0; i < letras.length; i++) { t[letras[i]] = (i % 9 || 9); }
  var parts = nasc.split('-');
  var lp = r1Num(parseInt(parts[0], 10) + parseInt(parts[1], 10) + parseInt(parts[2], 10));
  var nu = nome.toUpperCase().replace(/[^A-Z]/g, '');
  var te = 0, tv = 0, tp = 0;
  for (var j = 0; j < nu.length; j++) {
    var ch = nu[j];
    var val = t[ch] || 0;
    te += val;
    if ("AEIOU".indexOf(ch) >= 0) { tv += val; } else { tp += val; }
  }
  return [lp, r1Num(te), r1Num(tv), r1Num(tp), r1Num(r1Num(te) + lp)];
}

var ultimosNumeros = null;

function calcularMapa() {
  var lang = getLang();
  var t = translations[lang] || translations["pt"];
  var nome = (document.getElementById("calcNome") ? document.getElementById("calcNome").value : "").trim();
  var nasc = (document.getElementById("calcNasc") ? document.getElementById("calcNasc").value : "").trim();
  if (!nome || !nasc) {
    alert(t.preencha_dados || "Preencha nome e data de nascimento primeiro.");
    var sec = document.getElementById("calcSection") || document.getElementById("calculadora");
    if (sec) sec.scrollIntoView({ behavior: "smooth" });
    return;
  }
  if (typeof calcular5Numeros === "function") { ultimosNumeros = calcular5Numeros(nome, nasc); }
  else { ultimosNumeros = [1, 2, 3, 4, 5]; }
  renderizarNumeros();
}

function renderizarNumeros() {
  if (!ultimosNumeros) return;
  var lang = getLang();
  var t = translations[lang] || translations["pt"];
  var nomes = t.nomes5 || {};
  var chaves5 = ['caminho', 'realizacao', 'alma', 'personalidade', 'destino'];
  var html = "";
  for (var i = 0; i < ultimosNumeros.length && i < chaves5.length; i++) {
    var n = ultimosNumeros[i];
    var nomeE = nomes[chaves5[i]] || ("Energia " + n);
    html += '<div class="numero-gratis"><span class="numero-nome">' + nomeE + ':</span> <span class="numero-valor">' + n + '</span></div>';
  }
  var el = document.getElementById("resultadoNumeros") || document.getElementById("resultado") || document.getElementById("calcResultado");
  if (el) { el.innerHTML = html; el.style.display = "block"; }
  var box = document.getElementById("resultadoBox") || el;
  if (box) box.style.display = "block";
}

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
document.addEventListener('DOMContentLoaded', init);
