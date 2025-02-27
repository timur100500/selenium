import os
import time
import uuid
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--start-maximized")

CHROMEDRIVER_PATH = "C:\\driver\\chromedriver.exe"
service = ChromeService(executable_path=CHROMEDRIVER_PATH)

driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 10)
actions = ActionChains(driver)

try:
    driver.get("https://litecart.stqa.ru/admin/?app=catalog&doc=catalog")

    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("0b7dba1c77df25bf0")
    driver.find_element(By.NAME, "login").click()
    wait.until(EC.presence_of_element_located((By.ID, "box-apps-menu")))

    add_new_product_btn = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "a.button[href*='doc=edit_product']")))
    add_new_product_btn.click()

    enabled_radio = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='status'][value='1']")))
    enabled_radio.click()

    unique_product_name = f"Test Product {uuid.uuid4().hex[:8]}"
    name_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='name[en]']")))
    name_input.send_keys(unique_product_name)

    code_input = driver.find_element(By.CSS_SELECTOR, "input[name='code']")
    code_input.send_keys("TP-001")

    quantity_input = driver.find_element(By.CSS_SELECTOR, "input[name='quantity']")
    actions.double_click(quantity_input).perform()
    quantity_input.clear()
    quantity_input.send_keys("1")

    image_path = os.path.abspath("img.png")
    image_input = driver.find_element(By.CSS_SELECTOR, "input[name='new_images[]']")
    image_input.send_keys(image_path)

    time.sleep(1)

    info_tab = driver.find_element(By.XPATH, "//a[contains(text(),'Information')]")
    info_tab.click()
    time.sleep(1)

    manufacturer_select = wait.until(EC.presence_of_element_located((By.NAME, "manufacturer_id")))
    Select(manufacturer_select).select_by_value("1")

    keywords_input = driver.find_element(By.CSS_SELECTOR, "input[name='keywords']")
    keywords_input.send_keys("test keywords")

    short_desc_input = driver.find_element(By.CSS_SELECTOR, "input[name='short_description[en]']")
    short_desc_input.send_keys("Short description of product")

    head_title_input = driver.find_element(By.CSS_SELECTOR, "input[name='head_title[en]']")
    head_title_input.send_keys("Head Title")

    meta_desc_input = driver.find_element(By.CSS_SELECTOR, "input[name='meta_description[en]']")
    meta_desc_input.send_keys("Meta Description")

    time.sleep(1)

    prices_tab = driver.find_element(By.XPATH, "//a[contains(text(),'Prices')]")
    prices_tab.click()
    time.sleep(1)

    purchase_price_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='purchase_price']")))
    actions.double_click(purchase_price_input).perform()
    purchase_price_input.clear()
    purchase_price_input.send_keys("10")

    currency_select = driver.find_element(By.CSS_SELECTOR, "select[name='purchase_price_currency_code']")
    Select(currency_select).select_by_value("USD")

    time.sleep(1)

    save_button = driver.find_element(By.CSS_SELECTOR, "button[name='save']")
    save_button.click()

    catalog_url = "https://litecart.stqa.ru/admin/?app=catalog&doc=catalog"
    driver.get(catalog_url)

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.dataTable")))
    time.sleep(1)

    product_elements = driver.find_elements(By.XPATH, f"//tr[@class='row']//a[contains(text(), '{unique_product_name}')]")
    if product_elements:
        print(f"Новый товар '{unique_product_name}' успешно добавлен в каталог.")
    else:
        print(f"Товар '{unique_product_name}' не найден в каталоге.")

finally:
    time.sleep(3)
    driver.quit()