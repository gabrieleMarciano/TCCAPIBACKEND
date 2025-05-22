from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.prontuario_model import Prontuario
from app.schemas.prontuario_schema import ProntuarioCreate
from app.models.log_model import Log  # <--- IMPORTAÇÃO PARA LOG

def create_prontuario(db: Session, prontuario: ProntuarioCreate):
    db_prontuario = Prontuario(**prontuario.dict())
    db.add(db_prontuario)
    db.commit()
    db.refresh(db_prontuario)

    # LOG: criação de prontuário
    log = Log(
        id_usuario=None,
        acao="criação",
        tabela_afetada="prontuarios",
        registro_id=db_prontuario.id_prontuario,
        observacoes=f"Prontuário criado para consulta ID {db_prontuario.id_consulta}"
    )
    db.add(log)
    db.commit()

    return db_prontuario

def get_prontuarios(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Prontuario).offset(skip).limit(limit).all()

def get_prontuario_by_id(db: Session, prontuario_id: int):
    return db.query(Prontuario).filter(Prontuario.id_prontuario == prontuario_id).first()

def delete_prontuario(db: Session, prontuario_id: int):
    prontuario = get_prontuario_by_id(db, prontuario_id)
    if prontuario is None:
        raise HTTPException(status_code=404, detail="Prontuário não encontrado")

    db.delete(prontuario)
    db.commit()

    # LOG: exclusão de prontuário
    log = Log(
        id_usuario=None,
        acao="exclusão",
        tabela_afetada="prontuarios",
        registro_id=prontuario_id,
        observacoes=f"Prontuário excluído (consulta ID {prontuario.id_consulta})"
    )
    db.add(log)
    db.commit()

    return prontuario
