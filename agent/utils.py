
from enum import IntEnum


class EntityTypesChoices(IntEnum):
    SYSTEM = 1
    CUSTOM = 2
    USER = 3
    DEFAULT = 0

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class EventActionTypesChoices(IntEnum):
    TEXT = 1
    ACTION = 2
    API = 3

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
