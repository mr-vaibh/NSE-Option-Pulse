import requests
import argparse
import schedule
import time
import atexit
from datetime import datetime, timedelta

from read_config import read_config
from dumpers.gsheet import save_to_spreadsheet
from dumpers.xlsx import update_xlsx
from dumpers.sqlite import dump_data_to_sqlite, initialize_database

# Constants
config = read_config('config.json')

# On script termination
atexit.register(lambda x: print("...Schedular Stopped...\n"))

# Headers for HTTP request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

def format_datetime(time_obj, format = "%d-%b-%Y %H:%M:%S"):
    return datetime.strftime(time_obj, format)

def send_http_request(symbol):
    url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
    session = requests.Session()
    response = session.get(url, headers=HEADERS)
    return response.json()

def get_rectified_data(symbol, time_now, skip_retry = False):
    print("\n=== Fetching data at", format_datetime(time_now) , "===")
    while True:
        print("Trying at", datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
        data = send_http_request(symbol)

        # If data hasn't got published yet
        if data == {}:
            time.sleep(5)
            continue

        last_timestamp_str = data['records']['timestamp']
        last_timestamp = datetime.strptime(last_timestamp_str, '%d-%b-%Y %H:%M:%S')

        # Calculate the time difference
        time_difference = time_now - last_timestamp

        market_closed = format_datetime(last_timestamp, "%H:%M") == "15:30"

        # Skip fetching fresh current minute data instead get what is available this moment
        if args.init_now or market_closed:
            skip_retry = True

        # Check if the data is within the last minute
        if (skip_retry or time_difference.total_seconds() <= 59):
            print(f"Data found fresh [{format_datetime(last_timestamp)}]")
            print("Time difference:", time_difference)
            return data
        else:
            # Adjust the sleep time based on how often you want to check
            print(f"Data found was old [{last_timestamp}]. Retrying in 15s ...")
            time.sleep(15)

def fetch_option_chain(symbol, target_strike_prices):
    """Fetch option chain data from NSE website."""
    time_now = datetime.now()
    data = get_rectified_data(symbol, time_now)

    # Extract relevant data
    all_data = data['filtered']['data']
    underlying_value = data['records']['underlyingValue']
    timestamp_str = data['records']['timestamp']
    timestamp = datetime.strptime(timestamp_str, '%d-%b-%Y %H:%M:%S')

    # Dump data to SQLite
    dump_data_to_sqlite(data, symbol, datetime.strftime(timestamp, '%Y-%m-%d %H:%M:%S'))

    # Filter data based on target_strike_prices
    filtered_options = [option for option in all_data if option.get("strikePrice") in target_strike_prices]

    return filtered_options, timestamp, underlying_value

def transform_data(filtered_options):
    """Transform raw option chain data into required format."""
    transformed_data = []

    for entry in filtered_options:
        ce_entry = {
            'strikePrice': entry['strikePrice'],
            'identifier': entry['CE']['identifier'],
            'lastPrice': entry['CE']['lastPrice']
        }
        transformed_data.append(ce_entry)

        pe_entry = {
            'strikePrice': entry['strikePrice'],
            'identifier': entry['PE']['identifier'],
            'lastPrice': entry['PE']['lastPrice']
        }
        transformed_data.append(pe_entry)

    return transformed_data


def job():
    symbol = config["SYMBOL"]
    xlsx_filename = config["XLSX_DIR"] + symbol + '_options_data.xlsx'
    target_strike_prices = config["TARGET_STRIKE_PRICES"]
    credentials_filename = config["G-SHEET-CREDENTIALS"]
    sheet_name = config["G-SHEET-NAME"]
    worksheet_title = config["G-SHEET-TITLE"]

    filtered_options, timestamp, underlying_value = fetch_option_chain(symbol, target_strike_prices)
    transformed_data = transform_data(filtered_options)
    kwargs = {
        'symbol': symbol,
        'timestamp': timestamp,
        'underlying_value': underlying_value,
        'transformed_data': transformed_data
    }
    update_xlsx(xlsx_filename, **kwargs)
    save_to_spreadsheet(
        **kwargs,
        credentials_filename=credentials_filename,
        sheet_name=sheet_name,
        worksheet_title=worksheet_title
    )

if __name__ == '__main__':
    initialize_database()

    parser = argparse.ArgumentParser(description="Run scheduled jobs for fetching and processing stock options data.")
    parser.add_argument('--init', '-i', action='store_true', help="Initialize the database and perform the initial fetch.")
    parser.add_argument('--init-now', '-in', action='store_true', help="Initialize the database and perform the initial fetch immediately for current moment.")
    args = parser.parse_args()
    
    # Initial fetch and write to Excel if -i/--init or -in/--init-now
    if args.init or args.init_now:
        initialize_database()
        job()

    # List of times to run the job
    times = config["SCHEDULED_TIMES"]

    # Schedule the job at the specified times
    for time_str in times:
        schedule.every().day.at(time_str + ":59").do(job)

    # Keep the script running
    print("...Schedular Started...\n")
    while True:
        schedule.run_pending()
        time.sleep(1)