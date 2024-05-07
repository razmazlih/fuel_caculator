import customtkinter as ctk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import threading
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_fuel_price():
    # Define path for ChromeDriver
    service = Service(ChromeDriverManager().install())
    # Create WebDriver object for Chrome
    driver = webdriver.Chrome(service=service)

    try:
        # Load the website
        driver.get("https://fuelcalc.energydmz.org/")

        # More robust waiting mechanism
        element_class_name = "subConsumerStationPrice"
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, element_class_name))
        )
        element = driver.find_element(By.CLASS_NAME, element_class_name)

        # Safely extract the price and return as float
        price_text = element.text.split()[0]
        return float(price_text)

    except Exception as e:
        print(f"Failed to get fuel price: {str(e)}")
        return None  # Return None if there's an error
    finally:
        # Close the browser
        driver.quit()


def calculate_price(km, result_label):
    try:
        fuel_price = get_fuel_price()
        if fuel_price is None:
            raise ValueError("Fuel price could not be retrieved.")
        km_on_litre = 12  # Assuming 12 km per litre
        price = km / km_on_litre * fuel_price
        result_label.configure(text=f"Calculated cost: ILS{price:.2f}")  # Using configure to update the label
    except Exception as e:
        result_label.configure(text=f"Error: {str(e)}")  # Using configure to update the label on error

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
