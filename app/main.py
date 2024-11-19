from fastapi import FastAPI
from app.routes.enhance import router as enhance_router
from app.routes.status import router as status_router

app = FastAPI(title="Real Estate Image Enhancement API")

app.include_router(enhance_router)
app.include_router(status_router)