# NIFTY Options Pulse

## Overview

The NIFTY Options Pulse is a Python-based tool designed to fetch, process, and store NIFTY options data. The data is retrieved from the NSE website, filtered based on specified strike prices, transformed, and then stored in both an SQLite database and an Excel file for easy analysis and record-keeping.

## Features

- **Automated Data Fetching**: Periodically fetches options data from the NSE website.
- **Data Transformation**: Transforms raw options data into a structured format.
- **Excel Report Generation**: Creates and updates an Excel report with the latest options data.
- **SQLite Database Storage**: Stores raw data in an SQLite database for historical analysis.
- **Customizable Strike Prices**: Filter options data based on user-defined strike prices.

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/nifty-options-tracker.git
    cd nifty-options-tracker
    ```

2. **Install required packages**:
    ```sh
    pip install requests openpyxl
    ```

## Usage

1. **Configure Constants**:
    In `main.py`, adjust the constants to suit your needs:
    ```python
    SYMBOL = 'NIFTY'
    TARGET_STRIKE_PRICES = [24600, 24700, 24500, 24400]
    XLSX_FILE = f"report/{SYMBOL}_options_data.xlsx"
    ```

2. **Run the script**:
    ```sh
    python main.py
    ```

3. **Continuous Data Fetching**:
    The script will automatically fetch and update data every 30 minutes.

## Files

### `main.py`

This is the main script that:
- Fetches options data from the NSE website.
- Dumps raw data to the SQLite database.
- Transforms and updates the data in an Excel report.

### `sqlite_dumper.py`

This script handles:
- Initializing the SQLite database.
- Dumping raw API data into the SQLite database.

## Excel Report Structure

- **Headers**: The report includes headers like `Identifier`, `Strike Price / Type`, and timestamps for easy tracking of price changes.
- **Strike Prices**: Options data is organized by strike prices and their corresponding call (CE) and put (PE) options.
- **Underlying Value**: The NIFTY index value is recorded for reference.

## Database

The SQLite database (`options_data.sqlite`) stores raw JSON data fetched from the NSE website along with timestamps. This allows for historical data analysis and auditing.

### Database Initialization

```python
initialize_database()
```

### Example Data Dump

```python
dump_data_to_sqlite(data, symbol)
```
