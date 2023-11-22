from contextlib import asynccontextmanager

import pytest

from it_co_test.db.dal import (
    add_project,
    delete_project,
    get_all_projects,
    patch_project,
)
from it_co_test.db.session import session


async def test_add_project() -> None:
    project = {"image": False, "description": "description", "name": "name"}
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
    project1 = {"image": False, "description": "description1", "name": "name1"}
    project2 = {"image": False, "description": "description2", "name": "name2"}
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
    project1 = {"image": False, "description": "description1", "name": "name1"}
    project2 = {"image": False, "description": "description2", "name": "name2"}
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


async def test_patch_all_fields() -> None:
    project1 = {"image": False, "description": "description1", "name": "name1"}
    project1_changed = {
        "image": False,
        "description": "description3",
        "name": "name3",
    }
    project2 = {"image": False, "description": "description2", "name": "name2"}
    db = asynccontextmanager(session)
    async with db() as sess:
        assert sess
        added1 = await add_project(sess, **project1)
        await add_project(sess, **project2)
        patch_returned = await patch_project(sess, id=added1.id, **project1_changed)
        queried = await get_all_projects(sess)
        patched = queried[0] if queried[0].id == added1.id else queried[1]
        non_patched = queried[0] if patched == queried[1] else queried[1]
        assert patch_returned.image == patched.image
        assert patch_returned.name == patched.name
        assert patch_returned.description == patched.description
        assert patch_returned.image == project1_changed["image"]
        assert patch_returned.name == project1_changed["name"]
        assert patch_returned.description == project1_changed["description"]
        assert non_patched.name == project2["name"]


async def test_patch_single_field() -> None:
    project = {"image": False, "description": "description1", "name": "name1"}
    db = asynccontextmanager(session)
    async with db() as sess:
        assert sess
        added = await add_project(sess, **project)
        patch_returned = await patch_project(sess, id=added.id, name="new_name")
        projects = await get_all_projects(sess)
        assert projects
        patched = projects[0]
        assert patch_returned.name == "new_name"
        assert patched.name == "new_name"
        assert patch_returned.image == project["image"]
        assert patched.image == project["image"]


if __name__ == "__main__":
    pytest.main()
