import os
import requests


def download_icon(icon_code):
    """
    Downloads the weather icon from OpenWeatherMap
    and saves it inside assets/icons/
    """

    # Create folder if it doesn't exist
    os.makedirs("assets/icons", exist_ok=True)

    icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"

    file_path = f"assets/icons/{icon_code}.png"

    # Download only if the icon isn't already saved
    if not os.path.exists(file_path):
        response = requests.get(icon_url)

        if response.status_code == 200:
            with open(file_path, "wb") as file:
                file.write(response.content)

    return file_path