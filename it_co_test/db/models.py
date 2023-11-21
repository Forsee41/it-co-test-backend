from typing import Type
from uuid import UUID, uuid4

from sqlalchemy import UUID as UUID_DB
from sqlalchemy import String
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

Base: Type = declarative_base()


class ProjectDB(Base):
    __tablename__ = "project"

    id: Mapped[UUID] = mapped_column(
        UUID_DB(as_uuid=True), primary_key=True, default=uuid4
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    image: Mapped[str] = mapped_column(String, nullable=False)
    link: Mapped[str] = mapped_column(String, nullable=False)
