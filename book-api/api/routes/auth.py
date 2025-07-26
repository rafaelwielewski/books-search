from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from api.core.auth import create_access_token, get_current_user
from api.core.models.auth import TokenResponse, TokenData

router = APIRouter()

FAKE_USER = {
    "username": "admin",
    "password": "admin123"
}

@router.post("/login", summary="Gera um token de acesso", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Realiza a autenticação do usuário e gera um token de acesso."""
    if form_data.username != FAKE_USER["username"] or form_data.password != FAKE_USER["password"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(data={"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/refresh", summary="Renova o token de acesso", response_model=TokenResponse)
def refresh_token(current_user: TokenData = Depends(get_current_user)):
    """Renova o token de acesso para o usuário autenticado."""
    token = create_access_token(data={"sub": current_user.username})
    return {"access_token": token, "token_type": "bearer"}