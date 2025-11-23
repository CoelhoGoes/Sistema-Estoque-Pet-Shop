# 🐾 Sistema de Gerenciamento de Estoque - PetShop

Este projeto é uma aplicação de console (CLI) desenvolvida para demonstrar a aplicação prática de ferramentas essenciais de desenvolvimento de software em um contexto de negócio simples: um sistema de controle de estoque e fornecedores para um Petshop.

O objetivo principal é exemplificar a construção de um sistema robusto utilizando Python e banco de dados relacional, implementando operações completas de **CRUD** (Create, Read, Update, Delete) e boas práticas de arquitetura.

---

## 🚀 Funcionalidades

O sistema foi projetado para cobrir fluxos essenciais de gerenciamento:

* **Gestão de Medicamentos/Produtos:**
  * Cadastro com validação de dados (ex: impedimento de valores negativos).
  * Listagem completa e formatada dos itens em estoque.
  * Busca detalhada de produtos por ID.
  * Atualização de registros existentes (preço, estoque, etc.).
  * Remoção segura de itens (com confirmação de exclusão).
* **Gestão de Fornecedores:**
  * Cadastro e controle de dados de fornecedores.
* **Relacionamentos:**
  * Vínculo entre Produtos e Fornecedores (uso de Chaves Estrangeiras).
  * Listagem filtrada: visualização de todos os produtos atrelados a um fornecedor específico.
* **Destaques Técnicos:**
  * ✅ **Testes Unitários Automatizados:** Implementação de testes para validar o fluxo lógico e garantir a integridade do CRUD.

---

## 🛠️ Tecnologias Utilizadas

O projeto foca no uso de ferramentas nativas e eficientes:

* **Linguagem:** Python 3.x (Sem dependência de frameworks externos pesados).
* **Banco de Dados:** SQLite 3 (Banco relacional leve e embutido, ideal para aplicações portáteis).
* **Testes:** Unittest (Biblioteca padrão do Python para testes automatizados).

---

## 📂 Estrutura do Projeto

A organização das pastas foi pensada para refletir uma estrutura de software escalável e organizada:

```text
Projeto_Petshop/
│
├── data/                       # Armazenamento do arquivo de banco de dados (app.db)
├── src/                        # Código Fonte Principal
│   ├── config/                 # Configuração de conexão e inicialização do banco
│   ├── models/                 # Classes que representam as entidades (Produto, Fornecedor)
│   ├── repositories/           # Camada de Persistência (Comandos SQL diretos)
│   └── main.py                 # Ponto de entrada da aplicação (Menu Principal)
│
├── tests/                      # Testes Automatizados
│   └── teste_crud.py           # Script de verificação dos fluxos do sistema
│
├── schema.sql                  # Script SQL de referência para criação das tabelas
└── README.md                   # Documentação do Projeto
```

---

## ⚙️ Instalação e Execução

Este projeto foi construído utilizando apenas a biblioteca padrão do Python, eliminando a necessidade de instalar dependências externas complexas.

### Pré-requisitos

* **Python 3.8** ou superior instalado.
* Sistema operacional Windows, Linux ou macOS.

### Passo a Passo

1. **Clone o repositório** (ou extraia o arquivo zip):

    ```bash
    git clone https://github.com/seu-usuario/projeto-petshop.git
    cd projeto-petshop
    ```

2. **Execute a aplicação**:

    Certifique-se de estar na pasta raiz do projeto e execute:

    ```bash
    python src/main.py
    ```

    *(Caso utilize Linux/Mac ou tenha múltiplas versões do Python, pode ser necessário usar `python3 src/main.py`)*

3. **Primeira Execução**:

    Não é necessário configurar o banco de dados manualmente. Ao iniciar, o sistema verificará automaticamente a existência do diretório `data/` e criará o arquivo `app.db` com todas as tabelas necessárias prontas para uso.

---

## 🧪 Executando os Testes Automatizados

O projeto inclui uma suíte de testes unitários desenvolvida com o módulo `unittest`. Os testes validam o ciclo completo de CRUD e as regras de negócio em um banco de dados temporário, garantindo a integridade dos dados de produção.

Para rodar os testes, execute o comando abaixo na raiz do projeto:

```bash
python -m unittest discover tests
```
