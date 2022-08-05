

class Graduate:

    name: str

    def __init__(self, name: str):
        self.name = name
    def __repr__(self):
        return str(f"'{self.__class__.__name__}': {self.__dict__}")


class Engineer(Graduate):
    salary: float

    def __init__(self, name: str, salary: float):
        super().__init__(name)
        self.salary = salary


eng = Engineer("Johnny", 1542.43)
print(eng)