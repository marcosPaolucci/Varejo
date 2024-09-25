from estoque import get_produto
from conexão import get_collection
COLLECTION_NAME = "Vendas"
collection = get_collection(COLLECTION_NAME)
from datetime import datetime

def Registrar_Venda(CPFcliente, codigoProdutos, quantidades, promoção=None):
    # Inicializa o total
    total = 0
    itens_venda = []

    # Percorre os produtos e suas quantidades
    for codigo, quantidade in zip(codigoProdutos, quantidades):
        produto = get_produto(codigo)  # Busca o produto pelo código diretamente do MongoDB
        if produto:
            preco = produto.preço  # Obtém o preço do produto
            if promoção:
                if codigo == promoção[0]:
                    preco = preco * promoção[1]
            quantidade_estoque = produto.quantidade
            if quantidade_estoque < quantidade:
                print(f"Quantidade insuficiente no estoque para o produto: {produto.nome}")
                return
            subtotal = preco * quantidade
            total += subtotal
            itens_venda.append({
                "codigo": codigo,
                "nome": produto.nome,
                "quantidade": quantidade,
                "preco_unitario": preco,
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
            produto.remover_quantidade()  # Atualiza a quantidade diretamente no MongoDB

    print("Venda registrada com sucesso!")
    
    # Retorna um dicionário com os dados da venda
    nota_fiscal = {
        "CPFcliente": CPFcliente,
        "itens": itens_venda,
        "total": total,
        "data_criacao": datetime.now()  
    }
    result = collection.insert_one(nota_fiscal)
    print(f'Venda registrada com ID: {result.inserted_id}')
    return 

#venda = Registrar_Venda("12345678900", [1], [2], [1,0.5])  # Código 1 (Geladeira), Código 2 (A Bela Adormecida)
print(list(collection.find({  "itens" : { "$elemMatch" : { "nome": "oculos" } } })) )

