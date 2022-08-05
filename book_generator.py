from datetime import datetime
from faker import Faker
from enum import Enum
import random


fake = Faker()

class BookCategory(Enum):
    horror = 0
    adventure = 1
    love = 2
    science = 3

class Book:
    book_category: BookCategory
    price: float
    def __init__(self):
        self.book_category = random.choice(list(BookCategory))
        self.price = round(random.uniform(10, 100), 2)
    def __str__(self):
        return f'Book(book_category={self.book_category.name}, price={self.price})'


class BookGenerator():
    @staticmethod
    def generate_books(n: int):
        """ Returns a generator with 'n' Books in it """    
        for i in range(n):
            yield Book()


def print_books(n):
    for item in BookGenerator.generate_books(n):
        pass #print(item)


if __name__ == "__main__":

    start_time = datetime.now()
    print_books(5000000)
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
