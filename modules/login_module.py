from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login(driver, username, password):
    """
    Logs into the application.
    """
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'username'))
        ).send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        print("Logged in successfully.")
    except Exception as e:
        print(f"Login failed: {e}")
