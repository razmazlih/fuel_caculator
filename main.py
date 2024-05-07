import customtkinter as ctk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import threading
import time

def get_fuel_price():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        driver.get("https://fuelcalc.energydmz.org/")
        # time.sleep(5)

        element_class_name = "subConsumerStationPrice"
        element = driver.find_element(By.CLASS_NAME, element_class_name)

        # Return the price as float
        return float(element.text.split()[0])

    finally:
        driver.quit()

def calculate_price(km, result_label):
    try:
        fuel_price = get_fuel_price()
        km_on_litre = 12  # Assuming 12 km per litre
        price = km / km_on_litre * fuel_price
        result_label.set(f"Calculated cost: ${price:.2f}")
    except Exception as e:
        result_label.set(f"Error: {str(e)}")

def calculate_wrapper(km_entry, result_label):
    try:
        km = float(km_entry.get())
        threading.Thread(target=calculate_price, args=(km, result_label)).start()
    except ValueError:
        result_label.set("Please enter a valid number for kilometers.")

def create_gui():
    app = ctk.CTk()
    app.title("Fuel Cost Calculator")

    ctk.CTkLabel(app, text="Enter kilometers:").pack(pady=(20, 10))
    km_entry = ctk.CTkEntry(app, width=200)
    km_entry.pack(pady=(0, 20))

    result_label = ctk.CTkLabel(app, text="")
    result_label.pack(pady=(10, 20))

    calculate_btn = ctk.CTkButton(app, text="Calculate Fuel Cost",
                                  command=lambda: calculate_wrapper(km_entry, result_label))
    calculate_btn.pack(pady=(0, 20))

    app.mainloop()

# Uncomment below line to run the GUI application
create_gui()
