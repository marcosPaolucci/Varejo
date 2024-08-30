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

def adicionar_produto_estoque(codigo, quantidade):
    for item in estoque:
        if item['codigo'] == codigo:
            print("Produto já existe no estoque.")
            return
    estoque.append({'codigo': codigo, 'quantidade': quantidade})
    salvar_estoque()  # Salva o estoque após a adição
    print(f"Produto com código {codigo} adicionado ao estoque com quantidade {quantidade}.")

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
        print(f"Código: {item['codigo']}, Quantidade: {item['quantidade']}")
