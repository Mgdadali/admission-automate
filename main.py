import os
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# إعداد الـ Logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# بيانات الدخول من متغيرات البيئة
EMAIL = os.getenv("EGYPT_USER")
PASSWORD = os.getenv("EGYPT_PASS")

# Selectors
EMAIL_SELECTOR = "input[name='email']"
PASS_SELECTOR = "input[name='password']"
WISHLIST_SELECTOR = ".react-select__value-container.css-1hwfws3"
DESIRED_TEXT = "تمريض القاهرة ساعات معتمدة ـ برنامج خاص بمصروفات"
ADD_BUTTON_SELECTOR = "//button[contains(text(), 'إضافة')]"

# روابط
LOGIN_URL = "https://admission.study-in-egypt.gov.eg/"
TARGET_URL = "https://admission.study-in-egypt.gov.eg/services/admission/requests/591263/edit"

WAIT_TIME = 30  # زيادة وقت الانتظار

def save_debug_files(driver):
    """حفظ Screenshot و HTML للصفحة"""
    try:
        driver.save_screenshot("error.png")
        with open("page.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        logging.info("تم حفظ ملفات debug: error.png و page.html")
    except Exception as e:
        logging.error(f"فشل حفظ ملفات debug: {e}")

def main():
    logging.info("بدء تشغيل السكربت...")

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        logging.info("فتح صفحة تسجيل الدخول...")
        driver.get(LOGIN_URL)

        logging.info("إدخال البريد...")
        WebDriverWait(driver, WAIT_TIME).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, EMAIL_SELECTOR))
        ).send_keys(EMAIL)

        logging.info("إدخال كلمة المرور...")
        WebDriverWait(driver, WAIT_TIME).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, PASS_SELECTOR))
        ).send_keys(PASSWORD)

        logging.info("تسجيل الدخول...")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        logging.info("الانتقال إلى صفحة الرغبات...")
        driver.get(TARGET_URL)

        logging.info("فتح قائمة الرغبات...")
        WebDriverWait(driver, WAIT_TIME).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, WISHLIST_SELECTOR))
        ).click()

        logging.info(f"اختيار الرغبة: {DESIRED_TEXT}")
        option_xpath = f"//div[contains(text(), '{DESIRED_TEXT}')]"
        WebDriverWait(driver, WAIT_TIME).until(
            EC.element_to_be_clickable((By.XPATH, option_xpath))
        ).click()

        logging.info("الضغط على زر إضافة...")
        WebDriverWait(driver, WAIT_TIME).until(
            EC.element_to_be_clickable((By.XPATH, ADD_BUTTON_SELECTOR))
        ).click()

        logging.info("تم تنفيذ جميع الخطوات بنجاح ✅")

    except Exception as e:
        logging.error(f"حدث خطأ: {e}")
        
        # حفظ الملفات
        save_debug_files(driver)
        
        # طباعة HTML الصفحة في اللوج
        page_html = driver.page_source
        logging.info("==== بداية HTML الصفحة ====")
        for i, line in enumerate(page_html.splitlines()[:200], start=1):
            logging.info(f"{i:03}: {line}")
        logging.info("==== نهاية HTML الصفحة ====")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
