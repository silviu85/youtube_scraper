### 1. Running Instructions 

#### Step 1: Environment Setup (One-Time)
1.  Ensure you have Python installed.
2.  Open a terminal in the project folder.
3.  Install the required packages:
    ```bash
    pip install pandas selenium webdriver-manager PyYAML
    ```

#### Step 2: Adding the Input Files
1.  Place **one or more CSV files** in the `input` folder. The script will find them automatically.

#### Step 3: Running the Interactive Scraper
1.  In the terminal, from the project's root folder, run the command:
    ```bash
    python youtube_scraper.py
    ```
2.  The script will list the files found.
3.  For **each file**, it will display a numbered list of the columns.
4.  **Enter the number** corresponding to the column that contains the links to the YouTube channels and press Enter.
5.  The script will process the file and save the result to the `output` folder with the `_processed.csv` suffix.
6.  The process will repeat for all CSV files found in the `input` folder.

#### Example Console Interaction:
```
Found 1 CSV file(s) to process.

--- Processing file: channels.csv ---
Columns found in 'channels.csv':
  1: Channel Name
  2: Link to Channel
  3: Category
Please enter the number of the column containing the YouTube channel URLs: 2
Processing channel 1/7: https://www.youtube.com/@GoogleDevelopers
  - Found email: partner-support@google.com
Processing channel 2/7: https://www.youtube.com/@Microsoft
  - Found email: msftsocial@microsoft.com
...
--- Finished processing. Results saved to: output/channels_processed.csv ---

All tasks completed. Browser has been closed.
```
### 2. How to Run the Test

1.  **Make sure you have everything ready:**
    *   The main script `youtube_scraper.py` is in the root folder.
    *   The file `tests/data/test_channels.csv` exists.
    *   The test file `tests/test_youtube_scraper.py`.
    *   The Python packages are installed (`pip install pandas selenium webdriver-manager PyYAML`).

2.  **Open a terminal** in the project's root folder (`/youtube_scraper_project/`).

3.  **Run the test** using the command below. It is important to use `-m unittest` so that Python can correctly discover and run the test files.

    ```bash
    python -m unittest tests/test_youtube_scraper.py
    ```

### What will happen when you run the command?

1.  The test script will create a temporary folder `tests/temp_test_environment`.
2.  It will copy the test CSV file and create a temporary `config.yaml` in this folder.
3.  It will run the `main()` function from `youtube_scraper.py`.
4.  When the main script reaches `input()`, it **will not stop and wait**. Instead, the fake (mock) function will automatically return the value `'2'`.
5.  After the main script finishes, the test script will verify if the output file was created correctly in the temporary folder and if it has the expected content.
6.  Finally, regardless of whether the test passed or failed, the temporary folder `tests/temp_test_environment` will be automatically deleted.

You will see an output in the console showing you the setup steps, the test execution, and a success or error message at the end.