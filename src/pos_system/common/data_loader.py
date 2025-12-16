"""Data loader utilities for reading CSV datasets into tree structures.

This module provides helper functions to load sample data from CSV files
and populate tree structures for testing and algorithm analysis.
"""
import csv
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
from src.pos_system.common.logger import log_operation, timed_operation
import time

def get_data_path(module_name: str, filename: str) -> Path:
    """Get the full path to a data file.
    
    Args:
        module_name: One of 'inventory', 'sales', or 'loyalty'
        filename: Name of the CSV file (e.g., 'products.csv')
    
    Returns:
        Path to the data file
    """
    # Navigate from common/ -> pos_system/ -> src/ -> project root -> data/
    base_path = Path(__file__).parent.parent.parent.parent / "data"
    return base_path / module_name / filename


def load_csv(module_name: str, filename: str) -> List[Dict[str, Any]]:
    """Load a CSV file and return as list of dicts.
    
    Args:
        module_name: One of 'inventory', 'sales', or 'loyalty'
        filename: Name of the CSV file
    
    Returns:
        List of dictionaries, one per row
        
    Raises:
        FileNotFoundError: If the file does not exist
    """
    path = get_data_path(module_name, filename)
    
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")
    
    rows = []
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    
    return rows


def load_inventory_products(filename: str = "products.csv") -> List[Dict[str, Any]]:
    """Load product inventory data.
    
    Returns:
        List of product records with product_id, name, price, quantity
    """
    return load_csv("inventory", filename)


def extract_data_from_common_dataset(input_file: Optional[str] = None) -> Dict[str, int]:
    """Extract inventory, sales, and loyalty data from the large common dataset.
    
    This function reads the Grocery_Inventory_and_Sales_Dataset.csv file and
    extracts data for each module, saving them as separate CSV files.
    
    Args:
        input_file: Path to the input CSV file. If None, uses default path.
    
    Returns:
        Dictionary with counts of extracted records for each module:
        {'inventory': count, 'sales': count, 'loyalty': count}
    
    Raises:
        FileNotFoundError: If the input file does not exist
    """
    if input_file is None:
        # Default path: data/common/Grocery_Inventory_and_Sales_Dataset.csv
        base_path = Path(__file__).parent.parent.parent.parent / "data" / "common"
        input_file = base_path / "Grocery_Inventory_and_Sales_Dataset.csv"
    else:
        input_file = Path(input_file)
    
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Read the large dataset
    rows = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    # Extract unique products for inventory
    inventory_products: Dict[str, Dict[str, Any]] = {}
    sales_records: List[Dict[str, Any]] = []
    loyalty_customers: Dict[str, Dict[str, Any]] = {}
    
    for row in rows:
        # Extract inventory data (products)
        product_id = row.get('Product_ID', '').strip()
        if product_id and product_id not in inventory_products:
            inventory_products[product_id] = {
                'product_id': product_id,
                'name': row.get('Product_Name', '').strip(),
                'category': row.get('Catagory', '').strip(),
                'price': row.get('Unit_Price', '0').strip().replace('$', ''),
                'quantity': row.get('Stock_Quantity', '0').strip(),
            }
        
        # Extract sales data (create synthetic transaction records)
        sales_volume = int(row.get('Sales_Volume', '0') or '0')
        if sales_volume > 0:
            # Create a transaction record for each unit sold
            sales_records.append({
                'transaction_id': f"{product_id}_{len(sales_records)}",
                'product_id': product_id,
                'quantity_sold': sales_volume,
                'price_per_unit': row.get('Unit_Price', '0').strip().replace('$', ''),
                'total_amount': str(float(row.get('Unit_Price', '0').strip().replace('$', '') or '0') * sales_volume),
                'timestamp': row.get('Date_Received', '').strip(),
            })
        
        # Extract loyalty data (customers - synthetic generation based on product rows)
        # Using Product_ID hash to create unique customer IDs
        customer_id = f"CUST_{hash(product_id) % 10000:05d}"
        if customer_id not in loyalty_customers:
            loyalty_customers[customer_id] = {
                'customer_id': customer_id,
                'name': f"Customer {customer_id}",
                'loyalty_points': str(int((int(row.get('Sales_Volume', '0') or '0') * 10))),
                'tier': 'Gold' if int(row.get('Sales_Volume', '0') or '0') > 50 else ('Silver' if int(row.get('Sales_Volume', '0') or '0') > 25 else 'Bronze'),
                'join_date': row.get('Last_Order_Date', '').strip(),
            }
    
    # Write inventory data
    inventory_path = input_file.parent.parent / "inventory" / "products.csv"
    inventory_path.parent.mkdir(parents=True, exist_ok=True)
    with open(inventory_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['product_id', 'name', 'category', 'price', 'quantity'])
        writer.writeheader()
        writer.writerows(inventory_products.values())
    
    # Write sales data
    sales_path = input_file.parent.parent / "sales" / "transactions.csv"
    sales_path.parent.mkdir(parents=True, exist_ok=True)
    with open(sales_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['transaction_id', 'product_id', 'quantity_sold', 'price_per_unit', 'total_amount', 'timestamp'])
        writer.writeheader()
        writer.writerows(sales_records)
    
    # Write loyalty data
    loyalty_path = input_file.parent.parent / "loyalty" / "customers.csv"
    loyalty_path.parent.mkdir(parents=True, exist_ok=True)
    with open(loyalty_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['customer_id', 'name', 'loyalty_points', 'tier', 'join_date'])
        writer.writeheader()
        writer.writerows(loyalty_customers.values())
    
    return {
        'inventory': len(inventory_products),
        'sales': len(sales_records),
        'loyalty': len(loyalty_customers),
    }