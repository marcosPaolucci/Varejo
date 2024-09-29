import logging
from conexão import get_collection
from datetime import datetime
from typing import Optional, List

# Configuração básica do logging
logging.basicConfig(filename='relatorios.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

class Relatorios:
    def __init__(self):
        """
        Inicializa as conexões com as coleções necessárias para gerar os relatórios.
        """
        try:
            self.vendas_collection = get_collection("Vendas")
            self.produtos_collection = get_collection("Produtos")
            self.movimentacoes_collection = get_collection("Movimentacoes")
            logging.info("Conexão com as coleções estabelecida com sucesso.")
        except Exception as e:
            logging.error(f"Erro ao conectar às coleções: {e}")
            print(f"Ocorreu um erro ao conectar às coleções: {e}")

    def relatorio_vendas(self, data_inicio: Optional[datetime] = None, data_fim: Optional[datetime] = None):
        """
        Gera um relatório detalhado das vendas realizadas.
        Filtros opcionais de data de início e data de fim.

        Args:
            data_inicio (datetime, optional): Data e hora de início do período. Defaults to None.
            data_fim (datetime, optional): Data e hora de fim do período. Defaults to None.
        """
        try:
            if (data_inicio and not isinstance(data_inicio, datetime)) or (data_fim and not isinstance(data_fim, datetime)):
                raise ValueError("data_inicio e data_fim devem ser objetos datetime.")
            
            query = {}
            if data_inicio and data_fim:
                query = {
                    'data_criacao': {
                        '$gte': data_inicio,
                        '$lte': data_fim
                    }
                }
            
            vendas = list(self.vendas_collection.find(query))
            if not vendas:
                print("Nenhuma venda registrada no período.")
                logging.info("Relatório de vendas gerado sem registros no período especificado.")
                return
            
            print("\nRelatório de Vendas")
            print("=" * 80)
            for venda in vendas:
                print(f"CPF Cliente       : {venda.get('CPFcliente', 'N/A')}")
                data_venda = venda.get('data_criacao')
                if isinstance(data_venda, datetime):
                    data_str = data_venda.strftime('%d/%m/%Y %H:%M')
                else:
                    data_str = 'N/A'
                print(f"Data              : {data_str}")
                print("Itens Vendidos:")
                for item in venda.get('itens', []):
                    print(f"  - Produto         : {item.get('nome', 'N/A')}")
                    print(f"    Quantidade      : {item.get('quantidade', 0)}")
                    print(f"    Preço Unitário  : R${item.get('preco_unitario', 0.0):.2f}")
                    print(f"    Subtotal        : R${item.get('subtotal', 0.0):.2f}")
                print(f"Total da Venda    : R${venda.get('total', 0.0):.2f}")
                print("-" * 80)
            print(f"Total de vendas: {len(vendas)}")
            logging.info(f"Relatório de vendas gerado com sucesso. Total de vendas: {len(vendas)}.")
        except Exception as e:
            print(f"Ocorreu um erro ao gerar o relatório de vendas: {e}")
            logging.error(f"Erro ao gerar relatório de vendas: {e}")

    def relatorio_estoque(self):
        """
        Gera um relatório da quantidade atual de todos os produtos no estoque.
        """
        try:
            produtos = list(self.produtos_collection.find({}))
            if not produtos:
                print("Estoque vazio.")
                logging.info("Relatório de estoque gerado sem produtos.")
                return
            
            print("\nRelatório de Estoque")
            print("=" * 80)
            for produto in produtos:
                print(f"Código               : {produto.get('codigo', 'N/A')}")
                print(f"Nome                 : {produto.get('nome', 'N/A')}")
                print(f"Quantidade em Estoque: {produto.get('quantidade', 0)}")
                preco = produto.get('preco', 0.0)
                print(f"Preço                : R${preco:.2f}")
                print("-" * 80)
            print(f"Total de produtos em estoque: {len(produtos)}")
            logging.info(f"Relatório de estoque gerado com sucesso. Total de produtos: {len(produtos)}.")
        except Exception as e:
            print(f"Ocorreu um erro ao gerar o relatório de estoque: {e}")
            logging.error(f"Erro ao gerar relatório de estoque: {e}")

    def historico_movimentacoes(self, codigo_produto: Optional[int] = None):
        """
        Exibe o histórico de todas as adições e remoções de estoque.
        Pode ser filtrado por código de produto.

        Args:
            codigo_produto (int, optional): Código do produto para filtrar as movimentações. Defaults to None.
        """
        try:
            query = {}
            if codigo_produto is not None:
                if not isinstance(codigo_produto, int):
                    raise ValueError("codigo_produto deve ser um inteiro.")
                query = {'codigo_produto': codigo_produto}
    
            movimentacoes = list(self.movimentacoes_collection.find(query))
            if not movimentacoes:
                print("Nenhuma movimentação registrada.")
                logging.info("Relatório de movimentações gerado sem registros.")
                return
            
            print("\nHistórico de Movimentações")
            print("=" * 80)
            for movimentacao in movimentacoes:
                data_movimentacao = movimentacao.get('data_movimentacao')
                if isinstance(data_movimentacao, datetime):
                    data_str = data_movimentacao.strftime('%d/%m/%Y %H:%M')
                else:
                    data_str = 'N/A'
                print(f"Data               : {data_str}")
                print(f"Produto Código     : {movimentacao.get('codigo_produto', 'N/A')}")
                print(f"Quantidade Movimentada: {movimentacao.get('quantidade', 0)}")
                tipo = movimentacao.get('tipo', 'N/A').capitalize()
                print(f"Tipo               : {tipo}")
                print(f"Motivo             : {movimentacao.get('motivo', 'N/A')}")
                print("-" * 80)
            print(f"Total de movimentações: {len(movimentacoes)}")
            logging.info(f"Relatório de movimentações gerado com sucesso. Total de movimentações: {len(movimentacoes)}.")
        except Exception as e:
            print(f"Ocorreu um erro ao gerar o relatório de movimentações: {e}")
            logging.error(f"Erro ao gerar relatório de movimentações: {e}")
