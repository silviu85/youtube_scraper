import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def get_channel_email(driver, channel_url: str):
    """
    Extracts an email from a channel's description by first waiting for the main
    'about-container' to load, then trying multiple specific selectors inside it.
    """
    if not isinstance(channel_url, str) or not channel_url.strip():
        return "Invalid URL"
        
    try:
        about_url = channel_url.rstrip('/') + '/about'
        driver.get(about_url)

        # Wait up to 10 seconds for the main about-container to be present.
        try:
            about_container_selector = '#about-container'
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, about_container_selector))
            )
            print("  - 'About' container loaded successfully.")
        except TimeoutException:
            print("  - The main 'about-container' did not load in time. Skipping channel.")
            return "Page Load Error"

        # Now search for the description inside the loaded container.
        possible_selectors = [
            '#description-container',
            '#description #plain-text',
            '#description'
        ]
        
        description_text = None
        
        for selector in possible_selectors:
            try:
                element = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                description_text = element.text
                if description_text:
                    print(f"  - Description found using selector: '{selector}'")
                    break
            except TimeoutException:
                print(f"  - Selector '{selector}' not found. Trying next...")
                continue

        if not description_text:
            print("  - Could not find the channel description text with any known selector.")
            return None

        # Search for the email within the extracted text using the corrected RegEx.
        email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        
        found_emails = re.findall(email_regex, description_text)
        
        if found_emails:
            first_email = found_emails[0]
            print(f"  - Found email in description: {first_email}")
            return first_email
        else:
            print("  - No email found in the channel description text.")
            return None

    except Exception as e:
        print(f"  - An unexpected error occurred: {e}")
        return "Error"