"""
The homepage of Empower U allowing users to login and select a series of options depending on what role they play (student, teacher, receptionist)
"""
import sys
import os

# Get the path to the 'Source Code' directory
current_dir = os.path.dirname(os.path.abspath(__file__))
source_code_dir = os.path.dirname(current_dir)
sys.path.insert(0, source_code_dir)

print(f"Current directory: {current_dir}")
print(f"Source code directory: {source_code_dir}")
print(f"Python path: {sys.path}")

# Check if 'classes' directory exists
classes_dir = os.path.join(source_code_dir, 'classes')
if os.path.exists(classes_dir):
    print(f"'classes' directory found: {classes_dir}")
else:
    print(f"'classes' directory not found at: {classes_dir}")

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Try importing custom modules and print any import errors
custom_modules = [
    'classes.user_class',
    'classes.student_class',
    'classes.teacher_class',
    'classes.receptionist_class',
    'classes.staff_class',
    'UI.student_page',
    'UI.teacher_page',
    'UI.receptionist_page'
]

for module in custom_modules:
    try:
        __import__(module)
        print(f"Successfully imported {module}")
    except ImportError as e:
        print(f"Error importing {module}: {e}")

# If all imports are successful, import them for use
from classes.user_class import User 
from classes.student_class import Student
from classes.teacher_class import Teacher
from classes.receptionist_class import Receptionist
from classes.staff_class import Staff
from UI.student_page import StudentPage
from UI.teacher_page import TeacherPage
from UI.receptionist_page import ReceptionistPage

class HomePage():
    """
    Home Page of the EmpowerU application.
    """

    def __init__(self, root):
        """
        Initialize the HomePage.

        Args:
            root (tk.Tk): The root window of the application.
        """
        self.root = root
        self.root.title("EmpowerU")
        self.window_size = "1000x1000"  # Store the window size
        self.root.geometry(self.window_size)  # Set the window size

        # Define current_dir
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Load and display the logo 
        self.logo_image = tk.PhotoImage(file=os.path.join(current_dir, "EmpowerU_logo.png")) # Image was AI generated (ChatGPT, 2024).
        self.logo_label = tk.Label(self.root, image=self.logo_image, width=400, height=400)
        self.logo_label.pack(pady=10)

        # Frame for the login form.
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        # Enter username.
        self.username_var = tk.StringVar()
        self.username_label = tk.Label(self.frame, text="Username:", font=("Forum", 10))
        self.username_label.grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(self.frame, textvariable=self.username_var, font=("Forum", 10))
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        # Enter password.
        self.password_var = tk.StringVar()
        self.password_label = tk.Label(self.frame, text="Password:", font=("Forum", 10))
        self.password_label.grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self.frame, show="*", textvariable=self.password_var, font=("Forum", 10))
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        # Login button.
        self.login_button = tk.Button(self.frame, text="Login", command=self.login, font=("Forum", 10))
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

    def login(self):
        """
        Authenticate the user and show the appropriate frame based on user type.
        """
        username = self.username_var.get()
        password = self.password_var.get()

        # Try to authenticate as staff first
        user = Staff.authenticate(username, password)
        
        # If staff authentication fails, try student authentication
        if user is None:
            user = Student.authenticate(username, password) 

        if user:
            if isinstance(user, Receptionist):
                self.show_receptionist_frame(user)
            elif isinstance(user, Teacher):
                self.show_teacher_frame(user)
            elif isinstance(user, Student):
                self.show_student_frame(user)
            else:
                print(f"Unknown user type: {type(user)}")
        else:
            if hasattr(self, 'error_label'):
                self.error_label.destroy()
            self.error_label = tk.Label(self.frame, text="Invalid username or password", fg="red", font=("Forum", 10))
            self.error_label.grid(row=3, column=0, columnspan=2, pady=5)

    def show_student_frame(self, student):
        """
        Show the student dashboard.

        Args:
            student (Student): The authenticated student user.
        """
        # Closes the HomePage window
        self.root.destroy()  
        
        # Open the student dashboard
        student_page = StudentPage(student)
        student_page.mainloop()

    def show_receptionist_frame(self, receptionist):
        """
        Show the receptionist dashboard.

        Args:
            receptionist (Receptionist): The authenticated receptionist user.
        """ 
        # Create a new Toplevel window for the ReceptionistPage
        receptionist_window = tk.Toplevel(self.root)
        receptionist_window.title("Receptionist Page")
        
        # Create the ReceptionistPage, passing the new window, this HomePage instance, and the receptionist user
        receptionist_page = ReceptionistPage(receptionist_window, self, receptionist)
        receptionist_page.pack(fill=tk.BOTH, expand=True)
        
        # Close the HomePage window
        self.root.withdraw()

        # Set up a protocol to exit the application when the ReceptionistPage is closed
        receptionist_window.protocol("WM_DELETE_WINDOW", self.exit_application)

    def show_teacher_frame(self, teacher):
        """
        Show the teacher dashboard.

        Args:
            teacher (Teacher): The authenticated teacher user.
        """
        # Closes the HomePage window
        self.root.destroy()  

        # Open the teacher dashboard
        teacher_page = TeacherPage(teacher)
        teacher_page.mainloop()
    
    def show_home_page(self):
        """
        Show the HomePage window.
        """
        self.root.deiconify()  # Show the HomePage window

    def exit_application(self):
        """
        Exit the application by stopping the mainloop and destroying all windows.
        """
        self.root.quit()  # This will stop the mainloop
        self.root.destroy()  # This will destroy all windows
    
    def remove_login_data(self):
        """Remove the username and password data from login fields
        """
        self.username_var.set("")
        self.password_var.set("")

if __name__ == "__main__":
    root = tk.Tk()
    home_page = HomePage(root)
    root.mainloop()