# main.py
from estoque import  exibir_estoque, get_produto
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

# Cosméticos = criar_subclasse("Cosméticos")
# Shampoo = Cosméticos(21, "Shampoo", 50, 10, "Shampoo para cabelo", "Natura", "Cabelo", "Nacional")
# Shampoo.adicionar_produto()
#exibir_estoque()


#teste = Categoria.get_categoria_por_nome("Jogos")
#teste.modificar_atributos_adicionais(None)
#print(get_produto(21))
# atributos = vars(get_produto(21)) 
# for atributo, valor in atributos.items():
#     print(f"{atributo}: {valor}")
doc = get_produto(21)
doc.adicionar_quantidade()