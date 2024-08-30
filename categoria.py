import json
import os

class Categoria:
    arquivo_json = 'categorias.json'

    def __init__(self, nome_categoria, *atributos_adicionais):
        self.nome_categoria = nome_categoria
        self.atributos_adicionais = list(atributos_adicionais)
        self.salvar_categoria()

    def salvar_categoria(self):
        categorias = self.carregar_categorias()

        # Verifica se a categoria já existe para evitar duplicação
        if not any(c['nome_categoria'] == self.nome_categoria for c in categorias):
            categorias.append({
                'nome_categoria': self.nome_categoria,
                'atributos_adicionais': self.atributos_adicionais
            })

            with open(self.arquivo_json, 'w') as f:
                json.dump(categorias, f, indent=4)
        else:
            print(f'Categoria "{self.nome_categoria}" já existe.')
    
    @classmethod
    def carregar_categorias(self):
        if os.path.exists(self.arquivo_json):
            with open(self.arquivo_json, 'r') as f:
                return json.load(f)
        else:
            return []

