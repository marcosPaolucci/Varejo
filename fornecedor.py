import json
import os
import re

class Fornecedor:
    arquivo_json = 'fornecedores.json'

    def __init__(self, nome, cnpj, endereco, telefone, email, nome_representante, id_fornecedor=None):
        # Valida o CNPJ
        if not self.validar_cnpj(cnpj):
            raise ValueError(f"CNPJ {cnpj} inválido.")
        
        # Atributos específicos do fornecedor
        self.nome = nome
        self.cnpj = cnpj
        self.endereco = endereco
        self.telefone = telefone
        self.email = email
        self.nome_representante = nome_representante
        self.id_fornecedor = id_fornecedor  # ID do fornecedor

    @classmethod
    def gerar_novo_id(cls):
        fornecedores = cls.carregar_fornecedores()

        if fornecedores:
            # Retorna o maior ID e soma 1 para gerar o próximo ID
            maior_id = max(f['id_fornecedor'] for f in fornecedores)
            return maior_id + 1
        else:
            return 1  # Se não houver fornecedores, o primeiro ID será 1

    def criar_fornecedor(self):
        fornecedores = self.carregar_fornecedores()

        if self.id_fornecedor is None:
            self.id_fornecedor = len(fornecedores) + 1

        novo_fornecedor = {
            'id_fornecedor': self.id_fornecedor,
            'nome': self.nome,
            'cnpj': self.cnpj,
            'endereco': self.endereco,
            'telefone': self.telefone,
            'email': self.email,
            'nome_representante': self.nome_representante
        }

        fornecedores.append(novo_fornecedor)
        self.salvar_fornecedores(fornecedores)
        print(f'Fornecedor "{self.nome}" criado com sucesso.')


    @classmethod
    def carregar_fornecedores(cls):
        if os.path.exists(cls.arquivo_json):
            with open(cls.arquivo_json, 'r', encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []  # Retorna uma lista vazia se o arquivo estiver vazio ou corrompido
        else:
            return []


    @classmethod
    def exibir_fornecedores_existentes(cls):
        fornecedores = cls.carregar_fornecedores()
        if fornecedores:
            print("\nFornecedores existentes:")
            for fornecedor in fornecedores:
                print("-" * 40)
                print(f"ID do Fornecedor: {fornecedor['id_fornecedor']}")
                print(f"Nome: {fornecedor['nome']}")
                print(f"CNPJ: {fornecedor['cnpj']}")
                print(f"Endereço: {fornecedor['endereco']}")
                print(f"Telefone: {fornecedor['telefone']}")
                print(f"E-mail: {fornecedor['email']}")
                print(f"Nome do Representante: {fornecedor['nome_representante']}")
                print("-" * 40)
        else:
            print("\nNenhum fornecedor cadastrado!")



    def modificar_fornecedor(self, novos_dados):
        fornecedores = self.carregar_fornecedores()

        for fornecedor in fornecedores:
            if fornecedor['id_fornecedor'] == self.id_fornecedor:
                fornecedor.update(novos_dados)
                break

        self.salvar_fornecedores(fornecedores)
        print(f"Fornecedor {self.nome} modificado com sucesso.")


    def remover_fornecedor(self):
        fornecedores = self.carregar_fornecedores()
        fornecedores = [f for f in fornecedores if f['id_fornecedor'] != self.id_fornecedor]
        self.salvar_fornecedores(fornecedores)
        print(f'Fornecedor "{self.nome}" removido com sucesso.')


    @staticmethod
    def remover_formatacao_cnpj(cnpj):
        return re.sub(r'\D', '', cnpj)  # Remove tudo que não for dígito (0-9)

    @staticmethod
    def validar_cnpj(cnpj):
        cnpj = Fornecedor.remover_formatacao_cnpj(cnpj)
        
        if len(cnpj) != 14:
            return False

        multiplicadores_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        multiplicadores_2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

        soma = sum(int(cnpj[i]) * multiplicadores_1[i] for i in range(12))
        digito_1 = 11 - (soma % 11)
        if digito_1 >= 10:
            digito_1 = 0

        soma = sum(int(cnpj[i]) * multiplicadores_2[i] for i in range(13))
        digito_2 = 11 - (soma % 11)
        if digito_2 >= 10:
            digito_2 = 0

        return cnpj[-2:] == f'{digito_1}{digito_2}'

    @classmethod
    def buscar_fornecedor(cls, busca):
        fornecedores = cls.carregar_fornecedores()

        fornecedor_atual = None

        # Se 'busca' for um número inteiro, trata como ID de fornecedor
        if isinstance(busca, int):
            fornecedor_atual = next((f for f in fornecedores if f['id_fornecedor'] == busca), None)
        else:
            # Se 'busca' for uma string, verifica se é um número ou um CNPJ sem formatação
            if busca.isdigit():
                # Tenta encontrar o fornecedor pelo CNPJ
                busca_cnpj = cls.remover_formatacao_cnpj(busca)
                fornecedor_atual = next((f for f in fornecedores if cls.remover_formatacao_cnpj(f['cnpj']) == busca_cnpj), None)

            # Se o formato é de CNPJ (contém pontos, barras ou traços), tenta buscar por CNPJ
            elif any(char in busca for char in ['.', '/', '-']):
                busca_cnpj = cls.remover_formatacao_cnpj(busca)
                fornecedor_atual = next((f for f in fornecedores if cls.remover_formatacao_cnpj(f['cnpj']) == busca_cnpj), None)

            # Caso contrário, tenta buscar por nome
            else:
                fornecedor_atual = next((f for f in fornecedores if f['nome'].lower() == busca.lower()), None)

        if fornecedor_atual is None:
            print("Fornecedor não encontrado.")
        return fornecedor_atual


    @classmethod
    def salvar_fornecedores(cls, fornecedores):
        with open(cls.arquivo_json, 'w', encoding="utf-8") as f:
            json.dump(fornecedores, f, indent=4)

    def to_dict(self):
        """Converte o objeto Fornecedor para um dicionário."""
        return {
            'nome': self.nome,
            'cnpj': self.cnpj,
            'endereco': self.endereco,
            'telefone': self.telefone,
            'email': self.email,
            'nome_representante': self.nome_representante,
            'id_fornecedor': self.id_fornecedor
        }