import json
import produto

def criar_subclasse(nome_categoria):
    # Carregar categorias do arquivo JSON
    try:
        with open('categorias.json', 'r') as f:
            categorias = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError('O arquivo categorias.json não foi encontrado.')
    except json.JSONDecodeError:
        raise ValueError('Erro ao decodificar o arquivo JSON. Verifique o formato do arquivo.')

    # Encontrar a categoria correspondente
    categoria = next((cat for cat in categorias if cat['nome_categoria'] == nome_categoria), None)
    
    if categoria is None:
        raise ValueError(f'Categoria "{nome_categoria}" não encontrada.')

    # Atributos adicionais da categoria
    atributos_adicionais = categoria.get('atributos_adicionais', [])
    
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