from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Dieta, DietaRequest
from app.auth_utils import is_admin

router = APIRouter()

@router.get("/dietas", summary="Listar todas as dietas")
def get_dietas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    dietas = db.query(Dieta).offset(skip).limit(limit).all()
    return dietas

@router.post("/dietas", summary="Adicionar uma nova dieta")
def create_dieta(
    dieta_data: DietaRequest,  # Modificado para receber DietaRequest
    current_user=Depends(is_admin), 
    db: Session = Depends(get_db)
):
    nova_dieta = Dieta(**dieta_data.dict())  # Criação da dieta com os dados recebidos
    db.add(nova_dieta)
    db.commit()
    db.refresh(nova_dieta)
    return nova_dieta

@router.put("/dietas/{dieta_id}", summary="Atualizar uma dieta")
def update_dieta(
    dieta_id: int, 
    dieta_data: DietaRequest,  # Modificado para receber DietaRequest
    current_user=Depends(is_admin), 
    db: Session = Depends(get_db)
):
    dieta = db.query(Dieta).filter(Dieta.id == dieta_id).first()
    if not dieta:
        raise HTTPException(status_code=404, detail="Dieta não encontrada!")

    # Atualização dos dados da dieta
    if dieta_data.tipo:
        dieta.tipo = dieta_data.tipo
    if dieta_data.descricao:
        dieta.descricao = dieta_data.descricao
    if dieta_data.consumo_caloria is not None:
        dieta.consumo_caloria = dieta_data.consumo_caloria

    db.commit()
    db.refresh(dieta)
    return dieta

@router.delete("/dietas/{dieta_id}", summary="Deletar uma dieta")
def delete_dieta(dieta_id: int, current_user=Depends(is_admin), db: Session = Depends(get_db)):
    dieta = db.query(Dieta).filter(Dieta.id == dieta_id).first()
    if not dieta:
        raise HTTPException(status_code=404, detail="Dieta não encontrada!")

    db.delete(dieta)
    db.commit()
    return {"message": f"Dieta {dieta_id} deletada com sucesso!"}
