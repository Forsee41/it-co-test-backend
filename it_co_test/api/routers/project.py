from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from it_co_test.api.schemas import ProjectPost, ProjectPostResponse, ProjectResponse
from it_co_test.db.dal import (
    ProjectNotFound,
    add_project,
    delete_project,
    get_all_projects,
    patch_project,
)
from it_co_test.db.session import session

router = APIRouter()
DBDependency = Annotated[AsyncSession, Depends(session)]


@router.get("/")
async def get_projects(session: DBDependency) -> list[ProjectResponse]:
    async with session:
        projects = await get_all_projects(session)
        result = [ProjectResponse(**project.__dict__) for project in projects]
    return result


@router.post("/")
async def add_new_project(
    session: DBDependency, project: ProjectPost
) -> ProjectPostResponse:
    async with session:
        added_project = await add_project(session, **project.__dict__)
    return ProjectPostResponse(id=added_project.id)


@router.delete("/{id}", status_code=204)
async def delete_project_by_id(session: DBDependency, id: UUID) -> None:
    async with session:
        try:
            await delete_project(session, id=id)
        except ProjectNotFound:
            raise HTTPException(status_code=404, detail="Project not found")


@router.put("/{id}")
async def change_project(session: DBDependency, id: UUID, project: ProjectPost) -> None:
    async with session:
        try:
            await patch_project(session, id=id, **project.__dict__)
        except ProjectNotFound:
            raise HTTPException(status_code=404, detail="Project not found")
