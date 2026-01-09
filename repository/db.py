from pymongo import AsyncMongoClient

MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "db_score"

PORT = 8888

client = AsyncMongoClient(MONGO_URL) #creo il client

database = client[DB_NAME] # creo database collegato al client

