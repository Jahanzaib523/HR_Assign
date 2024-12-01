from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from modules.overlay_handler_module import handle_leave_assignment_overlay
import time

def assign_leave(driver, employee_name, leave_type, from_date, to_date, comment):
    """
    Assigns leave to an employee.
    """
    try:
        # Click "Assign Leave" button
        assign_leave_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@title='Assign Leave']"))
        )
        assign_leave_button.click()
        print("Assign Leave button clicked.")

        # Select Employee Name
        employee_name_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Type for hints...']"))
        )
        employee_name_field.send_keys(employee_name)
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='option']"))
        )

        time.sleep(5)

        employee_name_field.send_keys(Keys.ARROW_DOWN)
        employee_name_field.send_keys(Keys.ENTER)
        print(f"Employee '{employee_name}' selected.")

        # Select Leave Type
        dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'oxd-select-text')]"))
        )
        dropdown.click()
        option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//span[text()='{leave_type}']"))
        )
        option.click()
        print(f"Leave type '{leave_type}' selected.")

        # Set Dates
        set_date(driver, "(//input[@placeholder='yyyy-dd-mm'])[1]", from_date, "From Date")
        set_date(driver, "(//input[@placeholder='yyyy-dd-mm'])[2]", to_date, "To Date")

        # Add Comment
        comment_field = driver.find_element(By.XPATH, "//textarea")
        comment_field.send_keys(comment)
        print("Comment added.")

       # Submit the form with overlay handling
        try:
            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
            )

            # Scroll into view to ensure visibility
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)

            try:
                # Attempt to click the button
                submit_button.click()
                print("Submit button clicked.")
            except ElementClickInterceptedException:
                print("Submit button click intercepted. Handling overlay...")
                handle_leave_assignment_overlay(driver, confirm=True)  # Handle the overlay and retry

                # Retry clicking the button
                submit_button.click()
                print("Submit button clicked after handling overlay.")

            # Wait for success message
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'oxd-toast--success')]"))
            )
            print("Leave assignment successful.")
        except TimeoutException:
            print("Submit button or success message not found.")
    except TimeoutException as e:
        print(f"Timeout during leave assignment: {e}")
    except ElementClickInterceptedException as e:
        print(f"Element click intercepted: {e}")

def set_date(driver, xpath, date, label):
    """
    Sets a date in a date input field, ensuring the field is cleared before entering new text.
    """
    try:
        # Wait for the field to be present
        date_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        
        # Scroll into view to ensure visibility
        driver.execute_script("arguments[0].scrollIntoView(true);", date_field)

        # Use JavaScript to clear the value
        driver.execute_script("arguments[0].value = '';", date_field)

        # Ensure the field is empty by simulating manual clearing
        date_field.click()  # Ensure the field is active
        for _ in range(10):  # Simulate pressing backspace multiple times
            date_field.send_keys(Keys.BACKSPACE)

        # Enter the new date
        date_field.send_keys(date)
        date_field.send_keys(Keys.ENTER)
        print(f"{label} set to {date}.")
    except TimeoutException:
        print(f"Failed to set {label}: Field not found or timeout occurred.")
    except Exception as e:
        print(f"Error setting {label}: {e}")
