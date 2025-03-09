"""
Customer and Sequence models for petroleum customers.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class Sequence:
    """
    Represents a delivery location (sequence) for a customer.
    """
    seq_id: int
    description: str


@dataclass
class Customer:
    """
    Represents a petroleum customer with delivery sequences.
    """
    customer_id: str
    name: str
    address: str = ""
    city: str = ""
    state: str = ""
    zip_code: str = ""
    contact_name: str = ""
    phone: str = ""
    email: str = ""
    sequences: List[Sequence] = field(default_factory=list)
    
    @classmethod
    def from_row(cls, row: List[str]) -> 'Customer':
        """
        Create a Customer instance from a CSV row.
        
        Args:
            row: CSV data row
            
        Returns:
            Customer instance
        """
        if len(row) < 2:
            raise ValueError("Customer data must include at least ID and name")
        
        return cls(
            customer_id=row[0],
            name=row[1],
            address=row[2] if len(row) > 2 else "",
            city=row[3] if len(row) > 3 else "",
            state=row[4] if len(row) > 4 else "",
            zip_code=row[5] if len(row) > 5 else "",
            contact_name=row[6] if len(row) > 6 else "",
            phone=row[7] if len(row) > 7 else "",
            email=row[8] if len(row) > 8 else ""
        )
    
    def to_row(self) -> List[str]:
        """
        Convert Customer to a CSV row.
        
        Returns:
            List of strings representing the customer fields
        """
        return [
            self.customer_id,
            self.name,
            self.address,
            self.city,
            self.state,
            self.zip_code,
            self.contact_name,
            self.phone,
            self.email
        ]
    
    def add_sequence(self, seq_id: int, description: str) -> None:
        """
        Add a delivery sequence to the customer.
        
        Args:
            seq_id: Sequence ID
            description: Sequence description
        """
        self.sequences.append(Sequence(seq_id=seq_id, description=description))
        
    def has_sequences(self) -> bool:
        """
        Check if customer has any sequences.
        
        Returns:
            True if customer has at least one sequence
        """
        return len(self.sequences) > 0