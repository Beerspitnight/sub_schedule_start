# sheets_utils.py

def load_teacherlist(sheets_client, teacherlist_id, worksheet_name="Sheet1"):
    """
    Loads teacher data from a given Google Sheets file.
    Args:
        sheets_client (gspread.Client): Authenticated gspread client
        teacherlist_id (str): The ID of the teacher list Google Sheet
        worksheet_name (str): The name of the worksheet to read from
    Returns:
        list of lists, or list of dict, etc.
    """
    doc = sheets_client.open_by_key(teacherlist_id)
    sheet = doc.worksheet(worksheet_name)
    data = sheet.get_all_values()
    # Possibly remove header row or convert to a dictionary
    return data

def load_sublist(sheets_client, sublist_id, worksheet_name="Sheet1"):
    """
    Loads sub data from a given Google Sheets file.
    """
    doc = sheets_client.open_by_key(sublist_id)
    sheet = doc.worksheet(worksheet_name)
    data = sheet.get_all_values()
    return data

def load_master_schedule(sheets_client, master_schedule_id, worksheet_name="Sheet1"):
    """
    Loads the master schedule data from Google Sheets.
    """
    doc = sheets_client.open_by_key(master_schedule_id)
    sheet = doc.worksheet(worksheet_name)
    data = sheet.get_all_values()
    return data

def update_daily_coverage(sheets_client, daily_coverage_id, data_to_write, worksheet_name="Sheet1"):
    """
    Writes coverage data to the Daily Coverage sheet.
    data_to_write is expected to be a list of lists or something similar.

    Args:
        sheets_client (gspread.Client)
        daily_coverage_id (str)
        data_to_write: The final coverage data
        worksheet_name (str)
    """
    doc = sheets_client.open_by_key(daily_coverage_id)
    sheet = doc.worksheet(worksheet_name)
    # If you want to clear existing data:
    sheet.clear()
    # Write new data:
    sheet.update("A1", data_to_write)
    print("Daily Coverage updated successfully!")
