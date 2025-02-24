import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="module")
def driver():
    options = Options()
    service = ChromeService(executable_path=r"C:\driver\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("http://localhost:8080/litecart/admin/")
    username = driver.find_element(By.NAME, "username")
    username.send_keys("admin")
    password = driver.find_element(By.NAME, "password")
    password.send_keys("admin")
    login_button = driver.find_element(By.NAME, "login")
    login_button.click()
    yield driver
    driver.quit()


def test_admin_menu_headers(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "box-apps-menu")))

    menu = driver.find_element(By.ID, "box-apps-menu")
    top_level_items = menu.find_elements(By.XPATH, "//li[starts-with(@id, 'app-')]")

    for i in range(len(top_level_items)):
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "box-apps-menu")))
        menu = driver.find_element(By.ID, "box-apps-menu")
        top_level_items = menu.find_elements(By.XPATH, "//li[starts-with(@id, 'app-')]")

        top_item = top_level_items[i]
        top_link = top_item.find_element(By.XPATH, "./a")
        top_link_text = top_link.find_element(By.CLASS_NAME, "name").text.strip()
        print(f"Переход по верхнему пункту меню: '{top_link_text}'")

        top_link.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "box-apps-menu")))

        try:
            header = driver.find_element(By.TAG_NAME, "h1")
            print(f"Заголовок на странице: '{header.text.strip()}'")
        except:
            print(f"Ошибка: На странице верхнего пункта '{top_link_text}' отсутствует заголовок <h1>!")

        try:
            WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CLASS_NAME, "docs")))
            sub_items = driver.find_elements(By.XPATH, "//ul[@class='docs']//a")
        except:
            print(f"У пункта '{top_link_text}' нет вложенных элементов.")
            continue  # Переходим к следующему верхнему пункту

        for sub_index in range(len(sub_items)):
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "docs")))
            sub_items = driver.find_elements(By.XPATH, "//ul[@class='docs']//a")
            sub_link = sub_items[sub_index]
            sub_link_text = sub_link.text.strip()
            print(f"Переход по вложенному пункту меню: '{sub_link_text}'")

            sub_link.click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "box-apps-menu")))

            try:
                header = driver.find_element(By.TAG_NAME, "h1")
                print(f"Заголовок на странице: '{header.text.strip()}'")
            except:
                print(f"Ошибка: На странице вложенного пункта '{sub_link_text}' отсутствует заголовок <h1>!")


if __name__ == "__main__":
    pytest.main(["-v"])