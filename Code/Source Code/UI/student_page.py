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
from classes.course_class import Course
from classes.student_class import Student
from tkinter.messagebox import showinfo
from tkinter import filedialog
import PyPDF2
import shutil 

class StudentPage(tk.Tk):
    def __init__(self, student):
        super().__init__()
        self.student = student
        self.title(f"{self.student.username}'s Dashboard")
        self.geometry("1000x1000")
        self.widgets()

    def widgets(self):
        # Welcome Text
        welcome_label = tk.Label(self, text=f"Welcome, {self.student.username}!", font=("Forum", 16))
        welcome_label.pack( pady=10)

        # Buttons for students actions
        view_courses_button = tk.Button(self, text="View Courses", command=self.view_courses, font=("Forum", 10))
        view_courses_button.pack(pady=5)

        # Download assignment button
        download_assignment_button = tk.Button(self, text="Download Assignment", command=self.download_assignment, font=("Forum", 10))
        download_assignment_button.pack(pady=5)

        # Submit assignment button
        submit_assignment_button = tk.Button(self, text="Submit Assignment", command=self.submit_assignment, font=("Forum", 10))
        submit_assignment_button.pack(pady=5)

        # Check grades button
        check_grades_button = tk.Button(self, text="Check Grades", command=self.check_grades, font=("Forum", 10))
        check_grades_button.pack(pady=5)

        # Logout button
        logout_button = tk.Button(self, text="Logout", command=self.logout, font=("Forum", 10))
        logout_button.pack(pady=10)
    
    def clear_window(self):
        #Clears the widgets when a button is pressed
        for widget in self.winfo_children():
            widget.destroy()

    def view_courses(self):
        self.clear_window()

        # Treeview Frame
        tree_frame = tk.Frame(self)
        tree_frame.pack(expand=True, fill=tk.BOTH)

        # Set up columns for the Treeview
        columns = ['Course ID', 'Course Name', 'Credits']

        # Create the Treeview widget
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        self.tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Set the column headings
        for column in columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, anchor="center")

        # Add vertical scrollbar for the Treeview
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Load and display courses
        self.load_and_display_courses()

        # Event binding to detect when a course is selected
        self.tree.bind('<<TreeviewSelect>>', self.on_course_select)

        # Button Frame (below Treeview)
        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X, pady=10)

        # Create the Enroll and Unenroll buttons (initially disabled)
        self.enroll_button = tk.Button(button_frame, text="Enroll", state=tk.DISABLED, command=self.enroll_course)
        self.enroll_button.pack(side=tk.LEFT, padx=5)

        self.unenroll_button = tk.Button(button_frame, text="Unenroll", state=tk.DISABLED, command=self.unenroll_course)
        self.unenroll_button.pack(side=tk.LEFT, padx=5)

        # Back button to return to the dashboard
        back_button = tk.Button(self, text="Back", command=self.back)
        back_button.pack(pady=10)

    def load_and_display_courses(self):
        """
        Load the courses from the text file and display them in the Treeview.
        """
        courses = self.load_courses()

        # Insert rows in the Treeview for each course
        for idx, course in enumerate(courses):
            course_id, course_name, credits = course
            self.tree.insert('', idx, iid=idx, values=(course_id, course_name, credits))

    def load_courses(self):
        """
        Load courses from the 'courses.txt' file and return them as a list of tuples.
        """
        courses_file_path = os.path.join(data_dir, 'courses.txt')
        courses = []
        if os.path.exists(courses_file_path):
            with open(courses_file_path, "r", encoding="utf8") as file:
                for line in file:
                    course_data = line.strip().split(",")
                    if len(course_data) == 3:
                        course_id, course_name, credits = course_data
                        courses.append((course_id, course_name, credits))
        else:
            messagebox.showerror("Error", "Courses file not found.")
        return courses

    def on_course_select(self, event):
        """
        Event handler when a course is selected in the Treeview.
        """
        selected_item = self.tree.selection()
        if selected_item:
            # Get the course details from the selected row
            selected_course = self.tree.item(selected_item[0], 'values')
            self.selected_course_id = selected_course[0]  # Assuming course ID is in the first column

            # Load the students' data from the file
            students_file_path = os.path.join(data_dir, "students.txt")
            
            # Initially disable both buttons
            self.enroll_button.config(state=tk.NORMAL)    # Enable the enroll button
            self.unenroll_button.config(state=tk.DISABLED)  # Disable the unenroll button
            
            try:
                with open(students_file_path, "r", encoding="utf8") as rf:
                    lines = rf.readlines()
                
                # Check if the username and unit code are present
                enrolled = False
                for line in lines:
                    parts = line.strip().split(",")
                    if len(parts) > 1:  # Ensure there are enough parts
                        username = parts[0]
                        unit_code = parts[2]  # Adjust the index based on your file structure
                        
                        if username == self.student.username and unit_code == self.selected_course_id:
                            enrolled = True
                            break
                
                # Set button states based on enrollment status
                if enrolled:
                    self.enroll_button.config(state=tk.DISABLED)  # Disable the enroll button
                    self.unenroll_button.config(state=tk.NORMAL)    # Enable the unenroll button
                else:
                    self.enroll_button.config(state=tk.NORMAL)      # Enable the enroll button
                    self.unenroll_button.config(state=tk.DISABLED)  # Disable the unenroll button

            except FileNotFoundError:
                print(f"The file {students_file_path} does not exist.")

    def enroll_course(self):
        """
        Enroll the student in the selected course.
        """
        if self.selected_course_id:
            self.student.enroll(self.selected_course_id)
            messagebox.showinfo("Enroll", f"Enrolled in {self.selected_course_id}")
            self.enroll_button.config(state=tk.DISABLED)
            self.unenroll_button.config(state=tk.NORMAL)

    def unenroll_course(self):
        """
        Unenroll the student from the selected course.
        """
        if self.selected_course_id:
            self.student.unenroll(self.selected_course_id)
            messagebox.showinfo("Unenroll", f"Unenrolled from {self.selected_course_id}")
            self.enroll_button.config(state=tk.NORMAL)
            self.unenroll_button.config(state=tk.DISABLED)
    
    def submit_assignment(self):
        """
        Open a new window for submitting assignments, where the student can select 
        an assignment and upload a PDF file.
        """
        # Create a new window for submitting assignments
        submit_window = tk.Toplevel(self)
        submit_window.title("Submit Assignment")
        submit_window.geometry("600x400")

        # Set up the window layout
        label = tk.Label(submit_window, text="Select an Assignment to Submit", font=("Forum", 14))
        label.pack(pady=10)

        # Create a Listbox to display available assignments
        assignments = self.load_assignments()

        assignment_listbox = tk.Listbox(submit_window, selectmode=tk.SINGLE, font=("Forum", 12))
        assignment_listbox.pack(pady=10, padx=20, expand=True, fill=tk.BOTH)

        # Populate the Listbox with available assignments
        for assignment in assignments:
            assignment_listbox.insert(tk.END, assignment)

        # Button to choose a file and submit the selected assignment
        submit_button = tk.Button(submit_window, text="Submit PDF", command=lambda: self.submit_pdf(assignment_listbox, submit_window))
        submit_button.pack(pady=10)

        # Back button to close the submission window
        back_button = tk.Button(submit_window, text="Back", command=submit_window.destroy, font=("Forum", 12))
        back_button.pack(pady=10)

    def submit_pdf(self, assignment_listbox, submit_window):
        """
        Handles the submission of a PDF file for the selected assignment.
        """
        # Get the selected assignment
        selected_index = assignment_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("No Selection", "Please select an assignment first.")
            return

        selected_assignment = assignment_listbox.get(selected_index)

        # Open a file dialog to select the PDF file
        file_path = filedialog.askopenfilename(
            title="Select PDF file",
            filetypes=[("PDF files", "*.pdf")]
        )

        # Error messages.
        if not file_path:
            messagebox.showwarning("No File", "No file was selected for submission.")
            return

        if not file_path.endswith('.pdf'):
            messagebox.showerror("Invalid File", "Only PDF files are allowed.")
            return

        # Define the target directory for storing submissions
        submissions_dir = os.path.join(data_dir, "submissions")
        if not os.path.exists(submissions_dir):
            os.makedirs(submissions_dir)  # Create the directory if it doesn't exist

        # Construct the path to save the PDF (e.g., username_assignment.pdf)
        new_file_path = os.path.join(submissions_dir)

        # Copy the PDF file to the submissions directory
        try:
            shutil.copy(file_path, new_file_path)

            # Save the submission record in submissions.txt
            self.save_submission(self.student.username, selected_assignment)

            # Display a success message
            messagebox.showinfo("Success", f"Assignment '{selected_assignment}' has been submitted successfully!")

            # Close the submission window after successful submission
            submit_window.destroy()
        except Exception as e:
            messagebox.showerror("Submission Failed", f"An error occurred while submitting the file: {e}")

    def save_submission(self, username, assignment):
        """
        Save the submission record in submissions.txt.
        """
        submission_file = os.path.join(data_dir, "submissions.txt")
        with open(submission_file, 'a') as f:
            f.write(f'{username},{assignment}\n')

    def download_assignment(self):
        """
        Allow the user to download the selected assignment PDF file.
        """
        # Create a new window for downloading assignments
        download_window = tk.Toplevel(self)
        download_window.title("Download Assignments")
        download_window.geometry("600x400")

        
        # Set up columns for the Treeview
        columns = ['Assignment Name', 'Download']
        
        # Create the Treeview widget
        tree_frame = ttk.Frame(download_window)
        tree_frame.pack(expand=True, fill=tk.BOTH)

        tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        # Set headers of colummns
        tree.heading('Assignment Name', text='Assignment Name')
        tree.column('Assignment Name', anchor="center", width=400)
        tree.heading('Download', text='Download')
        tree.column('Download', anchor="center", width=100)
        
        # Add vertical scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Load assignment files from the 'assignments' folder
        assignments = self.load_assignments()         
        
        # Insert rows in the Treeview for each assignment
        for assignment in enumerate(assignments):
            # Insert the assignment name
            tree.insert('', tk.END, values=(assignment, 'Download'))

        # when selected row is clicked once, it will call download_selected_assignment()
        tree.bind('<ButtonRelease-1>', lambda event: self.download_selected_assignment(event, tree))

        # Back button
        back_button = tk.Button(download_window, text="Back", command=download_window.destroy, font=("Forum", 10))
        back_button.pack(pady=10)

    def on_treeview_click(self, tree):
        """
        Handle the event when a row in the Treeview is double-clicked for downloading the assignment.
        """
        selected_item = tree.selection()
        if selected_item:
            item_values = tree.item(selected_item, 'values')
            assignment = item_values[0]  # Get the assignment name

            # Call the function to download the selected assignment
            self.download_selected_assignment(assignment)

    def download_selected_assignment(self, event, tree):
        """
        This function handles the downloading of the selected assignment using a single click.
        """
        # Get the selected assignment from the Treeview
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "No assignment selected.")
            return

        assignment = tree.item(selected_item)['values'][0]

        # Set subfolder to assignments
        pdf_subfolder = os.path.join(data_dir, 'assignments')

        # Construct the path to the assignment PDF file
        pdf_file_path = os.path.join(pdf_subfolder, assignment)

        # When file path does not exist.
        if not os.path.exists(pdf_file_path):
            messagebox.showerror("Error", f"The assignment file '{assignment}' does not exist.")
            return

        # Ask the user where to save the downloaded file
        save_location = filedialog.asksaveasfilename(
            initialfile=assignment,
            title="Save Assignment",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )

        # Displaying informative messages.
        if save_location:
            try:
                # Copy the PDF file to the selected location
                shutil.copy(pdf_file_path, save_location)
                messagebox.showinfo("Download", f"Assignment '{assignment}' has been downloaded successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to download the assignment: {e}")
        else:
            messagebox.showinfo("Cancelled", "Download cancelled.")
            
    def load_assignments(self):
        """
        Load assignment filenames from the 'assignments' folder.
        """
        # Define the path to the 'assignments' folder
        assignments_folder = os.path.join(data_dir, 'assignments')
        print("Assignments folder path:", assignments_folder)  # Debug line
        assignments = []

        # Check if the 'assignments' folder exists
        if os.path.exists(assignments_folder):
            # Iterate through the folder and collect filenames with .pdf extension
            assignments = [f for f in os.listdir(assignments_folder) if f.endswith('.pdf')]
            print("Loaded Assignments:", assignments)  # Debug line
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

        # Create a frame
        frame = tk.Frame(self)
        frame.pack(expand=True, fill=tk.BOTH)

        # Set up columns for displaying grades
        columns = ['Assessment', 'Score(%)']

        # Create a Treeview widget
        tree = ttk.Treeview(frame, columns=columns, show='headings')
        tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Set the column headings
        for column in columns:
            tree.heading(column, text=column)
            tree.column(column, anchor="center")

        # Add a vertical scrollbar for the Treeview
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Read the grades for the logged-in student
        student_data = self.get_student_data(self.student.username)

        if student_data:
            # Define the assessments
            assessments = [
                'Assignment 1', 'Assignment 2', 'Assignment 3', 'Assignment 4',
                'Test 1', 'Test 2', 'Average', 'Lessons Completed'
            ]

            # Insert rows into the Treeview with assessment names and corresponding grades
            for idx, assessment in enumerate(assessments):
                score = student_data[idx + 2]
                tree.insert('', tk.END, values=(assessment, score))
        else:
            messagebox.showwarning("Error", "No data found for this student")

        # A button to go back to the student dashboard
        back_button = tk.Button(self, text="Exit", command=self.back, font=("Forum", 10))
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
