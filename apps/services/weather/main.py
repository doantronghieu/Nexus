from tabnanny import verbose
import openmeteo_requests
from openmeteo_sdk.Variable import Variable
import requests_cache
from retry_requests import retry
import pandas as pd
import numpy as np
from typing import Dict, Union, Optional, List, Tuple, Any
from dataclasses import dataclass
from collections import defaultdict
import requests
from enum import Enum
from datetime import datetime, timezone
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

# Constants
API_ENDPOINTS = {
    'weather': "https://api.open-meteo.com/v1/forecast",
    'ensemble': "https://ensemble-api.open-meteo.com/v1/ensemble",
    'marine': "https://marine-api.open-meteo.com/v1/marine",
    'air_quality': "https://air-quality-api.open-meteo.com/v1/air-quality",
    'climate': "https://climate-api.open-meteo.com/v1/climate",
    'historical': "https://archive-api.open-meteo.com/v1/archive",
}

GEO_SERVICES = [
    "http://ip-api.com/json/",
    "https://ipapi.co/json/",
    "https://ipinfo.io/json"
]

class WeatherUnits(Enum):
    """Enumeration of available weather units."""
    CELSIUS = "celsius"
    FAHRENHEIT = "fahrenheit"
    KMH = "kmh"
    MS = "ms"
    MPH = "mph"
    KNOTS = "kn"
    MM = "mm"
    INCH = "inch"
    METRIC = "metric"
    IMPERIAL = "imperial"
    LENGTH_METRIC = "metric"     # For marine API
    LENGTH_IMPERIAL = "imperial" # For marine API

class CellSelection(Enum):
    """Enumeration of cell selection options."""
    LAND = "land"
    SEA = "sea"
    NEAREST = "nearest"

class AirQualityDomain(Enum):
    """Enumeration of air quality domains."""
    AUTO = "auto"
    CAMS_EUROPE = "cams_europe"
    CAMS_GLOBAL = "cams_global"

@dataclass
class WeatherCodeData:
    """Class to store weather code interpretations."""
    code: int
    description: str
    severity: str

class WMOWeatherCodes:
    """WMO weather code interpretations."""
    codes = {
        0: WeatherCodeData(0, "Clear sky", "clear"),
        1: WeatherCodeData(1, "Mainly clear", "clear"),
        2: WeatherCodeData(2, "Partly cloudy", "cloudy"),
        3: WeatherCodeData(3, "Overcast", "cloudy"),
        45: WeatherCodeData(45, "Foggy", "fog"),
        48: WeatherCodeData(48, "Depositing rime fog", "fog"),
        51: WeatherCodeData(51, "Light drizzle", "drizzle"),
        53: WeatherCodeData(53, "Moderate drizzle", "drizzle"),
        55: WeatherCodeData(55, "Dense drizzle", "drizzle"),
        56: WeatherCodeData(56, "Light freezing drizzle", "freezing_drizzle"),
        57: WeatherCodeData(57, "Dense freezing drizzle", "freezing_drizzle"),
        61: WeatherCodeData(61, "Slight rain", "rain"),
        63: WeatherCodeData(63, "Moderate rain", "rain"),
        65: WeatherCodeData(65, "Heavy rain", "rain"),
        66: WeatherCodeData(66, "Light freezing rain", "freezing_rain"),
        67: WeatherCodeData(67, "Heavy freezing rain", "freezing_rain"),
        71: WeatherCodeData(71, "Slight snow fall", "snow"),
        73: WeatherCodeData(73, "Moderate snow fall", "snow"),
        75: WeatherCodeData(75, "Heavy snow fall", "snow"),
        77: WeatherCodeData(77, "Snow grains", "snow"),
        80: WeatherCodeData(80, "Slight rain showers", "rain_showers"),
        81: WeatherCodeData(81, "Moderate rain showers", "rain_showers"),
        82: WeatherCodeData(82, "Violent rain showers", "rain_showers"),
        85: WeatherCodeData(85, "Slight snow showers", "snow_showers"),
        86: WeatherCodeData(86, "Heavy snow showers", "snow_showers"),
        95: WeatherCodeData(95, "Thunderstorm", "thunderstorm"),
        96: WeatherCodeData(96, "Thunderstorm with slight hail", "thunderstorm_hail"),
        99: WeatherCodeData(99, "Thunderstorm with heavy hail", "thunderstorm_hail"),
    }

    @classmethod
    def get_weather_description(cls, code: int) -> str:
        """Get weather description from code."""
        return cls.codes.get(code, WeatherCodeData(code, "Unknown", "unknown")).description

class ValueFormatter:
    """Utility class for formatting values."""
    
    @staticmethod
    def format_value(value: Any, unit: str = "", decimal_places: int = 1) -> str:
        """Format numeric values with units."""
        if value is None or value == "N/A":
            return "N/A"
        try:
            if isinstance(value, (int, float)):
                if value < -100 or value > 1000:  # Unreasonable values
                    return "N/A"
                return f"{float(value):.{decimal_places}f}{unit}"
            return f"{value}{unit}"
        except:
            return "N/A"

    @staticmethod
    def decode_if_bytes(value: Any) -> str:
        """Decode byte strings if necessary."""
        if isinstance(value, bytes):
            return value.decode('utf-8')
        return value

    @staticmethod
    def convert_temperature(value: float, to_unit: WeatherUnits) -> float:
        """Convert temperature between Celsius and Fahrenheit."""
        if to_unit == WeatherUnits.FAHRENHEIT:
            return (value * 9/5) + 32
        return value

    @staticmethod
    def convert_wind_speed(value: float, to_unit: WeatherUnits) -> float:
        """Convert wind speed between different units."""
        # Base unit is km/h
        conversions = {
            WeatherUnits.MS: lambda x: x / 3.6,
            WeatherUnits.MPH: lambda x: x / 1.609344,
            WeatherUnits.KNOTS: lambda x: x / 1.852,
            WeatherUnits.KMH: lambda x: x
        }
        return conversions[to_unit](value)

    @staticmethod
    def convert_precipitation(value: float, to_unit: WeatherUnits) -> float:
        """Convert precipitation between mm and inches."""
        if to_unit == WeatherUnits.INCH:
            return value / 25.4
        return value

# Create console instance
console = Console()

# Define category colors
CATEGORY_STYLES = {
    "LOCATION INFORMATION": {
        "panel": "bright_green",
        "label": "green",
        "value": "bright_white"
    },
    "CURRENT WEATHER CONDITIONS": {
        "panel": "bright_blue",
        "label": "blue",
        "value": "bright_white"
    },
    "HOURLY FORECAST": {
        "panel": "bright_yellow",
        "label": "yellow",
        "value": "bright_white"
    },
    "DAILY FORECAST": {
        "panel": "bright_magenta",
        "label": "magenta",
        "value": "bright_white"
    },
    "PRESSURE LEVELS": {
        "panel": "bright_cyan",
        "label": "cyan",
        "value": "bright_white"
    },
    "AIR QUALITY": {
        "panel": "bright_red",
        "label": "red",
        "value": "bright_white"
    },
    "MARINE CONDITIONS": {
        "panel": "bright_blue",
        "label": "blue3",
        "value": "bright_white"
    }
}

# Default style for any undefined categories
DEFAULT_STYLE = {
    "panel": "bright_white",
    "label": "white",
    "value": "bright_white"
}

@dataclass
class WeatherDisplay:
    """Class to store and format weather display data."""
    sections: Dict[str, List[str]]
    
    def __init__(self):
        self.sections = defaultdict(list)
        self._accumulated_text = ""
    
    def add_line(self, section: str, line: str = "") -> None:
        """Add a line to a section."""
        self.sections[section].append(line)
    
    def add_section(self, section: str, lines: List[str]) -> None:
        """Add multiple lines to a section."""
        self.sections[section].extend(lines)
    
    def _create_rich_panel(self, title: str, content: List[str]) -> Panel:
        """Create a rich panel with formatted content."""
        style = CATEGORY_STYLES.get(title, DEFAULT_STYLE)
        text = Text()
        
        # Style the title
        styled_title = Text(title, style=f"bold {style['panel']}")
        
        for line in content:
            if ":" in line:
                label, value = line.split(":", 1)
                text.append(f"{label}:", style=style["label"])
                text.append(f"{value}\n", style=style["value"])
            else:
                text.append(f"{line}\n", style=style["value"])
                
        return Panel(
            text,
            title=styled_title,
            title_align="left",
            border_style=style["panel"]
        )

    def _format_value_with_condition(self, value: str) -> Text:
        """Format values with conditional coloring."""
        text = Text()
        
        # Temperature formatting
        if "°C" in value:
            temp = float(value.replace("°C", ""))
            if temp > 30:
                text.append(value, style="bright_red")
            elif temp < 0:
                text.append(value, style="bright_blue")
            else:
                text.append(value, style="bright_white")
        
        # Precipitation probability formatting
        elif "%" in value and "precip" in value:
            prob = int(value.split("%")[0])
            if prob > 70:
                text.append(value, style="bright_red")
            elif prob > 30:
                text.append(value, style="bright_yellow")
            else:
                text.append(value, style="bright_green")
        
        # UV Index formatting
        elif "UV Index" in value:
            try:
                uv = float(value.split(": ")[1])
                if uv > 7:
                    text.append(value, style="bright_red")
                elif uv > 4:
                    text.append(value, style="bright_yellow")
                else:
                    text.append(value, style="bright_green")
            except:
                text.append(value, style="bright_white")
        
        # Air Quality formatting
        elif "AQI" in value:
            try:
                aqi = float(value.split(": ")[1])
                if aqi > 150:
                    text.append(value, style="bright_red")
                elif aqi > 100:
                    text.append(value, style="bright_yellow")
                else:
                    text.append(value, style="bright_green")
            except:
                text.append(value, style="bright_white")
        
        # Default formatting
        else:
            text.append(value, style="bright_white")
            
        return text
    
    def get_display(self, return_text: bool = False) -> str:
        """Get the formatted display string with rich formatting."""
        output = []
        self._accumulated_text = ""
        
        # Title banner - Only print once at the start
        if not return_text:  # Only show banner when displaying to console
            console.print(
                Panel(
                    Text("Weather Dashboard", style="bold bright_cyan", justify="center"),
                    border_style="bright_cyan",
                    padding=(1, 15)
                )
            )
            console.print()
        
        for section, lines in self.sections.items():
            # Create rich panel for each section
            panel = self._create_rich_panel(section, lines)
            
            # Print panel if not returning text
            if not return_text:
                console.print(panel)
                console.print()  # Add spacing between panels
            
            # Accumulate plain text version for return value
            section_text = f"\n{section}\n{'='*50}\n"
            section_text += "\n".join(lines)
            section_text += f"\n{'='*50}\n"
            output.append(section_text)
            self._accumulated_text += section_text
        
        if return_text:
            return self._accumulated_text
        return ""

class OpenMeteoAPI:
    """Enhanced client for Open-Meteo APIs with comprehensive feature support."""
    
    def __init__(self, cache_expire: int = 3600, apikey: Optional[str] = None):
        """Initialize API client with caching and optional API key."""
        self.cache_session = requests_cache.CachedSession('.cache', expire_after=cache_expire)
        self.retry_session = retry(self.cache_session, retries=5, backoff_factor=0.2)
        self.client = openmeteo_requests.Client(session=self.retry_session)
        self.urls = {**API_ENDPOINTS, 'geo_services': GEO_SERVICES}
        self.apikey = apikey
        self.formatter = ValueFormatter()
        self._initialize_pressure_levels()

    def _initialize_pressure_levels(self) -> None:
        """Initialize standard pressure levels with heights."""
        self.pressure_levels = {
            1000: 110,   # height in meters
            975: 320,
            950: 500,
            925: 800,
            900: 1000,
            850: 1500,
            800: 1900,
            700: 3000,
            600: 4200,
            500: 5600,
            400: 7200,
            300: 9200,
            250: 10400,
            200: 11800,
            150: 13500,
            100: 15800
        }

    def get_location_from_ip(self, ip: Optional[str] = None) -> Tuple[float, float]:
        """Get latitude and longitude from IP address."""
        url_suffix = ip if ip else ''
        errors = []

        for service_url in self.urls['geo_services']:
            try:
                response = requests.get(f"{service_url}{url_suffix}", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    
                    if 'lat' in data and 'lon' in data:
                        return float(data['lat']), float(data['lon'])
                    elif 'latitude' in data and 'longitude' in data:
                        return float(data['latitude']), float(data['longitude'])
                    elif 'loc' in data:
                        lat, lon = data['loc'].split(',')
                        return float(lat), float(lon)
            except Exception as e:
                errors.append(f"{service_url}: {str(e)}")
                continue
        
        raise Exception(
            f"Unable to get location from IP. All services failed: {'; '.join(errors)}"
        )

    def _process_response(self, response: Any, variables: List[str], include_minutely: bool = False) -> Dict:
        """Process API response with enhanced support for all data types."""
        if not response:
            raise ValueError("Empty response received from API")

        result = {
            "metadata": {
                "latitude": response.Latitude(),
                "longitude": response.Longitude(),
                "elevation": response.Elevation(),
                "timezone": response.Timezone(),
                "timezone_abbreviation": response.TimezoneAbbreviation(),
                "utc_offset_seconds": response.UtcOffsetSeconds(),
            }
        }
        
        self._process_current_data(response, variables, result)
        self._process_hourly_data(response, variables, result)
        
        if include_minutely and hasattr(response, 'Minutely15'):
            self._process_minutely_data(response, variables, result)
        
        if hasattr(response, 'Daily'):
            self._process_daily_data(response, variables, result)

        # Process pressure level data if available
        if hasattr(response, 'PressureLevels'):
            self._process_pressure_level_data(response.PressureLevels(), result)

        return result

    def _process_current_data(self, response: Any, variables: List[str], result: Dict) -> None:
        """Process current weather data with enhanced variable support."""
        if hasattr(response, 'Current'):
            current = response.Current()
            if current and current.VariablesLength() > 0:
                result["current"] = {}
                for i in range(current.VariablesLength()):
                    try:
                        var = current.Variables(i)
                        value = var.Value()
                        if isinstance(value, (int, float)) and -1000 <= value <= 1000:
                            var_name = variables[i]
                            result["current"][var_name] = value
                            
                            # Add weather code interpretation if applicable
                            if var_name == "weather_code":
                                result["current"]["weather_description"] = \
                                    WMOWeatherCodes.get_weather_description(int(value))
                    except Exception as e:
                        print(f"Warning: Error processing current variable {variables[i]}: {str(e)}")

    def _process_hourly_data(self, response: Any, variables: List[str], result: Dict) -> None:
        """Process hourly forecast data with enhanced variable support."""
        if hasattr(response, 'Hourly'):
            hourly = response.Hourly()
            if hourly and hourly.VariablesLength() > 0:
                try:
                    time_data = pd.date_range(
                        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                        freq=pd.Timedelta(seconds=hourly.Interval()),
                        inclusive="left"
                    )
                    
                    data = {"time": time_data}
                    for i in range(hourly.VariablesLength()):
                        self._process_hourly_variable(hourly, i, variables, time_data, data)
                    
                    result["hourly"] = pd.DataFrame(data)
                except Exception as e:
                    print(f"Warning: Error creating hourly dataframe: {str(e)}")

    def _process_minutely_data(self, response: Any, variables: List[str], result: Dict) -> None:
        """Process 15-minutely forecast data."""
        minutely = response.Minutely15()
        if minutely and minutely.VariablesLength() > 0:
            try:
                time_data = pd.date_range(
                    start=pd.to_datetime(minutely.Time(), unit="s", utc=True),
                    end=pd.to_datetime(minutely.TimeEnd(), unit="s", utc=True),
                    freq="15min",
                    inclusive="left"
                )
                
                data = {"time": time_data}
                for i in range(minutely.VariablesLength()):
                    var = minutely.Variables(i)
                    values = var.ValuesAsNumpy()
                    if len(values) == len(time_data):
                        data[variables[i]] = values
                
                result["minutely_15"] = pd.DataFrame(data)
            except Exception as e:
                print(f"Warning: Error creating minutely dataframe: {str(e)}")

    def _process_daily_data(self, response: Any, variables: List[str], result: Dict) -> None:
        """Process daily aggregated data."""
        daily = response.Daily()
        if daily and daily.VariablesLength() > 0:
            try:
                time_data = pd.date_range(
                    start=pd.to_datetime(daily.Time(), unit="s", utc=True),
                    end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
                    freq="D",
                    inclusive="left"
                )
                
                data = {"time": time_data}
                for i in range(daily.VariablesLength()):
                    var = daily.Variables(i)
                    values = var.ValuesAsNumpy()
                    if len(values) == len(time_data):
                        data[variables[i]] = values
                
                result["daily"] = pd.DataFrame(data)
            except Exception as e:
                print(f"Warning: Error creating daily dataframe: {str(e)}")

    def _process_hourly_variable(self, hourly: Any, index: int, variables: List[str], 
                               time_data: pd.DatetimeIndex, data: Dict) -> None:
        """Process individual hourly variable with enhanced support."""
        try:
            var_data = hourly.Variables(index)
            values = var_data.ValuesAsNumpy()
            if len(values) == len(time_data):
                var_name = variables[index]
                
                if hasattr(var_data, 'EnsembleMember'):
                    member = var_data.EnsembleMember()
                    data[f"{var_name}_member{member}"] = values
                else:
                    data[var_name] = values
                
                # Add weather code interpretations
                if var_name == "weather_code":
                    data[f"{var_name}_description"] = [
                        WMOWeatherCodes.get_weather_description(int(code)) for code in values
                    ]
                
                # Process pressure level variables
                if "_hPa" in var_name:
                    level = int(var_name.split("_")[1].replace("hPa", ""))
                    if level in self.pressure_levels:
                        if "pressure_levels" not in data:
                            data["pressure_levels"] = {}
                        if level not in data["pressure_levels"]:
                            data["pressure_levels"][level] = {"height": self.pressure_levels[level]}
                        base_var = var_name.split("_")[0]
                        data["pressure_levels"][level][base_var] = values
                        
        except Exception as e:
            print(f"Warning: Error processing hourly variable {variables[index]}: {str(e)}")
    
    def _process_weather_responses(self, responses: List[Any], params: Dict) -> List[Dict]:
        """Process weather API responses with enhanced variable support."""
        results = []
        variables = []
        
        # Collect all requested variables
        for param in ['current', 'hourly', 'daily']:
            if param in params:
                variables.extend(params[param] if isinstance(params[param], list) else [params[param]])
        
        include_minutely = bool(params.get('forecast_minutely_15') or params.get('past_minutely_15'))
        
        for response in responses:
            try:
                result = self._process_response(response, variables, include_minutely)
                results.append(result)
            except Exception as e:
                print(f"Warning: Error processing response: {str(e)}")
                continue

        if not results:
            raise ValueError("No valid weather data could be processed")
        
        return results

    def _determine_api_endpoint(self, kwargs: Dict) -> str:
        """Determine which API endpoint to use based on parameters."""
        if 'url' in kwargs:
            return self.urls[kwargs['url']]
        elif kwargs.get('models'):
            return self.urls['ensemble']
        elif any(key in kwargs for key in ['wave_height', 'wave_direction', 'wave_period']):
            return self.urls['marine']
        elif any(key in kwargs for key in ['pm10', 'pm2_5', 'aqi', 'pollen']):
            return self.urls['air_quality']
        return self.urls['weather']

    def _prepare_weather_params(self, kwargs: Dict) -> Dict:
        """Prepare comprehensive parameters for weather API request."""
        # Handle location
        latitude = kwargs.get('latitude')
        longitude = kwargs.get('longitude')
        ip = kwargs.get('ip')

        if latitude is None or longitude is None:
            if ip:
                lat, lon = self.get_location_from_ip(ip)
                latitude, longitude = [lat], [lon]
            else:
                raise ValueError("Either latitude/longitude or IP address must be provided")

        if isinstance(latitude, (int, float)):
            latitude = [latitude]
            longitude = [longitude]

        # Validate coordinates
        for lat, lon in zip(latitude, longitude):
            if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                raise ValueError(f"Invalid coordinates: {lat}, {lon}")

        # Base parameters
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "timezone": kwargs.get('timezone', "auto"),
        }

        # Optional parameters
        optional_params = [
            'hourly', 'daily', 'current', 'models', 'cell_selection',
            'temperature_unit', 'wind_speed_unit', 'precipitation_unit',
            'timeformat', 'past_days', 'forecast_days', 'forecast_hours',
            'past_hours', 'start_date', 'end_date', 'start_hour', 'end_hour',
            'domains', 'length_unit'
        ]
        
        for param in optional_params:
            if param in kwargs:
                params[param] = kwargs[param]

        # Handle forecast days limit based on API endpoint
        if 'forecast_days' in params:
            endpoint = self._determine_api_endpoint(kwargs)
            if endpoint == self.urls['marine']:
                params['forecast_days'] = min(params['forecast_days'], 8)
            elif endpoint == self.urls['air_quality']:
                params['forecast_days'] = min(params['forecast_days'], 7)
            else:
                params['forecast_days'] = min(params['forecast_days'], 16)

        # Solar radiation parameters
        if kwargs.get('solar'):
            radiation_vars = [
                "shortwave_radiation", "direct_radiation",
                "direct_normal_irradiance", "diffuse_radiation",
                "global_tilted_irradiance", "global_tilted_irradiance_instant"
            ]
            if 'hourly' in params:
                params['hourly'] = list(set(params['hourly'] + radiation_vars))
            else:
                params['hourly'] = radiation_vars

            if 'tilt' in kwargs:
                params['tilt'] = kwargs['tilt']
            if 'azimuth' in kwargs:
                params['azimuth'] = kwargs['azimuth']

        # Pressure level parameters
        if 'pressure_levels' in kwargs:
            levels = [level for level in kwargs['pressure_levels'] 
                     if level in self.pressure_levels]
            if levels:
                level_vars = []
                for level in levels:
                    for var in ["temperature", "relative_humidity", "wind_speed", "wind_direction"]:
                        level_vars.append(f"{var}_{level}hPa")
                if 'hourly' in params:
                    params['hourly'] = list(set(params['hourly'] + level_vars))
                else:
                    params['hourly'] = level_vars

        # 15-minutely data parameters
        if kwargs.get('forecast_minutely_15'):
            params['forecast_minutely_15'] = kwargs['forecast_minutely_15']
        if kwargs.get('past_minutely_15'):
            params['past_minutely_15'] = kwargs['past_minutely_15']

        # API key if provided
        if self.apikey:
            params['apikey'] = self.apikey

        return params

    def get_weather(self, **kwargs) -> Union[Dict, List[Dict]]:
        """
        Fetch comprehensive weather forecast data with enhanced features.
        
        Parameters:
        - latitude, longitude: float (required unless 'ip' is provided)
        - ip: str (optional) - IP address to get location from
        - hourly: List[str] - hourly variables to fetch
        - daily: List[str] - daily variables to fetch
        - current: List[str] - current condition variables
        - models: List[str] - specific weather models to use
        - cell_selection: str - land/sea/nearest cell selection
        - temperature_unit: str - celsius/fahrenheit
        - wind_speed_unit: str - kmh/ms/mph/knots
        - precipitation_unit: str - mm/inch
        - timeformat: str - iso8601/unixtime
        - timezone: str - timezone name or "auto"
        - past_days: int - number of past days (0-92)
        - forecast_days: int - number of forecast days (0-16)
        - forecast_hours: int - number of forecast hours
        - forecast_minutely_15: bool - include 15-minute forecasts
        - past_minutely_15: bool - include past 15-minute data
        - start_date, end_date: str - date range (YYYY-MM-DD)
        - start_hour, end_hour: str - hour range (YYYY-MM-DDTHH:MM)
        - tilt: float - solar panel tilt for radiation calculations
        - azimuth: float - solar panel azimuth for radiation calculations
        - pressure_levels: List[int] - pressure levels to include
        - solar: bool - include solar radiation data
        """
        try:
            params = self._prepare_weather_params(kwargs)
            url = self._determine_api_endpoint(kwargs)
            
            responses = self.client.weather_api(url, params=params)
            if not responses:
                raise ValueError("No response received from weather API")

            results = self._process_weather_responses(responses, params)
            return results[0] if len(results) == 1 else results

        except Exception as e:
            raise Exception(f"Error fetching weather data: {str(e)}")

    def get_air_quality(self, **kwargs) -> Union[Dict, List[Dict]]:
        """
        Fetch air quality data with enhanced pollutant and pollen support.
        
        Additional parameters specific to air quality:
        - domains: str - CAMS domain selection (auto/cams_europe/cams_global)
        - include_pollen: bool - include pollen data where available
        """
        kwargs['domains'] = kwargs.get('domains', 'auto')
        if kwargs.get('include_pollen'):
            pollen_vars = [
                'alder_pollen', 'birch_pollen', 'grass_pollen',
                'mugwort_pollen', 'olive_pollen', 'ragweed_pollen'
            ]
            kwargs['hourly'] = list(set(kwargs.get('hourly', []) + pollen_vars))
        
        return self.get_weather(**kwargs)

    def get_marine_weather(self, **kwargs) -> Union[Dict, List[Dict]]:
        """
        Fetch marine weather data with enhanced wave and current support.
        
        Additional parameters specific to marine weather:
        - length_unit: str - metric/imperial unit selection
        """
        marine_vars = [
            'wave_height', 'wind_wave_height', 'swell_wave_height',
            'wave_direction', 'wind_wave_direction', 'swell_wave_direction',
            'wave_period', 'wind_wave_period', 'swell_wave_period',
            'ocean_current_speed', 'ocean_current_direction'
        ]
        
        if 'hourly' in kwargs:
            kwargs['hourly'] = list(set(kwargs['hourly'] + marine_vars))
        else:
            kwargs['hourly'] = marine_vars
            
        return self.get_weather(**kwargs)

    def get_climate_data(self, **kwargs) -> Union[Dict, List[Dict]]:
        """Get historical climate statistics."""
        kwargs['url'] = 'climate'
        return self.get_weather(**kwargs)
    
class WeatherService:
    """Enhanced service for processing weather data and creating comprehensive displays."""
    
    def __init__(self, apikey: Optional[str] = None):
        self.api = OpenMeteoAPI(apikey=apikey)
        self.formatter = ValueFormatter()
        self.console = Console()

    def get_weather_dashboard(self, verbose: bool = False, **kwargs) -> str:
        """Get comprehensive weather information including air quality and marine data."""
        display = WeatherDisplay()

        try:
            # If no coordinates provided, get them from IP
            if 'latitude' not in kwargs and 'longitude' not in kwargs:
                try:
                    lat, lon = self.api.get_location_from_ip()
                    kwargs['latitude'] = lat
                    kwargs['longitude'] = lon
                except Exception as e:
                    raise Exception(f"Could not determine location from IP: {str(e)}")

            # Get weather data
            response = self._get_weather_data(**kwargs)
            
            # Display all sections
            self._display_location_info(response, display)
            self._display_current_conditions(response, display)
            
            if hasattr(response, 'Hourly'):
                self._display_hourly_forecast(response.Hourly(), display)
            
            if hasattr(response, 'Daily'):
                self._display_daily_forecast(response.Daily(), display)
            
            # Create metadata dict from response
            metadata = {
                'latitude': response.Latitude(),
                'longitude': response.Longitude(),
                'elevation': response.Elevation()
            }
            
            # Air quality info uses separate API call
            self._display_air_quality_info(metadata, display)

            # Display marine info if coastal location
            if self._is_coastal_location(metadata):
                self._display_marine_info(metadata, display)

            # Get the display text - only print to console if verbose is True
            display_text = display.get_display(return_text=not verbose)
            
            return display_text
            
        except Exception as e:
            error_text = f"Error: {str(e)}"
            if verbose:
                self.console.print(f"[bright_red]{error_text}[/bright_red]")
            return error_text
    
    def _get_weather_data(self, **kwargs) -> Any:
        """Fetch weather data from API."""
        response = self.api.client.weather_api(
            self.api.urls['weather'],
            params={
                "latitude": kwargs.get('latitude'),
                "longitude": kwargs.get('longitude'),
                "timezone": kwargs.get('timezone', 'auto'),
                "current": [
                    "temperature_2m",
                    "relative_humidity_2m",
                    "apparent_temperature",
                    "precipitation",
                    "weather_code",
                    "cloud_cover",
                    "pressure_msl",
                    "wind_speed_10m",
                    "wind_direction_10m",
                    "uv_index"
                ],
                "hourly": [
                    "temperature_2m",
                    "precipitation_probability",
                    "weather_code"
                ],
                "daily": [
                    "temperature_2m_max",
                    "temperature_2m_min",
                    "precipitation_sum",
                    "precipitation_probability_max"
                ]
            }
        )
        if not response:
            raise ValueError("No response received from weather API")
            
        return response[0]  # Get first response
    
    def _is_coastal_location(self, metadata: Dict) -> bool:
        """Determine if location is near coast for marine data relevance."""
        try:
            marine_data = self.api.get_marine_weather(
                latitude=metadata['latitude'],
                longitude=metadata['longitude'],
                hourly=["wave_height"],
                forecast_days=1
            )
            return 'hourly' in marine_data and not marine_data['hourly'].empty
        except:
            return False

    def _display_location_info(self, response: Any, display: WeatherDisplay) -> None:
        """Display location information."""
        display.add_line("LOCATION INFORMATION", 
                        f"Coordinates: {response.Latitude():.4f}°N, {response.Longitude():.4f}°E")
        display.add_line("LOCATION INFORMATION",
                        f"Elevation: {response.Elevation():.1f}m above sea level")
        
        timezone = self.formatter.decode_if_bytes(response.Timezone())
        tz_abbr = self.formatter.decode_if_bytes(response.TimezoneAbbreviation())
        display.add_line("LOCATION INFORMATION", 
                        f"Timezone: {timezone} ({tz_abbr})")
            
    def _display_weather_info(self, weather: Dict, display: WeatherDisplay) -> None:
        """Display comprehensive weather information."""
        if "current" in weather and weather["current"]:
            self._display_current_conditions(weather["current"], display)

        if "hourly" in weather and not weather["hourly"].empty:
            self._display_hourly_forecast(weather["hourly"], display)
            
        if "daily" in weather and not weather["daily"].empty:
            self._display_daily_forecast(weather["daily"], display)

    def _display_current_conditions(self, response: Any, display: WeatherDisplay) -> None:
        """Display current weather conditions."""
        display.add_line("CURRENT WEATHER CONDITIONS", "\nCurrent conditions:")
        
        if not hasattr(response, 'Current'):
            display.add_line("CURRENT WEATHER CONDITIONS", "No current weather data available")
            return
            
        current = response.Current()
        if not current:
            display.add_line("CURRENT WEATHER CONDITIONS", "No current weather data available")
            return

        variables = {}
        for i in range(current.VariablesLength()):
            var = current.Variables(i)
            try:
                value = var.Value()
                if isinstance(value, (int, float)) and -1000 <= value <= 1000:
                    variables[i] = value
            except:
                continue

        # Temperature information
        if 0 in variables:  # temperature_2m
            display.add_line("CURRENT WEATHER CONDITIONS",
                           f"Temperature: {self.formatter.format_value(variables[0], '°C')}")
        if 2 in variables:  # apparent_temperature
            display.add_line("CURRENT WEATHER CONDITIONS",
                           f"Feels like: {self.formatter.format_value(variables[2], '°C')}")
        
        # Humidity
        if 1 in variables:  # relative_humidity_2m
            display.add_line("CURRENT WEATHER CONDITIONS",
                           f"Humidity: {self.formatter.format_value(variables[1], '%')}")
        
        # Wind conditions
        if 7 in variables and 8 in variables:  # wind_speed_10m and wind_direction_10m
            display.add_line("CURRENT WEATHER CONDITIONS",
                           f"Wind: {self.formatter.format_value(variables[7], ' km/h')} "
                           f"from {self.formatter.format_value(variables[8], '°', 0)}")
        
        # Cloud cover and UV index
        if 5 in variables:  # cloud_cover
            display.add_line("CURRENT WEATHER CONDITIONS",
                           f"Cloud Cover: {self.formatter.format_value(variables[5], '%')}")
        if 9 in variables:  # uv_index
            display.add_line("CURRENT WEATHER CONDITIONS",
                           f"UV Index: {self.formatter.format_value(variables[9], '')}")
        
        # Precipitation
        if 3 in variables:  # precipitation
            display.add_line("CURRENT WEATHER CONDITIONS",
                           f"Precipitation: {self.formatter.format_value(variables[3], ' mm/h')}")
            
        # Weather code interpretation
        if 4 in variables:  # weather_code
            description = WMOWeatherCodes.get_weather_description(int(variables[4]))
            display.add_line("CURRENT WEATHER CONDITIONS", f"Conditions: {description}")

    def _display_hourly_forecast(self, hourly: Any, display: WeatherDisplay) -> None:
        """Display enhanced hourly forecast."""
        display.add_line("HOURLY FORECAST", "\nNext 24 hours:")
        
        # Process hourly data directly from response
        hourly_time = pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        )

        variables = []
        for i in range(hourly.VariablesLength()):
            var = hourly.Variables(i)
            values = var.ValuesAsNumpy()
            variables.append(values)

        # Display next 24 hours of forecasts
        for i in range(min(24, len(hourly_time))):
            time = hourly_time[i].strftime('%H:%M')
            conditions = []

            # Temperature
            if len(variables) > 0:  # temperature_2m
                temp = variables[0][i]
                conditions.append(f"{self.formatter.format_value(temp, '°C')}")
            
            # Precipitation probability
            if len(variables) > 1:  # precipitation_probability
                prob = variables[1][i]
                if prob > 10:
                    conditions.append(f"{int(prob)}% precip")
            
            # Weather code
            if len(variables) > 2:  # weather_code
                code = int(variables[2][i])
                description = WMOWeatherCodes.get_weather_description(code)
                conditions.append(description)
            
            line = f"{time}: {', '.join(conditions)}" if conditions else f"{time}: No data"
            display.add_line("HOURLY FORECAST", line)

    def _display_daily_forecast(self, daily: Any, display: WeatherDisplay) -> None:
        """Display comprehensive daily forecast."""
        display.add_line("DAILY FORECAST", "\n7-day forecast:")
        
        # Process daily data directly from response
        daily_time = pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
            freq="D",
            inclusive="left"
        )

        variables = []
        for i in range(daily.VariablesLength()):
            var = daily.Variables(i)
            values = var.ValuesAsNumpy()
            variables.append(values)

        # Display up to 7 days of forecasts
        for i in range(min(7, len(daily_time))):
            date = daily_time[i].strftime('%Y-%m-%d')
            conditions = []

            # Temperature max/min
            if len(variables) >= 2:  # temperature_2m_max and temperature_2m_min
                temp_max = variables[0][i]
                temp_min = variables[1][i]
                conditions.append(f"{self.formatter.format_value(temp_min, '°C')} to {self.formatter.format_value(temp_max, '°C')}")
            
            # Precipitation sum
            if len(variables) >= 3:  # precipitation_sum
                precip = variables[2][i]
                if precip > 0:
                    conditions.append(f"{self.formatter.format_value(precip, 'mm')} precip")
            
            # Precipitation probability
            if len(variables) >= 4:  # precipitation_probability_max
                prob = variables[3][i]
                if prob > 20:
                    conditions.append(f"{int(prob)}% chance of rain")

            line = f"{date}: {', '.join(conditions)}" if conditions else f"{date}: No data"
            display.add_line("DAILY FORECAST", line)

    def _display_pressure_levels(self, response: Dict, display: WeatherDisplay) -> None:
        """Display pressure level information."""
        if 'pressure_levels' not in response:
            return
            
        display.add_line("PRESSURE LEVELS", "\nPressure Level Data:")
        
        for pressure, data in sorted(response['pressure_levels'].items()):
            display.add_line("PRESSURE LEVELS", 
                           f"\n{pressure} hPa (altitude: {data['height']}m):")
            
            for var_name, value in data.items():
                if var_name != 'height':
                    unit = ''
                    if 'temperature' in var_name:
                        unit = '°C'
                    elif 'humidity' in var_name:
                        unit = '%'
                    elif 'speed' in var_name:
                        unit = ' km/h'
                    elif 'direction' in var_name:
                        unit = '°'
                    
                    display.add_line("PRESSURE LEVELS", 
                                   f"  {var_name}: {self.formatter.format_value(value, unit)}")
    
    def _display_air_quality_info(self, metadata: Dict, display: WeatherDisplay) -> None:
        """Display comprehensive air quality information."""
        try:
            response = self.api.client.weather_api(
                self.api.urls['air_quality'],
                params={
                    "latitude": metadata['latitude'],
                    "longitude": metadata['longitude'],
                    "current": [
                        "pm10",
                        "pm2_5",
                        "carbon_monoxide",
                        "nitrogen_dioxide",
                        "sulphur_dioxide",
                        "ozone",
                        "aerosol_optical_depth",
                        "dust",
                        "european_aqi",
                        "us_aqi"
                    ]
                }
            )

            if not response:
                display.add_line("AIR QUALITY", "Air quality data not available")
                return

            response = response[0]
            current = response.Current()
            if not current:
                display.add_line("AIR QUALITY", "No current air quality data available")
                return

            display.add_line("AIR QUALITY", f"Air quality location: {response.Latitude():.4f}°N, {response.Longitude():.4f}°E")

            # Process variables
            variables = {}
            for i in range(current.VariablesLength()):
                var = current.Variables(i)
                try:
                    value = var.Value()
                    if -1000 <= value <= 1000:
                        variables[i] = value
                except:
                    continue

            # Display AQI indices
            display.add_line("AIR QUALITY", "\nAir Quality Index:")
            
            # European AQI
            eu_aqi = variables.get(8)
            if eu_aqi is not None:
                display.add_line("AIR QUALITY", f"European AQI: {eu_aqi:.1f}")
                status = self._get_eu_aqi_status(eu_aqi)
                display.add_line("AIR QUALITY", f"Status: {status}")

            # US AQI
            us_aqi = variables.get(9)
            if us_aqi is not None:
                display.add_line("AIR QUALITY", f"\nUS AQI: {us_aqi:.1f}")
                status = self._get_us_aqi_status(us_aqi)
                display.add_line("AIR QUALITY", f"Status: {status}")

            # Display pollutant levels
            display.add_line("AIR QUALITY", "\nPollutant levels:")
            pollutants = [
                ("PM2.5", variables.get(1)),
                ("PM10", variables.get(0)),
                ("Ozone", variables.get(5)),
                ("NO₂", variables.get(3)),
                ("SO₂", variables.get(4)),
                ("CO", variables.get(2))
            ]

            for name, value in pollutants:
                if value is not None:
                    display.add_line("AIR QUALITY", f"{name}: {value:.1f} μg/m³")

            # Additional measurements
            dust = variables.get(7)
            if dust is not None:
                display.add_line("AIR QUALITY", f"Dust concentration: {dust:.1f} μg/m³")

            aod = variables.get(6)
            if aod is not None:
                display.add_line("AIR QUALITY", f"Aerosol optical depth: {aod:.1f}")

        except Exception as e:
            display.add_line("AIR QUALITY", f"Error fetching air quality data: {str(e)}")
    
    def _display_marine_info(self, metadata: Dict, display: WeatherDisplay) -> None:
        """Display comprehensive marine weather information."""
        try:
            marine_data = self.api.get_marine_weather(
                latitude=metadata['latitude'],
                longitude=metadata['longitude'],
                hourly=[
                    "wave_height", "wave_direction", "wave_period",
                    "wind_wave_height", "wind_wave_direction", "wind_wave_period",
                    "swell_wave_height", "swell_wave_direction", "swell_wave_period",
                    "ocean_current_speed", "ocean_current_direction"
                ]
            )
            
            if 'hourly' not in marine_data or marine_data['hourly'].empty:
                display.add_line("MARINE CONDITIONS", "Marine data not available for this location")
                return
                
            display.add_line("MARINE CONDITIONS", "\nCurrent marine conditions:")
            
            current_hour = marine_data['hourly'].iloc[0]
            
            # Wave conditions
            if 'wave_height' in current_hour:
                display.add_line("MARINE CONDITIONS",
                               f"Wave height: {self.formatter.format_value(current_hour['wave_height'], 'm')}")
            
            if 'wave_period' in current_hour:
                display.add_line("MARINE CONDITIONS",
                               f"Wave period: {self.formatter.format_value(current_hour['wave_period'], 's')}")
            
            # Swell conditions
            if 'swell_wave_height' in current_hour:
                display.add_line("MARINE CONDITIONS",
                               f"Swell height: {self.formatter.format_value(current_hour['swell_wave_height'], 'm')}")
            
            # Ocean currents
            if 'ocean_current_speed' in current_hour:
                display.add_line("MARINE CONDITIONS",
                               f"Current speed: {self.formatter.format_value(current_hour['ocean_current_speed'], ' km/h')}")

        except Exception as e:
            display.add_line("MARINE CONDITIONS", f"Error fetching marine data: {str(e)}")

    def _get_eu_aqi_status(self, aqi: float) -> str:
        """Get European AQI status description."""
        if 0 <= aqi <= 20:
            return "Good"
        elif aqi <= 40:
            return "Fair"
        elif aqi <= 60:
            return "Moderate"
        elif aqi <= 80:
            return "Poor"
        elif aqi <= 100:
            return "Very Poor"
        return "Extremely Poor"

    def _get_us_aqi_status(self, aqi: float) -> str:
        """Get US AQI status description."""
        if 0 <= aqi <= 50:
            return "Good"
        elif aqi <= 100:
            return "Moderate"
        elif aqi <= 150:
            return "Unhealthy for Sensitive Groups"
        elif aqi <= 200:
            return "Unhealthy"
        elif aqi <= 300:
            return "Very Unhealthy"
        return "Hazardous"

def process_weather_query(**kwargs):
    service = WeatherService()
    weather_info = service.get_weather_dashboard(
        solar=True,                 # Include solar radiation data
        pressure_levels=[850, 500], # Include pressure level data
        include_pollen=True         # Include pollen data where available
    )
    
    # The weather_info variable now contains the accumulated text
    return weather_info

def main():
    """Main function to run the weather dashboard."""
    try:
        service = WeatherService()
        verbose = False
        # Example usage with all features
        weather_info = service.get_weather_dashboard(
            verbose=False,
            solar=True,                # Include solar radiation data
            pressure_levels=[850, 500], # Include pressure level data
            include_pollen=True        # Include pollen data where available
        )
        if not verbose: print(weather_info)
        
        # The weather_info variable now contains the accumulated text
        return weather_info
    except Exception as e:
        console.print(f"[bright_red]Fatal Error: {str(e)}[/bright_red]")
        return str(e)

if __name__ == "__main__":
    main()

service = WeatherService()