# Weather Dashboard App
import requests

API_KEY = "dccf07408f449f285a27a856590a8c67"


def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()
    except requests.exceptions.RequestException:
        print("Error: Could not connect to the weather service. Check your internet.")
        return

    # OpenWeatherMap sometimes returns 'cod' as a string ("404") or an int (404)
    if str(data.get("cod")) != "200":
        print(f"Error: {data.get('message', 'City not found.')}")
        return

    # Extracting data safely
    city_name = data["name"]
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    wind = data["wind"]["speed"]
    description = data["weather"][0]["description"]

    # Displaying report
    print("\n===== WEATHER REPORT =====")
    print(f"City: {city_name}")
    print(f"Temperature: {temp}°C")
    print(f"Humidity: {humidity}%")
    print(f"Wind Speed: {wind} m/s")
    print(f"Condition: {description.capitalize()}")


while True:
    city = input("\nEnter city name (or 'exit'): ").strip()

    if not city:
        continue

    if city.lower() == "exit":
        print("Goodbye!")
        break

    get_weather(city)