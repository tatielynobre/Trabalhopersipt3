from odmantic import Model, Reference, Field
from typing import Optional
from datetime import date

class Atendente(Model):
        nome: Optional[str] = Field(default=None)

class Cliente(Model):
        nome: Optional[str] = Field(default=None)
        email: Optional[str] = Field(default=None)
        telefone: Optional[str] = Field(default=None)
class Quarto(Model):
        numQuarto: int
        nivel_quarto: str
        
class Reserva(Model):
        cliente: Cliente = Reference()
        quarto: Quarto = Reference ()
        data_inicio: date
        data_fim: date