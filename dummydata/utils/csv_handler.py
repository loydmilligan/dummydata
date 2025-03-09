"""
CSV file handling utilities for the DummyData package.
"""

import csv
import os
from pathlib import Path
from typing import List, Dict, Any, Union, Optional

class CSVHandler:
    """
    Handles CSV file operations including reading, writing, and checking existence.
    """
    
    @staticmethod
    def read_csv(file_path: Union[str, Path], skip_header: bool = True) -> List[List[str]]:
        """
        Read data from a CSV file.
        
        Args:
            file_path: Path to CSV file
            skip_header: Whether to skip the header row
            
        Returns:
            List of rows from the CSV file
        
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file is empty after skipping header (if applicable)
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        rows = []
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            
            # Skip header if requested
            if skip_header:
                next(reader, None)
                
            # Read all rows
            rows = list(reader)
        
        return rows
    
    @staticmethod
    def write_csv(file_path: Union[str, Path], headers: List[str], data: List[List[Any]]) -> bool:
        """
        Write data to a CSV file.
        
        Args:
            file_path: Path to CSV file to write
            headers: List of column headers
            data: List of rows to write
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
            
            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(headers)
                writer.writerows(data)
            return True
        except Exception:
            return False
    
    @staticmethod
    def file_exists(file_path: Union[str, Path]) -> bool:
        """
        Check if a file exists.
        
        Args:
            file_path: Path to file to check
            
        Returns:
            True if file exists, False otherwise
        """
        return os.path.exists(file_path)