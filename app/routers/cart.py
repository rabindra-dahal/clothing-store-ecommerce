import time
import json
import sqlite3
from datetime import UTC, datetime
from fastapi import APIRouter, Depends, HTTPException
from app.models import CartItemRequest, PaymentRequest
from app.database import get_db_connection
from app.auth import get_current_user

router = APIRouter(tags=["Shopping, Checkout & Orders"])

@router.get("/cart")
def view_cart(current_user: str = Depends(get_current_user)):
    """View items currently in your shopping list saved in SQLite database."""
    conn = get_db_connection()
    query = """
        SELECT c.cloth_id, cl.name, cl.price, c.quantity 
        FROM carts c 
        JOIN clothes cl ON c.cloth_id = cl.id 
        WHERE c.username = ?
    """
    rows = conn.execute(query, (current_user,)).fetchall()
    conn.close()

    cart_details = []
    total_amount = 0.0

    for row in rows:
        item_total = row["price"] * row["quantity"]
        total_amount += item_total
        cart_details.append({
            "cloth_id": row["cloth_id"],
            "name": row["name"],
            "price_per_unit": row["price"],
            "quantity": row["quantity"],
            "subtotal": round(item_total, 2)
        })

    return {
        "user": current_user,
        "items": cart_details,
        "total_payable_balance": round(total_amount, 2)
    }

@router.post("/cart/add")
def add_to_cart(item: CartItemRequest, current_user: str = Depends(get_current_user)):
    """Add a clothing item into your shopping list database table."""
    conn = get_db_connection()
    cloth = conn.execute("SELECT * FROM clothes WHERE id = ?", (item.cloth_id,)).fetchone()
    
    if not cloth:
        conn.close()
        raise HTTPException(status_code=404, detail="Clothing item does not exist")
    
    if cloth["stock"] < item.quantity:
        conn.close()
        raise HTTPException(status_code=400, detail=f"Insufficient inventory. Only {cloth['stock']} units left.")

    existing_cart_item = conn.execute(
        "SELECT quantity FROM carts WHERE username = ? AND cloth_id = ?", 
        (current_user, item.cloth_id)
    ).fetchone()

    if existing_cart_item:
        new_qty = existing_cart_item["quantity"] + item.quantity
        conn.execute(
            "UPDATE carts SET quantity = ? WHERE username = ? AND cloth_id = ?", 
            (new_qty, current_user, item.cloth_id)
        )
    else:
        conn.execute(
            "INSERT INTO carts (username, cloth_id, quantity) VALUES (?, ?, ?)", 
            (current_user, item.cloth_id, item.quantity)
        )
        
    conn.commit()
    conn.close()
    return {"message": f"Successfully added {item.quantity} units of '{cloth['name']}' to your shopping list."}

@router.post("/checkout/pay")
def checkout_and_pay(payment: PaymentRequest, current_user: str = Depends(get_current_user)):
    """Checkout via transactional statements, deduct stock, log receipt details and wipe out the active cart."""
    conn = get_db_connection()
    
    query = """
        SELECT c.cloth_id, cl.name, cl.category, cl.price, cl.stock, c.quantity 
        FROM carts c 
        JOIN clothes cl ON c.cloth_id = cl.id 
        WHERE c.username = ?
    """
    cart_items = conn.execute(query, (current_user,)).fetchall()
    
    if not cart_items:
        conn.close()
        raise HTTPException(status_code=400, detail="Your shopping list is empty.")

    shopped_clothes_info = []
    total_bill = 0.0

    for item in cart_items:
        if item["stock"] < item["quantity"]:
            conn.close()
            raise HTTPException(
                status_code=400, 
                detail=f"Stock mismatch for '{item['name']}'. Only {item['stock']} items available now."
            )
        
        item_cost = item["price"] * item["quantity"]
        total_bill += item_cost
        shopped_clothes_info.append({
            "cloth_id": item["cloth_id"],
            "name": item["name"],
            "category": item["category"],
            "unit_price": item["price"],
            "purchased_quantity": item["quantity"],
            "subtotal": round(item_cost, 2)
        })

    try:
        conn.execute("BEGIN")
        
        for item in cart_items:
            new_stock = item["stock"] - item["quantity"]
            conn.execute("UPDATE clothes SET stock = ? WHERE id = ?", (new_stock, item["cloth_id"]))
            
        tx_id = f"TXN-{int(time.time())}-{current_user.upper()[:3]}"
        timestamp_str = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
        masked_card = f"************{payment.card_number[-4:]}"
        items_json_str = json.dumps(shopped_clothes_info)
        
        conn.execute(
            "INSERT INTO payments (transaction_id, timestamp, customer, amount_paid, card_masked, shopped_items_json) VALUES (?, ?, ?, ?, ?, ?)",
            (tx_id, timestamp_str, current_user, round(total_bill, 2), masked_card, items_json_str)
        )
        
        conn.execute("DELETE FROM carts WHERE username = ?", (current_user,))
        conn.commit()
    except sqlite3.Error as e:
        conn.execute("ROLLBACK")
        conn.close()
        raise HTTPException(status_code=500, detail=f"Transaction processing failed: {str(e)}")

    conn.close()
    return {
        "status": "Payment Processed Successfully",
        "payslip": {
            "transaction_id": tx_id,
            "timestamp": timestamp_str,
            "customer": current_user,
            "amount_paid": round(total_bill, 2),
            "payment_status": "SUCCESSFUL",
            "card_masked": masked_card,
            "shopped_items": shopped_clothes_info
        }
    }

@router.get("/orders")
def view_order_history(current_user: str = Depends(get_current_user)):
    """Retrieve all past payslip transaction logs straight from SQLite fields."""
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM payments WHERE customer = ? ORDER BY timestamp DESC", (current_user,)).fetchall()
    conn.close()

    history = []
    for row in rows:
        history.append({
            "transaction_id": row["transaction_id"],
            "timestamp": row["timestamp"],
            "amount_paid": row["amount_paid"],
            "payment_status": "SUCCESSFUL",
            "card_masked": row["card_masked"],
            "shopped_items": json.loads(row["shopped_items_json"])
        })

    return {
        "user": current_user,
        "total_orders": len(history),
        "order_history": history
    }
