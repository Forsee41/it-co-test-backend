from contextlib import asynccontextmanager

import pytest

from it_co_test.db.dal import add_project, get_all_projects
from it_co_test.db.session import session


async def test_add_project() -> None:
    project = {"image": "image", "description": "description", "name": "name"}
    db = asynccontextmanager(session)
    async with db() as sess:
        assert sess
        await add_project(sess, **project)
        projects = await get_all_projects(sess)
        assert projects
        result = projects[0]
        assert result.image == project["image"]
        assert result.name == project["name"]
        assert result.description == project["description"]


if __name__ == "__main__":
    pytest.main()
