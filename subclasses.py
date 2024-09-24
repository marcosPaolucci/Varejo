import json
import produto
from categoria import Categoria

def criar_subclasse(nome_categoria):
    categoria = Categoria.get_categoria_por_nome(nome_categoria)

    # Atributos adicionais da categoria
    atributos_adicionais = categoria.atributos_adicionais
    
    # Cria o dicionário de atributos da nova classe
    class_dict = {'__module__': __name__}
    
    # Define o construtor da nova classe
    def __init__(self, nome, quantidade, preco, descricao, fornecedor, *args):
        # Chama o construtor da classe base Produto
        produto.Produto.__init__(self, nome, quantidade, preco, descricao, fornecedor)
        
        # Verifica se o número de atributos adicionais está correto
        if len(args) != len(atributos_adicionais):
            raise ValueError(f"Esperado {len(atributos_adicionais)} atributos adicionais, mas {len(args)} foram fornecidos.")
        
        # Inicializa os atributos adicionais
        for i, atributo in enumerate(atributos_adicionais):
            setattr(self, atributo, args[i])
            
        # Adiciona o atributo categoria
        self.categoria = nome_categoria
        self.codigo = None

    # Adiciona o construtor ao dicionário de classe
    class_dict['__init__'] = __init__

    # Cria a nova subclasse dinamicamente
    nova_subclasse = type(nome_categoria, (produto.Produto,), class_dict)
    
    return nova_subclasse