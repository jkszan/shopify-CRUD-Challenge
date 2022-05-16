-- Using an enum for city may not be a great decision if there are going to be a lot of updates on the table as only the table owner
-- can add new values. A reference table with city_name as PK would be better
CREATE TYPE city AS ENUM(
    'Ottawa',
    'Halifax',
    'Toronto',
    'Vancouver',
    'Edmonton'
);

CREATE TYPE condition_type AS ENUM(
    'New',
    'Used',
    'Refurbished'
);

CREATE TABLE IF NOT EXISTS address(
    address_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    address_country text NOT NULL,
    address_state text NOT NULL,
    address_city city NOT NULL,
    street_name text NOT NULL,
    house_number int NOT NULL,
    apt_specifier text,
    postal_code text NOT NULL
);

-- Owner could be a reference to a user or an organization in a final implementation
CREATE TABLE IF NOT EXISTS inventory(
    inventory_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    address_id int REFERENCES address(address_id) NOT NULL,
    inventory_name text NOT NULL UNIQUE,
    owner text,
    size int DEFAULT 0
);

-- In some applications, having product_name unique may cause issues. It's possible to switch this to UNIQUE(product_name, product_brand)
-- if that better fits design
CREATE TABLE IF NOT EXISTS product(
    product_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_name text NOT NULL UNIQUE,
    product_brand text NOT NULL,
    product_description text
    );

-- inventory_id may be null to allow for historical data storage
CREATE TABLE IF NOT EXISTS item(
    serial_number int PRIMARY KEY,
    inventory_id int REFERENCES inventory(inventory_id),
    product_id int REFERENCES product(product_id) NOT NULL,
    condition condition_type DEFAULT 'New' NOT NULL,
    damage_description text
);

CREATE OR REPLACE FUNCTION update_size() RETURNS trigger AS $update_size$
    BEGIN
        UPDATE inventory SET size = (Select Count(*) FROM item WHERE inventory_id in (NEW.inventory_id, OLD.inventory_id)) WHERE inventory_id in (OLD.inventory_id,NEW.inventory_id);
        Return NEW;
    END;
$update_size$ LANGUAGE plpgsql;

CREATE TRIGGER update_size AFTER INSERT OR DELETE ON item FOR EACH ROW EXECUTE FUNCTION update_size();