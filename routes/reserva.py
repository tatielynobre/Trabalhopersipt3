from fastapi import APIRouter, HTTPException
from database import get_engine
from models.models import Reserva, Cliente, Quarto
from bson import ObjectId
from schema.schema import ReservaCreate
from datetime import datetime
from odmantic import engine
import logging

'''
a) Consultas por ID ok
b) Listagens filtradas por relacionamentos ok
c) Buscas por texto parcial e case insensitive. ok
d) Filtros por data/ano utilizando consultas baseadas em operadores do MongoDB ok
e) Agregações e contagens utilizando aggregation pipeline
f) Classificações e ordenações ok
g) Consultas complexas envolvendo múltiplas coleções
'''
logging.basicConfig(level=logging.INFO)

router = APIRouter(
    prefix="/reservas",
    tags=["Reservas"],
)

engine = get_engine()


# Função para converter datetime.date para datetime (com hora 00:00)
def convert_date_to_datetime(date_obj):
    return datetime.combine(date_obj, datetime.min.time())

@router.post("/reservas/", response_model=Reserva)
async def criar_reserva(reserva_data: ReservaCreate):
    try:
        cliente_id = ObjectId(reserva_data.cliente_id)  # Converter ID do cliente
        quarto_id = ObjectId(reserva_data.quarto_id)    # Converter ID do quarto
    except:
        raise HTTPException(status_code=400, detail="ID inválido")

    # Buscar Cliente e Quarto no banco
    cliente = await engine.find_one(Cliente, Cliente.id == cliente_id)
    quarto = await engine.find_one(Quarto, Quarto.id == quarto_id)

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    if not quarto:
        raise HTTPException(status_code=404, detail="Quarto não encontrado")

    # Converter as datas para datetime com hora zero
    data_inicio_dt = convert_date_to_datetime(reserva_data.data_inicio)
    data_fim_dt = convert_date_to_datetime(reserva_data.data_fim)

    # Criar e salvar a reserva com referências corretas e datas ajustadas
    reserva = Reserva(
        data_inicio=data_inicio_dt,
        data_fim=data_fim_dt,
        cliente=cliente,  # Passando o objeto Cliente
        quarto=quarto     # Passando o objeto Quarto
    )

    await engine.save(reserva)
    return reserva

@router.get("/reservas/{reserva_id}")
async def obter_reserva(reserva_id: str):
    try:
        obj_id = ObjectId(reserva_id)
    except:
        raise HTTPException(status_code=400, detail="ID inválido")
    
    reserva = await engine.find_one(Reserva, Reserva.id == obj_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    
    return reserva

@router.get("/reservas/", response_model=list[Reserva])
async def listar_reservas():
    return await engine.find(Reserva)

# Função para converter datetime.date para datetime (com hora 00:00)
def convert_date_to_datetime(date_obj):
    return datetime.combine(date_obj, datetime.min.time())

@router.put("/reservas/{reserva_id}", response_model=Reserva)
async def atualizar_reserva(reserva_id: str, reserva_data: ReservaCreate):
    try:
        reserva_obj_id = ObjectId(reserva_id)  # Converter reserva_id para ObjectId
    except:
        raise HTTPException(status_code=400, detail="ID da reserva inválido")

    reserva = await engine.find_one(Reserva, Reserva.id == reserva_obj_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")

    # Buscar Cliente e Quarto no banco
    cliente = await engine.find_one(Cliente, Cliente.id == reserva_data.cliente_id)
    quarto = await engine.find_one(Quarto, Quarto.id == reserva_data.quarto_id)

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    if not quarto:
        raise HTTPException(status_code=404, detail="Quarto não encontrado")

    # Converter as datas para datetime com hora zero
    reserva.data_inicio = convert_date_to_datetime(reserva_data.data_inicio)
    reserva.data_fim = convert_date_to_datetime(reserva_data.data_fim)
    reserva.cliente = cliente
    reserva.quarto = quarto

    await engine.save(reserva)
    return reserva


@router.delete("/reservas/{reserva_id}")
async def deletar_reserva(reserva_id: str):
    reserva = await engine.find_one(Reserva, Reserva.id == reserva_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    await engine.delete(reserva)
    return {"message": "Reserva removida"}

@router.get("/reservas/ordenadas")
async def listar_reservas_ordenadas():
    return await engine.find(Reserva, sort=Reserva.data_inicio.desc())

@router.get("/reservas/cliente/{cliente_id}", response_model=list[Reserva])
async def listar_reservas_por_cliente(cliente_id: str):
    try:
        cliente_obj_id = ObjectId(cliente_id)  # Converter para ObjectId
    except:
        raise HTTPException(status_code=400, detail="ID do cliente inválido")

    # Buscar reservas pelo campo cliente (sem acessar cliente.id)
    reservas = await engine.find(Reserva, Reserva.cliente == cliente_obj_id)
    return reservas

@router.get("/reservas/ordenadas/crescente")
async def listar_reservas_ordenadas_crescente():
    return await engine.find(Reserva, sort=Reserva.data_inicio.asc())

@router.get("/reservas/ordenadas/decrescente")
async def listar_reservas_ordenadas_decrescente():
    return await engine.find(Reserva, sort=Reserva.data_inicio.desc())

@router.get("/reservas/contagem-por-cliente/{cliente_id}")
async def contar_reservas_por_cliente(cliente_id: str):
    try:
        object_id = ObjectId(cliente_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

    pipeline = [
        {"$match": {"cliente": object_id}},  # Ajustado para procurar clientes como ObjectId
        {"$group": {"_id": "$cliente", "total_reservas": {"$sum": 1}}}
    ]

    resultado = await engine.get_collection(Reserva).aggregate(pipeline).to_list(None)

    if not resultado:
        return {"cliente_id": cliente_id, "total_reservas": 0}

    return {"cliente_id": cliente_id, "total_reservas": resultado[0]["total_reservas"]}