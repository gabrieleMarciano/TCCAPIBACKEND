# app/crud/consulta_crud.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.consulta_model import Consulta
from app.schemas.consulta_schema import ConsultaCreate
from app.models.log_model import Log  # ✅ Importa o modelo Log
from datetime import datetime         # ✅ Para data/hora dos logs

def create_consulta(db: Session, consulta: ConsultaCreate, id_usuario_atuante: int = None):
    db_consulta = Consulta(**consulta.dict())
    db.add(db_consulta)
    db.commit()
    db.refresh(db_consulta)

    # ✅ Cria log automaticamente
    if id_usuario_atuante:
        criar_log(db, id_usuario_atuante, "CREATE", "consultas", db_consulta.id_consulta, "Consulta criada")

    return db_consulta

def get_consulta_by_id(db: Session, consulta_id: int):
    return db.query(Consulta).filter(Consulta.id_consulta == consulta_id).first()

def get_consultas(db: Session, skip: int = 0, limit: int = 10):
    skip = max(skip, 0)
    limit = max(limit, 1)
    return db.query(Consulta).offset(skip).limit(limit).all()

def delete_consulta(db: Session, consulta_id: int, id_usuario_atuante: int = None):
    db_consulta = get_consulta_by_id(db, consulta_id)
    if db_consulta is None:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    
    db.delete(db_consulta)
    db.commit()

    # ✅ Cria log automaticamente
    if id_usuario_atuante:
        criar_log(db, id_usuario_atuante, "DELETE", "consultas", consulta_id, "Consulta deletada")

    return db_consulta

# ✅ Função auxiliar para log (adicionada no final do arquivo)
def criar_log(db: Session, id_usuario: int, acao: str, tabela_afetada: str, registro_id: int, observacoes: str = None):
    log = Log(
        id_usuario=id_usuario,
        acao=acao,
        tabela_afetada=tabela_afetada,
        registro_id=registro_id,
        data_hora=datetime.utcnow(),
        observacoes=observacoes
    )
    db.add(log)
    db.commit()