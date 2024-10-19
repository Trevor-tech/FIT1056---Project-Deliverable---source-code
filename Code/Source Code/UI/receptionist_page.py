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
from Utilities.validator import is_date_valid
import UI.teacher_page
import UI.receptionist_page
from tkinter.messagebox import showinfo
from UI.manage_enrollments import ManageEnrollmentsPage

class ReceptionistPage(tk.Frame):
    def __init__(self, master, home_page, receptionist_user):
        super().__init__(master)
        self.master = master
        self.home_page = home_page
        self.receptionist_user = receptionist_user
        self.master.geometry("1000x1000")

        self.manage_enrollments_page = None  # Initialize to None

        self.create_widgets()
        self.pack(fill=tk.BOTH, expand=True)  # Make sure the frame fills the window

    def create_widgets(self):
        # Clear any existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        # Create a main frame to hold all widgets
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # A welcome label
        welcome_label = tk.Label(main_frame, text=f"Welcome, {self.receptionist_user.username}!", font=("Forum", 16))
        welcome_label.pack(pady=20)

        # Add buttons for receptionist actions
        button_frame = tk.Frame(main_frame)
        button_frame.pack(expand=True)

        tk.Button(button_frame, text="Manage Enrolments", command=self.show_manage_enrollments, font=("Forum", 10)).pack(pady=10)
        tk.Button(button_frame, text="Schedule Appointments", command=self.schedule_appointments, font=("Forum", 10)).pack(pady=10)
        tk.Button(button_frame, text="Generate Reports", command=self.generate_reports, font=("Forum", 10)).pack(pady=10)
        
        # Logout button
        logout_button = tk.Button(button_frame, text="Logout", command=self.logout, font=("Forum", 10))
        logout_button.pack(pady=20)

    def show_manage_enrollments(self):
        if self.manage_enrollments_page is None:
            self.manage_enrollments_page = ManageEnrollmentsPage(self.master, self, self.receptionist_user)
        self.pack_forget()
        self.manage_enrollments_page.show()

    def show_receptionist_menu(self):
        if self.manage_enrollments_page:
            self.manage_enrollments_page.hide()
        self.pack()
        # We don't need to call create_widgets() here anymore

    def schedule_appointments(self):
        pass

    def generate_reports(self):
        pass

    def logout(self):
        self.master.destroy()  # Close the ReceptionistPage window
        self.home_page.show_home_page()  # Show the HomePage