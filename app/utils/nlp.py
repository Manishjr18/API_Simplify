import os

# Simple keyword-based detection for gold investment questions
GOLD_KEYWORDS = {
    "gold", "digital gold", "sgb", "sovereign gold bond", "24k", "22k", "karat",
    "purity", "hedge", "inflation", "gold price", "bullion", "coin", "kuber", "kuber ai",
    "gold etf", "gold mutual fund", "buy gold", "invest in gold"
}

FACTS = [
    "Gold is commonly viewed as a hedge against inflation and currency depreciation.",
    "Digital gold allows fractional investments and is typically backed by 24K (99.9%) purity gold held with a custodian.",
    "Sovereign Gold Bonds (SGBs) are government securities that offer interest plus price appreciation, but they have lock-in periods.",
    "Physical gold has making/storage costs, while digital gold avoids making charges and enables easy liquidity.",
    "Diversifying a portfolio with 5–10% allocation to gold is a common conservative strategy (not financial advice)."
]

def is_gold_question(text: str) -> bool:
    t = (text or '').lower()
    return any(kw in t for kw in GOLD_KEYWORDS)

def _openai_answer(question: str, api_key: str, model: str) -> str:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        completion = client.chat.completions.create(
            model=model or "gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a concise investment assistant. Keep answers under 80 words."},
                {"role": "user", "content": f"Answer briefly a gold investment question: {question}"}
            ],
            temperature=0.4,
            max_tokens=120
        )
        return completion.choices[0].message.content.strip()
    except Exception:
        return ""


def generate_answer(question: str, config) -> str:
    api_key = getattr(config, "OPENAI_API_KEY", None)
    model = getattr(config, "OPENAI_MODEL", "gpt-4o-mini")

    if api_key:
        ans = _openai_answer(question, api_key, model)
        if ans:
            return ans

    # Fallback: pick a relevant fact heuristically
    t = (question or "").lower()
    if "inflation" in t or "hedge" in t:
        return "Gold is often used as a hedge during inflation, as it tends to retain purchasing power when fiat currencies weaken."
    if "digital" in t or "app" in t or "simplify" in t:
        return "Digital gold enables small ticket purchases, instant buy/sell, and custody by a trusted vault partner—ideal for starting with low amounts."
    if "sgb" in t or "bond" in t or "sovereign" in t:
        return "SGBs are government-backed and pay periodic interest; they suit longer horizons but have a lock-in and price risk at exit."
    if "purity" in t or "24k" in t or "22k" in t:
        return "Investment-grade digital gold is typically 24K (99.9%) purity; jewelry is often 22K due to alloy strength."
    # Generic fact
    return FACTS[0]
