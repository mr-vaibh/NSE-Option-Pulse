import gspread

def authenticate(credentials_filename='credentials.json'):
    """Authenticate with Google Sheets using OAuth2 credentials."""
    gc = gspread.oauth(scopes=["https://www.googleapis.com/auth/spreadsheets"], credentials_filename=credentials_filename)
    return gc

def open_worksheet(gc, sheet_name, worksheet_title):
    """Open the specified worksheet in the given spreadsheet."""
    sh = gc.open(sheet_name)
    worksheet = sh.worksheet(title=worksheet_title)
    return worksheet

def format_data(data, timestamp, symbol, underlying_value):
    """Format the data to be written to the spreadsheet."""
    rows = []
    rows.append([timestamp.strftime("%d-%m-%Y"), symbol, timestamp.strftime("%I:%M %p"), underlying_value])

    for item in data:
        if 'CE' in item['identifier']:
            option_type = 'CE'
        elif 'PE' in item['identifier']:
            option_type = 'PE'
        else:
            continue  # Skip if neither CE nor PE

        strike_price = item['strikePrice']
        last_price = item['lastPrice']
        formatted_row = [
            timestamp.strftime("%d-%m-%Y"),
            f"{symbol} {strike_price} {option_type}",
            timestamp.strftime("%I:%M %p"),
            last_price
        ]
        rows.append(formatted_row)
    
    return rows

def update_spreadsheet(worksheet, rows):
    """Update the specified worksheet with the formatted data."""
    # Get all values in column A to determine the last row
    column_a = worksheet.col_values(1)
    last_row = len(column_a)
    start_row = last_row + 1
    
    # Batch update the data to Google Sheet
    end_row = start_row + len(rows) - 1
    cell_range = f"A{start_row}:D{end_row}"
    cell_list = worksheet.range(cell_range)

    flat_rows = [item for sublist in rows for item in sublist]  # Flatten the 2D list
    for cell, value in zip(cell_list, flat_rows):
        cell.value = value
    
    worksheet.update_cells(cell_list)
    worksheet.format(cell_range, {'horizontalAlignment': 'CENTER'})

    print("[Updated Google Sheet]")

def needs_update(worksheet, last_time):
    column_c_values = worksheet.col_values(3)
    last_value_in_column_c = worksheet.cell(len(column_c_values), 3).value

    return last_value_in_column_c != last_time

def save_to_spreadsheet(symbol, timestamp, underlying_value, transformed_data, credentials_filename, sheet_name, worksheet_title):
    """Main function to save data to Google Sheets."""
    gc = authenticate(credentials_filename)
    worksheet = open_worksheet(gc, sheet_name, worksheet_title)

    stop_saving = not needs_update(worksheet, timestamp.strftime('%I:%M %p'))
    if stop_saving:
        print("[Google Sheet already up-to-date]")
        return

    formatted_data = format_data(transformed_data, timestamp, symbol, underlying_value)
    update_spreadsheet(worksheet, formatted_data)
