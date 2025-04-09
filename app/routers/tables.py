from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.services.table_service import TableService, TableNotFoundError
from app.schemas.table import TableBase as TableSchema, TableCreate
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=List[TableSchema])
def get_tables(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return TableService.get_tables(db, skip=skip, limit=limit)

@router.post("/", response_model=TableSchema, status_code=status.HTTP_201_CREATED)
def create_table(table: TableCreate, db: Session = Depends(get_db)):
    return TableService.create_table(db, table)

@router.delete("/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_table(table_id: int, db: Session = Depends(get_db)):
    try:
        TableService.delete_table(db, table_id)
    except TableNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Table not found"
        )