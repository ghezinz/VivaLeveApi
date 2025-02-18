import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, Depends, HTTPException
from app.users_controllers import router as users_router
from app.produtos_controllers import router as produtos_router
from app.dietas_controllers import router as dietas_router
from app.treinos_controllers import router as treinos_router
from app.auth_controllers import router as auth_router
from app.models import SQLModel  # Importando o SQLModel para criar as tabelas
from app.database import init_db
from app.auth_utils import get_logged_user  # Para verificar se o usuário é admin
from app.models import User
from fastapi.middleware.cors import CORSMiddleware
from app.routes import favoritos

app = FastAPI()

# Configuração do CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://ghezinz.github.io",  # Sem o /vivaleveFRONT/ se for apenas esse domínio
    "https://ghezinz.github.io/vivaleveFRONT/",  # Com o caminho correto se necessário
    "http://127.0.0.1:5501",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Define os domínios permitidos
    allow_methods=["*"],  # Certifique-se de permitir todos os métodos
    allow_credentials=True,
    allow_headers=["Content-Type", "*"],  # Permita todos os cabeçalhos
)

# Registrando as rotas na aplicação
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])  # Inclua as rotas de autenticação
app.include_router(produtos_router, prefix="/produtos", tags=["Produtos"])
app.include_router(dietas_router, prefix="/dietas", tags=["Dietas"])
app.include_router(treinos_router, prefix="/treinos", tags=["Treinos"])
app.include_router(favoritos.router, prefix="/favoritos", tags=["Favoritos"])

@app.get("/")
def read_root():
    return {"message": "API FastAPI funcionando!"}

if __name__ == "__main__":
    init_db()


