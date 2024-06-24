### LinkedIn Job Applier

## Overview

**LinkedIn Job Applier** is an automated tool designed to streamline the process of applying for jobs on LinkedIn. Built using Python and Selenium, this tool automates the navigation, form filling, and submission of job applications, making it easier and faster to apply for multiple positions.

## Features

- **Automated Login**: Automatically logs into LinkedIn using stored credentials.
- **Job Application**: Automatically applies for jobs by clicking the "Easy Apply" button, filling out required fields, and submitting applications.
- **Field Handling**: Supports handling of text inputs, text areas, dropdowns, and radio buttons.
- **Overlay Handling**: Closes any overlays that may block interaction with the application buttons.
- **Feedback Handling**: Checks for feedback messages during the application process and handles them accordingly.
- **Error Handling**: Robust error handling for various exceptions like timeouts and element interception.

## Future Enhancements

- **Captcha Handling**: Implement automated handling of captchas that may appear during the login or application process.
- **Enhanced Field Handling**: Improve the handling of additional questions and fields, including edge cases.
- **Dynamic Form Filling**: Enhance the logic to dynamically fill forms based on the specific requirements of each job application.

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/your-username/linkedin-job-applier.git
    cd linkedin-job-applier
    ```

2. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Set up environment variables**:
    Create a `.env` file in the root directory and add your LinkedIn credentials:
    ```env
    LINKEDIN_EMAIL=your-email@example.com
    LINKEDIN_PASSWORD=your-linkedin-password
    ```

## Usage

1. **Run the script**:
    ```sh
    python linkedin_job_applier.py
    ```

2. **Sit back and relax**:
    The script will automatically log in to LinkedIn, search for jobs, and apply to them using the "Easy Apply" button. It will handle any additional questions and submit the applications.

## Code Overview

Here's a breakdown of the main components of the script:

### Initialization
The `LinkedInJobApplier` class initializes the WebDriver, loads environment variables, and sets up WebDriverWait.

### Methods

- **`wait_for_element`**: Waits for an element to be present on the page.
- **`wait_for_clickable`**: Waits for an element to be clickable.
- **`close_overlay`**: Closes any overlay that may block interactions.
- **`process_text_input` and `process_text_area`**: Handles text inputs and text areas respectively.
- **`process_dropdowns`**: Handles dropdown selections.
- **`process_radio_buttons`**: Handles radio button selections.
- **`process_label`**: Processes labels to find and fill associated input fields.
- **`handle_additional_questions`**: Handles all additional questions in the application form.
- **`click_buttons`**: Handles the sequence of clicking "Next", "Review", and "Submit" buttons.
- **`check_for_feedback_and_dismiss`**: Checks for feedback messages and handles the "Dismiss" and "Discard" actions.
- **`apply_to_job`**: Applies to a single job.
- **`apply_to_jobs`**: Applies to multiple jobs in a loop.
- **`login`**: Logs into LinkedIn using provided credentials.
- **`start_applying`**: Starts the application process.

### Handling Feedback and Discarding Applications

The script checks for specific feedback messages and, if found, dismisses the application and confirms the discard action.

### Example Snippet

```python
def check_for_feedback_and_dismiss(self):
    try:
        feedback_message = self.driver.find_element(By.XPATH, "//span[@class='artdeco-inline-feedback__message']")
        if "Enter a decimal number larger than 0.0" in feedback_message.text:
            self._dismiss_application()
            discard_button = self.wait_for_clickable(By.XPATH, "//button[@data-control-name='discard_application_confirm_btn']")
            discard_button.click()
    except TimeoutException:
        print("No feedback message found.")
    except Exception as e:
        print(f"An error occurred while handling feedback: {e}")
```

## Future Enhancements

1. **Captcha Handling**:
    - Implement a captcha-solving service or prompt the user to solve captchas during the automation process.

2. **Dynamic Form Filling**:
    - Enhance the logic to dynamically adapt to different types of additional questions and fields, including more complex validations and conditional logic.

3. **Improved Error Handling**:
    - Implement more sophisticated error handling and retry mechanisms to improve robustness.

4. **User Interface**:
    - Develop a user-friendly interface to configure settings, view logs, and monitor the application process.

5. **Parallel Processing**:
    - Enable parallel processing to apply for multiple jobs simultaneously, further reducing the time required to complete applications.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your improvements.

---

*Note: This script is intended for educational purposes only. Please ensure you comply with LinkedIn's terms of service and any applicable laws and regulations.*
