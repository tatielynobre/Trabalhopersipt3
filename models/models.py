from odmantic import Model, Reference
from typing import Optional
from datetime import datetime

class Atendente(Model):
        nome: Optional[str] = None

class Cliente(Model):
        nome: Optional[str] = None
        email: Optional[str] = None
        telefone: Optional[str] = None

class Quarto(Model):
        numQuarto: int
        nivel_quarto: str
        
class Reserva(Model):
        cliente: Cliente = Reference()
        quarto: Quarto = Reference()
        data_inicio: datetime
        data_fim: datetime