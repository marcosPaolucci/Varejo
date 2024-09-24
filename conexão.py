from pymongo import MongoClient

# Configurações do MongoDB
host = "localhost"  # Host do MongoDB
port = 27017  # Porta do MongoDB
DATABASE_NAME = "todolist"  # Nome do banco de dados

# Conectar ao MongoDB
client = MongoClient(host, port)
db = client[DATABASE_NAME]

# Função para obter a coleção
def get_collection(collection_name):
    return db[collection_name]

