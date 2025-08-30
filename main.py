from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# بيانات الدخول
LOGIN_URL = "https://admission.study-in-egypt.gov.eg/login"
TARGET_URL = "https://admission.study-in-egypt.gov.eg/services/admission/requests/591263/edit"
EMAIL = "mgdadsubs@gmail.com"
PASSWORD = "Test@12100"
WAIT_TIME = 20

def main():
    chrome_options = Options()
    chrome_options.add_argument('--headless') # لتشغيل المتصفح في وضع الـ headless
    chrome_options.add_argument('--disable-gpu') # لتعطيل الـ GPU
    chrome_options.add_argument('--no-sandbox') # لتعطيل الـ sandbox (مهم في بيئات مثل Render)
    chrome_options.add_argument('--disable-dev-shm-usage') # لحل بعض مشاكل الذاكرة في بيئات السيرفر
    chrome_options.add_argument('--window-size=1920x1080') # لتحديد حجم النافذة
    chrome_options.add_argument(f'--binary=/usr/bin/chromium') # تحديد مسار الـ Chromium

    # تأكد من أنك تستخدم السائق الصحيح لـ Chromium
    chromedriver_path = ChromeDriverManager().install()

    # تحميل المتصفح
    driver = webdriver.Chrome(service=Service(chromedriver_path), options=chrome_options)

    try:
        print("فتح صفحة تسجيل الدخول...")
        driver.get(LOGIN_URL)

        # إدخال البريد الإلكتروني
        email_input = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-id="backEnd-backEnd-email"]'))
        )
        email_input.clear()
        email_input.send_keys(EMAIL)

        # إدخال كلمة المرور
        password_input = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-id="backEnd-backEnd-password"]'))
        )
        password_input.clear()
        password_input.send_keys(PASSWORD)

        # الضغط على زر تسجيل الدخول
        login_button = WebDriverWait(driver, WAIT_TIME).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
        )
        login_button.click()

        # الانتقال إلى صفحة الرغبات
        WebDriverWait(driver, WAIT_TIME).until(EC.url_contains("/dashboard"))
        driver.get(TARGET_URL)

        print("التحقق من الوصول إلى صفحة الرغبات...")
        WebDriverWait(driver, WAIT_TIME).until(EC.url_contains("/edit"))

        # هنا يمكنك إضافة الرغبات حسب المطلوب

    except Exception as e:
        print(f"حدث خطأ: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
