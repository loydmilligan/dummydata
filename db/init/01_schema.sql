-- PostgreSQL schema for petroleum sales data
-- This is a placeholder for future database integration

-- Products table
CREATE TABLE IF NOT EXISTS products (
    product_id SERIAL PRIMARY KEY,
    product_code VARCHAR(10) NOT NULL UNIQUE,
    product_name VARCHAR(100) NOT NULL,
    abbrev VARCHAR(10),
    product_group VARCHAR(50),
    cycle_code VARCHAR(10),
    method VARCHAR(20),
    account_group VARCHAR(50),
    tax_profile VARCHAR(20),
    tax_group VARCHAR(50),
    packaging VARCHAR(30),
    unit_of_measure VARCHAR(20) DEFAULT 'Gallon',
    status VARCHAR(20) DEFAULT 'Active',
    stocked VARCHAR(5) DEFAULT 'Yes',
    upc_code VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Customers table
CREATE TABLE IF NOT EXISTS customers (
    customer_id SERIAL PRIMARY KEY,
    customer_code VARCHAR(20) NOT NULL UNIQUE,
    customer_name VARCHAR(100) NOT NULL,
    address VARCHAR(200),
    city VARCHAR(100),
    state VARCHAR(2),
    zip_code VARCHAR(10),
    contact_name VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Customer sequences (delivery locations)
CREATE TABLE IF NOT EXISTS customer_sequences (
    sequence_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    sequence_number INTEGER NOT NULL,
    description VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(customer_id, sequence_number)
);

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    order_id SERIAL PRIMARY KEY,
    order_number VARCHAR(30) NOT NULL UNIQUE,
    customer_id INTEGER REFERENCES customers(customer_id),
    sequence_id INTEGER REFERENCES customer_sequences(sequence_id),
    po_required BOOLEAN DEFAULT FALSE,
    po_number VARCHAR(30),
    order_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'Completed',
    invoice_number VARCHAR(30),
    invoice_date DATE,
    bol VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Order line items
CREATE TABLE IF NOT EXISTS order_items (
    item_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id),
    product_id INTEGER REFERENCES products(product_id),
    unit_price DECIMAL(10, 2) NOT NULL,
    quantity INTEGER NOT NULL,
    additional_product VARCHAR(100),
    charges DECIMAL(10, 2),
    special_charges DECIMAL(10, 2),
    total_taxes DECIMAL(10, 2),
    exempt_taxes DECIMAL(10, 2),
    total DECIMAL(10, 2),
    total_cost DECIMAL(10, 2),
    margin_per_gallon DECIMAL(10, 3),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_order_date ON orders(order_date);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);
CREATE INDEX idx_customer_sequences_customer_id ON customer_sequences(customer_id);