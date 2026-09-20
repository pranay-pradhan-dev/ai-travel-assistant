from enum import Enum


class Intent(str, Enum):
    RAG_ONLY = "rag_only"
    WEATHER_ONLY = "weather_only"
    CURRENCY_ONLY = "currency_only"
    RAG_AND_WEATHER = "rag_and_weather"
    RAG_AND_CURRENCY = "rag_and_currency"
    RAG_WEATHER_CURRENCY = "rag_weather_currency"


WEATHER_TERMS = {
    "weather",
    "forecast",
    "rain",
    "raining",
    "temperature",
    "climate",
}

CURRENCY_TERMS = {
    "convert",
    "currency",
    "exchange",
    "sgd",
    "inr",
    "usd",
    "eur",
    "budget",
}

TRAVEL_PLANNING_TERMS = {
    "plan",
    "trip",
    "itinerary",
    "attraction",
    "attractions",
    "visit",
    "activities",
    "activity",
    "sightseeing",
    "family",
    "cultural",
    "indoor",
    "outdoor",
}


def _contains_any(text: str, terms: set[str]) -> bool:
    return any(term in text for term in terms)


def detect_intent(user_message: str) -> Intent:

    text = user_message.lower()

    has_weather = _contains_any(
        text,
        WEATHER_TERMS,
    )

    has_currency = _contains_any(
        text,
        CURRENCY_TERMS,
    )

    has_travel = _contains_any(
        text,
        TRAVEL_PLANNING_TERMS,
    )

    if has_weather and has_currency and has_travel:
        return Intent.RAG_WEATHER_CURRENCY

    if has_weather and has_travel:
        return Intent.RAG_AND_WEATHER

    if has_currency and has_travel:
        return Intent.RAG_AND_CURRENCY

    if has_weather:
        return Intent.WEATHER_ONLY

    if has_currency:
        return Intent.CURRENCY_ONLY

    return Intent.RAG_ONLY