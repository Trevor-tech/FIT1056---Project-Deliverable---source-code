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
from classes.receptionist_class import Receptionist
import UI.teacher_page
import UI.receptionist_page
from tkinter.messagebox import showinfo

class ReceptionistPage(tk.Tk):
    def __init__(self, receptionist):
        super().__init__()
        self.receptionist = receptionist
        self.geometry("1000x1000")
        self.widgets()

    def widgets(self):
        # A welcome label
        welcome_label = tk.Label(self, text=f"Welcome, {self.receptionist.username}!", font=("Arial", 24))
        welcome_label.pack( pady=10)

        # Add buttons for receptionist actions
        tk.Button(self, text="Manage Enrolments", command = self.show_manage_enrolments, font=("Arial", 18)).pack(pady=5)
        tk.Button(self, text="Schedule Appointments", command= self.schedule_appointments, font=("Arial", 18)).pack(pady=5)
        tk.Button(self, text="Generate Reports", command= self.generate_reports, font=("Arial", 18)).pack(pady=5)
        
        # Logout button
        logout_button = tk.Button(self, text="Logout", command=self.logout, font=("Arial", 18))
        logout_button.pack(pady=10)
    
    def show_manage_enrolments(self):
        root = tk.Tk()
        root.title(f'Manage Enrolments:')
        root.geometry("800x800")

        # Hide current widgets to show ManageEnrolments
        #for widget in self.winfo_children():
         #   widget.pack_forget()

        # Create and display instance of ManageEnrolments
        manage_enrolments_page = ManageEnrolments(self)
        manage_enrolments_page.pack(fill="both", expand=True)

    def schedule_appointments(self):
        pass

    def generate_reports(self):
        pass

    def logout(self):
        self.destroy()
        from UI.home_page import HomePage
        root = tk.Tk()
        home_page = HomePage(root)
        root.mainloop()


class ManageEnrolments(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)  # Initialize the tk.Frame
        self.parent = parent  # Store reference to parent
        
        self.enrolment_label = tk.Label(self, text="Manage Enrolments")
        self.enrolment_label.pack(padx=10, pady=10)

        self.enrolment_frame = tk.Frame(self)
        self.enrolment_frame.pack(padx=10, pady=10)

        # Increase the width of the listbox
        self.enrolment_listbox = tk.Listbox(self.enrolment_frame, width=80)  # Changed from 50 to 80
        self.enrolment_listbox.pack(side=tk.LEFT, padx=10, pady=10)

        self.enrolment_scrollbar = tk.Scrollbar(self.enrolment_frame)
        self.enrolment_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.enrolment_listbox.config(yscrollcommand=self.enrolment_scrollbar.set)
        self.enrolment_scrollbar.config(command=self.enrolment_listbox.yview)

        self.load_enrolments()

        self.enrol_button = tk.Button(self, text="Enrol Student", command=self.enrol_student)
        self.enrol_button.pack(padx=10, pady=10)

        self.unenrol_button = tk.Button(self, text="Unenrol Student", command=self.unenrol_student)
        self.unenrol_button.pack(padx=10, pady=10)

        #self.back_button = tk.Button(self, text="Back", command=self.back_to_menu)
        #self.back_button.pack(padx=10, pady=10)
    
    

    def load_enrolments(self):
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
                messagebox.showwarning("File Not Found", f"The enrolments.txt file was not found at {os.path.abspath(file_path)}")
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
                    self.enrolment_listbox.insert(tk.END, f"Course ID: {course_id}, Student Name: {name}, Enrolment Date: {date}, Credit: {credit}")
            
            print("Finished loading enrollments")
        except FileNotFoundError:
            print(f"FileNotFoundError: {file_path}")
            messagebox.showwarning("File Not Found", f"The enrolments.txt file was not found at {os.path.abspath(file_path)}")
        except Exception as e:
            print(f"Error loading enrolments: {str(e)}")
            messagebox.showerror("Error", f"An error occurred while loading enrollments: {str(e)}")

    def enrol_student(self):
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

        self.date_label = tk.Label(self.enrol_window, text="Enter enrollment date (YYYY-MM-DD):")
        self.date_label.pack(padx=10, pady=10)

        self.date_entry = tk.Entry(self.enrol_window)
        self.date_entry.pack(padx=10, pady=10)

        self.enrol_button = tk.Button(self.enrol_window, text="Enroll", command=self.enrol_student_confirm)
        self.enrol_button.pack(padx=10, pady=10)
        pass

    def enrol_student_confirm(self):
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
            
            self.enrolment_listbox.insert(tk.END, f"Course ID: {course_id}, Student Name: {name}, Enrolment Date: {date}, Credit: {credit}")
            messagebox.showinfo("Success", "Student enroled successfully")
            self.enrol_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to enrol student: {str(e)}")

        self.load_enrolments()  # Reload the enrollments to show the new entry

    def unenrol_student(self):
        # Add code to unenroll a student here
        pass

    


    