from estoque import exibir_estoque, get_produto
from categoria import Categoria
from produto import Produto
from subclasses import criar_subclasse
from fornecedor import Fornecedor
from vendas import Registrar_Venda

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
    Categoria.exibir_categorias_existentes()
    categorias = list(Categoria.buscar_todas_categorias())
    if not categorias:
        print("Crie uma categoria para adicionar ao produto!")
        return

    nome_categoria = input("Digite o nome da categoria do produto que será criado: ")
    categoria = Categoria.get_categoria_por_nome(nome_categoria)

    if categoria:
        Subclasse = criar_subclasse(nome_categoria)
        #categoria = Categoria.get_categoria_por_nome(nome_categoria)
        atributos_adicionais = []
        nome_produto = input("Digite o nome do produto: ")
        preco = float(input("Digite o preço do produto: "))
        quantidade = int(input("Digite a quantidade do produto: "))
        descricao = input("Digite a descrição do produto: ")

        # Coleta os valores para os atributos adicionais
        if len(categoria.atributos_adicionais) > 0:
            print("\nPreencha os seguintes atributos adicionais:")
            for atributo in categoria.atributos_adicionais:
                valor = input(f"{atributo}: ")
                atributos_adicionais.append(valor)

        # Exibir fornecedores existentes
        Fornecedor.exibir_fornecedores_existentes()
        fornecedores = list(Fornecedor.buscar_todos_fornecedores())
        if not fornecedores:
            print("\nFornecedor não encontrado. Vamos cadastrar um novo fornecedor.")
            adicionar_fornecedor()
            fornecedor_selecionado = Fornecedor.buscar_ultimo_fornecedor()

        else:
            busca_fornecedor = input("Digite o nome ou cnpj do fornecedor para associar ao produto: ")
            fornecedor_selecionado = Fornecedor.buscar_fornecedor(busca_fornecedor)

            if fornecedor_selecionado is None:
                print("\nFornecedor não encontrado. Vamos cadastrar um novo fornecedor.")
                adicionar_fornecedor()
                fornecedor_selecionado = Fornecedor.buscar_ultimo_fornecedor()

        produto = Subclasse(nome_produto, quantidade, preco, descricao, fornecedor_selecionado["nome"], *atributos_adicionais)
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
    Categoria.exibir_categorias_existentes()

def gerenciar_categoria():

    Categoria.exibir_categorias_existentes()

    nome_categoria = input("Digite o número da categoria que deseja gerenciar: ")
     
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
    fornecedores = list(Fornecedor.buscar_todos_fornecedores())
    if not fornecedores:
        print("\nNenhum fornecedor cadastrado!")
        return

    Fornecedor.exibir_fornecedores_existentes()

    try:
        num_fornecedor = input("Digite nome ou cnpj do fornecedor que deseja modificar: ")
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
        print(f"\nDados do Fornecedor (ID: {fornecedor_atual['_id']}):")
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

        fornecedor_atual_id = fornecedor_atual['_id']
        print(fornecedor_atual_id)
        print(novos_dados)
        # Chama a função para modificar e salvar
        Fornecedor.modificar_fornecedor(fornecedor_atual_id, novos_dados)
        break

def remover_fornecedor():
    fornecedores = list(Fornecedor.buscar_todos_fornecedores())
    if not fornecedores:
        print("\nNenhum fornecedor cadastrado!")
        return

    Fornecedor.exibir_fornecedores_existentes()

    try:
        busca_fornecedor = input("Digite o nome ou cnpj do fornecedor que deseja remover: ")
        fornecedor_atual = Fornecedor.buscar_fornecedor(busca_fornecedor)

        if fornecedor_atual is None:
            print("Fornecedor não encontrado.")
            return

    except ValueError:
        print("Entrada inválida. Por favor, insira um número válido.")
        return

    confirmacao = input(f"Tem certeza que deseja remover o fornecedor '{fornecedor_atual['nome']}'? (s/n): ")
    id_fornecedor = fornecedor_atual['_id']
    if confirmacao.lower() == 's':
        Fornecedor.remover_fornecedor(id_fornecedor)
    else:
        print("Remoção cancelada.")

def registrar_venda():
     # Solicita o CPF do cliente
    cpf_cliente = input("Digite o CPF do cliente: ")
    
    # Inicializa as listas de produtos e quantidades
    lista_produtos = []
    lista_quantidades = []
    
    while True:
        # Solicita o código do produto
        codigo_produto = input("Digite o código do produto (ou 'finalizar' para encerrar, 'sair' para cancelar a venda): ")
        
        # Verifica se o usuário quer finalizar ou sair
        if codigo_produto.lower() == 'sair':
            print("Venda cancelada. Retornando ao menu principal.")
            return  # Sai do menu sem registrar a venda
        
        if codigo_produto.lower() == 'finalizar':
            if lista_produtos:
                break  # Sai do loop para finalizar a venda
            else:
                print("Nenhum produto foi adicionado. Venda não pode ser finalizada.")
                continue
        
        codigo_produto = int(codigo_produto)
        # Verifica se o produto existe no estoque
        produto = get_produto(codigo_produto)
        if not produto:
            print(f"Produto com código {codigo_produto} não encontrado.")
            continue

        if codigo_produto in lista_produtos:
            print("Produto já adicionado! Selecione outro produto!")
            continue
        
        # Solicita a quantidade
        try:
            quantidade = int(input(f"Digite a quantidade para o produto {produto.nome}: "))
            if quantidade <= 0:
                print("Quantidade inválida. Tente novamente.")
                continue
        except ValueError:
            print("Quantidade inválida. Digite um número inteiro.")
            continue
        
        # Adiciona o produto e a quantidade nas listas
        lista_produtos.append(codigo_produto)
        lista_quantidades.append(quantidade)
    
    # Pergunta se há alguma promoção após o cliente decidir finalizar a compra
    promocao = input("Há alguma promoção para aplicar? (S/N): ").strip().lower()
    if promocao == 's':
        codigo_promocao = input("Digite o código do produto em promoção: ")
        desconto = float(input("Digite o percentual de desconto (0 a 1, ex: 0.1 para 10%): "))
        promocao = (codigo_promocao, 1 - desconto)
    else:
        promocao = None

    # Chama a função de registro de venda
    Registrar_Venda(cpf_cliente, lista_produtos, lista_quantidades, promocao)


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
        print("7. Gerenciar Fornecedores")
        print("8. Registrar venda")
        print("9. Sair")

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
            gerenciar_fornecedores()
        elif escolha == '8':
            registrar_venda()
        elif escolha == '9':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")
