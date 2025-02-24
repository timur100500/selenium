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

def test_geo_zones_alphabetical_order(driver):
    driver.get("http://localhost:8080/litecart/admin/?app=geo_zones&doc=geo_zones")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "dataTable")))

    table = driver.find_element(By.CLASS_NAME, "dataTable")
    rows = table.find_elements(By.TAG_NAME, "tr")[1:]

    country_elements = table.find_elements(By.XPATH, ".//td[3]/a")
    countries = [elem.text.strip() for elem in country_elements if elem.text.strip()]
    assert countries, "Список стран пуст!"
    assert countries == sorted(countries), f"Страны не в алфавитном порядке!\nОжидалось: {sorted(countries)}\nПолучено: {countries}"

    for i in range(len(rows)):
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "dataTable")))
        table = driver.find_element(By.CLASS_NAME, "dataTable")
        rows = table.find_elements(By.TAG_NAME, "tr")[1:]

        row = rows[i]
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) < 5:
            print(f"Пропущена строка {i + 1}: недостаточно ячеек ({len(cells)})")
            continue

        try:
            country_link = cells[2].find_element(By.TAG_NAME, "a")
            country_name = country_link.text.strip()
        except Exception as e:
            print(f"Ошибка в строке {i + 1}: не удалось найти ссылку на страну. Причина: {str(e)}")
            continue

        zones_count = cells[3].text.strip()
        if not zones_count.isdigit() or int(zones_count) == 0:
            print(f"У страны '{country_name}' нет зон для проверки ({zones_count})")
            continue

        print(f"Открываем страницу страны: '{country_name}'")
        country_link.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "dataTable")))

        zone_table = driver.find_element(By.CLASS_NAME, "dataTable")
        zone_rows = zone_table.find_elements(By.TAG_NAME, "tr")[1:]
        zones = []
        for zone_row in zone_rows:
            zone_cells = zone_row.find_elements(By.TAG_NAME, "td")
            if len(zone_cells) >= 3:
                zone_name = zone_cells[2].text.strip()
                if zone_name:
                    zones.append(zone_name)

        if zones:
            print(f"Zones for {country_name}: {zones}")
            sorted_zones = sorted(zones)
            if zones != sorted_zones:
                print(f"Для страны '{country_name}' геозоны не в алфавитном порядке!\nОжидалось: {sorted_zones}\nПолучено: {zones}")
            else:
                print(f"Для страны '{country_name}' геозоны в алфавитном порядке.")
        else:
            print(f"Для страны '{country_name}' не найдено видимых геозон.")

        driver.get("http://localhost:8080/litecart/admin/?app=geo_zones&doc=geo_zones")

if __name__ == "__main__":
    pytest.main(["-v"])