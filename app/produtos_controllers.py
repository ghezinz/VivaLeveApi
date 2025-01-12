from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Produto, ProdutoRequest
from app.auth_utils import is_admin

router = APIRouter()

@router.get("/produtos", summary="Listar todos os produtos")
def get_produtos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    produtos = db.query(Produto).offset(skip).limit(limit).all()
    return produtos

@router.post("/produtos", summary="Adicionar um novo produto")
def create_produto(
    produto_data: ProdutoRequest,  # Modificado para receber o ProdutoRequest
    current_user=Depends(is_admin), 
    db: Session = Depends(get_db)
):
    # Criação do produto com os dados recebidos
    novo_produto = Produto(**produto_data.dict())
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto

@router.put("/produtos/{produto_id}", summary="Atualizar um produto")
def update_produto(
    produto_id: int, 
    produto_data: ProdutoRequest,  # Modificado para receber o ProdutoRequest
    current_user=Depends(is_admin), 
    db: Session = Depends(get_db)
):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado!")

    # Atualização dos dados do produto
    if produto_data.nome:
        produto.nome = produto_data.nome
    if produto_data.preco is not None:  # Verificação de preco
        produto.preco = produto_data.preco
    if produto_data.descricao:
        produto.descricao = produto_data.descricao

    db.commit()
    db.refresh(produto)
    return produto

@router.delete("/produtos/{produto_id}", summary="Deletar um produto")
def delete_produto(produto_id: int, current_user=Depends(is_admin), db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado!")

    db.delete(produto)
    db.commit()
    return {"message": f"Produto {produto_id} deletado com sucesso!"}
