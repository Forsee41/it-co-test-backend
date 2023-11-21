from fastapi import APIRouter, FastAPI

from it_co_test.api.routers import project, service

root_router = APIRouter()
root_router.include_router(service.router, tags=["Service"])
root_router.include_router(project.router, tags=["Projects"])

app = FastAPI(title="IT-CO-Test")
app.include_router(root_router)
