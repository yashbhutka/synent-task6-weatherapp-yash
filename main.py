from weather_api import get_weather

city = input("Enter city name: ")

weather = get_weather(city)

if weather:
    print("\n===== Weather Report =====")
    print("City:", weather["name"])
    print("Temperature:", weather["main"]["temp"], "°C")
    print("Feels Like:", weather["main"]["feels_like"], "°C")
    print("Humidity:", weather["main"]["humidity"], "%")
    print("Pressure:", weather["main"]["pressure"], "hPa")
    print("Weather:", weather["weather"][0]["description"])
    print("Wind Speed:", weather["wind"]["speed"], "m/s")
else:
    print("City not found!")