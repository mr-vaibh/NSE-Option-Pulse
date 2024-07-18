import sqlite3
import json
from datetime import datetime

DATABASE_FILE = 'options_data.db'

def initialize_database():
    """Initialize the SQLite database with the necessary table."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS options_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            data TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def dump_data_to_sqlite(data, symbol):
    """Dump API data to the SQLite database."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute('''
        INSERT INTO options_data (symbol, data, timestamp) VALUES (?, ?, ?)
    ''', (symbol, json.dumps(data), timestamp))

    conn.commit()
    conn.close()
    print(f"Data successfully dumped to database at {timestamp}")

# Example usage
if __name__ == '__main__':
    initialize_database()
    # Dummy data for testing
    dummy_data = {
        'symbol': 'NIFTY',
        'data': [
            {'strikePrice': 24600, 'CE': {'identifier': 'NIFTY24JAN24600CE', 'lastPrice': 100}, 'PE': {'identifier': 'NIFTY24JAN24600PE', 'lastPrice': 50}},
            {'strikePrice': 24700, 'CE': {'identifier': 'NIFTY24JAN24700CE', 'lastPrice': 200}, 'PE': {'identifier': 'NIFTY24JAN24700PE', 'lastPrice': 100}},
        ],
        'timestamp': '16-Jul-2024 15:30:00'
    }
    dump_data_to_sqlite(dummy_data, 'NIFTY')
