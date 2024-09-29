# test_fornecedor.py

import pytest
from unittest.mock import patch, MagicMock, call
from fornecedor import Fornecedor
from bson import ObjectId

@pytest.fixture
def mock_get_collection():
    with patch('fornecedor.get_collection') as mock_get_collection:
        yield mock_get_collection  # Retorna a função get_collection mockada

def test_criar_fornecedor(mock_get_collection):
    """Testa a criação de um fornecedor."""
    mock_collection = mock_get_collection.return_value
    mock_collection.find_one.return_value = None  # Simula que o fornecedor não existe

    fornecedor = Fornecedor(
        nome="Fornecedor Teste",
        cnpj="12.345.678/0001-95",
        endereco="Rua Teste, 123",
        telefone="11999999999",
        email="teste@fornecedor.com",
        nome_representante="Representante Teste"
    )
    
    # Configura o retorno do método insert_one
    mock_result = MagicMock()
    mock_result.inserted_id = ObjectId()
    mock_collection.insert_one.return_value = mock_result

    fornecedor.criar_fornecedor()
    
    # Verifica se insert_one foi chamado com os dados corretos
    mock_collection.insert_one.assert_called_once_with({
        'nome': "Fornecedor Teste",
        'cnpj': "12345678000195",  # CNPJ sem formatação
        'endereco': "Rua Teste, 123",
        'telefone': "11999999999",
        'email': "teste@fornecedor.com",
        'nome_representante': "Representante Teste"
    })

def test_buscar_todos_fornecedores(mock_get_collection):
    """Testa a busca de todos os fornecedores."""
    mock_collection = mock_get_collection.return_value
    fornecedores_mock = [
        {'nome': 'Fornecedor A', 'cnpj': '12345678000195'},
        {'nome': 'Fornecedor B', 'cnpj': '98765432000110'}
    ]
    mock_collection.find.return_value = fornecedores_mock  # Simula dois fornecedores
    
    fornecedores = list(Fornecedor.buscar_todos_fornecedores())
    
    assert len(fornecedores) == 2
    assert fornecedores[0]['nome'] == 'Fornecedor A'
    assert fornecedores[1]['nome'] == 'Fornecedor B'
    
    # Verifica se a função find foi chamada
    mock_collection.find.assert_called_once_with()

def test_buscar_fornecedor_por_nome(mock_get_collection):
    """Testa a busca de um fornecedor por nome."""
    mock_collection = mock_get_collection.return_value
    nome = "Fornecedor A"
    fornecedor_data = {'nome': nome, 'cnpj': '12345678000195'}
    mock_collection.find_one.side_effect = [None, fornecedor_data]

    fornecedor = Fornecedor.buscar_fornecedor(nome)

    assert fornecedor['nome'] == nome
    assert fornecedor['cnpj'] == '12345678000195'

    busca = nome.strip()  # Remover .lower()

    expected_calls = [
        call({'cnpj': Fornecedor.remover_formatacao_cnpj(nome)}),
        call({'nome': {'$regex': f'^{busca}$', '$options': 'i'}})
    ]
    mock_collection.find_one.assert_has_calls(expected_calls)

def test_buscar_fornecedor_por_cnpj(mock_get_collection):
    """Testa a busca de um fornecedor por CNPJ."""
    mock_collection = mock_get_collection.return_value
    cnpj = "12.345.678/0001-95"
    fornecedor_data = {'nome': 'Fornecedor A', 'cnpj': '12345678000195'}
    mock_collection.find_one.return_value = fornecedor_data
    
    fornecedor = Fornecedor.buscar_fornecedor(cnpj)
    
    assert fornecedor['nome'] == 'Fornecedor A'
    assert fornecedor['cnpj'] == '12345678000195'
    
    # Verifica se find_one foi chamado com o CNPJ correto
    mock_collection.find_one.assert_called_once_with({'cnpj': "12345678000195"})  # CNPJ sem formatação

def test_modificar_fornecedor(mock_get_collection):
    """Testa a modificação de dados de um fornecedor."""
    mock_collection = mock_get_collection.return_value
    id_fornecedor = ObjectId()
    novos_dados = {'nome': 'Fornecedor Atualizado'}
    
    # Configura o retorno do método update_one
    mock_result = MagicMock()
    mock_result.modified_count = 1
    mock_collection.update_one.return_value = mock_result
    
    Fornecedor.modificar_fornecedor(id_fornecedor, novos_dados)
    
    # Verifica se update_one foi chamado com os dados corretos
    mock_collection.update_one.assert_called_once_with(
        {'_id': id_fornecedor},
        {'$set': novos_dados}
    )

def test_remover_fornecedor(mock_get_collection):
    """Testa a remoção de um fornecedor."""
    mock_collection = mock_get_collection.return_value
    id_fornecedor = ObjectId()
    
    # Configura o retorno do método delete_one
    mock_result = MagicMock()
    mock_result.deleted_count = 1
    mock_collection.delete_one.return_value = mock_result
    
    Fornecedor.remover_fornecedor(id_fornecedor)
    
    # Verifica se delete_one foi chamado com os dados corretos
    mock_collection.delete_one.assert_called_once_with({'_id': id_fornecedor})

def test_validar_cnpj_valido():
    """Testa a validação de um CNPJ válido."""
    cnpj = "12.345.678/0001-95"
    assert Fornecedor.validar_cnpj(cnpj) is True

def test_validar_cnpj_invalido():
    """Testa a validação de um CNPJ inválido."""
    cnpj = "12.345.678/0001-XX"
    assert Fornecedor.validar_cnpj(cnpj) is False
