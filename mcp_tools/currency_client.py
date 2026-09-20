import asyncio
import json
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def _convert_currency(
    amount: float,
    from_currency: str,
    to_currency: str,
) -> dict:
    """
    Call the currency MCP server and convert an amount
    from one currency to another.
    """

    server_params = StdioServerParameters(
        command=sys.executable,
        args=[
            "-m",
            "mcp_tools.currency_server",
        ],
    )

    async with stdio_client(server_params) as streams:

        read_stream, write_stream = streams

        async with ClientSession(
            read_stream,
            write_stream,
        ) as session:

            # Initialize MCP connection
            await session.initialize()

            # Call MCP tool
            result = await session.call_tool(
                "convert_currency",
                arguments={
                    "amount": amount,
                    "from_currency": from_currency.upper(),
                    "to_currency": to_currency.upper(),
                },
            )

            # Handle MCP tool errors
            if result.isError:
                error_message = "Currency MCP tool failed."

                if result.content:
                    error_message = (
                        f"Currency MCP tool failed: "
                        f"{result.content}"
                    )

                raise RuntimeError(error_message)

            # Parse MCP response
            for block in result.content:

                if hasattr(block, "text"):
                    try:
                        return json.loads(block.text)

                    except json.JSONDecodeError as exc:
                        raise RuntimeError(
                            "Currency MCP returned invalid JSON."
                        ) from exc

            raise RuntimeError(
                "Currency MCP tool returned no usable response."
            )


def convert_currency(
    amount: float,
    from_currency: str,
    to_currency: str,
) -> dict:
    """
    Synchronous wrapper used by the travel application.
    """

    if amount < 0:
        raise ValueError(
            "Amount cannot be negative."
        )

    if not from_currency:
        raise ValueError(
            "Source currency is required."
        )

    if not to_currency:
        raise ValueError(
            "Target currency is required."
        )

    return asyncio.run(
        _convert_currency(
            amount=amount,
            from_currency=from_currency,
            to_currency=to_currency,
        )
    )


if __name__ == "__main__":

    try:
        conversion = convert_currency(
            amount=50000,
            from_currency="INR",
            to_currency="SGD",
        )

        print(
            json.dumps(
                conversion,
                indent=2,
            )
        )

    except Exception as exc:
        print(
            f"Currency conversion failed: {exc}"
        )