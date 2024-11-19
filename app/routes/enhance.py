from fastapi import APIRouter, BackgroundTasks, UploadFile, File
from fastapi.responses import JSONResponse
from pathlib import Path
import uuid
from typing import List
from app.models.image_enhancer import ImageEnhancer

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
PROCESSED_DIR = Path("processed")
PROCESSED_DIR.mkdir(exist_ok=True)

router = APIRouter(prefix="/enhance", tags=["Enhance"])

enhancer = ImageEnhancer()

@router.post("/")
async def enhance_images(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...)
):
    job_id = str(uuid.uuid4())
    job_dir = UPLOAD_DIR / job_id
    job_dir.mkdir(exist_ok=True)

    saved_paths = []
    for file in files:
        file_path = job_dir / file.filename
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        saved_paths.append(file_path)

    background_tasks.add_task(process_images_batch, saved_paths, job_id)
    return JSONResponse({"status": "success", "job_id": job_id})

async def process_images_batch(image_paths: List[Path], job_id: str):
    output_dir = PROCESSED_DIR / job_id
    output_dir.mkdir(exist_ok=True)
    for path in image_paths:
        await enhancer.process_image(path, output_dir)
