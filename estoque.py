from fornecedor import Fornecedor
from categoria import Categoria
from conexão import get_collection
COLLECTION_NAME = "Produtos"
collection = get_collection(COLLECTION_NAME)


def gerar_codigo_unico():

    produto_com_maior_codigo = collection.find_one(sort=[('codigo', -1)])
    if produto_com_maior_codigo:
        return produto_com_maior_codigo['codigo'] + 1
    else:
        return 1  # Se não há produtos, começa com 1
    
def adicionar_produto_estoque(produto):

    # Gera o código único para o produto
    codigo_unico = gerar_codigo_unico()

    produto_dict = vars(produto)
    produto_dict['codigo'] = codigo_unico

    # Converte o objeto fornecedor para um dicionário
    produto_dict['fornecedor'] = produto.fornecedor.to_dict()

    # Insere o produto no MongoDB
    collection.insert_one(produto_dict)
    print(f"Produto {produto.nome} adicionado ao estoque com o código {codigo_unico}.")

def adicionar_quantidade_estoque(codigo):

    collection.update_one(
        {'codigo': codigo},
        {'$inc': {'quantidade': 1}}
    )
    print(f"Quantidade do produto de código {codigo} aumentada em 1.")

def remover_quantidade_estoque(codigo):

    collection.update_one(
        {'codigo': codigo},
        {'$inc': {'quantidade': -1}}
    )
    print(f"Quantidade do produto de código {codigo} reduzida em 1.")

def alterar_quantidade_estoque(codigo, nova_quantidade):

    collection.update_one(
        {'codigo': codigo},
        {'$set': {'quantidade': nova_quantidade}}
    )
    print(f"Quantidade do produto de código {codigo} alterada para {nova_quantidade}.")

def exibir_estoque():

    estoque = list(collection.find({}))

    if estoque:
        print("-" * 20)
        for contador, item in enumerate(estoque, start=1):
            for atributo, valor in item.items():
                print(f"{atributo}: {valor}")
            print("-" * 20)
        print(f"Total de produtos no estoque: {contador}")
    else:
        print("\nEstoque vazio!")

def get_produto(codigo):

    item = collection.find_one({'codigo': codigo})

    if item:
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

    resultado = collection.delete_one({'codigo': codigo})

    if resultado.deleted_count > 0:
        print(f"Produto com código {codigo} removido do estoque.")
    else:
        print(f"Produto com código {codigo} não encontrado no estoque.")

def atualizar_preco_estoque(codigo, novo_preco):

    resultado = collection.update_one(
        {'codigo': codigo},
        {'$set': {'preço': novo_preco}}
    )
    if resultado.matched_count > 0:
        print(f"Preço do produto de código {codigo} atualizado para {novo_preco}")
    else:
        print(f"Produto com código {codigo} não encontrado no estoque.")

def alterar_nome_estoque(codigo, novo_nome):

    resultado = collection.update_one(
        {'codigo': codigo},
        {'$set': {'nome': novo_nome}}
    )
    if resultado.matched_count > 0:
        print(f"Nome do produto de código {codigo} alterado para {novo_nome}")
    else:
        print(f"Produto com código {codigo} não encontrado no estoque.")

def alterar_descrição_estoque(codigo, nova_descrição):

    resultado = collection.update_one(
        {'codigo': codigo},
        {'$set': {'descricao': nova_descrição}}
    )
    if resultado.matched_count > 0:
        print(f"Descrição do produto de código {codigo} alterada para {nova_descrição}")
    else:
        print(f"Produto com código {codigo} não encontrado no estoque.")


    
