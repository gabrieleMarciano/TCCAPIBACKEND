from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.log_model import Log
from app.auth.jwt_handler import get_usuario_atual

router = APIRouter()

@router.get("/", response_model=list[dict])
def listar_logs(db: Session = Depends(get_db), usuario_logado: dict = Depends(get_usuario_atual)):
    logs = db.query(Log).order_by(Log.data_hora.desc()).all()
    
    return [
        {
            "id_log": log.id_log,
            "id_usuario": log.id_usuario,
            "acao": log.acao,
            "tabela_afetada": log.tabela_afetada,
            "registro_id": log.registro_id,
            "data_hora": log.data_hora,
            "observacoes": log.observacoes,
        }
        for log in logs
    ]
