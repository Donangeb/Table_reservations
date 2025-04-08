from fastapi import APIRouter
from .tables import router as tables_router
from .reservations import router as reservations_router

router = APIRouter()
router.include_router(tables_router, prefix="/tables", tags=["tables"])
router.include_router(reservations_router, prefix="/reservations", tags=["reservations"])

__all__ = ["router"]