# FinanceUp Backend

Backend em Django REST Framework para a plataforma FinanceUp, focado em autenticação, controle financeiro pessoal, metas, educação financeira, notificações e indicadores para dashboard.

## Visão Geral

Este projeto implementa a camada de API do FinanceUp com:

- autenticação JWT;
- cadastro e atualização de usuário;
- receitas, despesas e categorias;
- metas financeiras;
- dashboard com totais e gráficos;
- conteúdos educacionais e progresso do usuário;
- base para notificações e tarefas assíncronas.

## Stack

- Django
- Django REST Framework
- PostgreSQL
- JWT com Simple JWT
- Celery
- Redis
- drf-spectacular para documentação OpenAPI

## Requisitos Funcionais Cobertos

O backend foi estruturado para atender os requisitos do documento de requisitos do FinanceUp, incluindo:

- cadastro e autenticação de usuários;
- recuperação de senha;
- gerenciamento de perfil;
- receitas e despesas;
- categorias personalizadas e padrão;
- dashboard consolidado;
- gráficos financeiros;
- metas financeiras;
- conteúdos educacionais;
- progresso educacional por usuário;
- notificações e base para automações.

## Estrutura do Projeto

- backend: configuração principal do Django
- apps/accounts: autenticação, usuário, perfil e recuperação de senha
- apps/financial_aux: finanças, categorias, metas, notificações e dashboard
- apps/education: conteúdos educacionais e progresso
- apps/gamification: base para gamificação
- apps/simulations: base para simulações
- apps/investiments: base para investimentos

## Principais Endpoints

Autenticação:

- POST /api/v1/auth/register/
- POST /api/v1/auth/login/
- POST /api/v1/auth/logout/
- POST /api/v1/auth/refresh/
- POST /api/v1/auth/forgot-password/
- POST /api/v1/auth/reset-password/

Usuário:

- GET /api/v1/users/me/
- PUT /api/v1/users/me/
- PATCH /api/v1/users/me/

Finanças:

- GET /api/v1/receitas/
- POST /api/v1/receitas/
- GET /api/v1/receitas/{id}/
- PUT /api/v1/receitas/{id}/
- PATCH /api/v1/receitas/{id}/
- DELETE /api/v1/receitas/{id}/
- GET /api/v1/despesas/
- POST /api/v1/despesas/
- GET /api/v1/despesas/{id}/
- PUT /api/v1/despesas/{id}/
- PATCH /api/v1/despesas/{id}/
- DELETE /api/v1/despesas/{id}/
- GET /api/v1/categorias/
- POST /api/v1/categorias/
- GET /api/v1/categorias/{id}/
- PUT /api/v1/categorias/{id}/
- PATCH /api/v1/categorias/{id}/
- DELETE /api/v1/categorias/{id}/
- GET /api/v1/metas/
- POST /api/v1/metas/
- GET /api/v1/metas/{id}/
- PUT /api/v1/metas/{id}/
- PATCH /api/v1/metas/{id}/
- DELETE /api/v1/metas/{id}/
- POST /api/v1/metas/{id}/atualizar_progresso/
- GET /api/v1/dashboard/resumo/
- GET /api/v1/dashboard/graficos/
- GET /api/v1/notificacoes/
- POST /api/v1/notificacoes/{id}/marcar_lida/

Educação:

- GET /api/v1/education/conteudos/
- GET /api/v1/education/conteudos/{id}/
- POST /api/v1/education/conteudos/{id}/concluir/
- GET /api/v1/education/conteudos/progresso/

Documentação:

- GET /api/schema/
- GET /api/docs/

## Execução Local

### 1. Clonar o repositório

    git clone <url-do-repositorio>
    cd tcc

### 2. Criar e ativar o ambiente virtual

No PowerShell:

    python -m venv venv
    .\venv\Scripts\Activate.ps1

Se o ambiente já existir, ative apenas:

    .\venv\Scripts\Activate.ps1

### 3. Instalar dependências

    pip install -r requirements.txt

Se o arquivo requirements.txt ainda não existir, instale os pacotes principais manualmente:

    pip install django djangorestframework djangorestframework-simplejwt drf-spectacular django-cors-headers psycopg2-binary celery redis

### 4. Configurar variáveis de ambiente

Crie um arquivo .env ou defina as variáveis no ambiente com valores como:

    DJANGO_SECRET_KEY=uma-chave-secreta-forte
    DJANGO_DEBUG=true
    DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=financeup
    DB_USER=postgres
    DB_PASSWORD=senha
    DB_HOST=127.0.0.1
    DB_PORT=5432
    CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
    CELERY_BROKER_URL=redis://127.0.0.1:6379/0
    CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/1

Observação: o projeto possui fallback para SQLite no ambiente local, mas o banco recomendado para uso real é PostgreSQL.

### 5. Criar e aplicar migrações

    python manage.py makemigrations
    python manage.py migrate

### 6. Criar superusuário

    python manage.py createsuperuser

### 7. Executar o servidor

    python manage.py runserver

A API ficará disponível em:

    http://127.0.0.1:8000/

A documentação Swagger ficará disponível em:

    http://127.0.0.1:8000/api/docs/

## Execução dos Testes

Rodar toda a suíte:

    python manage.py test -v 2

Rodar testes por app:

    python manage.py test apps.accounts.tests apps.financial_aux.tests apps.education.tests apps.gamification.tests apps.simulations.tests apps.investiments.tests -v 2

## Celery e Redis

As tasks assíncronas estão preparadas para:

- envio de e-mail de recuperação de senha;
- lembretes de metas;
- alertas financeiros;
- rotinas futuras de automação.

Para usar Celery de forma completa, é necessário subir um broker Redis local ou em contêiner.

Exemplo de uso em desenvolvimento:

    celery -A backend worker -l info

Se houver agendamento periódico, também será necessário o beat:

    celery -A backend beat -l info

## Banco de Dados

O projeto foi estruturado para PostgreSQL em produção. O uso recomendado é:

- PostgreSQL para persistência principal;
- índices em datas, usuário e categorias;
- agregações por período para dashboard e gráficos;
- soft delete em categorias para preservar histórico.

## Observações de Implementação

- O backend usa JWT com blacklist para logout com invalidação de refresh token.
- O usuário possui e-mail único e perfil estendido.
- As receitas, despesas, categorias, metas e progresso educacional são vinculados ao usuário autenticado.
- O dashboard é calculado por agregação de dados financeiros.
- Os testes automatizados foram implementados em cápsulas por app e já executam com sucesso.

## Status Atual

- Sistema de autenticação funcional.
- CRUD financeiro funcional.
- Dashboard funcional.
- Educação funcional.
- Testes automatizados funcionando.
- Base pronta para ampliar notificações, gamificação avançada, investimentos e simulações.

## Comandos Úteis

    python manage.py check
    python manage.py test -v 2
    python manage.py migrate
    python manage.py createsuperuser
