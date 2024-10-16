import os
import sys
from classes.staff_class import Staff

# Get the absolute path of the current file
current_file_path = os.path.abspath(__file__)

# Navigate up to the Source Code directory
source_code_dir = os.path.dirname(os.path.dirname(current_file_path))

# Add the Source Code directory to the Python path
sys.path.insert(0, source_code_dir)

# Construct the path to the data directory
data_dir = os.path.join(source_code_dir, 'data')

class Teacher(Staff):

    @staticmethod
    def authenticate(input_username, input_password):
        """
    Method to authenticate a Teacher user.

    Parameter(s):
    - input_username: str
    - input_password: str

    Returns:
    - True if authentication is successful, False otherwise
    """
        teachers_path = os.path.join(data_dir, 'teachers.txt')
        if os.path.exists(teachers_path):
            with open(teachers_path, "r", encoding="utf8") as rf:
                lines = rf.readlines()
                for line in lines:
                    username, email, password, role, recept_ID, salary, staff_info = [item.strip() for item in line.strip("\n").split(",")]
                    
                    print(f"Checking: {username}, Input: {input_username}")  # Debug print
            
                    if input_username == username:
                        if input_password == password:
                            return Teacher(username, email, password, role, recept_ID, salary, staff_info)
                        else:
                            return False
        # If we've gone through all lines and haven't returned yet, the username wasn't found
                print(f"Username {input_username} not found in file")  # Debug print
                return False
        else:
            print(f"Please check that the file {teachers_path} exists.")
            return False
            
    def __init__(self, username, email, password, role, teacher_ID, salary, staff_info):
        super().__init__(username, email, password, role, teacher_ID, salary, staff_info)

    def create_assignment(self):
        """
        Method to create a new assignment.

        This method prompts the teacher for assignment details and saves them to a file.
        """
        assignment_name = input("Enter assignment name: ")
        due_date = input("Enter due date (YYYY-MM-DD): ")
        description = input("Enter assignment description: ")

        assignments_path = os.path.join(data_dir, 'assignments.txt')
        
        # Generate a unique assignment ID
        assignment_id = f"A{str(sum(1 for line in open(assignments_path, 'r'))+1).zfill(3)}"

        with open(assignments_path, "a", encoding="utf8") as af:
            af.write(f"{assignment_id},{assignment_name},{due_date},{description},{self.teacher_ID}\n")

        print(f"Assignment '{assignment_name}' created successfully with ID: {assignment_id}")

    def grade_assignment(self):
        """
        Method to grade assignments submitted by students.

        This method allows the teacher to select an assignment, view submissions,
        and assign grades to students' work.
        """
        assignments_path = os.path.join(data_dir, 'assignments.txt')
        submissions_path = os.path.join(data_dir, 'submissions.txt')
        grades_path = os.path.join(data_dir, 'grades.txt')

        # Display available assignments
        print("Available assignments:")
        with open(assignments_path, "r", encoding="utf8") as af:
            assignments = af.readlines()
            for assignment in assignments:
                assignment_id, name, _, _, _ = assignment.strip().split(',')
                print(f"{assignment_id}: {name}")

        # Select an assignment to grade
        assignment_id = input("Enter the assignment ID to grade: ")

        # Read submissions for the selected assignment
        with open(submissions_path, "r", encoding="utf8") as sf:
            submissions = [line.strip().split(',') for line in sf if line.split(',')[1] == assignment_id]

        if not submissions:
            print("No submissions found for this assignment.")
            return

        # Grade each submission
        for submission in submissions:
            student_id, _, submission_file = submission
            print(f"\nGrading submission from student {student_id}")
            print(f"Submission file: {submission_file}")
            
            # In a real system, you might open and display the submission file here
            # For this example, we'll just ask for a grade
            grade = input("Enter grade for this submission (0-100): ")

            # Save the grade
            with open(grades_path, "a", encoding="utf8") as gf:
                gf.write(f"{student_id},{assignment_id},{grade},{self.teacher_ID}\n")

        print("Grading completed for the selected assignment.")

    def student_progress_details(self):
        '''
        Method to fetch student progress information

        Returns:
        - A list of depth 2 of each student's progress.
        '''
        with open(os.path.join(data_dir, 'student_progress.txt'), "r", encoding="utf8") as rf:
            lines = rf.readlines()
            students = []
            
            #Iterates each row of student progress information
            for line in lines[1:]: 
                # Remove unwanted spaces, entry spaces and splits into list.
                line = line.strip().strip('\n').split(',') 
                # Creates a list of student profress information
                student_info = [line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9]]
                students.append(student_info)
            return students

if __name__ == "__main__":
    teacher = Teacher("John Doe", "john.doe@example.com", "password123", "teacher", "T001", 50000, "Teacher of Mathematics", "T001")
    print(teacher.username)
    print(teacher.email)
    print(teacher.password)
    print(teacher.role)
    print(teacher.staff_ID)
    print(teacher.salary)
    print(teacher.staff_info)
    print(teacher.teacher_ID)