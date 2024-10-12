"""
The homepage of Empower U allowing users to login and select a series of options depending on what role they play (student, teacher, receptionist)
"""
import sys
import os
print('current directory:', os.getcwd())
# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import tkinter as tk
from tkinter import messagebox
from classes.user_class import User 
from classes.student_class import Student
from classes.teacher_class import Teacher
from classes.receptionist_class import Receptionist
from classes.staff_class import Staff
import UI.student_page
import UI.teacher_page
import UI.receptionist_page

class HomePage:
    def __init__(self, root):
        self.root = root
        self.root.title("Empower U")
        self.root.geometry("1000x1000")  # Increased height to accommodate logo

        # Load and display the logo
        self.logo_image = tk.PhotoImage(file=os.path.join(current_dir, "EmpowerU_logo.png")) # Image was AI generated (ChatGPT, 2024).
        self.logo_label = tk.Label(self.root, image=self.logo_image, width=400, height=400)
        self.logo_label.pack(pady=10)

        # Frame for the login form.
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        # Enter username.
        self.username_var = tk.StringVar()
        self.username_label = tk.Label(self.frame, text="Username:")
        self.username_label.grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(self.frame, textvariable=self.username_var)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        # Enter password.
        self.password_var = tk.StringVar()
        self.password_label = tk.Label(self.frame, text="Password:")
        self.password_label.grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self.frame, show="*", textvariable=self.password_var)
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        # Login button.
        self.login_button = tk.Button(self.frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

    def login(self):
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
            self.error_label = tk.Label(self.frame, text="Invalid username or password", fg="red", font=("Arial", 10, "bold"))
            self.error_label.grid(row=3, column=0, columnspan=2, pady=5)

    """
    def authenticate(self, username, password):
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'Data')
        
        with open(os.path.join(data_dir, 'receptionist.txt'), 'r') as receptionist_file:
            receptionist_data = receptionist_file.readlines()
            for line in receptionist_data:
                line = line.strip().split(',')
                if line[0] == username and line[2] == password:
                    return Receptionist(line[0], line[1], line[2], line[4], line[5], line[6], line[7])
        
        with open(os.path.join(data_dir, 'students.txt'), 'r') as student_file:
            student_data = student_file.readlines()
            for line in student_data:
                line = line.strip().split(',')
                if line[0] == username and line[2] == password:
                    return Student(line[0], line[1], line[2], line[3])
        
        with open(os.path.join(data_dir, 'teachers.txt'), 'r') as teacher_file:
            teacher_data = teacher_file.readlines()
            for line in teacher_data:
                line = line.strip().split(',')
                if line[0] == username and line[2] == password:
                    return Teacher(line[0], line[1], line[2], line[3], line[4], line[5], line[6])
        
        return False
        """
    
    def show_options(self, user):
        options_window = tk.Toplevel(self.root)
        options_window.title(f"Welcome, {user.name}")
        options_window.geometry("300x200")

        if isinstance(user, Student):
            options = ["View Courses", "Submit Assignment", "Check Grades"]
        elif isinstance(user, Teacher):
            options = ["Manage Courses", "Grade Assignments", "View Student Progress"]
        elif isinstance(user, Receptionist):
            options = ["Manage Enrollments", "Schedule Appointments", "Generate Reports"]
        else:
            options = []

        for i, option in enumerate(options):
            btn = tk.Button(options_window, text=option, command=lambda o=option: self.select_option(o))
            btn.pack(pady=5)

    def select_option(self, option):
        # This method would handle the selected option
        messagebox.showinfo("Option Selected", f"You selected: {option}")

    def show_student_frame(self, student):
        # Clear the login frame
        self.frame.destroy()

        # Create a new frame for the student
        student_frame = tk.Frame(self.root)
        student_frame.pack(pady=20)

        tk.Label(student_frame, text=f"Welcome, {student.username}!").pack()

        # Add buttons for student actions
        tk.Button(student_frame, text="View Courses", command=lambda: self.show_option("View Courses")).pack(pady=5)
        tk.Button(student_frame, text="Submit Assignment", command=lambda: self.show_option("Submit Assignment")).pack(pady=5)
        tk.Button(student_frame, text="Check Grades", command=lambda: self.show_option("Check Grades")).pack(pady=5)

        # Add a logout button
        tk.Button(student_frame, text="Logout", command=self.logout).pack(pady=10)

    def show_option(self, option):
        messagebox.showinfo("Option Selected", f"You selected: {option}")

    def logout(self):
        self.root.destroy()
        new_root = tk.Tk()
        HomePage(new_root)
        new_root.mainloop()

    def show_receptionist_frame(self, receptionist):
        # Clear the login frame
        self.frame.destroy()

        # Create a new frame for the receptionist
        receptionist_frame = tk.Frame(self.root)
        receptionist_frame.pack(pady=20)

        tk.Label(receptionist_frame, text=f"Welcome, {receptionist.username}!").pack()

        # Add buttons for receptionist actions
        tk.Button(receptionist_frame, text="Manage Enrollments", command=lambda: self.show_option("Manage Enrollments")).pack(pady=5)
        tk.Button(receptionist_frame, text="Schedule Appointments", command=lambda: self.show_option("Schedule Appointments")).pack(pady=5)
        tk.Button(receptionist_frame, text="Generate Reports", command=lambda: self.show_option("Generate Reports")).pack(pady=5)

        # Add a logout button
        tk.Button(receptionist_frame, text="Logout", command=self.logout).pack(pady=10)

    def show_teacher_frame(self, teacher):
        # Clear the login frame
        self.frame.destroy()

        # Create a new frame for the teacher
        teacher_frame = tk.Frame(self.root)
        teacher_frame.pack(pady=20)

        tk.Label(teacher_frame, text=f"Welcome, {teacher.username}!").pack()

        # Add buttons for teacher actions
        tk.Button(teacher_frame, text="Manage Courses", command=lambda: self.show_option("Manage Courses")).pack(pady=5)
        tk.Button(teacher_frame, text="Grade Assignments", command=lambda: self.show_option("Grade Assignments")).pack(pady=5)
        tk.Button(teacher_frame, text="View Student Progress", command=lambda: self.show_option("View Student Progress")).pack(pady=5)

        # Add a logout button
        tk.Button(teacher_frame, text="Logout", command=self.logout).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    home_page = HomePage(root)
    root.mainloop()
