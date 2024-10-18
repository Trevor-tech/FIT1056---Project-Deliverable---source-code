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
        # Welcome Text
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
    
    def clear_window(self):
        #Clears the widgets when a button is pressed
        for widget in self.winfo_children():
            widget.destroy()

    def view_courses(self):
        messagebox.showinfo(" Enrolled courses")

    def submit_assignment(self):
        self.clear_window()

        # Set up columns for the Treeview
        columns = ['Assignment Name', 'Submit', 'Status']

        # Create the Treeview widget
        tree_frame = ttk.Frame(self)
        tree_frame.pack(expand=True, fill=tk.BOTH)

        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        self.tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Set the column headings
        for column in columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, anchor="center")

        # Add vertical scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Show assignment and submission status
        assignments = self.load_assignments()
        submissions = self.load_submissions()

        # Insert rows in the Treeview
        for idx, assignment in enumerate(assignments):
            status = 'Submitted' if (self.student.username, assignment) in submissions else 'Not Submitted'
            self.tree.insert('', idx, iid=idx, values=(assignment, '', status))

            # Add a submission button
            button = tk.Button(self.tree, text="Submission", command=lambda a=assignment: self.submit(a))
            self.tree.set(idx, column=1) # Insert the button in the second column
            self.tree.window_create(idx, column=1, window=button)  # Insert the button in the second column


        # Add a back button
        back_button = tk.Button(self, text="Back", command=self.back, font=("Arial", 18))
        back_button.pack(pady=10, side=tk.BOTTOM)

    def load_assignments(self):
        #shows assignments tasked to student
        assignment= os.path.join(data_dir, "assignments.txt")
        assignments = []
        if os.path.exists(assignment):
            with open(assignment, 'r') as f:
                assignments = [line.strip() for line in f.readlines()]
        return assignments

    def load_submissions(self):
        #reads submission file and returns values
        submissions = set()
        submission= os.path.join(data_dir, "submissions.txt")
        if os.path.exists(submission):
            with open(submission, 'r') as f:
                for line in f:
                    username, assignment = line.strip().split(',')
                    submissions.add((username, assignment))
        return submissions

    def submit(self, assignment):
        # Save the submission in submission.txt
        submission= os.path.join(data_dir, "submissions.txt")
        with open(submission, 'a') as f:
            f.write(f'{self.student.username},{assignment}\n')

        # Update the status in the Treeview
        for item in self.tree.get_children():
            item_data = self.tree.item(item)
            if item_data['values'][0] == assignment:
                self.tree.item(item, values=(assignment, '', 'Submitted'))

        messagebox.showinfo("Submit", f"Submitted {assignment}")

    def check_grades(self):
        self.clear_window()

        # Set up Treeview
        columns = ['Assignment 1', 'Assignment 2', 'Assignment 3', 'Assignment 4', 'Test 1', 'Test 2', 'Average', 'Lessons Completed']
        tree = ttk.Treeview(self, columns=columns, show='headings')
        tree.pack(expand=True, fill=tk.BOTH)

        # Set the column headings
        for column in columns:
            tree.heading(column, text=column)
            tree.column(column, anchor="center")

        # Read the grades file and display grades for the logged-in student
        student_data = self.get_student_data(self.student.username)

        if student_data:
            # Insert the student's grades into the Treeview
            tree.insert('', tk.END, values=student_data[2:])
        else:
            messagebox.showwarning("Error", "No data found for this student")

        # A button to go back to the student dashboard
        back_button = tk.Button(self, text="Exit", command=self.back, font=("Arial", 18))
        back_button.pack(pady=10)

    def back(self):
        #Back button will clear window and restore original student dashboard
        self.clear_window()
        self.widgets()

    def get_student_data(self, username):
        student_progress= os.path.join(data_dir, "student_progress.txt")
        if os.path.exists(student_progress):
            with open(student_progress, "r") as file:
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
