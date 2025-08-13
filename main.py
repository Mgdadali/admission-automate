from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

EMAIL = "mgdadsubs@gmail.com"
PASSWORD = "Test@12100"
TARGET_URL = "https://admission.study-in-egypt.gov.eg/services/admission/requests/591263/edit"
DESIRED_CHOICE = "تمريض القاهرة ساعات معتمدة ـ برنامج خاص بمصروفات"

def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.binary_location = "/usr/bin/chromium"

    driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=chrome_options)
    wait = WebDriverWait(driver, 15)

    print("[INFO] فتح صفحة تسجيل الدخول...")
    driver.get("https://admission.study-in-egypt.gov.eg/login")

    wait.until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(EMAIL)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.TAG_NAME, "button").click()

    wait.until(EC.url_contains("/dashboard"))
    driver.get(TARGET_URL)

    choice_container = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "react-select__value-container")))
    choice_container.click()

    choice = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[text()='{DESIRED_CHOICE}']")))
    choice.click()

    add_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button:nth-child(1)")))
    add_button.click()

    print("[INFO] تم اختيار الرغبة وإضافتها بنجاح.")
    driver.quit()

if __name__ == "__main__":
    main()
