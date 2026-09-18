from database.connection import get_connection


def create_customer(name, email, phone, connection=None):
    own_connection = connection is None

    if own_connection:
        connection = get_connection()

    try:
        with connection.cursor() as cursor:
            query = """
                INSERT INTO customers (name, email, phone)
                VALUES (%s, %s, %s)
                RETURNING id;
            """

            cursor.execute(
                query,
                (name, email, phone)
            )

            customer_id = cursor.fetchone()[0]

        if own_connection:
            connection.commit()

        return customer_id

    except Exception:
        if own_connection:
            connection.rollback()
        raise

    finally:
        if own_connection:
            connection.close()


def get_customer(customer_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            query = """
                SELECT id, name, email, phone
                FROM customers
                WHERE id = %s;
            """

            cursor.execute(query, (customer_id,))
            return cursor.fetchone()

    finally:
        connection.close()


def get_all_customers():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            query = """
                SELECT id, name, email, phone
                FROM customers
                ORDER BY id;
            """

            cursor.execute(query)
            return cursor.fetchall()

    finally:
        connection.close()


def update_customer(customer_id, name, email, phone):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            query = """
                UPDATE customers
                SET name = %s,
                    email = %s,
                    phone = %s
                WHERE id = %s;
            """

            cursor.execute(
                query,
                (name, email, phone, customer_id)
            )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def delete_customer(customer_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            query = """
                DELETE FROM customers
                WHERE id = %s;
            """

            cursor.execute(query, (customer_id,))

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()