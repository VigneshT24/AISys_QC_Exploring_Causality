import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# set up the headless chrome options
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# initialize the driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # automate opening the app to keep it from sleeping
    app_url = "https://aisys-quantumcausality.streamlit.app/"
    print(f"I am navigating to {app_url}...")
    driver.get(app_url)
    time.sleep(10) # give a buffer for page to load

    # find the wake-up button (if it is there)
    buttons = driver.find_elements(By.TAG_NAME, "buttom")
    woken = False

    for button in buttons:
        if "Yes, get this app back up" in button.txt:
            button.click()
            print("App was sleeping. Just woke it up!")
            woken = True
            time.sleep(5)
            break

    if not woken:
        print("App was already woken up or I couldn't find the button")

except Exception as e:
    print(f"The following error occured: {e}")

finally:
    driver.quit()