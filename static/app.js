// ===== A1ELOS GLOBAL NUMEROLOGY - APP.JS (VERSÃO CONSOLIDADA) =====
// ================================================================
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
      if (typeof montarTudo === "function") montarTudo();
      else if (typeof traduzirTudo === "function") traduzirTudo();
      atualizarLinkInvestidores();   // ← CHAMA a função global
      var ativos = container.querySelectorAll('.lang-btn');
      for (var i = 0; i < ativos.length; i++) ativos[i].classList.remove('active');
      b.classList.add('active');
    };
    container.appendChild(b);
  });
}
function pagarVida(){var n=document.getElementById('vidaNome').value.trim(),b=document.getElementById('vidaNasc').value;if(!n||!b){alert(t_preencha());return;}location.href='/criar-checkout?produto=vida&nome='+encodeURIComponent(n)+'&nascimento='+encodeURIComponent(b)+'&lang='+getLang();}
function pagarIa(){var n=document.getElementById('iaNome').value.trim(),e=document.getElementById('iaEnergia').value;if(!n||!e){alert(t_preencha());return;}location.href='/criar-checkout?produto=ia&nome='+encodeURIComponent(n)+'&energia='+encodeURIComponent(e)+'&lang='+getLang();}
function pagarImovel(){var n=document.getElementById('imovelNumero').value.trim();if(!n){alert(t_preencha());return;}location.href='/criar-checkout?produto=imovel&dado='+encodeURIComponent(n)+'&lang='+getLang();}
function pagarCalendario(){var n=document.getElementById('calNome').value.trim(),m=document.getElementById('calMes').value;if(!n||!m){alert(t_preencha());return;}location.href='/criar-checkout?produto=calendario&nome='+encodeURIComponent(n)+'&dado='+encodeURIComponent(m)+'&lang='+getLang();}
function pagarArtistico(){var n=document.getElementById('artNome').value.trim();if(!n){alert(t_preencha());return;}location.href='/criar-checkout?produto=artistico&dado='+encodeURIComponent(n)+'&lang='+getLang();}
function pagarBebe(){var n=document.getElementById('bebeSobrenome').value.trim(),e=document.getElementById('bebeEnergia').value;if(!n||!e){alert(t_preencha());return;}location.href='/criar-checkout?produto=bebe&dado='+encodeURIComponent(n)+'&energia='+encodeURIComponent(e)+'&lang='+getLang();}
function pagarAssinatura(){var n=document.getElementById('assinaturaTexto').value.trim();if(!n){alert(t_preencha());return;}location.href='/criar-checkout?produto=assinatura&dado='+encodeURIComponent(n)+'&lang='+getLang();}
function pagarNegocio(){var n=document.getElementById('negocioNome').value.trim(),e=document.getElementById('negocioEnergia').value;if(!n||!e){alert(t_preencha());return;}location.href='/criar-checkout?produto=negocio&dado='+encodeURIComponent(n)+'&energia='+encodeURIComponent(e)+'&lang='+getLang();}
function pagarCasal(){var n1=document.getElementById('casalNome1').value.trim(),n2=document.getElementById('casalNome2').value.trim();if(!n1||!n2){alert(t_preencha());return;}location.href='/criar-checkout?produto=casal&dado='+encodeURIComponent(n1+' & '+n2)+'&lang='+getLang();}
function pagarFamilia(){var n=document.getElementById('familiaMembros').value.trim();if(!n){alert(t_preencha());return;}location.href='/criar-checkout?produto=familia&dado='+encodeURIComponent(n)+'&lang='+getLang();}
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
...
+ '&numero_existente=' + encodeURIComponent(existente) 
  var nome = (document.getElementById('eleiNome') ? document.getElementById('eleiNome').value : '').trim();
  var cargo = (document.getElementById('eleiCargo') ? document.getElementById('eleiCargo').value : '').trim();
  var sigla = (document.getElementById('eleiSigla') ? document.getElementById('eleiSigla').value : '').trim();
  if (!nome || !sigla) { alert(t_preencha()); return; }
  location.href = '/criar-checkout?produto=eleitoral&nome_completo=' + encodeURIComponent(nome)
    + '&cargo=' + encodeURIComponent(cargo)
    + '&numero=' + encodeURIComponent(sigla)
    + '&lang=' + getLang();
};
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
function abrirModalDado(produto, lang) {
  var t = translations[lang] || translations.pt;
  var label = (DADO_LABEL[lang] && DADO_LABEL[lang][produto]) ? DADO_LABEL[lang][produto] : DADO_LABEL.pt[produto];
  var titulo = (PRODUTOS_TRAD[lang] && PRODUTOS_TRAD[lang][produto]) ? PRODUTOS_TRAD[lang][produto] : produto;  // ← DEFINIR
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
  }
  // ✅ FIX: reatribui o onclick a CADA abertura (evita capturar o 1º produto)
  document.getElementById("modalDadoOk").onclick = function(){ confirmarModalDado(produto, lang); };
  document.getElementById("modalDadoTitulo").textContent = titulo;
  document.getElementById("modalDadoLabel").textContent = label;
   // Monta passos
  window._modalDado = { produto: produto, lang: lang, tipo: "", energia: "" };
  montarPassoTipo(produto, lang);
  overlay.classList.add("active");
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
function montarPassoTipo(produto, lang) {
  var t = translations[lang] || translations.pt;
  document.getElementById("modalPassoTipo").style.display = "block";
  document.getElementById("modalPassoEnergia").style.display = "none";
  document.getElementById("modalPassoNome").style.display = "none";
  var conf = CONF_COLETA[produto] || {};
  var label = (t.f_tipo || "Tipo") + ":";
  document.getElementById("modalTipoLabel").textContent = label;
  var box = document.getElementById("modalTipoOpcoes");
  box.innerHTML = "";
  (conf.tipos || []).forEach(function(ch) {
    var b = document.createElement("button");
    b.className = "btn btn-full";
    b.textContent = tradOpcao(ch);
    b.onclick = function(){ _modalDado.tipo = ch; montarPassoEnergia(produto, lang); };
    box.appendChild(b);
  });
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
  // aproveita nome/data da calculadora se já preenchidos
  var nome = (document.getElementById("calcNome") ? document.getElementById("calcNome").value : "").trim();
  var nasc = (document.getElementById("calcNasc") ? document.getElementById("calcNasc").value : "").trim();
  if (nome) qs += '&nome=' + encodeURIComponent(nome);
  if (nasc) qs += '&nascimento=' + encodeURIComponent(nasc);
  window.location.href = '/criar-checkout?' + qs;
}
// ===== TOGGLE FORM (mostra/oculta um formulário) — usada pelos botões "Iniciar Validação" etc. =====
function toggleForm(formId) {
  var el = document.getElementById(formId);
  if (!el) return;
  var escondido = (el.style.display === 'none' || el.style.display === '');
  el.style.display = escondido ? 'block' : 'none';
  if (escondido) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
}
// ===== ENVIAR MENSAGEM / ATIVAR BÔNUS (adicionadas — padrão do arquivo) =====
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
// ===== MONTAR TUDO (consolidado e blindado) =====
function montarTudo() {
  if (typeof montarTabelaBC === "function") {
    console.log("[A1ELOS] montarTabelaBC() EXECUTANDO");
    montarTabelaBC();
  } else {
    console.warn("[A1ELOS] montarTabelaBC NÃO encontrada");
  }
  if (typeof montarEnergias === "function") {
    console.log("[A1ELOS] montarEnergias() EXECUTANDO");
    montarEnergias();
  } else {
    console.warn("[A1ELOS] montarEnergias NÃO encontrada");
  }
  // Re-traduz TUDO agora que as seções existem (BC + energias + cards)
  if (typeof traduzirTudo === "function") traduzirTudo();
}
// ===== INICIALIZAÇÃO =====
function init() {
  var savedLang = localStorage.getItem('lang');
  var browserLang = navigator.language.split('-')[0];
  var defaultLang = savedLang || (translations[browserLang] ? browserLang : 'pt');
  montarSeletorIdioma();
  setLanguage(defaultLang);
  carregarPartials();   // ← injeta os cards e depois chama montarTudo()
}
// ===== INICIALIZAÇÃO AUTOMÁTICA GARANTIDA (única via de disparo) =====
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
