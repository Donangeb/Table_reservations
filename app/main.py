from fastapi import FastAPI
from app.routers.reservations import router as reservations_router
from app.routers.tables import router as tables_router

app = FastAPI()

app.include_router(
    reservations_router,
    prefix="/reservations",
    tags=["reservations"]
)

app.include_router(
    tables_router,
    prefix="/tables",
    tags=["tables"]
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Restaurant Reservation System"}