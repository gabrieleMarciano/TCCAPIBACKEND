# app/crud/paciente_crud.py
from sqlalchemy.orm import Session
from app.models.paciente_model import Paciente
from app.schemas.paciente_schema import PacienteCreate
from app.models.log_model import Log

def create_paciente(db: Session, paciente: PacienteCreate, id_usuario_atuante: int = None):
    db_paciente = Paciente(
        nome=paciente.nome,
        data_nascimento=paciente.data_nascimento,
        sexo=paciente.sexo,
        cpf=paciente.cpf,
        telefone=paciente.telefone,
        endereco=paciente.endereco
    )
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)

    if id_usuario_atuante:
        log = Log(
            id_usuario=id_usuario_atuante,
            acao="CREATE",
            tabela_afetada="pacientes",
            registro_id=db_paciente.id_paciente,
            observacoes="Paciente criado"
        )
        db.add(log)
        db.commit()

    return db_paciente

def get_pacientes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Paciente).offset(skip).limit(limit).all()

def get_paciente_by_id(db: Session, paciente_id: int):
    return db.query(Paciente).filter(Paciente.id_paciente == paciente_id).first()

def update_paciente(db: Session, paciente_id: int, paciente: PacienteCreate, id_usuario_atuante: int = None):
    db_paciente = db.query(Paciente).filter(Paciente.id_paciente == paciente_id).first()
    if db_paciente:
        db_paciente.nome = paciente.nome
        db_paciente.data_nascimento = paciente.data_nascimento
        db_paciente.sexo = paciente.sexo
        db_paciente.cpf = paciente.cpf
        db_paciente.telefone = paciente.telefone
        db_paciente.endereco = paciente.endereco
        db.commit()
        db.refresh(db_paciente)

        if id_usuario_atuante:
            log = Log(
                id_usuario=id_usuario_atuante,
                acao="UPDATE",
                tabela_afetada="pacientes",
                registro_id=db_paciente.id_paciente,
                observacoes="Paciente atualizado"
            )
            db.add(log)
            db.commit()
    return db_paciente

def delete_paciente(db: Session, paciente_id: int, id_usuario_atuante: int = None):
    db_paciente = db.query(Paciente).filter(Paciente.id_paciente == paciente_id).first()
    if db_paciente:
        db.delete(db_paciente)
        db.commit()

        if id_usuario_atuante:
            log = Log(
                id_usuario=id_usuario_atuante,
                acao="DELETE",
                tabela_afetada="pacientes",
                registro_id=paciente_id,
                observacoes="Paciente deletado"
            )
            db.add(log)
            db.commit()
    return db_paciente
