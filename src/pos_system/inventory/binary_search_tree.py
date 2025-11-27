"""
Tan Seng Hooi's Binary Search Tree implementation for the inventory module.
"""
from dataclasses import dataclass
from typing import Generic, Optional, TypeVar, Generator
from src.pos_system.common.interfaces import TreeInterface
from src.pos_system.common.Product import Product

T = TypeVar("T")

@dataclass
class BinarySearchNode(Generic[T]):
    """Binary Search Tree Node for Product class"""

    def __init__(self, key: T, value: Optional[Product] = None):
        self.key = key # Key of the node, could be Product ID or name
        self.value = value # The Product object (contains other data)
        self.left = None
        self.right = None
    
    def __repr__(self): # Helpful representation for debugging
        left = self.left.key if self.left else None
        right = self.right.key if self.right else None
        return f"BinarySearchNode(key={self.key}, value={str(self.value)}, left={left}, right={right})"

class BinarySearchTree(TreeInterface[T]):
    """Binary Search Tree for Product nodes"""
    
    def __init__(self):
        self.root: Optional[BinarySearchNode[T]] = None

    def insert(self, key: T, value: Optional[BinarySearchNode[T]] = None) -> None:
        # Helper insertion function for recursion
        def _insert(node: Optional[BinarySearchNode[T]], key: T, value: Optional[BinarySearchNode[T]]) -> BinarySearchNode[T]:
            if node is None:    # Base case: Found empty slot to insert
                return BinarySearchNode(key, value)
            if key < node.key:  # Left subtree
                node.left = _insert(node.left, key, value)
            elif key > node.key:    # Right subtree
                node.right = _insert(node.right, key, value)
            else:   # Key already exists, update value
                node.value = value
            return node
        
        self.root = _insert(self.root, key, value) # Start from root of tree

    def search(self, key: T) -> Optional[BinarySearchNode[T]]:
        node = self.root    # Start from root
        while node: # Traverse until leaf node is None
            if key == node.key: # Found node, check current node first
                return node
            node = node.left if key < node.key else node.right # Traverse left or right
        return None
    
    def delete(self, key: T) -> None:
        # Helper deletion function for recursion
        def _delete(node: Optional[BinarySearchNode[T]], key: T) -> Optional[BinarySearchNode[T]]:
            if node is None:
                return None
            if key < node.key:
                node.left = _delete(node.left, key)
            elif key > node.key:
                node.right = _delete(node.right, key)
            else:
                # Node with 1 child or no child
                if node.left is None:
                    return node.right
                if node.right is None:
                    return node.left
                # Node with two children: Get inorder successor (smallest in right subtree)
                current = node.right
                while current and current.left: # Find smallest key in right subtree
                    current = current.left
                successor = current
                # Copy successor's content to this node
                node.key = successor.key
                node.value = successor.value
                # Delete the inorder successor
                node.right = _delete(node.right, successor.key)
            return node
        self.root = _delete(self.root, key)

    def traverse(self) -> Generator[BinarySearchNode[T], None, None]:
        """Inorder Traversal (Good for printing sorted order)"""
        def _inorder_traversal(node: Optional[BinarySearchNode[T]]) -> Generator[BinarySearchNode[T], None, None]:
            if node:
                yield from _inorder_traversal(node.left) # Go down left subtree
                yield node # Current node (root if first invocation)
                yield from _inorder_traversal(node.right) # Go down right subtree
        yield from _inorder_traversal(self.root)
