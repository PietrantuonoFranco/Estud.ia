from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from ..utils.validate_email import validate_email
from ..database import get_db

from ..security.auth import authenticate_user, get_current_user
from ..security.token import create_access_token
from ..security.oauth_config import oauth

from ..schemas.user_schema import UserCreate

from ..crud.user_crud import get_user_by_email, create_user, create_user_from_google

from ..config import conf

# Creamos el router para agrupar estas rutas
router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.get("/me", status_code=status.HTTP_200_OK)
async def get_me(current_user=Depends(get_current_user)):
    return current_user

@router.post("/login", status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    if not validate_email(form_data.username):
        raise HTTPException(
            status_code=400, 
            detail="El formato del correo electrónico no es válido"
        )
    
    formatted_email = form_data.username.strip().lower()
    form_data.username = formatted_email
    
    user = await authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(status_code=400, detail="Correo o contraseña incorrectos")
    
    accessToken = create_access_token(data={"sub": user.email})
    
    # Crear respuesta con cookie
    response = JSONResponse(
        content={"message": "Login exitoso", "token_type": "bearer"}
    )
    
    # Setear cookie con opciones de seguridad
    response.set_cookie(
        key="accessToken",
        value=accessToken,
        httponly=True,          # No accesible desde JavaScript
        secure=True,            # False en desarrollo, True en producción con HTTPS
        samesite="none",        # Permite enviar la cookie entre Vercel y Render
        max_age=60*conf.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    
    return response

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(form_data: UserCreate, db: AsyncSession = Depends(get_db)):
    if not validate_email(form_data.email):
        raise HTTPException(
            status_code=400, 
            detail="El formato del correo electrónico no es válido"
        )
    
    formatted_email = form_data.email.strip().lower()

    existing_user = await get_user_by_email(db, formatted_email)

    if existing_user:
        raise HTTPException(
            status_code=400, 
            detail="El correo electrónico ya está registrado"
        )
    
    form_data.email = formatted_email
    form_data.name = form_data.name.title()
    form_data.lastname = form_data.lastname.title()

    new_user = await create_user(db, form_data)
    accessToken = create_access_token(data={"sub": new_user.email})
    
    response = JSONResponse(
        content={"message": "Registro exitoso", "token_type": "bearer"},
        status_code=status.HTTP_201_CREATED
    )
    
    response.set_cookie(
        key="accessToken",
        value=accessToken,
        httponly=True,
        secure=True,         # False en desarrollo, True en producción con HTTPS
        samesite="none",     # Permite enviar la cookie entre Vercel y Render
        max_age=60*conf.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    
    return response

@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout():
    response = JSONResponse(content={"message": "Logout exitoso"})
    response.delete_cookie(key="accessToken")
    
    return response

# --- Rutas de Google ---

@router.get("/login/google")
async def login_google(request: Request):
    # Redirige al usuario a Google
    redirect_uri = request.url_for('auth_google_callback')
    return await oauth.google.authorize_redirect(request, str(redirect_uri))

@router.get("/callback/google")
async def auth_google_callback(request: Request, db: AsyncSession = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get('userinfo')
    
    if not user_info:
        raise HTTPException(status_code=400, detail="No se pudo obtener info de Google")

    # 1. Buscar si el usuario ya existe en tu DB
    user = await get_user_by_email(db, user_info['email'])
    
    # 2. Si no existe, lo creamos (Registro automático)
    if not user:
        # Aquí puedes adaptar tu UserCreate o crear una lógica específica
        # para usuarios que vienen de Google (sin password convencional)
        user = await create_user_from_google(db, user_info)

    # 3. Generar tu propio JWT (el que ya usas en /login)
    accessToken = create_access_token(data={"sub": user.email})

    # 4. Responder con la misma Cookie que ya implementaste
    response = RedirectResponse(url=conf.FRONTEND_URL)  # Redirige al frontend después del login
    response.set_cookie(
        key="accessToken",
        value=accessToken,
        httponly=True,
        secure=True,            # False en desarrollo, True en producción con HTTPS
        samesite="none",        # Permite enviar la cookie entre Vercel y Render
        max_age=60*conf.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return response