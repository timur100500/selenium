import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--start-maximized")

CHROMEDRIVER_PATH = "C:\\driver\\chromedriver.exe"
service = ChromeService(executable_path=CHROMEDRIVER_PATH)

driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 10)

try:
    driver.get("http://localhost:8080/litecart/en/")
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "listing-wrapper")))

    for i in range(3):
        # 2. Открываем первый товар из списка
        products_list = driver.find_element(By.CLASS_NAME, "listing-wrapper")
        first_product = products_list.find_element(By.CSS_SELECTOR, "li.product.column.shadow.hover-light")
        product_link = first_product.find_element(By.CLASS_NAME, "link")
        product_link.click()

        wait.until(EC.presence_of_element_located((By.NAME, "add_cart_product")))

        try:
            size_select = driver.find_element(By.NAME, "options[Size]")
            Select(size_select).select_by_value("Small")
            print(f"Выбран размер 'Small' для товара {i + 1}")
        except:
            print(f"Выпадающий список размеров не найден для товара {i + 1}")

        add_button = driver.find_element(By.NAME, "add_cart_product")
        try:
            cart_quantity = driver.find_element(By.CLASS_NAME, "quantity")
            current_quantity = int(cart_quantity.text) if cart_quantity.text.isdigit() else 0
        except:
            current_quantity = 0

        add_button.click()

        expected_quantity = str(current_quantity + 1)
        try:
            wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "quantity"), expected_quantity))
            print(f"Товар {i + 1} добавлен. Количество в корзине: {expected_quantity}")
        except:
            print(f"Ошибка: Счётчик не обновился до {expected_quantity} после добавления товара {i + 1}")

        driver.get("http://localhost:8080/litecart/en/")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "listing-wrapper")))

    checkout_link = driver.find_element(By.LINK_TEXT, "Checkout »")
    checkout_link.click()
    wait.until(EC.presence_of_element_located((By.ID, "order_confirmation-wrapper")))

    while True:
        try:
            remove_button = driver.find_element(By.NAME, "remove_cart_item")
            remove_button.click()

            try:
                wait.until(EC.staleness_of(remove_button))
                try:

                    wait.until(EC.presence_of_element_located((By.ID, "order_confirmation-wrapper")))
                    print("Удалён товар. Корзина обновлена.")
                except:
                    wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "There are no items in your cart."))
                    print("Все товары удалены из корзины. Появилось сообщение 'There are no items in your cart.'")
                    break
            except:
                print("Ошибка: Корзина не обновилась после удаления товара")
        except:
            try:
                wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "There are no items in your cart."))
                print("Все товары удалены из корзины. Появилось сообщение 'There are no items in your cart.'")
                break
            except:
                print("Ошибка: Не удалось подтвердить удаление всех товаров")

finally:
    time.sleep(3)
    driver.quit()