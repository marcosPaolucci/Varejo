import json
import produto

def criar_subclasse(nome_categoria):
    # Carregar categorias do arquivo JSON
    with open('categorias.json', 'r') as f:
        categorias = json.load(f)
    
    # Encontrar a categoria correspondente
    categoria = next((cat for cat in categorias if cat['nome_categoria'] == nome_categoria), None)
    
    if categoria is None:
        raise ValueError(f'Categoria "{nome_categoria}" não encontrada.')

    # Atributos adicionais da categoria
    atributos_adicionais = categoria['atributos_adicionais']
    
    # Cria o dicionário de atributos da nova classe
    class_dict = {'__module__': __name__}
    
    # Define o construtor da nova classe
    def __init__(self, nome, quantidade, preço, descricao, fornecedor, *args):
        # Chama o construtor da classe base
        produto.Produto.__init__(self, nome, quantidade, preço, descricao, fornecedor)
        
        # Inicializa os atributos adicionais
        for i, atributo in enumerate(atributos_adicionais):
            setattr(self, atributo, args[i])
            
        # Adiciona o atributo categoria
        self.categoria = nome_categoria
        self.codigo = None

    # Adiciona o construtor ao dicionário de classe
    class_dict['__init__'] = __init__

    # Cria a nova subclasse
    nova_subclasse = type(nome_categoria, (produto.Produto,), class_dict)
    
    return nova_subclasse

