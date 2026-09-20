import httpx

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("weather")


@mcp.tool()
async def get_weather(
    latitude: float,
    longitude: float,
    forecast_days: int = 3,
) -> dict:
    """
    Get the weather forecast for a geographic location.
    """

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": ",".join(
            [
                "weather_code",
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_probability_max",
            ]
        ),
        "timezone": "auto",
        "forecast_days": forecast_days,
    }

    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.get(
            url,
            params=params,
        )

        response.raise_for_status()

        data = response.json()

    return {
        "source": "Open-Meteo",
        "latitude": data.get("latitude"),
        "longitude": data.get("longitude"),
        "timezone": data.get("timezone"),
        "daily": data.get("daily", {}),
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")