import os
import sys
# Get the absolute path of the current file
current_file_path = os.path.abspath(__file__)

# Navigate up to the Source Code directory
source_code_dir = os.path.dirname(os.path.dirname(current_file_path))

# Add the Source Code directory to the Python path
sys.path.insert(0, source_code_dir)

# Construct the path to the data directory
data_dir = os.path.join(source_code_dir, 'data/assignments')

# Set the path to the student_progress.txt file
student_progress_file = os.path.join(data_dir, 'student_progress.txt')

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from classes.teacher_class import Teacher
from tkinter.messagebox import showinfo
import PyPDF2
import shutil 

class TeacherPage(tk.Tk):
    def __init__(self, teacher):
        super().__init__()
        self.teacher = teacher
        self.geometry("1000x1000")
        self.widgets()

    def widgets(self):
        # A welcome label
        welcome_label = tk.Label(self, text=f"Welcome, {self.teacher.username}! ({self.teacher.staff_info})", font=("Forum", 16))
        welcome_label.pack( pady=10)

        # Add buttons for teacher actions
        tk.Button(self, text="Create Assignment", command= self.create_assignment, font=("Forum", 10)).pack(pady=5)
        tk.Button(self, text="Grade Assignments", command= self.grade_assignment, font=("Forum", 10)).pack(pady=5)
        tk.Button(self, text="View Student Progress", command=self.view_student_progress, font=("Forum", 10)).pack(pady=5)
        
        # Logout button
        logout_button = tk.Button(self, text="Logout", command=self.logout, font=("Forum", 10))
        logout_button.pack(pady=10)
    
    
    def create_assignment(self):
        self.withdraw()

        # Create a new window
        root = tk.Toplevel(self)
        root.title(f'Create assignment:')
        root.geometry("1000x1000")

        # Creates a new frame
        create_assignment_frame = tk.Frame(root)
        create_assignment_frame.pack(pady=20)
        

        # Add buttons for teacher actions
        upload_file_label = tk.Label(create_assignment_frame, text='Upload File', font=("Forum", 16))
        upload_file_label.pack(pady=10)

        # Label to display selected file
        self.display_file_label = tk.Label(create_assignment_frame, text="No file selected", font=("Forum", 10))
        self.display_file_label.pack(pady=20)

        # Upload button
        upload_button = tk.Button(create_assignment_frame, text="Upload .pdf File", command=self.upload_file, font=("Forum", 10))
        upload_button.pack(pady=20)

        # Back button
        self.back_button = tk.Button(create_assignment_frame, text="Back", command=self.back_to_menu)
        self.back_button.pack(padx=10, pady=10)
    
    def upload_file(self):
        # Open file dialog to select a .txt file
        file_path = filedialog.askopenfilename(
            title="Select a pdf File",
            filetypes=(("Pdf files", "*.pdf"), ("All files", "*.*"))  # Filter only .txt files
        )

        if file_path:
            # Extract the file name from the selected file path
            file_name = os.path.basename(file_path)
            
            # Display selected file path in the label
            self.display_file_label.config(text=f'Selected file: {file_name}')

            # Destination path where the file will be stored in the 'data' subfolder
            destination = os.path.join(data_dir, file_name)

            # Allow you to open and read file
            try:
                # Copy the selected file to the 'data' directory
                shutil.copy(file_path, destination)
                messagebox.showinfo("Success", f"File successfully uploaded to: {destination}")

                # Read and extract content from the PDF file of assignment.
                pdf_text = ""
                with open(file_path, "rb") as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    # Iterate over the pages of the pdf file.
                    for page_num in range(len(pdf_reader.pages)):
                        pdf_page = pdf_reader.pages[page_num]
                        pdf_text += pdf_page.extract_text()
                
                # Display preview of submitted file for teacher to confirm.
                if pdf_text:
                    messagebox.showinfo("File Content Preview (Note, not all contents of the pdf file may be displayed.)", pdf_text[:])
                else:
                    messagebox.showwarning("Warning", "No text content found in the PDF file.")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file: {e}")
        else:
            self.display_file_label(text="No file selected")

    def grade_assignment(self):
        # Create a new window for downloading assignments
        download_window = tk.Toplevel(self)
        download_window.title("Grade Assignments")
        download_window.geometry("600x400")

        # Create new frame
        download_frame = tk.Frame(download_window)
        download_frame.pack(pady=20)
        
        # Upload button
        download_button = tk.Button(download_frame, text="Download Student Assignment", command=self.download_submission, font=("Forum", 10))
        download_button.pack(pady=20)

        # Upload button
        grade_button = tk.Button(download_frame, text="Grade Student Assignment", command=self.grade, font=("Forum", 10))
        grade_button.pack(pady=20)

        # Back button
        back_button = tk.Button(download_frame, text="Back", command=download_window.destroy, font=("Forum", 10))
        back_button.pack(pady=10)

    def grade(self):
        """
        Display the enrolled students for the teacher to grade.
        Only students in the teacher's course are shown.
        """
        ### Displays student progress but this time, allowing teachers to select students and enter grade.
        # Create a new window 
        grade_window = tk.Toplevel(self)
        grade_window.title(f'Grade Assignments')
        grade_window.geometry("1000x600")

        # Extract course ID from teacher's staff info
        teacher_course_id = self.teacher.staff_info.split("-")[0].strip()
        
        # Filter student progress for the teacher's course by the course ID in students.txt
        filtered_student_progress = [student for student in self.teacher.student_progress_details() if student[1].strip() == teacher_course_id]
        
        # Create Treeview frame
        student_progress_frame = tk.Frame(self)
        student_progress_frame.pack(pady=20)

        # Table displaying students and their progress through the assignments.
        self.tree = ttk.Treeview(grade_window, columns=('Student', 'Course ID', 'A1', 'A2', 'A3', 'A4', 'T1', 'T2', 'Average', 'Lessons Completed'), show="headings")
        self.tree.heading('Student', text='Student Name')
        self.tree.heading('Course ID', text='Course ID')
        self.tree.heading('A1', text='A1 (%)')
        self.tree.heading('A2', text='A2 (%)')
        self.tree.heading('A3', text='A3 (%)')
        self.tree.heading('A4', text='A4 (%)')
        self.tree.heading('T1', text='T1 (%)')
        self.tree.heading('T2', text='T2 (%)')
        self.tree.heading('Average', text='Average Mark (%)')
        self.tree.heading('Lessons Completed', text='Lessons Completed (%)')
        
        # Adjust column sizes
        self.tree.column('Student', width=150)
        self.tree.column('Course ID', width=150)
        self.tree.column('A1', width=50)
        self.tree.column('A2', width=50)
        self.tree.column('A3', width=50)
        self.tree.column('A4', width=50)
        self.tree.column('T1', width=50)
        self.tree.column('T2', width=50)
        self.tree.column('Average', width=250)
        self.tree.column('Lessons Completed', width=250)

        # Insert rows
        for row in filtered_student_progress:
            self.tree.insert('', tk.END, values=row)

        self.tree.pack(expand=True, fill=tk.BOTH)
        
        # Bind click event to select student and grade assignment
        self.tree.bind("<ButtonRelease-1>", lambda event: self.on_student_click(event, self.tree, filtered_student_progress))

        # Back button
        back_button = tk.Button(grade_window, text="Back", command=grade_window.destroy, font=("Forum", 10))
        back_button.pack(pady=10)

    def on_student_click(self, event, tree, filtered_student_progress):
        """
        Handle the event when a student row is clicked.
        Open a dialog to enter grades for assignments.
        """
        selected_item = tree.focus()  # Get the selected item
        if not selected_item:
            return

        student_values = tree.item(selected_item, 'values')
        student_name = student_values[0]  # Get the student's name
        course_id = student_values[1]  # Get the course ID

        # Create a popup to select assignment and enter grade
        popup = tk.Toplevel(self)
        popup.title(f"Grade Assignment for {student_name}")
        popup.geometry("400x300")

        # store value selected from dropdown
        assignment_var = tk.StringVar(popup)
        assignment_var.set("Assignment 1")  # Default value

        #Dropdown box to select assignment
        assignments = ["Assignment 1", "Assignment 2", "Assignment 3", "Assignment 4", "Test 1", "Test 2"]
        tk.Label(popup, text="Select Assignment:").pack(pady=10)
        assignment_menu = ttk.Combobox(popup, textvariable=assignment_var, values=assignments)
        assignment_menu.pack(pady=10)

        # Entry for entering grade
        tk.Label(popup, text="Enter Grade (%):").pack(pady=10)
        grade_entry = tk.Entry(popup)
        grade_entry.pack(pady=10)

        # Submit button to save the grade
        submit_button = tk.Button(popup, text="Submit", command=lambda: self.submit_grade(student_name, course_id, assignment_var.get(), grade_entry.get(), popup))
        submit_button.pack(pady=20)

    def submit_grade(self, student_name, course_id, assignment, grade, popup):
        """
        Save the grade entered by the teacher for the selected assignment.
        Update the student's progress in the 'student_progress.txt' file.
        """
        # Check if grade is a valid percentage
        try:
            grade = float(grade)
            if grade < 0 or grade > 100:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid percentage (0-100).")
            return

        # Map the assignment to the correct column in the file
        assignment_map = {
            "Assignment 1": 2,
            "Assignment 2": 3,
            "Assignment 3": 4,
            "Assignment 4": 5,
            "Test 1": 6,
            "Test 2": 7
        }
        
        # Construct the path to the data directory
        data_dir = os.path.join(source_code_dir, 'data')
        
        # Set the path to the student_progress.txt file
        student_progress_file = os.path.join(data_dir, 'student_progress.txt')
        
        # Locate the correct student in the 'student_progress.txt' file and update their grade
        updated_data = []
        with open(student_progress_file, "r") as file:
            lines = file.readlines()
            for line in lines:
                data = line.strip().split(',')
                if data[0] == student_name and data[1] == course_id:
                    # Update the grade for the selected assignment
                    data[assignment_map[assignment]] = str(grade)
                    # Recalculate the average
                    grades = list(map(float, data[2:8]))  # Get assignment and test grades
                    data[8] = str(sum(grades) / len(grades))  # Update average
                updated_data.append(','.join(data))

        # Write the updated data back to the file
        with open(student_progress_file, "w") as file:
            file.write("\n".join(updated_data))

        messagebox.showinfo("Success", f"Grade for {assignment} updated successfully!")

        # Close the popup
        popup.destroy()
        
        # Reload the Treeview to reflect updated grades
        self.refresh_grade_treeview()
    
    def refresh_grade_treeview(self):
        """
        Update grades in the display of students when teacher selects grade students (so both student progress window and grade window reflect the same grades)
        """
        # Extract course ID from teacher's staff info
        teacher_course_id = self.teacher.staff_info.split("-")[0].strip()

        # Filter student progress for the teacher's course
        filtered_student_progress = [student for student in self.teacher.student_progress_details() if student[1].strip() == teacher_course_id]

        # Clear the current rows in the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert updated rows
        for row in filtered_student_progress:
            self.tree.insert('', tk.END, values=row)


    def download_submission(self):
        """
        Allow the user to download the selected assignment PDF file.
        """
        # Create a new window for downloading submissions
        download_window = tk.Toplevel(self)
        download_window.title("Download submission")
        download_window.geometry("600x400")

        
        # Set up columns for the Treeview
        columns = ['Submission Name', 'Download']
        
        # Create the Treeview widget
        tree_frame = ttk.Frame(download_window)
        tree_frame.pack(expand=True, fill=tk.BOTH)

        tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        # Set headers of colummns
        tree.heading('Submission Name', text='Submission Name')
        tree.column('Submission Name', anchor="center", width=400)
        tree.heading('Download', text='Download')
        tree.column('Download', anchor="center", width=100)
        
        # Add vertical scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Load assignment files from the 'submissions' folder
        submissions = self.load_submissions()         
        
        # Insert rows in the Treeview for each submission
        for idx, submission in enumerate(submissions):
            # Insert the submission name
            tree.insert('',tk.END, values=(f'{submission}', 'Download'))

        # when selected row is clicked once, it will call download_selected_submission()
        tree.bind('<ButtonRelease-1>', lambda event: self.download_selected_submission(event, tree))

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
            assignment = item_values[0]  # Get the submission name

            # Call the function to download the selected submission
            self.download_selected_submission(assignment)

    def download_selected_submission(self, event, tree):
        """
        This function handles the downloading of the selected assignment using a single click.
        """
        # Get the selected submission from the Treeview
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "No submission selected.")
            return

        submission = tree.item(selected_item)['values'][0]

        # Construct the path to the data submissions folder
        data_dir = os.path.join(source_code_dir, 'data/submissions')

        # Set subfolder to submissions
        pdf_subfolder = os.path.join(data_dir)

        # Construct the path to the submission PDF file
        pdf_file_path = os.path.join(pdf_subfolder, submission)
        print(f"Attempting to access file: {pdf_file_path}")  # Debugging line

        # When file path does not exist.
        if not os.path.exists(pdf_file_path):
            messagebox.showerror("Error", f"The submission file '{submission}' does not exist.")
            return

        # Ask the user where to save the downloaded file
        save_location = filedialog.asksaveasfilename(
            initialfile=submission,
            title="Save Assignment",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )

        # Displaying informative messages.
        if save_location:
            try:
                # Copy the PDF file to the selected location
                shutil.copy(pdf_file_path, save_location)
                messagebox.showinfo("Download", f"Submission '{submission}' has been downloaded successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to download the submission: {e}")
        else:
            messagebox.showinfo("Cancelled", "Download cancelled.")
            
    def load_submissions(self):
        """
        Load assignment filenames from the 'assignments' folder.
        """
        # Construct the path to the data directory
        data_dir = os.path.join(source_code_dir, 'data/submissions')

        # Define the path to the 'submission' folder
        submission_folder = os.path.join(data_dir)
        print("Submissions folder path:", submission_folder)  # Debug line
        submissions = []

        # Check if the 'submissions' folder exists
        if os.path.exists(submission_folder):
            # Iterate through the folder and collect filenames with .pdf extension
            submissions = [f for f in os.listdir(submission_folder) if f.endswith('.pdf')]
            print(submissions) # Debug line
        return submissions
    
    def view_student_progress(self):
        """
        A function which displays student progress as a table in a new window.
        """
        root = tk.Tk()
        root.title(f'Student Progress:')
        root.geometry("1000x1000")
        #self.frame.destroy()
        
        # Extracting course ID from teacher's staff info
        teacher_course_id = self.teacher.staff_info.split("-")[0].strip()
        
        # Filtering student with matching course ID
        filtered_student_progress = [student for student in self.teacher.student_progress_details() if student[1].strip() == teacher_course_id]
        
        # Creates a new window.
        student_progress_frame = tk.Frame(self)
        student_progress_frame.pack(pady=20)

        # Display table
        columns = ('Student', 'Course ID', 'A1', 'A2', 'A3', 'A4', 'T1', 'T2', 'Average', 'Lessons Completed')
        tree = ttk.Treeview(root, columns=columns, show="headings")
        tree.heading('Student', text='Student Name')
        tree.heading('Course ID', text='Course ID')
        tree.heading('A1', text='A1 (%)')
        tree.heading('A2', text='A2 (%)')
        tree.heading('A3', text='A3 (%)')
        tree.heading('A4', text ='A4 (%)')
        tree.heading('T1', text='T1 (%)')
        tree.heading('T2', text='T2 (%)')
        tree.heading('Average', text='Average Mark (%)')
        tree.heading('Lessons Completed', text='Lessons Completed (%)')
        
        # Adjusting size
        tree.column('Student', width = 150)
        tree.column('Course ID', width = 150)
        tree.column('A1', width = 50)
        tree.column('A2', width = 50)
        tree.column('A3', width = 50)
        tree.column('A4', width = 50)
        tree.column('T1', width = 50)
        tree.column('T2', width = 50)
        tree.column('Average', width = 250)
        tree.column('Lessons Completed', width = 250)

        # Enters extracted data into table 
        for row in filtered_student_progress:
            tree.insert('', tk.END, values = row)

        tree.pack(expand=True, fill=tk.BOTH)
        
    def back_to_menu(self):
        """Return to the teacher menu."""
        # Remove window for uploading file
        self.back_button.master.master.destroy()
        # Reopen teacher window
        self.deiconify()

    def logout(self):
        self.destroy()
        from UI.home_page import HomePage
        root = tk.Tk()
        home_page = HomePage(root)
        root.mainloop()
