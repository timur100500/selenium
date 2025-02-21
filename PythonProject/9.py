import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="module")
def driver():
    chrome_options = Options()
    service = ChromeService(executable_path='C:\driver\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    # Авторизация
    driver.get("http://localhost:8080/litecart/admin/")
    username = driver.find_element(By.NAME, "username")
    username.send_keys("admin")
    password = driver.find_element(By.NAME, "password")
    password.send_keys("admin")
    login_button = driver.find_element(By.NAME, "login")
    login_button.click()
    yield driver
    driver.quit()

def test_geo_zones_alphabetical_order(driver):
    # Переход на страницу геозон
    driver.get("http://localhost:8080/litecart/admin/?app=geo_zones&doc=geo_zones")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "dataTable")))

    table = driver.find_element(By.CLASS_NAME, "dataTable")
    rows = table.find_elements(By.TAG_NAME, "tr")[1:]

    for i in range(len(rows)):

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "dataTable")))
        table = driver.find_element(By.CLASS_NAME, "dataTable")
        rows = table.find_elements(By.TAG_NAME, "tr")[1:]

        row = rows[i]
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) < 2:
            continue

        try:
            country_link = cells[0].find_element(By.TAG_NAME, "a")
            country_name = country_link.text.strip()
        except:
            continue

        country_link.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "select")))

        select_elements = driver.find_elements(By.TAG_NAME, "select")
        zones = []
        for select in select_elements:
            options = select.find_elements(By.TAG_NAME, "option")

            zone_names = [option.text.strip() for option in options if
                          option.text.strip() and option.get_attribute("value")]
            zones.extend(zone_names)

        if zones:
            print(f"Zones for {country_name}: {zones}")  # Отладочный вывод
            sorted_zones = sorted(zones)
            if zones != sorted_zones:
                print(
                    f"Для страны '{country_name}' геозоны не в алфавитном порядке!\nОжидалось: {sorted_zones}\nПолучено: {zones}")

        driver.get("http://localhost:8080/litecart/admin/?app=geo_zones&doc=geo_zones")


if __name__ == "__main__":
    pytest.main(["-v"])