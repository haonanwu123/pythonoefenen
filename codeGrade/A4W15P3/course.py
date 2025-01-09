class Course:
    def __init__(self, name, points, id=None) -> None:
        self.id = id
        self.name = name
        self.points = points

    def __repr__(self) -> str:
        return "{}({})".format(
            type(self).__name__,
            ", ".join([f"{key}={value!r}" for key, value in self.__dict__.items()]),
        )
