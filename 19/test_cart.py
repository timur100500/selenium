from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage

# Настройка драйвера
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
CHROMEDRIVER_PATH = "C:\\driver\\chromedriver.exe"  # Укажите свой путь
service = ChromeService(executable_path=CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Создание экземпляров страниц
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)

    # Выполнение сценария
    home_page.open("http://localhost:8080/litecart/en/")  # Открываем главную страницу

    # Добавляем три товара в корзину
    for i in range(3):
        home_page.open_product_page()           # Переходим на страницу товара
        product_page.select_size_if_available() # Выбираем размер, если есть
        product_page.add_to_cart()              # Добавляем товар в корзину
        product_page.wait_for_cart_update(str(i + 1))  # Ждём обновления счётчика
        home_page.open("http://localhost:8080/litecart/en/")  # Возвращаемся на главную

    # Удаляем все товары из корзины
    cart_page.open("http://localhost:8080/litecart/en/checkout")
    cart_page.remove_all_items()

finally:
    driver.quit()