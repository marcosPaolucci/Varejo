import json

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
    
    # Gerar código único para o novo produto
    codigo_unico = gerar_codigo_unico(estoque)
    
    # Adicionar o código ao dicionário do produto
    produto_dict = vars(produto)
    produto_dict['codigo'] = codigo_unico
    
    # Adicionar o produto ao estoque e salvar
    estoque.append(produto_dict)
    salvar_estoque(estoque)
    print(f"Produto {produto.nome} adicionado ao estoque com o código {codigo_unico}.")

def adicionar_quantidade_estoque(codigo, quantidade):
    estoque = carregar_estoque()
    for item in estoque:
        if item['codigo'] == codigo:
            item['quantidade'] += quantidade
            salvar_estoque(estoque)
            return

def remover_quantidade_estoque(codigo, quantidade):
    estoque = carregar_estoque()
    for item in estoque:
        if item['codigo'] == codigo:
            item['quantidade'] -= quantidade
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
    for item in estoque:
        for atributo, valor in item.items():
            print(f"{atributo}: {valor}")
        print("-" * 20)  # Separador visual entre os produtos
    
def get_produto(codigo):
    estoque = carregar_estoque()
    for item in estoque:
        if item['codigo'] == codigo:
            from subclasses import criar_subclasse
            produto = {}
            for atributo, valor in item.items():
                produto[atributo] = valor

            subclasse = criar_subclasse(produto['categoria'])
            del produto['categoria']
            produtoobj = subclasse(*produto.values())  # Passando os argumentos como valor de *args
            produtoobj.codigo = produto['codigo']
            return produtoobj

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
