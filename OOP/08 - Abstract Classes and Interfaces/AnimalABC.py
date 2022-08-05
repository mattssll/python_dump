from abc import ABC, abstractmethod


class Animal(ABC):
    type: str = NotImplemented  # if not implemented will throw an error


    @property
    @abstractmethod
    def make_sound(self):
        ...







h1 = Cat(25)
print(h1.age)

