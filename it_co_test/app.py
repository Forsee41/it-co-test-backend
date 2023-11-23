import os

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from it_co_test.api.routers import images, project, service

if not os.path.isdir("images"):
    os.mkdir("images")

app = FastAPI(title="IT-CO-Test")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE", "PUT"],
    allow_headers=["*"],
)


root_router = APIRouter(prefix="/api")
root_router.include_router(service.router, tags=["Service"])
root_router.include_router(project.router, prefix="/project", tags=["Projects"])
root_router.include_router(images.router, prefix="/image", tags=["Images"])

app.include_router(root_router)
