"""Tests that demonstrate loading data and using it with tree structures."""

from src.pos_system.common.data_loader import (
    load_inventory_products,
    load_sales_transactions,
)
from src.pos_system.example.binary_tree import BinaryTree as ExampleBinaryTree


def test_load_inventory_data():
    """Test that inventory data loads correctly."""
    products = load_inventory_products()
    assert len(products) == 990  # extracted from large dataset
    assert products[0]["product_id"] == "29-205-1132"
    assert products[0]["name"] == "Sushi Rice"
    assert "price" in products[0]
    assert "quantity" in products[0]


def test_load_sales_data():
    """Test that sales data loads correctly."""
    transactions = load_sales_transactions()
    assert len(transactions) == 990  # extracted from large dataset
    assert transactions[0]["transaction_id"] == "29-205-1132_0"
    assert "product_id" in transactions[0]
    assert "quantity_sold" in transactions[0]
    assert "total_amount" in transactions[0]


def test_populate_tree_with_product_data():
    """Example: populate an inventory tree with real data."""
    products = load_inventory_products()
    tree = ExampleBinaryTree[int]()
    
    # Insert first 100 products using index as numeric key (to avoid duplicates)
    for idx, product in enumerate(products[:100]):
        tree.insert(idx, value=product)
    
    # Search for a product
    result = tree.search(0)
    assert result is not None
    assert result.value["product_id"] == products[0]["product_id"]
    
    # Verify traversal is in sorted order
    keys = [n.key for n in tree.traverse()]
    assert len(keys) == 100
    assert keys == sorted(keys)  # in-order traversal should be sorted
