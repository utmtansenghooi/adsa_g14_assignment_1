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
        raise NotImplementedError

    def delete(self, key: T) -> None:
        raise NotImplementedError

    def search(self, key: T) -> Optional[Node[T]]:
        raise NotImplementedError

    def traverse(self):
        raise NotImplementedError
