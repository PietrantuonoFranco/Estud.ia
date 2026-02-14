from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..models.role_model import Role


async def get_role_by_name(db: AsyncSession, name: str):
    query = select(Role).filter(Role.name == name)
    result = await db.execute(query)
    return result.scalars().first()


async def get_or_create_role(db: AsyncSession, name: str):
    role = await get_role_by_name(db, name)
    if role:
        return role

    role = Role(name=name)
    db.add(role)
    await db.commit()
    await db.refresh(role)
    return role
