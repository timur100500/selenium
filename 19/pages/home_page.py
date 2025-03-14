from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.product_link = (By.CSS_SELECTOR, "ul.listing-wrapper.products li.product a.link")

    def open(self, url):
        """Открывает главную страницу по заданному URL."""
        self.driver.get(url)

    def open_product_page(self):
        """Кликает по первому товару и переходит на страницу товара."""
        product = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.product_link)
        )
        product.click()