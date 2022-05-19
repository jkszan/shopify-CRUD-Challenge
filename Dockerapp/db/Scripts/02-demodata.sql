-- This script gives us some test values to play with, a user can now edit, delete, add, and read items using the predefined
-- products and location

INSERT INTO product(product_name, product_brand, product_description)
VALUES ('Pixel 6', 'Google', 'Dual rear camera system: 50 MP wide 12 MP ultrawide'),
       ('Rambler® 30 oz Tumbler', 'Yeti', 'Iced coffee, sweet tea, lemonade, water, you name it, you’re set. Fits in most cupholders.'),
       ('Anti-Dust Chalk Sticks', 'Crayola', 'Crayola Anti-Dust Chalk sticks keep dust to a minimum and are perfect for writing and drawing on blackboards. Available in white.');

WITH addressID AS (INSERT INTO address(address_country, address_state, address_city, street_name, house_number, postal_code)
VALUES ('Canada', 'ON', 'Ottawa', 'O''Connor St', 151, 'K2P 2L8') RETURNING address_id
)
INSERT INTO inventory(address_id, inventory_name, owner) VALUES ((SELECT address_id from addressID), 'Backend Storage', 'Alex Placeholder');

WITH addressID AS (INSERT INTO address(address_country, address_state, address_city, street_name, apt_specifier, house_number, postal_code)
VALUES ('Canada', 'ON', 'Ottawa', 'Laurier Ave W', '#500', 234, 'K2P 2L8') RETURNING address_id
)
INSERT INTO inventory(address_id, inventory_name, owner) VALUES ((SELECT address_id from addressID), 'Frontend Storage', 'Jerry Placeholder');


WITH addressID AS (INSERT INTO address(address_country, address_state, address_city, street_name, house_number, postal_code)
VALUES ('Canada', 'BC', 'Vancouver', 'Dunsmuir Street', 1055, 'V7X 1L3') RETURNING address_id
)
INSERT INTO inventory(address_id, inventory_name, owner) VALUES ((SELECT address_id from addressID), 'Vancouver Storage', 'Linda Placeholder');


-- Bad practice to use the ids statically like this, but given that its a startup script we can be relatively sure that those are stable
INSERT INTO item(serial_number, inventory_id, product_id, condition, damage_description) VALUES
    (2312412, 2, 1, 'Refurbished', 'Like new'),
    (2424444, 3, 2, 'Used', 'Weak magnet'),
    (2142444, 1, 3, 'New', NULL);