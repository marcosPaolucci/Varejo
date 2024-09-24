from conexão import get_collection
COLLECTION_NAME = "Categorias"
collection = get_collection(COLLECTION_NAME)

class Categoria:
    def __init__(self, nome_categoria, *atributos_adicionais):
        self.nome_categoria = nome_categoria
        self.atributos_adicionais = list(atributos_adicionais)

   
    def criar_categoria(self):

        # Verifica se a categoria já existe
        if collection.find_one({'nome_categoria': self.nome_categoria}) is None:
            # Insere a nova categoria no MongoDB
            categoria_data = {
                'nome_categoria': self.nome_categoria,
                'atributos_adicionais': self.atributos_adicionais
            }
            collection.insert_one(categoria_data)
            print(f'Categoria "{self.nome_categoria}" criada com sucesso.')
        else:
            print(f'Categoria "{self.nome_categoria}" já existe.')

    def modificar_atributos_adicionais(self, novos_atributos_adicionais):
        self.atributos_adicionais = novos_atributos_adicionais

        # Atualiza a categoria com o novo atributo
        resultado = collection.update_one(
            {'nome_categoria': self.nome_categoria},
            {'$set': {'atributos_adicionais': self.atributos_adicionais}}
        )

        if resultado.modified_count > 0:
            print(f"Categoria {self.nome_categoria} modificada com sucesso!")
        else:
            print(f"Categoria {self.nome_categoria} não encontrada ou não foi modificada.")

    def remover_categoria(self):

        # Remove a categoria do MongoDB
        resultado = collection.delete_one({'nome_categoria': self.nome_categoria})

        if resultado.deleted_count > 0:
            print(f'Categoria "{self.nome_categoria}" removida com sucesso.')
        else:
            print(f'Categoria "{self.nome_categoria}" não encontrada.')

    @classmethod
    def get_categoria_por_nome(cls, nome_categoria):

        categoria_data = collection.find_one({'nome_categoria': nome_categoria})
        if categoria_data:
            nome_categoria = categoria_data['nome_categoria']
            atributos_adicionais = categoria_data.get('atributos_adicionais', [])
            return cls(nome_categoria, *atributos_adicionais)  # Retorna uma nova instância de Categoria
        else:
            print(f'Categoria "{nome_categoria}" não encontrada.')
            return None

    @classmethod
    def exibir_categorias_existentes(cls):

        #categorias = list(collection.find({}, {'_id': 0, 'nome_categoria': 1}))  # Busca apenas os nomes das categorias
        categorias = list(collection.find())  # Busca apenas os nomes das categorias
        if categorias:
            print("Categorias existentes:")
            for idx, categoria in enumerate(categorias, start=1):
                print(f"{idx}. {categoria['nome_categoria']}")
        else:
            print("Nenhuma categoria encontrada.")

