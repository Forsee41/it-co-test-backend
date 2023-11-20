from typing import Type
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from it_co_test.db.models import ProjectDB


class ProjectNotFound(Exception):
    """Raised when a project with chosen ID is not present in DB"""


async def get_all_projects(db: Type[AsyncSession]) -> list[ProjectDB]:
    stmt = select(ProjectDB)
    async with db() as session:
        scalars = await session.scalars(stmt)
    return list(scalars.all())


async def patch_project(
    db: Type[AsyncSession],
    id: UUID,
    image: str | None = None,
    description: str | None = None,
    title: str | None = None,
) -> ProjectDB:
    stmt = select(ProjectDB).where(ProjectDB.id == id)
    async with db() as session:
        scalars = await session.scalars(stmt)
        project = scalars.first()

        if project is None:
            raise ProjectNotFound()

        if image:
            project.image = image
        if description:
            project.description = description
        if title:
            project.title = title

        session.add(project)
        await session.commit()
    return project


async def add_project(
    db: Type[AsyncSession], image: str, description: str, title: str
) -> ProjectDB:
    async with db() as session:
        project = ProjectDB(image=image, description=description, title=title)
        session.add(project)
        await session.commit()
        await session.refresh(project)
    return project


async def delete_project(db: Type[AsyncSession], id: UUID):
    stmt = delete(ProjectDB).where(ProjectDB.id == id).returning(ProjectDB.id)
    async with db() as session:
        scalars = await session.scalars(stmt)
        if scalars.first() is not None:
            raise ProjectNotFound()
