"""Binary tree skeleton for loyalty module."""
from typing import Optional, TypeVar
from ..common.interfaces import Node, TreeInterface

T = TypeVar("T")


class BinaryTree(TreeInterface[T]):
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
