from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
import os

#carregando variaveis do arquivo .env
load_dotenv()

#conectando ao banco de dados
DATABASE_URL = os.getenv("DATABASE_URL")
client = AsyncIOMotorClient(DATABASE_URL)
engine = AIOEngine(client=client, database="Hotel")
db = client.Hotel

def get_engine() -> AIOEngine:
    return engine