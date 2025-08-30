import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.remote.webdriver import WebElement

# بيانات تسجيل الدخول
EMAIL = "your_email@example.com"
PASSWORD = "your_password"
TARGET_URL = "https://admission.study-in-egypt.gov.eg/services/admission/requests/591263/edit"
DESIRED_CHOICE = "Choice Name"  # قم بتعديل هذه القيمة حسب الرغبة التي تريد إضافتها

def main():
    # إعدادات المتصفح
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.binary_location = "/usr/bin/chromium"

    driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=chrome_options)
    wait = WebDriverWait(driver, 20)  # زيادة وقت الانتظار لزيادة التأكيد

    print("[INFO] فتح صفحة تسجيل الدخول...")
    driver.get("https://admission.study-in-egypt.gov.eg/login")

    # إدخال البريد وكلمة المرور
    wait.until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(EMAIL)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.TAG_NAME, "button").click()

    # التحقق من نجاح عملية تسجيل الدخول
    try:
        user_icon = wait.until(EC.presence_of_element_located((By.XPATH, "//img[@alt='User Icon']")))  # قم بتعديل هذا حسب العنصر المميز
        print("[INFO] تم تسجيل الدخول بنجاح.")
    except TimeoutException:
        print("[ERROR] لم يتم تسجيل الدخول بنجاح.")
        driver.quit()
        return

    # بعد تسجيل الدخول، الانتقال إلى الرابط المطلوب
    driver.get(TARGET_URL)

    # الانتظار حتى تظهر قائمة الرغبات
    choice_container = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "react-select__value-container")))
    choice_container.click()

    # اختيار الرغبة المطلوبة
    choice = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[text()='{DESIRED_CHOICE}']")))
    choice.click()

    # الضغط على زر إضافة الرغبة
    add_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button:nth-child(1)")))
    add_button.click()

    print("[INFO] تم اختيار الرغبة وإضافتها بنجاح.")
    
    # إنهاء الجلسة
    driver.quit()

if __name__ == "__main__":
    main()
