# Weather Application with Photovoltaic Energy Forecast

## Project Description

The application displays a 7-day weather forecast using the external API [Open-Meteo](https://open-meteo.com). Additionally, it calculates the estimated energy production from a photovoltaic installation based on the provided weather data.

Integrated React frontend is available [here](https://github.com/spirteque/weather_frontend.git).

The application is publicly accessible. Visit: [weather.spirteque.com](www.weather.spirteque.com).

## Features

### Endpoint 1: `/api/v1/week_forecast` - 7-Day Weather Forecast

- **Parameters**: geographic latitude (`latitude`), geographic longitude (`longitude`).
- **Returns**:
  - Data in JSON format, mapped from the `WeatherForecast` model, which includes:
    - Forecast dates.
    - Weather codes for each day.
    - Minimum and maximum daily temperatures.
    - Estimated energy production (kWh).
  - Additional information, such as units, panel efficiency, and photovoltaic installation power.

### Endpoint 2: `/api/v1/week_summary` - Weather Summary for the Upcoming Week

- **Returns**:
  - Data in JSON format, mapped from the `WeatherWeekSummary` model, which includes:
    - Average atmospheric pressure.
    - Average sun exposure duration.
    - Extreme temperatures of the week.
    - Weekly summary (e.g., with rain/without rain).
  - Additional information, such as utilized units.


## Technologies Used

- Python 3.12
- FastAPI 0.115.6
- Pydantic 2.10.3
- All required libraries are listed in the `requirements.txt` file.
- [Open-Meteo API](https://open-meteo.com) - used for fetching weather data.
- Docker (optional) - the repository includes a `Dockerfile` for the backend application.


## Installation and Launch

1. **Clone the repository**:
   ```bash
   git clone https://github.com/spirteque/weather_backend.git
   cd weather_backend

2. **Set up a virtual environment**:  
   Create and activate a virtual environment for the project:

   - On Unix/macOS:
   ```bash
   python3 -m venv ./venv
   source venv/bin/activate
    ```
   - On Windows:
   ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

3. **Install dependencies**:  
   Install the required packages in a virtual environment:
   ```bash
   pip install -r requirements.txt


4. **Environment variable configuration**:  

   The repository includes a `.env` file containing all the necessary environment variables.


5. **Start the server**:
   ```bash
   uvicorn app.main:app --reload

## Example Usage
### Endpoint 1: api/v1/week_forecast
Request:
```bash
GET api/v1/week_forecast?latitude=51&longitude=16
```

Response:
```bash
{
  "latitude": 51,
  "longitude": 15.999998,
  "time_unit": "iso8601",
  "weather_code_unit": "wmo code",
  "temp_max_unit": "°C",
  "temp_min_unit": "°C",
  "sunshine_duration_unit": "s",
  "generated_energy_unit": "kWh",
  "installation_power_unit": "kW",
  "installation_power": 2.5,
  "installation_efficiency": 0.2,
  "days": [
    {
      "time": "2024-12-09",
      "day": "MONDAY",
      "weather_code": 77,
      "weather_type": "SNOW_GRAINS",
      "temp_max": 1.5,
      "temp_min": -0.5,
      "sunshine_duration": 0,
      "generated_energy": 0
    },
    {
      "time": "2024-12-10",
      "day": "TUESDAY",
      "weather_code": 71,
      "weather_type": "SNOW",
      "temp_max": 0.2,
      "temp_min": -0.9,
      "sunshine_duration": 0,
      "generated_energy": 0
    },
    {
      "time": "2024-12-11",
      "day": "WEDNESDAY",
      "weather_code": 56,
      "weather_type": "FREEZING_DRIZZLE",
      "temp_max": -0.2,
      "temp_min": -0.9,
      "sunshine_duration": 0,
      "generated_energy": 0
    },
    {
      "time": "2024-12-12",
      "day": "THURSDAY",
      "weather_code": 3,
      "weather_type": "CLOUDY",
      "temp_max": -0.4,
      "temp_min": -1.6,
      "sunshine_duration": 1510.42,
      "generated_energy": 0.2098
    },
    {
      "time": "2024-12-13",
      "day": "FRIDAY",
      "weather_code": 2,
      "weather_type": "CLOUDY",
      "temp_max": 0.8,
      "temp_min": -2.5,
      "sunshine_duration": 23568.19,
      "generated_energy": 3.2734
    },
    {
      "time": "2024-12-14",
      "day": "SATURDAY",
      "weather_code": 71,
      "weather_type": "SNOW",
      "temp_max": 1,
      "temp_min": -1.4,
      "sunshine_duration": 16434.82,
      "generated_energy": 2.2826
    },
    {
      "time": "2024-12-15",
      "day": "SUNDAY",
      "weather_code": 71,
      "weather_type": "SNOW",
      "temp_max": 2.9,
      "temp_min": 0.2,
      "sunshine_duration": 14710.31,
      "generated_energy": 2.0431
    }
  ]
}
```
### Endpoint 2: /api/v1/week_summary
Request:
    ```bash
    GET /api/v1/week_summary?latitude=51&longitude=16
    ```

Response:
```bash
{
  "latitude": 51,
  "longitude": 15.999998,
  "hourly_time_unit": "iso8601",
  "pressure_msl_unit": "hPa",
  "daily_time_unit": "iso8601",
  "weather_code_unit": "wmo code",
  "temp_max_unit": "°C",
  "temp_min_unit": "°C",
  "sunshine_duration_unit": "s",
  "mean_pressure": 1026.5,
  "mean_sunshine_duration": 8031.96,
  "temp_max_week": 2.9,
  "temp_min_week": -2.5,
  "weather_types": [
    "SNOW"
  ]
}
```

## Tests
Run unit tests:
```bash
pytest
```

