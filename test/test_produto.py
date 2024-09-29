# test_produto.py
# test_produto.py

import pytest
from unittest.mock import patch, MagicMock
from produto import Produto
from fornecedor import Fornecedor
from bson import ObjectId

@pytest.fixture
def mock_collection():
    with patch('produto.get_collection') as mock_get_collection:
        mock_collection = MagicMock()
        mock_get_collection.return_value = mock_collection
        yield mock_collection

def test_adicionar_produto(mock_collection):
    fornecedor = Fornecedor(
        nome="Fornecedor Teste",
        cnpj="12.345.678/0001-95",
        endereco="Rua Teste",
        telefone="11999999999",
        email="teste@fornecedor.com",
        nome_representante="Representante Teste"
    )
    produto = Produto(
        nome="Produto Teste",
        quantidade=10,
        preco=99.99,
        descricao="Descrição do produto teste",
        fornecedor=fornecedor,
        collection=mock_collection  # Injetar o mock_collection aqui
    )

    # Configurar o retorno de find_one para None
    mock_collection.find_one.return_value = None

    # Configurar o retorno do método insert_one
    mock_inserted_id = ObjectId()
    mock_collection.insert_one.return_value.inserted_id = mock_inserted_id

    produto.adicionar_produto()

    # Verifica se insert_one foi chamado com os dados corretos
    expected_data = produto.to_dict()
    expected_data['codigo'] = None  # 'codigo' é None antes da inserção

    mock_collection.insert_one.assert_called_once_with(expected_data)

    # Verifica se 'codigo' foi atualizado corretamente após a inserção
    assert produto.codigo == mock_inserted_id

def test_adicionar_quantidade(mock_collection):
    produto = Produto(
        nome="Produto Teste",
        quantidade=10,
        preco=99.99,
        descricao="Descrição do produto teste",
        fornecedor="Fornecedor Teste",
        codigo=1,
        collection=mock_collection  # Injetar o mock_collection
    )

    # Configurar o retorno do método update_one
    mock_result = MagicMock()
    mock_result.modified_count = 1  # Certifique-se de que é um inteiro
    mock_collection.update_one.return_value = mock_result

    produto.adicionar_quantidade(5)

    # Verifica se update_one foi chamado com os parâmetros corretos
    mock_collection.update_one.assert_called_once_with(
        {'codigo': produto.codigo},
        {'$inc': {'quantidade': 5}}
    )

def test_remover_quantidade(mock_collection):
    produto = Produto(
        nome="Produto Teste",
        quantidade=10,
        preco=99.99,
        descricao="Descrição do produto teste",
        fornecedor="Fornecedor Teste",
        codigo=1,
        collection=mock_collection  # Injetar o mock_collection
    )

    # Configurar o retorno do método update_one
    mock_result = MagicMock()
    mock_result.modified_count = 1
    mock_collection.update_one.return_value = mock_result

    produto.remover_quantidade(3)

    # Verifica se update_one foi chamado com os parâmetros corretos
    mock_collection.update_one.assert_called_once_with(
        {'codigo': produto.codigo},
        {'$inc': {'quantidade': -3}}
    )

def test_atualizar_quantidade(mock_collection):
    produto = Produto(
        nome="Produto Teste",
        quantidade=10,
        preco=99.99,
        descricao="Descrição do produto teste",
        fornecedor="Fornecedor Teste",
        codigo=1,
        collection=mock_collection  # Injetar o mock_collection
    )

    # Configurar o retorno do método update_one
    mock_result = MagicMock()
    mock_result.modified_count = 1
    mock_collection.update_one.return_value = mock_result

    produto.atualizar_quantidade(20)

    # Verifica se update_one foi chamado com os parâmetros corretos
    mock_collection.update_one.assert_called_once_with(
        {'codigo': produto.codigo},
        {'$set': {'quantidade': 20}}
    )

def test_atualizar_preco(mock_collection):
    produto = Produto(
        nome="Produto Teste",
        quantidade=10,
        preco=99.99,
        descricao="Descrição do produto teste",
        fornecedor="Fornecedor Teste",
        codigo=1,
        collection=mock_collection  # Injetar o mock_collection
    )

    # Configurar o retorno do método update_one
    mock_result = MagicMock()
    mock_result.modified_count = 1
    mock_collection.update_one.return_value = mock_result

    produto.atualizar_preco(149.99)

    # Verifica se update_one foi chamado com os parâmetros corretos
    mock_collection.update_one.assert_called_once_with(
        {'codigo': produto.codigo},
        {'$set': {'preço': 149.99}}
    )

def test_alterar_nome(mock_collection):
    produto = Produto(
        nome="Produto Teste",
        quantidade=10,
        preco=99.99,
        descricao="Descrição do produto teste",
        fornecedor="Fornecedor Teste",
        codigo=1,
        collection=mock_collection  # Injetar o mock_collection
    )

    novo_nome = "Produto Atualizado"

    # Configurar o retorno do método update_one
    mock_result = MagicMock()
    mock_result.modified_count = 1
    mock_collection.update_one.return_value = mock_result

    produto.alterar_nome(novo_nome)

    # Verifica se update_one foi chamado com os parâmetros corretos
    mock_collection.update_one.assert_called_once_with(
        {'codigo': produto.codigo},
        {'$set': {'nome': novo_nome}}
    )

def test_alterar_descricao(mock_collection):
    produto = Produto(
        nome="Produto Teste",
        quantidade=10,
        preco=99.99,
        descricao="Descrição do produto teste",
        fornecedor="Fornecedor Teste",
        codigo=1,
        collection=mock_collection  # Injetar o mock_collection
    )

    nova_descricao = "Nova descrição do produto"

    # Configurar o retorno do método update_one
    mock_result = MagicMock()
    mock_result.modified_count = 1
    mock_collection.update_one.return_value = mock_result

    produto.alterar_descricao(nova_descricao)

    # Verifica se update_one foi chamado com os parâmetros corretos
    mock_collection.update_one.assert_called_once_with(
        {'codigo': produto.codigo},
        {'$set': {'descricao': nova_descricao}}
    )

def test_remover_produto(mock_collection):
    produto = Produto(
        nome="Produto Teste",
        quantidade=10,
        preco=99.99,
        descricao="Descrição do produto teste",
        fornecedor="Fornecedor Teste",
        codigo=1,
        collection=mock_collection  # Injetar o mock_collection
    )

    # Configurar o retorno do método delete_one
    mock_result = MagicMock()
    mock_result.deleted_count = 1
    mock_collection.delete_one.return_value = mock_result

    produto.remover_produto()

    # Verifica se delete_one foi chamado com os parâmetros corretos
    mock_collection.delete_one.assert_called_once_with({'codigo': produto.codigo})
