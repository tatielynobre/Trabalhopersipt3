from fastapi import FastAPI
from routes import cliente, atendente, quarto, reserva

# FastAPI app instance
app = FastAPI()

# Rotas para Endpoints
app.include_router(cliente.router)
app.include_router(atendente.router)
app.include_router(quarto.router)
app.include_router(reserva.router)
