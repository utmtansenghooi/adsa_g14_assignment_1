"""AVL Tree skeleton for loyalty module."""
from typing import Optional, TypeVar
from ..common.interfaces import Node, TreeInterface
from ..common.logger import log_operation

T = TypeVar("T")

class AVLNode:
    def __init__(self, customer):
        self.customer = customer
        self.left = None
        self.right = None
        self.height = 1

class AVLTree(TreeInterface[T]):
    def __init__(self):
        self.root = None

    def insert(self, customer):
        inserted = False
        def _insert(node, customer):
            nonlocal inserted
            if not node:
                inserted = True
                log_operation(f"Inserted: {customer}")
                return AVLNode(customer)

            if customer.customer_id < node.customer.customer_id:
                node.left = _insert(node.left, customer)
            elif customer.customer_id > node.customer.customer_id:
                node.right = _insert(node.right, customer)
            else:
                log_operation(f"Customer {customer.customer_id} already exists.")
                return node

            # Update height
            node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

            # Balance factor
            balance = self.get_balance(node)

            # Left heavy
            if balance > 1 and customer.customer_id < node.left.customer.customer_id:
                return self.right_rotate(node)
            if balance < -1 and customer.customer_id > node.right.customer.customer_id:
                return self.left_rotate(node)
            if balance > 1 and customer.customer_id > node.left.customer.customer_id:
                node.left = self.left_rotate(node.left)
                return self.right_rotate(node)
            if balance < -1 and customer.customer_id < node.right.customer.customer_id:
                node.right = self.right_rotate(node.right)
                return self.left_rotate(node)
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

    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y
    
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
                succ = node.right
                while succ.left:
                    succ = succ.left
                node.customer = succ.customer
                node.right = _delete(node.right, succ.customer.customer_id)

            # Update height and balance
            node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
            balance = self.get_balance(node)
            if balance > 1 and self.get_balance(node.left) >= 0:
                return self.right_rotate(node)
            if balance < -1 and self.get_balance(node.right) <= 0:
                return self.left_rotate(node)
            if balance > 1 and self.get_balance(node.left) < 0:
                node.left = self.left_rotate(node.left)
                return self.right_rotate(node)
            if balance < -1 and self.get_balance(node.right) > 0:
                node.right = self.right_rotate(node.right)
                return self.left_rotate(node)
            return node
        self.root = _delete(self.root, customer_id)