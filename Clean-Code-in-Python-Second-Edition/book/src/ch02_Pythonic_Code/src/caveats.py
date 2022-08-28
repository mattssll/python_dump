"""Clean Code in Python - Chapter 2: Pythonic Code

> Caveats in Python
"""

def wrong_user_display(user_metadata: dict = {"name": "John", "age": 30}):  # creates dict only once and can't be called two times
    name = user_metadata.pop("name")
    age = user_metadata.pop("age")

    return f"{name} ({age})"


def user_display(user_metadata: dict = None):
    user_metadata = user_metadata or {"name": "John", "age": 30}

    name = user_metadata.pop("name")
    age = user_metadata.pop("age")

    return f"{name} ({age})"


class BadList(list):
    def __getitem__(self, index):
        value = super().__getitem__(index)
        if index % 2 == 0:
            prefix = "even"
        else:
            prefix = "odd"
        return f"[{prefix}] {value}"


from collections import UserList

class GoodList(UserList):
    def __getitem__(self, index):
        value = super().__getitem__(index)
        if index % 2 == 0:
            prefix = "even"
        else:
            prefix = "odd"
        return f"[{prefix}] {value}"


def main():
    gl = GoodList((0,1,2,3))
    # below's for loop would not work for previous implementation
    for item in gl:
        print(item)
    

if __name__ == "__main__":
    main()