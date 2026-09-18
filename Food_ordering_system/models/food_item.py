class FoodItem:

    food_id = 0

    def __init__(self, name, price):
        FoodItem.food_id += 1

        self.__food_id = FoodItem.food_id
        self.__name = name
        self.__price = price

    def get_food_detail(self):
        return {
            "ID": self.__food_id,
            "Name": self.__name,
            "Price": self.__price
        }

    def get_price(self):
        return self.__price

    def __str__(self):
        return f"{self.__food_id}. {self.__name} - ₹{self.__price}"
