from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..database import get_db
from ..schemas.summary_schema import SummaryCreate, SummaryOut
from ..security.auth import get_current_user
from ..utils.validate_admin import validate_admin
from ..crud.summary_crud import (
    create_summary,
    get_all_summaries,
    get_summary,
    delete_summary,
    get_summaries_by_notebook,
    get_summaries_by_user,
)
from ..crud.notebook_crud import get_notebook

router = APIRouter(prefix="/summaries", tags=["summaries"])


@router.post("/", response_model=SummaryOut, status_code=status.HTTP_201_CREATED)
async def create_summary_endpoint(
    summary: SummaryCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    notebook = await get_notebook(db, notebook_id=summary.notebook_id)
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook no encontrado")

    if not validate_admin(current_user) and notebook.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para crear este resumen")

    if not validate_admin(current_user) and summary.notebook_users_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para crear este resumen")

    return await create_summary(db=db, summary=summary)


@router.get("/", response_model=List[SummaryOut], status_code=status.HTTP_200_OK)
async def read_summaries(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await get_all_summaries(db, skip=skip, limit=limit)


@router.get("/{summary_id}", response_model=SummaryOut, status_code=status.HTTP_200_OK)
async def read_summary(summary_id: int, db: AsyncSession = Depends(get_db)):
    summary = await get_summary(db, summary_id=summary_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Resumen no encontrado")
    return summary


@router.delete("/{summary_id}", response_model=SummaryOut, status_code=status.HTTP_200_OK)
async def delete_summary_endpoint(
    summary_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    summary = await get_summary(db, summary_id=summary_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Resumen no encontrado")

    if not validate_admin(current_user) and summary.notebook_users_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar este resumen")

    return await delete_summary(db, summary_id=summary_id)


@router.get("/notebook/{notebook_id}", response_model=List[SummaryOut], status_code=status.HTTP_200_OK)
async def read_summaries_by_notebook(notebook_id: int, db: AsyncSession = Depends(get_db)):
    summaries = await get_summaries_by_notebook(db, notebook_id=notebook_id)
    if not summaries:
        raise HTTPException(status_code=404, detail="No se encontraron resúmenes para este notebook")
    return summaries


@router.get("/user/{user_id}", response_model=List[SummaryOut], status_code=status.HTTP_200_OK)
async def read_summaries_by_user(user_id: int, db: AsyncSession = Depends(get_db)):
    summaries = await get_summaries_by_user(db, user_id=user_id)
    if not summaries:
        raise HTTPException(status_code=404, detail="No se encontraron resúmenes para este usuario")
    return summaries
