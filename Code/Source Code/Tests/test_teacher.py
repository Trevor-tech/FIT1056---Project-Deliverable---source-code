# test teacher class

import pytest
import os
import sys
from unittest.mock import mock_open, patch

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from classes.teacher_class import Teacher

@pytest.fixture
def sample_teacher():
    return Teacher("John Doe", "john.doe@example.com", "password123", "teacher", "T001", 50000, "Teacher of Mathematics")

def test_teacher_initialization(sample_teacher):
    assert sample_teacher.username == "John Doe"
    assert sample_teacher.email == "john.doe@example.com"
    assert sample_teacher.password == "password123"
    assert sample_teacher.role == "teacher"
    assert sample_teacher.staff_ID == "T001"
    assert sample_teacher.salary == 50000
    assert sample_teacher.staff_info == "Teacher of Mathematics"

@pytest.mark.parametrize("username,password,expected", [
    ("John Doe", "password123", True),
    ("John Doe", "wrongpassword", False),
    ("Jane Doe", "password123", False),
])
def test_teacher_authentication(username, password, expected):
    mock_data = "John Doe,john.doe@example.com,password123,teacher,T001,50000,Teacher of Mathematics\n"
    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = Teacher.authenticate(username, password)
        if expected:
            assert isinstance(result, Teacher)
            assert result.username == "John Doe"
        else:
            assert result == False

def test_student_progress_details(sample_teacher):
    mock_data = "ID,Name,Math,Science,English,History,Geography,Art,Music,PE\n1,Alice,90,85,88,92,87,95,91,89\n2,Bob,88,91,85,89,90,87,93,92\n"
    with patch("builtins.open", mock_open(read_data=mock_data)):
        progress = sample_teacher.student_progress_details()
        assert len(progress) == 2
        assert progress[0] == ['1', 'Alice', '90', '85', '88', '92', '87', '95', '91', '89']
        assert progress[1] == ['2', 'Bob', '88', '91', '85', '89', '90', '87', '93', '92']

def test_grade_assignment(sample_teacher):
    # This test is a placeholder since the method is not implemented yet
    assert sample_teacher.grade_assignment() is None

if __name__ == "__main__":
    pytest.main()
