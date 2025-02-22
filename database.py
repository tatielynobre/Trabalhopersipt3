from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
import os

#carregando variaveis do arquivo .env
load_dotenv()

#conectando ao banco de dados
DATABASE_URL = os.getenv("Database_url")
client = AsyncIOMotorClient(DATABASE_URL)
db = client.mydatabase
engine = AIOEngine(client=client, database="mydatabase")

def get_engine() -> AIOEngine:
    return engine

