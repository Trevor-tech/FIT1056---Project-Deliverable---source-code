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

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from classes.student_class import Student
from tkinter.messagebox import showinfo
class StudentPage(tk.Tk):
    def __init__(self, student):
        super().__init__()
        self.student = student
        self.title(f"{self.student.username}'s Dashboard")
        self.geometry("1000x1000")
        self.widgets()

    def widgets(self):
        # A welcome label
        welcome_label = tk.Label(self, text=f"Welcome, {self.student.username}!", font=("Arial", 24))
        welcome_label.pack( pady=10)

        # Buttons for students actions
        view_courses_button = tk.Button(self, text="View Courses", command=self.view_courses, font=("Arial", 18))
        view_courses_button.pack(pady=5)

        submit_assignment_button = tk.Button(self, text="Submit Assignment", command=self.submit_assignment, font=("Arial", 18))
        submit_assignment_button.pack(pady=5)

        check_grades_button = tk.Button(self, text="Check Grades", command=self.check_grades, font=("Arial", 18))
        check_grades_button.pack(pady=5)

        # Logout button
        logout_button = tk.Button(self, text="Logout", command=self.logout, font=("Arial", 18))
        logout_button.pack(pady=10)
    
    
    def view_courses(self):
        messagebox.showinfo("Courses", "Here you will see your courses.")

    def submit_assignment(self):
        messagebox.showinfo("Submit Assignment", "Assignment submission functionality.")

    def check_grades(self):
        root=tk.Tk()
        root.title("Overview")
        root.geometry("720x640")
        

    def logout(self):
        self.destroy()
        from UI.home_page import HomePage
        root = tk.Tk()
        home_page = HomePage(root)
        root.mainloop()
