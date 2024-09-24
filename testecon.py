from conexão import get_collection

# Nome da coleção que este script vai usar
COLLECTION_NAME = "tarefas"

# Obter a coleção
collection = get_collection(COLLECTION_NAME)

try:
    estoque = list(collection.find())
    print(estoque)
except Exception as e:
    print(f"Erro ao carregar o estoque: {e}")