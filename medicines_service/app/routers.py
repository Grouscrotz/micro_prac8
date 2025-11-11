from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .models import Medicine
from .repositories import MedicineRepo
from .rabbitmq import publish
import httpx

router = APIRouter(prefix="/api/medicines", tags=["Medicines"])

@router.post("/")
async def add(med: Medicine, db: Session = Depends(get_db)):
    repo = MedicineRepo(db)
    new_med = repo.create(med)
    await publish(new_med.medicine_id)
    return {"medicine_id": str(new_med.medicine_id), "message": "Добавлено"}

@router.get("/{med_id}")
def get(med_id: str, db: Session = Depends(get_db)):
    repo = MedicineRepo(db)
    med = repo.get_by_id(med_id)
    if not med:
        raise HTTPException(404, "Не найдено")
    return med

@router.get("/")
def list_meds(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    repo = MedicineRepo(db)
    return repo.list_all(skip, limit)

@router.put("/{med_id}")
def update(med_id: str, update_data: Medicine, db: Session = Depends(get_db)):
    repo = MedicineRepo(db)
    med = repo.update(med_id, update_data)
    if not med:
        raise HTTPException(404)
    return med

@router.delete("/{med_id}")
def delete(med_id: str, db: Session = Depends(get_db)):
    repo = MedicineRepo(db)
    success = repo.delete(med_id)
    if not success:
        raise HTTPException(404)
    return {"message": "Удалено"}