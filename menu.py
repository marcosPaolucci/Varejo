from estoque import exibir_estoque, get_produto, adicionar_produto_estoque
from categoria import Categoria
from produto import Produto
from subclasses import criar_subclasse
from fornecedor import Fornecedor

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
    # Carregar categorias
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

        # Coleta os valores para os atributos adicionais
        if len(categoria.atributos_adicionais) > 0:  # Acessando o atributo da categoria corretamente
            print("\nPreencha os seguintes atributos adicionais:")
            for atributo in categoria.atributos_adicionais:
                valor = input(f"{atributo}: ")
                atributos_adicionais.append(valor)

        # Carregar fornecedores existentes
        fornecedores = Fornecedor.carregar_fornecedores()
        Fornecedor.exibir_fornecedores_existentes()
        
        num_fornecedor = int(input("Digite o ID do fornecedor para associar ao produto: "))
        fornecedor_selecionado = next((f for f in fornecedores if f['id_fornecedor'] == num_fornecedor), None)

        # Se o fornecedor não for encontrado, chamar o cadastro de um novo fornecedor
        if fornecedor_selecionado is None:
            print("\nFornecedor não encontrado. Vamos cadastrar um novo fornecedor.")
            adicionar_fornecedor()  # Chama a função de cadastro de fornecedor
            fornecedores = Fornecedor.carregar_fornecedores()  # Atualiza a lista de fornecedores
            fornecedor_selecionado = fornecedores[-1]  # Seleciona o último fornecedor criado (recém-cadastrado)

        # Criar o objeto Fornecedor a partir do fornecedor selecionado
        fornecedor = Fornecedor(
            fornecedor_selecionado['nome'],
            fornecedor_selecionado['cnpj'],
            fornecedor_selecionado['endereco'],
            fornecedor_selecionado['telefone'],
            fornecedor_selecionado['email'],
            fornecedor_selecionado['nome_representante']
        )
        
        # Criar o produto com o fornecedor associado e os atributos adicionais
        produto = Subclasse(nome_produto, quantidade, preco, descricao, fornecedor, *atributos_adicionais)
        produto.adicionar_produto()  # Adiciona o produto ao estoque
        adicionar_produto_estoque(produto)  # Garante que o produto será salvo no estoque
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

def adicionar_fornecedor():
    nome = input("Digite o nome do fornecedor: ")

    # Loop para validar o CNPJ até que o usuário insira um válido
    while True:
        cnpj = input("Digite o CNPJ do fornecedor: ")
        if Fornecedor.validar_cnpj(cnpj):
            break  # Sai do loop se o CNPJ for válido
        else:
            print("CNPJ inválido. Por favor, tente novamente.")
    
    endereco = input("Digite o endereço do fornecedor: ")
    telefone = input("Digite o telefone do fornecedor: ")
    email = input("Digite o e-mail do fornecedor: ")
    nome_representante = input("Digite o nome do representante: ")

    # Criar o fornecedor com os atributos corretos
    fornecedor = Fornecedor(
        nome=nome,
        cnpj=cnpj,
        endereco=endereco,
        telefone=telefone,
        email=email,
        nome_representante=nome_representante
    )

    fornecedor.criar_fornecedor()





def exibir_fornecedores():
    Fornecedor.exibir_fornecedores_existentes()

def modificar_fornecedor():
    fornecedores = Fornecedor.carregar_fornecedores()
    if not fornecedores:
        print("\nNenhum fornecedor cadastrado!")
        return

    Fornecedor.exibir_fornecedores_existentes()

    try:
        num_fornecedor = int(input("Digite o número do fornecedor que deseja modificar: "))
        fornecedor_atual = Fornecedor.buscar_fornecedor(num_fornecedor)

        if fornecedor_atual is None:
            print("Fornecedor não encontrado.")
            return

    except ValueError:
        print("Entrada inválida. Por favor, insira um número válido.")
        return

    novos_dados = {}

    while True:
        # Exibir os dados atuais do fornecedor
        print(f"\nDados do Fornecedor (ID: {fornecedor_atual['id_fornecedor']}):")
        print(f"1. Nome: {fornecedor_atual['nome']}")
        print(f"2. CNPJ: {fornecedor_atual['cnpj']}")
        print(f"3. Endereço: {fornecedor_atual['endereco']}")
        print(f"4. Telefone: {fornecedor_atual['telefone']}")
        print(f"5. E-mail: {fornecedor_atual['email']}")
        print(f"6. Nome do Representante: {fornecedor_atual['nome_representante']}")
        print("7. Voltar")

        # Escolher qual campo modificar
        escolha = input("Digite o número do campo que deseja modificar ou 7 para voltar: ")

        if escolha == '1':
            novos_dados['nome'] = input(f"Novo nome (atual: {fornecedor_atual['nome']}): ") or fornecedor_atual['nome']
        elif escolha == '2':
            novos_dados['cnpj'] = input(f"Novo CNPJ (atual: {fornecedor_atual['cnpj']}): ") or fornecedor_atual['cnpj']
        elif escolha == '3':
            novos_dados['endereco'] = input(f"Novo endereço (atual: {fornecedor_atual['endereco']}): ") or fornecedor_atual['endereco']
        elif escolha == '4':
            novos_dados['telefone'] = input(f"Novo telefone (atual: {fornecedor_atual['telefone']}): ") or fornecedor_atual['telefone']
        elif escolha == '5':
            novos_dados['email'] = input(f"Novo e-mail (atual: {fornecedor_atual['email']}): ") or fornecedor_atual['email']
        elif escolha == '6':
            novos_dados['nome_representante'] = input(f"Novo nome do representante (atual: {fornecedor_atual['nome_representante']}): ") or fornecedor_atual['nome_representante']
        elif escolha == '7':
            print("Voltando ao menu anterior.")
            break
        else:
            print("Opção inválida, tente novamente.")
            continue

        # Criar uma instância de Fornecedor com os dados atuais
        fornecedor = Fornecedor(
            fornecedor_atual['nome'],
            fornecedor_atual['cnpj'],
            fornecedor_atual['endereco'],
            fornecedor_atual['telefone'],
            fornecedor_atual['email'],
            fornecedor_atual['nome_representante'],
            id_fornecedor=fornecedor_atual['id_fornecedor']
        )

        # Chama a função para modificar e salvar
        fornecedor.modificar_fornecedor(novos_dados)
        break



def remover_fornecedor():
    fornecedores = Fornecedor.carregar_fornecedores()
    if not fornecedores:
        print("\nNenhum fornecedor cadastrado!")
        return

    Fornecedor.exibir_fornecedores_existentes()

    try:
        num_fornecedor = int(input("Digite o número do fornecedor que deseja remover: "))
        fornecedor_atual = Fornecedor.buscar_fornecedor(num_fornecedor)

        if fornecedor_atual is None:
            print("Fornecedor não encontrado.")
            return

    except ValueError:
        print("Entrada inválida. Por favor, insira um número válido.")
        return

    confirmacao = input(f"Tem certeza que deseja remover o fornecedor '{fornecedor_atual['nome']}'? (s/n): ")
    
    if confirmacao.lower() == 's':
        fornecedor_obj = Fornecedor(
            fornecedor_atual['nome'],
            fornecedor_atual['cnpj'],
            fornecedor_atual['endereco'],
            fornecedor_atual['telefone'],
            fornecedor_atual['email'],
            fornecedor_atual['nome_representante'],
            id_fornecedor=fornecedor_atual['id_fornecedor']
        )
        fornecedor_obj.remover_fornecedor()
    else:
        print("Remoção cancelada.")


def gerenciar_fornecedores():
    while True:
        print("\nGerenciamento de Fornecedores:")
        print("1. Adicionar Fornecedor")
        print("2. Modificar Fornecedor")
        print("3. Remover Fornecedor")
        print("4. Exibir Fornecedores")
        print("5. Voltar ao Menu Principal")
        
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            adicionar_fornecedor()
        elif escolha == '2':
            modificar_fornecedor()
        elif escolha == '3':
            remover_fornecedor()
        elif escolha == '4':
            exibir_fornecedores()
        elif escolha == '5':
            break
        else:
            print("Opção inválida. Tente novamente.")

# Menu Principal

def mostrar_menu():
    while True:
        print("\nMenu Principal:")
        print("1. Adicionar Categoria")
        print("2. Criar Produto")
        print("3. Gerenciar Produto")
        print("4. Exibir Todos os Produtos")
        print("5. Exibir Todas as Categorias")
        print("6. Gerenciar Categoria")
        print("7. Gerenciar Fornecedores")  # Novo gerenciamento de fornecedores
        print("8. Sair")
        
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
            gerenciar_fornecedores()  # Chama a função de gerenciamento de fornecedores
        elif escolha == '8':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

