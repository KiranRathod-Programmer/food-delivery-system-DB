from database.connection import get_connection


def create_payment(
    order_id,
    amount,
    payment_method,
    status,
    connection=None
):
    own_connection = connection is None

    if own_connection:
        connection = get_connection()

    try:
        with connection.cursor() as cursor:
            query = """
                INSERT INTO payments
                    (order_id, amount, payment_method, status)
                VALUES
                    (%s, %s, %s, %s)
                RETURNING id;
            """

            cursor.execute(
                query,
                (order_id, amount, payment_method, status)
            )

            payment_id = cursor.fetchone()[0]

        if own_connection:
            connection.commit()

        return payment_id

    except Exception:
        if own_connection:
            connection.rollback()
        raise

    finally:
        if own_connection:
            connection.close()


def get_payment_by_order(order_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            query = """
                SELECT id,
                       order_id,
                       amount,
                       payment_method,
                       status,
                       payment_date
                FROM payments
                WHERE order_id = %s;
            """

            cursor.execute(query, (order_id,))
            return cursor.fetchone()

    finally:
        connection.close()