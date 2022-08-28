"""Clean Code in Python - Chapter 1: Introduction, Tools, and Formatting

> Annotations
"""
from dataclasses import dataclass
from typing import Tuple, List

Client = Tuple[int, str]


def process_clients(clients: List[Client]):
    pass


@dataclass
class Point:
    lat: float
    long: float


def locate(latitude: float, longitude: float) -> Point:
    """Find an object in the map by its coordinates"""
    return Point(latitude, longitude)



# The code below will print our type annotations for ea object:
print(process_clients.__annotations__)
print(Point.__annotations__)
print(locate.__annotations__)