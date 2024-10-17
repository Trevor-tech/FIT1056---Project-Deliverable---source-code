import pytest
import os
import sys

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from classes.receptionist_class import Receptionist

class TestReceptionist:

    @pytest.mark.parametrize("username, password, expected", [
        ("willeykong", "password123", True),
    ])
    def test_authenticate_valid(self, username, password, expected):
        result = Receptionist.authenticate(username, password)
        assert isinstance(result, Receptionist) == expected

    @pytest.mark.parametrize("username, password, expected", [
        ("willeykong", "wrongpassword", False),
        ("nonexistent_user", "anypassword", False),
        ("", "", False),
    ])
    def test_authenticate_invalid(self, username, password, expected):
        result = Receptionist.authenticate(username, password)
        assert result == expected

    def test_authenticate_file_not_found(self):
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