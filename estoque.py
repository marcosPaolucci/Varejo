import json

# Nome do arquivo onde o estoque será salvo
ARQUIVO_ESTOQUE = 'estoque.json'

# Tenta carregar o estoque do arquivo, se existir
try:
    with open(ARQUIVO_ESTOQUE, 'r') as file:
        estoque = json.load(file)
except FileNotFoundError:
    estoque = []

def salvar_estoque():
    """Salva o estoque no arquivo JSON."""
    with open(ARQUIVO_ESTOQUE, 'w') as file:
        json.dump(estoque, file, indent=4)

def adicionar_produto_estoque(produto):
    """Adiciona um produto ao estoque. Recebe um objeto da classe Produto."""
    produto_dict = vars(produto)
    for item in estoque:
        if item['codigo'] == produto_dict['codigo']:
            print("Produto já existe no estoque.")
            return
    estoque.append(produto_dict)
    salvar_estoque()
    print(f"Produto {produto.nome} adicionado ao estoque.")

def adicionar_quantidade_estoque(codigo, quantidade):
    for item in estoque:
        if item['codigo'] == codigo:
            item['quantidade'] += quantidade
            salvar_estoque()  # Salva o estoque após a remoção
            return

def remover_quantidade_estoque(codigo, quantidade):
    for item in estoque:
        if item['codigo'] == codigo:
            item['quantidade'] -= quantidade
            if item['quantidade'] < 0:
                item['quantidade'] = 0
            salvar_estoque()  # Salva o estoque após a remoção
            return

def alterar_quantidade_estoque(codigo, nova_quantidade):
    for item in estoque:
        if item['codigo'] == codigo:
            item['quantidade'] = nova_quantidade
            salvar_estoque()  # Salva o estoque após a atualização
            return

def exibir_estoque():
    for item in estoque:
        for atributo, valor in item.items():
            print(f"{atributo}: {valor}")
        print("-" * 20)  # Separador visual entre os produtos
    
def get_produto(codigo):
    for item in estoque:
        if item['codigo'] == codigo:
            from subclasses import criar_subclasse
            produto = {}
            for atributo, valor in item.items():
                produto[atributo] = valor

            subclasse = criar_subclasse(produto['categoria'])
            del produto['categoria']
            produtoobj = subclasse(*produto.values())  # Passando os argumentos como valor de *args
            return produtoobj

    print("Produto não encontrado no estoque.")
    return None

def remover_produto(codigo):
    """Remove um produto do estoque com base no código."""
    for i, item in enumerate(estoque):
        if item['codigo'] == codigo:
            estoque.pop(i)
            salvar_estoque()
            print(f"Produto com código {codigo} removido do estoque.")
            return
    print(f"Produto com código {codigo} não encontrado no estoque.")


def atualizar_preco_estoque(codigo, novo_preco):
     """Atualiza o preço de um produto no estoque com base no código."""
     for item in estoque:
        if item['codigo'] == codigo:
            item['preço'] = novo_preco
            salvar_estoque()  # Salva o estoque após a atualização
            print(f"Preço do produto de código {codigo} atualizado para {novo_preco}")
            return
     print(f"Produto com código {codigo} não encontrado no estoque.")