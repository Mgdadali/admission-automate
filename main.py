import os
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

EMAIL = os.getenv("EGYPT_USER")
PASSWORD = os.getenv("EGYPT_PASS")

EMAIL_SELECTOR = "input[name='email']"
PASS_SELECTOR = "input[name='password']"
WISHLIST_SELECTOR = ".react-select__value-container.css-1hwfws3"
DESIRED_TEXT = "تمريض القاهرة ساعات معتمدة ـ برنامج خاص بمصروفات"
ADD_BUTTON_SELECTOR = "//button[contains(text(), 'إضافة')]"

LOGIN_URL = "https://admission.study-in-egypt.gov.eg/login"
TARGET_URL = "https://admission.study-in-egypt.gov.eg/services/admission/requests/591263/edit"

WAIT_TIME = 30

def click_if_exists(driver, selector, by=By.CSS_SELECTOR):
    try:
        el = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((by, selector)))
        el.click()
        logging.info(f"تم الضغط على: {selector}")
    except:
        pass

def save_debug_files(driver):
    try:
        driver.save_screenshot("error.png")
        with open("page.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        logging.info("تم حفظ ملفات debug: error.png و page.html")
    except Exception as e:
        logging.error(f"فشل حفظ ملفات debug: {e}")

def print_input_fields(driver):
    inputs = driver.find_elements(By.XPATH, "//input[not(@type='hidden')]")
    logging.info(f"تم العثور على {len(inputs)} حقل إدخال:")
    for i, inp in enumerate(inputs, start=1):
        try:
            name = inp.get_attribute("name") or ""
            placeholder = inp.get_attribute("placeholder") or ""
            logging.info(f"- حقل {i}: name='{name}', placeholder='{placeholder}'")
        except:
            pass

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

        # عرض الحقول الموجودة قبل إدخال البيانات
        print_input_fields(driver)

        logging.info("إدخال البريد...")
        email_field = WebDriverWait(driver, WAIT_TIME).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, EMAIL_SELECTOR))
        )
        email_field.send_keys(EMAIL)

        logging.info("إدخال كلمة المرور...")
        pass_field = WebDriverWait(driver, WAIT_TIME).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, PASS_SELECTOR))
        )
        pass_field.send_keys(PASSWORD)

        logging.info("تسجيل الدخول...")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        logging.info("الانتقال إلى صفحة الرغبات...")
        driver.get(TARGET_URL)

        # التحقق من الوصول للصفحة الصحيحة
        logging.info("التحقق من الوصول إلى صفحة الرغبات...")
        WebDriverWait(driver, WAIT_TIME).until(EC.url_contains("/edit"))
        if "/edit" not in driver.current_url:
            raise Exception("لم يتم الوصول إلى صفحة تعديل الرغبات!")

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
        save_debug_files(driver)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
