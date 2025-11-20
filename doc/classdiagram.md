```mermaid
---
config:
  theme: default
title: UBEJR class mdiagram
---

classDiagram
namespace data_models {
    class Address {
        +address_id: int
        +address_number: int
        +address_street: str
        +address_city: str
        +address_postal_code: int
        +address_country: str
    }
    class Admin {
        +username: str
    }

    class Customer {
        +customer_address: Address
        +customer_phone: str
        +customer_mail: str
    }

    class Driver {
        +driver_phone: str
        +driver_is_delivering: bool = False
    }

    class Orderable {
        +orderable_id: int
        +orderable_type: Literal["item", "bundle"]
        +orderable_image_data: Optional[bytes] = None
        +is_in_menu: bool = False
    }

    class Item {
        +item_id: int
        +orderable_id: int
        +item_name: str
        +item_price: float > 0 
        +item_type: Literal["Starter", "Main course", "Dessert", "Side dish", "Drink"]
        +item_description: str
        +item_stock: int >= 0

    }

    class Bundle {
        +bundle_id: int
        +orderable_id: int
        +bundle_name: str
        +bundle_reduction: int
        +bundle_description: str
        +bundle_availability_start_date: datetime
        +bundle_availability_end_date: datetime
        +bundle_items: Dict[Item, int]

    }

    class Order {
        +order_id: int
        +order_customer_id: int
        +order_state: OrderState = OrderState.PENDING
        +order_created_at: datetime
        +order_paid_at: Optional[datetime] = None
        +order_orderables: Dict[Union[Bundle, Item], int]

    }

    class Delivery {
        +delivery_order_id: int
        +delivery_driver_id: int
        +delivery_created_at: datetime
        +delivery_state: Optional[int] = None
    }
}

namespace services {
    class Dummy {
        dummy : int
    }
}

namespace DAOs {
    class AddressDAO {
        +create_address(address_number: int, address_street: str, address_city: str, address_postal_code: int, address_country: str) : Address
        +get_address_by_id(self, address_id: int): Optional[Address]
        +get_address_by_customer_id(self, customer_id: int): Optional[Address]
        +update_address(self, address_id: int, update: dict): Optional[Address]
        +delete_address_by_id(self, address_id: int): None
    }
    class AdminDAO {
        +get_admin: Admin
        +create_admin( username: str, first_name: str, last_name: str, password: str, salt: str): Admin
        +update_admin_password(new_password): Admin
        _map_db_to_model(raw_admin: dict): dict
    }
    class CustomerDAO {
        +create_customer(first_name: str, last_name: str, phone: str, mail: str, password_hash: str, salt: str, address_id: int): Customer
        +get_customer_by_id(customer_id: int): Optional[Customer]
        +get_customer_by_email(mail: str) -> Optional[Customer]
        +get_customer_by_phone(phone: str) -> Optional[Customer]
        +get_all_customers(): Optional[List[Customer]]
        +update_customer(customer_id: int, update: dict): Optional[Customer]
        +delete_customer(self, customer_id: int):None
        _map_db_to_model(raw_customer: dict) -> dict:

    }
    class DriverDAO {
        create_driver(self, first_name: str, last_name: str, phone: str, password_hash: str, salt: str) -> Driver:
        get_driver_by_id(self, driver_id: int) -> Optional[Driver]:
        get_driver_by_phone(self, phone_number: str) -> Optional[Driver]:
        get_all_drivers(self) -> Optional[list[Driver]]:
        update_driver(self, driver_id: int, update: dict):
        delete_driver(self, driver_id: int) -> None:
        _map_db_to_model(raw_driver: dict) -> dict:
    }

    class ItemDAO {
        +create_item(item_name: str, item_price: float, item_type: str, item_description: str, item_stock: int, item_image: Optional[bytes] = None, is_in_menu: bool = False) -> Item:
        +get_item_by_id(self, item_id: int) -> Optional[Item]:
        +get_item_by_orderable_id(self, orderable_id: int) -> Optional[Item]:
        +get_all_items(self) -> List[Item]:
        +update_item(self, item_id: int, update: dict) -> Item:
        +delete_item_by_id(self, item_id: int) -> None:
        _item_is_in_bundle(self, item_id: int) -> bool:

    }

    class OrderableDAO {
        +create_orderable(orderable_type: str, orderable_name: str = None, orderable_image_data: Optional[bytes] = None, is_in_menu: bool = False): int
        +get_orderable_by_id(self, orderable_id: int): Optional[Dict]
        +get_all_orderables(): List[Dict]
        +update_orderable_state(self, orderable_id: int, is_in_menu: bool): Dict
        +get_image_from_orderable(self, orderable_id: int): bytes
        +update_image(self, orderable_id: int, orderable_type: str, orderable_name: str,orderable_image_data: bytes): Dict
        update_image(orderable_id: int, orderable_type: str, orderable_name: str, orderable_image_data: bytes): Dict
        delete_orderable(self, orderable_id: int): None
        _is_in_menu(self, orderable_id: int): bool

    }

    class OrderDAO {
        +create_order(customer_id: int): Order
        +get_order_by_id(order_id: int): Optional[Order]
        get_all_orders(limit: int): Optional[List[Order]]
        +get_all_orders_by_customer(customer_id: int): Optional[List[Order]]
        +get_customer_current_order(customer_id: int): Optional[Order]
        +get_orders_by_state(state: int, order_by: Literal["DESC", "ASC"] = "DESC"): List[Order]
        +get_actives_orders(self): List[Order]
        +update_order_state(self, order_id: int, new_state: int): Order
        +delete_order(self, order_id): None
        +add_orderable_to_order(self, order_id: int, orderable_id: int, quantity: int = 1): Order
        +remove_orderable_from_order(order_id: int, orderable_id: int, quantity: int = 1): Order
        +get_quantity_of_orderables(order_id: int, orderable_id: int): int
        _get_orderables_in_order(order_id: int): Dict[Union[Item, Bundle], int]:

    }

    class DeliveryDAO {
        +create_delivery(order_id: int, driver_id: int): Delivery
        +get_delivery_by_driver(delivery_id_driver: int): Optional[Delivery]
        +get_driver_current_delivery(delivery_id_driver: int): Optional[Delivery]
        +get_delivery_by_user(customer_id: int): Optional[Delivery]
        +get_delivery_by_order_id(order_id: int): Optional[Delivery]
        +update_delivery_state(delivery_id: int, state: int): Delivery
        +change_driver(delivery_id: int, driver_id: int): Delivery
        +delete_delivery(delivery_id: int): None

    }
}
namespace controllers {
    class Dummy {
        dummy : int
    }
}


    %% ============================
    %% Relationships
    %% ============================

