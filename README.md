# NSE Option Pulse

## Overview

NSE Option Pulse is a Python application designed to fetch, process, and store stock options data from the NSE India website. The data is retrieved from the NSE website and filtered based on specified strike prices. It supports multiple data storage formats including SQLite, Google Sheets, and Excel, and includes a Flask web interface to start and stop the script remotely. The application is scheduled to run at specific times to ensure data is up-to-date. The data can be further used to analyze the market precisely and develop better trading strategies.

## Features

- **Data Fetching**: Retrieves stock options data from the NSE India API.
- **SQLite Storage**: Stores the fetched data in an SQLite database for historical tracking.
- **Google Sheets Integration**: Updates Google Sheets with the latest data for easy access and sharing.
- **Excel Export**: Exports data to an Excel file for offline analysis.
- **Scheduling**: Runs the data fetching process at predefined intervals using a scheduling mechanism.

## Installation

### Prerequisites

Ensure you have Python 3.x installed on your system.

### Setup

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/mr-vaibh/NSE-Option-Pulse.git
    cd NSE-Option-Pulse
    ```

2. **Install Required Libraries:**

    ```bash
    pip install requests schedule gspread openpyxl
    ```

3. **Google Sheets Credentials:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project or select an existing project.
   - Enable the Google Sheets API.
   - Create OAuth 2.0 credentials and download the `credentials.json` file.
   - Place `credentials.json` in the project root directory.

4. **Configure `config.json`:**
   - Create a `config.json` file in the project root directory with the following structure:

    ```json
    {
        "SYMBOL": "NIFTY",
        "SCHEDULED_TIMES": [
            "09:15", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00",
            "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:35"
        ],
        "XLSX_DIR": "report/",
        "G-SHEET-CREDENTIALS": "credentials.json",
        "G-SHEET-NAME": "NSE Option Trading",
        "G-SHEET-TITLE": "Historical Data Collection"
    }
    ```

    - **SYMBOL**: The stock symbol for which data will be fetched.
    - **SCHEDULED_TIMES**: List of times at which the data must be fetched and recorded.
    - **XLSX_DIR**: Directory where Excel files will be saved.
    - **G-SHEET-CREDENTIALS**: Path to your Google Sheets credentials file.
    - **G-SHEET-NAME**: Name of the Google Sheets spreadsheet.
    - **G-SHEET-TITLE**: Title of the worksheet within the Google Sheets spreadsheet.

## How It Works

### Main Components

1. **`main.py`**: This is the main script that coordinates the data fetching, processing, and scheduling.
    - **Configuration**: Reads settings from `config.json`.
    - **Data Fetching**: Uses the NSE India API to retrieve stock options data.
    - **Data Processing**: Filters and transforms data.
    - **Storage**:
        - **SQLite**: Stores the raw data in an SQLite database for historical records.
        - **Google Sheets**: Updates a specified Google Sheets document with the processed data.
        - **Excel**: Exports the data to an Excel file for offline use.
    - **Scheduling**: Uses the `schedule` library to run data fetching at predefined times.

2. **`read_config.py`**: Contains a function to read configuration settings from `config.json`.

3. **`dumpers/gsheet.py`**: Handles Google Sheets operations.
    - **Authentication**: Uses OAuth2 credentials to authenticate with Google Sheets.
    - **Worksheet Operations**: Opens a specified worksheet and updates it with new data.
    - **Data Formatting**: Formats the data to fit the structure of Google Sheets.
    - **Update Check**: Ensures that data is only updated if necessary.

4. **`dumpers/sqlite.py`**: Manages SQLite database operations.
    - **Database Initialization**: Creates the necessary database table if it doesn't exist.
    - **Data Dumping**: Inserts fetched data into the SQLite database.

5. **`dumpers/xlsx.py`**: Manages Excel file operations.
    - **Update/Create Excel File**: Updates an existing Excel file or creates a new one if it does not exist.
    - **Column Management**: Determines where to place new data and adjusts columns accordingly.
    - **Formatting**: Adjusts column widths and formats cells for readability.

### Scheduling

The `schedule` library is used to run the `job` function at specific times throughout the trading day. The times are specified in `main.py` and can be adjusted based on your needs.

## Usage

1. **Initial Setup:**
   Run the following command to initialize the database and perform the initial data fetch:

    ```bash
    python main.py --init
    ```

2. **Immediate Data Fetch:**
   Run the following command to fetch data immediately and initialize the database:

    ```bash
    python main.py --init-now
    ```

3. **Automated Data Fetching:**
   The script will run automatically at scheduled times if executed without the `--init` or `--init-now` arguments.

   ```bash
    python main.py
    ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request to improve the project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or feedback, please reach out to [me](mailto:shuklavaibhav336@gmail.com).
