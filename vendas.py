class Venda:
    def __init__(self, CPFcliente, codigoProdutos, quantidades, preços):
        self.CPFcliente = CPFcliente
        self.codigoProdutos = codigoProdutos  # Lista de códigos de produtos
        self.quantidades = quantidades        # Lista de quantidades correspondentes
        self.preços = preços                  # Lista de preços correspondentes
        self.total = self.calcular_total()    # Calcula o total da venda

    def calcular_total(self):
        total = 0
        for preco, quantidade in zip(self.preços, self.quantidades):
            total += preco * quantidade
        return total
    
# Exemplo de uso:
venda = Venda("12345678900", ["P001", "P002", "P003"], [2, 1, 5], [10.0, 20.0, 5.0])
print(venda.total)
