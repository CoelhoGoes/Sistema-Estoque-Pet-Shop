import sqlite3
from models.produto_medicamento import ProdutoMedicamento
from config.database import Database


class ProdutoRepository:
    def __init__(self):
        self.db = Database()

    def salvar(self, produto: ProdutoMedicamento):
        conexao = self.db.conectar()
        cursor = conexao.cursor()

        sql = """
        INSERT INTO produtos_medicamentos 
        (nome_produto, categoria, preco_unitario, estoque, id_fornecedor, data_atualizacao)
        VALUES (?, ?, ?, ?, ?, ?)
        """

        valores = (
            produto.nome_produto,
            produto.categoria,
            produto.preco_unitario,
            produto.estoque,
            produto.id_fornecedor,
            produto.data_atualizacao,
        )

        try:
            cursor.execute(sql, valores)
            conexao.commit()
            print(f"Medicamento '{produto.nome_produto}' salvo com sucesso!")
        except sqlite3.Error as erro:
            print(f"Erro ao salvar: {erro}")
        finally:
            conexao.close()

    def listar_todos_produtos(self):
        conexao = self.db.conectar()
        cursor = conexao.cursor()

        sql = """
        SELECT 
            p.id_produto,
            p.nome_produto,
            p.categoria,
            p.preco_unitario,
            p.estoque,
            p.id_fornecedor,
            p.data_atualizacao,
            f.nome_fornecedor,
            f.cidade
        FROM produtos_medicamentos p
        LEFT JOIN fornecedores f ON p.id_fornecedor = f.id_fornecedor
        """

        cursor.execute(sql)
        linhas = cursor.fetchall()
        conexao.close()

        return linhas

    def buscar_produto_por_id(self, id_busca):
        conexao = self.db.conectar()
        cursor = conexao.cursor()

        sql = "SELECT * FROM produtos_medicamentos WHERE id_produto = ?"
        cursor.execute(sql, (id_busca,))

        linha = cursor.fetchone()
        conexao.close()

        if linha:
            return ProdutoMedicamento(
                id_produto=linha[0],
                nome_produto=linha[1],
                categoria=linha[2],
                preco_unitario=linha[3],
                estoque=linha[4],
                id_fornecedor=linha[5],
                data_atualizacao=linha[6],
            )
        return None

    def atualizar_produto(self, produto: ProdutoMedicamento):
        conexao = self.db.conectar()
        cursor = conexao.cursor()

        sql = """
        UPDATE produtos_medicamentos
        SET nome_produto=?, categoria=?, preco_unitario=?, estoque=?, id_fornecedor=?, data_atualizacao=?
        WHERE id_produto=?
        """

        valores = (
            produto.nome_produto,
            produto.categoria,
            produto.preco_unitario,
            produto.estoque,
            produto.id_fornecedor,
            produto.data_atualizacao,
            produto.id_produto,
        )

        try:
            cursor.execute(sql, valores)
            conexao.commit()
            return True
        except sqlite3.Error as erro:
            print(f"Erro ao atualizar: {erro}")
            return False
        finally:
            conexao.close()

    def deletar_produto(self, id_produto):
        conexao = self.db.conectar()
        cursor = conexao.cursor()

        sql = "DELETE FROM produtos_medicamentos WHERE id_produto = ?"

        try:
            cursor.execute(sql, (id_produto,))
            conexao.commit()

            linhas_removidas = cursor.rowcount

            return linhas_removidas > 0

        except sqlite3.Error as erro:
            print(f"Erro ao deletar: {erro}")
            return False
        finally:
            conexao.close()

    def buscar_produtos_por_fornecedor(self, id_fornecedor):
        conexao = self.db.conectar()
        cursor = conexao.cursor()

        sql = "SELECT * FROM produtos_medicamentos WHERE id_fornecedor = ?"
        cursor.execute(sql, (id_fornecedor,))
        linhas = cursor.fetchall()

        produtos = []
        for linha in linhas:
            produto = ProdutoMedicamento(
                id_produto=linha[0],
                nome_produto=linha[1],
                categoria=linha[2],
                preco_unitario=linha[3],
                estoque=linha[4],
                id_fornecedor=linha[5],
                data_atualizacao=linha[6],
            )
            produtos.append(produto)

        conexao.close()
        return produtos
