from fastapi import HTTPException, status


class AIStudingHTTPException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Внутренняя ошибка сервера"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


# --------------------- NotFoundHTTPExceptions ---------------------
class ObjectNotFoundHTTPException(AIStudingHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Такого объекта не существует"


class TopicNotFoundHTTPException(ObjectNotFoundHTTPException):
    detail = "Такой темы не существует"


class TaskNotFoundHTTPException(ObjectNotFoundHTTPException):
    detail = "Задач к этой теме не существует"


class TaskTestNotFoundHTTPException(ObjectNotFoundHTTPException):
    detail = "Тестов к этому заданию не существует"


class SubmissionNotFoundHTTPException(ObjectNotFoundHTTPException):
    detail = "Такой попытки не существует"


# --------------------- ServiceHTTPException ---------------------
class ServiceHTTPException(AIStudingHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Ошибка работы сервиса"


class AIServiceHTTPException(ServiceHTTPException):
    detail = "Ошибка работы сервиса AI"


# --------------------- ExternalTimeoutHTTPException ---------------------
class ExternalTimeoutHTTPException(AIStudingHTTPException):
    status_code = status.HTTP_504_GATEWAY_TIMEOUT
    detail = "Время вышло"


class AIExternalTimeoutHTTPException(ExternalTimeoutHTTPException):
    detail = "Время попытки связаться с сервером AI вышло"
