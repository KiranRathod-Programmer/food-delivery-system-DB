from models.order import Order
from models.payment import UPIPayment, CardPayment, CashPayment
from database.services.customer_service import create_customer_with_address
from database.services.food_service import get_food_menu
from database.services.checkout_service import checkout as checkout_order

import re

# validation of user input 
def get_valid_name():
    while True:
        name = input("Enter your name: ").strip()

        if not name:
            print("Name cannot be empty.")
        elif not re.fullmatch(r"[A-Za-z ]+", name):
            print("Name should contain only alphabets and spaces.")
        else:
            return name


def get_valid_email():
    while True:
        email = input("Enter your email: ").strip()

        if not re.fullmatch(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email):
            print("Please enter a valid email address.")
        else:
            return email


def get_valid_phone():
    while True:
        phone = input("Enter your phone number: ").strip()

        if not re.fullmatch(r"[6-9][0-9]{9}", phone):
            print("Phone number must be a valid 10-digit Indian mobile number.")
        else:
            return phone


def get_valid_city():
    while True:
        city = input("Enter city: ").strip()

        if not city:
            print("City cannot be empty.")
        elif not re.fullmatch(r"[A-Za-z ]+", city):
            print("City should contain only alphabets and spaces.")
        else:
            return city


def get_valid_pincode():
    while True:
        pincode = input("Enter pincode: ").strip()

        if not re.fullmatch(r"[1-9][0-9]{5}", pincode):
            print("Pincode must be a valid 6-digit number.")
        else:
            return pincode


def get_valid_state():
    while True:
        state = input("Enter state: ").strip()

        if not state:
            print("State cannot be empty.")
        elif not re.fullmatch(r"[A-Za-z .]+", state):
            print("State should contain only alphabets, spaces and dots.")
        else:
            return state



def create_customer():

    print("\n========== CUSTOMER DETAILS ==========")

    name = get_valid_name()
    email = get_valid_email()
    phone = get_valid_phone()

    print("\n========== DELIVERY ADDRESS ==========")

    city = get_valid_city()
    pincode = get_valid_pincode()
    state = get_valid_state()

    customer = create_customer_with_address( name, email, phone, city, pincode, state)

    return customer


def show_menu(food_items):

    print("\n========== FOOD MENU ==========")

    for food in food_items:
        print(food)


def add_food_to_cart(customer, food_items):

    show_menu(food_items)

    try:
        choice = int(input("\nSelect food: "))

        if choice < 1 or choice > len(food_items):
            print("Invalid food selection.")
            return

        quantity = int(input("Enter quantity: "))

        if quantity <= 0:
            print("Quantity must be greater than 0.")
            return

        selected_food = food_items[choice - 1]

        customer.get_cart().add_item(
            selected_food,
            quantity
        )
    except ValueError:
        print("Please enter a valid number.")


def checkout(customer):

    cart = customer.get_cart()

    if cart.is_empty():

        print("\nYour cart is empty.")
        return

    cart.view_cart()

    confirm = input("\nDo you want to place the order? (y/n): ").lower()

    if confirm != "y":

        print("\nOrder cancelled.")
        return

    total = cart.calculate_total()

    print("\n========== PAYMENT ==========")
    print("1. UPI")
    print("2. Card")
    print("3. Cash on Delivery")

    choice = input("Select payment method: ")

    if choice == "1":
        payment = UPIPayment(total)
        payment_method = "UPI"
    elif choice == "2":
        payment = CardPayment(total)
        payment_method = "CARD"
    elif choice == "3":
        payment = CashPayment(total)
        payment_method = "CASH"
    else:
        print("Invalid payment option.")
        return
    try:

        order_id = checkout_order( customer.get_user_detail()["ID"], cart.get_items(), total, payment_method)

        payment.pay()

        order = Order( customer, cart, order_id=order_id)

        order.update_status("CONFIRMED")

        customer.add_order(order)

        cart.clear_cart()

        print("\n========== ORDER CONFIRMED ==========")
        print(order)

    except Exception as error:
        print("\nOrder could not be placed.")
        print("Reason:", error)


def main():

    print("======================================")
    print("       WELCOME TO FOODKART")
    print("======================================")

    try:
        customer = create_customer()
        food_items = get_food_menu()

        if not food_items:
            print("\nNo food items available.")
            return

        while True:

            print("\n========== MAIN MENU ==========")

            print("1. View Food Menu")
            print("2. Add Food to Cart")
            print("3. View Cart")
            print("4. Checkout")
            print("5. View Orders")
            print("6. View Profile")
            print("7. Exit")

            choice = input("\nEnter your choice from 'MAIN MENU': ")

            if choice == "1":
                show_menu(food_items)
            elif choice == "2":
                add_food_to_cart( customer, food_items)
            elif choice == "3":
                customer.get_cart().view_cart()
            elif choice == "4":
                checkout(customer)
            elif choice == "5":
                customer.view_orders()
            elif choice == "6":
                print("\n========== CUSTOMER PROFILE ==========")
                print(customer)
            elif choice == "7":
                print("\nThank you for using FoodKart!")
                break
            else:
                print("\nInvalid choice. Please try again.")

    except Exception as error:
        print("\nApplication could not start.")
        print("Reason:", error)


if __name__ == "__main__":
    main()