
INSERT INTO project.Addresses (address_number, address_street, address_city, address_postal_code, address_country)
VALUES
(7, 'Contour Antoine de Saint-Exupery', 'Bruz', '35170', 'France'),
(95, 'Rue Papu', 'Rennes', '35000', 'France'),
(8, 'Avenue de la Brocéliande', 'Chartres-de-Bretagne', '35131', 'France');

INSERT INTO project.Customers (customer_first_name, customer_last_name, customer_phone, customer_mail, customer_password_hash, customer_salt, customer_address_id)
VALUES
('Ronan', 'LE SAOUT', '0612345678', 'ronan.le-saout@email.com', '877689f07988660e66e3503b342a4cb46edc802906ad007788468b4b5be83e9e', 'f8b1e585ae4e7090dbb885756b3b1b67ab1ca291f623d5881e02bba56167efa79bef1957c537ec58d8046437cdf911c8e0fef5b14d332acf231429ca3fff9309427d91a9feec3a00728de4117aad7e57243a9ef554e2e2fd79a5f9184ff12ec655a001a31f6753b8366cf42a821dca9e88cf2ad64022a40853238a84da599e5b', 1),
('Mental', 'CRASHOUT', '0699988777', 'aled.prozaczopixan@email.com', 'hash2', 'salt2', 2),
('Plus', 'DIDIER', '0699988777', 'pas.dinspi@email.com', 'hash3', 'salt3', 3);

INSERT INTO project.Admins (username, admin_first_name, admin_last_name, admin_password_hash, admin_salt)
VALUES
('adminsee', 'Admin', 'INSEE', '2c91f4ac460ae560d41584d9e903b8f5a049ef85aa1d223a0ce7e4ae7ce76338', '4b58756f1be2e86d5f6a8325afbc7dbf210d46623ca78f46e804c1fa9ff31538b9482ea58f1321e499aeb8ddf96c09cc286b608ddbb48a4b82724854f56cdb5e879b51c3cc9312c3c81fc0352fd16afce929c4a59ee63972d91eb1037aeef863b91fd7cbcbb74ea8cd48f36b077494daa410f59756a91a40e70bd5b5f21b117f');

INSERT INTO project.Drivers (driver_first_name, driver_last_name, driver_password_hash, driver_salt, driver_is_delivering, driver_phone)
VALUES
('Lewis', 'HAMILTON', '2d9c2c8ed880bdeddf710231bcad9c30773beea10e54cc115f29e1956e240278', 'c9cf4540618ec20161eb83f8ea4a0a85fff464ac510992b72d41a0e0ed6197654678bf19fd1d9bdeaafd741f77971b34dd8c90b41e659b51f6bdb8fb18b7564078d8fcb27cf77ad592423f096b6d8d6f9b9ee672c5a15c9a7964ca7e7f9bb65a9b2ee08bad7ee1746706e4043ebbec0b0038491c4b2589147fb5e1a190c53b74', false, '0632659875'),
('Max', 'VERSTAPPEN', 'hash_driver2', 'salt_driver2', true, '0606060606');

INSERT INTO project.Items (orderable_id, item_name, item_price, item_type, item_description, item_stock)
VALUES
(1, 'Galette-Saucisse', 4.5, 'Main course', 'La fameuse galette-saucisse de l''EJR', 50),
(2, 'Coca-Cola 33cl', 0.5, 'Drink', 'Canette de Coca-Cola', 100),
(3, 'Tiramisu', 2.0, 'Dessert', 'Tiramisu-holic', 30),
(4, 'Banh-Mi', 4.5, 'Main course', 'Sandwich vietnamien', 40);

INSERT INTO project.Bundles (orderable_id, bundle_name, bundle_reduction, bundle_description, bundle_availability_start_date, bundle_availability_end_date)
VALUES
(5, 'Menu Galette-Saucisse', 30, 'Galette-Saucisse + Boisson + Dessert', '2025-01-01', '2025-12-31'),
(6, 'Menu Accompagnement', 10, 'Boisson + Dessert', '2025-01-01', '2025-12-31');

INSERT INTO project.Bundle_Items (bundle_id, item_id, item_quantity)
VALUES
(1, 1, 1),
(1, 2, 1),
(1, 3, 1),
(2, 3, 1),
(2, 2, 1);

INSERT INTO Orderables (orderable_type, is_in_menu)
VALUES
('item', true),
('item', true),
('item', true),
('item', false),
('bundle', false),
('bundle', true);

INSERT INTO Orders (order_customer_id, order_state, order_created_at, order_paid_at)
VALUES 
(1, 4, '2025-10-21 12:30:00', '2025-10-21 13:0:00'),
(2, 0, '2025-10-21 12:30:00', NULL),
(3, 4, '2025-10-22 12:30:00', '2025-10-21 13:0:00'),
(1, 1, '2025-10-22 12:30:00', '2025-10-21 13:0:00'),
(2, 4, '2025-10-23 12:30:00', '2025-10-21 13:0:00'),
(3, 2, '2025-10-23 12:30:00', '2025-10-21 13:0:00'),
(3, 2, '2025-10-23 12:30:00', '2025-10-21 13:0:00'),
(1, 1, '2025-10-24 12:30:00', '2025-10-21 13:0:00'),
(2, 0, '2025-10-24 12:30:00', NULL),
(3, 5, '2025-10-24 12:30:00', NULL);


INSERT INTO Order_contents (order_id, orderable_id, orderable_quantity)
VALUES
(1, 1, 1),
(1, 2, 1),
(1, 5, 1),
(2, 4, 2),
(3, 3, 2),
(4, 5, 1),
(5, 1, 1),
(5, 2, 1),
(6, 4, 1),
(7, 1, 1),
(7, 2, 1), 
(8, 5, 2), 
(9, 4, 1), 
(9, 3, 1), 
(10, 6, 1);
INSERT INTO Deliveries (delivery_order_id, delivery_driver_id, delivery_state)
VALUES
(1, 2, 2),
(3, 1, 2), 
(5, 2, 2);