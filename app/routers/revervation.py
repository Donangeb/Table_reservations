from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from typing import List
from pydantic import BaseModel
from database import SQLALCHEMY_DATABASE_URL
from schemas.table import *
from schemas.reservation import *

app = FastAPI()

# Database setup
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# API endpoints for Tables
@app.post("/tables/", response_model=TableResponse)
def create_table(table: TableCreate, db: Session = Depends(get_db)):
    db_table = TableBase(**table.dict())
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table

@app.get("/tables/", response_model=List[TableResponse])
def read_tables(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tables = db.query(TableBase).offset(skip).limit(limit).all()
    return tables

@app.delete("/tables/{table_id}")
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

# API endpoints for Reservations
@app.post("/reservations/", response_model=ReservationResponse)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    # Check if table exists
    table = db.query(TableBase).filter(TableBase.id == reservation.table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    
    db_reservation = ReservationBase(**reservation.dict())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

@app.get("/reservations/", response_model=List[ReservationResponse])
def read_reservations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reservations = db.query(ReservationBase).offset(skip).limit(limit).all()
    return reservations

@app.delete("/reservations/{reservation_id}")
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    db_reservation = db.query(ReservationBase).filter(ReservationBase.id == reservation_id).first()
    if not db_reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    db.delete(db_reservation)
    db.commit()
    return {"message": "Reservation deleted successfully"}