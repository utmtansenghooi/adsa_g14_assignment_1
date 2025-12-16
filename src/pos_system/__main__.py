"""Supermarket POS System - Main entry point."""
import time
from src.pos_system.inventory.inventory_module import InventoryModule, DataStructureType
import os


def inventory_demo():
    """Inventory management demo by Tan Seng Hooi"""
    data_structure = DataStructureType.BST
    print("Inventory Module Demo")
    while True:
        try:
            print("\nAvailable data structures:")
            print("  1. Binary Search Tree")
            print("  2. Splay Tree (Bottom up)")
            print("  3. Improved Splay Tree (Top down)")
            user_input = input("Which Data Structure would you like to use? ")
            if user_input == "1":
                data_structure = DataStructureType.BST
            elif user_input == "2":
                data_structure = DataStructureType.SPLAY
            elif user_input == "3":
                data_structure = DataStructureType.IMPROVED_SPLAY
            else:
                print("No such data structure...")
            break
        except (ValueError):
            print(f"Invalid input. Please enter a valid choice.")
    InventoryModule(data_structure = data_structure).operate()

def main():
    """Main CLI entry point."""
    print("=" * 60)
    print("  Supermarket POS System")
    print("=" * 60)
    print("\nAvailable modules:")
    print("  1. Inventory Management")
    while True:
        try:
            user_input = input("Which module would you like to use? ")
            if user_input == "1":
                inventory_demo()
            else:
                print("No such module...")
            return
        except (ValueError):
            print(f"Invalid input. Please enter a valid choice.")


if __name__ == "__main__":
    main()
