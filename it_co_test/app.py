from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from it_co_test.api.routers import project, service

app = FastAPI(title="IT-CO-Test")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE", "PATCH"],
    allow_headers=["*"],
)


root_router = APIRouter()
root_router.include_router(service.router, tags=["Service"])
root_router.include_router(project.router, prefix="/project", tags=["Projects"])

app.include_router(root_router)
