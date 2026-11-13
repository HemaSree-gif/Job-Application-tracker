
import sqlite3


def add_application():
    connection = sqlite3.connect("job_tracker.db")
    cursor = connection.cursor()

    print("\n===== ADD JOB APPLICATION =====")

    company = input("Enter Company Name: ")
    role = input("Enter Job Role: ")
    location = input("Enter Location: ")
    application_date = input("Enter Application Date (YYYY-MM-DD): ")
    status = input("Enter Status (Applied/Interview/Offer/Rejected): ")
    interview_date = input("Enter Interview Date (YYYY-MM-DD or NA): ")
    job_link = input("Enter Job Link: ")

    cursor.execute("""
        INSERT INTO applications
        (company_name, job_role, location, application_date,
         status, interview_date, job_link)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (company, role, location, application_date,
          status, interview_date, job_link))

    connection.commit()
    connection.close()

    print("\nJob application added successfully!")


def view_applications():
    connection = sqlite3.connect("job_tracker.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM applications")
    records = cursor.fetchall()

    print("\n===== ALL JOB APPLICATIONS =====")

    if records:
        for record in records:
            print("\nApplication ID:", record[0])
            print("Company:", record[1])
            print("Job Role:", record[2])
            print("Location:", record[3])
            print("Application Date:", record[4])
            print("Status:", record[5])
            print("Interview Date:", record[6])
            print("Job Link:", record[7])
            print("-------------------------------")
    else:
        print("No applications found.")

    connection.close()


def update_application():
    connection = sqlite3.connect("job_tracker.db")
    cursor = connection.cursor()

    cursor.execute("SELECT id, company_name, job_role FROM applications")
    records = cursor.fetchall()

    if not records:
        print("No applications available to update.")
        connection.close()
        return

    print("\n===== APPLICATIONS =====")

    for record in records:
        print("ID:", record[0], "| Company:", record[1], "| Role:", record[2])

    app_id = input("\nEnter Application ID to update: ")
    new_status = input("Enter New Status: ")

    cursor.execute(
        "UPDATE applications SET status = ? WHERE id = ?",
        (new_status, app_id)
    )

    if cursor.rowcount > 0:
        connection.commit()
        print("Application updated successfully!")
    else:
        print("Application ID not found!")

    connection.close()


def delete_application():
    connection = sqlite3.connect("job_tracker.db")
    cursor = connection.cursor()

    cursor.execute("SELECT id, company_name, job_role FROM applications")
    records = cursor.fetchall()

    if not records:
        print("No applications available to delete.")
        connection.close()
        return

    print("\n===== APPLICATIONS =====")

    for record in records:
        print("ID:", record[0], "| Company:", record[1], "| Role:", record[2])

    app_id = input("\nEnter Application ID to delete: ")

    cursor.execute(
        "DELETE FROM applications WHERE id = ?",
        (app_id,)
    )

    if cursor.rowcount > 0:
        connection.commit()
        print("Application deleted successfully!")
    else:
        print("Application ID not found!")

    connection.close()


def search_application():
    connection = sqlite3.connect("job_tracker.db")
    cursor = connection.cursor()

    keyword = input("\nEnter Company Name or Job Role to Search: ")

    cursor.execute("""
        SELECT * FROM applications
        WHERE company_name LIKE ? OR job_role LIKE ?
    """, ('%' + keyword + '%', '%' + keyword + '%'))

    records = cursor.fetchall()

    print("\n===== SEARCH RESULTS =====")

    if records:
        for record in records:
            print("\nApplication ID:", record[0])
            print("Company:", record[1])
            print("Job Role:", record[2])
            print("Location:", record[3])
            print("Application Date:", record[4])
            print("Status:", record[5])
            print("Interview Date:", record[6])
            print("Job Link:", record[7])
            print("-------------------------------")
    else:
        print("No matching applications found.")

    connection.close()


def show_dashboard():
    connection = sqlite3.connect("job_tracker.db")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM applications")
    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM applications
        WHERE LOWER(status) LIKE '%interview%'
    """)
    interviews = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM applications
        WHERE LOWER(status) LIKE '%offer%'
        OR LOWER(status) LIKE '%selected%'
    """)
    offers = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM applications
        WHERE LOWER(status) LIKE '%reject%'
    """)
    rejections = cursor.fetchone()[0]

    pending = total - interviews - offers - rejections

    print("\n========== CAREERTRACK DASHBOARD ==========")
    print("Total Applications:", total)
    print("Interviews Scheduled:", interviews)
    print("Offers Received:", offers)
    print("Rejected Applications:", rejections)
    print("Pending Applications:", pending)
    print("===========================================")

    connection.close()


def main():
    while True:
        print("\n========== CAREERTRACK SYSTEM ==========")
        print("1. Add Job Application")
        print("2. View All Applications")
        print("3. Update Application")
        print("4. Delete Application")
        print("5. Search Applications")
        print("6. View Dashboard")
        print("7. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_application()

        elif choice == "2":
            view_applications()

        elif choice == "3":
            update_application()

        elif choice == "4":
            delete_application()

        elif choice == "5":
            search_application()

        elif choice == "6":
            show_dashboard()

        elif choice == "7":
            print("\nThank you for using CareerTrack!")
            break

        else:
            print("Invalid choice! Please enter 1 to 7.")


if __name__ == "__main__":
    main()
