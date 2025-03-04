from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def test_external_links():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("http://localhost:8080/litecart/admin/?app=countries&doc=countries")

        driver.find_element(By.NAME, "username").send_keys("admin")
        driver.find_element(By.NAME, "password").send_keys("admin")
        driver.find_element(By.NAME, "login").click()

        edit_button = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "a[title='Edit']")))
        edit_button.click()

        external_links = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//i[contains(@class, 'fa-external-link')]/ancestor::a")))

        main_window = driver.current_window_handle

        for link in external_links:

            windows_before = driver.window_handles

            link.click()

            wait.until(lambda d: len(d.window_handles) == len(windows_before) + 1)
            new_window = [w for w in driver.window_handles if w not in windows_before][0]
            driver.switch_to.window(new_window)
            driver.close()
            driver.switch_to.window(main_window)

        print("Все внешние ссылки открываются в новых окнах")

    finally:
        driver.quit()


if __name__ == "__main__":
    test_external_links()