from datetime import datetime


class Student:
    def __init__(
        self, first_name, last_name, date_of_birth, class_code, id=None
    ) -> None:
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.class_code = class_code

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def get_age(self) -> int:
        birth_date = datetime.strptime(self.date_of_birth, "%Y-%m-%d")
        today = datetime.today()
        return (
            today.year
            - birth_date.year
            - ((today.month, today.day) < (birth_date.month, birth_date.day))
        )

    def __repr__(self) -> str:
        return "{}({})".format(
            type(self).__name__,
            ", ".join([f"{key}={value!r}" for key, value in self.__dict__.items()]),
        )
