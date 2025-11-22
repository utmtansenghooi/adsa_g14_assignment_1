"""Binary tree skeleton for loyalty module."""
from typing import Optional, TypeVar
from src.pos_system.common.interfaces import Node, TreeInterface
from src.pos_system.common.logger import log_operation
T = TypeVar("T")

class BSTNode:
    def __init__(self, customer):
        self.customer = customer
        self.left = None
        self.right = None

class BSTTree(TreeInterface[T]):
    def __init__(self):
        self.root = None

    def insert(self, customer):
        inserted = False
        def _insert(node, customer):
            nonlocal inserted
            if not node:
                inserted = True
                log_operation(f"Inserted: {customer}")
                return BSTNode(customer)
            if customer.customer_id < node.customer.customer_id:
                node.left = _insert(node.left, customer)
            elif customer.customer_id > node.customer.customer_id:
                node.right = _insert(node.right, customer)
            else:
                log_operation(f"Customer {customer.customer_id} already exists.")
            return node
        self.root = _insert(self.root, customer)
        return inserted

    def search(self, customer_id):
        node = self.root
        while node:
            if customer_id < node.customer.customer_id:
                node = node.left
            elif customer_id > node.customer.customer_id:
                node = node.right
            else:
                log_operation(f"Found customer: {node.customer}")
                return node.customer
        log_operation(f"Customer {customer_id} not found")
        return None
    
    def inorder_traversal(self, node=None, result=None):
        if result is None:
            result = []
        if node is None:
            node = self.root
        if node.left:
            self.inorder_traversal(node.left, result)
        result.append(node.customer)
        if node.right:
            self.inorder_traversal(node.right, result)
        return result
    
    def traverse(self):
        """Implements the abstract traverse method (in-order by default)."""
        return self.inorder_traversal()
    
    def delete(self, customer_id):
        def _delete(node, customer_id):
            if not node:
                return None
            if customer_id < node.customer.customer_id:
                node.left = _delete(node.left, customer_id)
            elif customer_id > node.customer.customer_id:
                node.right = _delete(node.right, customer_id)
            else:
                log_operation(f"Deleted: {node.customer}")
                if not node.left:
                    return node.right
                if not node.right:
                    return node.left
                # Node with two children: get inorder successor
                succ = node.right
                while succ.left:
                    succ = succ.left
                node.customer = succ.customer
                node.right = _delete(node.right, succ.customer.customer_id)
            return node
        self.root = _delete(self.root, customer_id)

