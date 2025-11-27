import importlib


def test_import_modules():
    # Smoke test to ensure modules import without runtime errors
    modules = [
        "src.pos_system",
        "src.pos_system.common",
        "src.pos_system.inventory",
        "src.pos_system.inventory.binary_search_tree",
        "src.pos_system.inventory.splay_tree",
        "src.pos_system.loyalty",
        "src.pos_system.loyalty.avl_tree",
    ]
    for mod in modules:
        importlib.import_module(mod)
