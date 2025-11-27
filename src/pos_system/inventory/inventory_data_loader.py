from src.pos_system.common.data_loader import load_inventory_products
from src.pos_system.common.Product import Product
from src.pos_system.inventory.binary_search_tree import BinarySearchTree, BinarySearchNode
from src.pos_system.inventory.splay_tree import SplayTree, SplayNode
from enum import Enum
from typing import Type, Union, List

KeyType = Union[int, str]

class InventoryKeyType(Enum):
    PRODUCT_ID = 1
    PRODUCT_NAME = 2

def build_inventory_bst(key_type: InventoryKeyType = InventoryKeyType.PRODUCT_ID, class_type: Type[KeyType] = str, entries: int = -1) -> BinarySearchTree:
    """Build a binary search tree of products from inventory data.
    
    Returns:
        BinarySearchTree with product_id or name as keys and Product objects as values
    """

    # Setup and load data
    product_records = load_inventory_products()
    if entries > 0:
        product_records = product_records[:entries]

    bst = BinarySearchTree()
    
    # Node key creation
    for record in product_records:
        product = Product(
            product_id=str(record["product_id"]),
            name=str(record["name"]),
            category=str(record["category"]),
            price=float(record["price"]),
            quantity=int(record["quantity"])
        )

        if key_type == InventoryKeyType.PRODUCT_ID:
            raw_key = product.product_id

            if class_type is int:
                node_key = int(raw_key.replace("-", ""))
            else:
                node_key = raw_key
        else:
            node_key = product.name

        node = BinarySearchNode(key=node_key, value=product)
        bst.insert(node.key, node.value)
    
    return bst

def build_inventory_splay_tree(key_type: InventoryKeyType = InventoryKeyType.PRODUCT_ID, class_type: Type[KeyType] = str, entries: int = -1) -> SplayTree:
    """Build a splay tree of products from inventory data.
    
    Returns:
        SplayTree with product_id or name as keys and Product objects as values
    """

    # Setup and load data
    product_records = load_inventory_products()
    if entries > 0:
        product_records = product_records[:entries]

    splay_tree = SplayTree()
    
    # Node key creation
    for record in product_records:
        product = Product(
            product_id=str(record["product_id"]),
            name=str(record["name"]),
            category=str(record["category"]),
            price=float(record["price"]),
            quantity=int(record["quantity"])
        )

        if key_type == InventoryKeyType.PRODUCT_ID:
            raw_key = product.product_id

            if class_type is int:
                node_key = int(raw_key.replace("-", ""))
            else:
                node_key = raw_key
        else:
            node_key = product.name

        node = SplayNode(key=node_key, value=product)
        splay_tree.insert(node.key, node.value)
    
    return splay_tree