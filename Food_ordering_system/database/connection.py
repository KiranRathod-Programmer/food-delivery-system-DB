import psycopg2


def get_connection():
    connection = psycopg2.connect(
        host="localhost",
        port=5432,
        database="food_ordering_db",
        user="postgres",
        password="12345"
    )

    return connection