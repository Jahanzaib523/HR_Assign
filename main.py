from selenium import webdriver
from modules.login_module import login
from modules.logout_module import logout
from modules.leave_assignment_module import assign_leave
import time

if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    print("Page title is:", driver.title)

    try:
        # Login to the application
        login(driver, "Admin", "admin123")

        # Perform leave assignment
        assign_leave(
            driver,
            employee_name="James Butler",
            leave_type="US - Vacation",
            from_date="2020-10-19",
            to_date="2020-10-23",
            comment="Vacation leave request for personal reasons."
        )

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        # Logout and close the browser
        logout(driver)
        driver.quit()
