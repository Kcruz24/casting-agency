import enum


class Gender(enum.Enum):
    male = 'Male'
    female = 'Female'
    other = 'Other'

    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]
