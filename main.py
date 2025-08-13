import time
import logging
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO, format='[INFO] %(message)s')

EMAIL = "mgdadsubs@gmail.com"
PASSWORD = "Test@12100"
LOGIN_URL = "https://admission.study-in-egypt.gov.eg/login"
TARGET_URL = "https://admission.study-in-egypt.gov.eg/services/admission/requests/591263/edit"
WAIT_TIME = 15

def main():
    logging.info("تشغيل المتصفح في وضع Stealth...")
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = uc.Chrome(options=options)

    try:
        logging.info("فتح صفحة تسجيل الدخول...")
        driver.get(LOGIN_URL)

        # إدخال البريد
        logging.info("إدخال البريد...")
        email_field = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        email_field.send_keys(EMAIL)

        # إدخال الباسورد
        logging.info("إدخال كلمة المرور...")
        pass_field = driver.find_element(By.NAME, "password")
        pass_field.send_keys(PASSWORD)

        # الضغط على زر تسجيل الدخول
        logging.info("الضغط على زر تسجيل الدخول...")
        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'تسجيل الدخول')]")
        login_button.click()

        # الانتظار حتى الوصول للداشبورد
        logging.info("الانتظار للوصول للداشبورد...")
        WebDriverWait(driver, WAIT_TIME * 2).until(
            EC.url_contains("/dashboard")
        )

        # الانتقال لصفحة الرغبات
        logging.info("الانتقال لصفحة الرغبات...")
        driver.get(TARGET_URL)

        try:
            WebDriverWait(driver, WAIT_TIME).until(
                EC.url_contains("/edit")
            )
        except:
            logging.warning("لم يتم الوصول من أول مرة... إعادة المحاولة")
            driver.get(TARGET_URL)
            WebDriverWait(driver, WAIT_TIME).until(EC.url_contains("/edit"))

        logging.info("فتح قائمة الرغبات...")
        dropdown = WebDriverWait(driver, WAIT_TIME).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "react-select__value-container"))
        )
        dropdown.click()

        logging.info("اختيار الرغبة المطلوبة...")
        option = WebDriverWait(driver, WAIT_TIME).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'تمريض القاهرة ساعات معتمدة ـ برنامج خاص بمصروفات')]"))
        )
        option.click()

        logging.info("الضغط على زر إضافة...")
        add_button = driver.find_element(
            By.CSS_SELECTOR,
            "#root > div > div > div.ContinueRequest_container__3pQh_ > div > form > div > section > div > div > section > div.FlexibleMulti_multiple-fields__2mn2G > div.undefined > div > form > div.FlexibleMulti_footer-container__1viNx > div > button:nth-child(1)"
        )
        add_button.click()

        logging.info("تمت العملية بنجاح! 🎯")

    except Exception as e:
        logging.error(f"حدث خطأ: {e}")
        driver.save_screenshot("error.png")
        with open("page.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
