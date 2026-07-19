# Django Project Template

Template base para iniciar novos projetos Django seguindo boas práticas de organização, configuração e escalabilidade.

## Objetivo

Este repositório foi criado para servir como ponto de partida para futuras aplicações Django, fornecendo uma estrutura mínima, organizada e reutilizável.

## Tecnologias

- Python 3
- Django
- Bootstrap 5 (CDN)
- python-dotenv
- dj-database-url
- SQLite
- PostgreSQL (opcional)

## Pré-requisitos

- Python 3.10 ou superior
- Git
- pip

---

# Como utilizar

## 1. Clonar o repositório

```bash
git clone https://github.com/Joaoptoaldo/django-project-template.git
cd django-project-template
```

## 2. Criar e ativar o ambiente virtual

### Windows (PowerShell)

```bash
python -m venv .venv
.venv\Scripts\activate 
```

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

## 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

## 4. Criar o arquivo `.env`

Na raiz do projeto, crie um arquivo chamado `.env`.

Primeiro, gere uma nova `SECRET_KEY`:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Depois, crie o arquivo utilizando a estrutura abaixo:

```env
# Gere sua própria SECRET_KEY
SECRET_KEY=cole_aqui_sua_chave_secreta_gerada

# Modo de desenvolvimento
DEBUG=True

# Hosts permitidos
ALLOWED_HOSTS=localhost,127.0.0.1

# Banco de dados (opcional)
# Deixe vazio para utilizar SQLite
DATABASE_URL=
```

## 5. Aplicar as migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

Inicialmente pode não haver migrações para gerar.

## 6. Executar o servidor

```bash
python manage.py runserver
```

Acesse:

- http://127.0.0.1:8000/

## 7. Criar um superusuário

```bash
python manage.py createsuperuser
```

Depois acesse:

- http://127.0.0.1:8000/admin/

---

# Configuração

## SECRET_KEY

Obrigatória.

Caso não esteja definida no `.env`, o projeto interromperá a inicialização exibindo uma mensagem de erro clara.

---

## DEBUG

Controla o modo de desenvolvimento da aplicação.

Os seguintes valores são interpretados como **True**:

```text
True
true
1
yes
on
```

Qualquer outro valor (como `False`, `false`, `0`, `no` ou `off`) será interpretado como **False**.

---

## ALLOWED_HOSTS

Informe os hosts separados por vírgula.

Exemplo:

```env
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## DATABASE_URL

Opcional.

Quando definida, o projeto utiliza automaticamente a configuração informada.

Exemplo para PostgreSQL:

```env
DATABASE_URL=postgresql://usuario:senha@host:5432/banco
```

Caso a variável não exista, o Django utilizará automaticamente o banco SQLite (`db.sqlite3`).

---

# Próximos passos

Após criar um novo projeto baseado neste template, recomenda-se:

1. Criar os modelos da aplicação.
2. Gerar as migrações.
3. Implementar autenticação e autorização.
4. Organizar o projeto em múltiplas aplicações quando necessário.
5. Configurar ambientes de desenvolvimento e produção.
6. Adicionar testes automatizados.
7. Configurar Docker e CI/CD (opcional).

# Contribuição

Sugestões, melhorias e correções são bem-vindas.

Caso tenha alguma ideia para evoluir este template, fique à vontade para abrir uma *Issue* ou enviar um *Pull Request*.