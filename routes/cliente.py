from fastapi import APIRouter, HTTPException
from database import get_engine
from models import Cliente, Reserva

router = APIRouter(
    prefix="/clientes", # Prefixo para todas as rotas
    tags=["Clientes"], # Tag para documentação automática
)

engine = get_engine()

@router.post("/clientes/", response_model=Cliente)
async def criar_cliente(cliente: Cliente):
    await engine.save(cliente)
    return cliente

@router.get("/clientes/{cliente_id}", response_model=Cliente)
async def obter_cliente(cliente_id: str):
    cliente = await engine.find_one(Cliente, Cliente.id == cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente

@router.get("/clientes/", response_model=list[Cliente])
async def listar_clientes():
    return await engine.find(Cliente)

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