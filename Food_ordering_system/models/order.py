class Order:

    order_id = 0

    def __init__(self, customer, cart):
        Order.order_id += 1

        self.__order_id = Order.order_id
        self.__customer = customer
        self.__items = cart.get_items().copy()
        self.__total = cart.calculate_total()
        self.__status = "PLACED"

    def get_total(self):
        return self.__total

    def get_status(self):
        return self.__status

    def update_status(self, status):
        self.__status = status

    def __str__(self):

        return (
            f"Order ID: {self.__order_id}\n"
            f"Customer: {self.__customer.get_user_detail()['Name']}\n"
            f"Total   : ₹{self.__total}\n"
            f"Status  : {self.__status}"
        )