"""
Tan Seng Hooi's Improved Splay Tree implementation for the inventory module.
"""
from dataclasses import dataclass
from typing import Generic, Optional, TypeVar, Generator
from src.pos_system.common.interfaces import TreeInterface
from src.pos_system.common.Product import Product

T = TypeVar("T")

@dataclass
class ImprovedSplayNode(Generic[T]):
    """Splay Tree Node for Product class"""
    def __init__(self, key: T, value: Optional[Product] = None):
        self.key = key # Key of the node, could be Product ID or name
        self.value = value # The Product object (contains other data)
        self.left = None
        self.right = None
    
    def __repr__(self): # Helpful representation for debugging
        left = self.left.key if self.left else None
        right = self.right.key if self.right else None
        return f"ImprovedSplayNode(key={self.key}, value={str(self.value)}, left={left}, right={right})"

class ImprovedSplayTree(TreeInterface[T]):
    """Splay Tree for Product nodes"""

    def __init__(self):
        self.root: Optional[ImprovedSplayNode[T]] = None

    def _splay(self, node: Optional[ImprovedSplayNode[T]], key: T) -> Optional[ImprovedSplayNode[T]]:
        """
        Top-Down Splay operation. 
        It moves the node with 'key' to the root. If 'key' is not found, 
        it moves the last accessed node (the split point) to the root.
        
        It partitions the tree into three parts: L (less than key), R (greater than key), and the middle.
        """
        if node is None:
            return None

        # Create dummy nodes for L and R trees
        header = ImprovedSplayNode(key=None) # Sentinel node
        left_max = header
        right_min = header

        while True:
            if key < node.key:
                if node.left is None:
                    break
                
                # --- Zig-Zig Case (Node and child are both left) ---
                if key < node.left.key:
                    # Right rotation on node
                    new_node = node.left
                    node.left = new_node.right
                    new_node.right = node
                    node = new_node
                    if node.left is None: # New node has no left child, we stop here
                        break
                
                # Link to R (right) tree
                right_min.left = node
                right_min = node
                node = node.left
                right_min.left = None # Disconnect old pointer

            elif key > node.key:
                if node.right is None:
                    break
                
                # --- Zag-Zag Case (Node and child are both right) ---
                if key > node.right.key:
                    # Left rotation on node
                    new_node = node.right
                    node.right = new_node.left
                    new_node.left = node
                    node = new_node
                    if node.right is None: # New node has no right child, we stop here
                        break

                # Link to L (left) tree
                left_max.right = node
                left_max = node
                node = node.right
                left_max.right = None # Disconnect old pointer
            
            else: # Key found (key == node.key)
                break
        
        # Re-join L, M (middle), and R trees
        # 1. Attach L tree (rooted at header.left) to node.left
        left_max.right = node.left
        node.left = header.right

        # 2. Attach R tree (rooted at header.right) to node.right
        right_min.left = node.right
        node.right = header.left
        
        return node
    
    def insert(self, key: T, value: Optional[Product] = None) -> None:
        """
        Inserts a key-value pair. The new node becomes the root.
        This uses the split/join method after splaying.
        """
        if self.root is None:
            self.root = ImprovedSplayNode(key, value)
            return

        # 1. Splay the tree with the new key. The new root will be the split point.
        self.root = self._splay(self.root, key)
        
        # If the key already exists, update the value and return.
        if key == self.root.key:
            self.root.value = value
            return

        new_node = ImprovedSplayNode(key, value)
        
        # 2. Split and Join
        if key < self.root.key:
            # The new node takes the original root's left subtree
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else: # key > self.root.key
            # The new node takes the original root's right subtree
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None
            
        self.root = new_node # New node is the root

    def search(self, key: T) -> Optional[ImprovedSplayNode[T]]:
        self.root = self._splay(self.root, key)
        if self.root and self.root.key == key:
            return self.root
        return None
    
    def delete(self, key: T) -> None:
        """
        Deletes a key using the two-splay method.
        1. Splay the node to be deleted (x) to the root.
        2. Remove x, leaving its left (A) and right (B) subtrees.
        3. Splay the maximum element in A to the root of A.
        4. Join: Set A's new root's right child to B.
        """
        if self.root is None:
            return
            
        # 1. Splay the key to the root
        self.root = self._splay(self.root, key)
        
        # If key is not found, splay operation ends at the split point, return
        if self.root.key != key:
            return
            
        # Key is found, the root is the node to delete
        # Separate the left (A) and right (B) subtrees
        left_subtree = self.root.left
        right_subtree = self.root.right
        
        # Delete the root node
        self.root = None
        
        if left_subtree is None:
            # Left subtree is empty, right subtree (B) is the new tree
            self.root = right_subtree
            return
        
        # 3. Splay the maximum element of the left subtree (A) to its root
        # We splay on a key that is guaranteed to be greater than all keys in A
        # This will bring the rightmost node of A to the root of A.
        # We use the key from the old root's right child (right_subtree.key) as the splay key
        # since it's guaranteed to be greater than all keys in A.
        
        # NOTE: Splaying with a key larger than max(A) will bring max(A) to the root
        # I will use a placeholder key, 'None', to signify splaying to Max
        
        # We use a dedicated helper to find and splay the max of the left_subtree
        def _splay_max(node: ImprovedSplayNode[T]) -> ImprovedSplayNode[T]:
            """Splays the node with the maximum key to the root of the given subtree."""
            if node.right is None:
                return node
            while node.right.right is not None:
                node = node.right
            # Final rotation to bring max to root
            new_root = node.right
            node.right = new_root.left
            new_root.left = node
            return new_root
            
        self.root = _splay_max(left_subtree)
        
        # 4. Join: The new root (the max of A) has no right child, attach B
        self.root.right = right_subtree

    def traverse(self) -> Generator[ImprovedSplayNode[T], None, None]:
        """Inorder Traversal (Good for printing sorted order)"""
        def _inorder_traversal(node: Optional[ImprovedSplayNode[T]]) -> Generator[ImprovedSplayNode[T], None, None]:
            if node:
                yield from _inorder_traversal(node.left) # Go down left subtree
                yield node # Current node (root if first invocation)
                yield from _inorder_traversal(node.right) # Go down right subtree
        yield from _inorder_traversal(self.root)