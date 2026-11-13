
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
from datetime import date

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "job_tracker.db")

STATUSES = [
    "Applied",
    "Shortlisted",
    "Interview",
    "Offer",
    "Rejected"
]


def connect_db():
    return sqlite3.connect(DB_NAME, timeout=10)


def create_table():
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT NOT NULL,
                job_role TEXT NOT NULL,
                location TEXT,
                application_date TEXT,
                status TEXT DEFAULT 'Applied',
                interview_date TEXT,
                job_link TEXT
            )
        """)
        conn.commit()
    finally:
        conn.close()


class CareerTrack:

    def __init__(self, root):
        self.root = root
        self.root.title("CareerTrack - Job Application Tracker")
        self.root.geometry("1250x750")
        self.root.minsize(1000, 600)
        self.root.configure(bg="#f4f6fb")

        self.setup_style()
        self.create_layout()
        self.show_dashboard()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="white",
            foreground="#222222",
            rowheight=35,
            fieldbackground="white",
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            background="#263b63",
            foreground="white",
            font=("Arial", 10, "bold"),
            padding=10
        )

        style.map(
            "Treeview",
            background=[("selected", "#dce8ff")],
            foreground=[("selected", "#172b4d")]
        )

    def create_layout(self):
        header = tk.Frame(self.root, bg="#172b4d", height=75)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="CAREERTRACK",
            font=("Arial", 23, "bold"),
            bg="#172b4d",
            fg="white"
        ).pack(side="left", padx=25)

        tk.Label(
            header,
            text="Smart Job Application Management System",
            font=("Arial", 11),
            bg="#172b4d",
            fg="#dce6f5"
        ).pack(side="right", padx=25)

        body = tk.Frame(self.root, bg="#f4f6fb")
        body.pack(fill="both", expand=True)

        sidebar = tk.Frame(body, bg="#263b63", width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        buttons = [
            ("Dashboard", self.show_dashboard),
            ("Add Application", self.add_application),
            ("All Applications", self.show_applications),
            ("Update Application", self.update_application),
            ("Delete Application", self.delete_application),
            ("Search Applications", self.search_applications),
            ("Exit", self.root.destroy)
        ]

        for label, command in buttons:
            tk.Button(
                sidebar,
                text=label,
                command=command,
                font=("Arial", 11, "bold"),
                bg="#263b63",
                fg="white",
                activebackground="#405d91",
                activeforeground="white",
                relief="flat",
                anchor="w",
                padx=20,
                pady=15,
                cursor="hand2"
            ).pack(fill="x")

        self.content = tk.Frame(body, bg="#f4f6fb")
        self.content.pack(side="right", fill="both", expand=True)

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def get_applications(self):
        conn = connect_db()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, company_name, job_role, location,
                       application_date, status, interview_date, job_link
                FROM applications
                ORDER BY id ASC
            """)
            return cursor.fetchall()
        finally:
            conn.close()

    def show_dashboard(self):
        self.clear_content()

        tk.Label(
            self.content,
            text="Dashboard",
            font=("Arial", 23, "bold"),
            bg="#f4f6fb",
            fg="#172b4d"
        ).pack(anchor="w", padx=30, pady=25)

        records = self.get_applications()

        stats = [
            ("Total Applications", len(records)),
            ("Interviews", sum(1 for r in records if r[5] == "Interview")),
            ("Offers", sum(1 for r in records if r[5] == "Offer")),
            ("Rejected", sum(1 for r in records if r[5] == "Rejected")),
            ("Pending", sum(1 for r in records if r[5] in ("Applied", "Shortlisted")))
        ]

        card_frame = tk.Frame(self.content, bg="#f4f6fb")
        card_frame.pack(fill="x", padx=20, pady=20)

        for title, value in stats:
            card = tk.Frame(card_frame, bg="white", padx=20, pady=25)
            card.pack(side="left", fill="both", expand=True, padx=8)

            tk.Label(
                card,
                text=str(value),
                font=("Arial", 25, "bold"),
                bg="white",
                fg="#263b63"
            ).pack()

            tk.Label(
                card,
                text=title,
                font=("Arial", 10, "bold"),
                bg="white",
                fg="#555555"
            ).pack(pady=8)

        tk.Label(
            self.content,
            text="Welcome to CareerTrack! Manage and monitor all your job applications in one place.",
            font=("Arial", 12),
            bg="#f4f6fb",
            fg="#444444",
            wraplength=850
        ).pack(anchor="w", padx=35, pady=25)

        tk.Button(
            self.content,
            text="View All Applications",
            command=self.show_applications,
            bg="#263b63",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10
        ).pack(anchor="w", padx=35)

    def show_applications(self, records=None):
        self.clear_content()

        tk.Label(
            self.content,
            text="All Job Applications",
            font=("Arial", 22, "bold"),
            bg="#f4f6fb",
            fg="#172b4d"
        ).pack(anchor="w", padx=25, pady=20)

        if records is None:
            records = self.get_applications()

        table_frame = tk.Frame(self.content, bg="white")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = (
            "ID", "Company", "Role", "Location",
            "Application Date", "Status", "Interview Date", "Job Link"
        )

        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        widths = {
            "ID": 55,
            "Company": 150,
            "Role": 160,
            "Location": 120,
            "Application Date": 130,
            "Status": 110,
            "Interview Date": 130,
            "Job Link": 230
        }

        for column in columns:
            tree.heading(column, text=column)
            tree.column(
                column,
                width=widths[column],
                minwidth=70,
                anchor="center",
                stretch=True
            )

        vertical_scroll = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=tree.yview
        )

        horizontal_scroll = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=tree.xview
        )

        tree.configure(
            yscrollcommand=vertical_scroll.set,
            xscrollcommand=horizontal_scroll.set
        )

        tree.grid(row=0, column=0, sticky="nsew")
        vertical_scroll.grid(row=0, column=1, sticky="ns")
        horizontal_scroll.grid(row=1, column=0, sticky="ew")

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        for record in records:
            tree.insert("", "end", values=record)

        tk.Label(
            self.content,
            text=f"Total records: {len(records)}",
            font=("Arial", 10, "bold"),
            bg="#f4f6fb",
            fg="#263b63"
        ).pack(anchor="w", padx=25, pady=10)

    def add_application(self):
        self.open_form("Add Job Application")

    def open_form(self, title, record=None):
        form = tk.Toplevel(self.root)
        form.title(title)
        form.geometry("500x700")
        form.configure(bg="white")
        form.resizable(False, False)
        form.transient(self.root)
        form.grab_set()

        tk.Label(
            form,
            text=title,
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#172b4d"
        ).pack(pady=18)

        fields = [
            ("Company Name", "company_name"),
            ("Job Role", "job_role"),
            ("Location", "location"),
            ("Application Date", "application_date"),
            ("Interview Date", "interview_date"),
            ("Job Link", "job_link")
        ]

        entries = {}

        for label, key in fields:
            tk.Label(
                form,
                text=label,
                font=("Arial", 10, "bold"),
                bg="white"
            ).pack(anchor="w", padx=35, pady=(6, 2))

            entry = tk.Entry(form, font=("Arial", 11), width=45)
            entry.pack(padx=35, pady=3, ipady=5)
            entries[key] = entry

        status_var = tk.StringVar(
            value=record[5] if record else "Applied"
        )

        tk.Label(
            form,
            text="Status",
            font=("Arial", 10, "bold"),
            bg="white"
        ).pack(anchor="w", padx=35, pady=(8, 2))

        status_box = ttk.Combobox(
            form,
            textvariable=status_var,
            values=STATUSES,
            state="readonly",
            width=42
        )
        status_box.pack(padx=35, pady=3, ipady=4)

        if record:
            values = {
                "company_name": record[1],
                "job_role": record[2],
                "location": record[3],
                "application_date": record[4],
                "interview_date": record[6],
                "job_link": record[7]
            }

            for key, value in values.items():
                entries[key].insert(0, value or "")
        else:
            entries["application_date"].insert(0, str(date.today()))

        def save():
            company = entries["company_name"].get().strip()
            role = entries["job_role"].get().strip()

            if not company or not role:
                messagebox.showwarning(
                    "Missing Details",
                    "Company Name and Job Role are required.",
                    parent=form
                )
                return

            values = (
                company,
                role,
                entries["location"].get().strip(),
                entries["application_date"].get().strip(),
                status_var.get(),
                entries["interview_date"].get().strip(),
                entries["job_link"].get().strip()
            )

            conn = None

            try:
                conn = connect_db()
                cursor = conn.cursor()

                if record:
                    cursor.execute("""
                        UPDATE applications
                        SET company_name=?, job_role=?, location=?,
                            application_date=?, status=?,
                            interview_date=?, job_link=?
                        WHERE id=?
                    """, values + (record[0],))

                    if cursor.rowcount == 0:
                        raise Exception("The selected application was not found.")

                else:
                    cursor.execute("""
                        INSERT INTO applications
                        (company_name, job_role, location,
                         application_date, status, interview_date, job_link)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, values)

                conn.commit()

                messagebox.showinfo(
                    "Success",
                    "Application saved successfully!",
                    parent=form
                )

                form.destroy()
                self.show_applications()

            except Exception as error:
                if conn:
                    conn.rollback()

                messagebox.showerror(
                    "Save Failed",
                    f"Could not save the application.\n\n{error}",
                    parent=form
                )

            finally:
                if conn:
                    conn.close()

        tk.Button(
            form,
            text="Save Application",
            command=save,
            bg="#263b63",
            fg="white",
            activebackground="#405d91",
            activeforeground="white",
            font=("Arial", 11, "bold"),
            padx=25,
            pady=12,
            cursor="hand2"
        ).pack(pady=25)

    def update_application(self):
        self.choose_application("Update Job Application")

    def delete_application(self):
        self.choose_application("Delete Job Application", deleting=True)

    def choose_application(self, title, deleting=False):
        records = self.get_applications()

        if not records:
            messagebox.showinfo(
                "Information",
                "No applications available."
            )
            return

        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("500x270")
        window.configure(bg="white")
        window.transient(self.root)
        window.grab_set()

        tk.Label(
            window,
            text=title,
            font=("Arial", 17, "bold"),
            bg="white",
            fg="#172b4d"
        ).pack(pady=20)

        choices = [
            f"{r[0]} - {r[1]} - {r[2]}"
            for r in records
        ]

        selected = tk.StringVar()

        combo = ttk.Combobox(
            window,
            values=choices,
            textvariable=selected,
            state="readonly",
            width=50
        )
        combo.pack(pady=10)
        combo.current(0)

        def proceed():
            index = combo.current()

            if index < 0:
                messagebox.showwarning(
                    "Select Application",
                    "Please select an application.",
                    parent=window
                )
                return

            record = records[index]
            window.destroy()

            if deleting:
                answer = messagebox.askyesno(
                    "Confirm Delete",
                    f"Delete application for {record[1]}?"
                )

                if answer:
                    conn = None
                    try:
                        conn = connect_db()
                        cursor = conn.cursor()
                        cursor.execute(
                            "DELETE FROM applications WHERE id=?",
                            (record[0],)
                        )
                        conn.commit()

                        messagebox.showinfo(
                            "Deleted",
                            "Application deleted successfully!"
                        )
                        self.show_applications()

                    except sqlite3.Error as error:
                        if conn:
                            conn.rollback()
                        messagebox.showerror("Delete Failed", str(error))

                    finally:
                        if conn:
                            conn.close()
            else:
                self.open_form("Update Job Application", record)

        tk.Button(
            window,
            text="Continue",
            command=proceed,
            bg="#263b63",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=25,
            pady=8
        ).pack(pady=15)

    def search_applications(self):
        self.clear_content()

        tk.Label(
            self.content,
            text="Search Applications",
            font=("Arial", 22, "bold"),
            bg="#f4f6fb",
            fg="#172b4d"
        ).pack(anchor="w", padx=25, pady=20)

        search_frame = tk.Frame(self.content, bg="#f4f6fb")
        search_frame.pack(fill="x", padx=25)

        search_entry = tk.Entry(
            search_frame,
            font=("Arial", 12),
            width=40
        )
        search_entry.pack(side="left", ipady=7)

        def search():
            keyword = search_entry.get().strip()

            conn = connect_db()
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, company_name, job_role, location,
                           application_date, status, interview_date, job_link
                    FROM applications
                    WHERE company_name LIKE ?
                       OR job_role LIKE ?
                       OR location LIKE ?
                       OR status LIKE ?
                    ORDER BY id ASC
                """, tuple(["%" + keyword + "%"] * 4))

                records = cursor.fetchall()
            finally:
                conn.close()

            self.show_applications(records)

        tk.Button(
            search_frame,
            text="Search",
            command=search,
            bg="#263b63",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8
        ).pack(side="left", padx=10)

        tk.Button(
            search_frame,
            text="Show All",
            command=self.show_applications,
            bg="#607da9",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8
        ).pack(side="left")


if __name__ == "__main__":
    create_table()
    root = tk.Tk()
    app = CareerTrack(root)
    root.mainloop()
