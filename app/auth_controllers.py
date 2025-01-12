from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import SignInUserRequest, User
from app.database import get_db
from app.auth_utils import verify_hash, generate_token, get_logged_user

router = APIRouter()

@router.get("/verificar-token", summary="Verificar validade do token")
def verificar_token(current_user: User = Depends(get_logged_user)):
    # Se o token for válido, o `current_user` será retornado
    return {"message": "Token válido", "user": current_user}


@router.post("/login")
def login(request: SignInUserRequest, db: Session = Depends(get_db)):
    # Extrai os dados do modelo LoginRequest
    username = request.username
    senha = request.senha

    # Busca o usuário no banco de dados
    usuario = db.query(User).filter(User.username == username).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado!")

    # Verifica se a senha está correta
    if not verify_hash(senha, usuario.password):
        raise HTTPException(status_code=401, detail="Senha incorreta!")

    # Gera um token de acesso, incluindo o tipo de usuário (admin ou não)
    payload = {
        "sub": usuario.username,
        "is_admin": usuario.is_admin  # Inclui se o usuário é admin no token
    }
    token = generate_token(payload, token_type="access")

    return {"access_token": token, "token_type": "bearer"}
