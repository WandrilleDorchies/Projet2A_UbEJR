from src.DAO.CustomerDAO import CustomerDAO
from src.Model.Address import Address
from src.Service.GoogleMapService import GoogleMapService

from .UserService import UserService


class CustomerService:
    def __init__(
        self, user_service: UserService, customer_dao: CustomerDAO, gm_service: GoogleMapService
    ):
        self.user_service = user_service
        self.customer_dao = customer_dao
        self.gm_service = gm_service

    def create_customer(
        self,
        password: str,
        first_name: str,
        last_name: str,
        address: str,
        phone: str,
        mail: str,
    ):
        hashed_password: str = self.user_service.create_hashed_password(password)
        customer_address = self.gm_service.validate_address(address)
        address_id = customer

        return self.customer_dao.create_customer(
            first_name, last_name, phone, mail, hashed_password, address_id
        )

    def update_customer(self, customer_id: int, update) -> None:

        update_message_parts = []
        for field, value in update.customer():
            update_message_parts.append(f"{field}={value}")

        print(f"[CustomerService] Updating customer: {", ".join(update_message_parts)}")

        updated_customer = self.customer_dao.update_customer(customer_id=id, update=update)
        print(f"[CustomerService] DAO returned after creation: {updated_customer}")
        return updated_customer

    def delete_customer(self, customer_id : int) -> None:
        """
        Deletes a customer from the database by its ID.

        Parameters
        ----------
        customer_id : int
        The ID of the customer to delete.
        """
        print(f"[CustomerService] Deleting customer with ID: {customer_id}")

        customer = self.customer_dao.get_customer_by_id(customer_id)
        if customer is None:
            raise ValueError(f"[CustomerService] Cannot delete: customer with ID {customer_id} not found.")

        self.customer_dao.delete_customer_by_id(customer_id)
        print(f"[CustomerService] Customer with ID {customer_id} has been deleted.")

    def get_customer_by_id(self, customer_id: int)  -> Item | None:
        print(f"[CustomerService] Getting customer with ID: {customer_id}")
        customer = self.customer_dao.get_customer_by_id(customer_id)
        print(f"[CustomerService] DAO returned: {customer}")
        return customer
    
    def get_all_customer(self) -> list[Customer] | None:
        print("[CustomerService] Getting all customers")
        customers = self.customer_dao.get_all_item()
        print(f"[CustomerService] DAO returned: {customers}")
        return customers

    def order_history(self,customer_id:int) -> list[Order] | None:
        print(f"[CustomerService] Getting order history with customer ID: {customer_id}")
        history = self.order_dao.get_all_order_by_customer(customer_id)
        print(f"[CustomerService] DAO returned: {history}")
        return history

    def make_order() -> Order :
        pass