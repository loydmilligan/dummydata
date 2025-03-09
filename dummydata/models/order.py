"""
Order model for petroleum orders.
"""

import random
import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Union


@dataclass
class Order:
    """
    Represents a petroleum order with all associated data.
    """
    # Customer information
    customer_name: str
    
    # Order details
    order_number: str
    sequence_id: int
    sequence_desc: str
    date: Union[datetime.date, str]
    
    # Product information
    product_name: str
    unit_price: float
    quantity: int
    
    # Status
    status: str = "Completed"  # Completed, In Progress, Pending
    
    # Purchase order info
    po_required: str = "No"  # Yes, No
    po_number: str = ""
    
    # Invoice details
    invoice_number: str = ""
    invoice_date: Union[datetime.date, str, None] = None
    bol: str = ""  # Bill of Lading
    
    # Additional charges
    additional_product: str = ""
    charges: Union[float, str] = ""
    special_charges: Union[float, str] = ""
    
    # Financial data
    total_taxes: float = 0.0
    exempt_taxes: float = 0.0
    total: float = 0.0
    total_cost: float = 0.0
    margin_per_gallon: float = 0.0
    
    def to_row(self) -> List[Union[str, float, int]]:
        """
        Convert Order to a CSV row.
        
        Returns:
            List representing the order fields
        """
        # Format date fields
        date_str = self.date if isinstance(self.date, str) else self.date.strftime('%m/%d/%Y')
        invoice_date_str = ""
        
        if self.invoice_date:
            if isinstance(self.invoice_date, str):
                invoice_date_str = self.invoice_date
            else:
                invoice_date_str = self.invoice_date.strftime('%m/%d/%Y')
        
        return [
            self.customer_name, 
            self.order_number, 
            self.sequence_id, 
            self.sequence_desc,
            self.po_number,
            self.po_required,
            date_str,
            self.status,
            self.invoice_number,
            invoice_date_str,
            self.bol,
            self.product_name,
            self.unit_price,
            self.quantity,
            self.additional_product,
            self.charges,
            self.special_charges,
            self.total_taxes,
            self.total,
            self.exempt_taxes,
            self.total_cost,
            self.margin_per_gallon
        ]
    
    @classmethod
    def from_row(cls, row: List[str]) -> 'Order':
        """
        Create an Order instance from a CSV row.
        
        Args:
            row: CSV data row
            
        Returns:
            Order instance
        """
        if len(row) < 14:  # Minimum required fields
            raise ValueError("Order data is missing required fields")
        
        # Parse numeric values safely
        try:
            unit_price = float(row[12]) if row[12] else 0.0
            quantity = int(row[13]) if row[13] else 0
            
            charges = row[15] if not row[15] or not row[15].strip() else float(row[15])
            special_charges = row[16] if not row[16] or not row[16].strip() else float(row[16])
            
            total_taxes = float(row[17]) if row[17] else 0.0
            total = float(row[18]) if row[18] else 0.0
            exempt_taxes = float(row[19]) if row[19] else 0.0
            total_cost = float(row[20]) if row[20] else 0.0
            margin_per_gallon = float(row[21]) if row[21] else 0.0
        except (ValueError, IndexError):
            # Default to zero if conversion fails
            unit_price = 0.0
            quantity = 0
            charges = ""
            special_charges = ""
            total_taxes = 0.0
            total = 0.0
            exempt_taxes = 0.0
            total_cost = 0.0
            margin_per_gallon = 0.0
        
        return cls(
            customer_name=row[0],
            order_number=row[1],
            sequence_id=int(row[2]) if row[2].isdigit() else 0,
            sequence_desc=row[3],
            po_number=row[4],
            po_required=row[5],
            date=row[6],
            status=row[7],
            invoice_number=row[8],
            invoice_date=row[9],
            bol=row[10],
            product_name=row[11],
            unit_price=unit_price,
            quantity=quantity,
            additional_product=row[14] if len(row) > 14 else "",
            charges=charges,
            special_charges=special_charges,
            total_taxes=total_taxes,
            total=total,
            exempt_taxes=exempt_taxes,
            total_cost=total_cost,
            margin_per_gallon=margin_per_gallon
        )
        
    def calculate_totals(self) -> None:
        """
        Calculate all the financial totals for the order.
        """
        # Calculate main charges
        main_charges = round(self.unit_price * self.quantity, 2)
        
        # Get additional charges as float
        additional_charges = 0.0
        if isinstance(self.charges, (int, float)):
            additional_charges = float(self.charges)
        
        # Get special charges as float
        special_charges = 0.0
        if isinstance(self.special_charges, (int, float)):
            special_charges = float(self.special_charges)
        
        # Calculate taxes
        tax_rate = random.uniform(0.05, 0.10)
        self.total_taxes = round(main_charges * tax_rate, 2)
        self.exempt_taxes = round(random.uniform(0, self.total_taxes * 0.3), 2)
        
        # Calculate total
        self.total = main_charges + additional_charges + special_charges + self.total_taxes - self.exempt_taxes
        
        # Calculate cost and margin
        self.total_cost = round(main_charges * 0.85, 2)  # Cost is 85% of main charges
        
        # Calculate margin per gallon
        if self.quantity > 0:
            self.margin_per_gallon = round((main_charges - self.total_cost) / self.quantity, 3)
        else:
            self.margin_per_gallon = 0.0