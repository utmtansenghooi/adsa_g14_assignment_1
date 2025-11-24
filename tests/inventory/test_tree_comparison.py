from src.pos_system.inventory.binary_search_tree import BinarySearchTree, BinarySearchNode
from src.pos_system.inventory.splay_tree import SplayTree, SplayNode
from src.pos_system.inventory.inventory_data_loader import build_inventory_bst, build_inventory_splay_tree, InventoryKeyType
from src.pos_system.common.Product import Product
from src.pos_system.common.data_loader import load_inventory_products
from src.pos_system.common.logger import log_operation, timed_operation
import time

def test_tree_insertion_comparison_random_100():
    n = 100
    
    product_records = load_inventory_products() # load full dataset
    products = []
    for record in product_records[:n]:
        product = Product(
            product_id=str(record["product_id"]),
            name=str(record["name"]),
            category=str(record["category"]),
            price=float(record["price"]),
            quantity=int(record["quantity"])
        )
        products.append(product)


    # Build BST by product ID
    nodes = [BinarySearchNode(key=p.product_id, value=p) for p in products]
    bst = BinarySearchTree[BinarySearchNode[str]]()
    start_bst = time.perf_counter()
    for node in nodes:
        bst.insert(node.key, node.value)
    end_bst = time.perf_counter()
    total_bst_duration = end_bst - start_bst

    # Build Splay Tree by product ID
    nodes = [SplayNode(key=p.product_id, value=p) for p in products]
    splay_tree = SplayTree[SplayNode[str]]()
    start_splay = time.perf_counter()
    for node in nodes:
        splay_tree.insert(node.key, node.value)
    end_splay = time.perf_counter()
    total_splay_duration = end_splay - start_splay

    print()
    print(f"BST insertion time for {n} nodes: {total_bst_duration*1000*1000:.6f} nanoseconds")
    print(f"Splay Tree insertion time for {n} nodes: {total_splay_duration*1000*1000:.6f} nanoseconds")
    print(f"Splay Tree was {'faster' if total_splay_duration < total_bst_duration else 'slower'} than BST by {abs(total_splay_duration - total_bst_duration)*1000*1000:.6f} nanoseconds")

def test_tree_deletion_comparison_random_100():
    n = 100
    
    product_records = load_inventory_products() # load full dataset
    products = []
    for record in product_records[:n]:
        product = Product(
            product_id=str(record["product_id"]),
            name=str(record["name"]),
            category=str(record["category"]),
            price=float(record["price"]),
            quantity=int(record["quantity"])
        )
        products.append(product)

    
    # Build BST by product ID
    nodes = [BinarySearchNode(key=p.product_id, value=p) for p in products]
    bst = BinarySearchTree[BinarySearchNode[str]]()
    for node in nodes:
        bst.insert(node.key, node.value)

    # Build Splay Tree by product ID
    nodes = [SplayNode(key=p.product_id, value=p) for p in products]
    splay_tree = SplayTree[SplayNode[str]]()
    for node in nodes:
        splay_tree.insert(node.key, node.value)

    # Delete all nodes in both trees and time them
    start_bst = time.perf_counter()
    for p in products:
        bst.delete(p.product_id)
    end_bst = time.perf_counter()
    total_bst_duration = end_bst - start_bst

    start_splay = time.perf_counter()
    for p in products:
        splay_tree.delete(p.product_id)
    end_splay = time.perf_counter()
    total_splay_duration = end_splay - start_splay

    print()
    print(f"BST deletion time for {n} nodes: {total_bst_duration*1000*1000:.6f} nanoseconds")
    print(f"Splay Tree deletion time for {n} nodes: {total_splay_duration*1000*1000:.6f} nanoseconds")
    print(f"Splay Tree was {'faster' if total_splay_duration < total_bst_duration else 'slower'} than BST by {abs(total_splay_duration - total_bst_duration)*1000*1000:.6f} nanoseconds")

def test_tree_search_comparison_random_100():
    n = 100
    
    product_records = load_inventory_products() # load full dataset
    products = []
    for record in product_records[:n]:
        product = Product(
            product_id=str(record["product_id"]),
            name=str(record["name"]),
            category=str(record["category"]),
            price=float(record["price"]),
            quantity=int(record["quantity"])
        )
        products.append(product)

    
    # Build BST by product ID
    nodes = [BinarySearchNode(key=p.product_id, value=p) for p in products]
    bst = BinarySearchTree[BinarySearchNode[str]]()
    for node in nodes:
        bst.insert(node.key, node.value)

    # Build Splay Tree by product ID
    nodes = [SplayNode(key=p.product_id, value=p) for p in products]
    splay_tree = SplayTree[SplayNode[str]]()
    for node in nodes:
        splay_tree.insert(node.key, node.value)

    # Search all nodes in both trees and time them
    start_bst = time.perf_counter()
    for p in products:
        bst.search(p.product_id)
    end_bst = time.perf_counter()
    total_bst_duration = end_bst - start_bst

    start_splay = time.perf_counter()
    for p in products:
        splay_tree.search(p.product_id)
    end_splay = time.perf_counter()
    total_splay_duration = end_splay - start_splay

    print()
    print(f"BST search time for {n} nodes: {total_bst_duration*1000*1000:.6f} nanoseconds")
    print(f"Splay Tree search time for {n} nodes: {total_splay_duration*1000*1000:.6f} nanoseconds")
    print(f"Splay Tree was {'faster' if total_splay_duration < total_bst_duration else 'slower'} than BST by {abs(total_splay_duration - total_bst_duration)*1000*1000:.6f} nanoseconds")

def test_tree_search_comparison_20percent_100():
    n = 100
    
    product_records = load_inventory_products() # load full dataset
    products = []
    for record in product_records[:n]:
        product = Product(
            product_id=str(record["product_id"]),
            name=str(record["name"]),
            category=str(record["category"]),
            price=float(record["price"]),
            quantity=int(record["quantity"])
        )
        products.append(product)

    
    # Build BST by product ID
    nodes = [BinarySearchNode(key=p.product_id, value=p) for p in products]
    bst = BinarySearchTree[BinarySearchNode[str]]()
    for node in nodes:
        bst.insert(node.key, node.value)

    # Build Splay Tree by product ID
    nodes = [SplayNode(key=p.product_id, value=p) for p in products]
    splay_tree = SplayTree[SplayNode[str]]()
    for node in nodes:
        splay_tree.insert(node.key, node.value)

    # Search 20% of nodes repeatedly in both trees and time them
    search_keys = [p.product_id for p in products[:int(n*0.2)]]

    start_bst = time.perf_counter()
    for _ in range(10): # repeat to amplify time difference
        for key in search_keys:
            bst.search(key)
    end_bst = time.perf_counter()
    total_bst_duration = end_bst - start_bst

    start_splay = time.perf_counter()
    for _ in range(10): # repeat to amplify time difference
        for key in search_keys:
            splay_tree.search(key)
    end_splay = time.perf_counter()
    total_splay_duration = end_splay - start_splay

    print()
    print(f"BST 20/80 search time for {n} nodes: {total_bst_duration*1000*1000:.6f} nanoseconds")
    print(f"Splay Tree 20/80 search time for {n} nodes: {total_splay_duration*1000*1000:.6f} nanoseconds")
    print(f"Splay Tree was {'faster' if total_splay_duration < total_bst_duration else 'slower'} than BST by {abs(total_splay_duration - total_bst_duration)*1000*1000:.6f} nanoseconds")

def test_tree_search_comparison_5percent_100():
    n = 100
    
    product_records = load_inventory_products() # load full dataset
    products = []
    for record in product_records[:n]:
        product = Product(
            product_id=str(record["product_id"]),
            name=str(record["name"]),
            category=str(record["category"]),
            price=float(record["price"]),
            quantity=int(record["quantity"])
        )
        products.append(product)

    
    # Build BST by product ID
    nodes = [BinarySearchNode(key=p.product_id, value=p) for p in products]
    bst = BinarySearchTree[BinarySearchNode[str]]()
    for node in nodes:
        bst.insert(node.key, node.value)

    # Build Splay Tree by product ID
    nodes = [SplayNode(key=p.product_id, value=p) for p in products]
    splay_tree = SplayTree[SplayNode[str]]()
    for node in nodes:
        splay_tree.insert(node.key, node.value)

    # Search 5% of nodes repeatedly in both trees and time them
    search_keys = [p.product_id for p in products[:int(n*0.05)]]

    start_bst = time.perf_counter()
    for _ in range(10): # repeat to amplify time difference
        for key in search_keys:
            bst.search(key)
    end_bst = time.perf_counter()
    total_bst_duration = end_bst - start_bst

    start_splay = time.perf_counter()
    for _ in range(10): # repeat to amplify time difference
        for key in search_keys:
            splay_tree.search(key)
    end_splay = time.perf_counter()
    total_splay_duration = end_splay - start_splay

    print()
    print(f"BST 5/95 search time for {n} nodes: {total_bst_duration*1000*1000:.6f} nanoseconds")
    print(f"Splay Tree 5/95 search time for {n} nodes: {total_splay_duration*1000*1000:.6f} nanoseconds")
    print(f"Splay Tree was {'faster' if total_splay_duration < total_bst_duration else 'slower'} than BST by {abs(total_splay_duration - total_bst_duration)*1000*1000:.6f} nanoseconds")