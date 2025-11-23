"""Loyalty module: customer loyalty and discount implementations."""

from src.pos_system.common.logger import log_operation

__all__ = ["BinaryTree", "AVLTree"]

def update_points(tree, customer_id, earned_points):
    updated = False
    customer = tree.search(customer_id)
    if not customer:
        return updated
    old_points = customer.loyalty_points
    customer.loyalty_points += earned_points

    # Tier upgrade logic
    old_tier = customer.tier
    if customer.loyalty_points >= 1000:
        customer.tier = "Gold"
    elif customer.loyalty_points >= 500:
        customer.tier = "Silver"
    else:
        customer.tier = "Bronze"

    log_operation(f"Updated Points: {customer_id}, {old_points} -> {customer.loyalty_points}, Tier: {old_tier} -> {customer.tier}")
    return True

def calculate_discount(customer):
    if customer.tier == "Gold":
        return 20
    elif customer.tier == "Silver":
        return 10
    return 5  # Bronze tier

def top_n_customers(tree, n):
    # Get all customers in-order
    customers = tree.inorder_traversal()
    # Sort descending by loyalty points
    customers_sorted = sorted(customers, key=lambda c: c.loyalty_points, reverse=True)
    log_operation(f"Top {n} customers by points generated")
    return customers_sorted[:n]

# ----------------- Range Query by Points -----------------
def range_query(tree, min_points, max_points):
    customers = tree.inorder_traversal()
    filtered = [c for c in customers if min_points <= c.loyalty_points <= max_points]
    log_operation(f"Range query for points {min_points} to {max_points} generated ({len(filtered)} customers)")
    return filtered
