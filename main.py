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
from selenium.webdriver.support.ui import Select

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


def process_text_input(label):
    input_id = label.get_attribute('for')
    if input_id:
        input_field = driver.find_element(By.ID, input_id)
        if input_field.tag_name == "input" and input_field.get_attribute("type") == "text":
            if input_field.is_enabled():
                input_field.clear()
                input_field.send_keys("5")
                print(f"Set years of experience to 5 for input field {input_id}")
            else:
                print(f"Input field {input_id} is not enabled")


def process_dropdowns():
    print("Before locating dropdowns")
    dropdowns = driver.find_elements(By.TAG_NAME, 'select')
    print("Dropdowns found:", len(dropdowns))

    for dropdown in dropdowns:
        select = Select(dropdown)
        options = select.options
        print("Options found in dropdown:", len(options))
        if options:
            if any('yes' in option.text.lower() for option in options) and any(
                    'no' in option.text.lower() for option in options):
                # Select "Yes" if it's a yes/no question
                for option in options:
                    if 'yes' in option.text.lower():
                        driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)
                        if dropdown.is_enabled():
                            select.select_by_visible_text(option.text)
                            print("Selected 'Yes' option in dropdown")
                        else:
                            print(f"Dropdown {dropdown.get_attribute('id')} is not enabled")
                        break
            else:
                # Select the last option for other dropdowns
                last_option = options[-1]
                driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)
                if dropdown.is_enabled():
                    select.select_by_visible_text(last_option.text)
                    print("Selected last option in dropdown")
                else:
                    print(f"Dropdown {dropdown.get_attribute('id')} is not enabled")


def process_label(label):
    print("Processing label:", label.text)
    input_id = label.get_attribute('for')
    if input_id:
        input_field = driver.find_element(By.ID, input_id)
        if 'years' in label.text.lower() and 'experience' in label.text.lower():
            process_text_input(label)
        elif input_field.tag_name == "select":
            process_dropdowns()
        elif input_field.tag_name == "textarea":
            # Handle multi-line text inputs
            if input_field.is_enabled():
                input_field.clear()
                input_field.send_keys("5 years")
                print(f"Set years of experience to 5 years in textarea {input_id}")
            else:
                print(f"Textarea {input_id} is not enabled")
    else:
        print(f"No input field associated with label: {label.text}")


def handle_additional_questions():
    try:
        print("Starting handle_additional_questions")

        # Handle text inputs based on label
        label_elements = driver.find_elements(By.TAG_NAME, 'label')
        print("Labels found:", len(label_elements))

        for label in label_elements:
            process_label(label)

        # Process any remaining dropdowns not handled in process_label
        process_dropdowns()

        # Click the submit button
        review_button = wait_for_clickable(By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div[2]/form/footer/div['
                                                     '2]/button[2]')
        review_button.click()
        print("Clicked the review button.")
        time.sleep(5)


    except Exception as e:
        print("An error occurred while handling additional questions:", e)


def apply_to_jobs(job_list):
    for job in job_list:
        try:
            job.click()
            time.sleep(2)  # Adjust this delay as needed

            # Debug: Print the page source or a portion of it to understand the current state
            # print(driver.page_source[:2000])  # Print the first 2000 characters of the page source

            # Wait for the Easy Apply button to appear after clicking on the job
            apply_button_xpath = "//button[contains(@aria-label, 'Easy Apply')]"

            apply_button = wait_for_clickable(By.XPATH, apply_button_xpath)

            # Scroll the apply button into view
            driver.execute_script("arguments[0].scrollIntoView(true);", apply_button)

            # Close any potential overlays that might be blocking the button
            close_overlay()

            apply_button.click()
            time.sleep(2)  # Adjust this delay as needed

            next_button_xpath = "/html/body/div[3]/div/div/div[2]/div/div[2]/form/footer/div[2]/button"
            next_button = wait_for_clickable(By.XPATH, next_button_xpath)
            next_button.click()
            time.sleep(2)

            next_button_2_xpath = "/html/body/div[3]/div/div/div[2]/div/div[2]/form/footer/div[2]/button[2]"
            next_button_2 = wait_for_clickable(By.XPATH, next_button_2_xpath)
            next_button_2.click()
            time.sleep(2)

            handle_additional_questions()
            time.sleep(2)

            # Wait for the submit button to be present and clickable
            # submit_button_xpath = '/html/body/div[3]/div/div/div[2]/div/div[2]/div/footer/div[2]/button[2]'
            submit_button_xpath = "//button[contains(@aria-label, 'Submit application')]"
            submit_button = wait_for_clickable(By.XPATH, submit_button_xpath)
            submit_button.click()
            print("Submitted the application.")
        except TimeoutException:
            print(f"TimeoutException: The apply button was not found in the given time. XPATH: {apply_button_xpath}")
        except StaleElementReferenceException:
            print("StaleElementReferenceException: The element is no longer attached to the DOM.")
        except ElementClickInterceptedException:
            print("ElementClickInterceptedException: Another element is blocking the button.")
        except Exception as e:
            print(f"An error occurred while applying for a job: {e}")


try:
    # Open LinkedIn Jobs page
    driver.get(
        'https://www.linkedin.com/jobs/search/?currentJobId=3951086724&distance=25&f_AL=true&f_E=2%2C3%2C4&f_WT=1%2C3'
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
