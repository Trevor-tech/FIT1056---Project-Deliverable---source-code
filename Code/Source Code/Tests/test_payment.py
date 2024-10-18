import pytest
import os
import sys

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from classes.payment_class import TeacherSalary

class TestTeacherSalary:
    """
    A test class for the TeacherSalary class.
    """

    @pytest.fixture
    def sample_teacher_salary(self):
        """
        Fixture that creates and returns a sample TeacherSalary object.

        Returns:
            TeacherSalary: A sample TeacherSalary object for testing.
        """
        return TeacherSalary("trevorlim", "trevorlim@gmail.com", "T001", "50000", "Teacher of Python Programming")

    def test_teacher_salary_initialization(self, sample_teacher_salary):
        """
        Test the initialization of a TeacherSalary object.

        Args:
            sample_teacher_salary (TeacherSalary): A sample TeacherSalary object.

        Asserts:
            The attributes of the sample_teacher_salary object match the expected values.
        """
        assert sample_teacher_salary.username == "trevorlim"
        assert sample_teacher_salary.email == "trevorlim@gmail.com"
        assert sample_teacher_salary.recept_id == "T001"
        assert sample_teacher_salary.salary == "50000"
        assert sample_teacher_salary.staff_info == "Teacher of Python Programming"

    def test_import_teachers_data_success(self, tmp_path):
        """
        Test the successful import of teachers' data from a file.

        Args:
            tmp_path (Path): A temporary directory path provided by pytest.

        Asserts:
            The import is successful and the imported data matches the expected values.
        """
        # Create a temporary file with actual data
        temp_file = tmp_path / "teachers.txt"
        temp_file.write_text("trevorlim, trevorlim@gmail.com, password123, Teacher, T001, 50000, Teacher of Python Programming\n"
                             "yuchong, yuchong@gmail.com, password123, Teacher, T002, 50000, Teacher of Information Security\n")
        
        # Temporarily change the file path
        original_path = TeacherSalary.teachers_path
        TeacherSalary.teachers_path = str(temp_file)
        
        teacher_salary = TeacherSalary("", "", "", "", "")
        result = teacher_salary.import_teachers_data()
        
        # Restore the original path
        TeacherSalary.teachers_path = original_path
        
        assert result == True
        assert len(teacher_salary.teachers_salary) == 2
        assert teacher_salary.teachers_salary[0].username == "trevorlim"
        assert teacher_salary.teachers_salary[1].username == "yuchong"

    def test_import_teachers_data_file_not_found(self):
        """
        Test the import_teachers_data method when the file is not found.

        Asserts:
            The import fails and returns False when the file is not found.
        """
        # Set a non-existent file path
        original_path = TeacherSalary.teachers_path
        TeacherSalary.teachers_path = "/non/existent/path.txt"
        
        teacher_salary = TeacherSalary("", "", "", "", "")
        result = teacher_salary.import_teachers_data()
        
        # Restore the original path
        TeacherSalary.teachers_path = original_path
        
        assert result == False

    def test_salary_display(self, capsys, sample_teacher_salary):
        """
        Test the Salary method of TeacherSalary class.

        Args:
            capsys: Pytest fixture to capture stdout and stderr.
            sample_teacher_salary (TeacherSalary): A sample TeacherSalary object.

        Asserts:
            The output of the Salary method matches the expected format.
        """
        sample_teacher_salary.teachers_salary = [sample_teacher_salary]
        sample_teacher_salary.teacher_salary()
        
        captured = capsys.readouterr()
        expected_output = "trevorlim trevorlim@gmail.com T001 50000 Teacher of Python Programming\n"
        assert captured.out == expected_output

    @pytest.mark.parametrize("username, email, recept_id, salary, staff_info", [
        ("trevorlim", "trevorlim@gmail.com", "T001", "50000", "Teacher of Python Programming"),
        ("yuchong", "yuchong@gmail.com", "T002", "50000", "Teacher of Information Security"),
    ])
    
    def test_multiple_teacher_salaries(self, username, email, recept_id, salary, staff_info):
        """
        Test the creation of multiple TeacherSalary objects with different parameters.

        Args:
            username (str): The username of the teacher.
            email (str): The email of the teacher.
            recept_id (str): The receipt ID of the teacher.
            salary (str): The salary of the teacher.
            staff_info (str): Additional information about the teacher.

        Asserts:
            The attributes of each created TeacherSalary object match the input parameters.
        """
        teacher = TeacherSalary(username, email, recept_id, salary, staff_info)
        assert teacher.username == username
        assert teacher.email == email
        assert teacher.recept_id == recept_id
        assert teacher.salary == salary
        assert teacher.staff_info == staff_info

if __name__ == "__main__":
    pytest.main([__file__])
