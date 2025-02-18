from selenium import webdriver
from selenium.webdriver.common.by import By

# Инициализация веб-драйвера
driver = webdriver.Chrome()
driver.get("http://localhost:8080/litecart/en/")

# Находим все товары
products = driver.find_elements(By.CSS_SELECTOR, "li.product.column.shadow.hover-light")

# Проверяем, что товары найдены
if not products:
    print(" Ошибка: На странице нет товаров!")
else:
    print(f" Найдено товаров: {len(products)}")

# Проверяем, что у каждого товара ровно один стикер
for index, product in enumerate(products, start=1):
    # Получаем название товара
    name_element = product.find_element(By.CSS_SELECTOR, "div.name")
    product_name = name_element.text.strip() if name_element else "Без названия"

    # Получаем список стикеров
    stickers = product.find_elements(By.CSS_SELECTOR, "div.sticker")

    # Проверяем количество стикеров
    if len(stickers) == 1:
        print(f" '{product_name}': 1 стикер")
    else:
        print(f" Ошибка! '{product_name}': {len(stickers)} стикеров")

# Закрываем браузер
driver.quit()
