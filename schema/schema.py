from pydantic import BaseModel
from datetime import datetime

class ReservaCreate(BaseModel):
    data_inicio: datetime
    data_fim: datetime
    cliente_id: str
    quarto_id: str

class ClienteID(BaseModel):
    cliente_id: str