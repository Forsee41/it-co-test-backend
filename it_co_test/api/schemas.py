from uuid import UUID

from pydantic import BaseModel


class Model(BaseModel):
    class Config:
        orm_mode = True


class ProjectResponse(Model):
    id: UUID
    name: str
    description: str
    image: str
    link: str


class ProjectPost(Model):
    name: str
    description: str
    image: str
    link: str


class ProjectPostResponse(Model):
    id: UUID
