"""Supermarket POS System - Main entry point."""
import time
from src.pos_system.inventory.inventory_module import InventoryModule
import os


def inventory_demo():
    """Inventory management demo by Tan Seng Hooi"""
    print("Inventory Module Demo")
    InventoryModule().operate()

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
