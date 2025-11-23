CREATE TABLE IF NOT EXISTS fornecedores (
    id_fornecedor INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_fornecedor VARCHAR(100) NOT NULL,
    cidade VARCHAR(80),
    contato VARCHAR(100),
    data_cadastro DATE
);

CREATE TABLE IF NOT EXISTS produtos_medicamentos (
    id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_produto VARCHAR(100) NOT NULL,
    categoria VARCHAR(60),
    preco_unitario NUMERIC(10,2),
    estoque INT,
    id_fornecedor INT REFERENCES fornecedores(id_fornecedor),
    data_atualizacao DATE
);