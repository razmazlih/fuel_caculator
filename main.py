import customtkinter as ctk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import threading
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests


def get_price_new():
    url = "https://fuelcalc.energydmz.org/api/prices/getLatestPrice"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    result = requests.get(url, headers=headers)

    result_dict = result.json()

    the_cost = result_dict[2]["PriceValue"]
    return the_cost

def calculate_price(km, result_label, fuel_price):
    try:
        if fuel_price is None:
            raise ValueError("Fuel price could not be retrieved.")
        km_on_litre = 12  # Assuming 12 km per litre
        price = km / km_on_litre * fuel_price
        result_label.configure(text=f"Trip cost: ₪{price:.2f}")  # Using configure to update the label
    except Exception as e:
        result_label.configure(text=f"Error: {str(e)}")  # Using configure to update the label on error

def calculate_wrapper(km_entry, result_label, fuel_price):
    try:
        km = float(km_entry.get())
        threading.Thread(target=calculate_price, args=(km, result_label, fuel_price)).start()
    except ValueError:
        result_label.set("Please enter a valid number for kilometers.")

def create_gui(fuel_price):
    app = ctk.CTk()
    app.title("Fuel Cost Calculator")

    ctk.CTkLabel(app, text="Enter kilometers:").pack(pady=(20, 10))
    km_entry = ctk.CTkEntry(app, width=200)
    km_entry.pack(pady=(0, 20))

    # car_type_entry = ctk.
    

    result_label = ctk.CTkLabel(app, text="")
    result_label.pack(pady=(10, 20))

    calculate_btn = ctk.CTkButton(app, text="Calculate Fuel Cost",
                                  command=lambda: calculate_wrapper(km_entry, result_label, fuel_price))
    calculate_btn.pack(pady=(0, 20))

    app.mainloop()


fuel_price = get_price_new()

# Uncomment below line to run the GUI application
create_gui(fuel_price)
