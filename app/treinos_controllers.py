from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Treino, TreinoRequest
from app.auth_utils import is_admin

router = APIRouter()

@router.get("/treinos", summary="Listar todos os treinos")
def get_treinos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    treinos = db.query(Treino).offset(skip).limit(limit).all()
    return treinos

@router.post("/treinos", summary="Adicionar um novo treino")
def create_treino(
    treino_data: TreinoRequest, 
    current_user=Depends(is_admin), 
    db: Session = Depends(get_db)
):
    # Criação do treino com os dados recebidos
    novo_treino = Treino(**treino_data.dict())
    db.add(novo_treino)
    db.commit()
    db.refresh(novo_treino)
    return novo_treino

@router.put("/treinos/{treino_id}", summary="Atualizar um treino")
def update_treino(
    treino_id: int, 
    treino_data: TreinoRequest, 
    current_user=Depends(is_admin), 
    db: Session = Depends(get_db)
):
    treino = db.query(Treino).filter(Treino.id == treino_id).first()
    if not treino:
        raise HTTPException(status_code=404, detail=f"Treino com ID {treino_id} não encontrado!")

    # Atualização dos dados do treino
    if treino_data.nome:
        treino.nome = treino_data.nome
    if treino_data.tipo:
        treino.tipo = treino_data.tipo
    if treino_data.descricao:
        treino.descricao = treino_data.descricao
    if treino_data.duracao:
        treino.duracao = treino_data.duracao

    db.commit()
    db.refresh(treino)
    return treino

@router.delete("/treinos/{treino_id}", summary="Deletar um treino")
def delete_treino(treino_id: int, current_user=Depends(is_admin), db: Session = Depends(get_db)):
    treino = db.query(Treino).filter(Treino.id == treino_id).first()
    if not treino:
        raise HTTPException(status_code=404, detail=f"Treino com ID {treino_id} não encontrado!")

    db.delete(treino)
    db.commit()
    return {"message": f"Treino com ID {treino_id} deletado com sucesso!"}
