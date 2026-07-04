import tkinter as tk
from weather_api import get_weather
from PIL import Image, ImageTk
from icon_manager import download_icon
from weather_api import get_forecast

# ==============================
# Search Weather Function
# ==============================
def search_weather():

    city = city_entry.get().strip()

    if city == "":
        city_result.config(text="❌ Please enter a city!")
        temp_result.config(text="")
        weather_result.config(text="")
        humidity_result.config(text="")
        wind_result.config(text="")
        pressure_result.config(text="")
        return

    weather = get_weather(city)

    if weather:
        city_result.config(text=f"📍 {weather['name']}")
        icon_code = weather["weather"][0]["icon"]
        print("Icon Code:", icon_code)

        icon_path = download_icon(icon_code)

        image = Image.open(icon_path)
        image = image.resize((100, 100))

        icon = ImageTk.PhotoImage(image)

        icon_label.config(image=icon)
        icon_label.image = icon
        temp_result.config(text=f"🌡 Temperature : {weather['main']['temp']} °C")
        weather_result.config(text=f"☁ Weather : {weather['weather'][0]['description'].title()}")
        humidity_result.config(text=f"💧 Humidity : {weather['main']['humidity']} %")
        wind_result.config(text=f"🌬 Wind Speed : {weather['wind']['speed']} m/s")
        pressure_result.config(text=f"🌍 Pressure : {weather['main']['pressure']} hPa")

    else:
        city_result.config(text="❌ City not found!")
        temp_result.config(text="")
        weather_result.config(text="")
        humidity_result.config(text="")
        wind_result.config(text="")
        pressure_result.config(text="")

def show_forecast():
     city = city_entry.get().strip()
     data = get_forecast(city)

     if not data:
        city_result.configure(text="❌ Forecast not available")
        return

     forecast_text = ""

     for i in range(0, len(data["list"]), 8):  # every 24 hours
        day = data["list"][i]
        temp = day["main"]["temp"]
        desc = day["weather"][0]["description"]

        forecast_text += f"{temp}°C | {desc}\n"

        city_result.configure(text=f"📅 5-Day Forecast\n\n{forecast_text}")
# ==============================
# Main Window
# ==============================
root = tk.Tk()
root.title("Weather Forecast App")
root.geometry("900x700")
root.configure(bg="#87CEEB")
root.resizable(False, False)

# ==============================
# Header
# ==============================
title = tk.Label(
    root,
    text="🌦 Weather Forecast",
    font=("Arial", 22, "bold"),
    bg="#87CEEB",
    fg="navy"
)
title.pack(pady=20)

# ==============================
# Search Section
# ==============================
search_frame = tk.Frame(root, bg="#87CEEB")
search_frame.pack()

city_label = tk.Label(
    search_frame,
    text="Enter City",
    font=("Arial", 12),
    bg="#87CEEB"
)
city_label.pack()

city_entry = tk.Entry(
    search_frame,
    font=("Arial", 14),
    width=25
)
city_entry.pack(pady=10)

search_button = tk.Button(
    search_frame,
    text="🔍 Search",
    font=("Arial", 12, "bold"),
    bg="#1E90FF",
    fg="white",
    padx=15,
    pady=5,
    command=search_weather
)
search_button.pack(pady=10)

forcast_button = tk.Button(
    search_frame,
    text="🔍 5-day forcast",
    font=("Arial", 12, "bold"),
    bg="#1E90FF",
    fg="white",
    padx=15,
    pady=5,
    command=show_forecast
)
forcast_button.pack(pady=10)

# ==============================
# Weather Card
# ==============================
weather_frame = tk.Frame(
    root,
    bg="white",
    bd=3,
    relief="ridge"
)
weather_frame.pack(padx=35, pady=20, fill="both", expand=True)

icon_label = tk.Label(
    weather_frame,
    bg="white"
)

icon_label.pack(pady=10)
city_result = tk.Label(
    weather_frame,
    text="📍 City",
    font=("Arial", 16, "bold"),
    bg="white"
)
city_result.pack(pady=10)

temp_result = tk.Label(
    weather_frame,
    text="🌡 Temperature",
    font=("Arial", 14),
    bg="white"
)
temp_result.pack(pady=5)

weather_result = tk.Label(
    weather_frame,
    text="☁ Weather",
    font=("Arial", 14),
    bg="white"
)
weather_result.pack(pady=5)

humidity_result = tk.Label(
    weather_frame,
    text="💧 Humidity",
    font=("Arial", 14),
    bg="white"
)
humidity_result.pack(pady=5)

wind_result = tk.Label(
    weather_frame,
    text="🌬 Wind Speed",
    font=("Arial", 14),
    bg="white"
)
wind_result.pack(pady=5)

pressure_result = tk.Label(
    weather_frame,
    text="🌍 Pressure",
    font=("Arial", 14),
    bg="white"
)
pressure_result.pack(pady=5)

# ==============================
# Footer
# ==============================
footer = tk.Label(
    root,
    text="Developed using Python & OpenWeather API",
    font=("Arial", 10),
    bg="#87CEEB",
    fg="black"
)
footer.pack(pady=10)

# ==============================
# Run App
# ==============================
root.mainloop()