"""Command-line chatbot for answering 123Burger customer questions."""

from __future__ import annotations

import re
from dataclasses import dataclass
from difflib import SequenceMatcher


@dataclass(frozen=True)
class FAQ:
    intent: str
    answer: str
    keywords: tuple[str, ...]


RESTAURANT_NAME = "123Burger"
PHONE_NUMBER = "(+1) 919-679-7400"
EMAIL_ADDRESS = "123burgernc@gmail.com"
ADDRESS = "4150 Fayetteville Rd, Raleigh, NC 27603"
ORDERING_URL = "https://www.123burger.com/menu"
APP_STORE_URL = "https://apps.apple.com/pk/app/123burger/id6748468634"
GOOGLE_PLAY_URL = "https://play.google.com/store/apps/details?id=com.app.burger123"

HOURS = (
    "Monday through Thursday: 10:30 AM to 9:30 PM; "
    "Friday and Saturday: 10:30 AM to 11:00 PM; "
    "Sunday: 10:30 AM to 9:30 PM."
)

MENU_ITEMS = (
    "#1 Cheese Burger - $7.99, combo $12.99",
    "#2 Double Cheeseburger - $8.99, combo $14.99",
    "#3 Triple Cheeseburger - $10.99, combo $17.99",
    "#1 Chicken Sandwich - $7.99, combo $11.99",
    "#2 Spicy Sandwich - $7.99, combo $11.99",
    "#3 Chicken Tenders 3pcs - $14.99, combo $14.99",
    "Fries - $3.99",
    "Shakes - $6.99",
)

FAQS = (
    FAQ(
        intent="hours",
        answer=(
            f"{RESTAURANT_NAME} is open {HOURS} You can call {PHONE_NUMBER} to "
            "confirm holiday hours or today's closing time."
        ),
        keywords=("hours", "open", "close", "closing", "time", "schedule", "today", "when"),
    ),
    FAQ(
        intent="location",
        answer=(
            f"{RESTAURANT_NAME} is located at {ADDRESS}. It serves the Raleigh, NC "
            "community with pickup available."
        ),
        keywords=("where", "location", "address", "directions", "parking", "garage", "raleigh"),
    ),
    FAQ(
        intent="reservations",
        answer=(
            f"{RESTAURANT_NAME} is a casual burger restaurant focused on pickup and "
            f"made-to-order food. For large groups or special requests, call {PHONE_NUMBER}."
        ),
        keywords=("reservation", "reserve", "booking", "book", "table", "party", "group"),
    ),
    FAQ(
        intent="menu",
        answer=(
            "The menu includes burgers, chicken, fries, and shakes. Current listed "
            f"items include: {'; '.join(MENU_ITEMS)}."
        ),
        keywords=("menu", "dish", "food", "popular", "recommend", "special", "price", "cost"),
    ),
    FAQ(
        intent="burgers",
        answer=(
            f"{RESTAURANT_NAME} lists a #1 Cheese Burger for $7.99, #2 Double "
            "Cheeseburger for $8.99, and #3 Triple Cheeseburger for $10.99. Combos "
            "are listed at $12.99, $14.99, and $17.99."
        ),
        keywords=("burger", "burgers", "cheeseburger", "double", "bacon", "toppings", "combo"),
    ),
    FAQ(
        intent="chicken",
        answer=(
            f"{RESTAURANT_NAME} serves a #1 Chicken Sandwich for $7.99, #2 Spicy "
            "Sandwich for $7.99, and #3 Chicken Tenders 3pcs for $14.99. Chicken "
            "sandwich combos are listed at $11.99."
        ),
        keywords=("chicken", "sandwich", "spicy", "tenders", "tender", "crispy"),
    ),
    FAQ(
        intent="fries_shakes",
        answer=(
            "Fries are listed at $3.99 and shakes are listed at $6.99. The site says "
            "fries are cut daily from whole potatoes and cooked in beef tallow."
        ),
        keywords=("fries", "fry", "shake", "shakes", "ice cream", "dessert", "beef tallow"),
    ),
    FAQ(
        intent="halal",
        answer=(
            f"Yes. {RESTAURANT_NAME} describes its food as fresh, halal, and made to "
            "order, with premium Black Angus beef that is fresh and never frozen."
        ),
        keywords=("halal", "angus", "beef", "fresh", "frozen", "made to order"),
    ),
    FAQ(
        intent="dietary",
        answer=(
            "Please call or ask the team before ordering if you have allergies or "
            "dietary restrictions. The menu includes beef, chicken, fries cooked in "
            "beef tallow, shakes, and other items that may involve common allergens."
        ),
        keywords=(
            "vegetarian",
            "vegan",
            "gluten",
            "allergy",
            "allergies",
            "dairy",
            "nut",
            "dietary",
        ),
    ),
    FAQ(
        intent="takeout",
        answer=(
            f"Pickup is available in Raleigh. Start an order at {ORDERING_URL}, or "
            f"call {PHONE_NUMBER} if you need help."
        ),
        keywords=("takeout", "pickup", "delivery", "deliver", "order", "to-go", "togo", "online"),
    ),
    FAQ(
        intent="app",
        answer=(
            f"{RESTAURANT_NAME} has a mobile app for deals, one-tap reordering, and "
            f"order tracking. App Store: {APP_STORE_URL}. Google Play: {GOOGLE_PLAY_URL}."
        ),
        keywords=("app", "mobile", "download", "iphone", "android", "track", "tracking"),
    ),
    FAQ(
        intent="contact",
        answer=(
            f"You can reach {RESTAURANT_NAME} at {PHONE_NUMBER} or {EMAIL_ADDRESS}."
        ),
        keywords=("phone", "call", "email", "contact", "number", "reach"),
    ),
    FAQ(
        intent="kids",
        answer=(
            "Families are welcome. Kid-friendly picks can include the cheese burger, "
            "fries, chicken tenders, and shakes."
        ),
        keywords=("kids", "children", "family", "families", "child", "high chair"),
    ),
)

GREETINGS = ("hi", "hello", "hey", "good morning", "good afternoon", "good evening")
THANKS = ("thanks", "thank you", "thx", "appreciate it")
GOODBYES = ("bye", "goodbye", "see you", "quit", "exit")


def normalize(text: str) -> str:
    """Lowercase text and keep only searchable words."""
    return " ".join(re.findall(r"[a-z0-9']+", text.lower()))


def token_set(text: str) -> set[str]:
    return set(normalize(text).split())


def has_phrase(normalized: str, tokens: set[str], phrase: str) -> bool:
    if " " in phrase:
        return phrase in normalized
    return phrase in tokens


def score_question(question: str, faq: FAQ) -> float:
    normalized = normalize(question)
    tokens = token_set(question)
    keyword_hits = sum(1 for keyword in faq.keywords if keyword in normalized or keyword in tokens)
    fuzzy = max(SequenceMatcher(None, normalized, keyword).ratio() for keyword in faq.keywords)
    return keyword_hits * 2.5 + fuzzy


def answer_question(question: str) -> str:
    normalized = normalize(question)

    if not normalized:
        return "Please type a question and I will do my best to help."

    tokens = token_set(question)

    if any(has_phrase(normalized, tokens, greeting) for greeting in GREETINGS):
        return f"Hello! I am the {RESTAURANT_NAME} assistant. How can I help today?"

    if any(has_phrase(normalized, tokens, thank) for thank in THANKS):
        return "You are very welcome. Anything else I can help with?"

    if any(has_phrase(normalized, tokens, goodbye) for goodbye in GOODBYES):
        return "Thanks for chatting with us. We hope to see you soon!"

    best_faq = max(FAQS, key=lambda faq: score_question(question, faq))
    best_score = score_question(question, best_faq)

    if best_score < 1.35:
        return (
            "I am not completely sure about that. I can help with hours, location, "
            "menu items, burger prices, chicken, fries, shakes, halal information, "
            "takeout, contact details, the mobile app, and family-friendly options."
        )

    return best_faq.answer


def run_chat() -> None:
    print(f"Welcome to {RESTAURANT_NAME} customer support.")
    print("Ask a question, or type 'quit' to leave.")

    while True:
        try:
            question = input("\nYou: ").strip()
        except EOFError:
            print("\nBot: Chat ended. We hope to see you soon!")
            break

        response = answer_question(question)
        print(f"Bot: {response}")

        if normalize(question) in {"quit", "exit", "bye", "goodbye"}:
            break


if __name__ == "__main__":
    run_chat()
