from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def logout(driver):
    """
    Logs out from the application.
    """
    try:
        user_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "oxd-userdropdown-tab"))
        )
        user_dropdown.click()
        logout_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Logout"))
        )
        logout_option.click()
        print("Logged out successfully.")
    except Exception as e:
        print(f"Logout failed: {e}")
