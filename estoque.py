# estoque.py

estoque = []

def adicionar_produto_estoque(codigo, quantidade):
    for item in estoque:
        if item['codigo'] == codigo:
            item['quantidade'] += quantidade
            return
    estoque.append({'codigo': codigo, 'quantidade': quantidade})

def remover_produto_estoque(codigo, quantidade):
    for item in estoque:
        if item['codigo'] == codigo:
            item['quantidade'] -= quantidade
            if item['quantidade'] < 0:
                item['quantidade'] = 0
            return

def atualizar_produto_estoque(codigo, nova_quantidade):
    for item in estoque:
        if item['codigo'] == codigo:
            item['quantidade'] = nova_quantidade
            return

def exibir_estoque():
    for item in estoque:
        print(f"Código: {item['codigo']}, Quantidade: {item['quantidade']}")
