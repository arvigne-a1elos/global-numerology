/* ============================================================
   translations.js — A1ELOS Global Numerology
   Módulo de tradução (12 idiomas, 15 produtos)
   Carregar ANTES do script principal do index.html
   ============================================================ */

// ===== IDIOMAS DISPONÍVEIS (12) =====
const languages = [
    { code: 'pt', name: 'PT', flag: '🇧🇷' },
    { code: 'en', name: 'EN', flag: '🇺🇸' },
    { code: 'es', name: 'ES', flag: '🇪🇸' },
    { code: 'it', name: 'IT', flag: '🇮🇹' },
    { code: 'fr', name: 'FR', flag: '🇫🇷' },
    { code: 'de', name: 'DE', flag: '🇩🇪' },
    { code: 'ja', name: 'JA', flag: '🇯🇵' },
    { code: 'zh', name: 'ZH', flag: '🇨🇳' },
    { code: 'ru', name: 'RU', flag: '🇷🇺' },
    { code: 'hi', name: 'HI', flag: '🇮🇳' },
    { code: 'he', name: 'HE', flag: '🇮🇱' },
    { code: 'ar', name: 'AR', flag: '🇸🇦' }
];

// ===== TRADUÇÕES (12 IDIOMAS) =====
const translations = {
    pt: { hero_title: "MAPA NUMEROLÓGICO", hero_subtitle: "Descubra o que os números revelam sobre você", hero_desc: "Uma jornada de autoconhecimento baseada na numerologia pitagórica. Seu mapa pessoal revela talentos, desafios e caminhos através dos números que regem sua vida.", hero_btn: "✦ GERAR MEU MAPA", hero_btn2: "VER PRODUTOS", section_what_title: "O que é o Mapa Numerológico?", section_what_subtitle: "Uma ferramenta de autoconhecimento baseada na numerologia pitagórica", card1_title: "Números da Sua Vida", card1_desc: "Calculamos o Caminho da Vida, Destino, Alma, Realização e outros números essenciais a partir da sua data de nascimento e nome completo.", card2_title: "Seu Mapa Pessoal", card2_desc: "Cada número revela uma dimensão única da sua personalidade, talentos inatos, desafios e oportunidades ao longo da vida.", card3_title: "Relatório Completo", card3_desc: "Você recebe um relatório detalhado em PDF com a interpretação profissional de cada número do seu mapa, pronto para download.", card4_title: "Orientação Prática", card4_desc: "Mais que uma leitura, um guia para tomar decisões alinhadas com seus ciclos numerológicos e seu propósito de vida.", section_how_title: "Como Funciona", section_how_subtitle: "Em poucos passos, seu mapa está pronto", step1_title: "Insira seus dados", step1_desc: "Informe seu nome completo e data de nascimento — as duas chaves para o seu mapa numerológico.", step2_title: "Cálculo automatizado", step2_desc: "Nossa engine calcula todos os números fundamentais da numerologia pitagórica com precisão.", step3_title: "Relatório em PDF", step3_desc: "Receba um relatório profissional e elegante com a interpretação completa do seu mapa.", section_products_title: "Produtos e Serviços", section_products_subtitle: "Escolha o produto ideal para sua análise numerológica", buy_btn: "Comprar", recommended: "RECOMENDADO", premium: "PREMIUM", sob_consulta: "Sob consulta", know_more: "Saiba Mais", start_urna: "Iniciar Validação", start_eleitoral: "Calcular Nº Eleitoral", urna_title: "Validação do Nome de Urna", urna_sub: "5 tentativas + cálculo letra a letra + PDF sigiloso — R$ 26", f_nome: "Nome Completo da Pessoa", f_cargo: "Cargo em Disputa", f_email: "Email (resultado sigiloso)", urna_options: "Insira até 5 opções de nome de candidato:", pay_urna: "🔒 Pagar R$ 26 — Resultado por Email", eleitoral_title: "Cálculo do Número Eleitoral", eleitoral_sub: "Sugestões com energia 8 para sua candidatura — R$ 26", f_cargo2: "Cargo", c_vereador: "Vereador", c_estadual: "Dep. Estadual", c_federal: "Dep. Federal", c_senador: "Senador", f_sigla: "Número da Sigla Partidária (2 dígitos)", f_existente: "Número já existente (opcional)", pay_eleitoral: "🔒 Pagar R$ 26 — Sugestões por Email", bi_title: "🎁 Ativar Código Bônus", bi_sub: "Recebeu um código? Insira abaixo e ative para gerar seu presente — sem pagamento.", bi_label: "Código Bônus", bi_btn: "🎁 Ativar Código", bc_title: "🏢 Bônus Coletivo / Empresarial", bc_sub: "Contrate brindes numerológicos para seus clientes ou funcionários. Escolha um plano pronto ou monte sob medida. Descontos de 10% a 70%.", bc_plans_title: "Planos Prontos", bc_plan1_name: "Plano Básico", bc_plan1_price: "50 códigos", bc_plan1_desc: "50x Mapa Express (R$ 8) — ideal para presentear clientes", bc_plan2_name: "Plano Intermediário", bc_plan2_price: "100 códigos", bc_plan2_desc: "50x Mapa Express + 50x Pesquisa IA (R$ 17) — para equipes", bc_plan3_name: "Plano Premium", bc_plan3_price: "200 códigos", bc_plan3_desc: "100x Mapa Express + 100x Mapa Completo (R$ 17) — programas completos", select: "Selecionar", bc_custom_title: "Montar Sob Medida", bc_custom_sub: "Marque a quantidade desejada de cada serviço. O desconto é aplicado automaticamente.", bc_tbl_service: "Serviço", bc_tbl_price: "Valor", bc_tbl_qty: "Quantidade", bc_total: "Total bruto:", bc_discount: "Desconto aplicado:", bc_final: "Total final:", bc_confirm: "📋 Confirmar Resumo e Ir para Pagamento", inv_title: "Investidores e Parceiros", inv_sub: "Baixe a apresentação empresarial da A1ELOS no seu idioma, gratuitamente.", download: "Baixar PDF", section_numbers_title: "Os Números no Centro", section_numbers_subtitle: "Cada número de 1 a 9 carrega uma energia única", numbers_masters: "✦ Números Mestres 11, 22 e 33 também são considerados ✦", cta_title: "Pronto para descobrir seu caminho?", cta_desc: "Seu mapa numerológico pessoal está a poucos cliques de distância.", cta_btn1: "✦ GERAR MAPA GRÁTIS", cta_btn2: "CONHEÇA A A1ELOS", footer_text: "© 2026 A1ELOS Assessoria e Consultoria. Todos os direitos reservados." },
    en: { hero_title: "NUMEROLOGICAL MAP", hero_subtitle: "Discover what numbers reveal about you", hero_desc: "A self-discovery journey based on Pythagorean numerology. Your personal map reveals talents, challenges, and paths through the numbers that rule your life.", hero_btn: "✦ GENERATE MY MAP", hero_btn2: "VIEW PRODUCTS", section_what_title: "What is the Numerological Map?", section_what_subtitle: "A self-discovery tool based on Pythagorean numerology", card1_title: "Numbers of Your Life", card1_desc: "We calculate Life Path, Destiny, Soul, Realization and other essential numbers from your birth date and full name.", card2_title: "Your Personal Map", card2_desc: "Each number reveals a unique dimension of your personality, innate talents, challenges and opportunities throughout life.", card3_title: "Complete Report", card3_desc: "You receive a detailed PDF report with professional interpretation of each number in your map, ready for download.", card4_title: "Practical Guidance", card4_desc: "More than a reading, a guide to make decisions aligned with your numerological cycles and life purpose.", section_how_title: "How It Works", section_how_subtitle: "In a few steps, your map is ready", step1_title: "Enter your data", step1_desc: "Enter your full name and birth date — the two keys to your numerological map.", step2_title: "Automated Calculation", step2_desc: "Our engine calculates all fundamental Pythagorean numerology numbers with precision.", step3_title: "PDF Report", step3_desc: "Receive a professional and elegant report with the complete interpretation of your map.", section_products_title: "Products & Services", section_products_subtitle: "Choose the ideal product for your numerology analysis", buy_btn: "Buy", recommended: "RECOMMENDED", premium: "PREMIUM", sob_consulta: "On request", know_more: "Learn More", start_urna: "Start Validation", start_eleitoral: "Calculate Electoral Nº", urna_title: "Ballot Name Validation", urna_sub: "5 attempts + letter-by-letter calculation + confidential PDF — US$ 5", f_nome: "Full Name", f_cargo: "Position in Dispute", f_email: "Email (confidential result)", urna_options: "Enter up to 5 candidate name options:", pay_urna: "🔒 Pay US$ 5 — Result by Email", eleitoral_title: "Electoral Number Calculation", eleitoral_sub: "Suggestions with energy 8 for your candidacy — US$ 5", f_cargo2: "Position", c_vereador: "City Councilor", c_estadual: "State Deputy", c_federal: "Federal Deputy", c_senador: "Senator", f_sigla: "Party Acronym Number (2 digits)", f_existente: "Existing number (optional)", pay_eleitoral: "🔒 Pay US$ 5 — Suggestions by Email", bi_title: "🎁 Activate Bonus Code", bi_sub: "Got a code? Enter it below and activate to generate your gift — no payment.", bi_label: "Bonus Code", bi_btn: "🎁 Activate Code", bc_title: "🏢 Corporate / Group Bonus", bc_sub: "Hire numerology gifts for your clients or employees. Choose a ready plan or build custom. Discounts from 10% to 70%.", bc_plans_title: "Ready Plans", bc_plan1_name: "Basic Plan", bc_plan1_price: "50 codes", bc_plan1_desc: "50x Express Map (US$ 1.50) — ideal for gifting clients", bc_plan2_name: "Intermediate Plan", bc_plan2_price: "100 codes", bc_plan2_desc: "50x Express Map + 50x AI Search (US$ 3.50) — for teams", bc_plan3_name: "Premium Plan", bc_plan3_price: "200 codes", bc_plan3_desc: "100x Express Map + 100x Complete Map (US$ 3.50) — full programs", select: "Select", bc_custom_title: "Build Custom", bc_custom_sub: "Set the desired quantity of each service. The discount is applied automatically.", bc_tbl_service: "Service", bc_tbl_price: "Price", bc_tbl_qty: "Quantity", bc_total: "Gross total:", bc_discount: "Discount applied:", bc_final: "Final total:", bc_confirm: "📋 Confirm Summary and Pay", inv_title: "Investors & Partners", inv_sub: "Download the A1ELOS business presentation in your language, free.", download: "Download PDF", section_numbers_title: "The Numbers at the Core", section_numbers_subtitle: "Each number from 1 to 9 carries a unique energy", numbers_masters: "✦ Master Numbers 11, 22 and 33 are also considered ✦", cta_title: "Ready to discover your path?", cta_desc: "Your personal numerological map is just a few clicks away.", cta_btn1: "✦ GENERATE FREE MAP", cta_btn2: "DISCOVER A1ELOS", footer_text: "© 2026 A1ELOS Assessoria e Consultoria. All rights reserved." }
    // ... (os outros 10 idiomas: es, it, fr, de, ja, zh, ru, hi, he, ar — cole os que você já tem no seu arquivo)
};

// ===== NOMES DOS 15 PRODUTOS (12 IDIOMAS) =====
const PRODUTOS_TRAD = {
    pt: { express:"Mapa Express", vida:"Qual Vida/Ano", completo:"Mapa Completo", ia:"Pesquisa IA de Nomes", urna:"Validação Nome de Urna", eleitoral:"Número Eleitoral", imovel:"Número do Imóvel", calendario:"Calendário Mensal Energético", artistico:"Validação Nome Artístico", bebe:"Planejamento Nome de Bebê", assinatura:"Validação de Assinaturas", negocio:"Nome para Negócio/Produto", casal:"Mapa do Casal", familia:"Mapa Família Premium", coletivo:"Bônus Coletivo/Empresarial" }
    // ... (os outros 11 idiomas — cole os que você já tem)
};

// ===== PREÇOS POR IDIOMA =====
const PRODUTO_FAIXA = { express:0, vida:0, completo:1, ia:1, urna:2, eleitoral:2, imovel:2, calendario:2, artistico:3, bebe:3, assinatura:3, negocio:4, casal:4, familia:5 };

const PRECO_DISPLAY = {
    pt: ["R$ 8","R$ 17","R$ 26","R$ 35","R$ 44","R$ 98"]
    // ... (os outros 11 idiomas — cole os que você já tem)
};

// ===== FUNÇÕES DE IDIOMA =====
function getLang() {
    return localStorage.getItem('selectedLang') || 'pt';
}
function setLanguage(lang) {
    localStorage.setItem('selectedLang', lang);
    document.querySelectorAll('.lang-btn').forEach(function(btn) {
        btn.classList.toggle('active', btn.dataset.lang === lang);
    });
    var isRTL = ['ar', 'he'].includes(lang);
    document.documentElement.dir = isRTL ? 'rtl' : 'ltr';
    document.documentElement.lang = lang;
    document.querySelectorAll('[data-i18n]').forEach(function(el) {
        var key = el.getAttribute('data-i18n');
        if (translations[lang] && translations[lang][key]) {
            el.innerText = translations[lang][key];
        }
    });
    document.querySelectorAll('.product-card[data-prod]').forEach(function(card) {
        var prod = card.getAttribute('data-prod');
        var nomeEl = card.querySelector('.prod-nome');
        if (nomeEl && PRODUTOS_TRAD[lang] && PRODUTOS_TRAD[lang][prod]) {
            nomeEl.innerText = PRODUTOS_TRAD[lang][prod];
        }
        var precoEl = card.querySelector('.prod-preco');
        if (precoEl && PRODUTO_FAIXA[prod] !== undefined) {
            precoEl.innerText = PRECO_DISPLAY[lang][PRODUTO_FAIXA[prod]];
        }
    });
}
function traduzir() {
    var lang = getLang();
    document.querySelectorAll('[data-i18n]').forEach(function(el) {
        var chave = el.getAttribute('data-i18n');
        if (translations[lang] && translations[lang][chave]) {
            el.textContent = translations[lang][chave];
        }
    });
}
