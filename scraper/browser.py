from contextlib import contextmanager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

def _initialize_driver(config: dict):
    """Private function to configure and create the driver instance."""
    print("Initializing browser...")
    options = webdriver.ChromeOptions()
    language = config.get('language', 'en-US')
    is_headless = config.get('headless', False)
    options.add_argument('--log-level=3')
    options.add_argument(f'--lang={language}')
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    options.add_argument(f'user-agent={user_agent}')
    if is_headless:
        print("Running in headless mode.")
        options.add_argument('--headless')
        options.add_argument("--window-size=1920,1080")
    else:
        print("Running in visible mode.")
    return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

def _handle_cookie_consent(driver):
    """Private function to handle the cookie banner."""
    print("Checking for cookie consent banner...")
    driver.get("https://www.youtube.com")
    try:
        accept_button_xpath = "//button[.//span[text()='Accept all']]"
        accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, accept_button_xpath))
        )
        print("Cookie consent banner found. Clicking 'Accept all'.")
        driver.execute_script("arguments[0].click();", accept_button)
        time.sleep(2)
    except TimeoutException:
        print("Cookie banner not found, already accepted or not present.")

@contextmanager
def browser_session(config: dict):
    """
    A context manager for the Selenium browser session.
    Handles setup, cookie consent, and guaranteed cleanup.
    """
    driver = _initialize_driver(config)
    try:
        _handle_cookie_consent(driver)
        yield driver  
    finally:
        print("\nClosing browser session...")
        driver.quit() 