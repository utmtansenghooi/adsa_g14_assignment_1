#!/usr/bin/env python3
"""Convenience script to extract datasets from the large common dataset.

Usage:
    python scripts/extract_datasets.py [--input PATH]

Example:
    python scripts/extract_datasets.py
    python scripts/extract_datasets.py --input data/common/Grocery_Inventory_and_Sales_Dataset.csv
"""
import argparse
from pathlib import Path

from src.pos_system.common.data_loader import extract_data_from_common_dataset


def main():
    parser = argparse.ArgumentParser(
        description="Extract datasets from the large common dataset"
    )
    parser.add_argument(
        "--input",
        type=str,
        default=None,
        help="Path to the input CSV file (default: data/common/Grocery_Inventory_and_Sales_Dataset.csv)",
    )
    
    args = parser.parse_args()
    
    try:
        print("Extracting data from large dataset...")
        results = extract_data_from_common_dataset(args.input)
        
        print("\n✓ Extraction successful!")
        print(f"\n  📦 Inventory:  {results['inventory']:,} products")
        print(f"  💳 Sales:      {results['sales']:,} transactions")
        print(f"  👥 Loyalty:    {results['loyalty']:,} customers")
        print("\nFiles saved to:")
        print(f"  - data/inventory/products.csv")
        print(f"  - data/sales/transactions.csv")
        print(f"  - data/loyalty/customers.csv")
        
    except FileNotFoundError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
