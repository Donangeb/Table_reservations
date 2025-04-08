from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Table(Base):
    __tablename__ = 'tables'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False) 
    seats = Column(Integer, nullable=False)
    location = Column(String)
    
    reservations = relationship("Reservation", back_populates="table")
    
    def __repr__(self):
        return f"<Table(id={self.id}, name='{self.name}', seats={self.seats}, location='{self.location}')>"

class Reservation(Base):
    __tablename__ = 'reservations'
    
    id = Column(Integer, primary_key=True)
    customer_name = Column(String, nullable=False)
    table_id = Column(Integer, ForeignKey('tables.id'), nullable=False)
    reservation_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    
    table = relationship("Table", back_populates="reservations")
    
    def __repr__(self):
        return f"<Reservation(id={self.id}, customer='{self.customer_name}', table_id={self.table_id}, time={self.reservation_time}, duration={self.duration_minutes} mins)>"