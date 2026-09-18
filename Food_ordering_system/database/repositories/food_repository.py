from database.connection import get_connection


def create_food(name, price, connection=None):
    own_connection = connection is None

    if own_connection:
        connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO food_items (name, price)
                VALUES (%s, %s)
                RETURNING id;
                """,
                (name, price)
            )

            food_id = cursor.fetchone()[0]

        if own_connection:
            connection.commit()

        return food_id

    except Exception:
        if own_connection:
            connection.rollback()
        raise

    finally:
        if own_connection:
            connection.close()


def get_food(food_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, name, price
                FROM food_items
                WHERE id = %s;
                """,
                (food_id,)
            )

            return cursor.fetchone()

    finally:
        connection.close()


def get_all_food():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, name, price
                FROM food_items
                ORDER BY id;
                """
            )

            return cursor.fetchall()

    finally:
        connection.close()