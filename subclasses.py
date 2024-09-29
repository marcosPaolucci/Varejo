import json
import produto
from categoria import Categoria

# Dicionário de cache para subclasses
_subclasses_cache = {}

def criar_subclasse(nome_categoria):
    if nome_categoria in _subclasses_cache:
        return _subclasses_cache[nome_categoria]
    
    try:
        categoria = Categoria.get_categoria_por_nome(nome_categoria)
        if not categoria:
            raise ValueError(f"Categoria '{nome_categoria}' não encontrada. Não foi possível criar a subclasse.")
        
        atributos_adicionais = categoria.atributos_adicionais
        
        # Validação dos atributos adicionais
        for attr in atributos_adicionais:
            if not attr.isidentifier():
                raise ValueError(f"Atributo adicional '{attr}' não é um identificador válido em Python.")
        
        class_dict = {'__module__': __name__}
        
        def __init__(self, nome, quantidade, preco, descricao, fornecedor, *args):
            produto.Produto.__init__(self, nome, quantidade, preco, descricao, fornecedor)
            
            if len(args) != len(atributos_adicionais):
                raise ValueError(f"Esperado {len(atributos_adicionais)} atributos adicionais, mas {len(args)} foram fornecidos.")
            
            for i, atributo in enumerate(atributos_adicionais):
                setattr(self, atributo, args[i])
                
            self.categoria = nome_categoria
            self.codigo = None
        
        class_dict['__init__'] = __init__
        
        nova_subclasse = type(nome_categoria, (produto.Produto,), class_dict)
        
        # Armazena a subclasse no cache
        _subclasses_cache[nome_categoria] = nova_subclasse
        
        return nova_subclasse
    except Exception as e:
        print(f"Ocorreu um erro ao criar a subclasse para a categoria '{nome_categoria}': {e}")
        return None
