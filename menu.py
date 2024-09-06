# menu.py
from estoque import exibir_estoque, get_produto
from categoria import Categoria
from produto import Produto
from subclasses import criar_subclasse

def adicionar_categoria():
    nome = input("Digite o nome da categoria: ")
    # Verifica se o usuário inseriu atributos adicionais corretamente
    atributos_input = input("Digite os atributos adicionais da categoria (separados por vírgula): ").strip()
    # Filtra atributos válidos
    atributos = [atributo.strip() for atributo in atributos_input.split(',') if atributo.strip()]
    categoria = Categoria(nome, *atributos)
    categoria.criar_categoria()
    print(f"Categoria '{nome}' criada com sucesso.")

def criar_produto():
    categorias = Categoria.carregar_categorias()
    for i in categorias:
        print(i["nome_categoria"])
    nome_categoria = input("Digite o nome da categoria para criar o produto: ")
    Subclasse = criar_subclasse(nome_categoria)

    if Subclasse:
        categoria = Categoria.get_categoria_por_nome(nome_categoria)
        atributos_adicionais = []
        # Se a categoria tem atributos adicionais válidos, solicita os valores
        if categoria.atributos_adicionais:
            for i in categoria.atributos_adicionais:
                if i:  # Verifica se o atributo realmente existe
                    valor_atributo = input(f"Digite o valor de {i}: ").strip() or ""
                    atributos_adicionais.append(valor_atributo)
        # Preenche com strings vazias se a categoria não possuir atributos adicionais
        else:
            atributos_adicionais = [""] * len(categoria.atributos_adicionais)

        # Corrige para garantir que o número de valores corresponda ao número de atributos
        while len(atributos_adicionais) < len(categoria.atributos_adicionais):
            atributos_adicionais.append("")  # Adiciona strings vazias até que os comprimentos coincidam

        nome_produto = input("Digite o nome do produto: ")
        preco = float(input("Digite o preço do produto: "))
        quantidade = int(input("Digite a quantidade do produto: "))
        descricao = input("Digite a descrição do produto: ")
        fornecedor = input("Digite a marca do produto: ")
        produto = Subclasse(nome_produto, quantidade, preco, descricao, fornecedor, *atributos_adicionais)
        produto.adicionar_produto()
        print(f"Produto '{nome_produto}' adicionado com sucesso.")
    else:
        print("Categoria não encontrada.")



def gerenciar_produto():
    codigo = int(input("Digite o código do produto: "))
    produto = get_produto(codigo)
    if produto:
        while True:
            print("\nEscolha uma ação:")
            print("1. Adicionar quantidade")
            print("2. Remover quantidade")
            print("3. Atualizar quantidade")
            print("4. Atualizar preço")
            print("5. Remover produto")
            print("6. Voltar ao menu principal")
            escolha = input("Escolha uma opção: ")

            if escolha == '1':
                quantidade = int(input("Digite a quantidade a ser adicionada: "))
                produto.adicionar_quantidade(quantidade)
                print("Quantidade adicionada com sucesso.")
            elif escolha == '2':
                quantidade = int(input("Digite a quantidade a ser removida: "))
                produto.remover_quantidade(quantidade)
                print("Quantidade removida com sucesso.")
            elif escolha == '3':
                nova_quantidade = int(input("Digite a nova quantidade: "))
                produto.atualizar_quantidade(nova_quantidade)
                print("Quantidade atualizada com sucesso.")
            elif escolha == '4':
                novo_preço = float(input("Digite o novo preço: "))
                produto.atualizar_preço(novo_preço)
                print("Preço atualizado com sucesso.")
            elif escolha == '5':
                produto.remover_produto()
                print("Produto removido com sucesso.")
            elif escolha == '6':
                break
            else:
                print("Opção inválida. Tente novamente.")
    else:
        print("Produto não encontrado.")

def exibir_categorias():
    categorias = Categoria.carregar_categorias()
    if categorias:
        for categoria in categorias:
            print(categoria)
    else:
        print("Nenhuma categoria encontrada.")

def gerenciar_categoria():
    nome_categoria = input("Digite o nome da categoria: ")
    categoria = Categoria.get_categoria_por_nome(nome_categoria)
    if categoria:
        while True:
            print("\nEscolha uma ação:")
            print("1. Modificar atributos adicionais")
            print("2. Remover categoria")
            print("3. Voltar ao menu principal")
            escolha = input("Escolha uma opção: ")

            if escolha == '1':
                novos_atributos = input("Digite os novos atributos (separados por vírgula): ").split(',')
                categoria.modificar_atributos_adicionais(novos_atributos)
                print("Atributos modificados com sucesso.")
                print("Atributos atuais:", categoria.atributos_adicionais)
            elif escolha == '2':
                categoria.remover_categoria()
                print("Categoria removida com sucesso.")
                break
            elif escolha == '3':
                break
            else:
                print("Opção inválida. Tente novamente.")
    else:
        print("Categoria não encontrada.")

def mostrar_menu():
    while True:
        print("\nMenu Principal:")
        print("1. Adicionar Categoria")
        print("2. Criar Produto")
        print("3. Gerenciar Produto")
        print("4. Exibir Todos os Produtos")
        print("5. Exibir Todas as Categorias")
        print("6. Gerenciar Categoria")
        print("7. Sair")
        
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            adicionar_categoria()
        elif escolha == '2':
            criar_produto()
        elif escolha == '3':
            gerenciar_produto()
        elif escolha == '4':
            exibir_estoque()
        elif escolha == '5':
            exibir_categorias()
        elif escolha == '6':
            gerenciar_categoria()
        elif escolha == '7':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")
