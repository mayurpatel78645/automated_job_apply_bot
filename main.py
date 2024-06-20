import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, \
    StaleElementReferenceException
from dotenv import load_dotenv


class LinkedInJobApplier:
    def __init__(self):
        load_dotenv()
        self.linkedin_email = os.getenv('LINKEDIN_EMAIL')
        self.linkedin_password = os.getenv('LINKEDIN_PASSWORD')
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def wait_for_element(self, by, value, timeout=10):
        return self.wait.until(EC.presence_of_element_located((by, value)))

    def wait_for_clickable(self, by, value, timeout=10):
        return self.wait.until(EC.element_to_be_clickable((by, value)))

    def close_overlay(self):
        try:
            overlay_close_button = self.driver.find_element(By.CSS_SELECTOR, ".overlay-close-button")
            if overlay_close_button.is_displayed():
                overlay_close_button.click()
        except Exception:
            pass

    def process_text_input(self, input_id):
        try:
            input_field = self.driver.find_element(By.ID, input_id)
            if input_field.tag_name == "input" and input_field.get_attribute(
                    "type") == "text" and input_field.is_enabled():
                input_field.clear()
                input_field.send_keys("5")
                print(f"Set text input for {input_id}")
        except Exception as e:
            print(f"Failed to process text input for {input_id}: {e}")

    def process_text_area(self, input_id):
        try:
            input_field = self.driver.find_element(By.ID, input_id)
            if input_field.tag_name == "textarea" and input_field.is_enabled():
                input_field.clear()
                input_field.send_keys("5 years")
                print(f"Set text area for {input_id}")
        except Exception as e:
            print(f"Failed to process text area for {input_id}: {e}")

    def process_dropdowns(self):
        try:
            dropdowns = self.driver.find_elements(By.TAG_NAME, 'select')
            for dropdown in dropdowns:
                select = Select(dropdown)
                options = select.options
                if options:
                    if any('yes' in option.text.lower() for option in options) and any(
                            'no' in option.text.lower() for option in options):
                        for option in options:
                            if 'yes' in option.text.lower():
                                self.driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)
                                if dropdown.is_enabled():
                                    select.select_by_visible_text(option.text)
                                    print("Selected 'Yes' in dropdown")
                                    break
                    else:
                        last_option = options[-1]
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)
                        if dropdown.is_enabled():
                            select.select_by_visible_text(last_option.text)
                            print("Selected last option in dropdown")
        except Exception as e:
            print(f"Failed to process dropdown: {e}")

    def process_radio_buttons(self):
        try:
            fieldsets = self.driver.find_elements(By.XPATH,
                                                  '//fieldset[@data-test-form-builder-radio-button-form-component="true"]')
            for fieldset in fieldsets:
                legend_text = fieldset.find_element(By.TAG_NAME, 'legend').text
                print(f"Processing fieldset with legend: {legend_text}")

                options = fieldset.find_elements(By.XPATH, './/input[@type="radio"]')
                for option in options:
                    label = option.find_element(By.XPATH, 'following-sibling::label')
                    label_text = label.text.lower()
                    if "require sponsorship" in legend_text.lower() and 'no' in label_text:
                        label.click()
                        print("Selected 'No' for sponsorship requirement")
                        break
                    elif "require sponsorship" not in legend_text.lower() and 'yes' in label_text:
                        label.click()
                        print("Selected 'Yes'")
                        break
        except Exception as e:
            print(f"Failed to process radio buttons: {e}")

    def process_label(self, label):
        input_id = label.get_attribute('for')
        if input_id:
            try:
                input_field = self.driver.find_element(By.ID, input_id)
                if 'years' in label.text.lower() and 'experience' in label.text.lower():
                    self.process_text_input(input_id)
                elif input_field.tag_name == "select":
                    self.process_dropdowns()
                elif input_field.tag_name == "textarea":
                    self.process_text_area(input_id)
            except Exception as e:
                print(f"Failed to process label for {input_id}: {e}")

    def handle_additional_questions(self):
        try:
            label_elements = self.driver.find_elements(By.TAG_NAME, 'label')
            for label in label_elements:
                self.process_label(label)
            self.process_dropdowns()
            self.process_radio_buttons()
        except Exception as e:
            print(f"An error occurred while handling additional questions: {e}")

    def click_buttons(self):
        while True:
            try:
                next_button = self.wait_for_clickable(By.XPATH, "//button[contains(@aria-label, 'Continue')]")
                next_button.click()
                time.sleep(1)
            except TimeoutException:
                break

        try:
            review_button = self.wait_for_clickable(By.XPATH, "//button[contains(@aria-label, 'Review')]")
            self.handle_additional_questions()
            review_button.click()
            time.sleep(1)
        except TimeoutException:
            pass

        try:
            submit_button = self.wait_for_clickable(By.XPATH, "//button[contains(@aria-label, 'Submit application')]")
            submit_button.click()
            print("Submitted the application.")
            time.sleep(1)
            dismiss_button = self.wait_for_clickable(By.XPATH, "//button[contains(@aria-label, 'Dismiss')]")
            dismiss_button.click()
        except TimeoutException:
            print("TimeoutException: The submit button was not found in the given time.")

    def apply_to_job(self, job):
        try:
            job.click()
            time.sleep(1)
            apply_button = self.wait_for_clickable(By.CLASS_NAME, "jobs-apply-button--top-card")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", apply_button)
            self.close_overlay()
            apply_button.click()
            time.sleep(1)
            self.click_buttons()
        except TimeoutException:
            print("TimeoutException: The apply button was not found in the given time.")
        except StaleElementReferenceException:
            print("StaleElementReferenceException: The element is no longer attached to the DOM.")
        except ElementClickInterceptedException:
            print("ElementClickInterceptedException: Another element is blocking the button.")
        except Exception as e:
            print(f"An error occurred while applying for a job: {e}")

    def apply_to_jobs(self):
        while True:
            try:
                job_list = self.wait.until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "jobs-search-results__list-item")))
                for job in job_list:
                    self.apply_to_job(job)
            except StaleElementReferenceException:
                continue

    def login(self):
        self.driver.get(
            'https://www.linkedin.com/jobs/search/?currentJobId=3954175374&distance=25&f_AL=true&f_E=2%2C3%2C4&f_TPR'
            '=r86400&f_WT=1%2C3%2C2&geoId=101174742&keywords=software%20developer&origin=JOB_SEARCH_PAGE_JOB_FILTER'
            '&refresh=true')
        sign_in_button = self.wait_for_clickable(By.CLASS_NAME, "nav__button-secondary")
        sign_in_button.click()
        email = self.wait_for_element(By.ID, "username")
        email.send_keys(self.linkedin_email)
        password = self.wait_for_element(By.ID, "password")
        password.send_keys(self.linkedin_password)
        password.send_keys(Keys.RETURN)
        time.sleep(3)

    def start_applying(self):
        try:
            self.login()
            self.apply_to_jobs()
        finally:
            self.driver.quit()


if __name__ == "__main__":
    job_applier = LinkedInJobApplier()
    job_applier.start_applying()
