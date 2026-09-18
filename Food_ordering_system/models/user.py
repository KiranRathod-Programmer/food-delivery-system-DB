class User:

    user_id = 0

    def __init__(self, name, email, phone):
        User.user_id += 1

        self.__user_id = User.user_id
        self.__name = name
        self.__email = email
        self.__phone = phone

    def get_user_detail(self):
        return {
            "ID": self.__user_id,
            "Name": self.__name,
            "Email": self.__email,
            "Phone": self.__phone
        }

    def __str__(self):
        return (
            f"ID       : {self.__user_id}\n"
            f"Name     : {self.__name}\n"
            f"Email    : {self.__email}\n"
            f"Phone No : {self.__phone}"
        )