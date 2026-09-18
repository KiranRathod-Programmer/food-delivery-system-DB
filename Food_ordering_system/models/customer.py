from models.user import User
from models.cart import Cart


class Customer(User):

    def __init__(self, name, email, phone, address):
        super().__init__(name, email, phone)

        self.__address = address
        self.__cart = Cart()
        self.__orders = []  

    def get_address(self):
        return self.__address

    def get_cart(self):
        return self.__cart

    def add_order(self, order):
        self.__orders.append(order)

    def view_orders(self):

        if not self.__orders:
            print("\nNo orders found.")
            return

        print("\n========== ORDER HISTORY ==========")

        for order in self.__orders:
            print(order)
            print("----------------------------------")

    def get_customer_profile(self):

        profile = self.get_user_detail()


        # update is dictonary built-in function to kind of add the additional key-value pairs in the dictonary
        profile.update(self.__address.get_address())

        return profile

    def __str__(self):

        return (
            super().__str__()
            + "\n"
            + str(self.__address)
        )
