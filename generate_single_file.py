#!/usr/bin/env python3
"""
Script to generate a single petroleum orders file.
"""

import logging
import argparse
import datetime

from dummydata.config import SINGLE_OUTPUT_FILE
from dummydata.utils import setup_logging
from dummydata.generators import ReportGenerator


def main():
    """
    Main function to generate a single petroleum orders file.
    """
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Generate a single petroleum orders file')
    parser.add_argument('--orders', type=int, default=50,
                        help='Number of orders to generate (default: 50)')
    parser.add_argument('--output', type=str, default=str(SINGLE_OUTPUT_FILE),
                        help=f'Output file path (default: {SINGLE_OUTPUT_FILE})')
    parser.add_argument('--force-new', action='store_true',
                        help='Force creation of new product and customer data')
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logging()
    
    # Create report generator
    generator = ReportGenerator(logger=logger)
    
    # Generate a single file with orders
    success = generator.generate_single_file(
        output_file=args.output,
        num_orders=args.orders,
        force_new_base_data=args.force_new
    )
    
    if success:
        logger.info(f"Single file generation completed successfully in {args.output}")
        return 0
    else:
        logger.error(f"Single file generation failed.")
        return 1


if __name__ == "__main__":
    exit(main())