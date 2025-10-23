import pandas as pd
import os
import glob

def get_csv_files(input_folder: str):
    """Find all CSV files in the input folder."""
    search_path = os.path.join(input_folder, '*.csv')
    return glob.glob(search_path)

def ask_for_url_column(file_path: str, config: dict):
    """Displays columns and asks the user which one to use."""
    try:
        # Get setting from configuration
        error_handling_mode = config.get('csv_error_handling', 'strict') # 'strict' is the default value, for safety
        
        # Construim opțiunile pentru read_csv
        read_csv_options = {}
        if error_handling_mode == 'warn':
            read_csv_options['on_bad_lines'] = 'warn'
            read_csv_options['engine'] = 'python'
            
        columns = pd.read_csv(file_path, nrows=0, **read_csv_options).columns.tolist()
        
        if not columns:
            print(f"Warning: File '{os.path.basename(file_path)}' is empty. Skipping.")
            return None

        print(f"\nColumns found in '{os.path.basename(file_path)}':")
        for i, col_name in enumerate(columns):
            print(f"  {i + 1}: {col_name}")

        while True:
            try:
                choice = int(input("Please enter the number of the column with YouTube channel URLs: "))
                if 1 <= choice <= len(columns):
                    return columns[choice - 1]
                else:
                    print("Invalid number. Please choose from the list.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    except Exception as e:
        print(f"Could not read columns from '{file_path}'. Error: {e}")
        return None