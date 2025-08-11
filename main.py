import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

LOGIN_PAGE = "https://admission.study-in-egypt.gov.eg/"
EDIT_PAGE = "https://admission.study-in-egypt.gov.eg/services/admission/requests/591263/edit"
DESIRED_TEXT = "اسم الرغبة اللي عايز تختارها هنا"
WAIT_TIMEOUT = 15

USERNAME = os.environ.get("EGYPT_USER")
PASSWORD = os.environ.get("EGYPT_PASS")

if not USERNAME or not PASSWORD:
    raise SystemExit("❌ لازم تضيف المتغيرات EGYPT_USER و EGYPT_PASS في بيئة التشغيل (Environment Variables).")

def start_browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    return driver

def find_input_for_login(driver):
    candidates = [
        (By.CSS_SELECTOR, "input[type='email']"),
        (By.CSS_SELECTOR, "input[name='email']"),
        (By.CSS_SELECTOR, "input[id*='email']"),
        (By.CSS_SELECTOR, "input[type='text']"),
        (By.CSS_SELECTOR, "input[name='username']"),
        (By.CSS_SELECTOR, "input[id*='username']"),
    ]
    pw_candidates = [
        (By.CSS_SELECTOR, "input[type='password']"),
        (By.CSS_SELECTOR, "input[name='password']"),
        (By.CSS_SELECTOR, "input[id*='password']"),
    ]
    email_el = pw_el = None
    for sel in candidates:
        try:
            email_el = WebDriverWait(driver, 3).until(EC.presence_of_element_located(sel))
            break
        except:
            continue
    for sel in pw_candidates:
        try:
            pw_el = WebDriverWait(driver, 3).until(EC.presence_of_element_located(sel))
            break
        except:
            continue
    return email_el, pw_el

def click_by_text(driver, tag, text_substr):
    xpath = f".//{tag}[contains(normalize-space(string(.)), '{text_substr}')]"
    return driver.find_elements(By.XPATH, xpath)

def main():
    driver = start_browser()
    wait = WebDriverWait(driver, WAIT_TIMEOUT)
    try:
        driver.get(LOGIN_PAGE)

        email_el, pw_el = find_input_for_login(driver)
        if email_el and pw_el:
            email_el.clear()
            email_el.send_keys(USERNAME)
            pw_el.clear()
            pw_el.send_keys(PASSWORD)
            pw_el.send_keys(Keys.ENTER)
        else:
            print("⚠️ ما لقيت الحقول تلقائياً، لازم تحدد الـ selectors يدوياً.")

        time.sleep(3)
        driver.get(EDIT_PAGE)

        try:
            candidates = click_by_text(driver, "button", "الرغبات") + click_by_text(driver, "a", "الرغبات")
            if candidates:
                candidates[0].click()
        except TimeoutException:
            print("⏳ ما ظهر عنصر الرغبات.")

        if DESIRED_TEXT.strip():
            found = False
            for tag in ("label", "li", "button", "a", "div", "span"):
                els = click_by_text(driver, tag, DESIRED_TEXT)
                if els:
                    els[0].click()
                    found = True
                    break
            if not found:
                print(f"⚠️ ما لقيت الرغبة: {DESIRED_TEXT}")

        cont = click_by_text(driver, "button", "استمر") + click_by_text(driver, "button", "استمرار")
        if cont:
            cont[0].click()
            print("✅ تم الضغط على استمرار.")
        else:
            print("⚠️ ما لقيت زر استمرار.")

        time.sleep(3)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()