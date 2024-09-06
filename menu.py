from estoque import exibir_estoque, get_produto
from categoria import Categoria
from produto import Produto
from subclasses import criar_subclasse

def adicionar_categoria():
    nome = input("Digite o nome da categoria: ")
    atributos = input("Digite os atributos adicionais da categoria (separados por vírgula), Enter caso nenhum atributo adicional: ").split(',')
    
    # Remove strings vazias e espaços em branco
    atributos = [attr.strip() for attr in atributos if attr.strip()]

      # Verifica se há atributos
    if atributos:  # Se a lista não estiver vazia
        categoria = Categoria(nome, *atributos)
    else:  # Se não houver atributos adicionais
        categoria = Categoria(nome)
    categoria.criar_categoria()

def criar_produto():
    categorias = Categoria.carregar_categorias()
    if not categorias:
        print("\nNenhuma categoria encontrada! Crie uma categoria antes de adicionar um produto!")
        return
    Categoria.exibir_categorias_existentes(categorias)

    try:
        num_categoria = int(input("Digite o número da categoria para criar o produto: "))
        if num_categoria < 1 or num_categoria > len(categorias):
            print("Número de categoria inválido.")
            return
    except ValueError:
        print("Entrada inválida. Por favor, insira um número.")
        return
    
    nome_categoria = categorias[num_categoria - 1]['nome_categoria']
    Subclasse = criar_subclasse(nome_categoria)

    if Subclasse:
        categoria = Categoria.get_categoria_por_nome(nome_categoria)
        atributos_adicionais = []
        nome_produto = input("Digite o nome do produto: ")
        preco = float(input("Digite o preço do produto: "))
        quantidade = int(input("Digite a quantidade do produto: "))
        descricao = input("Digite a descrição do produto: ")
        fornecedor = input("Digite a marca do produto: ")
        if len(categoria.atributos_adicionais) > 0:
            for atributo in categoria.atributos_adicionais:
                valor = input(f"Digite o valor de {atributo}: ")
                atributos_adicionais.append(valor)
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
            print("1. Incrementar quantidade")
            print("2. Decrementar quantidade")
            print("3. Atualizar quantidade")
            print("4. Atualizar preço")
            print("5. Alterar nome do produto")
            print("6. Alterar descrição do produto")
            print("7. Remover produto")
            print("8. Voltar ao menu principal")
            escolha = input("Escolha uma opção: ")

            if escolha == '1':
                produto.adicionar_quantidade()
                print("Quantidade incrementada com sucesso.")
            elif escolha == '2':
                produto.remover_quantidade()
                print("Quantidade decrementada com sucesso.")
            elif escolha == '3':
                nova_quantidade = int(input("Digite a nova quantidade: "))
                produto.atualizar_quantidade(nova_quantidade)
                print("Quantidade atualizada com sucesso.")
            elif escolha == '4':
                novo_preço = float(input("Digite o novo preço: "))
                produto.atualizar_preço(novo_preço)
                print("Preço atualizado com sucesso.")
            elif escolha == '5':
                novo_nome = input("Digite o novo nome: ")
                produto.alterar_nome(novo_nome)
            elif escolha == '6':
                novo_desc = input("Digite a nova descrição: ")
                produto.alterar_descrição(novo_desc)
            elif escolha == '7':
                produto.remover_produto()
            elif escolha == '8':
                break
            else:
                print("Opção inválida. Tente novamente.")
        

def exibir_categorias():
    categorias = Categoria.carregar_categorias()
    if categorias:
        for categoria in categorias:
            print(categoria)
    else:
        print("\nNenhuma categoria encontrada!")

def gerenciar_categoria():
    categorias = Categoria.carregar_categorias()
    if not categorias:
        print("\nNenhuma categoria encontrada para gerenciar!")
        return
    Categoria.exibir_categorias_existentes(categorias)

    try:
        num_categoria = int(input("Digite o número da categoria que deseja gerenciar: "))
        if num_categoria < 1 or num_categoria > len(categorias):
            print("Número de categoria inválido.")
            return
    except ValueError:
        print("Entrada inválida. Por favor, insira um número.")
        return
    
    nome_categoria = categorias[num_categoria - 1]['nome_categoria']
    categoria = Categoria.get_categoria_por_nome(nome_categoria)
    if categoria:
        while True:
            print("\nEscolha uma ação:")
            print("1. Modificar atributos adicionais")
            print("2. Remover categoria")
            print("3. Voltar ao menu principal")
            escolha = input("Escolha uma opção: ")

            if escolha == '1':
                print("Atributos atuais:", categoria.atributos_adicionais)
                novos_atributos = input("Digite os novos atributos (separados por vírgula), Enter caso nenhum atributo adicional: ").split(',')
                novos_atributos = [attr.strip() for attr in novos_atributos if attr.strip()]
                categoria.modificar_atributos_adicionais(novos_atributos)
                print("Atributos modificados com sucesso.")
            elif escolha == '2':
                categoria.remover_categoria()
                print("Categoria removida com sucesso.")
                break
            elif escolha == '3':
                break
            else:
                print("Opção inválida. Tente novamente.")
    else:
        return

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