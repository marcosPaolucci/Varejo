from estoque import exibir_estoque, get_produto
from categoria import Categoria
from produto import Produto
from subclasses import criar_subclasse
from fornecedor import Fornecedor
from vendas import Registrar_Venda
from relatorios import Relatorios
from datetime import datetime
from typing import Optional


class Menu:
    def __init__(self):
        # Instancia a classe de Relatórios
        self.relatorios = Relatorios()

    def adicionar_categoria(self):
        try:
            nome = input("Digite o nome da categoria: ").strip()
            if not nome:
                print("Nome da categoria não pode ser vazio.")
                return

            atributos_input = input("Digite os atributos adicionais da categoria (separados por vírgula), Enter caso nenhum atributo adicional: ").strip()
            atributos = [attr.strip() for attr in atributos_input.split(',') if attr.strip()]

            # Verifica se há atributos
            if atributos:
                categoria = Categoria(nome, *atributos)
            else:
                categoria = Categoria(nome)
            categoria.criar_categoria()
            print(f"Categoria '{nome}' adicionada com sucesso.")
        except Exception as e:
            print(f"Ocorreu um erro ao adicionar a categoria: {e}")

    def criar_produto(self):
        try:
            Categoria.exibir_categorias_existentes()
            categorias = list(Categoria.buscar_todas_categorias())
            if not categorias:
                print("Crie uma categoria para adicionar ao produto!")
                return

            nome_categoria = input("Digite o nome da categoria do produto que será criado: ").strip()
            categoria = Categoria.get_categoria_por_nome(nome_categoria)

            if categoria:
                Subclasse = criar_subclasse(nome_categoria)
                if Subclasse is None:
                    print("Não foi possível criar a subclasse para a categoria selecionada.")
                    return

                atributos_adicionais = []
                nome_produto = input("Digite o nome do produto: ").strip()
                if not nome_produto:
                    print("Nome do produto não pode ser vazio.")
                    return

                # Valida a entrada do preço
                preco = self._input_float("Digite o preço do produto: ", positivo=True)

                # Valida a entrada da quantidade
                quantidade = self._input_int("Digite a quantidade do produto: ", positivo=True)

                descricao = input("Digite a descrição do produto: ").strip()
                if not descricao:
                    print("Descrição do produto não pode ser vazia.")
                    return

                # Coleta os valores para os atributos adicionais
                if categoria.atributos_adicionais:
                    print("\nPreencha os seguintes atributos adicionais:")
                    for atributo in categoria.atributos_adicionais:
                        valor = input(f"{atributo}: ").strip()
                        atributos_adicionais.append(valor)

                # Exibir fornecedores existentes
                Fornecedor.exibir_fornecedores_existentes()
                fornecedores = list(Fornecedor.buscar_todos_fornecedores())
                if not fornecedores:
                    print("\nFornecedor não encontrado. Vamos cadastrar um novo fornecedor.")
                    self.adicionar_fornecedor()
                    fornecedor_selecionado = Fornecedor.buscar_ultimo_fornecedor()
                else:
                    busca_fornecedor = input("Digite o nome ou CNPJ do fornecedor para associar ao produto: ").strip()
                    fornecedor_selecionado = Fornecedor.buscar_fornecedor(busca_fornecedor)

                    if fornecedor_selecionado is None:
                        print("\nFornecedor não encontrado. Vamos cadastrar um novo fornecedor.")
                        self.adicionar_fornecedor()
                        fornecedor_selecionado = Fornecedor.buscar_ultimo_fornecedor()

                if fornecedor_selecionado is None:
                    print("Falha ao associar fornecedor. Produto não foi adicionado.")
                    return

                produto = Subclasse(
                    nome_produto,
                    quantidade,
                    preco,
                    descricao,
                    fornecedor_selecionado["nome"],
                    *atributos_adicionais
                )
                produto.adicionar_produto()
                print(f"Produto '{nome_produto}' adicionado com sucesso.")
            else:
                print("Categoria não encontrada.")
        except Exception as e:
            print(f"Ocorreu um erro ao criar o produto: {e}")

    def gerenciar_produto(self):
        try:
            codigo_input = input("Digite o código do produto: ").strip()
            if not codigo_input.isdigit():
                print("Código do produto inválido. Por favor, insira um número válido.")
                return
            codigo = int(codigo_input)

            produto = get_produto(codigo)
            if produto:
                while True:
                    print("\n=== Gerenciamento de Produto ===")
                    print("1. Incrementar quantidade")
                    print("2. Decrementar quantidade")
                    print("3. Atualizar quantidade")
                    print("4. Atualizar preço")
                    print("5. Alterar nome do produto")
                    print("6. Alterar descrição do produto")
                    print("7. Remover produto")
                    print("8. Voltar ao menu principal")
                    escolha = input("Escolha uma opção: ").strip()

                    if escolha == '1':
                        try:
                            quantidade = self._input_int("Digite a quantidade a ser adicionada: ", positivo=True)
                            produto.adicionar_quantidade(quantidade)
                            print("Quantidade incrementada com sucesso.")
                        except Exception as e:
                            print(f"Erro ao incrementar quantidade: {e}")
                    elif escolha == '2':
                        try:
                            quantidade = self._input_int("Digite a quantidade a ser removida: ", positivo=True)
                            produto.remover_quantidade(quantidade)
                            print("Quantidade decrementada com sucesso.")
                        except Exception as e:
                            print(f"Erro ao decrementar quantidade: {e}")
                    elif escolha == '3':
                        try:
                            nova_quantidade = self._input_int("Digite a nova quantidade: ", positivo=True)
                            produto.atualizar_quantidade(nova_quantidade)
                            print("Quantidade atualizada com sucesso.")
                        except Exception as e:
                            print(f"Erro ao atualizar quantidade: {e}")
                    elif escolha == '4':
                        try:
                            novo_preco = self._input_float("Digite o novo preço: ", positivo=True)
                            produto.atualizar_preco(novo_preco)
                            print("Preço atualizado com sucesso.")
                        except Exception as e:
                            print(f"Erro ao atualizar preço: {e}")
                    elif escolha == '5':
                        try:
                            novo_nome = input("Digite o novo nome: ").strip()
                            if not novo_nome:
                                print("Nome do produto não pode ser vazio.")
                                continue
                            produto.alterar_nome(novo_nome)
                            print("Nome do produto atualizado com sucesso.")
                        except Exception as e:
                            print(f"Erro ao alterar nome: {e}")
                    elif escolha == '6':
                        try:
                            nova_descricao = input("Digite a nova descrição: ").strip()
                            if not nova_descricao:
                                print("Descrição do produto não pode ser vazia.")
                                continue
                            produto.alterar_descricao(nova_descricao)
                            print("Descrição do produto atualizada com sucesso.")
                        except Exception as e:
                            print(f"Erro ao alterar descrição: {e}")
                    elif escolha == '7':
                        try:
                            confirmacao = input(f"Tem certeza que deseja remover o produto '{produto.nome}'? (s/n): ").strip().lower()
                            if confirmacao == 's':
                                produto.remover_produto()
                                print("Produto removido com sucesso.")
                                break
                            else:
                                print("Remoção cancelada.")
                        except Exception as e:
                            print(f"Erro ao remover produto: {e}")
                    elif escolha == '8':
                        break
                    else:
                        print("Opção inválida. Tente novamente.")
            else:
                print("Produto não encontrado.")
        except Exception as e:
            print(f"Ocorreu um erro ao gerenciar o produto: {e}")

    def exibir_categorias(self):
        try:
            Categoria.exibir_categorias_existentes()
        except Exception as e:
            print(f"Ocorreu um erro ao exibir categorias: {e}")

    def gerenciar_categoria(self):
        try:
            Categoria.exibir_categorias_existentes()

            nome_categoria = input("Digite o nome da categoria que deseja gerenciar: ").strip()
            if not nome_categoria:
                print("Nome da categoria não pode ser vazio.")
                return

            categoria = Categoria.get_categoria_por_nome(nome_categoria)
            if categoria:
                while True:
                    print("\n=== Gerenciamento de Categoria ===")
                    print("1. Modificar atributos adicionais")
                    print("2. Remover categoria")
                    print("3. Voltar ao menu principal")
                    escolha = input("Escolha uma opção: ").strip()

                    if escolha == '1':
                        try:
                            print("Atributos atuais:", categoria.atributos_adicionais)
                            novos_atributos_input = input("Digite os novos atributos (separados por vírgula), Enter caso nenhum atributo adicional: ").strip()
                            novos_atributos = [attr.strip() for attr in novos_atributos_input.split(',') if attr.strip()]
                            categoria.modificar_atributos_adicionais(novos_atributos)
                            print("Atributos modificados com sucesso.")
                        except Exception as e:
                            print(f"Erro ao modificar atributos: {e}")
                    elif escolha == '2':
                        try:
                            confirmacao = input(f"Tem certeza que deseja remover a categoria '{categoria.nome_categoria}'? (s/n): ").strip().lower()
                            if confirmacao == 's':
                                categoria.remover_categoria()
                                print("Categoria removida com sucesso.")
                                break
                            else:
                                print("Remoção cancelada.")
                        except Exception as e:
                            print(f"Erro ao remover categoria: {e}")
                    elif escolha == '3':
                        break
                    else:
                        print("Opção inválida. Tente novamente.")
            else:
                print("Categoria não encontrada.")
        except Exception as e:
            print(f"Ocorreu um erro ao gerenciar a categoria: {e}")

    def adicionar_fornecedor(self):
        try:
            nome = input("Digite o nome do fornecedor: ").strip()
            if not nome:
                print("Nome do fornecedor não pode ser vazio.")
                return

            # Loop para validar o CNPJ até que o usuário insira um válido
            while True:
                cnpj = input("Digite o CNPJ do fornecedor: ").strip()
                if Fornecedor.validar_cnpj(cnpj):
                    break  # Sai do loop se o CNPJ for válido
                else:
                    print("CNPJ inválido. Por favor, tente novamente.")

            endereco = input("Digite o endereço do fornecedor: ").strip()
            if not endereco:
                print("Endereço do fornecedor não pode ser vazio.")
                return

            telefone = input("Digite o telefone do fornecedor: ").strip()
            if not telefone:
                print("Telefone do fornecedor não pode ser vazio.")
                return

            email = input("Digite o e-mail do fornecedor: ").strip()
            if not email:
                print("E-mail do fornecedor não pode ser vazio.")
                return

            nome_representante = input("Digite o nome do representante: ").strip()
            if not nome_representante:
                print("Nome do representante não pode ser vazio.")
                return

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
            print(f"Fornecedor '{nome}' adicionado com sucesso.")
        except Exception as e:
            print(f"Ocorreu um erro ao adicionar o fornecedor: {e}")

    def exibir_fornecedores(self):
        try:
            Fornecedor.exibir_fornecedores_existentes()
        except Exception as e:
            print(f"Ocorreu um erro ao exibir fornecedores: {e}")

    def modificar_fornecedor(self):
        try:
            fornecedores = list(Fornecedor.buscar_todos_fornecedores())
            if not fornecedores:
                print("\nNenhum fornecedor cadastrado!")
                return

            Fornecedor.exibir_fornecedores_existentes()

            num_fornecedor = input("Digite o nome ou CNPJ do fornecedor que deseja modificar: ").strip()
            if not num_fornecedor:
                print("Entrada vazia. Retornando ao menu anterior.")
                return

            fornecedor_atual = Fornecedor.buscar_fornecedor(num_fornecedor)

            if fornecedor_atual is None:
                print("Fornecedor não encontrado.")
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
                escolha = input("Digite o número do campo que deseja modificar ou 7 para voltar: ").strip()

                if escolha == '1':
                    novo_nome = input(f"Novo nome (atual: {fornecedor_atual['nome']}): ").strip()
                    if novo_nome:
                        novos_dados['nome'] = novo_nome
                elif escolha == '2':
                    novo_cnpj = input(f"Novo CNPJ (atual: {fornecedor_atual['cnpj']}): ").strip()
                    if novo_cnpj:
                        if Fornecedor.validar_cnpj(novo_cnpj):
                            novos_dados['cnpj'] = novo_cnpj
                        else:
                            print("CNPJ inválido. Não foi atualizado.")
                elif escolha == '3':
                    novo_endereco = input(f"Novo endereço (atual: {fornecedor_atual['endereco']}): ").strip()
                    if novo_endereco:
                        novos_dados['endereco'] = novo_endereco
                elif escolha == '4':
                    novo_telefone = input(f"Novo telefone (atual: {fornecedor_atual['telefone']}): ").strip()
                    if novo_telefone:
                        novos_dados['telefone'] = novo_telefone
                elif escolha == '5':
                    novo_email = input(f"Novo e-mail (atual: {fornecedor_atual['email']}): ").strip()
                    if novo_email:
                        novos_dados['email'] = novo_email
                elif escolha == '6':
                    novo_nome_representante = input(f"Novo nome do representante (atual: {fornecedor_atual['nome_representante']}): ").strip()
                    if novo_nome_representante:
                        novos_dados['nome_representante'] = novo_nome_representante
                elif escolha == '7':
                    print("Voltando ao menu anterior.")
                    break
                else:
                    print("Opção inválida, tente novamente.")
                    continue

                if novos_dados:
                    fornecedor_atual_id = fornecedor_atual['_id']
                    # Chama a função para modificar e salvar
                    Fornecedor.modificar_fornecedor(fornecedor_atual_id, novos_dados)
                    print("Dados do fornecedor atualizados com sucesso.")
                else:
                    print("Nenhuma alteração realizada.")
                break  # Sai após uma modificação
        except Exception as e:
            print(f"Ocorreu um erro ao modificar o fornecedor: {e}")

    def remover_fornecedor(self):
        try:
            fornecedores = list(Fornecedor.buscar_todos_fornecedores())
            if not fornecedores:
                print("\nNenhum fornecedor cadastrado!")
                return

            Fornecedor.exibir_fornecedores_existentes()

            busca_fornecedor = input("Digite o nome ou CNPJ do fornecedor que deseja remover: ").strip()
            if not busca_fornecedor:
                print("Entrada vazia. Retornando ao menu anterior.")
                return

            fornecedor_atual = Fornecedor.buscar_fornecedor(busca_fornecedor)

            if fornecedor_atual is None:
                print("Fornecedor não encontrado.")
                return

            confirmacao = input(f"Tem certeza que deseja remover o fornecedor '{fornecedor_atual['nome']}'? (s/n): ").strip().lower()
            if confirmacao == 's':
                id_fornecedor = fornecedor_atual['_id']
                Fornecedor.remover_fornecedor(id_fornecedor)
                print("Fornecedor removido com sucesso.")
            else:
                print("Remoção cancelada.")
        except Exception as e:
            print(f"Ocorreu um erro ao remover o fornecedor: {e}")

    def registrar_venda(self):
        try:
            cpf_cliente = input("Digite o CPF do cliente: ").strip()
            if not cpf_cliente:
                print("CPF do cliente não pode ser vazio.")
                return

            lista_produtos = []
            lista_quantidades = []

            while True:
                codigo_produto_input = input("Digite o código do produto (ou 'finalizar' para encerrar, 'sair' para cancelar a venda): ").strip().lower()

                if codigo_produto_input == 'sair':
                    print("Venda cancelada. Retornando ao menu principal.")
                    return

                if codigo_produto_input == 'finalizar':
                    if lista_produtos:
                        break
                    else:
                        print("Nenhum produto foi adicionado. Venda não pode ser finalizada.")
                        continue

                if not codigo_produto_input.isdigit():
                    print("Erro: O código do produto deve ser um número inteiro.")
                    continue

                codigo_produto = int(codigo_produto_input)
                produto = get_produto(codigo_produto)
                if not produto:
                    print(f"Produto com código {codigo_produto} não encontrado.")
                    continue

                if codigo_produto in lista_produtos:
                    print("Produto já adicionado! Selecione outro produto!")
                    continue

                quantidade = self._input_int(f"Digite a quantidade para o produto '{produto.nome}': ", positivo=True)
                if quantidade is None:
                    print("Quantidade inválida. Produto não adicionado.")
                    continue

                lista_produtos.append(codigo_produto)
                lista_quantidades.append(quantidade)

            promocao = None
            promocao_input = input("Há alguma promoção para aplicar? (s/n): ").strip().lower()
            if promocao_input == 's':
                try:
                    codigo_promocao = self._input_int("Digite o código do produto em promoção: ", positivo=True)
                    if codigo_promocao is None:
                        print("Código de promoção inválido. Promoção não será aplicada.")
                    else:
                        desconto = self._input_float("Digite o percentual de desconto (0 a 1, ex: 0.1 para 10%): ", minimo=0, maximo=1)
                        if desconto is None:
                            print("Desconto inválido. Promoção não será aplicada.")
                        else:
                            promocao = (codigo_promocao, 1 - desconto)
                except Exception as e:
                    print("Erro ao aplicar promoção. Certifique-se de digitar valores numéricos corretos.")
                    promocao = None

            Registrar_Venda(cpf_cliente, lista_produtos, lista_quantidades, promocao)
        except Exception as e:
            print(f"Ocorreu um erro ao registrar a venda: {e}")

    def visualizar_relatorios(self):
        while True:
            try:
                print("\n=== Visualização de Relatórios ===")
                print("1. Relatório de Vendas")
                print("2. Relatório de Estoque")
                print("3. Histórico de Movimentações")
                print("4. Voltar ao Menu Principal")
                escolha = input("Escolha uma opção: ").strip()

                if escolha == '1':
                    data_inicio_str = input("Digite a data de início (formato AAAA-MM-DD) ou Enter para todas as vendas: ").strip()
                    data_fim_str = input("Digite a data de fim (formato AAAA-MM-DD) ou Enter para todas as vendas: ").strip()

                    data_inicio = None
                    data_fim = None

                    if data_inicio_str:
                        try:
                            data_inicio = datetime.strptime(data_inicio_str, "%Y-%m-%d")
                        except ValueError:
                            print("Erro: Data de início inválida.")
                            data_inicio = None

                    if data_fim_str:
                        try:
                            data_fim = datetime.strptime(data_fim_str, "%Y-%m-%d")
                        except ValueError:
                            print("Erro: Data de fim inválida.")
                            data_fim = None

                    self.relatorios.relatorio_vendas(data_inicio, data_fim)

                elif escolha == '2':
                    self.relatorios.relatorio_estoque()

                elif escolha == '3':
                    codigo_produto_input = input("Digite o código do produto para ver o histórico ou Enter para todos: ").strip()
                    codigo_produto = None
                    if codigo_produto_input:
                        if not codigo_produto_input.isdigit():
                            print("Erro: O código do produto deve ser um número inteiro.")
                        else:
                            codigo_produto = int(codigo_produto_input)
                    self.relatorios.historico_movimentacoes(codigo_produto)

                elif escolha == '4':
                    break
                else:
                    print("Opção inválida. Tente novamente.")
            except Exception as e:
                print(f"Ocorreu um erro ao visualizar relatórios: {e}")

    def gerenciar_fornecedores(self):
        while True:
            try:
                print("\n=== Gerenciamento de Fornecedores ===")
                print("1. Adicionar Fornecedor")
                print("2. Modificar Fornecedor")
                print("3. Remover Fornecedor")
                print("4. Exibir Fornecedores")
                print("5. Voltar ao Menu Principal")
                escolha = input("Escolha uma opção: ").strip()

                if escolha == '1':
                    self.adicionar_fornecedor()
                elif escolha == '2':
                    self.modificar_fornecedor()
                elif escolha == '3':
                    self.remover_fornecedor()
                elif escolha == '4':
                    self.exibir_fornecedores()
                elif escolha == '5':
                    break
                else:
                    print("Opção inválida. Tente novamente.")
            except Exception as e:
                print(f"Ocorreu um erro ao gerenciar fornecedores: {e}")

    def mostrar_menu(self):
        while True:
            try:
                print("\n=== Menu Principal ===")
                print("1. Adicionar Categoria")
                print("2. Criar Produto")
                print("3. Gerenciar Produto")
                print("4. Exibir Todos os Produtos")
                print("5. Exibir Todas as Categorias")
                print("6. Gerenciar Categoria")
                print("7. Gerenciar Fornecedores")
                print("8. Registrar venda")
                print("9. Visualizar Relatórios")
                print("10. Sair")
                escolha = input("Escolha uma opção: ").strip()

                if escolha == '1':
                    self.adicionar_categoria()
                elif escolha == '2':
                    self.criar_produto()
                elif escolha == '3':
                    self.gerenciar_produto()
                elif escolha == '4':
                    exibir_estoque()
                elif escolha == '5':
                    self.exibir_categorias()
                elif escolha == '6':
                    self.gerenciar_categoria()
                elif escolha == '7':
                    self.gerenciar_fornecedores()
                elif escolha == '8':
                    self.registrar_venda()
                elif escolha == '9':
                    self.visualizar_relatorios()
                elif escolha == '10':
                    print("Saindo...")
                    break
                else:
                    print("Opção inválida. Tente novamente.")
            except Exception as e:
                print(f"Ocorreu um erro no menu principal: {e}")

    def _input_int(self, prompt: str, positivo: bool = False) -> Optional[int]:
        """
        Função auxiliar para obter uma entrada inteira do usuário com validação.

        Args:
            prompt (str): Mensagem a ser exibida para o usuário.
            positivo (bool, optional): Se True, somente aceita valores positivos. Defaults to False.

        Returns:
            Optional[int]: O valor inteiro inserido pelo usuário ou None se inválido.
        """
        while True:
            entrada = input(prompt).strip()
            try:
                valor = int(entrada)
                if positivo and valor < 0:
                    print("O valor deve ser positivo.")
                    continue
                return valor
            except ValueError:
                print("Erro: Por favor, insira um número inteiro válido.")

    def _input_float(self, prompt: str, positivo: bool = False, minimo: float = None, maximo: float = None) -> Optional[float]:
        """
        Função auxiliar para obter uma entrada float do usuário com validação.

        Args:
            prompt (str): Mensagem a ser exibida para o usuário.
            positivo (bool, optional): Se True, somente aceita valores positivos. Defaults to False.
            minimo (float, optional): Valor mínimo permitido. Defaults to None.
            maximo (float, optional): Valor máximo permitido. Defaults to None.

        Returns:
            Optional[float]: O valor float inserido pelo usuário ou None se inválido.
        """
        while True:
            entrada = input(prompt).strip()
            try:
                valor = float(entrada)
                if positivo and valor < 0:
                    print("O valor deve ser positivo.")
                    continue
                if minimo is not None and valor < minimo:
                    print(f"O valor deve ser no mínimo {minimo}.")
                    continue
                if maximo is not None and valor > maximo:
                    print(f"O valor deve ser no máximo {maximo}.")
                    continue
                return valor
            except ValueError:
                print("Erro: Por favor, insira um número válido.")

# Inicia o Menu Principal
if __name__ == "__main__":
    menu = Menu()
    menu.mostrar_menu()
