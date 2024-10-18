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
    def __init__(self, master, home_page, receptionist_user):
        super().__init__(master)
        self.master = master
        self.home_page = home_page
        self.receptionist_user = receptionist_user

        self.create_widgets()

    def create_widgets(self):
        self.enrolment_label = tk.Label(self, text="Manage Enrollments")
        self.enrolment_label.pack(padx=10, pady=10)

        self.enrollment_frame = tk.Frame(self)
        self.enrollment_frame.pack(padx=10, pady=10)

        # Increase the width of the listbox
        self.enrollment_listbox = tk.Listbox(self.enrollment_frame, width=80)  # Changed from 50 to 80
        self.enrollment_listbox.pack(side=tk.LEFT, padx=10, pady=10)

        self.enrollment_scrollbar = tk.Scrollbar(self.enrollment_frame)
        self.enrollment_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.enrollment_listbox.config(yscrollcommand=self.enrollment_scrollbar.set)
        self.enrollment_scrollbar.config(command=self.enrollment_listbox.yview)

        self.enrol_button = tk.Button(self, text="Enroll Student", command=self.enroll_student)
        self.enrol_button.pack(padx=10, pady=10)

        self.unenrol_button = tk.Button(self, text="Unenroll Student", command=self.unenroll_student)
        self.unenrol_button.pack(padx=10, pady=10)

        self.back_button = tk.Button(self, text="Back", command=self.back_to_menu)
        self.back_button.pack(padx=10, pady=10)

    def show(self):
        self.pack()
        self.load_enrollments()

    def hide(self):
        self.pack_forget()

    def load_enrollments(self):
        self.enrollment_listbox.delete(0, tk.END)  # Clear existing entries
        try:
            file_path = os.path.join(data_dir, "enrollments.txt")
            if not os.path.exists(file_path):
                messagebox.showwarning("File Not Found", f"The enrollments.txt file was not found at {os.path.abspath(file_path)}")
                return

            with open(file_path, "r") as f:
                lines = f.readlines()
                for line in lines:
                    parts = line.strip().split(',')
                    if len(parts) == 3:  # Old format without credit
                        course_id, name, date = parts
                        credit = "6"  # Default credit value
                    elif len(parts) == 4:  # New format with credit
                        course_id, name, date, credit = parts
                    else:
                        print(f"Skipping invalid line: {line.strip()}")
                        continue
                    self.enrollment_listbox.insert(tk.END, f"Course ID: {course_id}, Student Name: {name}, Enrollment Date: {date}, Credit: {credit}")
            
        except Exception as e:
            print(f"Error loading enrollments: {str(e)}")
            messagebox.showerror("Error", f"An error occurred while loading enrollments: {str(e)}")

    def enroll_student(self):
        self.enrol_window = tk.Toplevel(self)
        self.enrol_window.title("Enroll Student")

        self.course_id_label = tk.Label(self.enrol_window, text="Enter course ID (4 digits):")
        self.course_id_label.pack(padx=10, pady=10)

        self.course_id_entry = tk.Entry(self.enrol_window, width=4)
        self.course_id_entry.pack(padx=10, pady=10)

        self.name_label = tk.Label(self.enrol_window, text="Enter student name:")
        self.name_label.pack(padx=10, pady=10)

        self.name_entry = tk.Entry(self.enrol_window)
        self.name_entry.pack(padx=10, pady=10)

        self.date_label = tk.Label(self.enrol_window, text="Enter enrollment date (DD/MM/YYYY):")
        self.date_label.pack(padx=10, pady=10)

        self.date_entry = tk.Entry(self.enrol_window)
        self.date_entry.pack(padx=10, pady=10)

        self.enrol_button = tk.Button(self.enrol_window, text="Enroll", command=self.enrol_student_confirm)
        self.enrol_button.pack(padx=10, pady=10)

    def enrol_student_confirm(self):
        course_id = self.course_id_entry.get()
        name = self.name_entry.get()
        date = self.date_entry.get()

        if len(course_id) != 4 or not course_id.isdigit():
            messagebox.showerror("Error", "Course ID must be 4 digits")
            return
        elif not is_date_valid(date):
            messagebox.showerror("Error", "Invalid date format. Please use DD/MM/YYYY format and ensure the date is within the five-year range starting from 2023.")
            return

        # Assuming credit is always 6 for now. You can add a credit entry field if needed.
        credit = "6"

        file_path = os.path.join(data_dir, 'enrollments.txt')
        try:
            with open(file_path, "a", encoding="utf8") as f:
                f.write(f"{course_id},{name},{date},{credit}\n")
            
            messagebox.showinfo("Success", "Student enrolled successfully")
            self.enrol_window.destroy()
            self.load_enrollments()  # Reload the enrollments to show the new entry
        except Exception as e:
            messagebox.showerror("Error", f"Failed to enroll student: {str(e)}")

    def unenroll_student(self):
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
        file_path = os.path.join(data_dir, 'enrollments.txt')
        try:
            with open(file_path, "r") as f:
                lines = f.readlines()
            
            del lines[index]

            with open(file_path, "w") as f:
                f.writelines(lines)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to unenroll student: {str(e)}")

    def back_to_menu(self):
        self.hide()
        self.home_page.show_receptionist_menu()
