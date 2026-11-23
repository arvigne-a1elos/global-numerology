# DECISÕES — A1ELOS Global Numerology

Registro das decisões fechadas. Se o código contrariar este arquivo,
o código está errado. Não reabra uma decisão sem registrar a nova data aqui.

---

## 2026-11-23 — Fonte de verdade de PREÇOS

**Hierarquia:** Stripe → `referencia/precos.py` → `/api/precos` → todo o resto.

- O Stripe decide quanto é cobrado. É a autoridade final.
- `referencia/precos.py` registra os valores. **É o único arquivo do projeto
  autorizado a conter número de preço.**
- `/api/precos` publica o que o registro diz. Não decide.
- `main.py`, `app.js`, `produtos.js`, `translations.js` e os scripts
  **consomem**. Nenhum declara preço, exibe preço ou guarda cópia.

**Casas decimais:** `JPY`, `VND`, `IDR` = 0 casas no nosso código.
Mapeamento único em `referencia/precos.py::CASAS`.

> Ressalva aberta: o Stripe trata IDR como **2 casas** (não está na lista
> oficial de zero-decimais). A tabela diz 0. Resolver antes de abrir a Indonésia.

**Exibição:** sempre de `/api/precos`. Proibido formatar preço no navegador.

**Conferência:** `python checar_precos.py` antes de cada commit.
Exit 1 bloqueia o deploy.

**Verificado em 23/11/2026:** Stripe, `precos.py` e `/api/precos` concordam
nas 6 faixas em JPY (¥1.376 / ¥2.924 / ¥4.472 / ¥6.020 / ¥7.568 / ¥16.856).

---

## 2026-11-23 — Fonte de verdade de CÁLCULO

**Hierarquia:** `referencia/cissay.py` → `produtos/mapa.py` → produtos.

- `cissay.py` guarda a matriz, `LETRAS_BASE`, `LETRAS_ESPECIAIS`, `reduzir`,
  `numero_pessoa`, `normalizar_nome`.
- `normalizar_nome`: **uma única definição**, e ela aplica `LETRAS_ESPECIAIS`.
  (Havia duas; a segunda sobrescrevia a primeira e ignorava 12 letras
  especiais — 9 dos 14 idiomas.)
- `casal.py`, `familia.py`, `equipe.py` importam os primitivos. Não redefinem.

---

## 2026-11-23 — PDFs de relação (Casal, Família, Equipes)

- Sem capa. As informações da capa vão nas folhas internas.
- Blocos contíguos, separados por linha ou título. Não abrir página por seção.
- Numeração no rodapé: "N de TOTAL".
- Fecho ("Documento sigiloso", ©) **no rodapé do canvas**, nunca como flowable.
- Blocos: nome completo → apelido → síntese comparativa.

---

## 2026-11-23 — Nomes de arquivo proibidos na raiz

`main_backup_precos.py`, `main_backup_precos_LOCAL.py`, `price_ids_teste.py`,
`apresentacao_textos.py`, `scripts/*_LOCAL.py`.
São cópias mortas que parecem autoridade. Se precisar guardar, use `_historico/`
(fora do versionamento).
