# tests/test_relatorios.py

import pytest
from unittest.mock import patch, MagicMock
from relatorios import Relatorios
from datetime import datetime

@pytest.fixture
def mock_vendas_collection():
    with patch('relatorios.get_collection') as mock_get_collection:
        mock_col_vendas = MagicMock()
        mock_get_collection.side_effect = lambda name: mock_col_vendas if name == "Vendas" else MagicMock()
        yield mock_col_vendas

@pytest.fixture
def mock_produtos_collection():
    with patch('relatorios.get_collection') as mock_get_collection:
        mock_col_produtos = MagicMock()
        mock_get_collection.side_effect = lambda name: mock_col_produtos if name == "Produtos" else MagicMock()
        yield mock_col_produtos

@pytest.fixture
def mock_movimentacoes_collection():
    with patch('relatorios.get_collection') as mock_get_collection:
        mock_col_movimentacoes = MagicMock()
        mock_get_collection.side_effect = lambda name: mock_col_movimentacoes if name == "Movimentacoes" else MagicMock()
        yield mock_col_movimentacoes

def test_relatorio_vendas_sem_filtro(mock_vendas_collection, capsys):
    relatorios = Relatorios()
    mock_vendas_collection.find.return_value = []
    
    relatorios.relatorio_vendas()
    
    captured = capsys.readouterr()
    assert "Nenhuma venda registrada no período." in captured.out

def test_relatorio_vendas_com_vendas(mock_vendas_collection, capsys):
    relatorios = Relatorios()
    vendas_mock = [
        {
            'CPFcliente': '123.456.789-00',
            'data_criacao': datetime(2024, 5, 20, 14, 30),
            'itens': [
                {'nome': 'Produto A', 'quantidade': 2, 'preco_unitario': 50.0, 'subtotal': 100.0},
                {'nome': 'Produto B', 'quantidade': 1, 'preco_unitario': 150.0, 'subtotal': 150.0}
            ],
            'total': 250.0
        }
    ]
    mock_vendas_collection.find.return_value = vendas_mock
    
    relatorios.relatorio_vendas()
    
    captured = capsys.readouterr()
    assert "Relatório de Vendas" in captured.out
    assert "CPF Cliente       : 123.456.789-00" in captured.out
    assert "Data              : 20/05/2024 14:30" in captured.out
    assert "Produto         : Produto A" in captured.out
    assert "Quantidade      : 2" in captured.out
    assert "Preço Unitário  : R$50.00" in captured.out
    assert "Subtotal        : R$100.00" in captured.out
    assert "Total da Venda    : R$250.00" in captured.out
    assert "Total de vendas: 1" in captured.out

def test_relatorio_estoque_vazio(mock_produtos_collection, capsys):
    relatorios = Relatorios()
    mock_produtos_collection.find.return_value = []
    
    relatorios.relatorio_estoque()
    
    captured = capsys.readouterr()
    assert "Estoque vazio." in captured.out

def test_relatorio_estoque_com_produtos(mock_produtos_collection, capsys):
    relatorios = Relatorios()
    produtos_mock = [
        {'codigo': 1, 'nome': 'Produto A', 'quantidade': 10, 'preco': 50.0},
        {'codigo': 2, 'nome': 'Produto B', 'quantidade': 5, 'preco': 150.0}
    ]
    mock_produtos_collection.find.return_value = produtos_mock
    
    relatorios.relatorio_estoque()
    
    captured = capsys.readouterr()
    assert "Relatório de Estoque" in captured.out
    assert "Código               : 1" in captured.out
    assert "Nome                 : Produto A" in captured.out
    assert "Quantidade em Estoque: 10" in captured.out
    assert "Preço                : R$50.00" in captured.out
    assert "Total de produtos em estoque: 2" in captured.out

def test_historico_movimentacoes_sem_filtro(mock_movimentacoes_collection, capsys):
    relatorios = Relatorios()
    mock_movimentacoes_collection.find.return_value = []
    
    relatorios.historico_movimentacoes()
    
    captured = capsys.readouterr()
    assert "Nenhuma movimentação registrada." in captured.out

def test_historico_movimentacoes_com_movimentacoes(mock_movimentacoes_collection, capsys):
    relatorios = Relatorios()
    movimentacoes_mock = [
        {
            'data_movimentacao': datetime(2024, 6, 15, 10, 0),
            'codigo_produto': 1,
            'quantidade': 5,
            'tipo': 'entrada',
            'motivo': 'Reabastecimento'
        },
        {
            'data_movimentacao': datetime(2024, 6, 16, 12, 30),
            'codigo_produto': 1,
            'quantidade': 2,
            'tipo': 'saida',
            'motivo': 'Venda'
        }
    ]
    mock_movimentacoes_collection.find.return_value = movimentacoes_mock
    
    relatorios.historico_movimentacoes()
    
    captured = capsys.readouterr()
    assert "Histórico de Movimentações" in captured.out
    assert "Data               : 15/06/2024 10:00" in captured.out
    assert "Produto Código     : 1" in captured.out
    assert "Quantidade Movimentada: 5" in captured.out
    assert "Tipo               : Entrada" in captured.out
    assert "Motivo             : Reabastecimento" in captured.out
    assert "Data               : 16/06/2024 12:30" in captured.out
    assert "Tipo               : Saida" in captured.out
    assert "Motivo             : Venda" in captured.out
    assert "Total de movimentações: 2" in captured.out
