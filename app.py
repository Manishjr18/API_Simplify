
# from flask import Flask, request, jsonify, render_template
# from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS
# from datetime import datetime
# import os
# import random

# app = Flask(__name__)
# CORS(app)

# # ===========================
# # SQLite Database Config
# # ===========================
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'purchases.db')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# # ===========================
# # Database Model
# # ===========================
# class Purchase(db.Model):
#     __tablename__ = "purchases"

#     id = db.Column(db.Integer, primary_key=True)
#     user_name = db.Column(db.String(100), nullable=False)
#     amount = db.Column(db.Float, nullable=False)
#     grams = db.Column(db.Float, nullable=False)
#     price_per_gram = db.Column(db.Float, nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

#     def to_dict(self):
#         return {
#             "purchase_id": self.id,
#             "user_name": self.user_name,
#             "amount": self.amount,
#             "grams": self.grams,
#             "price_per_gram": self.price_per_gram,
#             "created_at": self.created_at.isoformat()
#         }

# # ===========================
# # Create DB (Only once)
# # ===========================
# with app.app_context():
#     db.create_all()

# # ===========================
# # API 1: Ask Question
# # ===========================
# GOLD_KEYWORDS = {"gold", "digital gold", "sgb", "sovereign gold bond", "carat","24k", "22k",
#                  "karat", "purity", "hedge", "inflation", "gold price", "bullion", "coin",
#                  "kuber", "kuber ai", "gold etf", "gold mutual fund", "buy gold", "invest in gold"}

# GOLD_RESPONSES = [
#     "Gold is a timeless investment and often acts as a hedge against inflation.",
#     "Investing in digital gold is a convenient way to own gold without physical storage.",
#     "Sovereign Gold Bonds are government-backed and can earn interest along with capital appreciation.",
#     "24K gold is the purest form, but 22K is more common for investment jewelry.",
#     "Gold can protect your wealth against market volatility and currency devaluation.",
#     "Buying gold ETFs is a modern, liquid alternative to physical gold."
# ]

# @app.route('/ask', methods=['POST'])
# def ask_question():
#     data = request.get_json()
#     question = data.get("question", "").lower()

#     # Check if gold related
#     related = any(kw in question for kw in GOLD_KEYWORDS)

#     if related:
#         answer = random.choice(GOLD_RESPONSES)
#         return jsonify({
#             "answer": answer,
#             "next_action": {
#                 "endpoint": "/purchase",
#                 "method": "POST",
#                 "required_fields": ["user_name", "amount"]
#             },
#             "nudge": "You can invest in gold using Simplify Money via digital gold purchase. Would you like to proceed?",
#             "related": True
#         }), 200
#     else:
#         return jsonify({
#             "answer": "This question is not identified as a gold investment query. Try asking about digital gold, SGBs, purity, price, or hedging with gold.",
#             "related": False
#         }), 200

# # ===========================
# # API 2: Purchase Gold
# # ===========================
# @app.route('/purchase', methods=['POST'])
# def purchase_gold():
#     try:
#         data = request.get_json()
#         user_name = data['user_name']
#         amount = float(data['amount'])

#         # Gold price fixed (for now)
#         price_per_gram = 7500.0
#         grams = round(amount / price_per_gram, 6)

#         # Save to DB
#         purchase = Purchase(
#             user_name=user_name,
#             amount=amount,
#             grams=grams,
#             price_per_gram=price_per_gram
#         )
#         db.session.add(purchase)
#         db.session.commit()

#         return jsonify({
#             "status": "success",
#             "message": f"Congratulations {user_name}! Your digital gold purchase of ₹{amount:.2f} succeeded.",
#             "data": purchase.to_dict()
#         }), 201

#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 400

# # ===========================
# # API 3: Get All Purchases
# # ===========================
# @app.route('/purchases', methods=['GET'])
# def get_purchases():
#     try:
#         all_purchases = Purchase.query.all()
#         return jsonify([p.to_dict() for p in all_purchases]), 200
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 400

# # ===========================
# # API 4: Get Single Purchase
# # ===========================
# @app.route('/purchase/<int:purchase_id>', methods=['GET'])
# def get_purchase(purchase_id):
#     purchase = Purchase.query.get(purchase_id)
#     if not purchase:
#         return jsonify({"status": "error", "message": "Purchase not found"}), 404
#     return jsonify(purchase.to_dict()), 200

# @app.route('/purchase')
# def purchase_page():
#     return render_template('purchase.html')

# # ===========================
# # Run App
# # ===========================
# if __name__ == '__main__':
#     app.run(debug=True)





from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os
import random

app = Flask(__name__)
CORS(app)

# ===========================
# SQLite Database Config
# ===========================
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'purchases.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ===========================
# Database Model
# ===========================
class Purchase(db.Model):
    __tablename__ = "purchases"

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    grams = db.Column(db.Float, nullable=False)
    price_per_gram = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "purchase_id": self.id,
            "user_name": self.user_name,
            "amount": self.amount,
            "grams": self.grams,
            "price_per_gram": self.price_per_gram,
            "created_at": self.created_at.isoformat()
        }

# ===========================
# Create DB (Only once)
# ===========================
with app.app_context():
    db.create_all()

# ===========================
# API 1: Ask Question
# ===========================
GOLD_KEYWORDS = {"gold", "digital gold", "sgb", "sovereign gold bond", "carat","24k", "22k",
                 "karat", "purity", "hedge", "inflation", "gold price", "bullion", "coin",
                 "kuber", "kuber ai", "gold etf", "gold mutual fund", "buy gold", "invest in gold"}

GOLD_RESPONSES = [
    "Gold is a timeless investment and often acts as a hedge against inflation.",
    "Investing in digital gold is a convenient way to own gold without physical storage.",
    "Sovereign Gold Bonds are government-backed and can earn interest along with capital appreciation.",
    "24K gold is the purest form, but 22K is more common for investment jewelry.",
    "Gold can protect your wealth against market volatility and currency devaluation.",
    "Buying gold ETFs is a modern, liquid alternative to physical gold."
]

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get("question", "").lower()

    # Check if gold related
    related = any(kw in question for kw in GOLD_KEYWORDS)

    if related:
        answer = random.choice(GOLD_RESPONSES)
        return jsonify({
            "answer": answer,
            "next_action": {
                "endpoint": "/purchase",
                "method": "POST",
                "required_fields": ["user_name", "amount"]
            },
            "nudge": "You can invest in gold using Simplify Money via digital gold purchase. Would you like to proceed?",
            "related": True
        }), 200
    else:
        return jsonify({
            "answer": "This question is not identified as a gold investment query. Try asking about digital gold, SGBs, purity, price, or hedging with gold.",
            "related": False
        }), 200

# ===========================
# API 2: Purchase Gold
# ===========================
@app.route('/purchase', methods=['POST'])
def purchase_gold():
    try:
        data = request.get_json()
        user_name = data['user_name']
        amount = float(data['amount'])

        # Gold price fixed (for now)
        price_per_gram = 7500.0
        grams = round(amount / price_per_gram, 6)

        # Save to DB
        purchase = Purchase(
            user_name=user_name,
            amount=amount,
            grams=grams,
            price_per_gram=price_per_gram
        )
        db.session.add(purchase)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": f"Congratulations {user_name}! Your digital gold purchase of ₹{amount:.2f} succeeded.",
            "data": purchase.to_dict()
        }), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

# ===========================
# API 3: Get All Purchases
# ===========================
@app.route('/purchases', methods=['GET'])
def get_purchases():
    try:
        all_purchases = Purchase.query.all()
        return jsonify([p.to_dict() for p in all_purchases]), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

# ===========================
# API 4: Get Single Purchase
# ===========================
@app.route('/purchase/<int:purchase_id>', methods=['GET'])
def get_purchase(purchase_id):
    purchase = Purchase.query.get(purchase_id)
    if not purchase:
        return jsonify({"status": "error", "message": "Purchase not found"}), 404
    return jsonify(purchase.to_dict()), 200

# ===========================
# Frontend Pages
# ===========================
@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/purchase-page')
def purchase_page():
    return render_template('purchase.html')

# ===========================
# Run App
# ===========================
if __name__ == '__main__':
    app.run(debug=True)
