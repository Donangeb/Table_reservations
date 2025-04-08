from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from database import SQLALCHEMY_DATABASE_URL
from schemas.table import *
from schemas.reservation import *

router = APIRouter(
    prefix="/tables",
    tags=["tables"]
)

# API endpoints for Tables
@router.post("/", response_model=TableResponse)
def create_table(table: TableCreate, db: Session = Depends(get_db)):
    db_table = TableBase(**table.dict())
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table

@router.get("/", response_model=List[TableResponse])
def read_tables(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tables = db.query(TableBase).offset(skip).limit(limit).all()
    return tables

@router.delete("/{table_id}")
def delete_table(table_id: int, db: Session = Depends(get_db)):
    db_table = db.query(TableBase).filter(TableBase.id == table_id).first()
    if not db_table:
        raise HTTPException(status_code=404, detail="Table not found")
    
    # Check if there are reservations for this table
    reservations = db.query(ReservationBase).filter(ReservationBase.table_id == table_id).count()
    if reservations > 0:
        raise HTTPException(
            status_code=400, 
            detail="Cannot delete table with existing reservations"
        )
    
    db.delete(db_table)
    db.commit()
    return {"message": "Table deleted successfully"}