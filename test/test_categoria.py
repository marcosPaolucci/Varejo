import pytest
from unittest.mock import patch, MagicMock
from categoria import Categoria

@pytest.fixture
def mock_get_collection():
    with patch('categoria.get_collection') as mock_get_collection:
        yield mock_get_collection  # Retorna a função get_collection mockada

def test_criar_categoria_sem_atributos(mock_get_collection):
    nome = "Eletrônicos"
    # Obter a coleção mockada
    mock_collection = mock_get_collection.return_value
    mock_collection.find_one.return_value = None  # Simula que a categoria não existe
    categoria = Categoria(nome)

    categoria.criar_categoria()

    mock_collection.insert_one.assert_called_once_with({
        'nome_categoria': nome,
        'atributos_adicionais': []
    })

def test_criar_categoria_com_atributos(mock_get_collection):
    nome = "Eletrônicos"
    atributos = ["voltagem", "peso"]
    mock_collection = mock_get_collection.return_value
    mock_collection.find_one.return_value = None  # Simula que a categoria não existe
    categoria = Categoria(nome, *atributos)

    categoria.criar_categoria()

    mock_collection.insert_one.assert_called_once_with({
        'nome_categoria': nome,
        'atributos_adicionais': atributos
    })
    
def test_buscar_todas_categorias(mock_get_collection):
    categorias_mock = [
        {'nome_categoria': 'Eletrônicos', 'atributos_adicionais': ['voltagem', 'peso']},
        {'nome_categoria': 'Alimentos', 'atributos_adicionais': ['data_validade']}
    ]
    mock_collection = mock_get_collection.return_value
    mock_collection.find.return_value = categorias_mock  # Simula o retorno correto
    
    categorias = list(Categoria.buscar_todas_categorias())
    
    assert len(categorias) == 2
    assert categorias[0]['nome_categoria'] == 'Eletrônicos'
    assert categorias[1]['nome_categoria'] == 'Alimentos'

def test_get_categoria_por_nome_encontrada(mock_get_collection):
    nome = "Eletrônicos"
    categoria_data = {'nome_categoria': nome, 'atributos_adicionais': ['voltagem', 'peso']}
    mock_collection = mock_get_collection.return_value
    mock_collection.find_one.return_value = categoria_data
    
    categoria = Categoria.get_categoria_por_nome(nome)
    
    assert categoria.nome_categoria == nome
    assert categoria.atributos_adicionais == ['voltagem', 'peso']

def test_get_categoria_por_nome_nao_encontrada(mock_get_collection):
    nome = "Inexistente"
    mock_collection = mock_get_collection.return_value
    mock_collection.find_one.return_value = None
    
    categoria = Categoria.get_categoria_por_nome(nome)
    
    assert categoria is None

def test_modificar_atributos_adicionais(mock_get_collection):
    nome = "Eletrônicos"
    novos_atributos = ["voltagem", "peso", "cor"]
    mock_collection = mock_get_collection.return_value
    categoria = Categoria(nome, "voltagem", "peso")
    
    # Configurar o retorno do método update_one
    mock_result = MagicMock()
    mock_result.modified_count = 1
    mock_collection.update_one.return_value = mock_result
    
    categoria.modificar_atributos_adicionais(novos_atributos)
    
    mock_collection.update_one.assert_called_once_with(
        {'nome_categoria': nome},
        {'$set': {'atributos_adicionais': novos_atributos}}
    )

def test_remover_categoria(mock_get_collection):
    nome = "Eletrônicos"
    mock_collection = mock_get_collection.return_value
    categoria = Categoria(nome, "voltagem", "peso")
    
    # Configurar o retorno do método delete_one
    mock_result = MagicMock()
    mock_result.deleted_count = 1
    mock_collection.delete_one.return_value = mock_result
    
    categoria.remover_categoria()
    
    mock_collection.delete_one.assert_called_once_with({'nome_categoria': nome})

