import json
from estoque import get_produto

def Registrar_Venda(CPFcliente, codigoProdutos, quantidades, promoção=None):
    # Abre e lê o arquivo estoque.json (que agora é uma lista de JSONs)
    with open('estoque.json', 'r') as f:
        estoque = json.load(f)

    # Função para localizar o produto no estoque pelo código
    def buscar_produto_por_codigo(codigo):
        for produto in estoque:
            if produto["codigo"] == codigo:
                return produto
        return None

    # Inicializa o total
    total = 0
    itens_venda = []

    # Percorre os produtos e suas quantidades
    for codigo, quantidade in zip(codigoProdutos, quantidades):
        produto = buscar_produto_por_codigo(codigo)  # Busca o produto pelo código
        if produto:
            preco = produto["preço"]  # Obtém o preço do produto
            if promoção:
                if codigo == promoção[0]:
                    preco = preco * promoção[1]
            quantidade_estoque = produto["quantidade"]
            if quantidade_estoque < quantidade:
                print(f"Quantidade insuficiente no estoque para o produto: {produto['nome']}")
                return
            subtotal = preco * quantidade
            total += subtotal
            itens_venda.append({
                "codigo": codigo,
                "nome": produto["nome"],
                "quantidade": quantidade,
                "preço_unitario": preco,
                "subtotal": subtotal
            })
        else:
            print(f"Produto com código {codigo} não encontrado no estoque.")
            return 
    
    # Atualiza a quantidade de produtos no estoque
    for item in itens_venda:
        produto = get_produto(item["codigo"])
        quantidade = item["quantidade"]
        for i in range(quantidade):
            produto.remover_quantidade()

    print("Venda Registrada com sucesso! ")
    # Retorna um dicionário com os dados da venda
    return {
        "CPFcliente": CPFcliente,
        "itens": itens_venda,
        "total": total
    }

# Exemplo de uso:
#venda = Registrar_Venda("12345678900", [1, 2], [1, 1])  # Código 1 (Geladeira), Código 2 (A Bela Adormecida)
venda = Registrar_Venda("12345678900", [2], [2], [2,0.5])  # Código 1 (Geladeira), Código 2 (A Bela Adormecida)
print(venda["total"])  # Imprime o total da venda
print(venda["itens"])
print(venda["CPFcliente"])
