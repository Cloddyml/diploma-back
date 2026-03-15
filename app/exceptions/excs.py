class AIStudingException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


# --------------------- AlreadyExistsExceptions ---------------------
class ObjectAlreadyExistsException(AIStudingException):
    detail = "Такой объект уже существует"


class TopicAlreadyExistsException(AIStudingException):
    detail = "Такая тема уже существует (slug должен быть уникальным)"


class TaskAlreadyExistsException(ObjectAlreadyExistsException):
    detail = "Такое задание уже существует"


# --------------------- NotFoundExceptions ---------------------
class ObjectNotFoundException(AIStudingException):
    detail = "Такого объекта не существует"


class TopicNotFoundException(ObjectNotFoundException):
    detail = "Такой темы не существует"


class TaskNotFoundException(ObjectNotFoundException):
    detail = "Задач к этой теме не существует"


# --------------------- EmptyUpdateDataExceptions ---------------------
class EmptyUpdateDataException(AIStudingException):
    detail = "Нет данных для обновления"


class EmptyUpdateTopicDataException(EmptyUpdateDataException):
    detail = "Нет данных для обновления темы"


class EmptyUpdateTaskDataException(EmptyUpdateDataException):
    detail = "Нет данных для обновления задания"


# --------------------- CannotBeEmptyExceptions ---------------------
class CannotBeEmptyException(AIStudingException):
    detail = "Введенное поле или поля не могут быть пустыми"


class CannotBeEmptyTopicException(CannotBeEmptyException):
    detail = "Введенное поле или поля не могут быть пустыми"


class CannotBeEmptyTaskException(CannotBeEmptyException):
    detail = "Введенное поле или поля не могут быть пустыми"
