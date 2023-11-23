import glob
import mimetypes
import os
from typing import Annotated
from uuid import UUID

import aiofiles
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from it_co_test.db.dal import ProjectNotFound, patch_project, register_image
from it_co_test.db.session import session

router = APIRouter()
DBDependency = Annotated[AsyncSession, Depends(session)]


async def delete_images_by_id(id: UUID) -> None:
    filenames = glob.glob(f"images/{id}*")
    for filename in filenames:
        os.remove(filename)


@router.put("/{id}")
async def put_image(
    session: DBDependency, id: UUID, file: UploadFile = File(...)
) -> None:
    if not file.filename:
        raise HTTPException(status_code=404, detail="No filename")

    _, extension = os.path.splitext(file.filename)
    target_filename = f"images/{id}{extension}"

    async with session:
        try:
            await register_image(session, id=id)
        except ProjectNotFound:
            raise HTTPException(status_code=404, detail="Project not found")

    await delete_images_by_id(id)
    async with aiofiles.open(target_filename, "wb") as out_file:
        while content := await file.read(1024):
            await out_file.write(content)


@router.delete("/{id}")
async def delete_image(session: DBDependency, id: UUID) -> None:
    await delete_images_by_id(id)
    async with session:
        try:
            await patch_project(session, id=id, image=False)
        except ProjectNotFound:
            raise HTTPException(status_code=404, detail="Project not found")


@router.get("/{id}")
async def get_image(id: UUID) -> FileResponse:
    filenames = glob.glob(f"images/{id}*")
    if not filenames:
        return FileResponse("image_placeholder.jpg", media_type="image/jpeg")
    filename = filenames[0]
    media_type, _ = mimetypes.guess_type(filename)
    return FileResponse(filename, media_type=media_type)
