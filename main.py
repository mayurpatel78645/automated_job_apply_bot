# #todo automate the radio buttons
# #todo handle the text areas and text boxes
# #todo handle captcha
#
# import os
# import time
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait, Select
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, \
#     StaleElementReferenceException
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
#     return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
#
#
# def wait_for_clickable(by, value, timeout=10):
#     return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, value)))
#
#
# def close_overlay():
#     try:
#         overlay_close_button = driver.find_element(By.CSS_SELECTOR, ".overlay-close-button")
#         if overlay_close_button.is_displayed():
#             overlay_close_button.click()
#     except Exception as e:
#         pass  # Overlay not found or failed to close
#
#
# def process_text_input(label):
#     input_id = label.get_attribute('for')
#     if input_id:
#         input_field = driver.find_element(By.ID, input_id)
#         if input_field.tag_name == "input" and input_field.get_attribute("type") == "text":
#             if input_field.is_enabled():
#                 input_field.clear()
#                 input_field.send_keys("5")
#
#
# def get_parent_label(element):
#     return driver.execute_script(
#         "return arguments[0].closest('label')", element)
#
#
# def process_radio_buttons():
#     radio_buttons = driver.find_elements(By.XPATH, '//input[@type="radio"]')
#     print("Radio buttons found:", len(radio_buttons))
#     for radio_button in radio_buttons:
#         parent_label = get_parent_label(radio_button)
#         print("Parent label:", parent_label)
#         if parent_label:
#             if 'require sponsorship' in parent_label.text.lower():
#                 print("Found radio button:", parent_label.text)
#                 if 'no' in parent_label.text.lower():
#                     print("Selecting 'No' radio button")
#                     radio_button.click()
#                 else:
#                     # Select "Yes" as the first option
#                     first_radio_button = parent_label.find_element(By.XPATH, './preceding::input[@type="radio"]')
#                     print("Selecting 'Yes' radio button")
#                     if first_radio_button:
#                         first_radio_button.click()
#                         print("Selected 'Yes' radio button")
#
#
# def process_dropdowns():
#     dropdowns = driver.find_elements(By.TAG_NAME, 'select')
#     for dropdown in dropdowns:
#         select = Select(dropdown)
#         options = select.options
#         if options:
#             if any('yes' in option.text.lower() for option in options) and any(
#                     'no' in option.text.lower() for option in options):
#                 for option in options:
#                     if 'yes' in option.text.lower():
#                         driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)
#                         if dropdown.is_enabled():
#                             select.select_by_visible_text(option.text)
#                             break
#             else:
#                 last_option = options[-1]
#                 driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)
#                 if dropdown.is_enabled():
#                     select.select_by_visible_text(last_option.text)
#
#
# def process_label(label):
#     input_id = label.get_attribute('for')
#     if input_id:
#         input_field = driver.find_element(By.ID, input_id)
#         if 'years' in label.text.lower() and 'experience' in label.text.lower():
#             process_text_input(label)
#         elif input_field.tag_name == "select":
#             process_dropdowns()
#         elif input_field.tag_name == "textarea":
#             if input_field.is_enabled():
#                 input_field.clear()
#                 input_field.send_keys("5 years")
#
#
# def handle_additional_questions():
#     try:
#         label_elements = driver.find_elements(By.TAG_NAME, 'label')
#         for label in label_elements:
#             process_label(label)
#         process_radio_buttons()
#         process_dropdowns()
#         review_button_xpath = "//button[contains(@aria-label, 'Review')]"
#         review_button = wait_for_clickable(By.XPATH, review_button_xpath)
#         review_button.click()
#         time.sleep(5)
#     except Exception as e:
#         print(f"An error occurred while handling additional questions: {e}")
#
#
# def apply_to_jobs(job_list):
#     for job in job_list:
#         try:
#             job.click()
#             time.sleep(2)
#             apply_button = wait_for_clickable(By.CLASS_NAME, "jobs-apply-button--top-card")
#             driver.execute_script("arguments[0].scrollIntoView(true);", apply_button)
#             close_overlay()
#             apply_button.click()
#             time.sleep(2)
#             for _ in range(2):
#                 next_button_xpath = "//button[contains(@aria-label, 'Continue')]"
#                 next_button = wait_for_clickable(By.XPATH, next_button_xpath)
#                 next_button.click()
#                 time.sleep(2)
#             handle_additional_questions()
#             time.sleep(2)
#             submit_button_xpath = "//button[contains(@aria-label, 'Submit application')]"
#             submit_button = wait_for_clickable(By.XPATH, submit_button_xpath)
#             submit_button.click()
#             print("Submitted the application.")
#         except TimeoutException:
#             print("TimeoutException: The apply button was not found in the given time.")
#         except StaleElementReferenceException:
#             print("StaleElementReferenceException: The element is no longer attached to the DOM.")
#         except ElementClickInterceptedException:
#             print("ElementClickInterceptedException: Another element is blocking the button.")
#         except Exception as e:
#             print(f"An error occurred while applying for a job: {e}")
#
#
# try:
#     driver.get('https://www.linkedin.com/jobs/search/?currentJobId=3951086724&distance=25&f_AL=true&f_E=2%2C3%2C4'
#                '&f_WT=1%2C3%2C2&geoId=101174742&keywords=software%20developer&origin=JOB_SEARCH_PAGE_JOB_FILTER'
#                '&refresh=true')
#     sign_in_button = wait_for_clickable(By.CLASS_NAME, "nav__button-secondary")
#     sign_in_button.click()
#     email = wait_for_element(By.ID, "username")
#     email.send_keys(linkedin_email)
#     password = wait_for_element(By.ID, "password")
#     password.send_keys(linkedin_password)
#     password.send_keys(Keys.RETURN)
#     time.sleep(5)
#     job_list = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "jobs-search"
#                                                                                                    "-results__list-item")))
#     apply_to_jobs(job_list)
# finally:
#     driver.quit()


import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchWindowException, ElementClickInterceptedException, \
    StaleElementReferenceException
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
linkedin_email = os.getenv('LINKEDIN_EMAIL')
linkedin_password = os.getenv('LINKEDIN_PASSWORD')

# Initialize WebDriver
driver = webdriver.Chrome()


def wait_for_element(by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))


def wait_for_clickable(by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, value)))


def close_overlay():
    try:
        overlay_close_button = driver.find_element(By.CSS_SELECTOR, ".overlay-close-button")
        if overlay_close_button.is_displayed():
            overlay_close_button.click()
    except Exception as e:
        pass  # Overlay not found or failed to close


def process_text_input(label):
    input_id = label.get_attribute('for')
    if input_id:
        input_field = driver.find_element(By.ID, input_id)
        if input_field.tag_name == "input" and input_field.get_attribute("type") == "text":
            if input_field.is_enabled():
                input_field.clear()
                input_field.send_keys("5")


def process_text_area(label):
    input_id = label.get_attribute('for')
    if input_id:
        input_field = driver.find_element(By.ID, input_id)
        if input_field.tag_name == "textarea":
            if input_field.is_enabled():
                input_field.clear()
                input_field.send_keys("5 years")


def get_associated_label(element):
    try:
        # Try to find a label element that is an ancestor
        parent_label = element.find_element(By.XPATH, "ancestor::label")
        if parent_label:
            return parent_label
    except:
        pass

    try:
        # Try to find a label element using the 'for' attribute
        element_id = element.get_attribute("id")
        if element_id:
            associated_label = driver.find_element(By.XPATH, f"//label[@for='{element_id}']")
            if associated_label:
                return associated_label
    except:
        pass

    return None


def process_radio_buttons():
    fieldsets = driver.find_elements(By.XPATH, '//fieldset[@data-test-form-builder-radio-button-form-component="true"]')
    for fieldset in fieldsets:
        legend_text = fieldset.find_element(By.TAG_NAME, 'legend').text
        print(f"Processing fieldset with legend: {legend_text}")  # Debugging print

        options = fieldset.find_elements(By.XPATH, './/input[@type="radio"]')
        if "require sponsorship" in legend_text.lower():
            for option in options:
                label = option.find_element(By.XPATH, 'following-sibling::label')
                label_text = label.text
                if 'no' in label_text.lower():
                    label.click()  # Click the label instead of the radio button
                    print("Selected 'No' for sponsorship requirement")  # Debugging print
                    break
        else:
            for option in options:
                label = option.find_element(By.XPATH, 'following-sibling::label')
                label_text = label.text
                if 'yes' in label_text.lower():
                    label.click()  # Click the label instead of the radio button
                    print("Selected 'Yes'")  # Debugging print
                    break


def process_dropdowns():
    dropdowns = driver.find_elements(By.TAG_NAME, 'select')
    for dropdown in dropdowns:
        select = Select(dropdown)
        options = select.options
        if options:
            if any('yes' in option.text.lower() for option in options) and any(
                    'no' in option.text.lower() for option in options):
                for option in options:
                    if 'yes' in option.text.lower():
                        driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)
                        if dropdown.is_enabled():
                            select.select_by_visible_text(option.text)
                            break
            else:
                last_option = options[-1]
                driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)
                if dropdown.is_enabled():
                    select.select_by_visible_text(last_option.text)


def process_label(label):
    input_id = label.get_attribute('for')
    if input_id:
        input_field = driver.find_element(By.ID, input_id)
        if 'years' in label.text.lower() and 'experience' in label.text.lower():
            process_text_input(label)
        elif input_field.tag_name == "select":
            process_dropdowns()
        elif input_field.tag_name == "textarea":
            process_text_area(label)


def handle_additional_questions():
    try:
        label_elements = driver.find_elements(By.TAG_NAME, 'label')
        for label in label_elements:
            process_label(label)
        process_dropdowns()
        process_radio_buttons()
        review_button_xpath = "//button[contains(@aria-label, 'Review')]"
        review_button = wait_for_clickable(By.XPATH, review_button_xpath)
        review_button.click()
        time.sleep(5)
    except Exception as e:
        print(f"An error occurred while handling additional questions: {e}")


def apply_to_jobs(job_list):
    for job in job_list:
        try:
            job.click()
            time.sleep(2)
            apply_button = wait_for_clickable(By.CLASS_NAME, "jobs-apply-button--top-card")
            driver.execute_script("arguments[0].scrollIntoView(true);", apply_button)
            close_overlay()
            apply_button.click()
            time.sleep(2)
            for _ in range(2):
                next_button_xpath = "//button[contains(@aria-label, 'Continue')]"
                next_button = wait_for_clickable(By.XPATH, next_button_xpath)
                next_button.click()
                time.sleep(2)
            handle_additional_questions()
            time.sleep(2)
            submit_button_xpath = "//button[contains(@aria-label, 'Submit application')]"
            submit_button = wait_for_clickable(By.XPATH, submit_button_xpath)
            submit_button.click()
            print("Submitted the application.")
        except TimeoutException:
            print("TimeoutException: The apply button was not found in the given time.")
        except StaleElementReferenceException:
            print("StaleElementReferenceException: The element is no longer attached to the DOM.")
        except ElementClickInterceptedException:
            print("ElementClickInterceptedException: Another element is blocking the button.")
        except Exception as e:
            print(f"An error occurred while applying for a job: {e}")


try:
    driver.get(
        'https://www.linkedin.com/jobs/search/?currentJobId=3951086724&distance=25&f_AL=true&f_E=2%2C3%2C4&f_WT=1%2C3%2C2&geoId=101174742&keywords=software%20developer&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true')
    sign_in_button = wait_for_clickable(By.CLASS_NAME, "nav__button-secondary")
    sign_in_button.click()
    email = wait_for_element(By.ID, "username")
    email.send_keys(linkedin_email)
    password = wait_for_element(By.ID, "password")
    password.send_keys(linkedin_password)
    password.send_keys(Keys.RETURN)
    time.sleep(5)
    job_list = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "jobs-search-results__list-item")))
    apply_to_jobs(job_list)
finally:
    driver.quit()
