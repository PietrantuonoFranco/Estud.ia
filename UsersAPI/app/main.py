from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

# Database configuration
from .database import SessionLocal

# Schemas
from .schemas.user_schema import UserCreate, UserOut

# Modelos
from .models import User, Notebook, Source

# Routers
from .routers.user_router import router as users_router

app = FastAPI()

app.include_router(users_router)

# Dependencia para obtener la sesión de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        email=user.email,
        name=user.name,
        lastname=user.lastname,
        password=user.password,
        profile_image_url=user.profile_image_url,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user