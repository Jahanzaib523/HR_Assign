from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time


def search_and_select_from_suggestions(driver, search_text, fallback_text):
    """
    Searches for text in a search input box, checks Google-style suggestions, and selects the search text if found.

    :param driver: WebDriver instance
    :param search_text: Text to search for
    :param fallback_text: Fallback text if the search text is not found in suggestions
    """
    try:
        # Locate the input box
        input_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Type for hints...']"))  # Example XPath for Google search box
        )
        input_box.clear()
        input_box.send_keys(search_text)
        
        # Wait for suggestions to appear
        suggestions = WebDriverWait(driver, 5).until(
            EC.visibility_of_all_elements_located((By.XPATH, "//div[@role='option']" ))
        )
        
        # Print all suggestions
        for suggestion in suggestions:
            print(f"Suggestion: {suggestion.text}")

        # Check if the search text matches any suggestion
        selected = False
        for suggestion in suggestions:
            if search_text.lower() in suggestion.text.lower():
                suggestion.click()
                print(f"Selected suggestion: {suggestion.text}")
                selected = True
                break

        # If not found, clear input and type fallback text
        if not selected:
            print(f"'{search_text}' not found in suggestions. Typing fallback: '{fallback_text}'")
            input_box.clear()
            input_box.send_keys(fallback_text)
            input_box.send_keys(Keys.ARROW_DOWN)
            input_box.send_keys(Keys.ENTER)
    
    except TimeoutException:
        print("Timed out waiting for suggestions or input box.")
    except NoSuchElementException as e:
        print(f"Element not found: {e}")

def logout(driver):
    """
    Function to log out from the application.
    :param driver: WebDriver instance
    """
    try:
        # Wait for the user dropdown to be clickable
        user_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "oxd-userdropdown-tab"))
        )
        user_dropdown.click()
        print("User dropdown clicked.")

        # Wait for the logout option and click it
        logout_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Logout"))
        )
        logout_option.click()
        print("Logged out successfully.")
    except TimeoutException:
        print("Failed to log out. Please check the application or locators.")

# Main script
if __name__ == "__main__":

    # Initialize WebDriver
    driver = webdriver.Chrome()  # Ensure chromedriver is in your PATH

    # Open the login page
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    print("Page title is:", driver.title)

    try:
        # Login to the application
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'username'))
        ).send_keys("Admin")
        driver.find_element(By.NAME, "password").send_keys("admin123")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        print("Logged in successfully.")
        time.sleep(5)

        driver.maximize_window()

        #Click "Assign Leave" button
        try:
            assign_leave_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@title='Assign Leave']"))
            )
            assign_leave_button.click()
            print("Assign Leave button clicked.")
        except TimeoutException:
            print("Assign Leave button not found.")
            logout(driver)

        #  # Define input and suggestion XPaths
        
        try:
            # Locate the input field
            employee_name_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Type for hints...']"))
            )
            employee_name_field.send_keys("James Butler")  # Enter the name
            print("Entered 'James Butler' in the input field.")

            # Wait for suggestions to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='option']"))
            )
            print("Suggestions loaded.")

            time.sleep(10)

            # Use keyboard to navigate and select the suggestion
            employee_name_field.send_keys(Keys.ARROW_DOWN)  # Navigate to the first suggestion
            employee_name_field.send_keys(Keys.ENTER)       # Select the suggestion
            print("Successfully selected 'James Butler' from suggestions.")
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error: {e}")

        # # Select "Leave Type"
        
        try:
           # Wait for the dropdown to be clickable and click it to open the menu
            dropdown = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'oxd-select-text') and contains(@class, 'oxd-select-text--active')]"))
            )
            dropdown.click()

            # Wait for the dropdown options to appear and select "US - Vacation"
            option = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'oxd-select-dropdown')]//span[text()='US - Vacation']"))
            )
            option.click()
            print("Successfully selected 'US - Vacation'.")

        except Exception as e:
            print(f"An error occurred: {e}")
        
        # Set "From Date"
        try:
            from_date_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                (By.XPATH, "(//input[@placeholder='yyyy-dd-mm'])[1]")  # Index 1 for the first input
                )
            )
            from_date_field.click()
            from_date_field.send_keys("2020-19-10")  # Enter the From Date
            from_date_field.send_keys(Keys.ENTER)
            print("From Date set.")
        except TimeoutException:
            print("Failed to set From Date.")

        # Set "To Date"
        try:
            to_date_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                (By.XPATH, "(//input[@placeholder='yyyy-dd-mm'])[2]")  # Index 2 for the second input
                )
            )
            to_date_field.click()
            driver.execute_script("arguments[0].value = '';", to_date_field)  # Clear the input
            time.sleep(5)
            to_date_field.send_keys("2020-23-10")  # Enter the To Date
            to_date_field.send_keys(Keys.ENTER)
            print("To Date set.")
        except TimeoutException:
            print("Failed to set To Date.")

        # Add a comment
        try:
            comment_field = driver.find_element(By.XPATH, "//textarea")
            comment_field.send_keys("Vacation leave request for personal reasons.")
            print("Comment added.")
        except NoSuchElementException:
            print("Failed to add comment.")
            logout(driver)

        # Submit the form
        try:
            assign_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
            )
            assign_button.click()

            # Wait for success message
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'oxd-toast--success')]")
                )
            )
            print("Leave assigned successfully.")
        except TimeoutException:
            print("Error submitting the form.")
            logout(driver)

    finally:
        # Close the browser
        logout(driver)
        driver.quit()
