class Address:

    def __init__(self, city, pincode, state):
        self.__city = city
        self.__pincode = pincode
        self.__state = state

    def get_address(self):
        return {
            "City": self.__city,
            "Pincode": self.__pincode,
            "State": self.__state
        }

    def __str__(self):
        return (
            f"City    : {self.__city}\n"
            f"Pincode : {self.__pincode}\n"
            f"State   : {self.__state}"
        )