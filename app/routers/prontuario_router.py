from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.prontuario_schema import ProntuarioCreate, ProntuarioOut
from app.prontuario_crud import (
    create_prontuario,
    get_prontuarios,
    get_prontuario_by_id,
    delete_prontuario,
)

router = APIRouter()

@router.post("/", response_model=ProntuarioOut)
def criar_prontuario(prontuario: ProntuarioCreate, db: Session = Depends(get_db)):
    return create_prontuario(db, prontuario)

@router.get("/", response_model=list[ProntuarioOut])
def listar_prontuarios(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_prontuarios(db, skip, limit)

@router.get("/{prontuario_id}", response_model=ProntuarioOut)
def obter_prontuario(prontuario_id: int, db: Session = Depends(get_db)):
    prontuario = get_prontuario_by_id(db, prontuario_id)
    if prontuario is None:
        raise HTTPException(status_code=404, detail="Prontuário não encontrado")
    return prontuario

@router.delete("/{prontuario_id}", response_model=ProntuarioOut)
def excluir_prontuario(prontuario_id: int, db: Session = Depends(get_db)):
    return delete_prontuario(db, prontuario_id)
