class Cart:

    def __init__(self):
        self.__items = []

    def add_item(self, food_object, quantity):

        item = {

            "food": food_object,
            "quantity": quantity
        }
        

        self.__items.append(item)

        print(
            f"\n{food_object.get_food_detail()['Name']} "
            f"added to cart successfully."
        )

    def view_cart(self):

        if not self.__items:
            print("\nCart is empty.")
            return
        print("\n========== YOUR CART ==========")

        for item in self.__items:

            food = item["food"]
            quantity = item["quantity"]

            total = food.get_price() * quantity

            print(
                f"{food.get_food_detail()['Name']} "
                f"x {quantity} = ₹{total}"
            )

        print("--------------------------------")
        print(f"Total: ₹{self.calculate_total()}")

    def calculate_total(self):

        total = 0

        for item in self.__items:

            food = item["food"]
            quantity = item["quantity"]

            total += food.get_price() * quantity

        return total

    def get_items(self):
        return self.__items

    def is_empty(self):
        return len(self.__items) == 0