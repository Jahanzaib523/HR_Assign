from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def handle_leave_assignment_overlay(driver, confirm=True):
    """
    Handles the overlay that appears during leave assignment.
    """
    try:
        overlay = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'oxd-dialog-sheet')]"))
        )
        print("Overlay detected.")
        if confirm:
            button = overlay.find_element(By.XPATH, ".//button[contains(@class, 'oxd-button--secondary')]")
        else:
            button = overlay.find_element(By.XPATH, ".//button[contains(@class, 'oxd-button--ghost')]")
        button.click()
        WebDriverWait(driver, 5).until(EC.invisibility_of_element_located((By.XPATH, "//div[contains(@class, 'oxd-dialog-sheet')]")))
        print("Overlay handled successfully.")
    except Exception as e:
        print(f"Error handling overlay: {e}")
