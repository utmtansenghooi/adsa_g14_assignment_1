import time
from src.pos_system.inventory.inventory_data_loader import build_inventory_bst, build_inventory_splay_tree, build_inventory_improved_splay_tree, InventoryKeyType
from src.pos_system.common.Product import Product
from enum import Enum

class DataStructureType(Enum):
    BST = 1
    SPLAY = 2
    IMPROVED_SPLAY = 3

class InventoryModule:

    def __init__(self, data_structure: DataStructureType = DataStructureType.BST):
        if data_structure is DataStructureType.BST:
            self.inventory_data = build_inventory_bst(key_type=InventoryKeyType.PRODUCT_ID, class_type=str, entries=100)
        elif data_structure is DataStructureType.SPLAY:
            self.inventory_data = build_inventory_splay_tree(key_type=InventoryKeyType.PRODUCT_ID, class_type=str, entries=100)
        elif data_structure is DataStructureType.IMPROVED_SPLAY:
            self.inventory_data = build_inventory_improved_splay_tree(key_type=InventoryKeyType.PRODUCT_ID, class_type=str, entries=100)

    def _entry(self, message: str, allowed_input: type):
        while True:
            try:
                user_input = input(message)
                converted_input = allowed_input(user_input)
                return converted_input
            except (ValueError, TypeError):
                print(f"Invalid input. Please enter a valid {allowed_input.__name__}.")

    def display_inventory_menu(self):
        print("###################################")
        print("|      Supermarket POS System     |")
        print("|         Inventory Module        |")
        print("|             Main Menu           |")
        print("###################################")
        print("1. Insert new inventory item")
        print("2. Search inventory by id")
        print("3. Delete inventory item by id")
        print("4. Display all inventory items")
        print("5. Exit")
    
    def operate(self):
        while True:
            self.display_inventory_menu()
            choice = self._entry("Enter your choice (1-5): ", int)
            if choice >= 1 and choice <= 5:
                if choice == 1:
                    self.insert_item()
                elif choice == 2:
                    self.search_item()
                elif choice == 3:
                    self.delete_item()
                elif choice == 4:
                    self.display_data()
                elif choice == 5:
                    print("Exiting Inventory Module...")
                    break
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")

    def insert_item(self):
        print("Please provide:")
        product_id = self._entry("Product ID (eg. 29-205-1132):", str)
        name = self._entry("Name (eg. Eggs):", str)
        category = self._entry("Category (eg. Dairy):", str)
        price = self._entry("Price (eg. 10.59):", float)
        quantity = self._entry("Quantity (eg. 15):", int)
        product = Product(product_id, name, category, price, quantity)
        node = BinarySearchNode(key=product.product_id, value=product)
        start_bst = time.perf_counter()
        self.inventory_data.insert(node.key, node.value)
        end_bst = time.perf_counter()
        total_bst_duration = end_bst - start_bst
        print(f"Item inserted in {total_bst_duration*1000*1000:.3f}ns")
    
    def search_item(self):
        product_id = self._entry("Provide Product ID (eg. 29-205-1132) to search:", str)
        start_bst = time.perf_counter()
        node = self.inventory_data.search(product_id)
        end_bst = time.perf_counter()
        total_bst_duration = end_bst - start_bst
        print(f"Item {'found' if node else 'not found'} in {total_bst_duration*1000*1000:.3f}ns")
        if node:
            item = node.value
            print(f"\n{'Product ID':<20} | {'Name':<20} | {'Category':<25} | {'Price':<10} | {'Quantity':<10}")
            print("-" * 80)
            print(f"{item.product_id:<20} | {item.name:<20} | {item.category:<25} | ${item.price:<9.2f} | {item.quantity:<10}")

    def delete_item(self):
        product_id = self._entry("Provide Product ID (eg. 29-205-1132) to delete:", str)
        start_bst = time.perf_counter()
        item = self.inventory_data.delete(product_id)
        end_bst = time.perf_counter()
        total_bst_duration = end_bst - start_bst
        print(f"Item deleted in {total_bst_duration*1000*1000:.3f}ns")
    
    def display_data(self):
        if not self.inventory_data.root:
            print("No product data...")
            return
        print(f"\n{'Product ID':<20} | {'Name':<20} | {'Category':<25} | {'Price':<10} | {'Quantity':<10}")
        print("-" * 80)
        number_of_items = 0
        for node in self.inventory_data.traverse():
            number_of_items+=1
            item = node.value
            print(f"{item.product_id:<20} | {item.name:<20} | {item.category:<25} | ${item.price:<9.2f} | {item.quantity:<10}")
        print(f"Total {number_of_items} products in inventory.")
        
if __name__ == "__main__":
    InventoryModule().operate()