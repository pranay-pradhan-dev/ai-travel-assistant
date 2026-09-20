import asyncio
import json
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


SINGAPORE_LATITUDE = 1.3521
SINGAPORE_LONGITUDE = 103.8198


async def _get_weather(
    forecast_days: int = 3,
) -> dict:

    server_params = StdioServerParameters(
        command=sys.executable,
        args=[
            "-m",
            "mcp_tools.weather_server",
        ],
    )

    async with stdio_client(server_params) as streams:

        read_stream, write_stream = streams

        async with ClientSession(
            read_stream,
            write_stream,
        ) as session:

            await session.initialize()

            result = await session.call_tool(
                "get_weather",
                arguments={
                    "latitude": SINGAPORE_LATITUDE,
                    "longitude": SINGAPORE_LONGITUDE,
                    "forecast_days": forecast_days,
                },
            )

            if result.isError:
                raise RuntimeError(
                    f"Weather MCP tool failed: {result.content}"
                )

            for block in result.content:

                if hasattr(block, "text"):
                    return json.loads(block.text)

            raise RuntimeError(
                "Weather MCP tool returned no text response."
            )


def get_weather(
    forecast_days: int = 3,
) -> dict:

    return asyncio.run(
        _get_weather(forecast_days)
    )