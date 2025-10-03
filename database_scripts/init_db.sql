DROP SCHEMA IF EXISTS project CASCADE;
CREATE SCHEMA project;

-- Table: Addresses
CREATE TABLE project.Addresses (
    address_id SERIAL PRIMARY KEY,
    address_number INT NOT NULL,
    address_street VARCHAR(256) NOT NULL,
    address_city VARCHAR(128) NOT NULL,
    address_postal_code VARCHAR(8) NOT NULL,
    address_country VARCHAR(128) NOT NULL
);

-- Table: Customers
CREATE TABLE project.Customers (
    customer_id SERIAL PRIMARY KEY,
    customer_first_name VARCHAR(128),
    customer_last_name VARCHAR(128),
    customer_phone VARCHAR(16),
    customer_email VARCHAR(128),
    customer_password_hash VARCHAR(512) NOT NULL,
    customer_address_id INTEGER,
    FOREIGN KEY (customer_address_id) REFERENCES Addresses(address_id)
);

-- Table: Admins
CREATE TABLE project.Admins (
    admin_id SERIAL PRIMARY KEY,
    admin_first_name VARCHAR(128),
    admin_last_name VARCHAR(128),
    admin_password_hash VARCHAR(512)
);

-- Table: Drivers
CREATE TABLE project.Drivers (
    driver_id SERIAL PRIMARY KEY,
    driver_first_name VARCHAR(128),
    driver_last_name VARCHAR(128),
    driver_password_hash VARCHAR(512),
    driver_is_delivering BOOLEAN,
    driver_phone VARCHAR(16)
);

-- Table: Orders
CREATE TABLE project.Orders (
    order_id SERIAL PRIMARY KEY,
    order_customer_id INTEGER,
    order_state INTEGER,
    order_date DATE,
    order_time TIME,
    order_is_paid BOOLEAN,
    order_is_prepared BOOLEAN,
    FOREIGN KEY (order_customer_id) REFERENCES Customers(customer_id)
);

-- Table: Items
CREATE TABLE project.Items (
    item_id SERIAL PRIMARY KEY,
    item_name VARCHAR(128),
    item_price FLOAT(24) CHECK (item_price >= 0),
    item_type VARCHAR(32),
    item_description VARCHAR(256),
    item_stock INTEGER CHECK (item_stock >= 0),
    item_in_menu BOOLEAN DEFAULT false
);

-- Table: Orders_Items 
CREATE TABLE project.Order_Items (
    order_id INTEGER,
    item_id INTEGER,
    item_quantity INTEGER CHECK (item_quantity > 0),
    item_price FLOAT(24) CHECK (item_price >= 0),
    PRIMARY KEY (order_id, item_id),
    FOREIGN KEY (order_id) REFERENCES project.Orders(order_id),
    FOREIGN KEY (item_id) REFERENCES project.Items(item_id)
);


-- Table: Deliveries
CREATE TABLE project.Deliveries (
    delivery_id_order INTEGER,
    delivery_id_driver INTEGER,
    delivery_state INTEGER,
    PRIMARY KEY (delivery_id_order, delivery_id_driver),
    FOREIGN KEY (delivery_id_order) REFERENCES project.Orders(order_id),
    FOREIGN KEY (delivery_id_driver) REFERENCES project.Drivers(driver_id)
);

