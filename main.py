import os
import requests
import zipfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# تحميل ChromeDriver من GitHub (إذا لم يكن موجوداً على Render)
def download_chromedriver():
    url = "https://github.com/Mgdadali/admission-automate/raw/main/chromedriver/chromedriver_linux64.zip"  # رابط تحميل ChromeDriver
    response = requests.get(url)
    with open("/tmp/chromedriver.zip", "wb") as f:
        f.write(response.content)

    with zipfile.ZipFile("/tmp/chromedriver.zip", "r") as zip_ref:
        zip_ref.extractall("/tmp")

    os.chmod("/tmp/chromedriver", 0o755)

# استخدام ChromeDriver من GitHub
def main():
    # تحميل ChromeDriver إذا لم يكن موجوداً
    if not os.path.exists("/tmp/chromedriver"):
        download_chromedriver()

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115 Safari/537.36")

    # تحديد مسار ChromeDriver
    chromedriver_path = "/tmp/chromedriver"
    driver = webdriver.Chrome(service=Service(chromedriver_path), options=chrome_options)

    try:
        # فتح الصفحة
        driver.get("https://admission.study-in-egypt.gov.eg/login")

        # تسجيل الدخول
        email_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-id="backEnd-backEnd-email"]')))
        email_input.clear()
        email_input.send_keys("mgdadsubs@gmail.com")

        password_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-id="backEnd-backEnd-password"]')))
        password_input.clear()
        password_input.send_keys("Test@12100")

        login_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
        login_button.click()

        # الانتقال إلى صفحة الرغبات
        WebDriverWait(driver, 20).until(EC.url_contains("/dashboard"))
        driver.get("https://admission.study-in-egypt.gov.eg/services/admission/requests/591263/edit")

    except Exception as e:
        print(f"حدث خطأ: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
