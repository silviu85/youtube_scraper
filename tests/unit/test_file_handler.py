from scraper.file_handler import ask_for_url_column
from unittest.mock import patch

def test_ask_for_url_column_valid_input():
    """Checks if the function returns the correct column for a valid input."""
    csv_path = 'tests/data/test_channels.csv'
    # Create a mock config object to pass to the function
    mock_config = {'csv_error_handling': 'warn'} 
    
    # Simulate user entering '2'
    with patch('builtins.input', return_value='2'):
        # Pass the mock config
        column_name = ask_for_url_column(csv_path, mock_config) 
    
    # Check if the header is correct
    assert column_name == "Channel Link"