from flask import Blueprint, request, jsonify, current_app
from app.utils.nlp import is_gold_question, generate_answer

ask_bp = Blueprint('ask', __name__)

@ask_bp.route('/ask', methods=['POST'])
def ask():
    data = request.get_json(silent=True) or {}
    question = (data.get("question") or "").strip()

    if not question:
        return jsonify({"error": "Missing field: 'question'"}), 400

    related = is_gold_question(question)

    if not related:
        return jsonify({
            "related": False,
            "answer": "This question is not identified as a gold investment query. Try asking about digital gold, SGBs, purity, price, or hedging with gold."
        }), 200

    answer = generate_answer(question, current_app.config)

    return jsonify({
        "related": True,
        "answer": answer,
        "nudge": "You can invest in gold using Simplify Money via digital gold purchase. Would you like to proceed?",
        "next_action": {
            "endpoint": "/purchase",
            "method": "POST",
            "required_fields": ["user_name", "amount"]
        }
    }), 200
