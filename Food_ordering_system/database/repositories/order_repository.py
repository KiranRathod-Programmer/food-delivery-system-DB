from database.connection import get_connection


def create_order(customer_id, total, connection=None):
    own_connection = connection is None

    if own_connection:
        connection = get_connection()

    try:
        with connection.cursor() as cursor:
            query = """
                INSERT INTO orders (customer_id, total)
                VALUES (%s, %s)
                RETURNING id;
            """

            cursor.execute(query, (customer_id, total))
            order_id = cursor.fetchone()[0]

        if own_connection:
            connection.commit()

        return order_id

    except Exception:
        if own_connection:
            connection.rollback()
        raise

    finally:
        if own_connection:
            connection.close()


def create_order_item(order_id, food_item_id, quantity, price, connection=None):
    own_connection = connection is None

    if own_connection:
        connection = get_connection()

    try:
        with connection.cursor() as cursor:
            query = """
                INSERT INTO order_items
                    (order_id, food_item_id, quantity, price)
                VALUES
                    (%s, %s, %s, %s)
                RETURNING id;
            """

            cursor.execute(
                query,
                (order_id, food_item_id, quantity, price)
            )

            order_item_id = cursor.fetchone()[0]

        if own_connection:
            connection.commit()

        return order_item_id

    except Exception:
        if own_connection:
            connection.rollback()
        raise

    finally:
        if own_connection:
            connection.close()


def get_customer_orders(customer_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            query = """
                SELECT id, customer_id, total, status, order_date
                FROM orders
                WHERE customer_id = %s
                ORDER BY order_date DESC;
            """

            cursor.execute(query, (customer_id,))
            return cursor.fetchall()

    finally:
        connection.close()


def update_order_status(order_id, status, connection=None):
    own_connection = connection is None

    if own_connection:
        connection = get_connection()

    try:
        with connection.cursor() as cursor:
            query = """
                UPDATE orders
                SET status = %s
                WHERE id = %s;
            """

            cursor.execute(query, (status, order_id))
            row_count = cursor.rowcount

        if own_connection:
            connection.commit()

        return row_count

    except Exception:
        if own_connection:
            connection.rollback()
        raise

    finally:
        if own_connection:
            connection.close()