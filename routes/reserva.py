from fastapi import APIRouter, HTTPException
from database import get_engine
from models.models import Reserva

router = APIRouter(
    prefix="/reservas",
    tags=["Reservas"],
)

engine = get_engine()

@router.post("/reservas/", response_model=Reserva)
async def criar_reserva(reserva: Reserva):
    await engine.save(reserva)
    return reserva

@router.get("/reservas/{reserva_id}", response_model=Reserva)
async def obter_reserva(reserva_id: str):
    reserva = await engine.find_one(Reserva, Reserva.id == reserva_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    return reserva

@router.get("/reservas/", response_model=list[Reserva])
async def listar_reservas():
    return await engine.find(Reserva)

@router.put("/reservas/{reserva_id}", response_model=Reserva)
async def atualizar_reserva(reserva_id: str, reserva: Reserva):
    reserva_atualizada = await engine.find_one(Reserva, Reserva.id == reserva_id)
    if not reserva_atualizada:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    reserva_atualizada.data_inicio = reserva.data_inicio
    reserva_atualizada.data_fim = reserva.data_fim
    await engine.save(reserva_atualizada)
    return reserva_atualizada

@router.delete("/reservas/{reserva_id}")
async def deletar_reserva(reserva_id: str):
    reserva = await engine.find_one(Reserva, Reserva.id == reserva_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    await engine.delete(reserva)
    return {"message": "Reserva removida"}

@router.get("/reservas/completas")
async def listar_reservas_completas():
    reservas = await engine.find(Reserva, projection={"cliente": 1, "quarto": 1})
    return reservas

@router.get("/reservas/data/{ano}")
async def listar_reservas_por_ano(ano: int):
    return await engine.find(Reserva, {"data_inicio": {"$gte": f"{ano}-01-01", "$lte": f"{ano}-12-31"}})