from datetime import date


class Fornecedor:
    def __init__(
        self,
        id_fornecedor,
        nome_fornecedor,
        cidade,
        contato,
        data_cadastro=None,
    ):
        self.id_fornecedor = id_fornecedor
        self.nome_fornecedor = nome_fornecedor
        self.cidade = cidade
        self.contato = contato
        self.data_cadastro = (
            data_cadastro if data_cadastro else date.today().isoformat()
        )

    def __str__(self):
        return f"ID: {self.id_fornecedor} | {self.nome_fornecedor} | {self.cidade} | Contato: {self.contato}"
