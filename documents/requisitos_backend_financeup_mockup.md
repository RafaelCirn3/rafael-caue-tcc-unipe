# Requisitos Funcionais de Back-end — FinanceUp

## 1. Visão Geral

O projeto FinanceUp é uma plataforma mobile-first de educação financeira com funcionalidades de controle financeiro pessoal, acompanhamento de metas, aprendizado gamificado e visualização didática de dados financeiros.

Com base no mockup disponibilizado no Lovable, os requisitos abaixo representam as necessidades de back-end necessárias para suportar a aplicação.

---

# 2. Requisitos Funcionais

## RF-001 — Cadastro de Usuário
O sistema deve permitir o cadastro de novos usuários utilizando:

- Nome
- E-mail
- Senha
- Foto de perfil (opcional)

### Regras
- O e-mail deve ser único.
- A senha deve ser armazenada utilizando hash seguro.
- O sistema deve validar formato de e-mail.

---

## RF-002 — Autenticação de Usuário
O sistema deve permitir autenticação via login.

### Funcionalidades
- Login com e-mail e senha
- Logout
- Renovação de sessão
- Recuperação de senha

### Regras
- Utilizar autenticação baseada em JWT ou sessão.
- Tokens expirados devem ser invalidados.

---

## RF-003 — Gerenciamento de Perfil
O sistema deve permitir que o usuário visualize e edite:

- Nome
- Foto
- Meta financeira
- Preferências
- Dados financeiros básicos

---

## RF-004 — Cadastro de Receitas
O sistema deve permitir cadastrar receitas financeiras.

### Campos
- Valor
- Categoria
- Descrição
- Data
- Tipo de receita

### Funcionalidades
- Criar receita
- Editar receita
- Excluir receita
- Listar receitas

---

## RF-005 — Cadastro de Despesas
O sistema deve permitir cadastrar despesas financeiras.

### Campos
- Valor
- Categoria
- Descrição
- Data
- Forma de pagamento

### Funcionalidades
- Criar despesa
- Editar despesa
- Excluir despesa
- Listar despesas

---

## RF-006 — Organização por Categorias
O sistema deve permitir categorizar receitas e despesas.

### Categorias esperadas
- Mercado
- Transporte
- Lazer
- Educação
- Saúde
- Investimentos
- Outros

### Funcionalidades
- Criar categoria personalizada
- Editar categoria
- Excluir categoria

---

## RF-007 — Dashboard Financeiro
O sistema deve fornecer um dashboard consolidado contendo:

- Saldo atual
- Total de receitas
- Total de despesas
- Economia do mês
- Percentual gasto
- Resumo mensal

### Funcionalidades
- Agrupar dados por período
- Calcular totais automaticamente
- Gerar indicadores financeiros

---

## RF-008 — Estatísticas Financeiras
O sistema deve gerar dados para gráficos financeiros.

### Gráficos previstos
- Receitas vs despesas
- Distribuição por categoria
- Evolução mensal
- Percentual de economia

### Regras
- Os dados devem ser agregados dinamicamente.
- O sistema deve permitir filtros por período.

---

## RF-009 — Controle de Metas Financeiras
O sistema deve permitir criar metas de economia.

### Campos
- Nome da meta
- Valor alvo
- Valor atual
- Data limite

### Funcionalidades
- Atualizar progresso
- Calcular percentual concluído
- Exibir previsão de conclusão

---

## RF-010 — Sistema Educacional
O sistema deve disponibilizar conteúdos educativos.

### Funcionalidades
- Listar trilhas de aprendizado
- Listar lições
- Marcar lição como concluída
- Exibir progresso semanal

### Tipos de conteúdo
- Artigos
- Dicas financeiras
- Curiosidades
- Conceitos financeiros

---

## RF-011 — Sistema de Progresso do Usuário
O sistema deve acompanhar o progresso educacional do usuário.

### Funcionalidades
- Quantidade de lições concluídas
- Percentual de progresso
- Histórico de aprendizado
- Sequência semanal

---

## RF-012 — Feed de Dicas Financeiras
O sistema deve disponibilizar dicas financeiras dinâmicas.

### Funcionalidades
- Exibir dica diária
- Rotacionar conteúdos
- Personalizar por perfil

---

## RF-013 — Persistência de Dados Financeiros
O sistema deve armazenar:

- Histórico financeiro
- Movimentações
- Categorias
- Metas
- Dados educacionais

### Regras
- Dados devem ser vinculados ao usuário autenticado.
- O histórico não deve ser perdido após logout.

---

## RF-014 — Filtros Financeiros
O sistema deve permitir filtrar movimentações.

### Filtros previstos
- Período
- Categoria
- Tipo
- Valor

---

## RF-015 — Notificações
O sistema deve permitir envio de notificações.

### Tipos
- Lembrete de meta
- Nova dica financeira
- Conclusão de meta
- Alertas financeiros

---

## RF-016 — API de Indicadores Financeiros
O sistema deve fornecer endpoints consolidados para o dashboard.

### Indicadores
- Saldo mensal
- Total de receitas
- Total de despesas
- Percentual economizado
- Categorias mais utilizadas

---

## RF-017 — Histórico Mensal
O sistema deve manter histórico financeiro por competência mensal.

### Funcionalidades
- Consultar meses anteriores
- Comparar períodos
- Gerar evolução financeira

---

## RF-018 — Controle de Sessão
O sistema deve controlar sessões ativas do usuário.

### Funcionalidades
- Encerrar sessões
- Detectar expiração
- Renovar autenticação

---

# 3. Regras de Negócio

## RN-001
Cada movimentação financeira deve pertencer a um único usuário.

## RN-002
O saldo do usuário deve ser calculado automaticamente:

Saldo = Receitas − Despesas

## RN-003
O percentual de economia deve ser calculado mensalmente.

## RN-004
Uma meta financeira não pode possuir valor alvo menor ou igual a zero.

## RN-005
Lições educacionais concluídas devem ser persistidas individualmente por usuário.

## RN-006
Categorias excluídas não devem remover movimentações antigas.

## RN-007
Os gráficos devem refletir dados em tempo real.

---

# 4. Entidades de Back-end

## Usuário
- id
- nome
- email
- senha_hash
- avatar
- created_at
- updated_at

## Receita
- id
- usuario_id
- valor
- categoria_id
- descricao
- data

## Despesa
- id
- usuario_id
- valor
- categoria_id
- descricao
- data
- forma_pagamento

## Categoria
- id
- usuario_id
- nome
- tipo

## MetaFinanceira
- id
- usuario_id
- nome
- valor_meta
- valor_atual
- data_limite

## ConteudoEducacional
- id
- titulo
- descricao
- tipo
- duracao

## ProgressoEducacional
- id
- usuario_id
- conteudo_id
- concluido
- data_conclusao

---

# 5. APIs Necessárias

## Autenticação
- POST /auth/register
- POST /auth/login
- POST /auth/logout
- POST /auth/refresh
- POST /auth/forgot-password

## Usuários
- GET /users/me
- PUT /users/me

## Receitas
- GET /receitas
- POST /receitas
- PUT /receitas/{id}
- DELETE /receitas/{id}

## Despesas
- GET /despesas
- POST /despesas
- PUT /despesas/{id}
- DELETE /despesas/{id}

## Categorias
- GET /categorias
- POST /categorias
- PUT /categorias/{id}
- DELETE /categorias/{id}

## Dashboard
- GET /dashboard/resumo
- GET /dashboard/graficos

## Metas
- GET /metas
- POST /metas
- PUT /metas/{id}
- DELETE /metas/{id}

## Educação Financeira
- GET /conteudos
- GET /conteudos/{id}
- POST /conteudos/{id}/concluir

---

# 6. Requisitos Não Funcionais Relacionados ao Back-end

## RNF-001 — Segurança
- Utilizar criptografia de senha.
- Utilizar HTTPS.
- Implementar proteção contra acesso não autorizado.

## RNF-002 — Performance
- Endpoints do dashboard devem responder rapidamente.
- Consultas agregadas devem ser otimizadas.

## RNF-003 — Escalabilidade
- Estrutura preparada para múltiplos usuários.
- APIs desacopladas do front-end.

## RNF-004 — Persistência
- Dados devem ser persistidos em banco relacional.

## RNF-005 — Auditoria
- Registrar data de criação e atualização das entidades.

---

# 7. Tecnologias de Back-end Recomendadas

## API
- Django REST Framework
- FastAPI
- NestJS

## Banco de Dados
- PostgreSQL

## Autenticação
- JWT

## Cache
- Redis

## Filas
- Celery ou BullMQ

---

# 8. Conclusão

O mockup do FinanceUp exige um back-end voltado principalmente para:

- autenticação;
- gerenciamento financeiro;
- cálculos analíticos;
- persistência de histórico;
- acompanhamento educacional;
- geração de indicadores e gráficos.

A arquitetura recomendada deve priorizar APIs REST desacopladas, modelagem relacional consistente e agregações financeiras otimizadas para alimentar dashboards em tempo real.

