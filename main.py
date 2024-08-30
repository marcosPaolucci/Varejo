# main.py
from estoque import adicionar_produto_estoque, adicionar_quantidade_estoque, remover_quantidade_estoque, alterar_quantidade_estoque, exibir_estoque
from categoria import Categoria
from produto import Produto
from subclasses import criar_subclasse

# exibir_estoque()
# categorias = Categoria.carregar_categorias()
# Jogos = Categoria("Jogos","Plataforma","Gênero")

Jogos = criar_subclasse("Jogos")
CS = Jogos(10, "CounterStrike 1.6", 100, 200, "Joguinho bom", "Valve", "PC", "FPS")
CS.adicionar_quantidade()
