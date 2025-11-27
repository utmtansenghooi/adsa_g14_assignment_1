from src.pos_system.inventory.binary_search_tree import BinarySearchTree, BinarySearchNode
from src.pos_system.inventory.splay_tree import SplayTree, SplayNode
from src.pos_system.inventory.inventory_data_loader import build_inventory_bst, build_inventory_splay_tree, InventoryKeyType
from src.pos_system.common.Product import Product
from src.pos_system.common.data_loader import load_inventory_products
from src.pos_system.common.logger import log_operation, timed_operation
import time
import random
import string
from splay_mod import Splay
from Binary_Search_Trees import BST

def test_tree_normal_comparison_random_100():
    n = 100
    
    # Generate numbers
    numbers = list(range(n))
    random.shuffle(numbers)
    numbers_str = [str(num) for num in numbers]

    ## Insertion comparison
    # Build BST
    bst_str = BinarySearchTree[str]()
    start_bst = time.perf_counter()
    for num in numbers_str:
        bst_str.insert(num)
    end_bst = time.perf_counter()
    total_bst_duration = end_bst - start_bst

    # Build Splay Tree
    splay_tree_str = SplayTree[str]()
    start_splay = time.perf_counter()
    for num in numbers_str:
        splay_tree_str.insert(num)
    end_splay = time.perf_counter()
    total_splay_duration = end_splay - start_splay

    print()
    print(f"BST str insertion time for {n} nodes: {total_bst_duration*1000*1000:.6f} nanoseconds")
    print(f"Splay Tree str insertion time for {n} nodes: {total_splay_duration*1000*1000:.6f} nanoseconds")
    print(f"Splay Tree str was {'faster' if total_splay_duration < total_bst_duration else 'slower'} than BST str by {abs(total_splay_duration - total_bst_duration)*1000*1000:.6f} nanoseconds")

    # Build BST with library
    bst_library = BST.CreateBST()
    start_bst = time.perf_counter()
    for num in numbers_str:
        BST.Insert(bst_library, num)
    end_bst = time.perf_counter()
    total_bst_duration = end_bst - start_bst

    # Build Splay Tree with library
    splay_tree_library = Splay()
    start_splay = time.perf_counter()
    for num in numbers_str:
        splay_tree_library[num] = None
    end_splay = time.perf_counter()
    total_splay_duration = end_splay - start_splay

    print()
    print(f"BST library insertion time for {n} nodes: {total_bst_duration*1000*1000:.6f} nanoseconds")
    print(f"Splay Tree library insertion time for {n} nodes: {total_splay_duration*1000*1000:.6f} nanoseconds")
    print(f"Splay Tree library was {'faster' if total_splay_duration < total_bst_duration else 'slower'} than BST by {abs(total_splay_duration - total_bst_duration)*1000*1000:.6f} nanoseconds")

    ## Search comparison
    # BST search
    start_bst = time.perf_counter()
    for _ in range(100): # repeat to amplify time difference
        for num in numbers_str:
            bst_str.search(num)
    end_bst = time.perf_counter()
    total_bst_duration = end_bst - start_bst

    # Splay Tree search
    start_splay = time.perf_counter()
    for _ in range(100): # repeat to amplify time difference
        for num in numbers_str:
            splay_tree_str.search(num)
    end_splay = time.perf_counter()
    total_splay_duration = end_splay - start_splay

    print()
    print(f"BST str search time for {n} nodes: {total_bst_duration*1000*1000:.6f} nanoseconds")
    print(f"Splay Tree str search time for {n} nodes: {total_splay_duration*1000*1000:.6f} nanoseconds")
    print(f"Splay Tree str was {'faster' if total_splay_duration < total_bst_duration else 'slower'} than BST str by {abs(total_splay_duration - total_bst_duration)*1000*1000:.6f} nanoseconds")

    # BST search with library
    start_bst = time.perf_counter()
    for _ in range(100): # repeat to amplify time difference
        for num in numbers_str:
            BST.Find(bst_library, num)
    end_bst = time.perf_counter()
    total_bst_duration = end_bst - start_bst

    # Splay Tree search with library
    start_splay = time.perf_counter()
    for _ in range(100): # repeat to amplify time difference
        for num in numbers_str:
            splay_tree_library.find(num)
    end_splay = time.perf_counter()
    total_splay_duration = end_splay - start_splay

    print()
    print(f"BST library search time for {n} nodes: {total_bst_duration*1000*1000:.6f} nanoseconds")
    print(f"Splay Tree library search time for {n} nodes: {total_splay_duration*1000*1000:.6f} nanoseconds")
    print(f"Splay Tree library was {'faster' if total_splay_duration < total_bst_duration else 'slower'} than BST str by {abs(total_splay_duration - total_bst_duration)*1000*1000:.6f} nanoseconds")

    ## Search 20% comparison
    search_keys = numbers_str[:int(n*0.2)]
    # BST search
    start_bst = time.perf_counter()
    for _ in range(100): # repeat to amplify time difference
        for num in search_keys:
            bst_str.search(num)
    end_bst = time.perf_counter()
    total_bst_duration = end_bst - start_bst

    # Splay Tree search
    start_splay = time.perf_counter()
    for _ in range(100): # repeat to amplify time difference
        for num in search_keys:
            splay_tree_str.search(num)
    end_splay = time.perf_counter()
    total_splay_duration = end_splay - start_splay

    print()
    print(f"BST search time for 20% of {n} nodes: {total_bst_duration*1000*1000:.6f} nanoseconds")
    print(f"Splay Tree search time for 20% of {n} nodes: {total_splay_duration*1000*1000:.6f} nanoseconds")
    print(f"Splay Tree was {'faster' if total_splay_duration < total_bst_duration else 'slower'} than BST by {abs(total_splay_duration - total_bst_duration)*1000*1000:.6f} nanoseconds")

    # BST search with library
    start_bst = time.perf_counter()
    for _ in range(100): # repeat to amplify time difference
        for num in search_keys:
            BST.Find(bst_library, num)
    end_bst = time.perf_counter()
    total_bst_duration = end_bst - start_bst

    # Splay Tree search with library
    start_splay = time.perf_counter()
    for _ in range(100): # repeat to amplify time difference
        for num in search_keys:
            splay_tree_library.find(num)
    end_splay = time.perf_counter()
    total_splay_duration = end_splay - start_splay

    print()
    print(f"BST library search time for 20% of {n} nodes: {total_bst_duration*1000*1000:.6f} nanoseconds")
    print(f"Splay Tree library search time for 20% of {n} nodes: {total_splay_duration*1000*1000:.6f} nanoseconds")
    print(f"Splay Tree library was {'faster' if total_splay_duration < total_bst_duration else 'slower'} than BST by {abs(total_splay_duration - total_bst_duration)*1000*1000:.6f} nanoseconds")