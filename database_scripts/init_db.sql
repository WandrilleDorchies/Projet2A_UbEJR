-- Table: Addresses
CREATE TABLE Addresses (
    address_id INTEGER PRIMARY KEY,
    number INT NOT NULL,
    street VARCHAR(256) NOT NULL,
    city VARCHAR(128) NOT NULL,
    postal_code VARCHAR(8) NOT NULL,
    country VARCHAR(128) NOT NULL
);

-- Table: Customers
CREATE TABLE Customers (
    customer_id INTEGER PRIMARY KEY,
    first_name VARCHAR(128),
    last_name VARCHAR(128),
    phone VARCHAR(16),
    mail VARCHAR(128),
    password_hash VARCHAR(512) NOT NULL,
    address_id INTEGER,
    FOREIGN KEY (address_id) REFERENCES Address(address_id)
);

-- Table: Admins
CREATE TABLE Admins (
    admin_id INTEGER PRIMARY KEY,
    first_name VARCHAR(128),
    last_name VARCHAR(128),
    password_hash VARCHAR(512)
);

-- Table: Drivers
CREATE TABLE Drivers (
    driver_id INTEGER PRIMARY KEY,
    first_name VARCHAR(128),
    last_name VARCHAR(128),
    password_hash VARCHAR(512),
    is_delivering BOOLEAN,
    phone VARCHAR(16)
);

-- Table: Orders
CREATE TABLE Orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    state INTEGER,
    order_date DATE,
    order_time TIME,
    is_paid BOOLEAN,
    is_prepared BOOLEAN,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);

-- Table: Items
CREATE TABLE Items (
    item_id INTEGER PRIMARY KEY,
    name VARCHAR(128),
    price DOUBLE CHECK (price >= 0),
    item_type VARCHAR(32),
    description VARCHAR(256),
    stock INTEGER CHECK (stock >= 0)
);

-- Table: Order_Details 
CREATE TABLE Order_Details (
    order_id INTEGER,
    item_id INTEGER,
    quantity INTEGER NOT NULL,
    price DOUBLE CHECK (price >= 0),
    PRIMARY KEY (order_id, item_id),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (item_id) REFERENCES Item(item_id)
);

-- Table: Deliveries
CREATE TABLE Deliveries (
    id_order INTEGER,
    id_driver INTEGER,
    state INTEGER,
    PRIMARY KEY (id_order, id_driver),
    FOREIGN KEY (id_order) REFERENCES Orders(order_id),
    FOREIGN KEY (id_driver) REFERENCES Drivers(driver_id)
);
