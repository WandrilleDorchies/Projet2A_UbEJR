DROP SCHEMA IF EXISTS test CASCADE;
CREATE SCHEMA test;

-- Table: Addresses
CREATE TABLE test.Addresses (
    address_id SERIAL PRIMARY KEY,
    address_number INT NOT NULL,
    address_street VARCHAR(256) NOT NULL,
    address_city VARCHAR(128) NOT NULL,
    address_postal_code VARCHAR(8) NOT NULL,
    address_country VARCHAR(128) NOT NULL
);

-- Table: Customers
CREATE TABLE test.Customers (
    customer_id SERIAL PRIMARY KEY,
    customer_first_name VARCHAR(128),
    customer_last_name VARCHAR(128),
    customer_phone VARCHAR(16),
    customer_email VARCHAR(128),
    customer_password_hash VARCHAR(512) NOT NULL,
    customer_salt CHAR(256) NOT NULL,
    customer_address_id INTEGER,
    FOREIGN KEY (customer_address_id) REFERENCES test.Addresses(address_id)
);

-- Table: Admins
CREATE TABLE test.Admins (
    admin_id SERIAL PRIMARY KEY,
    admin_first_name VARCHAR(128),
    admin_last_name VARCHAR(128),
    admin_password_hash VARCHAR(512),
    admin_salt CHAR(256)
);

-- Table: Drivers
CREATE TABLE test.Drivers (
    driver_id SERIAL PRIMARY KEY,
    driver_first_name VARCHAR(128),
    driver_last_name VARCHAR(128),
    driver_password_hash VARCHAR(512),
    driver_salt CHAR(256),
    driver_is_delivering BOOLEAN,
    driver_phone VARCHAR(16)
);

-- Table: Orders
CREATE TABLE test.Orders (
    order_id SERIAL PRIMARY KEY,
    order_customer_id INTEGER,
    order_state INTEGER,
    order_date DATE,
    order_time TIME,
    order_is_paid BOOLEAN,
    order_is_prepared BOOLEAN,
    FOREIGN KEY (order_customer_id) REFERENCES test.Customers(customer_id)
);

-- Table: Items
CREATE TABLE test.Items (
    item_id SERIAL PRIMARY KEY,
    item_name VARCHAR(128),
    item_price FLOAT(24) CHECK (item_price >= 0),
    item_type VARCHAR(32),
    item_description VARCHAR(256),
    item_stock INTEGER CHECK (item_stock >= 0),
    item_in_menu BOOLEAN DEFAULT false
);

-- Table: Orders_Items 
CREATE TABLE test.Order_Items (
    order_id INTEGER,
    item_id INTEGER,
    item_quantity INTEGER CHECK (item_quantity > 0),
    PRIMARY KEY (order_id, item_id),
    FOREIGN KEY (order_id) REFERENCES test.Orders(order_id),
    FOREIGN KEY (item_id) REFERENCES test.Items(item_id)
);

-- Table: Bundles
CREATE TABLE test.Bundles (
    bundle_id SERIAL PRIMARY KEY,
    bundle_name VARCHAR(128),
    -- bundle reduction: if 20% off, it's 20. Python App handles calculations.
    bundle_reduction INTEGER CHECK (bundle_reduction > 0 AND bundle_reduction < 100),
    bundle_description VARCHAR(256),
    bundle_availability_start_date DATE,
    bundle_availability_end_date DATE CHECK (bundle_availability_end_date > bundle_availability_start_date)
);

-- Table: Bundle_Items
CREATE TABLE test.Bundle_Items (
    bundle_id INTEGER,
    item_id INTEGER,
    item_quantity INTEGER CHECK (item_quantity > 0),
    PRIMARY KEY (bundle_id, item_id),
    FOREIGN KEY (bundle_id) REFERENCES test.Bundles(bundle_id),
    FOREIGN KEY (item_id) REFERENCES test.Items(item_id)
);

-- Table: Order_Bundles
CREATE TABLE test.Order_Bundles (
    order_id INTEGER,
    bundle_id INTEGER,
    bundle_quantity INTEGER CHECK (bundle_quantity > 0),
    PRIMARY KEY (order_id, bundle_id),
    FOREIGN KEY (order_id) REFERENCES test.Orders(order_id),
    FOREIGN KEY (bundle_id) REFERENCES test.Bundles(bundle_id)
);


-- Table: Deliveries
CREATE TABLE test.Deliveries (
    delivery_id_order INTEGER,
    delivery_id_driver INTEGER,
    delivery_state INTEGER,
    PRIMARY KEY (delivery_id_order, delivery_id_driver),
    FOREIGN KEY (delivery_id_order) REFERENCES test.Orders(order_id),
    FOREIGN KEY (delivery_id_driver) REFERENCES test.Drivers(driver_id)
);



INSERT INTO Addresses (address_number, address_street, address_city, address_postal_code, address_country)
VALUES
(7, 'Contour Antoine de Saint-Exupery', 'Bruz', '35170', 'France'),
(95, 'Rue Papu', 'Rennes', '35000', 'France'),
(8, 'Avenue de la Brocéliande', 'Chartres-de-Bretagne', '35131', 'France');

INSERT INTO Customers (customer_first_name, customer_last_name, customer_phone, customer_email, customer_password_hash, customer_salt, customer_address_id)
VALUES
('Ronan', 'LE SAOUT', '0612345678', 'ronan.le-saout@email.com', 'hash1', 'salt1', 1),
('Mental', 'CRASHOUT', '0699988777', 'aled.prozaczopixan@email.com', 'hash2', 'salt2', 2),
('Plus', 'DIDIER', '0699988777', 'pas.dinspi@email.com', 'hash3', 'salt3', 3);

INSERT INTO Admins (admin_first_name, admin_last_name, admin_password_hash, admin_salt)
VALUES
('Admin', 'INSEE', 'hash_admin1', 'salt_admin1');

INSERT INTO Drivers (driver_first_name, driver_last_name, driver_password_hash, driver_salt, driver_is_delivering, driver_phone)
VALUES
('Lewis', 'HAMILTON', 'hash_driver1', 'salt_driver1', false, '0707070707'),
('Max', 'VERSTAPPEN', 'hash_driver2', 'salt_driver2', true, '0606060606');

INSERT INTO Items (item_name, item_price, item_type, item_description, item_stock, item_in_menu)
VALUES
('Galette-Saucisse', 4.5, 'Plat', 'La fameuse galette-saucisse de l''EJR', 50, true),
('Coca-Cola 33cl', 0.5, 'Boisson', 'Canette de Coca-Cola', 100, true),
('Tiramisu', 2.0, 'Dessert', 'Tiramisu-holic', 30, true),
('Banh-Mi', 4.5, 'Plat', 'Sandwich vietnamien', 40, false);

INSERT INTO Bundles (bundle_name, bundle_reduction, bundle_description, bundle_availability_start_date, bundle_availability_end_date)
VALUES
('Menu Galette-Saucisse', 6, 'Galette-Saucisse + Boisson + Dessert', '2025-01-01', '2025-12-31');

INSERT INTO Bundle_Items (bundle_id, item_id, item_quantity)
VALUES
(1, 1, 1),
(1, 2, 1),
(1, 3, 1);

INSERT INTO Orders (order_customer_id, order_state, order_date, order_time, order_is_paid, order_is_prepared)
VALUES
(1, 1, '2025-10-21', '12:30:00', true, true),
(2, 0, '2025-10-21', '13:00:00', false, false);

INSERT INTO Order_Items (order_id, item_id, item_quantity)
VALUES
(1, 1, 1),  
(1, 2, 1), 
(2, 4, 2); 

INSERT INTO Order_Bundles (order_id, bundle_id, bundle_quantity)
VALUES
(1, 1, 1);  

INSERT INTO Deliveries (delivery_id_order, delivery_id_driver, delivery_state)
VALUES
(1, 2, 1), 
(2, 1, 0); 
