# test_integration.py

import pytest
from unittest.mock import patch, MagicMock
from produto import Produto
from fornecedor import Fornecedor
from bson import ObjectId

# Aplicar os patches diretamente na função de teste
@patch('produto.get_collection')
@patch('fornecedor.get_collection')
def test_criar_produto_com_fornecedor(mock_get_collection_fornecedor, mock_get_collection_produto):
    # A ordem dos argumentos é invertida em relação à ordem dos decorators
    # mock_get_collection_fornecedor corresponde a 'fornecedor.get_collection'
    # mock_get_collection_produto corresponde a 'produto.get_collection'

    # Obter as coleções mockadas
    mock_collection_fornecedor = mock_get_collection_fornecedor.return_value
    mock_collection_produto = mock_get_collection_produto.return_value

    # Mock da busca de fornecedor
    fornecedor_data = {'nome': 'Fornecedor A', 'cnpj': '12.345.678/0001-95'}
    mock_collection_fornecedor.find_one.return_value = fornecedor_data

    # Configurar o retorno de find_one para None no collection de produtos
    mock_collection_produto.find_one.return_value = None

    # Configurar o retorno de insert_one
    mock_inserted_id = ObjectId()
    mock_collection_produto.insert_one.return_value.inserted_id = mock_inserted_id

    # Criar o produto associado ao fornecedor
    fornecedor = Fornecedor(
        nome="Fornecedor A",
        cnpj="12.345.678/0001-95",
        endereco="Rua A, 100",
        telefone="11999999999",
        email="fornecedorA@exemplo.com",
        nome_representante="Representante A"
    )

    produto = Produto(
        nome="Produto X",
        quantidade=5,
        preco=200.0,
        descricao="Produto X descrição",
        fornecedor=fornecedor.nome  # O nome do fornecedor é passado aqui
    )

    # Adicionar o produto ao estoque
    produto.adicionar_produto()

    # Verifica se o produto foi inserido corretamente no mock da coleção de produtos
    expected_data = {
        'nome': "Produto X",
        'quantidade': 5,
        'preço': 200.0,
        'descricao': "Produto X descrição",
        'fornecedor': "Fornecedor A",
        'codigo': None  # 'codigo' é None antes da inserção
    }
    mock_collection_produto.insert_one.assert_called_once_with(expected_data)

    # Verifica se 'codigo' foi atualizado corretamente após a inserção
    assert produto.codigo == mock_inserted_id
