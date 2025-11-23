from datetime import date


class ProdutoMedicamento:
    def __init__(
        self,
        id_produto,
        nome_produto,
        categoria,
        preco_unitario,
        estoque,
        id_fornecedor=None,
        data_atualizacao=None,
    ):
        self.id_produto = id_produto
        self.nome_produto = nome_produto
        self.categoria = categoria
        self.preco_unitario = preco_unitario
        self.estoque = estoque
        self.id_fornecedor = id_fornecedor
        self.data_atualizacao = (
            data_atualizacao if data_atualizacao else date.today().isoformat()
        )

    def __str__(self):
        return f"ID: {self.id_produto} | {self.nome_produto} | R$ {self.preco_unitario:.2f} | Est: {self.estoque}"
