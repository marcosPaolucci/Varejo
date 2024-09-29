# test_vendas.py

import pytest
from unittest.mock import patch, MagicMock
from vendas import Registrar_Venda
from datetime import datetime

@patch('vendas.get_collection')
@patch('vendas.get_produto')
def test_registrar_venda_sucesso(mock_get_produto, mock_get_collection):
    # Configura o mock para retornar um produto válido
    mock_produto = MagicMock()
    mock_produto.nome = "Produto Teste"
    mock_produto.preco = 100.0  # Usando 'preco' sem acento
    mock_produto.quantidade = 10
    mock_produto.remover_quantidade = MagicMock()
    mock_get_produto.return_value = mock_produto

    # Configura o mock da coleção
    mock_collection = mock_get_collection.return_value

    # Chama a função Registrar_Venda
    Registrar_Venda("12345678900", [1], [2])

    # Verifica se a função removeu a quantidade correta de estoque
    mock_produto.remover_quantidade.assert_called_once_with(2)

    # Verifica se a venda foi inserida corretamente no MongoDB
    mock_collection.insert_one.assert_called_once()
    inserted_data = mock_collection.insert_one.call_args[0][0]

    # Verifica os dados da venda
    assert inserted_data['CPFcliente'] == "12345678900"
    assert inserted_data['total'] == 200.0  # 2 produtos a 100 cada
    assert len(inserted_data['itens']) == 1
    assert inserted_data['itens'][0]['nome'] == "Produto Teste"
    assert inserted_data['itens'][0]['quantidade'] == 2
    assert inserted_data['itens'][0]['subtotal'] == 200.0

@patch('vendas.get_collection')
@patch('vendas.get_produto')
def test_registrar_venda_estoque_insuficiente(mock_get_produto, mock_get_collection, capsys):
    # Configura o mock para retornar um produto com quantidade insuficiente
    mock_produto = MagicMock()
    mock_produto.nome = "Produto Teste"
    mock_produto.preco = 100.0
    mock_produto.quantidade = 1  # Quantidade insuficiente
    mock_get_produto.return_value = mock_produto

    # Chama a função Registrar_Venda
    Registrar_Venda("12345678900", [1], [2])

    # Captura a saída
    captured = capsys.readouterr()

    # Verifica a mensagem de erro
    assert "Quantidade insuficiente no estoque" in captured.out

    # Verifica que a venda não foi registrada no MongoDB
    mock_collection = mock_get_collection.return_value
    mock_collection.insert_one.assert_not_called()

@patch('vendas.get_collection')
@patch('vendas.get_produto')
def test_registrar_venda_produto_nao_encontrado(mock_get_produto, mock_get_collection, capsys):
    # Configura o mock para não encontrar o produto
    mock_get_produto.return_value = None

    # Chama a função Registrar_Venda
    Registrar_Venda("12345678900", [1], [2])

    # Captura a saída
    captured = capsys.readouterr()

    # Verifica a mensagem de erro
    assert "Produto com código 1 não encontrado no estoque." in captured.out

    # Verifica que a venda não foi registrada no MongoDB
    mock_collection = mock_get_collection.return_value
    mock_collection.insert_one.assert_not_called()

@patch('vendas.get_collection')
@patch('vendas.get_produto')
def test_registrar_venda_com_promocao(mock_get_produto, mock_get_collection):
    # Configura o mock para retornar um produto válido
    mock_produto = MagicMock()
    mock_produto.nome = "Produto Teste"
    mock_produto.preco = 100.0  # Usando 'preco' sem acento
    mock_produto.quantidade = 10
    mock_produto.remover_quantidade = MagicMock()
    mock_get_produto.return_value = mock_produto

    # Configura o mock da coleção
    mock_collection = mock_get_collection.return_value

    # Aplica uma promoção de 50% de desconto
    promocao = (1, 0.5)

    # Chama a função Registrar_Venda
    Registrar_Venda("12345678900", [1], [2], promocao)

    # Verifica se a função removeu a quantidade correta de estoque
    mock_produto.remover_quantidade.assert_called_once_with(2)

    # Verifica se a venda foi inserida corretamente no MongoDB
    mock_collection.insert_one.assert_called_once()
    inserted_data = mock_collection.insert_one.call_args[0][0]

    # Verifica os dados da venda com promoção aplicada
    assert inserted_data['total'] == 100.0  # 2 produtos com 50% de desconto
    assert inserted_data['itens'][0]['preco_unitario'] == 50.0  # Preço após desconto
    assert inserted_data['itens'][0]['subtotal'] == 100.0
