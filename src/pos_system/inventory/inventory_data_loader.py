from src.pos_system.common.data_loader import load_inventory_products
from src.pos_system.common.Product import Product
from src.pos_system.inventory.binary_search_tree import BinarySearchTree, BinarySearchNode
from src.pos_system.inventory.splay_tree import SplayTree, SplayNode
from enum import Enum
from typing import List

class InventoryKeyType(Enum):
    PRODUCT_ID = 1
    PRODUCT_NAME = 2

def build_inventory_bst(key_type: InventoryKeyType = InventoryKeyType.PRODUCT_ID, entries: int = -1) -> BinarySearchTree[str]:
    """Build a binary search tree of products from inventory data.
    
    Returns:
        BinarySearchTree with product_id or name as keys and Product objects as values
    """
    bst = BinarySearchTree[BinarySearchNode[str]]()
    product_records = load_inventory_products()
    
    if entries > 0:
        product_records = product_records[:entries]
    for record in product_records:
        product = Product(
            product_id=str(record["product_id"]),
            name=str(record["name"]),
            category=str(record["category"]),
            price=float(record["price"]),
            quantity=int(record["quantity"])
        )
        node = BinarySearchNode(
            key=product.product_id if key_type == InventoryKeyType.PRODUCT_ID else product.name,
            value=product
        )
        bst.insert(node.key, node.value)
    
    return bst

def build_inventory_splay_tree(key_type: InventoryKeyType = InventoryKeyType.PRODUCT_ID, entries: int = -1) -> SplayTree[str]:
    """Build a splay tree of products from inventory data.
    
    Returns:
        SplayTree with product_id or name as keys and Product objects as values
    """
    splay_tree = SplayTree[SplayNode[str]]()
    product_records = load_inventory_products()
    
    if entries > 0:
        product_records = product_records[:entries]
    for record in product_records:
        product = Product(
            product_id=str(record["product_id"]),
            name=str(record["name"]),
            category=str(record["category"]),
            price=float(record["price"]),
            quantity=int(record["quantity"])
        )
        node = SplayNode(
            key=product.product_id if key_type == InventoryKeyType.PRODUCT_ID else product.name,
            value=product
        )
        splay_tree.insert(node.key, node.value)
    
    return splay_tree