"""
Generator for monthly and multi-year petroleum order reports.
"""

import os
import datetime
import logging
from pathlib import Path
from typing import Optional, Union, List, Dict, Any, Tuple

from dummydata.config import (
    create_directories, PRODUCTS_FILE, CUSTOMERS_FILE, SEQUENCES_FILE,
    ORDER_HEADERS, ORDER_DIR, DEFAULT_ORDERS_PER_MONTH, SINGLE_OUTPUT_FILE
)
from dummydata.models import Product, Customer, Order
from dummydata.generators.data_generator import DataGenerator
from dummydata.utils.csv_handler import CSVHandler


class ReportGenerator:
    """
    Generates monthly and multi-year order reports.
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize the report generator.
        
        Args:
            logger: Logger instance (optional)
        """
        self.logger = logger or logging.getLogger(__name__)
        self.data_generator = DataGenerator(logger=self.logger)
        self.csv_handler = CSVHandler()
        
        # Create necessary directories
        create_directories()
    
    def generate_monthly_orders(
        self,
        year: int,
        month: int,
        output_file: Union[str, Path],
        num_orders: int = DEFAULT_ORDERS_PER_MONTH,
        force_new_base_data: bool = False
    ) -> bool:
        """
        Generate order data for a specific month and year.
        
        Args:
            year: Year for the orders
            month: Month for the orders (1-12)
            output_file: Path to the output CSV file
            num_orders: Number of orders to generate
            force_new_base_data: Whether to force new products and customers
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.logger.info(f"Starting to generate orders for {month}/{year}")
            
            # Generate or read products
            products = self.data_generator.generate_products(
                PRODUCTS_FILE, 
                force_new=force_new_base_data
            )
            
            # Generate or read customers
            customers = self.data_generator.generate_customers(
                CUSTOMERS_FILE,
                SEQUENCES_FILE,
                force_new=force_new_base_data
            )
            
            # Generate order data
            orders = self.data_generator.generate_orders(
                products, 
                customers, 
                year, 
                month, 
                num_orders
            )
            
            # Convert orders to rows
            order_rows = [order.to_row() for order in orders]
            
            # Write to CSV
            success = self.csv_handler.write_csv(output_file, ORDER_HEADERS, order_rows)
            
            if success:
                self.logger.info(f"Successfully generated orders for {month}/{year} in {output_file}")
                return True
            else:
                self.logger.error(f"Failed to write orders to {output_file}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error generating orders for {month}/{year}: {e}")
            return False
    
    def generate_multi_year_reports(
        self,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
        end_month: Optional[int] = None,
        orders_per_month: int = DEFAULT_ORDERS_PER_MONTH
    ) -> bool:
        """
        Generate monthly order reports from a starting year up to the current month.
        
        Args:
            start_year: The starting year, defaults to 5 years before current year
            end_year: The ending year (inclusive), defaults to current year
            end_month: The ending month (inclusive), defaults to current month
            orders_per_month: Number of orders to generate per month
            
        Returns:
            True if successful, False otherwise
        """
        # Get current date
        current_date = datetime.datetime.now()
        
        # Set defaults if not provided
        if start_year is None:
            start_year = current_date.year - 5
        
        if end_year is None:
            end_year = current_date.year
        
        if end_month is None:
            end_month = current_date.month
        
        # Validate inputs
        if start_year > end_year:
            self.logger.error(f"Start year ({start_year}) cannot be greater than end year ({end_year})")
            return False
        
        if start_year == end_year and end_month < 1:
            self.logger.error(f"End month ({end_month}) must be between 1 and 12")
            return False
        
        # Calculate total months to process
        total_months = 0
        for year in range(start_year, end_year + 1):
            if year == end_year:
                total_months += end_month
            else:
                total_months += 12
        
        self.logger.info(f"Generating reports for {total_months} months from {start_year} to {end_year}/{end_month}...")
        
        # Track progress
        months_processed = 0
        months_succeeded = 0
        
        # Force new base data only on the first report
        force_new_base_data = True
        
        # Loop through each year and month
        for year in range(start_year, end_year + 1):
            # Determine how many months to process in this year
            max_month = 12
            if year == end_year:
                max_month = end_month
            
            for month in range(1, max_month + 1):
                # Format the output filename
                output_file = os.path.join(ORDER_DIR, f"orders_{year}_{month:02d}.csv")
                
                # Generate orders for this month
                self.logger.info(f"Generating orders for {month}/{year}... ({months_processed+1}/{total_months})")
                
                success = self.generate_monthly_orders(
                    year, 
                    month, 
                    output_file, 
                    orders_per_month, 
                    force_new_base_data=force_new_base_data
                )
                
                # Only force new base data on first report
                force_new_base_data = False
                
                if success:
                    self.logger.info(f"Successfully generated orders for {month}/{year}")
                    months_succeeded += 1
                else:
                    self.logger.error(f"Failed to generate orders for {month}/{year}")
                
                months_processed += 1
                
        success_rate = (months_succeeded / total_months) * 100 if total_months > 0 else 0
        self.logger.info(f"Completed generating {months_succeeded}/{total_months} monthly reports ({success_rate:.2f}% success rate).")
        return months_succeeded > 0
    
    def generate_current_month(self, output_file: Optional[Union[str, Path]] = None) -> bool:
        """
        Generate order data just for the current month.
        
        Args:
            output_file: Optional custom output file path
            
        Returns:
            True if successful, False otherwise
        """
        # Get current date
        current_date = datetime.datetime.now()
        current_year = current_date.year
        current_month = current_date.month
        
        self.logger.info(f"Generating current month data for {current_month}/{current_year}")
        
        # Use provided output file or default
        if output_file is None:
            output_file = os.path.join(ORDER_DIR, f"orders_{current_year}_{current_month:02d}.csv")
        
        return self.generate_monthly_orders(current_year, current_month, output_file)
    
    def generate_single_file(
        self,
        output_file: Union[str, Path] = SINGLE_OUTPUT_FILE,
        num_orders: int = DEFAULT_ORDERS_PER_MONTH,
        force_new_base_data: bool = True
    ) -> bool:
        """
        Generate a single orders file with random dates within the last 90 days.
        
        Args:
            output_file: Path to the output CSV file
            num_orders: Number of orders to generate
            force_new_base_data: Whether to force new products and customers
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.logger.info(f"Generating single orders file with {num_orders} orders")
            
            # Generate or read products
            products = self.data_generator.generate_products(
                PRODUCTS_FILE, 
                force_new=force_new_base_data
            )
            
            # Generate or read customers
            customers = self.data_generator.generate_customers(
                CUSTOMERS_FILE,
                SEQUENCES_FILE,
                force_new=force_new_base_data
            )
            
            # Current date for reference
            current_date = datetime.datetime.now()
            current_year = current_date.year
            current_month = current_date.month
            
            # Generate order data based on current month
            orders = self.data_generator.generate_orders(
                products, 
                customers, 
                current_year, 
                current_month, 
                num_orders
            )
            
            # Convert orders to rows
            order_rows = [order.to_row() for order in orders]
            
            # Write to CSV
            success = self.csv_handler.write_csv(output_file, ORDER_HEADERS, order_rows)
            
            if success:
                self.logger.info(f"Successfully generated {num_orders} orders in {output_file}")
                return True
            else:
                self.logger.error(f"Failed to write orders to {output_file}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error generating single orders file: {e}")
            return False