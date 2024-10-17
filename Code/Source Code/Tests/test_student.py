import pytest
import os
import sys

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from classes.student_class import Student

@pytest.fixture
def test_data_dir(tmp_path):
    return tmp_path / "data"

@pytest.fixture
def test_file_path(test_data_dir):
    test_data_dir.mkdir(exist_ok=True)
    test_file = test_data_dir / "students.txt"
    with open(test_file, 'w', encoding='utf8') as f:
        f.write("johndoe,john@example.com,password123,S001\n")
        f.write("janedoe,jane@example.com,password456,S002\n")
    return test_file

@pytest.fixture
def student_class(monkeypatch, test_file_path):
    import classes.student_class as student_module
    monkeypatch.setattr(student_module, 'data_dir', str(test_file_path.parent))
    return Student

def test_authenticate_success(student_class):
    student = student_class.authenticate("johndoe", "password123")
    assert student is not None
    assert student.username == "johndoe"
    assert student.email == "john@example.com"
    assert student.student_ID == "S001"

def test_authenticate_wrong_password(student_class):
    student = student_class.authenticate("johndoe", "wrongpassword")
    assert student is None

def test_authenticate_nonexistent_user(student_class):
    student = student_class.authenticate("nonexistent", "password")
    assert student is None

def test_student_creation():
    student = Student("testuser", "test@example.com", "testpass", "S003")
    assert student.username == "testuser"
    assert student.email == "test@example.com"
    assert student.password == "testpass"
    assert student.student_ID == "S003"

def test_submit_assignment():
    student = Student("testuser", "test@example.com", "testpass", "S003")
    assert student.submit_assignment() is None

def test_view_feedback():
    student = Student("testuser", "test@example.com", "testpass", "S003")
    assert student.view_feedback() is None

def test_file_not_found(student_class, test_data_dir):
    import classes.student_class as student_module
    non_existent_dir = test_data_dir / "non_existent_dir"
    non_existent_dir.mkdir(exist_ok=True)
    student_module.data_dir = str(non_existent_dir)
    
    result = student_class.authenticate("johndoe", "password123")
    assert result is None

if __name__ == "__main__":
    pytest.main([__file__])