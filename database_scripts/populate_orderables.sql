INSERT INTO project.Orderables (orderable_type, is_in_menu)
VALUES
    ('item', true),
    ('item', true),
    ('item', true),
    ('item', true),
    ('item', false),
    ('item', false),
    ('bundle', true),
    ('bundle', true),
    ('bundle', true);

INSERT INTO project.Items (
    orderable_id, item_name, item_price, item_type,
    item_description, item_stock
)
VALUES
    (1, 'Galette Saucisse', 4.90, 'Main course',
        'La meilleure galette saucisse de Rennes', 120),

    (2, 'Fajitas VG', 4, 'Main course',
        'Des fajitas au stick de mozzarella frits', 200),

    (3, 'Coca-Cola 33cl', 21.50, 'Drink',
        'Canette de Coca-Cola', 300),

    (4, 'Bahn-Mi', 3.9, 'Main course',
        'Sandwich vietnamien aux crudités et poulet mariné', 75),

    (5, 'Tiramisu', 3, 'Dessert',
        'Tiramisu-holic', 40),

    (6, 'Chips', 1, 'Side dish',
        'Des chips natures', 250);


INSERT INTO project.Bundles (
    orderable_id, bundle_name, bundle_reduction, bundle_description,
    bundle_availability_start_date, bundle_availability_end_date
)
VALUES
    (7, 'Ah t''as faim', 15,
        '3 Galettes saucisses, 1 paquet de chips et une boisson',
        '2025-01-01', '2025-12-31'),

    (8, 'La totale', 20,
        'Un Bahn-Mi, un paquet de chips, un tiramisu et une boisson',
        '2025-01-01', '2025-12-31'),

    (9, 'Mejico', 20,
        'Une fajitas, 10 Cocas et un paquet de chips',
        '2025-01-01', '2025-12-31');


INSERT INTO project.Bundle_Items (bundle_id, item_id, item_quantity)
VALUES
    (1, 1, 3),
    (1, 6, 1), 
    (1, 3, 1),

    (2, 3, 1),  
    (2, 4, 1),  
    (2, 5, 1),
    (2, 6, 1),
 
    (3, 2, 1),  
    (3, 3, 10),  
    (3, 6, 1);  
