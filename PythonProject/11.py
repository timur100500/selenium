import time
import uuid
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as FirefoxOptions

firefox_options = FirefoxOptions()
firefox_options.add_argument("--start-maximized")

FIREFOXDRIVER_PATH = "C:\\driver\\geckodriver.exe"

service = FirefoxService(executable_path=FIREFOXDRIVER_PATH)
driver = webdriver.Firefox(service=service, options=firefox_options)
wait = WebDriverWait(driver, 10)

try:
    driver.get("http://localhost:8080/litecart/en/create_account")

    unique_email = f"user_{uuid.uuid4()}@example.com"
    password = "password123"

    driver.find_element(By.NAME, "firstname").send_keys("John")
    driver.find_element(By.NAME, "lastname").send_keys("Doe")
    driver.find_element(By.NAME, "address1").send_keys("123 Main St")
    driver.find_element(By.NAME, "postcode").send_keys("12345")
    driver.find_element(By.NAME, "city").send_keys("Anytown")

    country_dropdown = driver.find_element(By.CLASS_NAME, "select2-selection")
    country_dropdown.click()

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "select2-results")))
    country_option = driver.find_element(By.XPATH, "//li[contains(@class, 'select2-results__option') and text()='United States']")
    country_option.click()

    driver.find_element(By.NAME, "email").send_keys(unique_email)
    driver.find_element(By.NAME, "phone").send_keys("+11234567890")

    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "confirmed_password").send_keys(password)

    newsletter_checkbox = driver.find_element(By.NAME, "newsletter")
    if newsletter_checkbox.is_selected():
        newsletter_checkbox.click()

    driver.find_element(By.NAME, "create_account").click()

    wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Logout")))
    print(f"Регистрация завершена. Email: {unique_email}")

    driver.find_element(By.LINK_TEXT, "Logout").click()
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, "New customers click here")))
    print("Выполнен logout после регистрации.")

    driver.get("http://localhost:8080/litecart/en/")

    wait.until(EC.presence_of_element_located((By.NAME, "login_form")))

    driver.find_element(By.NAME, "email").send_keys(unique_email)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "login").click()

    wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Logout")))
    print("Повторный вход выполнен успешно.")

    driver.find_element(By.LINK_TEXT, "Logout").click()
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, "New customers click here")))
    print("Финальный logout выполнен.")

finally:
    time.sleep(3)
    driver.quit()