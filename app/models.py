from datetime import datetime
from app.database import db

class Purchase(db.Model):
    __tablename__ = "purchases"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Float, nullable=False)  # INR
    grams = db.Column(db.Float, nullable=False)   # computed based on price_per_gram
    price_per_gram = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="success")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
