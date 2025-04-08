from pydantic import BaseModel, field_validator
from datetime import datetime

class ReservationBase(BaseModel):
    customer_name: str
    table_id: int
    reservation_time: datetime
    duration_minutes: int

    @field_validator("duration_minutes")
    def validate_duration(cls, v):
        if v <= 0:
            raise ValueError("Duration must be positive")
        return v

class ReservationCreate(ReservationBase):
    pass

class ReservationResponse(ReservationBase):
    id: int

    class Config:
        from_attributes = True

class ReservationCheck(BaseModel):
    table_id: int
    reservation_time: datetime
    duration_minutes: int