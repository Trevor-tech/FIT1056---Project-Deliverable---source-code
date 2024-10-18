from datetime import datetime

def is_date_valid(date_str: str) -> bool:
    """
    This function validates a date string in the format 'DD/MM/YYYY'.
    """
    try:
        datetime.strptime(date_str, '%d/%m/%Y')
        return True
    except ValueError:
        print(f"Invalid input date format:{date_str}. Please enter a date in the format 'DD/MM/YYYY'.")
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