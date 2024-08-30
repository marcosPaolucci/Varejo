import json
from produto import Produto

# Classe Categoria que cria subclasses e as armazena em um dicionário
class Categoria:
    subclasses = {}

    def __init__(self, nome_categoria):
        self.nome_categoria = nome_categoria
        self.criar_subclasse()
        self.salvar_categoria()

    def criar_subclasse(self):
        subclass = type(self.nome_categoria, (Produto,), {"categoria": self.nome_categoria})
        Categoria.subclasses[self.nome_categoria] = subclass

    def salvar_categoria(self):
        try:
            with open("categorias.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {"categorias": []}

        if self.nome_categoria not in data["categorias"]:
            data["categorias"].append(self.nome_categoria)
            with open("categorias.json", "w") as file:
                json.dump(data, file)

    @classmethod
    def carregar_categorias(cls):
        try:
            with open("categorias.json", "r") as file:
                data = json.load(file)
                for nome_categoria in data["categorias"]:
                    cls(nome_categoria)
        except FileNotFoundError:
            print("Nenhuma categoria encontrada. Criando novo arquivo de categorias.")
            with open("categorias.json", "w") as file:
                json.dump({"categorias": []}, file)

    @classmethod
    def get_subclasse(cls, nome_categoria):
        return cls.subclasses.get(nome_categoria)

# Inicializando o sistema e carregando as categorias do JSON
Categoria.carregar_categorias()

