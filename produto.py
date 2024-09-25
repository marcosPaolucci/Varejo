from estoque import adicionar_produto_estoque, adicionar_quantidade_estoque, remover_quantidade_estoque, alterar_quantidade_estoque, remover_produto, atualizar_preco_estoque, alterar_nome_estoque, alterar_descrição_estoque
from fornecedor import Fornecedor

class Produto:
    def __init__(self, nome, quantidade, preco, descricao, fornecedor: Fornecedor):
        self.nome = nome
        self.quantidade = quantidade
        self.preço = preco
        self.descricao = descricao
        self.fornecedor = fornecedor  # Fornecedor agora é um atributo da classe Produto

    def adicionar_produto(self):
        adicionar_produto_estoque(self)

    def adicionar_quantidade(self):
        adicionar_quantidade_estoque(self.codigo)
        
    def remover_quantidade(self, quantidade):
        remover_quantidade_estoque(self.codigo, quantidade)
        self.alerta_estoque_baixo()

    def atualizar_quantidade(self, num):
         alterar_quantidade_estoque(self.codigo, num)
         self.alerta_estoque_baixo()

    def alerta_estoque_baixo(self):
        if self.quantidade < 5:
            print("Cuidado! Estoque baixo!")
    
    def atualizar_preço(self,num):
        atualizar_preco_estoque(self.codigo,num)
    
    def remover_produto(self):
        remover_produto(self.codigo)

    def alterar_nome(self, novo_nome):
        alterar_nome_estoque(self.codigo, novo_nome)

    def alterar_descrição(self, descricao):
        alterar_descrição_estoque(self.codigo, descricao)
        
    # def to_dict(self):
    #     # Converte o objeto Produto em um dicionário, incluindo o fornecedor como um dicionário
    #     produto_dict = vars(self).copy()  # Copia todos os atributos do produto
    #     produto_dict['fornecedor'] = vars(self.fornecedor)  # Converte o objeto fornecedor em dicionário
    #     return produto_dict

    

