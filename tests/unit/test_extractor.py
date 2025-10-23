import pytest
from scraper.extractor import get_channel_email
from unittest.mock import Mock, patch

@pytest.fixture
def mock_driver():
    """Creates a mock driver object where the .get() method does nothing."""
    driver = Mock()
    # This is crucial: we prevent driver.get() from trying to access a real file/URL
    driver.get.return_value = None
    return driver

def test_extracts_email_when_present(mock_driver):
    """Tests that the email is correctly extracted when present in the description."""
    # The text we want our mock element to have
    mock_element_text = "Sample description with an email: business.inquiries@example.com for contact."
    
    # Configure the mock element that WebDriverWait will "find"
    mock_element = Mock()
    mock_element.text = mock_element_text
    
    # Patch WebDriverWait to avoid real browser interaction
    with patch('scraper.extractor.WebDriverWait') as mock_wait:
        # Make the mocked WebDriverWait return our mock element
        mock_wait.return_value.until.return_value = mock_element
        
        # Call the function with the mock driver and a dummy URL
        email = get_channel_email(mock_driver, "http://dummy-youtube-url.com")
    
    assert email == "business.inquiries@example.com"

def test_returns_none_when_no_email(mock_driver):
    """Tests that None is returned when no email is present in the description."""
    mock_element_text = "This is a description without any contact information."
    
    mock_element = Mock()
    mock_element.text = mock_element_text
    
    with patch('scraper.extractor.WebDriverWait') as mock_wait:
        mock_wait.return_value.until.return_value = mock_element
        email = get_channel_email(mock_driver, "http://dummy-youtube-url.com")

    assert email is None