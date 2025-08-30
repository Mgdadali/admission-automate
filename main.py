import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# بيانات الدخول
LOGIN_URL = "https://admission.study-in-egypt.gov.eg/login"
TARGET_URL = "https://admission.study-in-egypt.gov.eg/services/admission/requests/591263/edit"
EMAIL = "mgdadsubs@gmail.com"
PASSWORD = "Test@12100"
WAIT_TIME = 20

logging.basicConfig(level=logging.INFO, format='[INFO] %(message)s')

def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # وضع التشغيل بدون واجهة مستخدم
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920x1080")
    
    # تحديد الإصدار المتوافق من ChromeDriver يدويًا
    chromedriver_path = ChromeDriverManager(version="139.0.7258.154").install()
    driver = webdriver.Chrome(service=Service(chromedriver_path), options=chrome_options)

    try:
        logging.info("فتح صفحة تسجيل الدخول...")
        driver.get(LOGIN_URL)

        # انتظار ظهور حقل البريد الإلكتروني
        logging.info("إدخال البريد...")
        email_input = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-id="backEnd-backEnd-email"]'))
        )
        email_input.clear()
        email_input.send_keys(EMAIL)

        # انتظار ظهور حقل كلمة المرور
        logging.info("إدخال كلمة المرور...")
        password_input = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-id="backEnd-backEnd-password"]'))
        )
        password_input.clear()
        password_input.send_keys(PASSWORD)

        # الضغط على زر تسجيل الدخول
        logging.info("تسجيل الدخول...")
        login_button = WebDriverWait(driver, WAIT_TIME).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
        )
        login_button.click()

        # الانتقال إلى صفحة الرغبات
        logging.info("الانتقال إلى صفحة الرغبات...")
        WebDriverWait(driver, WAIT_TIME).until(EC.url_contains("/dashboard"))
        driver.get(TARGET_URL)

        logging.info("التحقق من الوصول إلى صفحة الرغبات...")
        WebDriverWait(driver, WAIT_TIME).until(EC.url_contains("/edit"))

        # هنا نضيف اختيار الرغبة وزر الإضافة لاحقًا
        logging.info("فتح قائمة الرغبات...")
        
    except Exception as e:
        logging.error(f"حدث خطأ: {e}")
        with open("page.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        driver.save_screenshot("error.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
