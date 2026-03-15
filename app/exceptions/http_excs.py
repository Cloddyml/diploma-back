from fastapi import HTTPException, status


class AIStudingHTTPException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Внутренняя ошибка сервера"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


# --------------------- AlreadyExistsHTTPExceptions ---------------------
class ObjectAlreadyExistsHTTPException(AIStudingHTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Такой объект уже существует"


class TopicAlreadyExistsHTTPException(ObjectAlreadyExistsHTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Тема с таким slug уже существует"


# --------------------- NotFoundHTTPExceptions ---------------------
class ObjectNotFoundHTTPException(AIStudingHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Такого объекта не существует"


class TopicNotFoundHTTPException(ObjectNotFoundHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Такой темы не существует"


# --------------------- EmptyUpdateDataHTTPExceptions ---------------------
class EmptyUpdateDataHTTPException(AIStudingHTTPException):
    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
    detail = "Нет данных для обновления"


class EmptyUpdateTopicDataHTTPException(EmptyUpdateDataHTTPException):
    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
    detail = "Нет данных для обновления темы"


# --------------------- CannotBeEmptyHTTPExceptions ---------------------
class CannotBeEmptyHTTPException(AIStudingHTTPException):
    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
    detail = "Введенное поле или поля не могут быть пустыми"


class CannotBeEmptyTopicHTTPException(CannotBeEmptyHTTPException):
    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
    detail = "Введенное поле или поля не могут быть пустыми"
