import requests
import json
import os

# Constants
API_KEY = "bd5e378503939ddaee76f12ad7a97608"  # Replace with your API key
LINE_WIDTH = 50
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

# Function to get weather data from the API
def get_weather(city, units="metric"):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': API_KEY,
        'units': units,
        'lang': 'en'  # Language set to English
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        
        if response.status_code == 200:
            return data
        else:
            print(f"\n{RED}Error: {data.get('message', 'Unable to fetch data')}{RESET}")
            return None
    except Exception as e:
        print(f"\n{RED}Failed to retrieve weather data: {e}{RESET}")
        return None

# Function to get weather forecast data from the API
def get_forecast(city, units="metric"):
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        'q': city,
        'appid': API_KEY,
        'units': units,
        'lang': 'en',  # Language set to English
        'cnt': 5  # Get data for 5 periods
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        
        if response.status_code == 200:
            return data
        else:
            print(f"\n{RED}Error: {data.get('message', 'Unable to fetch data')}{RESET}")
            return None
    except Exception as e:
        print(f"\n{RED}Failed to retrieve weather forecast data: {e}{RESET}")
        return None

# Function to display weather data
def display_weather(data, units):
    main = data['main']
    weather = data['weather'][0]
    wind = data['wind']
    
    temp_unit = "°C" if units == "metric" else "°F"
    wind_speed_unit = "m/s" if units == "metric" else "mph"

    print(f"\n{GREEN}{'='*LINE_WIDTH}{RESET}")
    print(f"Weather in {data['name']}, {data['sys']['country']}:")
    print(f"{GREEN}{'='*LINE_WIDTH}{RESET}")
    print(f"Temperature: {main['temp']}{temp_unit}")
    print(f"Feels Like: {main['feels_like']}{temp_unit}")
    print(f"Humidity: {main['humidity']}%")
    print(f"Description: {weather['description'].capitalize()}")
    print(f"Wind Speed: {wind['speed']} {wind_speed_unit}")
    print(f"{GREEN}{'='*LINE_WIDTH}{RESET}\n")

# Function to display weather forecast data
def display_forecast(data, units):
    temp_unit = "°C" if units == "metric" else "°F"
    wind_speed_unit = "m/s" if units == "metric" else "mph"
    
    print(f"\n{GREEN}{'='*LINE_WIDTH}{RESET}")
    print("Weather Forecast:")
    print(f"{GREEN}{'='*LINE_WIDTH}{RESET}")
    for forecast in data['list']:
        date = forecast['dt_txt']
        temp = forecast['main']['temp']
        feels_like = forecast['main']['feels_like']
        description = forecast['weather'][0]['description'].capitalize()
        wind_speed = forecast['wind']['speed']
        humidity = forecast['main']['humidity']
        
        print(f"{date}:")
        print(f"  Temperature: {temp}{temp_unit}, Feels Like: {feels_like}{temp_unit}")
        print(f"  Humidity: {humidity}%, Description: {description}")
        print(f"  Wind Speed: {wind_speed} {wind_speed_unit}")
        print(f"{GREEN}{'-'*LINE_WIDTH}{RESET}\n")

# Function to save search history
def save_history(city, data):
    history_file = "weather_history.json"
    history = []

    if os.path.exists(history_file):
        with open(history_file, 'r') as file:
            history = json.load(file)

    history.append({
        "city": city,
        "data": data
    })

    with open(history_file, 'w') as file:
        json.dump(history, file, indent=4)

# Function to display search history
def display_history():
    history_file = "weather_history.json"
    
    if os.path.exists(history_file):
        with open(history_file, 'r') as file:
            history = json.load(file)
        
        print(f"\n{GREEN}{'='*LINE_WIDTH}{RESET}")
        print("Weather Search History:")
        print(f"{GREEN}{'='*LINE_WIDTH}{RESET}")
        for idx, record in enumerate(history):
            city = record['city']
            temp = record['data']['main']['temp']
            desc = record['data']['weather'][0]['description'].capitalize()
            print(f"{idx + 1}. {city}: {temp}°C, {desc}")
    else:
        print(f"\n{RED}No weather search history found.{RESET}")
    print(f"{GREEN}{'='*LINE_WIDTH}{RESET}\n")

# Main application function
def main():
    cities = ["Jakarta", "Bandung", "Surabaya", "Denpasar", "Lombok"]
    units_choice = {"1": "metric", "2": "imperial"}
    
    while True:
        print(f"\n{GREEN}{'='*LINE_WIDTH}{RESET}")
        print("Welcome to the Weather App")
        print(f"{GREEN}{'='*LINE_WIDTH}{RESET}")
        print("1. Choose Popular City")
        print("2. Enter City Name")
        print("3. Display Search History")
        print("4. Display Weather Forecast")
        print("5. Exit")
        
        choice = input("Choose an option (1/2/3/4/5): ")
        
        if choice == "1":
            print(f"\n{GREEN}{'='*LINE_WIDTH}{RESET}")
            print("Popular Cities:")
            print(f"{GREEN}{'='*LINE_WIDTH}{RESET}")
            for idx, city in enumerate(cities):
                print(f"{idx + 1}. {city}")
            city_choice = int(input("Choose a city (1-5): "))
            city = cities[city_choice - 1]
        
        elif choice == "2":
            city = input("Enter city name: ")
        
        elif choice == "3":
            display_history()
            continue
        
        elif choice == "4":
            print(f"\n{GREEN}{'='*LINE_WIDTH}{RESET}")
            print("Choose temperature unit:")
            print(f"{GREEN}{'='*LINE_WIDTH}{RESET}")
            print("1. Celsius")
            print("2. Fahrenheit")
            units = units_choice.get(input("Choose an option (1/2): "), "metric")
            city = input("Enter city name: ")
            forecast_data = get_forecast(city, units)
            
            if forecast_data:
                display_forecast(forecast_data, units)
            continue
        
        elif choice == "5":
            print(f"\n{GREEN}{'='*LINE_WIDTH}{RESET}")
            print("Thank you for using the Weather App!")
            print(f"{GREEN}{'='*LINE_WIDTH}{RESET}")
            break
        
        else:
            print(f"\n{RED}Invalid choice. Please try again.{RESET}")
            continue

        print(f"\n{GREEN}{'='*LINE_WIDTH}{RESET}")
        print("Choose temperature unit:")
        print(f"{GREEN}{'='*LINE_WIDTH}{RESET}")
        print("1. Celsius")
        print("2. Fahrenheit")
        units = units_choice.get(input("Choose an option (1/2): "), "metric")

        weather_data = get_weather(city, units)
        
        if weather_data:
            display_weather(weather_data, units)
            save_history(city, weather_data)

if __name__ == "__main__":
    main()
