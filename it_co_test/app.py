from fastapi import APIRouter, FastAPI

from it_co_test.api.routers import service

root_router = APIRouter()
root_router.include_router(service.router, tags=["Service"])

app = FastAPI(title="IT-CO-Test")
app.include_router(root_router)
