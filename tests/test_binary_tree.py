from src.pos_system.example.binary_tree import BinaryTree


def test_binary_tree_basic_operations():
    t = BinaryTree[int]()
    t.insert(10)
    t.insert(5)
    t.insert(15)
    t.insert(12)
    t.insert(3)

    # search
    assert t.search(10) is not None and t.search(10).key == 10
    assert t.search(99) is None

    # traversal yields sorted keys
    keys = [n.key for n in t.traverse()]
    assert keys == [3, 5, 10, 12, 15]

    # delete leaf
    t.delete(3)
    keys = [n.key for n in t.traverse()]
    assert keys == [5, 10, 12, 15]

    # delete node with one child
    t.delete(12)
    keys = [n.key for n in t.traverse()]
    assert keys == [5, 10, 15]

    # delete root
    t.delete(10)
    keys = [n.key for n in t.traverse()]
    assert keys == [5, 15]
