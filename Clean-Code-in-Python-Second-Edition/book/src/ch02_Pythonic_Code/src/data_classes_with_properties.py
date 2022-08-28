from dataclasses import dataclass, field


@dataclass
class Vehicle:

    wheels: int  # here we're adding to the __init__ constructor
    _wheels: int = field(init=False, repr=False)  # init=False means that this field is not part of the __init__ signature

    @property
    def wheels(self) -> int:
        print("getting wheels")
        return self._wheels

    @wheels.setter
    def wheels(self, wheels: int):
        print("setting wheels to", wheels)
        self._wheels = wheels
