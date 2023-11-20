from contextlib import asynccontextmanager

import pytest

from it_co_test.db.dal import add_project, delete_project, get_all_projects
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


async def test_add_multiple_projects() -> None:
    project1 = {"image": "image1", "description": "description1", "name": "name1"}
    project2 = {"image": "image2", "description": "description2", "name": "name2"}
    db = asynccontextmanager(session)
    async with db() as sess:
        assert sess
        await add_project(sess, **project1)
        await add_project(sess, **project2)
        projects = await get_all_projects(sess)
        assert projects
        assert len(projects) == 2
        result1 = projects[0]
        assert result1.image == project1["image"]
        assert result1.name == project1["name"]
        assert result1.description == project1["description"]
        result2 = projects[1]
        assert result2.image == project2["image"]
        assert result2.name == project2["name"]
        assert result2.description == project2["description"]


async def test_delete_project() -> None:
    project1 = {"image": "image1", "description": "description1", "name": "name1"}
    project2 = {"image": "image2", "description": "description2", "name": "name2"}
    db = asynccontextmanager(session)
    async with db() as sess:
        assert sess
        added1 = await add_project(sess, **project1)
        await add_project(sess, **project2)
        await delete_project(sess, added1.id)
        projects = await get_all_projects(sess)
        assert projects
        assert len(projects) == 1
        remaining = projects[0]
        assert remaining.name == project2["name"]


if __name__ == "__main__":
    pytest.main()
