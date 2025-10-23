import os
import pandas as pd
from unittest.mock import patch
import pytest
from scraper.core import run_scraper

@patch('scraper.core.initialize_driver')
@patch('scraper.core.handle_cookie_consent')
@patch('scraper.core.ask_for_url_column', return_value='Channel Link')
@patch('scraper.core.load_config')
def test_run_scraper_in_strict_mode_does_not_create_file(mock_config, mock_ask, mock_cookie, mock_driver, isolated_test_env):
    """
    Tests that the scraper does NOT create an output file in 'strict' mode
    when encountering a malformed CSV.
    """
    input_dir, output_dir = isolated_test_env
    
    mock_config.return_value = {
        'input_folder': input_dir,
        'output_folder': output_dir,
        'language': 'en-US',
        'csv_error_handling': 'strict'
    }
    
    run_scraper()

    output_file = os.path.join(output_dir, 'test_channels_processed.csv')
    # The real test is to confirm the output file was NOT created.
    assert not os.path.exists(output_file)