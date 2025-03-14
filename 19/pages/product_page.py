from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class ProductPage:
    def __init__(self, driver):
        self.driver = driver
        self.size_dropdown = (By.NAME, "options[Size]")
        self.add_to_cart_button = (By.NAME, "add_cart_product")
        self.cart_quantity = (By.CSS_SELECTOR, "#cart span.quantity")

    def select_size_if_available(self):
        """Выбирает размер 'Small', если выпадающий список доступен."""
        try:
            size_select = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.size_dropdown)
            )
            Select(size_select).select_by_visible_text("Small")
            print("Размер 'Small' выбран.")
        except:
            print("Выпадающий список размеров отсутствует, продолжаем без выбора.")

    def add_to_cart(self):
        """Добавляет товар в корзину."""
        add_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.add_to_cart_button)
        )
        add_button.click()

    def wait_for_cart_update(self, expected_quantity):
        """Ждёт, пока счётчик корзины обновится до ожидаемого значения."""
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element(self.cart_quantity, expected_quantity)
        )
        print(f"Счётчик корзины обновлён до {expected_quantity}.")