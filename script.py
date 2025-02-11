from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

service = ChromeService(executable_path='C:\driver\chromedriver\chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.get("http://localhost:8080/litecart/admin/")
time.sleep(2)
username = driver.find_element(By.NAME, "username")
username.send_keys("admin")
time.sleep(2)
password = driver.find_element(By.NAME, "password")
password.send_keys("admin")
time.sleep(2)
login_button = driver.find_element(By.NAME, "login")
login_button.click()
time.sleep(2)
driver.quit()