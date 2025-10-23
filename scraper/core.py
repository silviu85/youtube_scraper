import pandas as pd
import os
import time
import warnings
from pandas.errors import ParserWarning
from .config import load_config
from .browser import browser_session
from .extractor import get_channel_email
from .file_handler import get_csv_files, ask_for_url_column

DELAY_BETWEEN_REQUESTS = 2

def run_scraper():
    """The main function that orchestrates the entire scraping process."""
    config = load_config()
    
    if not config.get('show_csv_warnings', True):
        warnings.filterwarnings("ignore", category=ParserWarning)
        
    input_folder = config['input_folder']
    output_folder = config['output_folder']
    
    os.makedirs(input_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    csv_files = get_csv_files(input_folder)
    if not csv_files:
        print(f"No CSV files found in '{input_folder}'. Please add files to process.")
        return

    print(f"Found {len(csv_files)} CSV file(s) to process.")
    
    
    with browser_session(config) as driver:
        for file_path in csv_files:
            print(f"\n--- Processing file: {os.path.basename(file_path)} ---")
            url_column = ask_for_url_column(file_path, config)

            if url_column is None:
                continue
            
            error_handling_mode = config.get('csv_error_handling', 'strict')
            read_csv_options = {}
            if error_handling_mode == 'warn':
                read_csv_options['on_bad_lines'] = 'warn'
                read_csv_options['engine'] = 'python'

            try:
                df = pd.read_csv(file_path, **read_csv_options)
            except Exception as e:
                print(f"Critical error reading '{os.path.basename(file_path)}'. Cannot proceed with this file. Error: {e}")
                continue
            
            emails = []
            
            for i, row in df.iterrows():
                channel_url = row.get(url_column)
                print(f"Processing channel {i+1}/{len(df)}: {channel_url}")
                email = get_channel_email(driver, channel_url)
                emails.append(email)
                time.sleep(DELAY_BETWEEN_REQUESTS)

            df['Email'] = emails
            
            base_name = os.path.basename(file_path).replace('.csv', '')
            output_name = f"{base_name}_processed.csv"
            output_path = os.path.join(output_folder, output_name)
            
            df.to_csv(output_path, index=False)
            print(f"--- Finished. Results saved to: {output_path} ---")

    
    print("\nAll tasks completed.")