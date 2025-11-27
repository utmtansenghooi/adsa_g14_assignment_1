"""
Tan Seng Hooi's Splay Tree implementation for the inventory module.
"""
from dataclasses import dataclass
from typing import Generic, Optional, TypeVar, Generator
from src.pos_system.common.interfaces import TreeInterface
from src.pos_system.common.Product import Product

T = TypeVar("T")

@dataclass
class SplayNode(Generic[T]):
    """Splay Tree Node for Product class"""
    def __init__(self, key: T, value: Optional[Product] = None):
        self.key = key # Key of the node, could be Product ID or name
        self.value = value # The Product object (contains other data)
        self.left = None
        self.right = None
    
    def __repr__(self): # Helpful representation for debugging
        left = self.left.key if self.left else None
        right = self.right.key if self.right else None
        return f"SplayNode(key={self.key}, value={str(self.value)}, left={left}, right={right})"

class SplayTree(TreeInterface[T]):
    """Splay Tree for Product nodes"""

    def __init__(self):
        self.root: Optional[SplayNode[T]] = None

    def _zig(self, node: SplayNode[T]) -> SplayNode[T]:
        """Rotate right"""
        new_root = node.left
        node.left = new_root.right
        new_root.right = node
        return new_root
    
    def _zag(self, node: SplayNode[T]) -> SplayNode[T]:
        """Rotate left"""
        new_root = node.right
        node.right = new_root.left
        new_root.left = node
        return new_root
    
    def _splay(self, node: Optional[SplayNode[T]], key: T) -> Optional[SplayNode[T]]:
        # Key at root, or tree is empty
        if node is None or node.key == key:
            return node
        
        # Key in left subtree (will zig at least once)
        if key < node.key:
            if node.left is None: # End of path
                return node
            # If key is in left-left subtree (zig-zig)
            if key < node.left.key:
                node.left.left = self._splay(node.left.left, key)
                node = self._zig(node)  # must zig grandparent first
             # If key is in left-right subtree (zag-zig)
            elif key > node.left.key:
                node.left.right = self._splay(node.left.right, key)
                if node.left.right:
                    node.left = self._zag(node.left) # must zag parent first
            return self._zig(node) if node.left else node # zig once (found)
        # Key in right subtree (will zag at least once)
        else:
            if node.right is None: # End of path
                return node
            # If key is in right-right subtree (zag-zag)
            if key > node.right.key: 
                node.right.right = self._splay(node.right.right, key)
                node = self._zag(node) # must zag grandparent first
            # If key is in right-left subtree (zig-zag)
            elif key < node.right.key:
                node.right.left = self._splay(node.right.left, key)
                if node.right.left:
                    node.right = self._zig(node.right) # must zig parent first
            return self._zag(node) if node.right else node # zag once (found)

    def insert(self, key: T, value: Optional[SplayNode[T]] = None) -> None:
        # Helper insertion function for recursion
        def _insert(node: Optional[SplayNode[T]], key: T, value: Optional[SplayNode[T]]) -> SplayNode[T]:
            if node is None:    # Base case: Found empty slot to insert
                return SplayNode(key, value)
            if key < node.key:  # Left subtree
                node.left = _insert(node.left, key, value)
            elif key > node.key:    # Right subtree
                node.right = _insert(node.right, key, value)
            else:   # Key already exists, update value
                node.value = value
            return node
        
        self.root = _insert(self.root, key, value) # Start from root of tree
        self.root = self._splay(self.root, key)  # Splay the inserted node to root

    def search(self, key: T) -> Optional[SplayNode[T]]:
        self.root = self._splay(self.root, key) # Splay the searched node to root
        if self.root and self.root.key == key:
            return self.root
        return None
    
    def delete(self, key: T) -> None:
        if self.root is None:   # Empty tree
            return
        self.root = self._splay(self.root, key) # Splay the searched node to root
        if self.root.key != key:    # Key not found
            return
        if self.root.left is None:  # Key found, but no left subtree
            self.root = self.root.right
        else:   # Key found, has left subtree
            right_subtree = self.root.right
            self.root = self._splay(self.root.left, key) # Splay the largest of left subtree
            self.root.right = right_subtree
        return self.root

    def traverse(self) -> Generator[SplayNode[T], None, None]:
        """Inorder Traversal (Good for printing sorted order)"""
        def _inorder_traversal(node: Optional[SplayNode[T]]) -> Generator[SplayNode[T], None, None]:
            if node:
                yield from _inorder_traversal(node.left) # Go down left subtree
                yield node # Current node (root if first invocation)
                yield from _inorder_traversal(node.right) # Go down right subtree
        yield from _inorder_traversal(self.root)