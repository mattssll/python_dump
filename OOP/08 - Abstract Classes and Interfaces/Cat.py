import AnimalABC


class Cat(AnimalABC):
    age: int
    def __init__(self, age):
        self.age = age
        #self.type = type

    def make_sound(self):
        print("uha")