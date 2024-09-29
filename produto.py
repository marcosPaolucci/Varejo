# produto.py

from fornecedor import Fornecedor
from conexão import get_collection
from pymongo.errors import PyMongoError

class Produto:
    COLLECTION_NAME = "Produtos"

    def __init__(self, nome, quantidade, preco, descricao, fornecedor, codigo=None, collection=None):
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco
        self.descricao = descricao
        self.fornecedor = fornecedor
        self.codigo = codigo
        if collection is None:
            self.collection = get_collection(self.COLLECTION_NAME)
        else:
            self.collection = collection

    def adicionar_produto(self):
        try:
            if self.collection.find_one({'nome': self.nome}) is None:
                produto_data = self.to_dict()
                resultado = self.collection.insert_one(produto_data)
                self.codigo = resultado.inserted_id  # Ou gere um código conforme sua lógica
                print(f"Produto '{self.nome}' adicionado com o código {self.codigo}.")
            else:
                print(f"Produto '{self.nome}' já existe no estoque.")
        except PyMongoError as e:
            print(f"Ocorreu um erro ao adicionar o produto ao estoque: {e}")
            print("Falha ao adicionar o produto ao estoque.")

    def adicionar_quantidade(self, quantidade):
        try:
            resultado = self.collection.update_one(
                {'codigo': self.codigo},
                {'$inc': {'quantidade': quantidade}}
            )
            if resultado.modified_count and resultado.modified_count > 0:
                self.quantidade += quantidade
                print(f"Quantidade do produto '{self.nome}' aumentada em {quantidade}.")
            else:
                print("Falha ao adicionar quantidade.")
        except PyMongoError as e:
            print(f"Ocorreu um erro ao adicionar quantidade: {e}")

    def remover_quantidade(self, quantidade):
        try:
            resultado = self.collection.update_one(
                {'codigo': self.codigo},
                {'$inc': {'quantidade': -quantidade}}
            )
            if resultado.modified_count and resultado.modified_count > 0:
                self.quantidade -= quantidade
                print(f"Quantidade do produto '{self.nome}' reduzida em {quantidade}.")
                self.alerta_estoque_baixo()
            else:
                print("Falha ao remover quantidade.")
        except PyMongoError as e:
            print(f"Ocorreu um erro ao remover quantidade: {e}")

    def atualizar_quantidade(self, nova_quantidade):
        try:
            resultado = self.collection.update_one(
                {'codigo': self.codigo},
                {'$set': {'quantidade': nova_quantidade}}
            )
            if resultado.modified_count and resultado.modified_count > 0:
                self.quantidade = nova_quantidade
                print(f"Quantidade do produto '{self.nome}' atualizada para {nova_quantidade}.")
                self.alerta_estoque_baixo()
            else:
                print("Falha ao atualizar quantidade.")
        except PyMongoError as e:
            print(f"Ocorreu um erro ao atualizar quantidade: {e}")

    def atualizar_preco(self, novo_preco):
        try:
            resultado = self.collection.update_one(
                {'codigo': self.codigo},
                {'$set': {'preço': novo_preco}}
            )
            if resultado.modified_count and resultado.modified_count > 0:
                self.preco = novo_preco
                print(f"Preço do produto '{self.nome}' atualizado para {self.preco}.")
            else:
                print("Falha ao atualizar preço.")
        except PyMongoError as e:
            print(f"Ocorreu um erro ao atualizar preço: {e}")

    def remover_produto(self):
        try:
            resultado = self.collection.delete_one({'codigo': self.codigo})
            if resultado.deleted_count and resultado.deleted_count > 0:
                print(f"Produto '{self.nome}' removido do estoque.")
            else:
                print("Falha ao remover o produto.")
        except PyMongoError as e:
            print(f"Ocorreu um erro ao remover o produto: {e}")

    def alterar_nome(self, novo_nome):
        try:
            resultado = self.collection.update_one(
                {'codigo': self.codigo},
                {'$set': {'nome': novo_nome}}
            )
            if resultado.modified_count and resultado.modified_count > 0:
                self.nome = novo_nome
                print(f"Nome do produto atualizado para '{self.nome}'.")
            else:
                print("Falha ao alterar o nome do produto.")
        except PyMongoError as e:
            print(f"Ocorreu um erro ao alterar o nome do produto: {e}")

    def alterar_descricao(self, nova_descricao):
        try:
            resultado = self.collection.update_one(
                {'codigo': self.codigo},
                {'$set': {'descricao': nova_descricao}}
            )
            if resultado.modified_count and resultado.modified_count > 0:
                self.descricao = nova_descricao
                print(f"Descrição do produto atualizada.")
            else:
                print("Falha ao alterar a descrição do produto.")
        except PyMongoError as e:
            print(f"Ocorreu um erro ao alterar a descrição do produto: {e}")

    def alerta_estoque_baixo(self):
        if self.quantidade < 5:
            print("Cuidado! Estoque baixo!")

    def to_dict(self):
        return {
            'nome': self.nome,
            'quantidade': self.quantidade,
            'preço': self.preco,
            'descricao': self.descricao,
            'fornecedor': self.fornecedor.nome if isinstance(self.fornecedor, Fornecedor) else self.fornecedor,
            'codigo': self.codigo
        }
