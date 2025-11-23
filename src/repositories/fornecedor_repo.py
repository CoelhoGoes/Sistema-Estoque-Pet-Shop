import sqlite3
from models.fornecedor import Fornecedor
from config.database import Database


class FornecedorRepository:
    def __init__(self):
        self.db = Database()

    def salvar(self, fornecedor: Fornecedor):
        conexao = self.db.conectar()
        cursor = conexao.cursor()

        sql = """
        INSERT INTO fornecedores 
        (nome_fornecedor, cidade, contato, data_cadastro)
        VALUES (?, ?, ?, ?)
        """

        valores = (
            fornecedor.nome_fornecedor,
            fornecedor.cidade,
            fornecedor.contato,
            fornecedor.data_cadastro,
        )

        try:
            cursor.execute(sql, valores)
            conexao.commit()
            print(f"Fornecedor '{fornecedor.nome_fornecedor}' salvo com sucesso!")
        except sqlite3.Error as erro:
            print(f"Erro ao salvar: {erro}")
        finally:
            conexao.close()

    def listar_todos_fornecedores(self):
        conexao = self.db.conectar()
        cursor = conexao.cursor()

        sql = "SELECT * FROM fornecedores"
        cursor.execute(sql)

        linhas = cursor.fetchall()

        fornecedores = []
        for linha in linhas:
            fornecedor = Fornecedor(
                id_fornecedor=linha[0],
                nome_fornecedor=linha[1],
                cidade=linha[2],
                contato=linha[3],
                data_cadastro=linha[4],
            )
            fornecedores.append(fornecedor)

        conexao.close()
        return fornecedores

    def buscar_fornecedor_por_id(self, id_busca):
        conexao = self.db.conectar()
        cursor = conexao.cursor()

        sql = "SELECT * FROM fornecedores WHERE id_fornecedor = ?"
        cursor.execute(sql, (id_busca,))

        linha = cursor.fetchone()
        conexao.close()

        if linha:
            return Fornecedor(
                id_fornecedor=linha[0],
                nome_fornecedor=linha[1],
                cidade=linha[2],
                contato=linha[3],
                data_cadastro=linha[4],
            )
        return None

    def deletar_fornecedor(self, id_fornecedor):
        conexao = self.db.conectar()
        cursor = conexao.cursor()

        sql = "DELETE FROM fornecedores WHERE id_fornecedor = ?"

        try:
            cursor.execute(sql, (id_fornecedor,))
            conexao.commit()

            linhas_removidas = cursor.rowcount

            return linhas_removidas > 0

        except sqlite3.Error as erro:
            print(f"Erro ao deletar: {erro}")
            return False
        finally:
            conexao.close()
