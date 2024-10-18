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
from classes.teacher_class import Teacher
from tkinter.messagebox import showinfo

class TeacherPage(tk.Tk):
    def __init__(self, teacher):
        super().__init__()
        self.teacher = teacher
        self.geometry("1000x1000")
        self.widgets()

    def widgets(self):
        # A welcome label
        welcome_label = tk.Label(self, text=f"Welcome, {self.teacher.username}!", font=("Arial", 24))
        welcome_label.pack( pady=10)

        # Add buttons for teacher actions
        tk.Button(self, text="Manage Courses", command=lambda: self.show_option, font=("Arial", 18)).pack(pady=5)
        tk.Button(self, text="Grade Assignments", command=lambda: self.grade_assignment, font=("Arial", 18)).pack(pady=5)
        tk.Button(self, text="View Student Progress", command=self.view_student_progress, font=("Arial", 18)).pack(pady=5)
        
        # Logout button
        logout_button = tk.Button(self, text="Logout", command=self.logout, font=("Arial", 18))
        logout_button.pack(pady=10)
    
    
    def manage_courses(self):
        messagebox.showinfo("Manage Courses")

    def grade_assignment(self):
        messagebox.showinfo("Grade Assignment")
    
    def view_student_progress(self):
        """
        A function which displays student progress as a table in a new window.
        """
        root = tk.Tk()
        root.title(f'Student Progress:')
        root.geometry("800x800")
        #self.frame.destroy()
        
        # Creates a new window.
        student_progress_frame = tk.Frame(self)
        student_progress_frame.pack(pady=20)

        student_progress = Teacher.student_progress_details(self) # Calls method from Teacher class which extracts stored data of student progress.

        # Display table
        columns = ('Student', 'Student ID', 'A1', 'A2', 'A3', 'A4', 'T1', 'T2', 'Average', 'Lessons Completed')
        tree = ttk.Treeview(root, columns=columns, show="headings")
        tree.heading('Student', text='Student Name')
        tree.heading('Student ID', text='Student ID')
        tree.heading('A1', text='A1 (%)')
        tree.heading('A2', text='A2 (%)')
        tree.heading('A3', text='A3 (%)')
        tree.heading('A4', text ='A4 (%)')
        tree.heading('T1', text='T1 (%)')
        tree.heading('T2', text='T2 (%)')
        tree.heading('Average', text='Average Mark (%)')
        tree.heading('Lessons Completed', text='Lessons Completed (%)')
        tree.column('Student', width = 150)
        tree.column('Student ID', width = 150)
        tree.column('A1', width = 50)
        tree.column('A2', width = 50)
        tree.column('A3', width = 50)
        tree.column('A4', width = 50)
        tree.column('T1', width = 50)
        tree.column('T2', width = 50)
        tree.column('Average', width = 250)
        tree.column('Lessons Completed', width = 250)

        # Enters extracted data into table 
        for row in student_progress:
            tree.insert('', tk.END, values = row)

        tree.pack(expand=True, fill=tk.BOTH)
        

    def logout(self):
        self.destroy()
        from UI.home_page import HomePage
        root = tk.Tk()
        home_page = HomePage(root)
        root.mainloop()
