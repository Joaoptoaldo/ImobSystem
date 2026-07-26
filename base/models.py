"""
App "base" — Centralização de templates e arquivos estáticos compartilhados.

Este app não possui models próprios nem lógica de negócio.
Sua única função é servir como repositório central para:
  - templates globais (base.html, navbar.html, pagination.html, message.html)
  - arquivos estáticos compartilhados (CSS, JS, imagens)
  - template de login (registration/login.html)

Os apps de domínio (locacao, etc.) herdam base.html e reutilizam
os componentes aqui definidos, evitando duplicação entre eles.
"""
