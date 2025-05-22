# app/routers/paciente_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud
from app.paciente_crud import create_paciente, get_pacientes, get_paciente_by_id, update_paciente, delete_paciente
from app.schemas.paciente_schema import PacienteCreate, PacienteOut
from app.database import get_db
from app.auth.jwt_handler import get_usuario_atual  # ✅ Importa o usuário logado

router = APIRouter()

@router.post("/", response_model=PacienteOut)
def criar_paciente(
    paciente: PacienteCreate,
    db: Session = Depends(get_db),
    usuario_logado: dict = Depends(get_usuario_atual)  # ✅ Pega o usuário do token
):
    return create_paciente(db=db, paciente=paciente, id_usuario_atuante=usuario_logado["id"])

@router.get("/", response_model=list[PacienteOut])
def get_pacientes_router(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    usuario_logado: dict = Depends(get_usuario_atual)  # ✅ Agora precisa de token
):
    return get_pacientes(db=db, skip=skip, limit=limit)

@router.get("/{paciente_id}", response_model=PacienteOut)
def get_paciente(
    paciente_id: int,
    db: Session = Depends(get_db),
    usuario_logado: dict = Depends(get_usuario_atual)  # ✅ Token obrigatório
):
    db_paciente = get_paciente_by_id(db=db, paciente_id=paciente_id)
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return db_paciente

@router.put("/{paciente_id}", response_model=PacienteOut)
def atualizar_paciente(
    paciente_id: int,
    paciente: PacienteCreate,
    db: Session = Depends(get_db),
    usuario_logado: dict = Depends(get_usuario_atual)  # ✅ Usa o ID do usuário
):
    db_paciente = update_paciente(db=db, paciente_id=paciente_id, paciente=paciente, id_usuario_atuante=usuario_logado["id"])
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return db_paciente

@router.delete("/{paciente_id}", response_model=PacienteOut)
def deletar_paciente_router(
    paciente_id: int,
    db: Session = Depends(get_db),
    usuario_logado: dict = Depends(get_usuario_atual)  # ✅ Usa o ID do usuário
):
    print("usuario_logado recebido:", usuario_logado)  # <-- aqui

    # Agora, pegue o id de forma segura, usando get() e tentando 'id' ou 'sub' (mais comum)
    id_usuario = usuario_logado.get("id") or usuario_logado.get("sub")
    if not id_usuario:
        raise HTTPException(status_code=400, detail="ID do usuário não encontrado no token")

    db_paciente = delete_paciente(db=db, paciente_id=paciente_id, id_usuario_atuante=id_usuario)
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return db_paciente

