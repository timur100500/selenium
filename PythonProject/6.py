import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--start-maximized")

CHROMEDRIVER_PATH = "C:\\driver\\chromedriver.exe"
service = ChromeService(executable_path=CHROMEDRIVER_PATH)

driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    driver.get("http://localhost:8080/litecart/admin/")

    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("admin")
    driver.find_element(By.NAME, "login").click()

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Appearence']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Template']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Logotype']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Catalog']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Product Groups']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Option Groups']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Manufacturers']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Suppliers']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Delivery Statuses']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Sold Out Statuses']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Quantity Units']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='CSV Import/Export']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Countries']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Customers']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='CSV Import/Export']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Newsletter']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Geo Zones']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Languages']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Storage Encoding']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Modules']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Background Jobs']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Customer']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Shipping']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Payment']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Order Total']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Order Success']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Order Action']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Orders']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Order Statuses']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Pages']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Reports']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Monthly Sales']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Most Sold Products']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Settings']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Store Info']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Defaults']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='General']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Listings']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Images']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Checkout']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Advanced']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Security']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Slides']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Tax']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Tax Classes']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Tax Rates']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Translations']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Search Translations']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Scan Files']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='CSV Import/Export']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='Users']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='vQmods']/..").click()
    time.sleep(0.25)

    driver.find_element(By.XPATH, "//span[@class='name' and text()='vQmods']/..").click()
    time.sleep(0.25)


except Exception as e:
    print(f"Ошибка: {e}")

finally:
    driver.quit()
