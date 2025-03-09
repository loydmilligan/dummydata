"""
Configuration settings for the DummyData package.
"""

import os
from pathlib import Path

# Base directory structure
BASE_DIR = Path("fuel_orders_data")
CSV_DIR = BASE_DIR / "csv_data"
PRODUCT_DIR = CSV_DIR / "products"
CUSTOMER_DIR = CSV_DIR / "customers"
ORDER_DIR = CSV_DIR / "orders"
LOG_DIR = Path("logs")

# Default file paths
PRODUCTS_FILE = PRODUCT_DIR / "products.csv"
CUSTOMERS_FILE = CUSTOMER_DIR / "customers.csv"
SEQUENCES_FILE = CUSTOMER_DIR / "customer_sequences.csv"
SINGLE_OUTPUT_FILE = Path("customer_orders.csv")

# Data generation defaults
DEFAULT_NUM_CUSTOMERS = 20
DEFAULT_ORDERS_PER_MONTH = 50
DEFAULT_LOOKBACK_YEARS = 5

# Order headers (CSV column names)
ORDER_HEADERS = [
    "CustomerName", "Order#", "Seq", "Seq Desc", "PO #", "PO Req", "Date", 
    "Status", "Invoice#", "Invoice Date", "BOL", "Product", "Unit Price", 
    "Quantity", "Product", "Charges", "Special Charges", "Total Taxes", 
    "Total", "Exempt Taxes", "Total Cost", "Margin Per Gallon"
]

# Product headers (CSV column names)
PRODUCT_HEADERS = [
    "Product Code", "ProductName", "Abbrev", "Product Group", "CycleCode", 
    "Method", "Account Group", "Tax Profile", "Tax Group", "Packaging", 
    "Unit of Measure", "Status", "Stocked", "UPC Code"
]

# Customer headers (CSV column names)
CUSTOMER_HEADERS = [
    "CustomerID", "CustomerName", "Address", "City", "State", "Zip", 
    "ContactName", "Phone", "Email"
]

# Sequence headers (CSV column names)
SEQUENCE_HEADERS = ["CustomerID", "SequenceID", "SequenceDesc"]

# Sample product data
SAMPLE_PRODUCTS = [
    ["REG001", "Regular Gasoline", "REG", "Fuel", "C1", "Direct", "Retail", "T1", "Fuel Tax", "Bulk", "Gallon", "Active", "Yes", "0123456789"],
    ["PRM001", "Premium Gasoline", "PRM", "Fuel", "C1", "Direct", "Retail", "T1", "Fuel Tax", "Bulk", "Gallon", "Active", "Yes", "1234567890"],
    ["DSL001", "Diesel", "DSL", "Fuel", "C2", "Direct", "Commercial", "T1", "Fuel Tax", "Bulk", "Gallon", "Active", "Yes", "2345678901"],
    ["KRS001", "Kerosene", "KRS", "Fuel", "C2", "Direct", "Commercial", "T1", "Fuel Tax", "Bulk", "Gallon", "Active", "Yes", "3456789012"],
    ["ETH001", "Ethanol", "ETH", "Fuel", "C3", "Direct", "Retail", "T2", "Alt Fuel Tax", "Bulk", "Gallon", "Active", "Yes", "4567890123"],
    ["BIO001", "Biodiesel", "BIO", "Fuel", "C3", "Direct", "Commercial", "T2", "Alt Fuel Tax", "Bulk", "Gallon", "Active", "Yes", "5678901234"],
    ["E85001", "E85 Fuel", "E85", "Fuel", "C3", "Direct", "Retail", "T2", "Alt Fuel Tax", "Bulk", "Gallon", "Active", "Yes", "6789012345"],
    ["DNF001", "Diesel No Freeze", "DNF", "Fuel", "C2", "Direct", "Commercial", "T1", "Fuel Tax", "Bulk", "Gallon", "Active", "Yes", "7890123456"],
    ["JET001", "Jet Fuel", "JET", "Fuel", "C4", "Direct", "Aviation", "T3", "Aviation Tax", "Bulk", "Gallon", "Active", "Yes", "8901234567"],
    ["AVG001", "Aviation Gasoline", "AVG", "Fuel", "C4", "Direct", "Aviation", "T3", "Aviation Tax", "Bulk", "Gallon", "Active", "Yes", "9012345678"]
]

# Standard charges for products
STANDARD_CHARGES = {
    "Labor Charge": 85.00,
    "Pump Fee": 45.00,
    "After Hours Fee": 125.00,
    "Weekend Delivery": 75.00,
    "Rush Delivery": 95.00
}

# Create directory structure
def create_directories():
    """Create the necessary directory structure for data files."""
    for directory in [BASE_DIR, CSV_DIR, PRODUCT_DIR, CUSTOMER_DIR, ORDER_DIR, LOG_DIR]:
        os.makedirs(directory, exist_ok=True)