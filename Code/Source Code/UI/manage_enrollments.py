import tkinter as tk
from tkinter import ttk, messagebox
from classes.enrollment_class import Enrollment
from classes.user_class import User 
from classes.student_class import Student
from classes.teacher_class import Teacher
from classes.receptionist_class import Receptionist
from classes.staff_class import Staff
from Utilities.validator import is_date_valid, is_time_valid
import UI.student_page
import UI.teacher_page
import UI.receptionist_page
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

class ManageEnrollmentsPage(tk.Frame):
    """
    A class to represent the Manage Enrollments page in the application.
    This page allows receptionists to view, add, and remove student enrollments.
    """

    def __init__(self, master, home_page, receptionist_user):
        """
        Initialize the ManageEnrollmentsPage.

        Args:
            master (tk.Tk): The root window.
            home_page (HomePage): The home page instance.
            receptionist_user (Receptionist): The logged-in receptionist user.
        """
        super().__init__(master)
        self.master = master
        self.home_page = home_page
        self.receptionist_user = receptionist_user
        self.master.geometry("1000x1000") 

        self.create_widgets()

    def create_widgets(self):
        """Create and place the widgets for the Manage Enrollments page."""
        # Create main label
        self.enrolment_label = tk.Label(self, text="Manage Enrollments", font=("Forum", 10))
        self.enrolment_label.pack(padx=10, pady=10)

        # Create frame to hold listbox and scrollbar
        self.enrollment_frame = tk.Frame(self)
        self.enrollment_frame.pack(padx=10, pady=10)

        # Create listbox to display enrollments
        self.enrollment_listbox = tk.Listbox(self.enrollment_frame, width=100, font=("Forum", 10))
        self.enrollment_listbox.pack(side=tk.LEFT, padx=10, pady=10)

        # Add scrollbar to listbox
        self.enrollment_scrollbar = tk.Scrollbar(self.enrollment_frame)
        self.enrollment_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure listbox and scrollbar
        self.enrollment_listbox.config(yscrollcommand=self.enrollment_scrollbar.set)
        self.enrollment_scrollbar.config(command=self.enrollment_listbox.yview)

        # Create buttons for enrolling, unenrolling, and going back
        self.enrol_button = tk.Button(self, text="Enroll Student", command=self.enroll_student, font=("Forum", 10))
        self.enrol_button.pack(padx=10, pady=10)

        self.unenrol_button = tk.Button(self, text="Unenroll Student", command=self.unenroll_student, font=("Forum", 10))
        self.unenrol_button.pack(padx=10, pady=10)

        self.back_button = tk.Button(self, text="Back", command=self.back_to_menu, font=("Forum", 10))
        self.back_button.pack(padx=10, pady=10)

    def show(self):
        """Display the Manage Enrollments page and load existing enrollments."""
        self.pack()
        self.load_enrollments()

    def hide(self):
        """Hide the Manage Enrollments page."""
        self.pack_forget()

    def load_enrollments(self):
        """
        Load existing students from students.txt and display them in the listbox.
        """
        self.enrollment_listbox.delete(0, tk.END)  # Clear existing entries
        try:
            file_path = os.path.join(data_dir, "students.txt")
            if not os.path.exists(file_path):
                messagebox.showwarning("File Not Found", f"The students.txt file was not found at {os.path.abspath(file_path)}", font=("Forum", 10))
                return

            with open(file_path, "r") as f:
                lines = f.readlines()
                for line in lines:
                    parts = line.strip().split(',')
                    try:
                        if len(parts) != 5:
                            raise ValueError(f"Invalid number of fields: {len(parts)}")
                        
                        username, password, course_id, enrollment_date, credit = parts
                        self.enrollment_listbox.insert(tk.END, f"Username: {username}, Password: {password}, Course ID: {course_id}, Enrollment Date: {enrollment_date}, Credit: {credit}")
                    except ValueError as e:
                        print(f"Error processing line: {line.strip()}. Error: {str(e)}")
                        continue  # Skip this line and continue with the next
    
        except Exception as e:
            print(f"Error loading enrollments: {str(e)}")
            messagebox.showerror("Error", f"An error occurred while loading enrollments: {str(e)}")

    def enroll_student(self):
        """Open a new window for enrolling a student with last name and first name fields."""
        self.enrol_window = tk.Toplevel(self)
        self.enrol_window.title("Enroll Student")

        tk.Label(self.enrol_window, text="Username:", font=("Forum", 10)).grid(row=1, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(self.enrol_window, font=("Forum", 10))
        self.username_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(self.enrol_window, text="Password:", font=("Forum", 10)).grid(row=2, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self.enrol_window, font=("Forum", 10))
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(self.enrol_window, text="Course ID:", font=("Forum", 10)).grid(row=0, column=0, padx=5, pady=5)
        self.course_id_entry = tk.Entry(self.enrol_window, font=("Forum", 10))
        self.course_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.enrol_window, text="Enrollment Date (DD/MM/YYYY):", font=("Forum", 10)).grid(row=3, column=0, padx=5, pady=5)
        self.enrollment_date_entry = tk.Entry(self.enrol_window, font=("Forum", 10))
        self.enrollment_date_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Button(self.enrol_window, text="Enroll", command=self.enrol_student_confirm, font=("Forum", 10)).grid(row=4, column=0, columnspan=2, pady=10)

    def enrol_student_confirm(self):
        """
        Confirm and process the student enrollment.
        Validates input data and adds the new enrollment to the enrollments.txt file.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()
        course_id = self.course_id_entry.get()
        enrollment_date = self.enrollment_date_entry.get()

        # Validate input data
        if len(course_id) != 4 or not course_id.isdigit():
            messagebox.showerror("Error", "Course ID must be 4 digits", font=("Forum", 10))
            return
        elif not is_date_valid(enrollment_date):
            messagebox.showerror("Error", "Invalid date format. Please use DD/MM/YYYY format and ensure the date is within the five-year range starting from 2023.")
            return

        # Assuming credit is always 6 for now. You can add a credit entry field if needed.
        credit = "6"

        # Add new enrollment to the file
        file_path = os.path.join(data_dir, 'students.txt')
        try:
            with open(file_path, "a", encoding="utf8") as f:
                f.write(f"{username},{password},{course_id},{enrollment_date},{credit}\n")
            
            messagebox.showinfo("Success", "Student enrolled successfully")
            self.enrol_window.destroy()
            self.load_enrollments()  # Reload the enrollments to show the new entry
        except Exception as e:
            messagebox.showerror("Error", f"Failed to enroll student: {str(e)}")
        
        file_path = os.path.join(data_dir, 'student_progress.txt')
        with open(file_path, "a", encoding="utf8") as f:
            f.write(f"{username},{course_id}, 0, 0, 0, 0, 0, 0, 0, 0\n")

    def unenroll_student(self):
        """
        Unenroll a selected student from the enrollment list.
        Prompts for confirmation before removing the enrollment.
        """
        selected_indices = self.enrollment_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("No Selection", "Please select an enrollment to unenroll.")
            return

        selected_index = selected_indices[0]
        enrollment_info = self.enrollment_listbox.get(selected_index)
        
        confirm = messagebox.askyesno("Confirm Unenrollment", f"Are you sure you want to unenroll:\n\n{enrollment_info}")
        if confirm:
            self.remove_enrollment(selected_index)
            self.load_enrollments()  # Reload the list
            messagebox.showinfo("Success", "Student has been unenrolled.")

    def remove_enrollment(self, index):
        """
        Remove a student from the students.txt file.
        
        Args:
            index (int): The index of the enrollment to remove.
        """
        file_path = os.path.join(data_dir, 'students.txt')
        try:
            with open(file_path, "r") as f:
                lines = f.readlines()
            
            del lines[index]

            with open(file_path, "w") as f:
                f.writelines(lines)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to unenroll student: {str(e)}", font=("Forum", 10))

    def back_to_menu(self):
        """Return to the receptionist menu."""
        self.hide()
        self.home_page.show_receptionist_menu()
