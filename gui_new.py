import customtkinter as ctk
from weather_api import get_weather
from datetime import datetime
from weather_api import get_forecast
from icon_manager import download_icon
from PIL import Image
import os
from location import get_current_location

# ----------------------------------------
# App Settings
# ----------------------------------------
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# ----------------------------------------
# Search Function
# ----------------------------------------
def search_weather():

    city = city_entry.get().strip()

    if city == "":
        city_name.configure(text="Please enter a city")
        
        
        icon_label.configure(image=None, text="")
        temperature.configure(text="")
        feels_like.configure(text="")
        description.configure(text="")
        humidity.configure(text="")
        wind.configure(text="")
        pressure.configure(text="")
        sunrise.configure(text="")
        sunset.configure(text="")
        return

    weather = get_weather(city)

    if weather:
                # ---------------- Weather Icon ----------------
        icon_code = weather["weather"][0]["icon"]

        icon_path = download_icon(icon_code)

        if os.path.exists(icon_path):

            image = Image.open(icon_path)

            weather_icon = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=(80, 80)
            )

            icon_label.configure(
                image=weather_icon,
                text=""
            )

            icon_label.image = weather_icon

        sunrise_time = datetime.fromtimestamp(
            weather["sys"]["sunrise"]
        ).strftime("%I:%M %p")

        sunset_time = datetime.fromtimestamp(
            weather["sys"]["sunset"]
        ).strftime("%I:%M %p")

        city_name.configure(
            text=f"📍 {weather['name']}"
        )

        temperature.configure(text=f"{round(weather['main']['temp'])}°C")

        feels_like.configure(
            text=f"🤗 Feels Like : {weather['main']['feels_like']} °C"
        )

        description.configure(
            text=f"☁ Weather : {weather['weather'][0]['description'].title()}"
        )

        humidity.configure(
            text=f"💧 Humidity : {weather['main']['humidity']} %"
        )

        wind.configure(
            text=f"🌬 Wind Speed : {weather['wind']['speed']} m/s"
        )

        pressure.configure(
            text=f"🌍 Pressure : {weather['main']['pressure']} hPa"
        )

        sunrise.configure(
            text=f"🌅 Sunrise : {sunrise_time}"
        )

        sunset.configure(
            text=f"🌇 Sunset : {sunset_time}"
        )

    else:
        icon_label.configure(image=None, text="")
        city_name.configure(text="❌ City not found!")

        temperature.configure(text="")
        feels_like.configure(text="")
        description.configure(text="")
        humidity.configure(text="")
        wind.configure(text="")
        pressure.configure(text="")
        sunrise.configure(text="")
        sunset.configure(text="")
def show_forecast():
     city = city_entry.get().strip()
     data = get_forecast(city)

     if not data:
        city_name.configure(text="❌ Forecast not available")
        return

     forecast_text = ""

     for i in range(0, len(data["list"]), 8):  # every 24 hours
        day = data["list"][i]
        temp = day["main"]["temp"]
        desc = day["weather"][0]["description"]

        date = day["dt_txt"].split()[0]

        forecast_text += (f"📅 {date}\n"f"🌡 {temp}°C\n"f"☁ {desc.title()}\n\n"
)

        forecast_label.configure(text=forecast_text)
        tabview.set("📅 Forecast")

def current_location_weather():

    city = get_current_location()

    if city:

        city_entry.delete(0, "end")
        city_entry.insert(0, city)

        search_weather()

    else:

        city_name.configure(text="❌ Unable to detect location")
def change_theme(choice):

    ctk.set_appearance_mode(choice)
# ----------------------------------------
# Main Window
# ----------------------------------------
app = ctk.CTk()
app.configure(fg_color="#384B53")

app.title("Weather Forecast App")
app.geometry("900x750")
app.resizable(False, False)


# ----------------------------------------
# Title
# ----------------------------------------
header = ctk.CTkFrame(
    app,
    height=80,
    corner_radius=0,
    fg_color="#1E3A8A"
)

header.pack(fill="x")

title = ctk.CTkLabel(
    header,
    text="🌦 Weather Dashboard",
    font=ctk.CTkFont(size=32, weight="bold"),
    text_color="white"
)

title.pack(pady=20)

# ----------------------------------------
# Search Card
# ----------------------------------------
search_frame = ctk.CTkFrame(
    app,
    corner_radius=15
)

search_frame.pack(
    padx=20,
    pady=10,
    fill="x"
)

city_label = ctk.CTkLabel(
    search_frame,
    text="Enter City",
    font=ctk.CTkFont(size=18)
)

city_label.pack(pady=(20,5))

city_entry = ctk.CTkEntry(
    search_frame,
    width=300,
    height=45,
    placeholder_text="Ahmedabad..."
)

city_entry.pack(pady=10)

# ---------------- Buttons ----------------
button_frame = ctk.CTkFrame(
    search_frame,
    fg_color="transparent"
)
button_frame.pack(pady=15)

search_button = ctk.CTkButton(
    button_frame,
    text="🔍 Search Weather",
    width=180,
    height=45,
    command=search_weather,
    fg_color="#2563EB",
    hover_color="#1D4ED8",
    corner_radius=12
)
search_button.pack(side="left", padx=10)

current_location_button = ctk.CTkButton(
    button_frame,
    text="📍 Current Location",
    width=180,
    height=45,
    command=current_location_weather,
    fg_color="#059669",
    hover_color="#047857",
    corner_radius=12
)
current_location_button.pack(side="left", padx=10)

forecast_button = ctk.CTkButton(
    button_frame,
    text="📅 5-Day Forecast",
    width=180,
    height=45,
    command=show_forecast,
    fg_color="#7C3AED",
    hover_color="#6D28D9",
    corner_radius=12
)
forecast_button.pack(side="left", padx=10)
# ----------------------------------------
# Weather Card
# ----------------------------------------
tabview = ctk.CTkTabview(
    app,
    width=820,
    height=700
)

tabview.pack(
    padx=20,
    pady=20,
    fill="both",
    expand=True
)

weather_tab = tabview.add("🌤 Current Weather")
forecast_tab = tabview.add("📅 Forecast")
forecast_frame = ctk.CTkFrame(
    forecast_tab,
    fg_color="transparent"
)

forecast_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)
forecast_label = ctk.CTkLabel(
    forecast_frame,
    text="Click '5-Day Forecast' to view forecast",
    font=ctk.CTkFont(size=18),
    justify="left"
)

forecast_label.pack(pady=20)
settings_tab = tabview.add("⚙️ Settings")
settings_frame = ctk.CTkFrame(
    settings_tab,
    fg_color="transparent"
)

settings_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)
settings_title = ctk.CTkLabel(
    settings_frame,
    text="⚙️ Settings",
    font=ctk.CTkFont(
        size=26,
        weight="bold"
    )
)

settings_title.pack(pady=(20,30))
location_button = ctk.CTkButton(
    settings_frame,
    text="📍 Use Current Location",
    width=250,
    height=45,
    command=current_location_weather
)

location_button.pack(pady=15)
theme_label = ctk.CTkLabel(
    settings_frame,
    text="Theme",
    font=ctk.CTkFont(size=18)
)

theme_label.pack(pady=(20,5))

theme_menu = ctk.CTkOptionMenu(
    settings_frame,
    values=["System", "Light", "Dark"],
    command=change_theme
)

theme_menu.pack()
unit_label = ctk.CTkLabel(
    settings_frame,
    text="Temperature Unit",
    font=ctk.CTkFont(size=18)
)

unit_label.pack(pady=(25,5))

unit_menu = ctk.CTkOptionMenu(
    settings_frame,
    values=["Celsius", "Fahrenheit"]
)

unit_menu.pack()
about = ctk.CTkLabel(
    settings_frame,
    text="Weather Dashboard\nVersion 1.0\nDeveloped using Python & CustomTkinter",
    justify="center",
    font=ctk.CTkFont(size=15)
)

about.pack(pady=40)

weather_frame = ctk.CTkFrame(
    weather_tab,
    fg_color="transparent"
)

weather_frame.pack(
    padx=20,
    pady=20,
    fill="both",
    expand=True
)

city_name = ctk.CTkLabel(
    weather_frame,
    text="Search a city",
    font=ctk.CTkFont(
        size=26,
        weight="bold"
    )
)

city_name.pack(pady=(25,15))

icon_label = ctk.CTkLabel(
    weather_frame,
    text=""
)
icon_label.pack(pady=10)

temperature = ctk.CTkLabel(
    weather_frame,
    text="--°C",
    font=ctk.CTkFont(
        size=42,
        weight="bold"
    )
)

info_frame = ctk.CTkFrame(
 weather_frame,
    fg_color="transparent"
)

feels_like = ctk.CTkLabel(
    info_frame,
    text="",
    font=ctk.CTkFont(size=18)
)
feels_like.grid(row=0, column=0, padx=20, pady=10, sticky="w")



info_frame.pack(pady=20)

description = ctk.CTkLabel(
    info_frame,
    text="",
    font=ctk.CTkFont(size=18)
)
description.grid(row=1, column=0, padx=20, pady=10, sticky="w")

humidity = ctk.CTkLabel(
    info_frame,
    text="",
    font=ctk.CTkFont(size=18)
)
humidity.grid(row=0, column=1, padx=20, pady=10, sticky="w")

wind = ctk.CTkLabel(
    info_frame,
    text="",
    font=ctk.CTkFont(size=18)
)
wind.grid(row=1, column=1, padx=20, pady=10, sticky="w")

pressure = ctk.CTkLabel(
    info_frame,
    text="",
    font=ctk.CTkFont(size=18)
)
pressure.grid(row=2, column=0, padx=20, pady=10, sticky="w")

sunrise = ctk.CTkLabel(
    info_frame,
    text="",
    font=ctk.CTkFont(size=18)
)
sunrise.grid(row=2, column=1, padx=20, pady=10, sticky="w")

sunset = ctk.CTkLabel(
    info_frame,
    text="",
    font=ctk.CTkFont(size=18)
)
sunset.grid(row=3, column=0, padx=20, pady=10, sticky="w")

# ----------------------------------------
# Footer
# ----------------------------------------
footer = ctk.CTkLabel(
    app,
    text="Developed By Parth Khorasiya using Python • CustomTkinter • OpenWeather API",
    font=ctk.CTkFont(size=12)
)

footer.pack(pady=15)

# ----------------------------------------
# Run App
# ----------------------------------------
app.mainloop()