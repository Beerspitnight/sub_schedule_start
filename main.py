# main.py

import os
from auth_utils import authenticate_google_apis
from drive_utils import get_latest_docx_in_folder, download_file
from sheets_utils import (
    load_teacher_list,
    load_sub_list,
    load_master_schedule,
    update_daily_coverage
)
from parsing_utils import parse_aesop_report_names, extract_teacher_and_sub_data

def main():
    # 1. Authenticate
    drive_service, docs_service, sheets_client = authenticate_google_apis()
    
    # 2. Grab the latest Aesop.docx in the specific folder
    folder_id = "1RJzDwcEluGkqglmX-e3cg09Ai35kBSQG"  # adjust to your actual folder ID
    file_id = get_latest_docx_in_folder(folder_id, drive_service)
    if not file_id:
        print("No Aesop.docx file found. Exiting...")
        return
    local_docx_path = "local_report.docx"
    download_file(file_id, local_docx_path, drive_service)
    
    # 3. Parse the doc to get teacher/sub data
    parsed_lines = parse_aesop_report_names(local_docx_path)

    # 4. Load teacher list, sub list, master schedule from Sheets
    teacherlist_id = "14PEFZHKCTyvtc8O-xSThvPvbPVLSd4BaGadk7UW6tGw"
    sublist_id = "10khvv6YZacm7lkNjq1gsJky3BpHqguR5C6dMjDr1Qjg"
    master_schedule_id = "12XNbaa4AvahxYxR7D6Qa6DfrEeZPgrSiTTo5V9uFTsg"
    daily_coverage_id = "1vFsNkhIVqaS72JD5PV1nOSlYYME4XTpJBBai8d65S84"

    teacher_data = load_teacher_list(sheets_client, teacherlist_id)
    sub_data = load_sub_list(sheets_client, sublist_id)
    master_schedule_data = load_master_schedule(sheets_client, master_schedule_id)

    # 5. Fuzzy match absent teachers, assigned subs
    teacher_and_sub_info = extract_teacher_and_sub_data(parsed_lines, teacher_data, sub_data)

    # 6. Identify each absent teacher's schedule from master_schedule_data
    #     - This logic depends on how your master schedule is structured
    #     - For now, let’s pretend we do something like:
    final_coverage_info = []
    for teacher in teacher_and_sub_info["absent_teachers"]:
        # example: find teacher row in master_schedule_data
        # we'll just add a row with teacher name for demonstration
        final_coverage_info.append([teacher, "Period 1", "Room 101"])
        final_coverage_info.append([teacher, "Period 2", "Room 202"])
        # etc. adapt to your real logic

    # 7. Insert the subs that have signed up
    #    You might store them in the next columns or rows
    #    For demonstration, do something like:
    for sub in teacher_and_sub_info["assigned_subs"]:
        final_coverage_info.append(["Sub Assigned:", sub])

    # 8. Write final coverage info to the daily coverage sheet
    update_daily_coverage(sheets_client, daily_coverage_id, final_coverage_info)

    print("All done!")

if __name__ == "__main__":
    main()
