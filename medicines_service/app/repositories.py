from sqlalchemy.orm import Session
from .models import Medicine  # ← ДОБАВИЛ
from .schemas import DBMedicine
from datetime import datetime

class MedicineRepo:
    def __init__(self, db: Session):
        self.db = db

    def create(self, med: Medicine):
        data = med.model_dump(exclude={"medicine_id", "updated_at"})
        db_med = DBMedicine(**data)
        self.db.add(db_med)
        self.db.commit()
        self.db.refresh(db_med)
        return Medicine.model_validate(db_med.__dict__)

    def get_by_id(self, med_id: str):
        return self.db.query(DBMedicine).filter(DBMedicine.medicine_id == med_id).first()

    def list_all(self, skip: int, limit: int):
        return self.db.query(DBMedicine).offset(skip).limit(limit).all()

    def update(self, med_id: str, update_data: Medicine):
        db_med = self.get_by_id(med_id)
        if not db_med:
            return None
        update_dict = update_data.dict(exclude_unset=True, exclude={"medicine_id"})
        for key, value in update_dict.items():
            setattr(db_med, key, value)
        db_med.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_med)
        return Medicine.from_orm(db_med)

    def delete(self, med_id: str):
        db_med = self.get_by_id(med_id)
        if not db_med:
            return False
        self.db.delete(db_med)
        self.db.commit()
        return True