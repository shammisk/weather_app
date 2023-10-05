import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap

root = tk.Tk()
root.title("Weather App")
root.geometry("400x400")
root.resizable(False, False)

image_icon=tk.PhotoImage(file="img/weather.png")
root.iconphoto(False,image_icon)


def get_weather(city):
    API_key = "3500b223f4819d45fa5597b45868055d"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    res = requests.get(url)

    if res.status_code == 404:
        messagebox.showerror("Error", "City not found")
        return None

    weather = res.json()
    icon_id = weather['weather'][0]['icon']
    temperature = weather['main']['temp'] - 273.15
    description = weather['weather'][0]['description']
    city_name = weather['name']
    country = weather['sys']['country']

    icon_url = f"http://openweathermap.org/img/w/{icon_id}.png"
    return (icon_url, temperature, description, city_name, country)

def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return

    icon_url, temperature, description, city_name, country = result
    location_label.configure(text=f"{city_name}, {country}")

    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon

    temperature_label.configure(text=f"Temperature: {temperature:.2f}°C")
    description_label.configure(text=f"Description: {description}")

city_entry = ttkbootstrap.Entry(root, font="Helvetica 18", justify="center")
city_entry.pack(pady=10)

search_button = ttkbootstrap.Button(root, text="Search", command=search, style="dark", padding= (35, 15))
search_button.pack(pady=10)

location_label = tk.Label(root, font="Helvetica 25")
location_label.pack(pady=20)

icon_label = tk.Label(root)
icon_label.pack()

temperature_label = tk.Label(root, font="Helvetica 20")
temperature_label.pack()

description_label = tk.Label(root, font="Helvetica 20")
description_label.pack()

root.mainloop()
