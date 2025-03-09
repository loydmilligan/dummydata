#!/usr/bin/env python3
"""
Script to generate monthly petroleum order data.
"""

import os
import logging
import argparse
import datetime
from pathlib import Path

from dummydata.config import ORDER_DIR
from dummydata.utils import setup_logging
from dummydata.generators import ReportGenerator


def main():
    """
    Main function to generate monthly petroleum order data.
    """
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Generate petroleum order data for the current month')
    parser.add_argument('--orders', type=int, default=50,
                        help='Number of orders to generate (default: 50)')
    parser.add_argument('--force-new', action='store_true',
                        help='Force creation of new product and customer data')
    parser.add_argument('--output', type=str,
                        help='Custom output file path (optional)')
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logging()
    
    # Create report generator
    generator = ReportGenerator(logger=logger)
    
    # Get current date for output file path
    if args.output:
        output_file = args.output
    else:
        now = datetime.datetime.now()
        output_file = os.path.join(ORDER_DIR, f"orders_{now.year}_{now.month:02d}.csv")
    
    # Generate orders for the current month
    success = generator.generate_current_month(output_file=output_file)
    
    if success:
        logger.info(f"Monthly order generation completed successfully.")
        return 0
    else:
        logger.error(f"Monthly order generation failed.")
        return 1


if __name__ == "__main__":
    exit(main())