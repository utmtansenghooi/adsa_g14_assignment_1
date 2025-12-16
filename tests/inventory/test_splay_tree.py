from src.pos_system.inventory.splay_tree import SplayTree, SplayNode
from src.pos_system.inventory.inventory_data_loader import build_inventory_splay_tree, InventoryKeyType
from src.pos_system.common.Product import Product

def test_splay_tree_traversal_empty_tree():
    t = SplayTree[int]()
    keys = [n.key for n in t.traverse()]
    assert keys == []

def test_splay_tree_traversal():
    t = SplayTree[int]()
    for key in [7, 3, 9, 1, 5, 8, 10]:
        t.insert(key)
    keys = [n.key for n in t.traverse()]
    assert keys == [1, 3, 5, 7, 8, 9, 10]

def test_splay_tree_basic_operations():
    def _genSplay() -> SplayTree[int]:
        t = SplayTree[int]()    #        15
        t.insert(5)             #       /
        t.insert(3)             #      10
        t.insert(10)            #     /
        t.insert(4)             #    4   
        t.insert(15)            #   / \
        return t                #  3   5

    # search existing
    t = _genSplay()
    val = t.search(10)
    assert val is not None and val.key == 10
    assert t.root.key == 10  # After search, 10 should be at root

    # search non-existing
    t = _genSplay()
    assert t.search(99) is None
    assert t.root.key == 15  # After failed search, last accessed node (15) should be at root

    # traversal yields sorted keys
    keys = [n.key for n in t.traverse()]
    assert keys == [3, 4, 5, 10, 15]

    # delete leaf
    t = _genSplay()
    t.delete(5)
    keys = [n.key for n in t.traverse()]
    assert keys == [3, 4, 10, 15]
    assert t.root.key == 4  # After deletion, last accessed node (4) should be at root

    # delete node with one child
    t = _genSplay()
    t.delete(10)
    keys = [n.key for n in t.traverse()]
    assert keys == [3, 4, 5, 15]
    assert t.root.key == 5  # After deletion, last accessed node (5) should be at root

    # delete node with two child
    t = _genSplay()
    t.delete(4)
    keys = [n.key for n in t.traverse()]
    assert keys == [3, 5, 10, 15]
    assert t.root.key == 3  # After deletion, last accessed node (3) should be at root

    # delete root
    t = _genSplay()
    t.delete(15)
    keys = [n.key for n in t.traverse()]
    assert keys == [3, 4, 5, 10]
    assert t.root.key == 10  # After deletion, last accessed node (10) should be at root

def test_splay_tree_product_insertion_product_id():
    t = SplayTree[SplayNode]()
    products = [
        Product(product_id=1, name="Apple", price=0.5, category="Fruit", quantity=100),
        Product(product_id=2, name="Banana", price=0.3, category="Fruit", quantity=150),
        Product(product_id=3, name="Cherry", price=0.2, category="Fruit", quantity=200),
        Product(product_id=4, name="Date", price=0.4, category="Fruit", quantity=120),
        Product(product_id=5, name="Elderberry", price=0.6, category="Fruit", quantity=80),
        Product(product_id=6, name="Fig", price=0.7, category="Fruit", quantity=90),
        Product(product_id=7, name="Grape", price=0.8, category="Fruit", quantity=110),
        Product(product_id=8, name="Honeydew", price=0.9, category="Fruit", quantity=70),
        Product(product_id=9, name="Indian Fig", price=1.0, category="Fruit", quantity=60),
    ]

    nodes = [SplayNode(key=p.product_id, value=p) for p in products]
    for node in nodes:
        t.insert(node.key, node.value)
    
    # search
    node = t.search(2)
    assert node is not None and node.value == nodes[1].value
    node = t.search(9)
    assert node is not None and node.value == nodes[8].value
    node = t.search(10)
    assert node is None

    # traversal yields sorted product ids
    ids = [n.key for n in t.traverse()]
    assert ids == [1, 2, 3, 4, 5, 6, 7, 8, 9]

def test_splay_tree_product_insertion_name():
    t = SplayTree[Product]()
    products = [
        Product(product_id=1, name="Apple", price=0.5, category="Fruit", quantity=100),
        Product(product_id=2, name="Banana", price=0.3, category="Fruit", quantity=150),
        Product(product_id=3, name="Cherry", price=0.2, category="Fruit", quantity=200),
        Product(product_id=4, name="Date", price=0.4, category="Fruit", quantity=120),
        Product(product_id=5, name="Elderberry", price=0.6, category="Fruit", quantity=80),
        Product(product_id=6, name="Fig", price=0.7, category="Fruit", quantity=90),
        Product(product_id=7, name="Grape", price=0.8, category="Fruit", quantity=110),
        Product(product_id=8, name="Honeydew", price=0.9, category="Fruit", quantity=70),
        Product(product_id=9, name="Indian Fig", price=1.0, category="Fruit", quantity=60),
    ]

    nodes = [SplayNode(key=p.name, value=p) for p in products]
    for node in nodes:
        t.insert(node.key, node.value)
    
    # search
    node = t.search("Banana")
    assert node is not None and node.value == products[1]
    node = t.search("Indian Fig")
    assert node is not None and node.value == products[8]
    node = t.search("Jackfruit")
    assert node is None

    # traversal yields sorted product names
    names = [n.key for n in t.traverse()]
    assert names == ["Apple", "Banana", "Cherry", "Date", "Elderberry", "Fig", "Grape", "Honeydew", "Indian Fig"]

def test_build_inventory_splay_tree():
    splay_by_id = build_inventory_splay_tree(InventoryKeyType.PRODUCT_ID)
    splay_by_name = build_inventory_splay_tree(InventoryKeyType.PRODUCT_NAME)

    # Check that Splay Trees are not empty
    assert splay_by_id.root is not None
    assert splay_by_name.root is not None

    # Check that we can search for a few known products by ID/name
    # sample data from data/inventory/products.csv
    samples = [
        ("00009998", "Broccoli"),  # row 9999
        ("00009999", "Nescafe"), # row 10000
        ("00010000", "Black Coffee") # row 10001
    ]
    for pid, name in samples:
        node = splay_by_id.search(pid)
        assert node is not None
        assert node.value.product_id == pid
        assert node.value.name == name
        node = splay_by_name.search(name)
        assert node is not None
        assert node.value.product_id == pid
        assert node.value.name == name
