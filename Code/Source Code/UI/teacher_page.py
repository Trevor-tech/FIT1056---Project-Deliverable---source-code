import os
import sys
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
        root.geometry("1000x1000")

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
        # Create a new window for downloading assignments
        download_window = tk.Toplevel(self)
        download_window.title("Grade Assignments")
        download_window.geometry("600x400")

        # Upload button
        download_button = tk.Button(self, text="Download Student Assignment", command=self.upload_file, font=("Forum", 10))
        download_button.pack(pady=20)


        self.download_assignment()

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
