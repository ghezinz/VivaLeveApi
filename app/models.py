from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlmodel import Relationship, SQLModel, Field
from pydantic import BaseModel
from typing import List
from datetime import datetime

# Classes Base
class BaseUser(SQLModel):
    name: str
    email: str
    username: str

class AdminBase(SQLModel):
    name: str
    email: str
    username: str
    is_admin: bool = True

class ProdutosBase(SQLModel):
    nome: str
    descricao: str
    preco: float
    url: str

class DietasBase(SQLModel):
    nome: str
    tipo: str
    descricao: str
    consumo_caloria: float

class TreinosBase(SQLModel):
    nome: str
    tipo: str
    descricao: str
    duracao: int

class FavoritosTreinos(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    treino_id: int = Field(foreign_key="treino.id", primary_key=True)
    user: "User" = Relationship(back_populates="favoritos_treinos")
    treino: "Treino" = Relationship(back_populates="favoritado_por")

class FavoritosDietas(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    dieta_id: int = Field(foreign_key="dieta.id", primary_key=True)
    user: "User" = Relationship(back_populates="favoritos_dietas")
    dieta: "Dieta" = Relationship(back_populates="favoritado_por")


# Modelos de Tabelas
class Administrador(AdminBase, table=True):
    id: int = Field(default=None, primary_key=True)
    password: str
    # Aqui podemos adicionar mais campos exclusivos para administradores se necessário
    
class User(BaseUser, table=True):
    id: int = Field(default=None, primary_key=True)
    password: str
    is_admin: bool = Field(default=False) 
    favoritos_treinos: List["FavoritosTreinos"] = Relationship(back_populates="user")
    favoritos_dietas: List["FavoritosDietas"] = Relationship(back_populates="user")

class Produto(ProdutosBase, table=True):
    id: int = Field(default=None, primary_key=True)
    nome: str
    descricao: str
    preco: float

class Treino(TreinosBase, table=True):
    id: int = Field(default=None, primary_key=True)
    tipo: str
    favoritado_por: List["FavoritosTreinos"] = Relationship(back_populates="treino")

class Dieta(DietasBase, table=True):
    id: int = Field(default=None, primary_key=True)
    favoritado_por: List["FavoritosDietas"] = Relationship(back_populates="dieta")

# Pydantic Models para Requisições
class SignUpUserRequest(BaseModel):
    name: str
    email: str
    username: str
    password: str
    confirm_password: str

class SignInUserRequest(BaseModel):
    username: str
    password: str

class TreinoRequest(BaseModel):
    nome: str
    tipo: str
    descricao: str
    duracao: str

class ProdutoRequest(BaseModel):
    nome: str
    preco: float
    descricao: str
    url: str

class DietaRequest(BaseModel):
    nome: str
    tipo: str
    descricao: str
    consumo_caloria: float
