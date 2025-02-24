from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("http://localhost:8080/litecart/en/")

products = driver.find_elements(By.CSS_SELECTOR, "li.product")

if not products:
    print("Ошибка: На странице нет товаров!")
else:
    print(f"Найдено товаров: {len(products)}")

for index, product in enumerate(products, start=1):
    name_element = product.find_element(By.CSS_SELECTOR, "div.name")
    product_name = name_element.text.strip() if name_element else "Без названия"

    stickers = product.find_elements(By.CSS_SELECTOR, "div.sticker")

    if len(stickers) == 1:
        print(f"'{product_name}': 1 стикер")
    else:
        print(f"Ошибка! '{product_name}': {len(stickers)} стикеров")

driver.quit()