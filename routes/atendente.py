from fastapi import APIRouter, HTTPException
from database import get_engine
from models.models import Atendente, Cliente
from bson import ObjectId
from schema.schema import AssociacaoClienteAtendente

router = APIRouter(
    prefix="/atendentes",
    tags=["Atendentes"],
)

engine = get_engine()

@router.post("/atendentes/", response_model=Atendente)
async def criar_atendente(atendente: Atendente):
    await engine.save(atendente)
    return atendente

@router.get("/atendentes/{atendente_id}")
async def obter_atendente(atendente_id: str):
    try:
        obj_id = ObjectId(atendente_id)
    except:
        raise HTTPException(status_code=400, detail="ID inválido")
    
    atendente = await engine.find_one(Atendente, Atendente.id == obj_id)
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

@router.post("/associar", response_model=dict)
async def associar_cliente_atendente(associacao: AssociacaoClienteAtendente):
    try:
        # Converter os IDs para ObjectId
        cliente_obj_id = ObjectId(associacao.cliente_id)
        atendente_obj_id = ObjectId(associacao.atendente_id)
    except:
        raise HTTPException(status_code=400, detail="IDs inválidos")

    # Buscar Cliente e Atendente no banco
    cliente = await engine.find_one(Cliente, Cliente.id == cliente_obj_id)
    atendente = await engine.find_one(Atendente, Atendente.id == atendente_obj_id)

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    if not atendente:
        raise HTTPException(status_code=404, detail="Atendente não encontrado")
    
    # Aqui você pode associar o cliente ao atendente (um exemplo simples)
    cliente.atendente = atendente
    await engine.save(cliente)

    return {"message": "Cliente associado ao atendente com sucesso", "cliente_id": cliente.id, "atendente_id": atendente.id}