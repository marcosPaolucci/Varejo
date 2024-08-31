import json
import os

class Categoria:
    arquivo_json = 'categorias.json'

    def __init__(self, nome_categoria, *atributos_adicionais):
        self.nome_categoria = nome_categoria
        self.atributos_adicionais = list(atributos_adicionais)

    def criar_categoria(self):
        categorias = self.carregar_categorias()

        # Verifica se a categoria já existe para evitar duplicação
        if not any(c['nome_categoria'] == self.nome_categoria for c in categorias):
            categorias.append({
                'nome_categoria': self.nome_categoria,
                'atributos_adicionais': self.atributos_adicionais
            })

            with open(self.arquivo_json, 'w') as f:
                json.dump(categorias, f, indent=4)
            print(f'Categoria "{self.nome_categoria}" criada com sucesso.')
        else:
            print(f'Categoria "{self.nome_categoria}" já existe.')
        
    def alterar_categoria(self):
        

    
    @classmethod
    def carregar_categorias(self):
        if os.path.exists(self.arquivo_json):
            with open(self.arquivo_json, 'r') as f:
                return json.load(f)
        else:
            return []
        
    @classmethod
    def get_categoria_por_nome(cls, nome_categoria):
        categorias = cls.carregar_categorias()
        for categoria_data in categorias:
            if categoria_data['nome_categoria'] == nome_categoria:
                nome_categoria = categoria_data['nome_categoria']
                atributos_adicionais = categoria_data.get('atributos_adicionais', [])
                return cls(nome_categoria, *atributos_adicionais)  # Instancia um novo objeto Categoria
        print(f'Categoria "{nome_categoria}" não encontrada.')
        return None  # Retorna None se não encontrar a categoria
            
    @classmethod
    def remover_categoria(cls, nome_categoria):
        categorias = cls.carregar_categorias()

        categorias_filtradas = [c for c in categorias if c['nome_categoria'] != nome_categoria]

        if len(categorias) == len(categorias_filtradas):
            print(f'Categoria "{nome_categoria}" não encontrada.')
        else:
            with open(cls.arquivo_json, 'w') as f:
                json.dump(categorias_filtradas, f, indent=4)
            print(f'Categoria "{nome_categoria}" removida com sucesso.')


