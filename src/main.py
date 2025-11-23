import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.database import Database
from models.produto_medicamento import ProdutoMedicamento
from repositories.produto_repo import ProdutoRepository
from models.fornecedor import Fornecedor
from repositories.fornecedor_repo import FornecedorRepository


def listar_todos_produtos():
    repo = ProdutoRepository()
    produtos_com_fornecedores = repo.listar_todos_produtos()

    if not produtos_com_fornecedores:
        print("\nNenhum produto cadastrado ainda.")
    else:
        print(f"\nTotal de produtos: {len(produtos_com_fornecedores)}\n")
        for linha in produtos_com_fornecedores:
            id_produto = linha[0]
            nome_produto = linha[1]
            categoria = linha[2]
            preco = linha[3]
            estoque = linha[4]
            id_fornecedor = linha[5]
            data_atualizacao = linha[6]
            nome_fornecedor = linha[7] if linha[7] else "Sem fornecedor"
            cidade_fornecedor = linha[8] if linha[8] else "-"

            print(f"ID: {id_produto} | {nome_produto}")
            print(f"   Categoria: {categoria}")
            print(f"   Preço: R$ {preco:.2f} | Estoque: {estoque}")
            print(f"   Fornecedor: {nome_fornecedor} ({cidade_fornecedor})")
            print(f"   ID Fornecedor: {id_fornecedor} | Atualizado: {data_atualizacao}")
            print("-" * 50)

    input("\nEnter para continuar...")


def cadastrar_produto():
    print("\n--- NOVO PRODUTO ---")

    # 1. Nome
    while True:
        nome = input("Nome do Produto: ").strip()
        if nome:
            break
        print("Erro: Nome obrigatório.")

    # 2. Categoria
    categorias_validas = ["Medicamento", "Vacina", "Ração", "Brinquedo", "Roupa"]
    print("\nCategorias disponíveis:")
    for i, cat in enumerate(categorias_validas, 1):
        print(f"  {i}. {cat}")

    while True:
        try:
            categoria_input = int(input("\nEscolha a categoria (número): "))
            if 1 <= categoria_input <= len(categorias_validas):
                categoria = categorias_validas[categoria_input - 1]
                break
            print(f"Erro: Digite um número indicado pelas categorias.")
        except ValueError:
            print("Erro: Digite um número válido.")

    # 3. Preço
    while True:
        try:
            preco = float(input("Preço Unitário: "))
            if preco >= 0:
                break
            else:
                print("Erro: O preço não pode ser negativo.")
        except ValueError:
            print("Erro: Digite um número válido.")

    # 4. Estoque
    while True:
        try:
            estoque = int(input("Quantidade em Estoque: "))
            if estoque >= 0:
                break
            else:
                print("Erro: Estoque não pode ser negativo.")
        except ValueError:
            print("Erro: Digite um inteiro válido.")

    # 5. Fornecedor
    print("\n--- Fornecedores Disponíveis ---")
    repo_fornecedor = FornecedorRepository()
    fornecedores = repo_fornecedor.listar_todos_fornecedores()

    if fornecedores:
        for forn in fornecedores:
            print(f"  ID {forn.id_fornecedor}: {forn.nome_fornecedor} - {forn.cidade}")
    else:
        print("  Nenhum fornecedor cadastrado ainda.")

    id_fornecedor_input = input(
        "\nID do Fornecedor (Opcional - Enter para pular): "
    ).strip()

    if id_fornecedor_input:
        if id_fornecedor_input.isdigit():
            id_temp = int(id_fornecedor_input)
            fornecedor_existe = repo_fornecedor.buscar_fornecedor_por_id(id_temp)
            if fornecedor_existe:
                id_fornecedor = id_temp
            else:
                print(f"Fornecedor com ID {id_temp} não existe.")
                print("O produto será registrado sem fornecedor.")
                id_fornecedor = None
        else:
            print("ID inválido. Deve ser um número inteiro.")
            print("O produto será registrado sem fornecedor.")
            id_fornecedor = None
    else:
        id_fornecedor = None

    novo_prod = ProdutoMedicamento(
        id_produto=None,
        nome_produto=nome,
        categoria=categoria,
        preco_unitario=preco,
        estoque=estoque,
        id_fornecedor=id_fornecedor,
    )

    repo = ProdutoRepository()
    repo.salvar(novo_prod)
    print(f"\nProduto '{novo_prod.nome_produto}' cadastrado com sucesso.")
    input("\nEnter para continuar...")


def buscar_produto_por_id():
    print("\n--- BUSCAR PRODUTO ---")
    try:
        id_busca = int(input("Digite o ID do produto: "))

        repo = ProdutoRepository()
        produto = repo.buscar_produto_por_id(id_busca)

        if produto:
            print("\nProduto Encontrado:")
            print(f"Nome: {produto.nome_produto}")
            print(f"Categoria: {produto.categoria}")
            print(f"Preço: R$ {produto.preco_unitario:.2f}")
            print(f"Estoque: {produto.estoque}")
            print(f"Fornecedor ID: {produto.id_fornecedor}")
            print(f"Última Atualização: {produto.data_atualizacao}")
        else:
            print("Produto não encontrado com este ID.")

    except ValueError:
        print("Erro: O ID deve ser um número inteiro.")

    input("\nEnter para voltar...")


def atualizar_produto():
    print("\n--- ATUALIZAR PRODUTO ---")
    try:
        id_input = input("Digite o ID do produto a ser alterado: ")
        id_produto = int(id_input)

        repo = ProdutoRepository()
        produto_atual = repo.buscar_produto_por_id(id_produto)

        if not produto_atual:
            print("Produto não encontrado.")
            return

        print(f"\nEditando: {produto_atual.nome_produto}")
        print("(Pressione Enter para manter o valor atual mostrado entre colchetes)")

        # 1. Edição do NOME
        novo_nome = input(f"Nome [{produto_atual.nome_produto}]: ").strip()
        if not novo_nome:
            novo_nome = produto_atual.nome_produto

        # 2. Edição da CATEGORIA
        categorias_validas = ["Medicamento", "Vacina", "Ração", "Brinquedo", "Roupa"]
        print(f"\nCategoria atual: {produto_atual.categoria}")
        print("Categorias disponíveis:")
        for i, cat in enumerate(categorias_validas, 1):
            print(f"  {i}. {cat}")
        
        nova_cat = produto_atual.categoria
        entrada_cat = input("\nEscolha a nova categoria (número) ou Enter para manter: ").strip()
        
        if entrada_cat:
            try:
                categoria_input = int(entrada_cat)
                if 1 <= categoria_input <= len(categorias_validas):
                    nova_cat = categorias_validas[categoria_input - 1]
                else:
                    print(f"Número inválido. Mantendo categoria atual: {produto_atual.categoria}")
            except ValueError:
                print(f"Entrada inválida. Mantendo categoria atual: {produto_atual.categoria}")

        # 3. Edição do PREÇO
        novo_preco = produto_atual.preco_unitario
        while True:
            entrada = input(f"Preço [{produto_atual.preco_unitario}]: ").strip()
            if not entrada:
                break
            try:
                valor = float(entrada)
                if valor >= 0:
                    novo_preco = valor
                    break
                print("O preço não pode ser negativo.")
            except ValueError:
                print("Digite um número válido.")

        # 4. Edição do ESTOQUE
        novo_estoque = produto_atual.estoque
        while True:
            entrada = input(f"Estoque [{produto_atual.estoque}]: ").strip()
            if not entrada:
                break
            try:
                valor = int(entrada)
                if valor >= 0:
                    novo_estoque = valor
                    break
                print("Estoque não pode ser negativo.")
            except ValueError:
                print("Digite um número inteiro.")

        # 5. Edição do FORNECEDOR
        print("\n--- Fornecedores Disponíveis ---")
        repo_fornecedor = FornecedorRepository()
        fornecedores = repo_fornecedor.listar_todos_fornecedores()

        if fornecedores:
            for forn in fornecedores:
                print(
                    f"  ID {forn.id_fornecedor}: {forn.nome_fornecedor} - {forn.cidade}"
                )
        else:
            print("Nenhum fornecedor cadastrado ainda.")

        novo_fornecedor = produto_atual.id_fornecedor
        entrada_forn = input(
            f"\nID Fornecedor [{produto_atual.id_fornecedor or 'Não especificado'}]: "
        ).strip()

        if entrada_forn:
            if entrada_forn.isdigit():
                id_temp = int(entrada_forn)
                fornecedor_existe = repo_fornecedor.buscar_fornecedor_por_id(id_temp)
                if fornecedor_existe:
                    novo_fornecedor = id_temp
                else:
                    print(f"Fornecedor com ID {id_temp} não existe.")
                    print("O fornecedor não será alterado.")
                    novo_fornecedor = produto_atual.id_fornecedor
            else:
                print("ID inválido. Deve ser um número inteiro.")
                print("O fornecedor não será alterado.")
                novo_fornecedor = produto_atual.id_fornecedor

        from datetime import date

        nova_data = date.today().isoformat()

        produto_atualizado = ProdutoMedicamento(
            id_produto=id_produto,
            nome_produto=novo_nome,
            categoria=nova_cat,
            preco_unitario=novo_preco,
            estoque=novo_estoque,
            id_fornecedor=novo_fornecedor,
            data_atualizacao=nova_data,
        )

        if repo.atualizar_produto(produto_atualizado):
            print("Produto atualizado com sucesso!")

    except ValueError:
        print("Erro: ID inválido.")

    input("\nEnter para voltar...")


def deletar_produto():
    print("\n--- REMOVER PRODUTO ---")
    try:
        id_input = input("Digite o ID do produto a ser removido: ")
        id_produto = int(id_input)

        repo = ProdutoRepository()

        produto = repo.buscar_produto_por_id(id_produto)

        if not produto:
            print("Produto não encontrado. Operação cancelada.")
            return

        print(f"\nATENÇÃO: Você está prestes a apagar: {produto.nome_produto}")
        confirmacao = input("Tem certeza absoluta? (S/N): ").upper()

        if confirmacao == "S":
            sucesso = repo.deletar_produto(id_produto)
            if sucesso:
                print("Produto removido com sucesso!")
            else:
                print("Erro ao tentar remover o registro.")
        else:
            print("Operação cancelada.")

    except ValueError:
        print("Erro: O ID deve ser um número inteiro.")

    input("\nEnter para voltar...")


def listar_produtos_por_fornecedor():
    """Lista todos os produtos de um fornecedor específico"""
    print("\n--- PRODUTOS POR FORNECEDOR ---")

    repo_fornecedor = FornecedorRepository()
    fornecedores = repo_fornecedor.listar_todos_fornecedores()

    if not fornecedores:
        print("Nenhum fornecedor cadastrado ainda.")
        input("\nEnter para voltar...")
        return

    print("\nFornecedores disponíveis:")
    for forn in fornecedores:
        print(f"  ID {forn.id_fornecedor}: {forn.nome_fornecedor}")

    try:
        id_fornecedor = int(input("\nDigite o ID do fornecedor: "))

        fornecedor = repo_fornecedor.buscar_fornecedor_por_id(id_fornecedor)
        if not fornecedor:
            print("Fornecedor não encontrado.")
            input("\nEnter para voltar...")
            return

        repo_produto = ProdutoRepository()
        produtos = repo_produto.buscar_produtos_por_fornecedor(id_fornecedor)

        print(f"\nProdutos do fornecedor: {fornecedor.nome_fornecedor}")
        print(f"   Cidade: {fornecedor.cidade}\n")

        if not produtos:
            print("Este fornecedor ainda não tem produtos cadastrados.")
        else:
            print(f"Total de produtos: {len(produtos)}\n")
            for produto in produtos:
                print(f"ID: {produto.id_produto} | {produto.nome_produto}")
                print(f"   Categoria: {produto.categoria}")
                print(
                    f"   Preço: R$ {produto.preco_unitario:.2f} | Estoque: {produto.estoque}"
                )
                print("-" * 50)

    except ValueError:
        print("Erro: O ID deve ser um número inteiro.")

    input("\nEnter para voltar...")


def listar_todos_fornecedores():
    repo = FornecedorRepository()
    fornecedores = repo.listar_todos_fornecedores()

    if not fornecedores:
        print("\nNenhum fornecedor cadastrado ainda.")
    else:
        print(f"\nTotal de fornecedores: {len(fornecedores)}\n")
        for fornecedor in fornecedores:
            print(f"ID: {fornecedor.id_fornecedor} | {fornecedor.nome_fornecedor}")
            print(f"   Cidade: {fornecedor.cidade}")
            print(f"   Contato: {fornecedor.contato}")
            print(f"   Data de Cadastro: {fornecedor.data_cadastro}")
            print("-" * 50)

    input("\nEnter para continuar...")


def cadastrar_fornecedor():
    print("\n--- NOVO FORNECEDOR ---")

    # 1. Nome do fornecedor
    while True:
        nome_fornecedor = input("Nome do fornecedor: ").strip()
        if nome_fornecedor:
            break
        print("Erro: Nome do fornecedor é obrigatório.")

    # 2. Cidade
    cidade = input("Cidade: ").strip()

    # 3. Contato
    contato = input("Contato: ").strip()

    novo_fornecedor = Fornecedor(
        id_fornecedor=None,
        nome_fornecedor=nome_fornecedor,
        cidade=cidade,
        contato=contato,
    )

    repo = FornecedorRepository()
    repo.salvar(novo_fornecedor)
    print(f"\nfornecedor '{novo_fornecedor.nome_fornecedor}' cadastrado com sucesso.")
    input("\nEnter para continuar...")


def buscar_fornecedor_por_id():
    print("\n--- BUSCAR FORNECEDOR ---")
    try:
        id_busca = int(input("Digite o ID do fornecedor: "))

        repo = FornecedorRepository()
        fornecedor = repo.buscar_fornecedor_por_id(id_busca)

        if fornecedor:
            print("\nFornecedor Encontrado:")
            print(f"Nome: {fornecedor.nome_fornecedor}")
            print(f"Cidade: {fornecedor.cidade}")
            print(f"Contato: {fornecedor.contato}")
            print(f"Data de Cadastro: {fornecedor.data_cadastro}")
        else:
            print("Fornecedor não encontrado com este ID.")

    except ValueError:
        print("Erro: O ID deve ser um número inteiro.")

    input("\nEnter para voltar...")


def deletar_fornecedor():
    print("\n--- REMOVER FORNECEDOR ---")
    try:
        id_input = input("Digite o ID do fornecedor a ser removido: ")
        id_fornecedor = int(id_input)

        repo = FornecedorRepository()

        fornecedor = repo.buscar_fornecedor_por_id(id_fornecedor)

        if not fornecedor:
            print("Fornecedor não encontrado. Operação cancelada.")
            return

        print(f"\nATENÇÃO: Você está prestes a apagar: {fornecedor.nome_fornecedor}")
        confirmacao = input("Tem certeza absoluta? (S/N): ").upper()

        if confirmacao == "S":
            sucesso = repo.deletar_fornecedor(id_fornecedor)
            if sucesso:
                print("Fornecedor removido com sucesso!")
            else:
                print("Erro ao tentar remover o registro.")
        else:
            print("Operação cancelada.")

    except ValueError:
        print("Erro: O ID deve ser um número inteiro.")

    input("\nEnter para voltar...")


def escolher_menu():
    print("\n=== ESCOLHER SISTEMA ===")
    print("1. Sistema de Estoque Petshop")
    print("2. Sistema de Gerenciamento de Fornecedores")
    print("0. Sair")
    return input("Escolha uma opção: ")


def exibir_menu_petshop():
    print("\n=== SISTEMA DE ESTOQUE PETSHOP ===")
    print("1. Listar Produtos")
    print("2. Cadastrar Produto")
    print("3. Buscar Produto por ID")
    print("4. Atualizar Produto")
    print("5. Deletar Produto")
    print("6. Listar Produtos por Fornecedor")
    print("0. Voltar")
    return input("Escolha uma opção: ")


def exibir_menu_fornecedor():
    print("\n=== SISTEMA DE GERENCIAMENTO DE FORNECEDORES ===")
    print("1. Listar Fornecedores")
    print("2. Cadastrar Fornecedor")
    print("3. Buscar Fornecedor por ID")
    print("4. Deletar Fornecedor")
    print("5. Listar Produtos por Fornecedor")
    print("0. Voltar")
    return input("Escolha uma opção: ")


def main():
    db = Database()
    db.inicializar_tabelas()

    while True:
        opcao = escolher_menu()
        if opcao == "1":
            while True:
                opcao_p = exibir_menu_petshop()
                if opcao_p == "1":
                    listar_todos_produtos()
                elif opcao_p == "2":
                    cadastrar_produto()
                elif opcao_p == "3":
                    buscar_produto_por_id()
                elif opcao_p == "4":
                    atualizar_produto()
                elif opcao_p == "5":
                    deletar_produto()
                elif opcao_p == "6":
                    listar_produtos_por_fornecedor()
                elif opcao_p == "0":
                    print("Voltando...")
                    break
                else:
                    print("Opção inválida!")
        elif opcao == "2":
            while True:
                opcao_f = exibir_menu_fornecedor()
                if opcao_f == "1":
                    listar_todos_fornecedores()
                elif opcao_f == "2":
                    cadastrar_fornecedor()
                elif opcao_f == "3":
                    buscar_fornecedor_por_id()
                elif opcao_f == "4":
                    deletar_fornecedor()
                elif opcao_f == "5":
                    listar_produtos_por_fornecedor()
                elif opcao_f == "0":
                    print("Voltando...")
                    break
                else:
                    print("Opção inválida!")
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")


if __name__ == "__main__":
    main()
