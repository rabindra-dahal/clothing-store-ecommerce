import pytest
"""
Run pytest from your project's root folder in the terminal:
pytest -v
"""


def test_browse_clothes_anonymous(client):
    """Test that users can browse clothes freely without a token."""
    response = client.get("/clothes")
    assert response.status_code == 200
    assert len(response.json()) > 0
    # Add index [0] to read the dictionary inside the list
    assert response.json()[0]["name"] == "Classic Denim Jacket"


def test_full_user_workflow(client):
    """Test complete customer journey: signup -> login -> add item -> pay -> check history."""
    
    # 1. Sign Up
    user_payload = {"username": "tester_joe", "password": "securePassword123"}
    signup_res = client.post("/auth/signup", json=user_payload)
    assert signup_res.status_code == 201
    assert signup_res.json()["message"] == "User registered successfully"

    # 2. Log In to fetch Token
    login_res = client.post("/auth/login", json=user_payload)
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. View Empty Cart
    cart_res = client.get("/cart", headers=headers)
    assert cart_res.status_code == 200
    assert cart_res.json()["total_payable_balance"] == 0.0

    # 4. Add Cloth to Cart (Item 1 has base stock of 10)
    add_item_payload = {"cloth_id": 1, "quantity": 2}
    add_res = client.post("/cart/add", json=add_item_payload, headers=headers)
    assert add_res.status_code == 200
    assert "Successfully added" in add_res.json()["message"]

    # 5. Check Cart Updates
    cart_res = client.get("/cart", headers=headers)
    assert cart_res.json()["total_payable_balance"] == 170.00  # 85.00 * 2
    assert len(cart_res.json()["items"]) == 1

    # 6. Checkout & Pay Balance
    payment_payload = {
        "card_number": "1111222233334444",
        "expiry": "11/30",
        "cvv": "999"
    }
    pay_res = client.post("/checkout/pay", json=payment_payload, headers=headers)
    assert pay_res.status_code == 200
    assert pay_res.json()["status"] == "Payment Processed Successfully"
    assert pay_res.json()["payslip"]["amount_paid"] == 170.00

    # 7. Check Order History Logs
    history_res = client.get("/orders", headers=headers)
    assert history_res.status_code == 200
    assert history_res.json()["total_orders"] == 1
    assert history_res.json()["order_history"][0]["amount_paid"] == 170.00

def test_add_to_cart_out_of_stock(client):
    """Test that buying more than available warehouse stock rejects with a 400 error."""
    # Register & Login
    user_payload = {"username": "stock_tester", "password": "password123"}
    client.post("/auth/signup", json=user_payload)
    token = client.post("/auth/login", json=user_payload).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Item ID 5 ("Wool Knit Sweater") only has a seeded inventory stock of 5 units.
    # Attempting to add 10 units should fail.
    bad_item_payload = {"cloth_id": 5, "quantity": 10}
    bad_res = client.post("/cart/add", json=bad_item_payload, headers=headers)
    assert bad_res.status_code == 400
    assert "Insufficient inventory" in bad_res.json()["detail"]
