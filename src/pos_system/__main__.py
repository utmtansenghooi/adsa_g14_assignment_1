"""Supermarket POS System - Main entry point."""
import time
from src.pos_system.common.Customer import Customer
from src.pos_system.loyalty.avl_tree import AVLTree
from src.pos_system.loyalty.binary_tree import BSTTree
from src.pos_system.common.data_loader import load_customers, save_customers
from src.pos_system.common.logger import log_operation, timed_operation
from src.pos_system.loyalty import update_points, calculate_discount, top_n_customers, range_query
from src.pos_system.inventory.inventory_module import InventoryModule
from src.pos_system.sales.bst import main as SalesModule
import os


def inventory_demo():
    """Inventory management demo by Tan Seng Hooi"""
    print("Inventory Module Demo")
    InventoryModule().operate()


def sales_demo():
    """Sales transactions demo by Quek Boon Siang"""
    print("Sales Module Demo")
    SalesModule()


def loyalty_demo():
    """Loyalty transactios demo by Chang Choon Kit"""
    bst = BSTTree()
    avl = AVLTree()

    # Load customers at start
    customer_file = os.path.join("data", "loyalty", "customers.csv")
    load_customers(customer_file, bst, avl)

    while True:
        print("\n--- Supermarket Loyalty System ---")
        print("1. New Customer Registration")
        print("2. Purchase / Earn Points")
        print("3. Customer Removal")
        print("4. Query / Report (All Customers)")
        print("5. Top N Customers by Points")
        print("6. Range Query by Points")
        print("7. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            cid = input("Customer ID: ")
            name = input("Name: ")
            customer = Customer(cid, name)
            bst_result, bst_time = timed_operation(bst.insert, customer)
            avl_result, avl_time = timed_operation(avl.insert, customer)
            if bst_result or avl_result:
                print(f"Customer {cid} inserted.")
                print(f"BST insert duration: {bst_time:.6f} seconds")
                print(f"AVL insert duration: {avl_time:.6f} seconds")
            else:
                print(f"Customer {cid} already exists. No insert performed.")

        elif choice == "2":
            cid = input("Customer ID: ")
            points = int(input("Points Earned: "))
            bst_result, bst_time = timed_operation(update_points, bst, cid, points)
            avl_result, avl_time = timed_operation(update_points, avl, cid, points)
            if bst_result or avl_result:
                print(f"Customer {cid} inserted.")
                print(f"BST search and update duration: {bst_time:.6f} seconds")
                print(f"AVL search and update duration: {avl_time:.6f} seconds")
            else:
                print(f"Customer {cid} not found. No update performed.")

        elif choice == "3":
            cid = input("Customer ID to remove: ")
            bst_result, bst_time = timed_operation(bst.delete, cid)
            avl_result, avl_time = timed_operation(avl.delete, cid)
            print(f"Customer {cid} removed.")
            print(f"BST delete duration: {bst_time:.6f} seconds")
            print(f"AVL delete duration: {avl_time:.6f} seconds")
            log_operation(f"Customer {cid} removed from both trees.")

        elif choice == "4":
            bst_customers, bst_time = timed_operation(bst.inorder_traversal)
            avl_customers, avl_time = timed_operation(avl.inorder_traversal)

            print("\n--- All Customers in BST ---")
            for c in bst_customers:
                print(f"{c} | Discount: {calculate_discount(c)}%")
            print("\n--- All Customers in AVL ---")
            for c in avl_customers:
                print(f"{c} | Discount: {calculate_discount(c)}%")
            print(f"BST traversal duration: {bst_time:.6f} seconds")
            print(f"AVL traversal duration: {avl_time:.6f} seconds")

        elif choice == "5":
            n = int(input("Enter N for top N customers: "))
            top_bst, bst_time = timed_operation(top_n_customers, bst, n)
            top_avl, avl_time = timed_operation(top_n_customers, avl, n)

            print(f"\n--- Top {n} Customers in BST ---")
            for c in top_bst:
                print(f"{c} | Discount: {calculate_discount(c)}%")
            print(f"\n--- Top {n} Customers in AVL ---")
            for c in top_avl:
                print(f"{c} | Discount: {calculate_discount(c)}%")
            print(f"BST Top N duration: {bst_time:.6f} seconds")
            print(f"AVL Top N duration: {avl_time:.6f} seconds")

        elif choice == "6":
            min_points = int(input("Enter minimum points: "))
            max_points = int(input("Enter maximum points: "))
            range_bst, bst_time = timed_operation(range_query, bst, min_points, max_points)
            range_avl, avl_time = timed_operation(range_query, avl, min_points, max_points)

            print(f"\n--- Customers with Points {min_points}-{max_points} in BST ---")
            for c in range_bst:
                print(f"{c} | Discount: {calculate_discount(c)}%")
            print(f"\n--- Customers with Points {min_points}-{max_points} in AVL ---")
            for c in range_avl:
                print(f"{c} | Discount: {calculate_discount(c)}%")
            print(f"BST range query duration: {bst_time:.6f} seconds")
            print(f"AVL range query duration: {avl_time:.6f} seconds")
        elif choice == "7":
            # Save before exit
            save_customers(customer_file, bst, avl)
            print("Exiting system.")
            break

        else:
            print("Invalid choice. Try again.")


def main():
    """Main CLI entry point."""
    print("=" * 60)
    print("  Supermarket POS System")
    print("=" * 60)
    print("\nAvailable modules:")
    print("  1. Inventory Management")
    print("  2. Sales Transactions")
    print("  3. Customer Loyalty")
    while True:
        try:
            user_input = input("Which module would you like to use? ")
            if user_input == "1":
                inventory_demo()
            elif user_input == "2":
                sales_demo()
            elif user_input == "3":
                loyalty_demo()
            else:
                print("No such module...")
            return
        except (ValueError):
            print(f"Invalid input. Please enter a valid choice.")


if __name__ == "__main__":
    main()
