import json
from fornecedor import Fornecedor
from categoria import Categoria

# Nome do arquivo onde o estoque será salvo
ARQUIVO_ESTOQUE = 'estoque.json'

def carregar_estoque():
    """Carrega o estoque do arquivo JSON, se existir."""
    try:
        with open(ARQUIVO_ESTOQUE, 'r', encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def salvar_estoque(estoque):
    """Salva o estoque no arquivo JSON."""
    with open(ARQUIVO_ESTOQUE, 'w', encoding="utf-8") as file:
        json.dump(estoque, file, indent=4)
    
def gerar_codigo_unico(estoque):
    """Gera um código único que não existe no estoque."""
    if not estoque:
        return 1  # Se o estoque estiver vazio, começa com 1
    else:
        # Gera o próximo código como sendo 1 maior que o maior código atual
        maior_codigo = max(item['codigo'] for item in estoque)
        return maior_codigo + 1

def adicionar_produto_estoque(produto):
    """Adiciona um produto ao estoque, gerando automaticamente o código."""
    estoque = carregar_estoque()
    
    codigo_unico = gerar_codigo_unico(estoque)
    
    produto_dict = vars(produto)
    produto_dict['codigo'] = codigo_unico
    
    # Converte o objeto fornecedor para um dicionário
    produto_dict['fornecedor'] = produto.fornecedor.to_dict()
    
    estoque.append(produto_dict)
    salvar_estoque(estoque)
    print(f"Produto {produto.nome} adicionado ao estoque com o código {codigo_unico}.")




def adicionar_quantidade_estoque(codigo):
    estoque = carregar_estoque()
    for item in estoque:
        if item['codigo'] == codigo:
            item['quantidade'] += 1
            salvar_estoque(estoque)
            return

def remover_quantidade_estoque(codigo):
    estoque = carregar_estoque()
    for item in estoque:
        if item['codigo'] == codigo:
            item['quantidade'] -= 1
            if item['quantidade'] < 0:
                item['quantidade'] = 0
            salvar_estoque(estoque)
            return

def alterar_quantidade_estoque(codigo, nova_quantidade):
    estoque = carregar_estoque()
    for item in estoque:
        if item['codigo'] == codigo:
            item['quantidade'] = nova_quantidade
            salvar_estoque(estoque)
            print(f"Quantidade do produto de código {codigo} altearado para {nova_quantidade}")
            return

def exibir_estoque():
    estoque = carregar_estoque()
    if estoque:
        print("-" * 20)
        contador = 0 
        for item in estoque:
            for atributo, valor in item.items():
                print(f"{atributo}: {valor}")
            print("-" * 20)  # Separador visual entre os produtos
            contador += 1
        print(f"Total de produtos no estoque: {contador}")
    else:
        print("\nEstoque vazio!")
        
def get_produto(codigo):
    estoque = carregar_estoque()
    for item in estoque:
        if item['codigo'] == codigo:
            from subclasses import criar_subclasse
            categoria_nome = item['categoria']
            
            # Criar a subclasse correta com base na categoria
            subclasse = criar_subclasse(categoria_nome)
            
            # Pegar os atributos adicionais da categoria
            categoria = Categoria.get_categoria_por_nome(categoria_nome)
            atributos_adicionais = categoria.atributos_adicionais if categoria else []
            
            # Separar os atributos adicionais do produto para passar como *args
            valores_adicionais = [item.get(attr) for attr in atributos_adicionais]
            
            # Criar o objeto do produto com todos os atributos esperados
            produto = subclasse(
                item['nome'],
                item['quantidade'],
                item['preço'],
                item['descricao'],
                item['fornecedor'],  # Lembrar de carregar o fornecedor correto
                *valores_adicionais
            )
            produto.codigo = item['codigo']
            return produto

    print("Produto não encontrado no estoque.")
    return None



def remover_produto(codigo):
    """Remove um produto do estoque com base no código."""
    estoque = carregar_estoque()
    for i, item in enumerate(estoque):
        if item['codigo'] == codigo:
            estoque.pop(i)
            salvar_estoque(estoque)
            print(f"Produto com código {codigo} removido do estoque.")
            return
    print(f"Produto com código {codigo} não encontrado no estoque.")

def atualizar_preco_estoque(codigo, novo_preco):
    """Atualiza o preço de um produto no estoque com base no código."""
    estoque = carregar_estoque()
    for item in estoque:
        if item['codigo'] == codigo:
            item['preço'] = novo_preco
            salvar_estoque(estoque)
            print(f"Preço do produto de código {codigo} atualizado para {novo_preco}")
            return
    print(f"Produto com código {codigo} não encontrado no estoque.")

def alterar_nome_estoque(codigo, novo_nome):
    """Altera o nome de um produto no estoque com base no código."""
    estoque = carregar_estoque()
    for item in estoque:
        if item['codigo'] == codigo:
            item['nome'] = novo_nome
            salvar_estoque(estoque)
            print(f"Nome do produto de código {codigo} alterado para {novo_nome}")
            return
    print(f"Produto com código {codigo} não encontrado no estoque.")

def alterar_descrição_estoque(codigo, nova_descrição):
    """Altera a descrição de um produto no estoque com base no código."""
    estoque = carregar_estoque()
    for item in estoque:
        if item['codigo'] == codigo:
            item['descricao'] = nova_descrição
            salvar_estoque(estoque)
            print(f"Descrição do produto de código {codigo} alterada para {nova_descrição}")
            return
    print(f"Produto com código {codigo} não encontrado no estoque.")