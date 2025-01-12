from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.auth_utils import generate_token, get_logged_user, hash_password, verify_hash, is_admin
from app.database import get_db
from app.models import BaseUser, SignInUserRequest, SignUpUserRequest, User

router = APIRouter()

@router.post('/signup', response_model=BaseUser)
def signup(user_data: SignUpUserRequest, db: Session = Depends(get_db)):
    # Check if username already exists
    sttm = select(User).where(User.username == user_data.username)
    result = db.execute(sttm)
    user = result.scalars().first()

    if user:
        raise HTTPException(status_code=400, detail='Já existe um usuário com esse username')

    if user_data.password != user_data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Senhas não coincidem!'
        )

    # Hash the password
    hashed_password = hash_password(user_data.password)

    user = User(
        email=user_data.email,
        name=user_data.name,
        username=user_data.username,
        password=hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post('/signin')
def signin(signin_data: SignInUserRequest, db: Session = Depends(get_db)):
    exception_wrong_user_password = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Usuário e/ou senha incorreto(S)'
    )

    # Get user by username
    sttm = select(User).where(User.username == signin_data.username)
    result = db.execute(sttm)
    user = result.scalars().first()

    if not user:  # User not found
        raise exception_wrong_user_password

    if not verify_hash(signin_data.password, user.password):  # Incorrect password
        raise exception_wrong_user_password

    # Generate JWT tokens
    access_token = generate_token(user.username, 'access')
    refresh_token = generate_token(user.username, 'refresh')

    return {'access_token': access_token, 'refresh_token': refresh_token}

@router.get('/me', response_model=User)
def me(user: Annotated[User, Depends(get_logged_user)]):
    return user

# Route to list all users, only for administrators
@router.get('/users', response_model=list[BaseUser])
def list_users(current_user: Annotated[User, Depends(is_admin)], db: Session = Depends(get_db)):
    result = db.execute(select(User))
    users = result.scalars().all()
    return users

# Route to update a user, only for administrators
@router.put('/users/{user_id}', response_model=BaseUser)
def update_user(user_id: int, user_data: SignUpUserRequest, current_user: Annotated[User, Depends(is_admin)], db: Session = Depends(get_db)):
    sttm = select(User).where(User.id == user_id)
    result = db.execute(sttm)
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado!")

    # Update user information
    user.name = user_data.name
    user.email = user_data.email
    if user_data.password:
        user.password = hash_password(user_data.password)

    db.commit()
    db.refresh(user)
    return user

# Route to delete a user, only for administrators
@router.delete('/users/{user_id}', response_model=dict)
def delete_user(user_id: int, current_user: Annotated[User, Depends(is_admin)], db: Session = Depends(get_db)):
    sttm = select(User).where(User.id == user_id)
    result = db.execute(sttm)
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado!")

    if user.is_admin:
        raise HTTPException(status_code=403, detail="Não é permitido deletar um administrador!")

    db.delete(user)
    db.commit()

    return {"message": f"Usuário {user_id} deletado com sucesso!"}

