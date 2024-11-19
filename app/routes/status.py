from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pathlib import Path

UPLOAD_DIR = Path("uploads")
PROCESSED_DIR = Path("processed")

router = APIRouter(prefix="/status", tags=["Status"])

@router.get("/{job_id}")
async def get_job_status(job_id: str):
    job_dir = UPLOAD_DIR / job_id
    processed_dir = PROCESSED_DIR / job_id

    if not job_dir.exists():
        return JSONResponse({"status": "error", "message": "Job not found"}, status_code=404)

    total_images = len(list(job_dir.glob("*")))
    processed_images = len(list(processed_dir.glob("*"))) if processed_dir.exists() else 0

    return JSONResponse({
        "status": "success",
        "job_id": job_id,
        "total_images": total_images,
        "processed_images": processed_images,
        "completed": processed_images == total_images
    })
