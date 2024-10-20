import tkinter as tk
from tkinter import ttk, messagebox
from classes.receptionist_class import Receptionist
from Utilities.validator import is_date_valid, is_time_valid
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

class ScheduleAppointmentsPage(tk.Frame):
    """
    A class to represent the Schedule Appointments page in the application.
    This page allows receptionists to schedule appointments for students.
    """

    def __init__(self, master, home_page, receptionist_user):
        """
        Initialize the ScheduleAppointmentsPage.

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
        self.appointment_label = tk.Label(self, text="Schedule Appointments", font=("Forum", 10))
        self.appointment_label.pack(padx=10, pady=10)

        # Create frame to hold listbox and scrollbar
        self.appointment_frame = tk.Frame(self)
        self.appointment_frame.pack(padx=10, pady=10)

        # Create listbox to display enrollments
        self.appointment_listbox = tk.Listbox(self.appointment_frame, width=100, font=("Forum", 10))
        self.appointment_listbox.pack(side=tk.LEFT, padx=10, pady=10)

        # Add scrollbar to listbox
        self.appointment_scrollbar = tk.Scrollbar(self.appointment_frame)
        self.appointment_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure listbox and scrollbar
        self.appointment_listbox.config(yscrollcommand=self.appointment_scrollbar.set)
        self.appointment_scrollbar.config(command=self.appointment_listbox.yview)

        # Create buttons for enrolling, unenrolling, and going back
        self.schedule_button = tk.Button(self, text="Schedule Appointment", command=self.schedule_appointment, font=("Forum", 10))
        self.schedule_button.pack(padx=10, pady=10)

        self.unschedule_button = tk.Button(self, text="Unschedule Appointment", command=self.unschedule_appointment, font=("Forum", 10))
        self.unschedule_button.pack(padx=10, pady=10)

        self.back_button = tk.Button(self, text="Back", command=self.back_to_menu, font=("Forum", 10))
        self.back_button.pack(padx=10, pady=10)

    def show(self):
        """Display the Schedule Appointments page and load existing appointments."""
        self.pack()
        self.load_appointments()

    def hide(self):
        """Hide the Schedule Appointments page."""
        self.pack_forget()

    def load_appointments(self):
        """
        Load existing students from students.txt and display them in the listbox.
        """
        self.appointment_listbox.delete(0, tk.END)  # Clear existing entries
        try:
            file_path = os.path.join(data_dir, "appointments.txt")
            if not os.path.exists(file_path):
                messagebox.showwarning("File Not Found", f"The appointments.txt file was not found at {os.path.abspath(file_path)}", font=("Forum", 10))
                return

            with open(file_path, "r") as f:
                lines = f.readlines()
                for line in lines:
                    parts = line.strip().split(',')
                    try:
                        if len(parts) != 5:
                            raise ValueError(f"Invalid number of fields: {len(parts)}")
                        
                        username, course_id, appointment_date, appointment_time, meeting_link = parts
                        self.appointment_listbox.insert(tk.END, f"Username: {username}, Course ID: {course_id}, Appointment Date: {appointment_date}, Appointment Time: {appointment_time}, Meeting Link: {meeting_link}")
                    except ValueError as e:
                        print(f"Error processing line: {line.strip()}. Error: {str(e)}")
                        continue  # Skip this line and continue with the next
    
        except Exception as e:
            print(f"Error loading appointments: {str(e)}")
            messagebox.showerror("Error", f"An error occurred while loading appointments: {str(e)}")

    def schedule_appointment(self):
        """Open a new window for scheduling an appointment with username, course ID, appointment date, appointment time, and meeting link fields."""
        self.appointment_window = tk.Toplevel(self)
        self.appointment_window.title("Schedule Appointment")

        tk.Label(self.appointment_window, text="Username:", font=("Forum", 10)).grid(row=1, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(self.appointment_window, font=("Forum", 10))
        self.username_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(self.appointment_window, text="Course ID:", font=("Forum", 10)).grid(row=0, column=0, padx=5, pady=5)
        self.course_id_entry = tk.Entry(self.appointment_window, font=("Forum", 10))
        self.course_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.appointment_window, text="Appointment Date (DD/MM/YYYY):", font=("Forum", 10)).grid(row=3, column=0, padx=5, pady=5)
        self.appointment_date_entry = tk.Entry(self.appointment_window, font=("Forum", 10))
        self.appointment_date_entry.grid(row=3, column=1, padx=5, pady=5)
        
        tk.Label(self.appointment_window, text="Appointment Time (HH:MM):", font=("Forum", 10)).grid(row=4, column=0, padx=5, pady=5)
        self.appointment_time_entry = tk.Entry(self.appointment_window, font=("Forum", 10))
        self.appointment_time_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(self.appointment_window, text="Meeting Link:", font=("Forum", 10)).grid(row=5, column=0, padx=5, pady=5)
        self.meeting_link_entry = tk.Entry(self.appointment_window, font=("Forum", 10))
        self.meeting_link_entry.grid(row=5, column=1, padx=5, pady=5)  

        tk.Button(self.appointment_window, text="Schedule", command=self.schedule_appointment_confirm, font=("Forum", 10)).grid(row=6, column=0, columnspan=2, pady=10)

    def schedule_appointment_confirm(self):
        """
        Confirm and process the appointment scheduling.
        Validates input data and adds the new appointment to the appointments.txt file.
        """
        username = self.username_entry.get()
        course_id = self.course_id_entry.get()
        appointment_date = self.appointment_date_entry.get()
        appointment_time = self.appointment_time_entry.get()
        meeting_link = self.meeting_link_entry.get()
        
        # Validate input data
        if not username or not course_id or not appointment_date or not appointment_time or not meeting_link:
            messagebox.showerror("Error", "All fields are required")
        elif len(course_id) != 4 or not course_id.isdigit():
            messagebox.showerror("Error", "Course ID must be 4 digits")
            return
        elif not is_date_valid(appointment_date):
            messagebox.showerror("Error", "Invalid date format. Please use DD/MM/YYYY format and ensure the date is within the five-year range starting from 2023.")
            return
        elif not is_time_valid(appointment_time):
            messagebox.showerror("Error", "Invalid time format. Please use HH:MM format.")
            return
        elif meeting_link == "":
            messagebox.showerror("Error", "Meeting link cannot be empty")
            return
        
        # Add new appointment to the file
        file_path = os.path.join(data_dir, 'appointments.txt')
        try:
            with open(file_path, "a", encoding="utf8") as f:
                f.write(f"{username},{course_id},{appointment_date},{appointment_time}, {meeting_link}\n")
            
            messagebox.showinfo("Success", "Appointment scheduled successfully")
            self.appointment_window.destroy()
            self.load_appointments()  # Reload the appointments to show the new entry
        except Exception as e:
            messagebox.showerror("Error", f"Failed to schedule appointment: {str(e)}")


    def unschedule_appointment(self):
        """
        Unschedule a selected appointment from the appointment list.
        Prompts for confirmation before removing the appointment.
        """
        selected_indices = self.appointment_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("No Selection", "Please select an appointment to unschedule.")
            return

        selected_index = selected_indices[0]
        appointment_info = self.appointment_listbox.get(selected_index)
        
        confirm = messagebox.askyesno("Confirm Unschedule", f"Are you sure you want to unschedule:\n\n{appointment_info}")
        if confirm:
            self.remove_appointment(selected_index)
            self.load_appointments()  # Reload the list
            messagebox.showinfo("Success", "Appointment has been unscheduled.")

    def remove_appointment(self, index):
        """
        Remove an appointment from the appointments.txt file.
        
        Args:
            index (int): The index of the appointment to remove.
        """
        file_path = os.path.join(data_dir, 'appointments.txt')
        try:
            with open(file_path, "r") as f:
                lines = f.readlines()
            
            del lines[index]

            with open(file_path, "w") as f:
                f.writelines(lines)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to unschedule appointment: {str(e)}", font=("Forum", 10))

    def back_to_menu(self):
        """Return to the receptionist menu."""
        self.hide()
        self.home_page.show_receptionist_menu()
