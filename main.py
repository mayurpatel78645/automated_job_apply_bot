# import os
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, NoSuchWindowException, ElementClickInterceptedException, \
#     StaleElementReferenceException
# import time
# from dotenv import load_dotenv
#
# # Load environment variables from .env file
# load_dotenv()
#
# # Retrieve environment variables
# linkedin_email = os.getenv('LINKEDIN_EMAIL')
# linkedin_password = os.getenv('LINKEDIN_PASSWORD')
#
# # Initialize WebDriver
# driver = webdriver.Chrome()
#
#
# def wait_for_element(by, value, timeout=10):
#     return WebDriverWait(driver, timeout).until(
#         EC.presence_of_element_located((by, value))
#     )
#
#
# def wait_for_clickable(by, value, timeout=10):
#     return WebDriverWait(driver, timeout).until(
#         EC.element_to_be_clickable((by, value))
#     )
#
#
# def close_overlay():
#     try:
#         # Example of closing a known overlay; adjust the selector as needed
#         overlay_close_button = driver.find_element(By.CSS_SELECTOR, ".overlay-close-button")
#         if overlay_close_button.is_displayed():
#             overlay_close_button.click()
#             print("Closed an overlay.")
#     except Exception as e:
#         print("No overlay found or failed to close overlay:", e)
#
#
# def apply_to_jobs(job_list):
#     for job in job_list:
#         retries = 3  # Number of retry attempts for stale element reference
#         while retries > 0:
#             try:
#                 job.click()
#                 time.sleep(2)  # Adjust this delay as needed
#
#                 # Wait for the Easy Apply button to appear after clicking on the job
#                 apply_button = wait_for_clickable(By.XPATH, "/html/body/div[5]/div[3]/div[4]/div/div/main/div/div["
#                                                             "2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div["
#                                                             "1]/div[1]/div[6]/div/div/div/button")
#
#                 # Scroll the apply button into view
#                 driver.execute_script("arguments[0].scrollIntoView(true);", apply_button)
#
#                 # Close any potential overlays that might be blocking the button
#                 close_overlay()
#
#                 apply_button.click()
#                 time.sleep(2)  # Adjust this delay as needed
#
#                 # Complete the application form here if needed
#
#                 break  # Break the loop if successful
#             except StaleElementReferenceException:
#                 print("StaleElementReferenceException: The element is no longer attached to the DOM. Retrying...")
#                 retries -= 1
#                 time.sleep(2)  # Wait a bit before retrying
#                 job_list = driver.find_elements(By.CLASS_NAME, "jobs-search-results__list-item")  # Re-find the job list
#                 break  # Exit the inner loop to reattempt the outer loop
#             except ElementClickInterceptedException:
#                 print("ElementClickInterceptedException: Another element is blocking the button. Retrying...")
#                 retries -= 1
#                 time.sleep(2)  # Wait a bit before retrying
#             except TimeoutException:
#                 print("TimeoutException: The apply button was not found in the given time.")
#                 break
#             except Exception as e:
#                 print(f"An error occurred while applying for a job: {e}")
#                 break  # Exit the inner loop on other exceptions
#
#
# try:
#     # Open LinkedIn Jobs page
#     driver.get(
#         'https://www.linkedin.com/jobs/search/?currentJobId=3941807035&distance=25&f_AL=true&f_E=2%2C3%2C4&f_WT=1%2C3'
#         '%2C2&geoId=101174742&keywords=software%20developer&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true')
#
#     # Click on the sign-in button
#     sign_in_button = wait_for_clickable(By.CLASS_NAME, "nav__button-secondary")
#     sign_in_button.click()
#
#     # Enter email
#     email = wait_for_element(By.ID, "username")
#     email.send_keys(linkedin_email)
#
#     # Enter password
#     password = wait_for_element(By.ID, "password")
#     password.send_keys(linkedin_password)
#     password.send_keys(Keys.RETURN)
#
#     # Wait for login to complete
#     time.sleep(5)  # Adjust this delay as needed
#
#     # Find jobs
#     job_list = WebDriverWait(driver, 20).until(
#         EC.presence_of_all_elements_located((By.CLASS_NAME, "jobs-search-results__list-item"))
#     )
#
#     apply_to_jobs(job_list)
#
# finally:
#     driver.quit()


import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchWindowException, ElementClickInterceptedException, \
    StaleElementReferenceException
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
linkedin_email = os.getenv('LINKEDIN_EMAIL')
linkedin_password = os.getenv('LINKEDIN_PASSWORD')

# Initialize WebDriver
driver = webdriver.Chrome()


def wait_for_element(by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )


def wait_for_clickable(by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    )


def close_overlay():
    try:
        # Example of closing a known overlay; adjust the selector as needed
        overlay_close_button = driver.find_element(By.CSS_SELECTOR, ".overlay-close-button")
        if overlay_close_button.is_displayed():
            overlay_close_button.click()
            print("Closed an overlay.")
    except Exception as e:
        print("No overlay found or failed to close overlay:", e)


def handle_additional_questions():
    try:
        # Example handling for different types of fields, adjust as needed
        text_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="text"]')
        for input_field in text_inputs:
            input_field.send_keys("4")  # Provide a suitable answer

        radio_buttons = driver.find_elements(By.CSS_SELECTOR, 'input[type="radio"]')
        if radio_buttons:
            radio_buttons[0].click()  # Select the first option

        checkboxes = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')
        for checkbox in checkboxes:
            if not checkbox.is_selected():
                checkbox.click()  # Select the checkbox

        # Handle dropdowns, text areas, etc., similarly

        # Click the submit button
        submit_button = wait_for_clickable(By.CSS_SELECTOR, 'button[aria-label="Submit application"]')
        submit_button.click()
        print("Submitted the application.")

    except Exception as e:
        print("An error occurred while handling additional questions:", e)


def apply_to_jobs(job_list):
    for job in job_list:
        try:
            job.click()
            time.sleep(2)  # Adjust this delay as needed

            # Wait for the Easy Apply button to appear after clicking on the job
            apply_button = wait_for_clickable(By.XPATH, "/html/body/div[5]/div[3]/div[4]/div/div/main/div/div[2]/div["
                                                        "2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div[1]/div["
                                                        "6]/div/div/div/button")

            # Scroll the apply button into view
            driver.execute_script("arguments[0].scrollIntoView(true);", apply_button)

            # Close any potential overlays that might be blocking the button
            close_overlay()

            apply_button.click()
            time.sleep(2)  # Adjust this delay as needed
            next_button = wait_for_clickable(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div[2]/form/footer/div["
                                                       "2]/button")
            next_button.click()
            time.sleep(2)

            next_button_ = wait_for_clickable(By.XPATH,
                                              "/html/body/div[3]/div/div/div[2]/div/div[2]/form/footer/div[2]/button[2]")
            next_button_.click()
            # Complete the application form here if needed

        except StaleElementReferenceException:
            print("StaleElementReferenceException: The element is no longer attached to the DOM.")
        except ElementClickInterceptedException:
            print("ElementClickInterceptedException: Another element is blocking the button.")
        except TimeoutException:
            print("TimeoutException: The apply button was not found in the given time.")
        except Exception as e:
            print(f"An error occurred while applying for a job: {e}")


try:
    # Open LinkedIn Jobs page
    driver.get(
        'https://www.linkedin.com/jobs/search/?currentJobId=3941807035&distance=25&f_AL=true&f_E=2%2C3%2C4&f_WT=1%2C3'
        '%2C2&geoId=101174742&keywords=software%20developer&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true')

    # Click on the sign-in button
    sign_in_button = wait_for_clickable(By.CLASS_NAME, "nav__button-secondary")
    sign_in_button.click()

    # Enter email
    email = wait_for_element(By.ID, "username")
    email.send_keys(linkedin_email)

    # Enter password
    password = wait_for_element(By.ID, "password")
    password.send_keys(linkedin_password)
    password.send_keys(Keys.RETURN)

    # Wait for login to complete
    time.sleep(5)  # Adjust this delay as needed

    # Find jobs
    job_list = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "jobs-search-results__list-item"))
    )

    apply_to_jobs(job_list)

finally:
    driver.quit()
