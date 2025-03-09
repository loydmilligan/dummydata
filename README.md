# DummyData - Petroleum Sales Data Generator

A tool for generating realistic petroleum sales data for demo purposes, particularly for use with AI chatbots for sales data analysis in the petroleum marketing and delivery business.

## Overview

This package generates synthetic sales data for petroleum and fuel products that mimics real-world sales patterns, including:

- Customer data with delivery locations (sequences/ship-to locations)
- Product data with realistic petroleum products and pricing
- Order data with realistic fields (PO, BOL, invoices, taxes, margins, etc.)
- Multi-year historical data generation capabilities
- Automatic monthly data generation for keeping demo data current

The data is suitable for demonstration purposes and includes all the typical information found in petroleum marketing and delivery ERP systems. This tool was built specifically to populate databases with realistic data that can be used to train and test AI chatbots for sales analysis.

## Installation

```bash
# Ensure you have Python 3.11+ installed
python -m pip install -r requirements.txt
```

## Usage

There are three main scripts for generating data:

### 1. Generate Current Month Data

```bash
./generate_monthly.py
```

Options:
- `--orders NUM`: Number of orders to generate (default: 50)
- `--force-new`: Force creation of new products and customers
- `--output PATH`: Custom output file path

### 2. Generate Multi-Year Data

```bash
./generate_multi_year.py
```

Options:
- `--auto`: Generate only the current month (for automated scheduling)
- `--start-year YEAR`: Starting year (default: 5 years before current year)
- `--end-year YEAR`: Ending year (default: current year)
- `--end-month MONTH`: Ending month (default: current month)
- `--orders NUM`: Number of orders per month (default: 50)

### 3. Generate Single File

```bash
./generate_single_file.py
```

Options:
- `--orders NUM`: Number of orders to generate (default: 50)
- `--output PATH`: Output file path (default: customer_orders.csv)
- `--force-new`: Force creation of new products and customers

## Output

Data is generated in CSV format and saved to:

- `fuel_orders_data/csv_data/products/products.csv`: Product data
- `fuel_orders_data/csv_data/customers/customers.csv`: Customer data
- `fuel_orders_data/csv_data/customers/customer_sequences.csv`: Customer delivery locations
- `fuel_orders_data/csv_data/orders/orders_YYYY_MM.csv`: Monthly order data
- `customer_orders.csv`: Single file output (when using generate_single_file.py)

## Scheduled Generation

To keep data current, you can set up a monthly cron job:

```bash
# Example cron job to run on the 1st of each month at 1:00 AM
0 1 1 * * cd /path/to/dummydata && ./generate_monthly.py --auto
```

## Project Structure

- `dummydata/`: Main package
  - `models/`: Data models (Product, Customer, Order)
  - `generators/`: Data generation logic
  - `utils/`: Utilities for CSV handling, logging, etc.
  - `config.py`: Configuration and constants
- `generate_monthly.py`: Script to generate current month data
- `generate_multi_year.py`: Script to generate historical data across multiple years
- `generate_single_file.py`: Script to generate a single consolidated orders file

## Data Schema

### Products
- Product codes and names for various petroleum products
- Pricing information with min/max ranges
- Product metadata (tax groups, packaging, etc.)

### Customers
- Company information including address and contact details
- Multiple delivery locations (sequences) per customer

### Orders
- Order header with customer, date, and status information
- Purchase order details
- Product, quantity, and pricing
- Tax and financial calculations
- Margin per gallon analysis

## Future Enhancements

- Database integration capabilities
- API endpoints for retrieving generated data
- Additional data types (inventory, pricing history, etc.)
- Configurable data generation patterns

## License

This project is licensed under the MIT License - see the LICENSE file for details.