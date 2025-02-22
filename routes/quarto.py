from fastapi import APIRouter, HTTPException
from database import get_engine
from models import Quarto

router = APIRouter(
    prefix="/quartos", # Prefixo para todas as rotas
    tags=["Quartos"], # Tag para documentação automática
)

engine = get_engine()


@router.post("/quartos/", response_model=Quarto)
async def criar_quarto(quarto: Quarto):
    await engine.save(quarto)
    return quarto

@router.get("/quartos/{quarto_id}", response_model=Quarto)
async def obter_quarto(quarto_id: str):
    quarto = await engine.find_one(Quarto, Quarto.id == quarto_id)
    if not quarto:
        raise HTTPException(status_code=404, detail="Quarto não encontrado")
    return quarto

@router.get("/quartos/", response_model=list[Quarto])
async def listar_quartos():
    return await engine.find(Quarto)

@router.put("/quartos/{quarto_id}", response_model=Quarto)
async def atualizar_quarto(quarto_id: str, quarto: Quarto):
    quarto_atualizado = await engine.find_one(Quarto, Quarto.id == quarto_id)
    if not quarto_atualizado:
        raise HTTPException(status_code=404, detail="Quarto não encontrado")
    quarto_atualizado.nivel_quarto = quarto.nivel_quarto
    quarto_atualizado.numero_quarto = quarto.numero_quarto
    await engine.save(quarto_atualizado)
    return quarto_atualizado

@router.delete("/quartos/{quarto_id}")
async def deletar_quarto(quarto_id: str):
    quarto = await engine.find_one(Quarto, Quarto.id == quarto_id)
    if not quarto:
        raise HTTPException(status_code=404, detail="Quarto não encontrado")
    await engine.delete(quarto)
    return {"message": "Quarto removido"}
