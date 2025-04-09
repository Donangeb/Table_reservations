class TableNotFoundError(Exception):
    """Столик не найден"""
    pass

class ReservationNotFoundError(Exception):
    """Бронь не найдена"""
    pass

class ReservationConflictError(Exception):
    """Конфликт бронирования (столик уже занят в это время)"""
    pass

class ValidationError(Exception):
    """Ошибка валидации данных"""
    pass