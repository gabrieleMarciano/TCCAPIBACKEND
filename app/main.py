from fastapi import FastAPI
from app.routers import consulta_router, paciente_router, usuario_router, prontuario_router, logs_router

app = FastAPI()


# Incluindo o router com o prefixo correto
app.include_router(usuario_router.router, prefix="/usuarios", tags=["usuarios"])
app.include_router(paciente_router.router, prefix="/pacientes")
app.include_router(consulta_router.router, prefix="/consultas", tags=["consultas"])
app.include_router(prontuario_router.router, prefix="/prontuarios", tags=["Prontuários"])
app.include_router(logs_router.router, prefix="/logs", tags=["Logs"])

@app.get("/")
def read_root():
    return {"message": "Welcome to SGHSS API!"}
