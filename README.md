# Sistema de Gerenciamento de Aluguéis

A documentação completa e a visão geral do projeto estão no [README da raiz do repositório](../README.md).

Abaixo, instruções específicas para quem vai rodar a aplicação Django localmente.

## Setup

```bash
# 1. Ambiente virtual
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate   # Linux / macOS

# 2. Dependências
pip install -r requirements.txt

# 3. Variáveis de ambiente
cp .env.example .env
# edite o .env com SECRET_KEY, DEBUG, ALLOWED_HOSTS e,
# opcionalmente, AWS_* para armazenamento S3 de imagens

# 4. Migrações
python manage.py migrate

# 5. (Opcional) Superusuário
python manage.py createsuperuser

# 6. Servidor de desenvolvimento
python manage.py runserver
```

Acesse [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Testes

```bash
python manage.py test
```

A suíte tem **11 testes** automatizados na aplicação `locacao`.

## Deploy

- **Procfile**: `web: gunicorn proj.wsgi --log-file -`
- **Runtime**: Python 3.12.10 (`runtime.txt`)
- **CI**: GitHub Actions ([`.github/workflows/tests.yml`](.github/workflows/tests.yml)) executa os testes a cada push
- **Release**: `python manage.py collectstatic --noinput && python manage.py migrate`

> Sem as variáveis `AWS_*` configuradas, as imagens são salvas localmente e **não persistem** entre deploys. Configure um bucket S3 para persistência real.

