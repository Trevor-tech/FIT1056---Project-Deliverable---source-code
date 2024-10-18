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
from UI.student_page import StudentPage
from UI.teacher_page import TeacherPage
from UI.receptionist_page import ReceptionistPage
#from UI.manage_enrollments import ManageEnrollments

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
 
    """
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
    """
    """
    def select_option(self, option):
        # This method would handle the selected option
    messagebox.showinfo("Option Selected", f"You selected: {option}")
    """
    def show_student_frame(self, student):
        # Closes the HomePage window
        self.root.destroy()  
        
        # Open the student dashboard
        student_page = StudentPage(student)
        student_page.mainloop()
    """
    def show_option(self, option):
        messagebox.showinfo("Option Selected", f"You selected: {option}")

    def logout(self):
        self.root.destroy()
        new_root = tk.Tk()
        HomePage(new_root)
        new_root.mainloop()
    """

    def show_receptionist_frame(self, receptionist):
        # Create a new Toplevel window for the ReceptionistPage
        receptionist_window = tk.Toplevel(self.root)
        receptionist_window.title("Receptionist Page")
        
        # Create the ReceptionistPage, passing the new window, this HomePage instance, and the receptionist user
        receptionist_page = ReceptionistPage(receptionist_window, self, receptionist)
        receptionist_page.pack(fill=tk.BOTH, expand=True)
        
        # Close the HomePage window
        self.root.withdraw()

        # Set up a protocol to exit the application when the ReceptionistPage is closed
        receptionist_window.protocol("WM_DELETE_WINDOW", self.exit_application)

    """
    def show_receptionist_menu(self):
        # This method will be called from ManageEnrollments to return to the receptionist menu
        if hasattr(self, 'manage_enrollments'):
            self.manage_enrollments.pack_forget()
        if hasattr(self, 'receptionist_frame'):
            self.receptionist_frame.pack()
    """
    def show_teacher_frame(self, teacher):
        # Closes the HomePage window
        self.root.destroy()  

        # Open the student dashboard
        teacher_page = TeacherPage(teacher)
        teacher_page.mainloop()
    
    def show_home_page(self):
        self.root.deiconify()  # Show the HomePage window

    def exit_application(self):
        self.root.quit()  # This will stop the mainloop
        self.root.destroy()  # This will destroy all windows

if __name__ == "__main__":
    root = tk.Tk()
    home_page = HomePage(root)
    root.mainloop()
