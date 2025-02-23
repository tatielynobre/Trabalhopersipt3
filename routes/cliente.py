from fastapi import APIRouter, HTTPException
from database import get_engine
from models.models import Cliente, Reserva
from bson import ObjectId

router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"],
)

engine = get_engine()

@router.post("/clientes/", response_model=Cliente)
async def criar_cliente(cliente: Cliente):
    await engine.save(cliente)
    return cliente

@router.get("/clientes/{cliente_id}")
async def obter_cliente(cliente_id: str):
    try:
        obj_id = ObjectId(cliente_id)  # Converte string para ObjectId
    except:
        raise HTTPException(status_code=400, detail="ID inválido")
    
    cliente = await engine.find_one(Cliente, Cliente.id == obj_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    return cliente

@router.get("/clientes/", response_model=list[Cliente])
async def listar_clientes(skip: int = 0, limit: int = 10):
    return await engine.find(Cliente, skip=skip, limit=limit)

@router.put("/clientes/{cliente_id}", response_model=Cliente)
async def atualizar_cliente(cliente_id: str, cliente: Cliente):
    cliente_atualizado = await engine.find_one(Cliente, Cliente.id == cliente_id)
    if not cliente_atualizado:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    cliente_atualizado.nome = cliente.nome
    cliente_atualizado.email = cliente.email
    cliente_atualizado.telefone = cliente.telefone
    await engine.save(cliente_atualizado)
    return cliente_atualizado

@router.delete("/clientes/{cliente_id}")
async def deletar_cliente(cliente_id: str):
    cliente = await engine.find_one(Cliente, Cliente.id == cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    await engine.remove(await engine.find(Reserva, Reserva.cliente == cliente.id))
    await engine.delete(cliente)
    return {"message": "Cliente e reservas associadas removidos"}

@router.get("/clientes/nome/{nome}")
async def buscar_cliente_por_nome(nome: str, skip: int = 0, limit: int = 10):
    return await engine.find(Cliente, {"nome": {"$regex": nome, "$options": "i"}}, skip=skip, limit=limit)

@router.get("/clientes/ordenados")
async def listar_clientes_ordenados():
    return await engine.find(Cliente, sort=Cliente.nome.asc())