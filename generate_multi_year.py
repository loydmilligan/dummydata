#!/usr/bin/env python3
"""
Script to generate multi-year petroleum order data.
"""

import logging
import argparse
import datetime

from dummydata.utils import setup_logging
from dummydata.generators import ReportGenerator


def main():
    """
    Main function to generate multi-year petroleum order data.
    """
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Generate petroleum order data for multiple years')
    parser.add_argument('--auto', action='store_true', 
                        help='Generate only the current month (for automated scheduling)')
    parser.add_argument('--start-year', type=int, 
                        help='Starting year (defaults to 5 years before current year)')
    parser.add_argument('--end-year', type=int, 
                        help='Ending year (defaults to current year)')
    parser.add_argument('--end-month', type=int, 
                        help='Ending month (defaults to current month)')
    parser.add_argument('--orders', type=int, default=50,
                        help='Number of orders per month (default: 50)')
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logging()
    
    # Create report generator
    generator = ReportGenerator(logger=logger)
    
    if args.auto:
        # Run in automatic mode - just generate current month
        logger.info("Running in automatic mode - generating current month only")
        success = generator.generate_current_month()
    else:
        # Generate multi-year reports with provided arguments
        success = generator.generate_multi_year_reports(
            start_year=args.start_year,
            end_year=args.end_year,
            end_month=args.end_month,
            orders_per_month=args.orders
        )
    
    if success:
        logger.info("Multi-year report generation completed successfully.")
        return 0
    else:
        logger.error("Multi-year report generation failed.")
        return 1


if __name__ == "__main__":
    exit(main())