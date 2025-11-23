import unittest
import os
import sys

# Ajusta o caminho para conseguir importar os módulos da pasta src
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from src.config.database import Database
from src.repositories.produto_repo import ProdutoRepository
from src.repositories.fornecedor_repo import FornecedorRepository
from src.models.produto_medicamento import ProdutoMedicamento
from src.models.fornecedor import Fornecedor


class TestProdutoCRUD(unittest.TestCase):

    def setUp(self):
        self.nome_db_teste = "teste_unitario.db"
        self.db = Database(db_name=self.nome_db_teste)
        self.db.inicializar_tabelas()

        self.repo_produto = ProdutoRepository()
        self.repo_produto.db = self.db

        self.repo_fornecedor = FornecedorRepository()
        self.repo_fornecedor.db = self.db

    def tearDown(self):
        if os.path.exists(self.db.db_path):
            os.remove(self.db.db_path)

    def test_fluxo_completo_crud_produto(self):

        # 1. CREATE (Cadastrar)
        produto = ProdutoMedicamento(
            id_produto=None,
            nome_produto="Vacina Teste",
            categoria="Vacinas",
            preco_unitario=50.00,
            estoque=100,
            id_fornecedor=None,
        )
        self.repo_produto.salvar(produto)

        lista = self.repo_produto.listar_todos_produtos()
        self.assertEqual(len(lista), 1)  # Tem que ter 1 produto na lista

        self.assertEqual(lista[0][1], "Vacina Teste")

        id_gerado = lista[0][0]

        # 2. READ (Buscar por ID)
        produto_recuperado = self.repo_produto.buscar_produto_por_id(id_gerado)
        self.assertIsNotNone(produto_recuperado)
        self.assertEqual(produto_recuperado.preco_unitario, 50.00)

        # 3. UPDATE (Atualizar)
        produto_recuperado.nome_produto = "Vacina Alterada"
        produto_recuperado.estoque = 90

        resultado_update = self.repo_produto.atualizar_produto(produto_recuperado)
        self.assertTrue(resultado_update)  # Tem que retornar True

        produto_atualizado = self.repo_produto.buscar_produto_por_id(id_gerado)
        self.assertEqual(produto_atualizado.nome_produto, "Vacina Alterada")
        self.assertEqual(produto_atualizado.estoque, 90)

        # 4. DELETE (Remover)
        resultado_delete = self.repo_produto.deletar_produto(id_gerado)
        self.assertTrue(resultado_delete)  # Tem que retornar True

        produto_apagado = self.repo_produto.buscar_produto_por_id(id_gerado)
        self.assertIsNone(produto_apagado)  # Tem que ser None

    def test_produto_com_fornecedor(self):

        # 1. Criar um fornecedor primeiro
        fornecedor = Fornecedor(
            id_fornecedor=None,
            nome_fornecedor="Pet Supplies LTDA",
            cidade="São Paulo",
            contato="(11) 1234-5678",
        )
        self.repo_fornecedor.salvar(fornecedor)

        fornecedores = self.repo_fornecedor.listar_todos_fornecedores()
        self.assertEqual(len(fornecedores), 1)
        id_fornecedor = fornecedores[0].id_fornecedor

        # 2. Criar um produto vinculado ao fornecedor
        produto = ProdutoMedicamento(
            id_produto=None,
            nome_produto="Ração Premium",
            categoria="Alimento",
            preco_unitario=120.00,
            estoque=50,
            id_fornecedor=id_fornecedor,
        )
        self.repo_produto.salvar(produto)

        # 3. Verificar se o JOIN está funcionando
        produtos_com_fornecedor = self.repo_produto.listar_todos_produtos()
        self.assertEqual(len(produtos_com_fornecedor), 1)

        linha = produtos_com_fornecedor[0]
        self.assertEqual(linha[1], "Ração Premium")
        self.assertEqual(linha[7], "Pet Supplies LTDA")
        self.assertEqual(linha[8], "São Paulo")

    def test_listar_produtos_por_fornecedor(self):

        # 1. Criar dois fornecedores
        fornecedor1 = Fornecedor(None, "Fornecedor A", "Rio de Janeiro", "1111-1111")
        fornecedor2 = Fornecedor(None, "Fornecedor B", "Belo Horizonte", "2222-2222")

        self.repo_fornecedor.salvar(fornecedor1)
        self.repo_fornecedor.salvar(fornecedor2)

        fornecedores = self.repo_fornecedor.listar_todos_fornecedores()
        id_forn1 = fornecedores[0].id_fornecedor
        id_forn2 = fornecedores[1].id_fornecedor

        # 2. Criar produtos para cada fornecedor
        produto1 = ProdutoMedicamento(None, "Produto A1", "Cat1", 10.0, 5, id_forn1)
        produto2 = ProdutoMedicamento(None, "Produto A2", "Cat1", 20.0, 10, id_forn1)
        produto3 = ProdutoMedicamento(None, "Produto B1", "Cat2", 30.0, 15, id_forn2)

        self.repo_produto.salvar(produto1)
        self.repo_produto.salvar(produto2)
        self.repo_produto.salvar(produto3)

        # 3. Verificar se a busca por fornecedor funciona
        produtos_forn1 = self.repo_produto.buscar_produtos_por_fornecedor(id_forn1)
        produtos_forn2 = self.repo_produto.buscar_produtos_por_fornecedor(id_forn2)

        self.assertEqual(len(produtos_forn1), 2)
        self.assertEqual(len(produtos_forn2), 1)
        self.assertEqual(produtos_forn1[0].nome_produto, "Produto A1")
        self.assertEqual(produtos_forn2[0].nome_produto, "Produto B1")

    def test_validacao_modelo(self):
        prod = ProdutoMedicamento(1, "Ração", "Alimento", 10.0, 5)
        self.assertEqual(prod.nome_produto, "Ração")
        self.assertIn("Ração", str(prod))
        self.assertIn("R$ 10.00", str(prod))


if __name__ == "__main__":
    unittest.main()
