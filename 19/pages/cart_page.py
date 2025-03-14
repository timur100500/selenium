from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CartPage:
    def __init__(self, driver):
        self.driver = driver
        # Локатор кнопки удаления
        self.remove_button = (By.NAME, "remove_cart_item")
        # Локатор сообщения о пустой корзине (обновлён для <em>)
        self.empty_cart_message = (By.XPATH, "//em[text()='There are no items in your cart.']")
        # Локатор строк с товарами в таблице корзины
        self.cart_items = (By.CSS_SELECTOR, "table.dataTable tr:not(.header):not(.footer)")

    def open(self, url):
        """Открывает страницу корзины."""
        self.driver.get(url)

    def remove_all_items(self):
        """Удаляет все товары из корзины и проверяет, что она пуста."""
        while True:
            # Проверяем, есть ли товары в корзине
            items = self.driver.find_elements(*self.cart_items)
            if not items:
                # Если товаров нет, проверяем сообщение о пустой корзине
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located(self.empty_cart_message)
                    )
                    print("Корзина пуста. Сообщение 'There are no items in your cart.' отображено.")
                    break
                except:
                    print("Ошибка: Сообщение о пустой корзине не появилось, хотя товары отсутствуют.")
                    break

            try:
                # Ждём, пока кнопка удаления станет кликабельной
                remove_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(self.remove_button)
                )
                remove_button.click()
                # Ждём, пока количество товаров уменьшится или появится сообщение о пустой корзине
                WebDriverWait(self.driver, 10).until(
                    lambda driver: len(driver.find_elements(*self.cart_items)) < len(items) or
                                   EC.presence_of_element_located(self.empty_cart_message)(driver)
                )
                print(f"Удалён товар. Осталось товаров: {len(self.driver.find_elements(*self.cart_items))}")
            except Exception as e:
                print(f"Не удалось удалить товар или корзина уже пуста: {e}")
                break