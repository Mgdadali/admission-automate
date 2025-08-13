from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

EMAIL = "mgdadsubs@gmail.com"
PASSWORD = "Test@12100"
TARGET_URL = "https://admission.study-in-egypt.gov.eg/services/admission/requests/591263/edit"
DESIRED_CHOICE = "تمريض القاهرة ساعات معتمدة ـ برنامج خاص بمصروفات"

def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")  # تشغيل بدون واجهة
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 15)

    try:
        print("[INFO] فتح صفحة تسجيل الدخول...")
        driver.get("https://admission.study-in-egypt.gov.eg/login")

        # إدخال البريد
        email_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        email_input.send_keys(EMAIL)

        # إدخال كلمة المرور
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys(PASSWORD)

        # زر تسجيل الدخول
        login_btn = driver.find_element(By.TAG_NAME, "button")
        login_btn.click()

        # الانتقال مباشرة للرابط
        wait.until(EC.url_contains("/dashboard"))
        print("[INFO] تسجيل الدخول ناجح، الانتقال للرابط المطلوب...")
        driver.get(TARGET_URL)

        # انتظار تحميل القائمة
        choice_container = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "react-select__value-container")))
        choice_container.click()

        # اختيار الرغبة
        choice = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[text()='{DESIRED_CHOICE}']")))
        choice.click()

        # الضغط على زر إضافة
        add_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button:nth-child(1)")))
        add_button.click()

        print("[INFO] تم اختيار الرغبة وإضافتها بنجاح.")

    except Exception as e:
        print("[ERROR]", e)
        driver.save_screenshot("error.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
