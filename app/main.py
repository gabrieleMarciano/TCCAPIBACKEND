from fastapi import FastAPI
from app.routers import usuario_router

app = FastAPI()

app.include_router(usuario_router.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to SGHSS API!"}
