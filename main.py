import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
linkedin_email = os.getenv('LINKEDIN_EMAIL')
linkedin_password = os.getenv('LINKEDIN_PASSWORD')

# Initialize WebDriver
driver = webdriver.Chrome()

# Open LinkedIn Jobs page
driver.get('https://www.linkedin.com/jobs/search/?currentJobId=3941807035&distance=25&f_AL=true&f_E=2%2C3%2C4&f_WT=1%2C3%2C2&geoId=101174742&keywords=software%20developer&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true')

# Click on the sign-in button
sign_in_button = driver.find_element(By.CLASS_NAME, "nav__button-secondary.btn-md.btn-secondary-emphasis")
sign_in_button.click()

# Enter email
email = driver.find_element(By.ID, "username")
email.send_keys(linkedin_email)

# Enter password
password = driver.find_element(By.ID, "password")
password.send_keys(linkedin_password)
password.send_keys(Keys.RETURN)

# Wait for login to complete
time.sleep(50)

# Close the browser
driver.quit()
