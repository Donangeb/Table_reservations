from sqlalchemy import inspect, create_engine, text

engine = create_engine("postgresql://postgres:Password@localhost/table_reservations")

# Получить список всех таблиц
from sqlalchemy import inspect

inspector = inspect(engine)
tables = inspector.get_table_names()
print("Tables in DB:", tables)