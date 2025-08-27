from flask import Blueprint, request, jsonify, current_app
from app.database import db
from app.models import Purchase

purchase_bp = Blueprint('purchase', __name__)

@purchase_bp.route('/purchase', methods=['POST'])
def purchase():
    data = request.get_json(silent=True) or {}
    user_name = (data.get("user_name") or "guest").strip()
    amount = data.get("amount")

    # Validate amount
    try:
        amount = float(amount) if amount is not None else 10.0
        if amount <= 0:
            raise ValueError()
    except Exception:
        return jsonify({"error": "Invalid 'amount'. Provide a positive number, e.g., 10"}), 400

    # Price per gram (hardcoded/override via env)
    price_per_gram = float(current_app.config.get("PRICE_PER_GRAM", 7500))
    grams = round(amount / price_per_gram, 6)

    purchase = Purchase(
        user_name=user_name or "guest",
        amount=amount,
        grams=grams,
        price_per_gram=price_per_gram,
        status="success"
    )
    db.session.add(purchase)
    db.session.commit()

    return jsonify({
        "message": f"Congratulations {user_name or 'guest'}! Your digital gold purchase of ₹{amount:.2f} succeeded.",
        "status": "success",
        "data": {
            "purchase_id": purchase.id,
            "user_name": purchase.user_name,
            "amount": purchase.amount,
            "grams": purchase.grams,
            "price_per_gram": purchase.price_per_gram,
            "created_at": purchase.created_at.isoformat()
        }
    }), 200
