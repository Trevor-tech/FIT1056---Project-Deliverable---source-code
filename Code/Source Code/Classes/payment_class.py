import os
import sys

from classes.receptionist_class import Receptionist

class TeacherSalary:
    """
    Represents a teacher's salary information within a school management system.

    Class Attributes:
        teachers_path (str): Path to the teachers' data file.

    Attributes:
        username (str): The user's username.
        email (str): The user's email address.
        recept_id (str): The recept ID.
        salary (str): The teacher's salary.
        staff_info (str): Additional staff information.

    Args:
        username (str): The user's username.
        email (str): The user's email address.
        recept_id (str): The recept ID.
        salary (str): The teacher's salary.
        staff_info (str): Additional staff information.
    """
    teachers_path = "./Data/teachers.txt"

    def __init__(self, username, email, recept_id, salary, staff_info):
        self.username = username
        self.email = email
        self.recept_id = recept_id
        self.salary = salary
        self.staff_info = staff_info
    
    def import_teachers_data(self):
        """
        Import teachers' data.

        Returns:
        Bool -  True if import successfully, 
                false otherwise
        """
        self.teachers_salary = []
        if os.path.exists(self.teachers_path):
            with open(self.teachers_path, "r", encoding="utf8") as rf:
                lines = rf.readlines()
            for line in lines:
                username, email, password, role, recept_id, salary, staff_info = line.strip("\n").split(",")
                teacher_obj = TeacherSalary(username, email, recept_id, salary, staff_info)
                self.teachers_salary.append(teacher_obj)
            return True
        else:
            print(f"Please check the subdirectory and file exists for {self.teachers_path}.")
            return False
            
    def teacher_salary(self):
        """
        Showing staff Salary
        """
        for teacher in self.teachers_salary:
            print(teacher.username, teacher.email,  teacher.recept_id, teacher.salary, teacher.staff_info)
