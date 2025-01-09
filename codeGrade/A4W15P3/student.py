class Student:
    def __init__(
        self, first_name, last_name, date_of_birth, class_code, id=None
    ) -> None:
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.class_code = class_code

    def __repr__(self) -> str:
        return "{}({})".format(
            type(self).__name__,
            ", ".join([f"{key}={value!r}" for key, value in self.__dict__.items()]),
        )
