from database.repositories.food_repository import get_all_food
from models.food_item import FoodItem


def get_food_menu():

    rows = get_all_food()

    food_items = []

    for row in rows:
        food_id, name, price = row

        food = FoodItem( name, price, food_id=food_id)

        food_items.append(food)

    return food_items