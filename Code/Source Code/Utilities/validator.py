from datetime import datetime, timedelta

def is_date_valid(date_str: str) -> bool:
    """
    This function validates a date string in the format 'DD/MM/YYYY'.
    It checks if the date is within a five-year range starting from 2023.
    """
    try:
        input_date = datetime.strptime(date_str, '%d/%m/%Y')
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2027, 12, 31)  # Five years from 2023

        if start_date <= input_date <= end_date:
            return True
        elif input_date < start_date:
            print(f"Date {date_str} is before 2023. Please enter a date from 2023 onwards.")
            return False
        else:
            print(f"Date {date_str} is beyond the allowed range. Please enter a date no later than 31/12/2027.")
            return False
    except ValueError:
        print(f"Invalid input date format: {date_str}. Please enter a date in the format 'DD/MM/YYYY'.")
        return False

def is_time_valid(time_str: str) -> bool:
    """
    This function validates a time string in the format 'HH:MM:SS'.
    """
    try:
        datetime.strptime(time_str, '%H:%M')
        return True
    except ValueError:
        print(f"Invalid input time format:{time_str}. Please enter a time in the format 'HH:MM'.")
        return False