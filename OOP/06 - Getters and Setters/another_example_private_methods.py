import csv


class Item:
    all = []

    # private method
    def __add_to_list(self):
        Item.all.append(self)

    @classmethod
    def instantiate_items_from_csv(cls, path):
        with open('items.csv', 'r') as f:
            reader = csv.DictReader(f)
            readers = list(reader)
        for item in readers:
            i = Item()
            i.name = item['name']
            i.price = item['price']
            i.quantity = item['quantity']
            i.__add_to_list()

    @staticmethod
    def return_integer_or_float(val):
        val = int(val) if float(val) == int(val) else val
        return val


    # Setters and getters for our three attributes
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, value):
        if len(value) > 10:
            raise Exception("The name is too long!")
        else:
            self.__name = value

    @property
    def price(self):
        return self.__price
    @price.setter
    def price(self, value):
        if float(value) < 0:
            raise Exception("The price has to be bigger than 0!")
        else:
            self.__price = self.return_integer_or_float(float(value))

    @property
    def quantity(self):
        return self.__quantity
    @quantity.setter
    def quantity(self, value):
        if int(value) < 0:
            raise Exception("The quantity has to be bigger than 0!")
        else:
            self.__quantity = int(value)


    def __repr__(self):
        return f"{self.__class__.__name__}('{self.__name}', {self.__price}, {self.__quantity})"




if __name__ == '__main__':
    # Instantiate lots of Item objects from the CSV, send to a list thanks to our instantiate from csv method
    Item.instantiate_items_from_csv('./items.csv')
    print(Item.all[0:5])

    item1 = Item.all[0]
    item1.quantity = 50  # using a setter
    print(len(Item.all))
    # item1.add_to_list() # this would not work because "__add_to_list" is a private method not accessible by the instance
    print(len(Item.all))


