import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(params=["chrome", "firefox", "edge"], scope="function")
def driver(request):
    browser = request.param
    driver_path = r"C:\driver"

    if browser == "chrome":
        options = ChromeOptions()
        service = ChromeService(executable_path=f"{driver_path}\chromedriver.exe")
        driver = webdriver.Chrome(service=service, options=options)
    elif browser == "firefox":
        options = FirefoxOptions()
        service = FirefoxService(executable_path=f"{driver_path}\geckodriver.exe")
        driver = webdriver.Firefox(service=service, options=options)
    elif browser == "edge":
        options = EdgeOptions()
        service = EdgeService(executable_path=f"{driver_path}\msedgedriver.exe")
        driver = webdriver.Edge(service=service, options=options)

    yield driver
    driver.quit()


def is_gray_color(color):
    if "rgba" in color or "rgb" in color:
        values = [int(x) for x in color.split("(")[1].split(")")[0].split(",")[:3]]
        return values[0] == values[1] == values[2]
    return False


def is_red_color(color):
    if "rgba" in color or "rgb" in color:
        values = [int(x) for x in color.split("(")[1].split(")")[0].split(",")[:3]]
        return values[1] == 0 and values[2] == 0 and values[0] > 0
    return False


def test_product_details(driver):
    driver.get("http://localhost:8080/litecart/en/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "title")))

    campaigns_block = driver.find_element(By.XPATH,
                                          "//h3[@class='title' and text()='Campaigns']/following-sibling::div[@class='content']//ul[@class='listing-wrapper products']")
    first_product_link = campaigns_block.find_element(By.XPATH,
                                                      ".//li[@class='product column shadow hover-light'][1]//a[@class='link']")
    product_url = first_product_link.get_attribute("href")
    print(f"URL первого товара: {product_url}")

    main_page_name = first_product_link.find_element(By.CLASS_NAME, "name").text.strip()
    print(f"Название на главной странице: {main_page_name}")

    main_price_wrapper = first_product_link.find_element(By.CLASS_NAME, "price-wrapper")
    main_regular_price = main_price_wrapper.find_element(By.CLASS_NAME, "regular-price").text.strip()
    main_campaign_price = main_price_wrapper.find_element(By.CLASS_NAME, "campaign-price").text.strip()
    print(f"Цены на главной: Обычная: {main_regular_price}, Акционная: {main_campaign_price}")

    main_regular_elem = main_price_wrapper.find_element(By.CLASS_NAME, "regular-price")
    main_regular_strike = driver.execute_script(
        "return window.getComputedStyle(arguments[0]).getPropertyValue('text-decoration');", main_regular_elem)
    main_regular_color = driver.execute_script(
        "return window.getComputedStyle(arguments[0]).getPropertyValue('color');", main_regular_elem)
    print(
        f"На главной странице обычная цена: Зачёркнута: {'Да' if 'line-through' in main_regular_strike else 'Нет'}, Серая: {'Да' if is_gray_color(main_regular_color) else f'Нет ({main_regular_color})'}")
    if "line-through" not in main_regular_strike:
        print(f"На главной странице обычная цена не зачёркнута!")
    if not is_gray_color(main_regular_color):
        print(f"На главной странице обычная цена не серая: {main_regular_color}")

    main_campaign_elem = main_price_wrapper.find_element(By.CLASS_NAME, "campaign-price")
    main_campaign_weight = driver.execute_script(
        "return window.getComputedStyle(arguments[0]).getPropertyValue('font-weight');", main_campaign_elem)
    main_campaign_color = driver.execute_script(
        "return window.getComputedStyle(arguments[0]).getPropertyValue('color');", main_campaign_elem)
    print(
        f"На главной странице акционная цена: Жирная: {'Да' if main_campaign_weight in ['bold', '700', '800', '900'] else f'Нет ({main_campaign_weight})'}, Красная: {'Да' if is_red_color(main_campaign_color) else f'Нет ({main_campaign_color})'}")
    if main_campaign_weight not in ["bold", "700", "800", "900"]:
        print(f"На главной странице акционная цена не жирная: {main_campaign_weight}")
    if not is_red_color(main_campaign_color):
        print(f"На главной странице акционная цена не красная: {main_campaign_color}")

    main_regular_size = float(
        driver.execute_script("return window.getComputedStyle(arguments[0]).getPropertyValue('font-size');",
                              main_regular_elem).replace("px", ""))
    main_campaign_size = float(
        driver.execute_script("return window.getComputedStyle(arguments[0]).getPropertyValue('font-size');",
                              main_campaign_elem).replace("px", ""))
    print(
        f"На главной странице размеры шрифта: Обычная: {main_regular_size}px, Акционная: {main_campaign_size}px, Акционная крупнее: {'Да' if main_campaign_size > main_regular_size else 'Нет'}")
    if main_campaign_size <= main_regular_size:
        print(f"На главной странице акционная цена ({main_campaign_size}px) не крупнее обычной ({main_regular_size}px)")

    driver.get(product_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "title")))

    product_page_name = driver.find_element(By.XPATH, "//h1[@class='title']").text.strip()
    print(f"Название на странице товара: {product_page_name}")
    if main_page_name != product_page_name:
        print(f"Названия товара не совпадают!\nГлавная: {main_page_name}\nСтраница товара: {product_page_name}")

    product_price_wrapper = driver.find_element(By.CLASS_NAME, "price-wrapper")
    product_regular_price = product_price_wrapper.find_element(By.CLASS_NAME, "regular-price").text.strip()
    product_campaign_price = product_price_wrapper.find_element(By.CLASS_NAME, "campaign-price").text.strip()
    print(f"Цены на странице товара: Обычная: {product_regular_price}, Акционная: {product_campaign_price}")
    if main_regular_price != product_regular_price:
        print(f"Обычные цены не совпадают!\nГлавная: {main_regular_price}\nСтраница товара: {product_regular_price}")
    if main_campaign_price != product_campaign_price:
        print(
            f"Акционные цены не совпадают!\nГлавная: {main_campaign_price}\nСтраница товара: {product_campaign_price}")

    product_regular_elem = product_price_wrapper.find_element(By.CLASS_NAME, "regular-price")
    product_regular_strike = driver.execute_script(
        "return window.getComputedStyle(arguments[0]).getPropertyValue('text-decoration');", product_regular_elem)
    product_regular_color = driver.execute_script(
        "return window.getComputedStyle(arguments[0]).getPropertyValue('color');", product_regular_elem)
    print(
        f"На странице товара обычная цена: Зачёркнута: {'Да' if 'line-through' in product_regular_strike else 'Нет'}, Серая: {'Да' if is_gray_color(product_regular_color) else f'Нет ({product_regular_color})'}")
    if "line-through" not in product_regular_strike:
        print(f"На странице товара обычная цена не зачёркнута!")
    if not is_gray_color(product_regular_color):
        print(f"На странице товара обычная цена не серая: {product_regular_color}")

    product_campaign_elem = product_price_wrapper.find_element(By.CLASS_NAME, "campaign-price")
    product_campaign_weight = driver.execute_script(
        "return window.getComputedStyle(arguments[0]).getPropertyValue('font-weight');", product_campaign_elem)
    product_campaign_color = driver.execute_script(
        "return window.getComputedStyle(arguments[0]).getPropertyValue('color');", product_campaign_elem)
    print(
        f"На странице товара акционная цена: Жирная: {'Да' if product_campaign_weight in ['bold', '700', '800', '900'] else f'Нет ({product_campaign_weight})'}, Красная: {'Да' if is_red_color(product_campaign_color) else f'Нет ({product_campaign_color})'}")
    if product_campaign_weight not in ["bold", "700", "800", "900"]:
        print(f"На странице товара акционная цена не жирная: {product_campaign_weight}")
    if not is_red_color(product_campaign_color):
        print(f"На странице товара акционная цена не красная: {product_campaign_color}")

    product_regular_size = float(
        driver.execute_script("return window.getComputedStyle(arguments[0]).getPropertyValue('font-size');",
                              product_regular_elem).replace("px", ""))
    product_campaign_size = float(
        driver.execute_script("return window.getComputedStyle(arguments[0]).getPropertyValue('font-size');",
                              product_campaign_elem).replace("px", ""))
    print(
        f"На странице товара размеры шрифта: Обычная: {product_regular_size}px, Акционная: {product_campaign_size}px, Акционная крупнее: {'Да' if product_campaign_size > product_regular_size else 'Нет'}")
    if product_campaign_size <= product_regular_size:
        print(
            f"На странице товара акционная цена ({product_campaign_size}px) не крупнее обычной ({product_regular_size}px)")


if __name__ == "__main__":
    pytest.main(["-v"])