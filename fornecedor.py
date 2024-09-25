import re

class Fornecedor:
    from conexão import get_collection
    COLLECTION_NAME = "Fornecedores"
    fornecedores_collection = get_collection(COLLECTION_NAME)

    def __init__(self, nome, cnpj, endereco, telefone, email, nome_representante, id_fornecedor=None):
        # Valida o CNPJ
        if not self.validar_cnpj(cnpj):
            raise ValueError(f"CNPJ {cnpj} inválido.")
        
        # Atributos do fornecedor
        self.nome = nome
        self.cnpj = self.remover_formatacao_cnpj(cnpj)  # Armazenar o CNPJ sem formatação
        self.endereco = endereco
        self.telefone = telefone
        self.email = email
        self.nome_representante = nome_representante
        self.id_fornecedor = id_fornecedor  # ID do fornecedor, gerado automaticamente

    def criar_fornecedor(self):
        # Verifica se o CNPJ já está registrado
        if Fornecedor.fornecedores_collection.find_one({"cnpj": self.cnpj}):
            raise ValueError(f"Fornecedor com CNPJ {self.cnpj} já está cadastrado.")
        
        novo_fornecedor = {
            'nome': self.nome,
            'cnpj': self.cnpj,
            'endereco': self.endereco,
            'telefone': self.telefone,
            'email': self.email,
            'nome_representante': self.nome_representante
        }

        # Insere o novo fornecedor no MongoDB
        resultado = Fornecedor.fornecedores_collection.insert_one(novo_fornecedor)
        self.id_fornecedor = resultado.inserted_id  # O ID é gerado automaticamente pelo MongoDB
        print(f'Fornecedor "{self.nome}" criado com sucesso.')

    @classmethod
    def exibir_fornecedores_existentes(cls):
        fornecedores = cls.fornecedores_collection.find()  # Obtém todos os fornecedores
        if fornecedores:
            print("\nFornecedores existentes:")
            for fornecedor in fornecedores:
                print("-" * 40)
                print(f"ID do Fornecedor: {fornecedor['_id']}")
                print(f"Nome: {fornecedor['nome']}")
                print(f"CNPJ: {cls.formatar_cnpj(fornecedor['cnpj'])}")
                print(f"Endereço: {fornecedor['endereco']}")
                print(f"Telefone: {fornecedor['telefone']}")
                print(f"E-mail: {fornecedor['email']}")
                print(f"Nome do Representante: {fornecedor['nome_representante']}")
                print("-" * 40)
        else:
            print("\nNenhum fornecedor cadastrado!")

    @classmethod
    def modificar_fornecedor(cls, id_recebido, novos_dados):
        # Atualiza os dados do fornecedor no MongoDB
        resultado = Fornecedor.fornecedores_collection.update_one(
            {"_id": id_recebido},
            {"$set": novos_dados}
        )

        if resultado.modified_count > 0:
            print(f"Fornecedor código {id_recebido} modificado com sucesso.")
        else:
            print(f"Nenhuma modificação feita para o fornecedor {id_recebido}.")

    @classmethod
    def remover_fornecedor(cls, id_recebido):
        # Remove o fornecedor do MongoDB
        resultado = Fornecedor.fornecedores_collection.delete_one({"_id": id_recebido})
        if resultado.deleted_count > 0:
            print(f'Fornecedor de cóidigo {id_recebido} removido com sucesso.')
        else:
            print(f"Fornecedor não encontrado.")

    @staticmethod
    def remover_formatacao_cnpj(cnpj):
        """Remove a formatação do CNPJ, deixando apenas os números."""
        return re.sub(r'\D', '', cnpj)  # Remove tudo que não for dígito

    @staticmethod
    def formatar_cnpj(cnpj):
        """Formata o CNPJ para o padrão xx.xxx.xxx/xxxx-xx."""
        cnpj = Fornecedor.remover_formatacao_cnpj(cnpj)
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"

    @staticmethod
    def validar_cnpj(cnpj):
        """Valida o CNPJ utilizando os cálculos de dígito verificador."""
        cnpj = Fornecedor.remover_formatacao_cnpj(cnpj)

        if len(cnpj) != 14:
            return False

        multiplicadores_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        multiplicadores_2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

        # Calcula o primeiro dígito verificador
        soma = sum(int(cnpj[i]) * multiplicadores_1[i] for i in range(12))
        digito_1 = 11 - (soma % 11)
        digito_1 = 0 if digito_1 >= 10 else digito_1

        # Calcula o segundo dígito verificador
        soma = sum(int(cnpj[i]) * multiplicadores_2[i] for i in range(13))
        digito_2 = 11 - (soma % 11)
        digito_2 = 0 if digito_2 >= 10 else digito_2

        # Verifica se os dígitos calculados conferem com os fornecidos
        return cnpj[-2:] == f'{digito_1}{digito_2}'

    @classmethod
    def buscar_fornecedor(cls, busca):
        """Busca um fornecedor por CNPJ ou nome."""
        fornecedor_atual = None

        # Remove espaços em branco e converte para minúsculas
        #busca = busca.strip().lower()

        try:
            # Tenta converter para inteiro (CNPJ sem formatação)
            busca_cnpj = int(busca)
            fornecedor_atual = cls.fornecedores_collection.find_one({"cnpj": busca_cnpj})
        except ValueError:
            # Se não for um inteiro, pode ser CNPJ com formatação ou nome
            busca_cnpj = cls.remover_formatacao_cnpj(busca)
            fornecedor_atual = cls.fornecedores_collection.find_one({"cnpj": busca_cnpj})

            # Se ainda não encontrou, busca por nome
            if not fornecedor_atual:
                fornecedor_atual = cls.fornecedores_collection.find_one({"nome": busca})

        if fornecedor_atual:
            return fornecedor_atual
        else:
            print("Fornecedor não encontrado.")
            return None
    
    @classmethod
    def buscar_todos_fornecedores(cls):
        """Busca todos os fornecedores no MongoDB."""
        return cls.fornecedores_collection.find()
    
    @classmethod
    def buscar_ultimo_fornecedor(cls):
        """Busca o último fornecedor adicionado."""
        return cls.fornecedores_collection.find_one(sort=[('_id', -1)])

    # def to_dict(self):
    #     """Converte o objeto Fornecedor para um dicionário."""
    #     return {
    #         'nome': self.nome,
    #         'cnpj': self.cnpj,
    #         'endereco': self.endereco,
    #         'telefone': self.telefone,
    #         'email': self.email,
    #         'nome_representante': self.nome_representante,
    #         'id_fornecedor': self.id_fornecedor
    #     }