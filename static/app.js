// ===== A1ELOS GLOBAL NUMEROLOGY - APP.JS =====
// Funções de interface extraídas do index.html (13/08/2026)

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

// ===== COMPRAR =====
function comprar(produto) {
    const lang = getLang();
    var nome = (document.getElementById("calcNome") ? document.getElementById("calcNome").value : "").trim();
    var nasc = (document.getElementById("calcNasc") ? document.getElementById("calcNasc").value : "").trim();
    if (!nome || !nasc) {
        alert(translations[lang].preencha_dados || "Preencha nome e data de nascimento primeiro.");
        var sec = document.getElementById("calcSection") || document.getElementById("calculadora");
        if (sec) sec.scrollIntoView({ behavior: "smooth" });
        return;
    }
    if (typeof calcularMapa === "function") { calcularMapa(); }
    window.location.href = '/criar-checkout?lang=' + lang + '&produto=' + produto
        + '&nome=' + encodeURIComponent(nome) + '&nascimento=' + encodeURIComponent(nasc);
}

// ===== ENERGIAS =====
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
    var nome = (document.getElementById("calcNome") ? document.getElementById("calcNome").value : "").trim();
    var nasc = (document.getElementById("calcNasc") ? document.getElementById("calcNasc").value : "").trim();
    if (!nome || !nasc) {
        alert(translations[lang].preencha_dados || "Preencha nome e data de nascimento primeiro.");
        var sec = document.getElementById("calcSection") || document.getElementById("calculadora");
        if (sec) sec.scrollIntoView({ behavior: "smooth" });
        return;
    }
    window.location.href = '/criar-checkout?lang=' + lang + '&produto=ia&energia=' + n
        + '&nome=' + encodeURIComponent(nome) + '&nascimento=' + encodeURIComponent(nasc);
}

// ===== FORMULÁRIOS URNA / ELEITORAL =====
function toggleForm(tipo) {
    const fUrna = document.getElementById('form-urna');
    const fEle = document.getElementById('form-eleitoral');
    if (tipo === 'urna') {
        fEle.classList.add('hidden-form');
        fUrna.classList.toggle('hidden-form');
        fUrna.scrollIntoView({ behavior: 'smooth' });
    } else {
        fUrna.classList.add('hidden-form');
        fEle.classList.toggle('hidden-form');
        fEle.scrollIntoView({ behavior: 'smooth' });
    }
}
function pagarUrna() {
    const nome = document.getElementById('urnaNome').value.trim();
    if (!nome) { alert(translations[getLang()].alert_urna_nome || 'Informe o nome completo.'); return; }
    const lang = getLang();
    var cargo = (document.getElementById('urnaCargo') ? document.getElementById('urnaCargo').value : 'vereador');
    var qs = 'lang=' + lang + '&produto=urna&nome_completo=' + encodeURIComponent(nome) + '&cargo=' + encodeURIComponent(cargo);
    for (var i = 1; i <= 5; i++) {
        var v = (document.getElementById('urnaNome' + i) ? document.getElementById('urnaNome' + i).value : '').trim();
        if (v) qs += '&nome' + i + '=' + encodeURIComponent(v);
    }
    window.location.href = '/criar-checkout?' + qs;
}
function pagarEleitoral() {
    const nome = document.getElementById('eleiNome').value.trim();
    if (!nome) { alert(translations[getLang()].alert_eleitoral_nome || 'Informe o nome completo.'); return; }
    const lang = getLang();
    var cargo = (document.getElementById('eleiCargo') ? document.getElementById('eleiCargo').value : 'vereador');
    var sigla = (document.getElementById('eleiSigla') ? document.getElementById('eleiSigla').value : '').trim();
    window.location.href = '/criar-checkout?lang=' + lang + '&produto=eleitoral'
        + '&nome_completo=' + encodeURIComponent(nome)
        + '&cargo=' + encodeURIComponent(cargo)
        + '&numero=' + encodeURIComponent(sigla);
}

// ===== BÔNUS =====
function ativarBonusInserido() {
    var t = translations[getLang()] || translations.pt;
    var codigo = document.getElementById("biCodigo").value.trim();
    var st = document.getElementById("biStatus");
    if (!codigo) { st.style.color = "#dc3545"; st.textContent = t.alert_bonus_vazio; return; }
    st.style.color = "var(--gold)"; st.textContent = t.alert_bonus_validando;
    fetch("/ativar-bonus", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ codigo: codigo }) })
    .then(function(r) { return r.json(); })
    .then(function(data) {
        if (data.ok) { st.style.color = "#28a745"; st.textContent = t.alert_bonus_ok; setTimeout(function() { window.location.href = "/#" + data.target; }, 800); }
        else { st.style.color = "#dc3545"; st.textContent = t.alert_bonus_invalido; }
    })
    .catch(function() { st.style.color = "#dc3545"; st.textContent = t.alert_bonus_erro; });
}

// ===== MENSAGENS =====
function enviarMensagem() {
    var t = translations[getLang()] || translations.pt;
    var nome = document.getElementById("msgNome").value.trim();
    var texto = document.getElementById("msgTexto").value.trim();
    var st = document.getElementById("msgStatus");
    if (!texto) { st.style.color = "#dc3545"; st.textContent = t.alert_msg_vazia; return; }
    st.style.color = "var(--gold)"; st.textContent = t.alert_msg_enviando;
    fetch("/sugestao", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ nome: nome, mensagem: texto }) })
    .then(function(r){ return r.json(); })
    .then(function(d){ if (d.ok) { st.style.color = "#28a745"; st.textContent = t.alert_msg_ok; document.getElementById("msgTexto").value = ""; } else { st.style.color = "#dc3545"; st.textContent = t.alert_msg_erro; } })
    .catch(function(){ st.style.color = "#dc3545"; st.textContent = t.alert_msg_conexao; });
}

// ===== BÔNUS COLETIVO / EMPRESARIAL =====
var BC_PRODUTOS = [
    ["express","Mapa Express",8,"🔮"],["vida","Qual Vida/Ano",8,"🔢"],["completo","Mapa Completo",17,"📘"],
    ["ia","Pesquisa IA de Nomes",17,"🤖"],["urna","Validação Nome de Urna",26,"🗳️"],["eleitoral","Número Eleitoral",26,"🔢"],
    ["imovel","Número do Imóvel",26,"🏠"],["calendario","Calendário Mensal",26,"📅"],["artistico","Nome Artístico",35,"🎭"],
    ["bebe","Nome de Bebê",35,"👶"],["assinatura","Assinaturas",35,"✍️"],["negocio","Nome para Negócio",44,"🏪"],
    ["casal","Mapa do Casal",44,"💞"],["familia","Mapa Família Premium",98,"🌟"],
    ["nome_pet","Nome do Pet",8,"🐾"],["nickname","Nickname Digital",8,"🎮"],["nome_dominio","Nome do Domínio",8,"🌐"],
    ["nome_canal","Nome do Canal",8,"🎥"],["nome_equipe","Nome da Equipe",8,"🧭"],["nome_ong","Nome de ONG",8,"🏛️"],
    ["nome_projeto","Nome do Projeto",8,"📋"],["nome_evento","Nome do Evento",8,"🎪"]
];
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
    if (itens.length === 0) { alert(t.alert_bc_vazio); return; }
    var bruto = itens.reduce(function(a, i) { return a + i.preco * i.qtd; }, 0);
    var qtdTotal = itens.reduce(function(a, i) { return a + i.qtd; }, 0);
    var pct = descontoBC(qtdTotal);
    var final = bruto - Math.round(bruto * pct / 100);
    var simbolo = (PRECO_DISPLAY[getLang()] ? PRECO_DISPLAY[getLang()][0].replace(/[0-9.,\s]/g, '').trim() : '') || 'R$';
    var linhas = itens.map(function(i) {
        return t.bc_linha
            .replace('{nome}', i.nome).replace('{qtd}', i.qtd).replace('{simbolo}', simbolo)
            .replace('{preco}', i.preco).replace('{total}', (i.qtd * i.preco));
    }).join("\n");
    var msg = t.bc_resumo_titulo + "\n\n" + linhas + "\n\n"
        + t.bc_total + " " + simbolo + " " + bruto + "\n"
        + t.bc_discount + " (" + pct + "%): " + simbolo + " " + Math.round(bruto * pct / 100) + "\n"
        + t.bc_final + " " + simbolo + " " + final + "\n\n"
        + t.bc_confirmar_pag;
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
