import re


SUPPORTED_CURRENCIES = {
    "INR",
    "SGD",
    "USD",
    "EUR",
}


def extract_currency_request(
    user_message: str,
):
    text = user_message.upper()

    currencies = [
        currency
        for currency in SUPPORTED_CURRENCIES
        if currency in text
    ]

    amount_match = re.search(
        r"[\d,]+(?:\.\d+)?",
        text,
    )

    if not amount_match:
        return None

    amount = float(
        amount_match.group(0).replace(",", "")
    )

    if len(currencies) < 2:
        return None

    # Preserve order in the user's sentence
    positions = sorted(
        (
            text.find(currency),
            currency,
        )
        for currency in currencies
    )

    from_currency = positions[0][1]
    to_currency = positions[1][1]

    return {
        "amount": amount,
        "from_currency": from_currency,
        "to_currency": to_currency,
    }
