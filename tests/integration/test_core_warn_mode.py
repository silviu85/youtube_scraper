import os
import pandas as pd
from unittest.mock import patch
from scraper.core import run_scraper

@patch('scraper.core.initialize_driver')
@patch('scraper.core.handle_cookie_consent')
@patch('scraper.core.get_channel_email', return_value='mock.email@example.com')
@patch('scraper.core.ask_for_url_column', return_value='Channel Link')
@patch('scraper.core.load_config')
def test_run_scraper_in_warn_mode(mock_config, mock_ask, mock_extractor, mock_cookie, mock_driver, isolated_test_env):
    """
    Integration test for the main scraper flow with 'csv_error_handling' set to 'warn'.
    It should process the valid lines and skip the bad lines based on the user-provided data.
    """
    input_dir, output_dir = isolated_test_env
    
    mock_config.return_value = {
        'input_folder': input_dir,
        'output_folder': output_dir,
        'language': 'en-US',
        'csv_error_handling': 'warn'
    }
    
    run_scraper()
    
    output_file = os.path.join(output_dir, 'test_channels_processed.csv')
    assert os.path.exists(output_file)
    
    df = pd.read_csv(output_file)
    assert 'Email' in df.columns
    
    # We now expect 5 valid rows after skipping the 3 bad ones from the provided test data.
    assert len(df) == 5