from estoque import adicionar_produto_estoque, adicionar_quantidade_estoque, remover_quantidade_estoque, alterar_quantidade_estoque, remover_produto

class Produto:
    def __init__(self, codigo, nome, quantidade, preço, descricao, fornecedor):
        self.codigo = codigo
        self.nome = nome
        self.quantidade = quantidade
        self.preço = preço
        self.descricao = descricao
        self.fornecedor = fornecedor
        
    def adicionar_produto(self):
        adicionar_produto_estoque(self)

    def adicionar_quantidade(self):
        self.quantidade = self.quantidade + 1
        adicionar_quantidade_estoque(self.codigo, 1)
        
    def remover_quantidade(self):
        self.quantidade = self.quantidade - 1
        remover_quantidade_estoque(self.codigo, 1)
        self.alerta_estoque_baixo()

    def atualizar_quantidade(self, num):
         self.quantidade = self.quantidade + num
         alterar_quantidade_estoque(self.codigo, self.quantidade)
         self.alerta_estoque_baixo()

    def alerta_estoque_baixo(self):
        if self.quantidade < 5:
            print("Cuidado! Estoque baixo!")
    
    def atualizar_preço(self,num):
        self.preço = num
        print(f"Preço do produto {self.nome} alterado para {self.preço}")
    
    def remover_produto(self):
        remover_produto(self.codigo)
    

