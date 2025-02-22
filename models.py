from odmantic import Model, Reference
from typing import Optional
from datetime import date

class Atendente(Model):
        nome: Optional[str] = None

class Cliente(Model):
        nome: Optional[str] = None
        email: Optional[str] = None
        telefone: Optional[str] = None
class Quarto(Model):
        numQuarto: int
        nivel_quarto: Optional[str] = None
        
class Reserva(Model):
        cliente: Cliente = Reference()
        quarto: Quarto = Reference ()
        data_inicio: date
        data_fim: date