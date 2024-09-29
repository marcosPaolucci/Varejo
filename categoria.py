from conexão import get_collection
from pymongo.errors import PyMongoError  # Exceções específicas do pymongo
import logging

# Configurar o logger
logging.basicConfig(level=logging.INFO)

COLLECTION_NAME = "Categorias"

class Categoria:
    def __init__(self, nome_categoria, *atributos_adicionais):
        self.nome_categoria = nome_categoria
        self.atributos_adicionais = list(atributos_adicionais)
        self.collection = get_collection(COLLECTION_NAME)  

    def criar_categoria(self):
        try:
            self.atributos_adicionais = [attr.strip() for attr in self.atributos_adicionais if attr.strip()]
            if self.collection.find_one({'nome_categoria': self.nome_categoria}) is None:
                categoria_data = {
                    'nome_categoria': self.nome_categoria,
                    'atributos_adicionais': self.atributos_adicionais
                }
                self.collection.insert_one(categoria_data)
                logging.info(f'Categoria "{self.nome_categoria}" criada com sucesso.')
            else:
                logging.info(f'Categoria "{self.nome_categoria}" já existe.')
        except PyMongoError as e:
            logging.error(f"Ocorreu um erro ao criar a categoria no MongoDB: {e}")

    def modificar_atributos_adicionais(self, novos_atributos_adicionais):
        try:
            self.atributos_adicionais = [attr.strip() for attr in novos_atributos_adicionais if attr.strip()]
            resultado = self.collection.update_one(
                {'nome_categoria': self.nome_categoria},
                {'$set': {'atributos_adicionais': self.atributos_adicionais}}
            )
            if resultado.modified_count > 0:
                print(f"Categoria '{self.nome_categoria}' modificada com sucesso!")
            else:
                print(f"Categoria '{self.nome_categoria}' não encontrada ou não foi modificada.")
        except PyMongoError as e:
            print(f"Ocorreu um erro ao modificar os atributos da categoria no MongoDB: {e}")

    def remover_categoria(self):
        try:
            resultado = self.collection.delete_one({'nome_categoria': self.nome_categoria})
            if resultado.deleted_count > 0:
                print(f'Categoria "{self.nome_categoria}" removida com sucesso.')
            else:
                print(f'Categoria "{self.nome_categoria}" não encontrada.')
        except PyMongoError as e:
            print(f"Ocorreu um erro ao remover a categoria no MongoDB: {e}")

    @classmethod
    def get_categoria_por_nome(cls, nome_categoria):
        try:
            collection = get_collection(COLLECTION_NAME)  # Obter a coleção no método de classe
            categoria_data = collection.find_one({'nome_categoria': nome_categoria})
            if categoria_data:
                atributos_adicionais = categoria_data.get('atributos_adicionais', [])
                return cls(nome_categoria, *atributos_adicionais)
            else:
                print(f'Categoria "{nome_categoria}" não encontrada.')
                return None
        except PyMongoError as e:
            print(f"Ocorreu um erro ao buscar a categoria no MongoDB: {e}")
            return None

    @classmethod
    def exibir_categorias_existentes(cls):
        try:
            collection = get_collection(COLLECTION_NAME)
            categorias = list(collection.find())
            if categorias:
                return categorias
            else:
                logging.info("Nenhuma categoria encontrada.")
                return []
        except PyMongoError as e:
            logging.error(f"Ocorreu um erro ao exibir categorias: {e}")
            return []

    @classmethod
    def buscar_todas_categorias(cls):
        try:
            collection = get_collection(COLLECTION_NAME)
            return collection.find()
        except PyMongoError as e:
            print(f"Ocorreu um erro ao buscar todas as categorias: {e}")
            return []
