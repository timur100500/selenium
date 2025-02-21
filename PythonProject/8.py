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
    driver.get("http://localhost:8080/litecart/admin/")
    username = driver.find_element(By.NAME, "username")
    username.send_keys("admin")
    password = driver.find_element(By.NAME, "password")
    password.send_keys("admin")
    login_button = driver.find_element(By.NAME, "login")
    login_button.click()
    yield driver
    driver.quit()


def test_countries_and_zones_alphabetical_order(driver):

    driver.get("http://localhost:8080/litecart/admin/?app=countries&doc=countries")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "dataTable")))

    table = driver.find_element(By.CLASS_NAME, "dataTable")
    rows = table.find_elements(By.TAG_NAME, "tr")[1:]

    country_elements = table.find_elements(By.XPATH, ".//td[5]/a")
    countries = [elem.text.strip() for elem in country_elements if elem.text.strip()]
    assert countries, "Список стран пуст!"
    assert countries == sorted(
        countries), f"Страны не в алфавитном порядке!\nОжидалось: {sorted(countries)}\nПолучено: {countries}"

    for i in range(len(rows)):
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "dataTable")))
        table = driver.find_element(By.CLASS_NAME, "dataTable")
        rows = table.find_elements(By.TAG_NAME, "tr")[1:]

        row = rows[i]
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) < 7:
            continue

        try:
            country_link = cells[4].find_element(By.TAG_NAME, "a")
            country_name = country_link.text.strip()
        except:
            continue

        zones_count = cells[5].text.strip()
        if not zones_count.isdigit() or int(zones_count) == 0:
            continue

        country_link.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[contains(@name, 'zones')]")))

        zone_inputs = driver.find_elements(By.XPATH, "//input[contains(@name, 'zones') and contains(@name, '[name]')]")
        zones = [input_elem.get_attribute("value").strip() for input_elem in zone_inputs if
                 input_elem.get_attribute("value").strip()]

        if zones != sorted(zones):
                print(
                    f"Для страны '{country_name}' геозоны не в алфавитном порядке!\nОжидалось: {sorted(zones)}\nПолучено: {zones}")

        driver.get("http://localhost:8080/litecart/admin/?app=countries&doc=countries")


if __name__ == "__main__":
    pytest.main(["-v"])