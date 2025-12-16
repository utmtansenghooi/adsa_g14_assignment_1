"""Tests that demonstrate loading data and using it with tree structures."""

from src.pos_system.common.data_loader import (
    load_inventory_products
)

def test_load_inventory_data():
    """Test that inventory data loads correctly."""
    products = load_inventory_products()
    assert len(products) == 990  # extracted from large dataset
    assert products[0]["product_id"] == "29-205-1132"
    assert products[0]["name"] == "Sushi Rice"
    assert "price" in products[0]
    assert "quantity" in products[0]