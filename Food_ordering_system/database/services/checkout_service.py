from database.connection import get_connection
from database.repositories.order_repository import create_order, create_order_item, update_order_status
from database.repositories.payment_repository import create_payment

def checkout(customer_id, cart_items, total, payment_method): 
    connection = get_connection()

    try:
        # 1. Create order
        order_id = create_order( customer_id, total, connection)

        # 2. Create order items
        for item in cart_items:
            food = item["food"]
            quantity = item["quantity"]

            food_detail = food.get_food_detail()

            food_item_id = food_detail["ID"]
            price = food.get_price()

            create_order_item( order_id, food_item_id, quantity, price, connection)

        # 3. Determine payment status
        if payment_method == "CASH":
            payment_status = "PENDING"
        else:
            payment_status = "SUCCESS"

        # 4. Create payment
        create_payment(order_id, total, payment_method, payment_status, connection)

        # 5. Confirm order
        update_order_status( order_id, "CONFIRMED", connection)

        # 6. Commit everything together
        connection.commit()

        return order_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()