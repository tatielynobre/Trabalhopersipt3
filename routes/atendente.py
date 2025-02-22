from fastapi import APIRouter, HTTPException
from database import get_engine
from models import Atendente

router = APIRouter(
    prefix="/atendentes",
    tags=["Atendentes"],
)

engine = get_engine()


@router.post("/atendentes/", response_model=Atendente)
async def criar_atendente(atendente: Atendente):
    await engine.save(atendente)
    return atendente

@router.get("/atendentes/{atendente_id}", response_model=Atendente)
async def obter_atendente(atendente_id: str):
    atendente = await engine.find_one(Atendente, Atendente.id == atendente_id)
    if not atendente:
        raise HTTPException(status_code=404, detail="Atendente não encontrado")
    return atendente

@router.get("/atendentes/", response_model=list[Atendente])
async def listar_atendentes():
    return await engine.find(Atendente)

@router.delete("/atendentes/{atendente_id}")
async def deletar_atendente(atendente_id: str):
    atendente = await engine.find_one(Atendente, Atendente.id == atendente_id)
    if not atendente:
        raise HTTPException(status_code=404, detail="Atendente não encontrado")
    await engine.delete(atendente)
    return {"message": "Atendente removido"}
