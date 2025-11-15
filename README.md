# Universiti Teknologi Malaysia
## Quickstart
```bash
# Install dependencies
pip install -r requirements.txt

# Run the POS system CLI
python -m src.pos_system

# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_binary_tree.py -v

# Extract/refresh datasets
python scripts/extract_datasets.py
```

## Advanced Data Structures and Algorithms (ADSA) - Assignment 1 (Group 14)
### Group 14 Members
- Tan Seng Hooi
- Quek Boon Siang
- Chang Choon Kit
### Objectives
- Design and implement programs in a programming language demonstrating the use of the Search Tree Structures representation
- Analyse the complexity of algorithms and the performance of the algorithms and data structure
### Assignment Details

<table border="1" cellpadding="4" cellspacing="0">
	<tr>
		<th><strong>Theme</strong></th>
		<th><strong>Members</strong></th>
		<th><strong>Programming Language Initial Proposal Title</strong></th>
		<th><strong>Individual Tree Data Structure</strong></th>
	</tr>
	<tr>
		<td rowspan="3"><strong>Supermarket Point-of-Sale (POS) System</strong></td>
		<td>Tan Seng Hooi</td>
		<td>Product Inventory Management Module</td>
		<td>Splay</td>
	</tr>
	<tr>
		<td>Quek Boon Siang</td>
		<td>Sales Transaction and Receipt Module</td>
		<td>B-Tree</td>
	</tr>
	<tr>
		<td>Chang Choon Kit</td>
		<td>Customer Loyalty and Discount Module</td>
		<td>AVL</td>
	</tr>
</table>

### Project Structure

This repository provides a complete template for the Supermarket POS application with data extraction and testing infrastructure. Each team member implements two algorithms for their assigned module.

**Directory layout:**

```
adsa_g14_assignment_1/
├─ README.md                              # Project documentation
├─ pyproject.toml                         # Python project configuration
├─ setup.cfg                              # Setuptools configuration
├─ requirements.txt                       # Python dependencies (pytest)
├─ .gitignore                             # Git ignore patterns
│
├─ scripts/
│  └─ extract_datasets.py                 # Utility to extract data from large dataset
│
├─ data/
│  ├─ common/
│  │  └─ Grocery_Inventory_and_Sales_Dataset.csv  # Large dataset (990 rows)
│  ├─ inventory/
│  │  └─ products.csv                     # 990 products (extracted)
│  ├─ sales/
│  │  └─ transactions.csv                 # 990 transactions (extracted)
│  └─ loyalty/
│     └─ customers.csv                    # 935 customers (extracted)
│
├─ src/
│  └─ pos_system/
│     ├─ __init__.py
│     ├─ __main__.py                      # CLI entry point
│     │
│     ├─ common/
│     │  ├─ __init__.py
│     │  ├─ interfaces.py                 # TreeInterface & Node base classes
│     │  └─ data_loader.py                # CSV data loading & extraction utilities
│     │
│     ├─ inventory/                       # Product Inventory Management Module (Tan Seng Hooi)
│     │  ├─ __init__.py
│     │  ├─ binary_tree.py                # Working BST implementation
│     │  └─ splay_tree.py                 # Splay tree skeleton
│     │
│     ├─ sales/                           # Sales Transaction and Receipt Module (Quek Boon Siang)
│     │  ├─ __init__.py
│     │  ├─ binary_tree.py                # Binary tree skeleton
│     │  └─ btree.py                      # B-tree skeleton
│     │
│     └─ loyalty/                         # Customer Loyalty and Discount Module (Chang Choon Kit)
│        ├─ __init__.py
│        ├─ binary_tree.py                # Binary tree skeleton
│        └─ avl_tree.py                   # AVL tree skeleton
│
└─ tests/
   ├─ test_imports.py                     # Module import smoke tests
   ├─ test_binary_tree.py                 # BinaryTree unit tests
   └─ test_data_loader.py                 # Data loading and integration tests
```

**Guidelines:**

- **Implementation:** Each member implements two algorithms for their assigned module (using files like `binary_tree.py` and your assigned tree type).
- **Interfaces:** Inherit from `TreeInterface` and use `Node` dataclass from `src/pos_system/common/interfaces.py`.
- **Testing:** Create unit tests in `tests/` to verify insert, search, delete, and traverse operations.
- **Data:** Use provided CSV files in `data/` for testing; extract fresh data with `scripts/extract_datasets.py` if needed.
- **CLI:** Implement your demos in the `src/pos_system/__main__.py` file (skeleton with TODO comments provided).


**Development workflow:**

1. **Implement your tree algorithms** in your assigned module files (e.g., `src/pos_system/inventory/splay_tree.py`)
2. **Add unit tests** in `tests/` to validate insert, search, delete, traverse operations
3. **Implement demos** in the TODO functions within `src/pos_system/__main__.py`
4. **Test with real data** using the provided CSV files in `data/`

## Run specific test file
python -m pytest tests/test_binary_tree.py -v

## Run CLI
python -m src.pos_system

## Extract/refresh datasets (optional)
python scripts/extract_datasets.py
```

### Data & Testing

The repository includes **990 products, 990 sales transactions, and 935 customers** for algorithm testing and performance analysis.

**Data files:**

| File | Records | Columns | Purpose |
|------|---------|---------|---------|
| `data/inventory/products.csv` | 990 | product_id, name, category, price, quantity | Product catalog for inventory tree tests |
| `data/sales/transactions.csv` | 990 | transaction_id, product_id, quantity_sold, price_per_unit, total_amount, timestamp | Sales history for transaction tree tests |
| `data/loyalty/customers.csv` | 935 | customer_id, name, loyalty_points, tier, join_date | Customer data for loyalty tree tests |

**Loading data in your code:**

```python
from src.pos_system.common.data_loader import (
    load_inventory_products,
    load_sales_transactions, 
    load_loyalty_customers
)

# Load all data
products = load_inventory_products()      # List of 990 dicts
transactions = load_sales_transactions()  # List of 990 dicts
customers = load_loyalty_customers()      # List of 935 dicts

# Populate a tree (example with inventory)
from src.pos_system.inventory.binary_tree import BinaryTree

tree = BinaryTree()
for idx, product in enumerate(products):
    tree.insert(idx, value=product)

# Search and traverse
result = tree.search(0)
for node in tree.traverse():
    print(node.key, node.value)
```

**Extracting/refreshing data:**

The large dataset in `data/common/Grocery_Inventory_and_Sales_Dataset.csv` can be split into module-specific files:

```bash
python scripts/extract_datasets.py
```

Or programmatically:

```python
from src.pos_system.common.data_loader import extract_data_from_common_dataset

results = extract_data_from_common_dataset()
print(f"✓ Extracted {results['inventory']} products")
print(f"✓ Extracted {results['sales']} transactions")
print(f"✓ Extracted {results['loyalty']} customers")
```

**Example tests:**

See `tests/test_data_loader.py` for complete examples of loading data, populating trees, and running performance tests.