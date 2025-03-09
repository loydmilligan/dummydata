"""
Product model for petroleum products.
"""

import random
from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class Product:
    """
    Represents a petroleum product with pricing information.
    """
    code: str
    name: str
    abbrev: str = ""
    product_group: str = "Fuel"
    cycle_code: str = ""
    method: str = "Direct"
    account_group: str = ""
    tax_profile: str = ""
    tax_group: str = ""
    packaging: str = "Bulk"
    unit_of_measure: str = "Gallon"
    status: str = "Active"
    stocked: str = "Yes"
    upc_code: str = ""
    
    # Price ranges
    min_price: float = 0.0
    max_price: float = 0.0
    
    @classmethod
    def from_row(cls, row: List[str]) -> 'Product':
        """
        Create a Product instance from a CSV row.
        
        Args:
            row: CSV data row (must have at least product code and name)
            
        Returns:
            Product instance
        """
        if len(row) < 2:
            raise ValueError("Product data must include at least code and name")
        
        # Create product with available data
        product = cls(
            code=row[0],
            name=row[1],
            abbrev=row[2] if len(row) > 2 else "",
            product_group=row[3] if len(row) > 3 else "Fuel",
            cycle_code=row[4] if len(row) > 4 else "",
            method=row[5] if len(row) > 5 else "Direct",
            account_group=row[6] if len(row) > 6 else "",
            tax_profile=row[7] if len(row) > 7 else "",
            tax_group=row[8] if len(row) > 8 else "",
            packaging=row[9] if len(row) > 9 else "Bulk",
            unit_of_measure=row[10] if len(row) > 10 else "Gallon",
            status=row[11] if len(row) > 11 else "Active",
            stocked=row[12] if len(row) > 12 else "Yes",
            upc_code=row[13] if len(row) > 13 else "",
        )
        
        # Generate random price ranges
        product.min_price = round(random.uniform(2.50, 3.20), 2)
        product.max_price = round(random.uniform(3.50, 4.50), 2)
        
        return product
    
    def to_row(self) -> List[str]:
        """
        Convert Product to a CSV row.
        
        Returns:
            List of strings representing the product fields
        """
        return [
            self.code,
            self.name,
            self.abbrev,
            self.product_group,
            self.cycle_code,
            self.method,
            self.account_group,
            self.tax_profile,
            self.tax_group,
            self.packaging,
            self.unit_of_measure,
            self.status,
            self.stocked,
            self.upc_code
        ]
    
    def get_random_price(self) -> float:
        """
        Get a random price within the product's price range.
        
        Returns:
            Float price value
        """
        return round(random.uniform(self.min_price, self.max_price), 2)