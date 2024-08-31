# main.py
from estoque import adicionar_produto_estoque, adicionar_quantidade_estoque, remover_quantidade_estoque, alterar_quantidade_estoque, exibir_estoque, remover_produto
from categoria import Categoria
from produto import Produto
from subclasses import criar_subclasse

# exibir_estoque()
# Categoria.carregar_categorias()
# Jogos = Categoria("Jogos2","Plataforma","Gênero")
# Jogos.salvar_categoria()

#Jogos = criar_subclasse("Jogos")
#CS = Jogos(10, "CounterStrike 1.6", 100, 200, "Joguinho bom", "Valve", "PC", "FPS")
#CS.adicionar_quantidade()


#print(Categoria.carregar_categorias())
#print(Categoria.get_categoria_por_nome("Jogos"))
#print(Categoria.get_categoria_por_nome("Roupas").atributos_adicionais)

#exibir_estoque()

#Cosméticos = Categoria("Cosméticos", "Corpo/Rosto","Importado/Nacional")
#Cosméticos.salvar_categoria()

#Cosméticos = Categoria.get_categoria_por_nome("Cosméticos")

#Cosméticos = criar_subclasse("Cosméticos")
#Shampoo = Cosméticos(21, "Shampoo", 50, 10, "Shampoo para cabelo", "Natura", "Cabelo", "Nacional")
#Shampoo.adicionar_produto()
exibir_estoque()

Jogos3 = Categoria("Jogos3","Plataforma","Categoria")
Jogos3.salvar_categoria()