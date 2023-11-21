from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from it_co_test.db.models import ProjectDB


class ProjectNotFound(Exception):
    """Raised when a project with chosen ID is not present in DB"""


async def get_all_projects(db: AsyncSession) -> list[ProjectDB]:
    stmt = select(ProjectDB)
    async with db as session:
        scalars = await session.scalars(stmt)
    return list(scalars.all())


async def patch_project(
    db: AsyncSession,
    id: UUID,
    image: str | None = None,
    description: str | None = None,
    name: str | None = None,
    link: str | None = None,
) -> ProjectDB:
    stmt = select(ProjectDB).where(ProjectDB.id == id)
    async with db as session:
        scalars = await session.scalars(stmt)
        project = scalars.first()

        if project is None:
            raise ProjectNotFound()

        if image:
            project.image = image
        if description:
            project.description = description
        if name:
            project.name = name
        if link:
            project.link = link

        session.add(project)
        await session.commit()
    return project


async def add_project(
    db: AsyncSession, image: str, description: str, name: str, link: str
) -> ProjectDB:
    async with db as session:
        project = ProjectDB(image=image, description=description, name=name, link=link)
        session.add(project)
        await session.commit()
        await session.refresh(project)
    return project


async def delete_project(db: AsyncSession, id: UUID) -> None:
    stmt = delete(ProjectDB).where(ProjectDB.id == id).returning(ProjectDB.id)
    async with db as session:
        scalars = await session.scalars(stmt)
        await session.commit()
        if scalars.first() is None:
            raise ProjectNotFound()
