from estoque import adicionar_produto_estoque, adicionar_quantidade_estoque, remover_quantidade_estoque, alterar_quantidade_estoque, remover_produto, atualizar_preco_estoque

class Produto:
    def __init__(self, nome, quantidade, preço, descricao, fornecedor):
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
         self.quantidade = num
         alterar_quantidade_estoque(self.codigo, self.quantidade)
         self.alerta_estoque_baixo()

    def alerta_estoque_baixo(self):
        if self.quantidade < 5:
            print("Cuidado! Estoque baixo!")
    
    def atualizar_preço(self,num):
        atualizar_preco_estoque(self.codigo,num)
    
    def remover_produto(self):
        remover_produto(self.codigo)
    

