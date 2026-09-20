import httpx

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("currency")


@mcp.tool()
async def convert_currency(
    amount: float,
    from_currency: str,
    to_currency: str,
) -> dict:
    """
    Convert an amount from one currency to another
    using a current exchange rate.
    """

    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    url = "https://api.frankfurter.app/latest"

    params = {
        "amount": amount,
        "from": from_currency,
        "to": to_currency,
    }

    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.get(
            url,
            params=params,
        )

        response.raise_for_status()
        data = response.json()

    converted_amount = data.get(
        "rates",
        {},
    ).get(to_currency)

    if converted_amount is None:
        raise ValueError(
            f"Could not convert "
            f"{from_currency} to {to_currency}."
        )

    return {
        "source": "Frankfurter",
        "date": data.get("date"),
        "amount": amount,
        "from_currency": from_currency,
        "to_currency": to_currency,
        "converted_amount": converted_amount,
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")