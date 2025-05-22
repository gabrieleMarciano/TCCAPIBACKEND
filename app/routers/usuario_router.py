from fastapi import APIRouter

router = APIRouter()

@router.get("/usuarios")
def get_usuarios():
    return {"message": "Lista de usuários"}
