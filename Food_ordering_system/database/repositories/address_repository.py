from database.connection import get_connection


def create_address(
    customer_id,
    city,
    pincode,
    state,
    connection=None
):
    own_connection = connection is None

    if own_connection:
        connection = get_connection()

    try:
        with connection.cursor() as cursor:
            query = """
                INSERT INTO addresses
                    (customer_id, city, pincode, state)
                VALUES
                    (%s, %s, %s, %s)
                RETURNING id;
            """

            cursor.execute(
                query,
                (customer_id, city, pincode, state)
            )

            address_id = cursor.fetchone()[0]

        if own_connection:
            connection.commit()

        return address_id

    except Exception:
        if own_connection:
            connection.rollback()
        raise

    finally:
        if own_connection:
            connection.close()


def get_address_by_customer(customer_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            query = """
                SELECT id,
                       customer_id,
                       city,
                       pincode,
                       state
                FROM addresses
                WHERE customer_id = %s;
            """

            cursor.execute(query, (customer_id,))
            return cursor.fetchone()

    finally:
        connection.close()


def update_address(
    customer_id,
    city,
    pincode,
    state
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            query = """
                UPDATE addresses
                SET city = %s,
                    pincode = %s,
                    state = %s
                WHERE customer_id = %s;
            """

            cursor.execute(
                query,
                (city, pincode, state, customer_id)
            )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()