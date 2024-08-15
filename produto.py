class Produto:
    def __init__(self, codigo, nome, categoria, quantidade, preço, descricao, fornecedor):
        self.codigo = codigo
        self.nome = nome
        self.categoria = categoria
        self.quantidade = quantidade
        self.preço = preço
        self.descricao = descricao
        self.fornecedor = fornecedor

    def adicionar_quantidade(self):
        self.quantidade = self.quantidade + 1

    def remover_quantidade(self):
        self.quantidade = self.quantidade - 1
        self.alerta_estoque_baixo()

    def atualizar_estoque(self, num):
         self.quantidade = self.quantidade + num
         self.alerta_estoque_baixo()

    def alerta_estoque_baixo(self):
        if self.quantidade < 5:
            print("Cuidado! Estoque baixo!")

#OBS: podemos criar categoria eletronicos por exemplo como uma classe filha de produtos

produto = Produto(1, "tenis de corrida", "calçado", 10, 500, "bom tenis", "Paraguai")
produto.adicionar_estoque()
print(produto.quantidade)
#print(dir(produto))
produto.remover_estoque()
print(produto.quantidade)
produto.atualizar_estoque(10)
print(produto.quantidade)
produto.atualizar_estoque(-10)
print(produto.quantidade)
produto.atualizar_estoque(-6)
