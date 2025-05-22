from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.usuario_model import Usuario
from app.schemas.usuario_schema import UsuarioCreate
from app.auth.jwt_handler import criar_hash_senha
from app.models.log_model import Log



def create_usuario(db: Session, usuario: UsuarioCreate, id_usuario_atuante: int = None):
    usuario_existente = get_usuario_by_email(db, usuario.email)
    if usuario_existente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    
    db_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=criar_hash_senha(usuario.senha),
        tipo=usuario.tipo.value
    )

    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)

    if id_usuario_atuante:
        novo_log = Log(
            id_usuario=id_usuario_atuante,
            acao="CREATE",
            tabela_afetada="usuarios",
            registro_id=db_usuario.id_usuario,
            observacoes="Usuário criado"
        )
        db.add(novo_log)
        db.commit()

    return db_usuario

def get_usuarios(db: Session):
    return db.query(Usuario).all()

def get_usuario_by_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()

def get_usuario_by_id(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()

def update_usuario(db: Session, usuario_id: int, usuario_atualizado: UsuarioCreate, id_usuario_atuante: int = None):
    usuario = get_usuario_by_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    usuario.nome = usuario_atualizado.nome
    usuario.email = usuario_atualizado.email
    usuario.senha = criar_hash_senha(usuario_atualizado.senha)
    usuario.tipo = usuario_atualizado.tipo.value

    db.commit()
    db.refresh(usuario)

    if id_usuario_atuante:
        novo_log = Log(
            id_usuario=id_usuario_atuante,
            acao="UPDATE",
            tabela_afetada="usuarios",
            registro_id=usuario.id_usuario,
            observacoes="Usuário atualizado"
        )
        db.add(novo_log)
        db.commit()

    return usuario

def delete_usuario(db: Session, usuario_id: int, id_usuario_atuante: int = None):
    usuario = get_usuario_by_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    db.delete(usuario)
    db.commit()

    if id_usuario_atuante:
        novo_log = Log(
            id_usuario=id_usuario_atuante,
            acao="DELETE",
            tabela_afetada="usuarios",
            registro_id=usuario_id,
            observacoes="Usuário deletado"
        )
        db.add(novo_log)
        db.commit()

    return usuario



