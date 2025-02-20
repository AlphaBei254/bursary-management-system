import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import datetime
import pandas as pd
import hashlib
import customtkinter as ctk

# Database setup
conn = sqlite3.connect('bursary.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL)''')

c.execute('''CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                second_name TEXT,
                email TEXT,
                gender TEXT,
                dob TEXT,
                sub_location TEXT,
                college TEXT,
                course TEXT,
                year_of_studies INTEGER,
                school_fees REAL,
                date_allocated TEXT,
                allocation_amount REAL)''')

conn.commit()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Main Application
class BursaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bidii Bursary Management System")
        self.root.geometry("800x600")
        self.create_login_panel()

    def create_login_panel(self):
        self.clear_frame()
        self.login_frame = ctk.CTkFrame(self.root)
        self.login_frame.pack(pady=50)

        ctk.CTkLabel(self.login_frame, text="Admin Login").grid(row=0, column=0, columnspan=2, pady=10)

        ctk.CTkLabel(self.login_frame, text="Username").grid(row=1, column=0, padx=10, pady=10)
        self.username_entry = ctk.CTkEntry(self.login_frame)
        self.username_entry.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(self.login_frame, text="Password").grid(row=2, column=0, padx=10, pady=10)
        self.password_entry = ctk.CTkEntry(self.login_frame, show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=10)

        button_frame = ctk.CTkFrame(self.login_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        ctk.CTkButton(button_frame, text="Login", command=self.login).grid(row=0, column=0, padx=10)
        ctk.CTkButton(button_frame, text="Create Account", command=self.create_account_panel).grid(row=0, column=1, padx=10)

    def create_account_panel(self):
        self.clear_frame()
        self.create_account_frame = ctk.CTkFrame(self.root)
        self.create_account_frame.pack(pady=50)

        ctk.CTkLabel(self.create_account_frame, text="Create Account").grid(row=0, column=0, columnspan=2, pady=10)

        ctk.CTkLabel(self.create_account_frame, text="Username").grid(row=1, column=0, padx=10, pady=10)
        self.new_username_entry = ctk.CTkEntry(self.create_account_frame)
        self.new_username_entry.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(self.create_account_frame, text="Password").grid(row=2, column=0, padx=10, pady=10)
        self.new_password_entry = ctk.CTkEntry(self.create_account_frame, show="*")
        self.new_password_entry.grid(row=2, column=1, padx=10, pady=10)

        button_frame = ctk.CTkFrame(self.create_account_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        ctk.CTkButton(button_frame, text="Create Account", command=self.create_account).grid(row=0, column=0, padx=10)
        ctk.CTkButton(button_frame, text="Back to Login", command=self.create_login_panel).grid(row=0, column=1, padx=10)

    def create_account(self):
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Username and Password cannot be empty")
            return
        hashed_password = hash_password(password)
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        messagebox.showinfo("Success", "Account created successfully")
        self.create_login_panel()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        hashed_password = hash_password(password)
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
        user = c.fetchone()
        if user:
            self.create_dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password")
    # The rest of the code remains unchanged

    def create_dashboard(self):
        self.clear_frame()
        self.dashboard_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.dashboard_frame.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(self.dashboard_frame, text="Admin Dashboard", font=("Arial", 24)).grid(row=0, column=0, columnspan=3, pady=20)

        # Centering the frame
        self.dashboard_frame.grid_rowconfigure(1, weight=1)
        self.dashboard_frame.grid_columnconfigure(0, weight=1)
        self.dashboard_frame.grid_columnconfigure(1, weight=1)
        self.dashboard_frame.grid_columnconfigure(2, weight=1)

        # Buttons Section
        buttons_frame = ctk.CTkFrame(self.dashboard_frame, corner_radius=10)
        buttons_frame.grid(row=1, column=0, columnspan=3, pady=10, padx=10)

        button_style = {"width": 200, "height": 40, "corner_radius": 10, "font": ("Arial", 14)}

        ctk.CTkButton(buttons_frame, text="Application Form", command=self.create_application_form, **button_style).grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkButton(buttons_frame, text="View Applications", command=self.view_applications, **button_style).grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkButton(buttons_frame, text="Export Data", command=self.export_data, **button_style).grid(row=0, column=2, padx=10, pady=10)
        ctk.CTkButton(buttons_frame, text="Logout", command=self.create_login_panel, **button_style).grid(row=0, column=3, padx=10, pady=10)

        # Statistics Section
        stats_frame = ctk.CTkFrame(self.dashboard_frame, corner_radius=10)
        ctk.CTkLabel(stats_frame, text="Statistics", font=("Arial", 18)).grid(row=0, column=0, pady=10)
        stats_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        total_applications = c.execute("SELECT COUNT(*) FROM applications").fetchone()[0]
        total_allocated = c.execute("SELECT SUM(allocation_amount) FROM applications").fetchone()[0] or 0

        ctk.CTkLabel(stats_frame, text=f"Total Applications: {total_applications}", font=("Arial", 14)).grid(row=1, column=0, pady=10)
        ctk.CTkLabel(stats_frame, text=f"Total Allocated Amount: Ksh {total_allocated}", font=("Arial", 14)).grid(row=2, column=0, pady=10)

        # Recent Applications Section
        recent_frame = ctk.CTkFrame(self.dashboard_frame, corner_radius=10)
        ctk.CTkLabel(recent_frame, text="Recent Applications", font=("Arial", 18)).grid(row=0, column=0, pady=10)
        recent_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        recent_applications = c.execute("SELECT first_name, second_name, date_allocated FROM applications ORDER BY date_allocated DESC LIMIT 5").fetchall()
        for idx, app in enumerate(recent_applications, start=1):
            ctk.CTkLabel(recent_frame, text=f"{app[0]} {app[1]} - {app[2]}", font=("Arial", 12)).grid(row=idx, column=0, pady=5)

        # Top Allocations Section
        top_allocations_frame = ctk.CTkFrame(self.dashboard_frame, corner_radius=10)
        top_allocations_frame.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(top_allocations_frame, text="Top Allocations", font=("Arial", 18)).grid(row=0, column=0, pady=10)

        top_allocations = c.execute("SELECT first_name, second_name, allocation_amount FROM applications ORDER BY allocation_amount DESC LIMIT 5").fetchall()
        for idx, alloc in enumerate(top_allocations, start=1):
            if alloc[2]:
                ctk.CTkLabel(top_allocations_frame, text=f"{alloc[0]} {alloc[1]} - Ksh {alloc[2]}", font=("Arial", 12)).grid(row=idx, column=0, pady=5)

        # Footer Section

        footer_frame = ctk.CTkFrame(self.dashboard_frame, corner_radius=10)
        footer_frame.grid(row=4, column=0, columnspan=3, pady=10, padx=10, sticky="ew")
        ctk.CTkLabel(footer_frame, text=f"Bidii Constituency", font=("Arial", 12)).pack(side="left", padx=10)
        current_year = datetime.datetime.now().year
        ctk.CTkLabel(footer_frame, text=f"Copyright © {current_year}", font=("Arial", 12)).pack(side="right", padx=10)


    def create_application_form(self, application=None):
        self.clear_frame()
        self.application_form_frame = ctk.CTkFrame(self.root)
        self.application_form_frame.pack(pady=20)

        # Student Section
        student_section = ctk.CTkFrame(self.application_form_frame)
        student_section.grid(row=0, column=0, columnspan=4, pady=10, padx=10, sticky="ew")

        ctk.CTkLabel(student_section, text="First Name").grid(row=1, column=0, padx=10, pady=10)
        self.first_name_entry = ctk.CTkEntry(student_section)
        self.first_name_entry.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(student_section, text="Second Name").grid(row=1, column=2, padx=10, pady=10)
        self.second_name_entry = ctk.CTkEntry(student_section)
        self.second_name_entry.grid(row=1, column=3, padx=10, pady=10)

        ctk.CTkLabel(student_section, text="Email").grid(row=2, column=0, padx=10, pady=10)
        self.email_entry = ctk.CTkEntry(student_section)
        self.email_entry.grid(row=2, column=1, padx=10, pady=10)

        ctk.CTkLabel(student_section, text="Gender").grid(row=2, column=2, padx=10, pady=10)
        self.gender_entry = ctk.CTkComboBox(student_section, values=["Male", "Female", "Other"])
        self.gender_entry.grid(row=2, column=3, padx=10, pady=10)

        ctk.CTkLabel(student_section, text="Date of Birth").grid(row=3, column=0, padx=10, pady=10)
        self.dob_entry = ctk.CTkEntry(student_section)
        self.dob_entry.grid(row=3, column=1, padx=10, pady=10)
        #self.dob_entry.insert(0, "YYYY-MM-DD")

        ctk.CTkLabel(student_section, text="Sub-location").grid(row=3, column=2, padx=10, pady=10)
        self.sub_location_entry = ctk.CTkEntry(student_section)
        self.sub_location_entry.grid(row=3, column=3, padx=10, pady=10)

        # School Section
        school_section = ctk.CTkFrame(self.application_form_frame)
        school_section.grid(row=4, column=0, columnspan=4, pady=10, padx=10, sticky="ew")

        ctk.CTkLabel(school_section, text="College/University").grid(row=5, column=0, padx=10, pady=10)
        self.college_entry = ctk.CTkEntry(school_section)
        self.college_entry.grid(row=5, column=1, padx=10, pady=10)

        ctk.CTkLabel(school_section, text="Course").grid(row=5, column=2, padx=10, pady=10)
        self.course_entry = ctk.CTkEntry(school_section)
        self.course_entry.grid(row=5, column=3, padx=10, pady=10)

        ctk.CTkLabel(school_section, text="Year of Studies").grid(row=6, column=0, padx=10, pady=10)
        self.year_of_studies_entry = ctk.CTkEntry(school_section)
        self.year_of_studies_entry.grid(row=6, column=1, padx=10, pady=10)

        ctk.CTkLabel(school_section, text="School Fees Amount").grid(row=6, column=2, padx=10, pady=10)
        self.school_fees_entry = ctk.CTkEntry(school_section)
        self.school_fees_entry.grid(row=6, column=3, padx=10, pady=10)

        # Allocation Section
        allocation_section = ctk.CTkFrame(self.application_form_frame)
        allocation_section.grid(row=7, column=0, columnspan=4, pady=10, padx=10, sticky="ew")

        ctk.CTkLabel(allocation_section, text="Allocation Amount (Ksh)").grid(row=8, column=0, padx=10, pady=10)
        self.allocation_amount_entry = ctk.CTkEntry(allocation_section)
        self.allocation_amount_entry.grid(row=8, column=1, padx=10, pady=10)

        if application:
            self.first_name_entry.insert(0, application[1])
            self.second_name_entry.insert(0, application[2])
            self.email_entry.insert(0, application[3])
            self.gender_entry.set(application[4])
            self.dob_entry.insert(0, application[5])
            self.college_entry.insert(0, application[7])
            self.course_entry.insert(0, application[8])
            self.year_of_studies_entry.insert(0, application[9])
            self.school_fees_entry.insert(0, application[10])
            self.allocation_amount_entry.insert(0, application[12])
            ctk.CTkButton(self.application_form_frame, text="Update", command=lambda: self.update_application(application[0])).grid(row=9, column=0, columnspan=4, pady=10)
        else:
            ctk.CTkButton(self.application_form_frame, text="Submit", command=self.submit_application).grid(row=9, column=0, columnspan=4, pady=10)

        ctk.CTkButton(self.application_form_frame, text="Back to Dashboard", command=self.create_dashboard).grid(row=10, column=0, columnspan=4, pady=10)

    def submit_application(self):
        first_name = self.first_name_entry.get()
        second_name = self.second_name_entry.get()
        email = self.email_entry.get()
        gender = self.gender_entry.get()
        dob = self.dob_entry.get()
        sub_location = self.sub_location_entry.get()
        college = self.college_entry.get()
        course = self.course_entry.get()
        year_of_studies = self.year_of_studies_entry.get()
        school_fees = self.school_fees_entry.get()
        allocation_amount = self.allocation_amount_entry.get()
        date_allocated = datetime.datetime.now().strftime("%Y-%m-%d")

        if not all([first_name, second_name, email, gender, dob, sub_location, college, course, year_of_studies, school_fees]):
            messagebox.showerror("Error", "All fields must be filled")
            return

        c.execute('''INSERT INTO applications (first_name, second_name, email, gender, dob, sub_location, college, course, year_of_studies, school_fees, date_allocated, allocation_amount)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (first_name, second_name, email, gender, dob, sub_location, college, course, year_of_studies, school_fees, date_allocated, allocation_amount))
        conn.commit()
        messagebox.showinfo("Success", "Application submitted successfully")
        self.create_dashboard()

    def view_applications(self):
        self.clear_frame()
        self.view_applications_frame = tk.Frame(self.root)
        self.view_applications_frame.pack(pady=20)

        self.tree = ttk.Treeview(self.view_applications_frame, columns=("ID", "First Name", "Second Name", "Email", "Gender", "DOB", "Sub-location", "College", "Course", "Year of Studies", "School Fees", "Date Allocated", "Allocation Amount"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("First Name", text="First Name")
        self.tree.heading("Second Name", text="Second Name")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Gender", text="Gender")
        self.tree.heading("DOB", text="DOB")
        self.tree.heading("Sub-location", text="Sub-location")
        self.tree.heading("College", text="College")
        self.tree.heading("Course", text="Course")
        self.tree.heading("Year of Studies", text="Year of Studies")
        self.tree.heading("School Fees", text="School Fees")
        self.tree.heading("Date Allocated", text="Date Allocated")
        self.tree.heading("Allocation Amount", text="Allocation Amount")
        self.tree.pack()

        c.execute("SELECT * FROM applications")
        rows = c.fetchall()
        for row in rows:
            self.tree.insert("", tk.END, values=row)

        self.tree.bind("<Double-1>", self.on_application_select)
        button_frame = tk.Frame(self.view_applications_frame)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Delete Selected", command=self.confirm_delete).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Back to Dashboard", command=self.create_dashboard).grid(row=0, column=1, padx=10)

    def confirm_delete(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showerror("Error", "No applications selected")
            return

        response = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected application(s)?")
        if response:
            for selected_item in selected_items:
                if self.tree.exists(selected_item):
                    application_id = self.tree.item(selected_item, "values")[0]
                    self.delete_application(application_id)
            self.view_applications()

    def on_application_select(self, event):
        selected_item = self.tree.selection()[0]
        application = self.tree.item(selected_item, "values")
        self.create_application_form(application)

    def update_application(self, application_id):
        first_name = self.first_name_entry.get()
        second_name = self.second_name_entry.get()
        email = self.email_entry.get()
        gender = self.gender_entry.get()
        dob = self.dob_entry.get()
        sub_location = self.sub_location_entry.get()
        college = self.college_entry.get()
        course = self.course_entry.get()
        year_of_studies = self.year_of_studies_entry.get()
        school_fees = self.school_fees_entry.get()
        allocation_amount = self.allocation_amount_entry.get()

        c.execute('''UPDATE applications SET first_name=?, second_name=?, email=?, gender=?, dob=?, sub_location=?, college=?, course=?, year_of_studies=?, school_fees=?, allocation_amount=? WHERE id=?''',
                  (first_name, second_name, email, gender, dob, sub_location, college, course, year_of_studies, school_fees, allocation_amount, application_id))
        conn.commit()
        messagebox.showinfo("Success", "Application updated successfully")
        self.create_dashboard()

    def delete_application(self, application_id):
        c.execute("DELETE FROM applications WHERE id=?", (application_id,))
        conn.commit()
        messagebox.showinfo("Success", "Application deleted successfully")
        self.view_applications()

    def export_data(self):
        self.clear_frame()
        self.export_data_frame = tk.Frame(self.root)
        self.export_data_frame.pack(pady=20)

        tk.Button(self.export_data_frame, text="Export to Excel", command=self.export_to_excel).pack(pady=10)
        tk.Button(self.export_data_frame, text="Export to JSON", command=self.export_to_json).pack(pady=10)
        tk.Button(self.export_data_frame, text="Export to CSV", command=self.export_to_csv).pack(pady=10)
        tk.Button(self.export_data_frame, text="Back to Dashboard", command=self.create_dashboard).pack(pady=10)

    def export_to_excel(self):
        c.execute("SELECT * FROM applications")
        rows = c.fetchall()
        df = pd.DataFrame(rows, columns=["ID", "First Name", "Second Name", "Email", "Gender", "DOB", "Sub-location", "College", "Course", "Year of Studies", "School Fees", "Date Allocated", "Allocation Amount"])
        df.to_excel("applications.xlsx", index=False)
        messagebox.showinfo("Success", "Data exported to applications.xlsx")

    def export_to_json(self):
        c.execute("SELECT * FROM applications")
        rows = c.fetchall()
        df = pd.DataFrame(rows, columns=["ID", "First Name", "Second Name", "Email", "Gender", "DOB", "Sub-location", "College", "Course", "Year of Studies", "School Fees", "Date Allocated", "Allocation Amount"])
        df.to_json("applications.json", orient="records")
        messagebox.showinfo("Success", "Data exported to applications.json")

    def export_to_csv(self):
        c.execute("SELECT * FROM applications")
        rows = c.fetchall()
        df = pd.DataFrame(rows, columns=["ID", "First Name", "Second Name", "Email", "Gender", "DOB", "Sub-location", "College", "Course", "Year of Studies", "School Fees", "Date Allocated", "Allocation Amount"])
        df.to_csv("applications.csv", index=False)
        messagebox.showinfo("Success", "Data exported to applications.csv")

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BursaryApp(root)
    root.mainloop()