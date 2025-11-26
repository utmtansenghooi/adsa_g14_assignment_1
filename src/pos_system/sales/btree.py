### Import what is needed ###
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pyodbc
from datetime import datetime
import time
from collections import defaultdict
import sys
from typing import Any, List, Optional, Tuple
import os


##################################
###      B-Tree Node class     ###
### Abstract Data Type: B-Tree ###
##################################
class BTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []  # List of (key, value) tuples
        self.children = []

##################################
###        B-Tree class        ###
##################################
class BTree:
    def __init__(self, t):
        self.root = BTreeNode(True)
        self.t = t  # Minimum degree

    def insert(self, k, v):
        root = self.root
        if len(root.keys) == (2 * self.t - 1):
            temp = BTreeNode()
            self.root = temp
            temp.children.insert(0, root)
            self._split_child(temp, 0)
            self._insert_non_full(temp, k, v)
        else:
            self._insert_non_full(root, k, v)

    def _insert_non_full(self, x, k, v):
        i = len(x.keys) - 1
        if x.leaf:
            x.keys.append((None, None))
            while i >= 0 and k < x.keys[i][0]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = (k, v)
        else:
            while i >= 0 and k < x.keys[i][0]:
                i -= 1
            i += 1
            if len(x.children[i].keys) == (2 * self.t - 1):
                self._split_child(x, i)
                if k > x.keys[i][0]:
                    i += 1
            self._insert_non_full(x.children[i], k, v)

    def _split_child(self, x, i):
        t = self.t
        y = x.children[i]
        z = BTreeNode(y.leaf)
        x.children.insert(i + 1, z)
        x.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t:(2 * t - 1)]
        y.keys = y.keys[0:(t - 1)]
        if not y.leaf:
            z.children = y.children[t:(2 * t)]
            y.children = y.children[0:t]

    def search_key(self, k):
        return self._search(self.root, k)

    def _search(self, x, k):
        i = 0
        while i < len(x.keys) and k > x.keys[i][0]:
            i += 1
        if i < len(x.keys) and k == x.keys[i][0]:
            return x.keys[i][1]
        if x.leaf:
            return None
        return self._search(x.children[i], k)
################# END B-TREE ######################

###################################################
# Abstract Data Type: Binary Search Tree (BST) #
class Node:
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, key, data):
        if self.root is None:
            self.root = Node(key, data)
        else:
            self._insert(self.root, key, data)

    def _insert(self, node, key, data):
        if key < node.key:
            if node.left is None:
                node.left = Node(key, data)
            else:
                self._insert(node.left, key, data)
        elif key > node.key:
            if node.right is None:
                node.right = Node(key, data)
            else:
                self._insert(node.right, key, data)
        else:
            # Update data if key exists
            node.data = data

    def search(self, key):
        return self._search(self.root, key)

    def search_key(self, key):
        return self.search(key)          # delegate to the real method

    def _search(self, node, key):
        if node is None:
            return None
        if key == node.key:
            return node.data
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)
################## END BST #########################

###################################################
###    Connect to source (MS Access database)   ###
###################################################
#db_path = os.path.join(os.getcwd(), "UTM_BST_data.accdb")
#print("DB Path:", db_path)
#print("Exists?", os.path.exists(db_path))
#print("ODBC Path: ", pyodbc.drivers())

db_path = os.path.join(os.getcwd(), "UTM_BST_data.accdb")
table_stored_name = "Sample_Transaction"

conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + db_path + ";")
cursor = conn.cursor()

##### Data Upload to B-Tree & BST ##### 
# Initialize B-Tree (order 3 for example)
btree = BTree(3)
#Initialize Binary Search Tree (BST)
bst = BST()
# Load existing transactions from Sample_Transaction into B-Tree
transactions = defaultdict(list)


date_times = {}
cursor.execute(f"SELECT Transaction_Id, Item_Code, Item_Description, qty, Unit_Price, Total_Item_Amount, Trans_Date FROM {table_stored_name}")

for row in cursor.fetchall():
    ### this is for B-Tree ###
    #print("Transaction_id", receipt_id)
    receipt_id = str(row.Transaction_Id)
    transactions[receipt_id].append({
        'Item_Code': str(row.Item_Code or "").strip(),
        'Item_Desc': str(row.Item_Description or "").strip(),
        'qty': int(row.qty),
        'Unit_Price': float(row.Unit_Price),
        'SubTotal': float(row.Total_Item_Amount)
     })
    date_times[receipt_id] = row.Trans_Date

    #Get all the receipt id using group by 
    #trans_groups = row.groupby('Transaction_Id')
    #transaction__all_ids = list(trans_groups.groups.keys())

for receipt_id in transactions:
    btree.insert(receipt_id, {
        'date_time': date_times[receipt_id],
        'items': transactions[receipt_id]
    })

    bst.insert(receipt_id, {
        'date_time': date_times[receipt_id],
        'items': transactions[receipt_id]
    })

    # Get all the receipt id using group by 
    #trans_groups = transactions[receipt_id].groupby
    #trans_groups = transactions.groupby('Transaction_Id')
    #transaction__all_ids = list(trans_groups.groups.keys())
###################################################


# Main menu
while True:
    print()
    print("###################################")
    print("|      Supermarket POS System     |")
    print("|    Sales Transaction Module     |")
    print("|          Main Menu              |")
    print("###################################")
    print("1. Insert new sales transaction")
    print("2. Search and print sales receipt")
    #print("3. Speed Testing For Single Receipt ID Searching Between B-Tree and BST")
    #print("4. Speed Testing For All Rceipt ID Searching Between B-Tree and BST With Graph")    
    print("0. Exit")
    choice = input("Enter your choice (0/1/2): ")

    if choice == '1':
        # Read from Sample_Sales
        new_transactions_btree = defaultdict(list)
        new_date_times = {}
        #cursor.execute("SELECT ReceiptID, ItemID, ItemName, Quantity, Price, TransactionDateTime FROM Sample_Sales")
        cursor.execute("SELECT Transaction_Id, Item_Code, Item_Description, qty, Unit_Price, Total_Item_Amount, Trans_Date FROM Sample_Sales")
        rows = cursor.fetchall()
        for row in rows:
            receipt_id = str(row.Transaction_Id)
            new_transactions_btree[receipt_id].append({
                'Item_Code': str(row.Item_Code or "").strip(),
                'Item_Desc': str(row.Item_Description or "").strip(),
                'qty': int(row.qty)if row.qty is not None else 0,
                'Unit_Price': float(row.Unit_Price) if row.Unit_Price is not None else 0.0,
                'SubTotal': float(row.Total_Item_Amount)  if row.Total_Item_Amount is not None else 0.0
            })
            new_date_times[receipt_id] = row[6]  # Assume same for all items in receipt

        for receipt_id in new_transactions_btree:
            items = new_transactions_btree[receipt_id]
            date_time = new_date_times[receipt_id]

            # Update stock for each item
            sufficient_stock = True
            for item in items:
                cursor.execute("SELECT Product_Qty FROM Product WHERE Product_Code = ?", (item['Item_Code'],))
                stock_row = cursor.fetchone()
                #print(f"Product Code: {item['Item_Code']}")
                if stock_row:
                    stock_qty = stock_row[0]
                    new_qty = stock_qty
                    #print(f"AA stock_qty: {stock_qty}")
                    #print(f"BB stock_row[0]: {stock_row[0]}")
                    if stock_qty < item['qty']:
                        print(f"Insufficient stock for item {item['Item_Desc']} in receipt {receipt_id}")
                        sufficient_stock = False
                        break
                else:
                    print(f"Item {item['Item_Desc']} not found in stock for receipt {receipt_id}")
                    sufficient_stock = False
                    break

            if not sufficient_stock:
                continue  # Skip this receipt if stock insufficient
            
            for item in items:
                upd_qty = 0
                upd_qty = new_qty - item['qty']
                
                cursor.execute("update Product set Product_Qty = ? WHERE Product_Code = ?",  (int(upd_qty) ,str(item['Item_Code'])))
                              

            # Insert into Sample_Transaction
            for item in items:
                cursor.execute(
                    "INSERT INTO Sample_Transaction (Transaction_Id, Item_Code, Item_Description, qty, Unit_Price, Trans_Date, Total_Item_Amount) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (receipt_id, item['Item_Code'], item['Item_Desc'], item['qty'], item['Unit_Price'], date_time, item['SubTotal'])
                )

            # Insert into B-Tree
            btree.insert(receipt_id, {'date_time': date_time, 'items': items})
            total_1 = 0
            item_count_1 = 0
            
            # Generate and print receipt
            #print(f"\nReceipt ID: {receipt_id}")
            print()
            print("=" * 64)
            print(f"{'Supermarket POS Receipt':^60}")
            print("=" * 64)
            print(f"{'Receipt ID:'} {receipt_id:>12}")    
            print(f"{'Date      :'} {date_time.strftime("%Y-%m-%d"):>12}")
            print(f"{'Time      :'} {date_time.strftime("%H:%M:%S"):>12}")
            print("-" * 64)
            print(f"{'Item':<31} {'Qty':>7} {'Price':>11} {'Sub Total':>11}")
            print("-" * 64)
            #print(f"Date Time: {date_time}")
            total = 0
            for item in items:
                #subtotal = item['qty'] * item['Unit_Price']
                print(f"{item['Item_Desc']:<31} {item['qty']:>7} {item['Unit_Price']:>11.2f} {item['SubTotal']:>11.2f}")
                total_1 += item['SubTotal']
                item_count_1 += 1
            #print(f"Total: {total_1:>32.2f}")
            print("-" * 64)
            print(f"{'Grand Total (RM)        : ':>30} {total_1:>32.2f}")
            print(f"{'Total Purchased Item(s) : ':>30} {int(item_count_1):>32}")
            print("=" * 64)
            print(f"{'Thank you for shopping with us':>45}")
            print("=" * 64) 

        # Commit changes and clear Sample_Sales - the temp table
        conn.commit()
        cursor.execute("DELETE FROM Sample_Sales")
        conn.commit()
        print("Sales transactions inserted successfully.")

    elif choice == '2':
        
        try:
            receipt_id = str(input("Enter Receipt ID: "))

            ############################################
            ###        B-Tree Start Searching        ###
            ############################################
            start_time = time.perf_counter_ns()
            transaction_btree = btree.search_key(receipt_id)
            end_time = time.perf_counter_ns()
            search_time = (end_time - start_time) / 1000
            ############################################
          
            if transaction_btree:
                ############################################
                ###        Transaction Date/Time         ###
                ############################################
                dt = transaction_btree['date_time']
                date_str = dt.strftime("%Y-%m-%d")
                time_str = dt.strftime("%H:%M:%S")
                ############################################
                    
                print()
                print("=" * 64)
                print(f"{'Supermarket POS Receipt':^60}")
                print("=" * 64)
                print(f"{'Receipt ID:'} {receipt_id:>12}")
                print(f"{'Date      :'} {date_str:>12}")
                print(f"{'Time      :'} {time_str:>12}")
                print("-" * 64)
                print(f"{'Item':<31} {'Qty':>7} {'Price':>11} {'Sub Total':>11}")
                print("-" * 64)
                #print(f"Date Time: {transaction['date_time']}")
                total = 0
                item_count = 0
                for item in transaction_btree['items']:
                    #subtotal = int(item['qty']) * float(item['Unit_Price'])
                    item_count += 1
                    print(f"{item['Item_Desc']:<31} {item['qty']:>7} {item['Unit_Price']:>11.2f} {item['SubTotal']:>11.2f}")
                    total += item['SubTotal']
                print("-" * 64)
                print(f"{'Grand Total (RM)        : ':>30} {total:>32.2f}")
                print(f"{'Total Purchased Item(s) : ':>30} {int(item_count):>32}")
                print("=" * 64)
                print(f"{'Thank you for shopping with us':>45}")
                print("=" * 64)               

                #print("=" * 64)
                #print(f"{'B-Tree Search Timing (Mirco Seconds)':^60}")
                #print(f"Search Time Ended           : {(end_time)/1000:.5f} μs")
                #print(f"Search Time Started         : {(start_time)/1000:.5f} μs")
                #print(f"Search Time Differences     : {search_time:16.5f} μs")
                #print(f"Search Receipt              : {1:21}")
                #print("=" * 64)
            else:
                print("Receipt not found.")
        except ValueError:
            print("Invalid Receipt ID.")

    elif choice == '3':
        
        receipt_id = str(input("Enter Receipt ID: "))
        frequency_num = input("Please Enter The Search Frequency: ")

        #validate the frequency is a valid number or not
        try:
            num = int(frequency_num)
            num_attempt_btree = 0
            num_attempt_bst = 0
            transaction_btree = btree.search_key(receipt_id)
            transaction_bst = bst.search_key(receipt_id)
            #Validate the receipt id availability before start the frequency test
            try:
                if transaction_btree:
                    ##### this is for b-tree search timing clocking #####
                    start_time_btree = time.perf_counter_ns()
                    while num_attempt_btree < num:
                        num_attempt_btree += 1
                        transaction_btree = btree.search_key(receipt_id)

                    end_time_btree = time.perf_counter_ns()                   
                    search_time_btree = (end_time_btree - start_time_btree)/1000   

                    ##### this is for bst search timing clocking #####
                    start_time_bst = time.perf_counter_ns()
                    while num_attempt_bst < num:
                        num_attempt_bst += 1
                        transaction_bst = bst.search_key(receipt_id)
            
                    end_time_bst = time.perf_counter_ns()                   
                    search_time_bst = (end_time_bst - start_time_bst)/1000   
                    
                    ################################################################
                    #####                   Printing the result                #####
                    ################################################################
                    print("\n\n")
                    print("=" * 64)
                    print(f"{'Comparing Search Timing for B-Tree vs BST (Mirco Seconds)':<4}")
                    print(f"Receipt ID                  : {receipt_id:>21}")
                    print(f"Recurring Search Frequency  : {frequency_num:>21}")

                    print("-" * 64)
                    print(f"B-Tree Search Timing (Mirco Seconds)")
                    print("-" * 64)
                    print(f"Search Time Ended           : {(end_time_btree)/1000:.5f} μs")
                    print(f"Search Time Started         : {(start_time_btree)/1000:.5f} μs")
                    print(f"Search Time Differences     : {search_time_btree:18.5f} μs")
                    print("-" * 64)
                    print(f"Binary Search Tree (BST) Search Timing (Mirco Seconds)")
                    print("-" * 64)
                    print(f"Search Time Ended           : {(end_time_bst)/1000:.5f} μs")
                    print(f"Search Time Started         : {(start_time_bst)/1000:.5f} μs")
                    print(f"Search Time Differences     : {search_time_bst:18.5f} μs")
                    print("-" * 64)
                    print(f"Time Diff (BTree - BST)     : {(search_time_btree - search_time_bst):18.5f} μs")
                    print("=" * 64)
                    ################################################################

                    
                else:
                    print("Receipt id not found in the system. Can't proceed with the frequency test.")
            except ValueError:
                print("Invalid Receipt ID. Can't proceed with the frequency test.")          
        
        except ValueError:
            print("Invalid input! Not an integer.")

    elif choice == '4':

        ##### Capture the frequency of testing #####
        frequency_num_all = input("Please Enter The Search Frequency: ")
        try: 
            num_all = int(frequency_num_all)
            bst_times = []
            btree_times = []
            transaction_ids_sorted = []
            
            ##### Extract all the receipt id #####
            cursor.execute("SELECT Transaction_Id FROM Sample_Transaction GROUP BY Transaction_Id")
            rows = cursor.fetchall()
            count_all_receipt_id = 0
            #width = 0.35
            
            for row in rows:
                value = row.Transaction_Id
                bst.insert(row.Transaction_Id, value)
                btree.insert(row.Transaction_Id, value)

            ##### Outer loop for receipt id #####
            for receipt_all_id in rows:
                #receipt_all_id = str(row.Transaction_Id)
                transaction_ids_sorted.append(str(row.Transaction_Id))
                count_all_receipt_id += 1

                ##### Clocking the search for B-tree ##### 
                btree_start = time.perf_counter()
                for _ in range(num_all):
                    btree.search_key(receipt_all_id.Transaction_Id)
                btree_end = time.perf_counter()   
                btree_times.append((btree_end - btree_start) / 1000)
                #print("Btree Receipt ID: ", receipt_all_id)

                ##### Clocking the search for BST ##### 
                bst_start = time.perf_counter()
                for _ in range(num_all):
                    bst.search_key(receipt_all_id.Transaction_Id)
                bst_end = time.perf_counter()   
                bst_times.append((bst_end - bst_start) / 1000)
                #print("\n")
            # Plot bar chart (histogram-like) for comparison between B-Tree and BST #
            x = np.arange(len(transaction_ids_sorted))
            width = 0.35
            
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.bar(x - width/2, bst_times, width, label='BST', color='skyblue')
            ax.bar(x + width/2, btree_times, width, label='B-Tree', color='lightcoral')
            
            ax.set_xlabel('Receipt ID')
            ax.set_ylabel('Average Search Time (Mirco Seconds)')
            ax.set_title(f"BST vs B-Tree: Search Performance With Frequency {num_all} Per ID")
            ax.set_xticks(x)
            ax.set_xticklabels([str(tid) for tid in transaction_ids_sorted], rotation=45, ha='right')
            ax.legend()
            
            plt.tight_layout()
            plt.show()
       
        except ValueError:
            print("Invalid input! Not an integer.")
    
    elif choice == '0':
        print("Thank you for using the system. See you again.")
        break

    else:
        print("Invalid choice.")

# Close connection
conn.close()