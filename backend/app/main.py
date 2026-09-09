from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import settings
from .database import Base, engine
from .routers import auth, content, projects, skills, upload
from .routers.upload import UPLOAD_DIR

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Portfolio API")

origins = [origin.strip() for origin in settings.origins.split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(content.router)
app.include_router(skills.router)
app.include_router(upload.router)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
