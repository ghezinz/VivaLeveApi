from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.auth_utils import get_logged_user
from app.database import get_db
from app.models import User, Treino, Dieta, FavoritosTreinos, FavoritosDietas

router = APIRouter()

# Adicionar treino aos favoritos
@router.post("/favoritos/treinos/{treino_id}")
def add_favorito_treino(treino_id: int, user: User = Depends(get_logged_user), db: Session = Depends(get_db)):
    sttm = select(FavoritosTreinos).where(FavoritosTreinos.user_id == user.id, FavoritosTreinos.treino_id == treino_id)
    if db.execute(sttm).first():
        raise HTTPException(status_code=400, detail="Treino já está nos favoritos")
    
    favorito = FavoritosTreinos(user_id=user.id, treino_id=treino_id)
    db.add(favorito)
    db.commit()
    return {"message": "Treino adicionado aos favoritos com sucesso!"}

# Adicionar dieta aos favoritos
@router.post("/favoritos/dietas/{dieta_id}")
def add_favorito_dieta(dieta_id: int, user: User = Depends(get_logged_user), db: Session = Depends(get_db)):
    sttm = select(FavoritosDietas).where(FavoritosDietas.user_id == user.id, FavoritosDietas.dieta_id == dieta_id)
    if db.execute(sttm).first():
        raise HTTPException(status_code=400, detail="Dieta já está nos favoritos")
    
    favorito = FavoritosDietas(user_id=user.id, dieta_id=dieta_id)
    db.add(favorito)
    db.commit()
    return {"message": "Dieta adicionada aos favoritos com sucesso!"}

# Listar treinos favoritos
@router.get("/favoritos/treinos", response_model=List[Treino])
def list_favoritos_treinos(user: User = Depends(get_logged_user), db: Session = Depends(get_db)):
    sttm = select(Treino).join(FavoritosTreinos).where(FavoritosTreinos.user_id == user.id)
    return db.execute(sttm).scalars().all()

# Listar dietas favoritas
@router.get("/favoritos/dietas", response_model=List[Dieta])
def list_favoritos_dietas(user: User = Depends(get_logged_user), db: Session = Depends(get_db)):
    sttm = select(Dieta).join(FavoritosDietas).where(FavoritosDietas.user_id == user.id)
    return db.execute(sttm).scalars().all()

# Remover treino dos favoritos
@router.delete("/favoritos/treinos/{treino_id}")
def remove_favorito_treino(treino_id: int, user: User = Depends(get_logged_user), db: Session = Depends(get_db)):
    sttm = select(FavoritosTreinos).where(FavoritosTreinos.user_id == user.id, FavoritosTreinos.treino_id == treino_id)
    favorito = db.execute(sttm).scalars().first()
    if not favorito:
        raise HTTPException(status_code=404, detail="Treino não está nos favoritos")
    
    db.delete(favorito)
    db.commit()
    return {"message": "Treino removido dos favoritos com sucesso!"}

# Remover dieta dos favoritos
@router.delete("/favoritos/dietas/{dieta_id}")
def remove_favorito_dieta(dieta_id: int, user: User = Depends(get_logged_user), db: Session = Depends(get_db)):
    sttm = select(FavoritosDietas).where(FavoritosDietas.user_id == user.id, FavoritosDietas.dieta_id == dieta_id)
    favorito = db.execute(sttm).scalars().first()
    if not favorito:
        raise HTTPException(status_code=404, detail="Dieta não está nos favoritos")
    
    db.delete(favorito)
    db.commit()
    return {"message": "Dieta removida dos favoritos com sucesso!"}
