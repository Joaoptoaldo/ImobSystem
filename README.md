# Sistema de Gerenciamento de Aluguéis

Aplicação web para gerenciamento de imóveis destinados à locação, com cadastro de clientes e imóveis, registro e encerramento de contratos de locação e consulta de relatórios.

## Funcionalidades

- **Clientes** - cadastro, edição, exclusão e listagem
- **Imóveis** - cadastro com imagens, edição, exclusão e listagem
- **Locação** - registro de contratos com datas, encerramento e validação de disponibilidade
- **Relatórios** - filtros por cliente, tipo de imóvel, período e status de locação
- **Autenticação** - acesso restrito a usuários logados
- **Testes automatizados** - 11 testes na aplicação `locacao`

## Documentação

A documentação do projeto está organizada nas seguintes pastas:

**docs/**

Contém a documentação produzida durante a fase de análise e modelagem do sistema, como o levantamento de requisitos.

- [Levantamento de Requisitos](docs/requirements.md)
- [Entidades e Relacionamentos do Sistema](docs/entities.md)
- [Classes do Sistema](docs/class-diagram.md)
- [Casos de Uso](docs/use-cases.md)

**diagrams/**

Contém os diagramas elaborados na fase inicial do projeto:

- [Diagrama de Entidade-Relacionamento](./diagrams/er-diagram/der.png)
- [Diagrama de Casos de Uso](./diagrams/use-case-diagram/use-case-diagram.png)
- [Diagrama de Classes](./diagrams/class-diagram/class-diagram.png)

---

## Tecnologias

- Python 3.12
- Django 6.0
- SQLite / PostgreSQL
- Bootstrap 5
- JavaScript
- Gunicorn
- WhiteNoise

---

## Código Fonte

A aplicação está disponível no diretório [`project/`](project/) e foi desenvolvida com **Django 6.0** e **Python 3.12**.

### Como rodar localmente

```bash
# 1. Acessar o diretório da aplicação
cd project

# 2. Criar e ativar o ambiente virtual
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate   # Linux / macOS

# 3. Instalar as dependências
pip install -r requirements.txt

# 4. Configurar as variáveis de ambiente
cp .env.example .env
# edite o .env com seus valores (SECRET_KEY, DEBUG, ALLOWED_HOSTS, e
# opcionalmente as variáveis AWS_* se for usar armazenamento S3 pras
# imagens)

# 5. Aplicar as migrações
python manage.py migrate

# 6. (Opcional) Criar um superusuário para acessar o admin
python manage.py createsuperuser

# 7. Iniciar o servidor de desenvolvimento
python manage.py runserver
```

Acesse [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

### Executar os testes

```bash
cd project
python manage.py test
```

São **11 testes** automatizados que cobrem validação de formulários, regras de negócio, views de relatórios, criação e encerramento de locações.

### Deploy

A aplicação está pronta para deploy em plataformas como Heroku, Render ou Railway:

- **Procfile**: `web: gunicorn proj.wsgi --log-file -`
- **Runtime**: Python 3.12.10 (`runtime.txt`)
- **CI**: GitHub Actions executa os testes automaticamente a cada push ([`.github/workflows/tests.yml`](project/.github/workflows/tests.yml))
- **Comando release** (executado antes do deploy): `python manage.py collectstatic --noinput && python manage.py migrate`

> Sem as variáveis `AWS_*` configuradas, as imagens de imóveis são salvas localmente e **não persistem** entre deploys na maioria das plataformas de hospedagem (Heroku, Render, Railway). Para persistência real, configure um bucket S3 (veja `.env.example`).

---

## Template

Este projeto foi iniciado a partir do template base para aplicações Django, utilizado como estrutura inicial para padronizar a organização dos projetos, configurações e boas práticas de desenvolvimento.

Repositório: [django-project-template](https://github.com/Joaoptoaldo/django-project-template)
