# main.py
from estoque import  exibir_estoque, get_produto
from categoria import Categoria
from produto import Produto
from subclasses import criar_subclasse

#Funcionalidade adicionar categoria:
#Cosméticos = Categoria("Cosméticos", "Corpo/Rosto","Importado/Nacional")
#Cosméticos.criar_categoria()

#Funcionalidade criar um produto - necessário criar pela subcategoria
# Cosméticos = criar_subclasse("Cosméticos")
# Shampoo = Cosméticos("Shampoo", 50, 10, "Shampoo para cabelo", "Natura", "Cabelo", "Nacional")
# Shampoo.adicionar_produto()

#Funcionalidade de get_produto por código e acessando métodos de produto, precisa rodar sempre a primeira linha que define Shampoo 
#Shampoo = get_produto(1)
#Shampoo.adicionar_quantidade()
#Shampoo.remover_quantidade()
#Shampoo.atualizar_quantidade(3)
#Shampoo.atualizar_preço(15)
#Shampoo.remover_produto()

#Funcionalidade de exibir todos os produtos:
#exibir_estoque()

#Funcionalidades de exibir todas as categorias:
#Categorias = Categoria.carregar_categorias()
#print(Categorias)

#Funcionalidade de get da categoria e acessar métodos das categorias:
Cosméticos = Categoria.get_categoria_por_nome("Cosméticos")
#Cosméticos.modificar_atributos_adicionais(["Corpo/Rosto", "Importado/Nacional", "Hipoalergenico"])
#print(Cosméticos.atributos_adicionais) #para visualização de atributos alterados
Cosméticos.remover_categoria()



