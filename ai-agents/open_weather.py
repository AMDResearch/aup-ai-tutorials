# Copyright (C) 2025 Advanced Micro Devices, Inc. All rights reserved.
#
# SPDX-License-Identifier: MIT


from mcp.server.fastmcp import FastMCP
import openmeteo_requests
import requests_cache
from retry_requests import retry


# Initialize FastMCP server
mcp = FastMCP("open-weather")

# Constants
BASE_URL = "https://api.open-meteo.com/v1/forecast"

"""https://open-meteo.com/en/docs"""

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> dict:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """

    # First get the forecast grid endpoint
    variables = ["cloud_cover", "pressure_msl", "surface_pressure",
                 "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m",
                 "weather_code", "precipitation", "rain", "showers",
                 "snowfall", "temperature_2m", "relative_humidity_2m",
                 "apparent_temperature", "is_day"]

    params = {
    	"latitude": latitude,
    	"longitude": longitude,
    	"current": variables,
    }

    responses = openmeteo.weather_api(BASE_URL, params=params)
    # Process first location only
    response = responses[0]
    # Process current data. Order of variables is the same as requested.
    current = response.Current()

    weather_dict = dict.fromkeys(variables, 0.0)
    for idx, item in enumerate(variables):
        weather_dict[item] = current.Variables(idx).Value()

    weather_dict['time'] = current.Time()
    weather_dict['elevation'] = response.Elevation()

    return weather_dict

@mcp.tool()
async def get_weather_past_2_days(latitude: float, longitude: float) -> dict:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """

    # First get the forecast grid endpoint

    variables =  ["temperature_2m", "weather_code", "wind_speed_10m",
                  "soil_temperature_0cm", "relative_humidity_2m",
                  "precipitation_probability", "precipitation", "rain",
                  "showers", "snowfall", "snow_depth"]

    params = {
    	"latitude": latitude,
    	"longitude": longitude,
    	"hourly": variables,
        "past_days": 2,
    }

    responses = openmeteo.weather_api(BASE_URL, params=params)
    # Process first location only
    response = responses[0]
    # Process current data. Order of variables is the same as requested.
    current = response.Current()

    weather_dict = dict.fromkeys(variables, 0.0)
    hourly = response.Hourly()
    for idx, item in enumerate(variables):
        weather_dict[item] = list(hourly.Variables(idx).ValuesAsNumpy())

    weather_dict['elevation'] = response.Elevation()
    weather_dict['difference_to_gmt0'] = response.UtcOffsetSeconds()

    return weather_dict

if __name__ == "__main__":
    mcp.run(transport='stdio')
