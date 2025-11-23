import sqlite3
import os


class Database:
    def __init__(self, db_name="app.db"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, "../../data")

        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        self.db_path = os.path.join(data_dir, db_name)

    def conectar(self):
        return sqlite3.connect(self.db_path)

    def inicializar_tabelas(self):
        conexao = self.conectar()
        cursor = conexao.cursor()

        db_pet_shop = """
        DROP TABLE IF EXISTS produtos_medicamentos;
        DROP TABLE IF EXISTS fornecedores;

        CREATE TABLE fornecedores (
            id_fornecedor INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_fornecedor VARCHAR(100) NOT NULL,
            cidade VARCHAR(80),
            contato VARCHAR(100),
            data_cadastro DATE
        );
        
        CREATE TABLE produtos_medicamentos (
            id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_produto VARCHAR(100) NOT NULL,
            categoria VARCHAR(60),
            preco_unitario NUMERIC(10,2),
            estoque INT,
            id_fornecedor INT REFERENCES fornecedores(id_fornecedor),
            data_atualizacao DATE
        );
        """

        cursor.executescript(db_pet_shop)
        conexao.commit()
        conexao.close()
        print("Banco de dados verificado/criado com sucesso!")
