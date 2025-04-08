from sqlalchemy.orm import Session
from models.models import Table
from schemas.table import TableCreate
from exceptions import TableNotFoundError

class TableService:
    @staticmethod
    def get_table(db: Session, table_id: int) -> Table:
        table = db.query(Table).filter(Table.id == table_id).first()
        if not table:
            raise TableNotFoundError()
        return table

    @staticmethod
    def get_tables(db: Session, skip: int = 0, limit: int = 100) -> list[Table]:
        return db.query(Table).offset(skip).limit(limit).all()

    @staticmethod
    def create_table(db: Session, table: TableCreate) -> Table:
        db_table = Table(
            name=table.name,
            seats=table.seats,
            location=table.location
        )
        db.add(db_table)
        db.commit()
        db.refresh(db_table)
        return db_table

    @staticmethod
    def delete_table(db: Session, table_id: int) -> None:
        table = db.query(Table).filter(Table.id == table_id).first()
        if not table:
            raise TableNotFoundError()
        db.delete(table)
        db.commit()