import pyodbc
import time
import os
import pathlib
from abc import ABC, abstractmethod
from typing import Any, List, Optional, Tuple


# =========================
# ADT: Database Repository
# =========================

class IDatabaseRepository(ABC):
    @abstractmethod
    def fetch_sales_by_receipt(self, receipt_id: str) -> List[dict]:
        pass

    @abstractmethod
    def insert_transactions(self, rows: List[dict]) -> None:
        pass

    @abstractmethod
    def update_stock(self, product_id: str, quantity_delta: int) -> None:
        pass

    @abstractmethod
    def fetch_transaction_by_receipt(self, receipt_id: str) -> List[dict]:
        pass



class AccessDatabaseRepository(IDatabaseRepository):
    def __init__(self, db_path: str):
        self.conn = pyodbc.connect(
            f"Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={db_path};"
        )
        self.conn.autocommit = False

    def _dict_rows(self, cursor) -> List[dict]:
        cols = [c[0] for c in cursor.description]
        return [dict(zip(cols, row)) for row in cursor.fetchall()]

    def fetch_sales_by_receipt(self, receipt_id: str) -> List[dict]:
        sql = """
            SELECT Transaction_Id, Item_Code, Item_Description, qty, Unit_Price, Trans_Date, Total_Item_Amount
            FROM Sample_Sales
            WHERE Transaction_Id = ?
        """
        with self.conn.cursor() as cur:
            cur.execute(sql, (receipt_id,))
            return self._dict_rows(cur)

    def insert_transactions(self, rows: List[dict]) -> None:
        sql = """
            INSERT INTO Sample_Transaction
                (Transaction_Id, Item_Code, Item_Description, qty, Unit_Price, Trans_Date, Total_Item_Amount)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        with self.conn.cursor() as cur:
            for r in rows:
                cur.execute(
                    sql,
                    (
                        r["Transaction_Id"],
                        r["Item_Code"],
                        r["Item_Description"],
                        r["qty"],
                        r["Unit_Price"],
                        r["Trans_Date"],
                        r["Total_Item_Amount"],
                    ),
                )
        self.conn.commit()

    def update_stock(self, product_id: str, quantity_delta: int) -> None:
        sql = "UPDATE Product SET Product_Qty = Product_Qty + ? WHERE Product_code = ?"
        with self.conn.cursor() as cur:
            cur.execute(sql, (quantity_delta, product_id))
        self.conn.commit()

    def fetch_transaction_by_receipt(self, receipt_id: str) -> List[dict]:
        sql = """
            SELECT Transaction_Id, Item_Code, Item_Description, qty, Unit_Price, Trans_Date, Total_Item_Amount
            FROM Sample_Transaction
            WHERE Transaction_Id = ?
            ORDER BY Item_Code
        """
        with self.conn.cursor() as cur:
            cur.execute(sql, (receipt_id,))
            return self._dict_rows(cur)

    def fetch_all_receipt_id(self, receipt_id: str) -> List[dict]:
        sql = "SELECT Transaction_Id, Trans_Date FROM Sample_Transaction group by Transaction_Id, Trans_Date "
        with self.conn.cursor() as cur:
            cur.execute(sql, (receipt_id,))
            return self._dict_rows(cur)


# =========================
# ADT: BST for timing metrics
# =========================

class IBST(ABC):
    @abstractmethod
    def insert_or_update(self, key: Any, insert_time_ms: float, traversal_time_ms: float) -> None:
        pass

    @abstractmethod
    def search_metrics(self, key: Any) -> Optional[dict]:
        pass

    @abstractmethod
    def stats(self) -> List[Tuple[Any, dict]]:
        pass


class BSTNode:
    def __init__(self, key: Any, metrics: dict):
        self.key = key
        self.metrics = metrics
        self.left: Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None


class BST(IBST):
    """
    Binary Search Tree storing per-receipt timing metrics:
    {
        "frequency": n,
        "insert_load_ms": cumulative,
        "traversal_ms": cumulative
    }
    """
    def __init__(self):
        self.root: Optional[BSTNode] = None

    def _update_metrics(self, node: BSTNode, insert_time_ms: float, traversal_time_ms: float):
        node.metrics["frequency"] += 1
        node.metrics["insert_load_ms"] += insert_time_ms
        node.metrics["traversal_ms"] += traversal_time_ms

    def insert_or_update(self, key: Any, insert_time_ms: float, traversal_time_ms: float) -> None:
        start = time.perf_counter()
        if self.root is None:
            self.root = BSTNode(key, {
                "frequency": 1,
                "insert_load_ms": insert_time_ms,
                "traversal_ms": traversal_time_ms
            })
            return

        cur = self.root
        while True:
            # Measure traversal per comparison
            comp_start = time.perf_counter()
            if key == cur.key:
                comp_ms = (time.perf_counter() - comp_start) * 1000.0
                # add measured traversal in addition to provided traversal_time_ms
                self._update_metrics(cur, insert_time_ms, traversal_time_ms + comp_ms)
                return
            elif key < cur.key:
                comp_ms = (time.perf_counter() - comp_start) * 1000.0
                traversal_time_ms += comp_ms
                if cur.left is None:
                    cur.left = BSTNode(key, {
                        "frequency": 1,
                        "insert_load_ms": insert_time_ms,
                        "traversal_ms": traversal_time_ms
                    })
                    return
                cur = cur.left
            else:
                comp_ms = (time.perf_counter() - comp_start) * 1000.0
                traversal_time_ms += comp_ms
                if cur.right is None:
                    cur.right = BSTNode(key, {
                        "frequency": 1,
                        "insert_load_ms": insert_time_ms,
                        "traversal_ms": traversal_time_ms
                    })
                    return
                cur = cur.right

    def search_metrics(self, key: Any) -> Optional[dict]:
        cur = self.root
        traversal_acc_ms = 0.0
        while cur is not None:
            step_start = time.perf_counter()
            if key == cur.key:
                step_ms = (time.perf_counter() - step_start) * 1000.0
                # Update traversal and frequency even for searches
                cur.metrics["frequency"] += 1
                cur.metrics["traversal_ms"] += traversal_acc_ms + step_ms
                return cur.metrics
            elif key < cur.key:
                step_ms = (time.perf_counter() - step_start) * 1000.0
                traversal_acc_ms += step_ms
                cur = cur.left
            else:
                step_ms = (time.perf_counter() - step_start) * 1000.0
                traversal_acc_ms += step_ms
                cur = cur.right
        return None

    def stats(self) -> List[Tuple[Any, dict]]:
        out: List[Tuple[Any, dict]] = []

        def inorder(n: Optional[BSTNode]):
            if n is None:
                return
            inorder(n.left)
            out.append((n.key, n.metrics))
            inorder(n.right)

        inorder(self.root)
        return out


# =========================
# ADT: Transaction Manager
# =========================

class ITransactionManager(ABC):
    @abstractmethod
    def insert_sales_transaction(self, receipt_id: str) -> bool:
        pass

    @abstractmethod
    def search_receipt(self, receipt_id: str) -> List[dict]:
        pass

    @abstractmethod
    def print_receipt(self, receipt_id: str) -> None:
        pass


class TransactionManager(ITransactionManager):
    def __init__(self, repo: IDatabaseRepository, metric_tree: IBST):
        self.repo = repo
        self.tree = metric_tree

    def insert_sales_transaction(self, receipt_id: str) -> bool:
        # Measure total insert load: read Sample_Sales, write Sample_Transaction, update Product
        t0 = time.perf_counter()
        sales_rows = self.repo.fetch_sales_by_receipt(receipt_id)
        if not sales_rows:
            t1 = time.perf_counter()
            self.tree.insert_or_update(receipt_id, insert_time_ms=(t1 - t0) * 1000.0, traversal_time_ms=0.0)
            return False

        tx_rows = []
        for r in sales_rows:
            #qty = int(r["Quantity"])
            #unit = float(r["UnitPrice"])
            #line_total = qty * unit
             tx_rows.append({
                "Transaction_Id": str(r["Transaction_Id"]),
                "Item_Code": str(r["Item_Code"]),
                "Item_Description": str(r["Item_Description"]),
                "qty": int(r["qty"]),
                "Unit_Price": float(r["Unit_Price"]),
                "Total_Item_Amount": float(r["Total_Item_Amount"]),
                "Trans_Date": r["Trans_Date"]  # reusing sales timestamp; could use now
            })

        # Insert transactions
        self.repo.insert_transactions(tx_rows)

        # Update stock (reduce)
        for r in tx_rows:
            self.repo.update_stock(r["Item_Code"], quantity_delta=-r["qty"])

        t1 = time.perf_counter()
        insert_ms = (t1 - t0) * 1000.0

        # Measure BST traversal during a metrics search/update (optional probe)
        trav_start = time.perf_counter()
        _ = self.tree.search_metrics(receipt_id)  # updates traversal on hit
        trav_ms = (time.perf_counter() - trav_start) * 1000.0

        # Record metrics
        self.tree.insert_or_update(receipt_id, insert_time_ms=insert_ms, traversal_time_ms=trav_ms)
        return True

    def search_receipt(self, receipt_id: str) -> List[dict]:
        t0 = time.perf_counter()
        rows = self.repo.fetch_transaction_by_receipt(receipt_id)
        t1 = time.perf_counter()
        trav_ms = (t1 - t0) * 1000.0
        # Record only traversal time for search (insert time = 0)
        self.tree.insert_or_update(receipt_id, insert_time_ms=0.0, traversal_time_ms=trav_ms)
        return rows

    def print_receipt(self, receipt_id: str) -> None:
        rows = self.search_receipt(receipt_id)
        if not rows:
            print(f"[Receipt {receipt_id}] not found.")
            return

        # Header
        #print("EE", rows[0]['Trans_Date'])
        dt = rows[0]['Trans_Date']
        date_str = dt.strftime("%Y-%m-%d")
        time_str = dt.strftime("%H:%M:%S")
        #total = sum(float(rows["Total_Item_Amount"]) for r in rows)
        item_count = 0
        total = 0
        
        print("=" * 64)
        print(f"{'Supermarket Receipt':^64}")
        print("=" * 64)
        print(f"{'Receipt ID:'} {receipt_id:>12}")
        print(f"{'Date      :'} {date_str:>12}")
        print(f"{'Time      :'} {time_str:>12}")
        print("-" * 64)
        print(f"{'Item':<31} {'Qty':>7} {'Price':>11} {'Sub Total':>11}")
        print("-" * 64)

        ## Lines
        for item in rows:
            #subtotal = int(item['qty']) * float(item['Unit_Price'])
            item_count += 1
            print(f"{item['Item_Description']:<31} {item['qty']:>7} {item['Unit_Price']:>11.2f} {item['Total_Item_Amount']:>11.2f}")
            total += item['Total_Item_Amount']
        print("-" * 64)
        print(f"{'Grand Total (RM)        : ':>30} {total:>32.2f}")
        print(f"{'Total Purchased Item(s) : ':>30} {int(item_count):>32}")
        print("=" * 64)
        print(f"{'Thank you for shopping with us':>45}")
        print("=" * 64)           
        
        # Header
        # Use the first row's PostedAt as the receipt timestamp (if present)
        #dt = rows[0].get("PostedAt")
        #print("\n==== Sales Receipt ====")
        #print(f"Receipt ID: {receipt_id}")
        #if dt:
        #    try:
        #        date_str = dt.strftime("%Y-%m-%d")
        #        time_str = dt.strftime("%H:%M:%S")
        #        print(f"Date: {date_str}  Time: {time_str}")
        #    except Exception:
        #        print(f"DateTime: {dt}")
        #print("-----------------------")

        ## Lines
        #for r in rows:
        #    print(f"ProductID: {r['ProductID']}  Qty: {r['Quantity']}  Unit: {float(r['UnitPrice']):.2f}  Line: {float(r['LineTotal']):.2f}")

        ## Total
        #total = sum(float(r["LineTotal"]) for r in rows)
        #print("-----------------------")
        #print(f"TOTAL: {total:.2f}")
        #print("=======================\n")


# =========================
# Console menu / Main
# =========================

def show_metrics(tree: IBST):
    print("===========================================")
    print("=== BST timing metrics (per receipt) ===")
    print("===========================================\n")
    for key, m in tree.stats():
        ## Also show averages if frequency > 0
        freq = max(1, m['frequency'])
        avg_insert = m['insert_load_ms'] / freq
        avg_traversal = m['traversal_ms'] / freq
        print(
            f"Receipt          : {key:>9} \n"
            f"Search Frequency :{m['frequency']:>10} \n"
            f"insert_load_ms   :{m['insert_load_ms']:5.5f} (avg {avg_insert:5.5f})\n"
            f"traversal_ms     :{m['traversal_ms']:5.5f}   (avg {avg_traversal:5.5f})")
    print("===========================================\n")
    
    #print("\n=== BST timing metrics (per receipt) ===")
    #for key, m in tree.stats():
    ## Also show averages if frequency > 0
        #freq = max(1, m["frequency"])
        #avg_insert = m["insert_load_ms"] / freq
        #avg_traversal = m["traversal_ms"] / freq
        #print(
        #    f"Receipt {key}: freq={m['frequency']}, "
        #    f"insert_load_ms={m['insert_load_ms']:.3f} (avg {avg_insert:.3f}), "
        #    f"traversal_ms={m['traversal_ms']:.3f} (avg {avg_traversal:.3f})"
        #)
    #print("========================================\n")


def main():
    db_path = os.path.join(pathlib.Path(__file__).resolve().parent, "UTM_BST_data.accdb")
    repo = AccessDatabaseRepository(db_path)
    metrics_tree = BST()
    manager = TransactionManager(repo, metrics_tree)

    actions = {
        "1": "Insert sales transaction",
        "2": "Search receipt",
        "3": "Print receipt",
        #"4": "Show timing metrics",
        "0": "Exit"
    }

    while True:
        print("\n--- Supermarket POS: Sales & Receipt Module ---")
        for k, v in actions.items():
            print(f"{k}. {v}")
        choice = input("Select action: ").strip()

        if choice == "0":
            print("Thank you. See you again.")
            break

        elif choice == "1":
            rid = input("Enter Receipt ID to post: ").strip()
            ok = manager.insert_sales_transaction(rid)
            if ok:
                print(f"Posted receipt {rid} into Sample_Transaction and updated stock.")
            else:
                print(f"No sales found for receipt {rid}. Nothing posted.")
            ##show_metrics(metrics_tree)

        elif choice == "2":
            rid = input("Enter Receipt ID to search: ").strip()
            rows = manager.search_receipt(rid)
            if rows:
                print(f"Found {len(rows)} transaction rows for receipt {rid}.")
            else:
                print("Receipt not found.")
            ##show_metrics(metrics_tree)
            manager.print_receipt(rid)

        elif choice == "3":
            rid = input("Enter Receipt ID to print: ").strip()
            
            ##show_metrics(metrics_tree)
            manager.print_receipt(rid)

        #elif choice == "4":
            ##show_metrics(metrics_tree)

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
