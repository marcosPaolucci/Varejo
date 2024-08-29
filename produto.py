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

    def atualizar_quantidade(self, num):
         self.quantidade = self.quantidade + num
         self.alerta_estoque_baixo()

    def alerta_estoque_baixo(self):
        if self.quantidade < 5:
            print("Cuidado! Estoque baixo!")
    
    def atualizar_preço(self,num):
        self.preço = num
        print(f"Preço do produto {self.nome} alterado para {self.preço}")

#OBS: podemos criar categoria eletronicos por exemplo como uma classe filha de produtos

class Eletrodomesticos(Produto):
    def __init__(self, codigo, nome, quantidade, preço, descricao, fornecedor, voltagem):
        self.categoria = "Eletronicos"
        super().__init__(codigo, nome, self.categoria ,quantidade, preço, descricao, fornecedor)
        self.voltagem = voltagem

class Roupas(Produto):
    def __init__(self, codigo, nome, quantidade, preço, descricao, fornecedor, tamanho):
        self.categoria = "Eletronicos"
        super().__init__(codigo, nome, self.categoria ,quantidade, preço, descricao, fornecedor)
        self.tamanho = tamanho

tenis = Produto(1, "tenis de corrida", "calçado", 10, 500, "bom tenis", "Paraguai")
tenis.adicionar_quantidade()
print(tenis.quantidade)
#print(dir(produto))
tenis.remover_quantidade()
print(tenis.quantidade)
tenis.atualizar_quantidade(10)
print(tenis.quantidade)
tenis.atualizar_quantidade(-10)
print(tenis.quantidade)
tenis.atualizar_quantidade(-6)
tenis.atualizar_preço(600)
print(tenis.preço)

# Exemplo de uso
tv = Eletrodomesticos("001", "TV", 10, 1500, "TV 4K", "Samsung", "110V")
secador = Eletrodomesticos("002", "Secador", 50, 100, "Secador bivolt", "Arco", "110/220V")
camiseta = Roupas("003", "Camiseta Blueprint", 20, 70, "Camiseta azul listrada", "Lacoste", "G")
print(tv.nome)        # TV
print(tv.categoria)   # Eletronicos
print(tv.voltagem)    # 220V
tv.adicionar_quantidade()
print(tv.quantidade)
camiseta.remover_quantidade()
print(camiseta.quantidade)
print(secador.descricao)
print(camiseta.tamanho)