from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def check_browser_logs():
    options = webdriver.ChromeOptions()
    options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("http://localhost:8080/litecart/admin/")
        driver.find_element(By.NAME, "username").send_keys("admin")
        driver.find_element(By.NAME, "password").send_keys("admin")
        driver.find_element(By.NAME, "login").click()

        driver.get("http://localhost:8080/litecart/admin/?app=catalog&doc=catalog&category_id=1")

        products = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//table[@class='dataTable']//tr[@class='row']//td[3]/a[contains(@href, 'product_id')]")
        ))

        for index in range(len(products)):

            products = driver.find_elements(
                By.XPATH, "//table[@class='dataTable']//tr[@class='row']//td[3]/a[contains(@href, 'product_id')]"
            )
            product = products[index]

            driver.get_log("browser")

            product_url = product.get_attribute("href")
            product_name = product.text

            driver.execute_script("window.open(arguments[0]);", product_url)
            driver.switch_to.window(driver.window_handles[1])

            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            logs = driver.get_log("browser")
            if logs:
                print(f"\nОбнаружены сообщения в логе для товара '{product_name}':")
                for log in logs:
                    print(f"Уровень: {log['level']}, Сообщение: {log['message']}")
            else:
                print(f"\nТовар '{product_name}': сообщений в логе нет")

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

    finally:
        driver.quit()


if __name__ == "__main__":
    check_browser_logs()