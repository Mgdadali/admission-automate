import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# إعدادات الـ Logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# المتغيرات من بيئة Render
EMAIL = os.getenv("EGYPT_USER")
PASSWORD = os.getenv("EGYPT_PASS")

# Selectors
EMAIL_SELECTOR = "input[name='email']"
PASS_SELECTOR = "input[name='password']"
WISHLIST_SELECTOR = ".react-select__value-container.css-1hwfws3"
DESIRED_TEXT = "تمريض القاهرة ساعات معتمدة ـ برنامج خاص بمصروفات"
ADD_BUTTON_SELECTOR = "//button[contains(text(), 'إضافة')]"

# رابط الصفحات
LOGIN_URL = "https://admission.study-in-egypt.gov.eg/"
TARGET_URL = "https://admission.study-in-egypt.gov.eg/services/admission/requests/591263/edit"

def main():
    logging.info("بدء تشغيل السكربت...")

    # إعداد المتصفح في وضع Headless
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        # 1. فتح صفحة تسجيل الدخول
        logging.info("فتح صفحة تسجيل الدخول...")
        driver.get(LOGIN_URL)

        # إدخال البريد
        logging.info("إدخال البريد...")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, EMAIL_SELECTOR))).send_keys(EMAIL)

        # إدخال كلمة المرور
        logging.info("إدخال كلمة المرور...")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, PASS_SELECTOR))).send_keys(PASSWORD)

        # الضغط على زر الدخول
        logging.info("تسجيل الدخول...")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # الانتقال مباشرة للصفحة المطلوبة
        logging.info("الانتقال إلى صفحة الرغبات...")
        driver.get(TARGET_URL)

        # فتح قائمة الرغبات
        logging.info("فتح قائمة الرغبات...")
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, WISHLIST_SELECTOR))).click()

        # اختيار الرغبة
        logging.info(f"اختيار الرغبة: {DESIRED_TEXT}")
        option_xpath = f"//div[contains(text(), '{DESIRED_TEXT}')]"
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, option_xpath))).click()

        # الضغط على زر إضافة
        logging.info("الضغط على زر إضافة...")
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, ADD_BUTTON_SELECTOR))).click()

        logging.info("تم تنفيذ جميع الخطوات بنجاح ✅")

    except Exception as e:
        logging.error(f"حدث خطأ: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
