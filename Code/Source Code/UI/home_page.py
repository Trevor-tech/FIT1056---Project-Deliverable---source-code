"""
The homepage of Empower U allowing users to login and select a series of options depending on what role they play (student, teacher, receptionist)
"""
import sys
import os

# Get the path to the 'Source Code' directory
source_code_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, source_code_dir)

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from classes.user_class import User 
from classes.student_class import Student
from classes.teacher_class import Teacher
from classes.receptionist_class import Receptionist
from classes.staff_class import Staff
import UI.student_page
import UI.teacher_page
import UI.receptionist_page
from UI.manage_enrollments import ManageEnrollments

class HomePage:
    def __init__(self, root):
        self.root = root
        self.root.title("Empower U")
        self.root.geometry("1000x1000")  # Increased height to accommodate logo

        # Define current_dir
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Load and display the logo
        self.logo_image = tk.PhotoImage(file=os.path.join(current_dir, "EmpowerU_logo.png")) # Image was AI generated (ChatGPT, 2024).
        self.logo_label = tk.Label(self.root, image=self.logo_image, width=400, height=400)
        self.logo_label.pack(pady=10)

        # Frame for the login form.
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        # Enter username.
        self.username_var = tk.StringVar()
        self.username_label = tk.Label(self.frame, text="Username:")
        self.username_label.grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(self.frame, textvariable=self.username_var)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        # Enter password.
        self.password_var = tk.StringVar()
        self.password_label = tk.Label(self.frame, text="Password:")
        self.password_label.grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self.frame, show="*", textvariable=self.password_var)
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        # Login button.
        self.login_button = tk.Button(self.frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()

        # Try to authenticate as staff first
        user = Staff.authenticate(username, password)
        
        # If staff authentication fails, try student authentication
        if user is None:
            user = Student.authenticate(username, password)

        if user:
            if isinstance(user, Receptionist):
                self.show_receptionist_frame(user)
            elif isinstance(user, Teacher):
                self.show_teacher_frame(user)
            elif isinstance(user, Student):
                self.show_student_frame(user)
            else:
                print(f"Unknown user type: {type(user)}")
        else:
            if hasattr(self, 'error_label'):
                self.error_label.destroy()
            self.error_label = tk.Label(self.frame, text="Invalid username or password", fg="red", font=("Arial", 10, "bold"))
            self.error_label.grid(row=3, column=0, columnspan=2, pady=5)
 
    def show_options(self, user):
        options_window = tk.Toplevel(self.root)
        options_window.title(f"Welcome, {user.name}")
        options_window.geometry("300x200")

        if isinstance(user, Student):
            options = ["View Courses", "Submit Assignment", "Check Grades"]
        elif isinstance(user, Teacher):
            options = ["Manage Courses", "Grade Assignments", "View Student Progress"]
        elif isinstance(user, Receptionist):
            options = ["Manage Enrollments", "Schedule Appointments", "Generate Reports"]
        else:
            options = []

        for i, option in enumerate(options):
            btn = tk.Button(options_window, text=option, command=lambda o=option: self.select_option(o))
            btn.pack(pady=5)

    def select_option(self, option):
        # This method would handle the selected option
        messagebox.showinfo("Option Selected", f"You selected: {option}")

    def show_student_frame(self, student):
        # Clear the login frame
        self.frame.destroy()

        # Create a new frame for the student
        student_frame = tk.Frame(self.root)
        student_frame.pack(pady=20)

        tk.Label(student_frame, text=f"Welcome, {student.username}!").pack()

        # Add buttons for student actions
        tk.Button(student_frame, text="View Courses", command=lambda: self.show_option("View Courses")).pack(pady=5)
        tk.Button(student_frame, text="Submit Assignment", command=lambda: self.show_option("Submit Assignment")).pack(pady=5)
        tk.Button(student_frame, text="Check Grades", command=lambda: self.show_option("Check Grades")).pack(pady=5)

        # Add a logout button
        tk.Button(student_frame, text="Logout", command=self.logout).pack(pady=10)

    def show_option(self, option):
        messagebox.showinfo("Option Selected", f"You selected: {option}")

    def logout(self):
        self.root.destroy()
        new_root = tk.Tk()
        HomePage(new_root)
        new_root.mainloop()

    def show_receptionist_frame(self, receptionist):
        # Clear the login frame
        if hasattr(self, 'frame'):
            self.frame.destroy()

        # Create a new frame for the receptionist
        self.receptionist_frame = tk.Frame(self.root)
        self.receptionist_frame.pack(pady=20)

        tk.Label(self.receptionist_frame, text=f"Welcome, {receptionist.username}!").pack()

        # Add buttons for receptionist actions
        tk.Button(self.receptionist_frame, text="Manage Enrollments", command=lambda: self.show_manage_enrollments(receptionist)).pack(pady=5)
        tk.Button(self.receptionist_frame, text="Schedule Appointments", command=lambda: self.show_option("Schedule Appointments")).pack(pady=5)
        tk.Button(self.receptionist_frame, text="Generate Reports", command=lambda: self.show_option("Generate Reports")).pack(pady=5)

        # Add a logout button
        tk.Button(self.receptionist_frame, text="Logout", command=self.logout).pack(pady=10)

    def show_manage_enrollments(self, receptionist):
        # Hide the receptionist frame
        self.receptionist_frame.pack_forget()

        # Create and show the ManageEnrollments frame
        self.manage_enrollments = ManageEnrollments(self.root, self, receptionist)
        self.manage_enrollments.pack(expand=True, fill=tk.BOTH)

    def show_receptionist_menu(self):
        # This method will be called from ManageEnrollments to return to the receptionist menu
        if hasattr(self, 'manage_enrollments'):
            self.manage_enrollments.pack_forget()
        if hasattr(self, 'receptionist_frame'):
            self.receptionist_frame.pack()

    def show_teacher_frame(self, teacher):
        # Clear the login frame
        self.frame.destroy()

        # Create a new frame for the teacher
        teacher_frame = tk.Frame(self.root)
        teacher_frame.pack(pady=20)

        tk.Label(teacher_frame, text=f"Welcome, {teacher.username}!").pack()

        # Add buttons for teacher actions
        tk.Button(teacher_frame, text="Manage Courses", command=lambda: self.show_option("Manage Courses")).pack(pady=5)
        tk.Button(teacher_frame, text="Grade Assignments", command=lambda: self.show_option("Grade Assignments")).pack(pady=5)
        tk.Button(teacher_frame, text="View Student Progress", command=self.view_student_progress).pack(pady=5)

        # Add a logout button
        tk.Button(teacher_frame, text="Logout", command=self.logout).pack(pady=10)

    def view_student_progress(self):
        root = tk.Tk()
        root.title(f'Student Progress:')
        root.geometry("800x800")
        #self.frame.destroy()
        
        student_progress_frame = tk.Frame(self.root)
        student_progress_frame.pack(pady=20)

        header = tk.Label(student_progress_frame, text=f'Student Progress:', font=("Arial", 20, "bold"))
        header.grid(row=0, column = 0, columnspan=2, padx=10, pady=10)

        student_progress = Teacher.student_progress_details(self)
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

        for row in student_progress:
            tree.insert('', tk.END, values = row)

        tree.pack(expand=True, fill=tk.BOTH)
        '''
        incrementer = 1
        for results in student_progress:
            result_label = tk.Label(student_progress_frame, text=results)
            result_label.grid(row=incrementer, column=0, columnspan=2, padx=10, pady=10)
            incrementer += 1
        '''

if __name__ == "__main__":
    root = tk.Tk()
    home_page = HomePage(root)
    root.mainloop()
