from sqlmodel import create_engine, SQLModel
from sqlalchemy.orm import sessionmaker
from app.models import User, Treino, Dieta, FavoritosTreinos, FavoritosDietas

# Criação do engine para o banco SQLite
DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL, echo=True)

# Configuração do SessionMaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Inicialização do banco de dados
def init_db():
    # Cria as tabelas se não existirem
    SQLModel.metadata.create_all(bind=engine)

# Agora você pode chamar init_db para garantir que o banco de dados seja inicializado corretamente
init_db()
