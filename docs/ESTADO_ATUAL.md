# ESTADO ATUAL — A1ELOS GLOBAL NUMEROLOGY

**Última atualização:** 09/11/2026
**Fase:** final de configuração (24 produtos × 14 idiomas)
**Ambiente:** Stripe em modo TESTE — não trocar para live antes de fechar os testes

## Números
- Pendências ativas: 49
- Prioridade P1 (dinheiro e causa-raiz): 5
- Pendências retiradas por triagem: 5
- Produtos testados: 1 de 24 (Mapa Express, em ja/ru/ar/vi)
- Deploys bem-sucedidos: 30
- Último commit: a1f6f9a

## Os 5 itens P1
| ID | Pendência | Ação |
|----|-----------|------|
| P-44 | Tabela de desconto com 20%/25% (oficial é 15%/20%) | Corrigir nos 3 arquivos: app.js, main.py, produtos.js |
| P-47 | IDs duplicados no card 23 (equipeEnergiaSel) | Renomear para compEquipeEnergiaSel no produtos.html |
| P-48 | pagarCompatibilidade() não existe | Criar a função no produtos.js |
| P-49 | BC_PRODUTOS pode não ter o produto 24 | Verificar e adicionar a linha a R$ 98 |
| P-50 | PRODUTO_FAIXA duplicado no translations.js | Corrigir a segunda cópia |

## O que está validado
- Checkout ponta a ponta em 4 idiomas (ja, ru, ar, vi)
- PDF com fontes corretas, incluindo RTL árabe e hebraico
- 336 preços no Stripe (24 produtos × 14 idiomas), dedup provado
- PRICE_IDS integrados no main.py
- Colheita da UI 20/20 (221.494 caracteres)
- Persistência SQLite (numerologia.db + .gitignore)
- Apresentação com 14 idiomas × 107 chaves idênticas

## O que está travado
- Produto 24 (Compatibilidade de Equipes): card não completa a compra por causa dos IDs duplicados (P-47)
- Tabela de desconto: cliente vê 20% na faixa de 50 unidades, mas a decisão oficial é 15% (P-44)

## Próximo passo
Bloco 1 — corrigir a tabela de desconto (P-44) nos três arquivos.

## Arquitetura de repositórios (decidido em 11/11/2026)

Cada projeto mantém a própria governança. Não há repositório central.

- **global-numerology** → governança da nave (este repositório)
- **Ex-Libris-Est** → governança da biblioteca
- **a1elos-governanca** → governança do Disco (privado)

Arquivos de governança da nave vivem em `docs/`:
`ESTADO_ATUAL.md`, `DECISOES.md`, `COMO_RETOMAR.md`, `controle/`, `relatorios/`.
