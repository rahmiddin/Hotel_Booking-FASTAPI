from fastapi import HTTPException, status


class MyException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(MyException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class IncorrectEmailOrPasswordException(MyException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"


class TokenExpiredException(MyException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Срок действия токена истек"


class TokenAbsentException(MyException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectTokenFormatException(MyException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserIsNotPresentException(MyException):
    status_code = status.HTTP_401_UNAUTHORIZED


class RoomCannotBeBooked(MyException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Не осталось свободных номеров"


class DateFromMoreThanDateTo(MyException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Дата заезда больше чем дата выезда или равна ей"
