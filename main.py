from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_fuel_price():
    # הגדרת נתיב ל-ChromeDriver
    service = Service(ChromeDriverManager().install())

    # יצירת אובייקט WebDriver עבור Chrome
    driver = webdriver.Chrome(service=service)

    try:
        # טעינת האתר
        driver.get("https://fuelcalc.energydmz.org/")

        # המתנה כדי שהעמוד יטען
        # time.sleep(1)

        element_class_name = "subConsumerStationPrice"
        element = driver.find_element(By.CLASS_NAME, element_class_name)

        # הדפסת הטקסט של האלמנט
        print("The fuel cost is:", element.text)

        return float(element.text[:3])

    finally:
        # סגירת הדפדפן
        driver.quit()



def calculate_price(km):
    fuel_price = get_fuel_price()
    km_on_litre = 12
    print(km / km_on_litre * fuel_price)
