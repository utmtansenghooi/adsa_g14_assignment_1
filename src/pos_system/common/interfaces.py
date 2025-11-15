from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, Iterable, Optional, TypeVar

T = TypeVar("T")


@dataclass
class Node(Generic[T]):
    key: T
    value: Optional[object] = None
    left: Optional["Node[T]"] = None
    right: Optional["Node[T]"] = None


class TreeInterface(ABC, Generic[T]):
    """A minimal interface that tree implementations should follow."""

    @abstractmethod
    def insert(self, key: T, value: Optional[object] = None) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, key: T) -> None:
        raise NotImplementedError

    @abstractmethod
    def search(self, key: T) -> Optional[Node[T]]:
        raise NotImplementedError

    @abstractmethod
    def traverse(self) -> Iterable[Node[T]]:
        raise NotImplementedError
