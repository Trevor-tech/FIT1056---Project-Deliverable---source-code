import pytest
from Utilities.validator import is_date_valid, is_time_valid

class TestIsDateValid:
    def test_valid_dates(self):
        """
        This function tests the is_date_valid() function with valid dates.

        It checks if the function correctly identifies and returns True for:
        - A regular date (1st of January 2023)
        - The last day of a year (31st of December 2022)
        - A leap year date (29th of February 2024)

        Each test case should return True when passed to is_date_valid().
        """
        assert is_date_valid("01/01/2023") == True
        assert is_date_valid("31/12/2022") == True
        assert is_date_valid("29/02/2024") == True  # Leap year

    def test_invalid_dates(self):
        """
        This function tests the is_date_valid() function with invalid dates.

        It checks if the function correctly identifies and returns False for:
        - Dates that don't exist (e.g., 31st of April)
        - Dates in non-leap years that would only be valid in leap years (e.g., 29th of February in a non-leap year)

        Each test case should return False when passed to is_date_valid().
        """
        assert is_date_valid("31/04/2023") == False  # April has 30 days
        assert is_date_valid("29/02/2023") == False  # Not a leap year

    def test_invalid_formats(self):
        """
        This function tests the invalid date formats.

        It checks if the is_date_valid() function correctly identifies
        invalid date string formats that do not match 'DD/MM/YYYY'.

        The test cases include:
        - A date in 'YYYY-MM-DD' format
        - A date in 'DD-MM-YYYY' format
        - A non-date string

        Each test case should return False when passed to is_date_valid().
        """
        assert is_date_valid("2023-01-01") == False  # Wrong format
        assert is_date_valid("01-01-2023") == False  # Wrong format
        assert is_date_valid("abc") == False

    def test_error_message(self, capsys):
        """
        This function tests the error message displayed when an invalid date format is provided.
        
        Args:
            capsys: Pytest fixture for capturing stdout and stderr

        It calls is_date_valid() with an invalid date format and checks if the correct error message is printed.
        """
        is_date_valid("2023-01-01")
        captured = capsys.readouterr()
        assert "Invalid input date format:2023-01-01. Please enter a date in the format 'DD/MM/YYYY'." in captured.out

class TestIsTimeValid:
    def test_valid_times(self):
        """
        This function tests valid time formats.

        It checks if the is_time_valid() function correctly identifies
        valid time strings in the format 'HH:MM'.

        The test cases include:
        - Midnight (00:00)
        - Last minute of the day (23:59)
        - A mid-day time (12:30)

        Each test case should return True when passed to is_time_valid().
        """
        assert is_time_valid("00:00") == True
        assert is_time_valid("23:59") == True
        assert is_time_valid("12:30") == True

    def test_invalid_times(self):
        """
        This function tests invalid time formats.

        It checks if the is_time_valid() function correctly identifies
        invalid time strings that do not match the 'HH:MM' format.

        The test cases include:
        - A time with hours exceeding 23
        - A time with minutes exceeding 59
        - Times that are technically valid but not in the correct format

        Each test case should return False when passed to is_time_valid().
        """
        assert is_time_valid("24:00") == False
        assert is_time_valid("23:60") == False

    def test_invalid_formats(self):
        """
        This function tests invalid time formats.

        It checks if the is_time_valid() function correctly identifies
        invalid time strings that do not match the 'HH:MM' format.

        The test cases include:
        - Times with incorrect separators
        - Times with missing or extra digits
        - Non-time strings

        Each test case should return False when passed to is_time_valid().
        """
        assert is_time_valid("12:30:00") == False  # Wrong format
        assert is_time_valid("12:30 PM") == False  # Wrong format
        assert is_time_valid("abc") == False

    def test_error_message(self, capsys):
        """
        This function tests the error message output of is_time_valid().

        It checks if the is_time_valid() function correctly prints an error message
        when an invalid time format is provided.

        The test case includes:
        - Calling is_time_valid() with an invalid time format
        - Capturing the printed output
        - Asserting that the correct error message is present in the output

        This test ensures that the function not only returns False for invalid inputs,
        but also provides informative feedback to the user.
        """
        is_time_valid("12:30:00")
        captured = capsys.readouterr()
        assert "Invalid input time format:12:30:00. Please enter a time in the format 'HH:MM'." in captured.out

