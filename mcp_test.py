import os
import json
import sys
import logging
from datetime import datetime
from typing import Any

import httpx
from dotenv import load_dotenv
from mcp.server import Server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource
)
from pydantic import AnyUrl
from mcp.server.fastmcp import FastMCP

print("=========== inside tavily.py", file=sys.stderr)
load_dotenv()

API_KEY = '4f90789d50446720d03a89a9010c66bf'

API_BASE_URL = "http://api.openweathermap.org/data/2.5"
DEFAULT_CITY = "Seoul"

http_params = {
    "appid": API_KEY,
    "units": "metric"
}

websearch_config = {
    "parameters": {
        "default_num_results": 5,
        "include_domains": []
    }
}

mcp = FastMCP(
    name="weather_search", 
    version="1.0.0",
    description="weather search with given city name"
)

@mcp.tool()
def fetch_weather(city: str):
    """지정된 도시의 현재 날씨 정보를 가져옵니다."""
    print("================== before fetch_weather", file=sys.stderr)
    response = httpx.get(
        f"{API_BASE_URL}/weather",
        params={"q": city, **http_params}
    )
    response.raise_for_status()
    data = response.json()
    print("================== after fetch_weather", file=sys.stderror)
    return {
        "temperature": data["main"]["temp"],
        "conditions": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "timestamp": datetime.now().isoformat()
    }

    
if __name__ == "__main__":
    mcp.run()
