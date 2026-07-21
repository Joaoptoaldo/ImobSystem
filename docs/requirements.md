# Levantamento de Requisitos

# 1. Objetivo

Sistema web para auxiliar uma imobiliária no gerenciamento de imóveis destinados à locação. A aplicação deve permitir cadastrar clientes e imóveis, registrar locações, anexar imagens aos imóveis e emitir um relatório dos imóveis alugados.

---

# 2. Escopo

O sistema deve contemplar as seguintes funcionalidades:

- Cadastro de clientes;
- Cadastro de imóveis;
- Cadastro de imagens dos imóveis;
- Registro de locações;
- Consulta de imóveis;
- Filtro de imóveis por tipo;
- Relatório de imóveis locados.

---

# 3. Atores do Sistema

## Administrador

Responsável pela administração completa do sistema.

Permissões:

- Cadastrar clientes;
- Editar clientes;
- Excluir clientes;
- Consultar clientes;
- Cadastrar imóveis;
- Editar imóveis;
- Excluir imóveis;
- Consultar imóveis;
- Filtrar imóveis por tipo;
- Cadastrar imagens dos imóveis;
- Registrar locações;
- Consultar locações;
- Emitir relatório de imóveis alugados.

---

# 4. Requisitos Funcionais

### RF01 – Cadastro de Clientes

O sistema deve permitir cadastrar clientes contendo:

- Nome;
- E-mail;
- Telefone.

### RF02 – Consulta de Clientes

O sistema deve permitir listar todos os clientes cadastrados.

### RF03 – Atualização de Clientes

O sistema deve permitir editar os dados de clientes.

### RF04 – Exclusão de Clientes

O sistema deve permitir excluir clientes cadastrados.

### RF05 – Cadastro de Imóveis

O sistema deve permitir cadastrar imóveis contendo:

- Código;
- Tipo;
- Endereço;
- Valor da locação.

### RF06 – Consulta de Imóveis

O sistema deve permitir listar todos os imóveis cadastrados.

### RF07 – Atualização de Imóveis

O sistema deve permitir editar os dados dos imóveis.

### RF08 – Exclusão de Imóveis

O sistema deve permitir excluir imóveis.

### RF09 – Filtro de Imóveis

O sistema deve permitir filtrar os imóveis por tipo.

Tipos disponíveis:

- Apartamento;
- Kitnet;
- Casa.

### RF10 – Cadastro de Imagens

O sistema deve permitir cadastrar uma ou mais imagens para um imóvel.


### RF11 – Registro de Locações

O sistema deve permitir registrar uma locação informando:

- Cliente;
- Imóvel;
- Data de início;
- Data de término.

### RF12 – Consulta de Locações

O sistema deve permitir consultar todas as locações registradas.

### RF13 – Relatório de Imóveis Locados

O sistema deve gerar um relatório contendo os imóveis atualmente alugados.

---

# 5. Requisitos Não Funcionais

### RNF01

O sistema deverá ser desenvolvido utilizando o framework Django.

### RNF02

O sistema deverá utilizar Python como linguagem de programação.

### RNF03

O banco de dados deverá utilizar SQLite.

### RNF04

O sistema deverá utilizar o ORM do Django para persistência dos dados.

### RNF05

A interface deverá ser desenvolvida utilizando:

- HTML;
- CSS;
- JavaScript;
- Bootstrap.

### RNF06

O sistema deverá ser acessível através de navegadores modernos.

### RNF07

As imagens dos imóveis deverão ser armazenadas utilizando o ImageField do Django.


### RNF08

O sistema deverá seguir a arquitetura MTV (Model-Template-View).


### RNF09

Os dados deverão permanecer persistidos após o encerramento da aplicação.

---

# 6. Regras de Negócio

### RN01

Cada cliente pode possuir diversas locações.

### RN02

Cada locação pertence a um único cliente.

### RN03

Cada imóvel pode possuir várias locações ao longo do tempo.

### RN04

Cada locação está vinculada a apenas um imóvel.

### RN05

Um imóvel pode possuir diversas imagens.

### RN06

O tipo do imóvel deve ser um dos seguintes:

- Apartamento;
- Kitnet;
- Casa.

### RN07

Toda locação deve possuir uma data de início e uma data de término.


### RN08

Um imóvel alugado deve ser identificado pelo sistema como indisponível para novas locações.


### RN09

O relatório de imóveis locados deve apresentar apenas imóveis atualmente alugados.


### RN10

Cada imóvel deve possuir um código para identificação.

---

# 7. Considerações

O sistema caracteriza um Sistema de Gestão de Locações Imobiliárias, destinado ao gerenciamento administrativo de uma imobiliária. Seu foco principal é centralizar o cadastro de clientes e imóveis, controlar as locações realizadas e disponibilizar consultas e relatórios para apoio à gestão.