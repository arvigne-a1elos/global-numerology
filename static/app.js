// ===== A1ELOS GLOBAL NUMEROLOGY - APP.JS (VERSÃO CONSOLIDADA) =====
// ================================================================
// ===== MONTAR SELETOR DE IDIOMAS (14 bandeiras) =====
// GUARDA ANTI-REENTRÂNCIA (adicione no topo do arquivo)
let _cicloEmExecucao = false;

function iniciarCiclo() {
    if (_cicloEmExecucao) return false;   // se já está rodando, ignora
    _cicloEmExecucao = true;
    return true;
}
function finalizarCiclo() {
    _cicloEmExecucao = false;
}

function montarSeletorIdioma() {
  var container = document.getElementById('langSelector');
  if (!container) {
    container = document.createElement('div');
    container.id = 'langSelector';
    document.body.insertBefore(container, document.body.firstChild);
  }
  if (container.children.length > 0) return;
  var lista = [
    {id:'pt'},{id:'en'},{id:'es'},{id:'it'},{id:'fr'},{id:'de'},{id:'ja'},{id:'zh'},
    {id:'ru'},{id:'id'},{id:'tr'},{id:'vi'},{id:'he'},{id:'ar'}
  ];
  var atual = (typeof getLang === 'function') ? getLang() : 'pt';
  lista.forEach(function(l) {
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'lang-btn' + (l.id === atual ? ' active' : '');
    b.title = l.id.toUpperCase();
    b.textContent = l.id.toUpperCase();
    b.onclick = function() {
      if (typeof setLanguage === 'function') setLanguage(l.id);
      var ativos = container.querySelectorAll('.lang-btn');
      for (var i = 0; i < ativos.length; i++) ativos[i].classList.remove('active');
      b.classList.add('active');
      if (typeof montarTudo === 'function') montarTudo();
      else if (typeof traduzirTudo === 'function') traduzirTudo();
    };
    container.appendChild(b);
  });
}
function _energiaSelecionada(idSel, produto) {
  var sel = document.getElementById(idSel);
  if (sel) {
    var ativo = sel.querySelector('.energia-btn.selecionada, .energia-btn.ativo');
    if (ativo) return ativo.textContent.trim();
  }
  var ideal = (typeof ENERGIA_IDEAL !== 'undefined' && ENERGIA_IDEAL[produto]) ? ENERGIA_IDEAL[produto] : '';
  return ideal ? String(ideal) : '';
}
function pagarVida(){var n=document.getElementById('vidaNome').value.trim(),b=converterData(document.getElementById('vidaNasc').value);if(!n||!b){alert(t_preencha());return;}location.href='/criar-checkout?produto=vida&nome='+encodeURIComponent(n)+'&nascimento='+encodeURIComponent(b)+'&lang='+getLang();}
function pagarIa(){
  var n = (document.getElementById('iaNome') ? document.getElementById('iaNome').value : '').trim();
  if (!n) { alert(t_preencha()); return; }
  location.href = '/criar-checkout?produto=ia&nome=' + encodeURIComponent(n)
    + '&energia=' + encodeURIComponent(_energiaSelecionada('iaEnergiaSel', 'ia')) + '&lang=' + getLang();
}

// ===== NÚMERO DO IMÓVEL — 3 campos, validação silenciosa (sem alert) =====
function _imovelPegaVisivel(ids){
  for (var j = 0; j < ids.length; j++){
    var todos = document.querySelectorAll('[id="' + ids[j] + '"]');
    for (var i = 0; i < todos.length; i++){
      if (todos[i].getClientRects().length > 0) return todos[i];
    }
  }
  for (var k = 0; k < ids.length; k++){
    var e = document.getElementById(ids[k]);
    if (e) return e;
  }
  return null;
}

function pagarImovel(){
  var n   = _imovelPegaVisivel(['imovelNumero']),
      ne  = _imovelPegaVisivel(['imovelNomeEntrega']),
      ap  = _imovelPegaVisivel(['imovelApto']),
      sal = _imovelPegaVisivel(['imovelSala']),
      aviso = _imovelPegaVisivel(['imovelAviso']);
  var vn   = n   ? n.value.trim()   : '';
  var vap  = ap  ? ap.value.trim()  : '';
  var vsal = sal ? sal.value.trim() : '';
  var vne  = ne ? ne.value.trim() : '';  
  // PDF liberado com 1 dado só (casa sozinha é suficiente)
  if (!vn && !vap && !vsal){
    if (aviso) aviso.style.display = 'block';
    return;
  }
  if (aviso) aviso.style.display = 'none';
  location.href = '/criar-checkout?produto=imovel'
    + '&dado='  + encodeURIComponent(vn)
    + '&dado2=' + encodeURIComponent(vap)
    + '&dado3=' + encodeURIComponent(vsal)
    + '&apelido=' + encodeURIComponent(vne)  
    + '&lang='  + getLang();
}

function _calMesNum(v){
  v = String(v || '').trim();
  if (/^\d{1,2}$/.test(v)) return parseInt(v, 10);
  var s = v.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  var nomes = {
    janeiro:1, january:1, enero:1, gennaio:1, janvier:1, januar:1,
    fevereiro:2, february:2, febrero:2, febbraio:2, fevrier:2, februar:2,
    marco:3, march:3, marzo:3, mars:3, marz:3,
    abril:4, april:4, aprile:4, avril:4,
    maio:5, may:5, mayo:5, maggio:5, mai:5,
    junho:6, june:6, junio:6, giugno:6, juin:6,
    julho:7, july:7, julio:7, luglio:7,
    agosto:8, august:8,
    setembro:9, september:9, septiembre:9, settembre:9, septembre:9,
    outubro:10, october:10, octubre:10, ottobre:10, octobre:10, oktober:10,
    novembro:11, november:11, noviembre:11, novembre:11,
    dezembro:12, december:12, diciembre:12, dicembre:12, decembre:12, dezember:12
  };
  return nomes[s] || 0;
}
function pagarCalendario(){
  var elN = _calPegaVisivel(['calNome']);
  var elB = _calPegaVisivel(['calNascimento']);
  var elA = _calPegaVisivel(['calAno']);
  var elM = _calPegaVisivel(['calMes']);
  if(!elN || !elM){
    alert("Formulário do calendário não encontrado. Recarregue a página (Ctrl+Shift+R) e tente novamente.");
    return;
  }
  var n = elN.value.trim();
  var b = elB ? elB.value : "";
  var a = elA ? elA.value : "";
  var m = elM.value;
  if(!n || !b || !a || !m){
    var msg = (typeof t_preencha === 'function') ? t_preencha() : "Preencha nome, data, ano e mês antes de pesquisar.";
    alert(msg);
    return;
  }
  var mes = a + "-" + (m.length === 1 ? "0" + m : m);
  window.location.href = '/criar-checkout?produto=calendario'
    + '&nome=' + encodeURIComponent(n)
    + '&nascimento=' + encodeURIComponent(converterData(b))
    + '&dado=' + encodeURIComponent(mes)
    + '&lang=' + getLang();
}
function pagarBebe(){
  var n = (document.getElementById('bebeSobrenome') ? document.getElementById('bebeSobrenome').value : '').trim();
  if (!n) { alert(t_preencha()); return; }
  location.href = '/criar-checkout?produto=bebe&dado=' + encodeURIComponent(n)
    + '&energia=' + encodeURIComponent(_energiaSelecionada('bebeEnergiaSel', 'bebe')) + '&lang=' + getLang();
}
function pagarAssinatura(){
  var n = (document.getElementById('assinaturaTexto') ? document.getElementById('assinaturaTexto').value : '').trim();
  if (!n) { alert(t_preencha()); return; }
  location.href = '/criar-checkout?produto=assinatura&dado=' + encodeURIComponent(n)
    + '&energia=' + encodeURIComponent(_energiaSelecionada('assinaturaEnergiaSel', 'assinatura')) + '&lang=' + getLang();
}
function pagarNegocio(){
  var n = (document.getElementById('negocioNome') ? document.getElementById('negocioNome').value : '').trim();
  if (!n) { alert(t_preencha()); return; }
  location.href = '/criar-checkout?produto=negocio&dado=' + encodeURIComponent(n)
    + '&energia=' + encodeURIComponent(_energiaSelecionada('negocioEnergiaSel', 'negocio')) + '&lang=' + getLang();
}

function pagarCasal(){
  var lang = getLang();
  var t = translations[lang] || translations.pt;
  var e1 = document.getElementById('casalNome1'), e2 = document.getElementById('casalNome2');
  var s1 = document.getElementById('casalNasc1'), s2 = document.getElementById('casalNasc2');
  var n1 = e1 ? e1.value.trim() : '', n2 = e2 ? e2.value.trim() : '';
  var d1 = s1 ? converterData(s1.value.trim()) : '', d2 = s2 ? converterData(s2.value.trim()) : '';
  if (!n1 || !n2 || !d1 || !d2) { alert(t.preencha_dado || 'Preencha os dados solicitados.'); return; }
  location.href = '/criar-checkout?produto=casal'
    + '&nome=' + encodeURIComponent(n1)
    + '&nascimento=' + encodeURIComponent(d1)
    + '&dado=' + encodeURIComponent(n1 + '|' + n2)
    + '&detalhe=' + encodeURIComponent(d1 + '|' + d2)
    + '&lang=' + encodeURIComponent(lang);
}

// ===== FAMÍLIA: principal + até 4 membros =====
function _coletarPares(prefixoP, prefixoM, qtdMax) {
  function _val(id) {
    var el = document.getElementById(id);
    return el ? String(el.value || '').trim() : '';
  }
  function _apelido(id) {
    return _val(id).replace(/[;|]/g, '').trim();
  }
  function _data(id) {
    var v = _val(id);
    return (v && typeof converterData === 'function') ? converterData(v) : v;
  }

  var principal = {
    nome: _val(prefixoP + 'Nome'),
    apelido: _apelido(prefixoP + 'Apelido'),
    nasc: _data(prefixoP + 'Nasc')
  };
  if (!principal.nome || !principal.nasc) return { erro: 'principal' };

  var membros = [];
  for (var i = 1; i <= qtdMax; i++) {
    var vn = _val(prefixoM + 'Nome' + i);
    var vd = _data(prefixoM + 'Nasc' + i);
    var va = _apelido(prefixoM + 'Apelido' + i);
    if (!vn && !vd && !va) continue;
    if (!vn || !vd) return { erro: 'incompleto', idx: i };
    membros.push({ nome: vn, apelido: va, nasc: vd });
  }
  return { principal: principal, membros: membros };
}

function _detalheComApelido(r) {
  return [r.principal].concat(r.membros).map(function (m) {
    return m.apelido ? (m.nasc + ';' + m.apelido) : m.nasc;
  }).join('|');
}

function pagarFamilia(){
  var lang = getLang();
  var t = translations[lang] || translations.pt;
  var r = _coletarPares('familiaPrincipal', 'familiaMembro', 2);
  if (r.erro === 'principal' || r.erro === 'incompleto' || !r.membros.length) {
    alert(t.preencha_dado || 'Preencha os dados solicitados.');
    return;
  }
  var dado = [r.principal.nome].concat(r.membros.map(function(m){ return m.nome; })).join('|');
  var det  = _detalheComApelido(r);
    + '&nome=' + encodeURIComponent(r.principal.nome)
    + '&nascimento=' + encodeURIComponent(r.principal.nasc)
    + '&dado=' + encodeURIComponent(dado)
    + '&detalhe=' + encodeURIComponent(det)
    + '&lang=' + encodeURIComponent(lang);
}

function pagarCompatibilidade(){
  var lang = getLang();
  var t = translations[lang] || translations.pt;
  var r = _coletarPares('equipePrincipal', 'equipeMembro', 2);
  if (r.erro === 'principal' || r.erro === 'incompleto' || !r.membros.length) {
    alert(t.preencha_dado || 'Preencha os dados solicitados.');
    return;
  }
  var dado = [r.principal.nome].concat(r.membros.map(function(m){ return m.nome; })).join('|');
  var det  = _detalheComApelido(r);
  location.href = '/criar-checkout?produto=compatibilidade_equipes'
    + '&nome=' + encodeURIComponent(r.principal.nome)
    + '&nascimento=' + encodeURIComponent(r.principal.nasc)
    + '&dado=' + encodeURIComponent(dado)
    + '&detalhe=' + encodeURIComponent(det)
    + '&energia=' + encodeURIComponent(energia)
    + '&lang=' + encodeURIComponent(lang);
}

function t_preencha(){var t=translations[getLang()]||translations.pt;return t.preencha_dado||'Preencha os dados solicitados.';}
window.pagarUrna = window.pagarUrna || function(){
  var nomeCompleto = (document.getElementById('urnaNome') ? document.getElementById('urnaNome').value : '').trim();
  var cargo = (document.getElementById('urnaCargo') ? document.getElementById('urnaCargo').value : '').trim();
  var n1 = (document.getElementById('urnaNome1') ? document.getElementById('urnaNome1').value : '').trim();
  var n2 = (document.getElementById('urnaNome2') ? document.getElementById('urnaNome2').value : '').trim();
  var n3 = (document.getElementById('urnaNome3') ? document.getElementById('urnaNome3').value : '').trim();
  var n4 = (document.getElementById('urnaNome4') ? document.getElementById('urnaNome4').value : '').trim();
  var n5 = (document.getElementById('urnaNome5') ? document.getElementById('urnaNome5').value : '').trim();
  if (!nomeCompleto || (!n1 && !n2 && !n3 && !n4 && !n5)) { alert(t_preencha()); return; }
  location.href = '/criar-checkout?produto=urna&nome_completo=' + encodeURIComponent(nomeCompleto)
    + '&cargo=' + encodeURIComponent(cargo)
    + '&nome1=' + encodeURIComponent(n1) + '&nome2=' + encodeURIComponent(n2)
    + '&nome3=' + encodeURIComponent(n3) + '&nome4=' + encodeURIComponent(n4)
    + '&nome5=' + encodeURIComponent(n5) + '&lang=' + getLang();
};
window.pagarEleitoral = window.pagarEleitoral || function(){
  var existente = (document.getElementById('eleiExistente') ? document.getElementById('eleiExistente').value : '').trim();
  var nome = (document.getElementById('eleiNome') ? document.getElementById('eleiNome').value : '').trim();
  var cargo = (document.getElementById('eleiCargo') ? document.getElementById('eleiCargo').value : '').trim();
  var sigla = (document.getElementById('eleiSigla') ? document.getElementById('eleiSigla').value : '').trim();
  if (!nome || !sigla) { alert(t_preencha()); return; }
  location.href = '/criar-checkout?produto=eleitoral&nome_completo=' + encodeURIComponent(nome)
    + '&numero_existente=' + encodeURIComponent(existente)
    + '&cargo=' + encodeURIComponent(cargo)
    + '&numero=' + encodeURIComponent(sigla)
    + '&lang=' + getLang();
};
window.pagarArte = window.pagarArte || function(){
  var nome = (document.getElementById('arteNome') ? document.getElementById('arteNome').value : '').trim();
  var n1 = (document.getElementById('arteNome1') ? document.getElementById('arteNome1').value : '').trim();
  var n2 = (document.getElementById('arteNome2') ? document.getElementById('arteNome2').value : '').trim();
  var n3 = (document.getElementById('arteNome3') ? document.getElementById('arteNome3').value : '').trim();
  var n4 = (document.getElementById('arteNome4') ? document.getElementById('arteNome4').value : '').trim();
  var n5 = (document.getElementById('arteNome5') ? document.getElementById('arteNome5').value : '').trim();
  if (!nome || (!n1 && !n2 && !n3 && !n4 && !n5)) { alert(t_preencha()); return; }
  var energia = _energiaSelecionada('arteEnergiaSel', 'artistico');
  location.href = '/criar-checkout?produto=artistico'
    + '&nome_completo=' + encodeURIComponent(nome)
    + '&nome=' + encodeURIComponent(nome)
    + '&nome1=' + encodeURIComponent(n1) + '&nome2=' + encodeURIComponent(n2)
    + '&nome3=' + encodeURIComponent(n3) + '&nome4=' + encodeURIComponent(n4)
    + '&nome5=' + encodeURIComponent(n5)
    + (energia ? '&energia=' + encodeURIComponent(energia) : '')
    + '&lang=' + getLang();
};
window.pagarOng = window.pagarOng || function(){
  var n1 = (document.getElementById('ongNome1') ? document.getElementById('ongNome1').value : '').trim();
  var n2 = (document.getElementById('ongNome2') ? document.getElementById('ongNome2').value : '').trim();
  var n3 = (document.getElementById('ongNome3') ? document.getElementById('ongNome3').value : '').trim();
  if (!n1 && !n2 && !n3) { alert(t_preencha()); return; }
  var natureza = (document.getElementById('ongNatureza') ? document.getElementById('ongNatureza').value : 'ong');
  var tipo = (document.getElementById('ongTipo') ? document.getElementById('ongTipo').value : '');
  var escopo = (document.getElementById('ongEscopo') ? document.getElementById('ongEscopo').value : 'nacional');
  var s1 = (document.getElementById('ongSigla1') ? document.getElementById('ongSigla1').value : '').trim();
  var s2 = (document.getElementById('ongSigla2') ? document.getElementById('ongSigla2').value : '').trim();
  var s3 = (document.getElementById('ongSigla3') ? document.getElementById('ongSigla3').value : '').trim();
  var energia = _energiaSelecionada('ongEnergiaSel', 'nome_ong');
  var qs = '/criar-checkout?produto=nome_ong'
    + '&nome1=' + encodeURIComponent(n1) + '&sigla1=' + encodeURIComponent(s1)
    + '&nome2=' + encodeURIComponent(n2) + '&sigla2=' + encodeURIComponent(s2)
    + '&nome3=' + encodeURIComponent(n3) + '&sigla3=' + encodeURIComponent(s3)
    + '&natureza=' + encodeURIComponent(natureza)
    + '&tipo_entidade=' + encodeURIComponent(tipo)
    + '&escopo=' + encodeURIComponent(escopo)
    + (energia ? '&energia=' + encodeURIComponent(energia) : '')
    + '&lang=' + getLang();
  window.location.href = qs;
};

// ===== LISTAS DE COLETA (globais — fora da função) =====
window.DADO_APLICA = window.DADO_APLICA || ["nome_pet","nickname","nome_dominio","nome_canal","nome_equipe","nome_projeto","nome_evento"];

window.DADO_LABEL = window.DADO_LABEL || {
  pt: { nome_pet:"Nome do pet", nickname:"Seu nickname ou usuário", nome_dominio:"Nome do domínio (ex.: meusite.com)", nome_canal:"Nome do canal", nome_equipe:"Nome da equipe", nome_projeto:"Nome do projeto", nome_evento:"Nome do evento" },
  en: { nome_pet:"Pet's name", nickname:"Your nickname or handle", nome_dominio:"Domain name (e.g.: mysite.com)", nome_canal:"Channel name", nome_equipe:"Team name", nome_projeto:"Project name", nome_evento:"Event name" }
};

window.CONF_COLETA = window.CONF_COLETA || {
  nome_pet:     { tipos:["cao","gato","passaro","outro"], sexos:true },
  nickname:     { tipos:["pessoal","profissional","artistico"], sexos:true },
  nome_dominio: { tipos:["empresa","pessoal","loja","blog"] },
  nome_canal:   { tipos:["youtube","podcast","instagram","tiktok"] },
  nome_equipe:  { tipos:["esportiva","corporativa","criativa"] },
  nome_projeto: { tipos:["digital","social","comercial"] },
  nome_evento:  { tipos:["congresso","curso","festa","palestra"] },
  nome_pet: { tipos:["cao","gato","passaro","outro"], sexos:["femea","macho"] }  
};

/* ===== IA NOMES — RÓTULOS EM 14 IDIOMAS ===== */
window.IA_NOMES_UI = window.IA_NOMES_UI || {
  pt: {n1:"Nome 1",n2:"Nome 2",n3:"Nome 3",energia:"Energia desejada",tipo:"Tipo",dica:"Informe até 3 nomes. Se nenhum atingir a energia escolhida, a IA sugere 1 nome com essa energia (4ª opção).",sugerido:"Sugestão da IA",escolhido:"Nome escolhido",energia_alvo:"Energia alvo",nenhum:"Nenhum nome atingiu a energia.", sexo:"Sexo do animal", femea:"Fêmea", macho:"Macho", indef:"Não sei / indefinido",},
  en: {n1:"Name 1",n2:"Name 2",n3:"Name 3",energia:"Desired energy",tipo:"Type",dica:"Enter up to 3 names. If none reaches the chosen energy, the AI suggests 1 name with that energy (4th option).",sugerido:"AI suggestion",escolhido:"Chosen name",energia_alvo:"Target energy",nenhum:"No name reached the energy.", sexo:"Animal's sex", femea:"Female", macho:"Male", indef:"Unknown",},
  es: {n1:"Nombre 1",n2:"Nombre 2",n3:"Nombre 3",energia:"Energía deseada",tipo:"Tipo",dica:"Informe hasta 3 nombres. Si ninguno alcanza la energía elegida, la IA sugiere 1 nombre con esa energía (4ª opción).",sugerido:"Sugerencia de la IA",escolhido:"Nombre elegido",energia_alvo:"Energía objetivo",nenhum:"Ningún nombre alcanzó la energía.", sexo:"Sexo del animal", femea:"Hembra", macho:"Macho", indef:"No sé",},
  it: {n1:"Nome 1",n2:"Nome 2",n3:"Nome 3",energia:"Energia desiderata",tipo:"Tipo",dica:"Inserisci fino a 3 nomi. Se nessuno raggiunge l'energia scelta, l'IA suggerisce 1 nome con quell'energia (4ª opzione).",sugerido:"Suggerimento IA",escolhido:"Nome scelto",energia_alvo:"Energia obiettivo",nenhum:"Nessun nome ha raggiunto l'energia.", sexo:"Sesso dell'animale", femea:"Femmina", macho:"Maschio", indef:"Non so",},
  fr: {n1:"Nom 1",n2:"Nom 2",n3:"Nom 3",energia:"Énergie souhaitée",tipo:"Type",dica:"Saisissez jusqu'à 3 noms. Si aucun n'atteint l'énergie choisie, l'IA suggère 1 nom avec cette énergie (4e option).",sugerido:"Suggestion IA",escolhido:"Nom choisi",energia_alvo:"Énergie cible",nenhum:"Aucun nom n'a atteint l'énergie.", sexo:"Sexe de l'animal", femea:"Femelle", macho:"Mâle", indef:"Inconnu",},
  de: {n1:"Name 1",n2:"Name 2",n3:"Name 3",energia:"Gewünschte Energie",tipo:"Typ",dica:"Geben Sie bis zu 3 Namen ein. Wenn keiner die gewählte Energie erreicht, schlägt die KI 1 Namen mit dieser Energie vor (4. Option).",sugerido:"KI-Vorschlag",escolhido:"Gewählter Name",energia_alvo:"Zielenergie",nenhum:"Kein Name erreichte die Energie.", sexo:"Geschlecht", femea:"Weibchen", macho:"Männchen", indef:"Unbekannt",},
  ja: {n1:"名前1",n2:"名前2",n3:"名前3",energia:"希望するエネルギー",tipo:"タイプ",dica:"最大3つの名前を入力してください。どれも選択したエネルギーに達しない場合、AIがそのエネルギーの名前を1つ提案します（4番目の選択肢）。",sugerido:"AIの提案",escolhido:"選ばれた名前",energia_alvo:"目標エネルギー",nenhum:"エネルギーに達した名前はありません。", sexo:"性別", femea:"メス", macho:"オス", indef:"不明",},
  zh: {n1:"名字1",n2:"名字2",n3:"名字3",energia:"所需能量",tipo:"类型",dica:"最多输入3个名字。如果没有一个达到所选能量，AI会建议1个具有该能量的名字（第4个选项）。",sugerido:"AI建议",escolhido:"选定的名字",energia_alvo:"目标能量",nenhum:"没有名字达到该能量。", sexo:"性别", femea:"母", macho:"公", indef:"未知",},
  ru: {n1:"Имя 1",n2:"Имя 2",n3:"Имя 3",energia:"Желаемая энергия",tipo:"Тип",dica:"Введите до 3 имён. Если ни одно не достигает выбранной энергии, ИИ предложит 1 имя с этой энергией (4-й вариант).",sugerido:"Предложение ИИ",escolhido:"Выбранное имя",energia_alvo:"Целевая энергия",nenhum:"Ни одно имя не достигло энергии.", sexo:"Пол", femea:"Самка", macho:"Самец", indef:"Неизвестно",},
  id: {n1:"Nama 1",n2:"Nama 2",n3:"Nama 3",energia:"Energi yang diinginkan",tipo:"Jenis",dica:"Masukkan hingga 3 nama. Jika tidak ada yang mencapai energi yang dipilih, AI menyarankan 1 nama dengan energi tersebut (opsi ke-4).",sugerido:"Saran AI",escolhido:"Nama terpilih",energia_alvo:"Energi target",nenhum:"Tidak ada nama yang mencapai energi.", sexo:"Jenis kelamin", femea:"Betina", macho:"Jantan", indef:"Tidak tahu",},
  tr: {n1:"İsim 1",n2:"İsim 2",n3:"İsim 3",energia:"İstenen enerji",tipo:"Tür",dica:"En fazla 3 isim girin. Hiçbiri seçilen enerjiye ulaşmazsa, yapay zekâ o enerjiye sahip 1 isim önerir (4. seçenek).",sugerido:"AI önerisi",escolhido:"Seçilen isim",energia_alvo:"Hedef enerji",nenhum:"Hiçbir isim enerjiye ulaşmadı.", sexo:"Cinsiyet", femea:"Dişi", macho:"Erkek", indef:"Bilinmiyor",},
  vi: {n1:"Tên 1",n2:"Tên 2",n3:"Tên 3",energia:"Năng lượng mong muốn",tipo:"Loại",dica:"Nhập tối đa 3 tên. Nếu không tên nào đạt năng lượng đã chọn, AI sẽ gợi ý 1 tên với năng lượng đó (lựa chọn thứ 4).",sugerido:"Gợi ý AI",escolhido:"Tên được chọn",energia_alvo:"Năng lượng mục tiêu",nenhum:"Không tên nào đạt năng lượng.", sexo:"Giới tính", femea:"Cái", macho:"Đực", indef:"Không rõ",},
  he: {n1:"שם 1",n2:"שם 2",n3:"שם 3",energia:"אנרגיה רצויה",tipo:"סוג",dica:"הזינו עד 3 שמות. אם אף אחד לא מגיע לאנרגיה שנבחרה, ה-AI יציע שם אחד עם האנרגיה הזו (אפשרות רביעית).",sugerido:"הצעת AI",escolhido:"השם הנבחר",energia_alvo:"אנרגיית יעד",nenhum:"אף שם לא הגיע לאנרגיה.", sexo:"מין", femea:"נקבה", macho:"זכר", indef:"לא ידוע",},
  ar: {n1:"الاسم 1",n2:"الاسم 2",n3:"الاسم 3",energia:"الطاقة المطلوبة",tipo:"النوع",dica:"أدخل حتى 3 أسماء. إذا لم يصل أي منها إلى الطاقة المختارة، سيقترح الذكاء الاصطناعي اسمًا واحدًا بهذه الطاقة (الخيار الرابع).",sugerido:"اقتراح الذكاء الاصطناعي",escolhido:"الاسم المختار",energia_alvo:"الطاقة المستهدفة",nenhum:"لم يصل أي اسم إلى الطاقة.", sexo:"الجنس", femea:"أنثى", macho:"ذكر", indef:"غير محدد",}
};

window.IA_ROMAN = {
  pt: "Os nomes são analisados em escrita latina porque a numerologia pitagórica atribui valor apenas às 26 letras A–Z. Nomes em outros alfabetos são romanizados antes do cálculo (ex.: メル → Meru, Иван → Ivan), garantindo que a energia seja sempre calculada.",
  en: "Names are analyzed in Latin script because Pythagorean numerology assigns value only to the 26 letters A–Z. Names in other alphabets are romanized before calculation (e.g. メル → Meru, Иван → Ivan), ensuring the energy is always computed.",
  es: "Los nombres se analizan en escritura latina porque la numerología pitagórica asigna valor solo a las 26 letras A–Z. Los nombres en otros alfabetos se romanizan antes del cálculo (ej.: メル → Meru, Иван → Ivan), garantizando que la energía siempre se calcule.",
  it: "I nomi sono analizzati in scrittura latina perché la numerologia pitagorica assegna valore solo alle 26 lettere A–Z. I nomi in altri alfabeti vengono romanizzati prima del calcolo (es.: メル → Meru, Иван → Ivan), garantendo che l'energia sia sempre calcolata.",
  fr: "Les noms sont analysés en écriture latine car la numérologie pythagoricienne n'attribue de valeur qu'aux 26 lettres A–Z. Les noms dans d'autres alphabets sont romanisés avant le calcul (ex. : メル → Meru, Иван → Ivan), garantissant que l'énergie soit toujours calculée.",
  de: "Namen werden in lateinischer Schrift analysiert, da die pythagoreische Numerologie nur den 26 Buchstaben A–Z einen Wert zuweist. Namen in anderen Alphabeten werden vor der Berechnung romanisiert (z. B. メル → Meru, Иван → Ivan), damit die Energie immer berechnet wird.",
  ja: "名前はラテン文字で分析されます。ピタゴラス数秘術はA–Zの26文字にのみ数値を割り当てるためです。他の文字体系の名前は計算前にローマ字化されます（例：メル → Meru、Иван → Ivan）。これによりエネルギーが常に算出されます。",
  zh: "名字以拉丁字母分析，因为毕达哥拉斯数字学只为A–Z这26个字母赋予数值。其他文字系统的名字在计算前会被罗马化（例如：メル → Meru、Иван → Ivan），从而确保能量始终被计算。",
  ru: "Имена анализируются в латинской записи, так как пифагорейская нумерология придаёт значение только 26 буквам A–Z. Имена в других алфавитах транслитерируются перед расчётом (напр.: メル → Meru, Иван → Ivan), чтобы энергия всегда вычислялась.",
  id: "Nama dianalisis dalam aksara Latin karena numerologi Pythagoras hanya memberi nilai pada 26 huruf A–Z. Nama dalam aksara lain diromanisasi sebelum perhitungan (mis.: メル → Meru, Иван → Ivan), memastikan energi selalu dihitung.",
  tr: "İsimler Latin alfabesinde analiz edilir çünkü Pisagor numerolojisi yalnızca A–Z arasındaki 26 harfe değer verir. Diğer alfabelerdeki isimler hesaplamadan önce romanize edilir (örn.: メル → Meru, Иван → Ivan); böylece enerji her zaman hesaplanır.",
  vi: "Tên được phân tích bằng chữ Latinh vì thần số học Pythagoras chỉ gán giá trị cho 26 chữ cái A–Z. Tên trong bảng chữ cái khác được La-tinh hóa trước khi tính (vd: メル → Meru, Иван → Ivan), đảm bảo năng lượng luôn được tính.",
  he: "השמות מנותחים בכתב לטיני מכיוון שהנומרולוגיה הפיתגורית מייחסת ערך רק ל-26 האותיות A–Z. שמות באלפבית אחר עוברים תעתיק לפני החישוב (למשל メル → Meru, Иван → Ivan), כדי שהאנרגיה תחושב תמיד.",
  ar: "تُحلَّل الأسماء بالحرف اللاتيني لأن علم الأعداد الفيثاغوري يمنح قيمة للحروف الـ26 من A إلى Z فقط. تُحوَّل الأسماء بالأبجديات الأخرى إلى الحرف اللاتيني قبل الحساب (مثل メル ← Meru، Иван ← Ivan)، لضمان حساب الطاقة دائمًا."
};

// ===== COMPRAR (entrada dos 24 cards) =====
function comprar(produto) {
  var lang = (typeof getLang === 'function') ? getLang() : 'pt';
  var t = (typeof translations !== 'undefined') ? (translations[lang] || translations.pt) : {};
  var lista = window.DADO_APLICA || ["nome_pet","nickname","nome_dominio","nome_canal","nome_equipe","nome_projeto","nome_evento"];
  if (lista.indexOf(produto) !== -1) { abrirModalDado(produto, lang); return; }
  var nome = (document.getElementById("calcNome") ? document.getElementById("calcNome").value : "").trim();
  var nascEl = document.getElementById("calcNasc");
  var nasc = (typeof converterData === 'function') ? converterData(nascEl ? nascEl.value : "") : (nascEl ? nascEl.value : "").trim();
  if (!nome || !nasc) {
    alert(t.preencha_dados || "Preencha nome e data de nascimento primeiro.");
    var sec = document.getElementById("calcSection") || document.getElementById("calculadora");
    if (sec) sec.scrollIntoView({ behavior: "smooth" });
    return;
  }
  window.location.href = '/criar-checkout?lang=' + encodeURIComponent(lang)
    + '&produto=' + encodeURIComponent(produto)
    + '&nome=' + encodeURIComponent(nome)
    + '&nascimento=' + encodeURIComponent(nasc);
}

function selecionarOpcao(container, btn) {
  container.querySelectorAll(".coleta-opcao").forEach(function(b){ b.classList.remove("ativo"); });
  btn.classList.add("ativo");
}

function fecharModalColeta() {
  var o = document.getElementById("modalColeta");
  if (o) o.style.display = "none";
}

// ===== MODAL ÚNICO DOS 7 PRODUTOS DA IA =====
function abrirModalDado(produto, lang) {
  var t  = (typeof translations !== 'undefined' && (translations[lang] || translations.pt)) || {};
  var UI = (window.IA_NOMES_UI || {})[lang] || (window.IA_NOMES_UI || {}).pt || {};
  var DL = window.DADO_LABEL || { pt: {} };
  var PT = window.PRODUTOS_TRAD || {};
  var label  = (DL[lang] && DL[lang][produto]) ? DL[lang][produto] : ((DL.pt && DL.pt[produto]) || produto);
  var titulo = (PT[lang] && PT[lang][produto]) ? PT[lang][produto] : ((PT.pt && PT.pt[produto]) || produto);
  var conf  = (window.CONF_COLETA && window.CONF_COLETA[produto]) || {};
  var tipos = conf.tipos || [];
  var ideal = (typeof ENERGIA_IDEAL !== 'undefined' && ENERGIA_IDEAL[produto]) ? ENERGIA_IDEAL[produto] : 0;

  var overlay = document.getElementById("modalDado");
  if (!overlay) {
    overlay = document.createElement("div");
    overlay.id = "modalDado";
    overlay.className = "modal-overlay";
    document.body.appendChild(overlay);
  }

  var htmlTipo = '';
  if (tipos.length) {
    htmlTipo = '<p style="color:#ccc;margin:12px 0 6px">' + (UI.tipo || 'Tipo') + ':</p>'
      + '<div id="modalTipoOpcoes" class="modal-grid">';
    for (var i = 0; i < tipos.length; i++) {
      var rotulo = (typeof tradOpcao === 'function') ? tradOpcao(tipos[i]) : tipos[i];
      htmlTipo += '<button type="button" class="btn btn-full modal-tipo-btn" data-tipo="' + tipos[i] + '">' + rotulo + '</button>';
    }
    htmlTipo += '</div>';
  }

  var htmlSexo = '';
  if (conf.sexos) {
    htmlSexo = '<p style="color:#ccc;margin:12px 0 6px">' + (UI.sexo || 'Sexo') + ':</p>'
      + '<div id="modalSexoOpcoes" class="modal-grid">'
      + '<button type="button" class="btn btn-full modal-sexo-btn" data-sexo="f">' + (UI.femea || 'Fêmea') + '</button>'
      + '<button type="button" class="btn btn-full modal-sexo-btn" data-sexo="m">' + (UI.macho || 'Macho') + '</button>'
      + '<button type="button" class="btn btn-full modal-sexo-btn" data-sexo="">' + (UI.indef || 'Indefinido') + '</button>'
      + '</div>';
  }
    
  overlay.innerHTML = '<div class="modal-box">'
    + '<button type="button" id="modalDadoX" aria-label="Fechar" style="position:absolute;top:8px;right:14px;background:none;border:none;color:#C9A94E;font-size:26px;line-height:1;cursor:pointer;">&times;</button>'
    + '<h3 id="modalDadoTitulo" style="color:var(--gold);margin-bottom:4px">' + titulo + '</h3>'
    + '<p id="modalDadoLabel" style="color:#ccc;margin-bottom:8px">' + label + ':</p>'
    + '<input id="modalDadoInput"  type="text" class="modal-input" placeholder="' + (UI.n1 || 'Nome 1') + '" autocomplete="off">'
    + '<input id="modalDadoInput2" type="text" class="modal-input" placeholder="' + (UI.n2 || 'Nome 2') + '" autocomplete="off" style="margin-top:8px">'
    + '<input id="modalDadoInput3" type="text" class="modal-input" placeholder="' + (UI.n3 || 'Nome 3') + '" autocomplete="off" style="margin-top:8px">'
    + '<p style="color:#888;font-size:.75rem;margin-top:6px">' + (UI.dica || '') + '</p>'
    + '<p style="color:#888;font-size:.72rem;margin-top:6px">'
    + ((window.IA_ROMAN || {})[lang] || (window.IA_ROMAN || {}).pt || '') + '</p>'  
    + '<p style="color:#ccc;margin:12px 0 6px">' + (UI.energia || 'Energia desejada') + ' (1-9):</p>'
    + '<div id="modalEnergiaOpcoes" class="energia-selector"></div>'
    + htmlTipo
    + htmlSexo  
    + '<div class="modal-actions">'
    + '<button type="button" id="modalDadoOk" class="btn">' + (t.confirmar_btn || t.confirmar || 'Confirmar') + '</button>'
    + '<button type="button" id="modalDadoCancel" class="btn btn-outline">' + (t.cancelar_btn || t.cancelar || 'Cancelar') + '</button>'
    + '</div></div>';

  var boxE = document.getElementById('modalEnergiaOpcoes');
  var energiaSel = ideal || 0;
  for (var n = 1; n <= 9; n++) {
    (function (num) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'energia-btn' + (num === ideal ? ' ideal selecionada' : '');
      b.textContent = String(num);
      b.dataset.energia = num;
      b.onclick = function () {
        var todos = boxE.querySelectorAll('.energia-btn');
        for (var k = 0; k < todos.length; k++) todos[k].classList.remove('selecionada');
        b.classList.add('selecionada');
        energiaSel = num;
      };
      boxE.appendChild(b);
    })(n);
  }

  var tipoSel = '';
  var btnsTipo = overlay.querySelectorAll('.modal-tipo-btn');
  for (var j = 0; j < btnsTipo.length; j++) {
    btnsTipo[j].onclick = function () {
      for (var k = 0; k < btnsTipo.length; k++) btnsTipo[k].classList.remove('selecionado');
      this.classList.add('selecionado');
      tipoSel = this.getAttribute('data-tipo');
    };
  }

  var sexoSel = '';
  var btnsSexo = overlay.querySelectorAll('.modal-sexo-btn');
  for (var s = 0; s < btnsSexo.length; s++) {
    btnsSexo[s].onclick = function () {
      for (var k = 0; k < btnsSexo.length; k++) btnsSexo[k].classList.remove('selecionado');
      this.classList.add('selecionado');
      sexoSel = this.getAttribute('data-sexo');
    };
  }
    
  window._modalDado = { produto: produto, lang: lang, tipo: '', energia: energiaSel };

  document.getElementById('modalDadoX').onclick      = fecharModalDado;
  document.getElementById('modalDadoCancel').onclick = fecharModalDado;
  document.getElementById('modalDadoOk').onclick     = function () {
    _confirmarCamposIA(produto, lang, tipoSel, energiaSel);
  };

  overlay.classList.add("active");
  var inp1 = document.getElementById('modalDadoInput');
  if (inp1) { try { inp1.focus(); } catch (e) {} }
}

function _confirmarCamposIA(produto, lang, tipo, energia, sexo) {
  var v = function (id) { var e = document.getElementById(id); return e ? e.value.trim() : ''; };
  var d1 = v('modalDadoInput'), d2 = v('modalDadoInput2'), d3 = v('modalDadoInput3');
  if (!d1 && !d2 && !d3) {
    var UI = (window.IA_NOMES_UI || {})[lang] || {};
    alert(UI.nenhum ? UI.nenhum : "Informe ao menos um nome.");
    return;
  }
  fecharModalDado();
  window.location.href = '/criar-checkout?lang=' + encodeURIComponent(lang)
    + '&produto=' + encodeURIComponent(produto)
    + '&dado='  + encodeURIComponent(d1)
    + '&dado2=' + encodeURIComponent(d2)
    + '&dado3=' + encodeURIComponent(d3)
    + '&tipo='  + encodeURIComponent(tipo || '')
    + '&energia=' + encodeURIComponent(energia || '')
    + '&sexo=' + encodeURIComponent(sexo || '');    
}

function fecharModalDado() {
  var o = document.getElementById("modalDado");
  if (o) o.classList.remove("active");
}

function confirmarModalDado(produto, lang) {
  var i1 = document.getElementById("modalDadoInput");
  var i2 = document.getElementById("modalDadoInput2");
  var sexo = _modalDado.sexo || "";  
  if (!i1 && !i2) return;
  _confirmarCamposIA(produto, lang, (_modalDado && _modalDado.tipo) || '', (_modalDado && _modalDado.energia) || '');
}

function montarPassoTipo(produto, lang) {
  abrirModalDado(produto, lang || ((typeof getLang === 'function') ? getLang() : 'pt'));
}

// ===== CONFIG DE DESCONTO DO BÔNUS COLETIVO — FONTE ÚNICA =====
// Zona automática: até 2.000 unidades, o site calcula o desconto sozinho (10% a 50%).
// Acima disso: NÃO calcula — entra em "sob consulta" (negociação manual).
window.CONFIG_DESCONTO = {
  faixas: [
    { min: 10,   pct: 10 },
    { min: 50,   pct: 15 },
    { min: 100,  pct: 20 },
    { min: 200,  pct: 30 },
    { min: 500,  pct: 40 },
    { min: 1000, pct: 45 },
    { min: 2000, pct: 50 }    
  ],
  teto_automatico: 2000,
  pct_teto_negociacao: 70
};
function obterConfigDesconto() {
  return (typeof window.CONFIG_DESCONTO !== 'undefined') ? window.CONFIG_DESCONTO : null;
}
// Desconto automático (%). Retorna o % aplicável; em zona de negociação retorna 0.
function descontoBC(qtd) {
  return calcDescontoBC(qtd).pct;
}

// Cálculo completo: distingue zona automática da zona de negociação.
// Retorno: { modo: 'auto'|'consulta', pct, qtd, teto }
function calcDescontoBC(qtd) {
  qtd = parseInt(qtd, 10) || 0;
  var cfg = obterConfigDesconto();
if (!cfg) {
  // fallback derivado, nunca duplicado à mão
  var pct = 0, tetoFb = 2000;
  if (qtd > tetoFb) return { modo: 'consulta', pct: 0, qtd: qtd, teto: tetoFb };
  if (qtd >= 2000) pct = 50;
  else if (qtd >= 1000) pct = 45;
  else if (qtd >= 500) pct = 40;
  else if (qtd >= 200) pct = 30;
  else if (qtd >= 100) pct = 20;
  else if (qtd >= 50) pct = 15;
  else if (qtd >= 10) pct = 10;
  return { modo: 'auto', pct: pct, qtd: qtd, teto: tetoFb };
}
  if (qtd > cfg.teto_automatico) {
    return { modo: 'consulta', pct: 0, qtd: qtd, teto: cfg.teto_automatico };
  }
  var melhor = 0;
  var faixas = cfg.faixas.slice().sort(function(a, b) { return b.min - a.min; });
  for (var i = 0; i < faixas.length; i++) {
    if (qtd >= faixas[i].min) { melhor = faixas[i].pct; break; }
  }
  return { modo: 'auto', pct: melhor, qtd: qtd, teto: cfg.teto_automatico };
}

// True quando a quantidade exige negociação manual (acima de 2.000)
function bcSobConsulta(qtd) {
  return calcDescontoBC(qtd).modo === 'consulta';
}
function precoUnitarioBC(id) {
  var lang = (typeof getLang === 'function') ? getLang() : 'pt';
  var faixa = (typeof PRODUTO_FAIXA !== 'undefined' && PRODUTO_FAIXA[id] !== undefined) ? PRODUTO_FAIXA[id] : null;
  if (faixa === null || faixa === undefined) return 0;
  var servidor = (typeof PRECO_VALORES !== 'undefined' && PRECO_VALORES[lang]);
  var base = servidor ? PRECO_VALORES[lang]
           : (typeof PRECO_BASE !== 'undefined' ? (PRECO_BASE[lang] || PRECO_BASE.pt) : null);
  if (!base) return 0;
  var unit = parseInt(base[faixa], 10) || 0;
  if (servidor) unit = Math.round(unit / 100);
  return unit;
}
function usarPlanoPronto(qExpress, qVida, qIa, qCompleto) {
  var mapa = { express: qExpress, vida: qVida, ia: qIa, completo: qCompleto };
  document.querySelectorAll("#bcTabelaCorpo input[data-prod]").forEach(function(inp) {
    var prod = inp.getAttribute("data-prod");
    inp.value = mapa[prod] || 0;
  });
  atualizarResumoBC();
}
// ===== CALCULADORA GRATUITA (5 números) =====
function r1Num(n) {
  // Reduz SEMPRE a 1-9. Mestres são exceção só no cruzamento.
  while (n > 9) {
    n = String(n).split('').reduce(function(a, d) { return a + parseInt(d, 10); }, 0);
  }
  return n;
}
function calcular5Numeros(nome, nasc) {
  var t = {};
  var letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  for (var i = 0; i < letras.length; i++) { t[letras[i]] = (i % 9) + 1; }
  var parts = nasc.split('-');
  var lp = r1Num(parseInt(parts[0], 10) + parseInt(parts[1], 10) + parseInt(parts[2], 10));
  var nu = nome.toUpperCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^A-Z]/g, '');
  var te = 0, tv = 0, tp = 0;
  for (var j = 0; j < nu.length; j++) {
    var ch = nu[j];
    var val = t[ch] || 0;
    te += val;
    if ("AEIOU".indexOf(ch) >= 0) { tv += val; } else { tp += val; }
  }
  // ordem dos rótulos: caminho, realizacao, alma, personalidade, destino
  // realizacao = consoantes (tp) | alma = vogais (tv) | personalidade = todas (te)
  return [lp, r1Num(tp), r1Num(tv), r1Num(te), r1Num(r1Num(te) + lp)];
}
var ultimosNumeros = null;
function calcularMapa() {
  var lang = getLang();
  var t = translations[lang] || translations["pt"];
  var nome = (document.getElementById("calcNome") ? document.getElementById("calcNome").value : "").trim();
    var nasc = converterData((document.getElementById("calcNasc") ? document.getElementById("calcNasc").value : "").trim());
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
  var sigs = t.sig || {};
  var chaves5 = ['caminho', 'realizacao', 'alma', 'personalidade', 'destino'];
  var html = "";
  for (var i = 0; i < ultimosNumeros.length && i < chaves5.length; i++) {
    var n = ultimosNumeros[i];
    var nomeE = nomes[chaves5[i]] || ("Energia " + n);
    var sigE = sigs["sig_" + chaves5[i]] || "";
    html += '<div class="numero-gratis">'
          + '<span class="numero-nome">' + nomeE + ':</span> '
          + '<span class="numero-valor">' + n + '</span>'
          + (sigE ? '<p class="numero-sig">' + sigE + '</p>' : '')
          + '</div>';
  }
  var el = document.getElementById("resultadoNumeros") || document.getElementById("resultado") || document.getElementById("calcResultado");
  if (el) { el.innerHTML = html; el.style.display = "block"; }
  var box = document.getElementById("resultadoBox") || el;
  if (box) box.style.display = "block";
}
// ===== IR PARA COMPRA (com energia) — usada pelos botões de energia e cards =====
function irParaCompra(produto, lang, energia) {
  if (!lang) lang = getLang();
  var qs = 'lang=' + encodeURIComponent(lang) + '&produto=' + encodeURIComponent(produto);
  if (energia) qs += '&energia=' + encodeURIComponent(energia);
  var nome = (document.getElementById("calcNome") ? document.getElementById("calcNome").value : "").trim();
    var nasc = converterData((document.getElementById("calcNasc") ? document.getElementById("calcNasc").value : "").trim());
  if (nome) qs += '&nome=' + encodeURIComponent(nome);
  if (nasc) qs += '&nascimento=' + encodeURIComponent(nasc);
  window.location.href = '/criar-checkout?' + qs;
}
// ===== TOGGLE FORM (abre no modal genérico do produtos.js — padrão Nome do Pet) =====
function toggleForm(formId) {
  if (typeof abrirFormModal === 'function') {
    abrirFormModal(formId);
    return;
  }
  var el = document.getElementById(formId);
  if (!el) return;
  var escondido = (el.style.display === 'none' || el.style.display === '');
  el.style.display = escondido ? 'block' : 'none';
  if (escondido) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// ===== ENVIAR MENSAGEM / ATIVAR BÔNUS =====
window.enviarMensagem = window.enviarMensagem || function(){
  var nome = (document.getElementById('msgNome') ? document.getElementById('msgNome').value : '').trim();
  var texto = (document.getElementById('msgTexto') ? document.getElementById('msgTexto').value : '').trim();
  var st = document.getElementById('msgStatus');
  if (!nome || !texto) { if (st) st.textContent = t_preencha(); return; }
  fetch('/sugestao', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nome: nome, email: '', mensagem: texto })
  }).then(function(r){ return r.json(); }).then(function(res){
    if (st) st.textContent = (res && res.ok) ? 'Enviado com sucesso!' : 'Erro ao enviar.';
  }).catch(function(){ if (st) st.textContent = 'Erro ao enviar.'; });
};
window.ativarBonusInserido = window.ativarBonusInserido || function(){
  var cod = (document.getElementById('biCodigo') ? document.getElementById('biCodigo').value : '').trim();
  var st = document.getElementById('biStatus');
  if (!cod) { if (st) st.textContent = t_preencha(); return; }
  fetch('/ativar-bonus', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ codigo: cod })
  }).then(function(r){ return r.json(); }).then(function(res){
    if (st) st.textContent = (res && res.ok) ? '🎁 Código ativado!' : 'Código inválido ou já usado.';
  }).catch(function(){ if (st) st.textContent = 'Erro ao validar o código.'; });
};

window.ativarBonusIA = window.ativarBonusIA || function(){
  var cod = (document.getElementById('iaCodigoBonus') ? document.getElementById('iaCodigoBonus').value : '').trim();
  var st = document.getElementById('iaBonusStatus');
  if (!cod) { if (st) st.textContent = t_preencha(); return; }
  fetch('/ativar-bonus', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ codigo: cod })
  }).then(function(r){ return r.json(); }).then(function(res){
    if (st) st.textContent = (res && res.ok) ? '🎁 Código ativado!' : 'Código inválido ou já usado.';
  }).catch(function(){ if (st) st.textContent = 'Erro ao validar o código.'; });
};

 /* ===== CARREGADOR DE PARTIALS ===== */
function carregarPartials() {
  fetch('/static/partials/produtos.html')
    .then(function(r){ if(!r.ok) throw new Error('HTTP ' + r.status); return r.text(); })
    .then(function(html){
      var alvo = document.getElementById('areaProdutos');
      if (alvo) alvo.innerHTML = html;
      montarTudo();
    })
    .catch(function(e){ console.warn('[partials] produtos.html:', e); });
}

function montarTudo() {
  if (window._montando) return;        // trava UMA vez, no topo
  window._montando = true;
  try {
    if (typeof montarSeletorIdioma === "function") montarSeletorIdioma();
  } catch (e) { console.error("[A1ELOS] ERRO em montarSeletorIdioma:", e); }
  try {
    if (typeof montarTabelaBC === "function") {
      montarTabelaBC();
    } else { console.warn("[A1ELOS] montarTabelaBC NÃO encontrada"); }
  } catch (e) { console.error("[A1ELOS] ERRO em montarTabelaBC:", e); }
  try {
    if (typeof montarEnergias === "function") {
      montarEnergias();
    } else { console.warn("[A1ELOS] montarEnergias NÃO encontrada"); }
  } catch (e) { console.error("[A1ELOS] ERRO em montarEnergias:", e); }
  try { if (typeof traduzirNomesBC === 'function') traduzirNomesBC(); } catch (e) {}  
  try {
    if (typeof traduzirTudo === "function") {
      traduzirTudo();
    } else { console.warn("[A1ELOS] traduzirTudo NÃO encontrada"); }
  } catch (e) { console.error("[A1ELOS] ERRO em traduzirTudo:", e); }
  if (typeof atualizarPrecos === 'function') atualizarPrecos();
  if (typeof atualizarLinksApresentacao === 'function') atualizarLinksApresentacao();
  try {
  if (typeof forcarTraducaoBC === "function") forcarTraducaoBC();
  } catch (e) { console.error("[A1ELOS] ERRO em forcarTraducaoBC:", e); }  
  window._montando = false;            // libera a trava no fim
}

function atualizarLinksApresentacao() {
  var lang = (typeof getLang === 'function') ? getLang() : 'pt';
  var btnAp = document.getElementById('btnApresentacao');
  if (btnAp) btnAp.href = '/api/apresentacao?lang=' + lang;
  var btnSlides = document.getElementById('btnApresentacaoSlides');
  if (btnSlides) btnSlides.href = '/api/apresentacao-slides?lang=' + lang;
  // Também cobre os cards de download da seção Investidores, se usarem links diretos
  var aInvest = document.querySelectorAll('a[data-doc="apresentacao"]');
  for (var i = 0; i < aInvest.length; i++) aInvest[i].href = '/api/apresentacao?lang=' + lang;
  var aSlides = document.querySelectorAll('a[data-doc="slides"]');
  for (var j = 0; j < aSlides.length; j++) aSlides[j].href = '/api/apresentacao-slides?lang=' + lang;
}

var MESES_TRAD = {
  pt:["Janeiro","Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"],
  en:["January","February","March","April","May","June","July","August","September","October","November","December"],
  es:["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"],
  it:["Gennaio","Febbraio","Marzo","Aprile","Maggio","Giugno","Luglio","Agosto","Settembre","Ottobre","Novembre","Dicembre"],
  fr:["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Août","Septembre","Octobre","Novembre","Décembre"],
  de:["Januar","Februar","März","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"],
  ru:["Январь","Февраль","Март","Апрель","Май","Июнь","Июль","Август","Сентябрь","Октябрь","Ноябрь","Декабрь"],
  zh:["一月","二月","三月","四月","五月","六月","七月","八月","九月","十月","十一月","十二月"],
  ja:["1月","2月","3月","4月","5月","6月","7月","8月","9月","10月","11月","12月"],
  ar:["يناير","فبراير","مارس","أبريل","مايو","يونيو","يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"],
  he:["ינואר","פברואר","מרץ","אפריל","מאי","יוני","יולי","אוגוסט","ספטמבר","אוקטובר","נובמבר","דצמבר"],
  id:["Januari","Februari","Maret","April","Mei","Juni","Juli","Agustus","September","Oktober","November","Desember"],
  tr:["Ocak","Şubat","Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos","Eylül","Ekim","Kasım","Aralık"],
  vi:["Tháng 1","Tháng 2","Tháng 3","Tháng 4","Tháng 5","Tháng 6","Tháng 7","Tháng 8","Tháng 9","Tháng 10","Tháng 11","Tháng 12"]
};

// ===== MÁSCARAS DE DATA — teclado numérico no celular (calcNasc + calNascimento) =====
["calcNasc", "calNascimento"].forEach(function (id) {
    document.querySelectorAll('[id="' + id + '"]').forEach(function (inp) {
        inp.setAttribute("inputmode", "numeric");
        inp.setAttribute("maxlength", "10");
        if (inp._mascarado) return;          // evita máscara duplicada nas cópias do modal
        inp._mascarado = true;
        inp.addEventListener("input", function () {
            var v = this.value.replace(/\D/g, "").slice(0, 8);
            if (v.length > 4)      this.value = v.slice(0,2) + "/" + v.slice(2,4) + "/" + v.slice(4);
            else if (v.length > 2) this.value = v.slice(0,2) + "/" + v.slice(2);
            else                   this.value = v;
        });
    });
});
// Reaplica máscaras quando os partials carregam (formulários injetados via fetch)
function aplicarMascarasData() {
    ["calcNasc", "calNascimento"].forEach(function (id) {
        document.querySelectorAll('[id="' + id + '"]').forEach(function (inp) {
            if (inp._mascarado) return;
            inp._mascarado = true;
            inp.setAttribute("inputmode", "numeric");
            inp.setAttribute("maxlength", "10");
            inp.addEventListener("input", function () {
                var v = this.value.replace(/\D/g, "").slice(0, 8);
                if (v.length > 4)      this.value = v.slice(0,2) + "/" + v.slice(2,4) + "/" + v.slice(4);
                else if (v.length > 2) this.value = v.slice(0,2) + "/" + v.slice(2);
                else                   this.value = v;
            });
        });
    });
}

function converterData(v) {
    var p = (v || "").split("/");
    if (p.length === 3 && p[0].length === 2) {
        return p[2] + "-" + p[1] + "-" + p[0];   // DD/MM/AAAA → AAAA-MM-DD
    }
    return v;   // já está em AAAA-MM-DD (ou vazio) — não mexe
}
function getLang() { return (typeof localStorage !== 'undefined' && localStorage.getItem('lang')) || 'pt'; }
function montarSeletorData() {
  var dia = document.getElementById("calcDia");
  var mes = document.getElementById("calcMes");
  var ano = document.getElementById("calcAno");
  if (!dia || !mes || !ano) return;
  if (dia.options.length > 0) { atualizarMesesData(); return; }
  for (var d = 1; d <= 31; d++) {
    var o = document.createElement("option");
    o.value = (d < 10 ? "0" : "") + d;
    o.textContent = d;
    dia.appendChild(o);
  }
  var anoAtual = new Date().getFullYear();
  for (var a = anoAtual; a >= 1900; a--) {
    var oa = document.createElement("option");
    oa.value = a;
    oa.textContent = a;
    ano.appendChild(oa);
  }
  atualizarMesesData();
  dia.onchange = mes.onchange = ano.onchange = montarValorData;
}
function atualizarMesesData() {
  var mes = document.getElementById("calcMes");
  if (!mes) return;
  var lang = getLang();
  var nomes = MESES_TRAD[lang] || MESES_TRAD.pt;
  var atual = mes.value;
  mes.innerHTML = "";
  for (var i = 0; i < 12; i++) {
    var o = document.createElement("option");
    o.value = (i + 1 < 10 ? "0" : "") + (i + 1);
    o.textContent = nomes[i];
    mes.appendChild(o);
  }
  if (atual) mes.value = atual;
  montarValorData();
}
function montarValorData() {
  var d = document.getElementById("calcDia").value;
  var m = document.getElementById("calcMes").value;
  var a = document.getElementById("calcAno").value;
  var hidden = document.getElementById("calcNasc");
  if (hidden && d && m && a) hidden.value = a + "-" + m + "-" + d;
}

// Interruptor automático: acima do teto, oculta o botão de pagamento
// e exibe o formulário de negociação sob consulta.
function aplicarEstadoBC(qtdTotal) {
  qtdTotal = parseInt(qtdTotal, 10) || 0;
  var consulta = bcSobConsulta(qtdTotal);
  var btn = document.getElementById('bcBtnConfirmar');
  if (!btn) btn = document.querySelector('#bcResumo button, #bcoResumo button, .bc-confirmar, [data-bc="confirmar"]');
  var formLead = document.getElementById('formNegociacao');
  var aviso = document.getElementById('bcAvisoConsulta');
  if (consulta) {
    if (btn) btn.style.display = 'none';
    if (formLead) formLead.style.display = 'block';
    if (aviso) aviso.style.display = 'block';
  } else {
    if (btn) btn.style.display = '';
    if (formLead) formLead.style.display = 'none';
    if (aviso) aviso.style.display = 'none';
  }
}

window.enviarPedidoNegociacao = window.enviarPedidoNegociacao || function(){
  var nome = (document.getElementById('negNome') ? document.getElementById('negNome').value : '').trim();
  var empresa = (document.getElementById('negEmpresa') ? document.getElementById('negEmpresa').value : '').trim();
  var email = (document.getElementById('negEmail') ? document.getElementById('negEmail').value : '').trim();
  var qtd = (document.getElementById('negQtd') ? document.getElementById('negQtd').value : '').trim();
  var msg = (document.getElementById('negMsg') ? document.getElementById('negMsg').value : '').trim();
  var st = document.getElementById('negStatus');
  if (!nome || !email || !qtd) { if (st) st.textContent = t_preencha(); return; }
  fetch('/api/negociacao', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nome: nome, empresa: empresa, email: email, quantidade: qtd, mensagem: msg })
  }).then(function(r){ return r.json(); }).then(function(res){
    if (st) st.textContent = (res && res.ok) ? '✅ Pedido enviado! Entraremos em contato.' : 'Erro ao enviar. Tente novamente.';
  }).catch(function(){ if (st) st.textContent = 'Erro ao enviar. Tente novamente.'; });
};

// ===== INICIALIZAÇÃO =====
function init() {
  var savedLang = localStorage.getItem('lang');
  var browserLang = navigator.language.split('-')[0];
  var defaultLang = savedLang || (typeof translations !== 'undefined' && translations[browserLang] ? browserLang : 'pt');
  montarSeletorIdioma();
  montarSeletorData();
  setLanguage(defaultLang);
  if (typeof carregarPartials === 'function') {
    carregarPartials();   // carregarPartials chama montarTudo() UMA vez no final
  } else if (typeof montarTudo === 'function') {
    montarTudo();
  }
}
// ===== INICIALIZAÇÃO AUTOMÁTICA GARANTIDA =====
function iniciarSeguro() {
  try {
    init();
  } catch (e) {
    console.error("[A1ELOS] init() falhou:", e);
  }
}
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", iniciarSeguro);
} else {
  iniciarSeguro();
}

// ===== ATUALIZAR PREÇOS DOS CARDS — FONTE ÚNICA: /api/precos =====
// Busca a tabela de referência do servidor (referencia/precos.py).
// Não altera a tabela; apenas lê dela. Respeita moeda local.
function formatarValor(centavos) {
  var v = (centavos / 100).toFixed(0);
  return v.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
}

// ===== SOMAR SOB MEDIDA NA MOEDA DO IDIOMA =====
function formatarMoeda(lang, valor) {
  var simbolo = (typeof SIMBOLO !== 'undefined' && SIMBOLO[lang]) ? SIMBOLO[lang] : 'R$';
  return simbolo + ' ' + String(valor).replace(/\B(?=(\d{3})+(?!\d))/g, '.');
}

function atualizarSomaSobMedida(lang, precos) {
  var sel = document.querySelectorAll('.sob-medida-item.selecionado, .item-selecionado');
  var soma = 0;
  for (var i = 0; i < sel.length; i++) {
    var el = sel[i];
    var faixa = parseInt(el.getAttribute('data-preco') || el.getAttribute('data-faixa'), 10);
    if (!isNaN(faixa) && precos[faixa]) {
      soma += parseInt(precos[faixa], 10);
    }
  }
  var alvo = document.getElementById('soma-sob-medida');
  if (alvo) alvo.textContent = formatarMoeda(lang, soma);
}

function atualizarPrecos() {
  var lang = getLang();
  var t = translations[lang] || translations.pt;
  // Se os dados ainda não chegaram do servidor, sai sem erro.
  // O fetch('/api/precos') no final do arquivo chama atualizarPrecos() de novo quando chegar.
  if (typeof PRECO_VALORES === 'undefined' || typeof PRODUTO_FAIXA === 'undefined') return;
  var precos = PRECO_VALORES[lang] || PRECO_VALORES.pt;
  var simbolo = (typeof SIMBOLO !== 'undefined' && SIMBOLO[lang]) ? SIMBOLO[lang] : 'R$';
  if (!precos) return;
  var cards = document.querySelectorAll('.product-card[data-prod]');
  for (var i = 0; i < cards.length; i++) {
    var prod = cards[i].getAttribute('data-prod');
    var el = cards[i].querySelector('.prod-preco');
    if (!el) continue;
    if (prod === 'coletivo') {
      el.textContent = t.sob_consulta || 'Sob consulta';
      continue;
    }
    var faixa = PRODUTO_FAIXA[prod];
    if (typeof faixa === 'undefined' || !precos[faixa]) continue;
    el.textContent = simbolo + ' ' + formatarValor(precos[faixa]);
  }
  try {
    if (typeof atualizarSomaSobMedida === 'function') {
      atualizarSomaSobMedida(lang, precos);
    }
  } catch (err) {
    console.error('[A1ELOS] erro em atualizarSomaSobMedida:', err);
  }
}
// ===== CARREGA PREÇOS DO SERVIDOR (fonte única: /api/precos) =====
fetch('/api/precos')
  .then(function(r){ if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
  .then(function(d){
    window.PRECO_VALORES = d.valores || {};
    window.SIMBOLO = d.simbolo || {};
    if (d.faixa) window.PRODUTO_FAIXA = d.faixa;
    if (typeof atualizarPrecos === 'function') atualizarPrecos();
  })
  .catch(function(e){ console.warn('[A1ELOS] /api/precos:', e); });
  
/* ===== AUTO-MONTAGEM DOS SELETORES DE ENERGIA (círculos) ===== */
/* Varre todos os .energia-selector VAZIOS e monta os círculos 1-9,
   marcando a energia ideal (★ verde) de cada produto. Idempotente. */
(function () {
  var IDEAL = {
    urna: 8, eleitoral: 8, artistico: 2, nome_ong: 6,
    ia: 8, bebe: 8, negocio: 8, assinatura: 8,
    nome_pet: 5, nickname: 8, nome_dominio: 8, nome_canal: 8,
    nome_equipe: 8, nome_projeto: 8, nome_evento: 3
  };
  var MAPA_ID_PROD = {
    urna: "urna", eleitoral: "eleitoral", arte: "artistico", ong: "nome_ong",
    ia: "ia", bebe: "bebe", negocio: "negocio", assinatura: "assinatura",
    equipe: "nome_equipe"
  };
  function montarSeletor(el) {
    if (el.children.length > 0) return;   // já montado por outra função? não mexe
    var m = (el.id || "").match(/^(.+?)EnergiaSel$/);
    if (!m) return;
    var prod = MAPA_ID_PROD[m[1]];
    if (!prod) return;
    var ideal = (window.ENERGIA_IDEAL && window.ENERGIA_IDEAL[prod]) || IDEAL[prod] || 0;
    var titulos = (window.ENERGIA_TITULOS && window.ENERGIA_TITULOS[getLang()]) || {};
    el.innerHTML = "";
    for (var i = 1; i <= 9; i++) {
      (function (n) {
        var b = document.createElement("button");
        b.type = "button";
        b.className = "energia-btn" + (n === ideal ? " ideal selecionada" : "");
        b.textContent = String(n);
        b.title = titulos[String(n)] || String(n);
        b.onclick = function () {
          var btns = el.querySelectorAll(".energia-btn");
          for (var k = 0; k < btns.length; k++) btns[k].classList.remove("selecionada");
          b.classList.add("selecionada");
        };
        el.appendChild(b);
      })(i);
    }
  }
  function montarTodos() {
    var sels = document.querySelectorAll(".energia-selector");
    for (var i = 0; i < sels.length; i++) montarSeletor(sels[i]);
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () { setTimeout(montarTodos, 300); });
  } else {
    setTimeout(montarTodos, 300);
  }
  if (typeof window.montarTudo === "function") {
    var _origMT = window.montarTudo;
    window.montarTudo = function () {
      var r = _origMT.apply(this, arguments);
      montarTodos();
      return r;
    };
  }
  window.montarTodosSeletoresEnergia = montarTodos;
})();

var COD_ALFABETO = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
function codChecksum(base) {
  var soma = 0;
  for (var i = 0; i < base.length; i++) soma += COD_ALFABETO.indexOf(base[i]);
  return COD_ALFABETO[soma % COD_ALFABETO.length];
}
function codNormalizar(codigo) {
  return (codigo || "").toUpperCase().replace(/[^A-Z0-9]/g, "");
}
function codValido(codigo) {
  var c = codNormalizar(codigo);
  if (c.length !== 10 || c.slice(0, 2) !== "A1") return false;
  var base = c.slice(2, 9);   // 7 chars
  var check = c.slice(9, 10); // 8º char
  return codChecksum(base) === check;
}

window.abrirHubIA = window.abrirHubIA || function(){
  var o = document.getElementById('modalHubIA');
  if (o) o.style.display = 'flex';
};
window.fecharHubIA = window.fecharHubIA || function(){
  var o = document.getElementById('modalHubIA');
  if (o) o.style.display = 'none';
};

function pagarEquipe(){
  var n = (document.getElementById('equipeNome') ? document.getElementById('equipeNome').value : '').trim();
  if (!n) { alert(t_preencha()); return; }
  location.href = '/criar-checkout?produto=nome_equipe&dado=' + encodeURIComponent(n)
    + '&energia=' + encodeURIComponent(_energiaSelecionada('equipeEnergiaSel', 'nome_equipe'))
    + '&lang=' + getLang();
}
// ===== BLOCO 6: pagamento do Compatibilidade de Equipes (RH) =====
window.pagarCompatibilidade = window.pagarCompatibilidade || function(){
  var n = (document.getElementById('equipeMembros') ? document.getElementById('equipeMembros').value : '').trim();
  if (!n) { alert(t_preencha()); return; }
  location.href = '/criar-checkout?produto=compatibilidade_equipes&dado=' + encodeURIComponent(n)
    + '&lang=' + getLang();
};
// ===== GUARDA GLOBAL ANTI-SUBMIT (A1ELOS — 20/10/2026) =====
// Motivo: <button> dentro de <form> sem type="button" dispara um submit nativo
// que cancela a navegação do onclick (pagarX). Este bloco impede o submit nativo
// de TODOS os formulários SEM action (os cards) — cobre cards injetados via
// fetch e clones do modal genérico. Formulários COM action real (ex.: POST
// /sugestao) continuam funcionando normalmente.
(function(){
  function _guarda(ev){
    var f = ev.target;
    if (f && f.tagName === 'FORM' && !f.getAttribute('action')) {
      ev.preventDefault();
      ev.stopPropagation();
    }
  }
  document.addEventListener('submit', _guarda, true);

  // Camada 2: marca type="button" nos botões dos formulários sem action
  function _blindar(){
    var forms = document.querySelectorAll('form');
    for (var i = 0; i < forms.length; i++) {
      if (forms[i].getAttribute('action')) continue;
      var bts = forms[i].querySelectorAll('button:not([type])');
      for (var j = 0; j < bts.length; j++) bts[j].setAttribute('type', 'button');
    }
  }
  _blindar();
  if (typeof MutationObserver !== 'undefined' && document.body) {
    new MutationObserver(_blindar).observe(document.body, {childList: true, subtree: true});
  }
})();

/* ===== SEXO DO ANIMAL: seleção única + valor ===== */
(function () {
  var MAPA = {
    "fêmea": "femea", "femea": "femea",
    "macho": "macho",
    "não sei": "indef", "nao sei": "indef", "indefinido": "indef"
  };

  function rotulo(b) {
    return (b.textContent || "").replace(/✓/g, "").trim().toLowerCase();
  }

  function pintar(b, ativo) {
    b.style.background = ativo ? "#C9A94E" : "transparent";
    b.style.color      = ativo ? "#0a0a0a" : "#C9A94E";
    b.style.border     = "1px solid #C9A94E";
    b.style.fontWeight = ativo ? "700" : "400";
    b.textContent = (b.textContent || "").replace(/\s*✓/g, "").trim() + (ativo ? " ✓" : "");
  }

  document.addEventListener("click", function (ev) {
    var b = ev.target.closest && ev.target.closest("button");
    if (!b) return;
    var r = rotulo(b);
    if (!MAPA[r]) return;

    if (window._modalDado) window._modalDado.sexo = MAPA[r];

    setTimeout(function () {
      var irmaos = b.parentNode ? b.parentNode.querySelectorAll("button") : [b];
      for (var i = 0; i < irmaos.length; i++) {
        if (MAPA[rotulo(irmaos[i])]) pintar(irmaos[i], irmaos[i] === b);
      }
    }, 0);
  }, false);
})();

// ===== COLETOR ÚNICO — CASAL, FAMÍLIA E EQUIPES =====
// Substitui pagarCasal / pagarFamilia / pagarCompatibilidade.
// Lê pelos IDs corretos; se não existirem, lê o modal visível.
(function () {
  "use strict";

  /* ---------- leitura de campos ---------- */
  function _visivel(el) { return el && el.getClientRects().length > 0; }

  function _campo(ids) {
    var primeiro = null;
    for (var i = 0; i < ids.length; i++) {
      var nos = document.querySelectorAll('[id="' + ids[i] + '"]');
      for (var j = 0; j < nos.length; j++) {
        if (!primeiro) primeiro = nos[j];
        if (_visivel(nos[j])) return nos[j];
      }
    }
    return primeiro;
  }

  function _valor(ids) {
    var el = _campo(ids);
    return el ? String(el.value || "").trim() : "";
  }

  function _data(ids) {
    var v = _valor(ids);
    return (v && typeof converterData === "function") ? converterData(v) : v;
  }

  /* ---------- leitura do modal genérico ---------- */
  function _inputsModal() {
    var raiz = document.getElementById("modalDado") ||
               document.getElementById("modalColeta") ||
               document.querySelector(".modal-box");
    if (!raiz) return [];
    var todos = raiz.querySelectorAll("input");
    var out = [];
    for (var i = 0; i < todos.length; i++) {
      if (todos[i].type === "hidden") continue;
      if (!_visivel(todos[i])) continue;
      out.push(todos[i]);
    }
    return out;
  }

  function _ehData(el) {
    var ph = (el.getAttribute("placeholder") || "").toLowerCase();
    var im = (el.getAttribute("inputmode") || "").toLowerCase();
    var tp = (el.type || "").toLowerCase();
    if (tp === "date") return true;
    if (im === "numeric") return true;
    return /data|nasc|date|birth/.test(ph);
  }

  function _coletarDoModal(qtd) {
    var els = _inputsModal();
    var nomes = [], datas = [];
    for (var i = 0; i < els.length; i++) {
      if (_ehData(els[i])) datas.push(els[i]); else nomes.push(els[i]);
    }
    var rn = [], rd = [];
    for (var k = 0; k < qtd; k++) {
      rn.push(nomes[k] ? String(nomes[k].value || "").trim() : "");
      var vd = datas[k] ? String(datas[k].value || "").trim() : "";
      rd.push((vd && typeof converterData === "function") ? converterData(vd) : vd);
    }
     return { nomes: rn, datas: rd, apelidos: [] };
  }

  /* ---------- configuração dos três produtos ---------- */

      var CFG = {
    casal: {
      qtd: 2, minimo: 2,
      mapa: [["casalNome1", "casalNasc1", "casalApelido1"], ["casalNome2", "casalNasc2", "casalApelido2"]],
      extra: function () { return {}; }
    },
    familia: {
      qtd: 2, minimo: 1,
      principal: ["familiaPrincipalNome", "familiaPrincipalNasc", "familiaPrincipalApelido"],
      membro: ["familiaMembroNome", "familiaMembroNasc", "familiaMembroApelido"],
      extra: function () { return {}; }
    },
    compatibilidade_equipes: {
      qtd: 2, minimo: 1,
      principal: ["equipePrincipalNome", "equipePrincipalNasc", "equipePrincipalApelido"],
      membro: ["equipeMembroNome", "equipeMembroNasc", "equipeMembroApelido"],
      extra: function () {
        var e = (window._compEnergia && window._compEnergia !== "0") ? window._compEnergia : "8";
        return { energia: e };
      }
    }
  };
  function _porMapa(mapa) {
    var nomes = [], datas = [], apelidos = [];
    for (var i = 0; i < mapa.length; i++) {
      nomes.push(_valor([mapa[i][0]]));
      datas.push(_data([mapa[i][1]]));
      apelidos.push(mapa[i][2] ? _valor([mapa[i][2]]).replace(/[;|]/g, "") : "");
    }
    return { nomes: nomes, datas: datas, apelidos: apelidos };
  }
    
  function _porPrincipalMembro(principal, membro, max) {
    var nomes = [_valor([principal[0]])];
    var datas = [_data([principal[1]])];
    var apelidos = [principal[2] ? _valor([principal[2]]).replace(/[;|]/g, "") : ""];
    for (var i = 1; i <= max; i++) {
      var n = _valor([membro[0] + i]);
      var d = _data([membro[1] + i]);
      var a = membro[2] ? _valor([membro[2] + i]).replace(/[;|]/g, "") : "";
      if (!n && !d && !a) continue;
      if (!n || !d) return { erro: "incompleto", idx: i };
      nomes.push(n); datas.push(d); apelidos.push(a);
    }
    return { nomes: nomes, datas: datas, apelidos: apelidos };
  }

  function _faltando(r, minimo) {
    if (!r || r.erro) return true;
    var ok = 0;
    for (var i = 0; i < r.nomes.length; i++) {
      if (r.nomes[i] && r.datas[i]) ok++;
    }
    return ok < minimo;
  }

  function _coletar(produto) {
    var cfg = CFG[produto];
    var r = cfg.mapa
      ? _porMapa(cfg.mapa)
      : _porPrincipalMembro(cfg.principal, cfg.membro, cfg.qtd);

    if (_faltando(r, cfg.minimo)) {
      var m = _coletarDoModal(cfg.qtd);
      if (!_faltando(m, cfg.minimo)) r = m;
    }
    return r;
  }

  /* ---------- envio ---------- */
  function _msgPreencha() {
    var lang = (typeof getLang === "function") ? getLang() : "pt";
    var t = (typeof translations !== "undefined" && translations[lang]) || {};
    return t.preencha_dado || "Preencha os dados solicitados.";
  }

  function _enviar(produto, nomes, datas, extra, apelidos) {
    var lang = (typeof getLang === "function") ? getLang() : "pt";
    var ap = apelidos || [];
    var n = [], det = [];
    for (var i = 0; i < nomes.length; i++) {
      if (nomes[i] && datas[i]) {
        n.push(nomes[i]);
        det.push(ap[i] ? (datas[i] + ";" + ap[i]) : datas[i]);
      }
    }
    var qs = "/criar-checkout?produto=" + encodeURIComponent(produto)
      + "&nome=" + encodeURIComponent(n[0])
      + "&nascimento=" + encodeURIComponent(det[0].split(";")[0])
      + "&dado=" + encodeURIComponent(n.join("|"))
      + "&detalhe=" + encodeURIComponent(det.join("|"))
      + "&lang=" + encodeURIComponent(lang);

    var ex = extra || {};
    for (var k in ex) {
      if (Object.prototype.hasOwnProperty.call(ex, k) && ex[k] !== "" && ex[k] != null) {
        qs += "&" + encodeURIComponent(k) + "=" + encodeURIComponent(ex[k]);
      }
    }
    window.location.href = qs;
  }

  function _pagar(produto) {
    var cfg = CFG[produto];
    var r = _coletar(produto);
    if (_faltando(r, cfg.minimo)) { alert(_msgPreencha()); return; }
    _enviar(produto, r.nomes, r.datas, cfg.extra(), r.apelidos);
  }

  /* ---------- fachada pública ---------- */
  window.pagarCasal           = function () { _pagar("casal"); };
  window.pagarFamilia         = function () { _pagar("familia"); };
  window.pagarCompatibilidade = function () { _pagar("compatibilidade_equipes"); };
})();
