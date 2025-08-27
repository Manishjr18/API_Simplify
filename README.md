# Simplify Money – AI Intern Assignment (Flask)

This project emulates a **Kuberi-style workflow** for **gold investments** with two APIs:

1. **`POST /ask`** — Detects if a user's question is related to gold investments, returns a concise fact-based answer, and nudges the user to purchase digital gold on Simplify Money.
2. **`POST /purchase`** — Simulates a digital gold purchase, makes a database entry, and returns a success response.

> **Note:** OpenAI integration is **optional**. By default, the system uses a lightweight rule-based fallback so it works 100% offline and free. If you provide an OpenAI API key, it will use LLM for richer answers.

---

## 🧱 Project Structure

```
simplify_ai_flask/
├── app.py
├── .env.example
├── requirements.txt
├── README.md
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── ask.py
│   │   └── purchase.py
│   └── utils/
│       └── nlp.py
└── Procfile
```

---

## 🚀 Quickstart (Local)

1. **Create & activate a virtual environment (recommended)**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **(Optional) Configure OpenAI**
   - Copy `.env.example` → `.env` and add your `OPENAI_API_KEY` (only if you want LLM-generated answers).
   - Otherwise, the rule-based answers will be used automatically.

4. **Run the app**
   ```bash
   python app.py
   ```
   The server starts on `http://127.0.0.1:5000`.

5. **Test the APIs**

   **Ask (gold Q&A + nudge)**
   ```bash
   curl -X POST http://127.0.0.1:5000/ask \
        -H "Content-Type: application/json" \
        -d '{"question": "Is gold a good investment during inflation?"}'
   ```

   **Purchase (simulate digital gold)**  
   ```bash
   curl -X POST http://127.0.0.1:5000/purchase \
        -H "Content-Type: application/json" \
        -d '{"user_name": "Manish", "amount": 10}'
   ```

---

## 📦 Deployment (Free-friendly)

**Render.com** (recommended)
- Connect your GitHub repository.
- **Build command:** `pip install -r requirements.txt`
- **Start command:** `gunicorn app:app`
- Environment: `PYTHON_VERSION=3.10` (or 3.11)

*(Heroku no longer offers a fully free tier.)*

---

## 🔐 Environment Variables

Create a `.env` file (optional) with:

```
# Enable OpenAI (optional)
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini

# If unset, the app uses offline rule-based answers.
```

---

## 🗄️ Database

- Uses **SQLite** (`sqlite:///db.sqlite3`) – zero setup.
- Table: `purchases` with `id`, `user_name`, `amount`, `grams`, `price_per_gram`, `status`, `created_at`.

---

## 🧪 Example Responses

### `/ask`
```json
{
  "related": true,
  "answer": "Gold is often used as a hedge against inflation because its price tends to hold value when fiat currency weakens.",
  "nudge": "You can invest in gold using Simplify Money via digital gold purchase. Would you like to proceed?",
  "next_action": {
    "endpoint": "/purchase",
    "method": "POST",
    "required_fields": ["user_name", "amount"]
  }
}
```

### `/purchase`
```json
{
  "message": "Congratulations Manish! Your digital gold purchase of ₹10.00 succeeded.",
  "status": "success",
  "data": {
    "purchase_id": 1,
    "user_name": "Manish",
    "amount": 10.0,
    "grams": 0.00133,
    "price_per_gram": 7500.0,
    "created_at": "2025-08-25T18:30:00"
  }
}
```

---

## 🛠️ Tech Choices

- **Flask** for APIs
- **Flask-SQLAlchemy** + **SQLite** for storage
- **Optional OpenAI** for richer answers, with **rule-based fallback** (works offline)
- **Gunicorn** for production server

---

## ✅ Submission Checklist

- [x] Public repo link or zip
- [x] Updated CV
- [x] Solution details (this README), deployment notes, and run steps
- [x] Bullet points on approach & challenges
- [x] APIs deployed and testable (Render link), or runnable locally

---

## 🧩 Approach & Notes

- Intent detection uses keyword heuristics (e.g., "gold", "digital gold", "SGB", "24k", "sovereign", "hedge", "inflation", "purity").
- Answer generation: attempts OpenAI if configured; otherwise, returns curated facts from an internal knowledge base.
- Purchase flow is simulated; price per gram is configurable/hardcoded (default ₹7500). Amount → grams computed = `amount / price_per_gram`.
- All purchases are recorded with a timestamp.

**Good luck!** 🚀
