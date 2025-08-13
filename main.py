import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# إعدادات عامة
LOGIN_URL = "https://admission.study-in-egypt.gov.eg/login"
TARGET_URL = "https://admission.study-in-egypt.gov.eg/services/admission/requests/591263/edit"
EMAIL = "mgdadsubs@gmail.com"
PASSWORD = "Test@12100"
WAIT_TIME = 20

logging.basicConfig(level=logging.INFO, format='[INFO] %(message)s')

def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # أو احذفها لو عايز تشوف المتصفح
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        logging.info("فتح صفحة تسجيل الدخول...")
        driver.get(LOGIN_URL)
        driver.implicitly_wait(10)

        # البحث عن الحقول
        inputs = driver.find_elements(By.TAG_NAME, "input")
        logging.info(f"تم العثور على {len(inputs)} حقل إدخال:")
        for i, inp in enumerate(inputs, start=1):
            name = inp.get_attribute("name")
            placeholder = inp.get_attribute("placeholder")
            logging.info(f"- حقل {i}: name='{name}', placeholder='{placeholder}'")

        # إدخال البيانات
        logging.info("إدخال البريد...")
        driver.find_element(By.NAME, "email").send_keys(EMAIL)

        logging.info("إدخال كلمة المرور...")
        driver.find_element(By.NAME, "password").send_keys(PASSWORD)

        logging.info("تسجيل الدخول...")
        driver.find_element(By.TAG_NAME, "button").click()

        # الانتقال إلى صفحة الرغبات
        logging.info("الانتقال إلى صفحة الرغبات...")
        WebDriverWait(driver, WAIT_TIME).until(EC.url_contains("/dashboard"))
        driver.get(TARGET_URL)

        logging.info("التحقق من الوصول إلى صفحة الرغبات...")
        WebDriverWait(driver, WAIT_TIME).until(EC.url_contains("/edit"))

        logging.info("فتح قائمة الرغبات...")
        # هنا تضيف كود اختيار الرغبة وزر الإضافة...

    except Exception as e:
        logging.error(f"حدث خطأ: {e}")
        with open("page.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        driver.save_screenshot("error.png")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
