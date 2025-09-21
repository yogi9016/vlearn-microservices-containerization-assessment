import pytest
import requests

# Base URLs
GATEWAY_SERVICE = "http://localhost:3003"
USER_SERVICE = f"{GATEWAY_SERVICE}/api/users"
PRODUCT_SERVICE = f"{GATEWAY_SERVICE}/api/products"
ORDER_SERVICE = f"{GATEWAY_SERVICE}/api/orders"

def test_end_to_end_order_flow():
    # 1️⃣ Get list of users
    r_users = requests.get(f"{USER_SERVICE}")
    assert r_users.status_code == 200, "Failed to get users"
    users = r_users.json()
    assert len(users) > 0, "No users found"
    user_id = users[0]['id']  # pick the first user

    # 2️⃣ Get list of products
    r_products = requests.get(f"{PRODUCT_SERVICE}")
    assert r_products.status_code == 200, "Failed to get products"
    products = r_products.json()
    assert len(products) > 0, "No products found"
    product_id = products[0]['id']  # pick the first product

    # 3️⃣ Get current orders
    r_orders_before = requests.get(f"{ORDER_SERVICE}")
    assert r_orders_before.status_code == 200, "Failed to get orders before placing new order"
    orders_before = r_orders_before.json()
    count_before = len(orders_before)

    # 4️⃣ Place a new order
    order_payload = {
        "userId": user_id,
        "productId": product_id,
    }
    r_place_order = requests.post(f"{ORDER_SERVICE}", json=order_payload)
    assert r_place_order.status_code == 200, "Failed to place order"
    order_response = r_place_order.json()
    assert order_response.get('id') is not None, "Order ID missing in response"

    # 5️⃣ Get orders again to verify
    r_orders_after = requests.get(f"{ORDER_SERVICE}")
    assert r_orders_after.status_code == 200, "Failed to get orders after placing new order"
    orders_after = r_orders_after.json()
    assert len(orders_after) == count_before + 1, "Order was not added successfully"
    assert any(order['id'] == order_response['id'] for order in orders_after), "New order not found in order list"