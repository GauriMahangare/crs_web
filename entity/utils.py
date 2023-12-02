from enum import IntEnum


class EntityTypesChoices(IntEnum):
    SYSTEM = 1
    CUSTOM = 2
    USER = 3
    DEFAULT = 0

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
