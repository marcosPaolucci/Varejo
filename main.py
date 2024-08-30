# main.py

from categoria import Categoria

# Carregar categorias do JSON
Categoria.carregar_categorias()

# Criar uma nova categoria
nova_categoria = Categoria("Esportes")

# Criar um produto na categoria Eletronicos
Eletronicos = Categoria.get_subclasse("Eletronicos")
if Eletronicos:
    tv = Eletronicos("001", "TV", 10, 1500, "TV 4K", "Samsung")
    print(tv.nome)         # TV
    print(tv.categoria)    # Eletronicos