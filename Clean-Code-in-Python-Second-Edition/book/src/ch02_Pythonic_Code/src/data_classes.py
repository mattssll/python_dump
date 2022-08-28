"""Clean code in Python - Second edition
Chapter 2: Data classes
"""

from typing import List
from dataclasses import dataclass, field


R = 26


@dataclass
class RTrieNode:
    size = R  # since it has no type notation it's not part of __init__ signature
    value: int
    next_: List["RTrieNode"] = field(  # for initialization we define a ...
        default_factory=lambda: [None] * R  # ... list of size R with None in all slots
    )
    # default_factory is a function that returns the default value for the field
    # we use it because if we define the value directly, we won't be able to set it in the object instantiation

    def __post_init__(self):
        if len(self.next_) != self.size:
            raise ValueError("Invalid length provided for next list")
