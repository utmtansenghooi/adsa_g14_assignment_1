from src.pos_system.inventory.binary_search_tree import BinarySearchTree, BinarySearchNode
from src.pos_system.inventory.splay_tree import SplayTree, SplayNode
from src.pos_system.inventory.inventory_data_loader import build_inventory_bst, build_inventory_splay_tree, InventoryKeyType
from src.pos_system.common.Product import Product
from src.pos_system.common.data_loader import load_inventory_products
from src.pos_system.common.logger import log_operation, timed_operation
import time
import random
import string

def test_tree_normal_comparison_random_100():
    n = 100
    
    # Generate numbers
    numbers = list(range(n))
    random.shuffle(numbers)

    ## Insertion comparison
    # Build BST
    bst = BinarySearchTree[int]()
    start_bst = time.perf_counter()
    for num in numbers:
        bst.insert(num)
    end_bst = time.perf_counter()
    total_bst_duration = end_bst - start_bst

    # Build Splay Tree
    splay_tree = SplayTree[int]()
    start_splay = time.perf_counter()
    for num in numbers:
        splay_tree.insert(num)
    end_splay = time.perf_counter()
    total_splay_duration = end_splay - start_splay

    print()
    print(f"BST insertion time for {n} nodes: {total_bst_duration*1000*1000:.6f} nanoseconds")
    print(f"Splay Tree insertion time for {n} nodes: {total_splay_duration*1000*1000:.6f} nanoseconds")
    print(f"Splay Tree was {'faster' if total_splay_duration < total_bst_duration else 'slower'} than BST by {abs(total_splay_duration - total_bst_duration)*1000*1000:.6f} nanoseconds")

    ## Search comparison
    # BST search
    start_bst = time.perf_counter()
    for _ in range(100): # repeat to amplify time difference
        for num in numbers:
            bst.search(num)
    end_bst = time.perf_counter()
    total_bst_duration = end_bst - start_bst

    # Splay Tree search
    start_splay = time.perf_counter()
    for _ in range(100): # repeat to amplify time difference
        for num in numbers:
            splay_tree.search(num)
    end_splay = time.perf_counter()
    total_splay_duration = end_splay - start_splay

    print()
    print(f"BST search time for {n} nodes: {total_bst_duration*1000*1000:.6f} nanoseconds")
    print(f"Splay Tree search time for {n} nodes: {total_splay_duration*1000*1000:.6f} nanoseconds")
    print(f"Splay Tree was {'faster' if total_splay_duration < total_bst_duration else 'slower'} than BST by {abs(total_splay_duration - total_bst_duration)*1000*1000:.6f} nanoseconds")

    ## Search 20% comparison
    search_keys = numbers[:int(n*0.2)]
    # BST search
    start_bst = time.perf_counter()
    for _ in range(100): # repeat to amplify time difference
        for num in search_keys:
            bst.search(num)
    end_bst = time.perf_counter()
    total_bst_duration = end_bst - start_bst

    # Splay Tree search
    start_splay = time.perf_counter()
    for _ in range(100): # repeat to amplify time difference
        for num in search_keys:
            splay_tree.search(num)
    end_splay = time.perf_counter()
    total_splay_duration = end_splay - start_splay

    print()
    print(f"BST search time for 20% of {n} nodes: {total_bst_duration*1000*1000:.6f} nanoseconds")
    print(f"Splay Tree search time for 20% of {n} nodes: {total_splay_duration*1000*1000:.6f} nanoseconds")
    print(f"Splay Tree was {'faster' if total_splay_duration < total_bst_duration else 'slower'} than BST by {abs(total_splay_duration - total_bst_duration)*1000*1000:.6f} nanoseconds")

def test_tree_insertion_search_comparison_random_100():
    n = 100
    
    # Generate products
    product_records = load_inventory_products()
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

    ## Insertion comparison
    # Build BST by product ID as String
    nodes = [BinarySearchNode(key=p.product_id, value=p) for p in products]
    bst = BinarySearchTree[BinarySearchNode[str]]()
    start_bst = time.perf_counter()
    for node in nodes:
        bst.insert(node.key, node.value)
    end_bst = time.perf_counter()
    total_bst_duration = end_bst - start_bst

    # Build BST by product ID as Integer
    nodes = [BinarySearchNode(key=int(p.product_id.replace("-", "")), value=p) for p in products]
    bstint = BinarySearchTree[int]()
    start_bstint = time.perf_counter()
    for node in nodes:
        bstint.insert(node.key, node.value)
    end_bstint = time.perf_counter()
    total_bstint_duration = end_bstint - start_bstint

    # Build Splay Tree by product ID as String
    nodes = [SplayNode(key=p.product_id, value=p) for p in products]
    splay_tree = SplayTree[SplayNode[str]]()
    start_splay = time.perf_counter()
    for node in nodes:
        splay_tree.insert(node.key, node.value)
    end_splay = time.perf_counter()
    total_splay_duration = end_splay - start_splay

    # Build Splay Tree by product ID as Integer
    nodes = [SplayNode(key=int(p.product_id.replace("-", "")), value=p) for p in products]
    splayint_tree = SplayTree[int]()
    start_splayint = time.perf_counter()
    for node in nodes:
        splayint_tree.insert(node.key, node.value)
    end_splayint = time.perf_counter()
    total_splayint_duration = end_splayint - start_splayint

    print()
    print(f"BST (STR) insertion time for {n} nodes: {total_bst_duration*1000*1000:.6f} nanoseconds")
    print(f"Splay Tree (STR) insertion time for {n} nodes: {total_splay_duration*1000*1000:.6f} nanoseconds")
    print(f"Splay Tree (STR) was {'faster' if total_splay_duration < total_bst_duration else 'slower'} than BST (STR) by {abs(total_splay_duration - total_bst_duration)*1000*1000:.6f} nanoseconds")

    print(f"BST (INT) insertion time for {n} nodes: {total_bstint_duration*1000*1000:.6f} nanoseconds")
    print(f"Splay Tree (INT) insertion time for {n} nodes: {total_splayint_duration*1000*1000:.6f} nanoseconds")
    print(f"Splay Tree (INT) was {'faster' if total_splayint_duration < total_bstint_duration else 'slower'} than BST (INT) by {abs(total_splayint_duration - total_bstint_duration)*1000*1000:.6f} nanoseconds")

    ## Search comparison
    # BST STR search
    start_bst = time.perf_counter()
    for p in products:
        bst.search(p.product_id)
    end_bst = time.perf_counter()
    total_bst_duration = end_bst - start_bst

    # BST INT search
    start_bstint = time.perf_counter()
    for p in products:
        bstint.search(int(p.product_id.replace("-", "")))
    end_bstint = time.perf_counter()
    total_bstint_duration = end_bstint - start_bstint

    # Splay Tree STR search
    start_splay = time.perf_counter()
    for p in products:
        splay_tree.search(p.product_id)
    end_splay = time.perf_counter()
    total_splay_duration = end_splay - start_splay

    # Splay Tree INT search
    start_splayint = time.perf_counter()
    for p in products:
        splayint_tree.search(int(p.product_id.replace("-", "")))
    end_splayint = time.perf_counter()
    total_splayint_duration = end_splayint - start_splayint

    print()
    print(f"BST search time for {n} nodes: {total_bst_duration*1000*1000:.6f} nanoseconds")
    print(f"Splay Tree search time for {n} nodes: {total_splay_duration*1000*1000:.6f} nanoseconds")
    print(f"Splay Tree was {'faster' if total_splay_duration < total_bst_duration else 'slower'} than BST by {abs(total_splay_duration - total_bst_duration)*1000*1000:.6f} nanoseconds")

    print(f"BST (INT) search time for {n} nodes: {total_bstint_duration*1000*1000:.6f} nanoseconds")
    print(f"Splay Tree (INT) search time for {n} nodes: {total_splayint_duration*1000*1000:.6f} nanoseconds")
    print(f"Splay Tree (INT) was {'faster' if total_splayint_duration < total_bstint_duration else 'slower'} than BST (INT) by {abs(total_splayint_duration - total_bstint_duration)*1000*1000:.6f} nanoseconds")

def test_tree_deletion_comparison_random_100():
    n = 100
    
    # Generate products
    product_records = load_inventory_products()
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

def test_tree_search_comparison_random_100_20percent():
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
    for _ in range(100): # repeat to amplify time difference
        for key in search_keys:
            bst.search(key)
    end_bst = time.perf_counter()
    total_bst_duration = end_bst - start_bst

    start_splay = time.perf_counter()
    for _ in range(100): # repeat to amplify time difference
        for key in search_keys:
            splay_tree.search(key)
    end_splay = time.perf_counter()
    total_splay_duration = end_splay - start_splay

    print()
    print(f"BST 20/80 search time for {n} nodes: {total_bst_duration*1000*1000:.6f} nanoseconds")
    print(f"Splay Tree 20/80 search time for {n} nodes: {total_splay_duration*1000*1000:.6f} nanoseconds")
    print(f"Splay Tree was {'faster' if total_splay_duration < total_bst_duration else 'slower'} than BST by {abs(total_splay_duration - total_bst_duration)*1000*1000:.6f} nanoseconds")