from fastapi import APIRouter, HTTPException
from database import get_engine
from models.models import Quarto

'''
a) Consultas por ID ok 
b) Listagens filtradas por relacionamentos 
c) Buscas por texto parcial e case insensitive. ok
e) Agregações e contagens utilizando aggregation pipeline
f) Classificações e ordenações ok
g) Consultas complexas envolvendo múltiplas coleções
'''

router = APIRouter(
    prefix="/quartos",
    tags=["Quartos"],
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

@router.get("/quartos/busca/{texto}", response_model=list[Quarto])
async def buscar_quartos_por_texto(texto: str):
    quartos = await engine.find(Quarto, {"$text": {"$search": texto, "$caseSensitive": False}})
    return quartos

@router.get("/quartos/ordenados/{campo}", response_model=list[Quarto])
async def listar_quartos_ordenados(campo: str):
    quartos = await engine.find(Quarto, sort={campo: 1})
    return quartos

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
