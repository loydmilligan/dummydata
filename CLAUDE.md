# DummyData Project Guide

## Commands
- Generate current month data: `python generate_monthly.py`
- Generate multi-year data: `python generate_multi_year.py`
- Generate single order file: `python generate_single_file.py`
- Automatic mode (current month only): `python generate_multi_year.py --auto`
- Specific date range: `python generate_multi_year.py --start-year 2023 --end-year 2024 --orders 100`
- Scheduling: `0 1 1 * * cd /path/to/dummydata && python generate_monthly.py` (monthly cron job)

## Code Style
- Use Python 3.11+ features
- Import order: stdlib, 3rd party libs, local modules
- Type hints: Use for all function parameters and return values
- Exception handling: Use specific exceptions with contextual error messages
- Naming: snake_case for variables/functions, PascalCase for classes
- Formatting: 4-space indentation
- Docstrings: Google style docstrings with Args/Returns sections
- OOP principles: Use dataclasses for models, proper encapsulation
- Test coverage: Unit tests recommended for all core functionality
- Logging: Use logger.info/error instead of print statements