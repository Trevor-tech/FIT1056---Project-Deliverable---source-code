import os
import sys

# Get the absolute path of the current file
current_file_path = os.path.abspath(__file__)

# Navigate up to the Source Code directory
source_code_dir = os.path.dirname(os.path.dirname(current_file_path))

# Add the Source Code directory to the Python path
sys.path.insert(0, source_code_dir)

# Construct the path to the data directory
data_dir = os.path.join(source_code_dir, 'data')

def authenticate(input_username, input_password):
    """
    Method to authenticate a Student user.

    Parameter(s):
    - input_username: str
    - input_password: str

    Returns:
    - True if authentication is successful, False otherwise
    """
    students_path = os.path.join(data_dir, 'students.txt')
    if os.path.exists(students_path):
        with open(students_path, "r", encoding="utf8") as rf:
            lines = rf.readlines()
        for line in lines:
            username, email, password, student_ID = [item.strip() for item in line.strip("\n").split(",")]
            
            print(f"Checking: {username}, Input: {input_username}")  # Debug print
            
            if input_username == username:
                if input_password == password:
                    return True
                else:
                    return False
        # If we've gone through all lines and haven't returned yet, the username wasn't found
        print(f"Username {input_username} not found in file")  # Debug print
        return False
    else:
        print(f"Please check that the file {students_path} exists.")
        return False

if __name__ == "__main__":
    print("Testing willeykong:", authenticate("willeykong", "password123"))
    print("Testing adamriz:", authenticate("adamriz", "password123"))