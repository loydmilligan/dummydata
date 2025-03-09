"""
Generator for synthetic petroleum data including products, customers, and orders.
"""

import os
import csv
import random
import calendar
import datetime
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Union

from faker import Faker

from dummydata.config import (
    PRODUCT_HEADERS, CUSTOMER_HEADERS, SEQUENCE_HEADERS, ORDER_HEADERS,
    SAMPLE_PRODUCTS, STANDARD_CHARGES, DEFAULT_NUM_CUSTOMERS
)
from dummydata.models import Product, Customer, Sequence, Order
from dummydata.utils.csv_handler import CSVHandler

# Initialize Faker for generating random data
fake = Faker()


class DataGenerator:
    """
    Generates synthetic data for petroleum products, customers, and orders.
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize the data generator.
        
        Args:
            logger: Logger instance (optional)
        """
        self.logger = logger or logging.getLogger(__name__)
        self.csv_handler = CSVHandler()
    
    def generate_products(self, products_file: Union[str, Path], force_new: bool = False) -> List[Product]:
        """
        Generate product data or read from existing file.
        
        Args:
            products_file: Path to products CSV file
            force_new: Whether to force creation of new products even if file exists
            
        Returns:
            List of Product objects
        """
        # If the file doesn't exist or force_new is True, create new products
        if force_new or not self.csv_handler.file_exists(products_file):
            self.logger.info(f"Creating new products data in {products_file}")
            products = self._create_sample_products()
            
            # Convert products to rows
            product_rows = [product.to_row() for product in products]
            
            # Write products to CSV
            success = self.csv_handler.write_csv(products_file, PRODUCT_HEADERS, product_rows)
            if not success:
                self.logger.error(f"Failed to write products to {products_file}")
                raise IOError(f"Failed to write products to {products_file}")
        else:
            self.logger.info(f"Reading products from {products_file}")
            # Read existing products
            try:
                product_rows = self.csv_handler.read_csv(products_file)
                products = [Product.from_row(row) for row in product_rows if len(row) >= 2]
            except Exception as e:
                self.logger.error(f"Error reading products from {products_file}: {e}")
                raise
        
        if not products:
            self.logger.error(f"No valid products found in {products_file}")
            raise ValueError(f"No valid products found in {products_file}")
        
        self.logger.info(f"Successfully loaded {len(products)} products")
        return products
    
    def _create_sample_products(self) -> List[Product]:
        """
        Create a list of sample products.
        
        Returns:
            List of Product objects
        """
        products = []
        for row in SAMPLE_PRODUCTS:
            product = Product.from_row(row)
            products.append(product)
        
        return products
    
    def generate_customers(
        self,
        customers_file: Union[str, Path],
        sequences_file: Union[str, Path],
        num_customers: int = DEFAULT_NUM_CUSTOMERS,
        force_new: bool = False
    ) -> List[Customer]:
        """
        Generate customer data with sequences or read from existing files.
        
        Args:
            customers_file: Path to customers CSV file
            sequences_file: Path to sequences CSV file
            num_customers: Number of customers to generate
            force_new: Whether to force creation of new customers even if files exist
            
        Returns:
            List of Customer objects with sequences
        """
        # Check if we need to create new customer data
        if force_new or not self.csv_handler.file_exists(customers_file) or not self.csv_handler.file_exists(sequences_file):
            self.logger.info(f"Creating new customer data in {customers_file} and {sequences_file}")
            customers = self._create_sample_customers(num_customers)
            
            # Prepare customer and sequence data for CSV
            customer_rows = []
            sequence_rows = []
            
            for i, customer in enumerate(customers):
                # Add customer row
                customer_rows.append(customer.to_row())
                
                # Add sequence rows
                for seq in customer.sequences:
                    sequence_rows.append([
                        customer.customer_id,
                        seq.seq_id,
                        seq.description
                    ])
            
            # Write customers to CSV
            customer_success = self.csv_handler.write_csv(customers_file, CUSTOMER_HEADERS, customer_rows)
            sequence_success = self.csv_handler.write_csv(sequences_file, SEQUENCE_HEADERS, sequence_rows)
            
            if not customer_success or not sequence_success:
                self.logger.error(f"Failed to write customer data to CSV files")
                raise IOError(f"Failed to write customer data to CSV files")
                
        else:
            self.logger.info(f"Reading customers from {customers_file} and {sequences_file}")
            # Read existing customers and sequences
            try:
                # Read customers
                customer_rows = self.csv_handler.read_csv(customers_file)
                customers_dict = {}
                
                for row in customer_rows:
                    if len(row) >= 2:
                        customer = Customer.from_row(row)
                        customers_dict[customer.customer_id] = customer
                
                # Read sequences
                sequence_rows = self.csv_handler.read_csv(sequences_file)
                
                for row in sequence_rows:
                    if len(row) >= 3:
                        customer_id = row[0]
                        if customer_id in customers_dict:
                            seq_id = int(row[1])
                            description = row[2]
                            customers_dict[customer_id].add_sequence(seq_id, description)
                
                # Convert to list of customers with sequences
                customers = [c for c in customers_dict.values() if c.has_sequences()]
                
            except Exception as e:
                self.logger.error(f"Error reading customer data: {e}")
                raise
        
        if not customers:
            self.logger.error("No valid customers found with sequences")
            raise ValueError("No valid customers found with sequences")
        
        self.logger.info(f"Successfully loaded {len(customers)} customers with sequences")
        return customers
    
    def _create_sample_customers(self, num_customers: int) -> List[Customer]:
        """
        Create sample customers with sequences.
        
        Args:
            num_customers: Number of customers to create
            
        Returns:
            List of Customer objects with sequences
        """
        customers = []
        
        for i in range(1, num_customers + 1):
            customer_id = f"CUST{i:04d}"
            
            # Create customer
            customer = Customer(
                customer_id=customer_id,
                name=fake.company(),
                address=fake.street_address(),
                city=fake.city(),
                state=fake.state_abbr(),
                zip_code=fake.zipcode(),
                contact_name=fake.name(),
                phone=fake.phone_number(),
                email=fake.email()
            )
            
            # Generate 1-5 delivery locations (sequences) for each customer
            num_sequences = random.randint(1, 5)
            for j in range(1, num_sequences + 1):
                sequence_desc = random.choice([
                    f"Location {j}", 
                    f"Facility {j}", 
                    f"Building {j}", 
                    f"Warehouse {j}", 
                    f"Tank {j}", 
                    f"Station {j}"
                ])
                customer.add_sequence(j, sequence_desc)
            
            customers.append(customer)
        
        return customers
    
    def generate_date_in_month(self, year: int, month: int) -> datetime.date:
        """
        Generate a random date within a specific month and year.
        
        Args:
            year: Year
            month: Month (1-12)
            
        Returns:
            Random date within the specified month
        """
        # Get the number of days in the specified month
        num_days = calendar.monthrange(year, month)[1]
        
        # Generate a random day
        day = random.randint(1, num_days)
        
        # Create the date object
        date_obj = datetime.date(year, month, day)
        
        return date_obj
    
    def generate_orders(
        self,
        products: List[Product],
        customers: List[Customer],
        year: int,
        month: int,
        num_orders: int = 50
    ) -> List[Order]:
        """
        Generate order data for a specific month and year.
        
        Args:
            products: List of available products
            customers: List of customers with sequences
            year: Year for orders
            month: Month for orders (1-12)
            num_orders: Number of orders to generate
            
        Returns:
            List of Order objects
        """
        orders = []
        
        # Generate dates for the month in chronological order
        dates = []
        for _ in range(num_orders):
            dates.append(self.generate_date_in_month(year, month))
        
        # Sort dates chronologically
        dates.sort()
        
        # Most orders should be completed
        statuses_weighted = ["Completed"] * 90 + ["In Progress"] * 5 + ["Pending"] * 5
        
        # Standard charges
        standard_charge_names = list(STANDARD_CHARGES.keys())
        
        # Month and year as string for order numbers
        month_year_str = f"{year}{month:02d}"
        
        for i in range(num_orders):
            # Select a random customer and one of their sequences
            customer = random.choice(customers)
            sequence = random.choice(customer.sequences)
            
            # Generate order number
            order_num = f"ORD-{month_year_str}-{i+1:04d}"
            
            # Determine if PO is required (60% chance)
            po_req = random.choice(["Yes"] * 60 + ["No"] * 40)
            
            # Only fill PO if required
            po_num = ""
            if po_req == "Yes":
                po_num = f"PO-{month_year_str}-{i+1:03d}"
            
            # Use the chronological date
            date_obj = dates[i]
            
            # Select order status
            status = random.choice(statuses_weighted)
            
            # All completed orders should have invoice details
            invoice_num = ""
            invoice_date = None
            if status == "Completed":
                invoice_num = f"INV-{month_year_str}-{i+1:04d}"
                
                # Invoice date is usually the day after delivery
                invoice_date_obj = date_obj + datetime.timedelta(days=1)
                
                # If invoice date is in the next month, keep it in the current month
                if invoice_date_obj.month != month:
                    invoice_date_obj = date_obj
                    
                invoice_date = invoice_date_obj
            
            # Generate Bill of Lading
            bol = f"BOL-{month_year_str}-{i+1:04d}"
            
            # Select a random product
            product = random.choice(products)
            unit_price = product.get_random_price()
            
            # Generate quantity between 200-3500, divisible by 10
            quantity = random.randint(20, 350) * 10
            
            # Only about 10% of orders should have additional charges
            has_additional_charges = random.random() < 0.10
            
            additional_product = ""
            charges = ""
            special_charges = ""
            
            if has_additional_charges:
                additional_product = random.choice(standard_charge_names)
                charges = STANDARD_CHARGES[additional_product]
                
                # Sometimes there are special charges on top of standard charges
                if random.random() < 0.30:
                    special_charges = round(random.uniform(10, 50), 2)
            
            # Create the order object
            order = Order(
                customer_name=customer.name,
                order_number=order_num,
                sequence_id=sequence.seq_id,
                sequence_desc=sequence.description,
                po_number=po_num,
                po_required=po_req,
                date=date_obj,
                status=status,
                invoice_number=invoice_num,
                invoice_date=invoice_date,
                bol=bol,
                product_name=product.name,
                unit_price=unit_price,
                quantity=quantity,
                additional_product=additional_product,
                charges=charges,
                special_charges=special_charges
            )
            
            # Calculate financials
            order.calculate_totals()
            
            orders.append(order)
        
        return orders