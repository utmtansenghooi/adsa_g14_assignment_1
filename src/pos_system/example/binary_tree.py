"""Working Binary Search Tree implementation for the inventory module.

Provides insert, delete, search and in-order traversal. This is a
straightforward BST implementation intended for teaching and tests.
"""
from typing import Optional, TypeVar, Generator

from ..common.interfaces import Node, TreeInterface

T = TypeVar("T")


class BinaryTree(TreeInterface[T]):
    """Simple binary search tree with typical operations."""

    def __init__(self) -> None:
        self.root: Optional[Node[T]] = None

    def insert(self, key: T, value: Optional[object] = None) -> None:
        def _insert(node: Optional[Node[T]], key: T, value: Optional[object]) -> Node[T]:
            if node is None:
                return Node(key=key, value=value)
            if key < node.key:
                node.left = _insert(node.left, key, value)
            elif key > node.key:
                node.right = _insert(node.right, key, value)
            else:
                # update existing
                node.value = value
            return node

        self.root = _insert(self.root, key, value)

    def search(self, key: T) -> Optional[Node[T]]:
        node = self.root
        while node:
            if key == node.key:
                return node
            node = node.left if key < node.key else node.right
        return None

    def delete(self, key: T) -> None:
        def _min_node(n: Node[T]) -> Node[T]:
            while n.left:
                n = n.left
            return n

        def _delete(node: Optional[Node[T]], key: T) -> Optional[Node[T]]:
            if node is None:
                return None
            if key < node.key:
                node.left = _delete(node.left, key)
            elif key > node.key:
                node.right = _delete(node.right, key)
            else:
                # Node to delete found
                if node.left is None:
                    return node.right
                if node.right is None:
                    return node.left
                # node with two children: replace with inorder successor
                succ = _min_node(node.right)
                node.key, node.value = succ.key, succ.value
                node.right = _delete(node.right, succ.key)
            return node

        self.root = _delete(self.root, key)

    def traverse(self) -> Generator[Node[T], None, None]:
        def _inorder(n: Optional[Node[T]]):
            if n is None:
                return
            yield from _inorder(n.left)
            yield n
            yield from _inorder(n.right)

        yield from _inorder(self.root)
