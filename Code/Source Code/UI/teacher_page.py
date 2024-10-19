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
data_dir = os.path.join(source_code_dir, 'assignments')

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

        root = tk.Toplevel(self)
        root.title(f'Create assignment:')
        root.geometry("800x800")

        # Creates a new window.
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
        pass
    
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
        
    def back_to_menu(self):
        """Return to the receptionist menu."""
        # Remove window for uploading file
        self.back_button.master.destroy()
        # Reopen teacher window
        self.deiconify()

    def logout(self):
        self.destroy()
        from UI.home_page import HomePage
        root = tk.Tk()
        home_page = HomePage(root)
        root.mainloop()
