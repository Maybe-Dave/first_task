from fastapi import FastAPI, Request
import requests

app = FastAPI()

GEO_API_URL = "http://ip-api.com/json/"
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
WEATHER_API_KEY = "7d6c07377fc13622df27bab859e1389b"  # Replace with your OpenWeather API key



@app.get("/")
async def home():
    return {"message": "Hello, World!"}

@app.get("/api/hello")
async def hello(request: Request, visitor_name: str):
    # Get client's IP address
    response = requests.get('https://api.ipify.org?format=json')
    ip_address = response.json()['ip']
    
    # Get location based on IP address
    geo_response = requests.get(f"{GEO_API_URL}{ip_address}")
    geo_data = geo_response.json()
    city = geo_data.get("city", "Unknown")
    
    # Get weather data
    weather_response = requests.get(WEATHER_API_URL, params={
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric"  # Use metric units to get temperature in Celsius
    })
    weather_data = weather_response.json()
    temperature = weather_data["main"]["temp"] if "main" in weather_data else "Unknown"

    # Create the response
    response = {
        "client_ip": ip_address,
        "location": city,
        "greeting": f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}"
    }
    return response



