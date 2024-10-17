import os
import sys
import csv
# Get the absolute path of the current file
current_file_path = os.path.abspath(__file__)

# Navigate up to the Source Code directory
source_code_dir = os.path.dirname(os.path.dirname(current_file_path))

# Add the Source Code directory to the Python path
sys.path.insert(0, source_code_dir)

# Construct the path to the data directory
data_dir = os.path.join(source_code_dir, 'data')

# Set the path to the student_progress.txt file
student_progress_file = os.path.join(data_dir, 'student_progress.txt')

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
        messagebox.showinfo(" Enrolled courses")

    def submit_assignment(self):
        messagebox.showinfo("Submit Assignment", "Assignment submission functionality.")

    def check_grades(self):
        # Create a new window to display the grades
        grades_window = tk.Toplevel(self)
        grades_window.title("Overview")
        grades_window.geometry("720x640")

        # Set up Treeview
        columns = ['Assignment 1', 'Assignment 2', 'Assignment 3', 'Assignment 4', 'Test 1', 'Test 2', 'Average', 'Lessons Completed']

        tree = ttk.Treeview(grades_window, columns=columns, show='headings')
        tree.pack(expand=True, fill=tk.BOTH)

        # Set the column headings
        for column in columns:
            tree.heading(column, text=column)
            tree.column(column, anchor="center")

        # Read the grades file and display grades for the logged-in student
        student_data = self.get_student_data(self.student.username)

        if student_data:
            # Insert the student's grades into the Treeview
            tree.insert('', tk.END, values=student_data[2:])  # Only insert grade-related data
        else:
            messagebox.showwarning("Error", "No data found for this student")

    def get_student_data(self, username):
        """Read the grades file and return the grades for the given username."""
        if os.path.exists(student_progress_file):
            with open(student_progress_file, "r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                for row in reader:
                    if row[0] == username:  # Match the username
                        return row
        return None
        

    def logout(self):
        self.destroy()
        from UI.home_page import HomePage
        root = tk.Tk()
        home_page = HomePage(root)
        root.mainloop()
