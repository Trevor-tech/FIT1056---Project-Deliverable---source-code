import tkinter as tk
from tkinter import ttk, messagebox
from classes.enrollment_class import Enrollment
from classes.user_class import User 
from classes.student_class import Student
from classes.teacher_class import Teacher
from classes.receptionist_class import Receptionist
from classes.staff_class import Staff
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


class ManageEnrollments(tk.Frame):
    def __init__(self, master, home_page, receptionist_user):
        super().__init__(master)
        self.master = master
        self.home_page = home_page
        self.receptionist_user = receptionist_user

        self.enrollment_label = tk.Label(self, text="Manage Enrollments")
        self.enrollment_label.pack(padx=10, pady=10)

        self.enrollment_frame = tk.Frame(self)
        self.enrollment_frame.pack(padx=10, pady=10)

        # Increase the width of the listbox
        self.enrollment_listbox = tk.Listbox(self.enrollment_frame, width=80)  # Changed from 50 to 80
        self.enrollment_listbox.pack(side=tk.LEFT, padx=10, pady=10)

        self.enrollment_scrollbar = tk.Scrollbar(self.enrollment_frame)
        self.enrollment_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.enrollment_listbox.config(yscrollcommand=self.enrollment_scrollbar.set)
        self.enrollment_scrollbar.config(command=self.enrollment_listbox.yview)

        self.load_enrollments()

        self.enroll_button = tk.Button(self, text="Enroll Student", command=self.enroll_student)
        self.enroll_button.pack(padx=10, pady=10)

        self.unenroll_button = tk.Button(self, text="Unenroll Student", command=self.unenroll_student)
        self.unenroll_button.pack(padx=10, pady=10)

        self.back_button = tk.Button(self, text="Back", command=self.back_to_menu)
        self.back_button.pack(padx=10, pady=10)

    def load_enrollments(self):
        try:
            # Use the data_dir variable that's already defined
            file_path = os.path.join(data_dir, "enrollments.txt")
            print(f"Attempting to open file: {os.path.abspath(file_path)}")
            
            if not os.path.exists(file_path):
                print(f"File does not exist: {file_path}")
                print(f"Current working directory: {os.getcwd()}")
                print(f"Contents of data directory:")
                for item in os.listdir(data_dir):
                    print(f"  {item}")
                messagebox.showwarning("File Not Found", f"The enrollments.txt file was not found at {os.path.abspath(file_path)}")
                return

            with open(file_path, "r") as f:
                lines = f.readlines()
                print(f"Number of lines read: {len(lines)}")
                for line in lines:
                    print(f"Processing line: {line.strip()}")
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
            
            print("Finished loading enrollments")
        except FileNotFoundError:
            print(f"FileNotFoundError: {file_path}")
            messagebox.showwarning("File Not Found", f"The enrollments.txt file was not found at {os.path.abspath(file_path)}")
        except Exception as e:
            print(f"Error loading enrollments: {str(e)}")
            messagebox.showerror("Error", f"An error occurred while loading enrollments: {str(e)}")

    def enroll_student(self):
        self.enroll_window = tk.Toplevel(self)
        self.enroll_window.title("Enroll Student")

        self.course_id_label = tk.Label(self.enroll_window, text="Enter course ID (4 digits):")
        self.course_id_label.pack(padx=10, pady=10)

        self.course_id_entry = tk.Entry(self.enroll_window, width=4)
        self.course_id_entry.pack(padx=10, pady=10)

        self.name_label = tk.Label(self.enroll_window, text="Enter student name:")
        self.name_label.pack(padx=10, pady=10)

        self.name_entry = tk.Entry(self.enroll_window)
        self.name_entry.pack(padx=10, pady=10)

        self.date_label = tk.Label(self.enroll_window, text="Enter enrollment date (YYYY-MM-DD):")
        self.date_label.pack(padx=10, pady=10)

        self.date_entry = tk.Entry(self.enroll_window)
        self.date_entry.pack(padx=10, pady=10)

        self.enroll_button = tk.Button(self.enroll_window, text="Enroll", command=self.enroll_student_confirm)
        self.enroll_button.pack(padx=10, pady=10)
        pass

    def enroll_student_confirm(self):
        course_id = self.course_id_entry.get()
        name = self.name_entry.get()
        date = self.date_entry.get()

        if len(course_id) != 4 or not course_id.isdigit():
            messagebox.showerror("Error", "Course ID must be 4 digits")
            return

        # Assuming credit is always 6 for now. You can add a credit entry field if needed.
        credit = "6"

        file_path = os.path.join(data_dir, 'enrollments.txt')
        try:
            with open(file_path, "a", encoding="utf8") as f:
                f.write(f"{course_id},{name},{date}\n")
            
            self.enrollment_listbox.insert(tk.END, f"Course ID: {course_id}, Student Name: {name}, Enrollment Date: {date}, Credit: {credit}")
            messagebox.showinfo("Success", "Student enrolled successfully")
            self.enroll_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to enroll student: {str(e)}")

        self.load_enrollments()  # Reload the enrollments to show the new entry

    def unenroll_student(self):
        # Add code to unenroll a student here
        pass

    def back_to_menu(self):
        self.pack_forget()
        self.home_page.show_receptionist_menu()
