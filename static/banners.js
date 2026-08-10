/* ===== BANNERS - ARQUIVO ISOLADO =====
   Não depende do script do site.
   Se falhar, o site continua funcionando normalmente. */
(function(){
  var LISTA = [];
  var CSS = ".a1-zona{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;max-width:1200px;margin:18px auto;padding:0 16px}"
          + ".a1-banner{flex:1 1 340px;max-width:560px;min-height:90px;border-radius:10px;overflow:hidden;background:#111;display:flex;align-items:center;justify-content:center}"
          + ".a1-banner img{width:100%;height:auto;display:block;border-radius:10px}";
  function injetarCSS(){
    var st = document.createElement("style");
    st.textContent = CSS;
    document.head.appendChild(st);
  }
  function gruposPorPosicao(){
    var g = {};
    LISTA.forEach(function(b){ if(!b.ativo) return; (g[b.posicao] = g[b.posicao] || []).push(b); });
    return g;
  }
  function render(){
    var g = gruposPorPosicao();
    ["topo","central","base"].forEach(function(pos){
      var zona = document.getElementById("zona" + pos.charAt(0).toUpperCase() + pos.slice(1));
      var itens = g[pos] || [];
      if(!zona || itens.length === 0) return;
      zona.innerHTML = "";
      itens.forEach(function(b, i){
        var div = document.createElement("div");
        div.className = "a1-banner";
        div.dataset.pos = pos;
        div.dataset.idx = String(i);
        div.innerHTML = '<a href="' + (b.url_anunciante || "#") + '" target="_blank" rel="noopener">'
                      + '<img src="' + b.imagem_url + '" alt="' + (b.marca || "Banner") + '"></a>';
        zona.appendChild(div);
      });
    });
  }
  function rotacionar(){
    var g = gruposPorPosicao();
    document.querySelectorAll(".a1-banner").forEach(function(el){
      var pos = el.dataset.pos;
      var idx = parseInt(el.dataset.idx, 10);
      var itens = g[pos] || [];
      if(itens.length < 2) return;
      var img = el.querySelector("img");
      if(!img) return;
      var prox = itens[(idx + 1) % itens.length].imagem_url;
      el.dataset.idx = String((idx + 1) % itens.length);
      img.setAttribute("src", prox);
    });
  }
  function iniciar(){
    injetarCSS();
    fetch("/static/banners.json")
      .then(function(r){ return r.json(); })
      .then(function(data){
        LISTA = data || [];
        render();
        setInterval(rotacionar, 8000);
      })
      .catch(function(){ /* banners fora do ar nunca derrubam o site */ });
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", iniciar);
  } else {
    iniciar();
  }
})();
