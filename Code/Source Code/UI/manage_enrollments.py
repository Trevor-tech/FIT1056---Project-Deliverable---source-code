import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from classes.enrollment_class import Enrollment
from classes.user_class import User 
from classes.student_class import Student
from classes.teacher_class import Teacher
from classes.receptionist_class import Receptionist
from classes.staff_class import Staff
import UI.student_page
import UI.teacher_page
import UI.receptionist_page


class ManageEnrollments(tk.Frame):
    def __init__(self, master, receptionist_menu, receptionist_user):
        super().__init__(master=master)
        self.master = master
        self.receptionist_menu = receptionist_menu
        self.receptionist_user = receptionist_user

        self.enrollment_label = tk.Label(self, text="Manage Enrollments")
        self.enrollment_label.pack(padx=10, pady=10)

        self.enrollment_frame = tk.Frame(self)
        self.enrollment_frame.pack(padx=10, pady=10)

        self.enrollment_listbox = tk.Listbox(self.enrollment_frame)
        self.enrollment_listbox.pack(side=tk.LEFT, padx=10, pady=10)

        self.enrollment_scrollbar = tk.Scrollbar(self.enrollment_frame)
        self.enrollment_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        self.enrollment_listbox.config(yscrollcommand=self.enrollment_scrollbar.set)
        self.enrollment_scrollbar.config(command=self.enrollment_listbox.yview)

        self.enroll_button = tk.Button(self, text="Enroll Student", command=self.enroll_student)
        self.enroll_button.pack(padx=10, pady=10)

        self.unenroll_button = tk.Button(self, text="Unenroll Student", command=self.unenroll_student)
        self.unenroll_button.pack(padx=10, pady=10)

        self.back_button = tk.Button(self, text="Back", command=self.back_to_menu)
        self.back_button.pack(padx=10, pady=10)

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

        try:
            enrollment = Enrollment(course_id, name, date)
            # Add the enrollment to the database or list of enrollments
            self.enrollment_listbox.insert(tk.END, f"Course ID: {course_id}, Student Name: {name}, Enrollment Date: {date}")
        
            # Write the enrollment information to a text file
            with open("enrollments.txt", "a") as f:
                f.write(f"Course ID: {course_id}, Student Name: {name}, Enrollment Date: {date}\n")
        
            self.enroll_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def unenroll_student(self):
        # Add code to unenroll a student here
        pass

    def back_to_menu(self):
        self.receptionist_menu.show_menu()
        self.place_forget()

class ReceptionistMenu(tk.Frame):
    def __init__(self, master, receptionist_user):
        super().__init__(master=master)
        self.master = master
        self.receptionist_user = receptionist_user

        # ... (other code)

        self.enrollments_button = tk.Button(self, text="Manage Enrollments", command=self.show_enrollments)
        self.enrollments_button.pack(padx=10, pady=10)

    def show_enrollments(self):
        self.hide_menu()
        enrollments = ManageEnrollments(self.master, self, self.receptionist_user)
        enrollments.place(relx=.5, rely=.5, anchor=tk.CENTER)