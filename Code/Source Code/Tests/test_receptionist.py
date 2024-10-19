import pytest
import os
import sys

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from classes.receptionist_class import Receptionist

class TestReceptionist:
    """
    A test that tests the authentication functionality of the Receptionist class.

    This class uses pytest test methods to verify the behavior of the Receptionist.authenticate under various scenarios.

    Methods:
        test_authenticate_valid: Tests valid authentication attempts.
        test_authenticate_invalid: Tests invalid authentication attempts.
        test_authenticate_file_not_found: Tests authentication when the data file is missing.
    """

    @pytest.mark.parametrize("username, password, expected", [
        ("willeykong", "password123", True),
    ])
    def test_authenticate_valid(self, username, password, expected):
        """
        Test valid authentication attempts.

        Args:
            username (str): The username to test.
            password (str): The password to test.
            expected (bool): The expected result of the authentication.

        Asserts:
            The result of Receptionist.authenticate is an instance of Receptionist for valid credentials.
        """
        result = Receptionist.authenticate(username, password)
        assert isinstance(result, Receptionist) == expected

    @pytest.mark.parametrize("username, password, expected", [
        ("willeykong", "wrongpassword", False),
        ("nonexistent_user", "anypassword", False),
        ("", "", False),
    ])
    def test_authenticate_invalid(self, username, password, expected):
        """
        Test invalid authentication attempts.

        Args:
            username (str): The username to test.
            password (str): The password to test.
            expected (bool): The expected result of the authentication.

        Asserts:
            The result of Receptionist.authenticate is False for invalid credentials.
        """
        result = Receptionist.authenticate(username, password)
        assert result == expected

    def test_authenticate_file_not_found(self):

        """
        Test authentication when the data file is missing.

        This test temporarily renames the receptionist data file to simulate a missing file scenario.

        Asserts:
            The result of Receptionist.authenticate is False when the data file is missing.
        """        
        # Temporarily rename the file to simulate it not existing
        original_path = os.path.join(parent_dir, 'data', 'receptionist.txt')
        temp_path = os.path.join(parent_dir, 'data', 'receptionist_temp.txt')
        
        os.rename(original_path, temp_path)
        result = Receptionist.authenticate("any_user", "any_password")
        os.rename(temp_path, original_path)
        
        assert result == False

    # Additional tests for other methods can be added here

if __name__ == "__main__":
    pytest.main([__file__])