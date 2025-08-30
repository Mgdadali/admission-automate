from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# إعدادات المتصفح
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # تشغيل المتصفح في الخلفية (بدون واجهة رسومية)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# فتح صفحة تسجيل الدخول
driver.get("https://admission.study-in-egypt.gov.eg/login")

# الانتظار حتى تحميل الصفحة
wait = WebDriverWait(driver, 10)

try:
    # تحديد حقل البريد الإلكتروني باستخدام CSS Selector أو XPath
    email_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".Label_required-label__12wpY")))
    
    # إدخال البريد الإلكتروني
    email_field.send_keys("example@example.com")

    # تحديد حقل كلمة المرور باستخدام CSS Selector أو XPath
    password_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".Label_required-label__12wpY")))  # تعديل حسب العنصر الصحيح
    
    # إدخال كلمة المرور
    password_field.send_keys("your_password_here")

    # تحديد زر تسجيل الدخول
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))  # تعديل حسب مكان الزر
    
    # الضغط على زر تسجيل الدخول
    login_button.click()

    # الانتظار قليلاً للتأكد من أنه تم تسجيل الدخول
    time.sleep(5)

    # بعد تسجيل الدخول، الانتقال إلى الرابط المحدد
    driver.get("https://admission.study-in-egypt.gov.eg/services/admission/requests/591263/edit")
    time.sleep(5)  # الانتظار حتى تحميل الصفحة

    print("تم تسجيل الدخول والانتقال إلى الصفحة المطلوبة.")
except Exception as e:
    print(f"حدث خطأ: {e}")
finally:
    # إغلاق المتصفح بعد التنفيذ
    driver.quit()
