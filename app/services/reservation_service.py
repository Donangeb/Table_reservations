from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.models import Reservation
from app.models.models import Table
from app.schemas.reservation import ReservationCreate
from app.services.exceptions import (
    ReservationConflictError,
    ReservationNotFoundError,
    TableNotFoundError
)

class ReservationService:
    @staticmethod
    def get_reservation(db: Session, reservation_id: int) -> Reservation:
        reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
        if not reservation:
            raise ReservationNotFoundError()
        return reservation

    @staticmethod
    def get_reservations(db: Session, skip: int = 0, limit: int = 100) -> list[Reservation]:
        return db.query(Reservation).offset(skip).limit(limit).all()

    @staticmethod
    def create_reservation(db: Session, reservation: ReservationCreate) -> Reservation:
        # Проверяем существование столика
        table = db.query(Table).filter(Table.id == reservation.table_id).first()
        if not table:
            raise TableNotFoundError()

        # Проверяем доступность столика
        reservation_end = reservation.reservation_time + timedelta(minutes=reservation.duration_minutes)
        
        conflicting_reservations = db.query(Reservation).filter(
            Reservation.table_id == reservation.table_id,
            Reservation.reservation_time < reservation_end,
            Reservation.reservation_time + timedelta(minutes=Reservation.duration_minutes) > reservation.reservation_time
        ).count()

        if conflicting_reservations > 0:
            raise ReservationConflictError("Столик уже занят в указанное время")

        db_reservation = Reservation(
            customer_name=reservation.customer_name,
            table_id=reservation.table_id,
            reservation_time=reservation.reservation_time,
            duration_minutes=reservation.duration_minutes
        )
        db.add(db_reservation)
        db.commit()
        db.refresh(db_reservation)
        return db_reservation

    @staticmethod
    def delete_reservation(db: Session, reservation_id: int) -> None:
        reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
        if not reservation:
            raise ReservationNotFoundError()
        db.delete(reservation)
        db.commit()

    @staticmethod
    def check_table_availability(db: Session, table_id: int, start_time: datetime, duration_minutes: int) -> bool:
        end_time = start_time + timedelta(minutes=duration_minutes)
        
        conflicting_reservations = db.query(Reservation).filter(
            Reservation.table_id == table_id,
            Reservation.reservation_time < end_time,
            Reservation.reservation_time + timedelta(minutes=Reservation.duration_minutes) > start_time
        ).count()

        return conflicting_reservations == 0