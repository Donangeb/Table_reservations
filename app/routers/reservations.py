from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from services.reservation_service import (
    ReservationService,
    ReservationNotFoundError,
    ReservationConflictError,
    TableNotFoundError
)
from services.table_service import TableNotFoundError
from schemas.reservation import (
    ReservationBase as ReservationSchema,
    ReservationCreate,
    ReservationCheck
)
from database import get_db

router = APIRouter()

@router.get("/", response_model=List[ReservationSchema])
def get_reservations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return ReservationService.get_reservations(db, skip=skip, limit=limit)

@router.post("/", response_model=ReservationSchema, status_code=status.HTTP_201_CREATED)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    try:
        return ReservationService.create_reservation(db, reservation)
    except TableNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Table not found"
        )
    except ReservationConflictError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )

@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    try:
        ReservationService.delete_reservation(db, reservation_id)
    except ReservationNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found"
        )

@router.post("/check-availability", status_code=status.HTTP_200_OK)
def check_availability(check: ReservationCheck, db: Session = Depends(get_db)):
    try:
        is_available = ReservationService.check_table_availability(
            db,
            table_id=check.table_id,
            start_time=check.reservation_time,
            duration_minutes=check.duration_minutes
        )
        return {"available": is_available}
    except TableNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Table not found"
        )