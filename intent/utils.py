from enum import IntEnum


class EventActionTypesChoices(IntEnum):
    TEXT = 1
    ACTION = 2
    API = 3

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
