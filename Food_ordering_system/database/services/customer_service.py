from database.connection import get_connection

from database.repositories.customer_repository import create_customer
from database.repositories.address_repository import create_address

from models.customer import Customer
from models.address import Address


def create_customer_with_address( name, email, phone, city, pincode, state):

    connection = get_connection()

    try:

        customer_id = create_customer( name, email, phone, connection )

        address_id = create_address( customer_id, city, pincode, state, connection )

        connection.commit()

        address = Address( city, pincode, state )

        customer = Customer( name, email, phone, address, customer_id=customer_id )

        return customer

    except Exception:
        connection.rollback()
        raise
    finally:

        connection.close()