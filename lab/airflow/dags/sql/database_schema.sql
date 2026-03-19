-- PostgreSQL Database Schema for Orders, Items, and Customers
-- Created for Curso ETL - BIT

-- Create customers table
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(50),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create items table
CREATE TABLE items (
    item_id SERIAL PRIMARY KEY,
    description VARCHAR(500) NOT NULL,
    list_price INTEGER NOT NULL CHECK (list_price >= 0)
);

-- Create orders table
CREATE TABLE orders (
    invoice_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    price INTEGER NOT NULL CHECK (price >= 0),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES items(item_id) ON DELETE CASCADE
);

-- Add indexes for better query performance
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_item_id ON orders(item_id);
CREATE INDEX idx_orders_invoice_id ON orders(invoice_id);
CREATE INDEX idx_orders_order_date ON orders(order_date);

-- Optional: Add some sample data
INSERT INTO customers (name, email, phone, address) VALUES
    ('John Doe', 'john.doe@email.com', '555-0101', '123 Main St, Anytown, USA'),
    ('Jane Smith', 'jane.smith@email.com', '555-0102', '456 Oak Ave, Somewhere, USA'),
    ('Bob Johnson', 'bob.johnson@email.com', '555-0103', '789 Pine Rd, Elsewhere, USA');

INSERT INTO items (description, list_price) VALUES
    ('Wireless Mouse', 29),
    ('Mechanical Keyboard', 89),
    ('USB-C Hub', 45),
    ('Monitor Stand', 35),
    ('Laptop Sleeve', 25);

INSERT INTO orders (invoice_id, customer_id, item_id, price, quantity) VALUES
    (1001, 1, 1, 29, 2),
    (1001, 1, 3, 45, 1),
    (1002, 2, 2, 89, 1),
    (1002, 2, 4, 35, 1),
    (1003, 3, 5, 25, 3),
    (1003, 3, 1, 29, 1);
