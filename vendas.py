# vendas.py

from estoque import get_produto
from conexão import get_collection
from datetime import datetime
from pymongo.errors import PyMongoError

COLLECTION_NAME = "Vendas"

def Registrar_Venda(CPFcliente, codigoProdutos, quantidades, promocao=None):
    collection = get_collection(COLLECTION_NAME)
    total = 0
    itens_venda = []

    for codigo, quantidade in zip(codigoProdutos, quantidades):
        produto = get_produto(codigo)
        if produto:
            preco = produto.preco
            if promocao and codigo == promocao[0]:
                preco *= promocao[1]
            if produto.quantidade < quantidade:
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

    for item in itens_venda:
        produto = get_produto(item["codigo"])
        produto.remover_quantidade(item["quantidade"])

    print("Venda registrada com sucesso!")

    nota_fiscal = {
        "CPFcliente": CPFcliente,
        "itens": itens_venda,
        "total": total,
        "data_criacao": datetime.now()
    }

    try:
        result = collection.insert_one(nota_fiscal)
        print(f'Venda registrada com ID: {result.inserted_id}')
    except PyMongoError as e:
        print(f"Ocorreu um erro ao registrar a venda: {e}")
