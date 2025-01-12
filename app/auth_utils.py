from datetime import datetime, timedelta
from typing import Annotated, Literal
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlmodel import Session, select
from app.database import get_db
from app.models import User

# Constantes de configuração de segurança
SECRET_KEY = '02a7e6efa2d0f77fc89f1f44d73acd7bf26e5dc6f3c1f939ff5d038ea3604f23'
ALGORITHM = 'HS256'
ACCESS_EXPIRES_MINUTES = 10  # 10 minutos
REFRESH_EXPIRES_MINUTES = 60 * 24 * 3  # 3 dias

# Instância do OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='signin')

# Instância do contexto de hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para pegar o usuário logado, usando o token JWT
async def get_logged_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    unauthorized_exception = HTTPException(status_code=401, detail='Não autorizado!')

    try:
        username = decode_token(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado!")
    except jwt.InvalidTokenError:
        raise unauthorized_exception

    if not username:
        raise unauthorized_exception

    # Buscar o usuário no banco de dados
    sttm = select(User).where(User.username == username)
    result = db.execute(sttm)
    user = result.scalars().first()

    if not user:
        raise unauthorized_exception

    return user

# Função para verificar se o usuário logado é um administrador
def is_admin(current_user: Annotated[User, Depends(get_logged_user)]):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Apenas administradores podem acessar esta rota!")
    return current_user

# Função para gerar um hash da senha
def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)

# Função para verificar se o hash da senha corresponde ao fornecido
def verify_hash(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Função para gerar o JWT Token
def generate_token(sub: str, token_type: Literal['access', 'refresh']) -> str:
    if token_type == 'refresh':
        expires = datetime.utcnow() + timedelta(minutes=REFRESH_EXPIRES_MINUTES)
    else:
        expires = datetime.utcnow() + timedelta(minutes=ACCESS_EXPIRES_MINUTES)

    token = jwt.encode({'sub': sub, 'exp': expires}, key=SECRET_KEY, algorithm=ALGORITHM)
    return token

# Função para decodificar o JWT Token
def decode_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get('sub')
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado!")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido!")
