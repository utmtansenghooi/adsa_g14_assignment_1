from src.pos_system.inventory.binary_search_tree import BinarySearchTree, BinarySearchNode
from src.pos_system.inventory.splay_tree import SplayTree, SplayNode
from src.pos_system.inventory.inventory_data_loader import build_inventory_bst, build_inventory_splay_tree, InventoryKeyType
from src.pos_system.common.Product import Product
from src.pos_system.common.data_loader import load_inventory_products
from src.pos_system.common.logger import log_operation, timed_operation
import time
import random
import string
import sys


# Increase recursion depth for deep trees (Scenario B)
sys.setrecursionlimit(5000)

def load_products():
    # Load products
    product_records = load_inventory_products()
    products = []
    for record in product_records:
        product = Product(
            product_id=str(record["product_id"]),
            name=str(record["name"]),
            category=str(record["category"]),
            price=float(record["price"]),
            quantity=int(record["quantity"])
        )
        products.append(product)
    return products


def generate_tree(products):
    # 2. Instantiate and populate the trees
    bst = BinarySearchTree()
    splay_tree = SplayTree()
    
    # Insert the product objects in the calculated balanced order
    for p in products:
        bst.insert(p.product_id, p)
        splay_tree.insert(p.product_id, p)
    
    return bst, splay_tree


def generate_balanced_tree(products):
    # 1. Sort the full list of product objects based on product_id.
    # The sorted list is now the input for the balanced insertion logic.
    sorted_products = sorted(products, key=lambda s: s.product_id)

    def _balanced_insertion(products_list, low, high, order):
        if low > high:
            return

        # find middle element (this is the root/sub-root)
        mid = (low + high) // 2
        
        # Append the actual product object from the sorted list
        order.append(products_list[mid])

        # recursively build left subtree
        _balanced_insertion(products_list, low, mid - 1, order)

        # recursively build the right subtree
        _balanced_insertion(products_list, mid + 1, high, order)

    insertion_order = []
    # Use the sorted list of actual product objects
    _balanced_insertion(sorted_products, 0, len(sorted_products) - 1, insertion_order)

    # 2. Instantiate and populate the trees
    bst = BinarySearchTree()
    splay_tree = SplayTree()
    
    # Insert the product objects in the calculated balanced order
    for p in insertion_order:
        bst.insert(p.product_id, p)
        splay_tree.insert(p.product_id, p)
    
    return bst, splay_tree


def run_benchmark(scenario_name, operations, bst, splay):
    # 1. Measure BST
    start_time = time.perf_counter()
    for op_type, pid, pname in operations:
        if op_type == 'insert':
            bst.insert(pid, pname)
        elif op_type == 'search':
            bst.search(pid)
    bst_time = time.perf_counter() - start_time

    # 2. Measure Splay
    start_time = time.perf_counter()
    for op_type, pid, pname in operations:
        if op_type == 'insert':
            splay.insert(pid, pname)
        elif op_type == 'search':
            splay.search(pid)
    splay_time = time.perf_counter() - start_time

    return (bst_time, splay_time)


def execute_test(title, operation, products, iterations, bst=None, splay=None):
    # Initialize BST and Splay tree
    bst = BinarySearchTree() if bst is None else bst
    splay = SplayTree() if splay is None else splay

    # Prepare same operation sequences for both BST and Splay
    ops = []
    for p in products:
        ops.append((f'{operation}', p.product_id, p))
    size = len(ops)

    bst_times = []
    splay_times = []
    # log_operation(f"{title}")
    for i in range(iterations):
        bst_time, splay_time = run_benchmark(f"{title} [{i}]", ops, bst, splay)
        bst_times.append(bst_time)
        splay_times.append(splay_time)

    average_bst_times = sum(bst_times)/iterations
    average_splay_times = sum(splay_times)/iterations
    # log_operation(f"BST {operation} {size} ({iterations} iterations): {bst_times}")
    # log_operation(f"BST {operation} {size} average: {average_bst_times}s")
    # log_operation(f"Splay {operation} {size} ({iterations} iterations): {splay_times}")
    # log_operation(f"Splay {operation} {size} average: {average_splay_times}s")
    log_operation(f"{title[:10]},{size:4},{average_bst_times:.6f},{average_splay_times:.6f}")


def test_tree_insert_random():
    """
    Scenario A: Random Insert
    Inventory: 50 | 100 | 200 | 400 | 800 | 1000 items
    Simulates: Normal day-to-day stock entry
    Compares: Baseline comparison of insertion speed
    """
    products = load_products()

    # Shuffle products to produce randomized list
    random.shuffle(products)

    # Configuration for all tests
    print()
    iterations = 10
    inventory_sizes = [50, 100, 200, 400, 800, 1000]
    for inventory in inventory_sizes:
        p = products[:inventory]
        execute_test(f"Scenario A: Random Insert {inventory} Dataset", "insert", p, iterations)


def test_tree_insert_sorted():
    """
    Scenario B: Sorted Insert
    Inventory: 50 | 100 | 200 | 400 | 800 | 1000 items
    Simulates: Importing a sorted product list (Product IDs)
    Compares: Force BST into worst case, minimal impact to Splay
    """
    products = load_products()

    # Sort products to produce sorted list
    products.sort(key=lambda s: s.product_id)

    # Configuration for all tests
    print()
    iterations = 10
    inventory_sizes = [50, 100, 200, 400, 800, 1000]
    for inventory in inventory_sizes:
        p = products[:inventory]
        execute_test(f"Scenario B: Sorted Insert {inventory} Dataset", "insert", p, iterations)


def test_tree_search_random():
    """
    Scenario C: Random Search
    Inventory: 50 | 100 | 200 | 400 | 800 | 1000 items
    Simulates: Checking stock for random items.
    Compares: Baseline comparison.
    """
    products = load_products()

    # Shuffle products to produce randomized list
    random.shuffle(products)

    # Configuration for all tests
    print()
    iterations = 10
    inventory_sizes = [50, 100, 200, 400, 800, 1000]
    for inventory in inventory_sizes:
        p = products[:inventory]
        # Generate balanced BST and Splay tree for fair comparison
        bst, splay = generate_balanced_tree(p)
        execute_test(f"Scenario C: Random Search {inventory} Dataset", "search", p, iterations, bst, splay)


def test_tree_search_20percent_random():
    """
    Scenario D: Search 20% of popular items randomly
    Inventory: 50 | 100 | 200 | 400 | 800 | 1000 items
    Simulates: The checkout counter, 80% of scans are for 20% of products
    Compares: Demonstrate effect of dynamic tree (splay) compared to static tree
    """
    products = load_products()

    # Shuffle products to produce randomized list
    random.shuffle(products)

    # Configuration for all tests
    print()
    hot_set_percentage = 20 # percent
    iterations = 10
    inventory_sizes = [50, 100, 200, 400, 800, 1000]
    for inventory in inventory_sizes:
        # Prepare hot and cold sets of products
        p = products[:inventory]
        split_index = int(len(p) * (hot_set_percentage/100))
        hot_set = p[:split_index]  # The 20%
        cold_set = p[split_index:] # The 80%

        # Generate balanced BST and Splay tree for fair comparison
        bst, splay = generate_balanced_tree(p)

        # Generate skewed sequence of product search
        s = []
        for _ in range(inventory*100):
            if random.random() < 0.8:
                # 80% chance to access Hot Set
                target = random.choice(hot_set)
            else:
                # 20% chance to access Cold Set
                target = random.choice(cold_set)
            s.append(target)

        execute_test(f"Scenario D: 80/20 Skewed Search {inventory} Dataset", "search", s, iterations, bst, splay)


def test_tree_search_20percent_sorted():
    """
    Scenario E: Search 20% of popular items with similar product-id (Locality of reference)
    Inventory: 50 | 100 | 200 | 400 | 800 | 1000 items
    Simulates: The checkout counter, 80% of scans are for 20% of products (that are pre-grouped together)
    Compares: Demonstrate the ideal effect of dynamic tree (splay) compared to static tree
    """
    products = load_products()

    # Sort products to produce sorted list (so that 20% of products have similar product-id)
    products.sort(key=lambda s: s.product_id)

    # Configuration for all tests
    print()
    hot_set_percentage = 20 # percent
    iterations = 10
    # inventory_sizes = [50, 100, 200, 400, 800, 1000]
    inventory_sizes = [20]
    for inventory in inventory_sizes:
        # Prepare hot and cold sets of products
        p = products[:inventory]
        split_index = int(len(p) * (hot_set_percentage/100))
        hot_set = p[:split_index]  # The 20%
        cold_set = p[split_index:] # The 80%

        # Generate balanced BST and Splay tree for fair comparison
        bst, splay = generate_balanced_tree(p)
        
        # Generate skewed sequence of product search
        s = []
        for _ in range(inventory):
            if random.random() < 0.8:
                # 80% chance to access Hot Set
                target = random.choice(hot_set)
            else:
                # 20% chance to access Cold Set
                target = random.choice(cold_set)
            s.append(target)

        execute_test(f"Scenario E: 80/20 Skewed Grouped Search {inventory} Dataset", "search", s, iterations, bst, splay)