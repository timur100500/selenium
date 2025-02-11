import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver(request):
    options = Options()
    options.headless = False  # Отключаем headless-режим
    service = ChromeService(executable_path='C:\driver\chromedriver\chromedriver.exe')
    wd = webdriver.Chrome(service=service, options=options)
    request.addfinalizer(wd.quit)
    return wd

def script(driver):
    driver.get("http://www.google.com/")
    search_box = driver.find_element(By.NAME, "q")  # Находим поле поиска
    search_box.send_keys("webdriver")
    search_box.submit()  # Отправляем форму поиска
    WebDriverWait(driver, 10).until(EC.title_is("webdriver - Поиск в Google"))

def test_google_search(driver):
    script(driver)